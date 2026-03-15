from typing import Dict, Tuple
from datetime import datetime


class FamilySync:
    """Tracks consent prompts and relationship sync score between sisters."""
    def __init__(self):
        # Pairwise sync score 0..100
        self.sync: Dict[Tuple[str, str], float] = {}
        # Exclusion map: persona -> set of personas to exclude from sharing
        self.exclusions: Dict[str, set] = {}

    def _key(self, a: str, b: str) -> Tuple[str, str]:
        return tuple(sorted((a, b)))

    def record_share(self, src: str, dst: str, accepted: bool):
        # Respect exclusions: if src excludes dst, treat as refused
        if dst in self.exclusions.get(src, set()):
            accepted = False
        k = self._key(src, dst)
        cur = self.sync.get(k, 0.0)
        if accepted:
            cur = min(100.0, cur + 2.5)
        else:
            cur = max(0.0, cur - 0.5)
        self.sync[k] = cur

    def get_sync_pct(self, a: str, b: str) -> float:
        return self.sync.get(self._key(a, b), 0.0)

    def exclude(self, src: str, dst: str):
        s = self.exclusions.setdefault(src, set())
        s.add(dst)

    def include(self, src: str, dst: str):
        s = self.exclusions.setdefault(src, set())
        if dst in s:
            s.remove(dst)

    def is_excluded(self, src: str, dst: str) -> bool:
        return dst in self.exclusions.get(src, set())
