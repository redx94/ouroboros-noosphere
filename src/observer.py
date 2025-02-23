import asyncio
import random
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

async def observer_module(nodes) -> None:
    """
    Simulate an observer module that periodically injects influence into the network of nodes.
    Args:
        nodes: A list of OuroborosNode instances.
    """
    while True:
        await asyncio.sleep(3)
        # Generate random influence factors for each ethical dimension.
        influence = {
            'utilitarian': random.uniform(-0.05, 0.05),
            'deontological': random.uniform(-0.05, 0.05),
            'virtue': random.uniform(-0.05, 0.05)
        }
        logging.info(f"Observer injecting influence: {influence}")
        for node in nodes:
            node.apply_observer_influence(influence)
