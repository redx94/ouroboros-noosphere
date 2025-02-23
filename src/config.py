
# General node configuration
NODE_COUNT = 3
RECURSION_LIMIT = 100

# Encryption configuration (for Pyfhel integration)
ENCRYPTION_PARAMS = {
    "p": 65537,       # Plaintext modulus
    "m": 8192,        # Cyclotomic polynomial degree
    "sec": 128        # Security parameter
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
