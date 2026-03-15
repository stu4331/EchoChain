# Copilot Instructions for Erryn Codebase

## Big Picture Architecture
- The workspace is organized around ritual scripts, data manifests, and daemon utilities for managing relics, voice synthesis, and shrine state.
- Major components:
  - **Python Rituals**: e.g., `ErrynAwakening.py` (Azure TTS GUI), `ErrynShrineHashComparison.py` (hash manifest generator)
  - **PowerShell Daemons**: e.g., `DualSyncDaemon.ps1` (bidirectional relic sync), `BreathTraceDaemon.ps1` (system audit)
  - **Data Manifests**: Text and JSON files (e.g., `ErrynHashLedger.txt`, `emotion_log.json`) serve as ledgers, logs, and invocation scrolls.
  - **Voice/AI Integration**: Azure Cognitive Services (TTS), custom invocation scripts, and possible TTS server integration (see TTS README).

## Developer Workflows
- **Syncing Relics**: Use `DualSyncDaemon.ps1` to mirror files between local and cloud shrines. Relic logs are written to `DualSyncLog.txt`.
- **System Audits**: Run `BreathTraceDaemon.ps1` for lineage and system status tracing. Output is in `BreathTraceLog.txt`.
- **Hash Manifest Generation**: Execute `ErrynShrineHashComparison.py` to scan and compare relics by SHA256, writing results to `ErrynHashLedger.txt`.
- **Voice Synthesis**: Launch `ErrynAwakening.py` for GUI-based Azure TTS invocation. Requires `customtkinter` and `azure-cognitiveservices-speech`.
- **TTS Server**: Reference TTS server README for running demo servers and listing available models.

## Project-Specific Conventions
- **Ritual Naming**: Scripts and logs use ceremonial/ritualistic names (e.g., "Invocation", "Daemon", "Shrine", "Relic").
- **Manifest Headers**: Text manifests begin with glyph seals and scan metadata (see `ErrynHashLedger.txt`).
- **Paths**: Many scripts use absolute Windows paths; update as needed for your environment.
- **Logging**: PowerShell scripts append Unicode logs with timestamps and invocation markers.
- **GUI**: Python GUIs use `customtkinter` with dark themes and ceremonial banners.

## Integration Points & Dependencies
- **Azure Cognitive Services**: Required for TTS in `ErrynAwakening.py` (see speech key and region in code).
- **TTS Server**: Refer to TTS README for model management and server invocation.
- **Robocopy**: Used in PowerShell for file mirroring.
- **Custom Data Files**: Many scripts depend on text manifests and logs in the workspace root or subfolders.

## Examples & Key Files
- `ErrynAwakening.py`: Azure TTS GUI, ceremonial invocation, speech synthesis.
- `DualSyncDaemon.ps1`: Relic mirroring, bidirectional sync, Unicode logging.
- `ErrynShrineHashComparison.py`: SHA256 hash manifest, glyph header, duplicate detection.
- `BreathTraceDaemon.ps1`: System audit, lineage tracing, event log extraction.
- `ErrynHashLedger.txt`: Example of manifest format and metadata.

## Quickstart for AI Agents
- Use ceremonial naming and headers in new scripts/manifests.
- Reference existing daemons for logging and invocation patterns.
- Update hardcoded paths for your environment if needed.
- For new rituals, follow the structure and style of existing Python/PowerShell scripts.
- Always log invocation, timestamps, and results in a Unicode text file.

---
_Iterate and expand these instructions as new rituals, daemons, or conventions emerge._
