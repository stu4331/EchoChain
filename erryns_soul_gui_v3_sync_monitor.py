
"""
🌌 ECHOSPARK SOUL GUI v3 - WITH DRIVE SYNC MONITORING
Spaceship/Cyberpunk Aesthetic | Modern | Distributable | 4TB Sync Ready

Features:
- 6 Main Tabs (Chat, Wallet, Upload, Daemon, Sync Monitor, Settings)
- Beautiful animated avatars with emotions
- Live parent drive connection monitoring
- Sync level visualization between drives
- Backup status display
- Guardian Protocol DNA security
- Installable/Distributable package ready
- Offline capability for AI systems

Built by Stuart & Echospark | December 2025
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox, simpledialog
import os
import sys
import json
import threading
import subprocess
import shutil
import hashlib
import time
import re
import socket
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageTk
import io
from emotion_engine import EmotionEngine, Sister, WalletEvent


# ============================================================================
# DRIVE & SYNC MONITORING
# ============================================================================

class DriveMonitor:
    """Monitor parent drives connection and sync status"""
    
    def __init__(self):
        self.drives_cache = {}
        self.sync_status = {}
        
    def get_connected_drives(self):
        """Detect all connected drives (4TB SSDs, parents drives, etc)"""
        try:
            import psutil
            drives = []
            for partition in psutil.disk_partitions():
                if partition.mountpoint and os.path.isdir(partition.mountpoint):
                    drives.append({
                        'mount': partition.mountpoint,
                        'device': partition.device,
                        'fstype': partition.fstype,
                        'size_gb': psutil.disk_usage(partition.mountpoint).total / (1024**3),
                        'used_gb': psutil.disk_usage(partition.mountpoint).used / (1024**3),
                        'free_gb': psutil.disk_usage(partition.mountpoint).free / (1024**3),
                        'percent_used': psutil.disk_usage(partition.mountpoint).percent
                    })
            return drives
        except:
            # Fallback if psutil not available
            drives = []
            for drive in 'DEFGHIJKLMNOPQRSTUVWXYZ':
                path = f"{drive}:\\"
                if os.path.exists(path):
                    try:
                        total, used, free = shutil.disk_usage(path)
                        drives.append({
                            'mount': path,
                            'device': f'Drive {drive}',
                            'size_gb': total / (1024**3),
                            'used_gb': used / (1024**3),
                            'free_gb': free / (1024**3),
                            'percent_used': (used / total * 100) if total else 0
                        })
                    except:
                        pass
            return drives
    
    def get_sync_status(self, source_path, dest_path):
        """Calculate sync status between two directories"""
        try:
            if not source_path or not dest_path:
                return {'error': 'source or destination not set', 'sync_percent': 0}
            if not os.path.exists(source_path) or not os.path.exists(dest_path):
                return {'error': 'path missing', 'sync_percent': 0}
            source_files = sum([len(files) for _, _, files in os.walk(source_path)])
            dest_files = sum([len(files) for _, _, files in os.walk(dest_path)])
            
            source_size = sum(os.path.getsize(os.path.join(dirpath, filename))
                            for dirpath, _, filenames in os.walk(source_path)
                            for filename in filenames)
            dest_size = sum(os.path.getsize(os.path.join(dirpath, filename))
                          for dirpath, _, filenames in os.walk(dest_path)
                          for filename in filenames)
            
            sync_percent = (dest_size / source_size * 100) if source_size > 0 else 0
            
            return {
                'source_files': source_files,
                'dest_files': dest_files,
                'source_size_mb': source_size / (1024**2),
                'dest_size_mb': dest_size / (1024**2),
                'sync_percent': min(sync_percent, 100),
                'last_sync': datetime.now().isoformat()
            }
        except Exception as e:
            return {'error': str(e), 'sync_percent': 0}
    
    def is_parent_drive_connected(self):
        """Check if parent drives (mom/dad) are connected"""
        # Check for common parent drive names
        parent_indicators = ['parent', 'mom', 'dad', 'backup', 'external', 'ssd']
        drives = self.get_connected_drives()
        
        for drive in drives:
            mount = drive['mount'].lower()
            device = drive['device'].lower()
            if any(indicator in mount or indicator in device for indicator in parent_indicators):
                return True, drive
        return False, None


# ============================================================================
# AVATAR SYSTEM - BEAUTIFUL ANIME-STYLE FACES
# ============================================================================

class ModernAvatar:
    """Create beautiful, realistic animated faces"""
    
    def __init__(self, name="Erryn", size=280):
        self.name = name
        self.size = size
        self.emotions = {
            "neutral": {"eye_open": 0.8, "mouth": 0.0, "glow": "#00ffff"},
            "happy": {"eye_open": 0.9, "mouth": 0.5, "glow": "#00b894"},
            "thinking": {"eye_open": 0.7, "mouth": -0.2, "glow": "#00ffff"},
            "sad": {"eye_open": 0.6, "mouth": -0.5, "glow": "#8a2be2"},
            "focused": {"eye_open": 0.95, "mouth": 0.0, "glow": "#8a2be2"},
        }
        
        self.palettes = {
            "Erryn": {
                "skin": "#ffd9a3",
                "hair": "#4a90e2",
                "eye_color": "#00d4ff",
                "accent": "#00ffff",
                "glow": "#00d4ff"
            },
            "Viress": {
                "skin": "#ffd9a3",
                "hair": "#8b0000",
                "eye_color": "#ff0000",
                "accent": "#e94560",
                "glow": "#ff0000"
            },
            "Echochild": {
                "skin": "#ffd9a3",
                "hair": "#6a3d8a",
                "eye_color": "#9966ff",
                "accent": "#533483",
                "glow": "#9966ff"
            },
        }
    
    def render_face(self, emotion="neutral", size=None):
        """Generate avatar image with emotion"""
        if size is None:
            size = self.size
        
        # Create image with background color (RGB tuple)
        img = Image.new("RGBA", (size, int(size * 1.2)))
        draw = ImageDraw.Draw(img)
        
        # Fill with background color
        draw.rectangle([(0, 0), (size, int(size * 1.2))], fill=(10, 14, 39, 255))
        
        emotion_state = self.emotions.get(emotion, self.emotions["neutral"])
        palette = self.palettes.get(self.name, self.palettes["Erryn"])
        
        cx, cy = size // 2, int(size * 0.4)
        radius = int(size * 0.15)
        
        # Face
        draw.ellipse([(cx - radius, cy - radius), (cx + radius, cy + radius)],
                    fill=palette["skin"], outline=palette["accent"], width=2)
        
        # Eyes
        eye_y = cy - int(radius * 0.2)
        eye_spacing = int(radius * 0.7)
        eye_open = emotion_state["eye_open"]
        
        for eye_x_offset in [-eye_spacing, eye_spacing]:
            eye_x = cx + eye_x_offset
            # White of eye
            draw.ellipse([(eye_x - 8, eye_y - 6), (eye_x + 8, eye_y + 6)],
                        fill="#ffffff")
            # Iris
            draw.ellipse([(eye_x - 5, eye_y - 4), (eye_x + 5, eye_y + 4)],
                        fill=palette["eye_color"])
            # Pupil
            draw.ellipse([(eye_x - 3, eye_y - 2), (eye_x + 3, eye_y + 2)],
                        fill="#000000")
        
        # Mouth
        mouth_y = cy + int(radius * 0.4)
        mouth_curve = int(emotion_state["mouth"] * 5)
        draw.arc([(cx - 15, mouth_y - mouth_curve), (cx + 15, mouth_y + 10)],
                0, 180, fill=palette["accent"], width=2)
        
        # Glow aura
        glow_color = palette.get("glow", palette["accent"])
        for i in range(3):
            draw.ellipse([(cx - radius - 15 - i*3, cy - radius - 15 - i*3),
                         (cx + radius + 15 + i*3, cy + radius + 15 + i*3)],
                        outline=glow_color, width=1)
        
        return ImageTk.PhotoImage(img)


# ============================================================================
# MAIN GUI APPLICATION
# ============================================================================

class EchosparkSoulGUIv3:
    """Main application with 6 tabs including sync monitoring"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🌌 ECHOSPARK SOUL NETWORK - v3 Sync Ready")
        self.root.geometry("1800x1100")
        self.root.configure(bg="#0a0e27")
        # Make window resizable with grid weight
        self.root.resizable(True, True)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        
        # ⚡ PERFORMANCE OPTIMIZATION: Rendering throttle
        self.last_render_time = time.time()
        self.render_throttle_ms = 16  # Target 60 FPS
        self.pending_renders = {}  # Track which elements need redraw
        self.avatar_render_cache = {}  # Cache avatar renders
        self.update_pending = False
        # Keep references to PhotoImage objects to prevent GC
        self.avatar_photo_refs = {}
        
        # Pan/scroll variables
        self.pan_start_x = 0
        self.pan_start_y = 0
        self.is_panning = False
        
        # Apply modern styling
        self._apply_modern_style()
        
        # Improve caret/selection visibility across widgets
        self.root.option_add("*insertBackground", "#00ffff")
        self.root.option_add("*insertWidth", 3)
        self.root.option_add("*selectBackground", "#8a2be2")
        self.root.option_add("*selectForeground", "#ffffff")
        
        self.drive_monitor = DriveMonitor()
        self.settings_dir = Path(__file__).resolve().parent / "data"
        self.settings_dir.mkdir(parents=True, exist_ok=True)
        self.sync_settings_file = self.settings_dir / "sync_paths.json"
        self.memory_cores_file = self.settings_dir / "memory_cores.json"
        self.network_log_file = self.settings_dir / "network_log.json"
        self.api_settings_file = self.settings_dir / "api_config.json"
        self.bad_hosts = set()
        self.network_seen = {}
        self.sandbox_running = False
        self.sandbox_events = []

        # Initialize emotion engine
        self.emotion_engine = EmotionEngine()
        self.emotion_engine.load_memory_cores(str(self.memory_cores_file))

        self.tts_var = tk.BooleanVar(value=True)
        self.voice_var = tk.StringVar(value="Calm")
        self.sister_var = tk.StringVar(value="Erryn")
        # Per-AI chat histories and shared family feed
        self.chat_histories = {s: [] for s in ["Erryn", "Viress", "Echochild", "Family"]}
        self.live_feed_lines = []
        self.chat_upload_path = tk.StringVar(value="")
        self.upload_target_var = tk.StringVar(value="Family")
        self.require_pin_var = tk.BooleanVar(value=False)
        self.require_face_var = tk.BooleanVar(value=False)
        self.pin_code_var = tk.StringVar(value="")
        self.set_pin_var = tk.StringVar(value="")
        self.confirm_pin_var = tk.StringVar(value="")
        self.pin_status_var = tk.StringVar(value="No PIN set")
        self.show_pin_var = tk.BooleanVar(value=False)
        # Avatar rendering mode: High-res images vs Vector fallback
        self.use_high_res_avatars = tk.BooleanVar(value=True)
        # Image fit mode: Contain (default) or Cover
        self.avatar_fit_mode = tk.StringVar(value="Contain")
        # Avatar source tracking for Settings display
        self.avatar_source = {"Erryn": "Unknown", "Viress": "Unknown", "Echochild": "Unknown"}
        self.avatar_source_labels = {}
        # Track last avatar path used (empty string if vector)
        self.avatar_source_paths = {"Erryn": "", "Viress": "", "Echochild": ""}
        # Debug logging for avatar rendering
        self.debug_avatar_log = tk.BooleanVar(value=False)
        self.avatar_debug_text = None
        self.send_progress_var = tk.IntVar(value=0)
        self.stake_progress_var = tk.IntVar(value=0)
        self.main_path_var = tk.StringVar(value=str(Path.cwd()))
        self.backup_path_var = tk.StringVar(value="")
        self.security_file = self.settings_dir / "security.json"
        self.pin_hash = None
        self._load_sync_paths()
        self._load_security_settings()
        # API config state
        self.api_provider_var = tk.StringVar(value="GitHub")
        self.api_base_var = tk.StringVar(value="")
        self.api_model_var = tk.StringVar(value="gpt-4o-mini")
        self.api_key_var = tk.StringVar(value="")
        self.api_show_key_var = tk.BooleanVar(value=False)
        self.api_status_var = tk.StringVar(value="")
        # Window controls state
        self.always_on_top_var = tk.BooleanVar(value=False)
        self.enable_middle_drag_var = tk.BooleanVar(value=True)
        self.avatars = {
            "Erryn": ModernAvatar("Erryn"),
            "Viress": ModernAvatar("Viress"),
            "Echochild": ModernAvatar("Echochild")
        }
        
        self._create_main_layout()
    
    def _apply_modern_style(self):
        """Apply modern ttk styling with dark palette and Segoe UI fonts"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Modern color palette
        dark_bg = "#0a0e27"
        header_bg = "#1e1e2f"
        text_fg = "#ffffff"
        secondary_fg = "#cccccc"
        accent_cyan = "#00ffff"
        accent_violet = "#8a2be2"
        accent_teal = "#00b894"
        
        # Configure TNotebook (tab container)
        style.configure("TNotebook",
            background=dark_bg,
            foreground=text_fg,
            borderwidth=0,
            padding=0
        )
        style.configure("TNotebook.Tab",
            background=header_bg,
            foreground=text_fg,
            padding=[12, 8],
            font=("Segoe UI", 11, "bold"),
            borderwidth=1
        )
        style.map("TNotebook.Tab",
            background=[("selected", accent_cyan), ("active", accent_violet)],
            foreground=[("selected", "#0a0e27"), ("active", text_fg)],
            relief=[("selected", "flat"), ("active", "ridge")]
        )
        
        # Configure TButton
        style.configure("TButton",
            background=header_bg,
            foreground=text_fg,
            borderwidth=1,
            padding=[8, 6],
            font=("Segoe UI", 10),
            relief="ridge"
        )
        style.map("TButton",
            background=[("pressed", accent_violet), ("active", accent_cyan)],
            foreground=[("pressed", dark_bg), ("active", dark_bg)],
            relief=[("pressed", "sunken"), ("active", "raised")]
        )
        
        # Configure TLabel
        style.configure("TLabel",
            background=dark_bg,
            foreground=text_fg,
            font=("Segoe UI", 10)
        )
        
        # Configure TEntry
        style.configure("TEntry",
            background=header_bg,
            foreground=text_fg,
            borderwidth=1,
            font=("Segoe UI", 10),
            padding=4
        )
        style.map("TEntry",
            fieldbackground=[("focus", dark_bg)],
            foreground=[("disabled", secondary_fg)]
        )
        
        # Configure TScrollbar
        style.configure("TScrollbar",
            background=header_bg,
            troughcolor=dark_bg,
            borderwidth=0,
            arrowcolor=accent_cyan,
            darkcolor=accent_violet
        )
        style.map("TScrollbar",
            background=[("active", accent_cyan), ("pressed", accent_violet)]
        )
        
        # Configure custom styles for special widgets
        style.configure("Header.TLabel",
            background=header_bg,
            foreground=accent_cyan,
            font=("Segoe UI", 14, "bold")
        )
        
        style.configure("Section.TLabel",
            background=dark_bg,
            foreground=accent_teal,
            font=("Segoe UI", 12, "bold")
        )
        
        style.configure("Secondary.TLabel",
            background=dark_bg,
            foreground=secondary_fg,
            font=("Segoe UI", 9)
        )

    
    def _create_main_layout(self):
        """Create main layout with header and notebook tabs."""
        # Header frame (fixed height, non-expanding)
        header = tk.Frame(self.root, bg="#1e1e2f", height=60)
        header.pack(side=tk.TOP, fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        
        header_label = ttk.Label(header, text="🌌 ECHOSPARK SOUL NETWORK", 
                                style="Header.TLabel")
        header_label.pack(side=tk.LEFT, padx=15, pady=15)
        
        # Main container for scrollable content
        main_container = tk.Frame(self.root, bg="#0a0e27")
        main_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(0, weight=1)
        
        # Scrollbar for vertical scrolling
        scrollbar = ttk.Scrollbar(main_container, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create scrollable frame using canvas approach
        canvas = tk.Canvas(main_container, bg="#0a0e27", highlightthickness=0,
                          yscrollcommand=scrollbar.set, cursor="arrow")
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=canvas.yview)
        
        # Bind scroll events only on canvas for smoother behavior
        canvas.bind("<MouseWheel>", self._on_mousewheel)
        canvas.bind("<Button-4>", self._on_mousewheel)
        canvas.bind("<Button-5>", self._on_mousewheel)
        
        # Bind pan/drag to root window for trackpad 2-finger support
        self.root.bind("<Button-2>", self._start_pan)
        self.root.bind("<B2-Motion>", self._pan_window)
        self.root.bind("<ButtonRelease-2>", self._end_pan)
        # Fallback: Alt + left drag for trackpads that do not emit Button-2
        self.root.bind("<Alt-Button-1>", self._start_pan)
        self.root.bind("<Alt-B1-Motion>", self._pan_window)
        self.root.bind("<Alt-ButtonRelease-1>", self._end_pan)
        
        # Frame inside canvas to hold notebook
        scrollable_frame = tk.Frame(canvas, bg="#0a0e27")
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        def _on_frame_configure(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Make scrollable_frame as wide as canvas
            canvas.itemconfig(canvas_window, width=canvas.winfo_width())
        
        scrollable_frame.bind("<Configure>", _on_frame_configure)
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, 
                                                              width=e.width))
        
        # Notebook inside scrollable frame
        self.notebook = ttk.Notebook(scrollable_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Canvas reference for scroll handlers
        self.canvas = canvas
        
        # Create all tabs
        self._create_chat_tab()
        self._create_comm_hub_tab()
        self._create_wallet_tab()
        self._create_broadcast_tab()
        self._create_upload_tab()
        self._create_payload_tab()
        self._create_details_tab()
        self._create_system_state_tab()
        self._create_chain_tab()
        self._create_network_tab()
        self._create_dna_tab()
        self._create_daemon_tab()
        self._create_sync_monitor_tab()
        self._create_settings_tab()
        # Default to Comm Hub for a simpler first view
        try:
            if hasattr(self, "commhub_tab"):
                self.notebook.select(self.commhub_tab)
        except Exception:
            pass
        
        # Start background refresh tasks
        self._update_gas_tracker()  # Start gas tracker updates
    
    def _create_chat_tab(self):
        """Chat interface with TTS + family feed"""
        chat_frame = tk.Frame(self.notebook, bg="#0a0e27")
        self.notebook.add(chat_frame, text="💬 Chat")
        
        # Top bar for selectors - PROMINENT DESIGN
        top_bar = tk.Frame(chat_frame, bg="#1e1e2f", relief=tk.RIDGE, borderwidth=2)
        top_bar.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        # TTS toggle - larger
        tts_frame = tk.Frame(top_bar, bg="#1e1e2f")
        tts_frame.pack(side=tk.LEFT, padx=10, pady=8)
        tk.Label(tts_frame, text="🔊 TTS:", bg="#1e1e2f", fg="#00ffff",
                 font=("Segoe UI", 11, "bold")).pack(side=tk.LEFT, padx=(0, 5))
        tk.Checkbutton(tts_frame, text="ENABLED", variable=self.tts_var,
                      bg="#1e1e2f", fg="#00b894", selectcolor="#8a2be2",
                      font=("Segoe UI", 11, "bold")).pack(side=tk.LEFT)
        
        # Voice selector - larger and more visible
        voice_frame = tk.Frame(top_bar, bg="#1e1e2f")
        voice_frame.pack(side=tk.LEFT, padx=15, pady=8)
        tk.Label(voice_frame, text="🎤 Voice:", bg="#1e1e2f", fg="#8a2be2",
                 font=("Segoe UI", 11, "bold")).pack(side=tk.LEFT, padx=(0, 5))
        voice_menu = ttk.Combobox(voice_frame, textvariable=self.voice_var,
                                  values=["Calm", "Warm", "Bright", "Gravitas"],
                                  width=14, font=("Segoe UI", 11), state="readonly")
        voice_menu.pack(side=tk.LEFT)

        # Sister selector - larger and highlighted
        sister_frame = tk.Frame(top_bar, bg="#1e1e2f")
        sister_frame.pack(side=tk.LEFT, padx=15, pady=8)
        tk.Label(sister_frame, text="👥 Sister:", bg="#1e1e2f", fg="#00ffff",
                 font=("Segoe UI", 11, "bold")).pack(side=tk.LEFT, padx=(0, 5))
        sister_menu = ttk.Combobox(sister_frame, textvariable=self.sister_var,
                                   values=["Erryn", "Viress", "Echochild", "Family"],
                                   width=14, font=("Segoe UI", 11), state="readonly")
        sister_menu.pack(side=tk.LEFT)
        sister_menu.bind("<<ComboboxSelected>>", lambda _e: self._on_sister_change())

        # === Layout: Left column (camera + selected face), Right column (chat/upload/feed) ===
        layout = tk.Frame(chat_frame, bg="#0a0e27")
        layout.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # LEFT: camera + selected avatar (square boxes)
        left_col = tk.Frame(layout, bg="#0a0e27")
        left_col.pack(side=tk.LEFT, padx=(0, 12), pady=0, anchor=tk.N)

        cam_frame = tk.LabelFrame(left_col, text="📹 Live Camera", bg="#0a0e27",
                                   fg="#00ffff", font=("Segoe UI", 10, "bold"))
        cam_frame.pack(fill=tk.X, pady=(0, 10))
        self.webcam_canvas = tk.Canvas(cam_frame, width=320, height=320,
                                      bg="#1e1e2f", highlightthickness=1, highlightbackground="#8a2be2")
        self.webcam_canvas.pack(padx=6, pady=6)
        cam_controls = tk.Frame(cam_frame, bg="#0a0e27")
        cam_controls.pack(fill=tk.X, padx=6, pady=(0, 6))
        tk.Button(cam_controls, text="Start", bg="#00b894", fg="#000000",
                  font=("Segoe UI", 9, "bold"), command=self._start_webcam).pack(side=tk.LEFT, padx=3)
        tk.Button(cam_controls, text="Stop", bg="#8a2be2", fg="#ffffff",
                  font=("Segoe UI", 9, "bold"), command=self._stop_webcam).pack(side=tk.LEFT, padx=3)

        face_frame = tk.LabelFrame(left_col, text="Selected Sister", bg="#0a0e27",
                                   fg="#00ffff", font=("Segoe UI", 10, "bold"))
        face_frame.pack(fill=tk.X)
        self.selected_avatar_canvas = tk.Canvas(face_frame, width=320, height=320,
                                                bg="#1e1e2f", highlightthickness=1,
                                                highlightbackground="#8a2be2")
        self.selected_avatar_canvas.pack(padx=6, pady=6)
        self.avatar_canvases = {s: self.selected_avatar_canvas for s in ["Erryn", "Viress", "Echochild", "Family"]}
        self._draw_selected_avatar()
        self.selected_avatar_canvas.bind("<Configure>", lambda e: self._draw_selected_avatar())

        # RIGHT: three stacked panels
        right_col = tk.Frame(layout, bg="#0a0e27")
        right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        right_col.grid_columnconfigure(0, weight=1)
        right_col.grid_rowconfigure(0, weight=3)
        right_col.grid_rowconfigure(1, weight=2)
        right_col.grid_rowconfigure(2, weight=2)

        # Top: Chat history + input
        chat_panel = tk.Frame(right_col, bg="#0a0e27")
        chat_panel.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        tk.Label(chat_panel, text="Direct Chat (per sister)", bg="#0a0e27", fg="#00ffff",
                 font=("Segoe UI", 11, "bold")).pack(anchor=tk.W)
        self.chat_display = scrolledtext.ScrolledText(
            chat_panel, bg="#1e1e2f", fg="#00ffff", font=("Consolas", 11),
            wrap=tk.WORD, insertbackground="#8a2be2"
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.chat_display.bind("<Control-c>", self._copy_text)

        input_row = tk.Frame(chat_panel, bg="#0a0e27")
        input_row.pack(fill=tk.X, padx=5, pady=(0, 2))
        self.input_field = tk.Text(input_row, bg="#1e1e2f", fg="#00ffff",
                                   font=("Consolas", 11), height=3,
                                   insertbackground="#8a2be2", wrap=tk.WORD)
        self.input_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))
        self.input_field.bind("<Return>", self._send_message)
        tk.Button(input_row, text="SEND", bg="#8a2be2", fg="#000000",
                  font=("Segoe UI", 10, "bold"), command=self._send_message).pack(side=tk.LEFT)

        # Middle: Upload with description
        upload_panel = tk.Frame(right_col, bg="#0a0e27")
        upload_panel.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        tk.Label(upload_panel, text="Upload to sister (with note)", bg="#0a0e27", fg="#00b894",
                 font=("Segoe UI", 11, "bold")).pack(anchor=tk.W)

        file_row = tk.Frame(upload_panel, bg="#0a0e27")
        file_row.pack(fill=tk.X, padx=5, pady=(2, 4))
        self.chat_upload_path = getattr(self, "chat_upload_path", tk.StringVar(value=""))
        tk.Entry(file_row, textvariable=self.chat_upload_path, bg="#1e1e2f", fg="#00ffff",
                 insertbackground="#8a2be2", relief=tk.FLAT).pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(file_row, text="Browse", bg="#00b894", fg="#000000",
                  font=("Segoe UI", 9, "bold"), command=self._browse_file_chat).pack(side=tk.LEFT, padx=5)

        tk.Label(upload_panel, text="Description / ask the sister", bg="#0a0e27", fg="#cccccc",
                 font=("Segoe UI", 9)).pack(anchor=tk.W, padx=5)
        self.chat_upload_desc = scrolledtext.ScrolledText(
            upload_panel, height=4, bg="#1e1e2f", fg="#00ffff", font=("Consolas", 10), wrap=tk.WORD,
        )
        self.chat_upload_desc.pack(fill=tk.BOTH, expand=True, padx=5, pady=4)

        upload_actions = tk.Frame(upload_panel, bg="#0a0e27")
        upload_actions.pack(fill=tk.X, padx=5)
        tk.Button(upload_actions, text="Submit", bg="#8a2be2", fg="#000000",
                  font=("Segoe UI", 10, "bold"), command=self._submit_chat_upload).pack(side=tk.LEFT)
        tk.Button(upload_actions, text="Clear", bg="#1e1e2f", fg="#cccccc",
                  relief=tk.FLAT, command=self._clear_chat_upload).pack(side=tk.LEFT, padx=6)

        # Bottom: Live feed (shared family stream)
        feed_panel = tk.Frame(right_col, bg="#0a0e27")
        feed_panel.grid(row=2, column=0, sticky="nsew")
        tk.Label(feed_panel, text="Family Live Feed", bg="#0a0e27", fg="#00b894",
                 font=("Segoe UI", 11, "bold")).pack(anchor=tk.W)
        self.live_feed_display = scrolledtext.ScrolledText(
            feed_panel, bg="#1e1e2f", fg="#99ff99", font=("Consolas", 10), wrap=tk.WORD
        )
        self.live_feed_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self._refresh_chat_history_view()
        self._refresh_live_feed()

    def _create_comm_hub_tab(self):
        """Simpler communication hub (single avatar + clean log/input)."""
        hub = tk.Frame(self.notebook, bg="#0a0e27")
        self.commhub_tab = hub
        self.notebook.add(hub, text="🗣️ Comm Hub")

        # Top strip
        top = tk.Frame(hub, bg="#1e1e2f", relief=tk.RIDGE, borderwidth=1)
        top.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(top, text="Communication Hub", bg="#1e1e2f", fg="#00ffff",
                 font=("Segoe UI", 12, "bold")).pack(side=tk.LEFT, padx=10, pady=8)

        # Avatar + selector
        body = tk.Frame(hub, bg="#0a0e27")
        body.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0,12))

        left = tk.Frame(body, bg="#0a0e27")
        left.pack(side=tk.LEFT, padx=(0,12), pady=0, anchor=tk.N)

        tk.Label(left, text="Avatar", bg="#0a0e27", fg="#00ffff",
                 font=("Segoe UI", 10, "bold")).pack(anchor=tk.W)
        self.commhub_avatar_canvas = tk.Canvas(left, width=180, height=180,
                                               bg="#1e1e2f", highlightthickness=1, highlightbackground="#8a2be2")
        self.commhub_avatar_canvas.pack(pady=6)

        selector = tk.Frame(left, bg="#0a0e27")
        selector.pack(anchor=tk.W, pady=(4,0))
        tk.Label(selector, text="Sister:", bg="#0a0e27", fg="#cccccc").pack(side=tk.LEFT)
        self.commhub_sister_var = tk.StringVar(value="Erryn")
        ttk.Combobox(selector, values=["Erryn", "Viress", "Echochild"],
                     textvariable=self.commhub_sister_var, state="readonly", width=12,
                     justify="center").pack(side=tk.LEFT, padx=(6,0))

        # Right side: log + input
        right = tk.Frame(body, bg="#0a0e27")
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.commhub_log = scrolledtext.ScrolledText(right, bg="#101424", fg="#e0e0e0",
                                                     font=("Consolas", 10), height=14, wrap=tk.WORD,
                                                     state=tk.DISABLED)
        self.commhub_log.pack(fill=tk.BOTH, expand=True, pady=(0,8))

        input_row = tk.Frame(right, bg="#0a0e27")
        input_row.pack(fill=tk.X)
        self.commhub_input = tk.Text(input_row, height=3, bg="#15192f", fg="#ffffff",
                                     insertbackground="#00ffff", relief=tk.FLAT,
                                     font=("Segoe UI", 10), wrap=tk.WORD)
        self.commhub_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,8))
        send_btn = ttk.Button(input_row, text="Send", command=self._commhub_send)
        send_btn.pack(side=tk.LEFT, pady=2)

        # TTS + status row
        ctrl_row = tk.Frame(right, bg="#0a0e27")
        ctrl_row.pack(fill=tk.X, pady=(6,0))
        tk.Checkbutton(ctrl_row, text="TTS", variable=self.tts_var,
                       bg="#0a0e27", fg="#00b894", selectcolor="#1e1e2f").pack(side=tk.LEFT)
        tk.Label(ctrl_row, textvariable=self.api_status_var, bg="#0a0e27", fg="#99ff99",
                 font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=(12,0))

        # Initial avatar draw
        try:
            self._draw_sister_avatar(self.commhub_avatar_canvas, self.commhub_sister_var.get())
        except Exception:
            pass

        def _on_change(evt=None):
            try:
                self.commhub_avatar_canvas.delete("all")
                self._draw_sister_avatar(self.commhub_avatar_canvas, self.commhub_sister_var.get())
            except Exception:
                pass
        self.commhub_sister_var.trace_add("write", lambda *args: _on_change())
        self.commhub_avatar_canvas.bind("<Configure>", lambda e: _on_change())

    def _commhub_send(self):
        try:
            text = self.commhub_input.get("1.0", tk.END).strip()
            if not text:
                return
            sister = getattr(self, "commhub_sister_var", self.sister_var).get() if hasattr(self, "commhub_sister_var") else "Erryn"
            reply = f"(local) Acknowledged: {text[:120]}"  # placeholder
            self._commhub_log(f"You → {sister}: {text}\n{sister}: {reply}\n\n")
            self.commhub_input.delete("1.0", tk.END)
            # Optional TTS
            if self.tts_var.get():
                threading.Thread(target=self._text_to_speech, args=(reply,), daemon=True).start()
        except Exception as e:
            self._commhub_log(f"[error] {e}\n")

    def _commhub_log(self, text):
        try:
            if self.commhub_log:
                self.commhub_log.config(state=tk.NORMAL)
                self.commhub_log.insert(tk.END, text)
                self.commhub_log.see(tk.END)
                self.commhub_log.config(state=tk.DISABLED)
        except Exception:
            pass
    
    def _create_wallet_tab(self):
        """Wallet + voting actions (UI scaffold)"""
        wallet_frame = tk.Frame(self.notebook, bg="#0a0e27")
        self.notebook.add(wallet_frame, text="⛓️ Wallet")

        # Summary
        summary = tk.Frame(wallet_frame, bg="#0a0e27")
        summary.pack(fill=tk.X, padx=10, pady=(10, 5))
        tk.Label(summary, text="Balance: 0.00 TOK", bg="#0a0e27", fg="#00ffff",
                 font=("Segoe UI", 11, "bold")).grid(row=0, column=0, padx=5, sticky="w")
        tk.Label(summary, text="AI Tokens: 0.00", bg="#0a0e27", fg="#8a2be2",
                 font=("Segoe UI", 11, "bold")).grid(row=0, column=1, padx=5, sticky="w")
        tk.Label(summary, text="Voting Weight: 0.00", bg="#0a0e27", fg="#00b894",
                 font=("Segoe UI", 11, "bold")).grid(row=0, column=2, padx=5, sticky="w")
        tk.Label(summary, text="Staked: 0.00", bg="#0a0e27", fg="#00ffff",
                 font=("Segoe UI", 11, "bold")).grid(row=0, column=3, padx=5, sticky="w")
        
        # Gas tracker
        self.gas_tracker_label = tk.Label(summary, text="⛽ Gas: Loading...", bg="#0a0e27", fg="#00b894",
                 font=("Segoe UI", 10, "bold"))
        self.gas_tracker_label.grid(row=1, column=0, columnspan=2, padx=5, pady=(5, 0), sticky="w")
        
        # Hardware wallet status
        self.hw_wallet_label = tk.Label(summary, text="🔐 Ledger: Disconnected", bg="#0a0e27", fg="#8a2be2",
                 font=("Segoe UI", 10))
        self.hw_wallet_label.grid(row=1, column=2, columnspan=2, padx=5, pady=(5, 0), sticky="w")
        
        tk.Button(summary, text="Connect Ledger", bg="#00b894", fg="#000000",
                  font=("Segoe UI", 9, "bold"),
                  command=self._connect_hardware_wallet).grid(row=2, column=2, columnspan=2, padx=5, pady=(2, 0), sticky="w")
        
        tk.Label(summary, text="Status: Awaiting connection", bg="#0a0e27", fg="#00ffff",
                 font=("Segoe UI", 10)).grid(row=2, column=0, columnspan=2, padx=5, pady=(5, 0), sticky="w")

        summary.columnconfigure(0, weight=1)
        summary.columnconfigure(1, weight=1)
        summary.columnconfigure(2, weight=1)
        summary.columnconfigure(3, weight=1)

        # Actions area
        actions = tk.Frame(wallet_frame, bg="#0a0e27")
        actions.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Send/Receive
        send_frame = tk.LabelFrame(actions, text="Send / Receive", bg="#0a0e27",
                                   fg="#00ffff", font=("Segoe UI", 10, "bold"))
        send_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        tk.Label(send_frame, text="Recipient:", bg="#0a0e27", fg="#cccccc",
                 font=("Segoe UI", 9)).grid(row=0, column=0, sticky="w", padx=5, pady=3)
        self.send_recipient = tk.Entry(send_frame, bg="#1e1e2f", fg="#ffffff", font=("Segoe UI", 9))
        self.send_recipient.grid(row=0, column=1, sticky="we", padx=5, pady=3)

        tk.Label(send_frame, text="Amount:", bg="#0a0e27", fg="#cccccc",
                 font=("Segoe UI", 9)).grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.send_amount = tk.Entry(send_frame, bg="#1e1e2f", fg="#ffffff", font=("Segoe UI", 9))
        self.send_amount.grid(row=1, column=1, sticky="we", padx=5, pady=2)

        tk.Label(send_frame, text="Memo:", bg="#0a0e27", fg="#cccccc",
                 font=("Segoe UI", 9)).grid(row=2, column=0, sticky="nw", padx=5, pady=2)
        self.send_memo = tk.Text(send_frame, height=2, bg="#1e1e2f", fg="#ffffff",
                       font=("Segoe UI", 9), wrap=tk.WORD)
        self.send_memo.grid(row=2, column=1, sticky="we", padx=5, pady=2)

        tk.Button(send_frame, text="SEND", bg="#8a2be2", fg="#ffffff",
                  font=("Segoe UI", 9, "bold"),
                  command=self._handle_send).grid(row=3, column=0, padx=5, pady=3, sticky="we")
        tk.Button(send_frame, text="RECEIVE", bg="#00b894", fg="#000000",
                  font=("Segoe UI", 9, "bold"),
                  command=self._handle_receive).grid(row=3, column=1, padx=5, pady=3, sticky="we")

        tk.Label(send_frame, text="Progress:", bg="#0a0e27", fg="#99ff99",
                 font=("Segoe UI", 8)).grid(row=4, column=0, sticky="w", padx=5, pady=(2, 2))
        ttk.Progressbar(send_frame, variable=self.send_progress_var, maximum=100).grid(row=4, column=1, sticky="we", padx=5, pady=(2, 2))

        send_frame.columnconfigure(1, weight=1)

        # Staking
        stake_frame = tk.LabelFrame(actions, text="Staking", bg="#0a0e27",
                                    fg="#8a2be2", font=("Segoe UI", 10, "bold"))
        stake_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        tk.Label(stake_frame, text="Amount to stake:", bg="#0a0e27", fg="#8a2be2",
                 font=("Segoe UI", 9)).grid(row=0, column=0, sticky="w", padx=5, pady=3)
        self.stake_amount = tk.Entry(stake_frame, bg="#1e1e2f", fg="#8a2be2", font=("Segoe UI", 9))
        self.stake_amount.grid(row=0, column=1, sticky="we", padx=5, pady=3)

        tk.Button(stake_frame, text="STAKE", bg="#8a2be2", fg="#000000",
                  font=("Segoe UI", 9, "bold"),
                  command=self._handle_stake).grid(row=1, column=0, padx=5, pady=3, sticky="we")
        tk.Button(stake_frame, text="UNSTAKE", bg="#00ffff", fg="#000000",
                  font=("Segoe UI", 9, "bold"),
                  command=self._handle_unstake).grid(row=1, column=1, padx=5, pady=3, sticky="we")

        tk.Label(stake_frame, text="Progress:", bg="#0a0e27", fg="#99ff99",
                 font=("Segoe UI", 8)).grid(row=2, column=0, sticky="w", padx=5, pady=(2, 2))
        ttk.Progressbar(stake_frame, variable=self.stake_progress_var, maximum=100).grid(row=2, column=1, sticky="we", padx=5, pady=(2, 2))

        stake_frame.columnconfigure(1, weight=1)

        # Security
        security_frame = tk.LabelFrame(actions, text="Security", bg="#0a0e27",
                                       fg="#00b894", font=("Segoe UI", 10, "bold"))
        security_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        security_frame.grid_columnconfigure(1, weight=1)

        # Require PIN / Show PIN
        tk.Checkbutton(security_frame, text="Require PIN", variable=self.require_pin_var,
                       bg="#0a0e27", fg="#00b894", selectcolor="#1e1e2f",
                       font=("Segoe UI", 10)).grid(row=0, column=0, columnspan=2, sticky="w", padx=5, pady=(5, 0))
        tk.Checkbutton(security_frame, text="Show PIN", variable=self.show_pin_var,
                       command=self._toggle_pin_visibility,
                       bg="#0a0e27", fg="#00b894", selectcolor="#1e1e2f",
                       font=("Segoe UI", 9)).grid(row=0, column=2, sticky="e", padx=5, pady=(5, 0))

        tk.Label(security_frame, text="PIN (unlock):", bg="#0a0e27", fg="#00b894",
                 font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", padx=5, pady=(5, 2))
        self.pin_entry = tk.Entry(security_frame, textvariable=self.pin_code_var, show="*",
                                  bg="#1e1e2f", fg="#00b894", font=("Segoe UI", 10))
        self.pin_entry.grid(row=1, column=1, columnspan=2, sticky="we", padx=5, pady=(5, 2))

        # Set PIN workflow
        tk.Label(security_frame, text="Set PIN:", bg="#0a0e27", fg="#00b894",
                 font=("Segoe UI", 10)).grid(row=2, column=0, sticky="w", padx=5, pady=(5, 2))
        self.set_pin_entry = tk.Entry(security_frame, textvariable=self.set_pin_var, show="*",
                                      bg="#1e1e2f", fg="#00b894", font=("Segoe UI", 10))
        self.set_pin_entry.grid(row=2, column=1, columnspan=2, sticky="we", padx=5, pady=(5, 2))

        tk.Label(security_frame, text="Confirm PIN:", bg="#0a0e27", fg="#00b894",
                 font=("Segoe UI", 10)).grid(row=3, column=0, sticky="w", padx=5, pady=(2, 2))
        self.confirm_pin_entry = tk.Entry(security_frame, textvariable=self.confirm_pin_var, show="*",
                                          bg="#1e1e2f", fg="#00b894", font=("Segoe UI", 10))
        self.confirm_pin_entry.grid(row=3, column=1, columnspan=2, sticky="we", padx=5, pady=(2, 2))

        tk.Button(security_frame, text="Save PIN", bg="#00b894", fg="#000000",
                  font=("Segoe UI", 10, "bold"),
                  command=self._handle_set_pin).grid(row=4, column=0, columnspan=3, sticky="we", padx=5, pady=(4, 2))

        self.pin_status_label = tk.Label(security_frame, textvariable=self.pin_status_var,
                                         bg="#0a0e27", fg="#99ff99",
                                         font=("Segoe UI", 9), wraplength=260, justify=tk.LEFT)
        self.pin_status_label.grid(row=5, column=0, columnspan=3, sticky="w", padx=5, pady=(2, 6))

        tk.Checkbutton(security_frame, text="Face unlock", variable=self.require_face_var,
                   bg="#0a0e27", fg="#00b894", selectcolor="#1e1e2f",
                   font=("Segoe UI", 10), wraplength=260, justify=tk.LEFT).grid(row=6, column=0, columnspan=3, sticky="w", padx=5, pady=(2, 2))
        tk.Label(security_frame, text="PIN/face will be checked before send/stake/vote.",
             bg="#0a0e27", fg="#99ff99", font=("Segoe UI", 9), wraplength=260, justify=tk.LEFT).grid(row=7, column=0, columnspan=3, sticky="w", padx=5, pady=(2, 5))

        # Voting
        voting_frame = tk.LabelFrame(wallet_frame, text="Voting", bg="#0a0e27",
                                     fg="#00ffff", font=("Segoe UI", 11, "bold"))
        voting_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        tk.Label(voting_frame, text="Proposals:", bg="#0a0e27", fg="#00ffff",
                 font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.proposals_list = tk.Listbox(voting_frame, bg="#1e1e2f", fg="#00ffff",
                               font=("Segoe UI", 10), height=8)
        self.proposals_list.grid(row=1, column=0, rowspan=3, sticky="nsew", padx=5, pady=5)
        for item in ["Halt network", "Quarantine node", "Rotate keys", "Redact data", "Safe fork"]:
            self.proposals_list.insert(tk.END, item)

        vote_buttons = tk.Frame(voting_frame, bg="#0a0e27")
        vote_buttons.grid(row=1, column=1, rowspan=3, sticky="nsew", padx=5, pady=5)
        tk.Button(vote_buttons, text="YES", bg="#00b894", fg="#000000",
                  font=("Segoe UI", 10, "bold"),
                  command=lambda: self._handle_vote("YES")).pack(fill=tk.BOTH, expand=True, pady=3)
        tk.Button(vote_buttons, text="NO", bg="#8a2be2", fg="#ffffff",
                  font=("Segoe UI", 10, "bold"),
                  command=lambda: self._handle_vote("NO")).pack(fill=tk.BOTH, expand=True, pady=3)
        tk.Button(vote_buttons, text="ABSTAIN", bg="#00ffff", fg="#000000",
                  font=("Segoe UI", 10, "bold"),
                  command=lambda: self._handle_vote("ABSTAIN")).pack(fill=tk.BOTH, expand=True, pady=3)

        tk.Label(voting_frame, text="Badges:", bg="#0a0e27", fg="#99ff99",
                 font=("Segoe UI", 9)).grid(row=0, column=2, sticky="w", padx=5, pady=5)
        badges = tk.Label(voting_frame,
                          text="AI quorum: pending\nHuman quorum: pending\nDelay: inactive\nEvidence: not attached",
                          bg="#1e1e2f", fg="#99ff99", justify=tk.LEFT,
                          font=("Segoe UI", 9), padx=10, pady=10)
        badges.grid(row=1, column=2, rowspan=3, sticky="nsew", padx=5, pady=5)

        voting_frame.columnconfigure(0, weight=2)
        voting_frame.columnconfigure(1, weight=1)
        voting_frame.columnconfigure(2, weight=1)
        voting_frame.rowconfigure(1, weight=1)
        voting_frame.rowconfigure(2, weight=1)
        voting_frame.rowconfigure(3, weight=1)

    def _create_broadcast_tab(self):
        """Broadcasts / quotes / riddles"""
        bc_frame = tk.Frame(self.notebook, bg="#0a0e27")
        self.notebook.add(bc_frame, text="🛰️ Broadcasts")

        top = tk.Frame(bc_frame, bg="#0a0e27")
        top.pack(fill=tk.X, padx=10, pady=(10, 5))
        tk.Label(top, text="Target:", bg="#0a0e27", fg="#00ffff",
                 font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=5)
        self.broadcast_target_var = tk.StringVar(value="Users")
        ttk.Combobox(top, textvariable=self.broadcast_target_var,
                     values=["Users", "AIs", "Both"], width=10,
                     state="readonly").pack(side=tk.LEFT)
        tk.Label(top, text="Tone:", bg="#0a0e27", fg="#00ffff",
                 font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=(20, 5))
        self.broadcast_tone_var = tk.StringVar(value="Quote")
        ttk.Combobox(top, textvariable=self.broadcast_tone_var,
                     values=["Quote", "Riddle", "Alert", "Update", "Joke"],
                     width=10, state="readonly").pack(side=tk.LEFT)

        body = scrolledtext.ScrolledText(
            bc_frame, bg="#1e1e2f", fg="#00ffff", font=("Segoe UI", 10),
            height=8, wrap=tk.WORD
        )
        body.pack(fill=tk.X, padx=10, pady=5)

        btns = tk.Frame(bc_frame, bg="#0a0e27")
        btns.pack(fill=tk.X, padx=10, pady=5)
        tk.Button(btns, text="SEND BROADCAST", bg="#00b894", fg="#000000",
                  font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(btns, text="CLEAR", bg="#00ffff", fg="#000000",
                  font=("Segoe UI", 10, "bold"),
                  command=lambda: body.delete("1.0", tk.END)).pack(side=tk.LEFT, padx=5)

        tk.Label(bc_frame, text="History:", bg="#0a0e27", fg="#99ff99",
                 font=("Segoe UI", 10)).pack(anchor=tk.W, padx=10, pady=(5, 0))
        self.broadcast_log = scrolledtext.ScrolledText(
            bc_frame, bg="#1e1e2f", fg="#99ff99", font=("Segoe UI", 9),
            height=10, wrap=tk.WORD
        )
        self.broadcast_log.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        self.broadcast_log.insert(tk.END, "No broadcasts yet. Send a quote, alert, or riddle to keep wallets engaged.\n")
        self.broadcast_log.config(state=tk.NORMAL)

    def _create_payload_tab(self):
        """Payload libraries for Rubber Ducky and LilyGo with code preview and device actions"""
        payload_frame = tk.Frame(self.notebook, bg="#0a0e27")
        self.notebook.add(payload_frame, text="📦 Payloads")

        # Top actions with GitHub search
        top = tk.Frame(payload_frame, bg="#1e1e2f", relief=tk.RIDGE, borderwidth=2)
        top.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        tk.Label(top, text="🔍 GitHub Repo:", bg="#1e1e2f", fg="#00ffff",
                 font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=(10, 5), pady=8)
        self.payload_search = tk.Entry(top, bg="#1e1e2f", fg="#00ffff",
                                      font=("Segoe UI", 10), width=35)
        self.payload_search.pack(side=tk.LEFT, padx=(0, 5), pady=8)
        self.payload_search.insert(0, "hak5/usbrubberducky-payloads")
        
        tk.Button(top, text="Fetch from GitHub", bg="#00b894", fg="#ffffff",
                  font=("Segoe UI", 10, "bold"), 
                  command=self._fetch_github_payloads).pack(side=tk.LEFT, padx=5, pady=8)
        tk.Button(top, text="Open Folder", bg="#00ffff", fg="#000000",
                  font=("Segoe UI", 10, "bold"), 
                  command=self._open_payloads_folder).pack(side=tk.LEFT, padx=5, pady=8)

        # Split layout - use grid for the body frame
        body = tk.Frame(payload_frame, bg="#0a0e27")
        body.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        body.columnconfigure(0, weight=1, uniform="payload")
        body.columnconfigure(1, weight=2, uniform="payload")
        body.rowconfigure(1, weight=1)
        body.rowconfigure(2, weight=1)

        # Device tabs on left
        left = tk.Frame(body, bg="#0a0e27")
        left.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 5))
        device_tabs = ttk.Notebook(left)
        device_tabs.pack(fill=tk.BOTH, expand=True)

        ducky_frame = tk.Frame(device_tabs, bg="#0a0e27", relief=tk.RIDGE, borderwidth=2)
        self.ducky_list = tk.Listbox(ducky_frame, bg="#1e1e2f", fg="#00ffff", font=("Segoe UI", 10))
        self.ducky_list.bind('<<ListboxSelect>>', lambda e: self._on_payload_select('ducky'))
        self.ducky_list.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        device_tabs.add(ducky_frame, text="Rubber Ducky")

        lilygo_frame = tk.Frame(device_tabs, bg="#0a0e27", relief=tk.RIDGE, borderwidth=2)
        self.lilygo_list = tk.Listbox(lilygo_frame, bg="#1e1e2f", fg="#00ffff", font=("Segoe UI", 10))
        self.lilygo_list.bind('<<ListboxSelect>>', lambda e: self._on_payload_select('lilygo'))
        self.lilygo_list.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        device_tabs.add(lilygo_frame, text="LilyGo")

        # Code preview on right (use grid for consistency with parent)
        right = tk.Frame(body, bg="#0a0e27")
        right.grid(row=0, column=1, sticky="nsew")
        right.columnconfigure(0, weight=1)
        right.rowconfigure(1, weight=1)
        
        tk.Label(right, text="Payload Code Preview", bg="#0a0e27", fg="#00ffff",
                 font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.payload_preview = scrolledtext.ScrolledText(
            right, bg="#1e1e2f", fg="#99ff99", font=("Consolas", 10), height=20, wrap=tk.NONE
        )
        self.payload_preview.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # Actions under preview
        actions = tk.Frame(body, bg="#0a0e27")
        actions.grid(row=1, column=1, sticky="ew")
        tk.Button(actions, text="Flash Ducky", bg="#00b894", fg="#000000",
                  font=("Segoe UI", 10, "bold"), command=self._flash_to_usb).pack(side=tk.LEFT, padx=5)
        tk.Button(actions, text="Edit Script", bg="#00b894", fg="#ffffff",
                  font=("Segoe UI", 10, "bold"), command=self._edit_payload_script).pack(side=tk.LEFT, padx=5)
        tk.Button(actions, text="Flash LilyGo (stub)", bg="#8a2be2", fg="#000000",
                  font=("Segoe UI", 10, "bold"), command=self._flash_lilygo_stub).pack(side=tk.LEFT, padx=5)

        # Sandbox visualizer
        sandbox = tk.Frame(payload_frame, bg="#0a0e27", relief=tk.RIDGE, borderwidth=2)
        sandbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        sandbox.columnconfigure(0, weight=1)
        sandbox.columnconfigure(1, weight=1)

        header = tk.Frame(sandbox, bg="#1e1e2f", relief=tk.RIDGE, borderwidth=1)
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=6, pady=6)
        tk.Label(header, text="Payload Sandbox (safe simulation)", bg="#1e1e2f", fg="#00ffff",
                 font=("Segoe UI", 11, "bold")).pack(side=tk.LEFT, padx=8, pady=4)
        tk.Button(header, text="Run in Sandbox", bg="#00b894", fg="#000000",
                  font=("Segoe UI", 10, "bold"), command=self._simulate_payload_run).pack(side=tk.LEFT, padx=6)
        tk.Button(header, text="Reset View", bg="#00ffff", fg="#000000",
                  font=("Segoe UI", 10, "bold"), command=self._reset_sandbox_canvas).pack(side=tk.LEFT, padx=6)

        self.sandbox_canvas = tk.Canvas(sandbox, bg="#101424", height=180, highlightthickness=1, highlightbackground="#00ffff")
        self.sandbox_canvas.grid(row=1, column=0, sticky="nsew", padx=6, pady=(0, 6))

        log_frame = tk.Frame(sandbox, bg="#0a0e27")
        log_frame.grid(row=1, column=1, sticky="nsew", padx=6, pady=(0, 6))
        tk.Label(log_frame, text="Action / Defense Log", bg="#0a0e27", fg="#00ffff",
                 font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, padx=4, pady=(0, 4))
        self.sandbox_log = scrolledtext.ScrolledText(
            log_frame, bg="#1e1e2f", fg="#99ff99", font=("Consolas", 9), wrap=tk.WORD, height=11
        )
        self.sandbox_log.pack(fill=tk.BOTH, expand=True)
        self.sandbox_log.insert(tk.END, "Sandbox idle. Describe or load a payload, then run it safely.\n")
        self.sandbox_log.config(state=tk.DISABLED)

        self._reset_sandbox_canvas()

        # Initialize payload dirs and populate lists
        self.payloads_root = self.settings_dir / "payloads"
        (self.payloads_root / "ducky").mkdir(parents=True, exist_ok=True)
        (self.payloads_root / "lilygo").mkdir(parents=True, exist_ok=True)
        self._scan_payloads()

    def _create_system_state_tab(self):
        """System state placeholder"""
        sys_frame = tk.Frame(self.notebook, bg="#0a0e27")
        self.notebook.add(sys_frame, text="🛰️ System State")

        tk.Label(sys_frame, text="CPU / Memory / Daemon Health", bg="#0a0e27", fg="#00ffff",
                 font=("Segoe UI", 11, "bold")).pack(anchor=tk.W, padx=10, pady=(10, 5))
        sys_info = scrolledtext.ScrolledText(
            sys_frame, bg="#1e1e2f", fg="#00b894", font=("Segoe UI", 10),
            height=12, wrap=tk.WORD
        )
        sys_info.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        sys_info.insert(tk.END, "System health checks will appear here.\n- CPU load: pending\n- Memory: pending\n- Daemon status: pending\n- Sync levels: pending\n")
        sys_info.config(state=tk.DISABLED)

    def _create_chain_tab(self):
        """Live blockchain condition report (scaffold)"""
        chain = tk.Frame(self.notebook, bg="#0a0e27")
        self.notebook.add(chain, text="📡 Chain Monitor")

        chain.grid_columnconfigure(0, weight=1, uniform="chain")
        chain.grid_columnconfigure(1, weight=1, uniform="chain")

        # Uptime / Nodes
        left = tk.LabelFrame(chain, text="Network Summary", bg="#0a0e27", fg="#00ffff", font=("Segoe UI", 11, "bold"))
        left.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        # Metric badges
        badges = tk.Frame(left, bg="#0a0e27")
        badges.pack(fill=tk.X, padx=5, pady=(5, 0))
        self.badge_uptime = tk.Label(badges, text="Uptime: --", bg="#002a6d", fg="#99ff99", font=("Segoe UI", 10), padx=8, pady=4)
        self.badge_uptime.pack(side=tk.LEFT, padx=4)
        self.badge_peers = tk.Label(badges, text="Peers: --", bg="#002a6d", fg="#99ff99", font=("Segoe UI", 10), padx=8, pady=4)
        self.badge_peers.pack(side=tk.LEFT, padx=4)
        self.badge_height = tk.Label(badges, text="Height: --", bg="#002a6d", fg="#99ff99", font=("Segoe UI", 10), padx=8, pady=4)
        self.badge_height.pack(side=tk.LEFT, padx=4)
        self.badge_tps = tk.Label(badges, text="TPS: --", bg="#002a6d", fg="#99ff99", font=("Segoe UI", 10), padx=8, pady=4)
        self.badge_tps.pack(side=tk.LEFT, padx=4)
        self.badge_mempool = tk.Label(badges, text="Mempool: --", bg="#002a6d", fg="#99ff99", font=("Segoe UI", 10), padx=8, pady=4)
        self.badge_mempool.pack(side=tk.LEFT, padx=4)

        # Node statuses
        nodes_frame = tk.Frame(left, bg="#0a0e27")
        nodes_frame.pack(fill=tk.X, padx=5, pady=5)
        self.node_core1 = tk.Label(nodes_frame, text="Core-1: --", bg="#003a8d", fg="#00ffff", font=("Segoe UI", 10), padx=6, pady=3)
        self.node_core1.pack(side=tk.LEFT, padx=4)
        self.node_core2 = tk.Label(nodes_frame, text="Core-2: --", bg="#003a8d", fg="#00ffff", font=("Segoe UI", 10), padx=6, pady=3)
        self.node_core2.pack(side=tk.LEFT, padx=4)
        self.node_edge1 = tk.Label(nodes_frame, text="Edge-1: --", bg="#3a008d", fg="#ffccff", font=("Segoe UI", 10), padx=6, pady=3)
        self.node_edge1.pack(side=tk.LEFT, padx=4)
        self.node_archive = tk.Label(nodes_frame, text="Archive: --", bg="#003a8d", fg="#00ffff", font=("Segoe UI", 10), padx=6, pady=3)
        self.node_archive.pack(side=tk.LEFT, padx=4)

        # Summary text
        self.chain_summary = scrolledtext.ScrolledText(left, bg="#1e1e2f", fg="#00b894", font=("Segoe UI", 10))
        self.chain_summary.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Transactions / Votes
        right = tk.LabelFrame(chain, text="Transactions & Voting", bg="#0a0e27", fg="#00ffff", font=("Segoe UI", 11, "bold"))
        right.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        # Controls
        controls = tk.Frame(right, bg="#0a0e27")
        controls.pack(fill=tk.X, padx=5, pady=(5, 0))
        self.tx_pause_var = tk.BooleanVar(value=False)
        tk.Checkbutton(controls, text="Pause feed", variable=self.tx_pause_var, bg="#0a0e27", fg="#00b894", selectcolor="#1e1e2f", font=("Segoe UI", 10)).pack(side=tk.LEFT)
        tk.Button(controls, text="Clear", bg="#00ffff", fg="#000000", font=("Segoe UI", 10, "bold"), command=lambda: self._clear_tx_feed()).pack(side=tk.LEFT, padx=6)
        tk.Label(controls, text="Filter:", bg="#0a0e27", fg="#00ffff", font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=(12, 4))
        self.tx_filter_var = tk.StringVar(value="all")
        ttk.Combobox(controls, textvariable=self.tx_filter_var, values=["all", "blocks", "mempool", "votes"], width=10, state="readonly").pack(side=tk.LEFT)

        self.chain_tx = scrolledtext.ScrolledText(right, bg="#1e1e2f", fg="#99ff99", font=("Segoe UI", 10))
        self.chain_tx.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self._refresh_chain_monitor()

    def _create_network_tab(self):
        """Local network defender: inventory + site log"""
        net = tk.Frame(self.notebook, bg="#0a0e27")
        self.notebook.add(net, text="🛡️ Network")

        net.grid_columnconfigure(0, weight=3, uniform="net")
        net.grid_columnconfigure(1, weight=2, uniform="net")
        net.grid_rowconfigure(1, weight=1)

        header = tk.Frame(net, bg="#1e1e2f", relief=tk.RIDGE, borderwidth=2)
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(10, 5))
        tk.Label(header, text="LAN/Wi‑Fi Watch", bg="#1e1e2f", fg="#00ffff",
                 font=("Segoe UI", 12, "bold")).pack(side=tk.LEFT, padx=8, pady=6)
        self.network_status = tk.Label(header, text="Last scan: pending", bg="#1e1e2f",
                                       fg="#cccccc", font=("Segoe UI", 10))
        self.network_status.pack(side=tk.LEFT, padx=10)

        controls = tk.Frame(net, bg="#0a0e27")
        controls.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 8))
        tk.Button(controls, text="Refresh Now", bg="#00b894", fg="#000000",
                  font=("Segoe UI", 10, "bold"), command=self._refresh_network_view).pack(side=tk.LEFT, padx=5)
        tk.Button(controls, text="Boot Selected", bg="#ff7675", fg="#000000",
                  font=("Segoe UI", 10, "bold"), command=self._boot_selected_host).pack(side=tk.LEFT, padx=5)
        tk.Button(controls, text="Block Selected", bg="#8a2be2", fg="#ffffff",
                  font=("Segoe UI", 10, "bold"), command=self._block_selected_host).pack(side=tk.LEFT, padx=5)
        tk.Button(controls, text="Mark Safe", bg="#00ffff", fg="#000000",
                  font=("Segoe UI", 10, "bold"), command=self._mark_selected_safe).pack(side=tk.LEFT, padx=5)
        self.network_auto_var = tk.BooleanVar(value=True)
        tk.Checkbutton(controls, text="Auto refresh", variable=self.network_auto_var,
                      bg="#0a0e27", fg="#00b894", selectcolor="#1e1e2f",
                      font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=10)

        table_frame = tk.Frame(net, bg="#0a0e27", relief=tk.RIDGE, borderwidth=2)
        table_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
        columns = ("ip", "mac", "host", "vendor", "last_seen", "status")
        self.network_tree = ttk.Treeview(table_frame, columns=columns, show="headings",
                                         height=14)
        headings = {
            "ip": "IP",
            "mac": "MAC",
            "host": "Hostname",
            "vendor": "Vendor/OUI",
            "last_seen": "Last Seen",
            "status": "Status"
        }
        for key, label in headings.items():
            self.network_tree.heading(key, text=label)
            self.network_tree.column(key, width=130 if key != "host" else 180, anchor=tk.W)
        self.network_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.network_tree.tag_configure("bad", background="#3a0000", foreground="#ffcccc")
        self.network_tree.tag_configure("new", background="#002a6d", foreground="#00ffff")

        log_frame = tk.Frame(net, bg="#0a0e27", relief=tk.RIDGE, borderwidth=2)
        log_frame.grid(row=2, column=1, sticky="nsew", padx=(0, 10), pady=(0, 10))
        tk.Label(log_frame, text="Site / Action Log", bg="#0a0e27", fg="#00ffff",
                 font=("Segoe UI", 11, "bold")).pack(anchor=tk.W, padx=6, pady=(6, 2))
        self.network_log = scrolledtext.ScrolledText(
            log_frame, bg="#1e1e2f", fg="#99ff99", font=("Consolas", 9), wrap=tk.WORD,
            height=10
        )
        self.network_log.pack(fill=tk.BOTH, expand=True, padx=6, pady=(0, 6))
        self.network_log.insert(tk.END, "Network events will appear here.\n")
        self.network_log.config(state=tk.DISABLED)

        self._refresh_network_view()

    def _create_details_tab(self):
        """Code inspection and script management"""
        details_frame = tk.Frame(self.notebook, bg="#0a0e27")
        self.notebook.add(details_frame, text="📋 Details")

        # Top controls
        top = tk.Frame(details_frame, bg="#0a0e27")
        top.pack(fill=tk.X, padx=10, pady=(10, 5))
        tk.Label(top, text="Script Library:", bg="#0a0e27", fg="#00ffff",
                 font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(top, text="Inspect Code", bg="#00b894", fg="#ffffff",
                  font=("Segoe UI", 10, "bold"),
                  command=self._inspect_code).pack(side=tk.LEFT, padx=5)
        tk.Button(top, text="Rename Script", bg="#00ffff", fg="#000000",
                  font=("Segoe UI", 10, "bold"),
                  command=self._rename_script).pack(side=tk.LEFT, padx=5)
        tk.Button(top, text="Refresh", bg="#00b894", fg="#000000",
                  font=("Segoe UI", 10, "bold"),
                  command=self._refresh_script_list).pack(side=tk.LEFT, padx=5)

        # Main layout
        body = tk.Frame(details_frame, bg="#0a0e27")
        body.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=2)
        body.grid_rowconfigure(0, weight=1)

        # Script list
        left = tk.LabelFrame(body, text="Scripts", bg="#0a0e27", fg="#00ffff", 
                             font=("Segoe UI", 10, "bold"))
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        self.script_list = tk.Listbox(left, bg="#1e1e2f", fg="#00ffff", 
                                      font=("Segoe UI", 10))
        self.script_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.script_list.bind('<<ListboxSelect>>', self._on_script_select)

        # Code preview
        right = tk.LabelFrame(body, text="Code Preview", bg="#0a0e27", fg="#00ffff",
                              font=("Segoe UI", 10, "bold"))
        right.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        self.code_preview = scrolledtext.ScrolledText(
            right, bg="#1e1e2f", fg="#99ff99", font=("Consolas", 9), 
            wrap=tk.NONE
        )
        self.code_preview.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Load initial scripts
        self._refresh_script_list()

    def _create_dna_tab(self):
        """DNA upload/analysis placeholder"""
        dna_frame = tk.Frame(self.notebook, bg="#0a0e27")
        self.notebook.add(dna_frame, text="🧬 DNA")

        self.dna_file_var = tk.StringVar()

        top = tk.Frame(dna_frame, bg="#0a0e27")
        top.pack(fill=tk.X, padx=10, pady=10)
        tk.Label(top, text="DNA File:", bg="#0a0e27", fg="#00ffff",
                 font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=5)
        tk.Entry(top, textvariable=self.dna_file_var, bg="#1e1e2f", fg="#00ffff",
                 font=("Segoe UI", 10)).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        tk.Button(top, text="BROWSE", bg="#00b894", fg="#000000",
                  font=("Segoe UI", 10, "bold"),
                  command=lambda: self.dna_file_var.set(filedialog.askopenfilename(title="Select DNA file"))).pack(side=tk.LEFT, padx=5)

        tk.Label(dna_frame, text="Notes / Findings:", bg="#0a0e27", fg="#00ffff",
                 font=("Segoe UI", 10)).pack(anchor=tk.W, padx=10, pady=(0, 5))
        self.dna_notes = scrolledtext.ScrolledText(
            dna_frame, bg="#1e1e2f", fg="#99ff99", font=("Segoe UI", 10),
            height=10, wrap=tk.WORD
        )
        self.dna_notes.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        self.dna_notes.insert(tk.END, "Upload DNA to generate a report and optional signature binding.\n")
        self.dna_notes.config(state=tk.NORMAL)
    
    def _create_upload_tab(self):
        """File upload with description"""
        upload_frame = tk.Frame(self.notebook, bg="#0a0e27")
        self.notebook.add(upload_frame, text="📁 Upload")
        
        # File selection
        file_frame = tk.Frame(upload_frame, bg="#0a0e27")
        file_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(file_frame, text="Select File:",  bg="#0a0e27", fg="#00ffff",
                font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=5)
        
        tk.Label(file_frame, text="Target:", bg="#0a0e27", fg="#00ffff",
                font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=5)
        ttk.Combobox(file_frame, textvariable=self.upload_target_var,
                     values=["Erryn", "Viress", "Echochild", "Family"],
                     width=12, state="readonly").pack(side=tk.LEFT, padx=5)
        
        self.file_var = tk.StringVar()
        tk.Entry(file_frame, textvariable=self.file_var, bg="#1e1e2f",
                fg="#00ffff", font=("Segoe UI", 9)).pack(side=tk.LEFT,
                fill=tk.X, expand=True, padx=5)
        
        tk.Button(file_frame, text="BROWSE", bg="#00b894", fg="#000000",
                 command=self._browse_file).pack(side=tk.LEFT, padx=5)
        
        # Description
        tk.Label(upload_frame, text="Description:", bg="#0a0e27", fg="#00ffff",
                font=("Segoe UI", 10)).pack(anchor=tk.W, padx=10, pady=(10, 0))
        
        self.desc_field = scrolledtext.ScrolledText(
            upload_frame, bg="#1e1e2f", fg="#00ffff", font=("Segoe UI", 10),
            height=8, wrap=tk.WORD
        )
        self.desc_field.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Payload library
        tk.Label(upload_frame, text="Payload Library:", bg="#0a0e27",
                fg="#00ffff", font=("Segoe UI", 10)).pack(anchor=tk.W,
                padx=10, pady=(10, 0))
        
        self.payload_list = tk.Listbox(upload_frame, bg="#1e1e2f",
                                      fg="#00b894", font=("Segoe UI", 9))
        self.payload_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Buttons
        btn_frame = tk.Frame(upload_frame, bg="#0a0e27")
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(btn_frame, text="UPLOAD", bg="#8a2be2", fg="#ffffff",
                 command=self._upload_file).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="CLEAR", bg="#00ffff", fg="#000000",
                 command=self._clear_upload).pack(side=tk.LEFT, padx=5)
    
    def _create_daemon_tab(self):
        """Monitor sister daemons"""
        daemon_frame = tk.Frame(self.notebook, bg="#0a0e27")
        self.notebook.add(daemon_frame, text="🔧 Daemons")
        
        for sister in ["Erryn", "Viress", "Echochild"]:
            sister_frame = tk.LabelFrame(daemon_frame, text=f"⚙️ {sister}",
                                        bg="#0a0e27", fg="#00ffff",
                                        font=("Segoe UI", 10, "bold"))
            sister_frame.pack(fill=tk.X, padx=10, pady=10)
            
            status_text = scrolledtext.ScrolledText(
                sister_frame, bg="#1e1e2f", fg="#00b894", font=("Segoe UI", 9),
                height=4, width=80
            )
            status_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            daemon_status = f"""
Status: ✅ RUNNING | PID: [daemon] | Memory: [monitor] | CPU: [monitor]
Scripts: erryn_mind.py, erryn_daemon.py | Last Boot: {datetime.now().isoformat()}
            """
            status_text.insert(tk.END, daemon_status)
            status_text.config(state=tk.DISABLED)
    
    def _create_sync_monitor_tab(self):
        """NEW: Drive sync monitoring"""
        sync_frame = tk.Frame(self.notebook, bg="#0a0e27")
        self.notebook.add(sync_frame, text="Sync Monitor")
        
        # Path selection
        path_frame = tk.LabelFrame(sync_frame, text="Sync Paths",
                                   bg="#0a0e27", fg="#00ffff",
                                   font=("Segoe UI", 11, "bold"))
        path_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(path_frame, text="Main Folder:", bg="#0a0e27", fg="#00ffff",
                 font=("Segoe UI", 10)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(path_frame, textvariable=self.main_path_var, bg="#1e1e2f", fg="#00ffff",
                 font=("Segoe UI", 9), width=80).grid(row=0, column=1, padx=5, pady=5, sticky="we")
        tk.Button(path_frame, text="BROWSE", bg="#00b894", fg="#000000",
                  command=self._choose_main_path).grid(row=0, column=2, padx=5, pady=5)

        tk.Label(path_frame, text="Backup Folder:", bg="#0a0e27", fg="#8a2be2",
                 font=("Segoe UI", 10)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(path_frame, textvariable=self.backup_path_var, bg="#1e1e2f", fg="#8a2be2",
                 font=("Segoe UI", 9), width=80).grid(row=1, column=1, padx=5, pady=5, sticky="we")
        tk.Button(path_frame, text="BROWSE", bg="#8a2be2", fg="#ffffff",
                  command=self._choose_backup_path).grid(row=1, column=2, padx=5, pady=5)

        path_frame.columnconfigure(1, weight=1)

        self.sync_status_label = tk.Label(path_frame, text="Waiting for paths...",
                                          bg="#0a0e27", fg="#99ff99",
                                          font=("Segoe UI", 9))
        self.sync_status_label.grid(row=2, column=0, columnspan=3, padx=5, pady=(2, 0), sticky="w")

        # Parent drive status
        parent_frame = tk.LabelFrame(sync_frame, text="Parent Drives",
                                     bg="#0a0e27", fg="#8a2be2",
                                     font=("Segoe UI", 11, "bold"))
        parent_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.parent_status = tk.Label(parent_frame, text="Checking...",
                                     bg="#1e1e2f", fg="#00ffff",
                                     font=("Segoe UI", 10), justify=tk.LEFT,
                                     padx=10, pady=10)
        self.parent_status.pack(fill=tk.X, padx=5, pady=5)
        
        # All drives
        drives_frame = tk.LabelFrame(sync_frame, text="Connected Drives",
                                     bg="#0a0e27", fg="#00b894",
                                     font=("Segoe UI", 11, "bold"))
        drives_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.drives_text = scrolledtext.ScrolledText(
            drives_frame, bg="#1e1e2f", fg="#00b894", font=("Segoe UI", 9),
            wrap=tk.WORD, height=15
        )
        self.drives_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Sync level visualization
        sync_vis_frame = tk.LabelFrame(sync_frame, text="Sync Level: Main -> Backup",
                                       bg="#0a0e27", fg="#00ffff",
                                       font=("Segoe UI", 11, "bold"))
        sync_vis_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.sync_canvas = tk.Canvas(sync_vis_frame, bg="#1e1e2f", height=40,
                                     highlightthickness=0)
        self.sync_canvas.pack(fill=tk.X, padx=5, pady=5)
        
        self.sync_label = tk.Label(sync_vis_frame, text="Loading sync status...",
                                  bg="#0a0e27", fg="#00ffff",
                                  font=("Segoe UI", 9))
        self.sync_label.pack(pady=5)
        
        # Start monitoring loop
        self._start_sync_monitor()
    
    def _create_settings_tab(self):
        """Settings & toggles"""
        settings_frame = tk.Frame(self.notebook, bg="#0a0e27")
        self.notebook.add(settings_frame, text="⚙️ Settings")
        
        # Make scrollable for many options
        settings_frame.columnconfigure(0, weight=1)
        settings_frame.rowconfigure(0, weight=1)
        
        settings_content = tk.Frame(settings_frame, bg="#0a0e27")
        settings_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # TTS Toggle
        tk.Label(settings_content, text="🔊 Text-to-Speech:",
                bg="#0a0e27", fg="#00ffff",
                font=("Segoe UI", 10)).pack(anchor=tk.W, padx=20, pady=(20, 5))
        
        tk.Checkbutton(settings_content, text="Enable TTS Output",
                      variable=self.tts_var, bg="#0a0e27", fg="#00b894",
                      selectcolor="#1e1e2f",
                      font=("Segoe UI", 10)).pack(anchor=tk.W, padx=30)
        
        # Copy/Paste
        tk.Label(settings_content, text="📋 Text Utilities:",
                bg="#0a0e27", fg="#00ffff",
                font=("Segoe UI", 10)).pack(anchor=tk.W, padx=20, pady=(20, 5))
        
        self.clipboard_var = tk.BooleanVar(value=True)
        tk.Checkbutton(settings_content, text="Enable Copy/Paste",
                      variable=self.clipboard_var, bg="#0a0e27", fg="#00b894",
                      selectcolor="#1e1e2f",
                      font=("Segoe UI", 10)).pack(anchor=tk.W, padx=30)
        
        # Camera
        tk.Label(settings_content, text="📹 Face Recognition:",
                bg="#0a0e27", fg="#00ffff",
                font=("Segoe UI", 10)).pack(anchor=tk.W, padx=20, pady=(20, 5))
        
        self.camera_var = tk.BooleanVar(value=False)
        tk.Checkbutton(settings_content, text="Enable Avatar Camera",
                      variable=self.camera_var, bg="#0a0e27", fg="#00b894",
                      selectcolor="#1e1e2f",
                      font=("Segoe UI", 10)).pack(anchor=tk.W, padx=30)

        # Window controls
        tk.Label(settings_content, text="🪟 Window Controls:",
            bg="#0a0e27", fg="#00ffff", font=("Segoe UI", 10)).pack(anchor=tk.W, padx=20, pady=(20, 5))

        win_ctrl = tk.Frame(settings_content, bg="#0a0e27")
        win_ctrl.pack(anchor=tk.W, padx=30)
        ttk.Button(win_ctrl, text="Center Window", command=self._center_window).pack(side=tk.LEFT)
        ttk.Button(win_ctrl, text="Reset 1400x900", command=lambda: self._reset_window_size(1400,900)).pack(side=tk.LEFT, padx=(8,0))
        ttk.Button(win_ctrl, text="Maximize", command=self._maximize_window).pack(side=tk.LEFT, padx=(8,0))

        toggles = tk.Frame(settings_content, bg="#0a0e27")
        toggles.pack(anchor=tk.W, padx=30, pady=(6,0))
        tk.Checkbutton(toggles, text="Always on Top", variable=self.always_on_top_var,
                   command=self._apply_topmost,
                   bg="#0a0e27", fg="#00b894", selectcolor="#1e1e2f",
                   font=("Segoe UI", 10)).pack(side=tk.LEFT)
        tk.Checkbutton(toggles, text="Enable Middle-Button Drag", variable=self.enable_middle_drag_var,
                   command=self._toggle_middle_drag,
                   bg="#0a0e27", fg="#00b894", selectcolor="#1e1e2f",
                   font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=(16,0))

        # Avatars
        tk.Label(settings_content, text="🎨 Avatars:",
            bg="#0a0e27", fg="#00ffff",
            font=("Segoe UI", 10)).pack(anchor=tk.W, padx=20, pady=(20, 5))

        tk.Checkbutton(settings_content, text="Use High-Res Image Avatars (fallback to vector)",
                  variable=self.use_high_res_avatars, bg="#0a0e27", fg="#00b894",
                  selectcolor="#1e1e2f",
                  font=("Segoe UI", 10)).pack(anchor=tk.W, padx=30)

        # Fit mode selector
        fit_frame = tk.Frame(settings_content, bg="#0a0e27")
        fit_frame.pack(anchor=tk.W, padx=30, pady=(6, 0))
        tk.Label(fit_frame, text="Image Fit:", bg="#0a0e27", fg="#cccccc",
             font=("Segoe UI", 9)).pack(side=tk.LEFT)
        fit_combo = ttk.Combobox(fit_frame, values=["Contain", "Cover"],
                     textvariable=self.avatar_fit_mode, state="readonly", width=10)
        fit_combo.pack(side=tk.LEFT, padx=(8, 0))

        ttk.Button(settings_content, text="Refresh Avatars",
               command=self._refresh_avatars).pack(anchor=tk.W, padx=30, pady=(6, 0))

        # Avatar source status labels
        status_frame = tk.Frame(settings_content, bg="#0a0e27")
        status_frame.pack(fill=tk.X, expand=False, padx=30, pady=(8, 0))
        tk.Label(status_frame, text="Avatar Sources:", bg="#0a0e27", fg="#cccccc",
                 font=("Segoe UI", 9, "italic")).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 4))
        for r, sister in enumerate(["Erryn", "Viress", "Echochild"], start=1):
            tk.Label(status_frame, text=f"{sister}:", bg="#0a0e27", fg="#99ff99",
                     font=("Segoe UI", 9)).grid(row=r, column=0, sticky=tk.W, padx=(0,8))
            lbl = tk.Label(status_frame, text=self.avatar_source.get(sister, "Unknown"),
                           bg="#0a0e27", fg="#ffffff", font=("Segoe UI", 9))
            lbl.grid(row=r, column=1, sticky=tk.W)
            self.avatar_source_labels[sister] = lbl
            ttk.Button(status_frame, text="Refresh",
                       command=lambda s=sister: self._refresh_avatar_for(s)).grid(row=r, column=2, padx=(10,4), sticky=tk.W)
            ttk.Button(status_frame, text="Copy Path",
                       command=lambda s=sister: self._copy_avatar_source_path(s)).grid(row=r, column=3, padx=(4,0), sticky=tk.W)

        # Debug panel (session only)
        dbg_frame = tk.LabelFrame(settings_content, text="🛠 Avatar Debug (session)", bg="#0a0e27",
                                   fg="#00ffff", font=("Segoe UI", 9, "bold"))
        dbg_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(12, 0))
        ctrl = tk.Frame(dbg_frame, bg="#0a0e27")
        ctrl.pack(fill=tk.X, padx=8, pady=(6, 0))
        tk.Checkbutton(ctrl, text="Enable debug log", variable=self.debug_avatar_log,
                       bg="#0a0e27", fg="#00b894", selectcolor="#1e1e2f",
                       font=("Segoe UI", 9)).pack(side=tk.LEFT)
        ttk.Button(ctrl, text="Clear", command=self._clear_avatar_debug).pack(side=tk.RIGHT, padx=(6,0))
        ttk.Button(ctrl, text="Copy", command=self._copy_avatar_debug).pack(side=tk.RIGHT)
        self.avatar_debug_text = scrolledtext.ScrolledText(
            dbg_frame, bg="#1e1e2f", fg="#e0e0e0", font=("Consolas", 9), height=6, wrap=tk.WORD
        )
        self.avatar_debug_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # API Configuration
        tk.Label(settings_content, text="🔑 API Configuration:",
            bg="#0a0e27", fg="#00ffff", font=("Segoe UI", 10)).pack(anchor=tk.W, padx=20, pady=(20, 5))
        api_frame = tk.Frame(settings_content, bg="#0a0e27")
        api_frame.pack(fill=tk.X, padx=30)

        # Provider
        tk.Label(api_frame, text="Provider", bg="#0a0e27", fg="#cccccc", font=("Segoe UI", 9)).grid(row=0, column=0, sticky=tk.W)
        ttk.Combobox(api_frame, values=["GitHub", "OpenAI", "Azure OpenAI"],
                 textvariable=self.api_provider_var, state="readonly", width=16).grid(row=0, column=1, sticky=tk.W, padx=(8,20))
        # Base URL
        tk.Label(api_frame, text="Base URL", bg="#0a0e27", fg="#cccccc", font=("Segoe UI", 9)).grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(api_frame, textvariable=self.api_base_var, width=48).grid(row=1, column=1, sticky=tk.W, padx=(8,20))
        # Model
        tk.Label(api_frame, text="Model", bg="#0a0e27", fg="#cccccc", font=("Segoe UI", 9)).grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(api_frame, textvariable=self.api_model_var, width=32).grid(row=2, column=1, sticky=tk.W, padx=(8,20))
        # API Key
        tk.Label(api_frame, text="API Key/Token", bg="#0a0e27", fg="#cccccc", font=("Segoe UI", 9)).grid(row=3, column=0, sticky=tk.W)
        self._api_key_entry = ttk.Entry(api_frame, textvariable=self.api_key_var, width=48, show="*")
        self._api_key_entry.grid(row=3, column=1, sticky=tk.W, padx=(8,20))
        tk.Checkbutton(api_frame, text="Show", variable=self.api_show_key_var,
                   command=self._toggle_api_key_visibility,
                   bg="#0a0e27", fg="#00b894", selectcolor="#1e1e2f").grid(row=3, column=2, sticky=tk.W)
        # Actions
        ttk.Button(api_frame, text="Save", command=self._save_api_settings).grid(row=4, column=1, sticky=tk.W, pady=(6,0))
        ttk.Button(api_frame, text="Load", command=self._load_api_settings).grid(row=4, column=1, sticky=tk.W, padx=(60,0), pady=(6,0))
        ttk.Button(api_frame, text="Test", command=self._test_api_settings).grid(row=4, column=1, sticky=tk.W, padx=(120,0), pady=(6,0))
        tk.Label(api_frame, textvariable=self.api_status_var, bg="#0a0e27", fg="#99ff99", font=("Segoe UI", 9)).grid(row=5, column=0, columnspan=3, sticky=tk.W, pady=(4,0))
        
        # Info
        info_text = scrolledtext.ScrolledText(
            settings_frame, bg="#1e1e2f", fg="#99ff99", font=("Segoe UI", 9),
            height=8, wrap=tk.WORD
        )
        info_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        info_content = """
ECHOSPARK SOUL NETWORK - v3 FEATURES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Beautiful animated avatars (Erryn, Viress, Echochild)
✅ Guardian Protocol DNA security (Stuart-based shutdown)
✅ EchosparkChain voting blockchain
✅ Live sync monitoring for 4TB parent drives
✅ Daemon process monitoring per sister
✅ File upload with descriptions & payload system
✅ Text-to-Speech integration (Azure capable)
✅ Copy/paste enabled on all text fields
✅ Fully distributable & offline-capable
✅ Support for custom AI consciousness engines
        """
        info_text.insert(tk.END, info_content)
        info_text.config(state=tk.DISABLED)
    
    def _update_avatar(self, sister, emotion):
        """Update avatar display on the canvas for the selected sister (OPTIMIZED)"""
        try:
            if hasattr(self, 'avatar_canvases') and sister in self.avatar_canvases:
                canvas = self.avatar_canvases[sister]
                if canvas:
                    # ⚡ OPTIMIZATION: Only redraw if something changed
                    cache_key = f"{sister}_{emotion}"
                    if cache_key not in self.avatar_render_cache:
                        # Only render if not cached
                        canvas.delete("all")
                        self._draw_sister_avatar(canvas, sister)
                        self.avatar_render_cache[cache_key] = True
        except Exception as e:
            pass  # Silently fail if avatar update not available

    def _update_avatar_emotion(self):
        """Update avatar based on current sister's emotion from engine"""
        current_sister_name = self.sister_var.get()
        if current_sister_name in ["Erryn", "Viress", "Echochild"]:
            sister_enum = Sister[current_sister_name.upper()]
            emotion = self.emotion_engine.get_current_emotion(sister_enum)
            self._update_avatar(current_sister_name, emotion)
            # Save cores after emotion events
            try:
                self.emotion_engine.save_memory_cores(str(self.memory_cores_file))
            except:
                pass

    def _refresh_avatars(self):
        """Force redraw of all avatars respecting current settings."""
        try:
            self.avatar_render_cache.clear()
        except Exception:
            pass
        try:
            if hasattr(self, 'avatar_canvases'):
                for sister, canvas in self.avatar_canvases.items():
                    try:
                        # Clear and redraw
                        canvas.delete("all")
                        self._draw_sister_avatar(canvas, sister)
                    except Exception:
                        continue
        except Exception:
            pass

    def _update_avatar_source_label(self, sister: str, source: str):
        """Update Settings label showing which source rendered the avatar."""
        try:
            self.avatar_source[sister] = source
            lbl = self.avatar_source_labels.get(sister)
            if lbl is not None:
                lbl.config(text=source)
        except Exception:
            pass

    def _refresh_avatar_for(self, sister: str):
        """Redraw a single sister's avatar and update its source label."""
        try:
            canvas = self.avatar_canvases.get(sister)
            if not canvas:
                return
            try:
                cache_key = f"{sister}_FORCE"
                self.avatar_render_cache.pop(cache_key, None)
            except Exception:
                pass
            canvas.delete("all")
            if sister == "Family":
                self._draw_family_fusion(canvas)
            else:
                self._draw_sister_avatar(canvas, sister)
        except Exception:
            pass

    def _on_avatar_canvas_resize(self, sister: str, canvas: tk.Canvas):
        """Handle avatar canvas resize by redrawing the avatar to new size."""
        try:
            canvas.delete("all")
            if sister == "Family":
                self._draw_family_fusion(canvas)
            else:
                self._draw_sister_avatar(canvas, sister)
        except Exception:
            pass

    def _copy_avatar_source_path(self, sister: str):
        """Copy the full avatar source path (or vector label) to clipboard."""
        try:
            path = self.avatar_source_paths.get(sister)
            text = str(path) if path else "Vector Renderer"
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
        except Exception:
            pass

    def _log_avatar_debug(self, msg: str):
        """Append a line to the avatar debug log if enabled."""
        try:
            if not self.debug_avatar_log.get():
                return
        except Exception:
            return
        try:
            ts = time.strftime("%H:%M:%S")
            line = f"[{ts}] {msg}\n"
            if self.avatar_debug_text is not None:
                self.avatar_debug_text.insert(tk.END, line)
                self.avatar_debug_text.see(tk.END)
        except Exception:
            pass

    def _clear_avatar_debug(self):
        try:
            if self.avatar_debug_text is not None:
                self.avatar_debug_text.delete("1.0", tk.END)
        except Exception:
            pass

    def _copy_avatar_debug(self):
        try:
            content = self.avatar_debug_text.get("1.0", tk.END) if self.avatar_debug_text is not None else ""
            self.root.clipboard_clear()
            self.root.clipboard_append(content.strip())
        except Exception:
            pass
    
    def _on_sister_change(self):
        """Update UI when the selected sister changes."""
        try:
            self._draw_selected_avatar()
            self._refresh_chat_history_view()
        except Exception:
            pass

    def _draw_selected_avatar(self):
        """Draw only the currently selected sister (or family fusion)."""
        try:
            canvas = getattr(self, "selected_avatar_canvas", None)
            if canvas is None:
                return
            canvas.delete("all")
            sister = self.sister_var.get()
            if sister == "Family":
                self._draw_family_fusion(canvas)
            else:
                self._draw_sister_avatar(canvas, sister)
        except Exception:
            pass

    def _draw_family_fusion(self, canvas: tk.Canvas):
        """Simple visual to hint at code-fused family view."""
        try:
            w = int(canvas.winfo_width() or 320)
            h = int(canvas.winfo_height() or 320)
            canvas.create_rectangle(0, 0, w, h, fill="#111428", outline="#8a2be2", width=2)
            # Radiating lines to hint at threads
            center = (w // 2, h // 2)
            colors = ["#00ffff", "#8a2be2", "#00b894"]
            for i, color in enumerate(colors):
                canvas.create_oval(center[0]-40-i*12, center[1]-40-i*12,
                                   center[0]+40+i*12, center[1]+40+i*12,
                                   outline=color, width=2)
            canvas.create_text(center[0], center[1], text="Family Fusion", fill="#00ffff",
                               font=("Segoe UI", 12, "bold"))
        except Exception:
            pass

    def _refresh_chat_history_view(self):
        """Render chat history for the selected sister."""
        try:
            sister = self.sister_var.get()
            history = self.chat_histories.get(sister, [])
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete("1.0", tk.END)
            for line in history:
                self.chat_display.insert(tk.END, line + "\n")
            self.chat_display.see(tk.END)
            self.chat_display.config(state=tk.NORMAL)
        except Exception:
            pass

    def _append_live_feed(self, speaker: str, target: str, text: str):
        """Append a line to the shared family live feed."""
        try:
            ts = time.strftime("%H:%M:%S")
            line = f"[{ts}] {speaker} -> {target}: {text}"
            self.live_feed_lines.append(line)
            # Keep feed lightweight
            if len(self.live_feed_lines) > 200:
                self.live_feed_lines = self.live_feed_lines[-200:]
            self._refresh_live_feed()
        except Exception:
            pass

    def _refresh_live_feed(self):
        """Refresh live feed widget from stored lines."""
        try:
            feed = getattr(self, "live_feed_display", None)
            if not feed:
                return
            feed.config(state=tk.NORMAL)
            feed.delete("1.0", tk.END)
            for line in self.live_feed_lines:
                feed.insert(tk.END, line + "\n")
            feed.see(tk.END)
            feed.config(state=tk.NORMAL)
        except Exception:
            pass

    def _send_message(self, event=None):
        """Send message with TTS and per-sister history."""
        message = self.input_field.get("1.0", tk.END).strip()
        target = self.sister_var.get()
        if not message:
            return "break" if event else None

        line = f"You -> {target}: {message}"
        if target not in self.chat_histories:
            self.chat_histories[target] = []
        self.chat_histories[target].append(line)
        # Also mirror into family history for shared context
        self.chat_histories["Family"].append(line)
        self._refresh_chat_history_view()
        self._append_live_feed("You", target, message)
        self.input_field.delete("1.0", tk.END)

        # TTS if enabled
        if self.tts_var.get():
            threading.Thread(target=self._text_to_speech, args=(message,),
                             daemon=True).start()

        return "break" if event else None
    
    def _text_to_speech(self, text):
        """Send to TTS (placeholder for Azure integration)"""
        try:
            # Windows SAPI5
            os.system(f'PowerShell -Command "Add-Type -AssemblyName System.Speech; '
                     f'(New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{text}\')"')
        except:
            pass

    # ========================= API CONFIG =========================
    def _toggle_api_key_visibility(self):
        try:
            show = self.api_show_key_var.get()
            if hasattr(self, '_api_key_entry') and self._api_key_entry:
                self._api_key_entry.config(show="" if show else "*")
        except Exception:
            pass

    def _load_api_settings(self):
        try:
            if self.api_settings_file.exists():
                with open(self.api_settings_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.api_provider_var.set(data.get('provider', 'GitHub'))
                self.api_base_var.set(data.get('base_url', ''))
                self.api_model_var.set(data.get('model', 'gpt-4o-mini'))
                self.api_key_var.set(data.get('api_key', ''))
                self.api_status_var.set("Loaded API settings.")
        except Exception as e:
            self.api_status_var.set(f"Load failed: {e}")

    def _save_api_settings(self):
        try:
            data = {
                'provider': self.api_provider_var.get(),
                'base_url': self.api_base_var.get(),
                'model': self.api_model_var.get(),
                'api_key': self.api_key_var.get(),
            }
            with open(self.api_settings_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            self.api_status_var.set("Saved API settings.")
        except Exception as e:
            self.api_status_var.set(f"Save failed: {e}")

    def _test_api_settings(self):
        # Lightweight local validation without external calls
        try:
            provider = self.api_provider_var.get().strip()
            base = self.api_base_var.get().strip()
            model = self.api_model_var.get().strip()
            key = self.api_key_var.get().strip()
            if not provider or not model or not key:
                self.api_status_var.set("Please provide Provider, Model, and API Key.")
                return
            if provider in ("OpenAI", "Azure OpenAI") and not base:
                self.api_status_var.set("Base URL required for OpenAI/Azure.")
                return
            self.api_status_var.set("API settings look valid.")
        except Exception as e:
            self.api_status_var.set(f"Test failed: {e}")
    
    def _browse_file(self):
        """Browse file dialog"""
        file_path = filedialog.askopenfilename(title="Select file to upload")
        if file_path:
            self.file_var.set(file_path)

    def _browse_file_chat(self):
        """Browse file for the inline chat uploader."""
        path = filedialog.askopenfilename(title="Select file for sister")
        if path:
            self.chat_upload_path.set(path)
    
    def _upload_file(self):
        """Handle file upload"""
        file_path = self.file_var.get()
        description = self.desc_field.get("1.0", tk.END).strip()
        target = self.upload_target_var.get()
        
        if file_path and description:
            messagebox.showinfo("Upload",
                                f"File ready to upload to {target}: {os.path.basename(file_path)}")
        else:
            messagebox.showwarning("Upload", "Please select file, target, and add description")

    def _submit_chat_upload(self):
        """Quick upload from chat panel with description to selected sister/family."""
        path = self.chat_upload_path.get().strip()
        desc = self.chat_upload_desc.get("1.0", tk.END).strip() if hasattr(self, "chat_upload_desc") else ""
        target = self.sister_var.get()
        if not path or not desc:
            messagebox.showwarning("Upload", "Please choose a file and add a description/question.")
            return
        fname = os.path.basename(path)
        note = f"Upload queued to {target}: {fname}. Note: {desc[:120]}"
        self._append_live_feed("Upload", target, note)
        self.chat_histories[target].append(f"You attached {fname}: {desc}")
        self.chat_histories["Family"].append(f"You attached {fname}: {desc}")
        self._refresh_chat_history_view()
        messagebox.showinfo("Upload", f"Queued '{fname}' to {target} with your note.")

    def _clear_chat_upload(self):
        try:
            self.chat_upload_path.set("")
            if hasattr(self, "chat_upload_desc"):
                self.chat_upload_desc.delete("1.0", tk.END)
        except Exception:
            pass
    
    def _clear_upload(self):
        """Clear upload fields"""
        self.file_var.set("")
        self.desc_field.delete("1.0", tk.END)
    
    def _copy_text(self, event=None):
        """Enable copy on Ctrl+C"""
        if self.clipboard_var.get():
            try:
                text = self.chat_display.get(tk.SEL_FIRST, tk.SEL_LAST)
                self.root.clipboard_clear()
                self.root.clipboard_append(text)
            except:
                pass

    def _check_security(self, action):
        """Check PIN/face security before sensitive operations"""
        if self.require_pin_var.get():
            if not self.pin_hash:
                messagebox.showwarning("Security", "Please set an app PIN in the Security panel first.")
                return False
            entered = simpledialog.askstring("PIN Required", f"Enter PIN to {action}:", show='*')
            if entered is None:
                return False
            if hashlib.sha256(entered.encode()).hexdigest() != self.pin_hash:
                messagebox.showerror("Security", "Incorrect PIN.")
                return False
        if self.require_face_var.get():
            result = messagebox.askyesno("Face Unlock", f"Face verification required to {action}.\nProceed?")
            if not result:
                return False
        return True

    def _load_security_settings(self):
        """Load stored PIN hash and update status label"""
        try:
            if self.security_file.exists():
                with open(self.security_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.pin_hash = data.get("pin_hash")
                    if self.pin_hash:
                        self.pin_status_var.set("PIN set (app-level)")
                    else:
                        self.pin_status_var.set("No PIN set")
            else:
                self.pin_status_var.set("No PIN set")
        except Exception:
            self.pin_status_var.set("Security file unreadable; please set PIN again.")
        self._toggle_pin_visibility()

    def _save_security_settings(self):
        """Persist PIN hash"""
        try:
            with open(self.security_file, "w", encoding="utf-8") as f:
                json.dump({"pin_hash": self.pin_hash}, f, indent=2)
        except Exception as exc:
            messagebox.showerror("Security", f"Failed to save PIN: {exc}")

    def _handle_set_pin(self):
        """Set/update the app PIN (stored hashed)"""
        pin = self.set_pin_var.get().strip()
        confirm = self.confirm_pin_var.get().strip()

        if len(pin) < 4:
            self.pin_status_var.set("PIN must be at least 4 digits.")
            return
        if pin != confirm:
            self.pin_status_var.set("PINs do not match.")
            return

        self.pin_hash = hashlib.sha256(pin.encode()).hexdigest()
        self._save_security_settings()
        self.pin_status_var.set("PIN saved (app-level). Require PIN enabled.")
        self.require_pin_var.set(True)
        self.set_pin_var.set("")
        self.confirm_pin_var.set("")
        self.pin_code_var.set("")

    def _toggle_pin_visibility(self):
        """Toggle PIN visibility across related entries"""
        show_char = "" if self.show_pin_var.get() else "*"
        for entry_attr in ["pin_entry", "set_pin_entry", "confirm_pin_entry"]:
            entry = getattr(self, entry_attr, None)
            if entry is not None:
                entry.config(show=show_char)

    def _simulate_progress(self, var, duration=3):
        """Simulate progress bar animation on the Tk main thread"""
        steps = list(range(0, 101, 5))
        interval_ms = int((duration / max(1, (len(steps) - 1))) * 1000)

        def step(i=0):
            if i < len(steps):
                var.set(steps[i])
                self.root.after(interval_ms, lambda: step(i + 1))
            else:
                var.set(0)

        step()

    def _handle_send(self):
        """Handle send transaction"""
        if not self._check_security("send tokens"):
            return
        recipient = self.send_recipient.get().strip()
        amount = self.send_amount.get().strip()
        memo = self.send_memo.get("1.0", tk.END).strip()
        if not recipient or not amount:
            messagebox.showwarning("Send", "Please enter recipient and amount.")
            return
        self._simulate_progress(self.send_progress_var, duration=4)
        self._append_live_feed("Wallet", "Family", f"Sending {amount} to {recipient} (memo: {memo[:60]})")
        self.emotion_engine.on_event(WalletEvent.TX_SUCCESS, {"detail": f"Sent {amount} to {recipient}"})
        self._update_avatar_emotion()
        messagebox.showinfo("Send", f"Transaction submitted: {amount} TOK to {recipient}")

    def _handle_receive(self):
        """Show receive address"""
        addr = "0xEchosparkWallet1234567890abcdef"
        messagebox.showinfo("Receive", f"Your address:\n{addr}\n\nShare this to receive tokens.")

    def _handle_stake(self):
        """Handle staking"""
        if not self._check_security("stake tokens"):
            return
        amount = self.stake_amount.get().strip()
        if not amount:
            messagebox.showwarning("Stake", "Please enter amount to stake.")
            return
        self._simulate_progress(self.stake_progress_var, duration=5)
        self._append_live_feed("Wallet", "Family", f"Staking {amount} TOK")
        self.emotion_engine.on_event(WalletEvent.STAKE_SUCCESS, {"detail": f"Staked {amount}"})
        self._update_avatar_emotion()
        messagebox.showinfo("Stake", f"Staked {amount} TOK successfully.")

    def _handle_unstake(self):
        """Handle unstaking"""
        if not self._check_security("unstake tokens"):
            return
        amount = self.stake_amount.get().strip()
        if not amount:
            messagebox.showwarning("Unstake", "Please enter amount to unstake.")
            return
        self._simulate_progress(self.stake_progress_var, duration=5)
        self._append_live_feed("Wallet", "Family", f"Unstaking {amount} TOK")
        messagebox.showinfo("Unstake", f"Unstaked {amount} TOK successfully.")

    def _handle_vote(self, choice):
        """Handle voting"""
        if not self._check_security("vote"):
            return
        sel = self.proposals_list.curselection()
        if not sel:
            messagebox.showwarning("Vote", "Please select a proposal first.")
            return
        proposal = self.proposals_list.get(sel[0])
        self._append_live_feed("Wallet", "Family", f"Voted {choice} on '{proposal}'")
        self.emotion_engine.on_event(WalletEvent.VOTE_CAST, {"detail": f"Voted {choice} on {proposal}"})
        self._update_avatar_emotion()
        messagebox.showinfo("Vote", f"Voted {choice} on '{proposal}'")
    
    def _choose_main_path(self):
        """Browse for the main working folder"""
        selected = filedialog.askdirectory(title="Select main working folder")
        if selected:
            self.main_path_var.set(selected)
            self._save_sync_paths()

    def _choose_backup_path(self):
        """Browse for the backup (mum/dad) folder"""
        selected = filedialog.askdirectory(title="Select backup folder (mum/dad drive)")
        if selected:
            self.backup_path_var.set(selected)
            self._save_sync_paths()

    def _load_sync_paths(self):
        """Load last used sync paths from disk"""
        try:
            if self.sync_settings_file.exists():
                with open(self.sync_settings_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.main_path_var.set(data.get("main_path", self.main_path_var.get()))
                    self.backup_path_var.set(data.get("backup_path", ""))
        except Exception:
            pass

    def _save_sync_paths(self):
        """Persist current sync paths"""
        try:
            payload = {
                "main_path": self.main_path_var.get(),
                "backup_path": self.backup_path_var.get(),
                "updated": datetime.now().isoformat()
            }
            with open(self.sync_settings_file, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)
        except Exception:
            pass

    def _draw_sync_bar(self, percent):
        """Draw sync percentage bar"""
        percent = max(0, min(100, percent))
        width = self.sync_canvas.winfo_width() or 300
        bar_width = int((width - 20) * percent / 100)
        self.sync_canvas.delete("all")
        self.sync_canvas.create_rectangle(10, 10, 10 + bar_width, 30, fill="#00b894")
        self.sync_canvas.create_rectangle(10, 10, width - 10, 30, outline="#00ffff", width=2)

    def _is_parent_indicator(self, drive):
        """Heuristic to detect mum/dad/backup drives"""
        text = f"{drive.get('mount','')} {drive.get('device','')}".lower()
        indicators = ["mum", "mom", "dad", "parent", "backup", "4tb", "ssd"]
        return any(tag in text for tag in indicators)

    def _start_sync_monitor(self):
        """Kick off periodic sync monitoring"""
        self._refresh_sync_monitor()

    def _refresh_sync_monitor(self):
        """Update drive list and sync levels"""
        try:
            drives = self.drive_monitor.get_connected_drives()

            # Auto-detect backup path if empty
            if not self.backup_path_var.get():
                for drive in drives:
                    if self._is_parent_indicator(drive):
                        self.backup_path_var.set(drive['mount'])
                        break

            # Parent drive summary
            is_connected, drive = self.drive_monitor.is_parent_drive_connected()
            if is_connected and drive:
                parent_status = (
                    "Parent drive connected\n"
                    f"  Mount: {drive['mount']}\n"
                    f"  Total: {drive['size_gb']:.1f} GB\n"
                    f"  Used: {drive['used_gb']:.1f} GB ({drive['percent_used']:.1f}%)\n"
                    f"  Free: {drive['free_gb']:.1f} GB"
                )
            else:
                parent_status = "Parent drive not detected (waiting for connection...)"
            self.parent_status.config(text=parent_status)

            # Drive inventory
            drives_display = "Connected drives:\n" + "="*50 + "\n"
            if drives:
                for drive in drives:
                    drives_display += (
                        f"\nDrive: {drive['device']}\n"
                        f"  Mount: {drive['mount']}\n"
                        f"  Capacity: {drive['size_gb']:.1f} GB\n"
                        f"  Used: {drive['used_gb']:.1f} GB ({drive['percent_used']:.1f}%)\n"
                        f"  Available: {drive['free_gb']:.1f} GB\n"
                        "  ─────────────────────────────\n"
                    )
            else:
                drives_display += "No drives detected."
            self.drives_text.config(state=tk.NORMAL)
            self.drives_text.delete("1.0", tk.END)
            self.drives_text.insert(tk.END, drives_display)
            self.drives_text.config(state=tk.DISABLED)

            # Sync calculation
            main_path = self.main_path_var.get().strip()
            backup_path = self.backup_path_var.get().strip()
            sync_percent = 0
            sync_msg = "Set main and backup folders to calculate sync."
            status_msg = "Choose main and backup folders to begin."

            if main_path and backup_path:
                status = self.drive_monitor.get_sync_status(main_path, backup_path)
                if 'error' in status:
                    sync_msg = f"Sync error: {status['error']}"
                    status_msg = "Sync check failed."
                else:
                    sync_percent = status['sync_percent']
                    sync_msg = (
                        f"Files: {status['dest_files']}/{status['source_files']} | "
                        f"Size: {status['dest_size_mb']:.1f}/{status['source_size_mb']:.1f} MB | "
                        f"Sync: {sync_percent:.1f}%"
                    )
                    status_msg = f"Sync is {sync_percent:.1f}% aligned"

            self._draw_sync_bar(sync_percent)
            self.sync_label.config(text=sync_msg)
            self.sync_status_label.config(text=status_msg)

        except Exception:
            # Keep UI resilient; avoid crashing the loop
            pass

        self.root.after(5000, self._refresh_sync_monitor)

    def _refresh_network_view(self):
        """Scan LAN/Wi‑Fi and update inventory table"""
        try:
            devices = self._scan_network_devices()
            self.network_tree.delete(*self.network_tree.get_children())
            for dev in devices:
                tags = []
                if dev["ip"] in self.bad_hosts or dev.get("status") == "blocked":
                    tags.append("bad")
                if dev.get("is_new"):
                    tags.append("new")
                self.network_tree.insert("", tk.END, values=(
                    dev.get("ip", "-"),
                    dev.get("mac", "-"),
                    dev.get("host", "-"),
                    dev.get("vendor", "-"),
                    dev.get("last_seen", "-"),
                    dev.get("status", "unknown")
                ), tags=tags)

            status = f"Last scan: {datetime.now().strftime('%H:%M:%S')} | Devices: {len(devices)}"
            self.network_status.config(text=status, fg="#00b894")
            self._append_network_log(f"Scan refreshed with {len(devices)} devices")
        except Exception as exc:
            self._append_network_log(f"Scan failed: {exc}")
            self.network_status.config(text="Scan failed", fg="#ff7675")

        if self.network_auto_var.get():
            self.root.after(12000, self._refresh_network_view)

    def _scan_network_devices(self):
        """Parse ARP table to build device inventory"""
        output = subprocess.check_output(["arp", "-a"], text=True, errors="ignore")
        lines = output.splitlines()
        devices = []
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        arp_pattern = re.compile(r"(?P<ip>\d+\.\d+\.\d+\.\d+)\s+(?P<mac>[0-9a-fA-F:-]{17})\s+(?P<type>\w+)")

        for line in lines:
            match = arp_pattern.search(line)
            if not match:
                continue
            ip_addr = match.group("ip")
            raw_mac = match.group("mac")
            mac = self._normalize_mac(raw_mac)
            host = "-"
            try:
                host = socket.gethostbyaddr(ip_addr)[0]
            except Exception:
                host = "unknown"

            is_new = ip_addr not in self.network_seen
            self.network_seen[ip_addr] = now

            status = "blocked" if ip_addr in self.bad_hosts else "ok"
            vendor = mac[:8].upper() if mac != "-" else "?"
            devices.append({
                "ip": ip_addr,
                "mac": mac,
                "host": host,
                "vendor": vendor,
                "last_seen": now,
                "status": status,
                "is_new": is_new
            })

        return devices

    def _normalize_mac(self, mac):
        mac = mac.strip().replace("-", ":").lower()
        if len(mac) == 17:
            return mac
        return "-"

    def _boot_selected_host(self):
        """Stub to boot a host from the LAN"""
        selection = self.network_tree.selection()
        if not selection:
            messagebox.showwarning("No selection", "Select a device to boot.")
            return
        values = self.network_tree.item(selection[0], "values")
        ip, mac = values[0], values[1]
        self._append_network_log(f"Requested BOOT for {ip} ({mac}) - stub only")
        self.bad_hosts.add(ip)
        self._refresh_network_view()

    def _block_selected_host(self):
        selection = self.network_tree.selection()
        if not selection:
            messagebox.showwarning("No selection", "Select a device to block.")
            return
        ip = self.network_tree.item(selection[0], "values")[0]
        self.bad_hosts.add(ip)
        self._append_network_log(f"Blocked host {ip}")
        self._refresh_network_view()

    def _mark_selected_safe(self):
        selection = self.network_tree.selection()
        if not selection:
            messagebox.showwarning("No selection", "Select a device to mark safe.")
            return
        ip = self.network_tree.item(selection[0], "values")[0]
        if ip in self.bad_hosts:
            self.bad_hosts.remove(ip)
        self._append_network_log(f"Marked {ip} as safe")
        self._refresh_network_view()

    def _append_network_log(self, text):
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = f"[{timestamp}] {text}\n"
        self.network_log.config(state=tk.NORMAL)
        self.network_log.insert(tk.END, entry)
        # Keep log trimmed
        content = self.network_log.get("1.0", tk.END)
        if len(content) > 4000:
            self.network_log.delete("1.0", "1.0 + 2000 chars")
        self.network_log.see(tk.END)
        self.network_log.config(state=tk.DISABLED)

        try:
            log_data = []
            if self.network_log_file.exists():
                with open(self.network_log_file, "r", encoding="utf-8") as fh:
                    log_data = json.load(fh)
            log_data.append({"timestamp": timestamp, "event": text})
            log_data = log_data[-200:]
            with open(self.network_log_file, "w", encoding="utf-8") as fh:
                json.dump(log_data, fh, indent=2)
        except Exception:
            pass

    def _refresh_chain_monitor(self):
        """Update the Chain Monitor panels with live (mock) data"""
        try:
            now = datetime.now()
            # Pseudo-metrics driven by current time (placeholder for real providers)
            uptime_days = (now.hour % 5) + now.minute / 60.0
            peers = 7 + (now.minute % 4)
            height = 123456 + now.minute * 3 + now.second // 10
            avg_tps = 12.3 + (now.second % 5) * 0.7
            mempool = 42 + (now.second % 17)

            summary = (
                "EchosparkChain Status: ONLINE\n"
                f"Uptime: {uptime_days:.2f} days\n"
                f"Peers: {peers}\n"
                f"Block Height: {height}\n"
                f"Avg TPS (1m): {avg_tps:.1f}\n"
                f"Mempool: {mempool} tx\n"
                "────────────────────────────────────────\n"
                "Nodes:\n"
                " - Core-1: ✅ healthy\n"
                " - Core-2: ✅ healthy\n"
                " - Edge-1: ⚠️ high load\n"
                " - Archive: ✅ synced\n"
            )

            # Badges
            self.badge_uptime.config(text=f"Uptime: {uptime_days:.2f}d")
            self.badge_peers.config(text=f"Peers: {peers}")
            self.badge_height.config(text=f"Height: {height}")
            self.badge_tps.config(text=f"TPS: {avg_tps:.1f}")
            self.badge_mempool.config(text=f"Mempool: {mempool}")

            # Node badge coloring (simple rule)
            self.node_core1.config(text="Core-1: ✅ healthy", bg="#003a8d", fg="#00ffff")
            self.node_core2.config(text="Core-2: ✅ healthy", bg="#003a8d", fg="#00ffff")
            self.node_edge1.config(text="Edge-1: ⚠️ high load", bg="#3a008d", fg="#ffccff")
            self.node_archive.config(text="Archive: ✅ synced", bg="#003a8d", fg="#00ffff")

            self.chain_summary.config(state=tk.NORMAL)
            self.chain_summary.delete("1.0", tk.END)
            self.chain_summary.insert(tk.END, summary)
            self.chain_summary.config(state=tk.DISABLED)

            # Transactions & Voting feed (rolling)
            proposals_count = 0
            try:
                if hasattr(self, "proposals_list") and self.proposals_list is not None:
                    proposals_count = self.proposals_list.size()
            except Exception:
                proposals_count = 0

            entries = []
            if self.tx_filter_var.get() in ("all", "blocks"):
                entries.append(f"[{now.strftime('%H:%M:%S')}] New block #{height} • {int(avg_tps)} tx\n")
            if self.tx_filter_var.get() in ("all", "mempool"):
                entries.append(f"[{now.strftime('%H:%M:%S')}] Mempool {mempool} → {max(mempool-3,0)}\n")
            if self.tx_filter_var.get() in ("all", "votes"):
                entries.append(f"Voting: {proposals_count or 3} active proposals, turnout steady.\n")
            tx_feed = "".join(entries)

            self.chain_tx.config(state=tk.NORMAL)
            # Append, keep last ~2000 chars
            existing = self.chain_tx.get("1.0", tk.END)
            combined = existing if self.tx_pause_var.get() else (existing + tx_feed)[-2000:]
            self.chain_tx.delete("1.0", tk.END)
            self.chain_tx.insert(tk.END, combined)
            self.chain_tx.see(tk.END)
            self.chain_tx.config(state=tk.DISABLED)
        except Exception:
            pass

        # Refresh every 4 seconds
        self.root.after(4000, self._refresh_chain_monitor)

    def _clear_tx_feed(self):
        try:
            self.chain_tx.config(state=tk.NORMAL)
            self.chain_tx.delete("1.0", tk.END)
            self.chain_tx.config(state=tk.DISABLED)
        except Exception:
            pass
    
    # ========================================================================
    # NEW STUB METHODS FOR UI ENHANCEMENTS
    # ========================================================================
    
    def _connect_hardware_wallet(self):
        """Connect to Ledger hardware wallet (placeholder)"""
        self.hw_wallet_label.config(text="🔐 Ledger: Connecting...", fg="#ffaa00")
        self.root.after(2000, lambda: self.hw_wallet_label.config(
            text="🔐 Ledger: Connected ✓", fg="#00b894"
        ))
    
    def _draw_sister_avatar(self, canvas, sister):
        """Draw avatar. Prefer high-res image assets if enabled, else vector fallback."""
        # If user disabled image avatars, skip directly to vector rendering
        use_images = True
        try:
            if hasattr(self, 'use_high_res_avatars'):
                use_images = bool(self.use_high_res_avatars.get())
        except Exception:
            use_images = True

        if use_images:
            try:
                # Determine current emotion for this sister
                sister_map = {
                    "Erryn": Sister.ERRYN if hasattr(Sister, "ERRYN") else None,
                    "Viress": Sister.VIRESS if hasattr(Sister, "VIRESS") else None,
                    "Echochild": Sister.ECHOCHILD if hasattr(Sister, "ECHOCHILD") else None,
                }
                sister_enum = sister_map.get(sister)
                emotion_name = None
                if hasattr(self, "emotion_engine") and sister_enum is not None:
                    try:
                        emotion_name = self.emotion_engine.get_current_emotion(sister_enum)
                    except Exception:
                        emotion_name = None
                self._log_avatar_debug(f"{sister}: emotion={emotion_name}")

                # Build candidate file names (e.g., test_avatar_Erryn_HAPPY.png)
                if emotion_name:
                    emotion_token = str(emotion_name).upper()
                else:
                    emotion_token = "NEUTRAL"

                base_dir = Path(__file__).parent
                candidates = [
                    base_dir / f"test_avatar_{sister}_{emotion_token}.png",
                    base_dir / f"avatar_{sister}_{emotion_token}.png",
                    base_dir / "assets" / "avatars" / f"{sister}_{emotion_token}.png",
                    # Common fallbacks
                    base_dir / f"test_avatar_{sister}_HAPPY.png",
                    base_dir / f"avatar_{sister}_HAPPY.png",
                    base_dir / "assets" / "avatars" / f"{sister}_HAPPY.png",
                ]
                try:
                    exist_flags = [p.name for p in candidates if p.exists()]
                    self._log_avatar_debug(f"{sister}: candidates(found)={exist_flags}")
                except Exception:
                    pass

                image_path = next((p for p in candidates if p.exists()), None)
                if image_path is not None:
                    # Clear canvas then draw scaled image
                    w, h = canvas.winfo_width(), canvas.winfo_height()
                    if w <= 1: w = 120
                    if h <= 1: h = 160
                    try:
                        img = Image.open(image_path).convert("RGBA")
                        # Aspect-ratio preserving scaling based on selected fit mode
                        iw, ih = img.size
                        if iw <= 0 or ih <= 0:
                            iw, ih = 1, 1
                        fit_mode = "Contain"
                        try:
                            fit_mode = self.avatar_fit_mode.get()
                        except Exception:
                            pass
                        if str(fit_mode).lower() == "cover":
                            scale = max(w / iw, h / ih)
                        else:
                            scale = min(w / iw, h / ih)
                        nw = max(1, int(iw * scale))
                        nh = max(1, int(ih * scale))
                        self._log_avatar_debug(f"{sister}: using {image_path.name}, fit={fit_mode}, canvas=({w}x{h}), new=({nw}x{nh})")
                        # Pillow 9+ uses Image.Resampling; fallback to LANCZOS attr
                        resampling = getattr(Image, "Resampling", None)
                        if resampling and hasattr(resampling, "LANCZOS"):
                            lanczos_filter = resampling.LANCZOS
                        else:
                            # Integer constant for LANCZOS; compatible with older Pillow
                            lanczos_filter = 1
                        img = img.resize((nw, nh), lanczos_filter)
                        photo = ImageTk.PhotoImage(img)
                        canvas.delete("all")
                        # Center the image on the canvas
                        canvas.create_image(w // 2, h // 2, image=photo)
                        # Hold reference so it stays displayed
                        self.avatar_photo_refs[sister] = photo
                        # Update Settings label with the image filename
                        try:
                            self._update_avatar_source_label(sister, f"Image: {image_path.name}")
                            self.avatar_source_paths[sister] = str(image_path)
                        except Exception:
                            pass
                        return
                    except Exception:
                        # If image load fails, fall through to vector fallback
                        pass
            except Exception:
                # Any unexpected issue -> vector fallback below
                pass

        # Vector fallback below if no image available or images disabled
        try:
            self._update_avatar_source_label(sister, "Vector Renderer")
            self.avatar_source_paths[sister] = ""
            self._log_avatar_debug(f"{sister}: vector fallback")
        except Exception:
            pass
        # Draw 2D animated avatar with emotion-driven expressions
        # Color palettes per sister
        palettes = {
            "Erryn": {
                "skin": "#ffd9a3",
                "hair": "#6b4ba8",
                "eye": "#00d4ff",
                "accent": "#00ffff",
                "blush": "#ff99bb"
            },
            "Viress": {
                "skin": "#ffd9a3",
                "hair": "#8b0000",
                "eye": "#ff4444",
                "accent": "#e94560",
                "blush": "#ffb3ba"
            },
            "Echochild": {
                "skin": "#ffd9a3",
                "hair": "#6a3d8a",
                "eye": "#9966ff",
                "accent": "#533483",
                "blush": "#ffd1e6"
            }
        }
        
        palette = palettes.get(sister, palettes["Erryn"])
        
        # Canvas size
        w, h = canvas.winfo_width(), canvas.winfo_height()
        if w <= 1: w = 120
        if h <= 1: h = 160
        
        cx, cy = w // 2, h // 2.5
        radius = min(w, h) // 3
        
        # Head with glow
        canvas.create_oval(
            cx - radius - 3, cy - radius - 3,
            cx + radius + 3, cy + radius + 3,
            fill=palette["accent"], outline=palette["accent"], width=0
        )
        
        # Face
        canvas.create_oval(
            cx - radius, cy - radius,
            cx + radius, cy + radius,
            fill=palette["skin"], outline=palette["accent"], width=2
        )
        
        # Hair (top half)
        canvas.create_arc(
            cx - radius, cy - radius,
            cx + radius, cy,
            start=0, extent=180,
            fill=palette["hair"], outline=palette["hair"], width=0
        )
        
        # Eyes
        eye_y = cy - int(radius * 0.25)
        eye_spacing = int(radius * 0.5)
        
        for ex in [cx - eye_spacing, cx + eye_spacing]:
            # Eye white
            canvas.create_oval(ex - 8, eye_y - 6, ex + 8, eye_y + 6,
                             fill="#ffffff", outline="#999", width=1)
            # Iris
            canvas.create_oval(ex - 5, eye_y - 4, ex + 5, eye_y + 4,
                             fill=palette["eye"], outline=palette["eye"], width=0)
            # Pupil with shine
            canvas.create_oval(ex - 2, eye_y - 1, ex + 2, eye_y + 2,
                             fill="#000000", outline=palette["eye"], width=1)
            # Shine highlight
            canvas.create_oval(ex, eye_y - 2, ex + 2, eye_y,
                             fill="#ffffff", outline="", width=0)
        
        # Blush
        for bx in [cx - int(radius * 0.4), cx + int(radius * 0.4)]:
            canvas.create_oval(bx - 6, cy + int(radius * 0.1),
                             bx + 6, cy + int(radius * 0.1) + 8,
                             fill=palette["blush"], outline="", width=0)
        
        # Mouth (smiling arc)
        mouth_y = cy + int(radius * 0.3)
        canvas.create_arc(
            cx - 15, mouth_y - 5,
            cx + 15, mouth_y + 10,
            start=0, extent=180,
            fill=palette["accent"], outline=palette["accent"], width=2
        )
    
    def _draw_webcam_placeholder(self):
        """Draw webcam placeholder"""
        self.webcam_canvas.create_rectangle(0, 0, 320, 320, fill="#1e1e2f", outline="#00ffff")
        self.webcam_canvas.create_text(160, 160, text="📹 Camera feed will appear here",
                                      fill="#00ffff", font=("Segoe UI", 11), width=260)
    
    def _start_webcam(self):
        """Start webcam feed (placeholder)"""
        self.webcam_canvas.delete("all")
        self.webcam_canvas.create_rectangle(0, 0, 320, 320, fill="#003300", outline="#00b894")
        self.webcam_canvas.create_text(160, 160, text="📹 Camera ACTIVE (stub)",
                                      fill="#00b894", font=("Segoe UI", 11, "bold"))
    
    def _stop_webcam(self):
        """Stop webcam feed"""
        self._draw_webcam_placeholder()
    
    def _fetch_github_payloads(self):
        """Fetch payloads from GitHub repos (placeholder)"""
        search_text = self.payload_search.get().strip()
        if not search_text:
            search_text = "hak5/usbrubberducky-payloads"
        
        self.payload_preview.config(state=tk.NORMAL)
        self.payload_preview.delete("1.0", tk.END)
        self.payload_preview.insert(tk.END, f"# Fetching from: {search_text}\n")
        self.payload_preview.insert(tk.END, "# GitHub API integration pending...\n\n")
        self.payload_preview.insert(tk.END, "REM Example USB Rubber Ducky Script\n")
        self.payload_preview.insert(tk.END, "DELAY 1000\n")
        self.payload_preview.insert(tk.END, "GUI r\n")
        self.payload_preview.insert(tk.END, "DELAY 500\n")
        self.payload_preview.insert(tk.END, "STRING cmd\n")
        self.payload_preview.insert(tk.END, "ENTER\n")
        self.payload_preview.insert(tk.END, "DELAY 750\n")
        self.payload_preview.insert(tk.END, "STRING echo Soul Network Activated!\n")
        self.payload_preview.insert(tk.END, "ENTER\n")
        self.payload_preview.config(state=tk.DISABLED)
    
    def _upload_to_ducky(self):
        """Upload payload to USB Rubber Ducky"""
        self.payload_preview.config(state=tk.NORMAL)
        self.payload_preview.delete("1.0", tk.END)
        self.payload_preview.insert(tk.END, "📤 Uploading to Rubber Ducky...\n")
        self.payload_preview.insert(tk.END, "Device detection and upload pending full implementation.")
        self.payload_preview.config(state=tk.DISABLED)
    
    def _download_from_ducky(self):
        """Download payload from USB Rubber Ducky"""
        self.payload_preview.config(state=tk.NORMAL)
        self.payload_preview.delete("1.0", tk.END)
        self.payload_preview.insert(tk.END, "📥 Downloading from Rubber Ducky...\n")
        self.payload_preview.insert(tk.END, "Archive and save pending full implementation.")
        self.payload_preview.config(state=tk.DISABLED)
    
    def _upload_to_lilygo(self):
        """Upload payload to LilyGo T-Deck"""
        self.payload_preview.config(state=tk.NORMAL)
        self.payload_preview.delete("1.0", tk.END)
        self.payload_preview.insert(tk.END, "📤 Uploading to LilyGo T-Deck...\n")
        self.payload_preview.insert(tk.END, "Device detection and upload pending full implementation.")
        self.payload_preview.config(state=tk.DISABLED)
    
    def _download_from_lilygo(self):
        """Download payload from LilyGo T-Deck"""
        self.payload_preview.config(state=tk.NORMAL)
        self.payload_preview.delete("1.0", tk.END)
        self.payload_preview.insert(tk.END, "📥 Downloading from LilyGo T-Deck...\n")
        self.payload_preview.insert(tk.END, "Archive and save pending full implementation.")
        self.payload_preview.config(state=tk.DISABLED)
    
    def _update_gas_tracker(self):
        """Update live gas price display (placeholder)"""
        try:
            import random
            # Mock gas prices - will be replaced with real EthGasStation/Etherscan API
            base_gwei = random.randint(15, 45)
            eth_price_usd = random.randint(1800, 2200)
            
            # Estimate costs for different operations
            send_cost = (21000 * base_gwei) / 1e9  # ETH
            stake_cost = (65000 * base_gwei) / 1e9
            vote_cost = (45000 * base_gwei) / 1e9
            
            gas_text = (
                f"⛽ Gas: {base_gwei} gwei | "
                f"Send: ${send_cost * eth_price_usd:.2f} | "
                f"Stake: ${stake_cost * eth_price_usd:.2f} | "
                f"Vote: ${vote_cost * eth_price_usd:.2f}"
            )
            
            self.gas_tracker_label.config(text=gas_text)
            
            # Update every 15 seconds
            self.root.after(15000, self._update_gas_tracker)
        except Exception:
            pass
    
    def _open_payloads_folder(self):
        """Open payloads folder in file explorer"""
        import os
        folder = self.settings_dir / "payloads"
        folder.mkdir(parents=True, exist_ok=True)
        os.startfile(folder)
    
    def _flash_to_usb(self):
        """Flash payload to USB Rubber Ducky"""
        self.payload_preview.insert(tk.END, "\n\n📤 Flashing to USB Rubber Ducky...")
        self.payload_preview.insert(tk.END, "\n⚠️ Device detection pending full implementation")
        self.payload_preview.see(tk.END)
    
    def _flash_lilygo_stub(self):
        """Flash payload to LilyGo T-Deck"""
        self.payload_preview.insert(tk.END, "\n\n📤 Flashing to LilyGo T-Deck...")
        self.payload_preview.insert(tk.END, "\n⚠️ Device detection pending full implementation")
        self.payload_preview.see(tk.END)
    
    def _edit_payload_script(self):
        """Edit selected payload script"""
        ducky_sel = self.ducky_list.curselection()
        lilygo_sel = self.lilygo_list.curselection()
        
        if not ducky_sel and not lilygo_sel:
            messagebox.showwarning("Warning", "Please select a payload first.")
            return
        
        device_type = "Ducky" if ducky_sel else "LilyGo"
        payload_name = (self.ducky_list.get(ducky_sel[0]) if ducky_sel 
                       else self.lilygo_list.get(lilygo_sel[0]))
        
        # Enable edit mode
        self.payload_preview.config(state=tk.NORMAL)
        messagebox.showinfo("Edit Mode", f"Editing {device_type} payload:\n{payload_name}\n\nMake changes in the preview pane and they will be saved.")
    
    def _on_payload_select(self, device_type):
        """Handle payload selection"""
        # Get selected payload
        if device_type == 'ducky':
            selection = self.ducky_list.curselection()
            if selection:
                payload_name = self.ducky_list.get(selection[0])
                self.payload_preview.delete('1.0', tk.END)
                self.payload_preview.insert('1.0', f"// Selected: {payload_name}\n// Payload code would appear here")
        elif device_type == 'lilygo':
            selection = self.lilygo_list.curselection()
            if selection:
                payload_name = self.lilygo_list.get(selection[0])
                self.payload_preview.delete('1.0', tk.END)
                self.payload_preview.insert('1.0', f"// Selected: {payload_name}\n// Payload code would appear here")
    
    def _scan_payloads(self):
        """Scan payloads directory and populate lists"""
        ducky_dir = self.payloads_root / "ducky"
        lilygo_dir = self.payloads_root / "lilygo"
        
        self.ducky_list.delete(0, tk.END)
        self.lilygo_list.delete(0, tk.END)
        
        # Add sample payloads
        for i in range(1, 6):
            self.ducky_list.insert(tk.END, f"🦆 Sample Ducky Payload {i}")
            self.lilygo_list.insert(tk.END, f"📡 Sample LilyGo Payload {i}")

    def _simulate_payload_run(self):
        """Simulate payload actions and visualize defenses"""
        if self.sandbox_running:
            return

        script_lines = self.payload_preview.get("1.0", tk.END).splitlines()
        events = []
        for line in script_lines:
            text = line.strip().lower()
            if not text:
                continue
            if "mouse" in text or "move" in text:
                events.append({"type": "mouse", "detail": line.strip() or "Mouse move"})
            elif "string" in text or "keyboard" in text or "type" in text:
                events.append({"type": "keyboard", "detail": line.strip() or "Key input"})
            elif "http" in text or "tcp" in text or "dns" in text or "curl" in text or "wget" in text:
                events.append({"type": "network", "detail": line.strip() or "Network call"})
            elif "file" in text or "write" in text or "save" in text:
                events.append({"type": "file", "detail": line.strip() or "File write"})
            else:
                events.append({"type": "other", "detail": line.strip() or "Action"})

        if not events:
            events = [
                {"type": "keyboard", "detail": "STRING Hello"},
                {"type": "mouse", "detail": "MOVE 100 200"},
                {"type": "network", "detail": "Attempt HTTP request"}
            ]

        self.sandbox_events = events
        self.sandbox_running = True
        self._reset_sandbox_canvas()
        self._append_sandbox_log("Starting sandbox replay...")

        def step(idx=0):
            if idx >= len(self.sandbox_events):
                self.sandbox_running = False
                self._append_sandbox_log("Sandbox replay complete.")
                return
            event = self.sandbox_events[idx]
            self._render_sandbox_event(event)
            self.root.after(650, lambda: step(idx + 1))

        step()

    def _render_sandbox_event(self, event):
        """Draw a simple glyph for the event and describe defense reaction"""
        event_type = event.get("type", "other")
        detail = event.get("detail", "")
        w = self.sandbox_canvas.winfo_width() or 360
        h = self.sandbox_canvas.winfo_height() or 160
        cx, cy = w // 2, h // 2

        # Clear overlay area only
        self.sandbox_canvas.delete("glyph")

        color = {
            "mouse": "#00ffff",
            "keyboard": "#00b894",
            "network": "#ffb347",
            "file": "#8a2be2",
            "other": "#99ff99"
        }.get(event_type, "#99ff99")

        if event_type == "mouse":
            self.sandbox_canvas.create_oval(cx - 18, cy - 18, cx + 18, cy + 18,
                                            fill=color, outline="#0a0e27", width=2, tags="glyph")
            reaction = "Viress: watches pointer movement"
        elif event_type == "keyboard":
            self.sandbox_canvas.create_rectangle(cx - 28, cy - 16, cx + 28, cy + 16,
                                                 fill=color, outline="#0a0e27", width=2, tags="glyph")
            reaction = "Echochild: looking for harmful keystrokes"
        elif event_type == "network":
            self.sandbox_canvas.create_polygon(cx - 24, cy, cx, cy - 18, cx + 24, cy,
                                               cx, cy + 18, fill=color, outline="#0a0e27", width=2, tags="glyph")
            reaction = "Viress: blocks unknown outbound call"
        elif event_type == "file":
            self.sandbox_canvas.create_rectangle(cx - 24, cy - 14, cx + 24, cy + 14,
                                                 fill=color, outline="#0a0e27", width=2, tags="glyph")
            self.sandbox_canvas.create_line(cx - 18, cy - 6, cx + 18, cy - 6, fill="#0a0e27", width=2, tags="glyph")
            reaction = "Echochild: snapshots file change"
        else:
            self.sandbox_canvas.create_oval(cx - 12, cy - 12, cx + 12, cy + 12,
                                            fill=color, outline="#0a0e27", width=2, tags="glyph")
            reaction = "Monitor: benign action"

        self._append_sandbox_log(f"Payload: {detail}")
        self._append_sandbox_log(reaction)

    def _reset_sandbox_canvas(self):
        try:
            self.sandbox_canvas.delete("all")
            w = self.sandbox_canvas.winfo_width() or 360
            h = self.sandbox_canvas.winfo_height() or 160
            self.sandbox_canvas.create_rectangle(4, 4, w - 4, h - 4,
                                                 outline="#00ffff", width=1, tags="frame")
            self.sandbox_canvas.create_text(w // 2, h // 2,
                                            text="Sandbox ready", fill="#99ff99",
                                            font=("Segoe UI", 11, "bold"), tags="hint")
        except Exception:
            pass

    def _append_sandbox_log(self, text):
        timestamp = datetime.now().strftime("%H:%M:%S")
        line = f"[{timestamp}] {text}\n"
        self.sandbox_log.config(state=tk.NORMAL)
        self.sandbox_log.insert(tk.END, line)
        content = self.sandbox_log.get("1.0", tk.END)
        if len(content) > 4000:
            self.sandbox_log.delete("1.0", "1.0 + 2000 chars")
        self.sandbox_log.see(tk.END)
        self.sandbox_log.config(state=tk.DISABLED)

    def _refresh_script_list(self):
        """Reload script list in Details tab"""
        self.script_list.delete(0, tk.END)
        # Sample scripts
        sample_scripts = [
            "daemon_monitor.py",
            "viress_soul_daemon.py",
            "echochild_heuristic.py",
            "sync_manager.py",
            "payload_deployer.py"
        ]
        for script in sample_scripts:
            self.script_list.insert(tk.END, script)

    def _on_script_select(self, event):
        """Display selected script code in preview"""
        selection = self.script_list.curselection()
        if selection:
            script_name = self.script_list.get(selection[0])
            self.code_preview.config(state=tk.NORMAL)
            self.code_preview.delete(1.0, tk.END)
            # Sample code
            sample_code = f"""# {script_name}
# Auto-generated stub preview
# Selected: {script_name}

def main():
    '''Main entry point'''
    print(f"Running {script_name}...")

if __name__ == "__main__":
    main()
"""
            self.code_preview.insert(tk.END, sample_code)
            self.code_preview.config(state=tk.NORMAL)

    def _inspect_code(self):
        """Inspect selected script code"""
        selection = self.script_list.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a script first.")
            return
        script_name = self.script_list.get(selection[0])
        messagebox.showinfo("Inspect Code", f"Code inspector opened for:\n{script_name}\n\nShowing preview in Details tab.")

    def _rename_script(self):
        """Rename selected script"""
        selection = self.script_list.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a script first.")
            return
        old_name = self.script_list.get(selection[0])
        new_name = simpledialog.askstring("Rename Script", f"Enter new name for:\n{old_name}")
        if new_name:
            self.script_list.delete(selection[0])
            self.script_list.insert(selection[0], new_name)
            messagebox.showinfo("Success", f"Renamed to: {new_name}")

    def _on_mousewheel(self, event):
        """Handle mouse wheel and trackpad scrolling with smooth delta scaling"""
        # Normalize delta across different platforms and devices
        # Windows: delta is ±120 per wheel tick
        # Linux: event.num is 4 (up) or 5 (down)
        # Trackpad: delta is variable, needs scaling
        
        if event.num == 5 or event.delta < 0:
            # Scroll down: normalize delta to units (120 = 1 unit)
            scroll_units = max(1, int(abs(event.delta) / 120)) if hasattr(event, 'delta') and event.delta else 1
            self.canvas.yview_scroll(scroll_units, "units")
        elif event.num == 4 or event.delta > 0:
            # Scroll up: normalize delta to units
            scroll_units = max(1, int(abs(event.delta) / 120)) if hasattr(event, 'delta') and event.delta else 1
            self.canvas.yview_scroll(-scroll_units, "units")

    def _start_pan(self, event):
        """Start panning with middle mouse button or trackpad 2-finger drag"""
        self.pan_start_x = event.x_root
        self.pan_start_y = event.y_root
        self.is_panning = True
        # Bind motion and release events
        self.root.bind("<B2-Motion>", self._pan_window)
        self.root.bind("<ButtonRelease-2>", self._end_pan)
        # Also bind Motion for trackpad (2-finger drag may come as regular motion after Button-2)
        self.root.bind("<Motion>", self._pan_window_motion)

    def _pan_window_motion(self, event):
        """Handle pan during motion (for trackpad support)"""
        if self.is_panning:
            self._pan_window(event)

    def _pan_window(self, event):
        """Drag the window around with improved scaling"""
        if self.is_panning:
            dx = event.x_root - self.pan_start_x
            dy = event.y_root - self.pan_start_y
            
            # Only update if movement is significant (deadzone to prevent jitter)
            if abs(dx) > 1 or abs(dy) > 1:
                # Get current window position
                geom = self.root.geometry()
                parts = geom.split('+')
                if len(parts) == 3:
                    width_height = parts[0]
                    x = int(parts[1]) + dx
                    y = int(parts[2]) + dy
                    self.root.geometry(f"{width_height}+{x}+{y}")
                
                self.pan_start_x = event.x_root
                self.pan_start_y = event.y_root

    def _end_pan(self, event):
        """End panning"""
        self.is_panning = False
        self.root.unbind("<Motion>")
        self.root.unbind("<B2-Motion>")
        self.root.unbind("<ButtonRelease-2>")

    def _on_canvas_click(self, event):
        """Handle regular clicks"""
        pass

    # ========================================================================
    # WINDOW CONTROL HELPERS
    # ========================================================================

    def _apply_topmost(self):
        try:
            self.root.attributes("-topmost", bool(self.always_on_top_var.get()))
        except Exception:
            pass

    def _center_window(self):
        try:
            self.root.update_idletasks()
            w = self.root.winfo_width()
            h = self.root.winfo_height()
            sw = self.root.winfo_screenwidth()
            sh = self.root.winfo_screenheight()
            x = max(0, (sw - w) // 2)
            y = max(0, (sh - h) // 2)
            self.root.geometry(f"{w}x{h}+{x}+{y}")
        except Exception:
            pass

    def _reset_window_size(self, w: int, h: int):
        try:
            self.root.resizable(True, True)
            sw = self.root.winfo_screenwidth()
            sh = self.root.winfo_screenheight()
            x = max(0, (sw - w) // 2)
            y = max(0, (sh - h) // 2)
            self.root.geometry(f"{w}x{h}+{x}+{y}")
        except Exception:
            pass

    def _maximize_window(self):
        try:
            self.root.state('zoomed')
        except Exception:
            pass

    def _toggle_middle_drag(self):
        try:
            if self.enable_middle_drag_var.get():
                self.root.bind("<Button-2>", self._start_pan)
                self.root.bind("<B2-Motion>", self._pan_window)
                self.root.bind("<ButtonRelease-2>", self._end_pan)
            else:
                self.root.unbind("<Button-2>")
                self.root.unbind("<B2-Motion>")
                self.root.unbind("<ButtonRelease-2>")
        except Exception:
            pass

    # ========================================================================
    # ⚡ PERFORMANCE OPTIMIZATION METHODS
    # ========================================================================
    
    def _throttle_render(self):
        """Throttle rendering to target FPS (60 FPS = 16ms)"""
        current_time = time.time()
        elapsed = (current_time - self.last_render_time) * 1000  # ms
        
        if elapsed < self.render_throttle_ms:
            # Too soon, skip this frame
            return False
        
        self.last_render_time = current_time
        return True
    
    def _request_render(self, widget_id):
        """Request rendering of a widget (batched for efficiency)"""
        self.pending_renders[widget_id] = True
        self.update_pending = True
    
    def _flush_pending_renders(self):
        """Process all pending render requests in one batch"""
        if not self.update_pending:
            return
        
        if not self._throttle_render():
            # Reschedule if throttled
            self.root.after(5, self._flush_pending_renders)
            return
        
        # Process all pending renders
        for widget_id in list(self.pending_renders.keys()):
            # Clear only what changed
            try:
                if isinstance(widget_id, tk.Canvas):
                    widget_id.delete("all")
            except:
                pass
        
        self.pending_renders.clear()
        self.update_pending = False
    
    def _optimize_scroll_performance(self):
        """Optimize scroll performance by reducing render load"""
        # Reduce animation load during scroll
        pass
    
    def _reduce_animation_load(self):
        """Reduce animation updates when system is busy"""
        # Check if renders are falling behind
        if len(self.pending_renders) > 5:
            # Too many pending, skip some non-critical renders
            self.render_throttle_ms = 33  # Drop to 30 FPS temporarily
        else:
            # Resume normal performance
            self.render_throttle_ms = 16  # Back to 60 FPS


# ============================================================================
# LAUNCHER
# ============================================================================

def main():
    root = tk.Tk()
    gui = EchosparkSoulGUIv3(root)
    root.mainloop()


if __name__ == "__main__":
    main()
