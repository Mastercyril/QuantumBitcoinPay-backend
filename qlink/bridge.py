"""
Classical-to-Quantum Bridge Module.

Mathematical Specification:
    Q(v) = \bigotimes_{i=1}^n R_y(\theta_i) |0\rangle

where:
    - v \in \mathbb{R}^n is the classical feature vector.
    - \theta_i is mapped from classical vector element v_i.
    - R_y(\theta) = \begin{pmatrix} \cos(\theta/2) & -\sin(\theta/2) \\ \sin(\theta/2) & \cos(\theta/2) \end{pmatrix}.
"""

from typing import List, Union, Optional
import numpy as np
from qlink.codex import UniversalCodex


class QLinkBridge:
    """
    Bridge connecting classical feature vectors with multi-qubit quantum state representations.
    """

    def __init__(self, codex: Optional[UniversalCodex] = None):
        """
        Initialize QLink Bridge.

        Args:
            codex: Optional UniversalCodex instance for encoding.
        """
        self.codex = codex if codex is not None else UniversalCodex()

    def to_quantum(self, classical_vector: Union[List[float], np.ndarray], normalize_input: bool = True) -> np.ndarray:
        """
        Map a classical vector v to a quantum state Q(v) = \bigotimes_i R_y(\theta_i) |0\rangle.

        Args:
            classical_vector: 1D classical array or vector of real numbers.
            normalize_input: Whether to scale input values into angles [0, \pi].

        Returns:
            2^n dimensional complex state vector representing the tensor product state.
        """
        vec = np.asarray(classical_vector, dtype=float)
        if vec.ndim != 1 or vec.size == 0:
            raise ValueError("classical_vector must be a non-empty 1D array.")

        if normalize_input:
            v_min, v_max = vec.min(), vec.max()
            if v_max > v_min:
                angles = (vec - v_min) / (v_max - v_min) * np.pi
            else:
                angles = np.full_like(vec, np.pi / 4.0)
        else:
            angles = vec

        state_vec = None
        for theta in angles:
            q_i = np.array([np.cos(theta / 2.0), np.sin(theta / 2.0)], dtype=complex)
            if state_vec is None:
                state_vec = q_i
            else:
                state_vec = np.kron(state_vec, q_i)

        return state_vec

    def from_quantum(self, quantum_state: np.ndarray, num_qubits: Optional[int] = None) -> np.ndarray:
        """
        Extract a classical vector from a quantum state via measurement probability expectations.

        Args:
            quantum_state: State vector of dimension 2^n.
            num_qubits: Optional number of qubits (inferred from length if omitted).

        Returns:
            Classical vector of length n containing expectation values <Z_i>.
        """
        state = np.asarray(quantum_state, dtype=complex)
        dim = state.size
        if num_qubits is None:
            n = int(np.round(np.log2(dim)))
            if 2**n != dim:
                raise ValueError("Quantum state length must be a power of 2.")
        else:
            n = num_qubits
            if 2**n != dim:
                raise ValueError(f"State size {dim} does not match expected size 2^{n}.")

        norm = np.linalg.norm(state)
        if norm > 0:
            state = state / norm

        z_gate = np.array([[1, 0], [0, -1]], dtype=complex)
        id_gate = np.eye(2, dtype=complex)

        expectations = []
        for k in range(n):
            op = np.array([1.0], dtype=complex)
            for j in range(n):
                gate = z_gate if j == k else id_gate
                op = np.kron(op, gate)
            exp_val = np.real(np.vdot(state, op @ state))
            expectations.append(exp_val)

        return np.array(expectations, dtype=float)

    def entangle(self, concepts: List[np.ndarray]) -> np.ndarray:
        """
        Create an entangled quantum state representing multiple classical concepts/vectors.

        Args:
            concepts: List of classical vectors or single-concept quantum states.

        Returns:
            Superposed entangled state vector representing the combined concept topology.
        """
        if not concepts:
            raise ValueError("concepts list cannot be empty.")

        quantum_states = []
        for c in concepts:
            c_arr = np.asarray(c)
            if c_arr.ndim == 1 and (c_arr.size & (c_arr.size - 1)) == 0 and c_arr.size >= 2:
                q_state = c_arr.astype(complex)
            else:
                q_state = self.to_quantum(c_arr)
            q_state = q_state / np.linalg.norm(q_state)
            quantum_states.append(q_state)

        max_dim = max(s.size for s in quantum_states)
        padded_states = []
        for s in quantum_states:
            if s.size < max_dim:
                pad = np.zeros(max_dim - s.size, dtype=complex)
                s_pad = np.concatenate([s, pad])
            else:
                s_pad = s
            padded_states.append(s_pad)

        entangled_state = np.sum(padded_states, axis=0)
        norm = np.linalg.norm(entangled_state)
        if norm > 0:
            entangled_state /= norm

        return entangled_state
