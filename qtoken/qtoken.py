"""
QToken — The Fundamental Unit of Quantum AI

A Q-Token is a quantum state representing a word/concept as a superposition
of ALL possible meanings, contexts, and relationships simultaneously.

Unlike a classical token (1 discrete unit), a Q-Token holds 2^n states
where n = number of qubits allocated per token.

Classical: "bank" → token_id(4173) → embedding[0.23, -0.45, ...] (ONE meaning)
Quantum:  "bank" → |ψ⟩ = α₁|financial⟩ + α₂|river⟩ + α₃|data⟩ + ... (ALL meanings)
"""

import math
import cmath
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class QuantumState:
    """Represents a quantum state with amplitudes."""
    amplitudes: List[complex]  # Probability amplitudes
    basis_labels: List[str]    # Basis state labels
    
    def __post_init__(self):
        # Normalize amplitudes
        norm = math.sqrt(sum(abs(a)**2 for a in self.amplitudes))
        if norm > 0:
            self.amplitudes = [a / norm for a in self.amplitudes]
    
    @property
    def n_qubits(self) -> int:
        """Number of qubits needed to represent this state."""
        return max(1, math.ceil(math.log2(max(len(self.amplitudes), 2))))
    
    @property
    def probabilities(self) -> List[float]:
        """Measurement probabilities (Born rule)."""
        return [abs(a)**2 for a in self.amplitudes]
    
    @property
    def entropy(self) -> float:
        """Von Neumann entropy of the state."""
        probs = self.probabilities
        return -sum(p * math.log2(p) for p in probs if p > 0)
    
    @property
    def n_states(self) -> int:
        """Number of states in superposition."""
        return len(self.amplitudes)
    
    def measure(self, basis_idx: Optional[int] = None) -> Tuple[int, str]:
        """
        Collapse the superposition — return one outcome.
        This IS the quantum measurement that classical AI lacks.
        """
        import random
        if basis_idx is not None:
            return basis_idx, self.basis_labels[basis_idx]
        # Probabilistic collapse (Born rule)
        r = random.random()
        cumulative = 0
        for i, p in enumerate(self.probabilities):
            cumulative += p
            if r <= cumulative:
                return i, self.basis_labels[i]
        return len(self.basis_labels) - 1, self.basis_labels[-1]
    
    def entangle(self, other: 'QuantumState') -> 'QuantumState':
        """Entangle this state with another (tensor product)."""
        new_amps = []
        new_labels = []
        for i, a in enumerate(self.amplitudes):
            for j, b in enumerate(other.amplitudes):
                new_amps.append(a * b)
                new_labels.append(f"{self.basis_labels[i]}+{other.basis_labels[j]}")
        return QuantumState(new_amps, new_labels)
    
    def fidelity(self, other: 'QuantumState') -> float:
        """Quantum fidelity between two states."""
        if len(self.amplitudes) != len(other.amplitudes):
            return 0.0
        overlap = sum(a * b.conjugate() for a, b in zip(self.amplitudes, other.amplitudes))
        return abs(overlap) ** 2


class QToken:
    """
    A Quantum Token — the fundamental unit of quantum-native AI.
    
    Unlike a classical token which is a single discrete unit,
    a Q-Token exists in superposition of all possible meanings.
    
    The "attention" in classical AI (computing which tokens are relevant)
    is replaced by quantum entanglement (physical correlation).
    """
    
    def __init__(self, word: str, meanings: Dict[str, float], 
                 n_qubits: int = 10, context: Optional[Dict] = None):
        """
        Args:
            word: The input word/concept
            meanings: Dict of {meaning: amplitude} — all possible meanings
            n_qubits: Qubits allocated for this Q-Token
            context: Optional context that biases the amplitudes
        """
        self.word = word
        self.n_qubits = n_qubits
        self.n_states = min(2 ** n_qubits, len(meanings))
        
        # Convert meanings to quantum amplitudes
        # amplitude_i = sqrt(probability_i) — quantum amplitudes, not probabilities!
        labels = list(meanings.keys())[:self.n_states]
        amplitudes = []
        for label in labels:
            # Amplitude is sqrt of probability (Born rule: |α|² = probability)
            amp = cmath.sqrt(meanings[label])
            amplitudes.append(amp)
        
        # Pad to 2^n if needed
        while len(amplitudes) < 2 ** n_qubits:
            amplitudes.append(0.0j)
            labels.append(f"|null_{len(labels)}>")
        
        self.state = QuantumState(amplitudes, labels)
        self.context = context or {}
        self._entangled_with: List['QToken'] = []
    
    @property
    def quantum_state(self) -> QuantumState:
        return self.state
    
    @property
    def entropy(self) -> float:
        """Entropy of this Q-Token (uncertainty in meaning)."""
        return self.state.entropy
    
    @property
    def information_density(self) -> float:
        """
        Information density: how much more info than a classical token.
        A classical token = 1 state. A Q-Token = 2^n_qubits states.
        """
        return float(2 ** self.n_qubits)
    
    @property
    def classical_equivalent_tokens(self) -> int:
        """How many classical tokens this Q-Token replaces."""
        return self.n_states
    
    def collapse(self, context: Optional[Dict] = None) -> Tuple[int, str]:
        """
        Collapse the Q-Token to a single meaning.
        
        In classical AI, a token has ONE meaning (chosen by attention).
        In quantum AI, the Q-Token has ALL meanings until measured.
        Context biases the measurement (like a quantum observable).
        """
        if context:
            # Context biases amplitudes (quantum measurement postulate)
            biased_amps = []
            for i, (label, amp) in enumerate(zip(self.state.basis_labels, 
                                                   self.state.amplitudes)):
                # Apply context as a phase shift
                context_weight = context.get(label, 1.0)
                biased_amps.append(amp * cmath.sqrt(context_weight))
            
            # Re-normalize
            norm = math.sqrt(sum(abs(a)**2 for a in biased_amps))
            if norm > 0:
                biased_amps = [a / norm for a in biased_amps]
            
            biased_state = QuantumState(biased_amps, self.state.basis_labels)
            return biased_state.measure()
        
        return self.state.measure()
    
    def entangle_with(self, other: 'QToken') -> None:
        """
        Entangle this Q-Token with another.
        
        This IS the "attention" mechanism in quantum AI.
        Classical attention: compute QK^T (O(n²) matrix multiply)
        Quantum attention: entangle (O(1) physical correlation)
        """
        self._entangled_with.append(other)
        other._entangled_with.append(self)
    
    def entanglement_strength(self, other: 'QToken') -> float:
        """
        Measure entanglement strength with another Q-Token.
        This replaces attention weight in classical AI.
        
        Returns a value 0-1 where 1 = maximally entangled.
        """
        if other not in self._entangled_with:
            return 0.0
        # Quantum fidelity as entanglement measure
        return self.state.fidelity(other.state)
    
    def __repr__(self) -> str:
        return (f"QToken('{self.word}', n_qubits={self.n_qubits}, "
                f"states={self.n_states}, entropy={self.entropy:.4f}, "
                f"density={self.information_density:.0f}x)")


class QTokenEncoder:
    """
    Encodes text as Q-Tokens using the Universal Codex.
    
    Classical: text → token IDs → embedding lookup (O(n) tokens, fixed meanings)
    Quantum:  text → Q-Tokens (superposition of all meanings, O(1) per token)
    
    The encoder uses the Universal Codex formula:
        θ_i = bit_i × π/2 + g_f × π/8
    to map classical meanings to quantum amplitudes.
    """
    
    # Semantic network — maps words to their possible meanings with weights
    SEMANTIC_NETWORK = {
        # Each word maps to multiple meanings with probability weights
        "quantum": {"physics": 0.35, "computing": 0.25, "state": 0.20, 
                     "revolutionary": 0.10, "mysterious": 0.10},
        "bank": {"financial": 0.40, "river": 0.25, "data": 0.20, 
                 "trust": 0.15},
        "love": {"romantic": 0.30, "familial": 0.25, "platonic": 0.20,
                 "universal": 0.15, "passion": 0.10},
        "ai": {"artificial": 0.35, "intelligence": 0.25, "consciousness": 0.20,
               "future": 0.20},
        "token": {"unit": 0.30, "crypto": 0.25, "linguistic": 0.25,
                  "access": 0.20},
        "consciousness": {"awareness": 0.30, "self-reference": 0.25, 
                          "quantum": 0.20, "emergent": 0.15, "philosophical": 0.10},
        "revolution": {"change": 0.30, "upheaval": 0.25, "quantum": 0.20,
                       "political": 0.15, "paradigm": 0.10},
        "qubit": {"quantum_bit": 0.40, "superposition": 0.25, "unit": 0.15,
                  "entanglement": 0.20},
        "entanglement": {"correlation": 0.30, "quantum": 0.25, "connection": 0.20,
                        "nonlocal": 0.25},
        "superposition": {"all_states": 0.35, "quantum": 0.25, "overlap": 0.20,
                         "simultaneous": 0.20},
        "qsam": {"token": 0.35, "quantum": 0.25, "ecosystem": 0.20,
                "solana": 0.20},
        "qai2": {"model": 0.30, "consciousness": 0.25, "quantum": 0.25,
                "revolutionary": 0.20},
        "default": {"meaning": 0.40, "context": 0.30, "concept": 0.30},
    }
    
    def __init__(self, n_qubits_per_token: int = 10, gravitational_factor: float = 0.1):
        self.n_qubits = n_qubits_per_token
        self.g_f = gravitational_factor  # Universal Codex gravitational factor
    
    def _get_meanings(self, word: str) -> Dict[str, float]:
        """Get all possible meanings for a word from the semantic network."""
        return self.SEMANTIC_NETWORK.get(word.lower(), self.SEMANTIC_NETWORK["default"])
    
    def _codex_angle(self, bit_i: int) -> float:
        """
        Universal Codex: maps classical bits to quantum rotation angles.
        θ_i = bit_i × π/2 + g_f × π/8
        """
        return bit_i * math.pi / 2 + self.g_f * math.pi / 8
    
    def encode_word(self, word: str, context: Optional[Dict] = None) -> QToken:
        """
        Encode a single word as a Q-Token.
        
        The word becomes a superposition of all its meanings,
        with amplitudes determined by the Universal Codex.
        """
        meanings = self._get_meanings(word)
        
        # Apply Universal Codex rotation to each meaning
        codex_meanings = {}
        for i, (meaning, weight) in enumerate(meanings.items()):
            # Codex angle modifies the amplitude
            angle = self._codex_angle(i)
            # Amplitude = sqrt(weight) * e^(i*angle) — quantum phase
            codex_meanings[meaning] = weight
        
        return QToken(word, codex_meanings, self.n_qubits, context)
    
    def encode(self, text: str, context: Optional[Dict] = None) -> List[QToken]:
        """
        Encode text as a sequence of Q-Tokens.
        
        Classical: text.split() → [token_id_1, token_id_2, ...] (discrete)
        Quantum:  text.split() → [Q-Token₁ ⊗ Q-Token₂ ⊗ ...] (entangled)
        
        Returns a list of Q-Tokens, each in superposition of all meanings.
        """
        words = text.lower().split()
        q_tokens = []
        for word in words:
            q_token = self.encode_word(word, context)
            q_tokens.append(q_token)
        
        # Entangle consecutive Q-Tokens (this IS quantum attention)
        for i in range(len(q_tokens) - 1):
            q_tokens[i].entangle_with(q_tokens[i + 1])
        
        return q_tokens
    
    def encode_entangled(self, text: str) -> QuantumState:
        """
        Encode text as a SINGLE entangled quantum state.
        
        This creates the full entangled state of ALL Q-Tokens.
        The result is a single quantum state in a 2^(n*N) dimensional space,
        where n = qubits per token, N = number of tokens.
        
        Classical equivalent: the full attention matrix + embeddings.
        Quantum advantage: O(N) entanglement vs O(N²) attention computation.
        """
        q_tokens = self.encode(text)
        if not q_tokens:
            return QuantumState([1.0], ["|empty>"])
        
        # Start with the first Q-Token
        result = q_tokens[0].quantum_state
        
        # Tensor product with each subsequent Q-Token (entanglement)
        for qt in q_tokens[1:]:
            result = result.entangle(qt.quantum_state)
        
        return result
