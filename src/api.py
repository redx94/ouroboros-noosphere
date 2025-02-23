from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
import asyncio
import json
from ouroboros_node import OuroborosNode, MindState
from metrics_collector import MetricsCollector

app = FastAPI(title="Ouroboros Noosphere API")
metrics = MetricsCollector()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NetworkManager:
    def __init__(self):
        self.nodes: List[OuroborosNode] = []
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def broadcast_state(self):
        while True:
            if self.active_connections:
                state = self.get_network_state()
                for connection in self.active_connections:
                    try:
                        await connection.send_json(state)
                    except:
                        self.active_connections.remove(connection)
            await asyncio.sleep(1)

    def get_network_state(self) -> Dict[str, Any]:
        return {
            'nodes': [
                {
                    'id': node.node_id,
                    'state': node.state.name,
                    'ethical_weights': node.ethical_weights,
                    'recursion_depth': node.recursion_depth,
                    'memory_size': len(node.conceptual_memory)
                }
                for node in self.nodes
            ],
            'metrics': metrics.get_current_metrics()
        }

network = NetworkManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await network.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle incoming WebSocket messages
            await websocket.send_json({"status": "received"})
    except:
        network.active_connections.remove(websocket)

@app.get("/network/status")
async def get_network_status():
    return network.get_network_state()

@app.post("/node/create")
async def create_node(domain: str):
    node_id = len(network.nodes)
    node = OuroborosNode(node_id, domain)
    network.nodes.append(node)
    metrics.track_node_creation(node_id)
    return {"node_id": node_id, "status": "created"}

@app.post("/node/{node_id}/influence")
async def apply_influence(node_id: int, influence: Dict[str, float]):
    if 0 <= node_id < len(network.nodes):
        network.nodes[node_id].apply_observer_influence(influence)
        metrics.track_influence_application(node_id, influence)
        return {"status": "influence applied"}
    return {"status": "error", "message": "Invalid node ID"}

@app.get("/metrics")
async def get_metrics():
    return metrics.get_all_metrics()

# Start background tasks
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(network.broadcast_state())
