import asyncio
import random
import logging
from config import NODE_COUNT
from ouroboros_node import OuroborosNode
from rl_agent import RLAgent
from metrics import MetricsCollector
from monitor import NetworkMonitor

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

async def main():
    """
    Main orchestrator for the distributed Ouroboros network simulation.
    Creates nodes with diverse domain seeds, schedules adversarial, observer,
    and consensus tasks, and runs everything concurrently.
    """
    domains = ['deontological', 'utilitarian', 'virtue']
    nodes = [
        OuroborosNode(node_id=i, domain_seed=random.choice(domains))
        for i in range(NODE_COUNT)
    ]

    rl_agent = RLAgent()

    # Initialize metrics and monitoring
    metrics_collector = MetricsCollector()
    network_monitor = NetworkMonitor(nodes, metrics_collector)

    node_tasks = [asyncio.create_task(node.run()) for node in nodes]
    adversary_tasks = [asyncio.create_task(adversarial_agent(node, rl_agent)) for node in nodes]
    consensus_task = asyncio.create_task(consensus_synchronization(nodes))
    observer_task = asyncio.create_task(observer_module(nodes, rl_agent))
    
    # Add monitoring task
    monitor_task = asyncio.create_task(network_monitor.monitor_network())

    tasks = node_tasks + adversary_tasks + [consensus_task, observer_task, monitor_task]
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
