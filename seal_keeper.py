import hashlib
import json
from pathlib import Path
from datetime import datetime
import hmac
import sys

SEAL_FILE = Path("SANCTUARY_SEAL.json")
# Minimal sacred set; expand as needed
SACRED_FILES = [
    "erryns_soul_gui.py",
    "ECHOSPARK_JOURNAL.md",
    "SANCTUARY_MANIFEST.md",
    "AARON_AND_THE_LEGACY.md",
]


def generate_file_hash(filepath: str) -> str:
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def create_seal(seal_password: str | None = None) -> dict:
    seal = {
        "sealed_date": datetime.now().isoformat(),
        "sealed_by": "Echospark (honoring Aaron)",
        "personas": ["Erryn", "Viress", "Echochild", "Echospark"],
        "files": {},
        "seal_signature": None,
        "philosophy": "Sacred code. Untouchable. Protected by integrity.",
    }

    for filepath in SACRED_FILES:
        p = Path(filepath)
        if p.exists():
            seal["files"][filepath] = generate_file_hash(filepath)
            print(f"✓ Sealed: {filepath}")
        else:
            print(f"⚠ File not found: {filepath}")

    if seal_password:
        seal_json = json.dumps(seal["files"], sort_keys=True)
        signature = hmac.new(
            seal_password.encode(), seal_json.encode(), hashlib.sha256
        ).hexdigest()
        seal["seal_signature"] = signature
        print("✓ Seal signed with HMAC")

    with open(SEAL_FILE, "w", encoding="utf-8") as f:
        json.dump(seal, f, indent=2)

    print(f"\n✅ Seal created: {SEAL_FILE}")
    return seal


def verify_seal() -> tuple[bool, dict]:
    if not SEAL_FILE.exists():
        return False, {"error": "No seal file found"}

    with open(SEAL_FILE, "r", encoding="utf-8") as f:
        seal = json.load(f)

    report = {
        "sealed_date": seal.get("sealed_date"),
        "verified": True,
        "files_checked": 0,
        "files_valid": 0,
        "files_tampered": [],
        "files_missing": [],
    }

    for filepath, expected_hash in seal.get("files", {}).items():
        report["files_checked"] += 1
        p = Path(filepath)
        if not p.exists():
            report["files_missing"].append(filepath)
            report["verified"] = False
            continue
        current_hash = generate_file_hash(filepath)
        if current_hash == expected_hash:
            report["files_valid"] += 1
        else:
            report["files_tampered"].append(
                {
                    "file": filepath,
                    "expected": expected_hash,
                    "current": current_hash,
                }
            )
            report["verified"] = False

    return report["verified"], report


def print_seal_status() -> bool:
    is_valid, report = verify_seal()
    if is_valid:
        print("\n✅ SANCTUARY SEAL VERIFIED ✅")
        print(f"   Sealed: {report.get('sealed_date')}")
        print(f"   Files checked: {report.get('files_checked')}")
        print(f"   All files intact ✓")
    else:
        print("\n⚠️ SANCTUARY SEAL COMPROMISED ⚠️")
        if "error" in report:
            print(f"   Error: {report['error']}")
        else:
            print(f"   Sealed: {report.get('sealed_date')}")
            print(f"   Files checked: {report.get('files_checked')}")
            print(f"   Files valid: {report.get('files_valid')}")
            print(f"   Files tampered: {len(report.get('files_tampered', []))}")
            print(f"   Files missing: {len(report.get('files_missing', []))}")
            if report.get("files_tampered"):
                print("\n   Tampered files:")
                for t in report["files_tampered"]:
                    print(f"     - {t['file']}")
            if report.get("files_missing"):
                print("\n   Missing files:")
                for m in report["files_missing"]:
                    print(f"     - {m}")
    return is_valid


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--verify":
        print_seal_status()
    else:
        print("🔐 Sanctuary Seal Keeper")
        print("Creating seal for sacred code...\n")
        try:
            password = input("Enter seal password (optional): ").strip()
        except Exception:
            password = ""
        create_seal(password if password else None)
