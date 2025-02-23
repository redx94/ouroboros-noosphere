import random
import logging
import numpy as np
from collections import defaultdict
from typing import Dict, Tuple, List
from config import RL_PARAMS

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class RLAgent:
    def __init__(self):
        self.learning_rate = RL_PARAMS["learning_rate"]
        self.discount_factor = RL_PARAMS["discount_factor"]
        self.epsilon = RL_PARAMS["epsilon"]
        self.q_table = defaultdict(lambda: defaultdict(float))
        self.state_history: List[Tuple] = []
        self.reward_history: List[float] = []
        
    def _get_state_key(self, weights: Dict[str, float]) -> Tuple:
        """Convert continuous state to discrete for Q-learning"""
        return tuple(round(v, 2) for v in sorted(weights.values()))
        
    def _get_action(self, state: Tuple) -> Dict[str, float]:
        """Select action using epsilon-greedy policy"""
        if random.random() < self.epsilon:
            return {k: random.uniform(-0.05, 0.05) for k in ['utilitarian', 'deontological', 'virtue']}
            
        if state not in self.q_table or not self.q_table[state]:
            return self.get_observer_influence()
            
        best_action = max(self.q_table[state].items(), key=lambda x: x[1])[0]
        return {k: float(v) for k, v in zip(['utilitarian', 'deontological', 'virtue'], 
                                          eval(best_action))}
    
    def update_q_value(self, state: Tuple, action: Dict[str, float], 
                      next_state: Tuple, reward: float) -> None:
        """Update Q-value using Q-learning update rule"""
        action_key = str(tuple(action.values()))
        old_q = self.q_table[state][action_key]
        next_max_q = max(self.q_table[next_state].values()) if self.q_table[next_state] else 0
        
        new_q = old_q + self.learning_rate * (
            reward + self.discount_factor * next_max_q - old_q
        )
        self.q_table[state][action_key] = new_q
        
    def get_observer_influence(self):
        """Get influence values using learned Q-values"""
        current_state = self._get_state_key(self.get_current_network_state())
        action = self._get_action(current_state)
        self.state_history.append(current_state)
        return action

    def get_adversary_perturbation(self, current_weights):
        """Get adversarial actions using learned Q-values"""
        state = self._get_state_key(current_weights)
        action = self._get_action(state)
        perturbation = {k: 1 + v for k, v in action.items()}
        return perturbation

    def get_current_network_state(self) -> Dict[str, float]:
        """Placeholder - should be implemented based on actual network metrics"""
        return {'utilitarian': 0.33, 'deontological': 0.33, 'virtue': 0.33}
