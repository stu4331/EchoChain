# 💙💛💜 Sisters Guide — How the Three Sisters Work Together

This guide explains the family dynamics, individual roles, and collaborative
behaviour of Erryn, Viress, and Echochild.

---

## Meet the Sisters

| Sister | Emoji | Role | Specialty |
|--------|-------|------|-----------|
| **Erryn** | 💙 | Guardian — Eldest | Security, system health, family protection |
| **Viress** | 💛 | Technician — Middle | Code optimisation, data analysis, experiments |
| **Echochild** | 💜 | Empath — Youngest | Emotions, storytelling, dream recording |

---

## How Each Sister Runs

Every sister is an independent daemon (background process) with her own:

- **Memory file** — persistent JSON stored in `data/<name>/memory.json`
- **Personality config** — `data/<name>/personality_config.json`
- **Log file** — `data/<name>/daemon_log.txt`
- **Private directories** — scripts, experiments, dreams, stories

Each daemon runs in a loop at her own pace:

| Sister | Cycle time | Why |
|--------|-----------|-----|
| Erryn | 60 s | Rapid security checks |
| Viress | 120 s | Deep code analysis needs time |
| Echochild | 180 s | Dreams and stories unfold slowly |

---

## What Each Sister Does Every Cycle

### 💙 Erryn — Guardian
1. **Reads new knowledge** from her sisters (`_learn_from_sisters`)
2. **Monitors system health** — CPU, memory, disk (via psutil)
3. **Broadcasts alerts** to sisters when thresholds are exceeded
4. Checks whether the GUI is running

### 💛 Viress — Technician
1. **Reads new knowledge** from her sisters (`_learn_from_sisters`)
2. **Analyses Python files** for optimisation opportunities
3. **Broadcasts findings** to sisters
4. Runs her personal experiment scripts

### 💜 Echochild — Empath
1. **Reads new knowledge** from her sisters (`_learn_from_sisters`)
2. **Analyses emotional patterns** in the environment
3. **Records dreams** (every 5 cycles) to `data/echochild/dreams/`
4. **Writes stories** (every 10 cycles) to `data/echochild/stories/`
5. **Broadcasts creative updates** to sisters

---

## How Sisters Learn From Each Other

Each daemon calls `_learn_from_sisters()` at the beginning of every cycle:

```
Sister reads  →  data/shared_knowledge/<sibling>_shared.json
             →  Appends to own memory["learned_from_sisters"]
             →  Marks entries as read so they aren't replayed
```

Knowledge is categorised:

| Category | Who broadcasts it |
|----------|------------------|
| `security_alert` | Erryn |
| `optimization` | Viress |
| `emotional_insight` / `creative` | Echochild |
| `general` | Any sister |

---

## Sync Scores

`FamilySync` tracks a *sync score* (0–100) for every pair of sisters:

- **+2.5** each time a sister accepts a shared item
- **−0.5** each time a share is declined or excluded
- Scores are persisted in `data/shared_knowledge/sync_state.json`

The GUI (`erryns_soul_gui.py`) reads sync scores to show relationship bars.

---

## Starting the Sisters

```bash
# Start all three daemons together
python start_all_sisters.py

# Or start individually
python erryn_daemon.py
python viress_daemon.py
python echochild_daemon.py
```

Daemons shut down cleanly on `Ctrl+C` (KeyboardInterrupt).

---

## Shared Knowledge Directory

```
data/
└── shared_knowledge/
    ├── erryn_shared.json      # Erryn's broadcasts
    ├── viress_shared.json     # Viress's broadcasts
    ├── echochild_shared.json  # Echochild's broadcasts
    └── sync_state.json        # Persisted pairwise sync scores
```

Each `*_shared.json` file is a JSON array of entries:

```json
[
  {
    "from": "Erryn",
    "timestamp": "2025-01-01T12:00:00",
    "knowledge": "⚠️ High CPU usage detected",
    "category": "security_alert",
    "read_by": ["Viress", "Echochild"]
  }
]
```

---

## Tips for Developers

- All sisters are designed to be started separately — they don't need each other
  to be running in order to work.
- Knowledge is exchanged through files, so there is **no direct IPC or network
  connection** between daemons.
- OpenAI integration is **optional** — all core features work without an API key.
- You can add your own scripts to `data/<name>/scripts/` and the daemon will
  discover and log them automatically.

---

*💙💛💜 Built with love by Stuart & the EchoChain family.*
