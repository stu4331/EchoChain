"""
Image Baseline Extractor
Computes simple visual features from an image to guide avatar styling:
- Dominant colors (palette)
- Average brightness and contrast
- Warmth/coolness via hue

Dependencies: Pillow (PIL)
"""
from typing import Dict, Tuple, List

try:
    from PIL import Image
    PIL_AVAILABLE = True
except Exception as _e:
    PIL_AVAILABLE = False
    raise


def _get_palette(img: Image.Image, k: int = 5) -> List[Tuple[int, int, int]]:
    """Return k dominant colors via Pillow's quantize."""
    # Convert to RGB and reduce size for speed
    small = img.convert('RGB')
    small.thumbnail((256, 256))
    pal = small.quantize(colors=k, method=2)
    palette = pal.getpalette()
    color_counts = pal.getcolors()
    # Build top colors list
    colors = []
    if palette and color_counts:
        for count, idx in sorted(color_counts, key=lambda x: -x[0])[:k]:
            base = idx * 3
            colors.append((palette[base], palette[base+1], palette[base+2]))
    return colors


def _avg_brightness_contrast(img: Image.Image) -> Tuple[float, float]:
    """Compute average brightness and a simple contrast proxy."""
    gray = img.convert('L')
    hist = gray.histogram()
    total = sum(hist)
    # Average brightness
    avg = sum(i * v for i, v in enumerate(hist)) / max(total, 1)
    # Contrast proxy: standard deviation approx using histogram
    mean = avg
    var = sum(((i - mean) ** 2) * v for i, v in enumerate(hist)) / max(total, 1)
    contrast = var ** 0.5
    return avg / 255.0, contrast / 128.0  # normalize


def _avg_hue(img: Image.Image) -> float:
    """Compute average hue (0..1)."""
    hsv = img.convert('HSV')
    w, h = hsv.size
    pixels = hsv.getdata()
    # sample up to ~50k pixels
    step = max(1, (w * h) // 50000)
    total = 0
    count = 0
    for i, (hh, ss, vv) in enumerate(pixels):
        if i % step:
            continue
        total += hh
        count += 1
    return (total / max(count, 1)) / 255.0


def analyze_image(path: str) -> Dict:
    """Load image and return baseline metrics and recommended avatar colors."""
    img = Image.open(path)
    metrics: Dict = {}
    palette = _get_palette(img, k=5)
    brightness, contrast = _avg_brightness_contrast(img)
    hue = _avg_hue(img)

    metrics['palette'] = palette
    metrics['brightness'] = brightness
    metrics['contrast'] = contrast
    metrics['avg_hue'] = hue

    # Simple guidance for avatar persona colors
    # Warm hues → pink/peach blush; cool hues → cyan/purple glow
    glow_color = '#00d4ff' if hue > 0.55 or hue < 0.10 else '#533483'
    blush_color = '#ffc9ba' if brightness >= 0.4 else '#ffd1e6'
    # Face base from top palette color
    def to_hex(rgb: Tuple[int, int, int]) -> str:
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
    base = to_hex(palette[0]) if palette else '#f2d2b4'

    metrics['recommendation'] = {
        'face_base_color': base,
        'blush_color': blush_color,
        'glow_color': glow_color
    }
    return metrics
