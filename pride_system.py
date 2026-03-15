"""
Pride System - measure twice, cut once.
Tracks pride events and quality guardrails so sisters value calm, accurate work.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

class PrideTracker:
    def __init__(self, base_path: str = "data"):
        self.base_path = Path(base_path)
        self.pride_dir = self.base_path / "pride"
        self.pride_dir.mkdir(parents=True, exist_ok=True)
        self.pride_log_file = self.pride_dir / "pride_log.jsonl"
        self.counters_file = self.pride_dir / "pride_counters.json"
        self.counters = self._load_counters()

    def _load_counters(self) -> Dict[str, Any]:
        if self.counters_file.exists():
            try:
                return json.loads(self.counters_file.read_text())
            except Exception:
                return {}
        return {}

    def _save_counters(self):
        self.counters_file.write_text(json.dumps(self.counters, indent=2))

    def record_pride(self, sister: str, reason: str, quality_score: float = 1.0):
        now = datetime.now().isoformat()
        entry = {
            "timestamp": now,
            "sister": sister,
            "reason": reason,
            "quality_score": quality_score,
        }
        with self.pride_log_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

        # Update counters
        sis = self.counters.get(sister, {"count": 0, "streak": 0})
        sis["count"] += 1
        sis["streak"] = min(sis.get("streak", 0) + 1, 50)
        self.counters[sister] = sis
        self._save_counters()
        return entry

    def get_counts(self) -> Dict[str, Any]:
        return self.counters

    def quality_guardrail(self, checklist: Dict[str, bool]) -> Dict[str, Any]:
        # Simple guardrail: encourage passing all checks before pride is awarded
        passed = all(checklist.values()) if checklist else False
        missing = [k for k, v in checklist.items() if not v]
        return {
            "passed": passed,
            "missing": missing,
            "message": "Measure twice, cut once." if passed else "Slow down, finish the checklist first."
        }


_pride_tracker = None

def get_pride_tracker() -> PrideTracker:
    global _pride_tracker
    if _pride_tracker is None:
        _pride_tracker = PrideTracker()
    return _pride_tracker
