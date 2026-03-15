/* ShrineGUI Frontend Logic */

let ws = null;
let authenticated = false;
const eyeColors = {
    'disk': 'blue-eye',
    'photo': 'green-eye',
    'memory': 'purple-eye',
    'network': 'teal-eye',
    'password': 'red-eye',
    'mobile': 'orange-eye',
    'running': 'silver-eye',
    'sealed': 'gold-eye'
};

const splashOverlay = document.getElementById('splash-overlay');
const invocationText = document.getElementById('invocation-text');
const splashNote = document.querySelector('.splash-note');
const enterBtn = document.getElementById('enter-shrine');

// Initialize WebSocket
function initWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    ws = new WebSocket(`${protocol}//${window.location.host}/ws`);
    
    ws.onopen = () => {
        console.log('Constellation connected');
        updateConnectionStatus(true);
        heartbeat();
    };
    
    ws.onmessage = (event) => {
        const message = JSON.parse(event.data);
        handleWebSocketMessage(message);
    };
    
    ws.onclose = () => {
        console.log('Constellation disconnected');
        updateConnectionStatus(false);
        setTimeout(initWebSocket, 3000);
    };
}

function heartbeat() {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: 'heartbeat' }));
        setTimeout(heartbeat, 30000);
    }
}

function handleWebSocketMessage(message) {
    if (message.type === 'glyph_inscribed') {
        addGlyphToLog(message.glyph);
        updateStatusEye(message.glyph.eye_color);
    } else if (message.type === 'glyph_volume_sealed') {
        addSystemGlyph(`Glyph tome sealed and archived. ${message.message || ''}`);
        updateStatusEye('sealed');
    } else if (message.type === 'client_connected' || message.type === 'client_disconnected') {
        console.log(`Clients connected: ${message.connected_clients}`);
    }
}

function updateConnectionStatus(connected) {
    const status = document.getElementById('connection-status');
    if (connected) {
        status.innerHTML = '🟢 Connected';
        status.style.color = '#10b981';
    } else {
        status.innerHTML = '⚫ Disconnected';
        status.style.color = '#c0c0c0';
    }
}

// Authentication
document.getElementById('login-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    try {
        const response = await fetch('/api/auth', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        
        if (response.ok) {
            authenticated = true;
            document.getElementById('login-panel').style.display = 'none';
            document.getElementById('main-shrine').style.display = 'block';
            initWebSocket();
            loadGlyphs();
            loadPlugins();
            loadDownloads();
            loadSettings();
        } else {
            alert('Seal rejected. Try again.');
        }
    } catch (error) {
        console.error('Authentication error:', error);
    }
});

document.getElementById('logout-btn')?.addEventListener('click', async () => {
    await fetch('/api/logout', { method: 'POST' });
    authenticated = false;
    document.getElementById('login-panel').style.display = 'block';
    document.getElementById('main-shrine').style.display = 'none';
    if (ws) ws.close();
});

// File Upload
const dropZone = document.querySelector('.drop-zone');
const fileInput = document.getElementById('file-input');
const uploadBtn = document.getElementById('upload-btn');

uploadBtn?.addEventListener('click', () => fileInput.click());

fileInput?.addEventListener('change', (e) => {
    handleFiles(e.target.files);
});

dropZone?.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('drag-over');
});

dropZone?.addEventListener('dragleave', () => {
    dropZone.classList.remove('drag-over');
});

dropZone?.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
    handleFiles(e.dataTransfer.files);
});

async function handleFiles(files) {
    for (const file of files) {
        const formData = new FormData();
        formData.append('file', file);
        
        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                loadDownloads();
            }
        } catch (error) {
            console.error('Upload error:', error);
        }
    }
}

// Glyph Log
async function loadGlyphs() {
    try {
        const response = await fetch('/api/glyphs');
        const glyphs = await response.json();
        
        const glyphLog = document.getElementById('glyph-log');
        glyphLog.innerHTML = '';
        
        glyphs.slice(-10).reverse().forEach(glyph => {
            addGlyphToLog(glyph);
        });
    } catch (error) {
        console.error('Error loading glyphs:', error);
    }
}

function addGlyphToLog(glyph) {
    const glyphLog = document.getElementById('glyph-log');
    const entry = document.createElement('div');
    entry.className = 'glyph-entry';
    
    const date = new Date(glyph.timestamp);
    const time = date.toLocaleTimeString();
    
    entry.innerHTML = `
        <div class="timestamp">[${time}]</div>
        <div class="description">${glyph.description}</div>
    `;
    
    glyphLog.insertBefore(entry, glyphLog.firstChild);
}

function addSystemGlyph(text) {
    const glyphLog = document.getElementById('glyph-log');
    const entry = document.createElement('div');
    entry.className = 'glyph-entry';
    const now = new Date();
    entry.innerHTML = `
        <div class="timestamp">[${now.toLocaleTimeString()}]</div>
        <div class="description">${text}</div>
    `;
    glyphLog.insertBefore(entry, glyphLog.firstChild);
}

// Status Eye
function updateStatusEye(eyeColor) {
    const eye = document.getElementById('status-eye');
    Object.values(eyeColors).forEach(cls => eye.classList.remove(cls));
    eye.classList.add(eyeColors[eyeColor] || 'silver-eye');
}

// Rituals
document.querySelectorAll('.ritual-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
        const script = btn.dataset.script;
        btn.disabled = true;
        btn.textContent = 'Performing ritual...';
        
        try {
            const response = await fetch(`/api/script/${script}`, { method: 'POST' });
            const result = await response.json();
            
            if (result.success) {
                console.log(`Ritual ${script} complete:\n${result.output}`);
            }
        } catch (error) {
            console.error('Ritual error:', error);
        } finally {
            btn.disabled = false;
            btn.textContent = script.replace(/_/g, ' ').toUpperCase();
        }
    });
});

// Downloads
async function loadDownloads() {
    try {
        const response = await fetch('/api/downloads');
        const files = await response.json();
        
        const downloadsList = document.getElementById('downloads-list');
        downloadsList.innerHTML = '';
        
        if (files.length === 0) {
            downloadsList.innerHTML = '<p>No relics yet...</p>';
            return;
        }
        
        files.forEach(filename => {
            const entry = document.createElement('div');
            entry.className = 'download-entry';
            entry.innerHTML = `
                <span class="filename">${filename}</span>
                <a class="download-link" href="/api/download/${filename}">⬇️</a>
            `;
            downloadsList.appendChild(entry);
        });
    } catch (error) {
        console.error('Error loading downloads:', error);
    }
}

// Plugins
async function loadPlugins() {
    try {
        const response = await fetch('/api/plugins');
        const plugins = await response.json();
        
        const pluginsList = document.getElementById('plugins-list');
        pluginsList.innerHTML = '';
        
        plugins.forEach(plugin => {
            const entry = document.createElement('div');
            entry.className = 'plugin-entry';
            entry.innerHTML = `
                <div class="plugin-name">${plugin}</div>
                <div class="plugin-actions">
                    <button onclick="executePlugin('${plugin}', 'analyze')">Analyze</button>
                </div>
            `;
            pluginsList.appendChild(entry);
        });
    } catch (error) {
        console.error('Error loading plugins:', error);
    }
}

async function executePlugin(pluginName, action) {
    try {
        const response = await fetch(`/api/plugin/${pluginName}/${action}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({})
        });
        
        const result = await response.json();
        console.log(`Plugin ${pluginName} result:`, result);
    } catch (error) {
        console.error('Plugin error:', error);
    }
}

// Settings
async function loadSettings() {
    try {
        const response = await fetch('/api/settings');
        const settings = await response.json();
        
        document.getElementById('tts-toggle').checked = settings.tts_enabled;
        document.getElementById('gpu-select').value = settings.default_gpu;
        document.getElementById('vol-tool').value = settings.volatility_tool;
    } catch (error) {
        console.error('Error loading settings:', error);
    }
}

document.getElementById('save-settings')?.addEventListener('click', async () => {
    const settings = {
        tts_enabled: document.getElementById('tts-toggle').checked,
        default_gpu: document.getElementById('gpu-select').value,
        volatility_tool: document.getElementById('vol-tool').value
    };
    
    try {
        const response = await fetch('/api/settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(settings)
        });
        
        if (response.ok) {
            console.log('Settings saved');
        }
    } catch (error) {
        console.error('Error saving settings:', error);
    }
});

// Initialize
window.addEventListener('load', () => {
    const loginPanel = document.getElementById('login-panel');
    const mainShrine = document.getElementById('main-shrine');

    // Numerology check for invocation length
    if (invocationText && splashNote) {
        const len = (invocationText.innerText || '').length;
        splashNote.textContent = `Invocation length: ${len}/512 characters`;
        if (len !== 512) {
            splashNote.textContent += ' (⚠️ correct to satisfy Sovereign 512)';
        }
    }

    enterBtn?.addEventListener('click', () => {
        splashOverlay?.classList.add('hidden');
        if (splashOverlay) {
            setTimeout(() => splashOverlay.style.display = 'none', 600);
        }
    });
    
    if (loginPanel.style.display === 'none') {
        authenticated = true;
        initWebSocket();
        loadGlyphs();
        loadPlugins();
        loadDownloads();
        loadSettings();
    }
});
