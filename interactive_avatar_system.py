"""
Interactive Avatar System - Complete Integration
Avatars watch you, read your emotions, and respond naturally
"""

from facial_expression_detector import FacialExpressionDetector, UserEmotion
from avatar_with_eye_tracking import AvatarWithEyeTracking, PersonaStyle, Emotion
import threading
import time
from PIL import Image

class InteractiveAvatarSystem:
    """
    Complete system that connects camera → expression detection → avatar response
    The avatars' eyes follow your face and they respond to your emotions
    """
    
    def __init__(self):
        # Expression detector
        self.detector = FacialExpressionDetector()
        
        # Create avatars for each sister
        self.avatars = {
            "Erryn": AvatarWithEyeTracking(PersonaStyle.erryn(), size=300),
            "Viress": AvatarWithEyeTracking(PersonaStyle.viress(), size=300),
            "Echochild": AvatarWithEyeTracking(PersonaStyle.echochild(), size=300)
        }
        
        # Currently active avatar
        self.active_avatar_name = "Erryn"
        
        # System state
        self.running = False
        self.update_thread = None
        
        # Emotion response mappings
        self.emotion_responses = {
            UserEmotion.HAPPY: Emotion.HAPPY,
            UserEmotion.SAD: Emotion.LOVING,  # Be comforting
            UserEmotion.SURPRISED: Emotion.EXCITED,
            UserEmotion.ANGRY: Emotion.CALM,  # Stay calm to defuse
            UserEmotion.NEUTRAL: Emotion.CALM,
            UserEmotion.FEARFUL: Emotion.LOVING,  # Be reassuring
            UserEmotion.DISGUSTED: Emotion.CONFUSED
        }
        
    def start(self, camera_index=0):
        """Start the interactive avatar system"""
        if self.running:
            return True
            
        # Start camera
        if not self.detector.start_camera(camera_index):
            return False
            
        self.running = True
        
        # Start update loop in background thread
        self.update_thread = threading.Thread(target=self._update_loop, daemon=True)
        self.update_thread.start()
        
        print("✅ Interactive Avatar System started!")
        return True
        
    def stop(self):
        """Stop the system"""
        self.running = False
        self.detector.stop_camera()
        
        if self.update_thread:
            self.update_thread.join(timeout=2)
            
        print("🛑 Interactive Avatar System stopped")
        
    def set_active_avatar(self, name: str):
        """Switch which sister is currently active"""
        if name in self.avatars:
            self.active_avatar_name = name
            print(f"👋 Switched to {name}")
            
    def get_active_avatar(self) -> AvatarWithEyeTracking:
        """Get the currently active avatar"""
        return self.avatars[self.active_avatar_name]
        
    def set_avatar_speaking(self, speaking: bool):
        """Set whether avatar is currently speaking"""
        avatar = self.get_active_avatar()
        avatar.set_speaking(speaking)
        
    def _update_loop(self):
        """
        Background loop that continuously:
        1. Detects user's face and emotion
        2. Updates avatar gaze to track face
        3. Updates avatar emotion to respond to user
        """
        blink_timer = 0
        blink_duration = 0.2  # seconds
        next_blink = time.time() + 3  # Random blinks every 3-5 seconds
        
        while self.running:
            # Detect user expression
            user_emotion, confidence, face_pos = self.detector.detect_expression()
            
            # Get face center for eye tracking
            face_center = self.detector.get_face_center()
            
            # Update avatar for each sister
            for avatar_name, avatar in self.avatars.items():
                # Track user's face with eyes
                if face_center:
                    avatar.set_gaze_target(face_center[0], face_center[1])
                else:
                    # No face detected - look forward
                    avatar.set_gaze_target(0, 0)
                    
                # Respond to user's emotion (only if confident)
                if confidence > 0.6:
                    response_emotion = self.emotion_responses.get(
                        user_emotion, 
                        Emotion.CALM
                    )
                    avatar.set_emotion(response_emotion)
                    
            # Blink animation
            current_time = time.time()
            if current_time >= next_blink:
                blink_timer = blink_duration
                next_blink = current_time + (3 + (hash(str(current_time)) % 2))
                
            if blink_timer > 0:
                # Blink animation curve
                progress = 1 - (blink_timer / blink_duration)
                if progress < 0.5:
                    blink_amount = progress * 2  # Close
                else:
                    blink_amount = (1 - progress) * 2  # Open
                    
                for avatar in self.avatars.values():
                    avatar.set_blink(blink_amount)
                    
                blink_timer -= 0.03
            else:
                for avatar in self.avatars.values():
                    avatar.set_blink(0)
                    
            # Small delay to prevent excessive CPU usage
            time.sleep(0.03)  # ~30 FPS update rate
            
    def render_active_avatar(self) -> Image:
        """
        Get the rendered image of the currently active avatar
        Returns: PIL Image
        """
        avatar = self.get_active_avatar()
        return avatar.render()
        
    def get_current_status(self):
        """
        Get current system status for display
        Returns: dict with status info
        """
        emotion, confidence, face_pos = self.detector.detect_expression()
        face_center = self.detector.get_face_center()
        avatar = self.get_active_avatar()
        
        return {
            "active_avatar": self.active_avatar_name,
            "user_emotion": emotion.value,
            "emotion_confidence": confidence,
            "face_detected": face_pos is not None,
            "face_center": face_center,
            "avatar_emotion": avatar.emotion.value,
            "avatar_gaze": avatar.gaze_target,
            "running": self.running
        }


# Test the complete system
if __name__ == "__main__":
    import cv2
    
    print("🎭 Testing Interactive Avatar System...")
    print("=" * 60)
    
    system = InteractiveAvatarSystem()
    
    if not system.start():
        print("❌ Failed to start system")
        exit(1)
        
    print("\n✅ System running!")
    print("📹 Camera is tracking your face")
    print("👁️  Avatars are watching you")
    print("😊 They respond to your emotions")
    print("\nControls:")
    print("  1/2/3 - Switch avatar (Erryn/Viress/Echochild)")
    print("  SPACE - Toggle speaking animation")
    print("  'q'   - Quit")
    print("=" * 60)
    
    speaking = False
    
    try:
        while True:
            # Get camera feed with detection overlay
            camera_frame = system.detector.get_frame_with_overlay()
            
            # Render active avatar
            avatar_img = system.render_active_avatar()
            avatar_frame = cv2.cvtColor(
                cv2.cvtColor(avatar_img.convert('RGB'), cv2.COLOR_RGB2BGR),
                cv2.COLOR_BGR2RGB
            )
            
            # Display both windows
            if camera_frame is not None:
                cv2.imshow('Camera - Expression Detection', camera_frame)
            cv2.imshow('Avatar - Interactive Response', cv2.cvtColor(avatar_frame, cv2.COLOR_RGB2BGR))
            
            # Print status
            status = system.get_current_status()
            print(f"👤 User: {status['user_emotion'].upper():12} ({status['emotion_confidence']:.0%}) | "
                  f"🤖 {status['active_avatar']}: {status['avatar_emotion'].upper():12}", 
                  end='\r')
            
            # Handle keyboard
            key = cv2.waitKey(30) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('1'):
                system.set_active_avatar("Erryn")
            elif key == ord('2'):
                system.set_active_avatar("Viress")
            elif key == ord('3'):
                system.set_active_avatar("Echochild")
            elif key == ord(' '):
                speaking = not speaking
                system.set_avatar_speaking(speaking)
                print(f"\n🗣️  Speaking: {speaking}")
                
    except KeyboardInterrupt:
        print("\n\n⏹️  Interrupted by user")
    finally:
        system.stop()
        cv2.destroyAllWindows()
        print("\n✅ System test complete!")
