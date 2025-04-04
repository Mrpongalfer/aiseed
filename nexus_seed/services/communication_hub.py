from typing import Dict, Any, List
import asyncio

class CommunicationHub:
    def __init__(self):
        self.channels: Dict[str, List[asyncio.Queue]] = {}

    async def register_channel(self, channel_name: str) -> asyncio.Queue:
        """
        Register a new communication channel.
        """
        if channel_name not in self.channels:
            self.channels[channel_name] = []
        queue = asyncio.Queue()
        self.channels[channel_name].append(queue)
        print(f"Channel '{channel_name}' registered.")
        return queue

    async def register_agent_channel(self, agent_name: str) -> asyncio.Queue:
        """
        Dynamically register a communication channel for an agent.
        """
        channel_name = f"agent_{agent_name}"
        return await self.register_channel(channel_name)

    async def send_message(self, channel_name: str, message: Dict[str, Any]) -> None:
        """
        Send a message to all subscribers of a channel.
        """
        if channel_name in self.channels:
            for queue in self.channels[channel_name]:
                await queue.put(message)
            print(f"Message sent on channel '{channel_name}': {message}")
        else:
            print(f"Channel '{channel_name}' does not exist.")

    async def receive_message(self, queue: asyncio.Queue) -> Dict[str, Any]:
        """
        Receive a message from a subscribed channel.
        """
        message = await queue.get()
        print(f"Message received: {message}")
        return message
