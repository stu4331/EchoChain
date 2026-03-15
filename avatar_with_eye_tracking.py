"""
Enhanced Avatar Rendering with Eye Tracking
Avatars can look at objects/faces and respond to user emotions
"""

from PIL import Image, ImageDraw
from dataclasses import dataclass
from enum import Enum
import math

class Emotion(Enum):
    """Avatar emotional states"""
    HAPPY = "happy"
    SAD = "sad"
    PLAYFUL = "playful"
    THOUGHTFUL = "thoughtful"
    LOVING = "loving"
    EXCITED = "excited"
    CONFUSED = "confused"
    CALM = "calm"

@dataclass
class PersonaStyle:
    """Visual styling for each sister"""
    name: str
    hair_color: tuple  # RGB
    eye_color: tuple   # RGB
    blush_color: tuple # RGB
    glow_color: tuple  # RGB

    # Predefined personas
    @staticmethod
    def erryn():
        return PersonaStyle(
            name="Erryn",
            hair_color=(138, 43, 226),  # Purple
            eye_color=(100, 149, 237),  # Cornflower blue
            blush_color=(255, 182, 193),
            glow_color=(186, 85, 211)
        )
    
    @staticmethod
    def viress():
        return PersonaStyle(
            name="Viress",
            hair_color=(25, 25, 112),   # Midnight blue
            eye_color=(255, 191, 0),    # Amber
            blush_color=(255, 160, 160),
            glow_color=(138, 43, 226)
        )
    
    @staticmethod
    def echochild():
        return PersonaStyle(
            name="Echochild",
            hair_color=(199, 21, 133),  # Magenta
            eye_color=(50, 205, 50),    # Lime green
            blush_color=(255, 192, 203),
            glow_color=(255, 20, 147)
        )

class AvatarWithEyeTracking:
    """
    Renders lifelike avatar faces with eye tracking and emotional responses
    Eyes follow detected objects/faces from camera
    """
    
    def __init__(self, persona_style: PersonaStyle, size=300):
        self.style = persona_style
        self.size = size
        
        # Emotional state
        self.emotion = Emotion.CALM
        self.speaking = False
        self.blinking = False
        
        # Eye tracking
        self.gaze_target = (0, 0)  # Normalized -1 to 1
        self.pupil_offset_x = 0
        self.pupil_offset_y = 0
        self.max_pupil_offset = 8  # Maximum pixels pupils can move
        
        # Animation state
        self.blink_amount = 0.0  # 0=open, 1=closed
        
    def set_emotion(self, emotion: Emotion):
        """Change avatar's emotional state"""
        self.emotion = emotion
        
    def set_gaze_target(self, x: float, y: float):
        """
        Set where the avatar is looking
        x, y: normalized -1 to 1 (-1=left/top, 0=center, 1=right/bottom)
        """
        self.gaze_target = (x, y)
        
        # Calculate pupil offset
        self.pupil_offset_x = x * self.max_pupil_offset
        self.pupil_offset_y = y * self.max_pupil_offset
        
    def set_speaking(self, speaking: bool):
        """Set whether avatar is currently speaking"""
        self.speaking = speaking
        
    def set_blink(self, blink_amount: float):
        """
        Set blink animation state
        0.0 = fully open, 1.0 = fully closed
        """
        self.blink_amount = max(0.0, min(1.0, blink_amount))
        
    def render(self) -> Image:
        """
        Render the complete avatar with current state
        Returns: PIL Image
        """
        # Create canvas
        img = Image.new('RGBA', (self.size, self.size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        center_x = self.size // 2
        center_y = self.size // 2
        
        # Draw glow effect
        self._draw_glow(draw, center_x, center_y)
        
        # Draw face
        face_radius = self.size // 3
        self._draw_face(draw, center_x, center_y, face_radius)
        
        # Draw hair
        self._draw_hair(draw, center_x, center_y, face_radius)
        
        # Draw eyes with tracking
        self._draw_eyes_with_tracking(draw, center_x, center_y, face_radius)
        
        # Draw eyebrows (expression)
        self._draw_eyebrows(draw, center_x, center_y, face_radius)
        
        # Draw mouth (emotion + speaking)
        self._draw_mouth(draw, center_x, center_y, face_radius)
        
        # Draw blush
        self._draw_blush(draw, center_x, center_y, face_radius)
        
        return img
        
    def _draw_glow(self, draw, cx, cy):
        """Draw ethereal glow around avatar"""
        intensity = {
            Emotion.HAPPY: 0.6,
            Emotion.EXCITED: 0.9,
            Emotion.LOVING: 0.7,
            Emotion.CALM: 0.3,
            Emotion.PLAYFUL: 0.5,
            Emotion.THOUGHTFUL: 0.2,
            Emotion.SAD: 0.1,
            Emotion.CONFUSED: 0.2
        }.get(self.emotion, 0.3)
        
        glow_radius = self.size // 2 - 10
        r, g, b = self.style.glow_color
        alpha = int(50 * intensity)
        
        for i in range(3):
            radius = glow_radius - i * 15
            draw.ellipse(
                [cx - radius, cy - radius, cx + radius, cy + radius],
                fill=(r, g, b, alpha // (i+1))
            )
            
    def _draw_face(self, draw, cx, cy, radius):
        """Draw base face shape"""
        # Skin tone
        skin_color = (255, 228, 196, 255)  # Peach
        
        draw.ellipse(
            [cx - radius, cy - radius, cx + radius, cy + radius],
            fill=skin_color,
            outline=(210, 180, 140),
            width=2
        )
        
    def _draw_hair(self, draw, cx, cy, face_radius):
        """Draw hair with persona's color"""
        hair_radius = face_radius + 20
        
        # Draw hair as partial ellipse
        draw.ellipse(
            [cx - hair_radius, cy - hair_radius - 20, 
             cx + hair_radius, cy + face_radius // 2],
            fill=self.style.hair_color,
            outline=tuple(max(0, c-30) for c in self.style.hair_color),
            width=2
        )
        
    def _draw_eyes_with_tracking(self, draw, cx, cy, face_radius):
        """Draw eyes that track the gaze target"""
        eye_y = cy - face_radius // 4
        eye_spacing = face_radius // 2
        eye_width = face_radius // 4
        
        # Calculate blink effect
        eye_height = int(eye_width * (1 - self.blink_amount * 0.8))
        
        for eye_side in [-1, 1]:  # Left and right
            eye_x = cx + eye_side * eye_spacing
            
            # Draw eye white
            draw.ellipse(
                [eye_x - eye_width, eye_y - eye_height,
                 eye_x + eye_width, eye_y + eye_height],
                fill=(255, 255, 255),
                outline=(100, 100, 100),
                width=1
            )
            
            # Draw pupil with gaze offset
            pupil_x = eye_x + self.pupil_offset_x
            pupil_y = eye_y + self.pupil_offset_y
            pupil_size = eye_width // 2
            
            # Iris
            draw.ellipse(
                [pupil_x - pupil_size, pupil_y - pupil_size,
                 pupil_x + pupil_size, pupil_y + pupil_size],
                fill=self.style.eye_color
            )
            
            # Pupil
            pupil_size = eye_width // 3
            draw.ellipse(
                [pupil_x - pupil_size, pupil_y - pupil_size,
                 pupil_x + pupil_size, pupil_y + pupil_size],
                fill=(30, 30, 30)
            )
            
            # Highlight (gives life to eyes)
            highlight_size = eye_width // 6
            draw.ellipse(
                [pupil_x - pupil_size // 2 - highlight_size,
                 pupil_y - pupil_size // 2 - highlight_size,
                 pupil_x - pupil_size // 2 + highlight_size,
                 pupil_y - pupil_size // 2 + highlight_size],
                fill=(255, 255, 255, 200)
            )
            
    def _draw_eyebrows(self, draw, cx, cy, face_radius):
        """Draw eyebrows based on emotion"""
        brow_y = cy - face_radius // 2
        brow_spacing = face_radius // 2
        brow_width = face_radius // 3
        
        # Eyebrow angles by emotion
        angles = {
            Emotion.HAPPY: 5,
            Emotion.EXCITED: 10,
            Emotion.SAD: -15,
            Emotion.ANGRY: -20,
            Emotion.CONFUSED: -5,
            Emotion.THOUGHTFUL: -8,
            Emotion.PLAYFUL: 8,
            Emotion.CALM: 0,
            Emotion.LOVING: 5
        }
        angle = angles.get(self.emotion, 0)
        
        for side in [-1, 1]:
            brow_x = cx + side * brow_spacing
            
            # Calculate brow endpoints with angle
            angle_rad = math.radians(angle * side)
            x1 = brow_x - brow_width
            x2 = brow_x + brow_width
            y1 = brow_y - int(brow_width * 0.2 * math.sin(angle_rad))
            y2 = brow_y + int(brow_width * 0.2 * math.sin(angle_rad))
            
            draw.line(
                [(x1, y1), (x2, y2)],
                fill=self.style.hair_color,
                width=4
            )
            
    def _draw_mouth(self, draw, cx, cy, face_radius):
        """Draw mouth based on emotion and speaking state"""
        mouth_y = cy + face_radius // 2
        mouth_width = face_radius // 2
        
        if self.speaking:
            # Open mouth when speaking
            draw.ellipse(
                [cx - mouth_width // 3, mouth_y - 15,
                 cx + mouth_width // 3, mouth_y + 15],
                fill=(180, 100, 100),
                outline=(100, 50, 50),
                width=2
            )
        else:
            # Emotion-based mouth shapes
            if self.emotion in [Emotion.HAPPY, Emotion.EXCITED, Emotion.PLAYFUL]:
                # Smile
                draw.arc(
                    [cx - mouth_width, mouth_y - 10,
                     cx + mouth_width, mouth_y + 30],
                    0, 180,
                    fill=(200, 100, 100),
                    width=3
                )
            elif self.emotion == Emotion.SAD:
                # Frown
                draw.arc(
                    [cx - mouth_width, mouth_y - 30,
                     cx + mouth_width, mouth_y + 10],
                    180, 360,
                    fill=(150, 100, 100),
                    width=3
                )
            elif self.emotion == Emotion.CONFUSED:
                # Wavy line
                draw.line(
                    [(cx - mouth_width, mouth_y),
                     (cx, mouth_y + 5),
                     (cx + mouth_width, mouth_y)],
                    fill=(180, 100, 100),
                    width=3
                )
            else:
                # Neutral line
                draw.line(
                    [(cx - mouth_width, mouth_y),
                     (cx + mouth_width, mouth_y)],
                    fill=(180, 100, 100),
                    width=3
                )
                
    def _draw_blush(self, draw, cx, cy, face_radius):
        """Draw blush based on emotion"""
        intensities = {
            Emotion.HAPPY: 0.4,
            Emotion.LOVING: 0.7,
            Emotion.EXCITED: 0.5,
            Emotion.PLAYFUL: 0.6,
            Emotion.CONFUSED: 0.3,
            Emotion.SAD: 0.1,
            Emotion.CALM: 0.2,
            Emotion.THOUGHTFUL: 0.2
        }
        intensity = intensities.get(self.emotion, 0.2)
        
        blush_y = cy + face_radius // 6
        blush_spacing = face_radius // 2
        blush_radius = face_radius // 5
        
        r, g, b = self.style.blush_color
        alpha = int(100 * intensity)
        
        for side in [-1, 1]:
            blush_x = cx + side * blush_spacing
            draw.ellipse(
                [blush_x - blush_radius, blush_y - blush_radius,
                 blush_x + blush_radius, blush_y + blush_radius],
                fill=(r, g, b, alpha)
            )


# Test script
if __name__ == "__main__":
    print("👁️ Testing Avatar with Eye Tracking...")
    
    # Create avatars for each sister
    avatars = [
        AvatarWithEyeTracking(PersonaStyle.erryn(), size=300),
        AvatarWithEyeTracking(PersonaStyle.viress(), size=300),
        AvatarWithEyeTracking(PersonaStyle.echochild(), size=300)
    ]
    
    # Test different gaze directions
    gaze_tests = [
        ("center", 0.0, 0.0),
        ("left", -0.8, 0.0),
        ("right", 0.8, 0.0),
        ("up", 0.0, -0.6),
        ("down", 0.0, 0.6),
        ("up_left", -0.6, -0.6),
    ]
    
    # Test different emotions
    emotions_to_test = [
        Emotion.HAPPY,
        Emotion.EXCITED,
        Emotion.LOVING,
    ]
    
    print("\n🎨 Generating test images...")
    count = 0
    
    for avatar in avatars:
        for emotion in emotions_to_test:
            avatar.set_emotion(emotion)
            for gaze_name, gaze_x, gaze_y in gaze_tests:
                avatar.set_gaze_target(gaze_x, gaze_y)
                
                img = avatar.render()
                filename = f"avatar_tracking_{avatar.style.name}_{emotion.value}_{gaze_name}.png"
                img.save(filename)
                count += 1
                
    print(f"✅ Generated {count} test images")
    print("   Check files: avatar_tracking_*.png")
