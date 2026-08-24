"""
ARQQ: Amplified Repeated Quantum Query Engine.

Mathematical Specification:
    \mathcal{A}^k(O_f |\psi\rangle) = (2 |\psi\rangle\langle\psi| - I)^k O_f |\psi\rangle

where:
    - O_f is the oracle reflection operator.
    - D = 2 |\psi\rangle\langle\psi| - I is the Grover diffusion operator.
"""

from typing import Union, Callable
import numpy as np


class ARQQ:
    """
    Amplified Repeated Quantum Query (ARQQ) engine implementing quantum amplitude amplification.
    """

    def amplify(
        self,
        oracle: Union[np.ndarray, Callable[[np.ndarray], np.ndarray]],
        state: np.ndarray,
        iterations: int = 1
    ) -> np.ndarray:
        """
        Amplify target quantum state amplitudes using repeated oracle queries and diffusion operations.

        Formula:
            |\psi_{k}\rangle = (2 |\psi_0\rangle\langle\psi_0| - I)^k O_f |\psi_{k-1}\rangle

        Args:
            oracle: Oracle matrix O_f OR a callable function mapping state -> oracle_applied_state.
            state: Initial state vector |\psi_0\rangle.
            iterations: Number of amplification iterations k.

        Returns:
            Amplified quantum state vector.
        """
        if iterations < 0:
            raise ValueError("iterations must be a non-negative integer.")

        psi_0 = np.asarray(state, dtype=complex)
        norm = np.linalg.norm(psi_0)
        if norm > 0:
            psi_0 = psi_0 / norm

        dim = psi_0.size
        proj_0 = np.outer(psi_0, np.conj(psi_0))
        D = 2.0 * proj_0 - np.eye(dim, dtype=complex)

        psi = psi_0.copy()

        for _ in range(iterations):
            if callable(oracle):
                psi = oracle(psi)
            else:
                O_f = np.asarray(oracle, dtype=complex)
                psi = O_f @ psi

            psi = D @ psi

            norm_k = np.linalg.norm(psi)
            if norm_k > 0:
                psi /= norm_k

        return psi
