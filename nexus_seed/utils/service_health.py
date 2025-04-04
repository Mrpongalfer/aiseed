from typing import Dict

class ServiceHealthMonitor:
    def __init__(self):
        self.services: Dict[str, str] = {}

    def register_service(self, name: str, status: str = "healthy") -> None:
        self.services[name] = status
        print(f"Service '{name}' registered with status '{status}'.")

    def update_status(self, name: str, status: str) -> None:
        if name in self.services:
            self.services[name] = status
            print(f"Service '{name}' status updated to '{status}'.")
        else:
            print(f"Error: Service '{name}' not found.")

    def get_health_report(self) -> Dict[str, str]:
        return self.services
