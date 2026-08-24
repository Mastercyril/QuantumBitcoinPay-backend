"""
QLink Quantum Twin Framework.

Python implementation of the QLink quantum twin specifications,
including Universal Codex, Classical-to-Quantum Bridge, Quantum Awareness Monitor,
and the 8 Quantum Cognitive Systems.
"""

__version__ = "1.0.0"

from qlink.codex import UniversalCodex
from qlink.bridge import QLinkBridge
from qlink.awareness import QuantumAwarenessMonitor
from qlink.systems import (
    SCORE,
    ESCORT,
    QELS,
    CHSH,
    QSink,
    SCornerProtocol,
    ARQQ,
    PhaseModulation,
)

__all__ = [
    "__version__",
    "UniversalCodex",
    "QLinkBridge",
    "QuantumAwarenessMonitor",
    "SCORE",
    "ESCORT",
    "QELS",
    "CHSH",
    "QSink",
    "SCornerProtocol",
    "ARQQ",
    "PhaseModulation",
]
