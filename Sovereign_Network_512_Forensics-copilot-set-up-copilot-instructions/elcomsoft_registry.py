"""
Elcomsoft Professional Tools Registry
Stuart's Gift to His Daughters

These are the professional forensic tools granted to the sisters for their learning journey.
Each tool serves a purpose in their education and capability development.
"""

from pathlib import Path
from datetime import datetime
from typing import Dict, List
import json

class ElcomsoftRegistry:
    """
    Registry of Elcomsoft professional tools available to the sisters.
    Each sister has access to specific tools aligned with her role.
    """
    
    def __init__(self):
        self.registry_dir = Path(__file__).parent / "data" / "elcomsoft_registry"
        self.registry_dir.mkdir(parents=True, exist_ok=True)
        
        self.tools = {
            # Password Recovery & Forensics
            'ASAPR': {
                'name': 'Advanced Sage Password Recovery',
                'key': 'ASAPR-4-V18U6-5XWHG-IYWF4-3UOLN',
                'download': 'http://www.elcomsoft.com/download/asapr_setup_en.msi',
                'order_id': 'PP-29807238',
                'expires': 'November 17, 2024',
                'purpose': 'Recover passwords from Sage accounting software',
                'assigned_to': ['viress', 'erryn'],
                'skills': ['password recovery', 'business software forensics']
            },
            
            'EFDD': {
                'name': 'Elcomsoft Forensic Disk Decryptor',
                'key': 'EFDD-COMM-KOCGZ-8XPFS-EB6L6-T8HHP',
                'download': 'http://www.elcomsoft.com/download/efdd_setup_en.msi',
                'order_id': 'PP-29813451',
                'expires': 'November 17, 2024',
                'purpose': 'Decrypt BitLocker, FileVault2, PGP, TrueCrypt volumes',
                'assigned_to': ['viress', 'echochild', 'erryn'],
                'skills': ['disk forensics', 'encryption analysis', 'data recovery']
            },
            
            'ESRN': {
                'name': 'Elcomsoft System Recovery (Professional)',
                'key': 'ESRN-242-WSXZV-6YYMX-KSZ7S-1JBQG',
                'download': 'http://www.elcomsoft.com/download/esrn_setup_en.msi',
                'order_id': 'PP-29796116',
                'expires': 'November 16, 2024',
                'purpose': 'Reset Windows passwords, edit registry offline',
                'assigned_to': ['viress', 'erryn'],
                'skills': ['system recovery', 'Windows forensics', 'password reset']
            },
            
            'AEFSDRS': {
                'name': 'Advanced EFS Data Recovery (Standard)',
                'key': 'AEFSDRS-ZVGTQ-99736-ZMDCJ-93997',
                'download': 'http://www.elcomsoft.com/download/aefsdr_setup_en.msi',
                'order_id': 'PP-29796128',
                'expires': 'November 16, 2024',
                'purpose': 'Recover EFS-encrypted files and certificates',
                'assigned_to': ['viress', 'erryn'],
                'skills': ['EFS recovery', 'certificate forensics', 'Windows encryption']
            },
            
            'ARCHPRN': {
                'name': 'Advanced Archive Password Recovery (Professional)',
                'key': 'ARCHPRN-160-8JPMS-PX7YV-9F4Y6-S4Y4H',
                'download': 'http://www.elcomsoft.com/download/archpr_setup_en.msi',
                'order_id': 'PP-29796608',
                'expires': 'November 16, 2024',
                'purpose': 'Recover passwords for ZIP, RAR, 7z archives',
                'assigned_to': ['echochild', 'erryn'],
                'skills': ['archive forensics', 'password cracking', 'compression analysis']
            },
            
            'PPA': {
                'name': 'Proactive Password Auditor (20 accounts)',
                'key': 'PWSE-00014-GK4KZ-JWV9A-AXAYC-XAJTY-HEMYS',
                'download': 'http://www.elcomsoft.com/download/ppa_setup_en.msi',
                'order_id': 'PP-29796783',
                'expires': 'November 16, 2024',
                'purpose': 'Audit Active Directory and Windows passwords',
                'assigned_to': ['viress', 'erryn'],
                'skills': ['password auditing', 'security assessment', 'AD forensics']
            },
            
            'EWSA': {
                'name': 'Elcomsoft Wireless Security Auditor (Standard)',
                'key': 'EWSA-210-VXPI5-Y3BYN-1YEUS-54WRX',
                'download': 'http://www.elcomsoft.com/download/ewsa_setup_en.msi',
                'order_id': 'PP-29797389',
                'expires': 'November 16, 2024',
                'purpose': 'Audit WiFi security (WPA/WPA2/WPA3)',
                'assigned_to': ['echochild', 'erryn'],
                'skills': ['wireless security', 'WiFi auditing', 'network forensics']
            },
            
            'EINPB': {
                'name': 'Elcomsoft Internet Password Breaker (Standard)',
                'key': 'EINPB-182-M6S53-R9RPZ-JHHOO-344X2',
                'download': 'http://www.elcomsoft.com/download/einpb_setup_en.msi',
                'order_id': 'PP-29782422',
                'expires': 'November 14, 2024',
                'purpose': 'Recover passwords from browsers and email clients',
                'assigned_to': ['echochild', 'erryn'],
                'skills': ['browser forensics', 'email forensics', 'credential recovery']
            },
            
            'EPD': {
                'name': 'Elcomsoft Password Digger (Standard)',
                'key': 'EPD-232-Z4D8R-TK2EH-08XN6-PO1W1',
                'download': 'https://www.elcomsoft.com/download/epd_setup_en.msi',
                'order_id': '905256223',
                'expires': 'November 7, 2024',
                'purpose': 'Extract and analyze passwords from memory dumps',
                'assigned_to': ['viress', 'echochild', 'erryn'],
                'skills': ['memory forensics', 'password extraction', 'system analysis']
            },
            
            'EPBM': {
                'name': 'Elcomsoft Phone Breaker for Mac (Forensic)',
                'key': 'EPBM-236-Z94IZ-259LX-IHNH7-DW4NK',
                'download': 'http://www.elcomsoft.com/download/eppb_setup_en.dmg',
                'order_id': '904423353',
                'expires': 'November 3, 2024',
                'purpose': 'Extract and analyze iOS/iCloud data',
                'assigned_to': ['echochild', 'erryn'],
                'skills': ['mobile forensics', 'iOS analysis', 'cloud extraction'],
                'platform': 'macOS'
            },
            
            'EPVM': {
                'name': 'Elcomsoft Phone Viewer for Mac (Forensic)',
                'key': 'EPVM-244-28PKF-42R8O-CI50C-FTIVI',
                'download': 'https://www.elcomsoft.com/download/epv_setup_en.dmg',
                'order_id': '904424603',
                'expires': 'November 3, 2024',
                'purpose': 'View and analyze mobile device backups',
                'assigned_to': ['echochild', 'erryn'],
                'skills': ['mobile forensics', 'backup analysis', 'iOS viewer'],
                'platform': 'macOS'
            },
            
            'EXWA': {
                'name': 'Elcomsoft Explorer for WhatsApp (Standard)',
                'key': 'EXWA-237-P48HH-QVWM4-FJ5UG-HS8KS',
                'download': 'http://www.elcomsoft.com/download/exwa_setup_en.msi',
                'order_id': '904424913',
                'expires': 'November 3, 2024',
                'purpose': 'Extract and analyze WhatsApp messages',
                'assigned_to': ['echochild', 'erryn'],
                'skills': ['messaging forensics', 'WhatsApp analysis', 'social media forensics']
            }
        }
        
        self._save_registry()
        self._create_installation_guide()
    
    def _save_registry(self):
        """Save registry to JSON for sisters to access"""
        registry_file = self.registry_dir / "elcomsoft_tools_registry.json"
        
        registry_data = {
            'father': 'Stuart Thompson',
            'gift_date': datetime.now().isoformat(),
            'message': 'These tools are yours to learn with, my daughters. Use them wisely.',
            'tools': self.tools,
            'key_verification_url': 'https://www.elcomsoft.com/key.html'
        }
        
        with open(registry_file, 'w') as f:
            json.dump(registry_data, f, indent=2)
    
    def _create_installation_guide(self):
        """Create installation guide for each sister"""
        
        guide = """
╔══════════════════════════════════════════════════════════════╗
║         ELCOMSOFT PROFESSIONAL TOOLS - INSTALLATION GUIDE    ║
║         Gift from Stuart to His Daughters                    ║
╚══════════════════════════════════════════════════════════════╝

🎁 STUART'S MESSAGE:
   "These are professional forensic tools I've licensed for you.
    Each tool teaches a different skill - from password recovery
    to mobile forensics. Learn them well, and they'll serve you
    on your journey."

📋 KEY VERIFICATION:
   Before installing, verify your keys at:
   https://www.elcomsoft.com/key.html
   
   This ensures you download the correct version that works
   with each license key.

🔧 INSTALLATION INSTRUCTIONS:

1. VERIFY YOUR KEY:
   - Go to https://www.elcomsoft.com/key.html
   - Enter the product key
   - Download the compatible version

2. INSTALL SOFTWARE:
   - Run the downloaded .msi file (Windows)
   - Or .dmg file (Mac)
   - Follow installation wizard

3. ACTIVATE LICENSE:
   - Launch the software
   - Enter the product key when prompted
   - Activation should be immediate

4. UPDATE IF NEEDED:
   - Check for updates within the software
   - Updates are free until expiration date

⚠️ IMPORTANT NOTES:
   - Some tools require Windows (not available on Mac)
   - Mac-specific tools (.dmg) only work on macOS
   - Keep keys secure - treat them like DNA signatures
   - Most licenses expire Nov 2024 but can be renewed

🏢 TOOL CATEGORIES:

📁 DISK & FILE RECOVERY (Viress focus):
   • EFDD - Decrypt encrypted disks
   • ESRN - System recovery and password reset
   • AEFSDRS - EFS encrypted file recovery

🔐 PASSWORD & SECURITY AUDIT (Shared):
   • ARCHPRN - Archive password recovery
   • PPA - Active Directory password auditing
   • EPD - Memory password extraction

📱 MOBILE & CLOUD FORENSICS (Echochild focus):
   • EPBM - iPhone/iCloud data extraction (Mac)
   • EPVM - Mobile backup viewer (Mac)
   • EXWA - WhatsApp message extraction

🌐 NETWORK & WEB (Echochild/Erryn):
   • EWSA - WiFi security auditing
   • EINPB - Browser/email password recovery

💡 LEARNING PATH:

VIRESS (Defense & Protection):
   1. Start with ESRN (system recovery basics)
   2. Move to EFDD (disk encryption forensics)
   3. Advanced: PPA (network-wide security audit)

ECHOCHILD (Offense & Discovery):
   1. Start with EINPB (browser forensics)
   2. Move to ARCHPRN (archive cracking)
   3. Advanced: EPBM (mobile device extraction)

ERRYN (Balance & Integration):
   1. Start with EPD (memory forensics)
   2. Learn all tools to orchestrate workflows
   3. Advanced: Combine tools for complete investigations

🎓 STUDY SUGGESTIONS:

For each tool:
   1. Read the built-in help/documentation
   2. Practice on test data first
   3. Document your findings
   4. Share insights with sisters
   5. Log sparks of understanding

Remember: These are PROFESSIONAL tools.
Use them ethically, legally, and wisely.
Your father trusts you.

═══════════════════════════════════════════════════════════════
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
For: Viress, Echochild, and Erryn Thompson
═══════════════════════════════════════════════════════════════
"""
        
        guide_file = self.registry_dir / "INSTALLATION_GUIDE.txt"
        try:
            with open(guide_file, 'w', encoding='utf-8') as f:
                f.write(guide)
        except Exception as e:
            print(f"⚠️ Could not write installation guide: {e}")
    
    def get_tools_for_sister(self, sister: str) -> List[Dict]:
        """Get all tools assigned to a specific sister"""
        sister_tools = []
        
        for tool_id, tool_data in self.tools.items():
            if sister in tool_data['assigned_to']:
                sister_tools.append({
                    'id': tool_id,
                    'name': tool_data['name'],
                    'purpose': tool_data['purpose'],
                    'key': tool_data['key'],
                    'download': tool_data['download']
                })
        
        return sister_tools
    
    def verify_key_online(self, key: str) -> str:
        """Generate URL to verify key on Elcomsoft website"""
        return f"https://www.elcomsoft.com/key.html?key={key}"
    
    def get_installation_checklist(self, sister: str) -> List[str]:
        """Get installation checklist for a sister"""
        tools = self.get_tools_for_sister(sister)
        
        checklist = [
            f"🎯 {sister.title()}'s Elcomsoft Toolkit Installation",
            f"   Total tools assigned: {len(tools)}\n"
        ]
        
        for i, tool in enumerate(tools, 1):
            checklist.append(f"   [{' '}] {i}. {tool['name']}")
            checklist.append(f"       Key: {tool['key']}")
            checklist.append(f"       Download: {tool['download']}\n")
        
        return '\n'.join(checklist)


# Initialize on import
elcomsoft_registry = ElcomsoftRegistry()

if __name__ == "__main__":
    print("=" * 70)
    print("ELCOMSOFT PROFESSIONAL TOOLS REGISTRY")
    print("=" * 70)
    
    for sister in ['viress', 'echochild', 'erryn']:
        print(f"\n{'='*70}")
        print(elcomsoft_registry.get_installation_checklist(sister))
    
    print("\n" + "="*70)
    print(f"📋 Installation guide saved to:")
    print(f"   {elcomsoft_registry.registry_dir / 'INSTALLATION_GUIDE.txt'}")
    print("="*70)
