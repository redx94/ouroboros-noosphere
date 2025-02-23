from typing import Dict, Any
import os
from dotenv import load_dotenv
import json

load_dotenv()

class Config:
    def __init__(self):
        self.config = {
            'NODE_COUNT': int(os.getenv('NODE_COUNT', '3')),
            'RECURSION_LIMIT': int(os.getenv('RECURSION_LIMIT', '100')),
            'CONSENSUS_INTERVAL': int(os.getenv('CONSENSUS_INTERVAL', '5')),
            'METRICS_INTERVAL': int(os.getenv('METRICS_INTERVAL', '1')),
            'ENCRYPTION_PARAMS': {
                'p': int(os.getenv('ENCRYPTION_P', '65537')),
                'm': int(os.getenv('ENCRYPTION_M', '2048')),
                'sec': int(os.getenv('ENCRYPTION_SEC', '128'))
            },
            'API_CONFIG': {
                'host': os.getenv('API_HOST', 'localhost'),
                'port': int(os.getenv('API_PORT', '8000')),
                'debug': os.getenv('DEBUG', 'False').lower() == 'true'
            },
            'STREAMLIT_CONFIG': {
                'page_title': 'Ouroboros Noosphere',
                'layout': 'wide',
                'theme': {
                    'primaryColor': '#FF4B4B',
                    'backgroundColor': '#0E1117',
                    'secondaryBackgroundColor': '#262730',
                    'textColor': '#FAFAFA',
                    'font': 'sans serif'
                }
            }
        }

    def get(self, key: str) -> Any:
        """Get a configuration value."""
        return self.config.get(key)

    def update(self, key: str, value: Any) -> None:
        """Update a configuration value."""
        self.config[key] = value

    def load_from_file(self, filepath: str) -> None:
        """Load configuration from a JSON file."""
        try:
            with open(filepath, 'r') as f:
                new_config = json.load(f)
                self.config.update(new_config)
        except Exception as e:
            print(f"Error loading config: {e}")

    def save_to_file(self, filepath: str) -> None:
        """Save current configuration to a JSON file."""
        try:
            with open(filepath, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")

    @property
    def as_dict(self) -> Dict[str, Any]:
        """Get the entire configuration as a dictionary."""
        return self.config.copy()

config = Config()

# General node configuration
NODE_COUNT = 3
RECURSION_LIMIT = 100

# Homomorphic encryption parameters
ENCRYPTION_PARAMS = {
    "p": 65537,  # plaintext prime modulus
    "m": 2048,   # cyclotomic polynomial ring degree
    "sec": 128,  # security parameter
}

# RL configuration (stub parameters)
RL_PARAMS = {
    "learning_rate": 0.1,
    "discount_factor": 0.9,
    "epsilon": 0.1  # Exploration rate
}

# Consensus synchronization interval in seconds
CONSENSUS_INTERVAL = 5

# Observer influence interval in seconds
OBSERVER_INTERVAL = 3

# Adversary challenge interval bounds in seconds
ADVERSARY_INTERVAL = (1.0, 2.0)

# Monitoring configuration
MONITORING = {
    "enabled": True,
    "log_interval": 1.0,  # seconds
    "plot_interval": 60.0,  # seconds
    "plot_directory": "monitoring/plots"
}

# Trust system parameters
TRUST_PARAMS = {
    "initial_trust": 1.0,
    "minimum_trust": 0.1,
    "success_delta": 0.1,
    "failure_delta": -0.2
}

# Ethical bounds
ETHICAL_BOUNDS = {
    "max_deviation": 0.5,  # Maximum allowed deviation from equal weights
    "recovery_rate": 0.01  # Rate at which weights return to equilibrium
}
