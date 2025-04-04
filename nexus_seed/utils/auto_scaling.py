from typing import List

class AutoScaler:
    def __init__(self):
        self.metrics: List[float] = []

    def add_metric(self, value: float) -> None:
        self.metrics.append(value)

    def scale(self) -> str:
        if not self.metrics:
            return "No data available for scaling."
        avg = sum(self.metrics) / len(self.metrics)
        if avg > 75.0:
            return "Scaling up"
        elif avg < 25.0:
            return "Scaling down"
        return "Maintaining current scale"

