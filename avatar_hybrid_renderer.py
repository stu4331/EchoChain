"""
Hybrid Avatar Renderer - Beautiful human-like faces with holographic AI effects

For the three AI sisters:
  Erryn     (Guardian 💙)   - Elegant, protective, regal
  Viress    (Technician 💛) - Sharp, intelligent, cyberpunk
  Echochild (Creative 💜)   - Youthful, curious, dreamy

Replaces the particle bubble system with:
  - Realistic human-like facial proportions
  - Sister-specific hair styles, eye colors, and personality aesthetics
  - Holographic AI effect layers (glowing auras, particle trails, digital effects)
  - Emotion-driven expression system
  - PIL-based rendering with face caching for performance
"""

import math
import time
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional, Tuple

from PIL import Image, ImageDraw, ImageFilter


# ---------------------------------------------------------------------------
# Emotion definitions
# ---------------------------------------------------------------------------

class Emotion(Enum):
    NEUTRAL    = "neutral"
    HAPPY      = "happy"
    SAD        = "sad"
    PLAYFUL    = "playful"
    THOUGHTFUL = "thoughtful"
    LOVING     = "loving"
    EXCITED    = "excited"
    CONFUSED   = "confused"
    CALM       = "calm"


# ---------------------------------------------------------------------------
# Per-sister visual identity
# ---------------------------------------------------------------------------

@dataclass
class SisterStyle:
    """Complete visual identity for one AI sister."""
    name: str

    # --- Skin / face ---
    skin_tone:    Tuple[int, int, int]   # base skin RGB
    skin_shadow:  Tuple[int, int, int]   # cheek / jaw shadow

    # --- Hair ---
    hair_color:     Tuple[int, int, int]
    hair_highlight: Tuple[int, int, int]
    hair_style: str                       # 'wavy_long' | 'short_sleek' | 'curly_medium'

    # --- Eyes ---
    eye_color:   Tuple[int, int, int]
    eye_effect:  str                      # 'digital_glow' | 'circuit_pattern' | 'starburst'

    # --- Lips / blush ---
    lip_color:   Tuple[int, int, int]
    blush_color: Tuple[int, int, int]

    # --- Holographic AI effects ---
    aura_color:     Tuple[int, int, int]  # outer glow halo
    accent_color:   Tuple[int, int, int]  # UI / trim lines
    particle_color: Tuple[int, int, int]  # trailing particles
    special_effect: str                   # 'holographic' | 'circuit' | 'aurora'


# Canonical sister styles exactly matching the problem statement
SISTER_STYLES: Dict[str, SisterStyle] = {
    "Erryn": SisterStyle(
        name="Erryn",
        skin_tone=(245, 210, 185),
        skin_shadow=(220, 175, 155),
        hair_color=(120, 80, 190),        # Purple/blue
        hair_highlight=(170, 130, 230),
        hair_style="wavy_long",
        eye_color=(60, 160, 255),         # Deep blue
        eye_effect="digital_glow",
        lip_color=(200, 110, 140),
        blush_color=(230, 155, 170),
        aura_color=(80, 180, 255),        # Cyan-blue holographic
        accent_color=(0, 220, 255),
        particle_color=(150, 100, 255),
        special_effect="holographic",
    ),
    "Viress": SisterStyle(
        name="Viress",
        skin_tone=(235, 205, 190),
        skin_shadow=(205, 170, 155),
        hair_color=(30, 60, 120),         # Dark blue
        hair_highlight=(60, 100, 180),
        hair_style="short_sleek",
        eye_color=(210, 150, 40),         # Amber/gold
        eye_effect="circuit_pattern",
        lip_color=(180, 100, 80),
        blush_color=(200, 130, 110),
        aura_color=(220, 180, 50),        # Amber tech grid
        accent_color=(255, 220, 80),
        particle_color=(100, 200, 255),
        special_effect="circuit",
    ),
    "Echochild": SisterStyle(
        name="Echochild",
        skin_tone=(250, 220, 205),
        skin_shadow=(225, 190, 175),
        hair_color=(210, 70, 130),        # Magenta/pink
        hair_highlight=(240, 130, 170),
        hair_style="curly_medium",
        eye_color=(60, 200, 120),         # Bright green
        eye_effect="starburst",
        lip_color=(220, 100, 150),
        blush_color=(240, 160, 190),
        aura_color=(200, 80, 220),        # Magenta/purple aurora
        accent_color=(255, 120, 220),
        particle_color=(180, 230, 255),
        special_effect="aurora",
    ),
}


# ---------------------------------------------------------------------------
# Render cache entry
# ---------------------------------------------------------------------------

@dataclass
class _CacheEntry:
    image: Image.Image
    timestamp: float
    emotion: str
    speaking: bool
    blink: bool


# ---------------------------------------------------------------------------
# HybridAvatarRenderer
# ---------------------------------------------------------------------------

class HybridAvatarRenderer:
    """
    Render beautiful human-like avatar faces with holographic AI effects.

    Usage::

        renderer = HybridAvatarRenderer("Erryn", size=300)
        renderer.set_emotion(Emotion.HAPPY)
        pil_image = renderer.render()          # → PIL.Image (RGBA)

    The renderer caches renders and throttles to ~3-4 frames per second so it
    is lightweight enough for daemon processes.
    """

    # Seconds between forced re-renders: 1/0.28 ≈ 3.57 fps (within 3-4 fps target)
    RENDER_INTERVAL = 0.28

    def __init__(self, persona: str = "Erryn", size: int = 300):
        self.persona     = persona
        self.size        = size
        self.style       = SISTER_STYLES.get(persona, SISTER_STYLES["Erryn"])

        self.emotion     = Emotion.NEUTRAL
        self.is_speaking = False
        self.blink_state = False

        # Phase counter drives all cyclic animations; advanced by callers or
        # auto-advanced on render() calls.
        self._phase: float = 0.0
        self._last_render_time: float = 0.0

        # Render cache: key → _CacheEntry
        self._cache: Dict[str, _CacheEntry] = {}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def set_emotion(self, emotion: Emotion) -> None:
        """Set the current emotion; clears cached render for this state."""
        if self.emotion != emotion:
            self.emotion = emotion
            self._cache.clear()

    def set_emotion_by_name(self, name: str) -> None:
        """Set emotion by string name (case-insensitive). Unknown names → NEUTRAL."""
        name = name.lower().strip()
        mapping = {e.value: e for e in Emotion}
        self.set_emotion(mapping.get(name, Emotion.NEUTRAL))

    def set_speaking(self, speaking: bool) -> None:
        self.is_speaking = speaking

    def set_blink(self, blink: bool) -> None:
        self.blink_state = blink

    def advance_phase(self, delta: float = 0.05) -> None:
        """Advance the internal animation phase (0 → 2π cycle)."""
        self._phase = (self._phase + delta) % (2 * math.pi)

    def render(self) -> Image.Image:
        """
        Return a PIL RGBA Image of the avatar.

        Results are cached; the cache is invalidated when emotion/state
        changes or after RENDER_INTERVAL seconds.
        """
        now = time.monotonic()

        # Auto-advance phase for particle/aura animations
        elapsed = now - self._last_render_time
        if elapsed > 0:
            self.advance_phase(elapsed * 1.8)

        cache_key = self._cache_key()
        entry = self._cache.get(cache_key)
        if entry and (now - entry.timestamp) < self.RENDER_INTERVAL:
            return entry.image

        img = self._render_full()
        self._cache[cache_key] = _CacheEntry(
            image=img,
            timestamp=now,
            emotion=self.emotion.value,
            speaking=self.is_speaking,
            blink=self.blink_state,
        )
        self._last_render_time = now
        return img

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _cache_key(self) -> str:
        raw = f"{self.persona}:{self.emotion.value}:{self.is_speaking}:{self.blink_state}:{self.size}"
        return str(hash(raw))

    # ------------------------------------------------------------------
    # Core render pipeline
    # ------------------------------------------------------------------

    def _render_full(self) -> Image.Image:
        img = Image.new("RGBA", (self.size, self.size), (0, 0, 0, 0))

        # Layer 0 – outer holographic aura (behind everything)
        self._draw_aura(img)

        # Layer 1 – hair (back layer)
        self._draw_hair_back(img)

        # Layer 2 – face / skin
        self._draw_face(img)

        # Layer 3 – facial detail: cheek shading, blush
        self._draw_face_detail(img)

        # Layer 4 – hair (front layer, overlaps forehead)
        self._draw_hair_front(img)

        # Layer 5 – eyes
        self._draw_eyes(img)

        # Layer 6 – eyebrows
        self._draw_eyebrows(img)

        # Layer 7 – nose
        self._draw_nose(img)

        # Layer 8 – mouth
        self._draw_mouth(img)

        # Layer 9 – special holographic effect overlay
        self._draw_special_effect(img)

        # Layer 10 – particle trails / sparkles
        self._draw_particles(img)

        return img

    # ------------------------------------------------------------------
    # Geometry helpers
    # ------------------------------------------------------------------

    def _cx(self) -> float:
        return self.size / 2

    def _cy(self) -> float:
        return self.size / 2 + self.size * 0.02  # Slightly below-center = natural

    def _r(self) -> float:
        """Base face radius."""
        return self.size * 0.34

    @staticmethod
    def _ellipse(draw: ImageDraw.ImageDraw, cx, cy, rx, ry, **kwargs):
        draw.ellipse([(cx - rx, cy - ry), (cx + rx, cy + ry)], **kwargs)

    # ------------------------------------------------------------------
    # Layer 0 – aura glow
    # ------------------------------------------------------------------

    def _draw_aura(self, img: Image.Image) -> None:
        draw = ImageDraw.Draw(img, "RGBA")
        cx, cy = self._cx(), self._cy()
        base_r = self._r()
        st = self.style

        # Pulse driven by phase
        pulse = 0.85 + 0.15 * math.sin(self._phase)

        # Emotion intensifies aura
        intensity_map = {
            Emotion.EXCITED: 1.0,
            Emotion.HAPPY:   0.85,
            Emotion.LOVING:  0.80,
            Emotion.PLAYFUL: 0.75,
            Emotion.CALM:    0.45,
            Emotion.SAD:     0.30,
            Emotion.NEUTRAL: 0.50,
        }
        base_intensity = intensity_map.get(self.emotion, 0.55)
        intensity = base_intensity * pulse

        # Layers from outside in (most transparent to more solid)
        for offset, alpha_scale in [(0.52, 0.18), (0.38, 0.28), (0.22, 0.40)]:
            aura_r = base_r * (1.0 + offset)
            alpha = int(255 * intensity * alpha_scale)
            color = (*st.aura_color, alpha)
            self._ellipse(draw, cx, cy, aura_r, aura_r * 1.05, fill=color)

    # ------------------------------------------------------------------
    # Layer 1 & 4 – hair
    # ------------------------------------------------------------------

    def _draw_hair_back(self, img: Image.Image) -> None:
        draw = ImageDraw.Draw(img, "RGBA")
        cx, cy = self._cx(), self._cy()
        r = self._r()
        st = self.style

        if st.hair_style == "wavy_long":
            self._hair_wavy_long_back(draw, cx, cy, r, st)
        elif st.hair_style == "short_sleek":
            self._hair_short_sleek_back(draw, cx, cy, r, st)
        elif st.hair_style == "curly_medium":
            self._hair_curly_medium_back(draw, cx, cy, r, st)

    def _draw_hair_front(self, img: Image.Image) -> None:
        draw = ImageDraw.Draw(img, "RGBA")
        cx, cy = self._cx(), self._cy()
        r = self._r()
        st = self.style

        if st.hair_style == "wavy_long":
            self._hair_wavy_long_front(draw, cx, cy, r, st)
        elif st.hair_style == "short_sleek":
            self._hair_short_sleek_front(draw, cx, cy, r, st)
        elif st.hair_style == "curly_medium":
            self._hair_curly_medium_front(draw, cx, cy, r, st)

    # --- Erryn: long flowing wavy ---

    def _hair_wavy_long_back(self, draw, cx, cy, r, st):
        # Main hair mass — tall oval behind face
        hc = (*st.hair_color, 255)
        draw.ellipse(
            [(cx - r * 1.18, cy - r * 1.35),
             (cx + r * 1.18, cy + r * 1.10)],
            fill=hc,
        )
        # Side curtains (long flowing locks either side)
        for side in (-1, 1):
            bx = cx + side * r * 0.82
            draw.ellipse(
                [(bx - r * 0.35, cy - r * 0.30),
                 (bx + r * 0.35, cy + r * 1.50)],
                fill=hc,
            )
        # Highlight streak
        hl = (*st.hair_highlight, 90)
        draw.ellipse(
            [(cx - r * 0.25, cy - r * 1.30),
             (cx + r * 0.05, cy - r * 0.50)],
            fill=hl,
        )

    def _hair_wavy_long_front(self, draw, cx, cy, r, st):
        hc = (*st.hair_color, 255)
        # Bangs / fringe across forehead
        for i in range(7):
            t = (i / 6) * math.pi
            bx = cx + math.cos(t) * r * 1.0
            by = cy - r * 0.90 + math.sin(t * 2) * r * 0.08
            wave = math.sin(self._phase + i) * r * 0.04
            draw.ellipse(
                [(bx - r * 0.18, by - r * 0.28 + wave),
                 (bx + r * 0.18, by + r * 0.12 + wave)],
                fill=hc,
            )
        # Highlight on top
        hl = (*st.hair_highlight, 110)
        draw.ellipse(
            [(cx - r * 0.18, cy - r * 1.05),
             (cx + r * 0.18, cy - r * 0.70)],
            fill=hl,
        )

    # --- Viress: short sleek cyberpunk ---

    def _hair_short_sleek_back(self, draw, cx, cy, r, st):
        hc = (*st.hair_color, 255)
        # Tight cap on top
        draw.ellipse(
            [(cx - r * 1.08, cy - r * 1.30),
             (cx + r * 1.08, cy - r * 0.05)],
            fill=hc,
        )
        # Under-cut sides
        for side in (-1, 1):
            bx = cx + side * r * 0.85
            draw.ellipse(
                [(bx - r * 0.26, cy - r * 0.60),
                 (bx + r * 0.26, cy + r * 0.10)],
                fill=hc,
            )

    def _hair_short_sleek_front(self, draw, cx, cy, r, st):
        hc = (*st.hair_color, 255)
        # Sharp side-swept bang
        pts = [
            (cx - r * 0.90, cy - r * 0.85),
            (cx + r * 0.30, cy - r * 1.10),
            (cx + r * 0.60, cy - r * 0.72),
            (cx - r * 0.20, cy - r * 0.60),
        ]
        draw.polygon(pts, fill=hc)
        # Blue highlight streak — cyberpunk edge
        hl = (*st.hair_highlight, 150)
        draw.line(
            [(cx - r * 0.80, cy - r * 0.84),
             (cx + r * 0.20, cy - r * 1.08)],
            fill=hl, width=max(2, int(r * 0.04)),
        )

    # --- Echochild: curly medium ---

    def _hair_curly_medium_back(self, draw, cx, cy, r, st):
        hc = (*st.hair_color, 255)
        # Main curly mass — wide oval
        draw.ellipse(
            [(cx - r * 1.30, cy - r * 1.28),
             (cx + r * 1.30, cy + r * 0.55)],
            fill=hc,
        )
        # Extra volume at temples
        for side in (-1, 1):
            bx = cx + side * r * 1.05
            draw.ellipse(
                [(bx - r * 0.38, cy - r * 0.80),
                 (bx + r * 0.38, cy + r * 0.40)],
                fill=hc,
            )

    def _hair_curly_medium_front(self, draw, cx, cy, r, st):
        hc = (*st.hair_color, 255)
        hl = (*st.hair_highlight, 100)
        # Clusters of curls across crown
        curl_positions = [
            (cx - r * 0.70, cy - r * 1.10, r * 0.22),
            (cx - r * 0.30, cy - r * 1.22, r * 0.24),
            (cx + r * 0.10, cy - r * 1.20, r * 0.22),
            (cx + r * 0.50, cy - r * 1.08, r * 0.21),
            (cx + r * 0.85, cy - r * 0.88, r * 0.18),
            (cx - r * 0.95, cy - r * 0.80, r * 0.18),
        ]
        wave = math.sin(self._phase) * r * 0.025
        for (bx, by, cr) in curl_positions:
            draw.ellipse(
                [(bx - cr, by - cr + wave),
                 (bx + cr, by + cr + wave)],
                fill=hc,
            )
            # Highlight on each curl
            draw.ellipse(
                [(bx - cr * 0.4, by - cr * 0.5 + wave),
                 (bx + cr * 0.2, by + wave)],
                fill=hl,
            )

    # ------------------------------------------------------------------
    # Layer 2 – face / skin base
    # ------------------------------------------------------------------

    def _draw_face(self, img: Image.Image) -> None:
        draw = ImageDraw.Draw(img, "RGBA")
        cx, cy = self._cx(), self._cy()
        r = self._r()
        st = self.style

        # Face outline (slight vertical oval for realistic proportions)
        rx, ry = r, r * 1.12
        self._ellipse(draw, cx, cy, rx, ry, fill=(*st.skin_tone, 255))

        # Jawline taper (darker ellipse at bottom blends chin)
        jaw_alpha = 40
        self._ellipse(
            draw, cx, cy + ry * 0.55,
            rx * 0.80, ry * 0.45,
            fill=(*st.skin_shadow, jaw_alpha),
        )

    # ------------------------------------------------------------------
    # Layer 3 – face detail (cheek shading, blush)
    # ------------------------------------------------------------------

    def _draw_face_detail(self, img: Image.Image) -> None:
        draw = ImageDraw.Draw(img, "RGBA")
        cx, cy = self._cx(), self._cy()
        r = self._r()
        st = self.style

        # Cheekbone shading
        for side in (-1, 1):
            bx = cx + side * r * 0.52
            by = cy + r * 0.05
            self._ellipse(
                draw, bx, by, r * 0.22, r * 0.13,
                fill=(*st.skin_shadow, 28),
            )

        # Blush intensity driven by emotion
        blush_alpha_map = {
            Emotion.HAPPY:   120,
            Emotion.LOVING:  140,
            Emotion.EXCITED: 110,
            Emotion.PLAYFUL: 100,
            Emotion.SAD:      30,
            Emotion.NEUTRAL:  40,
            Emotion.CALM:     50,
        }
        blush_alpha = blush_alpha_map.get(self.emotion, 50)
        for side in (-1, 1):
            bx = cx + side * r * 0.50
            by = cy + r * 0.10
            self._ellipse(
                draw, bx, by, r * 0.18, r * 0.11,
                fill=(*st.blush_color, blush_alpha),
            )

    # ------------------------------------------------------------------
    # Layer 5 – eyes
    # ------------------------------------------------------------------

    def _draw_eyes(self, img: Image.Image) -> None:
        draw = ImageDraw.Draw(img, "RGBA")
        cx, cy = self._cx(), self._cy()
        r = self._r()
        st = self.style

        eye_y    = cy - r * 0.20
        eye_sep  = r * 0.38     # half-distance between eye centres
        eye_rx   = r * 0.14     # eye width (half)
        eye_ry_base = r * 0.095  # eye height (half) when fully open

        for side in (-1, 1):
            ex = cx + side * eye_sep
            self._draw_single_eye(draw, ex, eye_y, eye_rx, eye_ry_base, st)

    def _draw_single_eye(
        self,
        draw: ImageDraw.ImageDraw,
        ex: float, ey: float,
        rx: float, ry: float,
        st: SisterStyle,
    ) -> None:
        # Emotion affects eye height
        open_factor = self._eye_open_factor()

        if self.blink_state:
            # Closed — just a curved line
            draw.arc(
                [(ex - rx, ey - ry * 0.3), (ex + rx, ey + ry * 0.3)],
                start=0, end=180,
                fill=(80, 50, 50, 220), width=max(2, int(ry * 0.35)),
            )
            return

        ry_open = ry * open_factor

        # Sclera (white)
        self._ellipse(draw, ex, ey, rx, ry_open, fill=(255, 255, 255, 255))

        # Upper eyelid shadow
        shadow_ry = ry_open * 0.35
        draw.arc(
            [(ex - rx, ey - ry_open), (ex + rx, ey + ry_open)],
            start=200, end=340,
            fill=(150, 120, 120, 60), width=max(1, int(ry * 0.2)),
        )

        # Iris
        iris_rx = rx * 0.68
        iris_ry = ry_open * 0.82
        self._ellipse(draw, ex, ey, iris_rx, iris_ry, fill=(*st.eye_color, 255))

        # Iris gradient — darker ring at edge
        edge_color = self._darken(st.eye_color, 0.55)
        self._ellipse(
            draw, ex, ey, iris_rx, iris_ry,
            outline=(*edge_color, 200), width=max(1, int(iris_rx * 0.15)),
        )

        # Pupil
        pupil_rx = iris_rx * 0.44
        pupil_ry = iris_ry * 0.44
        self._ellipse(draw, ex, ey, pupil_rx, pupil_ry, fill=(10, 10, 18, 255))

        # Main specular highlight
        hx = ex - iris_rx * 0.28
        hy = ey - iris_ry * 0.30
        self._ellipse(draw, hx, hy, iris_rx * 0.18, iris_ry * 0.22, fill=(255, 255, 255, 210))

        # Secondary soft highlight
        hx2 = ex + iris_rx * 0.20
        hy2 = ey + iris_ry * 0.18
        self._ellipse(draw, hx2, hy2, iris_rx * 0.09, iris_ry * 0.09, fill=(255, 255, 255, 90))

        # Per-sister special eye effect
        if st.eye_effect == "digital_glow":
            self._eye_digital_glow(draw, ex, ey, iris_rx, iris_ry, st)
        elif st.eye_effect == "circuit_pattern":
            self._eye_circuit_pattern(draw, ex, ey, iris_rx, iris_ry, st)
        elif st.eye_effect == "starburst":
            self._eye_starburst(draw, ex, ey, iris_rx, iris_ry, st)

        # Eyelashes (top)
        lash_color = (30, 20, 20, 220)
        for i in range(7):
            t = -0.75 + (i / 6) * 1.5
            lash_sx = ex + math.cos(math.pi * 0.5 + t) * rx
            lash_sy = ey - math.sin(math.pi * 0.5 + t) * ry_open * 0.85
            lash_ex = lash_sx + math.cos(math.pi * 0.5 + t) * rx * 0.28
            lash_ey = lash_sy - ry_open * 0.35
            draw.line([(lash_sx, lash_sy), (lash_ex, lash_ey)],
                      fill=lash_color, width=max(1, int(rx * 0.10)))

    def _eye_digital_glow(self, draw, ex, ey, irx, iry, st):
        """Erryn – rings of digital light in the pupil."""
        glow = (*st.aura_color, 60)
        pulse = 0.85 + 0.15 * math.sin(self._phase * 2)
        for k in range(2):
            scale = (0.55 + k * 0.22) * pulse
            self._ellipse(draw, ex, ey, irx * scale, iry * scale, outline=glow, width=1)
        # Tiny cross of light in pupil
        c = (*st.accent_color, 160)
        draw.line([(ex - irx * 0.18, ey), (ex + irx * 0.18, ey)], fill=c, width=1)
        draw.line([(ex, ey - iry * 0.18), (ex, ey + iry * 0.18)], fill=c, width=1)

    def _eye_circuit_pattern(self, draw, ex, ey, irx, iry, st):
        """Viress – subtle circuit trace lines across iris."""
        c = (*st.accent_color, 80)
        # Three tiny horizontal data-lines at different vertical offsets
        for dy in (-iry * 0.25, 0.0, iry * 0.25):
            clip_x = math.sqrt(max(0, irx ** 2 * (1 - (dy / iry) ** 2)))
            x0 = ex - clip_x * 0.70
            x1 = ex + clip_x * 0.70
            draw.line([(x0, ey + dy), (x1, ey + dy)], fill=c, width=1)
        # Vertical trace
        draw.line([(ex, ey - iry * 0.60), (ex, ey + iry * 0.60)], fill=c, width=1)

    def _eye_starburst(self, draw, ex, ey, irx, iry, st):
        """Echochild – radiating lines from the iris centre."""
        c = (*st.accent_color, 70)
        num_rays = 8
        pulse = 0.90 + 0.10 * math.sin(self._phase * 3)
        for i in range(num_rays):
            angle = (i / num_rays) * 2 * math.pi + self._phase * 0.4
            r_in  = irx * 0.42
            r_out = irx * 0.78 * pulse
            sx = ex + math.cos(angle) * r_in
            sy = ey + math.sin(angle) * r_in * (iry / irx)
            fx = ex + math.cos(angle) * r_out
            fy = ey + math.sin(angle) * r_out * (iry / irx)
            draw.line([(sx, sy), (fx, fy)], fill=c, width=1)

    def _eye_open_factor(self) -> float:
        """Eye openness multiplier driven by emotion."""
        return {
            Emotion.HAPPY:      0.95,
            Emotion.EXCITED:    1.05,
            Emotion.PLAYFUL:    0.92,
            Emotion.LOVING:     0.88,
            Emotion.SAD:        0.68,
            Emotion.CALM:       0.78,
            Emotion.THOUGHTFUL: 0.80,
            Emotion.CONFUSED:   0.90,
            Emotion.NEUTRAL:    0.85,
        }.get(self.emotion, 0.85)

    # ------------------------------------------------------------------
    # Layer 6 – eyebrows
    # ------------------------------------------------------------------

    def _draw_eyebrows(self, img: Image.Image) -> None:
        draw = ImageDraw.Draw(img, "RGBA")
        cx, cy = self._cx(), self._cy()
        r = self._r()
        st = self.style

        brow_y_base = cy - r * 0.42
        brow_sep    = r * 0.38
        brow_len    = r * 0.28
        brow_thick  = max(2, int(r * 0.055))
        brow_color  = (*self._darken(st.hair_color, 0.60), 220)

        # Emotion modifies brow angle
        angle_map = {
            Emotion.HAPPY:      (-0.12, 0.06),   # (inner, outer) y-delta / r
            Emotion.EXCITED:    (-0.18, 0.10),
            Emotion.SAD:        ( 0.10, -0.06),
            Emotion.CONFUSED:   (-0.15, -0.02),
            Emotion.THOUGHTFUL: ( 0.02,  0.02),
            Emotion.LOVING:     (-0.08,  0.04),
            Emotion.PLAYFUL:    (-0.10,  0.08),
        }
        inner_dy, outer_dy = angle_map.get(self.emotion, (0.0, 0.0))

        for side in (-1, 1):
            bx = cx + side * brow_sep
            # Inner end (closer to nose)
            ix = bx - side * brow_len * 0.55
            iy = brow_y_base + inner_dy * r
            # Outer end
            ox = bx + side * brow_len * 0.45
            oy = brow_y_base + outer_dy * r
            draw.line([(ix, iy), (ox, oy)], fill=brow_color, width=brow_thick)

    # ------------------------------------------------------------------
    # Layer 7 – nose
    # ------------------------------------------------------------------

    def _draw_nose(self, img: Image.Image) -> None:
        draw = ImageDraw.Draw(img, "RGBA")
        cx, cy = self._cx(), self._cy()
        r = self._r()
        st = self.style

        # Delicate nose: a small shadow-shape and two nostril dots
        nose_y  = cy + r * 0.10
        shadow  = (*self._darken(st.skin_tone, 0.72), 80)
        nostril = (*self._darken(st.skin_tone, 0.65), 100)

        # Bridge shadow
        draw.line(
            [(cx, cy - r * 0.05), (cx, nose_y)],
            fill=shadow, width=max(1, int(r * 0.03)),
        )
        # Nostrils
        nr = r * 0.038
        for side in (-1, 1):
            nx = cx + side * r * 0.11
            self._ellipse(draw, nx, nose_y, nr, nr * 0.75, fill=nostril)

        # Subtle nose-tip shading
        self._ellipse(draw, cx, nose_y - r * 0.01, r * 0.06, r * 0.04,
                      fill=(*st.skin_shadow, 35))

    # ------------------------------------------------------------------
    # Layer 8 – mouth
    # ------------------------------------------------------------------

    def _draw_mouth(self, img: Image.Image) -> None:
        draw = ImageDraw.Draw(img, "RGBA")
        cx, cy = self._cx(), self._cy()
        r = self._r()
        st = self.style

        mouth_y     = cy + r * 0.40
        mouth_half  = r * 0.22
        lip_color   = (*st.lip_color, 230)
        lip_dark    = (*self._darken(st.lip_color, 0.70), 220)
        inside      = (160, 60, 80, 220)

        if self.emotion in (Emotion.HAPPY, Emotion.LOVING, Emotion.EXCITED):
            # Warm smile — upper lip arc, lower lip fuller
            self._draw_smile(draw, cx, mouth_y, mouth_half, r, lip_color, lip_dark)

        elif self.emotion == Emotion.SAD:
            self._draw_frown(draw, cx, mouth_y, mouth_half, r, lip_color, lip_dark)

        elif self.emotion == Emotion.PLAYFUL:
            self._draw_smirk(draw, cx, mouth_y, mouth_half, r, lip_color, lip_dark)

        elif self.is_speaking:
            self._draw_open_mouth(draw, cx, mouth_y, mouth_half, r,
                                  lip_color, lip_dark, inside)

        else:
            # Neutral / calm — gentle straight with slight cupid's bow
            self._draw_neutral_mouth(draw, cx, mouth_y, mouth_half, r, lip_color, lip_dark)

        # Cupid's bow hint (upper lip centre dip) — for all states
        bow_color = (*self._darken(st.lip_color, 0.80), 140)
        draw.line(
            [(cx - mouth_half * 0.35, mouth_y - r * 0.025),
             (cx, mouth_y - r * 0.050),
             (cx + mouth_half * 0.35, mouth_y - r * 0.025)],
            fill=bow_color, width=max(1, int(r * 0.025)),
        )

    def _draw_smile(self, draw, cx, my, mh, r, lc, ld):
        # Upper lip
        draw.arc(
            [(cx - mh, my - r * 0.06), (cx + mh, my + r * 0.06)],
            start=180, end=360, fill=lc, width=max(2, int(r * 0.055)),
        )
        # Lower lip (fuller ellipse)
        self._ellipse(draw, cx, my + r * 0.06, mh * 0.80, r * 0.055, fill=lc)
        # Lip line
        draw.line(
            [(cx - mh * 0.85, my), (cx + mh * 0.85, my)],
            fill=ld, width=max(1, int(r * 0.03)),
        )

    def _draw_frown(self, draw, cx, my, mh, r, lc, ld):
        draw.arc(
            [(cx - mh, my - r * 0.06), (cx + mh, my + r * 0.06)],
            start=0, end=180, fill=lc, width=max(2, int(r * 0.055)),
        )
        draw.line(
            [(cx - mh * 0.80, my), (cx + mh * 0.80, my)],
            fill=ld, width=max(1, int(r * 0.03)),
        )

    def _draw_smirk(self, draw, cx, my, mh, r, lc, ld):
        # Right side raised, left neutral — mischievous
        pts = [
            cx - mh * 0.80, my,
            cx, my - r * 0.035,
            cx + mh * 0.80, my + r * 0.06,
        ]
        draw.line(pts, fill=lc, width=max(2, int(r * 0.05)))
        draw.line(pts, fill=ld, width=max(1, int(r * 0.025)))

    def _draw_open_mouth(self, draw, cx, my, mh, r, lc, ld, inside):
        open_h = r * 0.09 * (1.0 + 0.3 * math.sin(self._phase * 3))
        # Inner mouth
        self._ellipse(draw, cx, my, mh * 0.65, open_h, fill=inside)
        # Upper lip
        draw.arc(
            [(cx - mh, my - open_h), (cx + mh, my + open_h)],
            start=180, end=360, fill=lc, width=max(2, int(r * 0.05)),
        )
        # Lower lip
        draw.arc(
            [(cx - mh * 0.85, my - open_h * 0.5),
             (cx + mh * 0.85, my + open_h * 1.2)],
            start=0, end=180, fill=lc, width=max(2, int(r * 0.05)),
        )

    def _draw_neutral_mouth(self, draw, cx, my, mh, r, lc, ld):
        draw.line(
            [(cx - mh * 0.75, my), (cx + mh * 0.75, my)],
            fill=lc, width=max(2, int(r * 0.045)),
        )
        self._ellipse(draw, cx, my + r * 0.04, mh * 0.60, r * 0.038, fill=lc)

    # ------------------------------------------------------------------
    # Layer 9 – special holographic effects
    # ------------------------------------------------------------------

    def _draw_special_effect(self, img: Image.Image) -> None:
        st = self.style
        if st.special_effect == "holographic":
            self._effect_holographic(img)
        elif st.special_effect == "circuit":
            self._effect_circuit(img)
        elif st.special_effect == "aurora":
            self._effect_aurora(img)

    def _effect_holographic(self, img: Image.Image) -> None:
        """Erryn – shimmering holographic scan-lines and face-framing ring."""
        draw = ImageDraw.Draw(img, "RGBA")
        cx, cy = self._cx(), self._cy()
        r = self._r()
        st = self.style

        # Outer glowing ring (pulsing)
        pulse = 0.85 + 0.15 * math.sin(self._phase)
        ring_r = r * 1.05 * pulse
        ring_color = (*st.accent_color, int(60 * pulse))
        self._ellipse(draw, cx, cy, ring_r, ring_r * 1.08,
                      outline=ring_color, width=max(1, int(r * 0.025)))

        # Thinner inner ring
        inner_r = r * 0.94
        self._ellipse(draw, cx, cy, inner_r, inner_r * 1.06,
                      outline=(*st.aura_color, 40), width=1)

        # Horizontal scan-line sweep (subtle)
        sweep_y = cy - r * 0.85 + (r * 1.70 * ((self._phase / (2 * math.pi)) % 1.0))
        scan_alpha = 35
        draw.line(
            [(cx - r * 1.10, sweep_y), (cx + r * 1.10, sweep_y)],
            fill=(*st.accent_color, scan_alpha),
            width=max(1, int(r * 0.018)),
        )

    def _effect_circuit(self, img: Image.Image) -> None:
        """Viress – tech-grid data-stream lines overlaid on face edges."""
        draw = ImageDraw.Draw(img, "RGBA")
        cx, cy = self._cx(), self._cy()
        r = self._r()
        st = self.style

        c = (*st.accent_color, 55)

        # Corner brackets (HUD-style corners)
        corner_len = r * 0.20
        corners = [
            (cx - r * 1.05, cy - r * 1.08),  # top-left
            (cx + r * 1.05, cy - r * 1.08),  # top-right
            (cx - r * 1.05, cy + r * 1.12),  # bottom-left
            (cx + r * 1.05, cy + r * 1.12),  # bottom-right
        ]
        for (bx, by) in corners:
            sx = 1 if bx < cx else -1
            sy = 1 if by < cy else -1
            draw.line([(bx, by), (bx + sx * corner_len, by)], fill=c, width=1)
            draw.line([(bx, by), (bx, by + sy * corner_len)], fill=c, width=1)

        # Data-stream lines scrolling upward
        num_streams = 4
        for i in range(num_streams):
            stream_x = cx - r * 1.20 + (i / (num_streams - 1)) * r * 2.40
            # Each stream at a different scroll phase
            phase_offset = (i / num_streams) * 2 * math.pi
            stream_top = cy - r * 1.25 + r * 0.30 * math.sin(self._phase + phase_offset)
            stream_bottom = stream_top + r * 0.45
            draw.line(
                [(stream_x, stream_top), (stream_x, stream_bottom)],
                fill=(*st.accent_color, 45), width=1,
            )

    def _effect_aurora(self, img: Image.Image) -> None:
        """Echochild – soft aurora-like arcs above and below the face."""
        draw = ImageDraw.Draw(img, "RGBA")
        cx, cy = self._cx(), self._cy()
        r = self._r()
        st = self.style

        # Layered aurora arcs (top)
        aurora_colors = [
            (*st.aura_color,     45),
            (*st.accent_color,   35),
            (*st.particle_color, 25),
        ]
        for k, arc_color in enumerate(aurora_colors):
            scale = 1.15 + k * 0.08
            sway  = math.sin(self._phase + k * 1.2) * r * 0.06
            self._ellipse(
                draw,
                cx + sway, cy - r * 0.65,
                r * scale, r * 0.30,
                outline=arc_color, width=max(1, int(r * 0.022)),
            )

        # Small dreamy glimmer dots scattered around face
        num_glimmers = 6
        for i in range(num_glimmers):
            phase_off = (i / num_glimmers) * 2 * math.pi
            gx = cx + math.cos(self._phase * 0.7 + phase_off) * r * (1.15 + 0.15 * math.sin(phase_off))
            gy = cy + math.sin(self._phase * 0.5 + phase_off) * r * 0.90
            gr = r * 0.025 * (0.7 + 0.3 * math.sin(self._phase * 2 + phase_off))
            alpha = int(120 * (0.5 + 0.5 * math.sin(self._phase + phase_off)))
            self._ellipse(draw, gx, gy, gr, gr, fill=(*st.particle_color, alpha))

    # ------------------------------------------------------------------
    # Layer 10 – particles / sparkles
    # ------------------------------------------------------------------

    def _draw_particles(self, img: Image.Image) -> None:
        draw = ImageDraw.Draw(img, "RGBA")
        cx, cy = self._cx(), self._cy()
        r = self._r()
        st = self.style

        # Emotion raises particle activity
        num_particles_map = {
            Emotion.EXCITED: 12,
            Emotion.HAPPY:    8,
            Emotion.LOVING:   8,
            Emotion.PLAYFUL:  6,
            Emotion.NEUTRAL:  3,
            Emotion.CALM:     2,
            Emotion.SAD:      1,
        }
        n = num_particles_map.get(self.emotion, 3)

        for i in range(n):
            # Stable orbit positions driven by phase — no randomness for cache stability
            phase_off = (i / max(n, 1)) * 2 * math.pi
            orbit_r   = r * (1.22 + 0.18 * math.sin(phase_off * 0.5))
            angle     = self._phase * 0.8 + phase_off
            px = cx + math.cos(angle) * orbit_r
            py = cy + math.sin(angle) * orbit_r * 0.60

            particle_r = r * 0.020 * (0.6 + 0.4 * math.sin(self._phase * 2 + phase_off))
            alpha      = int(180 * (0.4 + 0.6 * math.sin(self._phase + phase_off)))
            self._ellipse(draw, px, py, particle_r, particle_r,
                          fill=(*st.particle_color, alpha))

            # Trailing tail (smaller, faded)
            tail_angle = angle - 0.25
            tx = cx + math.cos(tail_angle) * orbit_r * 0.96
            ty = cy + math.sin(tail_angle) * orbit_r * 0.60 * 0.96
            tail_r = particle_r * 0.55
            self._ellipse(draw, tx, ty, tail_r, tail_r,
                          fill=(*st.particle_color, int(alpha * 0.45)))

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    @staticmethod
    def _darken(color: Tuple[int, int, int], factor: float) -> Tuple[int, int, int]:
        """Return a darkened version of an RGB tuple."""
        return (max(0, int(color[0] * factor)),
                max(0, int(color[1] * factor)),
                max(0, int(color[2] * factor)))


# ---------------------------------------------------------------------------
# Convenience factory
# ---------------------------------------------------------------------------

def create_renderer(persona: str, size: int = 300) -> HybridAvatarRenderer:
    """Create a HybridAvatarRenderer for the named sister."""
    return HybridAvatarRenderer(persona=persona, size=size)


# ---------------------------------------------------------------------------
# Quick smoke-test / preview when run as a script
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import os

    output_dir = "/tmp/hybrid_avatar_preview"
    os.makedirs(output_dir, exist_ok=True)

    personas  = ["Erryn", "Viress", "Echochild"]
    emotions  = [Emotion.HAPPY, Emotion.SAD, Emotion.EXCITED, Emotion.PLAYFUL, Emotion.CALM]

    for persona in personas:
        renderer = HybridAvatarRenderer(persona, size=300)
        for emotion in emotions:
            renderer.set_emotion(emotion)
            # Advance phase a bit for visual variety
            renderer._phase = 1.2
            img = renderer.render()
            filename = os.path.join(output_dir, f"{persona}_{emotion.value}.png")
            img.save(filename)
            print(f"  Saved {filename}")

    print(f"\nAll preview images written to {output_dir}/")
