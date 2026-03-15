"""
Application Access & Control System
Allows the sisters to access and control any installed application on the computer
"""

import os
import subprocess
import winreg
import webbrowser
import urllib.parse
from pathlib import Path
from typing import List, Dict, Optional
import json
from datetime import datetime

class ApplicationRegistry:
    """
    Scans and maintains a registry of all installed applications on Windows
    """
    
    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.registry_file = self.data_dir / "application_registry.json"
        
        # Applications the sisters have access to
        self.applications = {}
        
        # Load existing registry
        self.load_registry()
        
    def scan_installed_applications(self) -> List[Dict]:
        """
        Scan Windows registry for all installed applications
        Returns list of applications with name, path, publisher
        """
        applications = []
        
        # Registry paths to check
        registry_paths = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        ]
        
        for hkey, path in registry_paths:
            try:
                key = winreg.OpenKey(hkey, path)
                for i in range(winreg.QueryInfoKey(key)[0]):
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        subkey = winreg.OpenKey(key, subkey_name)
                        
                        # Read application info
                        try:
                            name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                            
                            # Try to get install location or executable path
                            install_location = None
                            try:
                                install_location = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                            except:
                                pass
                                
                            # Try to get display icon (often points to .exe)
                            icon_path = None
                            try:
                                icon_path = winreg.QueryValueEx(subkey, "DisplayIcon")[0]
                            except:
                                pass
                                
                            # Get publisher
                            publisher = None
                            try:
                                publisher = winreg.QueryValueEx(subkey, "Publisher")[0]
                            except:
                                pass
                                
                            # Get version
                            version = None
                            try:
                                version = winreg.QueryValueEx(subkey, "DisplayVersion")[0]
                            except:
                                pass
                            
                            applications.append({
                                "name": name,
                                "install_location": install_location,
                                "icon_path": icon_path,
                                "publisher": publisher,
                                "version": version,
                                "registry_key": subkey_name
                            })
                            
                        except:
                            pass
                            
                        subkey.Close()
                    except:
                        pass
                        
                key.Close()
            except Exception as e:
                print(f"⚠️ Could not scan registry path {path}: {e}")
                
        # Also scan common program directories
        program_dirs = [
            Path(os.environ.get('ProgramFiles', 'C:\\Program Files')),
            Path(os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)')),
            Path.home() / "AppData" / "Local" / "Programs",
        ]
        
        for prog_dir in program_dirs:
            if prog_dir.exists():
                try:
                    for item in prog_dir.iterdir():
                        if item.is_dir():
                            # Look for .exe files
                            exe_files = list(item.glob("*.exe"))
                            if exe_files:
                                # Check if not already in registry
                                if not any(app['name'] == item.name for app in applications):
                                    applications.append({
                                        "name": item.name,
                                        "install_location": str(item),
                                        "icon_path": str(exe_files[0]),
                                        "publisher": "Local Installation",
                                        "version": "Unknown",
                                        "registry_key": None
                                    })
                except Exception as e:
                    pass
                    
        # Sort by name
        applications = sorted(applications, key=lambda x: x['name'].lower())
        
        return applications
        
    def grant_access(self, app_name: str, app_path: str, sisters: List[str]):
        """
        Grant specific sisters access to an application
        
        Args:
            app_name: Display name of application
            app_path: Path to executable or install directory
            sisters: List of sister names ['Erryn', 'Viress', 'Echochild']
        """
        app_id = app_name.lower().replace(" ", "_")
        
        self.applications[app_id] = {
            "name": app_name,
            "path": app_path,
            "granted_to": sisters,
            "granted_date": datetime.now().isoformat(),
            "usage_count": 0,
            "last_used": None
        }
        
        self.save_registry()
        print(f"✅ Granted access to '{app_name}' for: {', '.join(sisters)}")
        
    def revoke_access(self, app_name: str, sisters: Optional[List[str]] = None):
        """
        Revoke access to an application
        
        Args:
            app_name: Display name of application
            sisters: List of sisters to revoke from, or None to revoke from all
        """
        app_id = app_name.lower().replace(" ", "_")
        
        if app_id in self.applications:
            if sisters is None:
                # Revoke from all
                del self.applications[app_id]
                print(f"✅ Revoked all access to '{app_name}'")
            else:
                # Revoke from specific sisters
                app = self.applications[app_id]
                app['granted_to'] = [s for s in app['granted_to'] if s not in sisters]
                
                if not app['granted_to']:
                    # No one has access anymore
                    del self.applications[app_id]
                    
                print(f"✅ Revoked access to '{app_name}' for: {', '.join(sisters)}")
                
            self.save_registry()
            
    def get_applications_for_sister(self, sister_name: str) -> List[Dict]:
        """Get all applications a specific sister has access to"""
        return [
            app for app in self.applications.values()
            if sister_name in app['granted_to']
        ]
        
    def launch_application(self, app_name: str, sister_name: str, args: Optional[List[str]] = None) -> bool:
        """
        Launch an application on behalf of a sister
        
        Args:
            app_name: Display name of application
            sister_name: Which sister is launching it
            args: Optional command-line arguments
            
        Returns:
            True if launched successfully
        """
        app_id = app_name.lower().replace(" ", "_")
        
        if app_id not in self.applications:
            print(f"❌ Application '{app_name}' not in registry")
            return False
            
        app = self.applications[app_id]
        
        if sister_name not in app['granted_to']:
            print(f"❌ {sister_name} does not have access to '{app_name}'")
            return False
            
        # Launch the application
        try:
            app_path = app['path']
            
            # If path is a directory, look for .exe files
            if os.path.isdir(app_path):
                exe_files = list(Path(app_path).glob("*.exe"))
                if exe_files:
                    app_path = str(exe_files[0])
                else:
                    print(f"❌ No executable found in {app_path}")
                    return False
                    
            # Build command
            cmd = [app_path]
            if args:
                cmd.extend(args)
                
            # Launch
            subprocess.Popen(cmd, shell=True)
            
            # Update usage stats
            app['usage_count'] += 1
            app['last_used'] = datetime.now().isoformat()
            self.save_registry()
            
            print(f"✅ {sister_name} launched '{app_name}'")
            return True
            
        except Exception as e:
            print(f"❌ Failed to launch '{app_name}': {e}")
            return False
            
    def save_registry(self):
        """Save application registry to disk"""
        with open(self.registry_file, 'w') as f:
            json.dump(self.applications, f, indent=2)
    
        def download_instructions(self, app_name: str) -> str:
            """
            Open browser to search for user manual/instructions
            Returns the search URL used
            """
            # Generate comprehensive search query
            search_query = f"{app_name} user manual PDF tutorial how to use guide"
        
            # Check if we have publisher info
            app_id = app_name.lower().replace(" ", "_")
            if app_id in self.applications:
                app = self.applications[app_id]
                publisher = app.get('publisher', '')
                if publisher and publisher != "Local Installation":
                    search_query = f"{publisher} {app_name} official manual documentation"
        
            # Create search URL and open it
            search_url = f"https://www.google.com/search?q={urllib.parse.quote(search_query)}"
            webbrowser.open(search_url)
        
            print(f"🔍 Searching for '{app_name}' instructions...")
            print(f"   Save manuals to: {self.data_dir / 'software_manuals'}")
        
            # Create manuals directory if it doesn't exist
            manuals_dir = self.data_dir / "software_manuals"
            manuals_dir.mkdir(parents=True, exist_ok=True)
        
            return search_url
    
        def get_instruction_path(self, app_name: str) -> Path:
            """Get path where manual should be saved"""
            manuals_dir = self.data_dir / "software_manuals"
            manuals_dir.mkdir(parents=True, exist_ok=True)
            return manuals_dir / f"{app_name.replace(' ', '_')}_manual.pdf"
            
    def load_registry(self):
        """Load application registry from disk"""
        if self.registry_file.exists():
            try:
                with open(self.registry_file, 'r') as f:
                    self.applications = json.load(f)
            except Exception as e:
                print(f"⚠️ Could not load application registry: {e}")
                self.applications = {}


class TaskUnderstanding:
    """
    Understands natural language instructions for application tasks
    Converts human instructions into actionable commands
    """
    
    def __init__(self, erryn_mind=None):
        """
        Args:
            erryn_mind: Optional ErrynMind instance for AI-powered understanding
        """
        self.mind = erryn_mind
        
        # Common task patterns (rule-based fallback)
        self.task_patterns = {
            "open": ["open", "launch", "start", "run"],
            "close": ["close", "exit", "quit", "stop"],
            "edit": ["edit", "modify", "change", "update"],
            "create": ["create", "make", "new", "generate"],
            "delete": ["delete", "remove", "erase"],
            "save": ["save", "store", "export"],
            "load": ["load", "import", "open file"],
            "search": ["search", "find", "look for"],
            "analyze": ["analyze", "check", "inspect", "examine"],
        }
        
    def parse_instruction(self, instruction: str, application: str) -> Dict:
        """
        Parse a natural language instruction into structured task
        
        Args:
            instruction: User's instruction (e.g., "Open this file and search for errors")
            application: Application name the task is for
            
        Returns:
            Dict with action, parameters, and confidence
        """
        instruction_lower = instruction.lower()
        
        # Detect action
        detected_action = "unknown"
        for action, keywords in self.task_patterns.items():
            if any(keyword in instruction_lower for keyword in keywords):
                detected_action = action
                break
                
        # If we have AI mind, get more sophisticated understanding
        if self.mind and self.mind.client:
            try:
                prompt = f"""Analyze this task instruction and convert it to a structured command.

Application: {application}
Instruction: "{instruction}"

Return JSON with:
- action: primary action (open/close/edit/create/delete/save/load/search/analyze)
- target: what the action applies to (file, data, etc)
- parameters: any specific details
- steps: list of sub-tasks if complex
- confidence: 0-1 how well you understand it

Example:
{{"action": "search", "target": "error messages", "parameters": {{"scope": "entire document"}}, "steps": ["open file", "search for 'error'", "highlight results"], "confidence": 0.9}}
"""
                
                response = self.mind.client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=300
                )
                
                # Parse JSON response
                import json
                result = json.loads(response.choices[0].message.content)
                result['ai_powered'] = True
                return result
                
            except Exception as e:
                print(f"⚠️ AI parsing failed, using rule-based: {e}")
                
        # Rule-based fallback
        return {
            "action": detected_action,
            "target": "unknown",
            "parameters": {},
            "steps": [instruction],
            "confidence": 0.5,
            "ai_powered": False
        }
        
    def format_task_for_display(self, task: Dict) -> str:
        """Format a parsed task for display to user"""
        lines = [
            f"🎯 Action: {task['action'].upper()}",
            f"📍 Target: {task.get('target', 'N/A')}",
        ]
        
        if task.get('steps'):
            lines.append("\n📝 Steps:")
            for i, step in enumerate(task['steps'], 1):
                lines.append(f"  {i}. {step}")
                
        lines.append(f"\n🤖 AI-Powered: {'Yes' if task.get('ai_powered') else 'No'}")
        lines.append(f"✨ Confidence: {task.get('confidence', 0):.0%}")
        
        return "\n".join(lines)


# Test and demo
if __name__ == "__main__":
    print("🔍 Scanning installed applications...")
    
    registry = ApplicationRegistry(Path("data/application_access"))
    
    # Scan for applications
    print("\n📱 Scanning... (this may take a moment)")
    apps = registry.scan_installed_applications()
    
    print(f"\n✅ Found {len(apps)} installed applications")
    print("\nFirst 10 applications:")
    for i, app in enumerate(apps[:10], 1):
        print(f"  {i}. {app['name']}")
        if app['publisher']:
            print(f"     Publisher: {app['publisher']}")
        print()
        
    # Demo: Grant access to Notepad
    print("\n🔧 Demo: Granting access to Notepad...")
    registry.grant_access(
        "Notepad",
        "C:\\Windows\\System32\\notepad.exe",
        ["Erryn", "Viress", "Echochild"]
    )
    
    # Show what Erryn has access to
    erryn_apps = registry.get_applications_for_sister("Erryn")
    print(f"\n👋 Erryn has access to {len(erryn_apps)} applications:")
    for app in erryn_apps:
        print(f"  - {app['name']}")
        
    print("\n✅ Application Access System ready!")
