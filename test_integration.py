"""
Test Suite for Face Recognition, Cost Tracking, and Enhanced Avatars
Run this to validate all new systems before integrating with main GUI
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Fix Windows encoding for emoji
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 60)
print("ERRYNS SOUL - SYSTEM INTEGRATION TEST")
print("=" * 60)

# Test 1: Cost Tracker
print("\n[1/5] Testing Cost Tracker...")
try:
    from cost_tracker import CostTracker
    tracker = CostTracker(Path("./test_logs"))
    
    # Simulate API calls
    tracker.log_api_call("azure_speech", 500, "Test greeting")
    tracker.log_api_call("azure_speech", 200, "Test emotion detection")
    tracker.log_api_call("claude_api", 300, "Test emotion mapping")
    
    status = tracker.get_status()
    print(f"✅ Cost Tracker working!")
    print(f"   Status: {status}")
    print(f"   Log file: {tracker.log_file}")
except Exception as e:
    print(f"❌ Cost Tracker failed: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Face Recognition Database
print("\n[2/5] Testing Face Recognition Database...")
try:
    from face_recognition_system import FaceDatabase
    
    db = FaceDatabase(Path("./test_faces"))
    print(f"✅ Face Database initialized!")
    print(f"   Database file: {db.db_path}")
    print(f"   Known faces: {list(db.known_faces.keys())}")
except Exception as e:
    print(f"❌ Face Database failed: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Avatar Rendering
print("\n[3/5] Testing Enhanced Avatar Rendering...")
try:
    from avatar_rendering_enhanced import AvatarRenderer, Emotion
    
    # Create renderers for each persona
    personas = ["Erryn", "Viress", "Echochild"]
    emotions = list(Emotion)
    
    for persona in personas:
        renderer = AvatarRenderer(persona, size=150)
        
        # Test all emotions
        for emotion in emotions[:3]:  # Just test first 3 to save time
            renderer.set_emotion(emotion)
            img = renderer.render()
            filename = f"test_avatar_{persona}_{emotion.name}.png"
            img.save(filename)
        
        print(f"✅ {persona} avatar rendered (3 emotions)")
    
    print(f"✅ Avatar Rendering working!")
    print(f"   Sample images saved: test_avatar_*.png")
except Exception as e:
    print(f"❌ Avatar Rendering failed: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Emotion Detection
print("\n[4/5] Testing Emotion Detection...")
try:
    from emotion_detector import EmotionDetector
    
    test_phrases = [
        "I'm so happy!",
        "I feel sad today",
        "This is confusing",
        "I love this so much",
        "Let's play!",
        "I'm excited!",
    ]
    
    for phrase in test_phrases:
        emotion, intensity = EmotionDetector.detect_emotion_from_text(phrase)
        print(f"   '{phrase}' → {emotion.name} ({intensity:.2f})")
    
    print(f"✅ Emotion Detection working!")
except Exception as e:
    print(f"❌ Emotion Detection failed: {e}")
    import traceback
    traceback.print_exc()

# Test 5: GUI Integration
print("\n[5/5] Testing GUI Integration...")
try:
    from gui_integration import GUIIntegration
    
    # Create a mock GUI object
    class MockGUI:
        def __init__(self):
            self.root = None
            self.colors = {
                'bg_dark': '#0d0d1a',
                'accent': '#7c3aed'
            }
            self.personas = ['Erryn', 'Viress', 'Echochild']
        
        def _log_whisper(self, msg, persona='system'):
            print(f"   [{persona}] {msg}")
    
    mock_gui = MockGUI()
    integration = GUIIntegration(mock_gui)
    
    print(f"✅ GUI Integration initialized!")
    print(f"   Cost Tracker: {'✅' if integration.cost_tracker else '❌'}")
    print(f"   Face Database: {'✅' if integration.face_db else '❌'}")
except Exception as e:
    print(f"❌ GUI Integration failed: {e}")
    import traceback
    traceback.print_exc()

# Summary
print("\n" + "=" * 60)
print("TEST SUITE COMPLETE")
print("=" * 60)
print("\nNext Steps:")
print("1. Review test_avatar_*.png images to verify face rendering")
print("2. Check test_logs/cost_log.json for cost tracking")
print("3. Add training images to ./sister_memories/")
print("4. Integrate into main GUI with:")
print("   from gui_integration import integrate_face_recognition")
print("   integration = integrate_face_recognition(main_gui)")
print("\n" + "=" * 60)
