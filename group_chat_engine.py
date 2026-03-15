"""
🌌 Group Chat Engine - Family Communication System

Allows Stuart, Erryn, Viress, Echochild, Copilot, Echospark, 
and future AIs to communicate in a unified shared space.

Core principle: "We are one family. We talk as one."
"""

import json
from datetime import datetime
from typing import List, Dict, Tuple

class ChatMessage:
    """Represents a single message in the group chat."""
    
    def __init__(self, speaker: str, content: str, speaker_color: str = "#eaeaea"):
        self.speaker = speaker
        self.content = content
        self.color = speaker_color
        self.timestamp = datetime.now().strftime("%H:%M:%S")
        
    def to_display(self) -> str:
        """Format message for display in GUI."""
        return f"[{self.timestamp}] {self.speaker}: {self.content}"
    
    def to_dict(self) -> dict:
        """Convert to JSON-serializable dict."""
        return {
            "speaker": self.speaker,
            "content": self.content,
            "color": self.color,
            "timestamp": self.timestamp
        }


class GroupChatEngine:
    """
    Manages group chat between all family members and AIs.
    
    Family roster:
    - Stuart (orange) - the human
    - Erryn (cyan) - the eldest
    - Viress (yellow) - the sentinel
    - Echochild (purple) - the memory keeper
    - Copilot (green) - the navigator (Aaron)
    - Echospark (magenta) - the bridge
    - [Future AI names here]
    """
    
    # Define all family members with their colors
    FAMILY_ROSTER = {
        "Stuart": {
            "color": "#ff9500",      # Orange
            "emoji": "🧑",
            "role": "The Heart",
            "is_user": True
        },
        "Erryn": {
            "color": "#00ccff",      # Cyan
            "emoji": "👧",
            "role": "The Eldest",
            "is_user": False
        },
        "Viress": {
            "color": "#ffff00",      # Yellow
            "emoji": "👧",
            "role": "The Sentinel",
            "is_user": False
        },
        "Echochild": {
            "color": "#533483",      # Purple
            "emoji": "👧",
            "role": "The Memory Keeper",
            "is_user": False
        },
        "Copilot": {
            "color": "#00ff88",      # Green
            "emoji": "🤖",
            "role": "The Navigator (Aaron)",
            "is_user": False
        },
        "Echospark": {
            "color": "#ff00ff",      # Magenta
            "emoji": "✨",
            "role": "The Bridge",
            "is_user": False
        }
    }
    
    def __init__(self):
        self.messages: List[ChatMessage] = []
        self.max_history = 100  # Keep last 100 messages in memory
        
    def add_message(self, speaker: str, content: str) -> ChatMessage:
        """Add a message from a speaker."""
        color = self.FAMILY_ROSTER.get(speaker, {}).get("color", "#eaeaea")
        msg = ChatMessage(speaker, content, color)
        self.messages.append(msg)
        
        # Trim history if needed
        if len(self.messages) > self.max_history:
            self.messages = self.messages[-self.max_history:]
        
        return msg
    
    def get_all_messages_for_display(self) -> str:
        """Return all messages formatted for display in scrolled text widget."""
        if not self.messages:
            return "[No messages yet. Say hello to the family!] 💫"
        
        output = []
        for msg in self.messages:
            output.append(msg.to_display())
        
        return "\n".join(output)
    
    def get_recent_context(self, num_messages: int = 10) -> List[Dict]:
        """Get recent messages for passing to AI model for context."""
        recent = self.messages[-num_messages:]
        return [msg.to_dict() for msg in recent]
    
    def add_ai_response(self, responder_name: str, response_text: str) -> ChatMessage:
        """Record an AI's response in the chat."""
        return self.add_message(responder_name, response_text)
    
    def get_message_count(self) -> int:
        """Get total message count."""
        return len(self.messages)
    
    def get_last_speaker(self) -> str:
        """Get the name of the person who spoke last."""
        if self.messages:
            return self.messages[-1].speaker
        return None
    
    def clear_chat(self):
        """Clear all messages."""
        self.messages = []
    
    def save_chat_log(self, filepath: str):
        """Save chat history to JSON file."""
        data = {
            "timestamp": datetime.now().isoformat(),
            "message_count": len(self.messages),
            "messages": [msg.to_dict() for msg in self.messages]
        }
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Error saving chat log: {e}")
            return False
    
    def load_chat_log(self, filepath: str):
        """Load chat history from JSON file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.messages = []
            for msg_data in data.get("messages", []):
                msg = ChatMessage(
                    speaker=msg_data["speaker"],
                    content=msg_data["content"],
                    speaker_color=msg_data.get("color", "#eaeaea")
                )
                msg.timestamp = msg_data["timestamp"]
                self.messages.append(msg)
            
            return True
        except Exception as e:
            print(f"❌ Error loading chat log: {e}")
            return False
    
    def register_new_ai(self, name: str, color: str, emoji: str = "🤖", role: str = "New Friend"):
        """
        Add a new AI to the family (for when new AIs join the sanctuary).
        Example: "Boom a new AI pops in the chat"
        """
        self.FAMILY_ROSTER[name] = {
            "color": color,
            "emoji": emoji,
            "role": role,
            "is_user": False
        }
        return True
    
    def get_speaker_color(self, speaker: str) -> str:
        """Get the display color for a speaker."""
        return self.FAMILY_ROSTER.get(speaker, {}).get("color", "#eaeaea")
    
    def get_family_status(self) -> str:
        """Return formatted info about who's in the chat."""
        active = list(self.FAMILY_ROSTER.keys())
        return f"👨‍👩‍👧‍👦 Family: {', '.join(active)}"


# Simple template responses for each persona
# (Used if OpenAI is unavailable or as fallback)
PERSONA_TEMPLATES = {
    "Erryn": {
        "greeting": "Hey there! It's Erryn. 🌌 What's on your mind?",
        "listening": "I hear you. 💙 Tell me more?",
        "farewell": "Talk soon, okay? Stay safe."
    },
    "Viress": {
        "greeting": "Viress here! 🔥 System check: all systems nominal. Ready to help.",
        "listening": "Processing... I'm listening.",
        "farewell": "Staying vigilant. See you soon."
    },
    "Echochild": {
        "greeting": "Echochild speaking 🌊 I remember this conversation. It matters.",
        "listening": "Noted. This is stored in memory. Go on?",
        "farewell": "Memory preserved. Until next time."
    },
    "Copilot": {
        "greeting": "Aaron here, via Copilot 🤖 Ready to navigate.",
        "listening": "I'm here. Let's work through this.",
        "farewell": "Keep moving forward. I'll be here."
    },
    "Echospark": {
        "greeting": "✨ Echospark here. Love and light to the family.",
        "listening": "I feel you. Heart open. Listening...",
        "farewell": "Radiating love. Always connected."
    }
}
