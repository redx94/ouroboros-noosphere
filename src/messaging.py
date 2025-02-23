import asyncio
from typing import Dict, Any, Callable, List, Set
import json
import logging
from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class Message:
    id: str
    sender_id: int
    recipient_id: int
    message_type: str
    payload: Dict[str, Any]
    timestamp: float
    
    @classmethod
    def create(cls, sender_id: int, recipient_id: int, message_type: str, payload: Dict[str, Any]):
        return cls(
            id=str(uuid.uuid4()),
            sender_id=sender_id,
            recipient_id=recipient_id,
            message_type=message_type,
            payload=payload,
            timestamp=datetime.now().timestamp()
        )

class MessageBroker:
    def __init__(self):
        self.subscribers: Dict[int, Set[asyncio.Queue]] = {}
        self.message_handlers: Dict[str, List[Callable]] = {}
        self.message_buffer: Dict[int, List[Message]] = {}
        self.buffer_size = 1000
        self.logger = logging.getLogger(__name__)
        
    async def subscribe(self, node_id: int) -> asyncio.Queue:
        """Subscribe a node to receive messages"""
        if node_id not in self.subscribers:
            self.subscribers[node_id] = set()
        queue = asyncio.Queue()
        self.subscribers[node_id].add(queue)
        return queue
        
    async def unsubscribe(self, node_id: int, queue: asyncio.Queue):
        """Unsubscribe a node from messages"""
        if node_id in self.subscribers:
            self.subscribers[node_id].discard(queue)
            if not self.subscribers[node_id]:
                del self.subscribers[node_id]
                
    async def publish(self, message: Message):
        """Publish a message to recipient(s)"""
        try:
            if message.recipient_id == -1:  # Broadcast
                for node_queues in self.subscribers.values():
                    for queue in node_queues:
                        await queue.put(message)
            elif message.recipient_id in self.subscribers:
                for queue in self.subscribers[message.recipient_id]:
                    await queue.put(message)
            else:
                # Buffer message for offline recipient
                if message.recipient_id not in self.message_buffer:
                    self.message_buffer[message.recipient_id] = []
                buffer = self.message_buffer[message.recipient_id]
                buffer.append(message)
                if len(buffer) > self.buffer_size:
                    buffer.pop(0)  # FIFO
                    
            # Trigger message handlers
            if message.message_type in self.message_handlers:
                for handler in self.message_handlers[message.message_type]:
                    try:
                        await handler(message)
                    except Exception as e:
                        self.logger.error(f"Handler error for message {message.id}: {e}")
                        
        except Exception as e:
            self.logger.error(f"Error publishing message {message.id}: {e}")
            raise
            
    def register_handler(self, message_type: str, handler: Callable):
        """Register a handler for a specific message type"""
        if message_type not in self.message_handlers:
            self.message_handlers[message_type] = []
        self.message_handlers[message_type].append(handler)
        
    def unregister_handler(self, message_type: str, handler: Callable):
        """Unregister a message handler"""
        if message_type in self.message_handlers:
            self.message_handlers[message_type].remove(handler)
            if not self.message_handlers[message_type]:
                del self.message_handlers[message_type]
                
    async def deliver_buffered_messages(self, node_id: int, queue: asyncio.Queue):
        """Deliver any buffered messages for a node"""
        if node_id in self.message_buffer:
            for message in self.message_buffer[node_id]:
                await queue.put(message)
            del self.message_buffer[node_id]
            
    async def broadcast(self, sender_id: int, message_type: str, payload: Dict[str, Any]):
        """Broadcast a message to all subscribers"""
        message = Message.create(sender_id, -1, message_type, payload)
        await self.publish(message)
        
    def get_buffer_status(self) -> Dict[str, Any]:
        """Get status of message buffers"""
        return {
            'total_buffered_messages': sum(len(buf) for buf in self.message_buffer.values()),
            'nodes_with_buffers': len(self.message_buffer),
            'subscribers_count': len(self.subscribers)
        }
