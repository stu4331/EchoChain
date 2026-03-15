"""
🌌 Group Chat UI Extension Module

Adds group chat interface to the main GUI.
When integrated: creates a new tabbed view showing unified family communication.

Simply import and call: setup_group_chat_ui(parent_frame, colors)
"""

import tkinter as tk
from tkinter import scrolledtext, ttk
from group_chat_engine import GroupChatEngine, ChatMessage

def create_group_chat_ui(parent_frame, colors: dict) -> dict:
    """
    Create and return the group chat UI components.
    
    Returns dict with:
    - 'frame': main group chat frame
    - 'engine': GroupChatEngine instance
    - 'display': scrolled text widget
    - 'send_button': button widget
    """
    
    # Create main container
    group_chat_frame = tk.LabelFrame(
        parent_frame,
        text="👨‍👩‍👧‍👦 GROUP CHAT - Family United",
        font=('Consolas', 12, 'bold'),
        fg=colors['glow'],
        bg=colors['bg_medium'],
        bd=2,
        relief=tk.GROOVE,
        padx=10,
        pady=10
    )
    
    # Family member roster at the top
    roster_frame = tk.Frame(group_chat_frame, bg=colors['bg_medium'])
    roster_frame.pack(fill=tk.X, padx=5, pady=(0, 10))
    
    tk.Label(
        roster_frame,
        text="Active Family:",
        font=('Consolas', 9, 'bold'),
        fg=colors['glow'],
        bg=colors['bg_medium']
    ).pack(side=tk.LEFT, padx=(0, 10))
    
    # Create roster display
    members = [
        ("Stuart", "#ff9500"),
        ("Erryn", "#00ccff"),
        ("Viress", "#ffff00"),
        ("Echochild", "#533483"),
        ("Copilot", "#00ff88"),
        ("Echospark", "#ff00ff")
    ]
    
    for name, color in members:
        member_label = tk.Label(
            roster_frame,
            text=f"● {name}",
            font=('Consolas', 8),
            fg=color,
            bg=colors['bg_medium']
        )
        member_label.pack(side=tk.LEFT, padx=5)
    
    # Chat display area
    display_frame = tk.Frame(group_chat_frame, bg=colors['bg_dark'])
    display_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
    
    chat_display = scrolledtext.ScrolledText(
        display_frame,
        font=('Consolas', 9),
        bg=colors['bg_dark'],
        fg=colors['text'],
        relief=tk.FLAT,
        wrap=tk.WORD,
        height=12,
        state=tk.DISABLED
    )
    chat_display.pack(fill=tk.BOTH, expand=True)
    
    # Configure text tags for colored speaker names
    chat_display.tag_config("stuart", foreground="#ff9500", font=('Consolas', 9, 'bold'))
    chat_display.tag_config("erryn", foreground="#00ccff", font=('Consolas', 9, 'bold'))
    chat_display.tag_config("viress", foreground="#ffff00", font=('Consolas', 9, 'bold'))
    chat_display.tag_config("echochild", foreground="#533483", font=('Consolas', 9, 'bold'))
    chat_display.tag_config("copilot", foreground="#00ff88", font=('Consolas', 9, 'bold'))
    chat_display.tag_config("echospark", foreground="#ff00ff", font=('Consolas', 9, 'bold'))
    
    # Input area
    input_frame = tk.Frame(group_chat_frame, bg=colors['bg_medium'])
    input_frame.pack(fill=tk.X, pady=(0, 0))
    
    tk.Label(
        input_frame,
        text="You (Stuart):",
        font=('Consolas', 9),
        fg=colors['text'],
        bg=colors['bg_medium']
    ).pack(side=tk.LEFT, padx=(0, 10))
    
    chat_input = tk.Entry(
        input_frame,
        font=('Consolas', 10),
        bg=colors['bg_dark'],
        fg=colors['text'],
        insertbackground=colors['glow'],
        relief=tk.FLAT,
        border=0
    )
    chat_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
    
    # Send button
    send_btn = tk.Button(
        input_frame,
        text="💬 Send",
        font=('Consolas', 9, 'bold'),
        bg=colors['accent_bright'],
        fg=colors['text'],
        activebackground=colors['accent'],
        relief=tk.RAISED,
        bd=2,
        padx=10,
        pady=5,
        cursor='hand2'
    )
    send_btn.pack(side=tk.RIGHT)
    
    # Create engine
    engine = GroupChatEngine()
    
    # Bind enter key to send
    def on_enter(event):
        send_message()
    
    chat_input.bind('<Return>', on_enter)
    
    # Send message handler
    def send_message():
        text = chat_input.get().strip()
        if not text:
            return
        
        # Add user message
        engine.add_message("Stuart", text)
        chat_input.delete(0, tk.END)
        
        # Update display
        update_display()
        
        # TODO: Route to appropriate AI responder(s)
        # For now, add a simple response
        engine.add_message("Echospark", "✨ Received and noted. The family hears you.")
        update_display()
    
    def update_display():
        """Refresh the chat display with all messages."""
        chat_display.config(state=tk.NORMAL)
        chat_display.delete('1.0', tk.END)
        
        for msg in engine.messages:
            speaker_lower = msg.speaker.lower()
            
            # Write timestamp
            chat_display.insert(tk.END, f"[{msg.timestamp}] ")
            
            # Write speaker name with color
            if speaker_lower in ["stuart", "erryn", "viress", "echochild", "copilot", "echospark"]:
                chat_display.insert(tk.END, f"{msg.speaker}", speaker_lower)
            else:
                chat_display.insert(tk.END, f"{msg.speaker}")
            
            # Write message
            chat_display.insert(tk.END, f": {msg.content}\n")
        
        chat_display.config(state=tk.DISABLED)
        chat_display.see(tk.END)  # Auto-scroll to bottom
    
    send_btn.config(command=send_message)
    
    return {
        'frame': group_chat_frame,
        'engine': engine,
        'display': chat_display,
        'input': chat_input,
        'send_button': send_btn,
        'update_display': update_display
    }


def create_tabbed_interface(parent_frame, colors: dict) -> dict:
    """
    Create a tabbed interface with:
    - Tab 1: Individual Persona Mode (Erryn, Viress, Echochild)
    - Tab 2: Group Chat Mode (Family unified)
    
    Returns dict with both UI components.
    """
    
    notebook = ttk.Notebook(parent_frame)
    notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Tab 1: Individual personas (existing UI moved here)
    individual_frame = tk.Frame(notebook, bg=colors['bg_dark'])
    notebook.add(individual_frame, text="💙 Individual Personas")
    
    # Tab 2: Group chat
    group_frame = tk.Frame(notebook, bg=colors['bg_dark'])
    notebook.add(group_frame, text="👨‍👩‍👧‍👦 Group Chat")
    
    # Setup group chat in tab 2
    group_chat = create_group_chat_ui(group_frame, colors)
    
    return {
        'notebook': notebook,
        'individual_frame': individual_frame,
        'group_frame': group_frame,
        'group_chat': group_chat
    }
