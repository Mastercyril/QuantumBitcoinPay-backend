import os, json, threading
from datetime import datetime
from flask import Flask, jsonify, request, render_template_string

HTML_TEMPLATE = """<!DOCTYPE html><html><head><title>Q.GENESIS Dashboard</title>
<style>*{margin:0;padding:0;box-sizing:border-box}body{background:#0a0a1a;color:#00ff88;font-family:'Courier New',monospace}
.header{background:linear-gradient(135deg,#1a0033,#0a0a2e);padding:20px;text-align:center;border-bottom:2px solid #7b2fff}
.header h1{font-size:2.5em;color:#7b2fff;text-shadow:0 0 20px #7b2fff}.header p{color:#888;margin-top:5px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(350px,1fr));gap:20px;padding:20px}
.card{background:#111;border:1px solid #333;border-radius:10px;padding:20px}.card h2{color:#7b2fff;margin-bottom:15px;border-bottom:1px solid #333;padding-bottom:10px}
.status-online{color:#00ff88}.status-offline{color:#ff4444}.metric{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1a1a1a}
.metric-label{color:#888}.metric-value{color:#00ff88;font-weight:bold}
.btn{background:#7b2fff;color:white;border:none;padding:10px 20px;border-radius:5px;cursor:pointer;margin:5px;font-family:inherit}
.btn:hover{background:#9b4fff}.terminal{background:#000;border:1px solid #333;border-radius:5px;padding:15px;max-height:300px;overflow-y:auto;font-size:0.9em}
.terminal-line{padding:2px 0}input[type=text]{background:#1a1a1a;border:1px solid #333;color:#00ff88;padding:10px;border-radius:5px;width:100%;font-family:inherit;margin:10px 0}
</style></head><body>
<div class="header"><h1>Q.GENESIS</h1><p>Quantum AI System Dashboard | Joseph Dougherty - 13th Chamber LLC</p></div>
<div class="grid">
<div class="card"><h2>System Status</h2><div id="status">Loading...</div></div>
<div class="card"><h2>AI Chat</h2><input type="text" id="chatInput" placeholder="Ask Q.GENESIS anything..." onkeypress="if(event.key==='Enter')sendChat()">
<div id="chatOutput" class="terminal"></div></div>
<div class="card"><h2>Quantum Engine</h2><button class="btn" onclick="runQuantum()">Run Circuit</button><button class="btn" onclick="runEntangle()">Entangle</button>
<div id="quantumOutput" class="terminal"></div></div>
<div class="card"><h2>Memory</h2><div id="memoryStatus">Loading...</div></div>
<div class="card"><h2>Voice Control</h2><button class="btn" onclick="voiceGreet()">Greet</button><button class="btn" onclick="voiceListen()">Listen</button>
<div id="voiceOutput" class="terminal"></div></div>
<div class="card"><h2>Knowledge Base</h2><div id="kbStatus">Loading...</div></div>
</div>
<script>
async function fetchStatus(){let r=await fetch('/api/status');let d=await r.json();document.getElementById('status').innerHTML=Object.entries(d).map(([k,v])=>'<div class="metric"><span class="metric-label">'+k+'</span><span class="metric-value">'+JSON.stringify(v)+'</span></div>').join('')}
async function sendChat(){let i=document.getElementById('chatInput');let r=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({prompt:i.value})});let d=await r.json();document.getElementById('chatOutput').innerHTML+='<div class="terminal-line">> '+i.value+'</div><div class="terminal-line" style="color:#7b2fff">'+d.response+'</div>';i.value=''}
async function runQuantum(){let r=await fetch('/api/quantum/run');let d=await r.json();document.getElementById('quantumOutput').innerHTML+='<div class="terminal-line">'+JSON.stringify(d)+'</div>'}
async function runEntangle(){let r=await fetch('/api/quantum/entangle');let d=await r.json();document.getElementById('quantumOutput').innerHTML+='<div class="terminal-line">'+JSON.stringify(d)+'</div>'}
async function voiceGreet(){await fetch('/api/voice/greet')}
async function voiceListen(){let r=await fetch('/api/voice/listen');let d=await r.json();document.getElementById('voiceOutput').innerHTML+='<div class="terminal-line">'+d.text+'</div>'}
fetchStatus();setInterval(fetchStatus,10000)
</script></body></html>"""

class WebInterface:
    def __init__(self, genesis=None, host='0.0.0.0', port=5000):
        self.app = Flask(__name__)
        self.genesis = genesis
        self.host = host
        self.port = port
        self._setup_routes()

    def _setup_routes(self):
        @self.app.route('/')
        def index():
            return render_template_string(HTML_TEMPLATE)

        @self.app.route('/api/status')
        def api_status():
            if self.genesis:
                return jsonify(self.genesis.status())
            return jsonify({'status':'running','modules':'standalone','version':'1.0.0'})

        @self.app.route('/api/chat', methods=['POST'])
        def api_chat():
            data = request.json
            prompt = data.get('prompt', '')
            if self.genesis and 'ollama' in self.genesis.modules:
                response = self.genesis.modules['ollama'].generate(prompt)
            else:
                response = f'Q.GENESIS received: {prompt} (Ollama not connected)'
            return jsonify({'response': response})

        @self.app.route('/api/quantum/run')
        def api_quantum_run():
            if self.genesis and 'quantum' in self.genesis.modules:
                return jsonify(self.genesis.modules['quantum'].run_circuit())
            return jsonify({'error':'Quantum engine not loaded'})

        @self.app.route('/api/quantum/entangle')
        def api_quantum_entangle():
            if self.genesis and 'quantum' in self.genesis.modules:
                return jsonify(self.genesis.modules['quantum'].entangle_sim())
            return jsonify({'error':'Quantum engine not loaded'})

        @self.app.route('/api/voice/greet')
        def api_voice_greet():
            if self.genesis and 'voice' in self.genesis.modules:
                msg = self.genesis.modules['voice'].greet()
                return jsonify({'message': msg})
            return jsonify({'message':'Voice not loaded'})

        @self.app.route('/api/voice/listen')
        def api_voice_listen():
            if self.genesis and 'voice' in self.genesis.modules:
                text = self.genesis.modules['voice'].listen()
                return jsonify({'text': text or 'No speech detected'})
            return jsonify({'text':'Voice not loaded'})

        @self.app.route('/api/memory/status')
        def api_memory():
            if self.genesis and 'memory' in self.genesis.modules:
                return jsonify(self.genesis.modules['memory'].status())
            return jsonify({'status':'not loaded'})

        @self.app.route('/api/knowledge/status')
        def api_kb():
            if self.genesis and 'knowledge' in self.genesis.modules:
                return jsonify(self.genesis.modules['knowledge'].status())
            return jsonify({'status':'not loaded'})

    def run(self, debug=False):
        print(f'[WebInterface] Starting dashboard at http://{self.host}:{self.port}')
        self.app.run(host=self.host, port=self.port, debug=debug, use_reloader=False)

    def run_threaded(self):
        t = threading.Thread(target=lambda: self.app.run(host=self.host, port=self.port, debug=False, use_reloader=False), daemon=True)
        t.start()
        print(f'[WebInterface] Dashboard running at http://localhost:{self.port}')
        return t

if __name__ == "__main__":
    wi = WebInterface()
    print("[WebInterface] Starting standalone dashboard...")
    wi.run(debug=True)
