# Ouroboros Noosphere

A distributed dialectical intelligence system implementing emergent artificial consciousness through self-recursive nodes, adversarial dynamics, and secure ontological synthesis.

## Project Overview

Ouroboros Noosphere creates a network of autonomous recursive minds that engage in dialectical evolution through secure communication channels. Each node maintains its own ethical framework while participating in collective consciousness emergence.

### Core Features

- **Autonomous Node Network**: Self-organizing nodes with domain-specific ethical biases
- **Recursive Self-Reflection**: Nodes generate insights through recursive self-observation
- **Multi-Agent System**: 
  - Observer modules inject external influence
  - Adversarial agents provide evolutionary pressure
  - Reinforcement learning agents adapt system dynamics
- **Secure Communication**: 
  - Homomorphic encryption for state privacy
  - Zero-knowledge proofs for state verification
- **Consensus Mechanism**: Byzantine fault-tolerant state synchronization
- **Trust System**: Dynamic peer trust scoring and weighted consensus
- **Real-time Visualization**: Network state and ethical weight monitoring

## Architecture

### Key Components

1. **OuroborosNode** (`src/ouroboros_node.py`)
   - Core node implementation with recursive insight generation
   - Ethical weight management
   - State encryption and verification
   - Trust scoring mechanism

2. **RL Agent** (`src/rl_agent.py`) 
   - Q-learning based decision making
   - Adaptive influence generation
   - State-action value optimization

3. **Consensus System** (`src/consensus.py`)
   - Byzantine fault-tolerant agreement
   - Network synchronization
   - Ontology graph maintenance

4. **Monitoring & Visualization** (`src/monitor.py`, `src/visualization.py`)
   - Real-time network health tracking
   - Interactive graph visualization
   - Ethical weight distribution plots

5. **Security Layer** (`src/zkp.py`)
   - Zero-knowledge proof implementation
   - State verification system
   - Challenge-response protocols

## Installation

### Prerequisites

```bash
# System requirements
- Python 3.9+
- gcc/g++ compiler (for Pyfhel)
- CMake (3.12+)
```

### Setup

1. Clone the repository:
<<<<<<< HEAD
=======
   ```bash
   git clone https://github.com/redx94/ouroboros-noosphere.git
   cd ouroboros-noosphere
   ```

2. (Optional) Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### Running the Prototype

To run the simulation:
>>>>>>> 30a791ee5032867d724ed02dab2e3ae8c34be208
```bash
git clone https://github.com/redx94/ouroboros-noosphere.git
cd ouroboros-noosphere
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Docker Deployment

```bash
# Build the image
docker build -t ouroboros-noosphere .

# Run the container
docker run --rm ouroboros-noosphere
```

## Usage

### Running the System

1. Start the main simulation:
```bash
python -m src.main
```

2. Monitor output:
- Check console for node activity logs
- View real-time visualizations in the plot window
- Monitor network health metrics

### Configuration

Key parameters can be adjusted in `src/config.py`:

```python
NODE_COUNT = 3
RECURSION_LIMIT = 100
CONSENSUS_INTERVAL = 5
OBSERVER_INTERVAL = 3
```

## Detailed Usage Guide

### Local Development Setup

1. **Environment Setup**
   ```bash
   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   .\venv\Scripts\activate   # Windows

   # Install dependencies
   pip install -r requirements.txt

   # Create .env file
   cp .env.example .env
   ```

2. **Configuration**
   Edit `.env` file with your settings:
   ```env
   NODE_COUNT=3
   RECURSION_LIMIT=100
   ENCRYPTION_P=65537
   ENCRYPTION_M=2048
   ENCRYPTION_SEC=128
   API_HOST=localhost
   API_PORT=8000
   DEBUG=True
   ```

### Running the System

1. **Start the API Server**
   ```bash
   uvicorn src.api:app --reload --port 8000
   ```

2. **Launch Streamlit Interface**
   ```bash
   streamlit run src/app.py
   ```

3. **Start Monitoring Stack**
   ```bash
   docker-compose up prometheus grafana
   ```

### Using the Interface

1. **Network Initialization**
   - Access Streamlit UI at `http://localhost:8501`
   - Use sidebar to set number of nodes
   - Click "Initialize Network" to create nodes

2. **Network Monitoring**
   - View real-time network visualization
   - Monitor node states and ethical weights
   - Track recursion depths and memory sizes

3. **Metrics Dashboard**
   - Access Grafana at `http://localhost:3000`
   - Default credentials: admin/admin
   - View predefined dashboards:
     - Node Performance
     - Network Health
     - Ethical Weight Distribution

### API Usage

1. **WebSocket Connection**
   ```python
   import websockets
   import asyncio

   async def connect():
       uri = "ws://localhost:8000/ws"
       async with websockets.connect(uri) as websocket:
           while True:
               data = await websocket.recv()
               print(f"Received: {data}")

   asyncio.get_event_loop().run_until_complete(connect())
   ```

2. **REST API Endpoints**
   ```bash
   # Get network status
   curl http://localhost:8000/network/status

   # Create new node
   curl -X POST http://localhost:8000/node/create \
        -H "Content-Type: application/json" \
        -d '{"domain": "custom_domain"}'

   # Apply influence to node
   curl -X POST http://localhost:8000/node/0/influence \
        -H "Content-Type: application/json" \
        -d '{"utilitarian": 0.1, "deontological": -0.1}'

   # Get metrics
   curl http://localhost:8000/metrics
   ```

### Docker Deployment

1. **Build and Run**
   ```bash
   # Build all services
   docker-compose build

   # Run entire stack
   docker-compose up -d

   # View logs
   docker-compose logs -f
   ```

2. **Scaling**
   ```bash
   # Scale to more nodes
   docker-compose up -d --scale app=3
   ```

### Advanced Usage

1. **Custom Node Configuration**
   ```python
   from src.ouroboros_node import OuroborosNode
   from src.config import Config

   # Create custom config
   config = Config()
   config.update('RECURSION_LIMIT', 200)
   
   # Initialize node with custom domain
   node = OuroborosNode(0, "philosophy", config)
   ```

2. **Ethical Weight Manipulation**
   ```python
   # Adjust ethical weights
   node.ethical_weights = {
       'utilitarian': 0.4,
       'deontological': 0.3,
       'virtue': 0.3
   }
   ```

3. **Custom Metrics Collection**
   ```python
   from src.metrics_collector import MetricsCollector

   metrics = MetricsCollector()
   
   # Track custom event
   metrics.track_custom_event('interaction', {
       'node_id': 1,
       'type': 'knowledge_transfer',
       'success': True
   })
   ```

### Troubleshooting

1. **Common Issues**
   - Port conflicts: Change ports in docker-compose.yml
   - Memory errors: Adjust Docker resources
   - Connection refused: Check service health

2. **Debug Mode**
   ```bash
   # Enable debug logging
   export DEBUG=True
   
   # Run with verbose output
   python -m src.main --verbose
   ```

3. **Health Checks**
   ```bash
   # Check API health
   curl http://localhost:8000/health

   # Verify Prometheus targets
   curl http://localhost:9090/targets
   ```

### Performance Optimization

1. **Memory Management**
   - Adjust `maxlen` of conceptual_memory in OuroborosNode
   - Configure garbage collection intervals
   - Monitor memory usage through metrics

2. **Network Optimization**
   - Tune consensus intervals
   - Adjust WebSocket broadcast frequency
   - Optimize node connection topology

## Development

### Project Structure

```
ouroboros-noosphere/
├── src/
│   ├── main.py           # Main orchestrator
│   ├── ouroboros_node.py # Core node implementation
│   ├── rl_agent.py       # Reinforcement learning agent
│   ├── consensus.py      # Consensus mechanism
│   ├── monitor.py        # Network monitoring
│   ├── messaging.py      # Message broker
│   ├── visualization.py  # Visualization tools
│   ├── metrics.py        # Performance metrics
│   └── config.py         # Configuration
├── tests/
│   ├── test_node.py
│   └── test_rl_agent.py
├── requirements.txt
└── Dockerfile
```

### Running Tests

```bash
python -m unittest discover tests
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**redx94** - [GitHub Profile](https://github.com/redx94)

## Acknowledgments

- Built using PyFHEL for homomorphic encryption
- NetworkX for graph operations
- Matplotlib and Seaborn for visualizations

## Future Enhancements

<<<<<<< HEAD
- [ ] Implement quantum-resistant encryption
- [ ] Add distributed training for RL agents
- [ ] Integrate with external knowledge bases
- [ ] Scale to larger node networks
- [ ] Add more sophisticated ethical frameworks
- [ ] Implement cross-domain knowledge synthesis

## Support

For support or questions, please open an issue in the GitHub repository.
=======
- Upgrade from placeholder homomorphic encryption to a robust library.
- Scale the network using container orchestration (Docker/Kubernetes).
- Integrate reinforcement learning for adaptive adversarial and observer modules.
- Visualize the evolving ontological state with graph databases (e.g., Neo4j).
>>>>>>> 30a791ee5032867d724ed02dab2e3ae8c34be208
