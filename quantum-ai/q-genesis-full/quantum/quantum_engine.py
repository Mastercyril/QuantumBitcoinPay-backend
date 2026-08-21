import json, os, random, math
from datetime import datetime

class QuantumEngine:
    def __init__(self, config_path=None):
        self.name = "QuantumEngine"
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if config_path is None:
            config_path = os.path.join(base_dir, 'config', 'quantum.json')
        if os.path.exists(config_path):
            with open(config_path) as f:
                self.config = json.load(f)
        else:
            self.config = {'backend':'simulator','shots':1024,'optimization_level':3}
        self.shots = self.config.get('shots', 1024)
        self.backend = self.config.get('backend', 'simulator')
        self.qubit_count = 4
        self.circuit_history = []

    def hadamard_sim(self, qubit_state=0):
        if qubit_state == 0:
            return (1/math.sqrt(2), 1/math.sqrt(2))
        return (1/math.sqrt(2), -1/math.sqrt(2))

    def measure(self, amplitudes):
        prob_0 = abs(amplitudes[0])**2
        return 0 if random.random() < prob_0 else 1

    def run_circuit(self, num_qubits=None):
        n = num_qubits or self.qubit_count
        results = {'0'*n: 0}
        for _ in range(self.shots):
            bits = ''
            for q in range(n):
                amp = self.hadamard_sim(0)
                bits += str(self.measure(amp))
            results[bits] = results.get(bits, 0) + 1
        record = {'timestamp': datetime.now().isoformat(), 'qubits': n, 'shots': self.shots, 'backend': self.backend, 'counts': dict(sorted(results.items(), key=lambda x: -x[1])[:10])}
        self.circuit_history.append(record)
        return record

    def entangle_sim(self):
        outcomes = {'00':0, '11':0}
        for _ in range(self.shots):
            if random.random() < 0.5:
                outcomes['00'] += 1
            else:
                outcomes['11'] += 1
        return {'type':'bell_state','counts':outcomes,'correlation': abs(outcomes['00']-outcomes['11'])/self.shots}

    def quantum_random(self, bits=256):
        return ''.join([str(random.randint(0,1)) for _ in range(bits)])

    def status(self):
        return {'engine':self.name,'backend':self.backend,'shots':self.shots,'circuits_run':len(self.circuit_history)}

if __name__ == "__main__":
    qe = QuantumEngine()
    print(f"[QuantumEngine] Backend: {qe.backend}")
    r = qe.run_circuit(4)
    print(f"[QuantumEngine] Circuit result: {r}")
    e = qe.entangle_sim()
    print(f"[QuantumEngine] Entanglement: {e}")
    print(f"[QuantumEngine] Random 32-bit: {qe.quantum_random(32)}")
