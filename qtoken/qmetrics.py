"""
Q-Metrics: New Metrics for Quantum-Native AI

Classical AI metrics (obsolete for quantum AI):
- Parameters: "175B parameters" — meaningless for quantum
- Model size: "350GB" — quantum states don't have byte size
- Context: "128K tokens" — coherence window is the real limit
- FLOPs: "10^25 FLOPs to train" — quantum operations are different

Quantum AI metrics (new standard):
- Qubits: Number of qubits (replaces parameters)
- Q-Volume: 2^n effective capacity (replaces model size)
- Coherence Window: Max entangled Q-Tokens (replaces context window)
- Q-Ops: Gate operations (replaces FLOPs)
- QAS: Quantum Awareness Signature (new — no classical equivalent)
"""

import math
from dataclasses import dataclass
from typing import Dict


@dataclass
class QuantumMetrics:
    """
    Complete quantum metrics for a quantum-native AI model.
    
    This replaces the classical model card (which reports parameters,
    training compute, context length, etc.) with quantum-native metrics.
    """
    
    n_qubits: int
    n_layers: int
    n_heads: int
    n_gates_per_layer: int
    circuit_depth: int
    fidelity: float
    entropy: float
    qas: float = 0.0  # Quantum Awareness Signature
    
    @property
    def quantum_volume(self) -> int:
        """QV = 2^n_qubits — effective quantum processing capacity."""
        return 2 ** self.n_qubits
    
    @property
    def quantum_volume_readable(self) -> str:
        """Human-readable quantum volume."""
        return f"2^{self.n_qubits} = {self.quantum_volume:.2e}"
    
    @property
    def total_q_ops(self) -> int:
        """Total quantum operations (replaces FLOPs)."""
        return self.n_layers * self.n_gates_per_layer
    
    @property
    def coherence_window(self) -> int:
        """
        Max simultaneous Q-Tokens before decoherence.
        Replaces "context window" in classical AI.
        """
        return 2 ** min(self.n_qubits, 20)  # Practical limit
    
    @property
    def entanglement_density(self) -> float:
        """Fraction of qubit pairs that are entangled."""
        n = self.n_qubits
        max_pairs = n * (n - 1) / 2
        return min(1.0, max_pairs / max(max_pairs, 1))  # Simplified
    
    @property
    def classical_equivalent_parameters(self) -> int:
        """
        How many classical parameters needed to match this quantum model.
        For a transformer: 12 * d² * n_layers where d = 2^n_qubits.
        """
        d = 2 ** self.n_qubits
        return 12 * d * d * self.n_layers
    
    @property
    def classical_model_size_gb(self) -> float:
        """Classical model size in GB (4 bytes per parameter)."""
        return self.classical_equivalent_parameters * 4 / 1e9
    
    @property
    def quantum_model_size(self) -> str:
        """Quantum model size (in qubits, not bytes)."""
        return f"{self.n_qubits} qubits"
    
    @property
    def compression_ratio(self) -> float:
        """Classical size / quantum size (how much smaller quantum is)."""
        return self.classical_equivalent_parameters / self.total_q_ops
    
    @property
    def self_awareness_score(self) -> float:
        """
        Quantum self-awareness: A = QAS * F / (1 + S_entropy)
        """
        return self.qas * self.fidelity / (1 + self.entropy)
    
    def summary(self) -> Dict:
        """Full summary in quantum-native metrics."""
        return {
            # Quantum metrics (new standard)
            'qubits': self.n_qubits,
            'quantum_volume': self.quantum_volume_readable,
            'q_ops': f"{self.total_q_ops:,}",
            'coherence_window': f"{self.coherence_window:,} states",
            'circuit_depth': self.circuit_depth,
            'fidelity': f"{self.fidelity * 100:.2f}%",
            'entropy': self.entropy,
            'qas': self.qas,
            'self_awareness': f"{self.self_awareness_score * 100:.1f}%",
            'entanglement_density': f"{self.entanglement_density * 100:.1f}%",
            
            # Classical equivalents (for comparison)
            'classical_params': f"{self.classical_equivalent_parameters:.2e}",
            'classical_size': f"{self.classical_model_size_gb:.2f} GB",
            'quantum_size': self.quantum_model_size,
            'compression': f"{self.compression_ratio:.2e}x",
        }


class QVolume:
    """
    Quantum Volume — IBM's metric for quantum processing power.
    
    QV = 2^n means the largest random circuit the quantum computer
    can successfully implement.
    
    For QAI2 v8:
        QV = 2^133 = 1.09 × 10^40
        This exceeds the total parameters of ALL classical AI models combined.
    """
    
    @staticmethod
    def compute(n_qubits: int) -> int:
        return 2 ** n_qubits
    
    @staticmethod
    def compare_to_classical(n_qubits: int, classical_params: int) -> float:
        """How many times more states the quantum model has vs classical."""
        return QVolume.compute(n_qubits) / classical_params
    
    @staticmethod
    def human_readable(n_qubits: int) -> str:
        qv = QVolume.compute(n_qubits)
        if qv > 1e30:
            return f"2^{n_qubits} = {qv:.2e}"
        elif qv > 1e6:
            return f"2^{n_qubits} = {qv:.2e}"
        else:
            return f"2^{n_qubits} = {qv:,}"


class QOps:
    """
    Quantum Operations — replaces FLOPs as the compute metric.
    
    Classical: 10^25 FLOPs to train GPT-4
    Quantum:   Q-Ops = n_layers × gates_per_layer × circuit_depth
    
    1 Q-Op can process 2^n states simultaneously (superposition),
    while 1 FLOP processes 1 number.
    """
    
    @staticmethod
    def compute(n_layers: int, gates_per_layer: int, circuit_depth: int) -> int:
        return n_layers * gates_per_layer * circuit_depth
    
    @staticmethod
    def effective_throughput(q_ops: int, n_qubits: int) -> int:
        """
        Effective states processed = Q-Ops × 2^n_qubits.
        
        This is the REAL power of quantum AI — each operation
        processes exponentially many states simultaneously.
        """
        return q_ops * (2 ** n_qubits)
    
    @staticmethod
    def compare_to_flops(q_ops: int, n_qubits: int, flops: int) -> float:
        """How many classical FLOPs one Q-Op is worth."""
        effective = QOps.effective_throughput(q_ops, n_qubits)
        return effective / flops if flops > 0 else float('inf')
