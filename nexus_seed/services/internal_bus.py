import asyncio
from typing import Callable, Dict, List, Coroutine, Any

class InternalEventBus:
    def __init__(self):
        self.subscribers: Dict[str, List[Callable[[Any], Coroutine]]] = {}

    async def subscribe(self, event_type: str, callback: Callable[[Any], Coroutine]) -> None:
        """
        Subscribe to a specific event type.
        """
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)
        print(f"Subscribed to event type '{event_type}'")

    async def publish(self, event_type: str, data: Any) -> None:
        """
        Publish an event to all subscribers of the given event type.
        """
        if event_type in self.subscribers:
            tasks = []
            for callback in self.subscribers[event_type]:
                tasks.append(asyncio.create_task(self._safe_callback(callback, data)))
            await asyncio.gather(*tasks)
        else:
            print(f"No subscribers for event type: {event_type}")

    async def _safe_callback(self, callback: Callable[[Any], Coroutine], data: Any) -> None:
        """
        Safely execute a callback with error handling.
        """
        try:
            await callback(data)
        except Exception as e:
            print(f"Error in callback for event type '{data}': {e}")
