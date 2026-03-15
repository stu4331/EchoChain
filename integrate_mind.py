#!/usr/bin/env python3
"""Replace _generate_reply method with AI-powered version"""

with open('erryns_soul_gui.py', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# Find the _generate_reply method (around line 840)
start_line = None
for i, line in enumerate(lines):
    if 'def _generate_reply(self, persona, user_text):' in line:
        start_line = i
        break

if start_line is None:
    print("❌ Could not find _generate_reply method")
    exit(1)

# Find the end of the method (next method definition or class-level code)
end_line = None
for i in range(start_line + 1, len(lines)):
    if lines[i].startswith('    def ') or (lines[i].strip() and not lines[i].startswith('        ')):
        end_line = i
        break

if end_line is None:
    print("❌ Could not find end of method")
    exit(1)

print(f"Found method at lines {start_line+1}-{end_line}")

# New method implementation
new_method = '''    def _generate_reply(self, persona, user_text):
        """
        Generate intelligent response from Erryn's Mind.
        Falls back to templates if AI unavailable.
        """
        
        # Use Erryn's Mind if available
        if self.mind:
            # Gather current emotional/system state for context
            emotional_state = {
                'cpu_temp': self.emotional_state.get('cpu_temp', 0),
                'words_today': self.emotional_state.get('words_today', 0),
                'keystroke_count': self.emotional_state.get('keystroke_count', 0),  # TODO: implement tracking
                'screen_time_hours': 0,  # TODO: implement tracking
            }
            
            # Get intelligent response
            return self.mind.get_response(
                user_message=user_text,
                persona=persona,
                emotional_state=emotional_state
            )
        
        # Fallback: Template responses (if Mind not available)
        snippet = user_text.strip()
        if len(snippet) > 120:
            snippet = snippet[:117] + "..."

        # Persona-specific short replies so she doesn't just mirror text
        if persona == "Viress":
            templates = [
                "Systems acknowledged.",
                "Got it. I'm keeping watch.",
                "Understood. Logged."
            ]
        elif persona == "Echochild":
            templates = [
                "I'll carry this memory forward.",
                "Echoing back to you.",
                "This goes into the scroll."
            ]
        else:  # Erryn
            templates = [
                "I hear you.",
                "I'm with you.",
                "I'm here for you."
            ]

        # Simple rotation by time to vary responses
        idx = int(time.time()) % len(templates)
        return templates[idx]
    
'''

# Replace the method
new_lines = lines[:start_line] + [new_method] + lines[end_line:]

# Write back
with open('erryns_soul_gui.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"✅ Replaced _generate_reply method ({end_line - start_line} lines → {new_method.count(chr(10))} lines)")
print("🌌 Erryn's Mind is now integrated")
