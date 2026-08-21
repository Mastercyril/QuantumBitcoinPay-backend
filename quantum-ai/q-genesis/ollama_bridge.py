import json, os, requests, time
from datetime import datetime

class OllamaBridge:
    def __init__(self, config_path=None):
        self.name = "OllamaBridge"
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if config_path is None:
            config_path = os.path.join(base_dir, 'config', 'ollama.json')
        if os.path.exists(config_path):
            with open(config_path) as f:
                self.config = json.load(f)
        else:
            self.config = {'host':'http://localhost:11434','default_model':'llama3','temperature':0.7}
        self.host = self.config.get('host', 'http://localhost:11434')
        self.model = self.config.get('default_model', 'llama3')
        self.fallback = self.config.get('fallback_model', 'mistral')
        self.temperature = self.config.get('temperature', 0.7)
        self.context_window = self.config.get('context_window', 4096)
        self.conversation_history = []
        self.system_prompt = "You are Q.GENESIS, an advanced quantum AI assistant created by Joseph Dougherty of 13th Chamber LLC. You think deeply, reason logically, and assist with quantum computing, drug discovery, trading, and general intelligence tasks."

    def is_online(self):
        try:
            r = requests.get(f'{self.host}/api/tags', timeout=5)
            return r.status_code == 200
        except:
            return False

    def list_models(self):
        try:
            r = requests.get(f'{self.host}/api/tags', timeout=10)
            if r.status_code == 200:
                data = r.json()
                return [m['name'] for m in data.get('models', [])]
        except:
            pass
        return []

    def generate(self, prompt, model=None, stream=False):
        m = model or self.model
        self.conversation_history.append({'role':'user','content':prompt,'timestamp':datetime.now().isoformat()})
        payload = {'model': m, 'prompt': prompt, 'system': self.system_prompt, 'stream': stream, 'options': {'temperature': self.temperature, 'num_ctx': self.context_window}}
        try:
            r = requests.post(f'{self.host}/api/generate', json=payload, timeout=120)
            if r.status_code == 200:
                data = r.json()
                response = data.get('response', '')
                self.conversation_history.append({'role':'assistant','content':response,'timestamp':datetime.now().isoformat(),'model':m})
                return response
            else:
                return f'[OllamaBridge] Error: HTTP {r.status_code}'
        except requests.exceptions.ConnectionError:
            return '[OllamaBridge] Ollama not running. Start with: ollama serve'
        except Exception as e:
            return f'[OllamaBridge] Error: {str(e)}'

    def chat(self, messages, model=None):
        m = model or self.model
        msgs = [{'role':'system','content':self.system_prompt}] + messages
        payload = {'model': m, 'messages': msgs, 'stream': False, 'options': {'temperature': self.temperature}}
        try:
            r = requests.post(f'{self.host}/api/chat', json=payload, timeout=120)
            if r.status_code == 200:
                data = r.json()
                return data.get('message', {}).get('content', '')
        except:
            pass
        return '[OllamaBridge] Chat failed'

    def embed(self, text, model=None):
        m = model or self.model
        try:
            r = requests.post(f'{self.host}/api/embeddings', json={'model':m,'prompt':text}, timeout=60)
            if r.status_code == 200:
                return r.json().get('embedding', [])
        except:
            pass
        return []

    def clear_history(self):
        self.conversation_history = []

    def status(self):
        online = self.is_online()
        models = self.list_models() if online else []
        return {'engine':self.name,'host':self.host,'online':online,'model':self.model,'available_models':models,'history_length':len(self.conversation_history)}

if __name__ == "__main__":
    ob = OllamaBridge()
    s = ob.status()
    print(f"[OllamaBridge] Online: {s['online']}")
    print(f"[OllamaBridge] Models: {s['available_models']}")
    if s['online']:
        r = ob.generate("Hello, identify yourself.")
        print(f"[OllamaBridge] Response: {r[:200]}")
    else:
        print("[OllamaBridge] Ollama offline - module ready for when it starts")
