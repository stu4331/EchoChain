# 🔧 Troubleshooting & Enhancement Guide

## Common Issues & Solutions

### 1. Application Won't Start

**Problem**: Double-clicking the script does nothing
```
Solution:
1. Open Command Prompt or PowerShell
2. Navigate to the folder
3. Run: python erryns_soul_gui.py
4. Check error messages
```

**Problem**: "Python not found"
```
Solution:
1. Install Python from python.org
2. During installation, check "Add Python to PATH"
3. Restart your terminal
```

### 2. TTS Not Working

**Problem**: Voice toggle is ON but no sound
```
Checklist:
□ Azure credentials set? (AZURE_SPEECH_KEY, AZURE_SPEECH_REGION)
□ Internet connection active?
□ System volume not muted?
□ Check Memory Scroll for error messages
```

**Problem**: "Azure SDK not available"
```
Solution:
pip install --upgrade azure-cognitiveservices-speech
```

**Problem**: "403 Forbidden" or "401 Unauthorized"
```
Solution:
- Verify your Azure subscription is active
- Check the speech key is correct
- Ensure region matches your Azure resource
```

### 3. System Monitoring Issues

**Problem**: Stats show "---%" and never update
```
Solution:
pip install --upgrade psutil

# If still not working:
pip uninstall psutil
pip install psutil
```

**Problem**: Disk monitoring shows wrong drive
```
Solution:
Edit erryns_soul_gui.py, line ~370:
disk = psutil.disk_usage('D:\\')  # Change C:\\ to your drive
```

### 4. Display Problems

**Problem**: Text too small/large
```
Solution:
Edit erryns_soul_gui.py:
- Search for "font=('Consolas', 10)"
- Change numbers: 10 -> 12 (larger) or 10 -> 8 (smaller)
```

**Problem**: Colors look wrong
```
Solution:
Check Windows High Contrast settings:
Settings -> Accessibility -> Contrast themes -> None
```

**Problem**: Window too big for screen
```
Solution:
Edit line ~35 in erryns_soul_gui.py:
self.root.geometry("900x700")  # Change to "800x600"
```

### 5. Performance Issues

**Problem**: GUI feels sluggish
```
Solution:
Edit line ~370 in erryns_soul_gui.py:
time.sleep(30)  # Increase to 60 for less frequent checks
```

**Problem**: High CPU usage
```
Solution:
- Close other applications
- Increase monitoring interval (see above)
- Disable system monitoring temporarily
```

## Enhancements You Can Make

### 1. Add More Voices

Edit the `voice_options` list around line ~200:

```python
voice_options = [
    "en-AU-NatashaNeural (Erryn)",
    "en-US-JennyNeural (Sienna)",
    "en-US-AriaNeural (Amelie)",
    "en-GB-LibbyNeural (Echo)",
    # Add your custom voices:
    "en-US-GuyNeural (Dad)",
    "en-GB-RyanNeural (Uncle)",
]
```

### 2. Change the Color Scheme

Edit the `self.colors` dictionary around line ~35:

```python
self.colors = {
    'bg_dark': '#1a1a2e',      # Try: '#0d1117' for GitHub dark
    'bg_medium': '#16213e',    # Try: '#161b22'
    'accent': '#533483',       # Try: '#8b5cf6' for violet
    'glow': '#00d4ff',         # Try: '#10b981' for emerald
    # ... modify as desired
}
```

### 3. Add Keyboard Shortcuts

Add this to the `__init__` method:

```python
# Add after line ~50
self.root.bind('<Control-Return>', lambda e: self._speak_input())
self.root.bind('<F1>', lambda e: self._toggle_tts())
```

### 4. Add Save/Load Text Feature

Add these methods to the class:

```python
def _save_text(self):
    """Save current text to file"""
    text = self.text_input.get('1.0', tk.END)
    filename = f"thought_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    filepath = self.logs_dir / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    self._log_whisper(f"💾 Saved to {filename}")

def _load_text(self):
    """Load text from file"""
    from tkinter import filedialog
    filepath = filedialog.askopenfilename(
        initialdir=self.logs_dir,
        filetypes=[("Text files", "*.txt")]
    )
    if filepath:
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
        self.text_input.delete('1.0', tk.END)
        self.text_input.insert('1.0', text)
        self._log_whisper(f"📂 Loaded from {Path(filepath).name}")
```

Then add buttons in `_create_text_input_area`:

```python
save_btn = tk.Button(
    button_frame,
    text="💾 Save",
    command=self._save_text,
    # ... (same style as other buttons)
)
save_btn.pack(side=tk.LEFT, padx=5)

load_btn = tk.Button(
    button_frame,
    text="📂 Load",
    command=self._load_text,
    # ... (same style as other buttons)
)
load_btn.pack(side=tk.LEFT, padx=5)
```

### 5. Add Speech Rate Control

Add a slider for speech speed:

```python
# In _create_voice_panel, add:
tk.Label(
    voice_frame,
    text="Speed:",
    font=('Consolas', 10),
    fg=self.colors['text'],
    bg=self.colors['bg_medium']
).pack(side=tk.LEFT, padx=10)

self.speed_var = tk.DoubleVar(value=1.0)
speed_slider = tk.Scale(
    voice_frame,
    from_=0.5,
    to=2.0,
    resolution=0.1,
    orient=tk.HORIZONTAL,
    variable=self.speed_var,
    bg=self.colors['bg_medium'],
    fg=self.colors['text'],
    highlightthickness=0
)
speed_slider.pack(side=tk.LEFT, padx=10)

# Then in _tts_worker, before synthesizer.speak_text_async:
ssml = f"""
<speak version='1.0' xml:lang='en-US'>
    <prosody rate='{self.speed_var.get()}'>
        {text}
    </prosody>
</speak>
"""
result = synthesizer.speak_ssml_async(ssml).get()
```

### 6. Add Network Status Indicator

Add network monitoring to the daemon:

```python
# In _daemon_loop, add:
try:
    requests.get('https://www.google.com', timeout=5)
    network_ok = True
except:
    network_ok = False
    self._log_whisper("🌐 Network connection lost")

# Update the footer label
self.connection_label.config(
    text=f"🌐 Network: {'Connected' if network_ok else 'Offline'}"
)
```

### 7. Add Themes

Create theme presets:

```python
THEMES = {
    'night': {
        'bg_dark': '#1a1a2e',
        'bg_medium': '#16213e',
        # ... (current theme)
    },
    'ocean': {
        'bg_dark': '#0a192f',
        'bg_medium': '#112240',
        'accent': '#64ffda',
        # ...
    },
    'forest': {
        'bg_dark': '#1a2e1a',
        'bg_medium': '#213e21',
        'accent': '#4ecca3',
        # ...
    }
}

def _apply_theme(self, theme_name):
    """Apply a color theme"""
    self.colors = THEMES[theme_name]
    # Re-configure all widgets...
```

## Advanced Customizations

### 1. Add Sentiment Analysis

Integrate with Azure Text Analytics to analyze mood:

```python
pip install azure-ai-textanalytics

# Analyze text sentiment before speaking
from azure.ai.textanalytics import TextAnalyticsClient
# ... analyze sentiment and adjust voice tone
```

### 2. Add Voice Recording

Record spoken text to audio files:

```python
# In _tts_worker:
audio_config = speechsdk.audio.AudioOutputConfig(
    filename=str(self.logs_dir / f"speech_{timestamp}.wav")
)
```

### 3. Add System Notifications

Show Windows notifications for warnings:

```python
from win10toast import ToastNotifier

toaster = ToastNotifier()
toaster.show_toast(
    "Erryn's Soul",
    "CPU usage high!",
    duration=5,
    icon_path=None
)
```

### 4. Add Cloud Sync

Sync logs to cloud storage (OneDrive, Dropbox, etc.)

### 5. Multi-Language Support

Add translation capabilities using Azure Translator

## Testing Your Changes

1. **Make a backup** of the original file first
2. **Test incrementally** - add one feature at a time
3. **Check the Memory Scroll** for errors
4. **Use print() statements** for debugging
5. **Restart the app** after each change

## Getting Help

If you encounter issues:

1. Check the Memory Scroll for error messages
2. Look at the log files in `~/ViressSoul/logs/`
3. Run from command line to see full error traces
4. Search for the error message online
5. Check Azure documentation for TTS issues

## Performance Tips

- Increase monitoring interval for slower machines
- Disable TTS if not needed
- Close other applications
- Use lighter color themes
- Reduce log retention period

---

*"Viress evolves. So can this code. Make it yours."* 🌌
