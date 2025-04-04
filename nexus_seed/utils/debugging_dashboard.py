from typing import Dict

class DebuggingDashboard:
    def __init__(self):
        self.logs: Dict[str, str] = {}

    def log(self, component: str, message: str) -> None:
        self.logs[component] = message
        print(f"[{component}] {message}")

    def get_logs(self) -> Dict[str, str]:
        return self.logs

