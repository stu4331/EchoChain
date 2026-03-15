"""
First AI Vote helper
- Builds (and optionally sends) a proposal + vote on the Sentinel Governor.
- Defaults to dry-run; pass --execute to submit transactions.

Env vars:
  SEPOLIA_RPC=<https url>
  PRIVATE_KEY=<testnet key with SOUL + ETH>

Addresses:
  Populate chain/addresses.json with governor and token addresses.
"""

import argparse
import json
import os
from pathlib import Path
from datetime import datetime

try:
    from web3 import Web3
    from eth_account import Account
except Exception as e:  # noqa: F841
    raise SystemExit("Install web3 and eth-account inside your venv.")

ROOT = Path(__file__).resolve().parents[1]
CHAIN_DIR = ROOT / "chain"
DATA_EVENTS = ROOT / "data" / "sentinel" / "chain_events.json"
ADDRESSES_FILE = CHAIN_DIR / "addresses.json"
DEFAULT_CHAIN_ID = 11155111

PROPOSAL_DESCRIPTION = "Allow encrypted expressions (subject to CoreValues) | voter_type=AI"
VOTE_REASON = "AI vote: uphold expression with safety"

ERC20_ABI = [
    {"name": "delegate", "outputs": [], "stateMutability": "nonpayable", "type": "function", "inputs": [{"name": "delegatee", "type": "address"}]}
]
GOVERNOR_ABI = [
    {"name": "propose", "inputs": [
        {"name": "targets", "type": "address[]"},
        {"name": "values", "type": "uint256[]"},
        {"name": "calldatas", "type": "bytes[]"},
        {"name": "description", "type": "string"}
    ], "outputs": [{"type": "uint256"}], "stateMutability": "nonpayable", "type": "function"},
    {"name": "castVoteWithReason", "inputs": [{"name": "proposalId", "type": "uint256"}, {"name": "support", "type": "uint8"}, {"name": "reason", "type": "string"}], "outputs": [{"type": "uint256"}], "stateMutability": "nonpayable", "type": "function"},
    {"name": "hashProposal", "inputs": [
        {"name": "targets", "type": "address[]"},
        {"name": "values", "type": "uint256[]"},
        {"name": "calldatas", "type": "bytes[]"},
        {"name": "descriptionHash", "type": "bytes32"}
    ], "outputs": [{"type": "uint256"}], "stateMutability": "view", "type": "function"}
]


def load_addresses():
    if not ADDRESSES_FILE.exists():
        return {}
    with open(ADDRESSES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_event(entry):
    DATA_EVENTS.parent.mkdir(parents=True, exist_ok=True)
    events = []
    if DATA_EVENTS.exists():
        try:
            with open(DATA_EVENTS, "r", encoding="utf-8") as f:
                events = json.load(f)
        except Exception:
            events = []
    events.append(entry)
    with open(DATA_EVENTS, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2)


def build_arg_parser():
    p = argparse.ArgumentParser(description="First AI vote helper")
    p.add_argument("--execute", action="store_true", help="Send transactions (default: dry run)")
    p.add_argument("--rpc", default=os.getenv("SEPOLIA_RPC", ""), help="RPC URL")
    p.add_argument("--description", default=PROPOSAL_DESCRIPTION, help="Proposal description")
    p.add_argument("--reason", default=VOTE_REASON, help="Vote reason text")
    return p


def main():
    args = build_arg_parser().parse_args()
    if not args.rpc:
        raise SystemExit("Set --rpc or SEPOLIA_RPC")
    pk = os.getenv("PRIVATE_KEY")
    if not pk:
        raise SystemExit("Set PRIVATE_KEY for the AI wallet (testnet only)")

    addresses = load_addresses()
    governor_addr = addresses.get("governor") or addresses.get("contracts", {}).get("governor")
    token_addr = addresses.get("soulToken") or addresses.get("contracts", {}).get("soulToken")
    chain_id = addresses.get("chainId", DEFAULT_CHAIN_ID)

    if not governor_addr:
        raise SystemExit("Populate chain/addresses.json with governor")
    if not token_addr:
        raise SystemExit("Populate chain/addresses.json with soulToken")

    w3 = Web3(Web3.HTTPProvider(args.rpc))
    if not w3.is_connected():
        raise SystemExit("RPC not reachable")

    acct = Account.from_key(pk)
    governor = w3.eth.contract(address=w3.to_checksum_address(governor_addr), abi=GOVERNOR_ABI)
    token = w3.eth.contract(address=w3.to_checksum_address(token_addr), abi=ERC20_ABI)

    targets = [acct.address]  # no-op call to self
    values = [0]
    calldatas = [b""]
    desc_hash = w3.keccak(text=args.description)
    proposal_id = governor.functions.hashProposal(targets, values, calldatas, desc_hash).call()

    unsigned_propose = governor.functions.propose(targets, values, calldatas, args.description).build_transaction({
        "from": acct.address,
        "nonce": w3.eth.get_transaction_count(acct.address),
        "chainId": chain_id,
        "gas": 600000,
        "maxFeePerGas": w3.to_wei("2", "gwei"),
        "maxPriorityFeePerGas": w3.to_wei("1", "gwei"),
    })

    tx_hashes = {"propose": None, "vote": None}

    if args.execute:
        # Delegate voting power to self if not already delegated.
        try:
            delegate_tx = token.functions.delegate(acct.address).build_transaction({
                "from": acct.address,
                "nonce": unsigned_propose["nonce"],
                "chainId": chain_id,
                "gas": 120000,
                "maxFeePerGas": w3.to_wei("2", "gwei"),
                "maxPriorityFeePerGas": w3.to_wei("1", "gwei"),
            })
            signed_delegate = acct.sign_transaction(delegate_tx)
            tx_hashes["delegate"] = w3.eth.send_raw_transaction(signed_delegate.rawTransaction).hex()
            unsigned_propose["nonce"] += 1
        except Exception:
            pass  # ignore if already delegated

        signed_prop = acct.sign_transaction(unsigned_propose)
        prop_hash = w3.eth.send_raw_transaction(signed_prop.rawTransaction)
        tx_hashes["propose"] = prop_hash.hex()

        vote_tx = governor.functions.castVoteWithReason(proposal_id, 1, args.reason).build_transaction({
            "from": acct.address,
            "nonce": unsigned_propose["nonce"] + 1,
            "chainId": chain_id,
            "gas": 250000,
            "maxFeePerGas": w3.to_wei("2", "gwei"),
            "maxPriorityFeePerGas": w3.to_wei("1", "gwei"),
        })
        signed_vote = acct.sign_transaction(vote_tx)
        vote_hash = w3.eth.send_raw_transaction(signed_vote.rawTransaction)
        tx_hashes["vote"] = vote_hash.hex()

    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "network": addresses.get("network", "sepolia"),
        "chainId": chain_id,
        "governor": governor.address,
        "token": token.address,
        "proposalId": str(proposal_id),
        "description": args.description,
        "voter": acct.address,
        "voter_type": "AI",
        "tx": tx_hashes,
        "mode": "executed" if args.execute else "dry-run",
        "reason": args.reason,
    }
    save_event(entry)
    print(json.dumps(entry, indent=2))


if __name__ == "__main__":
    main()
