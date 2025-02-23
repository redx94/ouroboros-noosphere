import asyncio
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

async def consensus_synchronization(nodes):
    while True:
        await asyncio.sleep(5)
        logging.info("--- Consensus Event Initiated ---")
        snapshots = {node.node_id: node.encrypt_state() for node in nodes}
        logging.info(f"Consensus snapshots: {snapshots}")
        logging.info("--- Consensus Event Concluded ---")
