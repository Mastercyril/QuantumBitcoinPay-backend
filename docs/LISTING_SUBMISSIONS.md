# QSAM/QBTC Listing Submissions — Pre-filled Information

## CoinMarketCap Submission

**URL:** https://support.coinmarketcap.com/hc/en-us/requests/new  
**Form:** Select "1 - [New Listing] Add cryptoasset"  
**Requires:** CoinMarketCap account login

### QSAM Fields:
- **Coin Name:** QSAM Quantum Token
- **Symbol:** QSAM
- **Blockchain:** Solana
- **Contract/Mint Address:** 5nHg43TTkmCafvUPpjnvu57hWMRXUheN3CFdDuzdQM9x
- **Decimals:** 9
- **Total Supply:** 350,000,000
- **Circulating Supply:** 350,000,000 (all minted to treasury)
- **Website:** https://quantumbitcoinpay.com
- **GitHub:** https://github.com/Mastercyril/QuantumBitcoinPay-backend
- **Explorer:** https://solscan.io/token/5nHg43TTkmCafvUPpjnvu57hWMRXUheN3CFdDuzdQM9x
- **Treasury:** https://solscan.io/account/2iG3NGn2pcRabznaU1ndC17JcQqewERhQL53G3Z5Suff
- **Logo:** https://raw.githubusercontent.com/Mastercyril/QuantumBitcoinPay-backend/main/assets/qsam-logo.svg
- **Description:** QSAM is a quantum-native cryptocurrency powered by the Quantum State Amplitude Modulation framework. Using IBM Quantum hardware (ibm_torino, 133 qubits), QSAM achieves 1965x total quantum advantage over classical systems with 99.73% fidelity. The token uses Proof of Quantum Work (PoQW) consensus with CHSH parameter S=2.781, providing cryptographic proof of quantum execution. 8 proprietary systems: QSAM, SCORE, ESCORT, QELS, CACP (20000x coherence), CPAR, AQBB_v3 (35714x coherence), GEL. Post-quantum security via S-Corner Protocol (CRYSTALS-Dilithium + KYBER). Patent pending: 50 claims.

### QBTC Fields:
- **Coin Name:** Quantum Bitcoin
- **Symbol:** QBTC
- **Blockchain:** Solana
- **Contract/Mint Address:** EMzyVtLsjyzMztFHQ7wYTGM8ojSDQJzstjmRsitnt1F9
- **Decimals:** 9
- **Total Supply:** 21,000,000
- **Website:** https://quantumbitcoinpay.com
- **Explorer:** https://solscan.io/token/EMzyVtLsjyzMztFHQ7wYTGM8ojSDQJzstjmRsitnt1F9
- **Description:** Quantum Bitcoin (QBTC) is a quantum-mined cryptocurrency using PoQW consensus. ASIC-resistant quantum mining with CHSH > 2.0 verification. 21M fixed supply mirroring Bitcoin. Powered by 13th Chamber LLC quantum framework.

---

## CoinGecko Submission

**URL:** https://support.coingecko.com/hc/en-us/sections/32146983631641-Token-Coin-Listing  
**Form:** "How to List a New Cryptocurrency on CoinGecko"  
**Requires:** CoinGecko account login  
**PREREQUISITE:** Token must be actively tradable on an exchange tracked by CoinGecko

### Steps:
1. Create a CoinGecko account at coingecko.com
2. Navigate to the listing form
3. Fill in token details (same as CMC above)
4. Make a public verification post on X/Twitter
5. Wait for review (typically 1-2 weeks)

### Note:
CoinGecko requires the token to be actively tradable on a DEX or CEX they track.
**Action needed first:** Create a Raydium liquidity pool (QSAM/SOL) with 0.5+ SOL.

---

## DEXScreener (Automatic)

DEXScreener automatically indexes Solana tokens with liquidity.
Once the Raydium pool is created, QSAM will appear automatically at:
https://dexscreener.com/solana/5nHg43TTkmCafvUPpjnvu57hWMRXUheN3CFdDuzdQM9x

---

## Raydium Liquidity Pool Setup

**URL:** https://raydium.io/liquidity/create  
**Requirements:**
- 0.5+ SOL in treasury wallet
- QSAM tokens (already minted: 350M in treasury)
- Phantom wallet connected

**Pool Configuration:**
- Token: QSAM (5nHg43TTkmCafvUPpjnvu57hWMRXUheN3CFdDuzdQM9x)
- Pair: QSAM/SOL
- Initial Price: 1 QSAM = $0.01 (at SOL ~$150, this means 1 SOL = 10,000 QSAM)
- QSAM Amount: 350,000 QSAM (0.1% of supply for initial pool)
- SOL Amount: 0.5 SOL
- Slippage: 1%

---

## Summary of Manual Steps Required

1. **Fund treasury** with 0.5+ SOL (transfer from Phantom or exchange)
2. **Create Raydium pool** at raydium.io (QSAM/SOL pair)
3. **Log into CoinGecko** and submit listing request
4. **Log into CoinMarketCap** and submit listing request (form: "Add cryptoasset")
5. **Connect Phantom** to Pump.fun and sign the pending transaction
6. **Fund Base wallet** (0x6401EEAb258E24b8B9C43708663702354111cDC2) with ETH for ERC-20 deployment
