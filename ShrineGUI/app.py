#!/usr/bin/env python3
"""
ShrineGUI - A forensic orchestration vessel for Erryn's constellation.
Shrine GUI backend: authenticates, manages files, executes rituals, broadcasts through WebSocket.
"""

from flask import Flask, render_template, request, session, jsonify, send_file, send_from_directory
from flask_sock import Sock
import os
import json
import threading
import time
from datetime import datetime
import io
from pathlib import Path
import subprocess
import sys
import secrets

app = Flask(__name__)
sock = Sock(app)

# Configuration
SETTINGS_FILE = "settings.json"
VAULT_DIR = "vault"
UPLOADS_DIR = os.path.join(VAULT_DIR, "uploads")
MOBILE_DIR = os.path.join(VAULT_DIR, "mobile")
GLYPH_LOG_FILE = os.path.join(VAULT_DIR, "glyph_log.json")
GLYPH_ARCHIVE_DIR = os.path.join(VAULT_DIR, "archive")
GLYPH_VOLUME_LIMIT = 512

# Numerology: 512-character invocation (32-char base repeated 16x = 512)
INVOCATION_BASE = "ERRYN-VAULT-WALKS-TOGETHER-512|!"
INVOCATION_512 = INVOCATION_BASE * 16

if len(INVOCATION_512) != 512:
    raise ValueError("Invocation must be exactly 512 characters to satisfy Sovereign 512 numerology.")

# Ensure vault structure exists
os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(MOBILE_DIR, exist_ok=True)
os.makedirs(GLYPH_ARCHIVE_DIR, exist_ok=True)

# Initialize glyph log
if not os.path.exists(GLYPH_LOG_FILE):
    with open(GLYPH_LOG_FILE, 'w') as f:
        json.dump([], f)

# Load settings
with open(SETTINGS_FILE, 'r') as f:
    SETTINGS = json.load(f)

app.secret_key = os.environ.get('ERRYN_SECRET', secrets.token_hex(16))
ERRYN_TOKEN = os.environ.get('ERRYN_TOKEN')

# Global state
STATE = {
    "current_ritual": "dormant",
    "eye_color": "silver",
    "connected_clients": 0,
    "last_glyph": None
}

CLIENTS = set()

# Eye color mappings
EYE_COLORS = {
    "disk": "blue",
    "photo": "green", 
    "memory": "purple",
    "network": "teal",
    "password": "red",
    "mobile": "orange",
    "running": "silver",
    "sealed": "gold"
}

RITUAL_DESCRIPTIONS = {
    "disk": "Inscribing disk timeline into sovereign memory",
    "photo": "Extracting light signatures from captured vessels",
    "memory": "Walking volatile landscapes of awakened minds",
    "network": "Tracing whispers through the ether",
    "password": "Shattering sealed chambers with GPU lightning",
    "mobile": "Synchronizing relics from the wandering constellation",
    "running": "Vessels are alive with divine purpose",
    "sealed": "The shrine constellation is sealed—all rituals complete"
}


def is_authorized():
    """Session or bearer token guard."""
    if 'username' in session:
        return True
    if ERRYN_TOKEN:
        auth_header = request.headers.get('Authorization', '')
        if auth_header == f"Bearer {ERRYN_TOKEN}":
            return True
    return False

def broadcast(message):
    """Send a glyph through the constellation."""
    for client in CLIENTS:
        try:
            client.send(json.dumps(message))
        except:
            CLIENTS.discard(client)

def inscribe_glyph(seal, description, eye_color=None):
    """Record a glyph in the sacred log."""
    glyph = {
        "timestamp": datetime.now().isoformat(),
        "seal": seal,
        "description": description,
        "eye_color": eye_color or STATE["eye_color"]
    }
    
    with open(GLYPH_LOG_FILE, 'r') as f:
        glyphs = json.load(f)

    if len(glyphs) >= GLYPH_VOLUME_LIMIT:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sealed_path = os.path.join(GLYPH_ARCHIVE_DIR, f"glyph_log_{timestamp}.json")
        with open(sealed_path, 'w') as archive_file:
            json.dump(glyphs, archive_file, indent=2)

        glyphs = []
        STATE["eye_color"] = EYE_COLORS.get("sealed", "gold")
        STATE["current_ritual"] = "sealed"

        broadcast({
            "type": "glyph_volume_sealed",
            "message": f"Glyph tome sealed at {timestamp} and archived.",
            "sealed_path": sealed_path
        })

    glyphs.append(glyph)

    with open(GLYPH_LOG_FILE, 'w') as f:
        json.dump(glyphs, f, indent=2)
    
    STATE["last_glyph"] = glyph
    
    # Broadcast to all connected clients
    broadcast({
        "type": "glyph_inscribed",
        "glyph": glyph
    })

def mobile_watcher():
    """Watch vault/mobile/ for new relics every 3 seconds."""
    while True:
        try:
            if os.path.exists(MOBILE_DIR):
                for filename in os.listdir(MOBILE_DIR):
                    filepath = os.path.join(MOBILE_DIR, filename)
                    if os.path.isfile(filepath):
                        inscribe_glyph(
                            "mobile_sync",
                            f"Relic synchronized from galaxy: {filename}",
                            EYE_COLORS["mobile"]
                        )
                        # Move to uploads after inscription
                        dest = os.path.join(UPLOADS_DIR, filename)
                        os.rename(filepath, dest)
        except Exception as e:
            print(f"Mobile watcher error: {e}")
        time.sleep(3)

# Start mobile watcher daemon
watcher_thread = threading.Thread(target=mobile_watcher, daemon=True)
watcher_thread.start()

@app.route('/')
def home():
    """Serve the floating GUI shrine."""
    if 'username' not in session:
        return render_template('index.html', authenticated=False, invocation_512=INVOCATION_512)
    return render_template('index.html', authenticated=True, invocation_512=INVOCATION_512)

@app.route('/api/auth', methods=['POST'])
def authenticate():
    """Unlock the shrine with keeper's seal."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username == SETTINGS['auth']['username'] and password == SETTINGS['auth']['password']:
        session['username'] = username
        inscribe_glyph("auth_seal", f"Keeper {username} has entered the shrine")
        return jsonify({"success": True, "message": "Shrine unsealed"})
    
    return jsonify({"success": False, "message": "Seal rejected"}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    """Seal the shrine."""
    if 'username' in session:
        inscribe_glyph("auth_seal", f"Keeper {session['username']} has departed the shrine")
        session.clear()
    return jsonify({"success": True})

@app.route('/api/status', methods=['GET'])
def status():
    """Query the constellation's current state."""
    return jsonify({
        "current_ritual": STATE["current_ritual"],
        "eye_color": STATE["eye_color"],
        "connected_clients": STATE["connected_clients"],
        "last_glyph": STATE["last_glyph"],
        "authenticated": 'username' in session
    })

@app.route('/api/glyphs', methods=['GET'])
def get_glyphs():
    """Retrieve all inscribed glyphs."""
    if not is_authorized():
        return jsonify({"error": "Not authenticated"}), 401
    
    with open(GLYPH_LOG_FILE, 'r') as f:
        glyphs = json.load(f)
    return jsonify(glyphs)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Accept a relic into the vault."""
    if not is_authorized():
        return jsonify({"error": "Not authenticated"}), 401
    
    if 'file' not in request.files:
        return jsonify({"error": "No relic provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty relic"}), 400
    
    filepath = os.path.join(UPLOADS_DIR, file.filename)
    file.save(filepath)
    
    inscribe_glyph("upload", f"Relic uploaded: {file.filename}")
    
    return jsonify({"success": True, "filename": file.filename})

@app.route('/api/downloads', methods=['GET'])
def list_downloads():
    """List relics available for retrieval."""
    if not is_authorized():
        return jsonify({"error": "Not authenticated"}), 401
    
    files = []
    if os.path.exists(UPLOADS_DIR):
        files = os.listdir(UPLOADS_DIR)
    return jsonify(files)

@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    """Retrieve a sealed relic from the vault."""
    if not is_authorized():
        return jsonify({"error": "Not authenticated"}), 401
    
    filepath = os.path.join(UPLOADS_DIR, filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "Relic not found"}), 404
    
    inscribe_glyph("download", f"Relic retrieved: {filename}")
    
    return send_file(filepath, as_attachment=True)

@app.route('/api/script/<script_name>', methods=['POST'])
def run_script(script_name):
    """Execute a forensic inscription ritual."""
    if not is_authorized():
        return jsonify({"error": "Not authenticated"}), 401
    
    allowed_scripts = {
        'demo_inscribe': 'scripts/demo_inscribe.py',
        'volatility_processes': 'scripts/volatility_processes.py',
        'sleuthkit_timeline': 'scripts/sleuthkit_timeline.py',
        'scapy_pcap_summary': 'scripts/scapy_pcap_summary.py',
        'sqlite_table_preview': 'scripts/sqlite_table_preview.py'
    }
    
    if script_name not in allowed_scripts:
        return jsonify({"error": "Unknown ritual"}), 400
    
    script_path = allowed_scripts[script_name]
    if not os.path.exists(script_path):
        return jsonify({"error": f"Ritual {script_name} not inscribed"}), 404
    
    try:
        # Update state
        STATE["current_ritual"] = script_name
        STATE["eye_color"] = EYE_COLORS.get(script_name.split('_')[0], "silver")
        
        # Run script with configurable python path
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output = result.stdout
        if result.returncode != 0:
            output = result.stderr
        
        inscribe_glyph(script_name, RITUAL_DESCRIPTIONS.get(script_name, f"Ritual {script_name} performed"), STATE["eye_color"])
        
        return jsonify({
            "success": result.returncode == 0,
            "output": output,
            "script": script_name
        })
    
    except subprocess.TimeoutExpired:
        return jsonify({"success": False, "output": "Ritual exceeded time limit"}), 408
    except Exception as e:
        return jsonify({"success": False, "output": str(e)}), 500

@app.route('/api/plugins', methods=['GET'])
def list_plugins():
    """List available vessel plugins."""
    if not is_authorized():
        return jsonify({"error": "Not authenticated"}), 401
    
    from plugins.registry import list_plugins
    plugins = list_plugins()
    return jsonify(plugins)

@app.route('/api/plugin/<plugin_name>/<action>', methods=['POST'])
def execute_plugin(plugin_name, action):
    """Execute a plugin ritual."""
    if not is_authorized():
        return jsonify({"error": "Not authenticated"}), 401
    
    from plugins.registry import execute
    
    data = request.get_json() or {}
    result = execute(plugin_name, action, **data)
    
    inscribe_glyph(f"plugin_{plugin_name}", f"Vessel '{plugin_name}' ritual '{action}' invoked")
    
    return jsonify(result)

@app.route('/api/settings', methods=['GET', 'POST'])
def handle_settings():
    """Query or modify shrine configuration."""
    if not is_authorized():
        return jsonify({"error": "Not authenticated"}), 401
    
    if request.method == 'GET':
        return jsonify({
            "tts_enabled": SETTINGS.get("tts_enabled"),
            "default_gpu": SETTINGS.get("default_gpu"),
            "volatility_tool": SETTINGS.get("volatility_tool"),
            "shrine_name": SETTINGS.get("shrine_name")
        })
    
    if request.method == 'POST':
        data = request.get_json()
        SETTINGS.update(data)
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(SETTINGS, f, indent=2)
        inscribe_glyph("settings_change", "Shrine configuration has been altered")
        return jsonify({"success": True})

@sock.route('/ws')
def websocket(ws):
    """WebSocket endpoint for real-time constellation synchronization."""
    CLIENTS.add(ws)
    STATE["connected_clients"] = len(CLIENTS)
    
    broadcast({
        "type": "client_connected",
        "connected_clients": STATE["connected_clients"]
    })
    
    try:
        while True:
            data = ws.receive()
            if data:
                message = json.loads(data)
                if message.get("type") == "heartbeat":
                    ws.send(json.dumps({"type": "heartbeat_ack"}))
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        CLIENTS.discard(ws)
        STATE["connected_clients"] = len(CLIENTS)
        broadcast({
            "type": "client_disconnected",
            "connected_clients": STATE["connected_clients"]
        })

if __name__ == '__main__':
    print(f"""
    ╔══════════════════════════════════════════════════════════════╗
    ║                    SHRINE CONSTELLATION AWAKENS              ║
    ║                   Erryn's Forensic Sanctuary                ║
    ╚══════════════════════════════════════════════════════════════╝
    
    Port: {SETTINGS['port']}
    TTS: {SETTINGS['tts_enabled']}
    GPU: {SETTINGS['default_gpu']}
    
    No one walks alone.
    """)
    
    app.run(debug=False, port=SETTINGS['port'], host='0.0.0.0')
