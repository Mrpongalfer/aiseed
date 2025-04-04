import json
from typing import Dict, List

class SharedKnowledgeBase:
    def __init__(self, filepath: str = "/home/pong/Desktop/AIseed/logs/shared_knowledge.json"):
        self.filepath = filepath
        self.knowledge = self.load_knowledge()

    def add_entry(self, key: str, value: dict) -> None:
        """
        Add an entry to the shared knowledge base.
        """
        self.knowledge[key] = value
        self.save_knowledge()
        print(f"Added entry to Shared Knowledge Base: {key}")

    def get_entry(self, key: str) -> dict:
        """
        Retrieve an entry from the shared knowledge base.
        """
        return self.knowledge.get(key, {})

    def list_entries(self) -> List[str]:
        """
        List all keys in the shared knowledge base.
        """
        return list(self.knowledge.keys())

    def log_intent(self, intent: str, task: str, outcome: str) -> None:
        """
        Log an intent, its mapped task, and the outcome.
        """
        log_entry = {"intent": intent, "task": task, "outcome": outcome}
        self.knowledge.setdefault("intent_logs", []).append(log_entry)
        self.save_knowledge()
        print(f"Logged intent: {intent} -> Task: {task} -> Outcome: {outcome}")

    def query_knowledge(self, query: str) -> List[dict]:
        """
        Query the shared knowledge base using a simple keyword search.
        """
        results = []
        for key, value in self.knowledge.items():
            if query.lower() in key.lower() or query.lower() in json.dumps(value).lower():
                results.append({key: value})
        print(f"Query results for '{query}': {results}")
        return results

    def merge_knowledge(self, external_knowledge: Dict) -> None:
        """
        Merge external knowledge into the shared knowledge base.
        """
        for key, value in external_knowledge.items():
            if key in self.knowledge:
                # Example: Merge dictionaries or append lists
                if isinstance(self.knowledge[key], dict) and isinstance(value, dict):
                    self.knowledge[key].update(value)
                elif isinstance(self.knowledge[key], list) and isinstance(value, list):
                    self.knowledge[key].extend(value)
                else:
                    self.knowledge[key] = value  # Overwrite if types differ
            else:
                self.knowledge[key] = value
        self.save_knowledge()
        print(f"Merged external knowledge into Shared Knowledge Base.")

    def load_knowledge(self) -> Dict:
        """
        Load the shared knowledge base from a file.
        """
        try:
            with open(self.filepath, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_knowledge(self) -> None:
        """
        Save the shared knowledge base to a file.
        """
        with open(self.filepath, "w") as file:
            json.dump(self.knowledge, file, indent=4)
