"""
Universal Codex: Binary-to-Quantum Translation Module.

Mathematical Specification:
    \theta_i = bit_i \cdot \frac{\pi}{2} + g_f \cdot \frac{\pi}{8}

where:
    - bit_i \in \{0, 1\} is the classical bit.
    - g_f \in \mathbb{R} is the gravitational factor.
    - \theta_i \in \mathbb{R} is the quantum phase angle.

Bijection Proof:
    Let f: \{0, 1\} \to \Theta be the encoding map defined by:
        f(b) = b \cdot \frac{\pi}{2} + g_f \cdot \frac{\pi}{8}

    Injectivity:
        Suppose f(b_1) = f(b_2) for b_1, b_2 \in \{0, 1\}.
        Then:
            b_1 \cdot \frac{\pi}{2} + g_f \cdot \frac{\pi}{8} = b_2 \cdot \frac{\pi}{2} + g_f \cdot \frac{\pi}{8}
        Subtracting g_f \cdot \frac{\pi}{8} from both sides:
            b_1 \cdot \frac{\pi}{2} = b_2 \cdot \frac{\pi}{2}
        Dividing by \frac{\pi}{2} gives b_1 = b_2.
        Thus, f is injective.

    Surjectivity:
        Let \Theta = \{ g_f \cdot \frac{\pi}{8}, \frac{\pi}{2} + g_f \cdot \frac{\pi}{8} \} be the image set of f.
        For any angle \theta \in \Theta, the inverse map:
            f^{-1}(\theta) = \frac{\theta - g_f \cdot \frac{\pi}{8}}{\frac{\pi}{2}}
        uniquely recovers b \in \{0, 1\}.
        Thus, f is surjective onto its image set.

    Conclusion:
        The mapping f is a bijection between classical binary states and phase-encoded quantum angles.
"""

from typing import Union, List, Optional
import numpy as np


class UniversalCodex:
    """
    Translates classical binary strings/vectors into quantum phase angles and state vectors,
    incorporating gravitational metrics.
    """

    def __init__(self, gravitational_factor: float = 1.0):
        """
        Initialize the Universal Codex.

        Args:
            gravitational_factor: Scaling factor g_f representing gravitational field metric.
        """
        if not isinstance(gravitational_factor, (int, float, np.number)):
            raise TypeError("gravitational_factor must be a numeric value.")
        self.g_f = float(gravitational_factor)

    def gravitational_factor(self, metric: Optional[np.ndarray] = None) -> float:
        """
        Compute or retrieve the gravitational factor g_f based on an optional metric tensor.

        Args:
            metric: Optional 2D square matrix (e.g. 4x4 spacetime metric g_{\mu\nu}).

        Returns:
            Computed or default gravitational factor g_f.
        """
        if metric is not None:
            metric_arr = np.asarray(metric, dtype=float)
            if metric_arr.ndim != 2 or metric_arr.shape[0] != metric_arr.shape[1]:
                raise ValueError("Metric tensor must be a square 2D matrix.")
            self.g_f = float(np.abs(np.trace(metric_arr)) / metric_arr.shape[0])
        return self.g_f

    def encode(self, bits: Union[List[int], np.ndarray, str]) -> np.ndarray:
        """
        Encode binary sequence into quantum phase angles.

        Formula:
            \theta_i = bit_i \cdot \frac{\pi}{2} + g_f \cdot \frac{\pi}{8}

        Args:
            bits: Binary input sequence (list of ints, 1D numpy array, or binary string like "0110").

        Returns:
            Numpy array of phase angles in radians.
        """
        bit_arr = self._parse_bits(bits)
        phases = bit_arr * (np.pi / 2.0) + self.g_f * (np.pi / 8.0)
        return phases

    def decode(self, phases: Union[List[float], np.ndarray]) -> np.ndarray:
        """
        Decode quantum phase angles back to binary sequence.

        Formula:
            bit_i = \text{round}\left(\frac{\theta_i - g_f \cdot \frac{\pi}{8}}{\frac{\pi}{2}}\right)

        Args:
            phases: Array or list of phase angles.

        Returns:
            Numpy array of integer bits (0 or 1).
        """
        phase_arr = np.asarray(phases, dtype=float)
        shifted = phase_arr - self.g_f * (np.pi / 8.0)
        raw_bits = np.round(shifted / (np.pi / 2.0)).astype(int)
        bits = np.clip(raw_bits, 0, 1)
        return bits

    def quantum_state(self, bits: Union[List[int], np.ndarray, str], full_tensor: bool = False) -> np.ndarray:
        """
        Construct quantum state vector(s) from classical bits.

        Single qubit state for phase \theta_i:
            |\psi(\theta_i)\rangle = \cos(\theta_i / 2)|0\rangle + e^{i \theta_i} \sin(\theta_i / 2)|1\rangle

        Args:
            bits: Binary input sequence.
            full_tensor: If True, returns the 2^N dimensional tensor product state vector.
                        If False, returns array of shape (N, 2) containing single-qubit state vectors.

        Returns:
            Complex numpy array of quantum state amplitudes.
        """
        phases = self.encode(bits)
        qubit_states = []
        for theta in phases:
            c = np.cos(theta / 2.0)
            s = np.sin(theta / 2.0) * np.exp(1j * theta)
            qubit_states.append(np.array([c, s], dtype=complex))

        if not full_tensor:
            return np.array(qubit_states)

        state_vec = qubit_states[0]
        for q in qubit_states[1:]:
            state_vec = np.kron(state_vec, q)
        return state_vec

    def _parse_bits(self, bits: Union[List[int], np.ndarray, str]) -> np.ndarray:
        """Helper to parse and validate binary inputs."""
        if isinstance(bits, str):
            if not all(c in ('0', '1') for c in bits):
                raise ValueError("Binary string must contain only '0' and '1'.")
            bit_list = [int(c) for c in bits]
        elif isinstance(bits, (list, tuple, np.ndarray)):
            bit_list = [int(b) for b in bits]
            if not all(b in (0, 1) for b in bit_list):
                raise ValueError("All elements in bits array must be 0 or 1.")
        else:
            raise TypeError("bits must be a string, list, tuple, or numpy array.")

        if len(bit_list) == 0:
            raise ValueError("Input bits cannot be empty.")

        return np.array(bit_list, dtype=float)
