from typing import List

class PredictiveScaler:
    def __init__(self):
        self.metrics: List[float] = []

    def add_metric(self, value: float) -> None:
        self.metrics.append(value)

    def predict_scaling(self) -> str:
        if not self.metrics:
            return "No data available for prediction."
        avg = sum(self.metrics) / len(self.metrics)
        if avg > 80.0:
            return "Scale up"
        elif avg < 20.0:
            return "Scale down"
        return "Maintain current scale"

