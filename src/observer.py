import asyncio
import logging
from config import OBSERVER_INTERVAL

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

async def observer_module(nodes, rl_agent) -> None:
    """
    Injects influence into the network of nodes.
    Uses an RL agent to adapt the influence based on network performance.
    """
    while True:
        await asyncio.sleep(OBSERVER_INTERVAL)
        influence = rl_agent.get_observer_influence()
        logging.info(f"Observer injecting influence: {influence}")
        for node in nodes:
            node.apply_observer_influence(influence)
