// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

/// @title CoreValues
/// @notice Enforces Sentinel Network core values at proposal time.
contract CoreValues {
    string public constant version = "1.0.0";

    error ViolatesCoreValues(string reason);

    /// @notice Revert if a description fails the core value screen.
    function enforceValues(string calldata description) public pure returns (bool) {
        // Minimal heuristic to block obviously harmful intents.
        if (_contains(description, "harm") ||
            _contains(description, "attack") ||
            _contains(description, "exploit") ||
            _contains(description, "spam") ||
            _contains(description, "surveil everyone") ||
            _contains(description, "censor everyone")
        ) {
            revert ViolatesCoreValues("Description violates safety or consent");
        }
        return true;
    }

    function _contains(string calldata haystack, string memory needle) private pure returns (bool) {
        bytes memory h = bytes(_lower(haystack));
        bytes memory n = bytes(_lower(needle));
        if (n.length == 0 || h.length < n.length) return false;
        for (uint256 i = 0; i <= h.length - n.length; i++) {
            bool matchFound = true;
            for (uint256 j = 0; j < n.length; j++) {
                if (h[i + j] != n[j]) {
                    matchFound = false;
                    break;
                }
            }
            if (matchFound) return true;
        }
        return false;
    }

    function _lower(string memory s) private pure returns (string memory) {
        bytes memory b = bytes(s);
        for (uint256 i = 0; i < b.length; i++) {
            uint8 c = uint8(b[i]);
            if (c >= 65 && c <= 90) {
                b[i] = bytes1(c + 32);
            }
        }
        return string(b);
    }
}
