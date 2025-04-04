from typing import Dict, Any

class ValidationService:
    def __init__(self, goal_manager):
        self.goal_manager = goal_manager

    def validate_action(self, action: Dict[str, Any]) -> bool:
        """
        Validate that an action aligns with system goals and principles.
        """
        if not self.goal_manager.validate_principles(action):
            print(f"Action '{action['name']}' violates principles.")
            return False
        print(f"Action '{action['name']}' is valid.")
        return True

    def validate_pipeline(self, pipeline_config: Dict[str, Any]) -> bool:
        """
        Validate the CI/CD pipeline configuration.
        """
        required_keys = ["name", "on", "jobs"]
        for key in required_keys:
            if key not in pipeline_config:
                print(f"Pipeline validation failed: Missing key '{key}'")
                return False
        print("Pipeline validation passed.")
        return True

    def validate_deployment(self, deployment_status: Dict[str, Any]) -> bool:
        """
        Validate the deployment status.
        """
        if deployment_status.get("status") != "success":
            print(f"Deployment validation failed: {deployment_status.get('message')}")
            return False
        print("Deployment validation passed.")
        return True
