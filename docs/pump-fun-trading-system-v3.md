# Pump.fun Trading System v3

## Overview
Automated trading system for Pump.fun bonding curve tokens on Solana.

## Treasury
- Wallet: 2iG3NGn2pcRabznaU1ndC17JcQqewERhQL53G3Z5Suff
- Current SOL: 0.0009 (~$0.09)
- Needs 0.05+ SOL to activate sniper

## Our Tokens (5 on Pump.fun)
1. QSAM — https://pump.fun/48YZxAUXFcEG14kEWHyBBaEx1gabprkXxQsz2ViuPZPN
2. QBTC — https://pump.fun/GPPUwx7JiN7Q5VKxWmBk7VcKAfnStCaEju4Q1smMgUzo
3. QLINK — https://pump.fun/BC5vJhsfYSebgJLDZLLsZh1WcHaE5FhALjS4WjpHdi3R
4. SCORE — https://pump.fun/J9mJi56H1N3vdn8kR9X8erqy8GtZZGGZG132JZHTy1j3
5. ESCRT — https://pump.fun/3G5Hf6e9aTzKvyKqJyDsKMMJY3wK7phPFU2KVy9V9Zpp

## Sniper Configuration
- Buy amount: 0.001 SOL per snipe
- Priority fee: 0.001 SOL (high for confirmation)
- Take profit: +40%
- Stop loss: -25%
- Max hold time: 120 seconds
- Min dev buy filter: 0.5 SOL
- Min market cap filter: 5 SOL
- Max concurrent positions: 5
- Min SOL to trade: 0.03 SOL

## How It Works
1. WebSocket connects to PumpPortal (free — new token events only)
2. New token events stream in (~30/minute)
3. Filter: dev buy > 0.5 SOL AND market cap > 5 SOL
4. Buy via PumpPortal trade-local API
5. Monitor bonding curve via RPC every 3 seconds
6. Exit at +40% (take profit), -25% (stop loss), or 120s (time exit)
7. Results saved to sniper_v3_results.json

## Revenue Sources
1. Sniping profits (buy low, sell high on bonding curve)
2. Creator fees: 0.3% of ALL trading volume on our 5 tokens (passive)
3. Token appreciation: 71K tokens each of QBTC/QLINK/SCORE/ESCRT held

## Files
- pump_sniper_v3.js — Main sniper bot
- quick_check.js — Treasury balance check
- check_all_balances.js — Full token + bonding curve status
- pump_factory.js — Token creation script (creates new tokens on Pump.fun)

## Workflow
- "Pump.fun Trading Monitor" runs every 30 minutes
- Checks SOL balance and token status
- If SOL >= 0.05, runs sniper for 4 minutes
- If SOL < 0.05, reports status and reminds to bridge SOL

## To Activate
Bridge SOL to treasury wallet: 2iG3NGn2pcRabznaU1ndC17JcQqewERhQL53G3Z5Suff
Minimum needed: 0.05 SOL (~$5)
Recommended: 0.1-0.5 SOL for better sniping opportunities
