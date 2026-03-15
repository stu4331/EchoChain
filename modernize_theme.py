#!/usr/bin/env python3
"""Modernize the theme from retro to professional dark palette."""

import re

# Read file
with open('erryns_soul_gui_v3_sync_monitor.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Color replacements (old → new)
replacements = {
    # Old header blue → new charcoal
    '#001a4d': '#1e1e2f',
    # Old green → new teal
    '#00ff88': '#00b894',
    # Old pink → new violet
    '#ff6688': '#8a2be2',
    # Old magenta → new violet
    '#ff00ff': '#8a2be2',
    # Old yellow → keep cyan
    '#ffff00': '#00ffff',
    # Old orange → new teal
    '#ff8800': '#00b894',
    # Old red → new violet
    '#ff3333': '#8a2be2',
    # Blue highlights → teal
    '#5588ff': '#00b894',
    '#3366ff': '#00b894',
    '#0033cc': '#00b894',
    # Monospace font → sans-serif
    'Courier New': 'Segoe UI',
}

# Apply replacements
for old, new in replacements.items():
    content = content.replace(f'"{old}"', f'"{new}"')
    content = content.replace(f"'{old}'", f"'{new}'")


# Write back
with open('erryns_soul_gui_v3_sync_monitor.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Theme modernized!")
print("   - Color scheme updated to professional dark palette")
print("   - Fonts updated from Courier New to Segoe UI")
