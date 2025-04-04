import asyncio
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers
from nexus_seed.utils.event_bus import InternalEventBus
from nexus_seed.interfaces.events import EventTypes

class NATSAdapter:
    def __init__(self, nats_url: str, event_bus: InternalEventBus):
        self.nats_url = nats_url
        self.event_bus = event_bus
        self.nc = NATS()

    async def connect(self):
        try:
            await self.nc.connect(servers=[self.nats_url], reconnect_time_wait=2)
            print(f"Connected to NATS at {self.nats_url}")
        except ErrNoServers as e:
            print(f"Failed to connect to NATS: {e}")
            await asyncio.sleep(5)
            await self.connect()  # Retry connection

    async def subscribe(self, subject: str):
        async def message_handler(msg):
            data = msg.data.decode()
            print(f"Received message on {subject}: {data}")
            await self.event_bus.publish(EventTypes.SERVICE_STATE_UPDATED.value, {"subject": subject, "data": data})

        await self.nc.subscribe(subject, cb=message_handler)

    async def publish(self, subject: str, data: dict):
        try:
            await self.nc.publish(subject, str(data).encode())
            print(f"Published message to {subject}: {data}")
        except ErrConnectionClosed:
            print("Connection to NATS is closed.")
