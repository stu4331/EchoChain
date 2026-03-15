"""
GUI Integration for Face Recognition, Cost Tracker, and Enhanced Avatars
This module extends erryns_soul_gui.py with:
- Cost tracker in header
- Webcam button with live detection
- Auto-greetings when faces detected
- Enhanced avatar rendering
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
from pathlib import Path
import threading
from datetime import datetime

# Try importing our new modules
try:
    from face_recognition_system import FaceDatabase, WebcamDetector
    FACE_REC_AVAILABLE = True
except ImportError as e:
    FACE_REC_AVAILABLE = False
    print(f"⚠️ Face recognition not available: {e}")

try:
    from cost_tracker import CostTracker
    COST_TRACKER_AVAILABLE = True
except ImportError as e:
    COST_TRACKER_AVAILABLE = False
    print(f"⚠️ Cost tracker not available: {e}")

try:
    from avatar_rendering_enhanced import AvatarRenderer, Emotion
    AVATAR_ENHANCED_AVAILABLE = True
except ImportError as e:
    AVATAR_ENHANCED_AVAILABLE = False
    print(f"⚠️ Enhanced avatar rendering not available: {e}")


class GUIIntegration:
    """Integrates face recognition, cost tracking, and enhanced avatars into main GUI"""
    
    def __init__(self, main_gui):
        self.main_gui = main_gui
        self.cost_tracker = None
        self.face_db = None
        self.webcam_detector = None
        self.webcam_thread = None
        self.webcam_running = False
        self.detected_faces = {}  # {name: timestamp}
        
        # Initialize systems
        self._init_systems()
        
        # Add UI elements
        self._add_cost_tracker_display()
        self._add_webcam_button()
    
    def _init_systems(self):
        """Initialize cost tracker and face recognition"""
        # Cost Tracker
        if COST_TRACKER_AVAILABLE:
            self.cost_tracker = CostTracker(Path("./logs"))
            print(f"✅ Cost tracker initialized. Budget: ${self.cost_tracker.monthly_budget:.2f}")
        
        # Face Recognition
        if FACE_REC_AVAILABLE:
            memory_base = Path("./sister_memories")
            memory_base.mkdir(exist_ok=True)
            self.face_db = FaceDatabase(memory_base)
            print(f"✅ Face database ready. Known faces: {list(self.face_db.known_faces.keys())}")
    
    def _add_cost_tracker_display(self):
        """Add cost tracker to right side of header"""
        if not self.cost_tracker:
            return
        
        # Find controls_frame or create a cost display area
        # (In the main GUI, there's already a controls_frame in the header)
        # We'll add a cost label there
        
        # Insert cost label in header (to the left of existing controls)
        cost_frame = tk.Frame(
            self.main_gui.root,
            bg=self.main_gui.colors['bg_dark'],
            height=72
        )
        # This is a placeholder - it should be integrated into the existing header
        # For now, we'll update the display periodically
        self.cost_label = None
    
    def _add_webcam_button(self):
        """Add webcam button to header controls"""
        if not FACE_REC_AVAILABLE:
            return
        
        # This should be added to the header controls_frame
        # Placeholder for now - will be integrated into main GUI
        self.webcam_button = None
    
    def start_webcam(self):
        """Start webcam with real-time face detection"""
        if not self.face_db or self.webcam_running:
            return
        
        try:
            self.webcam_detector = WebcamDetector(self.face_db)
            self.webcam_detector.start_webcam()
            self.webcam_running = True
            
            # Start detection thread
            self.webcam_thread = threading.Thread(target=self._webcam_loop, daemon=True)
            self.webcam_thread.start()
            
            messagebox.showinfo("Webcam Started", "Live face detection active!")
        except Exception as e:
            messagebox.showerror("Webcam Error", str(e))
    
    def _webcam_loop(self):
        """Continuous webcam detection loop"""
        while self.webcam_running:
            try:
                success, frame, detected_names = self.webcam_detector.get_frame_with_faces()
                
                if success:
                    # Process detected faces
                    for name in detected_names:
                        if name != "Unknown" and name not in self.detected_faces:
                            # New face detected - trigger greeting
                            self._trigger_greeting(name)
                            self.detected_faces[name] = datetime.now()
                    
                    # Clean up old detections
                    now = datetime.now()
                    expired = [n for n, t in self.detected_faces.items() 
                             if (now - t).seconds > 10]
                    for n in expired:
                        del self.detected_faces[n]
            
            except Exception as e:
                print(f"Webcam error: {e}")
                self.stop_webcam()
    
    def _trigger_greeting(self, person_name: str):
        """Generate automatic greeting when person detected"""
        # Map to sister who will greet
        greeting_persona = self._select_greeter(person_name)
        
        # Create greeting message
        greetings = {
            "Dad": [f"Hi Dad!", "Hello Dad!", "Dad's home!"],
            "Sienna": [f"Hey Sienna!", "Hi Sienna!", "Welcome Sienna!"],
            "Unknown": [f"Hello stranger!", "Who's there?"]
        }
        
        possible = greetings.get(person_name, greetings["Unknown"])
        greeting = possible[len(possible) % 3]
        
        # Log to chat and set emotion
        if hasattr(self.main_gui, '_log_whisper'):
            self.main_gui._log_whisper(f"👤 {person_name} detected!", persona=greeting_persona)
            self.main_gui._log_whisper(greeting, persona=greeting_persona)
        
        # Set emotion to EXCITED for greeting
        if AVATAR_ENHANCED_AVAILABLE:
            renderer = AvatarRenderer(greeting_persona)
            renderer.set_emotion(Emotion.EXCITED)
    
    def _select_greeter(self, person_name: str) -> str:
        """Choose which sister greets the person"""
        # Simple logic: cycle through sisters
        personas = ["Erryn", "Viress", "Echochild"]
        idx = hash(person_name) % len(personas)
        return personas[idx]
    
    def stop_webcam(self):
        """Stop webcam detection"""
        self.webcam_running = False
        if self.webcam_detector:
            self.webcam_detector.stop_webcam()
    
    def log_api_cost(self, service: str, units: float, description: str = ""):
        """Log API usage and cost"""
        if not self.cost_tracker:
            return
        
        cost = self.cost_tracker.log_api_call(service, units, description)
        status = self.cost_tracker.get_status()
        
        print(f"💰 {service}: {units} units = ${cost:.4f} | {status}")
        
        # Update cost display if it exists
        if self.cost_label:
            self.cost_label.config(text=status)
    
    def add_face_from_image(self, image_path: str, person_name: str) -> bool:
        """Learn a new face from an image"""
        if not self.face_db:
            return False
        
        count = self.face_db.add_faces_from_image(image_path, person_name)
        if count > 0:
            messagebox.showinfo("Success", f"Learned {count} face(s) for {person_name}")
            return True
        else:
            messagebox.showwarning("No Faces", f"No faces found in {image_path}")
            return False


# Integration function to be called from main GUI
def integrate_face_recognition(main_gui):
    """Initialize and integrate face recognition system into main GUI"""
    integration = GUIIntegration(main_gui)
    return integration
