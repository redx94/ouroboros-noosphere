import unittest
from src.metrics import MetricsCollector, NetworkMetrics, NodeMetrics
import time

class TestMetricsCollector(unittest.TestCase):
    def setUp(self):
        self.metrics = MetricsCollector()
        
    def test_network_metrics_collection(self):
        test_state = {
            'nodes': [
                {'id': 1, 'trust_score': 0.8, 'ethical_weights': {'util': 0.5}},
                {'id': 2, 'trust_score': 0.9, 'ethical_weights': {'util': 0.5}}
            ],
            'consensus_count': 10,
            'message_count': 100,
            'validations': 50
        }
        
        async def test():
            metrics = await self.metrics.collect_metrics(test_state)
            self.assertEqual(metrics.node_count, 2)
            self.assertEqual(metrics.consensus_rounds, 10)
            self.assertAlmostEqual(metrics.average_trust, 0.85)
            
        loop = asyncio.get_event_loop()
        loop.run_until_complete(test())
        
    def test_diversity_calculation(self):
        nodes = [
            {'ethical_weights': {'util': 0.5, 'deont': 0.5}},
            {'ethical_weights': {'util': 0.7, 'deont': 0.3}}
        ]
        
        diversity = self.metrics._calculate_diversity(nodes)
        self.assertGreater(diversity, 0)
        
    def test_report_generation(self):
        test_event = {
            'type': 'consensus',
            'data': {'round': 1}
        }
        self.metrics.track_event(test_event['type'], test_event['data'])
        
        report = self.metrics.get_report()
        self.assertIn('uptime', report)
        self.assertIn('recent_events', report)
        
    def test_network_health(self):
        node = type('MockNode', (), {
            'node_id': 1,
            'recursion_depth': 5,
            'ethical_weights': {'util': 0.33, 'deont': 0.33, 'virtue': 0.34},
            'conceptual_memory': ['test']
        })
        
        self.metrics.record_node_metrics(node)
        health_score = self.metrics.get_network_health()
        self.assertGreaterEqual(health_score, 0.0)
        self.assertLessEqual(health_score, 1.0)
