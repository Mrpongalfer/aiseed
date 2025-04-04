import random

class ChaosTester:
    @staticmethod
    def introduce_failure() -> None:
        try:
            if random.random() < 0.1:  # 10% chance of failure
                raise Exception("Simulated chaos failure!")
            print("No failure introduced.")
        except Exception as e:
            print(f"Chaos failure occurred: {e}")
