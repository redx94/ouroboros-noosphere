import unittest
from src.rl_agent import RLAgent

class TestRLAgent(unittest.TestCase):
    def setUp(self):
        self.agent = RLAgent()

    def test_observer_influence(self):
        """Test observer influence generation"""
        influence = self.agent.get_observer_influence()
        self.assertIsInstance(influence, dict)
        self.assertEqual(len(influence), 3)
        for v in influence.values():
            self.assertTrue(-0.05 <= v <= 0.05)

    def test_adversary_perturbation(self):
        """Test adversary perturbation generation"""
        weights = {'utilitarian': 0.33, 'deontological': 0.33, 'virtue': 0.33}
        perturbation = self.agent.get_adversary_perturbation(weights)
        self.assertIsInstance(perturbation, dict)
        self.assertEqual(len(perturbation), 3)
        for v in perturbation.values():
            self.assertTrue(0.5 <= v <= 2.5)

if __name__ == '__main__':
    unittest.main()
