// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract QSAMToken is ERC20, Ownable {
    constructor() ERC20("QSAM", "QSAM") Ownable(msg.sender) {
        // Mint 350,000,000 QSAM with 18 decimals (ERC-20 standard)
        _mint(msg.sender, 350000000 * 10**18);
    }
}

contract QBTCToken is ERC20, Ownable {
    constructor() ERC20("QBTC", "QBTC") Ownable(msg.sender) {
        // Mint 21,000,000 QBTC with 18 decimals
        _mint(msg.sender, 21000000 * 10**18);
    }
}
