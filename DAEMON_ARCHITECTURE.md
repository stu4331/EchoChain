# 🏗️ Daemon Architecture — Technical Reference

This document describes the technical design of the three sister daemons
(`erryn_daemon.py`, `viress_daemon.py`, `echochild_daemon.py`) and the
modules they depend on.

---

## Overview

Each sister daemon is a self-contained Python process that:

1. Initialises her own file-system directories on first run
2. Loads (or creates) a personality configuration JSON
3. Loads persistent memory from disk
4. Optionally connects to the OpenAI API for language-model learning
5. Enters a monitoring loop that never exits until interrupted

```
┌────────────────────────────────────────────────────────────────┐
│  erryn_daemon.py          viress_daemon.py      echochild_daemon.py │
│  ┌──────────────┐         ┌──────────────┐      ┌──────────────┐    │
│  │ ErrynDaemon  │         │ ViressDaemon │      │EchochildDaemon│   │
│  └──────┬───────┘         └──────┬───────┘      └──────┬───────┘    │
│         │ _monitor_loop          │                      │            │
│         ▼                        ▼                      ▼            │
│   ┌──────────────────────────────────────────────────────────┐      │
│   │              data/shared_knowledge/                       │      │
│   │   erryn_shared.json   viress_shared.json  echochild_shared│      │
│   │                   sync_state.json                         │      │
│   └──────────────────────────────────────────────────────────┘      │
└────────────────────────────────────────────────────────────────────┘
```

---

## Class Structure

### Common attributes (all daemons)

| Attribute | Type | Purpose |
|-----------|------|---------|
| `name` | `str` | Sister's name (e.g. `"Erryn"`) |
| `emoji` | `str` | Visual identifier (`💙`, `💛`, `💜`) |
| `color` | `str` | Hex colour for GUI |
| `base_dir` | `Path` | Root of the EchoChain project |
| `data_dir` | `Path` | `data/<name>/` — private storage |
| `memory_file` | `Path` | `data/<name>/memory.json` |
| `log_file` | `Path` | `data/<name>/daemon_log.txt` |
| `personality_file` | `Path` | `data/<name>/personality_config.json` |
| `openai_client` | `OpenAI \| None` | API client (None if key absent) |
| `monitoring` | `bool` | Loop-control flag |

### Common methods (all daemons)

| Method | Description |
|--------|-------------|
| `_init_personality()` | Create default personality JSON if absent |
| `_load_memory()` | Deserialise memory from `memory.json` |
| `_save_memory()` | Serialise memory to `memory.json` |
| `_log(message)` | Append timestamped line to log file + stdout |
| `_check_gui_status()` | Return `True` if `data/gui_running.lock` exists |
| `_share_knowledge(item)` | Legacy alias → calls `_broadcast_to_sisters` |
| `_broadcast_to_sisters(item, category)` | Write to shared knowledge via `FamilySync` |
| `_learn_from_sisters()` | Read new entries from sisters' shared files |
| `_monitor_loop()` | Main daemon loop |
| `run()` | Entry point: start loop, handle shutdown |

---

## Daemon-Specific Methods

### ErrynDaemon (erryn_daemon.py)

| Method | Description |
|--------|-------------|
| `_monitor_system()` | Read CPU / memory / disk via psutil |
| `_run_erryn_scripts()` | Discover and log scripts in `data/erryn/scripts/` |

### ViressDaemon (viress_daemon.py)

| Method | Description |
|--------|-------------|
| `_analyze_codebase()` | Count Python files and identify analysis targets |
| `_run_experiments()` | Placeholder for experiment framework |
| `_run_viress_scripts()` | Discover and log scripts in `data/viress/scripts/` |

### EchochildDaemon (echochild_daemon.py)

| Method | Description |
|--------|-------------|
| `_record_dream()` | Write a dream JSON to `data/echochild/dreams/` |
| `_analyze_emotions()` | Placeholder for emotion-detection logic |
| `_create_story()` | Write a story JSON to `data/echochild/stories/` |
| `_run_echochild_scripts()` | Discover and log scripts in `data/echochild/scripts/` |

---

## File Layout

```
EchoChain/
├── erryn_daemon.py
├── viress_daemon.py
├── echochild_daemon.py
├── family_sync.py
├── start_all_sisters.py
└── data/
    ├── gui_running.lock          ← created by GUI on startup
    ├── shared_knowledge/
    │   ├── erryn_shared.json
    │   ├── viress_shared.json
    │   ├── echochild_shared.json
    │   └── sync_state.json
    ├── erryn/
    │   ├── memory.json
    │   ├── personality_config.json
    │   ├── daemon_log.txt
    │   └── scripts/
    ├── viress/
    │   ├── memory.json
    │   ├── personality_config.json
    │   ├── daemon_log.txt
    │   ├── scripts/
    │   └── experiments/
    └── echochild/
        ├── memory.json
        ├── personality_config.json
        ├── daemon_log.txt
        ├── scripts/
        ├── dreams/
        └── stories/
```

---

## Optional Dependencies

| Package | Used by | Fallback |
|---------|---------|---------|
| `psutil` | Erryn — system monitoring | Skipped; `PSUTIL_AVAILABLE = False` |
| `openai` | All sisters — GPT learning | Skipped; `OPENAI_AVAILABLE = False` |

All three daemons handle missing optional dependencies gracefully and continue
running with reduced functionality.

---

## Memory Schema

Each sister's `memory.json` starts with the following keys:

```json
{
  "created": "<ISO timestamp>",
  "conversations": [],
  "learned_insights": [],
  "learned_from_sisters": []
}
```

Daemon-specific extra keys:

- **Erryn**: `security_events`, `system_observations`
- **Viress**: `experiments_conducted`, `optimizations_found`
- **Echochild**: `emotional_observations`, `dreams_recorded`, `stories_written`, `recovery_notes`

---

## Shutdown Behaviour

| Signal | Result |
|--------|--------|
| `KeyboardInterrupt` (Ctrl+C) | Sets `monitoring = False`, logs graceful shutdown |
| Unhandled exception | Logs `FATAL ERROR`, calls `sys.exit(1)` |

---

*See also: SISTERS_GUIDE.md, SYNC_PROTOCOL.md*
