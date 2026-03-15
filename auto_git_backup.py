"""
Automatic Git Backup - saves every 5 minutes
Runs in background, non-intrusive commits
Set as a task or run in background terminal
"""

import os
import subprocess
import time
from datetime import datetime
from pathlib import Path

class AutoGitBackup:
    def __init__(self, repo_path: Path = Path("."), interval_minutes: int = 5):
        self.repo_path = Path(repo_path)
        self.interval = interval_minutes * 60  # Convert to seconds
        self.running = False
        
        # Verify git repo exists
        if not (self.repo_path / ".git").exists():
            print(f"❌ Not a git repository: {self.repo_path}")
            raise RuntimeError("Not a git repo")
        
        print(f"✅ Auto-backup initialized")
        print(f"   Path: {self.repo_path}")
        print(f"   Interval: {interval_minutes} min")
    
    def run(self):
        """Start auto-backup loop"""
        self.running = True
        print(f"🔄 Auto-backup started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Press Ctrl+C to stop\n")
        
        try:
            while self.running:
                try:
                    self._commit()
                    time.sleep(self.interval)
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"⚠️  Backup error: {e}")
                    time.sleep(30)  # Retry after 30s
        
        except KeyboardInterrupt:
            pass
        finally:
            print(f"\n✋ Auto-backup stopped at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    def _commit(self):
        """Perform git commit"""
        try:
            # Check if there are changes
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if not result.stdout.strip():
                # No changes
                return
            
            # Add all changes
            subprocess.run(
                ["git", "add", "-A"],
                cwd=self.repo_path,
                capture_output=True,
                timeout=10
            )
            
            # Commit with timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message = f"Auto-backup: {timestamp}"
            
            result = subprocess.run(
                ["git", "commit", "-m", message],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                print(f"✅ {timestamp} - Backup saved")
            else:
                if "nothing to commit" not in result.stderr.lower():
                    print(f"⚠️  {timestamp} - {result.stderr}")
        
        except subprocess.TimeoutExpired:
            print(f"⏱️  Commit timeout")
        except Exception as e:
            print(f"❌ Commit failed: {e}")


if __name__ == "__main__":
    import sys
    
    # Get interval from command line (default 5 minutes)
    interval = 5
    if len(sys.argv) > 1:
        try:
            interval = int(sys.argv[1])
        except ValueError:
            print(f"Usage: python auto_git_backup.py [interval_minutes]")
            print(f"Default: 5 minutes")
    
    backup = AutoGitBackup(interval_minutes=interval)
    backup.run()
