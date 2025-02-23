import asyncio
import random
import logging
from config import ADVERSARY_INTERVAL

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

async def adversarial_agent(node, rl_agent) -> None:
    """
    Periodically challenges the node by perturbing its ethical weights.
    Uses an RL agent to decide the magnitude of the challenge.
    """
    while True:
        await asyncio.sleep(random.uniform(*ADVERSARY_INTERVAL))
        if node.recursion_depth % 2 == 0 and node.recursion_depth > 0:
            logging.info(f"Adversary challenging Node {node.node_id} at depth {node.recursion_depth}")
            perturbation = rl_agent.get_adversary_perturbation(node.ethical_weights)
            node.ethical_weights = {k: max(0.1, random.uniform(0.2, 0.5) * perturbation.get(k, 1.0))
                                  for k in node.ethical_weights}
            total = sum(node.ethical_weights.values())
            node.ethical_weights = {k: v / total for k, v in node.ethical_weights.items()}
            logging.info(f"Node {node.node_id} ethical weights after adversary challenge: {node.ethical_weights}")
