const { Connection, PublicKey, Keypair, Transaction, SystemProgram, TransactionInstruction } = require('@solana/web3.js');
const crypto = require('crypto');
const bs58 = require('bs58');
const bs58decode = bs58.default.decode;

// === CONSTANTS ===
const PUMP_PROGRAM = new PublicKey('6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P');
const PUMP_FEE_PROGRAM = new PublicKey('pfeeUxB6jkeY1Hxd7CsFCAjcbHA9rWtchMGdZ6VojVZ');
const METADATA_PROGRAM = new PublicKey('metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s');
const TOKEN_PROGRAM_ID = new PublicKey('TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA');
const ATA_PROGRAM = new PublicKey('ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL');
const RENT_SYSVAR = new PublicKey('SysvarRent111111111111111111111111111111111');
const GLOBAL = new PublicKey('4wTV1YmiEkRvAtNtsSGPtUrqRYQMe5SKy2uB4Jjaxnjf');
const FEE_RECIPIENT = new PublicKey('FFWtrEQ4B4PKQoVuHYzZq8FabGkVatYzDpEVHsK5rrhF');

// Discriminators (from IDL)
const CREATE_DISC = Buffer.from([24, 30, 200, 40, 5, 28, 7, 119]);
const BUY_DISC = Buffer.from([102, 6, 61, 18, 1, 218, 235, 234]);

// Token details
const TOKEN_NAME = 'QSAM Quantum Token';
const TOKEN_SYMBOL = 'QSAM';
const TOKEN_URI = 'https://raw.githubusercontent.com/Mastercyril/QuantumBitcoinPay-backend/main/qsam-metadata.json';

// === HELPERS ===
function writeU32LE(val) { const b = Buffer.alloc(4); b.writeUInt32LE(val, 0); return b; }
function writeU64LE(val) { const b = Buffer.alloc(8); b.writeBigUInt64LE(BigInt(val), 0); return b; }

function bondingCurvePda(mint) {
  return PublicKey.findProgramAddressSync([Buffer.from('bonding-curve'), mint.toBuffer()], PUMP_PROGRAM)[0];
}
function eventAuthorityPda() {
  return PublicKey.findProgramAddressSync([Buffer.from('__event_authority')], PUMP_PROGRAM)[0];
}
function creatorVaultPda(creator) {
  return PublicKey.findProgramAddressSync([Buffer.from('creator-vault'), creator.toBuffer()], PUMP_PROGRAM)[0];
}
function mintAuthorityPda() {
  return PublicKey.findProgramAddressSync([Buffer.from('mint-authority')], PUMP_PROGRAM)[0];
}
function globalVolumePda() {
  return PublicKey.findProgramAddressSync([Buffer.from('global_volume_accumulator')], PUMP_PROGRAM)[0];
}
function userVolumePda(user) {
  return PublicKey.findProgramAddressSync([Buffer.from('user_volume_accumulator'), user.toBuffer()], PUMP_PROGRAM)[0];
}
function feeConfigPda() {
  return PublicKey.findProgramAddressSync([Buffer.from('fee_config'), PUMP_PROGRAM.toBuffer()], PUMP_FEE_PROGRAM)[0];
}
function ata(owner, mint) {
  return PublicKey.findProgramAddressSync([owner.toBuffer(), TOKEN_PROGRAM_ID.toBuffer(), mint.toBuffer()], ATA_PROGRAM)[0];
}
function metadataPda(mint) {
  return PublicKey.findProgramAddressSync([Buffer.from('metadata'), METADATA_PROGRAM.toBuffer(), mint.toBuffer()], METADATA_PROGRAM)[0];
}

async function main() {
  // Load treasury key
  const pk5 = process.env.SOLANA_PRIVATE_KEY_5;
  const treasury = Keypair.fromSecretKey(bs58decode(pk5));
  console.log('Treasury:', treasury.publicKey.toBase58());
  
  const conn = new Connection('https://solana-rpc.publicnode.com', 'confirmed');
  const balance = await conn.getBalance(treasury.publicKey);
  console.log('Balance:', balance / 1e9, 'SOL (~$' + (balance / 1e9 * 93.76).toFixed(2) + ')');
  
  // Create new mint keypair
  const mint = Keypair.generate();
  console.log('New Pump.fun mint:', mint.publicKey.toBase58());
  
  // Derive all PDAs
  const bondingCurve = bondingCurvePda(mint.publicKey);
  const associatedBondingCurve = ata(bondingCurve, mint.publicKey);
  const associatedUser = ata(treasury.publicKey, mint.publicKey);
  const metadata = metadataPda(mint.publicKey);
  const mintAuthority = mintAuthorityPda();
  const eventAuthority = eventAuthorityPda();
  const creatorVault = creatorVaultPda(treasury.publicKey);
  const globalVolume = globalVolumePda();
  const userVolume = userVolumePda(treasury.publicKey);
  const feeConfig = feeConfigPda();
  
  console.log('Bonding curve:', bondingCurve.toBase58());
  console.log('Mint authority:', mintAuthority.toBase58());
  console.log('Event authority:', eventAuthority.toBase58());
  console.log('Creator vault:', creatorVault.toBase58());
  
  // === CREATE INSTRUCTION ===
  // Data: discriminator + name(string) + symbol(string) + uri(string) + creator(pubkey)
  const nameBuf = Buffer.from(TOKEN_NAME);
  const symbolBuf = Buffer.from(TOKEN_SYMBOL);
  const uriBuf = Buffer.from(TOKEN_URI);
  
  const createData = Buffer.concat([
    CREATE_DISC,
    writeU32LE(nameBuf.length), nameBuf,
    writeU32LE(symbolBuf.length), symbolBuf,
    writeU32LE(uriBuf.length), uriBuf,
    treasury.publicKey.toBuffer(), // creator pubkey
  ]);
  
  // 14 accounts in exact order from IDL
  const createAccounts = [
    { pubkey: mint.publicKey, isSigner: true, isWritable: true },        // 0: mint
    { pubkey: mintAuthority, isSigner: false, isWritable: false },        // 1: mint_authority
    { pubkey: bondingCurve, isSigner: false, isWritable: true },           // 2: bonding_curve
    { pubkey: associatedBondingCurve, isSigner: false, isWritable: true }, // 3: associated_bonding_curve
    { pubkey: GLOBAL, isSigner: false, isWritable: false },               // 4: global
    { pubkey: METADATA_PROGRAM, isSigner: false, isWritable: false },     // 5: mpl_token_metadata
    { pubkey: metadata, isSigner: false, isWritable: true },              // 6: metadata
    { pubkey: treasury.publicKey, isSigner: true, isWritable: true },      // 7: user
    { pubkey: SystemProgram.programId, isSigner: false, isWritable: false }, // 8: system_program
    { pubkey: TOKEN_PROGRAM_ID, isSigner: false, isWritable: false },     // 9: token_program
    { pubkey: ATA_PROGRAM, isSigner: false, isWritable: false },          // 10: associated_token_program
    { pubkey: RENT_SYSVAR, isSigner: false, isWritable: false },          // 11: rent
    { pubkey: eventAuthority, isSigner: false, isWritable: false },       // 12: event_authority
    { pubkey: PUMP_PROGRAM, isSigner: false, isWritable: false },         // 13: program
  ];
  
  const createIx = new TransactionInstruction({
    programId: PUMP_PROGRAM, keys: createAccounts, data: createData
  });
  console.log('\nCreate: 14 accounts, data length:', createData.length);
  
  // === BUY INSTRUCTION ===
  // Buy ~50,000 tokens with max 0.003 SOL (conservative)
  const buyAmount = 50000000000;  // 50,000 tokens (6 decimals)
  const maxSolCost = 3000000;     // 0.003 SOL max
  const trackVolume = 0;          // false
  
  const buyData = Buffer.concat([
    BUY_DISC,
    writeU64LE(buyAmount),
    writeU64LE(maxSolCost),
    Buffer.from([trackVolume]),
  ]);
  
  // 16 accounts in exact order from IDL
  const buyAccounts = [
    { pubkey: GLOBAL, isSigner: false, isWritable: false },               // 0: global
    { pubkey: FEE_RECIPIENT, isSigner: false, isWritable: true },          // 1: fee_recipient
    { pubkey: mint.publicKey, isSigner: false, isWritable: false },       // 2: mint
    { pubkey: bondingCurve, isSigner: false, isWritable: true },          // 3: bonding_curve
    { pubkey: associatedBondingCurve, isSigner: false, isWritable: true }, // 4: associated_bonding_curve
    { pubkey: associatedUser, isSigner: false, isWritable: true },        // 5: associated_user
    { pubkey: treasury.publicKey, isSigner: true, isWritable: true },      // 6: user
    { pubkey: SystemProgram.programId, isSigner: false, isWritable: false }, // 7: system_program
    { pubkey: TOKEN_PROGRAM_ID, isSigner: false, isWritable: false },     // 8: token_program
    { pubkey: creatorVault, isSigner: false, isWritable: true },          // 9: creator_vault
    { pubkey: eventAuthority, isSigner: false, isWritable: false },        // 10: event_authority
    { pubkey: PUMP_PROGRAM, isSigner: false, isWritable: false },         // 11: program
    { pubkey: globalVolume, isSigner: false, isWritable: false },          // 12: global_volume_accumulator
    { pubkey: userVolume, isSigner: false, isWritable: true },            // 13: user_volume_accumulator
    { pubkey: feeConfig, isSigner: false, isWritable: false },            // 14: fee_config
    { pubkey: PUMP_FEE_PROGRAM, isSigner: false, isWritable: false },     // 15: fee_program
  ];
  
  const buyIx = new TransactionInstruction({
    programId: PUMP_PROGRAM, keys: buyAccounts, data: buyData
  });
  console.log('Buy: 16 accounts, data length:', buyData.length);
  console.log('Buy 50K tokens, max 0.003 SOL');
  
  // === BUILD & SEND TRANSACTION ===
  console.log('\n=== Sending transaction ===');
  const tx = new Transaction();
  tx.add(createIx);
  tx.add(buyIx);
  
  const { blockhash } = await conn.getLatestBlockhash();
  tx.recentBlockhash = blockhash;
  tx.feePayer = treasury.publicKey;
  tx.sign(treasury, mint);
  
  // Expected costs
  console.log('Expected: ~0.012 SOL (rent) + 0.003 SOL (buy) + 0.00001 SOL (fee) = ~0.015 SOL');
  console.log('Balance after:', ((balance - 15000000) / 1e9).toFixed(6), 'SOL');
  
  try {
    const sig = await conn.sendRawTransaction(tx.serialize(), { skipPreflight: false, maxRetries: 3 });
    console.log('\n✅ SUCCESS!');
    console.log('Signature:', sig);
    console.log('Solscan: https://solscan.io/tx/' + sig);
    console.log('Pump.fun: https://pump.fun/' + mint.publicKey.toBase58());
    
    // Save mint address
    const fs = require('fs');
    fs.writeFileSync('pump_mint.json', JSON.stringify({
      mint: mint.publicKey.toBase58(),
      name: TOKEN_NAME,
      symbol: TOKEN_SYMBOL,
      signature: sig,
      createdAt: new Date().toISOString()
    }, null, 2));
    console.log('Saved to pump_mint.json');
  } catch(e) {
    console.log('\n❌ Failed:', e.message.substring(0, 200));
    
    // Try without preflight
    console.log('\nTrying without preflight...');
    try {
      const sig2 = await conn.sendRawTransaction(tx.serialize(), { skipPreflight: true, maxRetries: 3 });
      console.log('Sent! Signature:', sig2);
      console.log('Solscan: https://solscan.io/tx/' + sig2);
    } catch(e2) {
      console.log('Failed:', e2.message.substring(0, 200));
    }
  }
}

main().catch(e => { console.error('Fatal:', e.message); console.error(e.stack); });
