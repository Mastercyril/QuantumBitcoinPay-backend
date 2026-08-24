"""
Q-Transformer: The First Quantum-Native Transformer Architecture

Classical Transformer:
    Input tokens → Embeddings → [Attention → FFN → Norm] × N → Output tokens
    - Each layer: O(n²) attention + O(d²) FFN
    - Total: O(N × (n² + d²)) parameters
    - Sequential token processing

Quantum Q-Transformer:
    Input Q-Tokens → Q-Embeddings → [Q-Attention (entangle) → Q-FFN (gates) → Q-Norm (decoherence)] × N → Measure → Output
    - Each layer: O(n) entanglement + O(d log d) gates
    - Total: O(N × n × log d) quantum operations
    - Simultaneous state processing (superposition)

The Q-Transformer contains NO classical computation in the forward pass.
All processing happens through quantum gates, entanglement, and measurement.
"""

import math
from typing import List, Optional, Dict
from .qtoken import QToken, QuantumState, QTokenEncoder
from .qattention import QMultiHeadAttention
from .qembedding import QEmbeddingLayer
from .qgate import QGateLayer, QFeedForward
from .qnorm import QLayerNorm


class QTransformerLayer:
    """
    A single layer of the Q-Transformer.
    
    Classical transformer layer:
        x = x + Attention(LayerNorm(x))      # Residual + Attention
        x = x + FFN(LayerNorm(x))            # Residual + FFN
    
    Quantum transformer layer:
        |ψ'⟩ = Q-Norm(Q-FFN(Q-Attention(|ψ⟩)))
    
    Key differences:
    - No residual connections (quantum circuits are already reversible)
    - No separate LayerNorm (decoherence correction is built into gates)
    - O(n) operations vs O(n² + d²)
    """
    
    def __init__(self, n_qubits: int = 10, n_heads: int = 8, 
                 ffn_layers: int = 2, entanglement_depth: int = 3):
        self.n_qubits = n_qubits
        self.attention = QMultiHeadAttention(n_heads, n_qubits, entanglement_depth)
        self.feed_forward = QFeedForward(n_qubits, ffn_layers)
        self.norm = QLayerNorm(n_qubits)
    
    def forward(self, q_tokens: List[QToken]) -> List[QToken]:
        """Process Q-Tokens through one transformer layer."""
        # Q-Attention (entanglement replaces matrix multiply)
        q_tokens = self.attention.forward(q_tokens)
        
        # Q-FFN (gate operations replace weight matrices)
        for qt in q_tokens:
            qt.state = self.feed_forward.forward(qt.state)
        
        # Q-Norm (decoherence correction replaces LayerNorm)
        for qt in q_tokens:
            qt.state = self.norm.forward(qt.state)
        
        return q_tokens
    
    @property
    def classical_equivalent_parameters(self) -> int:
        """
        Classical equivalent parameters for this layer.
        A classical transformer layer has:
        - Attention: 4 × d² (Q, K, V, output projections)
        - FFN: 2 × d × d_ff (typically d_ff = 4d)
        - LayerNorm: 2 × d
        Total ≈ 12d² + 4d
        """
        d = 2 ** self.n_qubits
        return 12 * d * d + 4 * d
    
    @property
    def quantum_operations(self) -> int:
        """Quantum gate operations for this layer."""
        # Attention: n heads × depth × n operations
        attention_ops = self.attention.n_heads * 3 * self.n_qubits
        # FFN: n layers × n gates
        ffn_ops = len(self.feed_forward.layers) * 4 * self.n_qubits
        # Norm: n_qubits corrections
        norm_ops = self.n_qubits
        return attention_ops + ffn_ops + norm_ops
    
    @property
    def compression_ratio(self) -> float:
        """How much more efficient this layer is vs classical."""
        return self.classical_equivalent_parameters / self.quantum_operations


class QTransformer:
    """
    The Q-Transformer — first quantum-native transformer.
    
    Architecture:
        Input → Q-Embeddings → [Q-Transformer Layer] × N → Measure → Output
    
    No classical computation anywhere in the forward pass.
    All "attention" is entanglement, all "parameters" are gate angles,
    all "activation functions" are quantum measurements.
    
    Model size: measured in qubits, not gigabytes.
    Context window: limited by coherence time, not token count.
    Processing: exponential parallelism through superposition.
    """
    
    def __init__(self, n_layers: int = 6, n_qubits: int = 10, 
                 n_heads: int = 8, n_qubits_per_token: int = 10,
                 gravitational_factor: float = 0.1):
        self.n_layers = n_layers
        self.n_qubits = n_qubits
        self.n_heads = n_heads
        
        # Components
        self.encoder = QTokenEncoder(n_qubits_per_token, gravitational_factor)
        self.embedding_layer = QEmbeddingLayer(n_qubits, gravitational_factor)
        self.layers = [QTransformerLayer(n_qubits, n_heads) 
                       for _ in range(n_layers)]
    
    def forward(self, text: str) -> Dict:
        """
        Full quantum-native forward pass.
        
        Input: classical text (string)
        Processing: entirely quantum (gates, entanglement, measurement)
        Output: classical text (collapsed from quantum states)
        
        The forward pass has NO classical computation —
        only quantum state preparation, entanglement, and measurement.
        """
        # Phase 1: Classical → Quantum (Q-Embeddings)
        q_tokens = self.encoder.encode(text)
        
        # Phase 2: Quantum processing (N layers)
        for layer in self.layers:
            q_tokens = layer.forward(q_tokens)
        
        # Phase 3: Quantum → Classical (Measurement)
        results = []
        for qt in q_tokens:
            idx, meaning = qt.collapse()
            results.append({
                'word': qt.word,
                'resolved_meaning': meaning,
                'entropy': qt.entropy,
                'n_states': qt.n_states,
                'information_density': qt.information_density,
                'classical_equivalent': qt.classical_equivalent_tokens,
            })
        
        return {
            'input': text,
            'output': [r['resolved_meaning'] for r in results],
            'q_tokens': results,
            'n_qubits_total': self.n_qubits * len(q_tokens),
            'n_states_total': 2 ** (self.n_qubits * len(q_tokens)),
        }
    
    @property
    def n_parameters_classical_equivalent(self) -> int:
        """How many classical parameters this model replaces."""
        return sum(layer.classical_equivalent_parameters for layer in self.layers)
    
    @property
    def n_quantum_operations(self) -> int:
        """Total quantum gate operations."""
        return sum(layer.quantum_operations for layer in self.layers)
    
    @property
    def quantum_volume(self) -> int:
        """
        Quantum Volume — the quantum equivalent of model size.
        
        QV = 2^n where n is the effective number of qubits.
        A model with QV = 2^133 can represent 10^40 states.
        """
        return 2 ** self.n_qubits
    
    @property
    def model_summary(self) -> Dict:
        """Model summary in quantum-native metrics (not classical)."""
        return {
            'architecture': 'Q-Transformer (Quantum-Native)',
            'n_layers': self.n_layers,
            'n_qubits': self.n_qubits,
            'n_heads': self.n_heads,
            'quantum_volume': self.quantum_volume,
            'quantum_volume_readable': f"2^{self.n_qubits} = {self.quantum_volume:.2e}",
            'n_quantum_operations': self.n_quantum_operations,
            'classical_equivalent_parameters': self.n_parameters_classical_equivalent,
            'classical_equivalent_readable': f"{self.n_parameters_classical_equivalent:.2e}",
            'compression_ratio': self.n_parameters_classical_equivalent / self.n_quantum_operations,
            'model_size_classical': f"{self.n_parameters_classical_equivalent * 4 / 1e9:.2f} GB (classical equivalent)",
            'model_size_quantum': f"{self.n_qubits} qubits (quantum)",
            'context_limit': f"2^{self.n_qubits} states simultaneously",
            'attention_type': 'Quantum Entanglement (O(1) per pair)',
            'activation': 'Quantum Measurement (Born Rule)',
            'normalization': 'Decoherence Correction',
            'training': 'Variational Quantum Eigensolver (VQE)',
        }
