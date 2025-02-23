import time
from dataclasses import dataclass
from typing import Dict, List
import logging

@dataclass
class NodeMetrics:
    node_id: int
    recursion_depth: int
    ethical_balance: float
    insight_count: int
    timestamp: float

class MetricsCollector:
    def __init__(self):
        self.metrics_history: List[NodeMetrics] = []
        self.node_performance: Dict[int, List[float]] = {}

    def record_node_metrics(self, node) -> None:
        """Record metrics for a single node"""
        ethical_balance = sum(abs(v - 0.33) for v in node.ethical_weights.values())
        metrics = NodeMetrics(
            node_id=node.node_id,
            recursion_depth=node.recursion_depth,
            ethical_balance=ethical_balance,
            insight_count=len(node.conceptual_memory),
            timestamp=time.time()
        )
        self.metrics_history.append(metrics)
        logging.info(f"Recorded metrics for Node {node.node_id}: {metrics}")

    def get_network_health(self) -> float:
        """Calculate overall network health score"""
        if not self.metrics_history:
            return 1.0
        
        recent_metrics = self.metrics_history[-len(self.node_performance):]
        avg_ethical_balance = sum(m.ethical_balance for m in recent_metrics) / len(recent_metrics)
        return max(0.0, 1.0 - avg_ethical_balance)
