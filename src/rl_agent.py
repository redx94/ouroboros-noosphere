import random
import logging
import numpy as np
from typing import Dict, Tuple, List

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class RLAgent:
    def __init__(self, learning_rate: float = 0.1, discount_factor: float = 0.95, epsilon: float = 0.1):
        self.q_table: Dict[str, Dict[str, float]] = {}
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.ethical_domains = ['utilitarian', 'deontological', 'virtue']
        
    def get_state_key(self, ethical_weights: Dict[str, float]) -> str:
        """Convert ethical weights to discrete state key"""
        return ':'.join(f"{k}={round(v, 2)}" for k, v in sorted(ethical_weights.items()))

    def get_actions(self) -> List[Tuple[str, float]]:
        """Generate possible actions as (domain, adjustment) pairs"""
        return [(domain, adj) for domain in self.ethical_domains 
                for adj in [-0.1, 0.1]]

    def choose_action(self, state_key: str) -> Tuple[str, float]:
        """Choose action using epsilon-greedy policy"""
        if state_key not in self.q_table:
            self.q_table[state_key] = {str(action): 0.0 for action in self.get_actions()}

        if random.random() < self.epsilon:
            return random.choice(self.get_actions())
        
        return eval(max(self.q_table[state_key].items(), key=lambda x: x[1])[0])

    def update(self, state: str, action: Tuple[str, float], reward: float, next_state: str):
        """Update Q-values using Q-learning"""
        if next_state not in self.q_table:
            self.q_table[next_state] = {str(action): 0.0 for action in self.get_actions()}
            
        max_next_q = max(self.q_table[next_state].values())
        current_q = self.q_table[state][str(action)]
        
        self.q_table[state][str(action)] = current_q + self.lr * (
            reward + self.gamma * max_next_q - current_q
        )
