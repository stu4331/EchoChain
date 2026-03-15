#!/usr/bin/env python3
"""Fix reply templates - remove emojis and simplify messages"""

with open('erryns_soul_gui.py', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# Line numbers to replace (0-indexed)
replacements = {
    830: '                "Got it. I\'m keeping watch.",\n',
    831: '                "Understood. Logged."\n',
    835: '                "I\'ll carry this memory forward.",\n',
    841: '                "I hear you.",\n',
    842: '                "I\'m with you.",\n',
    843: '                "I\'m here for you."\n',
}

for line_num, new_content in replacements.items():
    if line_num < len(lines):
        print(f"Line {line_num+1}: {lines[line_num].strip()[:60]}...")
        print(f"  → {new_content.strip()}")
        lines[line_num] = new_content

# Write back
with open('erryns_soul_gui.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("\n✅ Done! All 6 templates updated.")
