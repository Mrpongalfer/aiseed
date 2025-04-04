import psutil
import asyncio
from typing import Dict

class SystemMonitorService:
    def __init__(self, publish_interval_sec: int = 5):
        self.publish_interval_sec = publish_interval_sec
        self.running = False
        self.goal_manager = None  # Placeholder for goal manager

    async def get_system_metrics(self) -> Dict[str, float]:
        return {
            "cpu_percent": psutil.cpu_percent(interval=None),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent
        }

    async def get_network_metrics(self) -> Dict[str, float]:
        try:
            net_io = psutil.net_io_counters()
            return {
                "bytes_sent": net_io.bytes_sent,
                "bytes_recv": net_io.bytes_recv,
                "packets_sent": net_io.packets_sent,
                "packets_recv": net_io.packets_recv
            }
        except Exception as e:
            print(f"Error fetching network metrics: {e}")
            return {}

    async def adjust_monitoring_interval(self, load: float):
        """
        Adjust the monitoring interval based on system load.
        """
        if load > 80.0:
            self.publish_interval_sec = max(1, self.publish_interval_sec - 1)
        elif load < 50.0:
            self.publish_interval_sec = min(10, self.publish_interval_sec + 1)
        print(f"Adjusted monitoring interval to {self.publish_interval_sec} seconds.")

    async def publish_stats(self) -> None:
        """
        Periodically fetch and publish system metrics, adapting to goals.
        """
        while self.running:
            try:
                metrics = await self.get_system_metrics()
                network_metrics = await self.get_network_metrics()
                combined_metrics = {**metrics, **network_metrics}

                # Adapt behavior based on goals
                if self.goal_manager:
                    self.goal_manager.update_goal("Resource Optimization", metrics["cpu_percent"])

                print(f"Publishing Metrics: {combined_metrics}")
            except Exception as e:
                print(f"Error while fetching or publishing system metrics: {e}")
            await asyncio.sleep(self.publish_interval_sec)

    async def monitor_deployment(self, deployment_id: str) -> None:
        """
        Monitor the deployment process and provide real-time feedback.
        """
        try:
            print(f"Monitoring deployment: {deployment_id}")
            # Example: Simulate monitoring
            for i in range(5):
                print(f"Deployment progress: {i * 20}%")
                await asyncio.sleep(1)
            print("Deployment completed successfully.")
        except Exception as e:
            print(f"Error monitoring deployment: {e}")

    async def start(self):
        print("SystemMonitorService started.")
        self.running = True
        try:
            await self.publish_stats()
        except asyncio.CancelledError:
            print("SystemMonitorService stopped.")
            self.running = False
