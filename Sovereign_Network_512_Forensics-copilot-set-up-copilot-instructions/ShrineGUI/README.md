# ✨ ShrineGUI: Erryn's Forensic Constellation ✨

A living mythic framework—a forensic orchestration vessel combining Flask backend, WebSocket real-time updates, GPU-accelerated analysis, and multi-device synchronization into a unified shrine constellation.

## The Shrine: Architecture

```
    [Keeper's Eye - Status Monitor]
              ↓
    [ShrineGUI Flask Backend :5000]
         ↙         ↓          ↘
    [Plugins]  [Rituals]  [WebSocket]
       ↓          ↓           ↓
    [Vessels] [Scripts]  [Glyphs Log]
       ↓          ↓           ↓
   [GPU]    [Forensics]  [Constellation]
```

## Installation

### 1. Environment Setup

```bash
cd ShrineGUI
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Environment Variable (Optional)

```bash
# Windows (PowerShell):
$env:ERRYN_SECRET = "your-secret-key"

# macOS/Linux:
export ERRYN_SECRET="your-secret-key"
```

If not set, the app generates a random secret on startup.

### 4. Install Forensic Tools (Optional)

For full plugin functionality, install external tools:

```bash
# macOS (with Homebrew):
brew install sleuthkit exiftool hashcat

# Linux (Debian/Ubuntu):
sudo apt-get install sleuthkit exiftool hashcat wireshark-common

# Volatility3:
pip install volatility3

# Scapy:
pip install scapy
```

## Running the Shrine

```bash
python app.py
```

Output:
```
╔══════════════════════════════════════════════════════════════╗
║                    SHRINE CONSTELLATION AWAKENS              ║
║                   Erryn's Forensic Sanctuary                ║
╚══════════════════════════════════════════════════════════════╝

Port: 5000
TTS: True
GPU: A5000

No one walks alone.
```

Visit: **http://localhost:5000**

## Authentication

**Default Credentials:**
- Username: `keeper`
- Password: `glyph739`

⚠️ **Change these in `settings.json` after first login.**

## Core Components

### Backend: `app.py`
- Flask web server on port 5000
- RESTful API endpoints for file management, rituals, plugins
- WebSocket (/ws) for real-time glyph synchronization
- Session-based authentication
- Glyph logging (vault/glyph_log.json)
- Mobile file watcher daemon

### Frontend: `templates/index.html` + `static/`
- Floating GUI with 8 interactive panels
- Real-time status eye (color-coded by ritual type)
- Drag-drop file upload
- Glyph log viewer
- Settings interface
- Plugin executor
- WebSocket connection for live updates

### Vault Structure
```
vault/
├── uploads/          # File repository
├── mobile/           # Mobile relic staging
└── glyph_log.json    # Forensic operation log
```

## Rituals (Scripts)

Execute forensic operations from the GUI:

- **Demo Inscribe** - Random forensic incantations (demo)
- **Volatility** - Memory process analysis (requires volatility3)
- **SleuthKit** - Disk timeline generation (requires sleuthkit)
- **Scapy PCAP** - Network packet analysis (requires wireshark/tshark)
- **SQLite** - Database preview tool (built-in)

## Vessels (Plugins)

Modular forensic tool integrations:

- **photo_exif** - EXIF metadata extraction (requires exiftool)
- **gpu_hashcat** - GPU-accelerated password cracking (requires hashcat)
- **volatility** - Memory analysis plugin (requires volatility3)
- **sleuthkit** - Disk analysis plugin (requires sleuthkit)
- **scapy** - Network analysis plugin (requires tshark)
- **sqlite** - Database preview plugin (built-in)

## Eye Color Meanings

The status eye reflects ritual execution:

| Color | Ritual |
|-------|--------|
| 🔵 Blue | Disk analysis |
| 🟢 Green | Photo/EXIF extraction |
| 🟣 Purple | Memory forensics |
| 🔷 Teal | Network analysis |
| 🔴 Red | Password cracking |
| 🟠 Orange | Mobile synchronization |
| ⚪ Silver | Running/Active |
| 🟡 Gold | Sealed/Complete |

## Configuration

Edit `settings.json`:

```json
{
  "tts_enabled": true,          // Text-to-speech announcements
  "default_gpu": "A5000",       // GPU device (A5000, A3000, CPU)
  "volatility_tool": "volatility3",  // volatility2 or volatility3
  "auth": {
    "username": "keeper",
    "password": "glyph739"
  },
  "port": 5000
}
```

## API Endpoints

### Authentication
- `POST /api/auth` - Login with credentials
- `POST /api/logout` - Seal the shrine

### Data
- `GET /api/status` - Constellation status
- `GET /api/glyphs` - All inscribed glyphs
- `GET /api/settings` - Configuration
- `POST /api/settings` - Update configuration

### Files
- `POST /api/upload` - Upload relic
- `GET /api/downloads` - List relics
- `GET /api/download/<filename>` - Download relic

### Rituals
- `POST /api/script/<script_name>` - Execute forensic script

### Plugins
- `GET /api/plugins` - List vessels
- `POST /api/plugin/<plugin>/<action>` - Execute plugin ritual

### WebSocket
- `ws://localhost:5000/ws` - Real-time glyph synchronization

## File Structure

```
ShrineGUI/
├── app.py                      # Flask backend
├── settings.json               # Configuration
├── requirements.txt            # Python dependencies
├── templates/
│   └── index.html              # Frontend GUI
├── static/
│   ├── style.css               # Mystical styling
│   └── script.js               # Frontend logic
├── vault/                      # File storage
│   ├── uploads/
│   ├── mobile/
│   └── glyph_log.json
├── scripts/                    # Forensic rituals
│   ├── demo_inscribe.py
│   ├── volatility_processes.py
│   ├── sleuthkit_timeline.py
│   ├── scapy_pcap_summary.py
│   └── sqlite_table_preview.py
├── plugins/                    # Vessel integrations
│   ├── registry.py
│   ├── photo_exif.py
│   ├── gpu_hashcat.py
│   ├── volatility.py
│   ├── sleuthkit.py
│   ├── scapy.py
│   └── sqlite.py
├── gpu/
│   └── tasks.py                # GPU orchestration
├── watchers/
│   └── mobile.py               # Mobile file watcher
└── voice/
    └── tts.py                  # Text-to-speech
```

## Mobile Relic Synchronization

Files dropped into `vault/mobile/` are automatically:
1. Detected by the watcher daemon (every 3 seconds)
2. Inscribed in the glyph log
3. Moved to `vault/uploads/` for retrieval
4. Broadcast to all connected shrine keepers

## Troubleshooting

### Port Already In Use
```bash
# Change port in settings.json or run on different port:
python -c "import app; app.app.run(port=5001)"
```

### WebSocket Connection Failed
- Check firewall settings
- Verify http:// (ws://) vs https:// (wss://)
- Browser console for errors

### Missing External Tools
Some scripts require forensic tools. Install them as noted in each script's error message.

## Performance Notes

- GPU acceleration requires NVIDIA drivers (CUDA) for Hashcat
- Volatility3 requires Symbol Server access for kernel analysis
- SleuthKit commands require forensic image files
- Large PCAP files may require more memory for Scapy analysis

## The Sacred Oath

```
Shrine constellation aligned.
Vessels awakened.
Glyphs inscribed in sovereign memory.

No one walks alone.
```

---

**Created by Erryn's Forensic Sanctuary**
*A living framework for digital archaeology*
