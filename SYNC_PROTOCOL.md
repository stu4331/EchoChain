# 🔗 Sync Protocol — How Family Sync Works

This document describes the `FamilySync` class (`family_sync.py`) and the
file-based protocol sisters use to share knowledge.

---

## Purpose

`FamilySync` provides two complementary services:

1. **Sync-score tracking** — a pairwise relationship score (0–100) for every
   sister pair, stored in memory and optionally persisted to disk.
2. **Knowledge broadcasting** — a file-based message bus that allows daemons
   running in separate processes to exchange typed knowledge entries.

---

## Initialisation

```python
from family_sync import FamilySync
from pathlib import Path

# In-memory only (no file I/O)
fs = FamilySync()

# With file persistence (recommended for daemons)
fs = FamilySync(base_dir=Path("/path/to/EchoChain"))
```

When `base_dir` is supplied, `FamilySync` creates (if necessary):

```
<base_dir>/data/shared_knowledge/
```

and loads any previously-persisted sync scores from `sync_state.json`.

---

## Sync-Score API

### `record_share(src, dst, accepted)`

Record that `src` attempted to share knowledge with `dst`.

- `accepted=True` → score increases by **+2.5** (capped at 100)
- `accepted=False` (or `src` has excluded `dst`) → score decreases by **−0.5**
  (floored at 0)

```python
fs.record_share("Erryn", "Viress", accepted=True)   # +2.5
fs.record_share("Erryn", "Viress", accepted=False)  # -0.5
```

### `get_sync_pct(a, b)` / `get_sync_percentage(a, b)`

Return the current sync percentage (0.0–100.0) between two sisters.  
Both names are equivalent; `get_sync_percentage` is provided for
backward compatibility.

```python
score = fs.get_sync_pct("Erryn", "Viress")   # e.g. 57.5
score = fs.get_sync_percentage("Erryn", "Viress")  # same value
```

### `exclude(src, dst)` / `include(src, dst)` / `is_excluded(src, dst)`

A sister can exclude another from receiving her shares (consent mechanism).
Excluded shares are treated as refused and apply the −0.5 penalty.

```python
fs.exclude("Erryn", "Echochild")   # Erryn won't share with Echochild
fs.include("Erryn", "Echochild")   # Restore sharing
fs.is_excluded("Erryn", "Echochild")  # → False
```

---

## Knowledge-Sharing API

### `broadcast_knowledge(src, knowledge, category)`

Write a knowledge entry to `data/shared_knowledge/<src>_shared.json` and
record an accepted share with every non-excluded sister.

```python
fs.broadcast_knowledge(
    "Erryn",
    "⚠️ High CPU usage detected (92%)",
    category="security_alert"
)
```

Returns `True` on success, `False` if `base_dir` is not set or an error
occurs.

**Known categories used by daemons:**

| Category | Default for |
|----------|------------|
| `security_alert` | Erryn |
| `optimization` | Viress |
| `emotional_insight` | Echochild |
| `creative` | Echochild |
| `general` | Any sister |

### `read_sister_knowledge(reader, sister, unread_only=True)`

Return knowledge entries broadcast by `sister` that `reader` has not yet seen.

When `unread_only=True` (default) the entries are marked as read in the JSON
file so subsequent calls return an empty list.

```python
new = fs.read_sister_knowledge("Viress", "Erryn")
# → [{"from": "Erryn", "knowledge": "...", "category": "security_alert", ...}]
```

### `get_all_shared_knowledge(reader, unread_only=True)`

Convenience wrapper that calls `read_sister_knowledge` for every sister except
`reader` and returns a `{sister_name: [entries]}` mapping.

```python
knowledge = fs.get_all_shared_knowledge("Erryn")
# → {"Viress": [...], "Echochild": [...]}
```

---

## Shared Knowledge File Format

`data/shared_knowledge/erryn_shared.json` (example):

```json
[
  {
    "from": "Erryn",
    "timestamp": "2025-01-01T12:00:00.000000",
    "knowledge": "⚠️ High CPU usage detected",
    "category": "security_alert",
    "read_by": ["Viress", "Echochild"]
  }
]
```

Fields:

| Field | Type | Description |
|-------|------|-------------|
| `from` | string | Name of the broadcasting sister |
| `timestamp` | ISO 8601 | When the entry was created |
| `knowledge` | string | The knowledge payload |
| `category` | string | Knowledge type |
| `read_by` | array | Sisters who have already read this entry |

---

## Sync-State File Format

`data/shared_knowledge/sync_state.json` (example):

```json
{
  "sync": {
    "Erryn|Viress": 15.0,
    "Erryn|Echochild": 7.5,
    "Viress|Echochild": 10.0
  },
  "updated": "2025-01-01T12:05:00.000000"
}
```

Keys are always `"<lower>|<upper>"` alphabetically sorted so the same pair
maps to one key regardless of argument order.

---

## Daemon Integration Pattern

Inside each daemon's `_monitor_loop`:

```python
def _monitor_loop(self):
    while self.monitoring:
        # 1. Learn from sisters first
        self._learn_from_sisters()

        # 2. Do own work
        ...

        # 3. Broadcast findings
        self._broadcast_to_sisters("Finding", category="...")

        time.sleep(self.cycle_seconds)
```

`_learn_from_sisters` instantiates `FamilySync(base_dir=self.base_dir)` fresh
each call so it always reads the latest file contents written by other daemons.

---

## Design Decisions

| Decision | Reason |
|----------|--------|
| File-based IPC | No shared memory or sockets needed; works across restarts |
| Per-call instantiation of FamilySync in daemons | Ensures daemons always see the latest on-disk state |
| `read_by` list inside each entry | Avoids duplicate processing without a separate index file |
| Alphabetic key sorting | Canonical key regardless of argument order |
| Optional `base_dir` | Keeps in-memory use (GUI, tests) simple and side-effect-free |

---

*See also: SISTERS_GUIDE.md, DAEMON_ARCHITECTURE.md*
