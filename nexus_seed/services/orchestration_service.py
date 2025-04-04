import asyncio
import yaml
import os
from typing import Dict, Any
from nexus_seed.utils.event_bus import InternalEventBus
from nexus_seed.services.persistence import PersistenceOverseer

class OrchestratorService:
    def __init__(self, event_bus: InternalEventBus, persistence: PersistenceOverseer, workflows_dir: str):
        """
        Initialize the OrchestratorService with dependencies.
        """
        self.event_bus = event_bus
        self.persistence = persistence
        self.workflows_dir = workflows_dir
        self.active_workflows = {}
        self.running = False

    async def load_workflows(self) -> Dict[str, Any]:
        """
        Load declarative workflow definitions from the workflows directory.
        """
        workflows = {}
        for filename in os.listdir(self.workflows_dir):
            if filename.endswith(".yaml") or filename.endswith(".json"):
                filepath = os.path.join(self.workflows_dir, filename)
                with open(filepath, "r") as file:
                    workflows[filename] = yaml.safe_load(file)
        return workflows

    async def trigger_workflow(self, workflow_name: str, trigger_event: Dict[str, Any]) -> None:
        """
        Trigger a workflow based on its definition.
        """
        try:
            workflows = await self.load_workflows()
            workflow = workflows.get(workflow_name)
            if not workflow:
                raise ValueError(f"Workflow '{workflow_name}' not found.")

            print(f"Triggering workflow: {workflow_name}")
            self.active_workflows[workflow_name] = {"state": "running", "steps": []}

            for step in workflow.get("steps", []):
                step_type = step.get("type")
                step_params = step.get("params", {})
                if step_type == "event":
                    await self.event_bus.publish(step_params["event_type"], step_params["data"])
                elif step_type == "service_call":
                    service_name = step_params["service_name"]
                    method_name = step_params["method_name"]
                    service = getattr(self, service_name, None)
                    if service:
                        method = getattr(service, method_name, None)
                        if method:
                            await method(**step_params.get("args", {}))
                elif step_type == "decision":
                    decision_result = await self.make_decision(step_params)
                    print(f"Decision result: {decision_result}")
                self.active_workflows[workflow_name]["steps"].append(step)

            self.active_workflows[workflow_name]["state"] = "completed"
            print(f"Workflow '{workflow_name}' completed.")
        except Exception as e:
            print(f"Error triggering workflow '{workflow_name}': {e}")
            self.active_workflows[workflow_name]["state"] = "failed"

    async def make_decision(self, params: Dict[str, Any]) -> Any:
        """
        Make a decision using AI or predefined rules.
        """
        try:
            decision_type = params.get("type")
            if decision_type == "ai":
                # Example: Use AI model for decision-making
                input_data = params.get("input_data", {})
                decision = await self.event_bus.publish("ai_decision_request", input_data)
                return decision
            elif decision_type == "rule_based":
                # Example: Use predefined rules
                rules = params.get("rules", [])
                for rule in rules:
                    if rule["condition"](params):
                        return rule["action"]
            return "No decision made."
        except Exception as e:
            print(f"Error making decision: {e}")
            return None

    async def snapshot_workflow_states(self) -> None:
        """
        Persist active workflow states.
        """
        await self.persistence.save_global_snapshot(self.active_workflows)

    async def restore_workflow_states(self) -> None:
        """
        Restore active workflow states from the latest snapshot.
        """
        self.active_workflows = await self.persistence.load_global_snapshot() or {}

    async def optimize_workflows(self):
        """
        Automatically optimize workflows for efficiency.
        """
        try:
            workflows = await self.load_workflows()
            for workflow_name, workflow in workflows.items():
                # Example: Reorder steps based on priority
                workflow["steps"] = sorted(workflow["steps"], key=lambda step: step.get("priority", 0), reverse=True)
                await self.save_workflow(workflow_name, workflow)
                print(f"Optimized workflow: {workflow_name}")
        except Exception as e:
            print(f"Error optimizing workflows: {e}")

    async def start(self):
        print("OrchestrationService started.")
        self.running = True
        await self.restore_workflow_states()

    async def stop(self):
        print("OrchestrationService stopped.")
        self.running = False
        await self.snapshot_workflow_states()
