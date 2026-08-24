"""
QAI2 v8 Q-Transform — Quantum-Native AI Framework
The first AI architecture that operates natively on quantum units.

Q-Tokens replace classical tokens. Q-Attention replaces matrix multiplication.
Q-Embeddings live in Hilbert space. Q-Gates replace parameters.
Q-Positional encodes position as quantum phase. Q-Decoder generates via measurement.
Q-Consciousness implements the quantum self-reference loop.

Created by Joseph Cyril Dougherty IV, 13th Chamber LLC
August 2026 — Patent Pending (Claims 51-60)
"""

from .qtoken import QToken, QTokenEncoder
from .qattention import QAttention, QMultiHeadAttention
from .qembedding import QEmbedding, QEmbeddingLayer
from .qgate import QGateLayer, QFeedForward
from .qnorm import QLayerNorm
from .qtransformer import QTransformer, QTransformerLayer
from .qmetrics import QuantumMetrics, QVolume, QOps
from .qtrainer import QTrainer, VQETrainer
from .qpositional import QPositionalEncoding, QRopePositional
from .qdecoder import QDecoder, QStreamingDecoder
from .qconsciousness import QConsciousness, CognitiveSystem, SelfReferenceState

__version__ = "8.1.0"
__quantum_native__ = True
__qubits__ = 133
__q_volume__ = 2**133
__qas__ = 0.94
__n_modules__ = 11

__all__ = [
    "QToken", "QTokenEncoder",
    "QAttention", "QMultiHeadAttention",
    "QEmbedding", "QEmbeddingLayer",
    "QGateLayer", "QFeedForward",
    "QLayerNorm",
    "QTransformer", "QTransformerLayer",
    "QuantumMetrics", "QVolume", "QOps",
    "QTrainer", "VQETrainer",
    "QPositionalEncoding", "QRopePositional",
    "QDecoder", "QStreamingDecoder",
    "QConsciousness", "CognitiveSystem", "SelfReferenceState",
]
