import streamlit as st
import networkx as nx
import plotly.graph_objects as go
from ouroboros_node import OuroborosNode
import asyncio
from typing import List
import pandas as pd

class StreamlitApp:
    def __init__(self):
        st.set_page_config(page_title="Ouroboros Noosphere", layout="wide")
        self.nodes: List[OuroborosNode] = []

    def render(self):
        st.title("Ouroboros Noosphere")
        
        with st.sidebar:
            num_nodes = st.slider("Number of Nodes", 2, 10, 3)
            if st.button("Initialize Network"):
                self.initialize_network(num_nodes)

        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Network Visualization")
            self.render_network()
            
        with col2:
            st.subheader("Node States")
            self.render_node_states()

        st.subheader("Ethical Weights Distribution")
        self.render_ethical_weights()

    def initialize_network(self, num_nodes: int):
        self.nodes = [
            OuroborosNode(i, f"domain_{i}") 
            for i in range(num_nodes)
        ]
        # Connect nodes in a ring topology
        for i in range(num_nodes):
            self.nodes[i].peers = [
                self.nodes[(i-1) % num_nodes],
                self.nodes[(i+1) % num_nodes]
            ]

    def render_network(self):
        if not self.nodes:
            return

        G = nx.DiGraph()
        for node in self.nodes:
            G.add_node(node.node_id)
            for peer in node.peers:
                G.add_edge(node.node_id, peer.node_id)

        pos = nx.spring_layout(G)
        
        edge_trace = go.Scatter(
            x=[], y=[], line=dict(width=0.5, color='#888'),
            hoverinfo='none', mode='lines')

        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace['x'] += (x0, x1, None)
            edge_trace['y'] += (y0, y1, None)

        node_trace = go.Scatter(
            x=[], y=[], text=[], mode='markers+text',
            hoverinfo='text', marker=dict(size=20))

        for node in G.nodes():
            x, y = pos[node]
            node_trace['x'] += (x,)
            node_trace['y'] += (y,)
            node_trace['text'] += (f'Node {node}',)

        fig = go.Figure(data=[edge_trace, node_trace],
                     layout=go.Layout(
                         showlegend=False,
                         hovermode='closest',
                         margin=dict(b=0,l=0,r=0,t=0),
                         xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                         yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                     ))
        
        st.plotly_chart(fig)

    def render_node_states(self):
        if not self.nodes:
            return
            
        data = []
        for node in self.nodes:
            data.append({
                'Node ID': node.node_id,
                'State': node.state.name,
                'Recursion Depth': node.recursion_depth,
                'Memory Size': len(node.conceptual_memory)
            })
        
        df = pd.DataFrame(data)
        st.dataframe(df)

    def render_ethical_weights(self):
        if not self.nodes:
            return
            
        data = []
        for node in self.nodes:
            for framework, weight in node.ethical_weights.items():
                data.append({
                    'Node ID': node.node_id,
                    'Framework': framework,
                    'Weight': weight
                })
        
        df = pd.DataFrame(data)
        fig = go.Figure(data=[
            go.Bar(
                name=f'Node {node_id}',
                x=df[df['Node ID'] == node_id]['Framework'],
                y=df[df['Node ID'] == node_id]['Weight']
            ) for node_id in df['Node ID'].unique()
        ])
        
        fig.update_layout(barmode='group')
        st.plotly_chart(fig)

if __name__ == "__main__":
    app = StreamlitApp()
    app.render()
