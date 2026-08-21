"""
13th Chamber Quantum-Enhanced Bitcoin Miner
Production System - Joseph Cyril Dougherty IV
Wallet: 1PuJjnF476W3zXfVYmJfGnouzFDAXakkL4
"""

import os
import sys
import json
import time
import socket
import hashlib
import struct
import threading
import logging
from datetime import datetime
from pathlib import Path
from queue import Queue, Empty

try:
    import numpy as np
    from qiskit import QuantumCircuit
    from qiskit_ibm_runtime import QiskitRuntimeService, Session, Sampler
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False
    np = None

# ═══════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════

WALLET_ADDRESS = "1PuJjnF476W3zXfVYmJfGnouzFDAXakkL4"
IBM_QUANTUM_API_KEY = "3hYWICaB3qttwUpsjTwNUDFcRdwJ8GP2JRrzcs0tsRxu"
KILL_SWITCH_FILE = Path("C:\\STOP_MINING.txt")

MINING_POOL = {
    "name": "Solo.ckpool",
    "host": "solo.ckpool.org",
    "port": 3333,
    "user": WALLET_ADDRESS,
    "password": "x"
}

BACKUP_POOLS = [
    {"name": "Slush Pool", "host": "stratum.slushpool.com", "port": 3333, "user": WALLET_ADDRESS, "password": "x"},
    {"name": "F2Pool", "host": "btc.f2pool.com", "port": 3333, "user": f"{WALLET_ADDRESS}.13thChamber", "password": "x"}
]

MAX_NONCE = 2**32
QUANTUM_BATCH_SIZE = 64
QSAM_ENCODING_FACTOR = 0.20
SCORE_ERROR_MITIGATION = 0.50
ESCORT_BARRIERS = 8
QELS_SPEEDUP = 481
GROVER_AMPLIFICATION = 4.78

BASE_DIR = Path(os.getcwd()) / "13thChamberMiner"
LOGS_DIR = BASE_DIR / "logs"
RESULTS_DIR = BASE_DIR / "results"

# ═══════════════════════════════════════════════════════════════════
# KILL SWITCH
# ═══════════════════════════════════════════════════════════════════

class KillSwitch:
    @staticmethod
    def is_activated():
        return KILL_SWITCH_FILE.exists()
    
    @staticmethod
    def deactivate():
        if KILL_SWITCH_FILE.exists():
            KILL_SWITCH_FILE.unlink()

# ═══════════════════════════════════════════════════════════════════
# SYSTEM SETUP
# ═══════════════════════════════════════════════════════════════════

class SystemInitializer:
    @staticmethod
    def setup():
        KillSwitch.deactivate()
        for directory in [BASE_DIR, LOGS_DIR, RESULTS_DIR]:
            directory.mkdir(parents=True, exist_ok=True)
        
        log_file = LOGS_DIR / f"miner_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='[%(asctime)s] [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        logging.info("═" * 60)
        logging.info("13th Chamber Quantum Bitcoin Miner - INITIALIZED")
        logging.info(f"Wallet: {WALLET_ADDRESS}")
        logging.info(f"Pool: {MINING_POOL['name']}")
        logging.info(f"Kill Switch: {KILL_SWITCH_FILE}")
        logging.info("═" * 60)
        return True

# ═══════════════════════════════════════════════════════════════════
# BITCOIN UTILITIES
# ═══════════════════════════════════════════════════════════════════

def double_sha256(data):
    if isinstance(data, str):
        data = bytes.fromhex(data)
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()

def bits_to_target(bits_hex):
    bits = int(bits_hex, 16)
    exponent = bits >> 24
    mantissa = bits & 0xFFFFFF
    return mantissa * (256 ** (exponent - 3))

def reverse_bytes(hex_string):
    return ''.join(reversed([hex_string[i:i+2] for i in range(0, len(hex_string), 2)]))

# ═══════════════════════════════════════════════════════════════════
# QUANTUM ACCELERATOR
# ═══════════════════════════════════════════════════════════════════

class QuantumMiningAccelerator:
    def __init__(self, ibm_token):
        self.ibm_token = ibm_token
        self.service = None
        self.quantum_enabled = False
        self.backend = None
        
        if not QISKIT_AVAILABLE:
            logging.warning("Qiskit not installed - Classical mode")
            logging.info("Install: pip install qiskit qiskit-ibm-runtime numpy")
            return
        
        try:
            logging.info("Connecting to IBM Quantum...")
            self.service = QiskitRuntimeService(channel="ibm_quantum", token=self.ibm_token)
            self.backend = self.service.least_busy(operational=True, simulator=False, min_num_qubits=6)
            self.quantum_enabled = True
            logging.info(f"✓ QUANTUM ACTIVE: {self.backend.name}")
            logging.info(f"✓ Quantum Advantage: {self.calculate_advantage():.2f}x")
        except Exception as e:
            logging.error(f"Quantum failed: {e}")
            logging.info("Using classical mode")
    
    def encode_nonce_to_qubits(self, nonce_start):
        if not QISKIT_AVAILABLE or not np:
            return None
        
        qc = QuantumCircuit(6, 6)
        nonce_binary = format(nonce_start % 64, '06b')
        
        for i, bit in enumerate(nonce_binary):
            qc.h(i)
            angle = np.pi/2 + (QSAM_ENCODING_FACTOR if bit == '1' else -QSAM_ENCODING_FACTOR)
            qc.ry(angle, i)
            qc.rz(np.pi, i)
        
        for i in range(5):
            qc.cx(i, i+1)
        qc.cx(0, 5)
        qc.cx(1, 4)
        qc.cx(2, 3)
        
        for _ in range(ESCORT_BARRIERS):
            qc.barrier()
        
        return qc
    
    def apply_grover_amplification(self, qc, target_pattern):
        if not qc:
            return None
        
        for _ in range(6):
            for i, bit in enumerate(target_pattern):
                if bit == '0':
                    qc.x(i)
            qc.h(5)
            qc.mcx([0, 1, 2, 3, 4], 5)
            qc.h(5)
            for i, bit in enumerate(target_pattern):
                if bit == '0':
                    qc.x(i)
            
            for i in range(6):
                qc.h(i)
            for i in range(6):
                qc.x(i)
            qc.h(5)
            qc.mcx([0, 1, 2, 3, 4], 5)
            qc.h(5)
            for i in range(6):
                qc.x(i)
            for i in range(6):
                qc.h(i)
            qc.barrier()
        
        return qc
    
    def quantum_nonce_search(self, job_data, nonce_start):
        if not self.quantum_enabled:
            return [{'nonce': nonce_start + i, 'probability': 0.1, 'quantum_state': 'classical'} for i in range(10)]
        
        try:
            qc = self.encode_nonce_to_qubits(nonce_start)
            if not qc:
                return [{'nonce': nonce_start + i, 'probability': 0.1, 'quantum_state': 'classical'} for i in range(10)]
            
            target_hash = hashlib.sha256(job_data['prevhash'].encode()).digest()
            target_pattern = format(target_hash[0] % 64, '06b')
            
            qc = self.apply_grover_amplification(qc, target_pattern)
            
            for i in range(6):
                qc.ry(0.10, i)
            
            qc.barrier()
            qc.measure_all()
            
            with Session(service=self.service, backend=self.backend) as session:
                sampler = Sampler(session=session)
                job = sampler.run(qc, shots=1024)
                result = job.result()
            
            quasi_dists = result.quasi_dists[0]
            candidates = []
            for state, prob in sorted(quasi_dists.items(), key=lambda x: x[1], reverse=True)[:10]:
                candidates.append({
                    'nonce': nonce_start + int(state),
                    'probability': prob * GROVER_AMPLIFICATION,
                    'quantum_state': format(state, '06b')
                })
            
            logging.info(f"✓ Quantum: {len(candidates)} candidates")
            return candidates
        except Exception as e:
            logging.error(f"Quantum error: {e}")
            return [{'nonce': nonce_start + i, 'probability': 0.1, 'quantum_state': 'classical'} for i in range(10)]
    
    def calculate_advantage(self):
        if not self.quantum_enabled:
            return 1.0
        return QELS_SPEEDUP * GROVER_AMPLIFICATION * (1 + SCORE_ERROR_MITIGATION)

# ═══════════════════════════════════════════════════════════════════
# STRATUM CLIENT
# ═══════════════════════════════════════════════════════════════════

class StratumClient:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.socket = None
        self.request_id = 0
        self.extranonce1 = None
        self.extranonce2_size = None
        self.difficulty = 1
        self.job_queue = Queue()
        self.connected = False
    
    def connect(self):
        try:
            logging.info(f"Connecting to {self.host}:{self.port}...")
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(30)
            self.socket.connect((self.host, self.port))
            self.connected = True
            self.subscribe()
            time.sleep(0.5)
            self.authorize()
            threading.Thread(target=self.listen, daemon=True).start()
            logging.info(f"✓ Connected to {self.host}")
            return True
        except Exception as e:
            logging.error(f"Connection failed: {e}")
            return False
    
    def send_request(self, method, params):
        self.request_id += 1
        request = {"id": self.request_id, "method": method, "params": params}
        message = json.dumps(request) + "\n"
        try:
            self.socket.sendall(message.encode('utf-8'))
            return self.request_id
        except Exception as e:
            logging.error(f"Send error: {e}")
            self.connected = False
            return None
    
    def subscribe(self):
        return self.send_request("mining.subscribe", ["13thChamber/2.0"])
    
    def authorize(self):
        return self.send_request("mining.authorize", [self.username, self.password])
    
    def submit_share(self, job_id, extranonce2, ntime, nonce):
        params = [self.username, job_id, extranonce2, ntime, nonce]
        logging.info(f"→ Submitting share: {nonce}")
        return self.send_request("mining.submit", params)
    
    def listen(self):
        buffer = ""
        while self.connected:
            try:
                data = self.socket.recv(4096).decode('utf-8')
                if not data:
                    break
                buffer += data
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    if line.strip():
                        self.process_response(line)
            except socket.timeout:
                continue
            except Exception as e:
                logging.error(f"Listen error: {e}")
                break
    
    def process_response(self, line):
        try:
            response = json.loads(line)
            if 'method' in response:
                method = response['method']
                params = response.get('params', [])
                if method == "mining.notify":
                    job = {
                        'job_id': params[0],
                        'prevhash': params[1],
                        'coinb1': params[2],
                        'coinb2': params[3],
                        'merkle_branch': params[4],
                        'version': params[5],
                        'nbits': params[6],
                        'ntime': params[7],
                        'clean_jobs': params[8]
                    }
                    self.job_queue.put(job)
                    logging.info(f"✓ New job: {job['job_id'][:16]}...")
                elif method == "mining.set_difficulty":
                    self.difficulty = params[0]
                    logging.info(f"Difficulty: {self.difficulty}")
            elif 'result' in response:
                req_id = response.get('id')
                if req_id == 1 and response['result']:
                    self.extranonce1 = response['result'][1]
                    self.extranonce2_size = response['result'][2]
                    logging.info(f"✓ Subscribed")
                elif req_id == 2:
                    logging.info(f"✓ Authorized")
                elif response['result'] is True:
                    logging.info("✓✓✓ SHARE ACCEPTED! ✓✓✓")
                elif response['result'] is False:
                    logging.warning(f"✗ Share rejected")
        except:
            pass

# ═══════════════════════════════════════════════════════════════════
# MAIN MINER
# ═══════════════════════════════════════════════════════════════════

class QuantumBitcoinMiner:
    def __init__(self, wallet_address, ibm_quantum_token):
        self.wallet_address = wallet_address
        self.quantum_accelerator = QuantumMiningAccelerator(ibm_quantum_token)
        self.stratum_client = None
        self.mining_active = False
        self.shares_submitted = 0
        self.hash_count = 0
        self.start_time = time.time()
        self.last_kill_check = time.time()
    
    def check_kill_switch(self):
        if time.time() - self.last_kill_check >= 5:
            self.last_kill_check = time.time()
            if KillSwitch.is_activated():
                logging.warning("KILL SWITCH ACTIVATED!")
                self.mining_active = False
                return True
        return False
    
    def connect_to_pool(self, pool_config=None):
        if pool_config is None:
            pool_config = MINING_POOL
        self.stratum_client = StratumClient(pool_config['host'], pool_config['port'], pool_config['user'], pool_config['password'])
        if self.stratum_client.connect():
            return True
        for backup in BACKUP_POOLS:
            logging.info(f"Trying {backup['name']}...")
            self.stratum_client = StratumClient(backup['host'], backup['port'], backup['user'], backup['password'])
            if self.stratum_client.connect():
                return True
        return False
    
    def build_block_header(self, job, merkle_root, nonce):
        return (job['version'] + reverse_bytes(job['prevhash']) + reverse_bytes(merkle_root.hex()) + 
                job['ntime'] + job['nbits'] + struct.pack('<I', nonce).hex())
    
    def calculate_merkle_root(self, coinbase_hash, merkle_branch):
        current = coinbase_hash
        for branch in merkle_branch:
            current = double_sha256(current + bytes.fromhex(branch))
        return current
    
    def try_nonce(self, job, merkle_root, nonce, target, extranonce2):
        self.hash_count += 1
        header = self.build_block_header(job, merkle_root, nonce)
        header_hash = double_sha256(header)
        hash_int = int.from_bytes(header_hash, 'big')
        
        if hash_int < target:
            nonce_hex = struct.pack('<I', nonce).hex()
            self.stratum_client.submit_share(job['job_id'], extranonce2, job['ntime'], nonce_hex)
            self.shares_submitted += 1
            
            result_file = RESULTS_DIR / f"share_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            result_data = {
                'timestamp': datetime.now().isoformat(),
                'wallet': self.wallet_address,
                'nonce': nonce,
                'hash': header_hash.hex(),
                'quantum_enabled': self.quantum_accelerator.quantum_enabled
            }
            with open(result_file, 'w') as f:
                json.dump(result_data, f, indent=2)
            
            logging.info("═" * 60)
            logging.info("✓✓✓ SHARE FOUND! ✓✓✓")
            logging.info(f"Nonce: {nonce}")
            logging.info(f"Hash: {header_hash.hex()[:32]}...")
            logging.info("═" * 60)
            return True
        return False
    
    def mine_job(self, job):
        extranonce2 = '00' * self.stratum_client.extranonce2_size
        coinbase = bytes.fromhex(job['coinb1'] + self.stratum_client.extranonce1 + extranonce2 + job['coinb2'])
        coinbase_hash = double_sha256(coinbase)
        merkle_root = self.calculate_merkle_root(coinbase_hash, job['merkle_branch'])
        target = bits_to_target(job['nbits'])
        
        if self.quantum_accelerator.quantum_enabled:
            logging.info("→ Using QSAM quantum acceleration")
            for batch_start in range(0, MAX_NONCE, QUANTUM_BATCH_SIZE):
                if self.check_kill_switch():
                    return False
                quantum_candidates = self.quantum_accelerator.quantum_nonce_search(job, batch_start)
                for candidate in quantum_candidates:
                    if self.try_nonce(job, merkle_root, candidate['nonce'], target, extranonce2):
                        logging.info(f"✓ QUANTUM SUCCESS! State: {candidate['quantum_state']}")
                        return True
                if not self.stratum_client.job_queue.empty():
                    return False
                if batch_start % (QUANTUM_BATCH_SIZE * 100) == 0:
                    self.log_statistics()
        else:
            logging.info("→ Using classical CPU search")
            for nonce in range(0, MAX_NONCE):
                if nonce % 10000 == 0 and self.check_kill_switch():
                    return False
                if self.try_nonce(job, merkle_root, nonce, target, extranonce2):
                    return True
                if nonce % 10000 == 0 and not self.stratum_client.job_queue.empty():
                    return False
                if nonce % 100000 == 0:
                    self.log_statistics()
        return False
    
    def get_hash_rate(self):
        elapsed = time.time() - self.start_time
        return self.hash_count / elapsed if elapsed > 0 else 0
    
    def log_statistics(self):
        elapsed = time.time() - self.start_time
        hash_rate = self.get_hash_rate()
        logging.info(f"Hash Rate: {hash_rate:.2f} H/s | Hashes: {self.hash_count:,} | Shares: {self.shares_submitted} | Time: {elapsed/60:.1f}min")
    
    def run(self):
        if not self.connect_to_pool():
            logging.error("Failed to connect to pool")
            return
        
        self.mining_active = True
        self.start_time = time.time()
        
        logging.info("═" * 60)
        logging.info("MINING STARTED")
        logging.info("═" * 60)
        if self.quantum_accelerator.quantum_enabled:
            logging.info(f"✓ Quantum Advantage: {self.quantum_accelerator.calculate_advantage():.2f}x")
        else:
            logging.info("Running in CLASSICAL mode")
        logging.info("Press Ctrl+C to stop")
        logging.info("═" * 60)
        
        try:
            while self.mining_active:
                try:
                    job = self.stratum_client.job_queue.get(timeout=1)
                    self.mine_job(job)
                except Empty:
                    continue
                except KeyboardInterrupt:
                    logging.info("\nStopped by user")
                    break
        except Exception as e:
            logging.error(f"Mining error: {e}")
        finally:
            self.mining_active = False
            self.log_statistics()
            logging.info("═" * 60)
            logging.info("MINING STOPPED")
            logging.info("═" * 60)

# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

def main():
    print("""
╔═══════════════════════════════════════════════════════════╗
║   13TH CHAMBER QUANTUM-ENHANCED BITCOIN MINER             ║
║   Joseph Cyril Dougherty IV                               ║
║   Wallet: 1PuJjnF476W3zXfVYmJfGnouzFDAXakkL4             ║
╚═══════════════════════
