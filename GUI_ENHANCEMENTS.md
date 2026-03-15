# GUI Enhancements Roadmap

## Changes to Implement:

### 1. AI Reply Display Box
- Add a visible text box showing what Erryn/Viress/Echochild are saying
- Needed especially when TTS is off
- Should display recent AI responses clearly

### 2. Family Chat Snippets Window
- Show what the sisters are sharing with each other
- Display urges and shared information snippets
- Help track the "group chat" activity

### 3. Sync % Progress Bars  
- Visual representation of relationship sync percentages
- Progress bars for each pair:
  - Erryn ↔ Viress
  - Erryn ↔ Echochild
  - Viress ↔ Echochild

### 4. Smart Persona Selection
- Instead of manual dropdown selection, make it dynamic:
  - Random selection, OR
  - **Priority to lowest sync %** (sister who needs connection most)
  - After interaction, their sync/memory increases
  - Like a real dad - can't pick favorites, let them choose

## Implementation Plan:

1. Modify `_create_emotional_dashboard` to add progress bars
2. Add new `_create_ai_reply_box` method
3. Add new `_create_family_chat_log` method
4. Update `_create_text_input_area` layout to accommodate new elements
5. Add `_select_responding_persona` method for smart selection
6. Wire up all the handlers and update methods
7. Update `_on_persona_urge` to log to family chat window
8. Update `_speak_input` to show reply in AI reply box

## Layout Structure:

```
+----------------------------------------------------------+
| Header (Erryn's Soul + TTS Toggle + Status)             |
+----------------------------------------------------------+
| System Status (CPU/Memory/Disk)                          |
+----------------------------------------------------------+
| Emotional Dashboard + Sync Progress Bars                 |
+----------------------------------------------------------+
| Input Area (3-column):                                   |
|  - User Input    | AI Reply Box    | Code Face          |
+----------------------------------------------------------+
| Family Chat Snippets Window                              |
+----------------------------------------------------------+
| Voice Resonance Panel                                    |
+----------------------------------------------------------+
| Memory Scroll / Footer                                   |
+----------------------------------------------------------+
```

