<!--
author:   EduGreenLabs / OvGU Magdeburg – WP2 Training Lab
email:    edugreenlab@ovgu.de
version:  1.0.0
language: en
narrator: US English Female

comment:  Workshop 3 of the EduGreenLabs Training Lab Series (EU-GREEN Alliance).
          90-minute hands-on lab for Early Career Researchers on local AI deployment
          using Ollama, Gemma, VS Code, and GitHub for Educators.
          Covers hardware selection from laptop to NVIDIA DGX Spark to institutional server.

logo:     https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/OvGU_Logo.svg/320px-OvGU_Logo.svg.png

@style
.highlight { background-color: #e8f4f8; border-left: 4px solid #1a73e8; padding: 0.5em 1em; }
.warn      { background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 0.5em 1em; }
.success   { background-color: #d4edda; border-left: 4px solid #28a745; padding: 0.5em 1em; }
.code-note { font-size: 0.85em; color: #6c757d; }
@end
-->

# Workshop 3 – AI Implementation Sprint: From Metrics to Deployment Scenarios

> **EduGreenLabs · WP2 Training Lab · Magdeburg 2026**
>
> _Funded by the European Union – EU-GREEN University Alliance_

---

**⏱ Duration:** 90 minutes  
**👥 Audience:** Early Career Researchers (Post-Docs) in Informatics & Education  
**🛠️ Stack:** Ollama · Gemma · VS Code · GitHub Copilot for Educators  
**🎯 Goal:** Deploy a local, privacy-respecting AI model and understand hardware trade-offs across the full deployment spectrum

---

## ⚙️ Pre-Lab Requirements

> **Complete these before the workshop begins!**

```bash
# 1. Install Ollama (macOS / Linux / Windows WSL2)
curl -fsSL https://ollama.ai/install.sh | sh

# 2. Pull the Gemma model (~5 GB download — do this before the lab!)
ollama pull gemma:latest

# 3. Verify the installation
ollama run gemma:latest "Hello, are you working?"

# 4. Install VS Code  →  https://code.visualstudio.com
# 5. Install VS Code extension: "Continue" (offline AI) or GitHub Copilot

# 6. Clone the workshop repo
git clone https://github.com/edugreenlab/workshop3-deploy
cd workshop3-deploy
```

---

## 🗺️ Agenda Overview

| Block | Time | Topic |
|-------|------|-------|
| 0 | 0:00–0:05 | Welcome, goals & stack overview |
| 1 | 0:05–0:15 | UNESCO/OER context: why local AI matters |
| 2 | 0:15–0:32 | Hardware requirements & the deployment spectrum |
| 3 | 0:32–0:55 | Hands-on: Ollama + Gemma setup & first prompts |
| 4 | 0:55–1:10 | VS Code + GitHub Copilot for Educators |
| 5 | 1:10–1:25 | Deployment scenarios & green metrics |
| 6 | 1:25–1:30 | Wrap-up, quiz & next steps |

---

## Block 0 – Welcome & Goals _(0:00–0:05)_

### 🎯 Learning Objectives

By the end of this lab you will be able to:

1. Identify minimum hardware requirements for running **Gemma:latest** locally and compare to larger deployment options.
2. Install, configure, and interact with **Ollama** as a local model server.
3. Use **VS Code** with both **offline (Continue extension)** and **online (GitHub Copilot)** AI assistants.
4. Set up a **GitHub Codespace** as a zero-install fallback for running AI workflows.
5. Select an appropriate deployment scenario (laptop / DGX Spark / institutional server) based on task, privacy requirements, and energy constraints.
6. Estimate and log the **energy footprint** of local inference vs. cloud AI calls.

---

### 🧰 Stack Overview

```
┌───────────────────────────────────────────────────────────────────┐
│                    WORKSHOP 3 TOOLCHAIN                           │
├──────────────────────┬────────────────────────────────────────────┤
│  MODEL LAYER         │  Ollama (model manager) + Gemma:latest     │
│                      │  Alternative: Mistral 7B, Phi-3, LLaMA 3  │
├──────────────────────┼────────────────────────────────────────────┤
│  INTERFACE LAYER     │  VS Code + Continue.dev (offline)          │
│                      │  OR VS Code + GitHub Copilot (online)      │
├──────────────────────┼────────────────────────────────────────────┤
│  INFRA LAYER         │  GitHub (code + OER hosting)               │
│                      │  GitHub Codespaces (cloud dev environment) │
│                      │  GitHub Copilot for Educators (free tier)  │
├──────────────────────┼────────────────────────────────────────────┤
│  HARDWARE SPECTRUM   │  Laptop → DGX Spark → Institutional Server │
└──────────────────────┴────────────────────────────────────────────┘
```

---

## Block 1 – UNESCO/OER Context: Why Local AI Matters _(0:05–0:15)_

### 1.1 The Privacy-Sovereignty Argument for Local Deployment

The **UNESCO 2025 Guidance for Generative AI in Education** identifies a critical governance gap: most generative AI services are provided by a small number of US-based corporations, creating **data sovereignty risks** for educational institutions.

When a researcher sends a student essay to a cloud AI API:

```
Student essay ──► Cloud API ──► US server ──► Response
                       │
                       ▼
               ◎ Data may be used for model training
               ◎ EU GDPR Standard Contractual Clauses
                 may not fully address this risk
               ◎ Jurisdiction of the data: unclear
               ◎ Energy consumed: geographically remote
```

**Local inference with Ollama + Gemma eliminates all four risks:**

- ✅ Data never leaves your machine or institutional server
- ✅ GDPR compliance by design (no third-party processor)
- ✅ Works fully offline (critical for fieldwork, low-connectivity settings)
- ✅ Energy consumption is measurable and attributable

---

### 1.2 Why This Is Also an OER Issue

The **5R OER Principles** apply directly to the model layer:

| 5R Principle | Cloud AI (e.g., GPT-4 API) | Local Open Model (Gemma) |
|--------------|---------------------------|--------------------------|
| **Retain** | Model weights: proprietary | Weights: open licence (Gemma ToU) |
| **Reuse** | Limited by ToS | Freely usable for research |
| **Revise** | Not possible | Fine-tunable with your data |
| **Remix** | Not allowed | Can combine with other open models |
| **Redistribute** | Prohibited | Permitted (check licence version) |

> 💡 **Gemma licence note:** Gemma is released by Google under a custom open-weights licence. It permits research and educational use but has restrictions on using the model to train competing foundation models. Always check the current [Gemma Terms of Use](https://ai.google.dev/gemma/terms) before redistribution.

---

### 🧠 Quick Check: Local vs. Cloud AI

Which statement best justifies using local inference (Ollama + Gemma) for educational research involving student data?

[(X)] Local inference ensures student data never leaves the institution, removing the need for cloud data processing agreements
[( )] Local models are always more accurate than cloud models
[( )] Local inference is free of all licensing obligations
[( )] Cloud APIs always violate GDPR for educational use

---

## Block 2 – Hardware Requirements & the Deployment Spectrum _(0:15–0:32)_

### 2.1 Understanding Model Size and Hardware Needs

AI language models are described by their **parameter count** (billions of parameters = B). The memory required scales roughly linearly with parameters × precision:

```
Memory required (approximate):
─────────────────────────────────────────────────────────────
  Precision │ Formula               │ Gemma 7B example
────────────┼───────────────────────┼─────────────────────────
  FP32      │ params × 4 bytes      │ 7B × 4  = ~28 GB
  FP16/BF16 │ params × 2 bytes      │ 7B × 2  = ~14 GB
  Q8 (8-bit)│ params × 1 byte + oh  │ 7B × 1  ≈  8 GB
  Q4 (4-bit)│ params × 0.5 + oh     │ 7B × 0.5 ≈  5 GB  ← default Ollama
  Q2 (2-bit)│ params × 0.25 + oh    │ 7B × 0.25 ≈ 3 GB  (quality loss)
─────────────────────────────────────────────────────────────
"oh" = overhead for KV cache, system prompt, context window
```

**Ollama uses Q4_K_M quantisation by default** — a good balance of quality and memory efficiency.

---

### 2.2 The Deployment Spectrum

```
LOW END ◄──────────────────────────────────────────► HIGH END
                                                              
  💻 LAPTOP          🔷 DGX SPARK        🖥️ INST. SERVER
  Consumer HW         Edge AI Unit        Research HPC
                                                              
  RAM: 8–32 GB       RAM: 128 GB          RAM: 512+ GB
  GPU: None or       GPU: 1× H100 80GB   GPU: 4–8× A100/H100
       integrated         or B200         
  VRAM: 0 or 4GB    VRAM: 80 GB          VRAM: 320–640 GB
  Storage: 512GB–    NVMe: 1 TB SSD      Storage: 10+ TB NVMe
           2 TB
                                                              
  Models: ≤7B Q4    Models: 7B–70B       Models: 70B–405B
  Tokens/sec: 5–20  Tokens/sec: 100–500  Tokens/sec: 500+
  Energy: ~50W      Energy: 1000W        Energy: 5–20 kW
  Cost: your laptop Cost: ~$2,000        Cost: $50K+/unit
  Privacy: ✅✅✅   Privacy: ✅✅✅     Privacy: ✅✅ (shared)
  Setup: 10 min     Setup: 30 min        Setup: IT team
```

---

### 2.3 Hardware Specifications by Deployment Tier

#### Tier 1: Laptop Deployment (Workshop default)

Minimum recommended for `gemma:latest` (7B, Q4):

| Component | Minimum | Recommended | Notes |
|-----------|---------|-------------|-------|
| RAM | **8 GB** | 16 GB | 8 GB is tight; close all apps |
| CPU | Any modern (2019+) | Apple M2/M3 or AMD Ryzen 7 | Apple Silicon is best for inference |
| GPU/NPU | Not required | Apple M-series Neural Engine | CPU inference works, slower |
| Storage | 6 GB free | 20 GB free | For multiple models |
| OS | macOS 13+ / Ubuntu 22+ / Win 11 + WSL2 | macOS or Ubuntu | WSL2 adds overhead |

**Apple Silicon advantage:** The M-series chips use **unified memory** — the GPU and CPU share the same RAM pool, making 16 GB Apple Silicon faster for inference than a 32 GB Intel machine with a discrete GPU.

---

#### Tier 2: NVIDIA DGX Spark (Edge AI Unit)

The **NVIDIA DGX Spark** (formerly Project DIGITS, announced 2025) is a compact AI supercomputer designed for researchers who need serious inference capacity on-premises without a full server room.

| Component | DGX Spark Spec |
|-----------|---------------|
| GPU | 1× GB10 Grace Blackwell Superchip |
| GPU Memory | 128 GB LPDDR5X (unified) |
| CPU | 20-core ARM (Neoverse) |
| Storage | 4 TB NVMe SSD |
| Connectivity | 10 GbE + Thunderbolt 5 |
| Power | ~1,000 W peak, ~200 W idle |
| Form factor | Desktop (~15 cm cube) |
| Typical price | ~$3,000 USD (2025 launch) |
| Model capacity | Up to **200B parameter models** at FP8 |

**Use cases for EduGreenLabs:**

- Running multiple Gemma-27B / Mistral-7B instances in parallel
- Fine-tuning smaller models on institutional datasets (privacy compliant)
- Serving an AI endpoint to a classroom (5–20 concurrent students)
- A shared research resource for a department or ECR cohort

---

#### Tier 3: Institutional Server / HPC

For institutions with existing HPC infrastructure:

```yaml
# Example: Ollama on a university GPU server
# Managed by IT, accessed via SSH or API endpoint

hardware:
  GPU: "4× NVIDIA A100 80GB SXM5"
  CPU: "2× AMD EPYC 7763 (128 cores total)"
  RAM: "512 GB ECC DDR4"
  Storage: "10 TB NVMe (RAID-10)"
  Networking: "100 GbE InfiniBand"

ollama_config:
  OLLAMA_HOST: "0.0.0.0:11434"
  OLLAMA_NUM_PARALLEL: 4          # concurrent requests
  OLLAMA_MAX_LOADED_MODELS: 3     # models in VRAM simultaneously
  OLLAMA_FLASH_ATTENTION: "1"     # memory-efficient attention
  
models_capable:
  - "gemma:27b"          # 27B params, ~16 GB VRAM at Q4
  - "llama3.3:70b"       # 70B params, ~42 GB VRAM at Q4
  - "mixtral:8x22b"      # 141B MoE, ~90 GB VRAM at Q4
  - "llama3.1:405b"      # 405B params, needs all 4× A100
```

---

### 🧠 Hardware Quiz

A researcher wants to run `gemma:27b` (27 billion parameter model) locally for processing student essays. The model requires approximately 18 GB VRAM in Q4 quantisation. Which hardware tier supports this?

[( )] A standard laptop with 16 GB unified RAM (Apple M2)
[( )] A laptop with NVIDIA RTX 3060 (12 GB VRAM)
[(X)] A DGX Spark (128 GB unified memory) or institutional server with 24+ GB VRAM GPU
[( )] None of the above — 27B models can only run in the cloud

---

## Block 3 – Hands-On: Ollama + Gemma Setup _(0:32–0:55)_

### 3.1 Installing Ollama

Ollama is a local model manager that abstracts model downloading, quantisation, and serving behind a simple REST API.

```bash
# ── macOS ──────────────────────────────────────────────────────
# Download from https://ollama.ai (GUI installer available)
# OR via Homebrew:
brew install ollama

# ── Linux (Ubuntu 22.04 / Debian 12) ─────────────────────────
curl -fsSL https://ollama.ai/install.sh | sh
# This installs the ollama binary + systemd service

# Verify installation
ollama --version
# Expected output: ollama version 0.3.x (or later)

# ── Windows (WSL2 required) ────────────────────────────────────
# 1. Enable WSL2: wsl --install (in PowerShell as Admin)
# 2. Install Ubuntu 22.04 from Microsoft Store
# 3. Inside WSL2 terminal, run the Linux command above

# ── Check the Ollama service is running ───────────────────────
curl http://localhost:11434/api/version
# Expected: {"version":"0.3.x"}
```

---

### 3.2 Pulling and Running Gemma

```bash
# Pull the default Gemma model (Gemma 2 9B, Q4_K_M quantisation)
ollama pull gemma:latest
# Download size: ~5.4 GB — takes 5–15 min depending on connection

# Alternative smaller model (for 8 GB RAM machines):
ollama pull gemma:2b         # ~1.4 GB, faster, lower quality

# Alternative higher quality (for 16+ GB RAM or DGX):
ollama pull gemma2:27b       # ~16 GB, much better reasoning

# List downloaded models
ollama list
# NAME            ID              SIZE    MODIFIED
# gemma:latest    abc123def456    5.4 GB  2 hours ago

# Interactive chat (REPL mode)
ollama run gemma:latest

# Single prompt via command line
ollama run gemma:latest "Explain data minimisation in one paragraph for a GDPR audit."

# Stop the service (if needed)
# macOS: find Ollama in menu bar → Quit
# Linux: sudo systemctl stop ollama
```

---

### 3.3 Using the Ollama REST API

Ollama exposes a local HTTP API (port 11434) that is OpenAI-API-compatible. This means any tool built for the OpenAI API can be pointed at Ollama with minimal changes.

```python
# ── Python: requests library ──────────────────────────────────
import requests
import json

def ask_gemma(prompt: str, system: str = "") -> str:
    """
    Send a prompt to the local Gemma model via Ollama REST API.
    No data leaves your machine.
    """
    payload = {
        "model": "gemma:latest",
        "messages": [
            {"role": "system", "content": system},
            {"role": "user",   "content": prompt}
        ],
        "stream": False,          # True for streaming responses
        "options": {
            "temperature": 0.7,   # 0=deterministic, 1=creative
            "num_predict": 512,   # max tokens in response
            "top_k": 40,          # diversity of token selection
            "top_p": 0.9          # nucleus sampling threshold
        }
    }
    
    response = requests.post(
        "http://localhost:11434/api/chat",
        json=payload,
        timeout=120
    )
    response.raise_for_status()
    return response.json()["message"]["content"]


# Example 1: Research assistant for data management
dm_system = """You are a GDPR-compliant research assistant for educational 
data science. You help researchers design privacy-respecting study protocols. 
Never store or repeat personally identifiable information."""

result = ask_gemma(
    prompt="What pseudonymisation strategy should I use for longitudinal "
           "learning analytics data across 3 universities?",
    system=dm_system
)
print(result)
```

---

```python
# ── Python: OpenAI-compatible API (drop-in replacement) ───────
from openai import OpenAI

# Point the OpenAI client at your local Ollama instance
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",              # Ollama ignores the key value
)

response = client.chat.completions.create(
    model="gemma:latest",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful research assistant specialising "
                       "in educational AI ethics and GDPR compliance."
        },
        {
            "role": "user",
            "content": "List 5 data minimisation strategies for a learning "
                       "analytics study on PhD student writing habits."
        }
    ],
    temperature=0.7,
    max_tokens=800
)

print(response.choices[0].message.content)
# ✅ This code works identically with the real OpenAI API —
#    just change base_url to "https://api.openai.com/v1" and
#    provide a real API key. Zero code change needed.
```

---

### 3.4 Streaming Responses (for interactive applications)

```python
import requests
import json

def ask_gemma_streaming(prompt: str) -> None:
    """Stream tokens as they are generated — useful for UI responsiveness."""
    payload = {
        "model": "gemma:latest",
        "messages": [{"role": "user", "content": prompt}],
        "stream": True
    }
    
    with requests.post(
        "http://localhost:11434/api/chat",
        json=payload,
        stream=True,
        timeout=120
    ) as response:
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line)
                if not chunk.get("done", False):
                    # Print each token as it arrives (no newline)
                    print(chunk["message"]["content"], end="", flush=True)
        print()  # Final newline

ask_gemma_streaming(
    "Describe the NVIDIA DGX Spark and its relevance to educational AI research."
)
```

---

### 3.5 ✏️ Hands-On Exercise: Your First Research Prompt _(8 minutes)_

> _Run these in your terminal or in a Jupyter notebook_

**Exercise 3A:** Basic interaction

```bash
# In your terminal:
ollama run gemma:latest "What are the 5 key principles of privacy-by-design 
and how do they apply to AI-powered learning systems?"
```

**Exercise 3B:** Python API call

```python
# Save as workshop3_ex.py and run: python workshop3_ex.py
import requests, json

def ask(prompt):
    r = requests.post("http://localhost:11434/api/chat",
        json={"model": "gemma:latest",
              "messages": [{"role": "user", "content": prompt}],
              "stream": False})
    return r.json()["message"]["content"]

# TODO: Write a prompt that asks Gemma to help you design
# a minimal dataset for your own research project.
# Use what you learned in Workshop 2!

my_research_question = "..."   # fill in your question
prompt = f"""
I am a researcher studying {my_research_question}.
Help me identify:
1. The minimum data variables I need (apply data minimisation)
2. The GDPR legal basis for each variable
3. The appropriate pseudonymisation strategy

Be concise and practical.
"""

print(ask(prompt))
```

**Exercise 3C:** Model comparison

```bash
# If you have gemma:2b pulled, compare quality vs speed:
time ollama run gemma:2b    "Explain federated learning in 3 sentences."
time ollama run gemma:latest "Explain federated learning in 3 sentences."
# Note the difference in response time and quality
```

---

### 3.6 Ollama Model Configuration (Modelfile)

You can create customised model variants using a `Modelfile`:

```dockerfile
# Modelfile — EduGreenLabs Research Assistant
# Save as: Modelfile
# Build with: ollama create edugreenlab-assistant -f Modelfile

FROM gemma:latest

# System prompt baked into the model
SYSTEM """
You are the EduGreenLabs Research Assistant, specialised in:
- Privacy-by-design for educational AI systems
- GDPR compliance in research contexts
- UNESCO AI ethics principles
- Open Educational Resources (OER) best practices
- Green and low-energy AI design

You always:
1. Suggest data minimisation before suggesting data collection
2. Flag GDPR implications in your recommendations
3. Recommend open-source alternatives to proprietary tools
4. Note the energy cost of AI solutions when relevant

You never: provide personally identifiable information, 
store conversation history, or recommend collecting data 
beyond what is strictly necessary.
"""

# Inference parameters
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40
PARAMETER num_predict 1024
PARAMETER num_ctx 4096          # context window (token limit)
```

```bash
# Build the custom model
ollama create edugreenlab-assistant -f Modelfile

# Run it
ollama run edugreenlab-assistant

# Share it (within your institution — not publicly if trained on sensitive data)
ollama push your-registry/edugreenlab-assistant
```

---

## Block 4 – VS Code + GitHub Copilot for Educators _(0:55–1:10)_

### 4.1 Two Paths: Online (Copilot) vs. Offline (Continue.dev)

```
ONLINE PATH                          OFFLINE PATH
──────────────                       ──────────────
GitHub Copilot                       Continue.dev Extension
  • Best code completion             • Fully local (no data leaves machine)
  • Requires internet                • Uses Ollama as backend
  • Free for educators/students      • Free and open source
  • Data sent to GitHub/Azure        • Perfect for sensitive research
  • Rich IDE integration             • Good code completion + chat
```

**Rule of thumb:** Use **Copilot** for generic coding tasks. Use **Continue + Ollama** when working with sensitive data, student records, or research code that processes personal information.

---

### 4.2 Setting Up GitHub Copilot for Educators

GitHub provides **free Copilot access** to verified educators and students through the GitHub Education programme.

**Step 1: Apply for GitHub Education**

```
1. Go to https://education.github.com/
2. Click "Get benefits"
3. Select "Teacher" or "Researcher"
4. Verify with your institutional email (@ovgu.de, @uevora.pt, etc.)
5. Approval takes 1–7 days
6. You receive free: Copilot Individual, GitHub Pro, Codespaces credits
```

**Step 2: Enable Copilot in VS Code**

```
1. Open VS Code
2. Install extension: "GitHub Copilot" (publisher: GitHub)
3. Sign in with your GitHub account
4. Enable Copilot: Ctrl/Cmd + Shift + P → "GitHub Copilot: Enable"
```

**Step 3: Configure Copilot settings (important for research)**

```json
// .vscode/settings.json — add to your project
{
  "github.copilot.enable": {
    "*": true,
    "plaintext": false,    // disable in .txt files with research notes
    "markdown": false,     // disable in markdown to avoid generating content
    "csv": false           // NEVER enable for data files
  },
  // Privacy: exclude sensitive directories from Copilot context
  "github.copilot.advanced": {
    "excludeFiles": [
      "**/data/**",
      "**/private/**",
      "**/*.csv",
      "**/*.json" 
    ]
  }
}
```

> ⚠️ **Important privacy note:** GitHub Copilot sends **your code context** (surrounding lines) to GitHub's servers for completion. Never work in a Copilot-enabled file that contains personal data, pseudonyms, or confidential research data.

---

### 4.3 Setting Up Continue.dev (Offline AI in VS Code)

**Continue** is an open-source VS Code extension that connects to any local LLM via Ollama.

```
1. Install VS Code extension: "Continue" (publisher: Continue)
2. Open Continue sidebar: click the Continue icon in the activity bar
3. Configure to use Ollama: click the settings gear icon
```

```json
// ~/.continue/config.json
// This file configures Continue to use your local Gemma model
{
  "models": [
    {
      "title": "Gemma (Local - Private)",
      "provider": "ollama",
      "model": "gemma:latest",
      "apiBase": "http://localhost:11434",
      "contextLength": 4096,
      "description": "Local Gemma model via Ollama. No data leaves your machine."
    },
    {
      "title": "EduGreenLabs Assistant (Local)",
      "provider": "ollama", 
      "model": "edugreenlab-assistant",
      "apiBase": "http://localhost:11434",
      "contextLength": 4096,
      "description": "Custom EduGreenLabs research assistant. Fully private."
    }
  ],
  "slashCommands": [
    {
      "name": "privacy-check",
      "description": "Check this code for GDPR/privacy issues",
      "prompt": "Review this code for GDPR compliance issues and data privacy risks. Flag any personal data handling, suggest data minimisation improvements, and check for identifier smuggling:"
    },
    {
      "name": "oer-review",
      "description": "Review for OER compatibility",
      "prompt": "Review this code/content for Open Educational Resource compatibility. Check: Is it openly licensed? Does it depend on proprietary services? Can it be used offline? Are there privacy-respecting alternatives to cloud dependencies?"
    }
  ],
  "contextProviders": [
    {"name": "code"},
    {"name": "docs"},
    {"name": "diff"},
    {"name": "terminal"}
  ]
}
```

**Using Continue in VS Code:**

```
── Inline code completion ──────────────────────────────────────
  Just code normally — Continue suggests completions as you type
  Accept with Tab, reject with Esc

── Chat with your code ─────────────────────────────────────────
  Open Continue sidebar (Ctrl+L / Cmd+L)
  Type your question — it has context of your open file

── Slash commands ──────────────────────────────────────────────
  /privacy-check    → audit current code for GDPR issues
  /oer-review       → check for OER/openness issues
  /edit             → ask Continue to modify selected code
  /comment          → auto-generate docstrings

── Highlight + explain ─────────────────────────────────────────
  Select code → Ctrl+Shift+L → ask a question about it
```

---

### 4.4 GitHub Codespaces: Zero-Install Cloud Development

For participants without a compatible local machine, **GitHub Codespaces** provides a VS Code environment in the browser with pre-installed tools.

```
Workshop fallback procedure:
─────────────────────────────────────────────────────────────
1. Go to: https://github.com/edugreenlab/workshop3-deploy
2. Click "Code" → "Codespaces" → "Create codespace on main"
3. Wait ~90 seconds for the environment to build
4. VS Code opens in your browser — fully configured!
5. The devcontainer includes Python, Ollama, and all dependencies
─────────────────────────────────────────────────────────────
Note: Ollama in Codespaces runs WITHOUT a GPU (CPU only).
Gemma:2b will run; Gemma:latest will be slow (~2 tokens/sec).
This is fine for learning the API — not for production use.
```

```json
// .devcontainer/devcontainer.json (in the workshop repo)
{
  "name": "EduGreenLabs Workshop 3",
  "image": "mcr.microsoft.com/devcontainers/python:3.12",
  "features": {
    "ghcr.io/devcontainers/features/github-cli:1": {}
  },
  "postCreateCommand": "pip install -r requirements.txt && curl -fsSL https://ollama.ai/install.sh | sh && ollama serve &",
  "extensions": [
    "Continue.continue",
    "GitHub.copilot",
    "ms-python.python",
    "ms-toolsai.jupyter"
  ],
  "forwardPorts": [11434, 8888],
  "portAttributes": {
    "11434": {"label": "Ollama API"},
    "8888": {"label": "Jupyter"}
  }
}
```

---

### ✏️ Exercise: Privacy-Aware Coding with VS Code _(5 minutes)_

Using either Copilot or Continue, complete the following task:

```python
# workshop3_privacy_task.py
# TASK: Finish this function using your AI assistant (Copilot or Continue)
# CONSTRAINT: The completed function must pass the privacy checklist below

import hashlib, hmac, os

def process_research_data(raw_records: list[dict]) -> list[dict]:
    """
    Process raw educational research records:
    1. Pseudonymise the 'email' field using HMAC-SHA256
    2. Remove the 'name' field entirely (not needed)
    3. Bin 'login_time' to time-of-day category
    4. Keep only: pseudo_id, time_of_day, score_band, task_type
    
    Returns a list of privacy-minimised records.
    """
    SECRET = os.environ.get("PSEUDO_SECRET", "").encode()
    
    # TODO: Complete this function with your AI assistant
    # Use /privacy-check in Continue to verify your solution
    pass


# Privacy checklist for your implementation:
# [ ] No real names or emails in the output
# [ ] HMAC-SHA256 used for pseudonymisation (not plain SHA256)
# [ ] Exact timestamps removed
# [ ] Only necessary fields retained
# [ ] Secret key loaded from environment (not hardcoded)
```

> _After completing the function, use `/privacy-check` in Continue to have Gemma audit your code for GDPR issues._

---

## Block 5 – Deployment Scenarios & Green Metrics _(1:10–1:25)_

### 5.1 Deployment Scenario Matrix

Use this decision matrix to select the right deployment tier for your use case:

| Use Case | Data Sensitivity | Scale | Recommended Tier |
|----------|-----------------|-------|-----------------|
| Personal research assistant | No sensitive data | Single user | **Laptop** |
| Classroom AI tutor (pilot) | Student interactions (T2) | 10–30 students | **Laptop or DGX Spark** |
| Research data processing | Performance data (T2–T3) | 1–5 researchers | **DGX Spark or Institutional** |
| Cross-university study | Multi-institutional (T3) | 50–200 participants | **Institutional server (federated)** |
| AI writing assistant for PhDs | Essays/drafts (T2) | 20–100 users | **DGX Spark (shared)** |
| Real-time student feedback | Quiz responses (T1) | 100+ concurrent | **Institutional server** |
| Fine-tuning on local data | Any (T2–T4) | N/A | **DGX Spark or Institutional** |

---

### 5.2 Scenario A: Laptop Deployment — Personal Research Assistant

```bash
# Complete setup for a personal Ollama + Gemma research assistant
# Estimated time: 10 minutes

# 1. Start Ollama (runs as a background service after install)
ollama serve &          # Linux/macOS only — Windows: Ollama app starts automatically

# 2. Pull the model if not already done
ollama pull gemma:latest

# 3. Create a custom system prompt
cat > research_assistant.modelfile << 'EOF'
FROM gemma:latest
SYSTEM "You are a privacy-aware research assistant. Apply data minimisation principles to all suggestions."
PARAMETER temperature 0.7
PARAMETER num_predict 512
EOF

ollama create research-assistant -f research_assistant.modelfile

# 4. Interactive session
ollama run research-assistant

# 5. API usage from Python
python3 -c "
import requests
r = requests.post('http://localhost:11434/api/chat',
    json={'model':'research-assistant',
          'messages':[{'role':'user','content':'Suggest 3 minimal data variables for studying PhD dropout risk without collecting sensitive personal data.'}],
          'stream':False})
print(r.json()['message']['content'])
"
```

---

### 5.3 Scenario B: DGX Spark — Shared Departmental AI

```bash
# Setup Ollama as a shared service on DGX Spark
# Accessible to your research group over the local network

# 1. Install Ollama on the DGX Spark
# (SSH into the DGX Spark first: ssh your-name@dgx-spark.your-uni.de)
curl -fsSL https://ollama.ai/install.sh | sh

# 2. Configure for multi-user access
export OLLAMA_HOST="0.0.0.0:11434"    # listen on all interfaces
export OLLAMA_NUM_PARALLEL=4           # serve 4 concurrent users
export OLLAMA_MAX_LOADED_MODELS=3     # keep 3 models in VRAM

# 3. Set up systemd service for persistent operation
sudo tee /etc/systemd/system/ollama.service << 'EOF'
[Unit]
Description=Ollama AI Model Server
After=network.target

[Service]
Type=simple
User=ollama
Group=ollama
Environment="OLLAMA_HOST=0.0.0.0:11434"
Environment="OLLAMA_NUM_PARALLEL=4"
Environment="OLLAMA_MAX_LOADED_MODELS=3"
ExecStart=/usr/local/bin/ollama serve
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable ollama
sudo systemctl start ollama

# 4. Pull larger models (DGX Spark can handle these)
ollama pull gemma2:27b          # 27B params — high quality
ollama pull llama3.3:70b        # 70B — excellent reasoning
ollama pull nomic-embed-text    # for embedding/RAG workflows

# 5. From a researcher's laptop, connect to the shared DGX Spark:
# (Replace dgx-spark-ip with your unit's IP address)
export OLLAMA_HOST="http://dgx-spark-ip:11434"

python3 -c "
import os
import requests
base = os.environ.get('OLLAMA_HOST', 'http://localhost:11434')
r = requests.post(f'{base}/api/chat',
    json={'model':'gemma2:27b',
          'messages':[{'role':'user','content':'What are the key elements of a GDPR-compliant data management plan for an EU-GREEN research project?'}],
          'stream':False})
print(r.json()['message']['content'])
"
```

---

### 5.4 Scenario C: Institutional Server — Production Research Infrastructure

```yaml
# docker-compose.yml
# Production-grade Ollama deployment on institutional server
# Run with: docker-compose up -d

version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    container_name: ollama-research
    restart: unless-stopped
    ports:
      - "11434:11434"
    volumes:
      - ollama_models:/root/.ollama    # persistent model storage
    environment:
      - OLLAMA_HOST=0.0.0.0:11434
      - OLLAMA_NUM_PARALLEL=8
      - OLLAMA_MAX_LOADED_MODELS=4
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all                # use all available GPUs
              capabilities: [gpu]
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:11434/api/version"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx-proxy:
    image: nginx:alpine
    container_name: ollama-proxy
    restart: unless-stopped
    ports:
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro    # your institution's TLS certs
    depends_on:
      - ollama

volumes:
  ollama_models:
    driver: local
    driver_opts:
      type: none
      device: /data/ollama-models       # fast NVMe path
      o: bind
```

```nginx
# nginx.conf — TLS termination + access control for institutional Ollama
events { worker_processes auto; }
http {
    server {
        listen 443 ssl;
        server_name ai-research.your-uni.de;

        ssl_certificate     /etc/nginx/certs/cert.pem;
        ssl_certificate_key /etc/nginx/certs/key.pem;

        # Restrict to institutional IP ranges (replace with your ranges)
        allow 134.76.0.0/16;   # OvGU Magdeburg range (example)
        allow 193.137.0.0/16;  # UÉvora range (example)
        deny all;

        location / {
            proxy_pass         http://ollama:11434;
            proxy_read_timeout 300s;
            proxy_set_header   Host $host;
        }
    }
}
```

---

### 5.5 Green Metrics: Measuring Your AI's Energy Footprint

The **EduGreenLabs Green Metric** tracks CO₂-equivalent emissions per training/inference hour.

```python
# green_metrics.py
# Estimate energy consumption and CO₂ for local inference
# Contributes to the EduGreenLabs carbon log

import time
import psutil
import requests

# EU average grid carbon intensity (2024)
# Source: ember-climate.org
CARBON_INTENSITY = {
    "DE": 400,   # Germany: ~400 gCO₂/kWh (varies with renewables)
    "PT": 130,   # Portugal: lower (more hydro/wind)
    "RO": 340,   # Romania: ~340 gCO₂/kWh
    "EU": 300,   # EU average
}

def estimate_inference_footprint(
    prompt: str,
    model: str = "gemma:latest",
    country: str = "DE",
    hardware_tdp_watts: float = 65.0   # laptop CPU TDP
) -> dict:
    """
    Estimate the carbon footprint of a single Ollama inference call.
    
    Args:
        prompt: The user prompt
        model: Ollama model name
        country: Your country code (for grid carbon intensity)
        hardware_tdp_watts: Estimated power draw of your hardware
    
    Returns:
        dict with timing, token count, energy, and CO2 estimates
    """
    start = time.time()
    
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={"model": model, 
              "messages": [{"role": "user", "content": prompt}],
              "stream": False}
    )
    
    elapsed_sec = time.time() - start
    data = response.json()
    
    # Extract token counts from Ollama response
    prompt_tokens = data.get("prompt_eval_count", 0)
    gen_tokens    = data.get("eval_count", 0)
    total_tokens  = prompt_tokens + gen_tokens
    tokens_per_sec = gen_tokens / elapsed_sec if elapsed_sec > 0 else 0
    
    # Energy: assume ~50% of TDP during active inference
    energy_kwh = (hardware_tdp_watts * 0.5 * elapsed_sec) / (3_600_000)
    
    # CO₂
    co2_g = energy_kwh * CARBON_INTENSITY.get(country, 300)
    
    # Cloud comparison (GPT-4 API): ~0.001 kWh per 1000 tokens (estimate)
    cloud_energy_kwh = total_tokens * 0.001 / 1000
    cloud_co2_g      = cloud_energy_kwh * 300  # US grid mix
    
    return {
        "model":           model,
        "prompt_tokens":   prompt_tokens,
        "gen_tokens":      gen_tokens,
        "tokens_per_sec":  round(tokens_per_sec, 1),
        "elapsed_sec":     round(elapsed_sec, 2),
        "energy_kwh":      round(energy_kwh, 8),
        "co2_grams":       round(co2_g, 6),
        "cloud_co2_grams": round(cloud_co2_g, 6),
        "co2_saved_pct":   round((1 - co2_g / cloud_co2_g) * 100, 1) if cloud_co2_g > 0 else 0,
        "response":        data["message"]["content"]
    }


# Example usage
if __name__ == "__main__":
    result = estimate_inference_footprint(
        prompt="Summarise the key data minimisation principles from GDPR in 3 bullet points.",
        model="gemma:latest",
        country="DE",
        hardware_tdp_watts=65
    )
    
    print("=== EduGreenLabs Green Metric Report ===")
    print(f"Model:           {result['model']}")
    print(f"Tokens generated:{result['gen_tokens']} @ {result['tokens_per_sec']} tok/s")
    print(f"Time:            {result['elapsed_sec']}s")
    print(f"Energy:          {result['energy_kwh']:.8f} kWh")
    print(f"CO₂ (local):     {result['co2_grams']:.4f} g")
    print(f"CO₂ (cloud est): {result['cloud_co2_grams']:.4f} g")
    print(f"CO₂ saved:       {result['co2_saved_pct']}%")
    print(f"\nResponse:\n{result['response']}")
```

---

### 5.6 Hardware Comparison: Energy & Performance

| Deployment | Model | Tokens/sec | Power (W) | CO₂/1M tokens (g) | Privacy |
|------------|-------|-----------|-----------|-------------------|---------|
| Laptop (M2, 16GB) | gemma:latest | 25–40 | ~20 | ~15 | ✅✅✅ |
| Laptop (Intel+RTX3060) | gemma:latest | 30–50 | ~80 | ~60 | ✅✅✅ |
| DGX Spark | gemma2:27b | 200–400 | ~300 | ~25 | ✅✅✅ |
| DGX Spark | llama3.3:70b | 80–150 | ~600 | ~50 | ✅✅✅ |
| Institutional (4×A100) | llama3.1:405b | 300–500 | ~5000 | ~400 | ✅✅ |
| Cloud API (GPT-4o) | hosted | N/A | remote | ~100–500 (est.) | ❌ |

> 🌿 **EduGreenLabs target:** ≥ 25% CO₂ reduction per training/inference hour compared to cloud APIs. Local laptop inference achieves **70–95%** reduction in most scenarios.

---

### ✏️ Exercise: Run the Green Metrics Script _(5 minutes)_

```bash
# Save green_metrics.py from the code block above, then:
python3 green_metrics.py

# Log your results in the shared spreadsheet:
# https://docs.google.com/spreadsheets/... (link in workshop chat)

# Compare results across participants:
# - Different hardware: who gets the best tokens/sec?
# - Different models: gemma:2b vs gemma:latest — quality vs energy trade-off?
# - What is the collective CO₂ saved across all workshop participants?
```

---

## Block 6 – Wrap-Up & Final Quiz _(1:25–1:30)_

### 🔑 Key Takeaways

1. **Local AI = Privacy by architecture** — Ollama + Gemma means student data never leaves your institution.

2. **Hardware scales with model size** — `gemma:latest` runs on 8 GB RAM; `gemma2:27b` needs a DGX Spark or institutional GPU.

3. **Ollama is OpenAI-API-compatible** — minimal code changes to switch between local and cloud.

4. **VS Code + Continue** gives you AI-assisted coding without any cloud dependency — essential for sensitive research code.

5. **GitHub Copilot is free for educators** — apply via education.github.com; use responsibly (not with personal data files open).

6. **Measure your footprint** — local inference is significantly greener than cloud APIs; log it in the EduGreenLabs carbon tracking sheet.

---

### 🎓 Final Quiz

**Q1:** What is the approximate VRAM/RAM requirement to run `gemma:latest` (7B, Q4) locally?

[( )] 2 GB — any modern laptop
[(X)] 5–8 GB — works on 8 GB unified RAM (tight) or 16 GB recommended
[( )] 32 GB — requires workstation GPU
[( )] 80 GB — requires A100 class GPU

---

**Q2:** The Ollama REST API is compatible with:

[( )] Only Python — no other languages supported
[(X)] Any HTTP client; also drop-in compatible with the OpenAI Python SDK
[( )] Only JavaScript/Node.js environments
[( )] Only VS Code via the Continue extension

---

**Q3:** You are writing Python code that processes pseudonymised student data. You should:

[( )] Enable GitHub Copilot for maximum productivity — cloud services are safe
[(X)] Use Continue + Ollama so no code context containing the data structure leaves your machine
[( )] Use ChatGPT API as it has better code quality
[( )] Disable all AI assistants entirely — they are always unsafe for research code

---

**Q4:** A DGX Spark unit is most appropriate for which scenario in the EduGreenLabs context?

[( )] A single researcher running basic text classification on a laptop
[( )] Publishing aggregate anonymised statistics as OER
[(X)] Running a shared AI endpoint for 20 ECRs with a 27B parameter model, locally within the institution
[( )] Replacing the institution's HPC cluster for large-scale training

---

**Q5:** Which command pulls the default Gemma model in Ollama?

    [[ollama pull gemma:latest]]

---

### 📚 Resources & Links

| Resource | URL |
|----------|-----|
| Ollama Documentation | [ollama.ai/docs](https://ollama.ai/docs) |
| Gemma Model Card (Google) | [ai.google.dev/gemma](https://ai.google.dev/gemma) |
| Continue.dev (VS Code extension) | [continue.dev](https://continue.dev) |
| GitHub Education (free Copilot) | [education.github.com](https://education.github.com) |
| GitHub Copilot for Education Guide | [docs.github.com/copilot](https://docs.github.com/en/copilot) |
| NVIDIA DGX Spark (specs) | [nvidia.com/dgx-spark](https://www.nvidia.com/en-us/project-digits/) |
| Hugging Face Open LLM Leaderboard | [huggingface.co/open-llm-leaderboard](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard) |
| OpenDP — Differential Privacy | [opendp.org](https://opendp.org) |
| EduGreenLabs Workshop Repo | [github.com/edugreenlab/workshop3-deploy](https://github.com/edugreenlab/workshop3-deploy) |

---

### 🧩 Workshop 3 Deliverables

Before leaving today, complete these contributions to the EduGreenLabs project:

- [ ] Add your Green Metric results to the shared log
- [ ] Push your `workshop3_ex.py` solution to the workshop GitHub repo (using a fork + PR)
- [ ] Write a 2-sentence reflection in the shared document: _Which deployment scenario fits your current research project, and why?_
- [ ] Complete the post-workshop survey (link in chat)

---

### ➡️ Connection to WP3: Gamification Sprint (Évora)

The deployment architectures you practiced today will underpin the **WP3 Gamification Sprint** in Évora, where you will:

- Deploy a Gemma-based tutoring agent with gamification mechanics
- Apply low-connectivity design for schools without reliable internet
- Integrate the privacy-by-design principles from Workshop 2 into the prototype architecture

> 📋 **Homework before WP3:** Explore the `llama-cpp-python` library for even lighter inference on resource-constrained devices. Also review the `Phi-3-mini` model from Microsoft — it runs on CPU-only with only 2 GB RAM.

---

_This workshop was produced as an Open Educational Resource under CC BY-SA 4.0 by the EduGreenLabs consortium (EU-GREEN Alliance, OvGU Magdeburg). Funded by the European Union. All code examples are released under MIT Licence._

> **🌿 Green metric:** All AI inference during this workshop was performed locally using Ollama. Estimated CO₂ savings vs. equivalent cloud API usage: **~85%** per participant.

> **Material:**
[Videos of Zoom Presentations](/https://cloud.ovgu.de/s/HQBDJ2BAY6AtYtW)
