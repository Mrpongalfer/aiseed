from nexus_seed.adapters.nats_adapter import NATSAdapter
from nexus_seed.adapters.grpc_adapter import GRPCAdapter
import asyncio

class ExternalCommsOverseer:
    def __init__(self, nats_adapter: NATSAdapter, grpc_adapter: GRPCAdapter):
        self.nats_adapter = nats_adapter
        self.grpc_adapter = grpc_adapter

    async def start(self):
        await self.nats_adapter.connect()
        print("ExternalCommsOverseer started.")

    async def transform_message(self, message: dict) -> dict:
        """
        Transform a message before routing it to the target adapter.
        """
        try:
            # Example transformation: Add a timestamp
            message["timestamp"] = asyncio.get_event_loop().time()
            return message
        except Exception as e:
            print(f"Error transforming message: {e}")
            return message

    async def route_message(self, message: dict, target: str):
        """
        Route a message to the appropriate adapter with error recovery.
        """
        try:
            transformed_message = await self.transform_message(message)
            if target == "nats":
                await self.nats_adapter.publish(transformed_message["subject"], transformed_message["data"])
            elif target == "grpc":
                await self.grpc_adapter.publish_metrics(transformed_message["service_name"], transformed_message["metrics"])
            elif target == "custom_protocol":
                print(f"Routing message using custom protocol: {transformed_message}")
            else:
                print(f"Unknown target: {target}")
        except Exception as e:
            print(f"Error routing message: {e}")
            await asyncio.sleep(1)
            await self.route_message(message, target)
