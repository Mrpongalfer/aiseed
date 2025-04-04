from typing import Dict, Any

class HybridOptimizerOverseer:
    def __init__(self):
        self.state = {}

    def generate_guidance(self, metrics: Dict[str, float]) -> Dict[str, Any]:
        """
        Generate optimization guidance based on metrics.
        """
        guidance = {}
        for metric, value in metrics.items():
            if metric == "cpu_usage" and value > 80.0:
                guidance[metric] = "Reduce CPU load by pausing non-critical tasks."
            elif metric == "memory_usage" and value > 75.0:
                guidance[metric] = "Free up memory by clearing caches."
            else:
                guidance[metric] = "Maintain current state."
        return guidance

    async def get_snapshot_state(self) -> Dict[str, Any]:
        """
        Get the current state of the overseer for snapshotting.
        """
        return self.state

    async def restore_snapshot_state(self, state: Dict[str, Any]) -> None:
        """
        Restore the overseer state from a snapshot.
        """
        self.state = state
