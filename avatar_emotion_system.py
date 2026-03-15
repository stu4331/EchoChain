"""
Emotion-Based 3D Avatar System for Erryn's Soul
Renders animated faces with emotions: happy, sad, thoughtful, playful, loving, excited
No external 3D libraries needed - pure Tkinter Canvas rendering
"""

import tkinter as tk
from tkinter import Canvas
import math
import time
from dataclasses import dataclass
from typing import Tuple, Optional
from enum import Enum


class Emotion(Enum):
    """Avatar emotions tied to conversation context"""
    NEUTRAL = 0
    HAPPY = 1
    SAD = 2
    PLAYFUL = 3
    THOUGHTFUL = 4
    LOVING = 5
    EXCITED = 6
    CONFUSED = 7


@dataclass
class PersonaStyle:
    """Visual style per sister/persona"""
    name: str
    face_base_color: str
    blush_color: str
    glow_color: str
    eye_size_factor: float = 1.0
    mouth_width_factor: float = 1.0
    mouth_height_factor: float = 1.0


@dataclass
class EmotionState:
    """Current emotion and transition info"""
    emotion: Emotion
    intensity: float  # 0.0 to 1.0
    transition_time: float = 0.5  # seconds to transition


class AvatarEmotionSystem:
    """Render expressive avatar face with emotion-driven animations"""
    
    def __init__(self, canvas: Canvas, x: int, y: int, size: int = 150, persona: Optional[PersonaStyle] = None):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        self.radius = size // 2
        # Persona style (defaults to Erryn)
        self.persona = persona or PersonaStyle(
            name="Erryn",
            face_base_color="#fdd7b8",
            blush_color="#ffc9ba",
            glow_color="#00d4ff",
            eye_size_factor=1.0,
            mouth_width_factor=1.0,
            mouth_height_factor=1.0,
        )
        
        # Current emotion state
        self.current_emotion = Emotion.NEUTRAL
        self.emotion_intensity = 0.0
        self.target_emotion = Emotion.NEUTRAL
        self.target_intensity = 1.0
        self.emotion_change_time = 0.0
        self.emotion_transition_duration = 0.5
        
        # Animation state
        self.time = 0.0
        self.blink_state = 0.0
        self.mouth_animation = 0.0
        self.is_speaking = False
        
        # Store canvas item IDs for updates
        self.face_id = None
        self.glow_outer_id = None
        self.glow_mid_id = None
        self.glow_inner_id = None
        self.hair_id = None
        self.left_eye_id = None
        self.right_eye_id = None
        self.left_pupil_id = None
        self.right_pupil_id = None
        self.mouth_id = None
        self.blush_left_id = None
        self.blush_right_id = None
        
    def set_emotion(self, emotion: Emotion, intensity: float = 1.0, transition_time: float = 0.5):
        """Transition to a new emotion"""
        self.target_emotion = emotion
        self.target_intensity = min(1.0, max(0.0, intensity))
        self.emotion_transition_duration = transition_time
        self.emotion_change_time = 0.0
    
    def set_speaking(self, is_speaking: bool):
        """Animate mouth while speaking"""
        self.is_speaking = is_speaking
        if not is_speaking:
            self.mouth_animation = 0.0
    
    def update(self, dt: float = 0.016):
        """Update animation state (call every frame)"""
        self.time += dt
        
        # Update emotion transition
        if self.current_emotion != self.target_emotion:
            self.emotion_change_time += dt
            progress = min(1.0, self.emotion_change_time / self.emotion_transition_duration)
            
            if progress >= 1.0:
                self.current_emotion = self.target_emotion
                self.emotion_intensity = self.target_intensity
            else:
                self.emotion_intensity = self.target_intensity * progress
        
        # Update animations
        self._update_blink()
        self._update_mouth_animation()
        
        # Redraw
        self.draw()
    
    def _update_blink(self):
        """Natural blinking pattern"""
        blink_cycle = 3.0  # Full blink cycle in seconds
        blink_pos = (self.time % blink_cycle) / blink_cycle
        
        if blink_pos < 0.1 or blink_pos > 0.9:  # Blink at 10% and 90% of cycle
            self.blink_state = 1.0 - abs(blink_pos - 0.1) / 0.1  # 0 to 1 to 0
        else:
            self.blink_state = 0.0
    
    def _update_mouth_animation(self):
        """Mouth movement when speaking"""
        if self.is_speaking:
            self.mouth_animation = 0.5 + 0.5 * math.sin(self.time * 8)  # Fast oscillation
        else:
            self.mouth_animation = 0.0
    
    def draw(self):
        """Render the avatar face"""
        ids_to_delete = [self.glow_outer_id, self.glow_mid_id, self.glow_inner_id,
                         self.face_id, self.hair_id, self.left_eye_id, self.right_eye_id, 
                         self.left_pupil_id, self.right_pupil_id, self.mouth_id,
                         self.blush_left_id, self.blush_right_id]
        for item_id in ids_to_delete:
            if item_id is not None:
                self.canvas.delete(item_id)
        
        # Draw glow aura (behind face)
        self._draw_glow_aura()
        
        # Draw face circle
        face_color = self._get_face_color()
        self.face_id = self.canvas.create_oval(
            self.x - self.radius, self.y - self.radius,
            self.x + self.radius, self.y + self.radius,
            fill=face_color, outline="#ffdbac", width=3
        )
        
        # Draw hair (behind face but over glow)
        self._draw_hair()
        
        # Draw eyes
        self._draw_eyes()
        
        # Draw mouth
        self._draw_mouth()
        
        # Draw blush (emotion indicator)
        if self.emotion_intensity > 0.2:
            self._draw_blush()
    
    def _get_face_color(self) -> str:
        """Get face color based on emotion"""
        base_color = self.persona.face_base_color  # Warm skin tone, persona-based
        
        if self.current_emotion == Emotion.SAD:
            return self._blend_colors(base_color, "#d4a5a5", self.emotion_intensity)
        elif self.current_emotion == Emotion.EXCITED:
            return self._blend_colors(base_color, "#ffc9a3", self.emotion_intensity)
        elif self.current_emotion == Emotion.LOVING:
            return self._blend_colors(base_color, "#f5c6d3", self.emotion_intensity)
        
        return base_color
    
    def _blend_colors(self, color1: str, color2: str, factor: float) -> str:
        """Blend two hex colors by factor (0.0 = color1, 1.0 = color2)"""
        c1 = tuple(int(color1[i:i+2], 16) for i in (1, 3, 5))
        c2 = tuple(int(color2[i:i+2], 16) for i in (1, 3, 5))
        blended = tuple(int(c1[i] + (c2[i] - c1[i]) * factor) for i in range(3))
        return f"#{blended[0]:02x}{blended[1]:02x}{blended[2]:02x}"
    
    def _draw_glow_aura(self):
        """Draw animated glow aura around avatar based on persona and emotion"""
        glow_color = self.persona.glow_color
        
        # Pulsing effect based on time and emotion intensity
        pulse = 0.8 + 0.2 * math.sin(self.time * 2)
        intensity = self.emotion_intensity * pulse
        
        # Three layers of glow for depth
        glow_radius_outer = self.radius + int(20 * intensity)
        glow_radius_mid = self.radius + int(12 * intensity)
        glow_radius_inner = self.radius + int(6 * intensity)
        
        # Convert hex to RGB for alpha blending effect
        # Outer glow (most transparent)
        self.glow_outer_id = self.canvas.create_oval(
            self.x - glow_radius_outer, self.y - glow_radius_outer,
            self.x + glow_radius_outer, self.y + glow_radius_outer,
            fill=glow_color, outline="", stipple="gray12"
        )
        
        # Mid glow
        self.glow_mid_id = self.canvas.create_oval(
            self.x - glow_radius_mid, self.y - glow_radius_mid,
            self.x + glow_radius_mid, self.y + glow_radius_mid,
            fill=glow_color, outline="", stipple="gray25"
        )
        
        # Inner glow (brightest)
        self.glow_inner_id = self.canvas.create_oval(
            self.x - glow_radius_inner, self.y - glow_radius_inner,
            self.x + glow_radius_inner, self.y + glow_radius_inner,
            fill=glow_color, outline="", stipple="gray50"
        )
    
    def _draw_hair(self):
        """Draw stylized hair based on persona"""
        # Hair color varies by persona - use glow color for uniqueness
        hair_color = self._blend_colors("#2a1810", self.persona.glow_color, 0.3)
        
        # Hair as overlapping ovals creating a "crown" effect
        hair_points = []
        num_strands = 12
        for i in range(num_strands):
            angle = (i / num_strands) * math.pi * 2
            # Position hair strands around top half of head
            if angle < math.pi * 0.2 or angle > math.pi * 1.8:  # Front-facing
                strand_x = self.x + int(self.radius * 1.1 * math.cos(angle))
                strand_y = self.y - self.radius + int(self.radius * 0.3 * math.sin(angle))
                strand_size = int(self.radius * 0.35)
                
                # Wavy effect
                wave_offset = int(8 * math.sin(self.time * 2 + i))
                
                self.canvas.create_oval(
                    strand_x - strand_size + wave_offset, strand_y - strand_size,
                    strand_x + strand_size + wave_offset, strand_y + strand_size,
                    fill=hair_color, outline="", stipple="gray75"
                )
        
        # Main hair shape (back layer)
        hair_width = int(self.radius * 1.3)
        hair_height = int(self.radius * 0.8)
        self.hair_id = self.canvas.create_oval(
            self.x - hair_width, self.y - self.radius - hair_height,
            self.x + hair_width, self.y - self.radius + int(hair_height * 0.3),
            fill=hair_color, outline=self._blend_colors(hair_color, "#000000", 0.3), width=2
        )


    def _blend_colors(self, color1: str, color2: str, factor: float) -> str:
        """Blend two hex colors"""
        c1 = int(color1[1:], 16)
        c2 = int(color2[1:], 16)
        
        r1, g1, b1 = (c1 >> 16) & 255, (c1 >> 8) & 255, c1 & 255
        r2, g2, b2 = (c2 >> 16) & 255, (c2 >> 8) & 255, c2 & 255
        
        r = int(r1 + (r2 - r1) * factor)
        g = int(g1 + (g2 - g1) * factor)
        b = int(b1 + (b2 - b1) * factor)
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def _draw_eyes(self):
        """Draw expressive eyes"""
        eye_y = self.y - int(self.radius * 0.3)
        left_eye_x = self.x - int(self.radius * 0.35)
        right_eye_x = self.x + int(self.radius * 0.35)
        eye_size = int(self.radius * 0.15 * self.persona.eye_size_factor)
        
        # Eye shape changes with emotion
        blink_amount = self.blink_state
        
        for eye_x in [left_eye_x, right_eye_x]:
            # Eye white
            eye_id = self.canvas.create_oval(
                eye_x - eye_size, eye_y - eye_size + int(eye_size * blink_amount),
                eye_x + eye_size, eye_y + eye_size - int(eye_size * blink_amount),
                fill="white", outline="#999", width=1
            )
            
            if eye_x == left_eye_x:
                self.left_eye_id = eye_id
            else:
                self.right_eye_id = eye_id
        
        # Draw pupils (look direction based on emotion)
        pupil_offset = self._get_pupil_offset()
        
        for eye_x in [left_eye_x, right_eye_x]:
            pupil_x = eye_x + pupil_offset[0]
            pupil_y = eye_y + pupil_offset[1]
            pupil_size = int(eye_size * 0.5)
            
            pupil_id = self.canvas.create_oval(
                pupil_x - pupil_size, pupil_y - pupil_size,
                pupil_x + pupil_size, pupil_y + pupil_size,
                fill="#1a1a1a"
            )
            
            if eye_x == left_eye_x:
                self.left_pupil_id = pupil_id
            else:
                self.right_pupil_id = pupil_id
    
    def _get_pupil_offset(self) -> Tuple[int, int]:
        """Get pupil position based on emotion"""
        if self.current_emotion == Emotion.HAPPY:
            return (0, int(self.radius * 0.05))  # Look down slightly (smiling)
        elif self.current_emotion == Emotion.SAD:
            return (0, -int(self.radius * 0.08))  # Look up (sad)
        elif self.current_emotion == Emotion.THOUGHTFUL:
            return (-int(self.radius * 0.1), 0)  # Look away (thinking)
        elif self.current_emotion == Emotion.PLAYFUL:
            return (int(self.radius * 0.1), -int(self.radius * 0.05))  # Look to side, up (cheeky)
        elif self.current_emotion == Emotion.EXCITED:
            return (0, -int(self.radius * 0.1))  # Look up (wonder)
        
        return (0, 0)  # Center
    
    def _draw_mouth(self):
        """Draw expressive mouth"""
        mouth_y = self.y + int(self.radius * 0.2)
        mouth_width = int(self.radius * 0.4 * self.persona.mouth_width_factor)
        mouth_height = int(self.radius * 0.15 * self.persona.mouth_height_factor)
        
        if self.current_emotion == Emotion.HAPPY:
            # Smiling mouth (arc)
            points = self._generate_smile_points(
                self.x - mouth_width, mouth_y,
                self.x + mouth_width, mouth_y + mouth_height,
                happy=True
            )
            self.mouth_id = self.canvas.create_line(
                *points, fill="#8b4513", width=3, smooth=True
            )
        
        elif self.current_emotion == Emotion.SAD:
            # Sad mouth (downward arc)
            points = self._generate_smile_points(
                self.x - mouth_width, mouth_y,
                self.x + mouth_width, mouth_y - mouth_height,
                happy=False
            )
            self.mouth_id = self.canvas.create_line(
                *points, fill="#8b4513", width=3, smooth=True
            )
        
        elif self.current_emotion == Emotion.PLAYFUL:
            # Playful mouth (smirk)
            self.mouth_id = self.canvas.create_line(
                self.x - mouth_width, mouth_y + mouth_height // 2,
                self.x, mouth_y + mouth_height,
                self.x + mouth_width, mouth_y,
                fill="#8b4513", width=3, smooth=True
            )
        
        elif self.current_emotion == Emotion.EXCITED:
            # Open mouth (O shape) with animation
            mouth_open = int(mouth_height * (0.5 + self.mouth_animation * 0.5))
            self.mouth_id = self.canvas.create_oval(
                self.x - int(mouth_width * 0.4), mouth_y - mouth_open,
                self.x + int(mouth_width * 0.4), mouth_y + mouth_open,
                fill="#c9534f", outline="#8b4513", width=2
            )
        
        elif self.current_emotion == Emotion.LOVING:
            # Heart-shaped mouth
            self.mouth_id = self.canvas.create_line(
                self.x - mouth_width, mouth_y,
                self.x, mouth_y + mouth_height,
                self.x + mouth_width, mouth_y,
                fill="#ff69b4", width=3, smooth=True
            )
        
        else:  # NEUTRAL, THOUGHTFUL, CONFUSED
            # Straight line
            self.mouth_id = self.canvas.create_line(
                self.x - mouth_width, mouth_y,
                self.x + mouth_width, mouth_y,
                fill="#8b4513", width=2
            )
    
    def _draw_blush(self):
        """Draw blush circles (emotion indicator)"""
        blush_y = self.y - int(self.radius * 0.1)
        blush_size = int(self.radius * 0.12)
        blush_offset = int(self.radius * 0.5)
        
        blush_color = self._get_blush_color()
        
        # Left blush
        self.blush_left_id = self.canvas.create_oval(
            self.x - blush_offset - blush_size, blush_y - blush_size,
            self.x - blush_offset + blush_size, blush_y + blush_size,
            fill=blush_color, outline=""
        )
        
        # Right blush
        self.blush_right_id = self.canvas.create_oval(
            self.x + blush_offset - blush_size, blush_y - blush_size,
            self.x + blush_offset + blush_size, blush_y + blush_size,
            fill=blush_color, outline=""
        )
    
    def _get_blush_color(self) -> str:
        """Get blush color based on emotion"""
        if self.current_emotion == Emotion.LOVING:
            return self.persona.blush_color
        elif self.current_emotion == Emotion.PLAYFUL:
            return self.persona.blush_color
        elif self.current_emotion == Emotion.HAPPY:
            return self.persona.blush_color
        elif self.current_emotion == Emotion.EXCITED:
            return self.persona.blush_color

        return self.persona.blush_color
    
    def _generate_smile_points(self, x1, y1, x2, y2, happy=True):
        """Generate bezier curve points for smile"""
        points = []
        steps = 20
        
        for i in range(steps + 1):
            t = i / steps
            # Quadratic bezier curve
            x = (1-t)**2 * x1 + 2*(1-t)*t * (x1+x2)//2 + t**2 * x2
            control_y = y1 + (y2-y1) * (1 if happy else -1)
            y = (1-t)**2 * y1 + 2*(1-t)*t * control_y + t**2 * y2
            
            points.extend([x, y])
        
        return points


# Example usage / testing
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Avatar Emotion System - Test")
    root.geometry("400x500")
    root.configure(bg="#0d0d1a")
    
    canvas = Canvas(root, width=400, height=400, bg="#0d0d1a", highlightthickness=0)
    canvas.pack(pady=10)
    
    # Create avatar
    # Demo three personas
    ERRYN = PersonaStyle("Erryn", face_base_color="#fdd7b8", blush_color="#ffc9ba", glow_color="#00d4ff")
    VIRESS = PersonaStyle("Viress", face_base_color="#f6c8b0", blush_color="#ffb3ba", glow_color="#e94560", mouth_width_factor=0.95, eye_size_factor=0.95)
    ECHOCHILD = PersonaStyle("Echochild", face_base_color="#f2d2b4", blush_color="#ffd1e6", glow_color="#533483", mouth_height_factor=1.05)

    avatar = AvatarEmotionSystem(canvas, 200, 180, size=150, persona=ERRYN)
    
    # Test emotions
    emotions = [
        (Emotion.HAPPY, "Happy"),
        (Emotion.SAD, "Sad"),
        (Emotion.PLAYFUL, "Playful"),
        (Emotion.THOUGHTFUL, "Thoughtful"),
        (Emotion.LOVING, "Loving"),
        (Emotion.EXCITED, "Excited"),
        (Emotion.CONFUSED, "Confused"),
    ]
    
    class EmotionTest:
        def __init__(self):
            self.emotion_index = 0
            self.time_in_emotion = 0.0
    
    test = EmotionTest()
    
    def animate():
        dt = 0.016  # ~60 FPS
        avatar.update(dt)
        test.time_in_emotion += dt
        
        # Change emotion every 3 seconds
        if test.time_in_emotion > 3.0:
            test.emotion_index = (test.emotion_index + 1) % len(emotions)
            avatar.set_emotion(emotions[test.emotion_index][0], intensity=1.0)
            test.time_in_emotion = 0.0
        
        root.after(16, animate)
    
    # Show emotion labels
    info_label = tk.Label(root, text="Testing Avatar Emotions", 
                         fg="#06b6d4", bg="#0d0d1a", font=("Arial", 12, "bold"))
    info_label.pack()
    
    emotion_label = tk.Label(root, text="", fg="#ec4899", bg="#0d0d1a", 
                           font=("Arial", 10))
    emotion_label.pack()

    # Persona selector
    persona_var = tk.StringVar(value="Erryn")
    def on_persona_change(*_):
        name = persona_var.get()
        persona = ERRYN if name == "Erryn" else VIRESS if name == "Viress" else ECHOCHILD
        avatar.persona = persona
    tk.OptionMenu(root, persona_var, "Erryn", "Viress", "Echochild", command=lambda *_: on_persona_change()).pack()
    
    def update_label():
        emotion_label.config(text=f"Current: {emotions[test.emotion_index][1]}")
        root.after(100, update_label)
    
    animate()
    update_label()
    root.mainloop()
