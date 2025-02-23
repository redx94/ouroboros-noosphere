from prometheus_client import Counter, Gauge, Histogram
import time
from typing import Dict, Any
import numpy as np

class MetricsCollector:
    def __init__(self):
        # Prometheus metrics
        self.node_count = Gauge('ouroboros_node_count', 'Number of active nodes')
        self.insight_counter = Counter('ouroboros_insights_total', 'Total insights generated')
        self.recursion_depth = Histogram('ouroboros_recursion_depth', 'Recursion depth distribution')
        self.ethical_balance = Gauge('ouroboros_ethical_balance', 'Ethical framework balance')
        
        # Internal metrics storage
        self._metrics_history = []
        self._start_time = time.time()

    def track_node_creation(self, node_id: int):
        self.node_count.inc()
        self._record_event('node_creation', {'node_id': node_id})

    def track_insight_generation(self, node_id: int, insight: str):
        self.insight_counter.inc()
        self._record_event('insight', {
            'node_id': node_id,
            'insight': insight,
            'timestamp': time.time()
        })

    def track_recursion_depth(self, depth: int):
        self.recursion_depth.observe(depth)
        self._record_event('recursion_depth', {'depth': depth})

    def track_influence_application(self, node_id: int, influence: Dict[str, float]):
        self._record_event('influence', {
            'node_id': node_id,
            'influence': influence,
            'timestamp': time.time()
        })

    def _record_event(self, event_type: str, data: Dict[str, Any]):
        self._metrics_history.append({
            'type': event_type,
            'data': data,
            'timestamp': time.time()
        })

    def get_current_metrics(self) -> Dict[str, Any]:
        """Get the current state of all metrics."""
        return {
            'node_count': self.node_count._value.get(),
            'total_insights': self.insight_counter._value.get(),
            'avg_recursion_depth': np.mean([
                e['data']['depth'] for e in self._metrics_history 
                if e['type'] == 'recursion_depth'
            ]) if any(e['type'] == 'recursion_depth' for e in self._metrics_history) else 0,
            'uptime': time.time() - self._start_time
        }

    def get_all_metrics(self) -> Dict[str, Any]:
        """Get all historical metrics and analytics."""
        events_by_type = {}
        for event in self._metrics_history:
            if event['type'] not in events_by_type:
                events_by_type[event['type']] = []
            events_by_type[event['type']].append(event['data'])

        return {
            'current': self.get_current_metrics(),
            'history': events_by_type,
            'analytics': self._compute_analytics(events_by_type)
        }

    def _compute_analytics(self, events_by_type: Dict[str, list]) -> Dict[str, Any]:
        """Compute advanced analytics from metrics history."""
        return {
            'insight_rate': len(events_by_type.get('insight', [])) / 
                          (time.time() - self._start_time),
            'node_creation_rate': len(events_by_type.get('node_creation', [])) / 
                                (time.time() - self._start_time),
            'influence_frequency': len(events_by_type.get('influence', [])) / 
                                (time.time() - self._start_time)
        }
