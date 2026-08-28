# Pump.fun Sniper v4 — Dynamic Priority Fees

## Key Improvements over v3

### 1. Dynamic Fee Estimation
Queries `getRecentPrioritizationFees` from Solana RPC and uses 2x the 75th percentile, clamped to [0.003, 0.01] SOL. No more guessing the right fee.

### 2. Fee Escalation on Retries
If a transaction doesn't confirm, it retries with escalating fees: base → 2x → 4x. This means the first attempt uses a reasonable fee, but if the network is congested, subsequent attempts pay more to get confirmed.

### 3. Pre-Flight Cost Calculation
Before attempting a buy, checks: `balance >= buyAmount + priorityFee + baseTxFee + buffer`. Never starts a trade it can't afford to complete.

### 4. Compute Budget Instructions
Adds `setComputeUnitLimit` (200k CU) and `setComputeUnitPrice` instructions to legacy transactions, giving validators explicit priority information.

### 5. Multi-RPC Auto-Rotation
Rotates between 3 Solana RPC endpoints (mainnet, Ankr, PublicNode) on timeout, avoiding rate limits and single-endpoint failures.

### 6. Higher Sell Priority (0.005 SOL)
Sells use a higher base priority fee than buys (0.005 vs 0.003) because exits are more time-sensitive — you don't want to be stuck holding a crashing token.

### 7. Full Error Logging
All errors are captured and displayed — no more silent failures. Every failed buy/sell shows the actual error message.

### 8. Fee Tracking
Separately tracks buy fees, sell fees, and total fees paid, so you can see exactly how much goes to the network vs trading PnL.

### 9. Failed Sell Retry
If a sell fails after all escalation attempts, it schedules a retry in 10 seconds instead of giving up.

## Configuration
- Buy amount: 0.001 SOL per snipe
- Base priority fee: 0.003 SOL (buys), 0.005 SOL (sells)
- Max priority fee: 0.01 SOL cap
- Take profit: +40%
- Stop loss: -25%
- Max hold time: 120 seconds
- Min dev buy filter: 0.5 SOL
- Min market cap filter: 5 SOL
- Max concurrent positions: 5
- Min SOL to trade: 0.03 SOL
- Compute unit limit: 200,000

## Treasury
Wallet: 2iG3NGn2pcRabznaU1ndC17JcQqewERhQL53G3Z5Suff
Current: 0.0009 SOL — bridge 0.05+ SOL to activate
