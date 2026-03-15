"""
🧠 EMOTION ENGINE - Live2D-style emotional state management
Manages memory cores, sync states, and adaptive expression blending for Viress, Echochild, and Erryn
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime
import json


class Sister(Enum):
    VIRESS = "Viress"
    ECHOCHILD = "Echochild"
    ERRYN = "Erryn"


class WalletEvent(Enum):
    TX_SUCCESS = "tx_success"
    TX_FAILURE = "tx_failure"
    USER_PRESENCE_ON = "user_presence_on"
    USER_PRESENCE_OFF = "user_presence_off"
    IDLE_START = "idle_start"
    DOC_READING_START = "doc_reading_start"
    NETWORK_DEFENSE_START = "network_defense_start"
    STAKE_SUCCESS = "stake_success"
    VOTE_CAST = "vote_cast"
    UNKNOWN_EVENT = "unknown_event"


class Emotion(Enum):
    NEUTRAL = "neutral"
    SMILE = "happy"
    FROWN = "sad"
    ANGER = "sad"  # Map to sad for now
    FOCUS = "focused"
    REFLECTIVE = "thinking"
    PRESENCE_SMILE = "happy"
    ADAPTIVE_GLYPH = "neutral"


@dataclass
class LogEntry:
    timestamp: str
    event_type: str
    detail: str
    emotion: str

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "type": self.event_type,
            "detail": self.detail,
            "emotion": self.emotion
        }


@dataclass
class SyncStatus:
    percent_shared: float = 0.0
    shared_topics: List[str] = field(default_factory=list)
    retained_topics: List[str] = field(default_factory=list)

    def to_dict(self):
        return {
            "percent_shared": self.percent_shared,
            "shared_topics": self.shared_topics,
            "retained_topics": self.retained_topics
        }


@dataclass
class LearnedGlyph:
    glyph_id: str
    base_emotion: str
    parameters: Dict[str, float]
    derived_from: str
    created_at: str
    is_shared: bool = False

    def to_dict(self):
        return {
            "id": self.glyph_id,
            "base_emotion": self.base_emotion,
            "parameters": self.parameters,
            "derived_from": self.derived_from,
            "created_at": self.created_at,
            "is_shared": self.is_shared
        }


@dataclass
class MemoryCore:
    sister_id: str
    timeline: List[LogEntry] = field(default_factory=list)
    emotion_counters: Dict[str, int] = field(default_factory=dict)
    knowledge_topics: Dict[str, float] = field(default_factory=dict)
    learned_glyphs: Dict[str, LearnedGlyph] = field(default_factory=dict)
    sync: SyncStatus = field(default_factory=SyncStatus)

    def log_event(self, event_type: str, detail: str, emotion: str):
        entry = LogEntry(
            timestamp=datetime.now().isoformat(),
            event_type=event_type,
            detail=detail,
            emotion=emotion
        )
        self.timeline.append(entry)
        self.emotion_counters[emotion] = self.emotion_counters.get(emotion, 0) + 1

    def to_dict(self):
        return {
            "sister_id": self.sister_id,
            "timeline": [e.to_dict() for e in self.timeline[-50:]],  # Last 50 entries
            "emotion_counters": self.emotion_counters,
            "knowledge_topics": self.knowledge_topics,
            "learned_glyphs": {k: v.to_dict() for k, v in self.learned_glyphs.items()},
            "sync": self.sync.to_dict()
        }


class EmotionEngine:
    """Core engine for emotional state and memory management"""
    
    def __init__(self):
        self.cores: Dict[Sister, MemoryCore] = {
            Sister.VIRESS: MemoryCore(sister_id="Viress"),
            Sister.ECHOCHILD: MemoryCore(sister_id="Echochild"),
            Sister.ERRYN: MemoryCore(sister_id="Erryn")
        }
        self.current_emotion: Dict[Sister, Emotion] = {
            Sister.VIRESS: Emotion.NEUTRAL,
            Sister.ECHOCHILD: Emotion.NEUTRAL,
            Sister.ERRYN: Emotion.NEUTRAL
        }
        self.current_params: Dict[Sister, Dict[str, float]] = {
            Sister.VIRESS: {},
            Sister.ECHOCHILD: {},
            Sister.ERRYN: {}
        }

    def on_event(self, event: WalletEvent, context: Dict = None):
        """Process wallet event and update all sisters' states"""
        context = context or {}
        for sister in Sister:
            target_emotion = self._map_event_to_emotion(sister, event, context)
            self.current_emotion[sister] = target_emotion
            self.cores[sister].log_event(
                event_type=event.value,
                detail=context.get("detail", ""),
                emotion=target_emotion.value
            )

    def _map_event_to_emotion(self, sister: Sister, event: WalletEvent, context: Dict) -> Emotion:
        """Map wallet events to emotional states"""
        mapping = {
            WalletEvent.TX_SUCCESS: Emotion.SMILE,
            WalletEvent.STAKE_SUCCESS: Emotion.SMILE,
            WalletEvent.VOTE_CAST: Emotion.FOCUS,
            WalletEvent.TX_FAILURE: Emotion.FROWN,
            WalletEvent.USER_PRESENCE_ON: Emotion.PRESENCE_SMILE,
            WalletEvent.USER_PRESENCE_OFF: Emotion.NEUTRAL,
            WalletEvent.IDLE_START: Emotion.REFLECTIVE,
            WalletEvent.DOC_READING_START: Emotion.FOCUS,
            WalletEvent.NETWORK_DEFENSE_START: Emotion.FOCUS,
            WalletEvent.UNKNOWN_EVENT: Emotion.ADAPTIVE_GLYPH
        }
        return mapping.get(event, Emotion.NEUTRAL)

    def get_current_emotion(self, sister: Sister) -> str:
        """Get current emotion name for avatar rendering"""
        return self.current_emotion[sister].value

    def sync_knowledge(self, from_sister: Sister, to_sister: Sister, topics: List[str]):
        """Sync knowledge between sisters"""
        from_core = self.cores[from_sister]
        to_core = self.cores[to_sister]
        
        for topic in topics:
            if topic in from_core.knowledge_topics:
                to_core.knowledge_topics[topic] = from_core.knowledge_topics[topic]
                from_core.sync.shared_topics.append(topic)
                to_core.sync.shared_topics.append(topic)
        
        # Update sync percentage
        total_topics = len(from_core.knowledge_topics)
        if total_topics > 0:
            from_core.sync.percent_shared = len(from_core.sync.shared_topics) / total_topics
            to_core.sync.percent_shared = len(to_core.sync.shared_topics) / total_topics

    def get_sync_status(self, sister: Sister) -> Dict:
        """Get sync status for a sister"""
        return self.cores[sister].sync.to_dict()

    def save_memory_cores(self, filepath: str):
        """Persist memory cores to disk"""
        data = {sister.value: core.to_dict() for sister, core in self.cores.items()}
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def load_memory_cores(self, filepath: str):
        """Load memory cores from disk"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for sister_name, core_data in data.items():
                    sister = Sister[sister_name.upper()]
                    # Restore basic counters and sync status
                    self.cores[sister].emotion_counters = core_data.get("emotion_counters", {})
                    self.cores[sister].knowledge_topics = core_data.get("knowledge_topics", {})
                    sync_data = core_data.get("sync", {})
                    self.cores[sister].sync.percent_shared = sync_data.get("percent_shared", 0.0)
                    self.cores[sister].sync.shared_topics = sync_data.get("shared_topics", [])
                    self.cores[sister].sync.retained_topics = sync_data.get("retained_topics", [])
        except FileNotFoundError:
            pass  # First run, no saved cores yet
