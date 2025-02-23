import asyncio
import random
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

async def adversarial_agent(node) -> None:
    """
    Simulate an adversarial agent that periodically challenges the node by perturbing its ethical weights.
    Args:
        node: An instance of OuroborosNode.
    """
    while True:
        await asyncio.sleep(random.uniform(1.0, 2.0))
        if node.recursion_depth % 2 == 0 and node.recursion_depth > 0:
            logging.info(f"Adversary challenging Node {node.node_id} at depth {node.recursion_depth}")
            # Simulate ethical conflict resolution by randomly adjusting ethical weights.
            node.ethical_weights = {k: random.uniform(0.2, 0.5) for k in node.ethical_weights}
            total = sum(node.ethical_weights.values())
            node.ethical_weights = {k: v / total for k, v in node.ethical_weights.items()}
            logging.info(f"Node {node.node_id} ethical weights after adversary challenge: {node.ethical_weights}")
