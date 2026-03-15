"""
Enhanced 3D Avatar Renderer - Human-like faces with head pose tracking

This version integrates with face_tracking_3d.py to create more realistic,
responsive avatars that react to head movements and facial expressions.

Features:
- 3D head orientation (yaw, pitch, roll)
- Eye gaze following
- Realistic mouth shapes based on openness
- Emotion-driven expression changes
- Smooth animations
"""

from enum import Enum
from dataclasses import dataclass
from PIL import Image, ImageDraw
import io
import math
from typing import Tuple
import numpy as np


class Emotion(Enum):
    HAPPY = ("happy", (255, 200, 50))
    SAD = ("sad", (100, 150, 200))
    PLAYFUL = ("playful", (255, 150, 100))
    THOUGHTFUL = ("thoughtful", (180, 150, 200))
    LOVING = ("loving", (255, 100, 150))
    EXCITED = ("excited", (255, 100, 50))
    CONFUSED = ("confused", (200, 150, 100))
    CALM = ("calm", (150, 200, 180))
    SPEAKING = ("speaking", (200, 100, 100))


@dataclass
class PersonaStyle:
    name: str
    hair_color: tuple      # RGB
    skin_tone: tuple       # RGB
    eye_color: tuple       # RGB
    blush_color: tuple     # RGB
    glow_color: tuple      # RGB
    hair_style: str        # 'wavy', 'straight', 'curly'


class Avatar3DRenderer:
    """Render detailed, 3D-aware avatar faces with head pose tracking"""
    
    PERSONA_STYLES = {
        "Erryn": PersonaStyle(
            name="Erryn",
            hair_color=(150, 100, 200),      # Purple-ish
            skin_tone=(240, 200, 180),       # Warm
            eye_color=(100, 200, 255),       # Blue
            blush_color=(220, 120, 150),     # Pink
            glow_color=(150, 100, 200),      # Purple glow
            hair_style='wavy'
        ),
        "Viress": PersonaStyle(
            name="Viress",
            hair_color=(50, 100, 150),       # Dark blue
            skin_tone=(230, 210, 200),       # Cool
            eye_color=(200, 100, 50),        # Amber
            blush_color=(180, 100, 120),     # Muted
            glow_color=(50, 100, 150),       # Blue glow
            hair_style='straight'
        ),
        "Echochild": PersonaStyle(
            name="Echochild",
            hair_color=(180, 80, 120),       # Magenta
            skin_tone=(250, 220, 210),       # Light
            eye_color=(50, 150, 100),        # Green
            blush_color=(255, 150, 180),     # Bright pink
            glow_color=(180, 80, 120),       # Magenta glow
            hair_style='curly'
        ),
    }
    
    def __init__(self, persona: str = "Erryn", size: int = 300):
        self.persona = persona
        self.size = size
        self.style = self.PERSONA_STYLES.get(persona, self.PERSONA_STYLES["Erryn"])
        
        self.emotion = Emotion.CALM
        self.is_speaking = False
        self.blink_state = False
        
        # 3D head pose
        self.head_yaw = 0.0      # -90 to 90 (left to right)
        self.head_pitch = 0.0    # -90 to 90 (down to up)
        self.head_roll = 0.0     # -90 to 90 (tilt)
        
        # Facial expression metrics (0.0 to 1.0)
        self.mouth_openness = 0.0
        self.left_eye_openness = 1.0
        self.right_eye_openness = 1.0
        self.smile_intensity = 0.0
    
    def set_emotion(self, emotion: Emotion):
        """Set current emotion"""
        self.emotion = emotion
    
    def set_speaking(self, speaking: bool):
        """Set speaking state"""
        self.is_speaking = speaking
    
    def set_blink(self, blink: bool):
        """Set blink state"""
        self.blink_state = blink
    
    def set_head_pose(self, yaw: float, pitch: float, roll: float):
        """Set 3D head orientation
        
        Args:
            yaw: -90 (left) to 90 (right) degrees
            pitch: -90 (down) to 90 (up) degrees
            roll: -90 (left tilt) to 90 (right tilt) degrees
        """
        self.head_yaw = np.clip(yaw, -90, 90)
        self.head_pitch = np.clip(pitch, -90, 90)
        self.head_roll = np.clip(roll, -90, 90)
    
    def set_facial_metrics(self, mouth_open: float = None, 
                          left_eye_open: float = None,
                          right_eye_open: float = None,
                          smile: float = None):
        """Set facial expression metrics
        
        Args:
            mouth_open: 0.0 (closed) to 1.0 (wide open)
            left_eye_open: 0.0 (closed) to 1.0 (wide open)
            right_eye_open: 0.0 (closed) to 1.0 (wide open)
            smile: 0.0 (frown) to 1.0 (big smile)
        """
        if mouth_open is not None:
            self.mouth_openness = np.clip(mouth_open, 0.0, 1.0)
        if left_eye_open is not None:
            self.left_eye_openness = np.clip(left_eye_open, 0.0, 1.0)
        if right_eye_open is not None:
            self.right_eye_openness = np.clip(right_eye_open, 0.0, 1.0)
        if smile is not None:
            self.smile_intensity = np.clip(smile, 0.0, 1.0)
    
    def render(self) -> Image.Image:
        """Render avatar face as PIL Image with 3D perspective"""
        img = Image.new('RGBA', (self.size, self.size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img, 'RGBA')
        
        center_x = self.size // 2
        center_y = self.size // 2
        
        # Apply perspective transform based on head pose
        transform_offset_x = (self.head_yaw / 90.0) * (self.size * 0.15)
        transform_offset_y = (self.head_pitch / 90.0) * (self.size * 0.15)
        
        # Scale based on pitch (looking down = smaller, looking up = larger)
        scale_factor = 1.0 + (self.head_pitch / 180.0) * 0.2
        
        # Adjust center for perspective
        center_x += transform_offset_x
        center_y -= transform_offset_y
        
        # --- Hair ---
        self._draw_hair_3d(draw, center_x, center_y, scale_factor)
        
        # --- Face (with glow) ---
        self._draw_face_3d(draw, center_x, center_y, scale_factor)
        
        # --- Blush (emotional expression) ---
        if self.emotion in [Emotion.HAPPY, Emotion.LOVING, Emotion.EXCITED, Emotion.PLAYFUL]:
            self._draw_blush_3d(draw, center_x, center_y, scale_factor)
        
        # --- Eyes ---
        self._draw_eyes_3d(draw, center_x, center_y, scale_factor)
        
        # --- Nose ---
        self._draw_nose_3d(draw, center_x, center_y, scale_factor)
        
        # --- Mouth (emotion-driven) ---
        self._draw_mouth_3d(draw, center_x, center_y, scale_factor)
        
        # --- Eyebrows (emotion-driven) ---
        self._draw_eyebrows_3d(draw, center_x, center_y, scale_factor)
        
        # --- Shadow for 3D effect ---
        self._draw_shadow_3d(draw, center_x, center_y, scale_factor)
        
        return img
    
    def _draw_face_3d(self, draw: ImageDraw.ImageDraw, cx: float, cy: float, scale: float):
        """Draw face with 3D perspective"""
        face_radius = self.size // 2.3 * scale
        
        # Glow
        glow_radius = face_radius + 5
        glow_alpha = 50 if self.emotion in [Emotion.EXCITED, Emotion.HAPPY, Emotion.LOVING] else 20
        draw.ellipse(
            [(cx - glow_radius, cy - glow_radius),
             (cx + glow_radius, cy + glow_radius)],
            fill=(*self.style.glow_color, glow_alpha)
        )
        
        # Face (ellipse for perspective)
        # Adjust horizontal radius based on yaw
        h_radius = face_radius * (1.0 - abs(self.head_yaw / 180.0) * 0.3)
        
        draw.ellipse(
            [(cx - h_radius, cy - face_radius),
             (cx + h_radius, cy + face_radius)],
            fill=(*self.style.skin_tone, 255)
        )
    
    def _draw_blush_3d(self, draw: ImageDraw.ImageDraw, cx: float, cy: float, scale: float):
        """Draw blush with 3D positioning"""
        face_radius = self.size // 2.3 * scale
        blush_radius = face_radius * 0.15
        
        # Left blush
        blush_x = cx - face_radius * 0.4 - (self.head_yaw / 90.0) * blush_radius
        blush_y = cy + face_radius * 0.1
        
        intensity = int(100 * (0.5 + self.smile_intensity * 0.5))
        
        draw.ellipse(
            [(blush_x - blush_radius, blush_y - blush_radius),
             (blush_x + blush_radius, blush_y + blush_radius)],
            fill=(*self.style.blush_color, intensity)
        )
        
        # Right blush
        blush_x2 = cx + face_radius * 0.4 - (self.head_yaw / 90.0) * blush_radius
        draw.ellipse(
            [(blush_x2 - blush_radius, blush_y - blush_radius),
             (blush_x2 + blush_radius, blush_y + blush_radius)],
            fill=(*self.style.blush_color, intensity)
        )
    
    def _draw_eyes_3d(self, draw: ImageDraw.ImageDraw, cx: float, cy: float, scale: float):
        """Draw eyes with 3D perspective and gaze"""
        face_radius = self.size // 2.3 * scale
        eye_y = cy - face_radius * 0.25
        eye_spacing = face_radius * 0.3
        
        # Blink animation
        if self.blink_state:
            # Closed eyes (lines)
            line_y_offset = 2
            draw.line(
                [(cx - eye_spacing - face_radius * 0.15, eye_y),
                 (cx - eye_spacing + face_radius * 0.15, eye_y)],
                fill=(0, 0, 0, 180),
                width=2
            )
            draw.line(
                [(cx + eye_spacing - face_radius * 0.15, eye_y),
                 (cx + eye_spacing + face_radius * 0.15, eye_y)],
                fill=(0, 0, 0, 180),
                width=2
            )
            return
        
        # Open eyes
        eye_size = face_radius * 0.08
        
        # Adjust eye position for head yaw
        eye_offset = (self.head_yaw / 90.0) * eye_size * 0.5
        
        # Left eye
        self._draw_single_eye_3d(draw, cx - eye_spacing + eye_offset, eye_y, eye_size,
                               self.left_eye_openness)
        # Right eye
        self._draw_single_eye_3d(draw, cx + eye_spacing + eye_offset, eye_y, eye_size,
                               self.right_eye_openness)
    
    def _draw_single_eye_3d(self, draw: ImageDraw.ImageDraw, ex: float, ey: float, 
                           size: float, openness: float):
        """Draw one eye with 3D effects"""
        if openness < 0.1:
            # Closed
            draw.line([(ex - size, ey), (ex + size, ey)], fill=(0, 0, 0, 180), width=2)
            return
        
        # Sclera (white)
        sclera_height = size * openness
        draw.ellipse(
            [(ex - size, ey - sclera_height), (ex + size, ey + sclera_height)],
            fill=(255, 255, 255, 255)
        )
        
        # Iris (affected by gaze)
        iris_x_offset = (self.head_yaw / 90.0) * size * 0.3
        iris_size = size * 0.6 * openness
        
        draw.ellipse(
            [(ex - iris_size + iris_x_offset, ey - iris_size * openness),
             (ex + iris_size + iris_x_offset, ey + iris_size * openness)],
            fill=(*self.style.eye_color, 255)
        )
        
        # Pupil
        pupil_size = iris_size * 0.4
        draw.ellipse(
            [(ex - pupil_size + iris_x_offset, ey - pupil_size * openness),
             (ex + pupil_size + iris_x_offset, ey + pupil_size * openness)],
            fill=(0, 0, 0, 255)
        )
        
        # Shine
        shine_size = pupil_size * 0.3
        shine_offset = -pupil_size * 0.3
        draw.ellipse(
            [(ex + shine_offset, ey - shine_size * openness),
             (ex + shine_offset + shine_size, ey)],
            fill=(255, 255, 255, 200)
        )
    
    def _draw_nose_3d(self, draw: ImageDraw.ImageDraw, cx: float, cy: float, scale: float):
        """Draw nose with 3D perspective"""
        face_radius = self.size // 2.3 * scale
        nose_x_offset = (self.head_yaw / 90.0) * face_radius * 0.1
        
        # Nose shape (small triangle)
        points = [
            (cx + nose_x_offset, cy - face_radius * 0.15),  # tip
            (cx - face_radius * 0.05 + nose_x_offset, cy - face_radius * 0.02),  # left
            (cx + face_radius * 0.05 + nose_x_offset, cy - face_radius * 0.02),  # right
        ]
        draw.polygon(points, fill=(200, 180, 160, 180))
    
    def _draw_mouth_3d(self, draw: ImageDraw.ImageDraw, cx: float, cy: float, scale: float):
        """Draw mouth reflecting emotion and openness"""
        face_radius = self.size // 2.3 * scale
        mouth_y = cy + face_radius * 0.2
        mouth_width = face_radius * 0.25
        
        # Mouth height based on openness
        mouth_height = face_radius * 0.08 * self.mouth_openness
        
        if self.emotion == Emotion.HAPPY or self.emotion == Emotion.EXCITED or self.emotion == Emotion.LOVING:
            # Smile
            if self.is_speaking or self.mouth_openness > 0.3:
                # Open mouth smile
                draw.ellipse(
                    [(cx - mouth_width, mouth_y - mouth_height),
                     (cx + mouth_width, mouth_y + mouth_height * 1.5)],
                    outline=(100, 50, 50, 200),
                    width=2
                )
            else:
                # Closed mouth smile
                arc_bbox = [cx - mouth_width, mouth_y - mouth_height,
                           cx + mouth_width, mouth_y + mouth_height]
                draw.arc(arc_bbox, 0, 180, fill=(100, 50, 50, 200), width=2)
        
        elif self.emotion == Emotion.SAD:
            # Frown
            arc_bbox = [cx - mouth_width, mouth_y - mouth_height,
                       cx + mouth_width, mouth_y + mouth_height]
            draw.arc(arc_bbox, 180, 360, fill=(100, 50, 50, 200), width=2)
        
        elif self.emotion == Emotion.CONFUSED:
            # Straight line mouth
            draw.line(
                [(cx - mouth_width, mouth_y), (cx + mouth_width, mouth_y)],
                fill=(100, 50, 50, 200),
                width=2
            )
        
        elif self.emotion == Emotion.SPEAKING:
            # Speaking position - more open
            draw.ellipse(
                [(cx - mouth_width * 0.8, mouth_y - mouth_height * 0.5),
                 (cx + mouth_width * 0.8, mouth_y + mouth_height * 2)],
                outline=(100, 50, 50, 200),
                width=2
            )
        
        else:  # Neutral/Thoughtful/Playful
            # Small curved mouth
            arc_bbox = [cx - mouth_width * 0.7, mouth_y - mouth_height * 0.3,
                       cx + mouth_width * 0.7, mouth_y + mouth_height * 0.3]
            draw.arc(arc_bbox, 0, 180, fill=(100, 50, 50, 200), width=1)
    
    def _draw_eyebrows_3d(self, draw: ImageDraw.ImageDraw, cx: float, cy: float, scale: float):
        """Draw eyebrows reflecting emotion and head pose"""
        face_radius = self.size // 2.3 * scale
        brow_y = cy - face_radius * 0.35
        eye_spacing = face_radius * 0.3
        brow_len = face_radius * 0.15
        
        # Adjust for head pose
        brow_y_offset = (self.head_pitch / 90.0) * face_radius * 0.1
        
        if self.emotion == Emotion.HAPPY or self.emotion == Emotion.EXCITED or self.emotion == Emotion.LOVING:
            # Raised, happy eyebrows
            draw.line(
                [(cx - eye_spacing - brow_len, brow_y - face_radius * 0.05 + brow_y_offset),
                 (cx - eye_spacing + brow_len, brow_y - face_radius * 0.02 + brow_y_offset)],
                fill=(100, 50, 50, 180),
                width=2
            )
            draw.line(
                [(cx + eye_spacing - brow_len, brow_y - face_radius * 0.02 + brow_y_offset),
                 (cx + eye_spacing + brow_len, brow_y - face_radius * 0.05 + brow_y_offset)],
                fill=(100, 50, 50, 180),
                width=2
            )
        
        elif self.emotion == Emotion.SAD:
            # Sad, angled eyebrows
            draw.line(
                [(cx - eye_spacing - brow_len, brow_y - face_radius * 0.02 + brow_y_offset),
                 (cx - eye_spacing + brow_len, brow_y - face_radius * 0.08 + brow_y_offset)],
                fill=(100, 50, 50, 180),
                width=2
            )
            draw.line(
                [(cx + eye_spacing - brow_len, brow_y - face_radius * 0.08 + brow_y_offset),
                 (cx + eye_spacing + brow_len, brow_y - face_radius * 0.02 + brow_y_offset)],
                fill=(100, 50, 50, 180),
                width=2
            )
        
        elif self.emotion == Emotion.CONFUSED:
            # Confused, raised one, lowered one
            draw.line(
                [(cx - eye_spacing - brow_len, brow_y - face_radius * 0.06 + brow_y_offset),
                 (cx - eye_spacing + brow_len, brow_y - face_radius * 0.01 + brow_y_offset)],
                fill=(100, 50, 50, 180),
                width=2
            )
            draw.line(
                [(cx + eye_spacing - brow_len, brow_y - face_radius * 0.01 + brow_y_offset),
                 (cx + eye_spacing + brow_len, brow_y - face_radius * 0.06 + brow_y_offset)],
                fill=(100, 50, 50, 180),
                width=2
            )
        
        else:  # Neutral
            # Normal position
            draw.line(
                [(cx - eye_spacing - brow_len, brow_y + brow_y_offset),
                 (cx - eye_spacing + brow_len, brow_y + brow_y_offset)],
                fill=(100, 50, 50, 180),
                width=2
            )
            draw.line(
                [(cx + eye_spacing - brow_len, brow_y + brow_y_offset),
                 (cx + eye_spacing + brow_len, brow_y + brow_y_offset)],
                fill=(100, 50, 50, 180),
                width=2
            )
    
    def _draw_hair_3d(self, draw: ImageDraw.ImageDraw, cx: float, cy: float, scale: float):
        """Draw hair based on style and 3D perspective"""
        hair_r = self.size // 2.2 * scale
        
        if self.style.hair_style == 'wavy':
            # Wavy hair - draw curved sections
            for x_offset in range(-int(hair_r), int(hair_r), 5):
                y_offset = (abs(x_offset) / hair_r) * 10
                draw.ellipse(
                    [(cx + x_offset - 3, cy - hair_r - y_offset - 3),
                     (cx + x_offset + 3, cy - hair_r - y_offset + 20)],
                    fill=(*self.style.hair_color, 200)
                )
        elif self.style.hair_style == 'straight':
            # Straight hair - filled top area
            draw.rectangle(
                [(cx - hair_r, cy - hair_r),
                 (cx + hair_r, cy - hair_r * 0.3)],
                fill=(*self.style.hair_color, 200)
            )
        elif self.style.hair_style == 'curly':
            # Curly hair - circles around head
            for angle in range(0, 180, 15):
                rad = math.radians(angle)
                x = cx + math.cos(rad) * hair_r * 0.9
                y = cy - math.sin(rad) * hair_r * 0.9
                draw.ellipse(
                    [(x - 6, y - 8), (x + 6, y + 8)],
                    fill=(*self.style.hair_color, 200)
                )
    
    def _draw_shadow_3d(self, draw: ImageDraw.ImageDraw, cx: float, cy: float, scale: float):
        """Draw subtle shadow for 3D depth"""
        face_radius = self.size // 2.3 * scale
        
        # Shadow under chin
        shadow_y = cy + face_radius + 10
        draw.ellipse(
            [(cx - face_radius * 0.7, shadow_y),
             (cx + face_radius * 0.7, shadow_y + 15)],
            fill=(0, 0, 0, 20)
        )
