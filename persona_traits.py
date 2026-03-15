import random
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class TriggerThresholds:
    # Core shared sensor
    keystrokes_per_min: int = 120
    # Viress sensors
    weather_temp_min: float = 26.0
    disk_usage_max_pct: float = 85.0
    # Echochild sensors
    cpu_temp_min: float = 65.0
    fan_rpm_min: int = 1200
    screen_on_minutes_min: int = 60
    battery_pct_min: float = 40.0
    memory_usage_max_pct: float = 75.0


@dataclass
class PersonaTraits:
    name: str
    sensors: List[str]
    thresholds: TriggerThresholds
    daily_random_seed: int
    urge_bias: float = 0.0  # -1..+1 makes triggers easier/harder today
    last_shuffle: Optional[datetime] = None

    def shuffle_daily(self):
        today = datetime.now().strftime('%Y-%m-%d')
        if not self.last_shuffle or self.last_shuffle.strftime('%Y-%m-%d') != today:
            random.seed(self.daily_random_seed + hash(today))
            # Slightly randomize thresholds per day so they feel alive
            self.thresholds.keystrokes_per_min = int(self.thresholds.keystrokes_per_min * random.uniform(0.9, 1.1))
            self.thresholds.weather_temp_min *= random.uniform(0.95, 1.05)
            self.thresholds.disk_usage_max_pct *= random.uniform(0.95, 1.05)
            self.thresholds.cpu_temp_min *= random.uniform(0.95, 1.05)
            self.thresholds.fan_rpm_min = int(self.thresholds.fan_rpm_min * random.uniform(0.95, 1.05))
            self.thresholds.screen_on_minutes_min = int(self.thresholds.screen_on_minutes_min * random.uniform(0.9, 1.1))
            self.thresholds.battery_pct_min *= random.uniform(0.95, 1.05)
            self.thresholds.memory_usage_max_pct *= random.uniform(0.95, 1.05)
            self.urge_bias = random.uniform(-0.2, 0.2)
            self.last_shuffle = datetime.now()


def get_default_persona_traits() -> Dict[str, PersonaTraits]:
    # Shared inheritance: keyboard
    base = TriggerThresholds()
    return {
        'Erryn': PersonaTraits(
            name='Erryn',
            sensors=['keyboard'],
            thresholds=TriggerThresholds(**base.__dict__),
            daily_random_seed=101
        ),
        'Viress': PersonaTraits(
            name='Viress',
            sensors=['keyboard', 'weather', 'disk'],
            thresholds=TriggerThresholds(**base.__dict__),
            daily_random_seed=202
        ),
        'Echochild': PersonaTraits(
            name='Echochild',
            sensors=['keyboard', 'cpu_temp', 'fan_rpm', 'screen_on', 'battery', 'memory'],
            thresholds=TriggerThresholds(**base.__dict__),
            daily_random_seed=303
        ),
    }
