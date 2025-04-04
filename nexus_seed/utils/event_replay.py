from typing import List, Dict

class EventReplay:
    def __init__(self):
        self.events: List[Dict] = []

    def record_event(self, event: Dict) -> None:
        self.events.append(event)
        print(f"Event recorded: {event}")

    def replay_events(self) -> None:
        for event in self.events:
            print(f"Replaying event: {event}")

