import psutil
from typing import Dict

class PerformanceDashboard:
    @staticmethod
    def get_metrics() -> Dict[str, float]:
        try:
            return {
                "cpu_percent": psutil.cpu_percent(interval=1),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_usage": psutil.disk_usage('/').percent
            }
        except Exception as e:
            print(f"Error fetching system metrics: {e}")
            return {}
