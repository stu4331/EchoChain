// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {ERC20Permit} from "@openzeppelin/contracts/token/ERC20/extensions/draft-ERC20Permit.sol";
import {ERC20Votes} from "@openzeppelin/contracts/token/ERC20/extensions/ERC20Votes.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

/// @title SOUL Token (ERC20Votes)
/// @notice Governance token for Sentinel Network testnet deployments.
contract SoulToken is ERC20, ERC20Permit, ERC20Votes, Ownable {
    uint256 public immutable maxSupply;

    constructor(uint256 _initialSupply, uint256 _maxSupply, address treasury)
        ERC20("Sentinel Soul", "SOUL")
        ERC20Permit("Sentinel Soul")
    {
        require(treasury != address(0), "treasury required");
        require(_initialSupply <= _maxSupply, "initial > max");
        maxSupply = _maxSupply;
        _mint(treasury, _initialSupply);
    }

    /// @notice Mint additional tokens up to the maxSupply.
    function mint(address to, uint256 amount) external onlyOwner {
        require(totalSupply() + amount <= maxSupply, "maxSupply exceeded");
        _mint(to, amount);
    }

    // --- Overrides required by Solidity ---
    function _afterTokenTransfer(address from, address to, uint256 amount)
        internal
        override(ERC20, ERC20Votes)
    {
        super._afterTokenTransfer(from, to, amount);
    }

    function _mint(address to, uint256 amount)
        internal
        override(ERC20, ERC20Votes)
    {
        super._mint(to, amount);
    }

    function _burn(address account, uint256 amount)
        internal
        override(ERC20, ERC20Votes)
    {
        super._burn(account, amount);
    }
}
