"""
SCornerProtocol: S-Corner Protocol for Corner-Case Quantum Reasoning.

Mathematical Specification:
    U(\phi, \alpha) = \prod_i R_z(\phi_i) R_x(\alpha_i)

where:
    - R_z(\phi) = \begin{pmatrix} e^{-i\phi/2} & 0 \\ 0 & e^{i\phi/2} \end{pmatrix}
    - R_x(\alpha) = \begin{pmatrix} \cos(\alpha/2) & -i\sin(\alpha/2) \\ -i\sin(\alpha/2) & \cos(\alpha/2) \end{pmatrix}
"""

from typing import List, Tuple
import numpy as np


class SCornerProtocol:
    """
    S-Corner Protocol for quantum corner-case reasoning using product of sequential rotation operators.
    """

    @staticmethod
    def rx(alpha: float) -> np.ndarray:
        """Rx rotation matrix."""
        a2 = alpha / 2.0
        return np.array([
            [np.cos(a2), -1j * np.sin(a2)],
            [-1j * np.sin(a2), np.cos(a2)]
        ], dtype=complex)

    @staticmethod
    def rz(phi: float) -> np.ndarray:
        """Rz rotation matrix."""
        p2 = phi / 2.0
        return np.array([
            [np.exp(-1j * p2), 0.0],
            [0.0, np.exp(1j * p2)]
        ], dtype=complex)

    def apply(
        self,
        state: np.ndarray,
        rotations: List[Tuple[float, float]]
    ) -> np.ndarray:
        """
        Apply sequential R_z(\phi_i) R_x(\alpha_i) rotations to a quantum state vector.

        Formula:
            |\psi_{out}\rangle = \prod_i (R_z(\phi_i) R_x(\alpha_i)) |\psi_{in}\rangle

        Args:
            state: Single qubit state (2-element vector) or multi-qubit state vector.
            rotations: List of rotation angle pairs [(phi_1, alpha_1), (phi_2, alpha_2), ...].

        Returns:
            Transformed quantum state vector.
        """
        if not rotations:
            return np.asarray(state, dtype=complex)

        state_arr = np.asarray(state, dtype=complex)

        U_total = np.eye(2, dtype=complex)
        for phi_i, alpha_i in rotations:
            rz_mat = self.rz(phi_i)
            rx_mat = self.rx(alpha_i)
            U_total = rz_mat @ rx_mat @ U_total

        if state_arr.size == 2:
            transformed = U_total @ state_arr
        else:
            dim = state_arr.size
            n_qubits = int(np.round(np.log2(dim)))
            op = U_total
            for _ in range(n_qubits - 1):
                op = np.kron(op, U_total)
            transformed = op @ state_arr

        norm = np.linalg.norm(transformed)
        if norm > 0:
            transformed /= norm

        return transformed
