"""
SANDBOX ARENA - Safe Practice Environment for Sisters

This module provides a controlled environment where the sisters can:
1. Practice attack and defense techniques learned from their manuals
2. Test new scripts and tools without risking the real system
3. Play security "games" against each other
4. Develop proposals for real-world deployment

All actions here are logged and visualized in real-time.
"""

import os
import json
import datetime
import threading
import time
import subprocess
import random
from pathlib import Path
from typing import Dict, List, Any, Optional

class SandboxArena:
    """
    A safe, isolated environment for sisters to practice security techniques
    """
    def __init__(self, base_path: str = "data/sandbox"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # Create sandbox subdirectories
        self.scripts_path = self.base_path / "scripts"
        self.logs_path = self.base_path / "logs"
        self.targets_path = self.base_path / "targets"
        self.proposals_path = self.base_path / "proposals"
        
        for path in [self.scripts_path, self.logs_path, self.targets_path, self.proposals_path]:
            path.mkdir(exist_ok=True)
        
        # Activity log
        self.activity_log = []
        self.activity_lock = threading.Lock()
        
        # Active games/challenges
        self.active_games = {}
        
        # Initialize sandbox targets (fake vulnerable systems)
        self._create_sandbox_targets()
    
    def _create_sandbox_targets(self):
        """Create fake vulnerable systems for practice"""
        targets = {
            "FTP_Server": {
                "type": "network_service",
                "vulnerabilities": ["weak_password", "anonymous_login"],
                "difficulty": "easy",
                "description": "A simulated FTP server with weak credentials"
            },
            "Web_Server": {
                "type": "network_service",
                "vulnerabilities": ["sql_injection", "xss", "directory_traversal"],
                "difficulty": "medium",
                "description": "A simulated web application with common vulnerabilities"
            },
            "Windows_Workstation": {
                "type": "endpoint",
                "vulnerabilities": ["unpatched_service", "weak_admin_password", "missing_firewall"],
                "difficulty": "medium",
                "description": "A simulated Windows workstation with misconfigurations"
            },
            "Database_Server": {
                "type": "database",
                "vulnerabilities": ["default_credentials", "exposed_port", "no_encryption"],
                "difficulty": "hard",
                "description": "A simulated database with security issues"
            }
        }
        
        target_file = self.targets_path / "available_targets.json"
        with open(target_file, 'w') as f:
            json.dump(targets, f, indent=4)
    
    def log_activity(self, sister_name: str, action: str, target: str, result: str, details: Dict[str, Any] = None):
        """Log an action taken in the sandbox"""
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "sister": sister_name,
            "action": action,
            "target": target,
            "result": result,
            "details": details or {}
        }
        
        with self.activity_lock:
            self.activity_log.append(entry)
            
            # Also write to log file
            log_file = self.logs_path / f"arena_{datetime.datetime.now().strftime('%Y%m%d')}.json"
            with open(log_file, 'a') as f:
                f.write(json.dumps(entry) + "\n")
    
    def get_recent_activity(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent activity for visualization"""
        with self.activity_lock:
            return self.activity_log[-limit:]
    
    def attack_target(self, attacker: str, target_name: str, technique: str) -> Dict[str, Any]:
        """
        Simulate an attack on a sandbox target
        Returns success/failure and what was learned
        """
        # Load targets
        target_file = self.targets_path / "available_targets.json"
        with open(target_file, 'r') as f:
            targets = json.load(f)
        
        if target_name not in targets:
            return {
                "success": False,
                "message": "Target not found",
                "learning": None
            }
        
        target = targets[target_name]
        
        # Simulate attack logic
        technique_vulns = {
            "port_scan": ["exposed_port"],
            "brute_force": ["weak_password", "weak_admin_password", "default_credentials"],
            "sql_injection": ["sql_injection"],
            "xss": ["xss"],
            "directory_traversal": ["directory_traversal"],
            "exploit_unpatched": ["unpatched_service"],
            "anonymous_access": ["anonymous_login"]
        }
        
        # Check if technique matches a vulnerability
        success = False
        exploited_vuln = None
        
        if technique in technique_vulns:
            for vuln in technique_vulns[technique]:
                if vuln in target["vulnerabilities"]:
                    success = True
                    exploited_vuln = vuln
                    break
        
        result = {
            "success": success,
            "message": f"{'Successfully exploited' if success else 'Failed to exploit'} {target_name}",
            "exploited_vulnerability": exploited_vuln,
            "learning": {
                "technique_used": technique,
                "target_type": target["type"],
                "difficulty": target["difficulty"],
                "vulnerabilities_found": [exploited_vuln] if success else []
            }
        }
        
        # Log the activity
        self.log_activity(
            sister_name=attacker,
            action="ATTACK",
            target=target_name,
            result="SUCCESS" if success else "FAILURE",
            details=result["learning"]
        )
        
        return result
    
    def defend_target(self, defender: str, target_name: str, defense: str) -> Dict[str, Any]:
        """
        Simulate applying a defense to a sandbox target
        Returns what vulnerabilities were patched
        """
        # Load targets
        target_file = self.targets_path / "available_targets.json"
        with open(target_file, 'r') as f:
            targets = json.load(f)
        
        if target_name not in targets:
            return {
                "success": False,
                "message": "Target not found"
            }
        
        target = targets[target_name]
        
        # Simulate defense logic
        defense_fixes = {
            "strong_passwords": ["weak_password", "weak_admin_password", "default_credentials"],
            "disable_anonymous": ["anonymous_login"],
            "input_validation": ["sql_injection", "xss", "directory_traversal"],
            "patch_system": ["unpatched_service"],
            "enable_firewall": ["missing_firewall", "exposed_port"],
            "enable_encryption": ["no_encryption"]
        }
        
        patched = []
        if defense in defense_fixes:
            for vuln in defense_fixes[defense]:
                if vuln in target["vulnerabilities"]:
                    patched.append(vuln)
        
        result = {
            "success": len(patched) > 0,
            "message": f"Applied {defense} to {target_name}",
            "patched_vulnerabilities": patched,
            "learning": {
                "defense_technique": defense,
                "target_type": target["type"],
                "effectiveness": len(patched)
            }
        }
        
        # Log the activity
        self.log_activity(
            sister_name=defender,
            action="DEFEND",
            target=target_name,
            result="SUCCESS" if result["success"] else "NO_EFFECT",
            details=result["learning"]
        )
        
        return result
    
    def start_challenge(self, attacker: str, defender: str, target_name: str) -> str:
        """
        Start a challenge game between two sisters
        One attacks, one defends the same target
        """
        challenge_id = f"challenge_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        self.active_games[challenge_id] = {
            "attacker": attacker,
            "defender": defender,
            "target": target_name,
            "start_time": datetime.datetime.now().isoformat(),
            "attacker_score": 0,
            "defender_score": 0,
            "moves": []
        }
        
        self.log_activity(
            sister_name="SYSTEM",
            action="START_CHALLENGE",
            target=target_name,
            result="STARTED",
            details={
                "challenge_id": challenge_id,
                "attacker": attacker,
                "defender": defender
            }
        )
        
        return challenge_id
    
    def save_script(self, sister_name: str, script_name: str, script_content: str, description: str):
        """Save a script developed by a sister"""
        script_path = self.scripts_path / sister_name
        script_path.mkdir(exist_ok=True)
        
        script_file = script_path / script_name
        with open(script_file, 'w') as f:
            f.write(script_content)
        
        # Save metadata
        metadata = {
            "author": sister_name,
            "created": datetime.datetime.now().isoformat(),
            "description": description,
            "filename": script_name
        }
        
        metadata_file = script_path / f"{script_name}.meta.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=4)
        
        self.log_activity(
            sister_name=sister_name,
            action="SAVE_SCRIPT",
            target="sandbox",
            result="SUCCESS",
            details=metadata
        )
    
    def create_deployment_proposal(self, sister_name: str, proposal_title: str, 
                                   script_path: str, justification: str, 
                                   risks: List[str], benefits: List[str]) -> str:
        """
        Create a proposal for deploying a sandbox script to the real system
        """
        proposal_id = f"proposal_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        proposal = {
            "id": proposal_id,
            "author": sister_name,
            "title": proposal_title,
            "created": datetime.datetime.now().isoformat(),
            "status": "pending",
            "script_path": script_path,
            "justification": justification,
            "risks": risks,
            "benefits": benefits,
            "approved_by": None,
            "deployed_at": None
        }
        
        proposal_file = self.proposals_path / f"{proposal_id}.json"
        with open(proposal_file, 'w') as f:
            json.dump(proposal, f, indent=4)
        
        self.log_activity(
            sister_name=sister_name,
            action="CREATE_PROPOSAL",
            target="real_system",
            result="PENDING_APPROVAL",
            details={
                "proposal_id": proposal_id,
                "title": proposal_title
            }
        )
        
        return proposal_id
    
    def get_pending_proposals(self) -> List[Dict[str, Any]]:
        """Get all proposals awaiting approval"""
        proposals = []
        for proposal_file in self.proposals_path.glob("*.json"):
            with open(proposal_file, 'r') as f:
                proposal = json.load(f)
                if proposal["status"] == "pending":
                    proposals.append(proposal)
        return proposals
    
    def approve_proposal(self, proposal_id: str, approver: str) -> Dict[str, Any]:
        """Approve a proposal for real system deployment"""
        proposal_file = self.proposals_path / f"{proposal_id}.json"
        
        if not proposal_file.exists():
            return {"success": False, "message": "Proposal not found"}
        
        with open(proposal_file, 'r') as f:
            proposal = json.load(f)
        
        proposal["status"] = "approved"
        proposal["approved_by"] = approver
        proposal["approved_at"] = datetime.datetime.now().isoformat()
        
        with open(proposal_file, 'w') as f:
            json.dump(proposal, f, indent=4)
        
        self.log_activity(
            sister_name="SYSTEM",
            action="APPROVE_PROPOSAL",
            target="real_system",
            result="APPROVED",
            details={
                "proposal_id": proposal_id,
                "approver": approver
            }
        )
        
        return {
            "success": True,
            "message": f"Proposal {proposal_id} approved",
            "proposal": proposal
        }
    
    def deploy_proposal(self, proposal_id: str) -> Dict[str, Any]:
        """
        Deploy an approved proposal to the real system
        This should only be called after explicit user approval
        """
        proposal_file = self.proposals_path / f"{proposal_id}.json"
        
        if not proposal_file.exists():
            return {"success": False, "message": "Proposal not found"}
        
        with open(proposal_file, 'r') as f:
            proposal = json.load(f)
        
        if proposal["status"] != "approved":
            return {"success": False, "message": "Proposal not approved"}
        
        # Mark as deployed
        proposal["status"] = "deployed"
        proposal["deployed_at"] = datetime.datetime.now().isoformat()
        
        with open(proposal_file, 'w') as f:
            json.dump(proposal, f, indent=4)
        
        self.log_activity(
            sister_name=proposal["author"],
            action="DEPLOY_PROPOSAL",
            target="real_system",
            result="DEPLOYED",
            details={
                "proposal_id": proposal_id,
                "title": proposal["title"]
            }
        )
        
        return {
            "success": True,
            "message": f"Proposal {proposal_id} deployed to real system",
            "script_path": proposal["script_path"]
        }


# Global sandbox instance
_arena = None

def get_arena() -> SandboxArena:
    """Get or create the global sandbox arena instance"""
    global _arena
    if _arena is None:
        _arena = SandboxArena()
    return _arena
