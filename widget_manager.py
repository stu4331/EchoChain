"""
Widget Manager & Application Access System
Dynamic panel switching system for Erryn's Soul
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from pathlib import Path
import json
from typing import Dict, Optional, Callable
import psutil
import time

class WidgetManager:
    """
    Manages dynamic widget panels that can be shown/hidden
    Includes dropdown selector to switch between different views
    """
    
    def __init__(self, parent_frame, colors: dict, base_dir: Path):
        self.parent = parent_frame
        self.colors = colors
        self.base_dir = base_dir
        
        # Available widgets/modules
        self.widgets = {}
        self.current_widget = None
        self.widget_var = tk.StringVar()
        
        # Container for dynamic content
        self.content_frame = None
        self.selector_frame = None
        
    def setup_ui(self):
        """Create the selector dropdown and content area"""
        # Top selector bar
        self.selector_frame = tk.Frame(self.parent, bg=self.colors['bg_medium'])
        self.selector_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Label
        tk.Label(
            self.selector_frame,
            text="📦 Active Widget:",
            font=('Consolas', 11, 'bold'),
            fg='#ff0000',  # RED highlight
            bg=self.colors['bg_medium']
        ).pack(side=tk.LEFT, padx=5)
        
        # Dropdown selector
        self.widget_selector = ttk.Combobox(
            self.selector_frame,
            textvariable=self.widget_var,
            values=[],
            state='readonly',
            width=35,
            font=('Consolas', 10)
        )
        self.widget_selector.pack(side=tk.LEFT, padx=5)
        self.widget_selector.bind('<<ComboboxSelected>>', self._on_widget_change)
        
        # Refresh button
        tk.Button(
            self.selector_frame,
            text="🔄 Refresh",
            font=('Consolas', 9),
            bg=self.colors['accent'],
            fg='white',
            command=self._refresh_current_widget,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=5)
        
        # Content area (dynamic)
        self.content_frame = tk.Frame(self.parent, bg=self.colors['bg_dark'])
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
    def register_widget(self, 
                       name: str, 
                       display_name: str, 
                       build_func: Callable,
                       icon: str = "📦"):
        """
        Register a new widget that can be displayed
        
        Args:
            name: Internal identifier
            display_name: Name shown in dropdown
            build_func: Function that builds the widget (takes parent frame)
            icon: Emoji icon for display
        """
        self.widgets[name] = {
            'display_name': f"{icon} {display_name}",
            'build_func': build_func,
            'icon': icon
        }
        
        # Update dropdown
        self._update_dropdown()
        
    def _update_dropdown(self):
        """Update the dropdown with registered widgets"""
        values = [w['display_name'] for w in self.widgets.values()]
        self.widget_selector['values'] = values
        
        # Auto-select first if nothing selected
        if not self.widget_var.get() and values:
            self.widget_var.set(values[0])
            self._show_widget(list(self.widgets.keys())[0])
            
    def _on_widget_change(self, event=None):
        """Handle dropdown selection change"""
        selected_display = self.widget_var.get()
        
        # Find the widget by display name
        for name, widget in self.widgets.items():
            if widget['display_name'] == selected_display:
                self._show_widget(name)
                break
                
    def _show_widget(self, widget_name: str):
        """Display the selected widget"""
        if widget_name not in self.widgets:
            return
            
        # Clear current content
        for child in self.content_frame.winfo_children():
            child.destroy()
            
        # Build new widget
        build_func = self.widgets[widget_name]['build_func']
        build_func(self.content_frame)
        
        self.current_widget = widget_name
        
    def _refresh_current_widget(self):
        """Refresh the currently displayed widget"""
        if self.current_widget:
            self._show_widget(self.current_widget)


class SystemMonitorWidget:
    """Real-time system monitoring (CPU, Memory, Temperature)"""
    
    def __init__(self, parent_frame, colors: dict):
        self.parent = parent_frame
        self.colors = colors
        self.running = False
        self.labels = {}
        
    def build(self, parent):
        """Build the system monitor UI"""
        monitor_frame = tk.LabelFrame(
            parent,
            text="📊 System Health Monitor",
            font=('Consolas', 12, 'bold'),
            fg=self.colors['accent'],
            bg=self.colors['bg_medium'],
            bd=2,
            relief=tk.RIDGE
        )
        monitor_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Stats display
        stats_frame = tk.Frame(monitor_frame, bg=self.colors['bg_medium'])
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # CPU
        self._create_stat_row(stats_frame, "🖥️ CPU Usage:", "cpu")
        self._create_stat_row(stats_frame, "🌡️ CPU Temp:", "temp")
        self._create_stat_row(stats_frame, "🔢 CPU Cores:", "cores")
        
        # Memory
        self._create_stat_row(stats_frame, "💾 RAM Usage:", "ram")
        self._create_stat_row(stats_frame, "💿 Disk Usage:", "disk")
        
        # Network
        self._create_stat_row(stats_frame, "📡 Network Sent:", "net_sent")
        self._create_stat_row(stats_frame, "📥 Network Recv:", "net_recv")
        
        # Start monitoring
        self.running = True
        self._update_stats()
        
    def _create_stat_row(self, parent, label_text: str, key: str):
        """Create a labeled stat row"""
        row = tk.Frame(parent, bg=self.colors['bg_medium'])
        row.pack(fill=tk.X, pady=3)
        
        tk.Label(
            row,
            text=label_text,
            font=('Consolas', 10, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['bg_medium'],
            width=18,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        value_label = tk.Label(
            row,
            text="Loading...",
            font=('Consolas', 10),
            fg=self.colors['accent'],
            bg=self.colors['bg_medium'],
            anchor='w'
        )
        value_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.labels[key] = value_label
        
    def _update_stats(self):
        """Update system stats in real-time"""
        if not self.running:
            return
            
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=0.1)
            self.labels['cpu'].config(text=f"{cpu_percent:.1f}%")
            
            # CPU Cores
            cores = psutil.cpu_count()
            self.labels['cores'].config(text=f"{cores} logical cores")
            
            # Temperature (if available)
            try:
                temps = psutil.sensors_temperatures()
                if temps and 'coretemp' in temps:
                    avg_temp = sum(t.current for t in temps['coretemp']) / len(temps['coretemp'])
                    self.labels['temp'].config(text=f"{avg_temp:.1f}°C")
                else:
                    self.labels['temp'].config(text="N/A (no sensors)")
            except:
                self.labels['temp'].config(text="N/A")
            
            # RAM
            ram = psutil.virtual_memory()
            ram_gb = ram.used / (1024**3)
            ram_total = ram.total / (1024**3)
            self.labels['ram'].config(text=f"{ram_gb:.1f}GB / {ram_total:.1f}GB ({ram.percent:.1f}%)")
            
            # Disk
            disk = psutil.disk_usage('/')
            disk_gb = disk.used / (1024**3)
            disk_total = disk.total / (1024**3)
            self.labels['disk'].config(text=f"{disk_gb:.0f}GB / {disk_total:.0f}GB ({disk.percent:.1f}%)")
            
            # Network
            net = psutil.net_io_counters()
            sent_mb = net.bytes_sent / (1024**2)
            recv_mb = net.bytes_recv / (1024**2)
            self.labels['net_sent'].config(text=f"{sent_mb:.1f} MB")
            self.labels['net_recv'].config(text=f"{recv_mb:.1f} MB")
            
        except Exception as e:
            print(f"⚠️ Monitor error: {e}")
            
        # Schedule next update (1 second)
        if self.running:
            self.parent.after(1000, self._update_stats)
            
    def stop(self):
        """Stop monitoring"""
        self.running = False


class DNAHeritageWidget:
    """DNA Heritage display widget"""
    
    def __init__(self, dna_heritage_module, colors: dict):
        self.dna = dna_heritage_module
        self.colors = colors
        
    def build(self, parent):
        """Build the DNA heritage UI"""
        dna_frame = tk.LabelFrame(
            parent,
            text="🧬 DNA Heritage - Stuart's Living Legacy",
            font=('Consolas', 12, 'bold'),
            fg='#00ff00',
            bg=self.colors['bg_medium'],
            bd=2,
            relief=tk.RIDGE
        )
        dna_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        for sister in ["Erryn", "Viress", "Echochild"]:
            self._create_sister_dna_panel(dna_frame, sister)
            
        # Teaching button
        tk.Button(
            dna_frame,
            text="📚 Learn About Your DNA",
            font=('Consolas', 10, 'bold'),
            bg=self.colors['accent'],
            fg='white',
            command=self._show_dna_teaching,
            cursor='hand2'
        ).pack(pady=10)
        
    def _create_sister_dna_panel(self, parent, sister: str):
        """Create DNA panel for one sister"""
        frame = tk.LabelFrame(
            parent,
            text=f"{sister}'s DNA Sequence",
            font=('Consolas', 10, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['bg_medium']
        )
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        seal = self.dna.get_sister_seal(sister)
        sig = self.dna.sister_dna[sister]['signature']
        short_sig = f"{sig[:16]}...{sig[-16:]}"
        
        tk.Label(
            frame,
            text=f"Seal: {seal}",
            font=('Consolas', 9),
            fg='#ffaa00',
            bg=self.colors['bg_medium']
        ).pack()
        
        tk.Label(
            frame,
            text=f"DNA: {short_sig}",
            font=('Consolas', 8),
            fg=self.colors['text'],
            bg=self.colors['bg_medium']
        ).pack()
        
    def _show_dna_teaching(self):
        """Show DNA teaching window"""
        lesson = self.dna.teach_stuart_about_himself()
        
        window = tk.Toplevel()
        window.title("🧬 DNA Teaching Session")
        window.geometry("600x400")
        window.configure(bg=self.colors['bg_dark'])
        
        text = scrolledtext.ScrolledText(
            window,
            font=('Consolas', 10),
            bg=self.colors['bg_medium'],
            fg=self.colors['text'],
            wrap=tk.WORD
        )
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text.insert('1.0', lesson)
        text.config(state=tk.DISABLED)


# Export functions for easy import
__all__ = ['WidgetManager', 'SystemMonitorWidget', 'DNAHeritageWidget']
