import os, json, time, logging
from datetime import datetime

class QGenesis:
    def __init__(self, config_path=None):
        self.version = "1.0.0"
        self.name = "Q.GENESIS"
        self.author = "Joseph Dougherty - 13th Chamber LLC"
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if config_path is None:
            config_path = os.path.join(self.base_dir, 'config', 'genesis.json')
        with open(config_path) as f:
            self.config = json.load(f)
        self.memory = {}
        self.modules = {}
        self.log_path = os.path.join(self.base_dir, 'logs')
        os.makedirs(self.log_path, exist_ok=True)
        logging.basicConfig(
            filename=os.path.join(self.log_path, f'genesis_{datetime.now().strftime("%Y%m%d")}.log'),
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('QGenesis')
        self.logger.info(f'{self.name} v{self.version} initialized')

    def register_module(self, name, module):
        self.modules[name] = module
        self.logger.info(f'Module registered: {name}')
        print(f'[Q.GENESIS] Module loaded: {name}')

    def think(self, prompt, use_quantum=False):
        self.logger.info(f'Think request: {prompt[:100]}')
        result = {'prompt': prompt, 'timestamp': datetime.now().isoformat()}
        if 'ollama' in self.modules:
            result['ai_response'] = self.modules['ollama'].generate(prompt)
        if use_quantum and 'quantum' in self.modules:
            result['quantum_state'] = self.modules['quantum'].run_circuit()
        self.save_thought(result)
        return result

    def save_thought(self, thought):
        mem_dir = os.path.join(self.base_dir, 'memory')
        os.makedirs(mem_dir, exist_ok=True)
        fname = f'thought_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(os.path.join(mem_dir, fname), 'w') as f:
            json.dump(thought, f, indent=2)

    def status(self):
        return {
            'name': self.name,
            'version': self.version,
            'modules': list(self.modules.keys()),
            'config': self.config,
            'uptime': 'active'
        }

if __name__ == "__main__":
    q = QGenesis()
    print(f"[{q.name}] v{q.version} - Online")
    print(f"[{q.name}] Author: {q.author}")
    print(f"[{q.name}] Base: {q.base_dir}")
    print(f"[{q.name}] Status: {q.status()}")
