import unittest
from src.zkp import SchnorrZKP, ZKPManager

class TestSchnorrZKP(unittest.TestCase):
    def setUp(self):
        self.zkp = SchnorrZKP()
        
    def test_keypair_generation(self):
        private_key, public_key = self.zkp.generate_keypair()
        self.assertIsInstance(private_key, int)
        self.assertIsInstance(public_key, int)
        self.assertTrue(0 < private_key < self.zkp.q)
        
    def test_proof_verification(self):
        private_key, public_key = self.zkp.generate_keypair()
        state_hash = b"test_state"
        proof = self.zkp.create_proof(private_key, state_hash)
        
        self.assertTrue(
            self.zkp.verify_proof(public_key, state_hash, proof)
        )
        
    def test_invalid_proof_rejection(self):
        private_key, public_key = self.zkp.generate_keypair()
        state_hash = b"test_state"
        proof = self.zkp.create_proof(private_key, state_hash)
        
        # Tamper with proof
        proof['s'] = (proof['s'] + 1) % self.zkp.q
        
        self.assertFalse(
            self.zkp.verify_proof(public_key, state_hash, proof)
        )

class TestZKPManager(unittest.TestCase):
    def setUp(self):
        self.manager = ZKPManager()
        
    def test_node_initialization(self):
        node_id = 1
        public_key = self.manager.initialize_node(node_id)
        self.assertIn(node_id, self.manager.keypairs)
        self.assertEqual(len(self.manager.keypairs[node_id]), 2)
        
    def test_state_proof_creation_verification(self):
        node_id = 1
        self.manager.initialize_node(node_id)
        
        test_state = {"ethical_weights": {"utilitarian": 0.33}}
        proof_data = self.manager.create_state_proof(node_id, test_state)
        
        self.assertTrue(
            self.manager.verify_state_proof(node_id, test_state, proof_data)
        )
        
    def test_uninitialized_node_error(self):
        with self.assertRaises(ValueError):
            self.manager.create_state_proof(999, {})
