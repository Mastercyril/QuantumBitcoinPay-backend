import os, json, hashlib, time
from datetime import datetime

class MemoryManager:
    def __init__(self, memory_dir=None):
        self.name = "MemoryManager"
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.memory_dir = memory_dir or os.path.join(base_dir, 'memory')
        self.index_file = os.path.join(self.memory_dir, 'memory_index.json')
        os.makedirs(self.memory_dir, exist_ok=True)
        self.index = self._load_index()

    def _load_index(self):
        if os.path.exists(self.index_file):
            with open(self.index_file) as f:
                return json.load(f)
        return {'memories': [], 'total': 0, 'created': datetime.now().isoformat()}

    def _save_index(self):
        with open(self.index_file, 'w') as f:
            json.dump(self.index, f, indent=2)

    def _hash(self, text):
        return hashlib.sha256(text.encode()).hexdigest()[:12]

    def store(self, content, category='general', tags=None, metadata=None):
        mem_id = self._hash(content + str(time.time()))
        memory = {
            'id': mem_id,
            'content': content,
            'category': category,
            'tags': tags or [],
            'metadata': metadata or {},
            'timestamp': datetime.now().isoformat(),
            'access_count': 0,
            'last_accessed': None
        }
        fname = f'mem_{mem_id}.json'
        with open(os.path.join(self.memory_dir, fname), 'w') as f:
            json.dump(memory, f, indent=2)
        self.index['memories'].append({'id': mem_id, 'category': category, 'tags': tags or [], 'file': fname, 'timestamp': memory['timestamp']})
        self.index['total'] = len(self.index['memories'])
        self._save_index()
        return mem_id

    def recall(self, mem_id):
        for entry in self.index['memories']:
            if entry['id'] == mem_id:
                fpath = os.path.join(self.memory_dir, entry['file'])
                if os.path.exists(fpath):
                    with open(fpath) as f:
                        mem = json.load(f)
                    mem['access_count'] += 1
                    mem['last_accessed'] = datetime.now().isoformat()
                    with open(fpath, 'w') as f:
                        json.dump(mem, f, indent=2)
                    return mem
        return None

    def search(self, query, category=None):
        results = []
        query_lower = query.lower()
        for entry in self.index['memories']:
            if category and entry['category'] != category:
                continue
            fpath = os.path.join(self.memory_dir, entry['file'])
            if os.path.exists(fpath):
                with open(fpath) as f:
                    mem = json.load(f)
                if query_lower in mem['content'].lower() or query_lower in ' '.join(mem.get('tags', [])).lower():
                    results.append(mem)
        return results

    def list_categories(self):
        cats = {}
        for entry in self.index['memories']:
            c = entry['category']
            cats[c] = cats.get(c, 0) + 1
        return cats

    def delete(self, mem_id):
        for i, entry in enumerate(self.index['memories']):
            if entry['id'] == mem_id:
                fpath = os.path.join(self.memory_dir, entry['file'])
                if os.path.exists(fpath):
                    os.remove(fpath)
                self.index['memories'].pop(i)
                self.index['total'] = len(self.index['memories'])
                self._save_index()
                return True
        return False

    def export_all(self, export_path):
        all_mems = []
        for entry in self.index['memories']:
            fpath = os.path.join(self.memory_dir, entry['file'])
            if os.path.exists(fpath):
                with open(fpath) as f:
                    all_mems.append(json.load(f))
        with open(export_path, 'w') as f:
            json.dump(all_mems, f, indent=2)
        return len(all_mems)

    def status(self):
        return {'engine': self.name, 'total_memories': self.index['total'], 'categories': self.list_categories(), 'memory_dir': self.memory_dir}

if __name__ == "__main__":
    mm = MemoryManager()
    id1 = mm.store("Quantum entanglement enables instant correlation between particles", category="quantum", tags=["physics","entanglement"])
    id2 = mm.store("Ollama runs local LLMs for private AI inference", category="ai", tags=["ollama","llm"])
    id3 = mm.store("Bitcoin uses SHA-256 proof of work consensus", category="crypto", tags=["bitcoin","mining"])
    print(f"[MemoryManager] Stored 3 memories")
    r = mm.search("quantum")
    print(f"[MemoryManager] Search 'quantum': {len(r)} results")
    print(f"[MemoryManager] Categories: {mm.list_categories()}")
    print(f"[MemoryManager] Status: {mm.status()}")
