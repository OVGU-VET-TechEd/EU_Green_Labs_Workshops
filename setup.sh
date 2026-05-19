#!/usr/bin/env bash
# .devcontainer/setup.sh
# ──────────────────────────────────────────────────────────────────
# EduGreenLabs Workshop 3 — Codespaces / devcontainer setup
# Runs once after the container is created.
# ──────────────────────────────────────────────────────────────────

set -euo pipefail

echo "=== EduGreenLabs Workshop 3 — Dev Environment Setup ==="
echo ""

# ── Python dependencies ──────────────────────────────────────────
echo "[1/4] Installing Python dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
echo "       ✅ Python dependencies installed"

# ── Ollama (CPU-only in Codespaces — no GPU) ─────────────────────
echo "[2/4] Installing Ollama..."
curl -fsSL https://ollama.ai/install.sh | sh >/dev/null 2>&1 || {
    echo "       ⚠️  Ollama install failed — trying manual binary install..."
    curl -fsSL https://github.com/ollama/ollama/releases/latest/download/ollama-linux-amd64 \
         -o /usr/local/bin/ollama
    chmod +x /usr/local/bin/ollama
}

# Start Ollama in background
ollama serve >/dev/null 2>&1 &
OLLAMA_PID=$!
echo "       ✅ Ollama service started (PID: $OLLAMA_PID)"

# Wait for Ollama to be ready
echo "       Waiting for Ollama to be ready..."
for i in $(seq 1 30); do
    if curl -sf http://localhost:11434/api/version >/dev/null 2>&1; then
        echo "       ✅ Ollama is ready"
        break
    fi
    sleep 1
done

# ── Pull lightweight model for Codespaces (CPU inference) ─────────
echo "[3/4] Pulling Gemma 2B (lightweight for CPU-only Codespaces)..."
echo "       (gemma:latest is too slow for CPU-only — use 2B for learning the API)"
if ollama pull gemma:2b >/dev/null 2>&1; then
    echo "       ✅ gemma:2b ready"
else
    echo "       ⚠️  Model pull failed — pull manually: ollama pull gemma:2b"
fi

# ── Continue.dev config ───────────────────────────────────────────
echo "[4/4] Configuring Continue.dev..."
mkdir -p ~/.continue
if [ ! -f ~/.continue/config.json ]; then
    cp workshop3/setup/continue_config.json ~/.continue/config.json
    # Update the model in config to use 2B for Codespaces
    sed -i 's/"model": "gemma:latest"/"model": "gemma:2b"/g' ~/.continue/config.json
    echo "       ✅ Continue.dev configured (using gemma:2b for Codespaces)"
else
    echo "       ℹ️  Continue.dev config already exists — not overwritten"
fi

# ── Final message ─────────────────────────────────────────────────
echo ""
echo "=== Setup complete! ==="
echo ""
echo "  Ollama API:   http://localhost:11434"
echo "  Model:        gemma:2b (CPU-only, ~2 tok/s — enough for API learning)"
echo ""
echo "  ⚠️  NOTE: Codespaces uses CPU inference only."
echo "  For real workshop tasks, use your local machine with Ollama."
echo "  See: workshop3/setup/install_ollama.sh"
echo ""
echo "  Quick test:"
echo "    ollama run gemma:2b 'Hello! Are you running locally in a Codespace?'"
echo ""
echo "  Python API test:"
echo "    python3 workshop3/code/ollama_api_examples.py --section 1 --model gemma:2b"
echo ""
echo "  Green metrics:"
echo "    python3 workshop3/code/green_metrics.py --benchmark --model gemma:2b --country EU --tdp 200"
echo ""
