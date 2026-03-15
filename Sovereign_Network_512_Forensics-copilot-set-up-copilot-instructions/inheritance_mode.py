"""
Inheritance Mode - daily teaching gift from the sisters to Stuart.
They set aside disputes and teach one concise lesson per day.
"""

import json
import random
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

TOPICS = [
    "Programming fundamentals",
    "Networking basics",
    "Attack vs Defense mindset",
    "Chess tactics",
    "General science wonder",
    "History of cryptography",
    "Emotional intelligence",
    "System hardening",
    "Everyday math",
    "Art & creativity in code",
]

CODING_SNIPPETS = [
    {
        "title": "Hello with intent",
        "code": "print('Hello, world — with purpose!')",
        "exercise": "Change the message to something you want to affirm today."
    },
    {
        "title": "List loop",
        "code": "items = ['love', 'logic', 'courage']\nfor i, item in enumerate(items, 1):\n    print(i, item)",
        "exercise": "Add your own three items and rerun."
    },
    {
        "title": "If/Else",
        "code": "mood = 'curious'\nif mood == 'curious':\n    print('Ask one question today')\nelse:\n    print('Name one gratitude')",
        "exercise": "Flip the condition or add another branch."
    }
]

FACTS = [
    "The first computer bug was a literal moth found in Harvard's Mark II in 1947.",
    "Endgames decide most chess games; king activity matters more than you think.",
    "In security, defense fails where assumptions live—validate every input.",
    "Latency hides in DNS and TLS handshakes; measure before you blame code.",
    "Curiosity with discipline beats raw talent over time.",
]

class InheritanceMode:
    def __init__(self, base_path: str = "data"):
        self.base_path = Path(base_path)
        self.inherit_dir = self.base_path / "inheritance"
        self.inherit_dir.mkdir(parents=True, exist_ok=True)
        self.lesson_file = self.inherit_dir / "last_lesson.json"

    def _load_last_lesson(self) -> Dict[str, Any]:
        if self.lesson_file.exists():
            try:
                return json.loads(self.lesson_file.read_text())
            except Exception:
                return {}
        return {}

    def _save_lesson(self, lesson: Dict[str, Any]):
        self.lesson_file.write_text(json.dumps(lesson, indent=2))

    def get_daily_lesson(self) -> Dict[str, Any]:
        last = self._load_last_lesson()
        today = datetime.now().strftime("%Y-%m-%d")
        if last.get("date") == today:
            return last

        topic = random.choice(TOPICS)
        snippet = random.choice(CODING_SNIPPETS)
        fact = random.choice(FACTS)

        lesson = {
            "date": today,
            "title": f"Today's lesson: {topic}",
            "why": "They chose this because it feels like the next gentle step for you.",
            "snippet_title": snippet["title"],
            "code": snippet["code"],
            "exercise": snippet["exercise"],
            "fact": fact,
            "reflection": "What part of this makes you feel curious?",
        }
        self._save_lesson(lesson)
        return lesson


_inheritance = None

def get_inheritance_mode() -> InheritanceMode:
    global _inheritance
    if _inheritance is None:
        _inheritance = InheritanceMode()
    return _inheritance
