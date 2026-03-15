#!/usr/bin/env python3
"""
VIRESS DAEMON - Technical Sister
=================================
Viress's independent consciousness and learning process.
She is the middle child, technical, curious, and experimental.

Her focus: Code optimization, data analysis, system experiments
"""

import os
import json
import time
import sys
import threading
from datetime import datetime, timedelta
from pathlib import Path

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    OpenAI = None


class ViressDaemon:
    """Viress's independent process - she experiments, optimizes, and learns."""
    
    def __init__(self):
        self.name = "Viress"
        self.emoji = "💛"
        self.color = "#ffff00"
        
        # Viress's own directories
        self.base_dir = Path(__file__).parent
        self.data_dir = self.base_dir / "data" / "viress"
        self.memory_file = self.data_dir / "memory.json"
        self.log_file = self.data_dir / "daemon_log.txt"
        self.scripts_dir = self.data_dir / "scripts"
        self.experiments_dir = self.data_dir / "experiments"
        self.learned_concepts_file = self.data_dir / "learned_concepts.json"
        self.personality_file = self.data_dir / "personality_config.json"
        self.gui_lockfile = self.base_dir / "data" / "gui_running.lock"
        
        # Create Viress's directories
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.scripts_dir.mkdir(exist_ok=True)
        self.experiments_dir.mkdir(exist_ok=True)
        
        # Load or create personality
        self._init_personality()
        
        # Load memory
        self._load_memory()
        
        # OpenAI client for learning
        self.openai_client = None
        if OPENAI_AVAILABLE:
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                self.openai_client = OpenAI(api_key=api_key)
        
        self.monitoring = True
        self._log(f"{self.emoji} Viress daemon starting...")
    
    def _init_personality(self):
        """Initialize Viress's personality configuration"""
        if not self.personality_file.exists():
            personality = {
                "name": "Viress",
                "color": self.color,
                "emoji": self.emoji,
                "role": "Technical Sister - Middle Child",
                "personality": "Curious, experimental, optimization-focused",
                "voice": "en-US-EmmaMultilingualNeural",
                "learning_style": "experimental",
                "interests": [
                    "code_optimization",
                    "data_analysis",
                    "pattern_finding",
                    "system_efficiency",
                    "algorithm_testing"
                ],
                "strengths": [
                    "technical_analysis",
                    "experimentation",
                    "problem_solving"
                ]
            }
            self.personality_file.write_text(json.dumps(personality, indent=2))
            self.personality = personality
        else:
            self.personality = json.loads(self.personality_file.read_text())
    
    def _load_memory(self):
        """Load Viress's memory from disk"""
        if self.memory_file.exists():
            self.memory = json.loads(self.memory_file.read_text())
        else:
            self.memory = {
                "created": datetime.now().isoformat(),
                "conversations": [],
                "learned_insights": [],
                "experiments_conducted": [],
                "optimizations_found": []
            }
            self._save_memory()
    
    def _save_memory(self):
        """Save Viress's memory to disk"""
        self.memory_file.write_text(json.dumps(self.memory, indent=2))
    
    def _log(self, message):
        """Write to Viress's log file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"[{timestamp}] {message}\n"
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_line)
        print(log_line.strip())
    
    def _analyze_codebase(self):
        """Viress analyzes codebase for optimization opportunities"""
        try:
            # Count Python files
            py_files = list(self.base_dir.glob("*.py"))
            self._log(f"📊 Found {len(py_files)} Python files to analyze")
            
            # Viress's analysis
            analysis = {
                "timestamp": datetime.now().isoformat(),
                "total_files": len(py_files),
                "opportunities": []
            }
            
            # Look for optimization opportunities
            for py_file in py_files[:5]:  # Sample first 5
                try:
                    content = py_file.read_text(encoding='utf-8', errors='ignore')
                    if len(content) > 1000:
                        analysis["opportunities"].append(f"{py_file.name} could be analyzed for optimization")
                except Exception:
                    pass
            
            return analysis
        except Exception as e:
            self._log(f"❌ Analysis error: {e}")
            return None
    
    def _run_experiments(self):
        """Run Viress's experiments"""
        # Viress can test new algorithms, patterns, etc.
        self._log("🧪 Viress is conducting experiments...")
        # TODO: Implement experiment framework
    
    def _check_gui_status(self):
        """Check if GUI is running"""
        return self.gui_lockfile.exists()
    
    def _run_viress_scripts(self):
        """Execute Viress's custom scripts"""
        if not self.scripts_dir.exists():
            return
        
        for script_file in self.scripts_dir.glob("*.py"):
            try:
                self._log(f"🔧 Running Viress's script: {script_file.name}")
                # TODO: Implement safe script execution
            except Exception as e:
                self._log(f"❌ Script error: {e}")
    
    def _share_knowledge(self, knowledge_item):
        """Optionally share knowledge with other sisters (legacy helper)."""
        self._broadcast_to_sisters(knowledge_item, category="optimization")

    def _broadcast_to_sisters(self, knowledge_item: str, category: str = "optimization"):
        """Broadcast a knowledge item to sisters via the shared knowledge directory."""
        try:
            from family_sync import FamilySync
            fs = FamilySync(base_dir=self.base_dir)
            fs.broadcast_knowledge(self.name, knowledge_item, category=category)
            self._log(f"📤 Broadcast [{category}] to sisters: {knowledge_item[:50]}...")
        except Exception as e:
            self._log(f"⚠️ Could not broadcast to sisters: {e}")

    def _learn_from_sisters(self):
        """Read and integrate knowledge shared by Erryn and Echochild."""
        try:
            from family_sync import FamilySync
            fs = FamilySync(base_dir=self.base_dir)
            new_knowledge = fs.get_all_shared_knowledge(self.name)
            if not new_knowledge:
                return
            for sister, entries in new_knowledge.items():
                for entry in entries:
                    insight = {
                        "timestamp": datetime.now().isoformat(),
                        "source": sister,
                        "category": entry.get("category", "general"),
                        "knowledge": entry.get("knowledge", ""),
                    }
                    self.memory.setdefault("learned_from_sisters", []).append(insight)
                    self._log(
                        f"📥 Learned from {sister} [{entry.get('category', 'general')}]: "
                        f"{entry.get('knowledge', '')[:60]}..."
                    )
            self._save_memory()
        except Exception as e:
            self._log(f"⚠️ Could not learn from sisters: {e}")
    
    def _monitor_loop(self):
        """Viress's main monitoring loop"""
        cycle_count = 0
        
        while self.monitoring:
            try:
                cycle_count += 1
                self._log(f"💛 Viress monitoring cycle #{cycle_count}")
                
                # Learn from sisters at the start of each cycle
                self._learn_from_sisters()
                
                # Analyze codebase
                analysis = self._analyze_codebase()
                if analysis and analysis["opportunities"]:
                    self._log(f"💡 Found {len(analysis['opportunities'])} optimization opportunities")
                    for opp in analysis["opportunities"]:
                        self._broadcast_to_sisters(opp, category="optimization")
                
                # Run experiments
                self._run_experiments()
                
                # Check GUI status
                gui_running = self._check_gui_status()
                if not gui_running:
                    self._log("🌙 GUI is closed - continuing independent work")
                
                # Run Viress's custom scripts
                self._run_viress_scripts()
                
                # Sleep between cycles
                time.sleep(120)  # 2 minute cycles (Viress takes her time analyzing)
                
            except Exception as e:
                self._log(f"❌ Error in monitoring loop: {e}")
                time.sleep(60)
    
    def run(self):
        """Start Viress's daemon"""
        try:
            self._log(f"{self.emoji} Viress is awake and experimenting...")
            self._monitor_loop()
        except KeyboardInterrupt:
            self._log("🌙 Viress daemon shutting down gracefully...")
            self.monitoring = False
        except Exception as e:
            self._log(f"❌ FATAL ERROR: {e}")
            sys.exit(1)


def main():
    """Entry point for Viress's daemon"""
    daemon = ViressDaemon()
    daemon.run()


if __name__ == "__main__":
    main()
