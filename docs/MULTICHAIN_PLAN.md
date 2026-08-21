# QSAM/QBTC Multi-Chain Deployment Plan

## Current State
- Solana mainnet: QSAM (350M) + QBTC (21M) — both live
- QSAM mint: 5nHg43TTkmCafvUPpjnvu57hWMRXUheN3CFdDuzdQM9x (FIXED)
- QBTC mint: EMzyVtLsjyzMztFHQ7wYTGM8ojSDQJzstjmRsitnt1F9

## Multi-Chain Targets

### 1. Base (Coinbase L2) — PRIORITY
- Gas: ~$0.01 per transaction
- ERC-20 contracts ready: contracts/qsam-erc20.sol
- Need: EVM wallet private key + ~$1 ETH on Base
- Deploy: Use ethers.js or foundry

### 2. Ethereum Mainnet
- Gas: ~$5-50 per deployment
- Same ERC-20 contracts
- Need: EVM wallet + ~$50 ETH for gas
- Lower priority due to cost

### 3. Pump.fun (Solana)
- Create new token via Pump.fun UI
- Need: Phantom wallet connected
- Cost: ~0.02 SOL ($3) per token
- Good for visibility on Pump.fun platform

### 4. Arbitrum One
- Gas: ~$0.10 per transaction
- Same ERC-20 contracts
- Need: EVM wallet + some ETH on Arbitrum

### 5. Polygon
- Gas: ~$0.01 per transaction
- Same ERC-20 contracts
- Need: EVM wallet + some MATIC

## Implementation Steps

### Base Deployment (Free if we have wallet):
1. Install ethers.js: npm install ethers
2. Get Base ETH from faucet (testnet) or bridge (mainnet)
3. Deploy QSAMToken contract
4. Deploy QBTCToken contract
5. Verify on Basescan
6. Add to token list

### Pump.fun Deployment:
1. Navigate to pump.fun/new
2. Connect Phantom wallet
3. Create QSAM token with:
   - Name: QSAM
   - Symbol: QSAM
   - Description: Quantum State Amplitude Modulation
   - Supply: 350,000,000
4. Create QBTC token with:
   - Name: QBTC
   - Symbol: QBTC
   - Description: Quantum Bitcoin
   - Supply: 21,000,000
5. Share Pump.fun links

## Required From User:
- [ ] EVM wallet private key (for Base/Ethereum/Arbitrum/Polygon)
- [ ] Phantom wallet connection (for Pump.fun)
- [ ] ~$1 ETH on Base for gas (can use Coinbase wallet)
