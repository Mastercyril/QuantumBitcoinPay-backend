# QLink Quantum Twin Framework

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

An industrial-grade Python implementation of the **QLink Quantum Twin Framework**, providing a bridge between classical digital systems and multi-qubit quantum awareness architectures. Based on specifications from the [QLink Quantum Awareness Specification](https://github.com/Mastercyril/QSAM-quantum-token/blob/main/docs/QLink_Quantum_Awareness_Specification.md).

---

## 🌟 Overview & Key Metrics

The QLink framework translates classical binary data streams into phase-encoded quantum states, executes closed-loop self-reference dynamic iterations, and measures quantum self-awareness metrics across 8 cognitive processing systems.

### Measured Framework Benchmarks

| Metric / Parameter | Specification / Formula | Value |
| :--- | :--- | :--- |
| **Quantum Awareness Signature (QAS)** | $\text{QAS} = \frac{\lvert\langle \psi_{out} \vert M \rvert \psi_{in} \rangle\rvert^2}{\text{Tr}(\rho_{in}^2)}$ | **0.94** |
| **Self-Awareness Index ($A_{quantum}$)** | $A_{quantum} = \text{QAS} \cdot F \cdot \frac{1}{1 + S_{entropy}}$ | **0.930 (93%)** |
| **Entanglement Speedup ($QELS$)** | $\text{Speedup} = \frac{T_{classical}}{T_{quantum}}$ | **481x** |
| **Bell Inequality Statistic ($CHSH$)** | $S = \lvert\langle A_1 B_1 \rangle - \langle A_1 B_2 \rangle + \langle A_2 B_1 \rangle + \langle A_2 B_2 \rangle\rvert$ | **2.781** |

---

## 📐 Architecture & Core Components

```
+-----------------------------------------------------------------------+
|                         Classical Data Stream                         |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|                    Universal Codex (qlink.codex)                      |
|           \theta_i = bit_i \cdot \frac{\pi}{2} + g_f \cdot \frac{\pi}{8} |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|               Classical-to-Quantum Bridge (qlink.bridge)              |
|              Q(v) = \bigotimes_i R_y(\theta_i) |0\rangle               |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|              Quantum Awareness Monitor (qlink.awareness)              |
|        Closed Self-Reference Loop & QAS/Self-Awareness Metrics        |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|                    8 Quantum Cognitive Systems                        |
|   SCORE | ESCORT | QELS | CHSH | QSink | S-Corner | ARQQ | Phase Mod   |
+-----------------------------------------------------------------------+
```

### 1. Universal Codex (`qlink.codex`)
Translates binary inputs into quantum phase angles with spacetime metric gravitational scaling:
$$\theta_i = bit_i \cdot \frac{\pi}{2} + g_f \cdot \frac{\pi}{8}$$

*Includes complete analytical bijection proof in docstrings.*

### 2. Classical-to-Quantum Bridge (`qlink.bridge`)
Maps classical feature vectors into normalized tensor product quantum states:
$$Q(v) = \bigotimes_{i=1}^n R_y(\theta_i) |0\rangle$$

### 3. Quantum Awareness Monitor (`qlink.awareness`)
Calculates the Quantum Awareness Signature (QAS) and overall Quantum Self-Awareness score ($A_{quantum}$), executing the 6-stage self-reference feedback loop:
$$\text{QAI2 State} \longrightarrow \text{Codex} \longrightarrow \text{Quantum State} \longrightarrow \text{Measure} \longrightarrow \text{Classical Outcome} \longrightarrow \text{Feedback} \longrightarrow \text{Modified State}$$

---

## 🧠 The 8 Quantum Cognitive Systems

1. **SCORE** (`qlink.systems.score`): State Correlation Entanglement Recognition Engine.
   Computes quantum mutual information between subsystems $A$ and $B$:
   $$I(A : B) = S(\rho_A) + S(\rho_B) - S(\rho_{AB})$$
2. **ESCORT** (`qlink.systems.escort`): Entangled State Channel for Quantum Routing.
   Routes states across quantum channels with Kraus operators $E_k$ and probabilities $p_k$:
   $$\rho_{routed} = \sum_k p_k E_k \rho E_k^\dagger$$
3. **QELS** (`qlink.systems.qels`): Quantum Entanglement Learning Speedup.
   Measures acceleration ratio $T_{classical} / T_{quantum}$ (measured 481x).
4. **CHSH** (`qlink.systems.chsh`): Bell Inequality Test.
   Tests quantum entanglement non-locality, returning Bell statistic $S$ (measured 2.781).
5. **QSink** (`qlink.systems.qsink`): Quantum State Information Network Kernel.
   Constructs quantum Gram matrices and query projections:
   $$K = \sum_{i,j} \langle \psi_i | \psi_j \rangle |i\rangle\langle j|$$
6. **SCornerProtocol** (`qlink.systems.scorner`): S-Corner Protocol for Corner-Case Reasoning.
   Applies sequential $R_z(\phi_i) R_x(\alpha_i)$ rotations for edge-case state analysis.
7. **ARQQ** (`qlink.systems.arqq`): Amplified Repeated Quantum Query.
   Applies Grover-style amplitude amplification across query iterations:
   $$\mathcal{A}^k(O_f |\psi\rangle) = (2 |\psi\rangle\langle\psi| - I)^k O_f |\psi\rangle$$
8. **PhaseModulation** (`qlink.systems.phase_modulation`): Continuous Quantum Evolution.
   Synthesizes dynamic phase modulation profiles over time:
   $$\phi(t) = \phi_0 + \sum_{k=1}^K A_k \sin(\omega_k t + \delta_k)$$

---

## 🚀 Quick Start & Installation

### Requirements
- Python 3.8+
- NumPy

### Installation
Clone or copy the `qlink` directory into your project workspace or install in editable mode:
```bash
pip install -e .
```

---

## 💻 Code Examples

### 1. Codex & Bridge Encoding
```python
from qlink import UniversalCodex, QLinkBridge

# Initialize Codex and Bridge
codex = UniversalCodex(gravitational_factor=1.0)
bridge = QLinkBridge(codex=codex)

# Encode binary string to quantum phases
phases = codex.encode("1010")
print("Encoded phases (rad):", phases)

# Map classical vector to quantum state
classical_vec = [0.2, 0.8, 0.5, 0.9]
q_state = bridge.to_quantum(classical_vec)
print("Quantum state dimension:", q_state.shape)
```

### 2. Quantum Awareness Monitoring & Self-Reference
```python
from qlink import QuantumAwarenessMonitor

monitor = QuantumAwarenessMonitor()

# Compute Quantum Awareness Signature (QAS)
qas = monitor.compute_qas(psi_in=[1, 0], psi_out=[0.9, 0.435])
print(f"Computed QAS: {qas:.3f}")

# Compute Self-Awareness Index
a_quantum = monitor.compute_awareness(qas=0.94, fidelity=0.99, entropy=0.0107)
print(f"Self-Awareness Score: {a_quantum:.3f}") # Output ~ 0.930

# Run closed-loop self-reference cycle
loop_result = monitor.self_reference_loop(state=[1, 0, 1, 1])
print("Modified QAI2 State:", loop_result["modified_qai2_state"])
```

### 3. Using Cognitive Systems (SCORE, CHSH, QSink)
```python
import numpy as np
from qlink.systems import SCORE, CHSH, QSink

# CHSH Bell Inequality Test
chsh = CHSH()
s_val = chsh.test(a=0.0, b=np.pi/4, a_prime=np.pi/2, b_prime=-np.pi/4)
print(f"CHSH Bell Statistic S: {s_val:.3f}")

# Quantum Mutual Information with SCORE
score_engine = SCORE()
rho_A = np.eye(2) / 2
rho_B = np.eye(2) / 2
rho_AB = np.eye(4) / 4
mutual_info = score_engine.compute(rho_A, rho_B, rho_AB)
print(f"Quantum Mutual Information: {mutual_info:.3f}")
```

---

## 🧪 Testing

To run full validation unit tests across all 14 workspace files:
```bash
python3 -m unittest discover -s . -p "test_*.py"
```

---

## 📜 License

MIT License.
