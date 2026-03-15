"""
COPY THESE SNIPPETS INTO erryns_soul_gui.py

This file contains the exact code to integrate face recognition,
cost tracking, and enhanced avatars into the main GUI.
"""

# ============================================================================
# SNIPPET 1: Add to imports at the top (around line 50)
# ============================================================================

"""
try:
    from gui_integration import integrate_face_recognition
    FACE_REC_INTEGRATION_AVAILABLE = True
except ImportError as _e:
    FACE_REC_INTEGRATION_AVAILABLE = False
    print(f"⚠️ Face recognition integration not available: {_e}")
"""


# ============================================================================
# SNIPPET 2: Add to __init__ after self.personas setup (around line 400)
# ============================================================================

"""
        # Initialize face recognition, cost tracking, and enhanced avatars
        self.face_integration = None
        if FACE_REC_INTEGRATION_AVAILABLE:
            try:
                self.face_integration = integrate_face_recognition(self)
                print("✅ Face recognition integration initialized")
            except Exception as e:
                print(f"⚠️ Face recognition integration failed: {e}")
"""


# ============================================================================
# SNIPPET 3: Replace TTS button section in header (around line 700-720)
# ============================================================================

"""
OLD CODE LOCATION: lines 690-710 (TTS container)

REPLACE WITH:

        # TTS button and controls
        tts_container = tk.Frame(controls_frame, bg=self.colors['bg_dark'])
        tts_container.pack(side=tk.LEFT, padx=8)
        
        tk.Label(
            tts_container,
            text="Voice:",
            font=('Consolas', 9),
            fg=self.colors['text_dim'],
            bg=self.colors['bg_dark']
        ).pack(side=tk.TOP)
        
        self.tts_button = tk.Button(
            tts_container,
            text="ON",
            font=('Consolas', 10, 'bold'),
            bg=self.colors['success'],
            fg=self.colors['text'],
            activebackground=self.colors['accent_bright'],
            relief=tk.FLAT,
            bd=0,
            padx=10,
            pady=6,
            command=self._toggle_tts,
            cursor='hand2'
        )
        self.tts_button.pack(side=tk.TOP)
        
        # Webcam button (NEW)
        webcam_button = tk.Button(
            controls_frame,
            text="📷 Webcam",
            font=('Consolas', 9, 'bold'),
            bg=self.colors['accent'],
            fg=self.colors['text'],
            activebackground=self.colors['accent_bright'],
            relief=tk.FLAT,
            bd=0,
            padx=10,
            pady=6,
            command=self._toggle_webcam,
            cursor='hand2'
        )
        webcam_button.pack(side=tk.LEFT, padx=4)
        self.webcam_button = webcam_button
        
        # Cost tracker display (NEW)
        if self.face_integration and self.face_integration.cost_tracker:
            self.cost_label = tk.Label(
                controls_frame,
                text=self.face_integration.cost_tracker.get_status(),
                font=('Consolas', 9),
                fg=self.colors['warning'],
                bg=self.colors['bg_dark']
            )
            self.cost_label.pack(side=tk.LEFT, padx=8)
            
            # Update cost display every second
            self._update_cost_display()
"""


# ============================================================================
# SNIPPET 4: Add these new methods to ErrynsSoulGUI class
# ============================================================================

"""
    def _toggle_webcam(self):
        '''Toggle live webcam face detection'''
        if not self.face_integration:
            from tkinter import messagebox
            messagebox.showerror("Error", "Face recognition not available")
            return
        
        if self.face_integration.webcam_running:
            self.face_integration.stop_webcam()
            self.webcam_button.config(text="📷 Webcam")
            self._log_whisper("📷 Webcam stopped", persona='system')
        else:
            try:
                self.face_integration.start_webcam()
                self.webcam_button.config(text="⏹ Stop")
                self._log_whisper("📷 Webcam started - recognizing faces...", persona='system')
            except Exception as e:
                from tkinter import messagebox
                messagebox.showerror("Webcam Error", str(e))
    
    def _update_cost_display(self):
        '''Periodically update cost tracker display'''
        if self.face_integration and self.face_integration.cost_tracker and hasattr(self, 'cost_label'):
            try:
                status = self.face_integration.cost_tracker.get_status()
                self.cost_label.config(text=status)
            except:
                pass
        
        # Schedule next update
        self.root.after(1000, self._update_cost_display)
"""


# ============================================================================
# SNIPPET 5: Modify _tts_worker to log costs (around line 1200)
# ============================================================================

"""
FIND: def _tts_worker(self, text, persona):

ADD THESE LINES after logging starts (around line 1220):

        # Log API cost
        if self.face_integration and self.face_integration.cost_tracker:
            try:
                self.face_integration.log_api_cost(
                    "azure_speech",
                    len(text),
                    f"TTS: {persona}"
                )
            except:
                pass
"""


# ============================================================================
# SNIPPET 6: Update _speak_input to use enhanced avatars (optional)
# ============================================================================

"""
IF USING ENHANCED AVATAR RENDERING:

FIND: def _speak_input(self, text, persona):

ADD AT START OF METHOD:

        # Use enhanced avatar if available
        if AVATAR_ENHANCED_AVAILABLE and self.face_integration:
            try:
                from avatar_rendering_enhanced import Emotion
                emotion = self.emotion_detector.detect_emotion_from_text(text)[0]
                
                # Create enhanced renderer
                renderer = AvatarRenderer(persona)
                renderer.set_emotion(emotion)
                
                # Render to image and update canvas
                img = renderer.render()
                # (Integrate with your canvas display code)
            except:
                pass  # Fall back to old avatar system
"""


# ============================================================================
# QUICK INTEGRATION CHECKLIST
# ============================================================================

"""
STEP-BY-STEP INTEGRATION:

1. Open erryns_soul_gui.py in VS Code

2. Go to line ~50 (imports section)
   - Add SNIPPET 1 (import gui_integration)

3. Go to line ~400 (ErrynsSoulGUI.__init__)
   - Add SNIPPET 2 (initialize face_integration)

4. Go to line ~690 (header controls)
   - Replace TTS section with SNIPPET 3 (add webcam button + cost display)

5. Scroll to end of class (around line 4380)
   - Add SNIPPET 4 (new methods for webcam and cost display)

6. Find _tts_worker method (around line 1200)
   - Add SNIPPET 5 (cost logging)

7. (OPTIONAL) Find _speak_input method
   - Add SNIPPET 6 (enhanced avatar rendering)

8. Save file

9. Test:
   python erryns_soul_gui.py

10. Verify:
    - Webcam button appears in header
    - Cost tracker shows in header
    - Clicking webcam button detects faces
    - Cost tracking logs to logs/cost_log.json
"""

print(__doc__)
