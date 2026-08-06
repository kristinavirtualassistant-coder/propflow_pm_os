import sys
import os

# Ensure project root is in PATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.settings import settings

def verify_milestone_01():
    print("=== PROPFLOW PM OS - MILESTONE 1 VERIFICATION ===")
    
    # Check directory layout
    required_dirs = ["config", "models", "agents", "portals", "tests", "data"]
    for d in required_dirs:
        if not os.path.exists(d):
            print(f"✗ Required directory '{d}' is missing.")
            return False
    print("✓ Modular directory structure created.")

    # Check config settings
    if settings.APP_NAME == "PropFlow PM OS" and len(settings.PORTALS) == 5:
        print(f"✓ Configuration loaded successfully ({settings.APP_NAME}).")
        print(f"✓ All 5 Portal matrices indexed: {list(settings.PORTALS.keys())}")
        print("\n✓ MILESTONE 1 VERIFICATION SUCCESSFUL")
        return True
    else:
        print("✗ Configuration verification failed.")
        return False

if __name__ == "__main__":
    success = verify_milestone_01()
    sys.exit(0 if success else 1)
