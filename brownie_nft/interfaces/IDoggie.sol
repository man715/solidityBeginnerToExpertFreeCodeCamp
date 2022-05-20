// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

interface Doggie {
    function tokenURI(uint256) external view returns (string memory);

    function createCollectible(string memory) external view returns (uint256);
}
