#!/usr/bin/env python3
import os, sys, json, time, signal
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

def main():
    print("=" * 60)
    print("  Q.GENESIS v1.0.0 - Quantum AI System")
    print("  Created by Joseph Dougherty - 13th Chamber LLC")
    print("=" * 60)
    print(f"  Base Directory: {BASE_DIR}")
    print(f"  Started: {datetime.now().isoformat()}")
    print("=" * 60)

    # Load Core
    from core.q_genesis_core import QGenesis
    genesis = QGenesis()
    print("[BOOT] Core loaded")

    # Load Quantum Engine
    try:
        from quantum.quantum_engine import QuantumEngine
        qe = QuantumEngine()
        genesis.register_module('quantum', qe)
    except Exception as e:
        print(f"[BOOT] Quantum engine error: {e}")

    # Load Ollama Bridge
    try:
        from ollama.ollama_bridge import OllamaBridge
        ob = OllamaBridge()
        genesis.register_module('ollama', ob)
    except Exception as e:
        print(f"[BOOT] Ollama bridge error: {e}")

    # Load Memory Manager
    try:
        from memory.memory_manager import MemoryManager
        mm = MemoryManager()
        genesis.register_module('memory', mm)
    except Exception as e:
        print(f"[BOOT] Memory manager error: {e}")

    # Load Knowledge Base
    try:
        from memory.knowledge_base import KnowledgeBase
        kb = KnowledgeBase()
        genesis.register_module('knowledge', kb)
    except Exception as e:
        print(f"[BOOT] Knowledge base error: {e}")

    # Load Voice Engine
    try:
        from voice.voice_engine import VoiceEngine
        ve = VoiceEngine("Joseph")
        genesis.register_module('voice', ve)
    except Exception as e:
        print(f"[BOOT] Voice engine error: {e}")

    # Load Task Agent
    try:
        from core.task_agent import TaskAgent
        ta = TaskAgent()
        genesis.register_module('tasks', ta)
    except Exception as e:
        print(f"[BOOT] Task agent error: {e}")

    # Start Web Dashboard
    try:
        from web.web_interface import WebInterface
        wi = WebInterface(genesis=genesis, port=5000)
        wi.run_threaded()
    except Exception as e:
        print(f"[BOOT] Web interface error: {e}")

    # System Status
    status = genesis.status()
    print("\n" + "=" * 60)
    print("  Q.GENESIS SYSTEM STATUS")
    print("=" * 60)
    for key, val in status.items():
        print(f"  {key}: {val}")
    print("=" * 60)

    # Voice greeting
    if 'voice' in genesis.modules:
        genesis.modules['voice'].greet()

    # Log startup
    genesis.save_thought({
        'type': 'system_boot',
        'timestamp': datetime.now().isoformat(),
        'status': status,
        'message': 'Q.GENESIS fully initialized'
    })

    print("\n[Q.GENESIS] All systems online!")
    print("[Q.GENESIS] Dashboard: http://localhost:5000")
    print("[Q.GENESIS] Press Ctrl+C to shutdown\n")

    # Keep alive
    def shutdown(sig, frame):
        print("\n[Q.GENESIS] Shutting down gracefully...")
        if 'voice' in genesis.modules:
            genesis.modules['voice'].speak("Q Genesis shutting down. Goodbye Joseph.")
        genesis.save_thought({
            'type': 'system_shutdown',
            'timestamp': datetime.now().isoformat()
        })
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
