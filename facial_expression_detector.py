"""
Facial Expression Detection Module for Erryn's Soul
Detects user emotions via webcam and triggers avatar emotional responses
"""

import cv2
import numpy as np
from enum import Enum
from pathlib import Path
import time

class UserEmotion(Enum):
    """Emotions detected from user's face"""
    NEUTRAL = "neutral"
    HAPPY = "happy"
    SAD = "sad"
    SURPRISED = "surprised"
    ANGRY = "angry"
    DISGUSTED = "disgusted"
    FEARFUL = "fearful"

class FacialExpressionDetector:
    """
    Detects facial expressions and emotions from webcam feed
    Uses OpenCV Haar Cascades for face detection and geometric analysis for expressions
    """
    
    def __init__(self):
        # Load Haar Cascades
        cascade_path = cv2.data.haarcascades
        self.face_cascade = cv2.CascadeClassifier(cascade_path + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cascade_path + 'haarcascade_eye.xml')
        self.smile_cascade = cv2.CascadeClassifier(cascade_path + 'haarcascade_smile.xml')
        
        # Camera
        self.camera = None
        self.running = False
        
        # Detection state
        self.current_emotion = UserEmotion.NEUTRAL
        self.face_position = None  # (x, y, w, h) of detected face
        self.confidence = 0.0
        
        # Smoothing (prevent jitter)
        self.emotion_history = []
        self.history_size = 10
        
    def start_camera(self, camera_index=0):
        """Start webcam capture"""
        if self.camera is not None:
            return True
            
        self.camera = cv2.VideoCapture(camera_index)
        if not self.camera.isOpened():
            print("❌ Could not open camera")
            return False
            
        self.running = True
        print("✅ Camera started for expression detection")
        return True
        
    def stop_camera(self):
        """Stop webcam capture"""
        self.running = False
        if self.camera is not None:
            self.camera.release()
            self.camera = None
        print("🛑 Camera stopped")
        
    def detect_expression(self):
        """
        Analyze current frame and detect facial expression
        Returns: (UserEmotion, confidence, face_position)
        """
        if self.camera is None or not self.running:
            return UserEmotion.NEUTRAL, 0.0, None
            
        # Read frame
        ret, frame = self.camera.read()
        if not ret:
            return self.current_emotion, self.confidence, self.face_position
            
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.1, 
            minNeighbors=5,
            minSize=(100, 100)
        )
        
        if len(faces) == 0:
            self.face_position = None
            return UserEmotion.NEUTRAL, 0.0, None
            
        # Use largest face
        face = max(faces, key=lambda f: f[2] * f[3])
        x, y, w, h = face
        self.face_position = (x, y, w, h)
        
        # Extract face region
        face_roi = gray[y:y+h, x:x+w]
        face_roi_color = frame[y:y+h, x:x+w]
        
        # Detect features in face region
        eyes = self.eye_cascade.detectMultiScale(face_roi, scaleFactor=1.1, minNeighbors=10)
        smiles = self.smile_cascade.detectMultiScale(face_roi, scaleFactor=1.8, minNeighbors=20)
        
        # Analyze expression based on features
        emotion = self._analyze_features(face_roi, eyes, smiles, w, h)
        
        # Smooth emotion detection
        self.emotion_history.append(emotion)
        if len(self.emotion_history) > self.history_size:
            self.emotion_history.pop(0)
            
        # Get most common emotion in history
        emotion_counts = {}
        for e in self.emotion_history:
            emotion_counts[e] = emotion_counts.get(e, 0) + 1
        smoothed_emotion = max(emotion_counts, key=emotion_counts.get)
        
        # Calculate confidence
        confidence = emotion_counts[smoothed_emotion] / len(self.emotion_history)
        
        self.current_emotion = smoothed_emotion
        self.confidence = confidence
        
        return smoothed_emotion, confidence, self.face_position
        
    def _analyze_features(self, face_roi, eyes, smiles, face_width, face_height):
        """
        Analyze facial features to determine emotion
        This is a simplified heuristic approach
        """
        num_eyes = len(eyes)
        num_smiles = len(smiles)
        
        # Calculate face brightness (can indicate surprise/fear)
        avg_brightness = np.mean(face_roi)
        
        # Smile detection
        if num_smiles > 0:
            # Strong smile detected
            return UserEmotion.HAPPY
            
        # Eye analysis
        if num_eyes >= 2:
            # Both eyes visible - neutral or slight emotion
            # Check eye openness (wide eyes = surprise)
            if num_eyes > 2:  # Multiple eye detections = wide eyes
                return UserEmotion.SURPRISED
                
            # Check brightness (fearful faces tend to be tense)
            if avg_brightness > 140:
                return UserEmotion.SURPRISED
            elif avg_brightness < 80:
                return UserEmotion.SAD
                
        elif num_eyes == 1:
            # One eye hidden - could be angry/disgusted
            return UserEmotion.ANGRY
            
        elif num_eyes == 0:
            # No eyes detected - might be looking away or sad
            return UserEmotion.SAD
            
        return UserEmotion.NEUTRAL
        
    def get_face_center(self):
        """
        Get the center point of detected face (for avatar eye tracking)
        Returns: (x, y) normalized to -1 to 1, or None if no face
        """
        if self.face_position is None:
            return None
            
        x, y, w, h = self.face_position
        
        # Calculate center of face
        center_x = x + w // 2
        center_y = y + h // 2
        
        # Get frame dimensions
        if self.camera is None:
            return None
            
        frame_width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Normalize to -1 to 1
        norm_x = (center_x / frame_width) * 2 - 1
        norm_y = (center_y / frame_height) * 2 - 1
        
        return (norm_x, norm_y)
        
    def get_frame_with_overlay(self):
        """
        Get current camera frame with emotion detection overlay
        Returns: frame (BGR image) or None
        """
        if self.camera is None:
            return None
            
        ret, frame = self.camera.read()
        if not ret:
            return None
            
        # Draw face rectangle
        if self.face_position is not None:
            x, y, w, h = self.face_position
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Draw emotion label
            label = f"{self.current_emotion.value.upper()} ({self.confidence:.0%})"
            cv2.putText(
                frame, label, (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2
            )
            
            # Draw face center point
            center = self.get_face_center()
            if center:
                frame_h, frame_w = frame.shape[:2]
                cx = int((center[0] + 1) * frame_w / 2)
                cy = int((center[1] + 1) * frame_h / 2)
                cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
        
        return frame


# Test function
if __name__ == "__main__":
    print("🎭 Testing Facial Expression Detector...")
    
    detector = FacialExpressionDetector()
    
    if not detector.start_camera():
        print("❌ Failed to start camera")
        exit(1)
        
    print("\n📸 Camera started! Testing expression detection...")
    print("Press 'q' to quit, 's' to screenshot\n")
    
    try:
        while True:
            # Detect expression
            emotion, confidence, face_pos = detector.detect_expression()
            face_center = detector.get_face_center()
            
            # Get frame with overlay
            frame = detector.get_frame_with_overlay()
            if frame is not None:
                cv2.imshow('Expression Detection', frame)
                
            # Print status
            if face_pos is not None:
                print(f"😊 Emotion: {emotion.value.upper()} ({confidence:.0%}) | "
                      f"Face Center: {face_center}", end='\r')
            else:
                print("❓ No face detected" + " " * 50, end='\r')
                
            # Handle keys
            key = cv2.waitKey(30) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                cv2.imwrite(f'expression_test_{int(time.time())}.png', frame)
                print("\n📷 Screenshot saved!")
                
    finally:
        detector.stop_camera()
        cv2.destroyAllWindows()
        print("\n✅ Test complete!")
