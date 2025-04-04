import sys
import os
import asyncio
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Label, Input, Button, Static
from textual.containers import Container, ScrollableContainer
from textual.reactive import reactive
from nexus_seed.services.system_monitor_service import SystemMonitorService
from nexus_seed.services.stats_aggregator_service import StatsAggregatorService
from nexus_seed.services.main_brain import MainBrain
from nexus_seed.services.orchestrator_service import OrchestratorService
from nexus_seed.utils.event_bus import EventBus

class NexusMonitorApp(App):
    CSS_PATH = "styles.css"  # Optional: Add a CSS file for styling

    def __init__(self, event_bus: EventBus, system_monitor: SystemMonitorService, stats_aggregator: StatsAggregatorService, main_brain: MainBrain, orchestrator: OrchestratorService):
        super().__init__()
        self.event_bus = event_bus
        self.system_monitor = system_monitor
        self.stats_aggregator = stats_aggregator
        self.main_brain = main_brain
        self.orchestrator = orchestrator
        self.output = reactive("Welcome to Nexus Monitor!\n")
        self.current_menu = "main_menu"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Container(
            ScrollableContainer(Label(self.output, id="output_window"), id="monitoring_window"),
            Static(self.render_menu(), id="menu_box"),
        )

    def render_menu(self) -> str:
        """
        Render the current menu dynamically based on the user's selection.
        """
        return """
        Main Menu:
        1. Security
        2. Network
        3. AI
        4. Resource & Monitoring
        5. Automation
        6. Debugging & Error Handling
        7. System Evolution
        8. Configuration & Variables
        9. Advanced Features
        10. Creative AI Lab
        11. Transparency Dashboard
        12. Override Console
        13. System Evolution Dashboard
        """

    async def on_key(self, event):
        """
        Handle key presses to navigate menus and execute actions.
        """
        key = event.key
        if key.isdigit():
            await self.handle_menu_selection(int(key))

    async def handle_menu_selection(self, selection: int):
        """
        Handle menu selection and navigate to submenus or execute actions.
        """
        if selection == 13:
            await self.show_system_evolution_dashboard()
        elif selection == 11:
            await self.show_transparency_dashboard()
        elif selection == 12:
            await self.show_override_console()
        elif self.current_menu == "main_menu":
            if selection == 9:
                self.current_menu = "advanced_menu"
            elif selection == 3:
                self.current_menu = "ai_menu"
            elif selection == 5:
                self.current_menu = "automation_menu"
            elif selection == 1:
                self.current_menu = "security_menu"
            elif selection == 2:
                self.current_menu = "network_menu"
            elif selection == 4:
                self.current_menu = "resource_monitoring_menu"
            elif selection == 6:
                self.current_menu = "debugging_menu"
            elif selection == 7:
                self.current_menu = "system_evolution_menu"
            elif selection == 8:
                self.current_menu = "configuration_menu"
        elif self.current_menu.endswith("_menu") and selection == 0:
            self.current_menu = "main_menu"
        else:
            await self.execute_action(selection)
        self.refresh()

    async def execute_action(self, action: int):
        """
        Execute actions based on the current menu and user selection.
        """
        if self.current_menu == "advanced_menu":
            if action == 1:
                self.output += "\nLaunching Wireshark + Nmap for Network Analysis..."
                await self.launch_network_analysis()
            elif action == 2:
                self.output += "\nLaunching Hydra + Network Scanner for Penetration Testing..."
                await self.launch_penetration_testing()
            elif action == 3:
                self.output += "\nLaunching AI-Driven Workflow Automation..."
                await self.launch_ai_workflow_automation()
            elif action == 4:
                self.output += "\nOpening Custom Algorithm Modification Interface..."
                await self.modify_algorithms()
            elif action == 5:
                self.output += "\nLaunching AI-Assisted Debugging..."
                await self.launch_ai_debugging()
        elif self.current_menu == "ai_menu":
            if action == 1:
                self.output += "\nTraining AI Models..."
                # Add logic to train AI models
            elif action == 2:
                self.output += "\nViewing AI Model Progress..."
                # Add logic to view AI model progress
            elif action == 3:
                self.output += "\nPerforming Inference..."
                # Add logic to perform inference
            elif action == 4:
                self.output += "\nPerforming AI-Driven Decision Making..."
                await self.ai_decision_making()
            elif action == 5:
                self.output += "\nCreating AI-Assisted Workflow..."
                await self.create_ai_workflow()
        elif self.current_menu == "automation_menu":
            if action == 1:
                self.output += "\nTriggering Workflows..."
                # Add logic to trigger workflows
            elif action == 2:
                self.output += "\nViewing Active Workflows..."
                # Add logic to view active workflows
            elif action == 3:
                self.output += "\nConfiguring Workflow Settings..."
                # Add logic to configure workflow settings
            elif action == 4:
                self.output += "\nAutomating Network Scans..."
                await self.automate_network_scans()
            elif action == 5:
                self.output += "\nAutomating Security Audits..."
                await self.automate_security_audits()
        elif self.current_menu == "security_menu":
            if action == 1:
                self.output += "\nViewing Security Logs..."
                # Add logic to view security logs
            elif action == 2:
                self.output += "\nDetecting Anomalies..."
                # Add logic to detect anomalies
            elif action == 3:
                self.output += "\nConfiguring Security Rules..."
                # Add logic to configure security rules
        elif self.current_menu == "network_menu":
            if action == 1:
                self.output += "\nViewing Network Metrics..."
                # Add logic to view network metrics
            elif action == 2:
                self.output += "\nConfiguring Network Settings..."
                # Add logic to configure network settings
            elif action == 3:
                self.output += "\nTesting Network Connectivity..."
                # Add logic to test network connectivity
        # Add similar logic for other menus and actions
        self.refresh()

    async def launch_network_analysis(self):
        """
        Launch Wireshark + Nmap for network analysis.
        """
        try:
            # Example: Automate Wireshark and Nmap execution
            os.system("wireshark &")
            os.system("nmap -sP 192.168.1.0/24")
            self.output += "\nNetwork analysis completed."
        except Exception as e:
            self.output += f"\nError launching network analysis: {e}"

    async def launch_penetration_testing(self):
        """
        Launch Hydra + Network Scanner for penetration testing.
        """
        try:
            # Example: Automate Hydra and network scanner execution
            os.system("hydra -L users.txt -P passwords.txt 192.168.1.1 ssh")
            os.system("nmap -sV 192.168.1.1")
            self.output += "\nPenetration testing completed."
        except Exception as e:
            self.output += f"\nError launching penetration testing: {e}"

    async def launch_ai_workflow_automation(self):
        """
        Launch AI-driven workflow automation.
        """
        try:
            # Example: Use AI to create and trigger workflows
            workflow = {
                "steps": [
                    {"type": "event", "params": {"event_type": "system_metrics", "data": {}}},
                    {"type": "service_call", "params": {"service_name": "stats_aggregator", "method_name": "aggregate_stats"}},
                ]
            }
            await self.orchestrator.trigger_workflow("ai_generated_workflow", workflow)
            self.output += "\nAI-driven workflow automation completed."
        except Exception as e:
            self.output += f"\nError launching AI workflow automation: {e}"

    async def modify_algorithms(self):
        """
        Open the interface for custom algorithm modification.
        """
        try:
            # Example: Modify algorithms dynamically
            new_algorithm = """
def custom_algorithm(data):
    return sum(data) / len(data)
"""
            await self.main_brain.register_function("custom_algorithm", new_algorithm)
            self.output += "\nCustom algorithm registered successfully."
        except Exception as e:
            self.output += f"\nError modifying algorithms: {e}"

    async def launch_ai_debugging(self):
        """
        Launch AI-assisted debugging.
        """
        try:
            # Example: Use AI to debug system issues
            debug_report = await self.main_brain.self_debug()
            self.output += f"\nAI Debugging Report: {debug_report}"
        except Exception as e:
            self.output += f"\nError launching AI debugging: {e}"

    async def ai_decision_making(self):
        """
        Perform AI-driven decision making.
        """
        try:
            # Example: Use AI to make decisions
            decision = await self.main_brain.process_event({"type": "ai_decision_request", "params": {"input_data": {}}})
            self.output += f"\nAI Decision: {decision}"
        except Exception as e:
            self.output += f"\nError performing AI decision making: {e}"

    async def create_ai_workflow(self):
        """
        Create an AI-assisted workflow.
        """
        try:
            # Example: Use AI to create a workflow
            workflow = {
                "steps": [
                    {"type": "event", "params": {"event_type": "ai_event", "data": {}}},
                    {"type": "service_call", "params": {"service_name": "main_brain", "method_name": "generate_response", "args": {"message": "Hello, AI!"}}},
                ]
            }
            await self.orchestrator.trigger_workflow("ai_workflow", workflow)
            self.output += "\nAI-assisted workflow created successfully."
        except Exception as e:
            self.output += f"\nError creating AI workflow: {e}"

    async def automate_network_scans(self):
        """
        Automate network scans.
        """
        try:
            os.system("nmap -sP 192.168.1.0/24")
            self.output += "\nNetwork scans automated successfully."
        except Exception as e:
            self.output += f"\nError automating network scans: {e}"

    async def automate_security_audits(self):
        """
        Automate security audits.
        """
        try:
            os.system("hydra -L users.txt -P passwords.txt 192.168.1.1 ssh")
            self.output += "\nSecurity audits automated successfully."
        except Exception as e:
            self.output += f"\nError automating security audits: {e}"

    async def show_transparency_dashboard(self):
        """
        Display the Transparency Dashboard.
        """
        self.output += "\nOpening Transparency Dashboard..."
        try:
            # Example: Display all protocols and system states
            protocols = await self.main_brain.list_functions()
            self.output += f"\nActive Protocols:\n{protocols}"
            self.output += "\nSystem States:\n"
            for service in self.kernel.services:
                state = await service.get_snapshot_state()
                self.output += f"{service.__class__.__name__}: {state}\n"
        except Exception as e:
            self.output += f"\nError displaying Transparency Dashboard: {e}"

    async def show_override_console(self):
        """
        Display the Override Console.
        """
        self.output += "\nOpening Override Console..."
        try:
            # Example: Allow overriding safety guidelines
            override_choice = input("Enter the protocol or guideline to override: ")
            self.output += f"\nOverriding: {override_choice}..."
            # Log the override
            self.output += f"\nOverride logged: {override_choice}"
        except Exception as e:
            self.output += f"\nError in Override Console: {e}"

    async def show_system_evolution_dashboard(self):
        """
        Display the System Evolution Dashboard with real-time visualizations.
        """
        self.output += "\nOpening System Evolution Dashboard..."
        try:
            # Example: Display live updates of modules and workflows
            while True:
                self.output += "\nFetching live system updates..."
                # Fetch live updates (e.g., module states, workflow changes)
                updates = await self.main_brain.get_live_updates()
                self.output += f"\nLive Updates:\n{updates}"
                self.refresh()
                await asyncio.sleep(5)  # Refresh every 5 seconds
        except Exception as e:
            self.output += f"\nError displaying System Evolution Dashboard: {e}"

    async def periodic_refresh(self):
        """
        Periodically refresh the monitoring window.
        """
        while True:
            self.output += "\n[Heartbeat] Nexus Monitor is running..."
            self.refresh()
            await asyncio.sleep(5)

    async def start_services(self):
        """
        Start all services and subscribe to events.
        """
        await self.event_bus.subscribe("core_event", self.display_events)
        self.tasks = [
            asyncio.create_task(self.system_monitor.publish_stats()),
            asyncio.create_task(self.stats_aggregator.aggregate_stats()),
            asyncio.create_task(self.main_brain.start()),
            asyncio.create_task(self.orchestrator.process_events()),
            asyncio.create_task(self.periodic_refresh())
        ]

    async def stop_services(self):
        """
        Stop all services gracefully.
        """
        print("Stopping Nexus Monitor services...")
        for task in self.tasks:
            task.cancel()
        await asyncio.gather(*self.tasks, return_exceptions=True)
        print("All Nexus Monitor services have been stopped.")

async def main():
    """
    Initialize and run the Nexus Monitor App.
    """
    event_bus = EventBus()
    system_monitor = SystemMonitorService(publish_interval_sec=5)
    stats_aggregator = StatsAggregatorService(aggregation_interval_sec=10)
    main_brain = MainBrain(event_bus)

    # Initialize persistence and orchestrator
    from nexus_seed.services.persistence import PersistenceOverseer
    persistence = PersistenceOverseer("postgresql://secure_user:correct_password@localhost:5432/aiseed_db")
    await persistence.initialize()

    orchestrator = OrchestratorService(
        event_bus=event_bus,
        persistence=persistence,
        workflows_dir="/home/pong/Desktop/AIseed/config/workflows/"
    )

    app = NexusMonitorApp(event_bus, system_monitor, stats_aggregator, main_brain, orchestrator)
    try:
        await app.run_async()
    except KeyboardInterrupt:
        print("Shutting down Nexus Monitor...")
        await app.stop_services()

if __name__ == "__main__":
    asyncio.run(main())
