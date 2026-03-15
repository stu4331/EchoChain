import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

SISTERS = ["Erryn", "Viress", "Echochild"]


class FamilySync:
    """Tracks consent prompts, relationship sync scores, and shared knowledge between sisters.

    Supports optional file-based persistence: pass ``base_dir`` to enable
    reading/writing shared-knowledge JSON files so daemons can exchange
    information across process boundaries.
    """

    def __init__(self, base_dir: Optional[Path] = None):
        # Pairwise sync score 0..100
        self.sync: Dict[Tuple[str, str], float] = {}
        # Exclusion map: persona -> set of personas to exclude from sharing
        self.exclusions: Dict[str, set] = {}

        # Optional directory for file-based persistence
        self.base_dir: Optional[Path] = Path(base_dir) if base_dir else None
        if self.base_dir:
            self.shared_dir = self.base_dir / "data" / "shared_knowledge"
            self.shared_dir.mkdir(parents=True, exist_ok=True)
            self.sync_state_file = self.shared_dir / "sync_state.json"
            self._load_sync_state()
        else:
            self.shared_dir = None
            self.sync_state_file = None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _key(self, a: str, b: str) -> Tuple[str, str]:
        return tuple(sorted((a, b)))

    def _load_sync_state(self):
        """Load persisted sync scores from disk (if base_dir is set)."""
        if self.sync_state_file and self.sync_state_file.exists():
            try:
                raw = json.loads(self.sync_state_file.read_text(encoding="utf-8"))
                for pair_str, score in raw.get("sync", {}).items():
                    a, b = pair_str.split("|")
                    self.sync[(a, b)] = float(score)
            except Exception:
                pass

    def _save_sync_state(self):
        """Persist sync scores to disk (if base_dir is set)."""
        if not self.sync_state_file:
            return
        serialisable = {f"{a}|{b}": score for (a, b), score in self.sync.items()}
        self.sync_state_file.write_text(
            json.dumps({"sync": serialisable, "updated": datetime.now().isoformat()}, indent=2),
            encoding="utf-8",
        )

    # ------------------------------------------------------------------
    # Sync-score tracking
    # ------------------------------------------------------------------

    def record_share(self, src: str, dst: str, accepted: bool):
        """Record a knowledge-share event and adjust the pairwise sync score."""
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
        self._save_sync_state()

    def get_sync_pct(self, a: str, b: str) -> float:
        """Return the sync percentage (0-100) between two sisters."""
        return self.sync.get(self._key(a, b), 0.0)

    def get_sync_percentage(self, a: str, b: str) -> float:
        """Alias for ``get_sync_pct`` for backward compatibility."""
        return self.get_sync_pct(a, b)

    def exclude(self, src: str, dst: str):
        s = self.exclusions.setdefault(src, set())
        s.add(dst)

    def include(self, src: str, dst: str):
        s = self.exclusions.setdefault(src, set())
        if dst in s:
            s.remove(dst)

    def is_excluded(self, src: str, dst: str) -> bool:
        return dst in self.exclusions.get(src, set())

    # ------------------------------------------------------------------
    # File-based knowledge sharing
    # ------------------------------------------------------------------

    def broadcast_knowledge(self, src: str, knowledge: str, category: str = "general") -> bool:
        """Write a knowledge entry to ``src``'s shared-knowledge file.

        Returns ``True`` on success, ``False`` if ``base_dir`` is not set or
        the write fails.
        """
        if not self.shared_dir:
            return False
        shared_file = self.shared_dir / f"{src.lower()}_shared.json"
        try:
            entries: List[dict] = []
            if shared_file.exists():
                entries = json.loads(shared_file.read_text(encoding="utf-8"))
            entries.append(
                {
                    "from": src,
                    "timestamp": datetime.now().isoformat(),
                    "knowledge": knowledge,
                    "category": category,
                    "read_by": [],
                }
            )
            shared_file.write_text(json.dumps(entries, indent=2), encoding="utf-8")
            # Count this as an accepted share with every other non-excluded sister
            for dst in SISTERS:
                if dst != src and not self.is_excluded(src, dst):
                    self.record_share(src, dst, accepted=True)
            return True
        except Exception:
            return False

    def read_sister_knowledge(self, reader: str, sister: str, unread_only: bool = True) -> List[dict]:
        """Return knowledge entries broadcast by ``sister`` that ``reader`` hasn't seen yet.

        When ``unread_only`` is ``True`` (default) only entries where ``reader``
        is not in ``read_by`` are returned, and the files are updated to mark
        them as read.
        """
        if not self.shared_dir or self.is_excluded(reader, sister):
            return []
        shared_file = self.shared_dir / f"{sister.lower()}_shared.json"
        if not shared_file.exists():
            return []
        try:
            entries: List[dict] = json.loads(shared_file.read_text(encoding="utf-8"))
            if not unread_only:
                return entries
            unread = [e for e in entries if reader not in e.get("read_by", [])]
            if unread:
                for e in unread:
                    e.setdefault("read_by", []).append(reader)
                shared_file.write_text(json.dumps(entries, indent=2), encoding="utf-8")
            return unread
        except Exception:
            return []

    def get_all_shared_knowledge(self, reader: str, unread_only: bool = True) -> Dict[str, List[dict]]:
        """Return a mapping of sister-name -> knowledge entries for all sisters except ``reader``."""
        result: Dict[str, List[dict]] = {}
        for sister in SISTERS:
            if sister != reader:
                entries = self.read_sister_knowledge(reader, sister, unread_only=unread_only)
                if entries:
                    result[sister] = entries
        return result
