import asyncio
import logging
from typing import List
from metrics import MetricsCollector

class NetworkMonitor:
    def __init__(self, nodes: List, metrics_collector: MetricsCollector):
        self.nodes = nodes
        self.metrics = metrics_collector
        self.alert_threshold = 0.3  # Network health threshold for alerts

    async def monitor_network(self):
        """Continuous network monitoring coroutine"""
        while True:
            # Collect metrics for all nodes
            for node in self.nodes:
                self.metrics.record_node_metrics(node)

            # Check network health
            health = self.metrics.get_network_health()
            if health < self.alert_threshold:
                logging.warning(f"Network health critical: {health:.2f}")
                self._trigger_recovery_actions()

            await asyncio.sleep(5)  # Monitor interval

    def _trigger_recovery_actions(self):
        """Implement recovery actions when network health is poor"""
        for node in self.nodes:
            if node.state != MindState.NEURAL_ANNEALING:
                node.state = MindState.NEURAL_ANNEALING
                logging.info(f"Node {node.node_id} entering neural annealing state")
