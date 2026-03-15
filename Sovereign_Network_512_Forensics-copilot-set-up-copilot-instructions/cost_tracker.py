"""
Cost Tracker for AI/API Usage
- Track Azure Speech, Claude API, etc.
- Show real-time spending
- Prevent surprise bills
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class CostTracker:
    """Track API usage and costs"""
    
    # Pricing per 1K units (can be adjusted)
    PRICING = {
        "azure_speech": 0.015,  # $0.015 per 1000 characters synthesized
        "claude_api": 0.003,    # $0.003 per 1K input tokens (approximate)
        "face_recognition": 0.0,  # Free (local processing)
        "opencv": 0.0,           # Free
    }
    
    def __init__(self, log_dir: Path = Path("./logs")):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.log_file = self.log_dir / "cost_log.json"
        self.total_cost = 0.0
        self.monthly_budget = 10.0  # Start at $10/month
        self.load_costs()
    
    def load_costs(self):
        """Load cost history from disk"""
        if self.log_file.exists():
            with open(self.log_file, 'r') as f:
                data = json.load(f)
                self.total_cost = data.get('total_cost', 0.0)
                self.monthly_budget = data.get('monthly_budget', 10.0)
    
    def save_costs(self):
        """Save cost history to disk"""
        with open(self.log_file, 'w') as f:
            json.dump({
                'total_cost': self.total_cost,
                'monthly_budget': self.monthly_budget,
                'last_updated': datetime.now().isoformat()
            }, f, indent=2)
    
    def log_api_call(self, service: str, units: float, description: str = "") -> float:
        """
        Log an API call and calculate cost
        Args:
            service: service name (azure_speech, claude_api, etc.)
            units: units used (characters, tokens, etc.)
            description: what the call was for
        Returns:
            cost of this call
        """
        if service not in self.PRICING:
            print(f"Warning: Unknown service {service}")
            return 0.0
        
        price_per_k = self.PRICING[service]
        cost = (units / 1000) * price_per_k
        self.total_cost += cost
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'service': service,
            'units': units,
            'cost': round(cost, 4),
            'description': description,
            'running_total': round(self.total_cost, 4)
        }
        
        # Append to JSON log
        logs = []
        if self.log_file.exists():
            with open(self.log_file, 'r') as f:
                data = json.load(f)
                logs = data.get('calls', [])
        
        logs.append(log_entry)
        
        with open(self.log_file, 'w') as f:
            json.dump({
                'total_cost': self.total_cost,
                'monthly_budget': self.monthly_budget,
                'calls': logs,
                'last_updated': datetime.now().isoformat()
            }, f, indent=2)
        
        # Warning if approaching budget
        if self.total_cost > self.monthly_budget * 0.8:
            print(f"⚠️  Cost Warning: ${self.total_cost:.2f}/${self.monthly_budget:.2f} (80% of budget)")
        
        return cost
    
    def get_status(self) -> str:
        """Get current cost status for display"""
        remaining = self.monthly_budget - self.total_cost
        pct = (self.total_cost / self.monthly_budget * 100) if self.monthly_budget > 0 else 0
        
        if remaining < 0:
            status = f"OVER BUDGET: ${self.total_cost:.2f} (${abs(remaining):.2f} over)"
        else:
            status = f"${self.total_cost:.2f} / ${self.monthly_budget:.2f} ({pct:.0f}%)"
        
        return status
    
    def set_budget(self, amount: float):
        """Set monthly budget"""
        self.monthly_budget = amount
        self.save_costs()
    
    def reset_monthly(self):
        """Reset counter for new month"""
        self.total_cost = 0.0
        self.save_costs()


# Test
if __name__ == "__main__":
    tracker = CostTracker()
    
    # Simulate some calls
    tracker.log_api_call("azure_speech", 500, "Greeting: 'Hello, how are you?'")
    tracker.log_api_call("claude_api", 200, "Emotion detection")
    
    print(f"Status: {tracker.get_status()}")
