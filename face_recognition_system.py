"""
Face Recognition System for the Sisters
- Build face database from family photos
- Recognize people in webcam/images
- Store encodings per sister's memory

Note: Uses OpenCV Haar Cascades (no dlib/CMake needed)
For production use, install: pip install cmake dlib face-recognition
"""

import os
import pickle
from pathlib import Path
from typing import Dict, List, Tuple

try:
    import cv2
    import numpy as np
    FACE_REC_AVAILABLE = True
except ImportError as e:
    FACE_REC_AVAILABLE = False
    raise

# Try face_recognition (requires dlib/cmake), fall back to OpenCV
try:
    import face_recognition
    HAS_FACE_RECOGNITION = True
except ImportError:
    HAS_FACE_RECOGNITION = False
    print("⚠️ face_recognition not available (needs dlib/cmake). Using OpenCV fallback.")


class FaceDatabase:
    """Manage face encodings and recognition"""
    
    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
        self.db_path = self.base_dir / "face_encodings.pkl"
        self.known_faces: Dict[str, List] = {}  # {name: [face_encodings...]}
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.load_database()
    
    def load_database(self):
        """Load existing face database from disk"""
        if self.db_path.exists():
            with open(self.db_path, 'rb') as f:
                self.known_faces = pickle.load(f)
    
    def save_database(self):
        """Save face database to disk"""
        with open(self.db_path, 'wb') as f:
            pickle.dump(self.known_faces, f)
    
    def add_faces_from_image(self, image_path: str, person_name: str):
        """Extract and store face regions from an image"""
        try:
            image = cv2.imread(image_path)
            if image is None:
                return 0
            
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            if len(faces) == 0:
                return 0
            
            if person_name not in self.known_faces:
                self.known_faces[person_name] = []
            
            # Store face regions as numpy arrays
            for (x, y, w, h) in faces:
                face_region = image[y:y+h, x:x+w]
                # Convert to bytes for storage
                face_bytes = cv2.imencode('.jpg', face_region)[1].tobytes()
                self.known_faces[person_name].append(face_bytes)
            
            self.save_database()
            return len(faces)
        except Exception as e:
            print(f"Error adding faces from {image_path}: {e}")
            return 0
    
    def recognize_faces(self, image_path: str, tolerance: float = 0.6) -> List[Tuple[str, float]]:
        """Recognize faces in an image. Returns [(name, confidence)...]"""
        try:
            image = cv2.imread(image_path)
            if image is None:
                return []
            
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            unknown_faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            results = []
            for (x, y, w, h) in unknown_faces:
                # Simple heuristic: match against known faces
                face_region = image[y:y+h, x:x+w]
                
                best_match = ("Unknown", 0.0)
                for name, known_face_list in self.known_faces.items():
                    for known_face_bytes in known_face_list:
                        # Decode stored face
                        nparr = np.frombuffer(known_face_bytes, np.uint8)
                        known_face = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                        
                        # Simple similarity: histogram comparison
                        if known_face is not None and known_face.shape[:2] == face_region.shape[:2]:
                            # Resize to match
                            known_face = cv2.resize(known_face, (w, h))
                            
                            # Use template matching score
                            hist_known = cv2.calcHist([known_face], [0, 1, 2], None, [8, 8, 8],
                                                      [0, 256, 0, 256, 0, 256])
                            hist_unknown = cv2.calcHist([face_region], [0, 1, 2], None, [8, 8, 8],
                                                        [0, 256, 0, 256, 0, 256])
                            
                            similarity = cv2.compareHist(hist_known, hist_unknown, cv2.HISTCMP_CORREL)
                            
                            if similarity > best_match[1]:
                                best_match = (name, similarity)
                
                if best_match[1] > tolerance:
                    results.append(best_match)
                else:
                    results.append(("Unknown", 0.0))
            
            return results
        except Exception as e:
            print(f"Error recognizing faces: {e}")
            return []


class WebcamDetector:
    """Real-time face detection from webcam"""
    
    def __init__(self, face_db: FaceDatabase):
        self.face_db = face_db
        self.cap = None
        self.running = False
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
    
    def start_webcam(self):
        """Initialize webcam"""
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("Could not open webcam")
        self.running = True
    
    def get_frame_with_faces(self) -> Tuple[bool, np.ndarray, List[str]]:
        """Get next frame with face detection overlays. Returns (success, frame, detected_names)"""
        if not self.running or self.cap is None:
            return False, None, []
        
        ret, frame = self.cap.read()
        if not ret:
            return False, None, []
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        detected_names = []
        face_labels = []
        
        for (x, y, w, h) in faces:
            face_region = frame[y:y+h, x:x+w]
            
            # Simple matching against known faces
            best_match = ("Unknown", 0.0)
            for name, known_face_list in self.face_db.known_faces.items():
                for known_face_bytes in known_face_list:
                    try:
                        # Decode stored face
                        nparr = np.frombuffer(known_face_bytes, np.uint8)
                        known_face = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                        
                        if known_face is not None:
                            # Resize to match
                            known_face = cv2.resize(known_face, (w, h))
                            
                            # Histogram comparison
                            hist_known = cv2.calcHist([known_face], [0, 1, 2], None, [8, 8, 8],
                                                      [0, 256, 0, 256, 0, 256])
                            hist_unknown = cv2.calcHist([face_region], [0, 1, 2], None, [8, 8, 8],
                                                        [0, 256, 0, 256, 0, 256])
                            
                            similarity = cv2.compareHist(hist_known, hist_unknown, cv2.HISTCMP_CORREL)
                            
                            if similarity > best_match[1]:
                                best_match = (name, similarity)
                    except:
                        pass
            
            label = best_match[0] if best_match[1] > 0.5 else "Unknown"
            detected_names.append(label)
            face_labels.append(label)
            
            # Draw box and label
            color = (0, 255, 0) if label != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.rectangle(frame, (x, y-35), (x+w, y), color, cv2.FILLED)
            cv2.putText(frame, label, (x+6, y-6), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
        
        return True, frame, detected_names
    
    def stop_webcam(self):
        """Stop webcam"""
        if self.cap:
            self.cap.release()
        self.running = False


# Test
if __name__ == "__main__":
    db = FaceDatabase(Path("./data"))
    print(f"Known faces: {list(db.known_faces.keys())}")
