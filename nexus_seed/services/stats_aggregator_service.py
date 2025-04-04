import asyncio
from collections import deque
from typing import Deque

class StatsAggregatorService:
    def __init__(self, aggregation_interval_sec: int = 10, max_samples: int = 10):
        self.aggregation_interval_sec = aggregation_interval_sec
        self.samples: Deque[float] = deque(maxlen=max_samples)
        self.running = False

    def add_sample(self, sample: float) -> None:
        self.samples.append(sample)

    def calculate_rolling_average(self) -> float:
        if not self.samples:
            return 0.0
        return sum(self.samples) / len(self.samples)

    def predict_future_load(self) -> float:
        """
        Predict future system load based on historical data.
        """
        if not self.samples:
            return 0.0
        # Example prediction: Use the average of the last 3 samples
        prediction = sum(list(self.samples)[-3:]) / min(3, len(self.samples))
        print(f"Predicted future load: {prediction}")
        return prediction

    async def aggregate_stats(self) -> None:
        while self.running:
            try:
                rolling_avg = self.calculate_rolling_average()
                print(f"Rolling Average: {rolling_avg}")
                # Example: Publish aggregated stats to event bus or external system
            except Exception as e:
                print(f"Error while aggregating stats: {e}")
            await asyncio.sleep(self.aggregation_interval_sec)

    async def optimize_system_metrics(self):
        """
        Optimize system metrics based on rolling average thresholds.
        """
        try:
            rolling_avg = self.calculate_rolling_average()
            if rolling_avg > 80.0:
                print("Warning: High system load detected. Initiating optimization...")

                # Example optimization: Reduce CPU-intensive tasks
                print("Pausing non-critical services to reduce load...")
                # Add logic to pause or reschedule tasks here

                print("Optimization complete. System load reduced.")
            else:
                print("System load is within acceptable limits. No optimization required.")
        except Exception as e:
            print(f"Error optimizing system metrics: {e}")

    async def start(self):
        print("StatsAggregatorService started.")
        self.running = True
        try:
            await self.aggregate_stats()
        except asyncio.CancelledError:
            print("StatsAggregatorService stopped.")
            self.running = False
