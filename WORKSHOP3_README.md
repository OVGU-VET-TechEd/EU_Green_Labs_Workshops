# Workshop 3 – System Guide: Local AI with Ollama & Gemma

> **EduGreenLabs · WP2 Training Lab · OvGU Magdeburg 2026**  
> Step-by-step guide to set up and use the full Workshop 3 toolchain.

---

## What This System Does

This workshop deploys a **fully local, privacy-respecting AI assistant** on your own hardware. No data leaves your machine. The core stack is:

| Component | Role |
|---|---|
| **Ollama** | Local model server — downloads, manages, and serves LLM weights |
| **Gemma:latest** | The language model (7B params, ~5.4 GB on disk) |
| **VS Code + Continue.dev** | Offline AI coding assistant inside your editor |
| **VS Code + GitHub Copilot** | Online AI assistant (free for educators) |
| **green_metrics.py** | Measures CO₂ footprint of local vs. cloud inference |
| **GitHub Codespaces** | Zero-install browser fallback if local setup fails |

---

## Step 0 — Check Your Hardware

Before anything else, verify you meet the minimum requirements.

| Component | Minimum | Recommended |
|---|---|---|
| RAM | 8 GB | 16 GB |
| Free disk space | 6 GB | 20 GB |
| OS | macOS 13+ / Ubuntu 22+ / Windows 11 + WSL2 | macOS or Ubuntu |
| Internet (setup only) | Required to download Ollama and the model | — |

> **Apple Silicon note:** M2/M3 Macs with 16 GB unified memory are the best laptop option — the GPU and CPU share the same RAM pool, making inference ~2× faster than a comparable Intel machine.

> **8 GB RAM warning:** Gemma:latest will work but will be tight. Close all other applications before running inference.

---

## Step 1 — Install Ollama

Ollama is a lightweight daemon that handles model downloading, quantisation, and serving. It exposes a local REST API on `http://localhost:11434`.

**macOS (Homebrew):**
```bash
brew install ollama
```

**macOS (GUI installer):**  
Download from [https://ollama.ai](https://ollama.ai) and run the `.dmg`.

**Linux (Ubuntu 22.04 / Debian 12):**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
# Installs the binary and registers a systemd service
```

**Windows:**  
WSL2 is required. In PowerShell as Administrator:
```powershell
wsl --install
# Then install Ubuntu 22.04 from the Microsoft Store.
# Inside the WSL2 terminal, run the Linux command above.
```

**Verify the installation:**
```bash
ollama --version
# Expected: ollama version 0.3.x or later

curl http://localhost:11434/api/version
# Expected: {"version":"0.3.x"}
```

If the `curl` call fails, Ollama's service is not running yet. Start it manually:
```bash
ollama serve   # Linux/macOS — runs in foreground, Ctrl+C to stop
# Windows: launch the Ollama app from the Start menu
```

---

## Step 2 — Download the Gemma Model

**This step requires ~5.4 GB of internet bandwidth and takes 5–15 minutes. Do it before the workshop begins.**

```bash
# Default model used in the workshop (7B params, Q4_K_M quantisation)
ollama pull gemma:latest

# Low-RAM alternative (1.4 GB, faster but lower quality):
ollama pull gemma:2b

# High-quality option for DGX Spark / institutional servers:
ollama pull gemma2:27b
```

After downloading, check what you have:
```bash
ollama list
# NAME            ID              SIZE      MODIFIED
# gemma:latest    abc123def456    5.4 GB    2 hours ago
```

> **What is Q4 quantisation?** The model weights are compressed from 16-bit floats (14 GB) to 4-bit integers (~5 GB). This reduces RAM usage by ~60% with minimal quality loss. Ollama uses `Q4_K_M` by default — a well-tuned balance.

---

## Step 3 — Run Your First Prompt

Test that everything is working with an interactive session:

```bash
ollama run gemma:latest
# Opens an interactive REPL — type a message and press Enter
# Type /bye or press Ctrl+D to exit
```

Or send a single prompt non-interactively:
```bash
ollama run gemma:latest "Explain data minimisation in one paragraph for a GDPR audit."
```

You should see a response stream in your terminal within a few seconds. If inference is very slow (<1 token/sec), your machine is running in pure CPU mode — this is normal on machines without a discrete GPU or Apple Silicon.

---

## Step 4 — Use the REST API from Python

Ollama exposes a local HTTP API that is **OpenAI-API-compatible**. This means you can use the standard `openai` Python library pointed at your local server.

**Install dependencies:**
```bash
pip install requests openai
```

**Method A — Direct REST call (no extra libraries):**
```python
# workshop3_exercise.py (from the repo)
import requests

def ask_gemma(prompt: str, system: str = "") -> str:
    """Send a prompt to Gemma locally. No data leaves your machine."""
    payload = {
        "model": "gemma:latest",
        "messages": [
            {"role": "system", "content": system},
            {"role": "user",   "content": prompt}
        ],
        "stream": False,
        "options": {"temperature": 0.7, "num_predict": 512}
    }
    r = requests.post("http://localhost:11434/api/chat", json=payload, timeout=120)
    r.raise_for_status()
    return r.json()["message"]["content"]

print(ask_gemma("List 3 GDPR data minimisation strategies for learning analytics."))
```

**Method B — OpenAI-compatible SDK (drop-in replacement):**
```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",          # Ollama ignores the key — any string works
)

response = client.chat.completions.create(
    model="gemma:latest",
    messages=[{"role": "user", "content": "What is federated learning?"}],
    temperature=0.7,
    max_tokens=400
)
print(response.choices[0].message.content)
```

> **Switching to cloud later:** To use the real OpenAI API, change `base_url` to `"https://api.openai.com/v1"` and supply a real API key. The rest of the code is identical — this is the OpenAI-compatibility guarantee Ollama provides.

Run the example file from the repo:
```bash
python3 ollama_api_examples.py
```

---

## Step 5 — Create a Custom Model (Modelfile)

A `Modelfile` bakes a system prompt and inference parameters into a named model variant. Useful for giving Gemma a persistent research-assistant persona.

**Create the file:**
```
# Modelfile
FROM gemma:latest

SYSTEM """
You are the EduGreenLabs Research Assistant. You help researchers design
privacy-respecting study protocols. Always apply data minimisation before
suggesting data collection. Flag GDPR implications in your recommendations.
"""

PARAMETER temperature 0.7
PARAMETER num_predict 1024
PARAMETER num_ctx 4096
```

**Build and run it:**
```bash
ollama create edugreenlab-assistant -f Modelfile
ollama run edugreenlab-assistant
```

---

## Step 6 — Set Up VS Code with an AI Assistant

You have two paths. Choose based on your data sensitivity:

```
OFFLINE PATH (sensitive research data)     ONLINE PATH (generic coding)
─────────────────────────────────────────  ──────────────────────────────
Continue.dev + Ollama                      GitHub Copilot for Educators
• Fully local — no data leaves machine     • Best code completion quality
• Open source, free                        • Free for verified educators
• Uses Gemma as its backend                • Sends code context to GitHub
• Ideal for code touching personal data    • Fast, cloud-backed
```

### Option A — Continue.dev (Offline)

1. Open VS Code → Extensions (`Ctrl+Shift+X`) → search **"Continue"** → Install
2. Click the Continue icon in the left sidebar
3. Create or edit `~/.continue/config.json`:

```json
{
  "models": [
    {
      "title": "Gemma (Local)",
      "provider": "ollama",
      "model": "gemma:latest",
      "apiBase": "http://localhost:11434"
    }
  ]
}
```

**Key shortcuts in Continue:**
| Action | Shortcut |
|---|---|
| Open chat sidebar | `Ctrl+L` / `Cmd+L` |
| Inline edit selected code | `Ctrl+Shift+L` |
| Accept suggestion | `Tab` |
| Run `/privacy-check` on current file | Type `/privacy-check` in chat |

### Option B — GitHub Copilot (Online, Free for Educators)

1. Go to [https://education.github.com](https://education.github.com) → **Get benefits → Teacher/Researcher**
2. Verify with your institutional email (`@ovgu.de`, `@uevora.pt`, etc.)
3. Approval takes 1–7 days — apply early!
4. Install the **"GitHub Copilot"** extension in VS Code
5. Sign in with your GitHub account

> **Privacy rule:** Never have Copilot enabled in a file that contains personal data, pseudonyms, or confidential research records. Copilot sends the surrounding lines of your file to GitHub's servers for completion. Use Continue instead for sensitive code.

**Restrict Copilot from data files** — add to `.vscode/settings.json`:
```json
{
  "github.copilot.enable": {
    "csv": false,
    "plaintext": false
  },
  "github.copilot.advanced": {
    "excludeFiles": ["**/data/**", "**/*.csv", "**/*.json"]
  }
}
```

---

## Step 7 — Run the Green Metrics Script

The `green_metrics.py` script measures the CO₂ footprint of each inference call and compares it to equivalent cloud API usage.

```bash
python3 green_metrics.py
```

Expected output:
```
=== EduGreenLabs Green Metric Report ===
Model:           gemma:latest
Tokens generated:187 @ 18.4 tok/s
Time:            10.16s
Energy:          0.00009200 kWh
CO₂ (local):     0.0368 g
CO₂ (cloud est): 0.0561 g
CO₂ saved:       34.4%
```

**What the numbers mean:**
- `Energy (kWh)` — estimated from your hardware's TDP × active fraction × time
- `CO₂ (local)` — local energy × your country's grid carbon intensity (g CO₂/kWh)
- `CO₂ (cloud est)` — estimated cost of the same query via a cloud API
- `CO₂ saved` — percentage reduction from running locally

**EduGreenLabs target:** ≥ 25% CO₂ reduction vs. cloud API equivalents. Laptop inference typically achieves **70–95%** savings.

Edit the `country` parameter to match your location:
```python
# Available presets: "DE" (400 g/kWh), "PT" (130), "RO" (340), "EU" (300)
result = estimate_inference_footprint(..., country="DE", hardware_tdp_watts=65)
```

---

## Step 8 (Optional) — GitHub Codespaces Fallback

If your local machine can't run Ollama, use the pre-configured cloud development environment:

1. Go to [https://github.com/OVGU-VET-TechEd/EU_Green_Labs_Workshops](https://github.com/OVGU-VET-TechEd/EU_Green_Labs_Workshops)
2. Click **Code → Codespaces → Create codespace on main**
3. Wait ~90 seconds — VS Code opens in your browser with Python, Ollama, and Continue already installed
4. The Ollama API is available at `http://localhost:11434` exactly as in the local setup

> **Performance note:** Codespaces has no GPU. Gemma:2b will run fine (~5 tok/s); Gemma:latest will be slow (~2 tok/s). This is acceptable for learning the API — not for production use.

---

## Deployment Scenario Quick Reference

| Your situation | Recommended setup | Key command |
|---|---|---|
| Personal laptop, single user | Ollama + `gemma:latest` locally | `ollama run gemma:latest` |
| 8 GB RAM machine | Use `gemma:2b` instead | `ollama pull gemma:2b` |
| Shared server for a research group | Ollama systemd service, expose on LAN | `OLLAMA_HOST=0.0.0.0:11434 ollama serve` |
| DGX Spark (departmental) | Pull larger models, 4 parallel workers | `ollama pull gemma2:27b` |
| Institutional HPC | Docker Compose + NGINX TLS proxy | See `docker-compose.yml` in repo |
| No local GPU, need to learn the API | GitHub Codespaces | See Step 8 above |

---

## Troubleshooting

**Ollama command not found after install:**
```bash
export PATH=$PATH:/usr/local/bin   # Linux
# macOS: restart your terminal after Homebrew install
```

**`curl http://localhost:11434/api/version` returns "connection refused":**
```bash
ollama serve   # start the daemon manually
# or on Linux: sudo systemctl start ollama
```

**Inference is extremely slow (<1 token/sec):**  
This is CPU-only inference. It is normal on machines without Apple Silicon or a discrete NVIDIA/AMD GPU. Use `gemma:2b` for faster responses during the workshop.

**Python script: `ConnectionRefusedError`:**  
Ollama is not running. Start it with `ollama serve` in a separate terminal.

**Out of memory / model fails to load:**  
Close all browser tabs, other applications, and try `gemma:2b` instead of `gemma:latest`.

---

## Key Files in This Repository

| File | What it does |
|---|---|
| `workshop3_ai_implementation_sprint.md` | The full 90-min LiaScript workshop presentation |
| `ollama_api_examples.py` | Python code examples for the Ollama REST and OpenAI-compatible APIs |
| `green_metrics.py` | CO₂ footprint estimator for local inference |
| `workshop3_exercise.py` | Hands-on coding exercise template (GDPR-aware data processing) |
| `docker-compose.yml` | Production deployment stack (Ollama + NGINX TLS proxy) |
| `.devcontainer/devcontainer.json` | GitHub Codespaces configuration |

---

*EduGreenLabs · EU-GREEN University Alliance · OvGU Magdeburg · CC BY-SA 4.0*  
*All code examples: MIT Licence*
