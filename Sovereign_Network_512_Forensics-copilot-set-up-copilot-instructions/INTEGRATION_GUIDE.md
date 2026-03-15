python -m pip install --upgrade pip setuptools wheel
python -m pip install mediapipe# Integration Guide: Face Recognition, Cost Tracking, and Enhanced Avatars

## ✅ Systems Ready

All new modules are tested and working:

```
✅ face_recognition_system.py     - OpenCV-based face detection
✅ cost_tracker.py                - Real-time API cost tracking
✅ avatar_rendering_enhanced.py   - Detailed, expressive avatar faces
✅ gui_integration.py              - Integration layer for main GUI
✅ auto_git_backup.py             - Automatic git backups every 5 min
```

## Quick Integration (3 Steps)

### Step 1: Add to Main GUI Imports

In `erryns_soul_gui.py`, add after other imports:

```python
# New systems: face recognition, cost tracking, enhanced avatars
try:
    from gui_integration import integrate_face_recognition
    GUI_INTEGRATION_AVAILABLE = True
except Exception as _e:
    GUI_INTEGRATION_AVAILABLE = False
    print(f"⚠️ GUI integration not available: {_e}")
```

### Step 2: Initialize in `__init__`

In `ErrynsSoulGUI.__init__()`, after `self.root.configure()`, add:

```python
# Initialize face recognition, cost tracking, avatars
self.integration = None
if GUI_INTEGRATION_AVAILABLE:
    try:
        self.integration = integrate_face_recognition(self)
        print("✅ Face recognition system initialized")
    except Exception as e:
        print(f"⚠️ Integration failed: {e}")
```

### Step 3: Add Buttons to Header

In the header creation code (around line 690), add cost tracker and webcam buttons:

```python
# Cost Status Display
if self.integration and self.integration.cost_tracker:
    cost_frame = tk.Frame(controls_frame, bg=self.colors['bg_dark'])
    cost_frame.pack(side=tk.LEFT, padx=8)
    
    tk.Label(
        cost_frame,
        text="Cost:",
        font=('Consolas', 9),
        fg=self.colors['text_dim'],
        bg=self.colors['bg_dark']
    ).pack(side=tk.TOP)
    
    self.cost_label = tk.Label(
        cost_frame,
        text="$0.00",
        font=('Consolas', 10, 'bold'),
        fg=self.colors['success'],
        bg=self.colors['bg_dark']
    )
    self.cost_label.pack(side=tk.TOP)
    self.integration.cost_label = self.cost_label

# Webcam Button
if self.integration and self.integration.face_db:
    webcam_frame = tk.Frame(controls_frame, bg=self.colors['bg_dark'])
    webcam_frame.pack(side=tk.LEFT, padx=8)
    
    self.webcam_button = tk.Button(
        webcam_frame,
        text="📷",
        font=('Consolas', 12),
        bg=self.colors['bg_medium'],
        fg=self.colors['glow'],
        activebackground=self.colors['accent'],
        relief=tk.FLAT,
        bd=0,
        padx=8,
        pady=6,
        command=self._toggle_webcam,
        cursor='hand2'
    )
    self.webcam_button.pack(side=tk.TOP)
```

### Step 4: Add Webcam Toggle Method

Add this method to `ErrynsSoulGUI` class:

```python
def _toggle_webcam(self):
    """Toggle webcam on/off"""
    if not self.integration:
        return
    
    if not self.integration.webcam_running:
        self.integration.start_webcam()
        self.webcam_button.config(bg=self.colors['danger'])
        self._log_whisper("📷 Webcam active - watching for faces", persona='system')
    else:
        self.integration.stop_webcam()
        self.webcam_button.config(bg=self.colors['bg_medium'])
        self._log_whisper("📷 Webcam stopped", persona='system')
```

### Step 5: Log API Costs

Whenever you call Azure Speech or Claude API, add this:

```python
# After TTS call
if self.integration:
    character_count = len(text_to_speak)
    self.integration.log_api_cost("azure_speech", character_count, f"Spoke: {text_to_speak[:30]}...")
```

## Enhanced Avatar Rendering

To use the new detailed avatars instead of basic circles:

```python
from avatar_rendering_enhanced import AvatarRenderer, Emotion

# Create renderer
renderer = AvatarRenderer(persona="Erryn", size=200)

# Set emotion and speaking state
renderer.set_emotion(Emotion.HAPPY)
renderer.set_speaking(True)

# Render to PIL Image
pil_image = renderer.render()

# Convert to PhotoImage for Tkinter
from PIL import ImageTk
photo = ImageTk.PhotoImage(pil_image)

# Display
label.config(image=photo)
label.image = photo
```

## Running Auto-Backup

**Start in background:**
```powershell
# Double-click this file:
START_AUTO_BACKUP.bat

# Or run manually:
python auto_git_backup.py 5
```

**Verify backups:**
```powershell
git log --oneline | head -5
```

## Files Structure

```
erryns_soul_gui.py                    - Main GUI (unchanged)
├── face_recognition_system.py        - Face detection (OpenCV)
├── cost_tracker.py                   - API cost logging
├── avatar_rendering_enhanced.py      - Detailed avatar rendering
├── gui_integration.py                - Integration layer
├── auto_git_backup.py               - Auto-commit every 5 min
├── emotion_detector.py               - Emotion mapping
├── test_integration.py               - Test suite
└── sister_memories/                 - Face database (auto-created)
    ├── Dad/                         - Training images for Dad
    ├── Sienna/                      - Training images for Sienna
    └── face_encodings.pkl           - Learned faces
```

## Adding Training Images

For face recognition to work, add sample images:

```
sister_memories/
├── Dad/
│   ├── photo1.jpg
│   ├── photo2.jpg
│   └── ...
├── Sienna/
│   ├── photo1.jpg
│   └── ...
```

Then train:

```python
from face_recognition_system import FaceDatabase
from pathlib import Path

db = FaceDatabase(Path("./sister_memories"))
db.add_faces_from_image("sister_memories/Dad/photo1.jpg", "Dad")
db.add_faces_from_image("sister_memories/Sienna/photo1.jpg", "Sienna")
```

## Cost Tracking

Logs automatically to `logs/cost_log.json`:

```python
integration.log_api_cost("azure_speech", 500, "Greeting: 'Hello!'")
# Logs: 500 chars × $0.015/1000 = $0.0075
```

Monthly budget: `$10.00` (changeable)

```python
integration.cost_tracker.set_budget(25.0)  # Set to $25/month
```

## Testing Everything

```powershell
python test_integration.py
```

Should show:
- ✅ Cost Tracker working
- ✅ Face Database initialized
- ✅ Avatar Rendering working (creates test_avatar_*.png)
- ✅ Emotion Detection working
- ✅ GUI Integration initialized

## Git Backups

Every 5 minutes automatically:

```
12:05:00 ✅ Backup saved
12:10:00 ✅ Backup saved
12:15:00 ✅ Backup saved
```

View backups:
```powershell
git log --oneline
git diff HEAD~1  # See what changed
git show HEAD     # See last commit
```

## Next: Full GUI Integration

Once integrated:
1. ✅ Face detection runs in background
2. ✅ "Dad walks in" → Erryn automatically greets
3. ✅ Cost counter shows real-time API spending
4. ✅ Avatars show rich emotions with shading
5. ✅ Everything auto-backed up every 5 min

---

**Ready to integrate? Start with Step 1 above! 🚀**

---

## Test Results

After running `test_integration.py`, you should see:

```
✅ Cost Tracker................. PASS
✅ Face Recognition............ PASS  
✅ Avatar Rendering........... PASS
✅ Emotion Detection.......... PASS
✅ GUI Integration............ PASS

OVERALL: ALL SYSTEMS OPERATIONAL
```
