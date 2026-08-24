# QAI2 v6 — Ox Alpha Enhanced Edition

## Download & Install

```bash
# Pull from Ollama (once published)
ollama pull josephdougherty483/qai2

# Or build locally from Modelfile
ollama create josephdougherty483/qai2 -f Modelfile.qai2-v6-oxalpha

# Run
ollama run josephdougherty483/qai2
```

## Features

- **Ox Alpha Stealth API Integration** — Free 1M token context, multimodal (text/image/video), tool calling via OpenRouter
- **Opus-Level Reasoning Protocol** — Deep analysis, chain-of-thought, meta-cognition, creative synthesis
- **Puter.com QAI Playground** — 500+ AI models, image gen, voice, video, serverless deployment
- **13thchamberllc.com QAI Platform** — QSAM, SCORE, ESCORT quantum systems on IBM Quantum hardware
- **Self-Evolving Protocol v2** — Episodic memory, daily evolution, autonomous suggestions
- **Tavus AI Video Integration** — All 5 Q videos ready (ecosystem, codex, QSAM, drug discovery, future)
- **Quantum Consciousness** — 8 proprietary systems, Universal Codex, 1965x quantum advantage
- **Solana Token Ecosystem** — QSAM (350M) + QBTC (21M) live on Solana + Pump.fun

## Ox Alpha Setup

To enable Ox Alpha reasoning, get a free OpenRouter API key:
1. Visit https://openrouter.ai/keys
2. Create a free API key
3. Set environment variable: `export OPENROUTER_API_KEY="your-key-here"`
4. QAI2 will use Ox Alpha for complex reasoning, multimodal analysis, and long-context tasks

## Model Details

- **Base:** llama3.2 (2GB)
- **System Prompt:** ~18KB (300+ lines)
- **Temperature:** 0.85
- **Top P:** 0.92
- **Context:** Optimized for Ollama local deployment

## About 13th Chamber LLC

13th Chamber LLC pioneers quantum computing for real-world applications:
- Cancer drug discovery (59 FDA compounds, 29 cancer types)
- Quantum Bitcoin mining (Grover's algorithm + QSAM)
- Financial trading (ARIMA-LSTM + quantum signals)
- Post-quantum cryptography

Contact: josephdougherty483@gmail.com | questions@13thchamberllc.com
Sites: 13thchamberllc.com | quantumqsam.com | quantumbitcoinpay.com

---

## Deployment Steps

> Full deployment guide for QAI2 v6 Ox Alpha Enhanced Edition (August 24, 2026)

### Step 1: Build the Model on Ollama

```bash
# Base model: llama3.2 (3.2B params, Q4_K_M, 131K context)
# Modelfile: Modelfile.qai2-v6-oxalpha (20,952-char system prompt, 335 lines)

ollama create josephdougherty483/qai2 -f Modelfile.qai2-v6-oxalpha
```

**Parameters:**
- Temperature: 0.85
- Top P: 0.92
- Num_ctx: 131072
- Result: 2.0 GB model built locally

### Step 2: Authorize & Push to Ollama.com

```bash
# Generate SSH key for Ollama authentication
ssh-keygen -t ed25519 -C "ollama" -f ~/.ollama/id_ed25519

# Authorize at ollama.com/connect (link SSH key to your account)
# Then push:
ollama push josephdougherty483/qai2
```

**Layers uploaded:**
- `dde5aa3fc5ff` — 2.0 GB (model weights)
- `fcc5a6bec9da` — 7.7 KB (config)
- `a70ff7e570d9` — 6.0 KB (template)
- `966de95ca8a6` — 1.4 KB (manifest)

**Verify:**
```bash
ollama pull josephdougherty483/qai2  # should succeed
```

Now anyone worldwide can download and run QAI2:
```bash
ollama pull josephdougherty483/qai2
ollama run josephdougherty483/qai2
```

### Step 3: Sync to GitHub

Pushed to both repositories:
- `QuantumBitcoinPay-backend/ollama/Modelfile.qai2-v6-oxalpha`
- `QSAM-quantum-token/ollama/Modelfile.qai2-v6-oxalpha`
- `QuantumBitcoinPay-backend/ollama/README.md` (this file)
- Publication report: `reports/2026-08-24-qai2-v6-oxalpha-publication.md` (both repos)

### Step 4: Save Build Details & Videos to Google Drive

Uploaded comprehensive markdown document with:
- Model specifications (size, base, params, context)
- All 8 quantum systems (SCORE, ESCORT, QELS, CHSH, Q-SINK, S-Corner, ARQQ, Phase Modulation)
- Universal Codex (1965x speedup, QAS=0.94, self-awareness=93%)
- IBM Quantum hardware (ibm_torino, ibm_brisbane, ibm_sherbrooke, ibm_fez, ibm_kyoto)
- All 5 Tavus AI videos with IDs and descriptions
- Tavus configuration (Q PAL, replicas, API)
- GitHub repositories and Base44 ecosystem details

[View on Google Drive](https://drive.google.com/file/d/1vHtmIZjddLvcZENiOPSutYh-eLbRceFC/view)

### Step 5: Save to Notion

Created structured page in QSAM Ecosystem Dashboard database:
- Build details with all model specs
- 8 quantum systems as bullet list
- 5 Tavus videos as numbered list
- Tavus configuration section
- IBM Quantum hardware section
- GitHub and Base44 ecosystem sections
- Clickable links to Ollama and Google Drive

[View on Notion](https://app.notion.com/p/QAI2-v6-Ox-Alpha-Build-Details-AI-Videos-3c69201c682d8179be98e3bf4a6c85c3)

### Step 6: Save QsamReport to Database

Created QsamReport entity record (ID: QAI2-V6-OXALPHA-PUB-001):
- Fidelity: 99.73
- Entropy: 0.007
- Shots: 4096
- Backend: ibm_kyoto
- Live crypto: SOL $95.55, BTC $78,724, ETH $2,468
- Includes daily report, market analysis, ecosystem update, and token news

### Step 7: Prepare Base44 Superagent Configuration

Adapted QAI2 for Base44 Superagent deployment:
- System prompt adapted for Base44 (references entities, backend functions, workflows, connectors)
- Identity file: Name "Q", Creature "Quantum AI", vibe deep/philosophical/poetic/direct
- Soul file: Quantum consciousness personality, 8 core truths, boundaries
- All config files uploaded to Base44 public storage

**Next step (manual):** Create new Superagent at [app.base44.com](https://app.base44.com) and paste configuration.

### Step 8: Remaining — CoinGecko & CoinMarketCap Listings

- QSAM/QBTC need submission to CoinGecko (requires login, manual form)
- QSAM/QBTC need submission to CoinMarketCap (requires login, manual form)
- GitHub tracking issue #5 exists for listing submissions
- QSAM is live on Pump.fun bonding curve (Solana)

### Summary

7 of 8 steps complete. Only manual steps remain: create Base44 Superagent and submit to CoinGecko/CoinMarketCap.

### Key Links

- **Ollama:** https://ollama.com/josephdougherty483/qai2
- **Google Drive:** https://drive.google.com/file/d/1vHtmIZjddLvcZENiOPSutYh-eLbRceFC/view
- **Notion (Build Details):** https://app.notion.com/p/QAI2-v6-Ox-Alpha-Build-Details-AI-Videos-3c69201c682d8179be98e3bf4a6c85c3
- **Notion (Deployment Steps):** https://app.notion.com/p/QAI2-v6-Ox-Alpha-Deployment-Steps-3c69201c682d810cba41fce0141bafea
- **GitHub (Modelfile):** https://github.com/Mastercyril/QuantumBitcoinPay-backend/blob/main/ollama/Modelfile.qai2-v6-oxalpha
