from typing import Dict, Any

class SecurityOverseer:
    def __init__(self):
        self.state = {}

    def detect_anomalies(self, metrics: Dict[str, float]) -> Dict[str, Any]:
        """
        Detect anomalies based on thresholding.
        """
        anomalies = {}
        for metric, value in metrics.items():
            if value > 90.0:
                anomalies[metric] = "High anomaly detected"
        return anomalies

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
