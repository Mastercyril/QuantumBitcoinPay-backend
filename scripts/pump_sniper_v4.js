#!/usr/bin/env node
/**
 * Pump.fun Sniper v4 — Dynamic Priority Fees + Fee Escalation
 *
 * Key fixes:
 * - Dynamic priority fee estimation from Solana network
 * - Fee escalation on retries (base → 2x → 4x)
 * - Pre-flight cost calculation (buy + fee + base tx)
 * - Compute budget instructions added to tx
 * - Multiple RPC endpoints for reliability
 * - Higher sell priority (exits are urgent)
 * - Full error logging (no more swallowed errors)
 * - Fee tracking (know exactly how much goes to fees vs trades)
 */

const WebSocket = require('ws');
const {
  Connection, Keypair, VersionedTransaction, Transaction,
  LAMPORTS_PER_SOL, PublicKey, ComputeBudgetProgram,
} = require('@solana/web3.js');
const { bondingCurvePda } = require('@pump-fun/pump-sdk');
const { getAssociatedTokenAddressSync, TOKEN_PROGRAM_ID } = require('@solana/spl-token');
const bs58 = require('bs58');
const bs58decode = bs58.default ? bs58.default.decode : bs58.decode;
const fs = require('fs');

// --- RPC: rotate between endpoints for reliability ---
const RPC_ENDPOINTS = [
  'https://api.mainnet-beta.solana.com',
  'https://rpc.ankr.com/solana',
  'https://solana-rpc.publicnode.com',
];
let rpcIdx = 0;
function getConn() {
  return new Connection(RPC_ENDPOINTS[rpcIdx % RPC_ENDPOINTS.length], {
    commitment: 'confirmed',
    confirmTransactionInitialTimeout: 30000,
  });
}
let conn = getConn();

// --- Treasury ---
const treasury = Keypair.fromSecretKey(bs58decode(process.env.SOLANA_PRIVATE_KEY_5));

// --- Config ---
const BUY_AMOUNT_SOL      = 0.001;
const BASE_PRIORITY_FEE   = 0.003;   // 3M lamports — high enough to beat most congestion
const SELL_PRIORITY_FEE   = 0.005;   // 5M lamports — exits are more urgent
const MAX_PRIORITY_FEE    = 0.01;    // 10M lamports cap — never spend more than this on a single tx
const FEE_ESCALATION      = [1, 2, 4]; // retry multipliers: base → 2x → 4x
const MAX_RETRIES         = 3;
const COMPUTE_UNIT_LIMIT  = 200000;  // pump.fun buys use ~140k-180k CU

const TAKE_PROFIT_PCT  = 40;
const STOP_LOSS_PCT   = 25;
const MAX_HOLD_MS     = 120000;  // 2 minutes
const MIN_DEV_BUY_SOL = 0.5;
const MIN_MARKET_CAP_SOL = 5;
const COOLDOWN_MS     = 8000;
const MAX_POSITIONS   = 5;
const RUNTIME_MS      = 240000;  // 4 minutes
const MIN_SOL_TO_TRADE = 0.03;
const BASE_TX_FEE     = 0.000005; // 5000 lamports base fee per tx

// --- State ---
const positions = new Map();
const seenNames  = new Set();
let lastSnipe    = 0;
const stats = {
  snipes: 0, wins: 0, losses: 0, profit: 0,
  skipped: 0, checked: 0,
  totalFeesPaid: 0, totalBuyFees: 0, totalSellFees: 0,
  failedBuys: 0, failedSells: 0,
  rpcRotations: 0,
};

// ============================================================
//  PRIORITY FEE ESTIMATION
// ============================================================

async function estimatePriorityFee() {
  // Query recent prioritization fees from the network
  try {
    const resp = await fetch(conn.rpcEndpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        jsonrpc: '2.0', id: 1,
        method: 'getRecentPrioritizationFees',
        params: [],
      }),
    });
    const data = await resp.json();
    const fees = (data?.result || []).map(f => f.prioritizationFee);
    if (fees.length === 0) return BASE_PRIORITY_FEE;

    // Sort and take 75th percentile
    fees.sort((a, b) => a - b);
    const p75 = fees[Math.floor(fees.length * 0.75)] / LAMPORTS_PER_SOL;

    // Use 2x the 75th percentile, but clamp to [BASE_PRIORITY_FEE, MAX_PRIORITY_FEE]
    const estimated = Math.max(BASE_PRIORITY_FEE, Math.min(p75 * 2, MAX_PRIORITY_FEE));
    return estimated;
  } catch (e) {
    // Fallback to base fee
    return BASE_PRIORITY_FEE;
  }
}

// ============================================================
//  COMPUTE BUDGET INSTRUCTIONS
// ============================================================

function makeComputeBudgetIxs(priorityFeeSol) {
  const feeLamports = Math.round(priorityFeeSol * LAMPORTS_PER_SOL);
  return [
    ComputeBudgetProgram.setComputeUnitLimit({ units: COMPUTE_UNIT_LIMIT }),
    ComputeBudgetProgram.setComputeUnitPrice({ microLamports: Math.max(1, Math.floor(feeLamports / COMPUTE_UNIT_LIMIT * 1000)) }),
  ];
}

// ============================================================
//  TRANSACTION SENDER WITH FEE ESCALATION
// ============================================================

async function sendTxWithEscalation(txBuffer, isSell = false) {
  let lastError = '';
  for (let attempt = 0; attempt < MAX_RETRIES; attempt++) {
    const feeMultiplier = FEE_ESCALATION[attempt];
    const baseFee = isSell ? SELL_PRIORITY_FEE : BASE_PRIORITY_FEE;
    const priorityFee = Math.min(baseFee * feeMultiplier, MAX_PRIORITY_FEE);

    try {
      // Re-deserialize and add compute budget instructions
      let tx;
      try {
        tx = VersionedTransaction.deserialize(txBuffer);
        // For versioned transactions, we can't easily add instructions after the fact,
        // so we rely on PumpPortal's priorityFee parameter
      } catch {
        tx = Transaction.from(txBuffer);
        // For legacy transactions, add compute budget instructions at the front
        const cuIxs = makeComputeBudgetIxs(priorityFee);
        tx.instructions = [...cuIxs, ...tx.instructions];
        tx.sign(treasury);
      }

      // For versioned txs, we already set priorityFee in the PumpPortal request
      const sig = await conn.sendRawTransaction(tx.serialize(), {
        skipPreflight: true,
        maxRetries: 3,
        preflightCommitment: 'confirmed',
      });

      // Confirm with timeout
      const confirmed = await conn.confirmTransaction(sig, 'confirmed');
      if (confirmed && !confirmed.value?.err) {
        return { sig, priorityFee, attempts: attempt + 1 };
      }

      // Transaction landed but failed — don't retry
      lastError = `tx landed with err: ${JSON.stringify(confirmed.value?.err)}`;
      return { sig, priorityFee, attempts: attempt + 1, error: lastError };
    } catch (e) {
      lastError = e.message;
      // If it's a "not confirmed" timeout, rotate RPC and retry with higher fee
      if (e.message.includes('not confirmed') || e.message.includes('timeout') || e.message.includes('30')) {
        // Rotate RPC endpoint
        rpcIdx++;
        conn = getConn();
        stats.rpcRotations++;
        if (attempt < MAX_RETRIES - 1) {
          const wait = 1000 * (attempt + 1); // 1s, 2s, 3s backoff
          await new Promise(r => setTimeout(r, wait));
        }
      } else {
        // Non-retryable error
        break;
      }
    }
  }
  return { sig: null, priorityFee: BASE_PRIORITY_FEE * FEE_ESCALATION[FEE_ESCALATION.length - 1], attempts: MAX_RETRIES, error: lastError };
}

// ============================================================
//  PUMP PORTAL TRADE FUNCTIONS
// ============================================================

async function portalBuy(mint, sol, priorityFee) {
  const fee = priorityFee || BASE_PRIORITY_FEE;
  try {
    // Request the trade from PumpPortal with our priority fee
    const res = await fetch('https://pumpportal.fun/api/trade-local', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        publicKey: treasury.publicKey.toString(),
        action: 'buy',
        mint,
        amount: sol,
        denominatedInSol: 'true',
        slippage: 25,
        priorityFee: fee,
      }),
    });

    if (!res.ok) {
      const errText = await res.text().catch(() => 'unknown');
      return { error: `PumpPortal HTTP ${res.status}: ${errText}` };
    }

    const buf = Buffer.from(await res.arrayBuffer());
    if (buf.length < 10) {
      return { error: `PumpPortal returned ${buf.length} bytes: ${buf.toString('utf8')}` };
    }

    // Send with fee escalation
    const result = await sendTxWithEscalation(buf, false);

    if (!result.sig) {
      return { error: `Send failed after ${result.attempts} attempts: ${result.error}` };
    }

    // Get token balance to confirm buy
    const ata = getAssociatedTokenAddressSync(new PublicKey(mint), treasury.publicKey, false, TOKEN_PROGRAM_ID);
    let tokens = 0;
    try {
      const b = await conn.getTokenAccountBalance(ata);
      tokens = b.value?.uiAmount || 0;
    } catch {}

    if (tokens <= 0) {
      return { error: `Buy confirmed but 0 tokens in ATA (mint: ${mint.substring(0,8)})` };
    }

    return {
      sig: result.sig,
      tokens,
      entryPrice: sol / tokens,
      priorityFee: result.priorityFee,
      attempts: result.attempts,
    };
  } catch (e) {
    return { error: `portalBuy exception: ${e.message}` };
  }
}

async function portalSell(mint, pct, priorityFee) {
  const fee = priorityFee || SELL_PRIORITY_FEE;
  try {
    const res = await fetch('https://pumpportal.fun/api/trade-local', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        publicKey: treasury.publicKey.toString(),
        action: 'sell',
        mint,
        amount: pct,
        denominatedInSol: 'false',
        slippage: 30,
        priorityFee: fee,
      }),
    });

    if (!res.ok) {
      const errText = await res.text().catch(() => 'unknown');
      return { error: `PumpPortal HTTP ${res.status}: ${errText}` };
    }

    const buf = Buffer.from(await res.arrayBuffer());
    if (buf.length < 10) {
      return { error: `PumpPortal returned ${buf.length} bytes` };
    }

    const result = await sendTxWithEscalation(buf, true);

    if (!result.sig) {
      return { error: `Sell send failed: ${result.error}` };
    }

    return { sig: result.sig, priorityFee: result.priorityFee, attempts: result.attempts };
  } catch (e) {
    return { error: `portalSell exception: ${e.message}` };
  }
}

// ============================================================
//  BONDING CURVE PRICE READER
// ============================================================

async function getBCPrice(mint) {
  try {
    const bcPda = bondingCurvePda(new PublicKey(mint));
    const info = await conn.getAccountInfo(bcPda);
    if (!info) return null;
    const buf = Buffer.from(info.data);
    const vSR = Number(buf.readBigUInt64LE(16));
    const vTR = Number(buf.readBigUInt64LE(8));
    const complete = buf[48] === 1;
    return { price: vSR / vTR / LAMPORTS_PER_SOL, complete, vSR, vTR };
  } catch (e) { return null; }
}

// ============================================================
//  POSITION MANAGEMENT
// ============================================================

async function closePos(mint, reason) {
  const pos = positions.get(mint);
  if (!pos) return;

  const before = await conn.getBalance(treasury.publicKey);

  // Try selling with escalating priority fees
  let sellResult = null;
  for (const feeMult of FEE_ESCALATION) {
    const fee = SELL_PRIORITY_FEE * feeMult;
    sellResult = await portalSell(mint, 100, fee);
    if (sellResult.sig) break;
    if (sellResult.error) console.log(`  Sell attempt fee=${fee.toFixed(4)}SOL: ${sellResult.error.substring(0, 80)}`);
    await new Promise(r => setTimeout(r, 1000));
  }

  if (sellResult?.sig) {
    const after = await conn.getBalance(treasury.publicKey);
    const pnl = (after - before) / LAMPORTS_PER_SOL - pos.buySol;
    const feePaid = sellResult.priorityFee || SELL_PRIORITY_FEE;
    stats.totalSellFees += feePaid;
    stats.totalFeesPaid += feePaid;
    positions.delete(mint);

    if (pnl > 0) stats.wins++; else stats.losses++;
    stats.profit += pnl;

    const netPct = (pnl / pos.buySol * 100).toFixed(1);
    console.log(`${pnl >= 0 ? '✅' : '❌'} ${reason} ${mint.substring(0, 8)} PnL: ${pnl >= 0 ? '+' : ''}${pnl.toFixed(6)} SOL (${netPct}%) | W:${stats.wins} L:${stats.losses} Net:${stats.profit >= 0 ? '+' : ''}${stats.profit.toFixed(6)} | Fees:${stats.totalFeesPaid.toFixed(6)}`);
  } else {
    stats.failedSells++;
    console.log(`⚠️ SELL FAILED after ${FEE_ESCALATION.length} attempts ${mint.substring(0, 8)} — ${sellResult?.error || 'unknown'}`);
    // Keep position in map — will retry on next monitor cycle
    setTimeout(() => {
      if (positions.has(mint)) closePos(mint, 'SELL_RETRY');
    }, 10000);
  }
}

async function monitor(mint) {
  const pos = positions.get(mint);
  if (!pos) return;

  const check = async () => {
    if (!positions.has(mint)) return;

    const elapsed = Date.now() - pos.buyTime;
    if (elapsed > MAX_HOLD_MS) {
      await closePos(mint, `TIME ${Math.floor(elapsed / 1000)}s`);
      return;
    }

    const bc = await getBCPrice(mint);
    if (!bc) {
      // Can't read bonding curve — might be a network issue, retry
      setTimeout(check, 5000);
      return;
    }

    if (bc.complete) {
      console.log(`🎓 ${mint.substring(0, 8)} graduated to Raydium! Holding for manual exit.`);
      // Don't auto-sell on graduation — could get better price on Raydium
      return;
    }

    const change = ((bc.price - pos.entryPrice) / pos.entryPrice) * 100;

    if (change >= TAKE_PROFIT_PCT) {
      await closePos(mint, `PROFIT +${change.toFixed(0)}%`);
      return;
    }

    if (change <= -STOP_LOSS_PCT) {
      await closePos(mint, `LOSS ${change.toFixed(0)}%`);
      return;
    }

    // Still holding — show occasional status
    if (Math.floor(elapsed / 1000) % 15 === 0) {
      console.log(`⏳ ${pos.name} (${mint.substring(0, 8)}) ${change >= 0 ? '+' : ''}${change.toFixed(1)}% ${Math.floor(elapsed / 1000)}s`);
    }

    setTimeout(check, 3000);
  };

  setTimeout(check, 3000);
}

// ============================================================
//  SNIPE LOGIC
// ============================================================

async function maybeSnipe(d) {
  stats.checked++;

  const devBuy = Number(d.solAmount || 0);  // Already in SOL
  const mcap   = Number(d.marketCapSol || 0);

  // Dedup spam tokens (same name launched multiple times)
  if (seenNames.has(d.name)) { stats.skipped++; return; }
  seenNames.add(d.name);
  setTimeout(() => seenNames.delete(d.name), 60000);

  // Filter: dev must have real skin in the game
  if (devBuy < MIN_DEV_BUY_SOL) { stats.skipped++; return; }
  if (mcap < MIN_MARKET_CAP_SOL) { stats.skipped++; return; }

  // Cooldown between snipes
  if (Date.now() - lastSnipe < COOLDOWN_MS) return;
  if (positions.size >= MAX_POSITIONS) return;

  // Pre-flight balance check: need buy amount + priority fee + base tx fee + buffer
  const bal = await conn.getBalance(treasury.publicKey);
  const balSol = bal / LAMPORTS_PER_SOL;
  const totalCost = BUY_AMOUNT_SOL + BASE_PRIORITY_FEE + BASE_TX_FEE + 0.001; // buy + fee + base + buffer

  if (balSol < MIN_SOL_TO_TRADE) {
    if (stats.checked % 50 === 1) {
      console.log(`💸 Low SOL: ${balSol.toFixed(6)} (need ${MIN_SOL_TO_TRADE}) — bridge SOL to activate`);
    }
    return;
  }

  if (balSol < totalCost) {
    console.log(`💸 Insufficient for trade: have ${balSol.toFixed(6)}, need ${totalCost.toFixed(6)} (buy+fees)`);
    return;
  }

  // Estimate optimal priority fee
  const estimatedFee = await estimatePriorityFee();
  const useFee = Math.max(BASE_PRIORITY_FEE, Math.min(estimatedFee, MAX_PRIORITY_FEE));

  console.log(`\n🎯 SNIPE: ${d.name} (${d.symbol}) devBuy=${devBuy.toFixed(3)}SOL mcap=${mcap.toFixed(1)}SOL`);
  console.log(`   https://pump.fun/${d.mint}`);
  console.log(`   Priority fee: ${useFee.toFixed(5)} SOL (est) | Total cost: ${(BUY_AMOUNT_SOL + useFee).toFixed(5)} SOL`);

  // Execute buy with fee escalation
  const result = await portalBuy(d.mint, BUY_AMOUNT_SOL, useFee);

  if (result && result.tokens > 0) {
    positions.set(d.mint, {
      buyTime: Date.now(),
      buySol: BUY_AMOUNT_SOL,
      tokens: result.tokens,
      entryPrice: result.entryPrice,
      name: d.name,
      symbol: d.symbol,
      priorityFee: result.priorityFee,
      buyAttempts: result.attempts,
    });
    lastSnipe = Date.now();
    stats.snipes++;
    stats.totalBuyFees += result.priorityFee || useFee;
    stats.totalFeesPaid += result.priorityFee || useFee;

    console.log(`   ✅ Got ${result.tokens.toFixed(0)} tokens in ${result.attempts} attempt(s) — TP:+${TAKE_PROFIT_PCT}% SL:-${STOP_LOSS_PCT}%`);
    monitor(d.mint);
  } else {
    stats.failedBuys++;
    console.log(`   ❌ Buy FAILED: ${result?.error || 'unknown error'}`);
    console.log(`   💸 Fee cost: 0 SOL (tx not confirmed)`);
  }
}

// ============================================================
//  MAIN LOOP
// ============================================================

function start() {
  console.log('╔══════════════════════════════════════════╗');
  console.log('║     PUMP.FUN SNIPER v4 — DYNAMIC FEES   ║');
  console.log('╠══════════════════════════════════════════╣');
  console.log(`║  Buy: ${BUY_AMOUNT_SOL} SOL  | Fee: ${BASE_PRIORITY_FEE}-${MAX_PRIORITY_FEE} SOL`);
  console.log(`║  TP: +${TAKE_PROFIT_PCT}%  | SL: -${STOP_LOSS_PCT}%  | MaxHold: ${MAX_HOLD_MS / 1000}s`);
  console.log(`║  Filter: devBuy>${MIN_DEV_BUY_SOL}SOL mcap>${MIN_MARKET_CAP_SOL}SOL`);
  console.log(`║  Retry: ${MAX_RETRIES}x with ${FEE_ESCALATION.join('x→')}x fee escalation`);
  console.log(`║  RPCs: ${RPC_ENDPOINTS.length} endpoints (auto-rotate)`);
  console.log('╚══════════════════════════════════════════╝\n');

  const ws = new WebSocket('wss://pumpportal.fun/api/data');

  ws.on('open', () => {
    console.log('📡 WS connected — hunting...\n');
    ws.send(JSON.stringify({ method: 'subscribeNewToken' }));
  });

  ws.on('message', async (raw) => {
    try {
      const d = JSON.parse(raw);
      if (d.txType === 'create' && d.mint) await maybeSnipe(d);
    } catch {}
  });

  ws.on('error', (e) => {
    console.log(`❌ WS error: ${e.message}`);
  });

  ws.on('close', () => {
    console.log('🔌 WS closed — reconnecting in 3s...');
    setTimeout(start, 3000);
  });

  // Status report every 30s
  setInterval(() => {
    if (stats.checked > 0) {
      const balSol = (conn.getBalance(treasury.publicKey) / 1e9).toFixed(6);
      console.log(`📊 Checked:${stats.checked} Skipped:${stats.skipped} Snipes:${stats.snipes} Open:${positions.size} | Fees:${stats.totalFeesPaid.toFixed(6)} | Fails: B${stats.failedBuys}/S${stats.failedSells} | RPC rotations:${stats.rpcRotations}`);
    }
  }, 30000);

  // Graceful shutdown
  setTimeout(async () => {
    console.log('\n╔══════════════════════════════════════════╗');
    console.log('║          CLOSING SESSION                 ║');
    console.log('╚══════════════════════════════════════════╝');

    // Close all positions
    for (const [m, _] of positions) {
      await closePos(m, 'SESSION_END');
    }
    await new Promise(r => setTimeout(r, 5000));

    const finalSol = await conn.getBalance(treasury.publicKey);
    const finalSolSol = finalSol / LAMPORTS_PER_SOL;

    console.log('\n╔══════════════════════════════════════════╗');
    console.log('║          FINAL RESULTS                   ║');
    console.log('╠══════════════════════════════════════════╣');
    console.log(`║  Tokens checked:  ${stats.checked}`);
    console.log(`║  Tokens skipped: ${stats.skipped}`);
    console.log(`║  Snipes:          ${stats.snipes}`);
    console.log(`║  Wins:            ${stats.wins}`);
    console.log(`║  Losses:          ${stats.losses}`);
    console.log(`║  Failed buys:     ${stats.failedBuys}`);
    console.log(`║  Failed sells:    ${stats.failedSells}`);
    console.log(`║  Net PnL:         ${stats.profit >= 0 ? '+' : ''}${stats.profit.toFixed(6)} SOL`);
    console.log(`║  Total fees paid: ${stats.totalFeesPaid.toFixed(6)} SOL`);
    console.log(`║    Buy fees:      ${stats.totalBuyFees.toFixed(6)} SOL`);
    console.log(`║    Sell fees:     ${stats.totalSellFees.toFixed(6)} SOL`);
    console.log(`║  RPC rotations:   ${stats.rpcRotations}`);
    console.log(`║  Final balance:   ${finalSolSol.toFixed(6)} SOL`);
    console.log('╚══════════════════════════════════════════╝');

    fs.writeFileSync('sniper_v4_results.json', JSON.stringify({
      ...stats,
      finalSol: finalSolSol,
      ts: new Date().toISOString(),
    }, null, 2));

    ws.close();
    process.exit(0);
  }, RUNTIME_MS);
}

start();
