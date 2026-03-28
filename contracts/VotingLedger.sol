// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VotingLedger {
    address public owner;

    // Event to emit when a new block hash is recorded
    event HashRecorded(string blockHash, uint timestamp);

    constructor() {
        owner = msg.sender;
    }

    // Function to record a vote / block hash
    function recordVoteHash(string memory blockHash) public {
        require(msg.sender == owner, "Only the owner can record hashes");
        emit HashRecorded(blockHash, block.timestamp);
    }
}
