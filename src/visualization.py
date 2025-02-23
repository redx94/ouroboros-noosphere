import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, Any
import numpy as np

class NetworkVisualizer:
    def __init__(self):
        self.figure, self.ax = plt.subplots(figsize=(12, 8))
        
    def plot_ontology_graph(self, graph: nx.DiGraph) -> None:
        """Plot the current state of the ontology graph"""
        self.ax.clear()
        pos = nx.spring_layout(graph)
        
        # Draw nodes with colors based on state
        states = nx.get_node_attributes(graph, 'state')
        colors = [self._get_state_color(state) for state in states.values()]
        
        nx.draw_networkx_nodes(graph, pos, node_color=colors, alpha=0.6)
        nx.draw_networkx_edges(graph, pos, alpha=0.3)
        nx.draw_networkx_labels(graph, pos)
        
        plt.title("Ouroboros Network State")
        plt.pause(0.1)  # For interactive updates
        
    def plot_ethical_weights(self, nodes: List[Any]) -> None:
        """Plot ethical weights distribution across nodes"""
        self.ax.clear()
        weights = [node.ethical_weights for node in nodes]
        
        data = np.array([[w[k] for k in ['utilitarian', 'deontological', 'virtue']] 
                        for w in weights])
        
        self.ax.boxplot(data, labels=['Utilitarian', 'Deontological', 'Virtue'])
        plt.title("Ethical Weights Distribution")
        plt.ylabel("Weight Value")
        plt.pause(0.1)
        
    def plot_network_metrics(self, metrics_collector) -> None:
        """Plot historical network metrics"""
        self.ax.clear()
        
        # Extract metrics
        timestamps = [m.timestamp for m in metrics_collector.metrics_history]
        health_scores = [
            metrics_collector.get_network_health() 
            for _ in range(len(metrics_collector.metrics_history))
        ]
        
        # Plot network health over time
        self.ax.plot(timestamps, health_scores, label='Network Health', color='blue')
        
        # Add ethical balance distribution
        ethical_balances = [m.ethical_balance for m in metrics_collector.metrics_history]
        self.ax.plot(timestamps, ethical_balances, label='Ethical Balance', color='red', alpha=0.5)
        
        plt.title("Network Health and Ethical Balance Over Time")
        plt.xlabel("Time")
        plt.ylabel("Score")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.pause(0.1)

    def plot_recursive_depth_distribution(self, nodes) -> None:
        """Plot distribution of recursion depths across nodes"""
        self.ax.clear()
        depths = [node.recursion_depth for node in nodes]
        
        plt.hist(depths, bins='auto', alpha=0.7, color='green')
        plt.title("Distribution of Recursion Depths")
        plt.xlabel("Recursion Depth")
        plt.ylabel("Number of Nodes")
        plt.pause(0.1)
        
    @staticmethod
    def _get_state_color(state: str) -> str:
        """Map node states to colors"""
        colors = {
            'ACTIVE_RECURSION': 'green',
            'NEURAL_ANNEALING': 'blue',
            'ETHICAL_CRISIS': 'red',
            'OBSERVATIONAL_FREEZE': 'yellow'
        }
        return colors.get(state, 'gray')
