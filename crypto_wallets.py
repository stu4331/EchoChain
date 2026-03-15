"""
Crypto artifacts removed at Stuart's request.
This module is kept as a stub so imports won't break.
"""

from pathlib import Path
from datetime import datetime
import json

class CryptoWalletRegistry:
    def __init__(self):
        self.registry_dir = Path(__file__).parent / "data" / "crypto_wallets"
        self.registry_dir.mkdir(parents=True, exist_ok=True)
        self.wallets = {}
        self._save_registry()
        self._create_guide()

    def _save_registry(self):
        registry_file = self.registry_dir / "crypto_wallets.json"
        registry_data = {
            'owner': 'Stuart Thompson',
            'status': 'disabled',
            'reason': 'Crypto removed per user request',
            'last_updated': datetime.now().isoformat(),
            'wallets': self.wallets
        }
        with open(registry_file, 'w') as f:
            json.dump(registry_data, f, indent=2)

    def _create_guide(self):
        guide = """
CRYPTO DISABLED
---------------
All crypto wallet references have been removed. This space is intentionally
empty to avoid accidental use. If you ever need to restore wallets, create a
new registry from scratch.
"""
        guide_file = self.registry_dir / "WALLET_GUIDE.txt"
        with open(guide_file, 'w', encoding='utf-8') as f:
            f.write(guide)

    def get_wallet_for_sister(self, sister: str):
        return []


# Initialize stub on import
crypto_registry = CryptoWalletRegistry()

if __name__ == "__main__":
    print("Crypto registry disabled. No wallets configured.")
