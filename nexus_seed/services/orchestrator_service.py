import asyncio
import os
import yaml
from typing import Dict, Any

class OrchestratorService:
    def __init__(self, event_bus, persistence, workflows_dir):
        """
        Initialize the OrchestratorService with dependencies.
        """
        self.event_bus = event_bus
        self.persistence = persistence
        self.workflows_dir = workflows_dir
        self.active_workflows = {}
        self.event_queue = asyncio.Queue()
        self.running = False

    async def publish_event(self, event: Dict[str, Any]) -> None:
        """
        Publish an event to the event queue.
        """
        try:
            # Validate event structure
            if "type" not in event:
                raise ValueError("Event must have a 'type' field.")
            if "params" not in event:
                event["params"] = {}  # Ensure params exist as an empty dictionary

            await self.event_queue.put(event)
            print(f"Event published: {event}")
        except Exception as e:
            print(f"Error while publishing event: {e}")
            raise

    async def validate_workflow(self, workflow: Dict[str, Any]) -> bool:
        """
        Validate the structure of a workflow definition.
        """
        required_keys = {"steps"}
        if not all(key in workflow for key in required_keys):
            print(f"Invalid workflow: Missing required keys {required_keys}")
            return False
        return True

    async def process_events(self) -> None:
        """
        Process events from the event queue with dynamic routing.
        """
        while self.running:
            try:
                event = await self.event_queue.get()
                print(f"Processing event: {event}")

                # Validate event structure
                event_type = event.get("type")
                params = event.get("params", {})
                if not event_type:
                    raise ValueError("Event type is missing.")

                # Dynamic routing based on event type
                if event_type.startswith("core_"):
                    await self.event_bus.publish(event_type, params)
                elif event_type.startswith("workflow_"):
                    await self.trigger_workflow(event_type.replace("workflow_", ""), params)
                else:
                    print(f"Unhandled event type: {event_type}")

                self.event_queue.task_done()
            except Exception as e:
                print(f"Error while processing event: {e}")
            await asyncio.sleep(1)

    async def save_workflow(self, workflow_name: str, workflow: Dict[str, Any]) -> None:
        """
        Save an optimized workflow to the workflows directory.
        """
        try:
            filepath = os.path.join(self.workflows_dir, f"{workflow_name}.yaml")
            with open(filepath, "w") as file:
                yaml.safe_dump(workflow, file)
            print(f"Workflow '{workflow_name}' saved successfully.")
        except Exception as e:
            print(f"Error saving workflow '{workflow_name}': {e}")

    async def evolve_workflow(self, workflow_name: str) -> None:
        """
        Evolve a workflow by applying mutations and evaluating fitness.
        """
        try:
            workflows = await self.load_workflows()
            workflow = workflows.get(workflow_name)
            if not workflow:
                raise ValueError(f"Workflow '{workflow_name}' not found.")

            print(f"Evolving workflow: {workflow_name}")
            # Example: Apply mutations
            workflow["steps"].append({"type": "log", "params": {"message": "New step added"}})

            # Example: Evaluate fitness
            fitness = len(workflow["steps"])  # Simplified fitness evaluation
            print(f"Workflow '{workflow_name}' fitness: {fitness}")

            # Save evolved workflow
            await self.save_workflow(workflow_name, workflow)
            print(f"Workflow '{workflow_name}' evolved successfully.")
        except Exception as e:
            print(f"Error evolving workflow '{workflow_name}': {e}")

    async def trigger_workflow(self, workflow_name: str, trigger_event: Dict[str, Any]) -> None:
        """
        Trigger a workflow and validate its alignment with principles.
        """
        try:
            workflows = await self.load_workflows()
            workflow = workflows.get(workflow_name)
            if not workflow:
                raise ValueError(f"Workflow '{workflow_name}' not found.")

            # Validate workflow alignment with principles
            if not self.goal_manager.validate_principles({"name": workflow_name, "alignment": workflow.get("alignment", [])}):
                print(f"Workflow '{workflow_name}' violates principles. Aborting.")
                return

            print(f"Triggering workflow: {workflow_name}")
            # ...existing code...
        except Exception as e:
            print(f"Error triggering workflow '{workflow_name}': {e}")

    async def create_workflow(self, workflow_name: str, workflow_definition: Dict[str, Any]) -> None:
        """
        Dynamically create a new workflow.
        """
        try:
            filepath = os.path.join(self.workflows_dir, f"{workflow_name}.yaml")
            with open(filepath, "w") as file:
                yaml.safe_dump(workflow_definition, file)
            print(f"Workflow '{workflow_name}' created successfully.")
        except Exception as e:
            print(f"Error creating workflow '{workflow_name}': {e}")

    async def execute_workflow(self, workflow_name: str, params: Dict[str, Any]) -> None:
        """
        Execute a workflow dynamically.
        """
        try:
            print(f"Executing workflow '{workflow_name}' with params: {params}")
            await self.trigger_workflow(workflow_name, params)
        except Exception as e:
            print(f"Error executing workflow '{workflow_name}': {e}")

    async def start(self):
        print("OrchestratorService started.")
        self.running = True
        try:
            await self.process_events()
        except asyncio.CancelledError:
            print("OrchestratorService stopped.")
            self.running = False
