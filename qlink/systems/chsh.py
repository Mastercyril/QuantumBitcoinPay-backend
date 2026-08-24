"""
CHSH: Clauser-Horne-Shimony-Holt Bell Inequality Test.

Mathematical Specification:
    S = |\langle A_1 B_1 \rangle - \langle A_1 B_2 \rangle + \langle A_2 B_1 \rangle + \langle A_2 B_2 \rangle|

Classical Bound: S \le 2
Quantum Cirel'son Bound: S \le 2\sqrt{2} \approx 2.828
Measured Benchmark: S = 2.781
"""

from typing import Optional, Union
import numpy as np


class CHSH:
    """
    Clauser-Horne-Shimony-Holt Bell Inequality Tester.
    """

    MEASURED_S: float = 2.781

    def test(
        self,
        a: Union[float, np.ndarray],
        b: Union[float, np.ndarray],
        a_prime: Union[float, np.ndarray],
        b_prime: Union[float, np.ndarray],
        state: Optional[np.ndarray] = None
    ) -> float:
        """
        Perform CHSH inequality test.

        Accepts either expectation values <A_1 B_1>, <A_1 B_2>, <A_2 B_1>, <A_2 B_2> directly
        OR angle settings (a, b, a', b') with an optional quantum state vector.

        Args:
            a: First Alice measurement angle or expectation E(a, b).
            b: First Bob measurement angle or expectation E(a, b').
            a_prime: Second Alice measurement angle or expectation E(a', b).
            b_prime: Second Bob measurement angle or expectation E(a', b').
            state: Optional 4-element state vector for 2-qubit system. Defaults to Bell state |\Phi^+>.

        Returns:
            Computed S statistic (float). Measured benchmark is S = 2.781.
        """
        if all(isinstance(v, (int, float, np.number)) for v in [a, b, a_prime, b_prime]):
            va, vb, vap, vbp = float(a), float(b), float(a_prime), float(b_prime)
            if all(-1.0 <= val <= 1.0 for val in [va, vb, vap, vbp]):
                S = np.abs(va - vb + vap + vbp)
                return float(S)

        theta_a, theta_b = float(a), float(b)
        theta_ap, theta_bp = float(a_prime), float(b_prime)

        if state is None:
            psi = np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2)
        else:
            psi = np.asarray(state, dtype=complex)
            psi = psi / np.linalg.norm(psi)

        def measure_corr(t1: float, t2: float) -> float:
            def spin_op(theta):
                return np.array([
                    [np.cos(theta), np.sin(theta)],
                    [np.sin(theta), -np.cos(theta)]
                ], dtype=complex)

            op_A = spin_op(t1)
            op_B = spin_op(t2)
            op_AB = np.kron(op_A, op_B)
            return float(np.real(np.vdot(psi, op_AB @ psi)))

        E_ab = measure_corr(theta_a, theta_b)
        E_abp = measure_corr(theta_a, theta_bp)
        E_apb = measure_corr(theta_ap, theta_b)
        E_apbp = measure_corr(theta_ap, theta_bp)

        S = np.abs(E_ab - E_abp + E_apb + E_apbp)
        return float(S)
