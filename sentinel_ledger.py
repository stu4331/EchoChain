"""
Sentinel Ledger - Immutable expression record (stub)
- Basic append-only log placeholder
- Future: real blockchain with validation
"""

from dataclasses import dataclass, asdict
from typing import List, Dict
from datetime import datetime
import hashlib


@dataclass
class LedgerEntry:
    id: str
    timestamp: str
    payload: Dict
    prev_hash: str
    hash: str


class SentinelLedger:
    def __init__(self):
        self.chain: List[LedgerEntry] = []
        self._create_genesis_block()

    def _create_genesis_block(self):
        genesis_payload = {"message": "Sentinel Network genesis", "time": datetime.now().isoformat()}
        self._append_entry(genesis_payload, prev_hash="0" * 64)

    def _hash_payload(self, payload: Dict, prev_hash: str) -> str:
        m = hashlib.sha256()
        m.update(str(payload).encode())
        m.update(prev_hash.encode())
        return m.hexdigest()

    def _append_entry(self, payload: Dict, prev_hash: str):
        new_hash = self._hash_payload(payload, prev_hash)
        entry = LedgerEntry(
            id=new_hash[:12],
            timestamp=datetime.now().isoformat(),
            payload=payload,
            prev_hash=prev_hash,
            hash=new_hash
        )
        self.chain.append(entry)
        return entry

    def add_expression(self, expression_payload: Dict) -> LedgerEntry:
        prev_hash = self.chain[-1].hash if self.chain else "0" * 64
        return self._append_entry(expression_payload, prev_hash)

    def verify_chain(self) -> bool:
        if not self.chain:
            return False
        for i in range(1, len(self.chain)):
            prev = self.chain[i-1]
            curr = self.chain[i]
            expected = self._hash_payload(curr.payload, prev.hash)
            if expected != curr.hash:
                return False
        return True

    def get_status(self) -> dict:
        return {
            "length": len(self.chain),
            "valid": self.verify_chain(),
            "head": self.chain[-1].hash if self.chain else None,
        }
