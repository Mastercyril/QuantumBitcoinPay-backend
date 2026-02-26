# QuantumBitcoinPay Backend

> **Private repository** — QuantumBitcoinPay.com infrastructure, wallet builds, and presale backend.
> Owner: 13th Chamber LLC | josephdougherty483@gmail.com

---

## Overview

This repo stores all backend assets and logic for [QuantumBitcoinPay.com](https://www.quantumbitcoinpay.com), including:

- Android APK wallet releases
- Windows Desktop wallet installer releases
- Wix site backend / Velo code
- Daily ecosystem runner scripts
- QSAM & QBTC token configuration

---

## Repository Structure

```
QuantumBitcoinPay-backend/
├── releases/
│   ├── android/
│   │   └── QuantumPay-wallet-v1.0.0.apk
│   └── windows/
│       └── QuantumPay-wallet-setup-v1.0.0.exe
├── ecosystem/
│   ├── RUN_ECOSYSTEM_NOW.sh
│   ├── daily_ecosystem_executor.py
│   ├── QUICKSTART_ECOSYSTEM.md
│   └── DEPLOYMENT_CHECKLIST.md
├── wix-velo/
│   ├── presale.js
│   └── home.js
├── token/
│   └── QSAM-config.json
└── README.md
```

---

## Wallet Downloads

Wallet builds are published as **GitHub Releases** and linked from the Wix presale page download buttons.

| Platform | Download URL |
|---|---|
| Android APK | `https://github.com/Mastercyril/QuantumBitcoinPay-backend/releases/latest/download/QuantumPay-wallet.apk` |
| Windows Desktop | `https://github.com/Mastercyril/QuantumBitcoinPay-backend/releases/latest/download/QuantumPay-wallet-setup.exe` |

> To publish a new build: go to **Releases → Draft a new release**, attach the APK/EXE, tag it `v1.0.0`, publish.
> The download buttons on quantumbitcoinpay.com/presale will point to these URLs.

---

## Ecosystem & Token Info

### QSAM Token (Reward / Utility Token)
- **Token:** QSAM
- **Blockchain:** Quantum Blockchain (proprietary — NOT Ethereum)
- **Daily Reward:** 10 QSAM tokens per wallet (1,560+ QSAM distributed daily across 156+ wallets)
- **New Wallet Bonus:** 5,000 QSAM tokens credited on first install
- **IBM Quantum Bonus:** 10 QSAM per completed quantum test; 20 QSAM for entanglement experiments
- **Wallet Format:** `QPAY-YYYYMMDD-XXXXX` (unique per download)

### QBTC Token (Presale Token)
- **Token:** QBTC
- **Presale Address:** `0x66E0A49A91E45EEEFB9F9A9e4fDC9DC03F4CcFED`
- **Accepted Payments:** ETH, USDT, USDC
- **Phase 1 Price:** $0.001 / QBTC (+30% bonus)
- **Phase 2 Price:** $0.0015 / QBTC (+20% bonus)
- **Minimum Buy:** $50
- **Presale Countdown:** Ends March 28, 2026

---

## Daily Ecosystem Runner

The ecosystem runs automatically at **9:00 AM EST** daily with triple-layer redundancy (failover at 3PM and 9PM).

```bash
# Run immediately
chmod +x ecosystem/RUN_ECOSYSTEM_NOW.sh
./ecosystem/RUN_ECOSYSTEM_NOW.sh

# Or via Python
python3 ecosystem/daily_ecosystem_executor.py
```

Daily operations:
- Load 156+ wallets and distribute QSAM rewards
- Track new wallet downloads with unique quantum codes
- Sync transactions with the Quantum blockchain
- Encrypted backups to GitHub + Google Drive
- Email daily summary report

---

## Contact

- **Support Line:** (609) 451-6892
- **Email:** presale@quantumbitcoin.com
- **Telegram:** @QuantumBitcoinX
- **Site:** https://www.quantumbitcoinpay.com
- **Company:** 13th Chamber LLC | Wilmington, DE
