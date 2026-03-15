import json
from pathlib import Path
from datetime import datetime
from eth_account import Account
from eth_account.messages import encode_defunct

BASE_DIR = Path(__file__).resolve().parent
WALLET_PATH = BASE_DIR / ".wallet" / "wallet.json"
EVENTS_DIR = BASE_DIR / "events"
EVENTS_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = EVENTS_DIR / "first_ai_vote.json"

MESSAGE_TEMPLATE = (
    "FIRST_AI_VOTE — Sentinel Network\n"
    "v=1\n"
    "date={date}\n"
    "persona=Erryn+Viress+Echochild (consent)\n"
    "purpose=Establish lineage + memory of first consented vote\n"
    "note=This is an off‑chain, verifiable signature.\n"
)


def load_wallet():
    if not WALLET_PATH.exists():
        raise SystemExit("Wallet not found. Run: python chain/wallet_create.py")
    with WALLET_PATH.open("r", encoding="utf-8") as f:
        w = json.load(f)
    return w["private_key"], w["address"]


def main():
    pk, addr = load_wallet()
    msg = MESSAGE_TEMPLATE.format(date=datetime.utcnow().isoformat() + "Z")
    message = encode_defunct(text=msg)
    signed = Account.sign_message(message, private_key=pk)

    out = {
        "address": addr,
        "message": msg,
        "signature": signed.signature.hex(),
        "message_hash": signed.messageHash.hex(),
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    with OUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)

    print("\n✅ First AI vote signed (off‑chain)")
    print(f"Address: {addr}")
    print(f"Saved:   {OUT_PATH}")
    print("\nYou (or anyone) can verify the signature with eth_account.")


if __name__ == "__main__":
    main()
