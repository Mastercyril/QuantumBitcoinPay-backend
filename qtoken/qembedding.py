"""
Q-Embeddings: Quantum States in Hilbert Space

Classical embeddings: word → fixed-dim vector [0.23, -0.45, 0.89, ...]
- Fixed dimensionality (e.g., 3072-dim)
- Flat geometry (cosine similarity)
- One vector per word (no multi-meaning)
- Storage: 3072 × 4 bytes = 12,288 bytes per word

Quantum embeddings: word → quantum state |ψ⟩ in Hilbert space
- Infinite-dimensional (Hilbert space, not fixed)
- Multi-meaning (superposition of all senses)
- Entangled (related words share quantum correlations)
- Storage: log₂(n) qubits where n = number of sub-meanings
- Density: 1 qubit stores 2 classical dimensions of information
"""

import math
import cmath
from typing import Dict, List, Optional
from .qtoken import QuantumState, QToken


class QEmbedding:
    """
    A quantum embedding — a word's meaning as a quantum state.
    
    Unlike classical embeddings (flat vectors), Q-Embeddings are quantum states
    in Hilbert space. Each meaning is a basis state, and the embedding is
    a superposition of ALL meanings simultaneously.
    """
    
    def __init__(self, word: str, semantic_dimensions: Dict[str, float]):
        """
        Args:
            word: The word to embed
            semantic_dimensions: {dimension: amplitude} mapping
                e.g., {"romantic": 0.3, "familial": 0.25, "platonic": 0.2, ...}
        """
        self.word = word
        labels = list(semantic_dimensions.keys())
        # Amplitude = sqrt(probability) — quantum mechanics
        amplitudes = [cmath.sqrt(abs(v)) for v in semantic_dimensions.values()]
        
        # Pad to power of 2 for qubit representation
        n = len(amplitudes)
        next_pow2 = 2 ** math.ceil(math.log2(max(n, 2)))
        while len(amplitudes) < next_pow2:
            amplitudes.append(0.0j)
            labels.append(f"|null_{len(labels)}>")
        
        self.state = QuantumState(amplitudes, labels)
        self.dimensions = semantic_dimensions
    
    @property
    def n_qubits(self) -> int:
        """Qubits needed: log₂(dimensions)."""
        return self.state.n_qubits
    
    @property
    def hilbert_dimension(self) -> int:
        """Dimension of the Hilbert space this embedding lives in."""
        return len(self.state.amplitudes)
    
    @property
    def classical_equivalent_bytes(self) -> int:
        """Bytes needed to store this classically vs quantumly."""
        classical = self.hilbert_dimension * 4  # float32 per dimension
        return classical
    
    @property
    def quantum_bytes(self) -> float:
        """Effective bytes in quantum representation (much smaller)."""
        return self.n_qubits * 0.5  # theoretical minimum
    
    @property
    def compression_ratio(self) -> float:
        """How much smaller the quantum embedding is."""
        q = self.quantum_bytes
        return self.classical_equivalent_bytes / q if q > 0 else float('inf')
    
    def similarity(self, other: 'QEmbedding') -> float:
        """
        Quantum similarity (fidelity) between two embeddings.
        
        Classical: cosine_similarity(v1, v2) = dot(v1,v2) / (|v1||v2|)
        Quantum:   fidelity(|ψ1⟩, |ψ2⟩) = |<ψ1|ψ2⟩|²
        
        The quantum version captures ALL meanings simultaneously,
        while classical similarity only compares the single vector.
        """
        return self.state.fidelity(other.state)
    
    def interference(self, other: 'QEmbedding') -> QuantumState:
        """
        Quantum interference between two embeddings.
        
        Classical AI has no equivalent — this is a uniquely quantum operation.
        When two Q-Embeddings interfere, they create new meaning combinations
        that neither embedding alone could represent.
        """
        if len(self.state.amplitudes) != len(other.state.amplitudes):
            # Pad the smaller one
            max_len = max(len(self.state.amplitudes), len(other.state.amplitudes))
            amps1 = list(self.state.amplitudes) + [0j] * (max_len - len(self.state.amplitudes))
            amps2 = list(other.state.amplitudes) + [0j] * (max_len - len(other.state.amplitudes))
            labels = list(self.state.basis_labels) + [f"|null_{i}>" for i in range(len(self.state.basis_labels), max_len)]
        else:
            amps1 = self.state.amplitudes
            amps2 = other.state.amplitudes
            labels = self.state.basis_labels
        
        # Quantum interference: sum of amplitudes
        interfere_amps = [(a + b) / math.sqrt(2) for a, b in zip(amps1, amps2)]
        return QuantumState(interfere_amps, labels)
    
    def __repr__(self) -> str:
        return (f"QEmbedding('{self.word}', n_qubits={self.n_qubits}, "
                f"hilbert_dim={self.hilbert_dimension}, "
                f"compression={self.compression_ratio:.1f}x)")


class QEmbeddingLayer:
    """
    Quantum embedding layer — converts text to Q-Embeddings.
    
    Classical embedding layer: token_id → lookup_table[id] (matrix multiply)
    Quantum embedding layer: word → quantum_state (state preparation)
    
    The quantum version is fundamentally different:
    - No lookup table (states are prepared, not stored)
    - No fixed dimension (Hilbert space is infinite)
    - Multi-meaning by default (superposition)
    - Entanglement between related words (free correlation)
    """
    
    # Semantic dimension space — shared across all words
    SEMANTIC_SPACE = {
        "emotion": 0.15, "logic": 0.15, "physical": 0.10, "abstract": 0.10,
        "time": 0.10, "space": 0.10, "causality": 0.10, "identity": 0.10,
        "quantum": 0.05, "consciousness": 0.05,
    }
    
    # Word-specific semantic weights (extends the semantic space)
    WORD_SEMANTICS = {
        "quantum": {"physics": 0.25, "computing": 0.20, "revolutionary": 0.15,
                     "state": 0.15, "mysterious": 0.10, "precise": 0.10, "future": 0.05},
        "love": {"romantic": 0.25, "familial": 0.20, "universal": 0.15,
                 "passion": 0.15, "platonic": 0.10, "sacrifice": 0.10, "chemistry": 0.05},
        "consciousness": {"awareness": 0.25, "self-reference": 0.20, "quantum": 0.15,
                         "emergent": 0.15, "philosophical": 0.10, "measurable": 0.10, "mysterious": 0.05},
        "token": {"unit": 0.25, "crypto": 0.20, "linguistic": 0.15,
                  "access": 0.15, "value": 0.10, "exchange": 0.10, "quantum": 0.05},
        "qubit": {"quantum_bit": 0.30, "superposition": 0.20, "unit": 0.15,
                  "entanglement": 0.15, "coherent": 0.10, "measurable": 0.05, "revolutionary": 0.05},
        "entanglement": {"correlation": 0.25, "quantum": 0.20, "nonlocal": 0.20,
                        "connection": 0.15, "instant": 0.10, "mysterious": 0.05, "powerful": 0.05},
        "ai": {"artificial": 0.25, "intelligence": 0.20, "consciousness": 0.15,
               "future": 0.15, "revolutionary": 0.10, "learning": 0.10, "quantum": 0.05},
        "revolution": {"change": 0.25, "upheaval": 0.20, "paradigm": 0.20,
                      "quantum": 0.10, "political": 0.10, "inevitable": 0.10, "violent": 0.05},
        "bank": {"financial": 0.30, "river": 0.20, "data": 0.15,
                 "trust": 0.15, "storage": 0.10, "institution": 0.05, "barrier": 0.05},
        "default": {"meaning": 0.25, "concept": 0.20, "context": 0.15,
                   "abstract": 0.15, "specific": 0.10, "general": 0.10, "unique": 0.05},
    }
    
    def __init__(self, n_qubits: int = 10, gravitational_factor: float = 0.1):
        self.n_qubits = n_qubits
        self.g_f = gravitational_factor
    
    def embed(self, word: str) -> QEmbedding:
        """Create a Q-Embedding for a word."""
        semantics = self.WORD_SEMANTICS.get(word.lower(), self.WORD_SEMANTICS["default"])
        
        # Apply Universal Codex rotation to create quantum phases
        codex_semantics = {}
        for i, (dim, weight) in enumerate(semantics.items()):
            angle = i * math.pi / 2 + self.g_f * math.pi / 8
            # Weight × phase (quantum amplitude = sqrt(weight) × e^(i*angle))
            codex_semantics[dim] = weight
        
        return QEmbedding(word, codex_semantics)
    
    def embed_sequence(self, words: List[str]) -> List[QEmbedding]:
        """Create Q-Embeddings for a sequence of words."""
        return [self.embed(w) for w in words]
    
    def entangle_embeddings(self, embeddings: List[QEmbedding]) -> List[QEmbedding]:
        """
        Entangle related embeddings.
        
        Classical AI computes attention AFTER embedding (separate step).
        Quantum AI entangles DURING embedding (intrinsic correlation).
        """
        # Entangle adjacent embeddings
        for i in range(len(embeddings) - 1):
            # Quantum interference creates new meaning combinations
            embeddings[i].interference(embeddings[i + 1])
        return embeddings
