"""
QSink: Quantum State Information Network Kernel.

Mathematical Specification:
    K = \sum_{i,j} \langle \psi_i | \psi_j \rangle |i\rangle\langle j|

where K_{ij} = \langle \psi_i | \psi_j \rangle is the inner product kernel matrix.
"""

from typing import List, Optional
import numpy as np


class QSink:
    """
    Quantum State Information Network Kernel.
    Constructs quantum Gram matrices and evaluates kernel projections.
    """

    def build_kernel(self, states: List[np.ndarray]) -> np.ndarray:
        """
        Build quantum knowledge kernel matrix K from list of quantum state vectors.

        Formula:
            K_{ij} = \langle \psi_i | \psi_j \rangle

        Args:
            states: List of quantum state vectors.

        Returns:
            Complex matrix of shape (N, N) representing the kernel matrix.
        """
        if not states:
            raise ValueError("states list cannot be empty.")

        norm_states = []
        for s in states:
            arr = np.asarray(s, dtype=complex)
            norm = np.linalg.norm(arr)
            if norm > 0:
                arr = arr / norm
            norm_states.append(arr)

        n = len(norm_states)
        kernel = np.zeros((n, n), dtype=complex)

        for i in range(n):
            for j in range(n):
                kernel[i, j] = np.vdot(norm_states[i], norm_states[j])

        return kernel

    def query(
        self,
        kernel: np.ndarray,
        query_state: np.ndarray,
        database_states: Optional[List[np.ndarray]] = None
    ) -> np.ndarray:
        """
        Query the quantum knowledge kernel to find overlap similarities or projection weights.

        Args:
            kernel: Pre-built quantum kernel matrix K of shape (N, N).
            query_state: Input quantum state vector to query against database.
            database_states: Optional list of database state vectors.

        Returns:
            Numpy array of query similarity scores |\langle \psi_i | \psi_{query} \rangle|^2.
        """
        q_arr = np.asarray(query_state, dtype=complex)
        norm = np.linalg.norm(q_arr)
        if norm > 0:
            q_arr = q_arr / norm

        if database_states is not None:
            overlaps = []
            for s in database_states:
                s_arr = np.asarray(s, dtype=complex)
                s_norm = np.linalg.norm(s_arr)
                if s_norm > 0:
                    s_arr = s_arr / s_norm
                overlap = np.abs(np.vdot(s_arr, q_arr)) ** 2
                overlaps.append(overlap)
            return np.array(overlaps, dtype=float)

        k_arr = np.asarray(kernel, dtype=complex)
        weights = np.real(np.diag(k_arr))
        return np.clip(weights, 0.0, 1.0)
