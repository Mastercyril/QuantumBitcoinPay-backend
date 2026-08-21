import os, json, hashlib, math
from datetime import datetime
from collections import defaultdict

class KnowledgeBase:
    def __init__(self, kb_dir=None):
        self.name = "KnowledgeBase"
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.kb_dir = kb_dir or os.path.join(base_dir, 'memory', 'knowledge')
        os.makedirs(self.kb_dir, exist_ok=True)
        self.index_file = os.path.join(self.kb_dir, 'kb_index.json')
        self.index = self._load_index()
        self.word_index = defaultdict(set)
        self._build_word_index()

    def _load_index(self):
        if os.path.exists(self.index_file):
            with open(self.index_file) as f:
                return json.load(f)
        return {'entries': [], 'domains': {}, 'total': 0}

    def _save_index(self):
        self.index['total'] = len(self.index['entries'])
        with open(self.index_file, 'w') as f:
            json.dump(self.index, f, indent=2)

    def _build_word_index(self):
        for entry in self.index['entries']:
            words = entry.get('title', '').lower().split() + entry.get('domain', '').lower().split()
            for w in words:
                self.word_index[w].add(entry['id'])

    def learn(self, title, content, domain='general', source=None, confidence=1.0):
        kid = hashlib.sha256(f'{title}{content[:100]}'.encode()).hexdigest()[:12]
        entry = {
            'id': kid,
            'title': title,
            'content': content,
            'domain': domain,
            'source': source or 'direct_input',
            'confidence': confidence,
            'learned': datetime.now().isoformat(),
            'access_count': 0,
            'relations': []
        }
        fpath = os.path.join(self.kb_dir, f'kb_{kid}.json')
        with open(fpath, 'w') as f:
            json.dump(entry, f, indent=2)
        self.index['entries'].append({'id':kid,'title':title,'domain':domain,'file':f'kb_{kid}.json'})
        self.index['domains'][domain] = self.index['domains'].get(domain, 0) + 1
        self._save_index()
        for w in title.lower().split():
            self.word_index[w].add(kid)
        return kid

    def query(self, question, domain=None):
        question_words = set(question.lower().split())
        scores = defaultdict(float)
        for word in question_words:
            for kid in self.word_index.get(word, set()):
                scores[kid] += 1.0
        for entry in self.index['entries']:
            if domain and entry['domain'] != domain:
                continue
            kid = entry['id']
            fpath = os.path.join(self.kb_dir, entry['file'])
            if os.path.exists(fpath):
                with open(fpath) as f:
                    data = json.load(f)
                content_words = set(data['content'].lower().split())
                overlap = len(question_words & content_words)
                if overlap > 0:
                    scores[kid] += overlap * 0.5
        results = []
        for kid, score in sorted(scores.items(), key=lambda x: -x[1])[:10]:
            for entry in self.index['entries']:
                if entry['id'] == kid:
                    fpath = os.path.join(self.kb_dir, entry['file'])
                    if os.path.exists(fpath):
                        with open(fpath) as f:
                            data = json.load(f)
                        data['relevance_score'] = score
                        results.append(data)
                    break
        return results

    def relate(self, kid1, kid2, relation_type='related'):
        for entry in self.index['entries']:
            if entry['id'] == kid1:
                fpath = os.path.join(self.kb_dir, entry['file'])
                if os.path.exists(fpath):
                    with open(fpath) as f:
                        data = json.load(f)
                    data['relations'].append({'target':kid2,'type':relation_type})
                    with open(fpath, 'w') as f:
                        json.dump(data, f, indent=2)
                    return True
        return False

    def get_domains(self):
        return self.index.get('domains', {})

    def export_domain(self, domain, export_path):
        entries = []
        for entry in self.index['entries']:
            if entry['domain'] == domain:
                fpath = os.path.join(self.kb_dir, entry['file'])
                if os.path.exists(fpath):
                    with open(fpath) as f:
                        entries.append(json.load(f))
        with open(export_path, 'w') as f:
            json.dump(entries, f, indent=2)
        return len(entries)

    def status(self):
        return {'engine':self.name,'total':self.index['total'],'domains':self.get_domains(),'kb_dir':self.kb_dir}

if __name__ == "__main__":
    kb = KnowledgeBase()
    kb.learn("Quantum Superposition", "A quantum system can exist in multiple states simultaneously until measured", domain="quantum_physics")
    kb.learn("Hadamard Gate", "Creates superposition by mapping |0> to (|0>+|1>)/sqrt(2)", domain="quantum_computing")
    kb.learn("SHA-256 Mining", "Bitcoin mining uses SHA-256 hash function to find nonces that produce hashes below target", domain="cryptocurrency")
    kb.learn("Drug Binding Affinity", "Molecular docking simulates how drug molecules bind to protein targets", domain="drug_discovery")
    r = kb.query("quantum superposition")
    print(f"[KnowledgeBase] Query results: {len(r)}")
    print(f"[KnowledgeBase] Domains: {kb.get_domains()}")
    print(f"[KnowledgeBase] Status: {kb.status()}")
