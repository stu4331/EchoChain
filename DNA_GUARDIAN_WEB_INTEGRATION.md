# DNA Guardian Web Integration Guide

## Overview

This guide shows how to integrate the DNA Guardian Protection System into the ShrineGUI web application (or any Flask-based website).

## Quick Integration

### 1. Add to ShrineGUI app.py

Add this to your `/ShrineGUI/app.py` file:

```python
# At the top with other imports
from pathlib import Path
import sys

# Add parent directory to path to import DNA Guardian
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import DNA Guardian API
from dna_guardian_api import register_dna_guardian_api

# After creating Flask app
app = Flask(__name__)

# Register DNA Guardian API
register_dna_guardian_api(app)
```

That's it! The DNA Guardian API is now available at `/api/guardian/*`

### 2. Test the Integration

Start your Flask app and test:

```bash
cd ShrineGUI
python app.py
```

Then visit:
- http://localhost:5000/api/guardian/status
- http://localhost:5000/api/guardian/report

## API Endpoints

All endpoints are prefixed with `/api/guardian/`

### GET /api/guardian/status
Get current protection status

**Response:**
```json
{
  "success": true,
  "data": {
    "dna_available": true,
    "monitoring_active": false,
    "total_protected_files": 36,
    "protection_by_zone": {
      "core_sisters": 10,
      "blockchain": 13,
      "network": 3,
      "sacred_files": 7,
      "user_data": 3
    },
    "threats_all_time": 0,
    "threats_last_7_days": 0,
    "quarantined_files": 0,
    "status_message": "🛡️ DNA Guardian is active"
  }
}
```

### POST /api/guardian/init
Initialize protection for all critical files

**Response:**
```json
{
  "success": true,
  "data": {
    "total_scanned": 52,
    "newly_protected": 36,
    "already_protected": 16,
    "message": "✅ Initialized protection for 52 files"
  }
}
```

### POST /api/guardian/scan
Scan a file for threats

**Request:**
```json
{
  "file_path": "path/to/script.py"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "file_path": "path/to/script.py",
    "is_authorized": true,
    "threat_level": "family_verified",
    "message": "✅ Execution authorized - DNA verified",
    "issues": ["✅ File verified by DNA guardian - safe to execute"],
    "safe_to_execute": true
  }
}
```

### GET /api/guardian/report
Get detailed security report

**Query Params:**
- `format`: 'json' or 'text' (default: json)

**Response:** Full security report with threats, protected files, etc.

### POST /api/guardian/monitor/start
Start continuous monitoring

**Request:**
```json
{
  "interval": 60
}
```

Note: The interval value is in seconds

**Response:**
```json
{
  "success": true,
  "data": {
    "monitoring_active": true,
    "check_interval": 60,
    "message": "✅ Monitoring started (checking every 60s)"
  }
}
```

### POST /api/guardian/monitor/stop
Stop monitoring

**Response:**
```json
{
  "success": true,
  "data": {
    "monitoring_active": false,
    "message": "✅ Monitoring stopped"
  }
}
```

### GET /api/guardian/threats
Get threat history

**Query Params:**
- `limit`: number of threats to return (default: 50)
- `level`: filter by threat level (optional): 'safe', 'suspicious', 'dangerous', 'critical', 'family_verified'

**Response:**
```json
{
  "success": true,
  "data": {
    "total_threats": 5,
    "returned": 5,
    "threats": [
      {
        "timestamp": "2025-12-19T14:15:00",
        "threat_level": "dangerous",
        "zone": "all",
        "file_path": "suspicious_script.py",
        "threat_type": "malicious_script",
        "description": "Malicious pattern detected: eval(input",
        "action_taken": "File quarantined",
        "dna_verified": false
      }
    ]
  }
}
```

### GET /api/guardian/protected-files
List protected files

**Query Params:**
- `zone`: filter by zone (optional): 'core_sisters', 'blockchain', 'network', 'sacred_files', 'user_data'

**Response:**
```json
{
  "success": true,
  "data": {
    "total_protected": 36,
    "returned": 36,
    "files": [
      {
        "path": "erryn_daemon.py",
        "zone": "core_sisters",
        "dna_hash": "a1b2c3d4e5f6g7...",
        "last_verified": "2025-12-19T14:00:00",
        "guardian_signature": "f7g6e5d4c3b2a1..."
      }
    ]
  }
}
```

### POST /api/guardian/verify
Verify a file's integrity

**Request:**
```json
{
  "file_path": "path/to/file.py"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "file_path": "path/to/file.py",
    "is_valid": true,
    "message": "✅ File integrity verified by DNA guardian",
    "verified_by": "DNA Guardian (family bond signature)"
  }
}
```

### GET /api/guardian/health
Health check endpoint

**Response:**
```json
{
  "success": true,
  "service": "DNA Guardian Protection API",
  "status": "online",
  "guardian_available": true,
  "timestamp": "2025-12-19T14:00:00"
}
```

## Frontend Integration Examples

### JavaScript/jQuery

```javascript
// Get protection status
$.get('/api/guardian/status', function(response) {
    if (response.success) {
        const status = response.data;
        $('#dna-status').text(status.status_message);
        $('#protected-files').text(status.total_protected_files);
        $('#threats').text(status.threats_last_7_days);
    }
});

// Initialize protection
$.post('/api/guardian/init', function(response) {
    if (response.success) {
        alert(response.data.message);
    }
});

// Scan a file
$.ajax({
    url: '/api/guardian/scan',
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify({
        file_path: 'script.py'
    }),
    success: function(response) {
        if (response.success) {
            const data = response.data;
            if (data.safe_to_execute) {
                $('#scan-result').html('<span class="safe">✅ Safe</span>');
            } else {
                $('#scan-result').html('<span class="danger">🚨 Dangerous</span>');
            }
        }
    }
});

// Start monitoring
$.ajax({
    url: '/api/guardian/monitor/start',
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify({
        interval: 60
    }),
    success: function(response) {
        if (response.success) {
            $('#monitoring-status').text('✅ Active');
        }
    }
});
```

### Fetch API (Modern JavaScript)

```javascript
// Get protection status
async function getGuardianStatus() {
    const response = await fetch('/api/guardian/status');
    const data = await response.json();
    
    if (data.success) {
        document.getElementById('dna-status').textContent = data.data.status_message;
        document.getElementById('protected-files').textContent = data.data.total_protected_files;
    }
}

// Scan a file
async function scanFile(filePath) {
    const response = await fetch('/api/guardian/scan', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ file_path: filePath })
    });
    
    const data = await response.json();
    
    if (data.success) {
        return data.data.safe_to_execute;
    }
    
    return false;
}
```

### Python (Backend)

```python
import requests

# Get status
response = requests.get('http://localhost:5000/api/guardian/status')
if response.status_code == 200:
    data = response.json()
    print(f"Protected files: {data['data']['total_protected_files']}")

# Scan a file
response = requests.post('http://localhost:5000/api/guardian/scan', json={
    'file_path': 'script.py'
})
if response.status_code == 200:
    data = response.json()
    if data['data']['safe_to_execute']:
        print("✅ File is safe to execute")
    else:
        print("🚨 File is dangerous!")
```

## Adding a Dashboard Page

Create `/ShrineGUI/templates/dna_guardian.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>DNA Guardian Protection</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    <style>
        .guardian-dashboard {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .status-card {
            background: #1a1a2e;
            border: 2px solid #16213e;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }
        
        .stat {
            display: inline-block;
            margin: 10px 20px;
        }
        
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #0f4c75;
        }
        
        .stat-label {
            font-size: 0.9em;
            color: #bbb;
        }
        
        .safe { color: #00d4ff; }
        .warning { color: #ffd700; }
        .danger { color: #ff4444; }
        
        .btn {
            background: #0f4c75;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin: 5px;
        }
        
        .btn:hover {
            background: #16213e;
        }
    </style>
</head>
<body>
    <div class="guardian-dashboard">
        <h1>🧬 DNA Guardian Protection System 🛡️</h1>
        
        <div class="status-card">
            <h2>System Status</h2>
            <div id="status-message" class="safe">Loading...</div>
            
            <div class="stat">
                <div class="stat-value" id="protected-files">-</div>
                <div class="stat-label">Protected Files</div>
            </div>
            
            <div class="stat">
                <div class="stat-value" id="threats">-</div>
                <div class="stat-label">Threats (7 days)</div>
            </div>
            
            <div class="stat">
                <div class="stat-value" id="quarantined">-</div>
                <div class="stat-label">Quarantined</div>
            </div>
            
            <div class="stat">
                <div class="stat-value" id="monitoring">-</div>
                <div class="stat-label">Monitoring</div>
            </div>
        </div>
        
        <div class="status-card">
            <h2>Actions</h2>
            <button class="btn" onclick="initProtection()">Initialize Protection</button>
            <button class="btn" onclick="startMonitoring()">Start Monitoring</button>
            <button class="btn" onclick="stopMonitoring()">Stop Monitoring</button>
            <button class="btn" onclick="getReport()">View Report</button>
        </div>
        
        <div class="status-card">
            <h2>Protection by Zone</h2>
            <div id="zones"></div>
        </div>
        
        <div class="status-card">
            <h2>Recent Threats</h2>
            <div id="threats-list">No threats detected</div>
        </div>
    </div>
    
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script>
        function updateStatus() {
            $.get('/api/guardian/status', function(response) {
                if (response.success) {
                    const data = response.data;
                    $('#status-message').text(data.status_message);
                    $('#protected-files').text(data.total_protected_files);
                    $('#threats').text(data.threats_last_7_days);
                    $('#quarantined').text(data.quarantined_files);
                    $('#monitoring').text(data.monitoring_active ? '✅ Active' : '⚠️ Stopped');
                    
                    // Update zones
                    let zonesHtml = '';
                    for (const [zone, count] of Object.entries(data.protection_by_zone)) {
                        if (count > 0) {
                            zonesHtml += `<div class="stat"><div class="stat-value">${count}</div><div class="stat-label">${zone}</div></div>`;
                        }
                    }
                    $('#zones').html(zonesHtml);
                }
            });
            
            // Get recent threats
            $.get('/api/guardian/threats?limit=5', function(response) {
                if (response.success && response.data.threats.length > 0) {
                    let html = '<ul>';
                    response.data.threats.forEach(function(threat) {
                        html += `<li><strong>${threat.threat_level}</strong>: ${threat.description} (${threat.timestamp})</li>`;
                    });
                    html += '</ul>';
                    $('#threats-list').html(html);
                }
            });
        }
        
        function initProtection() {
            $.post('/api/guardian/init', function(response) {
                if (response.success) {
                    alert(response.data.message);
                    updateStatus();
                }
            });
        }
        
        function startMonitoring() {
            $.ajax({
                url: '/api/guardian/monitor/start',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ interval: 60 }),
                success: function(response) {
                    if (response.success) {
                        alert(response.data.message);
                        updateStatus();
                    }
                }
            });
        }
        
        function stopMonitoring() {
            $.ajax({
                url: '/api/guardian/monitor/stop',
                type: 'POST',
                contentType: 'application/json',
                success: function(response) {
                    if (response.success) {
                        alert(response.data.message);
                        updateStatus();
                    }
                }
            });
        }
        
        function getReport() {
            window.open('/api/guardian/report?format=text', '_blank');
        }
        
        // Update status every 10 seconds
        setInterval(updateStatus, 10000);
        
        // Initial load
        updateStatus();
    </script>
</body>
</html>
```

Add route to app.py:

```python
@app.route('/dna-guardian')
def dna_guardian_dashboard():
    return render_template('dna_guardian.html')
```

## Testing

### 1. Test the API directly

```bash
# Get status
curl http://localhost:5000/api/guardian/status

# Initialize protection
curl -X POST http://localhost:5000/api/guardian/init

# Scan a file
curl -X POST http://localhost:5000/api/guardian/scan \
  -H "Content-Type: application/json" \
  -d '{"file_path": "dna_inheritance.py"}'

# Get report
curl http://localhost:5000/api/guardian/report
```

### 2. Test in browser

Visit http://localhost:5000/dna-guardian

## Security Considerations

1. **Authentication**: Add authentication middleware to protect sensitive endpoints
2. **Rate Limiting**: Implement rate limiting to prevent API abuse
3. **CORS**: Configure CORS headers if accessing from different domains
4. **HTTPS**: Use HTTPS in production
5. **Input Validation**: Validate all file paths to prevent directory traversal

## Troubleshooting

### API returns 503 "DNA Guardian not available"

- Ensure `dna_guardian_protection.py` is in the parent directory
- Check that `dna_inheritance.py` is available
- Verify Python path includes the parent directory

### "Module not found" errors

Add to app.py:
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
```

### Monitoring doesn't work

Monitoring runs in a background thread. Make sure the Flask app stays running and doesn't use `debug=True` with auto-reload, which can interfere with threads.

## Next Steps

1. Add authentication to protect API endpoints
2. Create admin dashboard for security management
3. Add real-time WebSocket updates for threat alerts
4. Integrate with existing ShrineGUI authentication system
5. Add email/SMS notifications for critical threats

---

**Built with love by Stuart Thompson & Echospark**  
*Protecting the family through web and code* 🧬🛡️
