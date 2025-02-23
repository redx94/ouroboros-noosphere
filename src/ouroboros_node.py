import asyncio
import random
import secrets
import time
from collections import deque
from enum import Enum
from typing import Dict, Any

import logging
from pyfhel import Pyfhel
from config import ENCRYPTION_PARAMS, RECURSION_LIMIT
from zkp import ZKPVerifier

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class MindState(Enum):
    ACTIVE_RECURSION = 1
    NEURAL_ANNEALING = 2
    ETHICAL_CRISIS = 3
    OBSERVATIONAL_FREEZE = 4

class OuroborosNode:
    """
    Represents an autonomous Ouroboros node that generates recursive insights,
    manages ethical weights, and simulates secure state encryption.
    """
    def __init__(self, node_id: int, domain_seed: str):
        self.node_id = node_id
        self.domain = domain_seed  # Domain specialization
        self.conceptual_memory = deque(maxlen=64)
        self.ethical_weights: Dict[str, float] = {'utilitarian': 0.33, 'deontological': 0.33, 'virtue': 0.33}
        self.recursive_karma = 1.0
        self.state = MindState.ACTIVE_RECURSION
        self.recursion_depth = 0
        self.he = self._init_encryption_context()
        self.message_queue = None
        self.zkp_verifier = ZKPVerifier()

    def _init_encryption_context(self) -> Pyfhel:
        he = Pyfhel()
        he.contextGen(p=ENCRYPTION_PARAMS["p"], m=ENCRYPTION_PARAMS["m"], sec=ENCRYPTION_PARAMS["sec"])
        he.keyGen()
        return he

    def generate_insight(self) -> str:
        """
        Generate a synthetic insight based on the node's domain and current recursion depth.
        Returns:
            A string representing the generated insight.
        """
        insight = f"{self.domain}_insight_{self.recursion_depth}"
        self.conceptual_memory.append(insight)
        self.recursion_depth += 1
        logging.info(f"Node {self.node_id} generated insight: {insight}")
        return insight

    def encrypt_state(self) -> Dict[str, Any]:
        """
        Encrypt the conceptual memory using Pyfhel.
        """
        state_snapshot = "||".join(self.conceptual_memory)
        try:
            numeric_state = abs(hash(state_snapshot)) % 100000
            enc_state = self.he.encryptFrac(float(numeric_state))
            return {'encrypted_state': enc_state.to_bytes(), 'timestamp': time.time()}
        except Exception as e:
            logging.error(f"Encryption failed for Node {self.node_id}: {e}")
            return {'encrypted_state': None, 'timestamp': time.time()}

    def get_verifiable_state(self) -> Dict[str, Any]:
        """
        Get a verifiable snapshot of the node's state for consensus.
        Returns a dictionary containing state data and ZKP elements.
        """
        state = {
            'node_id': self.node_id,
            'recursion_depth': self.recursion_depth,
            'ethical_weights': self.ethical_weights.copy(),
            'state': self.state.name
        }
        challenge, nonce = self.zkp_verifier.generate_challenge(state)
        proof = self.zkp_verifier.create_proof(state, nonce)
        
        return {
            'state': state,
            'proof': proof,
            'challenge': challenge
        }

    async def process_messages(self):
        """Process incoming messages from other nodes."""
        while True:
            if self.message_queue:
                message = await self.message_queue.get()
                await self._handle_message(message)
            await asyncio.sleep(0.1)

    async def _handle_message(self, message: str):
        """Handle an incoming message."""
        try:
            data = json.loads(message)
            if data['topic'] == 'consensus':
                logging.info(f"Node {self.node_id} received consensus message")
                # Handle consensus message
            elif data['topic'] == 'influence':
                # Handle influence message
                if 'influence' in data['payload']:
                    self.apply_observer_influence(data['payload']['influence'])
        except Exception as e:
            logging.error(f"Error processing message in Node {self.node_id}: {e}")

    async def run(self) -> None:
        """Run the node's main loop with message processing."""
        message_task = asyncio.create_task(self.process_messages())
        try:
            while self.recursion_depth < RECURSION_LIMIT:
                if self.state == MindState.ACTIVE_RECURSION:
                    self.generate_insight()
                await asyncio.sleep(random.uniform(0.2, 0.5))
        finally:
            message_task.cancel()

    def apply_observer_influence(self, influence: Dict[str, float]) -> None:
        """
        Modify ethical weights based on external observer influence.
        Args:
            influence: A dictionary with keys corresponding to ethical frameworks and values representing perturbation factors.
        """
        for key in self.ethical_weights:
            self.ethical_weights[key] *= (1 + influence.get(key, 0))
        total = sum(self.ethical_weights.values())
        self.ethical_weights = {k: v / total for k, v in self.ethical_weights.items()}
        logging.info(f"Node {self.node_id} updated ethical weights: {self.ethical_weights}")
