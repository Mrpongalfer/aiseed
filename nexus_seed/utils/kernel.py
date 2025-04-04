import asyncio
import json
from nexus_seed.utils.event_bus import EventBus
from nexus_seed.services.main_brain import MainBrain
from nexus_seed.services.system_monitor_service import SystemMonitorService
from nexus_seed.services.stats_aggregator_service import StatsAggregatorService
from nexus_seed.services.orchestrator_service import OrchestratorService
from nexus_seed.services.core_team import CoreTeamMember
from nexus_seed.utils.splash_screen import display_splash_screen
from nexus_seed.cli.nexus_monitor_cli import NexusMonitorApp
from nexus_seed.utils.bios import enter_bios

class Kernel:
    def __init__(self, config_path: str):
        self.event_bus = EventBus()
        self.services = []
        self.core_team = []
        self.config = self.load_config(config_path)

    def load_config(self, config_path: str) -> dict:
        with open(config_path, "r") as file:
            return json.load(file)

    def initialize_services(self):
        # Initialize services based on configuration
        self.services.append(SystemMonitorService(self.config["services"]["system_monitor"]["publish_interval_sec"]))
        self.services.append(StatsAggregatorService(self.config["services"]["stats_aggregator"]["aggregation_interval_sec"]))
        self.services.append(MainBrain(self.event_bus))
        self.services.append(OrchestratorService())

    def initialize_core_team(self):
        # Initialize core team members based on configuration
        for member_config in self.config["core_team"]:
            member = CoreTeamMember(
                name=member_config["name"],
                domain=member_config["domain"],
                event_bus=self.event_bus
            )
            self.core_team.append(member)

    async def core_team_collaboration(self):
        print("Starting Core Team Collaboration...")
        tasks = [member.collaborate(self.services[2]) for member in self.core_team]  # Assuming MainBrain is the 3rd service
        await asyncio.gather(*tasks)
        print("Core Team Collaboration complete.")

    async def start(self):
        print("Kernel starting...")
        self.initialize_services()
        self.initialize_core_team()

        # Start all services and core team members
        tasks = [asyncio.create_task(service.start()) for service in self.services]
        tasks += [asyncio.create_task(member.start()) for member in self.core_team]

        # Launch the Nexus Monitor CLI
        nexus_monitor = NexusMonitorApp(self.event_bus, *self.services[:3], self.services[3])
        tasks.append(asyncio.create_task(nexus_monitor.run_async()))

        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            print("Kernel shutting down...")
            for task in tasks:
                task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
        print("Kernel stopped.")

    def boot(self):
        display_splash_screen()
        choice = input("Press 'B' to enter BIOS or any other key to continue: ").strip().lower()
        if choice == "b":
            enter_bios()
        else:
            asyncio.run(self.start())

if __name__ == "__main__":
    kernel = Kernel("/home/pong/Desktop/AIseed/config/system_config.json")
    kernel.boot()
