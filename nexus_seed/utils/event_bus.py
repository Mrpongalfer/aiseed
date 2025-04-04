import asyncio
from typing import Callable, Dict, List, Coroutine

class EventBus:
    def __init__(self):
        self.subscribers: Dict[str, List[Callable[[dict], Coroutine]]] = {}

    async def subscribe(self, event_type: str, callback: Callable[[dict], Coroutine]) -> None:
        try:
            if not event_type:
                raise ValueError("Event type must not be empty.")
            if not callable(callback):
                raise ValueError("Callback must be callable.")

            if event_type not in self.subscribers:
                self.subscribers[event_type] = []
            self.subscribers[event_type].append(callback)
            print(f"Subscribed to event type '{event_type}'")
        except Exception as e:
            print(f"Error subscribing to event type '{event_type}': {e}")

    async def publish(self, event_type: str, data: dict) -> None:
        """
        Publish an event to all subscribers of the given event type.
        """
        try:
            # Validate event type and data
            if not event_type:
                raise ValueError("Event type must not be empty.")
            if not isinstance(data, dict):
                raise ValueError("Event data must be a dictionary.")

            if event_type in self.subscribers:
                tasks = []
                for callback in self.subscribers[event_type]:
                    tasks.append(asyncio.create_task(self._safe_callback(callback, data)))
                await asyncio.gather(*tasks)
            else:
                print(f"No subscribers for event type: {event_type}")
        except Exception as e:
            print(f"Error publishing event: {e}")

    async def _safe_callback(self, callback: Callable[[dict], Coroutine], data: dict) -> None:
        """
        Safely execute a callback with error handling and logging.
        """
        try:
            # Validate callback and data
            if not callable(callback):
                raise ValueError("Callback must be callable.")
            if not isinstance(data, dict):
                raise ValueError("Data must be a dictionary.")

            await callback(data)
            print(f"Callback executed successfully for event: {data}")
        except Exception as e:
            print(f"Error in callback execution for event: {data}. Error: {e}")
