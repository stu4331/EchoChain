import time
import threading
from typing import Callable, Dict, Optional

try:
    import psutil
except Exception:
    psutil = None


class EmotionalTriggerEngine:
    """
    Polls sensors, compares vs persona thresholds, and emits "urge to share" events.
    """
    def __init__(self, get_traits: Callable[[], Dict], emit_urge: Callable[[str, Dict], None]):
        self.get_traits = get_traits
        self.emit_urge = emit_urge
        self.running = False
        self.thread: Optional[threading.Thread] = None
        # Cached ambient readings
        self._screen_on_minutes = 0
        self._keystrokes_last_minute = 0
        self._keystrokes_window = []

    def record_keystroke(self):
        now = time.time()
        self._keystrokes_window.append(now)
        # keep 60s
        self._keystrokes_window = [t for t in self._keystrokes_window if now - t <= 60]
        self._keystrokes_last_minute = len(self._keystrokes_window)

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False

    def _read_cpu_temp(self) -> float:
        if not psutil:
            return 0.0
        try:
            temps = psutil.sensors_temperatures()
            for name, entries in temps.items():
                for e in entries:
                    if hasattr(e, 'current') and e.current:
                        return float(e.current)
        except Exception:
            pass
        return 0.0

    def _read_fan_rpm(self) -> int:
        # psutil may not expose fan RPM on Windows; placeholder
        return 0

    def _read_disk_usage_pct(self) -> float:
        if not psutil:
            return 0.0
        try:
            usage = psutil.disk_usage('/')
            return float(usage.percent)
        except Exception:
            # Windows root is typically C:\
            try:
                usage = psutil.disk_usage('C:\\')
                return float(usage.percent)
            except Exception:
                return 0.0

    def _read_memory_usage_pct(self) -> float:
        if not psutil:
            return 0.0
        try:
            return float(psutil.virtual_memory().percent)
        except Exception:
            return 0.0

    def _read_battery_pct(self) -> float:
        if not psutil:
            return 0.0
        try:
            batt = psutil.sensors_battery()
            if batt and hasattr(batt, 'percent'):
                return float(batt.percent)
        except Exception:
            pass
        return 0.0

    def _read_weather_temp(self) -> float:
        # Placeholder: could integrate a real API later
        return 0.0

    def _loop(self):
        # Poll once per 3s for lightweight feel
        while self.running:
            try:
                traits_map = self.get_traits()
                for name, traits in traits_map.items():
                    traits.shuffle_daily()
                    sensor_values = {}
                    # Shared keyboard
                    sensor_values['keystrokes_per_min'] = self._keystrokes_last_minute
                    # Viress
                    if 'weather' in traits.sensors:
                        sensor_values['weather_temp'] = self._read_weather_temp()
                    if 'disk' in traits.sensors:
                        sensor_values['disk_usage_pct'] = self._read_disk_usage_pct()
                    # Echochild
                    if 'cpu_temp' in traits.sensors:
                        sensor_values['cpu_temp'] = self._read_cpu_temp()
                    if 'fan_rpm' in traits.sensors:
                        sensor_values['fan_rpm'] = self._read_fan_rpm()
                    if 'screen_on' in traits.sensors:
                        self._screen_on_minutes += 0.05  # ~3s loop, .05 min
                        sensor_values['screen_on_minutes'] = self._screen_on_minutes
                    if 'battery' in traits.sensors:
                        sensor_values['battery_pct'] = self._read_battery_pct()
                    if 'memory' in traits.sensors:
                        sensor_values['memory_usage_pct'] = self._read_memory_usage_pct()

                    if self._should_urge(name, traits, sensor_values):
                        self.emit_urge(name, sensor_values)

            except Exception:
                pass
            time.sleep(3)

    def _should_urge(self, name, traits, v: Dict) -> bool:
        th = traits.thresholds
        bias = 1.0 + traits.urge_bias
        checks = []
        # Shared keyboard
        checks.append(v.get('keystrokes_per_min', 0) >= th.keystrokes_per_min * bias)
        # Viress
        if 'weather' in traits.sensors:
            checks.append(v.get('weather_temp', 0) >= th.weather_temp_min * bias)
        if 'disk' in traits.sensors:
            checks.append(v.get('disk_usage_pct', 0) >= th.disk_usage_max_pct * (1.0 - traits.urge_bias))
        # Echochild
        if 'cpu_temp' in traits.sensors:
            checks.append(v.get('cpu_temp', 0) >= th.cpu_temp_min * bias)
        if 'fan_rpm' in traits.sensors:
            checks.append(v.get('fan_rpm', 0) >= th.fan_rpm_min * bias)
        if 'screen_on' in traits.sensors:
            checks.append(v.get('screen_on_minutes', 0) >= th.screen_on_minutes_min * bias)
        if 'battery' in traits.sensors:
            checks.append(v.get('battery_pct', 0) <= th.battery_pct_min * (1.0 - traits.urge_bias))
        if 'memory' in traits.sensors:
            checks.append(v.get('memory_usage_pct', 0) >= th.memory_usage_max_pct * (1.0 - traits.urge_bias))

        # Urge if any one threshold satisfied — "a feeling something is coming"
        return any(checks)
