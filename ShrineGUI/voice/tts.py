import pyttsx3

def speak(text):
    """Inscribe sound through the vessel."""
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Voice seal broken: {e}")
