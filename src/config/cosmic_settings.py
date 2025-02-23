from dataclasses import dataclass
from typing import List
from datetime import datetime

@dataclass
class QuantumSafeConfig:
    n: int = 1024
    q: int = 12289
    sigma: float = 3.2
    library: str = "lattice-based-crypto"

@dataclass
class CosmicConfig:
    quantum_safe: QuantumSafeConfig = QuantumSafeConfig()
    consensus_interval: int = 10
    byzantine_tolerance: float = 0.33
    multiverse_sync_epoch: datetime = datetime.fromisoformat("2025-03-01T00:00:00Z")
    quantum_entanglement_factor: float = 0.98
    temporal_resonance: float = 1.2
    dimensional_drift_compensation: float = 0.05
    cosmic_endpoints: List[str] = None

    def __post_init__(self):
        if self.cosmic_endpoints is None:
            self.cosmic_endpoints = [
                "https://cosmic-endpoint-1.example.com",
                "https://cosmic-endpoint-2.example.com"
            ]
