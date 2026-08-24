"""
ESCORT: Entangled State Channel for Quantum Routing.

Mathematical Specification:
    \rho_{routed} = \sum_k p_k E_k \rho E_k^\dagger

where:
    - p_k \ge 0, \sum_k p_k = 1 are channel routing probabilities.
    - E_k are quantum channel routing Kraus operators.
"""

from typing import List, Tuple, Union
import numpy as np


class ESCORT:
    """
    Entangled State Channel for Quantum Routing.
    Routes quantum state vectors or density matrices through quantum channels.
    """

    def route(
        self,
        state: np.ndarray,
        channels: List[Tuple[float, np.ndarray]]
    ) -> np.ndarray:
        """
        Route quantum state through channels weighted by probabilities p_k.

        Formula:
            \rho_{out} = \sum_k p_k E_k \rho E_k^\dagger

        Args:
            state: Quantum state vector (1D) or density matrix (2D).
            channels: List of (p_k, E_k) tuples where p_k is probability and E_k is operator.

        Returns:
            Routed quantum state array (density matrix or state vector).
        """
        if not channels:
            raise ValueError("channels list cannot be empty.")

        p_sum = sum(p for p, _ in channels)
        if not np.isclose(p_sum, 1.0, atol=1e-3):
            channels = [(p / p_sum, E) for p, E in channels]

        state_arr = np.asarray(state, dtype=complex)

        if state_arr.ndim == 1:
            norm = np.linalg.norm(state_arr)
            if norm > 0:
                state_arr = state_arr / norm
            rho = np.outer(state_arr, np.conj(state_arr))
            is_vector = True
        else:
            rho = state_arr
            is_vector = False

        dim = rho.shape[0]
        routed_rho = np.zeros((dim, dim), dtype=complex)

        for p_k, E_k in channels:
            E_arr = np.asarray(E_k, dtype=complex)
            if E_arr.shape != (dim, dim):
                raise ValueError(f"Kraus operator shape {E_arr.shape} does not match state dimension ({dim}, {dim}).")
            routed_rho += p_k * (E_arr @ rho @ E_arr.conj().T)

        if is_vector:
            eigvals, eigvecs = np.linalg.eigh(routed_rho)
            max_idx = np.argmax(eigvals)
            if np.isclose(eigvals[max_idx], 1.0, atol=1e-2):
                routed_vec = eigvecs[:, max_idx]
                return routed_vec / np.linalg.norm(routed_vec)

        return routed_rho
