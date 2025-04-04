from typing import Dict, Any

class ServiceMesh:
    def __init__(self):
        self.services: Dict[str, Any] = {}

    def register_service(self, name: str, service: Any) -> None:
        self.services[name] = service
        print(f"Service '{name}' registered.")

    def get_service(self, name: str) -> Any:
        return self.services.get(name, None)

    def list_services(self) -> Dict[str, Any]:
        return self.services

