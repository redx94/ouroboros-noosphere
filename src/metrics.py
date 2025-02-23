import time
from dataclasses import dataclass, asdict
from typing import Dict, List, Any
import logging
import json
import asyncio
from collections import deque

@dataclass
class NodeMetrics:
    node_id: int
    recursion_depth: int
    ethical_balance: float
    insight_count: int
    timestamp: float

@dataclass
class NetworkMetrics:
    node_count: int
    consensus_rounds: int
    average_trust: float
    ethical_diversity: float
    message_count: int
    proof_validations: int

class MetricsCollector:
    def __init__(self, history_size: int = 1000):
        self.metrics_history = deque(maxlen=history_size)
        self.start_time = time.time()
        self.event_log = deque(maxlen=history_size)
        self.node_performance: Dict[int, List[float]] = []

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

    async def collect_metrics(self, network_state: Dict[str, Any]) -> NetworkMetrics:
        """Collect current network metrics"""
        metrics = NetworkMetrics(
            node_count=len(network_state['nodes']),
            consensus_rounds=network_state['consensus_count'],
            average_trust=sum(n['trust_score'] for n in network_state['nodes']) / len(network_state['nodes']),
            ethical_diversity=self._calculate_diversity(network_state['nodes']),
            message_count=network_state['message_count'],
            proof_validations=network_state['validations']
        )
        self.metrics_history.append(asdict(metrics))
        return metrics

    def _calculate_diversity(self, nodes: List[Dict]) -> float:
        """Calculate ethical diversity score across nodes"""
        weights = [n['ethical_weights'] for n in nodes]
        variance = sum(sum((w1[k] - w2[k])**2 for k in w1) 
                      for i, w1 in enumerate(weights) 
                      for w2 in weights[i+1:])
        return variance / (len(nodes) * (len(nodes) - 1)) if len(nodes) > 1 else 0

    def track_event(self, event_type: str, data: Dict[str, Any]):
        """Track significant network events"""
        self.event_log.append({
            'timestamp': time.time(),
            'type': event_type,
            'data': data
        })

    def get_report(self) -> Dict[str, Any]:
        """Generate metrics report"""
        return {
            'uptime': time.time() - self.start_time,
            'current_metrics': self.metrics_history[-1] if self.metrics_history else None,
            'history_summary': self._summarize_history(),
            'recent_events': list(self.event_log)
        }

    def _summarize_history(self) -> Dict[str, Any]:
        """Summarize metrics history"""
        if not self.metrics_history:
            return {}
            
        metrics_list = list(self.metrics_history)
        return {
            'average_trust': sum(m['average_trust'] for m in metrics_list) / len(metrics_list),
            'max_nodes': max(m['node_count'] for m in metrics_list),
            'total_validations': sum(m['proof_validations'] for m in metrics_list)
        }

    def get_network_health(self) -> float:
        """Calculate overall network health score"""
        if not self.metrics_history:
            return 1.0
        
        recent_metrics = self.metrics_history[-len(self.node_performance):]
        avg_ethical_balance = sum(m.ethical_balance for m in recent_metrics) / len(recent_metrics)
        return max(0.0, 1.0 - avg_ethical_balance)
