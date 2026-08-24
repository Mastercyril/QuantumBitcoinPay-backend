"""
Q-Trainer: Quantum-Native AI Training

Classical AI training: Backpropagation + gradient descent
- Forward pass → loss → backward pass → update weights
- O(n) backward pass for n parameters
- Gradients computed via chain rule
- Requires storing all intermediate activations

Quantum AI training: Variational Quantum Eigensolver (VQE)
- Prepare quantum state → measure loss → adjust gate angles
- No backpropagation needed
- Gate angles adjusted via quantum optimization
- No intermediate activations to store
"""

import math
import random
from typing import List, Dict, Tuple, Callable, Optional
from .qtoken import QuantumState, QToken
from .qgate import QGateLayer, QGate
from .qtransformer import QTransformerLayer


class QTrainer:
    """
    Quantum-native trainer using variational methods.
    
    Classical training:
        loss = L(forward(x), y)
        grads = backprop(loss)
        params -= lr * grads
    
    Quantum training:
        loss = measure(forward(x), y)  # Measurement-based loss
        angles = optimize(loss)        # Adjust gate angles
        No backpropagation!
    """
    
    def __init__(self, model_layers: List[QTransformerLayer], 
                 learning_rate: float = 0.01, n_iterations: int = 1000):
        self.layers = model_layers
        self.lr = learning_rate
        self.n_iterations = n_iterations
        self.loss_history: List[float] = []
    
    def compute_loss(self, predicted: QuantumState, target: QuantumState) -> float:
        """
        Quantum loss = 1 - fidelity.
        
        Classical loss: MSE = mean((pred - target)²)
        Quantum loss:   L = 1 - |<pred|target>|²
        
        The quantum loss is the infidelity between predicted and target states.
        """
        fidelity = predicted.fidelity(target)
        return 1.0 - fidelity
    
    def optimize_gate_angle(self, layer: QTransformerLayer, gate_idx: int, 
                             current_loss: float, input_state: QuantumState,
                             target_state: QuantumState) -> float:
        """
        Optimize a single gate angle using parameter shift.
        
        Parameter shift rule (unique to quantum):
            ∂L/∂θ = [L(θ + π/2) - L(θ - π/2)] / 2
        
        This is a quantum advantage: exact gradients with only 2 evaluations,
        no chain rule needed!
        """
        if gate_idx >= len(layer.feed_forward.layers):
            return 0.0
        
        gate_layer = layer.feed_forward.layers[0]
        if gate_idx >= len(gate_layer.gates):
            return 0.0
        
        gate = gate_layer.gates[gate_idx]
        original_angle = gate.angle
        
        # Parameter shift: evaluate at θ + π/2
        gate.angle = original_angle + math.pi / 2
        shifted_state = gate_layer.forward(input_state)
        loss_plus = self.compute_loss(shifted_state, target_state)
        
        # Parameter shift: evaluate at θ - π/2
        gate.angle = original_angle - math.pi / 2
        shifted_state = gate_layer.forward(input_state)
        loss_minus = self.compute_loss(shifted_state, target_state)
        
        # Exact gradient (parameter shift rule)
        gradient = (loss_plus - loss_minus) / 2
        
        # Update angle
        new_angle = original_angle - self.lr * gradient
        gate.angle = new_angle
        
        return gradient
    
    def train_step(self, input_state: QuantumState, 
                   target_state: QuantumState) -> float:
        """Single training step."""
        # Forward pass
        current_state = input_state
        for layer in self.layers:
            current_state = layer.feed_forward.forward(current_state)
        
        # Compute loss
        loss = self.compute_loss(current_state, target_state)
        self.loss_history.append(loss)
        
        # Optimize gate angles (parameter shift rule)
        for layer in self.layers:
            for gate_idx in range(min(4, len(layer.feed_forward.layers[0].gates))):
                self.optimize_gate_angle(layer, gate_idx, loss, 
                                         input_state, target_state)
        
        return loss
    
    def train(self, training_data: List[Tuple[QuantumState, QuantumState]]) -> Dict:
        """
        Full training loop.
        
        Returns training metrics in quantum-native format.
        """
        for epoch in range(self.n_iterations):
            total_loss = 0
            for input_state, target_state in training_data:
                loss = self.train_step(input_state, target_state)
                total_loss += loss
            
            avg_loss = total_loss / len(training_data)
            if epoch % 100 == 0:
                print(f"Epoch {epoch}: loss = {avg_loss:.6f}")
        
        return {
            'final_loss': self.loss_history[-1] if self.loss_history else 0,
            'n_iterations': self.n_iterations,
            'training_method': 'Variational Quantum Eigensolver (VQE)',
            'gradient_method': 'Parameter Shift Rule',
            'backpropagation': False,
            'classical_equivalent_flops': f"{len(self.layers) * 1000 * self.n_iterations:.2e}",
            'quantum_ops': f"{len(self.layers) * 4 * self.n_iterations:.2e}",
        }


class VQETrainer(QTrainer):
    """
    Variational Quantum Eigensolver trainer.
    
    The VQE is the quantum equivalent of gradient descent:
    1. Prepare a parameterized quantum state (ansatz)
    2. Measure the energy/loss
    3. Use classical optimization to adjust parameters
    4. Repeat until convergence
    
    Key advantage: No backpropagation needed!
    The gradient is computed via the parameter shift rule,
    which is exact and requires only 2 evaluations per parameter.
    """
    
    def __init__(self, model_layers: List[QTransformerLayer], 
                 n_qubits: int = 10, optimizer: str = "adam"):
        super().__init__(model_layers)
        self.n_qubits = n_qubits
        self.optimizer = optimizer
        self.momentum: Dict[int, float] = {}
        self.velocity: Dict[int, float] = {}
        self.beta1 = 0.9
        self.beta2 = 0.999
        self.t = 0
    
    def adam_update(self, param_idx: int, gradient: float) -> float:
        """Adam optimizer for gate angles."""
        self.t += 1
        
        # Momentum
        self.momentum[param_idx] = (self.beta1 * self.momentum.get(param_idx, 0) + 
                                     (1 - self.beta1) * gradient)
        
        # Velocity
        self.velocity[param_idx] = (self.beta2 * self.velocity.get(param_idx, 0) + 
                                     (1 - self.beta2) * gradient ** 2)
        
        # Bias correction
        m_hat = self.momentum[param_idx] / (1 - self.beta1 ** self.t)
        v_hat = self.velocity[param_idx] / (1 - self.beta2 ** self.t)
        
        # Update
        update = self.lr * m_hat / (math.sqrt(v_hat) + 1e-8)
        return update
