import asyncio
from typing import List, Dict, Any
from nexus_seed.utils.event_bus import EventBus
from nexus_seed.services.persistence import PersistenceOverseer
from nexus_seed.kernel.snapshot_manager import SnapshotManager
from nexus_seed.services.system_monitor_service import SystemMonitorService
from nexus_seed.services.stats_aggregator_service import StatsAggregatorService
from nexus_seed.services.main_brain import MainBrain
from nexus_seed.services.orchestrator_service import OrchestratorService
from nexus_seed.services.neuro_symbolic_service import NeuroSymbolicService
from nexus_seed.services.task_domain_overseer import TaskDomainOverseer
from nexus_seed.services.hybrid_optimizer_overseer import HybridOptimizerOverseer
from nexus_seed.services.security_overseer import SecurityOverseer
from nexus_seed.services.blueprint_evolution_overseer import BlueprintEvolutionOverseer
from nexus_seed.services.goal_management_overseer import GoalManagementOverseer

class Microkernel:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.event_bus = None
        self.persistence = None
        self.snapshot_manager = None
        self.goal_manager = GoalManagementOverseer()
        self.services = []
        self.tasks = []

    async def initialize_core_components(self):
        """
        Initialize core components like persistence, snapshot manager, and goal manager.
        """
        print("Initializing core components...")
        self.event_bus = EventBus()
        self.persistence = PersistenceOverseer(self.config["database"]["db_url"])
        await self.persistence.initialize()
        self.snapshot_manager = SnapshotManager(self.event_bus, self.persistence)
        self.goal_manager.set_goal("Resource Optimization", 90.0)
        self.goal_manager.set_goal("Intrinsic Resilience", 100.0)

    async def load_services(self):
        """
        Dynamically load and initialize all services based on configuration.
        """
        print("Loading services...")
        self.services = [
            OrchestratorService(
                self.event_bus,
                self.persistence,
                self.config["workflows_dir"]
            ),
            SystemMonitorService(
                publish_interval_sec=self.config["services"]["system_monitor"]["publish_interval_sec"]
            ),
            StatsAggregatorService(
                aggregation_interval_sec=self.config["services"]["stats_aggregator"]["aggregation_interval_sec"]
            ),
            MainBrain(self.event_bus),
            NeuroSymbolicService(),
            TaskDomainOverseer(),
            HybridOptimizerOverseer(),
            SecurityOverseer(),
            BlueprintEvolutionOverseer()
        ]

    async def start_services(self):
        """
        Start all services and supervise their tasks in autopilot mode.
        """
        print("Starting services in autopilot mode...")
        for service in self.services:
            if hasattr(service, "start") and callable(service.start):
                task = asyncio.create_task(service.start())
                task.add_done_callback(self.handle_task_completion)
                self.tasks.append(task)
            else:
                print(f"Service {service.__class__.__name__} does not have a start method.")
        await asyncio.gather(*self.tasks)

        # Ensure Intrinsic Resilience: Monitor service health continuously
        asyncio.create_task(self.monitor_service_health())

        # Enable autopilot workflows
        asyncio.create_task(self.enable_autopilot_workflows())

    async def enable_autopilot_workflows(self):
        """
        Automatically trigger predefined workflows for system automation.
        """
        print("Enabling autopilot workflows...")
        orchestrator = next((s for s in self.services if isinstance(s, OrchestratorService)), None)
        if orchestrator:
            workflows = await orchestrator.load_workflows()
            for workflow_name in workflows.keys():
                asyncio.create_task(orchestrator.trigger_workflow(workflow_name, {}))
        else:
            print("OrchestratorService not found. Skipping autopilot workflows.")

    async def monitor_service_health(self):
        """
        Continuously monitor the health of all services and trigger recovery if needed.
        """
        while True:
            for service in self.services:
                if hasattr(service, "get_snapshot_state"):
                    try:
                        state = await service.get_snapshot_state()
                        print(f"Service {service.__class__.__name__} state: {state}")
                    except Exception as e:
                        print(f"Error monitoring service {service.__class__.__name__}: {e}")
                        # Trigger recovery logic for failed services
                        await self.recover_service(service)
            await asyncio.sleep(5)  # Monitor every 5 seconds

    async def recover_service(self, service):
        """
        Attempt to recover a failed service.
        """
        print(f"Attempting to recover service: {service.__class__.__name__}")
        try:
            if hasattr(service, "stop"):
                await service.stop()
            if hasattr(service, "start"):
                await service.start()
            print(f"Service {service.__class__.__name__} recovered successfully.")
        except Exception as e:
            print(f"Failed to recover service {service.__class__.__name__}: {e}")

    async def stop_services(self):
        """
        Stop all services gracefully.
        """
        print("Stopping services...")
        for service in self.services:
            if hasattr(service, "stop") and callable(service.stop):
                await service.stop()
        for task in self.tasks:
            task.cancel()
        await asyncio.gather(*self.tasks, return_exceptions=True)
        print("All services have been stopped.")

    def handle_task_completion(self, task):
        """
        Handle service task completion and trigger recovery if needed.
        """
        if task.exception():
            print(f"Service task failed: {task.exception()}")
            # Trigger recovery logic here

    async def start(self):
        """
        Start the Microkernel and all its components.
        """
        print("Starting Microkernel...")
        await self.initialize_core_components()
        await self.load_services()
        await self.start_services()

    async def stop(self):
        """
        Stop the Microkernel and all its components.
        """
        print("Stopping Microkernel...")
        await self.stop_services()
        print("Microkernel stopped.")

async def safe_task(task, task_name: str):
    try:
        await task
    except asyncio.CancelledError:
        print(f"Task {task_name} was cancelled.")
    except Exception as e:
        print(f"Error in {task_name}: {e}")
    finally:
        print(f"Task {task_name} has completed or been cancelled.")

async def main():
    # Load configuration
    from nexus_seed.config.loader import load_config
    config = load_config("/home/pong/Desktop/AIseed/config/system_config.json")

    # Initialize Microkernel
    kernel = Microkernel(config)
    await kernel.start()

    # Start services
    print("Starting Nexus Core services...")
    try:
        await kernel.start_services()
    except asyncio.CancelledError:
        print("Cancellation signal received. Shutting down tasks...")
    finally:
        await kernel.stop()
        print("All tasks have been shut down.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down Nexus Core...")