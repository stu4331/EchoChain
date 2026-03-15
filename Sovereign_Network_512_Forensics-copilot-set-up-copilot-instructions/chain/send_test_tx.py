import json
import os
from pathlib import Path
from web3 import Web3
from eth_account import Account

BASE_DIR = Path(__file__).resolve().parent
WALLET_PATH = BASE_DIR / ".wallet" / "wallet.json"
ENV_PATH = BASE_DIR / ".env"


def load_env(path: Path):
    if not path.exists():
        return {}
    env = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip()
    return env


def main():
    if not WALLET_PATH.exists():
        raise SystemExit("Wallet not found. Run: python chain/wallet_create.py")
    with WALLET_PATH.open("r", encoding="utf-8") as f:
        w = json.load(f)

    env = load_env(ENV_PATH)
    rpc = env.get("SEPOLIA_RPC") or os.environ.get("SEPOLIA_RPC")
    if not rpc:
        raise SystemExit("SEPOLIA_RPC not set in chain/.env or environment.")

    w3 = Web3(Web3.HTTPProvider(rpc))
    if not w3.is_connected():
        raise SystemExit("Could not connect to RPC. Check SEPOLIA_RPC.")

    acct = Account.from_key(w["private_key"])
    sender = acct.address
    nonce = w3.eth.get_transaction_count(sender)

    # Self‑tx with 0 ETH; optional data for provenance
    tx = {
        "to": sender,
        "value": 0,
        "nonce": nonce,
        "gas": 21000,
        "maxFeePerGas": w3.to_wei(2, 'gwei'),
        "maxPriorityFeePerGas": w3.to_wei(1, 'gwei'),
        "chainId": w3.eth.chain_id,
    }

    signed = acct.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    print("\n✅ Sent test tx (self‑ping)")
    print(f"From/To: {sender}")
    print(f"Hash:    {tx_hash.hex()}")


if __name__ == "__main__":
    main()
