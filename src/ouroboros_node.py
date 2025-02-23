import asyncio
import random
import secrets
import time
from collections import deque
from enum import Enum
from typing import Dict, Any, List, Optional
import json
import numpy as np
import networkx as nx

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
        self.consensus_state = {}
        self.peers = []
        self.trust_graph = nx.DiGraph()

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

    async def participate_in_consensus(self) -> Dict[str, Any]:
        """Participate in network consensus."""
        state = self.get_verifiable_state()
        peer_states = await self._gather_peer_states()
        
        # Byzantine fault tolerance check
        valid_states = self._validate_peer_states(peer_states)
        if len(valid_states) >= (2 * len(self.peers) // 3):
            consensus_state = self._compute_consensus(valid_states)
            self._update_local_state(consensus_state)
            return consensus_state
        return None

    def _validate_peer_states(self, peer_states: List[Dict]) -> List[Dict]:
        """Validate peer states using ZKP verification."""
        valid_states = []
        for state in peer_states:
            if self.zkp_verifier.verify_proof(
                state['state'],
                state['proof'],
                state['challenge']
            ):
                valid_states.append(state)
        return valid_states

    def _compute_consensus(self, valid_states: List[Dict]) -> Dict:
        """Compute consensus state using weighted trust scores."""
        consensus = {}
        weights = self._compute_trust_weights(valid_states)
        
        for key in ['ethical_weights', 'recursion_depth']:
            values = [s['state'][key] for s in valid_states]
            if isinstance(values[0], dict):
                consensus[key] = {
                    k: np.average([v[k] for v in values], weights=weights)
                    for k in values[0].keys()
                }
            else:
                consensus[key] = np.average(values, weights=weights)
        
        return consensus

    def _compute_trust_weights(self, states: List[Dict]) -> List[float]:
        """Compute trust weights based on historical interactions."""
        weights = []
        for state in states:
            node_id = state['state']['node_id']
            weight = self.trust_graph.nodes.get(node_id, {}).get('trust_score', 1.0)
            weights.append(weight)
        return weights if weights else [1.0] * len(states)

    def update_trust_score(self, node_id: int, interaction_success: bool):
        """Update trust scores based on interaction outcomes."""
        if not self.trust_graph.has_node(node_id):
            self.trust_graph.add_node(node_id, trust_score=1.0)
        
        current_score = self.trust_graph.nodes[node_id]['trust_score']
        delta = 0.1 if interaction_success else -0.2
        new_score = max(0.1, min(1.0, current_score + delta))
        self.trust_graph.nodes[node_id]['trust_score'] = new_score

    async def run(self) -> None:
        """Enhanced run loop with consensus participation."""
        message_task = asyncio.create_task(self.process_messages())
        consensus_task = asyncio.create_task(self._consensus_loop())
        
        try:
            while self.recursion_depth < RECURSION_LIMIT:
                if self.state == MindState.ACTIVE_RECURSION:
                    self.generate_insight()
                    await self._check_ethical_bounds()
                await asyncio.sleep(random.uniform(0.2, 0.5))
        finally:
            message_task.cancel()
            consensus_task.cancel()

    async def _consensus_loop(self):
        """Periodic consensus participation."""
        while True:
            await self.participate_in_consensus()
            await asyncio.sleep(CONSENSUS_INTERVAL)

    async def _check_ethical_bounds(self):
        """Check if ethical weights are within acceptable bounds."""
        total_deviation = sum(abs(w - 1/3) for w in self.ethical_weights.values())
        if total_deviation > 0.5:  # Threshold for ethical crisis
            self.state = MindState.ETHICAL_CRISIS
            logging.warning(f"Node {self.node_id} entered ethical crisis state")

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
