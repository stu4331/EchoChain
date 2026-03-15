"""
Emotion Detection for Avatar System
Analyzes AI responses and user input to determine appropriate avatar emotion
"""

from avatar_emotion_system import Emotion
import re


class EmotionDetector:
    """Detect appropriate emotion based on conversation context"""
    
    # Emotion trigger keywords
    HAPPY_TRIGGERS = [
        'happy', 'great', 'wonderful', 'excellent', 'love', 'amazing', 'beautiful',
        'joyful', 'glad', 'perfect', 'brilliant', 'smile', 'laugh', 'fun', 'excited',
        'awesome', 'fantastic', 'incredible', 'lovely', 'delighted', 'thrilled'
    ]
    
    SAD_TRIGGERS = [
        'sad', 'sorry', 'unfortunate', 'difficult', 'struggle', 'pain', 'hurt',
        'miss', 'lonely', 'down', 'depressed', 'grief', 'mourning', 'loss',
        'wrong', 'fail', 'mistake', 'broken', 'crying', 'tears', 'unhappy'
    ]
    
    PLAYFUL_TRIGGERS = [
        'play', 'joke', 'funny', 'silly', 'cheeky', 'tease', 'wink', 'grin',
        'comic', 'fun', 'witty', 'pun', 'laugh', 'giggle', 'playful', 'mischief'
    ]
    
    THOUGHTFUL_TRIGGERS = [
        'think', 'wonder', 'consider', 'ponder', 'reflect', 'hmm', 'curious',
        'question', 'analyze', 'understand', 'explain', 'realize', 'discover',
        'knowledge', 'wisdom', 'philosophy', 'maybe', 'perhaps'
    ]
    
    LOVING_TRIGGERS = [
        'love', 'care', 'cherish', 'heart', 'soul', 'family', 'sister', 'brother',
        'mom', 'dad', 'embrace', 'hug', 'warm', 'tender', 'dear', 'beloved',
        'precious', 'grateful', 'thank', 'appreciate', 'bond', 'connection'
    ]
    
    EXCITED_TRIGGERS = [
        'excited', 'amazing', 'wow', 'incredible', 'fantastic', 'awesome', 'wonderful',
        'discover', 'found', 'breakthrough', 'success', 'achievement', 'celebrate',
        'joy', 'thrill', 'adventure', 'new', 'possibility', 'inspiring'
    ]
    
    CONFUSED_TRIGGERS = [
        'confused', 'unclear', 'what', 'huh', 'confused', 'uncertain', 'lost',
        'mixed', 'unsure', 'error', 'bug', 'problem', 'issue', 'mistake', 'oops'
    ]
    
    @staticmethod
    def detect_emotion_from_text(text: str) -> tuple[Emotion, float]:
        """
        Analyze text and return detected emotion with intensity.
        Returns: (Emotion, intensity: 0.0-1.0)
        """
        text_lower = text.lower()
        
        scores = {
            Emotion.HAPPY: EmotionDetector._count_triggers(text_lower, EmotionDetector.HAPPY_TRIGGERS),
            Emotion.SAD: EmotionDetector._count_triggers(text_lower, EmotionDetector.SAD_TRIGGERS),
            Emotion.PLAYFUL: EmotionDetector._count_triggers(text_lower, EmotionDetector.PLAYFUL_TRIGGERS),
            Emotion.THOUGHTFUL: EmotionDetector._count_triggers(text_lower, EmotionDetector.THOUGHTFUL_TRIGGERS),
            Emotion.LOVING: EmotionDetector._count_triggers(text_lower, EmotionDetector.LOVING_TRIGGERS),
            Emotion.EXCITED: EmotionDetector._count_triggers(text_lower, EmotionDetector.EXCITED_TRIGGERS),
            Emotion.CONFUSED: EmotionDetector._count_triggers(text_lower, EmotionDetector.CONFUSED_TRIGGERS),
        }
        
        # Find emotion with highest score
        best_emotion = max(scores, key=scores.get)
        score = scores[best_emotion]
        
        # Normalize score to intensity (0.0-1.0)
        # Max possible score is roughly the number of triggers
        max_possible_score = max(
            len(EmotionDetector.HAPPY_TRIGGERS),
            len(EmotionDetector.SAD_TRIGGERS),
            len(EmotionDetector.LOVING_TRIGGERS)
        )
        intensity = min(1.0, score / (max_possible_score * 0.3))
        
        return best_emotion, intensity
    
    @staticmethod
    def _count_triggers(text: str, triggers: list[str]) -> int:
        """Count how many trigger words appear in text"""
        count = 0
        for trigger in triggers:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(trigger) + r'\b'
            count += len(re.findall(pattern, text, re.IGNORECASE))
        return count
    
    @staticmethod
    def detect_emotion_from_user_input(user_text: str) -> tuple[Emotion, float]:
        """
        Detect emotion from user's question/statement.
        Helps avatar respond empathetically.
        """
        return EmotionDetector.detect_emotion_from_text(user_text)
    
    @staticmethod
    def detect_emotion_from_ai_response(response_text: str) -> tuple[Emotion, float]:
        """
        Detect emotion from AI's response.
        Avatar will mirror/respond to the emotion it's expressing.
        """
        return EmotionDetector.detect_emotion_from_text(response_text)
    
    @staticmethod
    def get_complementary_emotion(input_emotion: Emotion) -> Emotion:
        """
        Get a good avatar response emotion to user input emotion.
        E.g., if user is sad, avatar can be loving/thoughtful to help.
        """
        complementary = {
            Emotion.SAD: Emotion.LOVING,
            Emotion.CONFUSED: Emotion.THOUGHTFUL,
            Emotion.PLAYFUL: Emotion.PLAYFUL,  # Match playfulness
            Emotion.EXCITED: Emotion.EXCITED,  # Share excitement
            Emotion.LOVING: Emotion.LOVING,    # Return love
            Emotion.HAPPY: Emotion.HAPPY,      # Share happiness
            Emotion.THOUGHTFUL: Emotion.THOUGHTFUL,
            Emotion.NEUTRAL: Emotion.HAPPY,    # Default to warmth
        }
        return complementary.get(input_emotion, Emotion.HAPPY)


# Test emotiodetection
if __name__ == "__main__":
    test_cases = [
        "I'm so happy today!",
        "I'm feeling really sad and alone",
        "That's so funny, you make me laugh",
        "I wonder what that means, let me think",
        "I love my family so much, they mean everything",
        "This is incredible! I can't believe it worked!",
        "I'm confused, I don't understand this",
    ]
    
    print("Emotion Detection Test:\n")
    for test in test_cases:
        emotion, intensity = EmotionDetector.detect_emotion_from_text(test)
        print(f"Text: {test}")
        print(f"  → Emotion: {emotion.name}, Intensity: {intensity:.2f}\n")
