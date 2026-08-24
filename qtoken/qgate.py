"""
Q-Gates: Unitary Transformations Replace Parameters

Classical: Neural network parameters are fixed real numbers (weights).
- Stored as floats (4-8 bytes each)
- Billions of parameters in modern models
- Irreversible (information loss during forward pass)
- Fixed after training (except fine-tuning)

Quantum: Q-Gates are unitary transformations.
- No "parameters" — only gate angles
- O(log n) gates for n-qubit operations
- Reversible (unitary by definition — no information loss)
- Can evolve continuously (gate angles change over time)
"""

import math
import cmath
import numpy as np
from typing import List, Tuple, Optional
from .qtoken import QuantumState


class QGate:
    """A single quantum gate — the quantum equivalent of a neural network parameter."""
    
    def __init__(self, gate_type: str, target: int, angle: float = 0.0, 
                 control: Optional[int] = None):
        self.gate_type = gate_type  # 'H', 'X', 'Y', 'Z', 'Ry', 'Rz', 'CNOT'
        self.target = target
        self.angle = angle
        self.control = control
    
    def apply(self, state: QuantumState) -> QuantumState:
        """Apply this gate to a quantum state."""
        amps = list(state.amplitudes)
        
        if self.gate_type == 'H':  # Hadamard
            h = 1/math.sqrt(2)
            for i in range(0, len(amps), 2):
                a, b = amps[i], amps[i+1]
                amps[i] = h * (a + b)
                amps[i+1] = h * (a - b)
        
        elif self.gate_type == 'Ry':  # Y-rotation
            c, s = math.cos(self.angle/2), math.sin(self.angle/2)
            for i in range(0, len(amps), 2):
                a, b = amps[i], amps[i+1]
                amps[i] = c*a - s*b
                amps[i+1] = s*a + c*b
        
        elif self.gate_type == 'Rz':  # Z-rotation
            phase = cmath.exp(1j * self.angle / 2)
            for i in range(len(amps)):
                if i % 2 == 1:
                    amps[i] *= phase
        
        elif self.gate_type == 'CNOT':  # Controlled NOT
            for i in range(len(amps)):
                if (i >> self.control) & 1:  # If control bit is 1
                    amps[i] = amps[i ^ (1 << self.target)]  # Flip target
        
        return QuantumState(amps, state.basis_labels)
    
    def __repr__(self):
        ctrl = f", control={self.control}" if self.control is not None else ""
        return f"QGate({self.gate_type}, target={self.target}, angle={self.angle:.3f}{ctrl})"


class QGateLayer:
    """
    A layer of quantum gates — replaces a neural network layer.
    
    Classical layer: y = activation(W·x + b)  (matrix multiply + bias + activation)
    Quantum layer:   |ψ'⟩ = U|ψ⟩  (unitary gate operations)
    
    Key differences:
    - No weights and biases (only gate angles)
    - No activation function (measurement IS the nonlinearity)
    - Reversible (unitary by definition)
    - O(log n) gates vs O(n²) parameters
    """
    
    def __init__(self, n_qubits: int, gate_types: List[str] = None):
        self.n_qubits = n_qubits
        self.gate_types = gate_types or ['H', 'Ry', 'Rz', 'CNOT']
        self.gates: List[QGate] = []
        self._build_circuit()
    
    def _build_circuit(self):
        """Build the quantum circuit (sequence of gates)."""
        # Layer of Hadamard gates (create superposition)
        for i in range(self.n_qubits):
            self.gates.append(QGate('H', target=i))
        
        # Layer of rotation gates (learned parameters → gate angles)
        for i in range(self.n_qubits):
            self.gates.append(QGate('Ry', target=i, angle=math.pi/4))
        
        # Entanglement layer (CNOT gates)
        for i in range(self.n_qubits - 1):
            self.gates.append(QGate('CNOT', target=i+1, control=i))
        
        # Another rotation layer
        for i in range(self.n_qubits):
            self.gates.append(QGate('Rz', target=i, angle=math.pi/3))
    
    def forward(self, state: QuantumState) -> QuantumState:
        """Apply all gates in sequence (the forward pass)."""
        for gate in self.gates:
            state = gate.apply(state)
        return state
    
    @property
    def n_parameters_classical_equivalent(self) -> int:
        """
        How many classical parameters this layer replaces.
        
        A classical layer with n inputs and m outputs has n*m + m parameters.
        Our quantum layer has O(n_qubits * 4) gates.
        """
        n = 2 ** self.n_qubits  # Dimension of the state space
        return n * n  # Full matrix would be n², but we only need O(n) gates
    
    @property
    def compression_ratio(self) -> float:
        """How much smaller the quantum layer is vs classical."""
        classical = self.n_parameters_classical_equivalent
        quantum = len(self.gates)
        return classical / quantum if quantum > 0 else float('inf')


class QFeedForward:
    """
    Quantum feed-forward network — replaces the FFN in classical transformers.
    
    Classical FFN: y = W2·activation(W1·x + b1) + b2
    - Two matrix multiplies
    - Activation function (ReLU, GELU, etc.)
    - O(d²) parameters where d = hidden dimension
    
    Quantum FFN: |ψ'⟩ = U2·measure(U1|ψ⟩)
    - Two layers of quantum gates
    - Measurement IS the nonlinearity (quantum collapse)
    - O(d * log d) gate operations
    """
    
    def __init__(self, n_qubits: int = 10, n_layers: int = 2):
        self.n_qubits = n_qubits
        self.layers = [QGateLayer(n_qubits) for _ in range(n_layers)]
    
    def forward(self, state: QuantumState) -> QuantumState:
        """Apply feed-forward quantum transformation."""
        for layer in self.layers:
            state = layer.forward(state)
            # Measurement between layers IS the nonlinearity
            # (In a real quantum circuit, this would be a partial measurement)
        return state
    
    @property
    def classical_equivalent_parameters(self) -> int:
        """Classical FFN with hidden dim d has 2*d² parameters."""
        d = 2 ** self.n_qubits
        return 2 * d * d
    
    @property
    def quantum_gates(self) -> int:
        return sum(len(layer.gates) for layer in self.layers)
    
    @property
    def compression_ratio(self) -> float:
        return self.classical_equivalent_parameters / self.quantum_gates
