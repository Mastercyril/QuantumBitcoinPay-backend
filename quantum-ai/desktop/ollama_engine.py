
import requests
import json

class OllamaEngine:
    """Ollama LLM backend for Quantum AI - 13th Chamber LLC"""
    
    def __init__(self, model="llama3.2", fallback_model="mistral"):
        self.base_url = "http://localhost:11434"
        self.model = model
        self.fallback_model = fallback_model
        self.available = self._check_available()
        self.active_model = None
        if self.available:
            self.active_model = self._get_best_model()
    
    def _check_available(self):
        try:
            r = requests.get(f"{self.base_url}", timeout=3)
            return r.status_code == 200
        except:
            return False
    
    def _get_best_model(self):
        try:
            r = requests.get(f"{self.base_url}/api/tags", timeout=5)
            models = r.json().get("models", [])
            names = [m["name"] for m in models]
            # Prefer in order: llama3, mistral, phi, gemma, any
            for preferred in ["llama3", "llama2", "mistral", "phi", "gemma", "qwen"]:
                for n in names:
                    if preferred in n.lower():
                        return n
            return names[0] if names else None
        except:
            return None
    
    def chat(self, prompt, system_prompt=None, context=None):
        if not self.available or not self.active_model:
            return None  # Fall back to other engine
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        if context:
            for msg in context[-10:]:  # Last 10 messages
                messages.append(msg)
        messages.append({"role": "user", "content": prompt})
        
        try:
            r = requests.post(
                f"{self.base_url}/api/chat",
                json={"model": self.active_model, "messages": messages, "stream": False},
                timeout=60
            )
            return r.json()["message"]["content"]
        except Exception as e:
            return None
    
    def analyze_image(self, image_path, prompt="Describe this image in detail"):
        """Analyze image using vision-capable model"""
        import base64
        try:
            with open(image_path, "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode()
            r = requests.post(
                f"{self.base_url}/api/generate",
                json={"model": self.active_model or "llava", "prompt": prompt, "images": [img_b64], "stream": False},
                timeout=60
            )
            return r.json().get("response", "Could not analyze image")
        except Exception as e:
            return f"Image analysis error: {str(e)}"
    
    def status(self):
        return {
            "available": self.available,
            "active_model": self.active_model,
            "url": self.base_url
        }
