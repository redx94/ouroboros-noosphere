import asyncio
import json
from typing import Dict, Any
import logging

class MessageBroker:
    """Handles asynchronous message passing between nodes."""
    
    def __init__(self):
        self.message_queues: Dict[int, asyncio.Queue] = {}
        self.subscribers = []

    async def publish(self, topic: str, message: Dict[str, Any]) -> None:
        """Publish a message to all subscribers."""
        encoded_message = json.dumps({
            'topic': topic,
            'payload': message,
            'timestamp': asyncio.get_event_loop().time()
        })
        
        for subscriber in self.subscribers:
            await self.message_queues[subscriber].put(encoded_message)
        
        logging.info(f"Published message to {len(self.subscribers)} subscribers on topic: {topic}")

    async def subscribe(self, node_id: int) -> asyncio.Queue:
        """Subscribe a node to receive messages."""
        if node_id not in self.message_queues:
            self.message_queues[node_id] = asyncio.Queue()
            self.subscribers.append(node_id)
        return self.message_queues[node_id]
