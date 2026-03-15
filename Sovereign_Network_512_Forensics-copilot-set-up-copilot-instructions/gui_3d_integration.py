"""
GUI Integration for 3D Face Tracking and Avatar Rendering
Connects face_tracking_3d.py and avatar_3d_renderer.py to the main GUI

This module handles:
- Webcam feed processing with 3D tracking
- Real-time avatar rendering
- Updating avatar based on facial expressions and head pose
"""

import tkinter as tk
from tkinter import PhotoImage
import threading
import cv2
from PIL import Image, ImageTk
import numpy as np
from typing import Optional, Callable

try:
    from face_tracking_3d import WebcamTracker3D, FacialExpressions, MEDIAPIPE_AVAILABLE
    from avatar_3d_renderer import Avatar3DRenderer, Emotion
except ImportError as e:
    print(f"⚠️ 3D tracking modules not available: {e}")
    MEDIAPIPE_AVAILABLE = False


class GUI3DTracker:
    """Manages 3D face tracking and avatar rendering in Tkinter"""
    
    def __init__(self, avatar_label: tk.Label, webcam_label: Optional[tk.Label] = None,
                 on_face_detected: Optional[Callable[[str], None]] = None):
        """
        Initialize 3D tracking and avatar system
        
        Args:
            avatar_label: Tk label to display avatar
            webcam_label: Tk label to display webcam feed with landmarks (optional)
            on_face_detected: Callback when face is detected (for greetings, etc.)
        """
        if not MEDIAPIPE_AVAILABLE:
            raise RuntimeError("MediaPipe not available. Install with: pip install mediapipe")
        
        self.avatar_label = avatar_label
        self.webcam_label = webcam_label
        self.on_face_detected = on_face_detected
        
        self.tracker = WebcamTracker3D("Person")
        self.avatar = Avatar3DRenderer("Erryn", size=300)
        
        self.running = False
        self.current_expressions: Optional[FacialExpressions] = None
        self.update_thread: Optional[threading.Thread] = None
        
        # For display efficiency
        self.last_face_detected = False
    
    def start(self) -> bool:
        """Start webcam and tracking"""
        if not self.tracker.start():
            return False
        
        self.running = True
        self.update_thread = threading.Thread(target=self._update_loop, daemon=True)
        self.update_thread.start()
        
        return True
    
    def _update_loop(self):
        """Main update loop for processing and rendering"""
        while self.running:
            frame, expressions = self.tracker.get_frame()
            
            if expressions:
                self.current_expressions = expressions
                
                # Update avatar based on facial expressions
                self._update_avatar_from_expressions(expressions)
                
                # Detect when face appears/disappears
                if not self.last_face_detected:
                    self.last_face_detected = True
                    if self.on_face_detected:
                        self.on_face_detected("Person detected!")
            
            else:
                if self.last_face_detected:
                    self.last_face_detected = False
                    if self.on_face_detected:
                        self.on_face_detected("Face lost")
            
            # Display frames
            if self.webcam_label and frame is not None:
                self._display_webcam_frame(frame)
            
            if self.current_expressions:
                self._display_avatar()
    
    def _update_avatar_from_expressions(self, expressions: FacialExpressions):
        """Update avatar based on detected facial expressions"""
        
        # Update head pose
        self.avatar.set_head_pose(
            expressions.head_pose.yaw,
            expressions.head_pose.pitch,
            expressions.head_pose.roll
        )
        
        # Update facial metrics
        mouth_open = 1.0 if expressions.mouth_open else 0.0
        self.avatar.set_facial_metrics(
            mouth_open=mouth_open,
            left_eye_open=expressions.left_eye_open,
            right_eye_open=expressions.right_eye_open,
            smile=expressions.smiling
        )
        
        # Update emotion based on expression
        if expressions.is_speaking():
            self.avatar.set_emotion(Emotion.SPEAKING)
        elif expressions.smiling > 0.6:
            self.avatar.set_emotion(Emotion.HAPPY)
        elif expressions.eyes_closed:
            self.avatar.set_emotion(Emotion.CALM)
        elif expressions.is_relaxed():
            self.avatar.set_emotion(Emotion.THOUGHTFUL)
    
    def _display_avatar(self):
        """Render and display avatar"""
        try:
            img = self.avatar.render()
            photo = ImageTk.PhotoImage(img)
            
            # Schedule update on main thread
            self.avatar_label.after(0, lambda: self._update_label(self.avatar_label, photo))
        except Exception as e:
            print(f"Error rendering avatar: {e}")
    
    def _display_webcam_frame(self, frame: np.ndarray):
        """Display webcam feed in label"""
        try:
            # Resize for display
            h, w = frame.shape[:2]
            display_width = 400
            display_height = int(h * display_width / w)
            resized = cv2.resize(frame, (display_width, display_height))
            
            # Convert to PIL and then PhotoImage
            rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb)
            photo = ImageTk.PhotoImage(pil_image)
            
            # Schedule update on main thread
            self.webcam_label.after(0, lambda: self._update_label(self.webcam_label, photo))
        except Exception as e:
            print(f"Error displaying webcam: {e}")
    
    def _update_label(self, label: tk.Label, photo):
        """Update label with image (must be called from main thread)"""
        try:
            label.config(image=photo)
            label.image = photo  # Keep reference
        except:
            pass
    
    def set_persona(self, persona: str):
        """Change avatar persona"""
        self.avatar = Avatar3DRenderer(persona, size=300)
    
    def set_emotion(self, emotion: Emotion):
        """Manually set avatar emotion"""
        self.avatar.set_emotion(emotion)
    
    def stop(self):
        """Stop tracking and cleanup"""
        self.running = False
        self.tracker.stop()
        if self.update_thread:
            self.update_thread.join(timeout=2)
    
    def get_current_expressions(self) -> Optional[FacialExpressions]:
        """Get latest facial expressions"""
        return self.current_expressions


# Example usage and testing
if __name__ == "__main__":
    
    root = tk.Tk()
    root.title("3D Avatar with Face Tracking")
    root.geometry("1000x600")
    
    # Avatar display
    avatar_label = tk.Label(root, bg="black", width=300, height=300)
    avatar_label.pack(side=tk.LEFT, padx=10, pady=10)
    
    # Webcam display
    webcam_label = tk.Label(root, bg="black", width=400, height=300)
    webcam_label.pack(side=tk.RIGHT, padx=10, pady=10)
    
    # Status label
    status_label = tk.Label(root, text="Starting...", font=("Arial", 12))
    status_label.pack(fill=tk.X, padx=10, pady=5)
    
    def on_face_detected(message: str):
        status_label.config(text=message)
    
    # Initialize tracker
    try:
        tracker = GUI3DTracker(avatar_label, webcam_label, on_face_detected)
        
        if tracker.start():
            status_label.config(text="✅ Tracking started. Point camera at your face!")
        else:
            status_label.config(text="❌ Could not start webcam")
    
    except Exception as e:
        status_label.config(text=f"❌ Error: {e}")
    
    def on_closing():
        tracker.stop()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
