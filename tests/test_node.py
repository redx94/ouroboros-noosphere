import unittest
from src.ouroboros_node import OuroborosNode, MindState

class TestOuroborosNode(unittest.TestCase):
    def setUp(self):
        self.node = OuroborosNode(node_id=1, domain_seed='utilitarian')

    def test_node_initialization(self):
        """Test node initialization with correct parameters"""
        self.assertEqual(self.node.node_id, 1)
        self.assertEqual(self.node.domain, 'utilitarian')
        self.assertEqual(self.node.state, MindState.ACTIVE_RECURSION)
        self.assertEqual(len(self.node.ethical_weights), 3)

    def test_insight_generation(self):
        """Test insight generation and memory management"""
        insight = self.node.generate_insight()
        self.assertIsInstance(insight, str)
        self.assertIn('utilitarian', insight)
        self.assertEqual(len(self.node.conceptual_memory), 1)

    def test_state_encryption(self):
        """Test state encryption functionality"""
        self.node.generate_insight()
        encrypted_state = self.node.encrypt_state()
        self.assertIn('encrypted_state', encrypted_state)
        self.assertIn('timestamp', encrypted_state)

if __name__ == '__main__':
    unittest.main()
