# Solana Metaplex Token Metadata Setup

## Why This Matters
QSAM and QBTC need Metaplex token metadata to display properly in Phantom, Solflare, and other Solana wallets. Without it, the tokens show as raw mint addresses instead of names/symbols/logos.

## Steps to Add Metadata On-Chain

### Option 1: Using Metaplex CLI
```bash
# Install Metaplex CLI
npm install -g @metaplex-foundation/mpl-cli

# Create metadata for QSAM
mpl create_metadata_account \
  --mint 5nHg43TTkmCafvUPpjnu57hWMRXUheN3CFdDuzdQM9x \
  --name "QSAM" \
  --symbol "QSAM" \
  --uri "https://raw.githubusercontent.com/Mastercyril/QuantumBitcoinPay-backend/main/metadata/metaplex-qsam.json" \
  --keypair ~/.config/solana/id.json

# Create metadata for QBTC
mpl create_metadata_account \
  --mint EMzyVtLsjyzMztFHQ7wYTGM8ojSDQJzstjmRsitnt1F9 \
  --name "QBTC" \
  --symbol "QBTC" \
  --uri "https://raw.githubusercontent.com/Mastercyril/QuantumBitcoinPay-backend/main/metadata/metaplex-qbtc.json" \
  --keypair ~/.config/solana/id.json
```

### Option 2: Using Solana CLI + Metaplex JS
```javascript
import { Metaplex } from "@metaplex-foundation/js";
import { Connection, clusterApiUrl } from "@solana/web3.js";

const connection = new Connection(clusterApiUrl("mainnet-beta"));
const metaplex = new Metaplex(connection);

// Create metadata for QSAM
await metaplex.nfts().create({
  uri: "https://raw.githubusercontent.com/Mastercyril/QuantumBitcoinPay-backend/main/metadata/metaplex-qsam.json",
  name: "QSAM",
  symbol: "QSAM",
  tokenStandard: "Fungible",
}).send();
```

### Option 3: Using Phantom Wallet
1. Go to https://phantom.app
2. Connect treasury wallet
3. Use "Create Token" feature
4. Upload QSAM metadata from metaplex-qsam.json

## Required SOL
Each metadata creation costs ~0.01 SOL. Treasury has 0.16 SOL - sufficient for both tokens.

## Metadata Files
- QSAM: metadata/metaplex-qsam.json
- QBTC: metadata/metaplex-qbtc.json
- Logo: assets/qsam-logo.svg
