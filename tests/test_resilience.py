import pytest
import asyncio
from nexus_seed.kernel.snapshot_manager import SnapshotManager
from nexus_seed.services.persistence import PersistenceOverseer
from nexus_seed.utils.event_bus import InternalEventBus

@pytest.fixture
async def snapshot_manager():
    event_bus = InternalEventBus()
    persistence = PersistenceOverseer("postgresql://user:password@localhost:5432/nexusdb")
    await persistence.initialize()
    return SnapshotManager(event_bus, persistence)

@pytest.mark.asyncio
async def test_snapshot_recovery(snapshot_manager):
    # Simulate saving a snapshot
    snapshot_data = {"service_states": {"service1": {"state": "running"}}}
    await snapshot_manager.persistence.save_global_snapshot(snapshot_data)

    # Simulate recovery
    recovered_snapshot = await snapshot_manager.persistence.load_global_snapshot()
    assert recovered_snapshot == snapshot_data
