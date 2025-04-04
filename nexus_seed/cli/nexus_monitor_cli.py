import sys
import os

# Add the project root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import asyncio
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Input, Button
from textual.containers import Container
from nexus_seed.services.system_monitor_service import SystemMonitorService
from nexus_seed.services.stats_aggregator_service import StatsAggregatorService
from nexus_seed.services.main_brain import MainBrain
from nexus_seed.services.orchestrator_service import OrchestratorService
from nexus_seed.utils.event_bus import EventBus

class NexusMonitorApp(App):
    def __init__(self, event_bus: EventBus, system_monitor: SystemMonitorService, stats_aggregator: StatsAggregatorService, main_brain: MainBrain, orchestrator: OrchestratorService):
        super().__init__()
        self.event_bus = event_bus
        self.system_monitor = system_monitor
        self.stats_aggregator = stats_aggregator
        self.main_brain = main_brain
        self.orchestrator = orchestrator
        self.output = Static("Initializing Nexus Monitor...\n")
        self.input = Input(placeholder="Type a command or message...")
        self.refresh_interval = 1  # Refresh interval in seconds

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Container(
            self.output,
            self.input,
            Button("Send Message", id="send_message_button"),
            Button("View Metrics", id="view_metrics_button"),
            Button("Simulate Event", id="simulate_event_button"),
            Button("Self-Debug", id="self_debug_button"),
            Button("Self-Heal", id="self_heal_button"),
            Button("Generate Code", id="generate_code_button"),
            Button("OS Info", id="os_info_button"),
            Button("List Files", id="list_files_button"),
            Button("Network Config", id="network_config_button"),
            Button("Evolve Blueprint", id="evolve_blueprint_button"),
            Button("Deploy AI Agent", id="deploy_ai_agent_button"),
            Button("Optimize System", id="optimize_system_button"),
            Button("Sandbox Test", id="sandbox_test_button"),
            Button("Protocol Omnitide", id="protocol_omnitide_button"),  # New button
            Button("Omnitide syncnexus pppowerpong", id="syncnexus_button"),  # New button
            Button("Blah Blah Blah", id="blah_blah_blah_button"),  # New button
        )

    async def on_button_pressed(self, event):
        # Handle button presses
        button_id = event.button.id
        if button_id == "send_message_button":
            await self.handle_chat_message(self.input.value)
        elif button_id == "view_metrics_button":
            await self.display_metrics()
        elif button_id == "simulate_event_button":
            await self.simulate_event()
        elif button_id == "self_debug_button":
            response = await self.main_brain.process_event({"type": "self_debug"})
            self.output.update(f"{self.output.renderable}\nAI: {response}")
        elif button_id == "self_heal_button":
            response = await self.main_brain.process_event({"type": "self_heal"})
            self.output.update(f"{self.output.renderable}\nAI: {response}")
        elif button_id == "generate_code_button":
            response = await self.main_brain.process_event({"type": "generate_code", "params": {"prompt": self.input.value}})
            self.output.update(f"{self.output.renderable}\nAI: {response}")
        elif button_id == "os_info_button":
            response = await self.main_brain.process_event({"type": "os_info"})
            self.output.update(f"{self.output.renderable}\nAI: {response}")
        elif button_id == "list_files_button":
            response = await self.main_brain.process_event({"type": "list_files", "params": {"directory": self.input.value}})
            self.output.update(f"{self.output.renderable}\nAI: {response}")
        elif button_id == "network_config_button":
            response = await self.main_brain.process_event({"type": "network_config"})
            self.output.update(f"{self.output.renderable}\nAI: {response}")
        elif button_id == "evolve_blueprint_button":
            response = await self.main_brain.process_event({"type": "evolve_blueprint"})
            self.output.update(f"{self.output.renderable}\nAI: {response}")
        elif button_id == "deploy_ai_agent_button":
            response = await self.main_brain.process_event({"type": "deploy_ai_agent", "params": {"task": "list_files", "params": {"directory": "."}}})
            self.output.update(f"{self.output.renderable}\nAI: {response}")
        elif button_id == "optimize_system_button":
            response = await self.main_brain.process_event({"type": "optimize_system"})
            self.output.update(f"{self.output.renderable}\nAI: {response}")
        elif button_id == "sandbox_test_button":
            response = await self.main_brain.process_event({"type": "sandbox_test", "params": {"code": self.input.value}})
            self.output.update(f"{self.output.renderable}\nAI: {response}")
        elif button_id == "protocol_omnitide_button":
            response = await self.main_brain.protocol_omnitide()
            self.output.update(f"{self.output.renderable}\nAI: {response}")
        elif button_id == "syncnexus_button":
            response = await self.main_brain.omnitide_syncnexus_pppowerpong()
            self.output.update(f"{self.output.renderable}\nAI: {response}")
        elif button_id == "blah_blah_blah_button":
            response = await self.main_brain.blah_blah_blah()
            self.output.update(f"{self.output.renderable}\nAI: {response}")

    async def handle_chat_message(self, message: str):
        # Send a message to the AI agent (MainBrain)
        if message.strip():
            self.output.update(f"{self.output.renderable}\nYou: {message}")
            if message.lower() == "menu":
                response = await self.main_brain.process_event({"type": "list_functions"})
            else:
                response = await self.main_brain.process_event({"type": "chat_message", "content": message})
            self.output.update(f"{self.output.renderable}\nAI: {response}")
            self.input.value = ""  # Clear the input field
            self.refresh()

    async def display_metrics(self):
        # Fetch and display real-time system metrics
        metrics = await self.system_monitor.get_system_metrics()
        self.output.update(f"{self.output.renderable}\nMetrics: {metrics}")
        self.refresh()

    async def simulate_event(self):
        # Simulate an event and publish it to the EventBus
        event = {"type": "test_event", "data": "Simulated Event"}
        await self.event_bus.publish("core_event", event)
        self.output.update(f"{self.output.renderable}\nSimulated Event Published: {event}")
        self.refresh()

    async def periodic_refresh(self):
        # Periodically refresh the UI to keep it active
        while True:
            self.output.update(f"{self.output.renderable}\n[Heartbeat] Nexus Monitor is running...")
            self.refresh()
            await asyncio.sleep(self.refresh_interval)

    async def display_events(self, event):
        # Append events to the output area
        self.output.update(f"{self.output.renderable}\nEvent Received: {event}")
        self.refresh()

    async def display_agent_response(self, agent_name: str, response: str):
        # Display AI agent responses on the monitor
        self.output.update(f"{self.output.renderable}\n{agent_name}: {response}")
        self.refresh()

    async def start_services(self):
        # Start all services and subscribe to events
        await self.event_bus.subscribe("core_event", self.display_events)
        self.tasks = [
            asyncio.create_task(self.system_monitor.publish_stats()),
            asyncio.create_task(self.stats_aggregator.aggregate_stats()),
            asyncio.create_task(self.main_brain.start()),
            asyncio.create_task(self.orchestrator.process_events()),
            asyncio.create_task(self.periodic_refresh())
        ]

    async def stop_services(self):
        print("Stopping Nexus Monitor services...")
        for task in self.tasks:
            task.cancel()
        await asyncio.gather(*self.tasks, return_exceptions=True)
        print("All Nexus Monitor services have been stopped.")

async def main():
    # Initialize services
    event_bus = EventBus()
    system_monitor = SystemMonitorService(publish_interval_sec=5)
    stats_aggregator = StatsAggregatorService(aggregation_interval_sec=10)
    main_brain = MainBrain(event_bus)
    orchestrator = OrchestratorService()

    # Initialize and run the Nexus Monitor App
    app = NexusMonitorApp(event_bus, system_monitor, stats_aggregator, main_brain, orchestrator)
    try:
        await app.run_async()
    except KeyboardInterrupt:
        print("Shutting down Nexus Monitor...")
        await app.stop_services()

if __name__ == "__main__":
    asyncio.run(main())
