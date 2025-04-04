import time

def display_splash_screen():
    print("""
    ==========================================
               AIseed Operating System
                  Version 1.0.0
    ==========================================
    """)
    print("Initializing system...")
    time.sleep(2)
    print("Press 'B' to enter BIOS or wait to continue...")
    for i in range(5, 0, -1):
        print(f"Continuing in {i} seconds...", end="\r")
        time.sleep(1)
    print("\nSystem ready. Launching Nexus Monitor...")
