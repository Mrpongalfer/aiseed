import grpc
from protos import stats_pb2, stats_pb2_grpc
from nexus_seed.utils.event_bus import InternalEventBus
from nexus_seed.interfaces.events import EventTypes

class GRPCAdapter:
    def __init__(self, grpc_server_url: str, event_bus: InternalEventBus):
        self.grpc_server_url = grpc_server_url
        self.event_bus = event_bus

    async def publish_metrics(self, service_name: str, metrics: dict):
        async with grpc.aio.insecure_channel(self.grpc_server_url) as channel:
            stub = stats_pb2_grpc.StatsServiceStub(channel)
            request = stats_pb2.MetricsRequest(service_name=service_name, metrics=metrics)
            try:
                response = await stub.PublishMetrics(request)
                print(f"Metrics published: {response.status} - {response.message}")
            except grpc.RpcError as e:
                print(f"Failed to publish metrics: {e}")
                # Retry logic or fallback mechanism can be added here
