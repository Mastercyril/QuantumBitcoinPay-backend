"""
PhaseModulation: Continuous Quantum Phase Modulation and Evolution.

Mathematical Specification:
    \phi(t) = \phi_0 + \sum_{k=1}^K A_k \sin(\omega_k t + \delta_k)

where:
    - \phi_0 is the baseline phase shift.
    - A_k, \omega_k, \delta_k are amplitude, frequency, and phase offset parameters.
"""

from typing import Dict, Any, Optional
import numpy as np


class PhaseModulation:
    """
    Continuous quantum phase modulation engine and Hamiltonian trajectory synthesizer.
    """

    def modulate(self, t: float, params: Dict[str, Any]) -> float:
        """
        Compute continuous phase \phi(t) at time t.

        Formula:
            \phi(t) = \phi_0 + \sum_{k=1}^K A_k \sin(\omega_k t + \delta_k)

        Args:
            t: Time instant (seconds).
            params: Dictionary containing:
                - 'phi_0': Baseline phase (float, default 0.0)
                - 'components': List of dicts [{'A': float, 'omega': float, 'delta': float}, ...]

        Returns:
            Phase angle \phi(t) in radians.
        """
        phi_0 = float(params.get("phi_0", 0.0))
        components = params.get("components", [])

        phi_t = phi_0
        for comp in components:
            A = float(comp.get("A", 1.0))
            omega = float(comp.get("omega", 1.0))
            delta = float(comp.get("delta", 0.0))
            phi_t += A * np.sin(omega * t + delta)

        return float(phi_t)

    def evolve(
        self,
        state: np.ndarray,
        duration: float,
        dt: float,
        params: Dict[str, Any],
        Hamiltonian: Optional[np.ndarray] = None
    ) -> np.ndarray:
        """
        Synthesize continuous quantum state trajectory |\psi(t)\rangle over a duration.

        Args:
            state: Initial quantum state vector |\psi(0)\rangle.
            duration: Total evolution time (seconds).
            dt: Time step size (seconds).
            params: Phase modulation parameters for modulate().
            Hamiltonian: Optional base system Hamiltonian H_0. Defaults to Pauli Z operator.

        Returns:
            Numpy array of shape (num_steps, dim) containing state vector trajectories over time.
        """
        if duration <= 0 or dt <= 0:
            raise ValueError("duration and dt must be strictly positive.")

        psi_0 = np.asarray(state, dtype=complex)
        norm = np.linalg.norm(psi_0)
        if norm > 0:
            psi_0 = psi_0 / norm

        dim = psi_0.size
        if Hamiltonian is None:
            if dim == 2:
                H_0 = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
            else:
                H_0 = np.eye(dim, dtype=complex)
        else:
            H_0 = np.asarray(Hamiltonian, dtype=complex)

        num_steps = int(np.ceil(duration / dt)) + 1
        trajectory = np.zeros((num_steps, dim), dtype=complex)
        trajectory[0] = psi_0

        psi_t = psi_0.copy()
        for i in range(1, num_steps):
            t = i * dt
            phi_t = self.modulate(t, params)
            evals, evecs = np.linalg.eigh(H_0)
            phase_diag = np.exp(-1j * phi_t * evals * dt)
            U_t = evecs @ np.diag(phase_diag) @ evecs.conj().T
            psi_t = U_t @ psi_t
            norm_t = np.linalg.norm(psi_t)
            if norm_t > 0:
                psi_t /= norm_t
            trajectory[i] = psi_t

        return trajectory
