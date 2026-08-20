#!/bin/bash
# QSAM/QBTC Token Submission Script
# Push tokens to all crypto tracking platforms

QSAM_MINT="5nHg43TTkmCafvUPpjnu57hWMRXUheN3CFdDuzdQM9x"
QBTC_MINT="EMzyVtLsjyzMztFHQ7wYTGM8ojSDQJzstjmRsitnt1F9"
TREASURY="2iG3NGn2pcRabznaU1ndC17JcQqewERhQL53G3Z5Suff"
WEBSITE="https://quantumbitcoinpay.com"
GITHUB="https://github.com/Mastercyril/QuantumBitcoinPay-backend"

echo "============================================"
echo "QSAM/QBTC Token Submission Script"
echo "============================================"

# 1. DexScreener (auto-indexes with liquidity)
echo "[1] DexScreener: Auto-indexes once liquidity pool is created"
curl -s "https://api.dexscreener.com/latest/dex/tokens/$QSAM_MINT" | python3 -c "import sys,json; d=json.load(sys.stdin); print('  Status:', 'Listed' if d.get('pairs') else 'Pending liquidity pool')"

# 2. Solscan
echo "[2] Solscan: Auto-indexed (on-chain)"
echo "  QSAM: https://solscan.io/token/$QSAM_MINT"
echo "  QBTC: https://solscan.io/token/$QBTC_MINT"

# 3. Solana Explorer
echo "[3] Solana Explorer: Auto-indexed (on-chain)"
echo "  QSAM: https://explorer.solana.com/address/$QSAM_MINT"
echo "  QBTC: https://explorer.solana.com/address/$QBTC_MINT"

# 4. Solana Beach
echo "[4] Solana Beach: Auto-indexed (on-chain)"
echo "  QSAM: https://solanabeach.io/token/$QSAM_MINT"

# 5. SolanaFM
echo "[5] SolanaFM: Auto-indexed (on-chain)"
echo "  QSAM: https://solana.fm/address/$QSAM_MINT"

# 6. CoinGecko (manual submission required)
echo "[6] CoinGecko: Manual submission at coingecko.com → Request Form"
echo "  Platform ID: solana"
echo "  Contract: $QSAM_MINT"

# 7. CoinMarketCap (manual submission required)
echo "[7] CoinMarketCap: Manual submission at coinmarketcap.com → Get listed"
echo "  Contract: $QSAM_MINT"

# 8. CoinPaprika (API submission)
echo "[8] CoinPaprika: API submission"
curl -s -X POST "https://api.coinpaprika.com/v1/coins" \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"QSAM\",\"symbol\":\"QSAM\",\"platform\":\"solana\",\"contract_address\":\"$QSAM_MINT\"}" \
  2>&1 | head -c 100

# 9. Birdeye (auto-indexes Solana tokens)
echo "[9] Birdeye: Auto-indexes Solana tokens"
echo "  QSAM: https://birdeye.so/token/$QSAM_MINT?chain=solana"

# 10. Step Finance
echo "[10] Step Finance: Auto-indexes Solana tokens"
echo "  QSAM: https://step.finance/tokens/$QSAM_MINT"

# 11. Jupiter Aggregator
echo "[11] Jupiter: Auto-indexes SPL tokens"
echo "  QSAM: https://jup.ag/token/$QSAM_MINT"

echo ""
echo "=== Platforms requiring liquidity pool ==="
echo "DexScreener, DEXTools, Birdeye, Jupiter trading"
echo "Create Raydium/Orca liquidity pool with ~0.5-1 SOL"

echo ""
echo "=== Platforms requiring manual submission ==="
echo "CoinGecko: https://www.coingecko.com → Request Form"
echo "CoinMarketCap: https://coinmarketcap.com → Get listed"
echo "CoinPaprika: https://coinpaprika.com → Add coin"
echo "CoinCodex: https://coincodex.com → Add coin"
echo "LiveCoinWatch: https://livecoinwatch.com → List a coin"
echo "Nomics: https://nomics.com → Add coin"
