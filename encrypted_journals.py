import os
import json
from pathlib import Path
from typing import Optional


class EncryptedJournal:
    """
    Minimal sealed journal API. Placeholder encryption (XOR with key bytes).
    Replace with proper cryptography later.
    """
    def __init__(self, base_dir: Path, persona: str, key: Optional[str]):
        self.dir = base_dir / 'journals' / persona.lower()
        self.dir.mkdir(parents=True, exist_ok=True)
        self.key_bytes = (key or 'soul-key').encode('utf-8')

    def _xor(self, data: bytes) -> bytes:
        kb = self.key_bytes
        return bytes(b ^ kb[i % len(kb)] for i, b in enumerate(data))

    def append(self, text: str):
        day = Path(self.dir / 'today.log')
        payload = json.dumps({'t': text}).encode('utf-8')
        enc = self._xor(payload)
        with open(day, 'ab') as f:
            f.write(enc + b'\n')

    def read_all(self) -> str:
        day = Path(self.dir / 'today.log')
        if not day.exists():
            return ''
        out = []
        with open(day, 'rb') as f:
            for line in f:
                dec = self._xor(line.strip())
                try:
                    obj = json.loads(dec.decode('utf-8'))
                    out.append(obj.get('t', ''))
                except Exception:
                    pass
        return '\n'.join(out)
