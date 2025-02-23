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
