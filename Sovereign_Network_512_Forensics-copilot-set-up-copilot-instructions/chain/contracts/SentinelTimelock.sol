// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import {TimelockController} from "@openzeppelin/contracts/governance/TimelockController.sol";

/// @title Sentinel Timelock
/// @notice Standard OZ Timelock with guardian-friendly defaults.
contract SentinelTimelock is TimelockController {
    constructor(
        uint256 minDelay,
        address[] memory proposers,
        address[] memory executors,
        address admin
    ) TimelockController(minDelay, proposers, executors, admin) {}
}
