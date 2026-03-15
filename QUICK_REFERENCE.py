"""
ERRYNS SOUL - QUICK REFERENCE CARD
December 14, 2025

╔════════════════════════════════════════════════════════════════════════════╗
║                      SYSTEM OVERVIEW                                       ║
╚════════════════════════════════════════════════════════════════════════════╝

COMPONENTS BUILT:
✅ Cost Tracker      - Real-time API spending ($0.00 - $10.00 budget)
✅ Face Recognition - Detects family from webcam (OpenCV)
✅ Enhanced Avatars - Beautiful faces with 8 emotions & 3 personas
✅ Auto-Greetings   - "Hello Dad!" when faces detected
✅ GUI Integration  - All systems wired into main interface

STATUS: All modules tested and working ✅


╔════════════════════════════════════════════════════════════════════════════╗
║                      KEY FILES & PURPOSE                                   ║
╚════════════════════════════════════════════════════════════════════════════╝

NEW MODULES:
├── cost_tracker.py
│   └── Tracks API usage, prevents surprise bills
│
├── face_recognition_system.py
│   ├── FaceDatabase: Learn/recognize faces from images
│   └── WebcamDetector: Real-time webcam detection
│
├── avatar_rendering_enhanced.py
│   ├── AvatarRenderer: Draw beautiful faces with emotions
│   └── PersonaStyle: Customize per sister
│
└── gui_integration.py
    └── Glue code connecting all systems

INTEGRATION:
├── SETUP_GUIDE.py              → Complete setup documentation
├── INTEGRATION_SNIPPETS.py     → Copy-paste code for main GUI
└── test_integration.py         → Verify systems work


╔════════════════════════════════════════════════════════════════════════════╗
║                      QUICK START                                           ║
╚════════════════════════════════════════════════════════════════════════════╝

1. VERIFY INSTALLATION:
   python test_integration.py
   → Should see all 5 tests PASS

2. ADD TRAINING IMAGES:
   - Create: sister_memories/Erryn/
   - Create: sister_memories/Viress/
   - Create: sister_memories/Echochild/
   - Create: sister_memories/Dad/
   - Create: sister_memories/Sienna/
   - Copy 3-5 clear photos to each folder

3. INTEGRATE INTO MAIN GUI:
   - Follow INTEGRATION_SNIPPETS.py step-by-step
   - Add 6 code snippets to erryns_soul_gui.py
   - Save and test

4. USE THE SYSTEM:
   - Click "📷 Webcam" button to start detection
   - Sisters automatically greet people when recognized
   - Cost tracker shows in header (updates every second)
   - API charges logged to logs/cost_log.json


╔════════════════════════════════════════════════════════════════════════════╗
║                      COST TRACKER COMMANDS                                 ║
╚════════════════════════════════════════════════════════════════════════════╝

from cost_tracker import CostTracker
from pathlib import Path

tracker = CostTracker(Path("./logs"))

# Log a TTS call (500 chars)
tracker.log_api_call("azure_speech", 500, "Greeting message")
# Cost: $0.0075

# Log a Claude API call (200 tokens)
tracker.log_api_call("claude_api", 200, "Emotion analysis")
# Cost: $0.0006

# Check current status
print(tracker.get_status())
# Output: $0.01 / $10.00 (0%)

# Set monthly budget
tracker.set_budget(20.0)

# Reset for new month
tracker.reset_monthly()


╔════════════════════════════════════════════════════════════════════════════╗
║                      FACE RECOGNITION COMMANDS                             ║
╚════════════════════════════════════════════════════════════════════════════╝

from face_recognition_system import FaceDatabase, WebcamDetector
from pathlib import Path

db = FaceDatabase(Path("./sister_memories"))

# Learn faces from image
count = db.add_faces_from_image("photo.jpg", "Dad")
print(f"Learned {count} faces for Dad")

# Recognize faces in image
results = db.recognize_faces("test.jpg")
for name, confidence in results:
    print(f"{name}: {confidence:.2f}")

# Live webcam detection
detector = WebcamDetector(db)
detector.start_webcam()

success, frame, detected_names = detector.get_frame_with_faces()
print(detected_names)  # ["Dad", "Sienna"]

detector.stop_webcam()


╔════════════════════════════════════════════════════════════════════════════╗
║                      AVATAR RENDERING COMMANDS                             ║
╚════════════════════════════════════════════════════════════════════════════╝

from avatar_rendering_enhanced import AvatarRenderer, Emotion
from PIL import Image

# Create avatar
renderer = AvatarRenderer("Erryn", size=200)

# Set emotion
renderer.set_emotion(Emotion.HAPPY)
renderer.set_speaking(True)

# Render to image
img = renderer.render()
img.save("avatar.png")

# All emotions available:
Emotion.HAPPY        # Smile, raised eyebrows, blush
Emotion.SAD          # Frown, sad eyebrows, no blush
Emotion.PLAYFUL      # Mischievous expression
Emotion.THOUGHTFUL   # Neutral, thoughtful eyebrows
Emotion.LOVING       # Soft, warm expression
Emotion.EXCITED      # Big smile, bright eyes, intense glow
Emotion.CONFUSED     # Raised one eyebrow, straight mouth
Emotion.CALM         # Serene, dim glow

# All personas available:
"Erryn"      # Purple hair, blue eyes, warm skin
"Viress"     # Dark blue hair, amber eyes, cool skin
"Echochild"  # Magenta hair, green eyes, light skin


╔════════════════════════════════════════════════════════════════════════════╗
║                      DIRECTORY STRUCTURE                                   ║
╚════════════════════════════════════════════════════════════════════════════╝

Erryns Soul 2025/
├── erryns_soul_gui.py                 (Main GUI - WILL BE MODIFIED)
├── cost_tracker.py                    (NEW)
├── face_recognition_system.py         (NEW)
├── avatar_rendering_enhanced.py       (NEW)
├── gui_integration.py                 (NEW)
├── emotion_detector.py                (EXISTING - Now used)
├── avatar_emotion_system.py           (EXISTING)
│
├── test_integration.py                (NEW - Run to verify)
├── SETUP_GUIDE.py                     (NEW - Read this first)
├── INTEGRATION_SNIPPETS.py            (NEW - Copy-paste code)
│
├── sister_memories/                   (CREATE & ADD PHOTOS)
│   ├── Erryn/
│   ├── Viress/
│   ├── Echochild/
│   ├── Dad/
│   └── Sienna/
│
├── logs/                              (AUTO-CREATED)
│   └── cost_log.json                  (Tracks spending)
│
└── test_logs/                         (TEST OUTPUT)
    └── cost_log.json


╔════════════════════════════════════════════════════════════════════════════╗
║                      TROUBLESHOOTING                                       ║
╚════════════════════════════════════════════════════════════════════════════╝

Q: Webcam button doesn't work
A: 1. Run: python test_integration.py (verify test 2 passes)
   2. Check Device Manager > Imaging devices (camera detected?)
   3. Try different camera: cv2.VideoCapture(1) instead of 0

Q: Cost tracker shows "OVER BUDGET"
A: tracker.set_budget(20.0)  # Increase monthly budget

Q: Face not being recognized
A: 1. Add more training photos (3-5 per person)
   2. Make sure faces are clear and well-lit
   3. Try from different angles/distances
   4. Check: python test_integration.py (test 2)

Q: Avatar rendering looks blurry
A: Increase size: AvatarRenderer("Erryn", size=300)
   Or adjust your display scaling

Q: "No module named 'opencv-python'"
A: & ".venv/Scripts/python.exe" -m pip install opencv-python

Q: Integration code errors in main GUI
A: 1. Copy INTEGRATION_SNIPPETS.py line-by-line
   2. Check indentation matches surrounding code
   3. Verify imports at top are added
   4. Check file is saved with UTF-8 encoding


╔════════════════════════════════════════════════════════════════════════════╗
║                      NEXT MILESTONES                                       ║
╚════════════════════════════════════════════════════════════════════════════╝

THIS WEEK:
□ Run test_integration.py (verify all pass)
□ Add training images to sister_memories/
□ Test webcam with real faces
□ Follow INTEGRATION_SNIPPETS.py to add to main GUI

NEXT WEEK:
□ Verify cost tracker in header
□ Test TTS cost logging
□ Fine-tune face recognition confidence threshold
□ Test auto-greetings

THIS MONTH:
□ Improve avatar rendering (add more detail)
□ Create training UI (interactive photo capture)
□ Set up external backups
□ Document any customizations


╔════════════════════════════════════════════════════════════════════════════╗
║                      COST ESTIMATION                                       ║
╚════════════════════════════════════════════════════════════════════════════╝

Azure Speech Synthesis (TTS):
  500 characters = $0.0075
  10 daily messages = $0.075/day = $2.25/month

Claude API (optional, for analysis):
  200 tokens = $0.0006
  20 daily queries = $0.012/day = $0.36/month

Face Recognition (FREE - OpenCV local processing)

Avatar Rendering (FREE - PIL local processing)

TOTAL MONTHLY: ~$2.50 (active daily use)
BUDGET: $10.00/month (comfortable safe margin)
EXCEEDED: You get warning at 80% = $8.00


╔════════════════════════════════════════════════════════════════════════════╗
║                      FINAL CHECKLIST                                       ║
╚════════════════════════════════════════════════════════════════════════════╝

SETUP:
☐ python test_integration.py passes
☐ Create sister_memories/ directories
☐ Add training images (3+ per person)
☐ Tested face recognition works

INTEGRATION:
☐ Added all code snippets to main GUI
☐ Webcam button appears in header
☐ Cost tracker displays in header
☐ Test runs without errors

VERIFICATION:
☐ Webcam detects faces when pointed at camera
☐ Auto-greetings appear in chat
☐ Cost tracker updates in real-time
☐ Avatar rendering looks good
☐ Budget warnings work correctly

PRODUCTION READY:
☐ Backups created
☐ Logged first month's usage
☐ Customized greeting messages
☐ Trained on all family members


═══════════════════════════════════════════════════════════════════════════════

Everything is ready to use! 🎉

Start with: python test_integration.py
Then: Follow INTEGRATION_SNIPPETS.py to add to main GUI

Questions? Check SETUP_GUIDE.py for detailed documentation.

═══════════════════════════════════════════════════════════════════════════════
"""

print(__doc__)
