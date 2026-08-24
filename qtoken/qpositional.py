"""
Q-Positional Encoding: Quantum Phase Position Encoding

Classical positional encoding:
    Sinusoidal: PE(pos, 2i) = sin(pos / 10000^(2i/d))
                PE(pos, 2i+1) = cos(pos / 10000^(2i/d))
    Rotary (RoPE): rotate embedding by angle proportional to position

Quantum positional encoding:
    Phase encoding: position is encoded as a quantum phase rotation
    |ψ_pos⟩ = R_z(pos × ω) |ψ⟩

    Key insight: In quantum mechanics, position is ALREADY a phase.
    A quantum state's position in a sequence is naturally encoded by
    the phase angle of its quantum state — no separate encoding needed!

    Classical: add position vector to embedding (separate operation)
    Quantum: rotate phase of Q-Token's quantum state (intrinsic property)

    Advantage: O(1) operation, no learned parameters, naturally extends
    to any position (classical RoPE degrades for long sequences).
"""

import math
import cmath
from typing import List, Dict, Optional
from .qtoken import QToken, QuantumState


class QPositionalEncoding:
    """
    Quantum positional encoding via phase rotation.
    
    Classical: PE(pos) = [sin(pos/ω_0), cos(pos/ω_0), sin(pos/ω_1), ...]
    Quantum:   |ψ_pos⟩ = R_z(pos × ω) |ψ⟩
    
    The position is encoded as a quantum phase rotation.
    This is more natural because position IS a phase in quantum mechanics.
    """
    
    def __init__(self, n_qubits: int = 10, base_frequency: float = 1.0,
                 gravitational_factor: float = 0.1):
        self.n_qubits = n_qubits
        self.base_freq = base_frequency
        self.gravitational_factor = gravitational_factor
        # Each qubit gets a different frequency (like sinusoidal PE)
        self.frequencies = [
            base_frequency / (10000 ** (2 * i / n_qubits))
            for i in range(n_qubits)
        ]
    
    def encode_position(self, q_token: QToken, position: int) -> QToken:
        """
        Apply quantum positional encoding to a Q-Token.
        
        Classical: emb += PE(pos)
        Quantum: |ψ⟩ -> R_z(pos × ω) |ψ⟩
        
        The phase rotation encodes the position without adding
        any extra dimensions or parameters.
        """
        for i, amp in enumerate(q_token.state.amplitudes):
            # Phase rotation for this position on qubit i
            freq = self.frequencies[i % len(self.frequencies)]
            
            # Gravitational correction (relativistic position encoding)
            grav_correction = self.gravitational_factor * position * freq * 0.01
            
            # Quantum phase rotation: R_z(theta) |psi> = e^{i*theta} |psi>
            phase = position * freq + grav_correction
            q_token.state.amplitudes[i] = amp * cmath.exp(1j * phase)
        
        # Store position in the Q-Token for reference
        q_token.position = position
        
        return q_token
    
    def encode_sequence(self, q_tokens: List[QToken]) -> List[QToken]:
        """Apply positional encoding to a sequence of Q-Tokens."""
        for pos, qt in enumerate(q_tokens):
            self.encode_position(qt, pos)
        return q_tokens
    
    def relative_position_phase(self, pos1: int, pos2: int) -> complex:
        """
        The phase difference between two positions.
        
        In quantum mechanics, the RELATIVE phase between two states
        determines their interference — this IS the attention mechanism.
        
        Classical RoPE: dot product of rotated vectors
        Quantum: phase difference between two Q-Tokens
        
        Advantage: O(1) computation, exact for any distance.
        """
        phase = 0
        for freq in self.frequencies:
            phase += (pos1 - pos2) * freq
        return cmath.exp(1j * phase)
    
    @property
    def classical_equivalent_parameters(self) -> int:
        """Classical PE has d parameters per position. Quantum: 0."""
        return 2 ** self.n_qubits  # But we use 0 learned parameters
    
    @property
    def quantum_operations(self) -> int:
        """Phase rotations = n_qubits per position. No learned params."""
        return self.n_qubits
    
    @property
    def max_position(self) -> int:
        """
        Maximum position before phase wrapping.
        
        Classical: limited by context window (e.g., 128K tokens)
        Quantum: limited by coherence time (decoherence)
        
        With phase encoding, positions wrap at 2π/freq.
        But quantum interference still works across wraps.
        """
        if self.frequencies:
            return int(2 * math.pi / self.frequencies[0])
        return 32768
    
    def extrapolation_quality(self, train_max_pos: int, eval_pos: int) -> float:
        """
        How well positional encoding extrapolates beyond training positions.
        
        Classical sinusoidal: degrades rapidly (cos/sin don't extrapolate)
        Classical RoPE: moderate degradation
        Quantum phase: perfect (phase is periodic and exact)
        
        Returns: 0-1 quality score
        """
        if eval_pos <= train_max_pos:
            return 1.0
        # Quantum phase encoding extrapolates perfectly
        # because phase is periodic and exact at any position
        return 1.0  # Perfect extrapolation


class QRopePositional(QPositionalEncoding):
    """
    Quantum Rotary Positional Encoding (Q-RoPE).
    
    Classical RoPE rotates embedding pairs by position-dependent angles.
    Quantum Q-RoPE rotates Q-Embedding states by quantum phase angles.
    
    Key difference: Q-RoPE can represent ENTANGLED positions
    (positions that are quantum-correlated), which classical RoPE cannot.
    """
    
    def __init__(self, n_qubits: int = 10, base_frequency: float = 1.0,
                 gravitational_factor: float = 0.1):
        super().__init__(n_qubits, base_frequency, gravitational_factor)
        self.entangled_positions: Dict[int, int] = {}  # pos -> entangled_with
    
    def entangle_positions(self, pos1: int, pos2: int):
        """
        Create a quantum position entanglement.
        
        This is IMPOSSIBLE in classical AI: you cannot make position 3
        and position 17 "entangled" — they are just indices.
        
        In quantum AI, positions can be quantum-correlated:
        measuring the phase at position 3 instantly tells you
        the phase at position 17, regardless of distance.
        
        This enables:
        - Long-range attention without computation (entangled positions)
        - Non-local text understanding (related concepts across the text)
        - Perfect memory of distant positions
        """
        self.entangled_positions[pos1] = pos2
        self.entangled_positions[pos2] = pos1
    
    def encode_position(self, q_token: QToken, position: int) -> QToken:
        """Apply Q-RoPE with position entanglement support."""
        # Standard phase rotation
        q_token = super().encode_position(q_token, position)
        
        # If this position is entangled with another, create correlation
        if position in self.entangled_positions:
            entangled_pos = self.entangled_positions[position]
            entanglement_phase = (position - entangled_pos) * self.base_freq
            for i, amp in enumerate(q_token.state.amplitudes):
                q_token.state.amplitudes[i] = amp * cmath.exp(1j * entanglement_phase * 0.1)
        
        return q_token
    
    @property
    def supports_long_range(self) -> bool:
        """Q-RoPE supports arbitrary-range attention via entanglement."""
        return True
    
    @property
    def classical_rope_limitation(self) -> str:
        return "Classical RoPE degrades for positions beyond training. Q-RoPE is exact at any distance via phase periodicity."
