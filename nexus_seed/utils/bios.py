import time

def enter_bios():
    print("""
    ==========================================
                     AIseed BIOS
    ==========================================
    """)
    print("Welcome to the AIseed BIOS. Use the options below to navigate:")
    print("1. View System Configuration")
    print("2. Debug EventBus")
    print("3. Exit BIOS")
    print("Starting BIOS in 3 seconds...")
    time.sleep(3)
    while True:
        choice = input("Enter your choice: ")
        if choice == "1":
            with open("/home/pong/Desktop/AIseed/config/system_config.json", "r") as f:
                print(f.read())
        elif choice == "2":
            print("Debugging EventBus...")
            # Add EventBus debugging logic here
        elif choice == "3":
            print("Exiting BIOS...")
            break
        else:
            print("Invalid choice. Try again.")
