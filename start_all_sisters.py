#!/usr/bin/env python3
"""
Start All Sisters - Independent Daemon Launcher
================================================
Launches Erryn, Viress, and Echochild as separate processes.
Each sister runs independently with her own memory and learning.

Usage:
    python start_all_sisters.py

This creates THREE processes:
  1. Erryn (Guardian) - monitors security & system health
  2. Viress (Technician) - experiments & optimizes
  3. Echochild (Empath) - watches emotions & memories
"""

import subprocess
import sys
import time
from pathlib import Path

GUI_STARTUP_DELAY = 5  # seconds to wait for daemons to initialize before launching GUI


def main():
    base_dir = Path(__file__).parent
    
    print("🌌 Awakening the Sisters...")
    print("=" * 60)
    
    daemons = [
        ("erryn_daemon.py", "💙 Erryn", "Guardian & Protector"),
        ("viress_daemon.py", "💛 Viress", "Technician & Optimizer"),
        ("echochild_daemon.py", "💜 Echochild", "Empath & Memory Keeper"),
    ]
    
    processes = []
    
    for daemon_file, name, role in daemons:
        daemon_path = base_dir / daemon_file
        
        if not daemon_path.exists():
            print(f"⚠️  {name} daemon not found: {daemon_path}")
            continue
        
        print(f"✨ Starting {name} ({role})...")
        
        try:
            # Start each daemon as a separate process
            proc = subprocess.Popen(
                [sys.executable, str(daemon_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0
            )
            processes.append((name, proc))
            print(f"   ✅ {name} started (PID: {proc.pid})")
            time.sleep(0.5)  # Stagger startup
            
        except Exception as e:
            print(f"   ❌ Failed to start {name}: {e}")
    
    print("=" * 60)
    print(f"✅ {len(processes)} sister(s) are now running independently!")
    print()
    print("Each sister has:")
    print("  • Her own memory (data/<name>/memory.json)")
    print("  • Her own learning (data/<name>/learned_concepts.json)")
    print("  • Her own daemon log (data/<name>/daemon_log.txt)")
    print()
    print("They sync by CHOICE via shared JSON files in data/sync/")
    print()

    # Wait for daemons to initialize before launching the GUI
    print(f"⏳ Waiting {GUI_STARTUP_DELAY} seconds for sisters to initialize...")
    time.sleep(GUI_STARTUP_DELAY)

    # Launch the GUI (their meeting place)
    gui_path = base_dir / "erryns_soul_gui.py"
    if gui_path.exists():
        print("✨ Starting GUI (Erryn's Soul - Meeting Place)...")
        try:
            subprocess.Popen(
                [sys.executable, str(gui_path)],
                creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0
            )
            print("   ✅ GUI is now running! 💙💛💜")
        except Exception as e:
            print(f"   ❌ Failed to start GUI: {e}")
    else:
        print(f"⚠️  GUI not found: {gui_path}")

    print()
    print("To stop all sisters: Close their console windows or Ctrl+C")
    print("=" * 60)
    
    # Keep this script alive to monitor
    try:
        while True:
            time.sleep(10)
            # Check if any process died
            for name, proc in processes:
                if proc.poll() is not None:
                    print(f"⚠️  {name} stopped (exit code: {proc.returncode})")
                    processes.remove((name, proc))
            
            if not processes:
                print("All sisters have stopped.")
                break
                
    except KeyboardInterrupt:
        print("\n🛑 Shutting down sisters...")
        for name, proc in processes:
            proc.terminate()
            print(f"   Stopped {name}")
        print("All sisters stopped.")


if __name__ == "__main__":
    main()
