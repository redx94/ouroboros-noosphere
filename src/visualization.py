import plotly.graph_objects as go
import plotly.express as px
import networkx as nx
import pandas as pd
from typing import Dict, List, Any
import asyncio
import logging

class NetworkVisualizer:
    def __init__(self):
        self.fig_network = go.Figure()
        self.fig_ethics = go.Figure()
        self.update_interval = 1.0  # seconds
        
    def update_network_graph(self, G: nx.Graph):
        """Update network graph visualization"""
        pos = nx.spring_layout(G)
        
        # Extract node positions
        node_x = [pos[node][0] for node in G.nodes()]
        node_y = [pos[node][1] for node in G.nodes()]
        
        # Extract edge positions
        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            
        # Create edges trace
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')
            
        # Create nodes trace
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            marker=dict(
                size=10,
                color=[G.nodes[node].get('trust_score', 0.5) for node in G.nodes()],
                colorscale='Viridis',
                showscale=True
            ),
            text=[f"Node {node}" for node in G.nodes()],
            textposition="top center"
        )
        
        self.fig_network = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='Network Trust Graph',
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
            ))
            
    def update_ethics_distribution(self, nodes_data: List[Dict[str, Any]]):
        """Update ethics distribution visualization"""
        df = pd.DataFrame([
            {
                'node': f"Node {node['id']}",
                'domain': domain,
                'weight': weight
            }
            for node in nodes_data
            for domain, weight in node['ethical_weights'].items()
        ])
        
        self.fig_ethics = px.bar(df, 
            x='node', 
            y='weight', 
            color='domain',
            title='Ethical Weight Distribution',
            barmode='stack'
        )
        
    async def start_visualization_loop(self, get_network_state):
        """Start continuous visualization updates"""
        while True:
            try:
                network_state = await get_network_state()
                self.update_network_graph(network_state['trust_graph'])
                self.update_ethics_distribution(network_state['nodes'])
            except Exception as e:
                logging.error(f"Visualization update error: {e}")
            await asyncio.sleep(self.update_interval)
            
    def get_figures(self):
        """Get current figure objects"""
        return {
            'network': self.fig_network,
            'ethics': self.fig_ethics
        }
