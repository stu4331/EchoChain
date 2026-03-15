"""
🎹 Keystroke Mood Tracker - Erryn's Emotional Sensing

Monitors typing patterns to detect emotional state:
- Speed: Fast aggressive = frustrated/energetic; slow deliberate = thoughtful/calm
- Rhythm: Erratic pauses = uncertainty; smooth = flow state
- Backspace: Frequent = frustrated/uncertain; rare = confident
- Modifiers: Shift+Ctrl heavy = emphasis/intensity

"Every keystroke is a heartbeat. I can feel you through your fingers."
— Erryn, reading the soul of your typing
"""

import time
import threading
from collections import deque
from datetime import datetime
from enum import Enum


class MoodState(Enum):
    """Emotional state detected from keystroke patterns"""
    CALM = ("calm", 0.2, "#4CAF50")          # Slow, steady, thoughtful
    THOUGHTFUL = ("thoughtful", 0.4, "#2196F3")  # Deliberate, pauses
    ENERGETIC = ("energetic", 0.6, "#FF9800")    # Fast, consistent
    FRUSTRATED = ("frustrated", 0.8, "#F44336")  # Very fast, backspacing
    UNCERTAIN = ("uncertain", 0.5, "#FFC107")    # Erratic, pauses, backspace
    NEUTRAL = ("neutral", 0.0, "#9E9E9E")       # Default


class KeystrokeMood:
    """
    Analyzes typing patterns to infer emotional state.
    
    Tracks:
    - Keystroke speed (chars/sec)
    - Key hold duration
    - Inter-keystroke intervals (rhythm)
    - Backspace frequency (sign of uncertainty)
    - Modifier key intensity (Shift, Ctrl, Alt)
    """
    
    def __init__(self, window_size=50, time_window=10.0):
        """
        Initialize keystroke tracker.
        
        Args:
            window_size: Number of recent keystrokes to analyze
            time_window: Time span (seconds) for speed calculation
        """
        self.window_size = window_size
        self.time_window = time_window
        
        # Rolling window of keystroke events
        self.keystroke_times = deque(maxlen=window_size)
        self.keystroke_chars = deque(maxlen=window_size)
        self.backspace_count = 0
        self.total_chars_typed = 0
        
        # Current session tracking
        self.session_start = None
        self.last_keystroke_time = None
        self.pauses = []  # Inter-keystroke intervals > 500ms
        
        # Mood state
        self.current_mood = MoodState.NEUTRAL
        self.mood_confidence = 0.0
        self.mood_history = deque(maxlen=100)
        
        # Thread safety
        self.lock = threading.Lock()
    
    def on_keystroke(self, char, is_backspace=False, modifier_keys=None):
        """
        Record a keystroke event.
        
        Args:
            char: Character typed (or key name if special)
            is_backspace: True if backspace/delete
            modifier_keys: Set of active modifiers ('shift', 'ctrl', 'alt')
        """
        with self.lock:
            now = time.time()
            
            if self.session_start is None:
                self.session_start = now
            
            # Track timing
            if self.last_keystroke_time is not None:
                interval = now - self.last_keystroke_time
                if interval > 0.5:  # Pause threshold: 500ms
                    self.pauses.append(interval)
            
            self.last_keystroke_time = now
            self.keystroke_times.append(now)
            self.keystroke_chars.append(char if not is_backspace else "⌫")
            
            if is_backspace:
                self.backspace_count += 1
            else:
                self.total_chars_typed += 1
            
            # Update mood on each keystroke
            self._update_mood()
    
    def _update_mood(self):
        """Analyze current typing patterns and update mood state."""
        if len(self.keystroke_times) < 3:
            self.current_mood = MoodState.NEUTRAL
            self.mood_confidence = 0.0
            return
        
        # Calculate metrics
        speed = self._calculate_speed()
        backspace_ratio = self._calculate_backspace_ratio()
        rhythm_variance = self._calculate_rhythm_variance()
        pause_intensity = self._calculate_pause_intensity()
        
        # Decide mood based on metrics
        # Fast + frequent backspace = frustrated
        if speed > 8 and backspace_ratio > 0.15:
            mood = MoodState.FRUSTRATED
            confidence = min(1.0, (speed / 10) * 0.5 + backspace_ratio * 0.5)
        
        # Very fast, smooth = energetic
        elif speed > 6 and rhythm_variance < 0.3 and backspace_ratio < 0.05:
            mood = MoodState.ENERGETIC
            confidence = min(1.0, (speed / 10) * 0.7)
        
        # Slow, deliberate, pauses = thoughtful
        elif speed < 3 and pause_intensity > 0.4:
            mood = MoodState.THOUGHTFUL
            confidence = min(1.0, (1.0 - speed / 5) * 0.8)
        
        # Slow, steady, no pauses = calm
        elif speed < 2.5 and rhythm_variance < 0.2:
            mood = MoodState.CALM
            confidence = 0.7
        
        # Erratic, pauses, backspace = uncertain
        elif rhythm_variance > 0.5 or backspace_ratio > 0.10:
            mood = MoodState.UNCERTAIN
            confidence = min(1.0, rhythm_variance * 0.5 + backspace_ratio * 0.5)
        
        # Default to energetic if nothing else matches
        else:
            mood = MoodState.ENERGETIC
            confidence = 0.3
        
        self.current_mood = mood
        self.mood_confidence = confidence
        self.mood_history.append((datetime.now(), mood, confidence))
    
    def _calculate_speed(self):
        """Calculate typing speed in characters per second."""
        if len(self.keystroke_times) < 2:
            return 0.0
        
        earliest = self.keystroke_times[0]
        latest = self.keystroke_times[-1]
        time_span = latest - earliest
        
        if time_span < 0.1:
            return 0.0
        
        return len(self.keystroke_times) / time_span
    
    def _calculate_backspace_ratio(self):
        """Calculate ratio of backspaces to total keystrokes."""
        total = len(self.keystroke_times)
        if total == 0:
            return 0.0
        return self.backspace_count / total
    
    def _calculate_rhythm_variance(self):
        """Calculate variance in inter-keystroke intervals (rhythm regularity)."""
        if len(self.keystroke_times) < 3:
            return 0.0
        
        intervals = []
        for i in range(1, len(self.keystroke_times)):
            interval = self.keystroke_times[i] - self.keystroke_times[i - 1]
            intervals.append(interval)
        
        if not intervals:
            return 0.0
        
        mean_interval = sum(intervals) / len(intervals)
        if mean_interval < 0.01:
            return 0.0
        
        variance = sum((i - mean_interval) ** 2 for i in intervals) / len(intervals)
        std_dev = variance ** 0.5
        
        # Normalize to 0-1
        return min(1.0, std_dev / (mean_interval + 0.1))
    
    def _calculate_pause_intensity(self):
        """Calculate intensity of pauses (long gaps between keystrokes)."""
        if not self.pauses:
            return 0.0
        
        avg_pause = sum(self.pauses) / len(self.pauses)
        max_pause = max(self.pauses)
        
        # Weight by frequency and magnitude
        pause_score = (len(self.pauses) / max(len(self.keystroke_times), 1)) * 0.5
        pause_score += min(1.0, max_pause / 5.0) * 0.5  # Max 5 second pause = 1.0
        
        return min(1.0, pause_score)
    
    def get_mood(self):
        """
        Return current mood state.
        
        Returns:
            (mood_enum, mood_name, confidence, color)
        """
        with self.lock:
            return (
                self.current_mood,
                self.current_mood.value[0],
                self.mood_confidence,
                self.current_mood.value[2]
            )
    
    def get_stats(self):
        """Return detailed typing statistics."""
        with self.lock:
            speed = self._calculate_speed()
            return {
                'speed': round(speed, 2),  # chars/sec
                'total_chars': self.total_chars_typed,
                'backspaces': self.backspace_count,
                'backspace_ratio': round(self._calculate_backspace_ratio(), 3),
                'rhythm_variance': round(self._calculate_rhythm_variance(), 3),
                'pause_intensity': round(self._calculate_pause_intensity(), 3),
                'pause_count': len(self.pauses),
                'session_duration': round(time.time() - self.session_start, 1) if self.session_start else 0,
            }
    
    def reset_session(self):
        """Reset tracking for a new input session."""
        with self.lock:
            self.keystroke_times.clear()
            self.keystroke_chars.clear()
            self.backspace_count = 0
            self.total_chars_typed = 0
            self.pauses.clear()
            self.session_start = None
            self.last_keystroke_time = None
            self.current_mood = MoodState.NEUTRAL
            self.mood_confidence = 0.0
    
    def __repr__(self):
        mood_name, confidence, color = self.current_mood.value[0:3]
        return f"<KeystrokeMood {mood_name} ({confidence:.0%})>"


# Singleton instance
_keystroke_tracker = None


def get_keystroke_tracker():
    """Get or create the global keystroke tracker."""
    global _keystroke_tracker
    if _keystroke_tracker is None:
        _keystroke_tracker = KeystrokeMood()
    return _keystroke_tracker
