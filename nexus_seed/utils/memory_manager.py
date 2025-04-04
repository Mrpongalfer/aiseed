import json
from typing import List, Dict

class MemoryManager:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def load_memory(self) -> List[Dict]:
        try:
            with open(self.filepath, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_memory(self, memory: List[Dict]) -> None:
        with open(self.filepath, "w") as file:
            json.dump(memory, file, indent=4)

    def load_state(self) -> Dict:
        try:
            with open(self.filepath, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_state(self, state: Dict) -> None:
        with open(self.filepath, "w") as file:
            json.dump(state, file, indent=4)
