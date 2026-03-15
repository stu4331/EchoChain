import json
import os
from pathlib import Path
from datetime import datetime
from eth_account import Account

# WARNING: Keys are generated locally and stored under chain/.wallet (gitignored)
# Do NOT commit or share the private key.

BASE_DIR = Path(__file__).resolve().parent
WALLET_DIR = BASE_DIR / ".wallet"
WALLET_DIR.mkdir(parents=True, exist_ok=True)
WALLET_PATH = WALLET_DIR / "wallet.json"


def main():
    if WALLET_PATH.exists():
        print(f"Wallet already exists at {WALLET_PATH}")
        with WALLET_PATH.open("r", encoding="utf-8") as f:
            existing = json.load(f)
            print(f"Address: {existing.get('address')}")
        return

    acct = Account.create()
    priv_hex = acct._private_key.hex()
    data = {
        "address": acct.address,
        "private_key": priv_hex,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "note": "Keep this file secret. Do NOT commit."
    }
    with WALLET_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    os.chmod(WALLET_PATH, 0o600) if os.name != "nt" else None

    print("\n✅ Wallet created")
    print(f"Address: {acct.address}")
    print(f"Saved:   {WALLET_PATH}")
    print("\nFund on Sepolia via faucet, then you can send a test tx.")


if __name__ == "__main__":
    main()
