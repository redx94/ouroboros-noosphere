import asyncio
import logging
import networkx as nx
from config import CONSENSUS_INTERVAL
from zkp import ZKPVerifier
from messaging import MessageBroker
from visualization import NetworkVisualizer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class ConsensusManager:
    def __init__(self, message_broker: MessageBroker):
        self.message_broker = message_broker
        self.verifier = ZKPVerifier()
        self.ontology_graph = nx.DiGraph()
        self.visualizer = NetworkVisualizer()
        
    async def synchronize_nodes(self, nodes) -> None:
        while True:
            await asyncio.sleep(CONSENSUS_INTERVAL)
            logging.info("--- Consensus Event Initiated ---")
            
            # Collect and verify node states
            for node in nodes:
                state = node.get_verifiable_state()
                challenge, nonce = self.verifier.generate_challenge(state)
                proof = self.verifier.create_proof(state, nonce)
                
                if self.verifier.verify_proof(proof, challenge):
                    await self.message_broker.publish('consensus', {
                        'node_id': node.node_id,
                        'state_proof': proof.hex(),
                        'timestamp': asyncio.get_event_loop().time()
                    })
                    
                    # Update graph with verified state
                    self._update_graph(node)
                else:
                    logging.warning(f"State verification failed for Node {node.node_id}")
            
            # Update visualizations
            self.visualizer.plot_ontology_graph(self.ontology_graph)
            self.visualizer.plot_ethical_weights(nodes)
            
            logging.info("--- Consensus Event Concluded ---")
    
    def _update_graph(self, node) -> None:
        """Update the ontology graph with node state."""
        self.ontology_graph.add_node(
            node.node_id,
            state=node.state.name,
            depth=node.recursion_depth,
            timestamp=asyncio.get_event_loop().time()
        )

async def consensus_synchronization(nodes) -> None:
    message_broker = MessageBroker()
    consensus_manager = ConsensusManager(message_broker)
    await consensus_manager.synchronize_nodes(nodes)
