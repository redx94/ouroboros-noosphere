import asyncio
import random
import logging

from ouroboros_node import OuroborosNode
from adversary import adversarial_agent
from observer import observer_module
from consensus import consensus_synchronization

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

async def main():
    """
    Main orchestrator for the distributed Ouroboros network simulation.
    Creates nodes with diverse domain seeds, schedules adversarial, observer,
    and consensus tasks, and runs everything concurrently.
    """
    # Create a network of Ouroboros nodes with diverse domain seeds
    nodes = [
        OuroborosNode(node_id=i, domain_seed=random.choice(['deontological', 'utilitarian', 'virtue']))
        for i in range(3)
    ]

    # Schedule node tasks
    node_tasks = [asyncio.create_task(node.run()) for node in nodes]
    # Schedule adversarial agents for each node
    adversary_tasks = [asyncio.create_task(adversarial_agent(node)) for node in nodes]
    # Schedule consensus synchronization and observer modules
    consensus_task = asyncio.create_task(consensus_synchronization(nodes))
    observer_task = asyncio.create_task(observer_module(nodes))

    # Run all tasks concurrently
    tasks = node_tasks + adversary_tasks + [consensus_task, observer_task]
    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        logging.info("Tasks cancelled. Shutting down simulation.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        for task in tasks:
            task.cancel()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Simulation terminated by user.")
