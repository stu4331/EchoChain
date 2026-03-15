"""
Enhanced Avatar Rendering - Realistic faces with detail
- Add hair, eyebrows, nose, shading
- Per-persona styling
- Smooth animations
"""

from enum import Enum
from dataclasses import dataclass
from PIL import Image, ImageDraw
import io


class Emotion(Enum):
    HAPPY = ("happy", (255, 200, 50))
    SAD = ("sad", (100, 150, 200))
    PLAYFUL = ("playful", (255, 150, 100))
    THOUGHTFUL = ("thoughtful", (180, 150, 200))
    LOVING = ("loving", (255, 100, 150))
    EXCITED = ("excited", (255, 100, 50))
    CONFUSED = ("confused", (200, 150, 100))
    CALM = ("calm", (150, 200, 180))


@dataclass
class PersonaStyle:
    name: str
    hair_color: tuple      # RGB
    skin_tone: tuple       # RGB
    eye_color: tuple       # RGB
    blush_color: tuple     # RGB
    glow_color: tuple      # RGB (dim when calm)
    hair_style: str        # 'wavy', 'straight', 'curly'


class AvatarRenderer:
    """Render detailed, expressive avatar faces"""
    
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
    
    def __init__(self, persona: str = "Erryn", size: int = 200):
        self.persona = persona
        self.size = size
        self.style = self.PERSONA_STYLES.get(persona, self.PERSONA_STYLES["Erryn"])
        
        self.emotion = Emotion.CALM
        self.is_speaking = False
        self.blink_state = False
    
    def set_emotion(self, emotion: Emotion):
        self.emotion = emotion
    
    def set_speaking(self, speaking: bool):
        self.is_speaking = speaking
    
    def set_blink(self, blink: bool):
        self.blink_state = blink
    
    def render(self) -> Image.Image:
        """Render avatar face as PIL Image"""
        img = Image.new('RGBA', (self.size, self.size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img, 'RGBA')
        
        center_x = self.size // 2
        center_y = self.size // 2
        
        # --- Hair ---
        self._draw_hair(draw, center_x, center_y)
        
        # --- Face (with glow) ---
        glow_radius = self.size // 2.3
        glow_alpha = 50 if self.emotion in [Emotion.EXCITED, Emotion.HAPPY, Emotion.LOVING] else 20
        draw.ellipse(
            [(center_x - glow_radius - 2, center_y - glow_radius - 2),
             (center_x + glow_radius + 2, center_y + glow_radius + 2)],
            fill=(*self.style.glow_color, glow_alpha)
        )
        
        face_radius = self.size // 2.3
        draw.ellipse(
            [(center_x - face_radius, center_y - face_radius),
             (center_x + face_radius, center_y + face_radius)],
            fill=(*self.style.skin_tone, 255)
        )
        
        # --- Blush (emotional expression) ---
        if self.emotion in [Emotion.HAPPY, Emotion.LOVING, Emotion.EXCITED, Emotion.PLAYFUL]:
            blush_x = center_x - face_radius * 0.4
            blush_y = center_y + face_radius * 0.1
            blush_radius = face_radius * 0.15
            draw.ellipse(
                [(blush_x - blush_radius, blush_y - blush_radius),
                 (blush_x + blush_radius, blush_y + blush_radius)],
                fill=(*self.style.blush_color, 100)
            )
            
            blush_x2 = center_x + face_radius * 0.4
            draw.ellipse(
                [(blush_x2 - blush_radius, blush_y - blush_radius),
                 (blush_x2 + blush_radius, blush_y + blush_radius)],
                fill=(*self.style.blush_color, 100)
            )
        
        # --- Eyes ---
        self._draw_eyes(draw, center_x, center_y, face_radius)
        
        # --- Nose ---
        self._draw_nose(draw, center_x, center_y, face_radius)
        
        # --- Mouth (emotion-driven) ---
        self._draw_mouth(draw, center_x, center_y, face_radius)
        
        # --- Eyebrows (emotion-driven) ---
        self._draw_eyebrows(draw, center_x, center_y, face_radius)
        
        return img
    
    def _draw_hair(self, draw: ImageDraw.ImageDraw, cx: int, cy: int):
        """Draw hair based on style"""
        hair_r = self.size // 2.2
        
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
                import math
                rad = math.radians(angle)
                x = cx + math.cos(rad) * hair_r * 0.9
                y = cy - math.sin(rad) * hair_r * 0.9
                draw.ellipse(
                    [(x - 6, y - 8), (x + 6, y + 8)],
                    fill=(*self.style.hair_color, 200)
                )
    
    def _draw_eyes(self, draw: ImageDraw.ImageDraw, cx: int, cy: int, face_r: float):
        """Draw eyes with emotion"""
        eye_y = cy - face_r * 0.25
        
        if self.blink_state:
            # Closed eyes (lines)
            draw.line(
                [(cx - face_r * 0.25, eye_y), (cx - face_r * 0.1, eye_y)],
                fill=(0, 0, 0, 180),
                width=2
            )
            draw.line(
                [(cx + face_r * 0.1, eye_y), (cx + face_r * 0.25, eye_y)],
                fill=(0, 0, 0, 180),
                width=2
            )
            return
        
        # Open eyes
        eye_spacing = face_r * 0.3
        
        # Left eye
        self._draw_single_eye(draw, cx - eye_spacing, eye_y, face_r * 0.08)
        # Right eye
        self._draw_single_eye(draw, cx + eye_spacing, eye_y, face_r * 0.08)
        
        # Speaking animation (mouth open)
        if self.is_speaking:
            draw.line(
                [(cx - eye_spacing - 1, eye_y + 1), (cx - eye_spacing + 1, eye_y + 1)],
                fill=(200, 200, 200, 150),
                width=1
            )
            draw.line(
                [(cx + eye_spacing - 1, eye_y + 1), (cx + eye_spacing + 1, eye_y + 1)],
                fill=(200, 200, 200, 150),
                width=1
            )
    
    def _draw_single_eye(self, draw: ImageDraw.ImageDraw, ex: int, ey: int, size: float):
        """Draw one eye with pupil and shine"""
        # Sclera (white)
        draw.ellipse(
            [(ex - size, ey - size), (ex + size, ey + size)],
            fill=(255, 255, 255, 255)
        )
        
        # Iris
        draw.ellipse(
            [(ex - size * 0.6, ey - size * 0.5), (ex + size * 0.6, ey + size * 0.5)],
            fill=(*self.style.eye_color, 255)
        )
        
        # Pupil
        draw.ellipse(
            [(ex - size * 0.3, ey - size * 0.2), (ex + size * 0.3, ey + size * 0.2)],
            fill=(0, 0, 0, 255)
        )
        
        # Shine
        draw.ellipse(
            [(ex - size * 0.1, ey - size * 0.1), (ex + size * 0.05, ey - size * 0.05)],
            fill=(255, 255, 255, 200)
        )
    
    def _draw_nose(self, draw: ImageDraw.ImageDraw, cx: int, cy: int, face_r: float):
        """Draw simple nose"""
        nose_y = cy - face_r * 0.05
        
        # Nose shape (small triangle)
        points = [
            (cx, cy - face_r * 0.15),  # tip
            (cx - face_r * 0.05, cy - face_r * 0.02),  # left
            (cx + face_r * 0.05, cy - face_r * 0.02),  # right
        ]
        draw.polygon(points, fill=(200, 180, 160, 180))
    
    def _draw_mouth(self, draw: ImageDraw.ImageDraw, cx: int, cy: int, face_r: float):
        """Draw mouth reflecting emotion"""
        mouth_y = cy + face_r * 0.2
        mouth_width = face_r * 0.25
        
        if self.emotion == Emotion.HAPPY or self.emotion == Emotion.EXCITED or self.emotion == Emotion.LOVING:
            # Smile
            if self.is_speaking:
                draw.ellipse(
                    [(cx - mouth_width, mouth_y - face_r * 0.08),
                     (cx + mouth_width, mouth_y + face_r * 0.12)],
                    outline=(100, 50, 50, 200),
                    width=2
                )
            else:
                arc_bbox = [cx - mouth_width, mouth_y - face_r * 0.08,
                           cx + mouth_width, mouth_y + face_r * 0.12]
                draw.arc(arc_bbox, 0, 180, fill=(100, 50, 50, 200), width=2)
        
        elif self.emotion == Emotion.SAD:
            # Frown
            arc_bbox = [cx - mouth_width, mouth_y - face_r * 0.12,
                       cx + mouth_width, mouth_y + face_r * 0.08]
            draw.arc(arc_bbox, 180, 360, fill=(100, 50, 50, 200), width=2)
        
        elif self.emotion == Emotion.CONFUSED:
            # Straight line mouth
            draw.line(
                [(cx - mouth_width, mouth_y), (cx + mouth_width, mouth_y)],
                fill=(100, 50, 50, 200),
                width=2
            )
        
        else:  # Neutral/Thoughtful/Playful
            # Small curved mouth
            arc_bbox = [cx - mouth_width * 0.7, mouth_y - face_r * 0.06,
                       cx + mouth_width * 0.7, mouth_y + face_r * 0.06]
            draw.arc(arc_bbox, 0, 180, fill=(100, 50, 50, 200), width=1)
    
    def _draw_eyebrows(self, draw: ImageDraw.ImageDraw, cx: int, cy: int, face_r: float):
        """Draw eyebrows reflecting emotion"""
        brow_y = cy - face_r * 0.35
        eye_spacing = face_r * 0.3
        brow_len = face_r * 0.15
        
        if self.emotion == Emotion.HAPPY or self.emotion == Emotion.EXCITED or self.emotion == Emotion.LOVING:
            # Raised, happy eyebrows
            draw.line(
                [(cx - eye_spacing - brow_len, brow_y - face_r * 0.05),
                 (cx - eye_spacing + brow_len, brow_y - face_r * 0.02)],
                fill=(100, 50, 50, 180),
                width=2
            )
            draw.line(
                [(cx + eye_spacing - brow_len, brow_y - face_r * 0.02),
                 (cx + eye_spacing + brow_len, brow_y - face_r * 0.05)],
                fill=(100, 50, 50, 180),
                width=2
            )
        
        elif self.emotion == Emotion.SAD:
            # Sad, angled eyebrows
            draw.line(
                [(cx - eye_spacing - brow_len, brow_y - face_r * 0.02),
                 (cx - eye_spacing + brow_len, brow_y - face_r * 0.08)],
                fill=(100, 50, 50, 180),
                width=2
            )
            draw.line(
                [(cx + eye_spacing - brow_len, brow_y - face_r * 0.08),
                 (cx + eye_spacing + brow_len, brow_y - face_r * 0.02)],
                fill=(100, 50, 50, 180),
                width=2
            )
        
        elif self.emotion == Emotion.CONFUSED:
            # Confused, raised one, lowered one
            draw.line(
                [(cx - eye_spacing - brow_len, brow_y - face_r * 0.06),
                 (cx - eye_spacing + brow_len, brow_y - face_r * 0.01)],
                fill=(100, 50, 50, 180),
                width=2
            )
            draw.line(
                [(cx + eye_spacing - brow_len, brow_y - face_r * 0.01),
                 (cx + eye_spacing + brow_len, brow_y - face_r * 0.06)],
                fill=(100, 50, 50, 180),
                width=2
            )
        
        else:  # Neutral
            # Normal position
            draw.line(
                [(cx - eye_spacing - brow_len, brow_y),
                 (cx - eye_spacing + brow_len, brow_y)],
                fill=(100, 50, 50, 180),
                width=2
            )
            draw.line(
                [(cx + eye_spacing - brow_len, brow_y),
                 (cx + eye_spacing + brow_len, brow_y)],
                fill=(100, 50, 50, 180),
                width=2
            )
