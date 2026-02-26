# 🔮 QuantumBitcoinPay Backend

> **Private repository** — QuantumBitcoinPay.com infrastructure, wallet builds, and presale backend.
> **Owner:** 13th Chamber LLC | josephdougherty483@gmail.com | Wilmington, DE
> **Related:** [QSAM Quantum Token Ecosystem](https://github.com/13thchamberllc/QSAM-quantum-token)

---

## Overview

This repo is the private backend for [QuantumBitcoinPay.com](https://www.quantumbitcoinpay.com) — the presale and wallet distribution platform for the QSAM + QBTC ecosystem built by 13th Chamber LLC. It stores:

- Android APK & Windows Desktop wallet releases
- Wix site backend / Velo code
- Daily ecosystem runner scripts
- QSAM & QBTC token configuration
- SCORE encryption references

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
│   ├── QSAM-config.json
│   └── QBTC-presale-config.json
└── README.md
```

---

## Wallet Downloads

Builds are published as **GitHub Releases** and linked from the presale page download buttons.

| Platform | URL |
|---|---|
| Android APK | `https://github.com/Mastercyril/QuantumBitcoinPay-backend/releases/latest/download/QuantumPay-wallet.apk` |
| Windows Desktop | `https://github.com/Mastercyril/QuantumBitcoinPay-backend/releases/latest/download/QuantumPay-wallet-setup.exe` |

> **To publish:** Go to Releases → Draft a new release → attach APK/EXE → tag `v1.0.0` → publish.

---

## QSAM Token — Full Ecosystem Details

### What is QSAM?

QSAM (Quantum Secured Asset Management) is a revolutionary token that rewards users for running quantum computing workloads on IBM Quantum and other quantum hardware platforms. Built on 13th Chamber LLC proprietary breakthroughs — SCORE encryption, quantum entanglement verification, and the ESCORT system.

### Token Details

| Field | Value |
|---|---|
| **Name** | QSAM (Quantum Secured Asset Management) |
| **Symbol** | QSAM |
| **Current Value** | $0.0000001 USD per QSAM |
| **Blockchain** | Custom Quantum Blockchain (Proof of Quantum Work) |
| **Consensus** | Proof of Quantum Work (PoQW) |
| **Block Time** | Daily block creation with Merkle Tree verification |
| **Wallet** | QuantumPay (exclusive QSAM wallet) |
| **Encryption** | SCORE Protocol (AES-256 + Quantum-resistant algorithms) |

### Supply Schedule (Controlled Release)

- **Years 1–2:** 350,000,000 QSAM released per year
- **Year 3+:** 350,000,000 QSAM every 3 years
- Ensures sustainable growth and prevents market flooding

### Distribution

| Recipient | Amount |
|---|---|
| New Wallet Download (all users) | 5,000 QSAM welcome bonus |
| Early Adopter Bonus (first 1,000 wallets) | Additional 5,000 QSAM |
| Daily per-wallet reward | 10 QSAM/day |

### Reward Structure

| Workload Type | QSAM Reward |
|---|---|
| Standard Quantum Job (IBM) | 10 QSAM |
| Quantum Entanglement Job | 20 QSAM |
| SCORE / ESCORT System Test | 10 QSAM |
| Entanglement + SCORE combined | 20 QSAM |

> Must use 13th Chamber LLC systems (QSAM, ESCORT, SCORE) on IBM Quantum or approved hardware. Valid workload verification number required.

---

## QBTC Token — Presale Details

| Field | Value |
|---|---|
| **Token** | QBTC |
| **Presale Address** | `0x66E0A49A91E45EEEFB9F9A9e4fDC9DC03F4CcFED` |
| **Accepted Payments** | ETH, USDT, USDC |
| **Phase 1 Price** | $0.001 / QBTC (+30% bonus) |
| **Phase 2 Price** | $0.0015 / QBTC (+20% bonus) |
| **Minimum Buy** | $50 |
| **Presale End** | March 28, 2026 |

---

## SCORE Encryption System

**SCORE** (Secure Cryptographic Operations with Redundant Entanglement) is 13th Chamber LLC's proprietary quantum-resistant encryption protocol:

- **Post-quantum algorithms** resistant to quantum computer attacks
- **Entanglement-based verification** — unhackable transaction validation
- **Multi-layer protection** with redundant encryption layers
- **AES-256 + Quantum-resistant key generation**
- **ESCORT System**: Enhanced SCORE for large-scale enterprise quantum operations

Every QuantumPay wallet uses SCORE encryption. All private keys are encrypted using quantum entanglement principles.

---

## Daily Ecosystem Runner

Runs automatically at **9:00 AM EST** with triple-layer redundancy (failover at 3PM + 9PM EST).

```bash
# Run immediately
chmod +x ecosystem/RUN_ECOSYSTEM_NOW.sh
./ecosystem/RUN_ECOSYSTEM_NOW.sh

# Or via Python directly
python3 ecosystem/daily_ecosystem_executor.py
```

### What Runs Daily

- Load 156+ wallets and distribute QSAM rewards (10 QSAM/wallet)
- Detect new wallet downloads → auto-send 5,000 QSAM welcome bonus
- Track IBM Quantum workload submissions and distribute job rewards
- Sync all transactions with the Quantum blockchain (Merkle tree)
- Encrypted backups to GitHub + Google Drive
- Email daily summary report to admin
- Complete audit trail with timestamps

### Required `.env` Config

```bash
GITHUB_TOKEN=your_github_token
BLOCKCHAIN_TOKEN=your_blockchain_token
EMAIL_FROM=ecosystem@quantumpay.dev
EMAIL_PASSWORD=your_password
ADMIN_EMAIL=admin@quantumpay.dev
GDRIVE_TOKEN=your_gdrive_token
```

---

## Roadmap (Updated Feb 2026)

### Phase 1: Foundation (2025 Q1–Q2) ✅
- [x] QSAM token creation
- [x] QuantumPay wallet launch
- [x] IBM Quantum integration
- [x] SCORE encryption implementation
- [x] Initial distribution to first 20 users

### Phase 2: Expansion (2025 Q3 – 2026) 🔄 IN PROGRESS
- [x] QuantumBitcoinPay.com presale site live
- [x] QBTC presale launched (Phase 1 live at $0.001)
- [x] GitHub private backend repository created
- [ ] Android APK wallet release
- [ ] Windows Desktop wallet release
- [ ] Mobile wallet (iOS) release
- [ ] Integration with additional quantum providers
- [ ] QSAM trading on decentralized exchanges

### Phase 3: Quantum Leap (2026–2027)
- [ ] Quantum teleportation transfers
- [ ] Cross-chain bridge development
- [ ] Enterprise quantum workload packages
- [ ] QSAM staking rewards
- [ ] DAO governance implementation

### Phase 4: Ecosystem Maturity (2027+)
- [ ] Integration with major blockchain ecosystems
- [ ] Quantum computing marketplace
- [ ] QSAM DeFi protocols

### Phase 5: Quantum Protection for All Cryptos (2028+)
- [ ] QSAM Quantum Shield API for external crypto protection
- [ ] SCORE encryption licensing for BTC, ETH, SOL, ADA
- [ ] Cross-chain quantum security layer
- [ ] Universal quantum threat protection protocol

---

## Contact

| | |
|---|---|
| **Support Line** | (609) 451-6892 |
| **Presale Email** | presale@quantumbitcoin.com |
| **Company Email** | info@13thchamberinc.com |
| **Telegram** | @QuantumBitcoinX |
| **Site** | https://www.quantumbitcoinpay.com |
| **Company** | 13th Chamber LLC — Wilmington, DE |
| **QSAM Repo** | https://github.com/13thchamberllc/QSAM-quantum-token |
