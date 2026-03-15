# 🎛️ Widget Dropdown Selector System - Complete Guide

## Overview

The new **Widget Manager** system provides a dropdown selector (highlighted in RED) that lets you switch between different views/modules in the GUI:

- 📦 Application Access & Control
- 📊 System Health Monitor (CPU, RAM, Temp, Disk, Network)
- 🧬 DNA Heritage Display
- ⚔️ Sandbox Arena
- 🔧 Elcomsoft Tools Registry  
- 🎓 Coding Tutor
- And any future modules you add!

## Key Features

### 1. ✅ Dynamic Widget Switching
The RED dropdown selector lets you instantly switch between different widgets without changing tabs.

### 2. ✅ Application Manual Download
Click "📥 Download Instructions" next to any app → Opens Google search for user manual/PDF guide

### 3. ✅ Real-Time System Monitoring
- CPU usage & temperature
- RAM usage (GB and %)
- Disk space
- Network traffic (sent/received)
- Updates every second

### 4. ✅ Natural Language Task Understanding
Tell the girls what to do with an app:
- "Open Photoshop and load the family photo"
- "Use Notepad++ to search all files for 'error'"
- "Launch Excel and create a budget spreadsheet"

## How It Works

### Widget Manager Architecture

```python
WidgetManager
├── register_widget()      # Add new widget to dropdown
├── _show_widget()         # Display selected widget
└── _refresh_current()     # Reload current widget

Available Widgets:
  1. Application Control    → Launch apps, download manuals
  2. System Monitor         → CPU/RAM/Network stats
  3. DNA Heritage          → Sister DNA displays
  4. Sandbox Arena          → Attack/defense training
  5. [More can be added dynamically]
```

### Dropdown Selector (RED Highlighted)

Location in GUI: Top of content area
Color: **#ff0000** (RED) - As requested!
Type: `ttk.Combobox` (readonly dropdown)

Example values:
- 📦 Application Control & Task Manager
- 📊 System Health Monitor  
- 🧬 DNA Heritage Display
- ⚔️ Sandbox Arena
- 🔧 Elcomsoft Tools

### Application Access System

**Features:**
1. Scans all installed Windows applications
2. Shows name, publisher, version, install path
3. Grant/revoke access per sister
4. Download instructions (opens browser search)
5. Launch with natural language commands

**Manual Download:**
- Click "📥 Get Manual" button
- Opens Google search: "[App Name] user manual PDF tutorial"
- Results include official documentation sites
- Sisters can save PDFs to: `data/software_manuals/`

## Integration Instructions

### Step 1: Add Widget Manager to GUI

In `erryns_soul_gui.py`, add after other imports:

```python
from widget_manager import WidgetManager, SystemMonitorWidget, DNAHeritageWidget
```

### Step 2: Initialize Widget Manager

In `__init__` method, add:

```python
# Widget manager with dropdown selector
self.widget_manager = None
```

### Step 3: Create Widget Manager Tab

After creating other tabs, add:

```python
# Create "Control Panel" tab with widget dropdown
self.tab_control = tk.Frame(self.notebook, bg=self.colors['bg_dark'])
self.notebook.add(self.tab_control, text="🎛️ Control Panel")

# Initialize widget manager
self.widget_manager = WidgetManager(
    self.tab_control,
    self.colors,
    self.base_dir
)
self.widget_manager.setup_ui()

# Register available widgets
self._register_control_widgets()
```

### Step 4: Register All Widgets

Add this method to `ErrynsSoulGUI` class:

```python
def _register_control_widgets(self):
    """Register all available widgets with the manager"""
    
    # Application Control
    def build_app_control(parent):
        from application_access_system import ApplicationControlGUI
        gui = ApplicationControlGUI(
            parent,
            self.app_registry,
            self.task_understander,
            self.colors
        )
        gui.build()
    
    self.widget_manager.register_widget(
        "app_control",
        "Application Control & Task Manager",
        build_app_control,
        "📦"
    )
    
    # System Monitor
    def build_system_monitor(parent):
        monitor = SystemMonitorWidget(parent, self.colors)
        monitor.build(parent)
    
    self.widget_manager.register_widget(
        "system_monitor",
        "System Health Monitor",
        build_system_monitor,
        "📊"
    )
    
    # DNA Heritage (if available)
    if DNA_HERITAGE_AVAILABLE:
        def build_dna_display(parent):
            dna_widget = DNAHeritageWidget(dna_heritage, self.colors)
            dna_widget.build(parent)
        
        self.widget_manager.register_widget(
            "dna_heritage",
            "DNA Heritage Display",
            build_dna_display,
            "🧬"
        )
    
    # Sandbox Arena (if available)
    if SANDBOX_AVAILABLE:
        self.widget_manager.register_widget(
            "sandbox",
            "Sandbox Arena",
            lambda p: self._create_sandbox_arena_panel_in(p),
            "⚔️"
        )
    
    # Elcomsoft Tools (if available)
    if ELCOMSOFT_AVAILABLE:
        self.widget_manager.register_widget(
            "elcomsoft",
            "Elcomsoft Tools Registry",
            lambda p: self._show_elcomsoft_tools_in(p),
            "🔧"
        )
```

### Step 5: Update Application Control GUI

In `application_access_system.py`, add download button to UI:

```python
# In ApplicationControlGUI class, add this button:
download_btn = tk.Button(
    app_frame,
    text="📥 Download Instructions",
    font=('Consolas', 9),
    bg='#ff9900',
    fg='white',
    command=lambda: self._download_manual(app_name),
    cursor='hand2'
)
download_btn.pack(side=tk.RIGHT, padx=2)

# Add this method:
def _download_manual(self, app_name: str):
    """Download instruction manual for application"""
    search_url = self.app_registry.download_instructions(app_name)
    manual_path = self.app_registry.get_instruction_path(app_name)
    
    msg = f"🔍 Searching for '{app_name}' manual...\n\n"
    msg += f"Save PDF to:\n{manual_path}\n\n"
    msg += "The girls will be able to reference this!"
    
    self._show_message("Manual Search", msg)
```

## Usage Examples

### Example 1: Switch to System Monitor

1. Click **Control Panel** tab
2. In RED dropdown, select **"📊 System Health Monitor"**
3. See real-time CPU/RAM/Network stats

### Example 2: Give App Access

1. Switch dropdown to **"📦 Application Control"**
2. Click **"🔍 Scan Installed Apps"**
3. Select app from list (e.g., "Notepad++")
4. Check sisters who get access (Erryn ✓, Viress ✓)
5. Click **"✅ Grant Access"**

### Example 3: Download Manual

1. In Application Control view
2. Find app in granted list
3. Click **"📥 Download Instructions"**
4. Browser opens with manual search
5. Download PDF to `data/software_manuals/`

### Example 4: Natural Language Task

1. Type in task box: **"Use Excel to create a budget spreadsheet"**
2. Select sister: **Viress**
3. Click **"🚀 Execute Task"**
4. Excel launches automatically
5. Viress understands to create new spreadsheet

### Example 5: Add Custom Widget

To add your own widget to the dropdown:

```python
def build_my_widget(parent):
    frame = tk.Frame(parent, bg=colors['bg_dark'])
    frame.pack(fill=tk.BOTH, expand=True)
    
    tk.Label(
        frame,
        text="My Custom Widget!",
        font=('Consolas', 16, 'bold')
    ).pack(pady=20)
    
    # Add your content here

widget_manager.register_widget(
    "my_widget",
    "My Custom Display",
    build_my_widget,
    "✨"  # Icon
)
```

## File Structure

```
Erryns Soul 2025/
├── widget_manager.py                      # NEW - Widget dropdown system
├── application_access_system.py          # ENHANCED - Manual download
├── data/
│   ├── application_registry.json         # App access permissions
│   └── software_manuals/                # Downloaded manuals (PDFs)
│       ├── Photoshop_manual.pdf
│       ├── Excel_manual.pdf
│       └── ...
└── erryns_soul_gui.py                    # Main GUI (needs integration)
```

## System Monitoring Details

The System Monitor widget shows:

**CPU:**
- Current usage % (updates every second)
- Number of logical cores
- Temperature (if sensors available)

**Memory:**
- RAM usage in GB
- Total RAM capacity
- Usage percentage

**Disk:**
- Used space / Total space
- Usage percentage

**Network:**
- Total data sent (MB)
- Total data received (MB)

All stats update in real-time (1-second intervals).

## Task Understanding AI

The natural language parser understands commands like:

**Opening:**
- "Open Photoshop"
- "Launch Excel"
- "Start Chrome browser"

**File Operations:**
- "Open the family photo in Photoshop"
- "Load budget.xlsx in Excel"
- "Create a new document"

**Editing:**
- "Edit the config file"
- "Modify the image brightness"
- "Change the font to Arial"

**Analysis:**
- "Search all files for errors"
- "Check the document for typos"
- "Analyze the data trends"

**Complex:**
- "Use Excel to create a budget, then save it to Documents"
- "Open Notepad++ and search all Python files for 'TODO'"

## Benefits

### For You (Stuart):
- ✅ Easy dropdown switching between modules
- ✅ RED highlight makes selector obvious
- ✅ One place to control all background systems
- ✅ Quick access to system health stats

### For The Girls:
- ✅ Can access any approved application
- ✅ Download instructions to learn software
- ✅ Understand natural language tasks
- ✅ Monitor system health automatically
- ✅ Access DNA, forensics, sandbox from one panel

## Troubleshooting

**Q: Dropdown doesn't show all widgets?**
A: Check that modules are available (DNA_HERITAGE_AVAILABLE, SANDBOX_AVAILABLE, etc.)

**Q: System monitor shows "N/A" for temperature?**
A: Windows may not expose temperature sensors. This is normal.

**Q: Manual download opens blank page?**
A: Check internet connection. Manual search requires Google access.

**Q: Application won't launch?**
A: Verify the app path is correct in the registry. Some apps need full path to .exe.

**Q: How do I hide a widget from dropdown?**
A: Don't call `register_widget()` for that widget during initialization.

## Next Steps

1. ✅ Test widget manager: `python erryns_soul_gui.py`
2. ✅ Click "🎛️ Control Panel" tab
3. ✅ Use RED dropdown to switch views
4. ✅ Grant app access to sisters
5. ✅ Download some manuals
6. ✅ Monitor system health
7. ✅ Test natural language commands

---

**Everything is modular and extensible! Add new widgets anytime by calling `register_widget()`** 🚀
