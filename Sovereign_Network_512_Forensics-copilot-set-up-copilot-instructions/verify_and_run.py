import subprocess
import sys
from seal_keeper import print_seal_status

if __name__ == "__main__":
    valid = print_seal_status()
    # Proceed regardless, but warn visually via exit code if needed
    try:
        subprocess.run([sys.executable, "erryns_soul_gui.py"], check=False)
    except Exception as e:
        print(f"Failed to launch GUI: {e}")
        sys.exit(1)
