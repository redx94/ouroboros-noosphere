import unittest
import asyncio
from src.messaging import MessageBroker, Message

class TestMessageBroker(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.broker = MessageBroker()
        
    def tearDown(self):
        self.loop.close()
        
    def test_message_creation(self):
        message = Message.create(
            sender_id=1,
            recipient_id=2,
            message_type="test",
            payload={"data": "test"}
        )
        self.assertEqual(message.sender_id, 1)
        self.assertEqual(message.recipient_id, 2)
        self.assertEqual(message.message_type, "test")
        
    def test_subscription(self):
        async def test():
            queue = await self.broker.subscribe(1)
            self.assertIn(1, self.broker.subscribers)
            self.assertIn(queue, self.broker.subscribers[1])
            
        self.loop.run_until_complete(test())
        
    def test_message_publishing(self):
        async def test():
            queue = await self.broker.subscribe(1)
            message = Message.create(1, 1, "test", {"data": "test"})
            await self.broker.publish(message)
            
            received = await queue.get()
            self.assertEqual(received.payload["data"], "test")
            
        self.loop.run_until_complete(test())
        
    def test_message_broadcast(self):
        async def test():
            queues = [
                await self.broker.subscribe(i) for i in range(3)
            ]
            
            await self.broker.broadcast(
                sender_id=0,
                message_type="broadcast",
                payload={"data": "test"}
            )
            
            for queue in queues:
                msg = await queue.get()
                self.assertEqual(msg.message_type, "broadcast")
                self.assertEqual(msg.payload["data"], "test")
                
        self.loop.run_until_complete(test())
        
    def test_message_buffering(self):
        async def test():
            message = Message.create(1, 2, "test", {"data": "test"})
            await self.broker.publish(message)
            
            self.assertIn(2, self.broker.message_buffer)
            self.assertEqual(
                len(self.broker.message_buffer[2]), 1
            )
            
            queue = await self.broker.subscribe(2)
            await self.broker.deliver_buffered_messages(2, queue)
            
            received = await queue.get()
            self.assertEqual(received.payload["data"], "test")
            self.assertNotIn(2, self.broker.message_buffer)
            
        self.loop.run_until_complete(test())
