"""
Q-Norm: Decoherence Correction Replaces Layer Normalization

Classical: LayerNorm normalizes activations across features.
- Statistics: mean and variance
- Prevents gradient issues (vanishing/exploding)
- Fixed normalization (same for all inputs)

Quantum: Q-Norm corrects for decoherence (quantum noise).
- Decoherence is the quantum equivalent of gradient issues
- Corrects phase errors and amplitude damping
- Dynamically adapts (quantum error correction is adaptive)
"""

import math
from typing import List
from .qtoken import QuantumState


class QLayerNorm:
    """
    Quantum Layer Normalization via Decoherence Correction.
    
    Classical LayerNorm: x_norm = (x - μ) / σ * γ + β
    - μ = mean of features
    - σ = std of features
    - γ, β = learned parameters
    
    Quantum Q-Norm: |ψ_norm⟩ = correct_decoherence(|ψ⟩)
    - Corrects amplitude damping (energy loss)
    - Corrects phase errors (dephasing)
    - No learned parameters — physics-based correction
    """
    
    def __init__(self, n_qubits: int = 10, correction_strength: float = 0.9):
        self.n_qubits = n_qubits
        self.correction_strength = correction_strength
    
    def forward(self, state: QuantumState) -> QuantumState:
        """Apply decoherence correction to a quantum state."""
        amps = list(state.amplitudes)
        
        # Re-normalize amplitudes (corrects amplitude damping)
        norm = math.sqrt(sum(abs(a)**2 for a in amps))
        if norm > 0:
            correction = self.correction_strength / norm
            amps = [a * correction for a in amps]
        
        # Phase correction (corrects dephasing)
        # Align phases to reduce quantum noise
        if amps:
            ref_phase = cmath.phase(amps[0]) if amps[0] != 0 else 0
            for i in range(len(amps)):
                if amps[i] != 0:
                    current_phase = cmath.phase(amps[i])
                    phase_diff = current_phase - ref_phase
                    # Damp the phase error
                    corrected_phase = ref_phase + phase_diff * (1 - self.correction_strength)
                    magnitude = abs(amps[i])
                    amps[i] = magnitude * cmath.exp(1j * corrected_phase)
        
        return QuantumState(amps, state.basis_labels)


import cmath
