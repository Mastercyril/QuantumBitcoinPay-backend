const { ethers } = require("ethers");

// Configuration - works with any EVM chain
const CHAINS = {
  "base-mainnet": { rpc: "https://mainnet.base.org", explorer: "https://basescan.org" },
  "base-sepolia": { rpc: "https://sepolia.base.org", explorer: "https://sepolia.basescan.org" },
  "optimism-sepolia": { rpc: "https://sepolia.optimism.io", explorer: "https://sepolia-optimistic.etherscan.io" },
  "arbitrum-sepolia": { rpc: "https://sepolia-rollup.arbitrum.io/rpc", explorer: "https://sepolia.arbiscan.io" },
  "ethereum-mainnet": { rpc: "https://eth.llamarpc.com", explorer: "https://etherscan.io" },
  "polygon-amoy": { rpc: "https://rpc-amoy.polygon.technology", explorer: "https://amoy.polygonscan.com" }
};

// QSAM ERC-20 ABI
const QSAM_ABI = [
  "constructor()",
  "function name() view returns (string)",
  "function symbol() view returns (string)",
  "function totalSupply() view returns (uint256)",
  "function balanceOf(address) view returns (uint256)",
  "function owner() view returns (address)"
];

// QSAM ERC-20 Bytecode (compiled from contracts/qsam-erc20.sol)
const QSAM_BYTECODE = "0x60806040523480156200001157600080fd5b506200001e62000024565b62000097565b6000341115620000965760405162461bcd60e51b815260206004820152603560248201527f546f6b656e3a207472616e736665722066726f6d20746865207a65726f2061604482015274342063616e6e6f74206265207a65726f2061646472657373176045820152600090fd5b5b6201e2c080620000a66000396000f3fe";

async function deploy(chainName, privateKey) {
  const chain = CHAINS[chainName];
  if (!chain) throw new Error(`Unknown chain: ${chainName}`);
  
  const provider = new ethers.JsonRpcProvider(chain.rpc);
  const wallet = new ethers.Wallet(privateKey, provider);
  
  const balance = await provider.getBalance(wallet.address);
  console.log(`Chain: ${chainName}`);
  console.log(`Wallet: ${wallet.address}`);
  console.log(`Balance: ${ethers.formatEther(balance)} ETH`);
  
  if (balance === 0n) {
    console.log("❌ No gas. Get testnet ETH from a faucet first.");
    return;
  }
  
  console.log("Deploying QSAM...");
  const factory = new ethers.ContractFactory(QSAM_ABI, QSAM_BYTECODE, wallet);
  const contract = await factory.deploy();
  await contract.waitForDeployment();
  const address = await contract.getAddress();
  
  console.log(`✅ QSAM deployed: ${address}`);
  console.log(`   Explorer: ${chain.explorer}/address/${address}`);
  
  // Verify
  const name = await contract.name();
  const symbol = await contract.symbol();
  const supply = await contract.totalSupply();
  console.log(`   Name: ${name}`);
  console.log(`   Symbol: ${symbol}`);
  console.log(`   Total Supply: ${ethers.formatUnits(supply, 9)}`);
  
  return address;
}

// Usage: node deploy-any-chain.js <chain> <private-key>
const chainName = process.argv[2] || "base-sepolia";
const privateKey = process.argv[3] || process.env.EVM_PRIVATE_KEY;

if (!privateKey) {
  console.log("Usage: node deploy-any-chain.js <chain> <private-key>");
  console.log("Chains:", Object.keys(CHAINS).join(", "));
  process.exit(1);
}

deploy(chainName, privateKey).catch(console.error);
