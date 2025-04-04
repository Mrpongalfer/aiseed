import pytest
import asyncio
from nexus_seed.utils.event_bus import EventBus

@pytest.fixture
def event_bus():
    return EventBus()

@pytest.mark.asyncio
async def test_event_subscription_and_publish(event_bus):
    results = []

    async def callback(event):
        results.append(event)

    await event_bus.subscribe("test_event", callback)
    await event_bus.publish("test_event", {"key": "value"})

    await asyncio.sleep(0.1)  # Allow time for async callback
    assert len(results) == 1
    assert results[0] == {"key": "value"}
