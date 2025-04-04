import asyncio
from nexus_seed.kernel.microkernel import Microkernel
from nexus_seed.config.loader import load_config
from nexus_seed.utils.splash_screen import display_splash_screen

async def main():
    # Display splash screen
    display_splash_screen()

    # Load configuration
    config = load_config("/home/pong/Desktop/AIseed/config/system_config.json")

    # Initialize Microkernel
    kernel = Microkernel(config)
    await kernel.start()

    # Keep the system running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down Nexus Core...")
        await kernel.stop()

if __name__ == "__main__":
    asyncio.run(main())
