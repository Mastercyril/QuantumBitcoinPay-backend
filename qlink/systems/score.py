"""
SCORE: State Correlation Entanglement Recognition Engine.

Mathematical Specification:
    I(A : B) = S(\rho_A) + S(\rho_B) - S(\rho_{AB})

where S(\rho) = -\text{Tr}(\rho \log_2 \rho) is the von Neumann entropy.
"""

from typing import Optional
import numpy as np


class SCORE:
    """
    State Correlation Entanglement Recognition Engine.
    Computes quantum mutual information between subsystems A and B.
    """

    @staticmethod
    def von_neumann_entropy(rho: np.ndarray, eps: float = 1e-12) -> float:
        """
        Compute von Neumann entropy S(\rho) = -\text{Tr}(\rho \log_2 \rho).

        Args:
            rho: Density matrix.
            eps: Numerical threshold for non-zero eigenvalues.

        Returns:
            Von Neumann entropy value (float).
        """
        rho_arr = np.asarray(rho, dtype=complex)
        eigenvalues = np.linalg.eigvalsh(rho_arr)
        pos_eigenvals = eigenvalues[eigenvalues > eps]
        if len(pos_eigenvals) == 0:
            return 0.0
        entropy = -np.sum(pos_eigenvals * np.log2(pos_eigenvals))
        return float(np.maximum(0.0, entropy))

    def compute(
        self,
        rho_A: np.ndarray,
        rho_B: np.ndarray,
        rho_AB: np.ndarray
    ) -> float:
        """
        Compute quantum mutual information I(A:B) = S(\rho_A) + S(\rho_B) - S(\rho_{AB}).

        Args:
            rho_A: Density matrix of subsystem A.
            rho_B: Density matrix of subsystem B.
            rho_AB: Joint density matrix of composite system AB.

        Returns:
            Quantum mutual information value I(A:B).
        """
        s_A = self.von_neumann_entropy(rho_A)
        s_B = self.von_neumann_entropy(rho_B)
        s_AB = self.von_neumann_entropy(rho_AB)

        mutual_info = s_A + s_B - s_AB
        return float(np.maximum(0.0, mutual_info))
