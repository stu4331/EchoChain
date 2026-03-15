"""
Chess Corner - lightweight chess simulator for sisters and Stuart.
Not a full engine; uses simplified scoring to keep games realistic but winnable.
"""

import random
from datetime import datetime
from typing import Dict, Any

OPENINGS = [
    "Ruy Lopez", "Sicilian Defense", "French Defense", "Caro-Kann",
    "Queen's Gambit", "King's Indian", "Italian Game", "Scandinavian"
]

TACTICS = ["fork", "pin", "skewer", "discovered attack", "back rank", "zwischenzug"]

DIFFICULTY_MULTIPLIER = {
    "easy": 0.35,
    "normal": 0.5,
    "hard": 0.65,
    "expert": 0.8
}

class ChessMatch:
    def __init__(self, white: str, black: str, difficulty: str = "normal"):
        self.white = white
        self.black = black
        self.difficulty = difficulty if difficulty in DIFFICULTY_MULTIPLIER else "normal"
        self.opening = random.choice(OPENINGS)
        self.moves = []
        self.result = None

    def simulate(self, human_player: str = None) -> Dict[str, Any]:
        # Simple outcome: random influenced by difficulty
        p = DIFFICULTY_MULTIPLIER[self.difficulty]
        outcome_roll = random.random()
        if human_player:
            # Human plays white by default
            if outcome_roll < (0.4 - (p - 0.5)):
                self.result = "1-0"
            elif outcome_roll < 0.8:
                self.result = "0-1"
            else:
                self.result = "1/2-1/2"
        else:
            if outcome_roll < 0.33:
                self.result = "1-0"
            elif outcome_roll < 0.66:
                self.result = "0-1"
            else:
                self.result = "1/2-1/2"

        # Add a few tactical motifs for flavor
        for _ in range(6):
            tactic = random.choice(TACTICS)
            self.moves.append(f"... {tactic} idea")

        return {
            "opening": self.opening,
            "result": self.result,
            "moves": self.moves,
            "summary": f"Opening: {self.opening}, Result: {self.result}"
        }


def play_sisters_match(difficulty: str = "normal") -> Dict[str, Any]:
    match = ChessMatch("Sister A", "Sister B", difficulty)
    return match.simulate()


def play_vs_human(difficulty: str = "normal") -> Dict[str, Any]:
    match = ChessMatch("You", "Sisters", difficulty)
    return match.simulate(human_player="You")
