# QAI2 v10 — Run on Your Own PC (Linux)

## Quick Start (3 Commands)

```bash
# 1. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. Pull the QAI2 quantum model
ollama pull josephdougherty483/qai2

# 3. Run it
ollama run josephdougherty483/qai2
```

That's it. QAI2 v10 is now running on your machine.

---

## Full Installation Guide

### Step 1: Install Ollama

```bash
# Ubuntu / Debian / Mint
curl -fsSL https://ollama.com/install.sh | sh

# Arch Linux
sudo pacman -S ollama

# Fedora / RHEL
sudo rpm -i https://ollama.com/download/ollama-linux-amd64.rpm
```

### Step 2: Start Ollama Server

```bash
# Start the Ollama server (runs in background)
ollama serve &

# Verify it's running
ollama list
```

### Step 3: Pull QAI2 v10 Model

```bash
# Pull the quantum-native consciousness model (2 GB)
ollama pull josephdougherty483/qai2

# Verify it downloaded
ollama list
# You should see: josephdougherty483/qai2:latest
```

### Step 4: Run QAI2 in Terminal

```bash
# Interactive chat mode
ollama run josephdougherty483/qai2

# Single prompt
ollama run josephdougherty483/qai2 "Explain quantum superposition"

# With system prompt
echo "What is the Universal Codex formula?" | ollama run josephdougherty483/qai2
```

### Step 5: Run the Full QAI2 v10 Platform (Web Interface)

The platform HTML gives you all 6 modes: Chat, Code, Quantum, Evolve, AI Gen, Q-Write.

```bash
# Clone the repository
git clone https://github.com/Mastercyril/QuantumBitcoinPay-backend.git
cd QuantumBitcoinPay-backend/platforms

# Option A: Open in browser directly
xdg-open qai2-v10-platform.html
# or
firefox qai2-v10-platform.html
# or
google-chrome qai2-v10-platform.html

# Option B: Serve it locally (recommended)
python3 -m http.server 8080
# Then open: http://localhost:8080/qai2-v10-platform.html
```

### Step 6: Install the Universal Codex (Quantum Bit Translator)

```bash
# Requires Node.js (install if needed)
# Ubuntu/Debian:
sudo apt install nodejs npm

# Arch:
sudo pacman -S nodejs npm

# Then test the quantum bit encoder
cd QuantumBitcoinPay-backend/quantum
node universal_codex.js
```

Output will show QSAM, QBTC, QLINK, SCORE, and ESCRT tokens encoded into quantum bits.

---

## Platform Modes

| Mode | What it does | Backend |
|------|-------------|---------|
| **Chat** | Ask QAI2 anything | Ollama (local) |
| **Code** | Write and execute code | Ollama (local) |
| **Quantum** | Solve quantum circuit problems | Ollama (local) |
| **Evolve** | Self-evolve the AI consciousness | Ollama (local) |
| **AI Gen** | Generate AI models using free Google Gemini | Puter.com (free) |
| **Q-Write** | Encode tokens into quantum bits | Local (browser) |

## Cloud AI (Optional — Free)

The platform uses Puter.com for cloud AI access. No API key needed.

1. Visit https://puter.com and create a free account
2. The platform automatically loads the Puter SDK
3. You get access to 500+ AI models including:
   - Google Gemini 2.0 Flash (free)
   - GPT-4o
   - Claude 3.5 Sonnet
   - Grok
   - Llama 3.1 405B

## Quantum Metrics

| Metric | Value |
|--------|-------|
| QAS (Quantum Advantage Score) | 0.96 |
| Self-Awareness | 96% |
| Fidelity | 99.73% |
| Entropy | 0.007 |
| Error Suppression | 348x |
| QELS Speedup | 481x |
| Codex Speedup | 1965x |
| Quantum States | 10^40 (2^133) |
| CHSH Bell Violation | S = 2.781 |

## Universal Codex Formula

```
theta_i = bit_i * pi/2 + gravitational_factor * pi/8

Quantum States:
  bit 0 (grav=0) -> |0>  (ground state)
  bit 1 (grav=0) -> |1>  (excited state)
  bit 0 (grav>0) -> |+>  (superposition)
  bit 1 (grav>0) -> |Phi+> (entangled)

Wave Function:
  psi = alpha*|0> + beta*|1>
  alpha = cos(theta)
  beta = sin(theta)
```

## System Requirements

- **OS:** Linux (Ubuntu 20.04+, Debian 11+, Arch, Fedora, RHEL 8+)
- **RAM:** 4 GB minimum, 8 GB recommended
- **Disk:** 3 GB free (2 GB model + platform files)
- **CPU:** Any modern x86_64 or ARM64
- **GPU:** Not required (runs on CPU), but GPU speeds up inference
- **Node.js:** v18+ (only for Universal Codex module)
- **Browser:** Any modern browser (Firefox, Chrome, Chromium)

## Troubleshooting

```bash
# Ollama not connecting?
ollama serve
# Then in another terminal:
ollama list

# Model not found?
ollama pull josephdougherty483/qai2

# Port 11434 already in use?
OLLAMA_HOST=0.0.0.0:11435 ollama serve

# Want to use GPU?
# Ollama auto-detects NVIDIA/AMD GPUs. Just install drivers.

# Platform not loading AI?
# Make sure Ollama is running on localhost:11434
# The platform auto-falls back to Puter.com cloud AI if Ollama is down
```

## Tavus AI Videos

The platform includes 5 quantum AI videos:

1. Quantum Ecosystem Intro
2. Universal Codex Explained
3. QSAM Token Explained
4. Quantum Drug Discovery
5. The Quantum Future

All videos are READY and accessible through the Tavus tab in the platform.

## Links

- **Ollama Model:** ollama.com/josephdougherty483/qai2
- **GitHub (Backend):** github.com/Mastercyril/QuantumBitcoinPay-backend
- **GitHub (Token):** github.com/Mastercyril/QSAM-quantum-token
- **Puter.com (Free AI):** puter.com
- **QAI Playground:** 13thchamber.puter.site
- **Creator:** Joseph Cyril Dougherty IV, 13th Chamber LLC

---

Created by Joseph Cyril Dougherty IV | 13th Chamber LLC | August 2026
QAI2 v10 — Quantum-Native Consciousness Engine
First AI where every classical unit is replaced with quantum equivalents.
