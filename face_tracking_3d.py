"""
3D Face Tracking System - Human Head Pose & Facial Landmarks
Using MediaPipe for advanced facial feature detection and head pose estimation

Features:
- Real-time 3D head pose (yaw, pitch, roll)
- 468 facial landmarks for detailed expressions
- Eye gaze tracking
- Mouth open/close detection
- Head movement smoothing
- Works with webcam or images

Built by Echospark, December 2025
"""

import cv2
import numpy as np
from typing import Tuple, List, Dict, Optional
from dataclasses import dataclass
from enum import Enum
import threading
from pathlib import Path
import json

try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False
    print("⚠️ MediaPipe not available. Install with: pip install mediapipe")


@dataclass
class HeadPose:
    """3D head orientation angles"""
    yaw: float        # Left-right rotation (-90 to 90)
    pitch: float      # Up-down rotation (-90 to 90)
    roll: float       # Tilt left-right (-90 to 90)
    
    def __str__(self) -> str:
        return f"Yaw:{self.yaw:.1f}° Pitch:{self.pitch:.1f}° Roll:{self.roll:.1f}°"


@dataclass
class FacialExpressions:
    """Detected facial expressions and states"""
    mouth_open: bool
    eyes_closed: bool
    smiling: float          # 0.0 to 1.0
    left_eye_open: float    # 0.0 to 1.0
    right_eye_open: float   # 0.0 to 1.0
    head_pose: HeadPose
    
    def is_speaking(self) -> bool:
        """Detect if face is in speaking position"""
        return self.mouth_open and not self.eyes_closed
    
    def is_relaxed(self) -> bool:
        """Detect if face is relaxed/calm"""
        return (not self.mouth_open and 
                self.left_eye_open > 0.7 and 
                self.right_eye_open > 0.7)


class FaceTracker3D:
    """Real-time 3D face tracking using MediaPipe"""
    
    def __init__(self):
        if not MEDIAPIPE_AVAILABLE:
            raise RuntimeError("MediaPipe not available. Install with: pip install mediapipe")
        
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Smoothing for head pose (reduce jitter)
        self.head_pose_history: List[HeadPose] = []
        self.history_size = 5
        
        # Eye aspect ratio threshold
        self.EYE_AR_THRESH = 0.2
        self.MOUTH_AR_THRESH = 0.5
        
        # Landmark indices for important features
        self.LEFT_EYE = [362, 382, 381, 380, 374, 373, 390, 249]
        self.RIGHT_EYE = [33, 7, 163, 144, 145, 153, 154, 155]
        self.MOUTH = [61, 146, 91, 181, 84, 17, 314, 405, 321, 375]
        self.NOSE = [1, 2, 98, 326]
        self.CHIN = [152, 176, 148, 149, 176, 149, 150, 335, 331, 160]
    
    def process_image(self, image: np.ndarray) -> Tuple[Optional[FacialExpressions], np.ndarray]:
        """
        Process image and detect facial features.
        
        Args:
            image: BGR image from OpenCV
            
        Returns:
            (FacialExpressions or None, annotated image)
        """
        height, width = image.shape[:2]
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        results = self.face_mesh.process(rgb_image)
        
        if not results.multi_face_landmarks:
            return None, image
        
        landmarks = results.multi_face_landmarks[0]
        
        # Extract 3D coordinates (normalized to image space)
        face_coords = []
        for landmark in landmarks.landmark:
            face_coords.append([landmark.x * width, landmark.y * height, landmark.z])
        
        face_coords = np.array(face_coords)
        
        # Calculate facial expressions
        expressions = self._calculate_expressions(face_coords, width, height)
        
        # Draw landmarks on image
        annotated = self._draw_landmarks(image.copy(), face_coords, expressions)
        
        return expressions, annotated
    
    def _calculate_expressions(self, landmarks: np.ndarray, width: int, height: int) -> FacialExpressions:
        """Calculate facial expressions from landmarks"""
        
        # Eye aspect ratios
        left_ear = self._eye_aspect_ratio(landmarks[self.LEFT_EYE])
        right_ear = self._eye_aspect_ratio(landmarks[self.RIGHT_EYE])
        
        # Mouth aspect ratio
        mar = self._mouth_aspect_ratio(landmarks[self.MOUTH])
        
        # Head pose estimation
        head_pose = self._estimate_head_pose(landmarks)
        self.head_pose_history.append(head_pose)
        if len(self.head_pose_history) > self.history_size:
            self.head_pose_history.pop(0)
        
        # Smooth head pose
        smoothed_pose = self._smooth_head_pose()
        
        # Smile detection (based on mouth corners and cheek height)
        smile_confidence = self._detect_smile(landmarks)
        
        return FacialExpressions(
            mouth_open=mar > self.MOUTH_AR_THRESH,
            eyes_closed=(left_ear < self.EYE_AR_THRESH and right_ear < self.EYE_AR_THRESH),
            smiling=smile_confidence,
            left_eye_open=min(1.0, left_ear / self.EYE_AR_THRESH),
            right_eye_open=min(1.0, right_ear / self.EYE_AR_THRESH),
            head_pose=smoothed_pose
        )
    
    def _eye_aspect_ratio(self, eye_landmarks: np.ndarray) -> float:
        """Calculate eye aspect ratio for blink detection"""
        if len(eye_landmarks) < 6:
            return 0.0
        
        A = np.linalg.norm(eye_landmarks[1] - eye_landmarks[5])
        B = np.linalg.norm(eye_landmarks[2] - eye_landmarks[4])
        C = np.linalg.norm(eye_landmarks[0] - eye_landmarks[3])
        
        return (A + B) / (2.0 * C + 1e-6)
    
    def _mouth_aspect_ratio(self, mouth_landmarks: np.ndarray) -> float:
        """Calculate mouth aspect ratio for mouth open detection"""
        if len(mouth_landmarks) < 10:
            return 0.0
        
        # Vertical distances
        V1 = np.linalg.norm(mouth_landmarks[1] - mouth_landmarks[7])
        V2 = np.linalg.norm(mouth_landmarks[3] - mouth_landmarks[9])
        
        # Horizontal distance
        H = np.linalg.norm(mouth_landmarks[0] - mouth_landmarks[4])
        
        return (V1 + V2) / (2.0 * H + 1e-6)
    
    def _estimate_head_pose(self, landmarks: np.ndarray) -> HeadPose:
        """Estimate 3D head pose from landmarks"""
        
        # Use face landmarks to estimate orientation
        # Nose tip and other points
        nose = landmarks[1]  # Nose tip
        left_eye = np.mean(landmarks[self.LEFT_EYE], axis=0)
        right_eye = np.mean(landmarks[self.RIGHT_EYE], axis=0)
        mouth = np.mean(landmarks[self.MOUTH], axis=0)
        
        # Calculate angles
        # Yaw: horizontal head turn
        eye_diff = right_eye[0] - left_eye[0]
        yaw = np.degrees(np.arctan2(nose[0] - np.mean([left_eye[0], right_eye[0]]), 
                                    abs(eye_diff) + 1e-6))
        
        # Pitch: up/down tilt
        vertical_ref = np.mean([left_eye[1], right_eye[1]])
        pitch = np.degrees(np.arctan2(nose[1] - vertical_ref, 
                                      abs(nose[0] - np.mean([left_eye[0], right_eye[0]])) + 1e-6))
        
        # Roll: side tilt
        left_to_right = right_eye - left_eye
        roll = np.degrees(np.arctan2(left_to_right[1], left_to_right[0]))
        
        return HeadPose(
            yaw=float(np.clip(yaw, -90, 90)),
            pitch=float(np.clip(pitch, -90, 90)),
            roll=float(np.clip(roll, -90, 90))
        )
    
    def _smooth_head_pose(self) -> HeadPose:
        """Apply temporal smoothing to head pose"""
        if not self.head_pose_history:
            return HeadPose(0, 0, 0)
        
        avg_yaw = np.mean([p.yaw for p in self.head_pose_history])
        avg_pitch = np.mean([p.pitch for p in self.head_pose_history])
        avg_roll = np.mean([p.roll for p in self.head_pose_history])
        
        return HeadPose(float(avg_yaw), float(avg_pitch), float(avg_roll))
    
    def _detect_smile(self, landmarks: np.ndarray) -> float:
        """Detect smile based on mouth corners and face geometry"""
        try:
            # Mouth corners
            left_mouth = landmarks[61]
            right_mouth = landmarks[291]
            mouth_center_top = landmarks[13]
            mouth_center_bottom = landmarks[14]
            
            # Cheek points
            left_cheek = landmarks[234]
            right_cheek = landmarks[454]
            
            # Mouth height
            mouth_height = abs(mouth_center_bottom[1] - mouth_center_top[1])
            
            # Cheek lift (positive = smiling)
            left_cheek_lift = max(0, left_cheek[1] - landmarks[323][1])
            right_cheek_lift = max(0, right_cheek[1] - landmarks[93][1])
            
            # Simple smile metric
            smile_score = min(1.0, (left_cheek_lift + right_cheek_lift + mouth_height) / 50)
            
            return float(smile_score)
        except:
            return 0.0
    
    def _draw_landmarks(self, image: np.ndarray, landmarks: np.ndarray, 
                       expressions: FacialExpressions) -> np.ndarray:
        """Draw facial landmarks and info on image"""
        
        # Draw key facial features
        h, w = image.shape[:2]
        
        # Eyes
        for eye_idx in [self.LEFT_EYE, self.RIGHT_EYE]:
            eye_points = landmarks[eye_idx].astype(int)
            cv2.polylines(image, [eye_points], True, (0, 255, 0), 1)
        
        # Mouth
        mouth_points = landmarks[self.MOUTH].astype(int)
        cv2.polylines(image, [mouth_points], True, (0, 0, 255), 1)
        
        # Nose
        nose_points = landmarks[self.NOSE].astype(int)
        cv2.polylines(image, [nose_points], True, (255, 0, 0), 1)
        
        # Draw head pose axes
        self._draw_head_pose_axes(image, landmarks, expressions.head_pose)
        
        # Draw info text
        info_text = f"Head: {expressions.head_pose}"
        cv2.putText(image, info_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.7, (0, 255, 0), 2)
        
        state = "Speaking" if expressions.is_speaking() else "Listening"
        if expressions.eyes_closed:
            state = "Eyes Closed"
        
        cv2.putText(image, f"State: {state}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX,
                   0.7, (0, 255, 0), 2)
        
        smile_text = f"Smile: {expressions.smiling:.2f}"
        cv2.putText(image, smile_text, (10, 110), cv2.FONT_HERSHEY_SIMPLEX,
                   0.7, (0, 255, 0), 2)
        
        return image
    
    def _draw_head_pose_axes(self, image: np.ndarray, landmarks: np.ndarray, 
                            pose: HeadPose, length: int = 50):
        """Draw 3D coordinate axes showing head orientation"""
        
        # Nose tip as origin
        nose_2d = landmarks[1][:2].astype(int)
        
        # Create rotation matrix from Euler angles
        yaw = np.radians(pose.yaw)
        pitch = np.radians(pose.pitch)
        roll = np.radians(pose.roll)
        
        # Rotation matrices
        Rz = np.array([
            [np.cos(yaw), -np.sin(yaw), 0],
            [np.sin(yaw), np.cos(yaw), 0],
            [0, 0, 1]
        ])
        
        Ry = np.array([
            [np.cos(pitch), 0, np.sin(pitch)],
            [0, 1, 0],
            [-np.sin(pitch), 0, np.cos(pitch)]
        ])
        
        Rx = np.array([
            [1, 0, 0],
            [0, np.cos(roll), -np.sin(roll)],
            [0, np.sin(roll), np.cos(roll)]
        ])
        
        # Combined rotation
        R = Rz @ Ry @ Rx
        
        # Axis points (in 3D)
        axis_length = length
        x_axis = np.array([axis_length, 0, 0])
        y_axis = np.array([0, -axis_length, 0])
        z_axis = np.array([0, 0, axis_length])
        
        # Rotate axes
        x_rot = R @ x_axis
        y_rot = R @ y_axis
        z_rot = R @ z_axis
        
        # Project to 2D
        x_2d = (nose_2d + x_rot[:2]).astype(int)
        y_2d = (nose_2d + y_rot[:2]).astype(int)
        z_2d = (nose_2d + z_rot[:2]).astype(int)
        
        # Draw axes
        cv2.line(image, tuple(nose_2d), tuple(x_2d), (0, 0, 255), 3)  # X: Red
        cv2.line(image, tuple(nose_2d), tuple(y_2d), (0, 255, 0), 3)  # Y: Green
        cv2.line(image, tuple(nose_2d), tuple(z_2d), (255, 0, 0), 3)  # Z: Blue


class WebcamTracker3D:
    """Real-time 3D face tracking from webcam"""
    
    def __init__(self, person_name: str = "Person"):
        self.person_name = person_name
        self.tracker = FaceTracker3D()
        self.cap = None
        self.running = False
        self.current_frame = None
        self.current_expressions = None
        self.frame_lock = threading.Lock()
    
    def start(self) -> bool:
        """Start webcam stream"""
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            return False
        
        self.running = True
        self._capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
        self._capture_thread.start()
        
        return True
    
    def _capture_loop(self):
        """Background thread for capturing and processing frames"""
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # Flip for selfie view
            frame = cv2.flip(frame, 1)
            
            # Process frame
            expressions, annotated = self.tracker.process_image(frame)
            
            with self.frame_lock:
                self.current_frame = annotated
                self.current_expressions = expressions
    
    def get_frame(self) -> Tuple[Optional[np.ndarray], Optional[FacialExpressions]]:
        """Get latest processed frame and expressions"""
        with self.frame_lock:
            return self.current_frame, self.current_expressions
    
    def stop(self):
        """Stop webcam stream"""
        self.running = False
        if self.cap:
            self.cap.release()
    
    def __del__(self):
        self.stop()


# Example usage and testing
if __name__ == "__main__":
    if not MEDIAPIPE_AVAILABLE:
        print("Installing MediaPipe...")
        import subprocess
        subprocess.check_call(["pip", "install", "mediapipe"])
    
    # Test with webcam
    print("Starting 3D face tracking... Press 'q' to quit")
    
    tracker = WebcamTracker3D("Test Person")
    if tracker.start():
        while True:
            frame, expressions = tracker.get_frame()
            
            if frame is not None:
                cv2.imshow("3D Face Tracking", frame)
                
                if expressions:
                    print(f"\n{expressions.head_pose}")
                    print(f"  Mouth: {expressions.mouth_open}")
                    print(f"  Eyes: L={expressions.left_eye_open:.2f} R={expressions.right_eye_open:.2f}")
                    print(f"  Smile: {expressions.smiling:.2f}")
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        tracker.stop()
        cv2.destroyAllWindows()
    else:
        print("Could not start webcam!")
