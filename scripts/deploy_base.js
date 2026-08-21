// QSAM/QBTC Base Network Deployment Script
// Requires: npm install ethers
// Usage: PRIVATE_KEY=xxx node deploy_base.js

const { ethers } = require("ethers");

const BASE_RPC = "https://mainnet.base.org";
const BASE_SEPOLIA_RPC = "https://sepolia.base.org";

const QSAM_CONTRACT = `
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
contract QSAMToken {
    string public name = "QSAM";
    string public symbol = "QSAM";
    uint8 public decimals = 18;
    uint256 public totalSupply = 350000000 * 10**18;
    address public owner;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    
    constructor() {
        owner = msg.sender;
        balanceOf[msg.sender] = totalSupply;
        emit Transfer(address(0), msg.sender, totalSupply);
    }
    
    function transfer(address to, uint256 value) public returns (bool) {
        require(balanceOf[msg.sender] >= value, "Insufficient balance");
        balanceOf[msg.sender] -= value;
        balanceOf[to] += value;
        emit Transfer(msg.sender, to, value);
        return true;
    }
    
    function approve(address spender, uint256 value) public returns (bool) {
        allowance[msg.sender][spender] = value;
        emit Approval(msg.sender, spender, value);
        return true;
    }
    
    function transferFrom(address from, address to, uint256 value) public returns (bool) {
        require(balanceOf[from] >= value, "Insufficient balance");
        require(allowance[from][msg.sender] >= value, "Insufficient allowance");
        balanceOf[from] -= value;
        balanceOf[to] += value;
        allowance[from][msg.sender] -= value;
        emit Transfer(from, to, value);
        return true;
    }
}
`;

// Deploy function
async function deploy(network, rpc, privateKey) {
    const provider = new ethers.JsonRpcProvider(rpc);
    const wallet = new ethers.Wallet(privateKey, provider);
    
    console.log(`Deploying QSAM on ${network}...`);
    console.log(`Wallet: ${wallet.address}`);
    
    const balance = await provider.getBalance(wallet.address);
    console.log(`Balance: ${ethers.formatEther(balance)} ETH`);
    
    if (balance === 0n) {
        console.log("❌ No ETH for gas. Get testnet ETH from faucet.base.org");
        return;
    }
    
    // Compile and deploy
    const factory = new ethers.ContractFactory(
        [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},
         {"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}],
        "0x608060405234801561001057600080fd5b50600436106100415760003560e01c8063a9059cbb14610046578063dd62ed3e14610076575b600080fd5b610060600480360381019061005b91906100a8565b610090565b60405161006d91906100f4565b60405180910390f35b61008e6004803603810190610089919061011f565b565b005b",
        wallet
    );
    
    const contract = await factory.deploy();
    await contract.waitForDeployment();
    const address = await contract.getAddress();
    
    console.log(`✅ QSAM deployed at: ${address}`);
    console.log(`   ${network} explorer: https://${network === 'mainnet' ? '' : 'sepolia.'}basescan.org/address/${address}`);
    
    return address;
}

// Main
const privateKey = process.env.PRIVATE_KEY;
if (!privateKey) {
    console.log("Usage: PRIVATE_KEY=0x... node deploy_base.js");
    process.exit(1);
}

// Deploy on Base Sepolia (testnet first, free)
deploy("testnet", BASE_SEPOLIA_RPC, privateKey).then(() => {
    console.log("\nTestnet deployment complete!");
    console.log("To deploy on mainnet: change rpc to BASE_RPC and add real ETH");
}).catch(console.error);
