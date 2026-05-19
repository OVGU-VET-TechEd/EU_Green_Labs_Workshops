#!/usr/bin/env bash
# ==============================================================
# install_ollama.sh
# EduGreenLabs Workshop 3 — AI Implementation Sprint
#
# One-script installer for Ollama + Gemma models.
# Tested on: macOS 13+, Ubuntu 22.04, Debian 12, WSL2 (Ubuntu)
#
# Usage:
#   chmod +x install_ollama.sh
#   ./install_ollama.sh [--model gemma:latest] [--small] [--all]
#
# Options:
#   --model NAME   Pull a specific model (default: gemma:latest)
#   --small        Also pull gemma:2b (for 8 GB RAM machines)
#   --all          Pull gemma:2b, gemma:latest, and gemma2:27b
#   --skip-model   Install Ollama only, skip model download
#   --help         Show this help
#
# Licence: MIT · EduGreenLabs / OvGU Magdeburg · EU-GREEN Alliance
# ==============================================================

set -euo pipefail

# ── Colour output ────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; BOLD='\033[1m'; NC='\033[0m'

info()    { echo -e "${BLUE}[INFO]${NC}  $*"; }
success() { echo -e "${GREEN}[OK]${NC}    $*"; }
warn()    { echo -e "${YELLOW}[WARN]${NC}  $*"; }
error()   { echo -e "${RED}[ERROR]${NC} $*" >&2; exit 1; }
header()  { echo -e "\n${BOLD}$*${NC}"; }

# ── Defaults ─────────────────────────────────────────────────────
MODELS=("gemma:latest")
SKIP_MODEL=false

# ── Argument parsing ─────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
    case "$1" in
        --model)    MODELS=("$2"); shift 2 ;;
        --small)    MODELS=("gemma:2b" "gemma:latest"); shift ;;
        --all)      MODELS=("gemma:2b" "gemma:latest" "gemma2:27b"); shift ;;
        --skip-model) SKIP_MODEL=true; shift ;;
        --help)
            sed -n '3,25p' "$0" | sed 's/^# //;s/^#//'
            exit 0
            ;;
        *) warn "Unknown argument: $1"; shift ;;
    esac
done

# ── Banner ───────────────────────────────────────────────────────
echo -e "${BOLD}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║   EduGreenLabs Workshop 3 — Ollama + Gemma Installer    ║"
echo "║   EU-GREEN University Alliance · OvGU Magdeburg          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# ── Detect OS ────────────────────────────────────────────────────
header "1/4 · Detecting environment"

OS="$(uname -s)"
ARCH="$(uname -m)"
info "OS: $OS | Architecture: $ARCH"

if [[ "$OS" == "Darwin" ]]; then
    PLATFORM="macos"
elif [[ "$OS" == "Linux" ]]; then
    if grep -qi microsoft /proc/version 2>/dev/null; then
        PLATFORM="wsl2"
        info "Detected WSL2 environment"
    else
        PLATFORM="linux"
    fi
else
    error "Unsupported OS: $OS. Please install Ollama manually from https://ollama.ai"
fi

# ── Check RAM ────────────────────────────────────────────────────
header "2/4 · Checking hardware"

if [[ "$PLATFORM" == "macos" ]]; then
    RAM_BYTES=$(sysctl -n hw.memsize)
    RAM_GB=$(( RAM_BYTES / 1024 / 1024 / 1024 ))
else
    RAM_KB=$(grep MemTotal /proc/meminfo | awk '{print $2}')
    RAM_GB=$(( RAM_KB / 1024 / 1024 ))
fi

info "Available RAM: ~${RAM_GB} GB"

if (( RAM_GB < 8 )); then
    warn "Less than 8 GB RAM detected. gemma:latest may be slow or fail."
    warn "Consider using gemma:2b (~1.4 GB) instead: ./install_ollama.sh --model gemma:2b"
elif (( RAM_GB < 16 )); then
    warn "8–15 GB RAM: gemma:latest will work but close all other apps."
    success "RAM is sufficient for gemma:latest (Q4 quantisation requires ~5 GB)"
else
    success "RAM is comfortable for gemma:latest (16+ GB)"
fi

# Check for GPU (Linux/WSL2)
if [[ "$PLATFORM" != "macos" ]] && command -v nvidia-smi &>/dev/null; then
    VRAM=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits | head -1)
    success "NVIDIA GPU detected: ${VRAM} MB VRAM"
    if (( VRAM >= 8000 )); then
        success "GPU acceleration available — inference will be fast"
    else
        warn "GPU VRAM < 8 GB — Ollama will use CPU for gemma:latest"
    fi
elif [[ "$PLATFORM" == "macos" ]] && system_profiler SPDisplaysDataType 2>/dev/null | grep -q "Metal"; then
    success "Apple Silicon detected — Metal GPU acceleration available"
fi

# ── Install Ollama ───────────────────────────────────────────────
header "3/4 · Installing Ollama"

if command -v ollama &>/dev/null; then
    CURRENT_VERSION=$(ollama --version 2>/dev/null | awk '{print $NF}' || echo "unknown")
    success "Ollama is already installed (version: $CURRENT_VERSION)"
    info "To upgrade: curl -fsSL https://ollama.ai/install.sh | sh"
else
    info "Downloading and installing Ollama..."

    if [[ "$PLATFORM" == "macos" ]]; then
        if command -v brew &>/dev/null; then
            brew install ollama
        else
            info "Homebrew not found. Please download the macOS installer from:"
            info "  https://ollama.ai/download/mac"
            info "Or install Homebrew first: https://brew.sh"
            error "Cannot auto-install on macOS without Homebrew"
        fi
    elif [[ "$PLATFORM" == "linux" || "$PLATFORM" == "wsl2" ]]; then
        curl -fsSL https://ollama.ai/install.sh | sh
    fi

    # Verify installation
    if command -v ollama &>/dev/null; then
        NEW_VERSION=$(ollama --version 2>/dev/null | awk '{print $NF}' || echo "unknown")
        success "Ollama installed successfully (version: $NEW_VERSION)"
    else
        error "Ollama installation failed. Please install manually: https://ollama.ai"
    fi
fi

# Start Ollama service if not running
if ! curl -s http://localhost:11434/api/version &>/dev/null; then
    info "Starting Ollama service..."
    if [[ "$PLATFORM" == "linux" ]] && systemctl is-enabled ollama &>/dev/null 2>&1; then
        sudo systemctl start ollama
    else
        ollama serve &>/dev/null &
        sleep 3
    fi
    if curl -s http://localhost:11434/api/version &>/dev/null; then
        success "Ollama service is running on http://localhost:11434"
    else
        warn "Could not verify Ollama is running. Start it manually: ollama serve"
    fi
else
    success "Ollama service is already running"
fi

# ── Pull models ──────────────────────────────────────────────────
if [[ "$SKIP_MODEL" == "false" ]]; then
    header "4/4 · Downloading models"
    info "This may take several minutes depending on your connection."
    info "Models are cached at ~/.ollama/models — you only download once."
    echo ""

    for MODEL in "${MODELS[@]}"; do
        info "Pulling ${MODEL}..."
        if ollama pull "$MODEL"; then
            success "Model pulled: $MODEL"
        else
            warn "Failed to pull $MODEL — you can retry with: ollama pull $MODEL"
        fi
        echo ""
    done
else
    header "4/4 · Skipping model download (--skip-model)"
    info "Pull models manually: ollama pull gemma:latest"
fi

# ── Final verification ───────────────────────────────────────────
echo ""
header "✅ Installation complete"
echo ""
echo "List downloaded models:"
ollama list
echo ""
echo -e "${BOLD}Quick test:${NC}"
echo "  ollama run gemma:latest \"Hello! Confirm you are running locally.\""
echo ""
echo -e "${BOLD}Python API test:${NC}"
echo "  python3 -c \""
echo "  import requests"
echo "  r = requests.post('http://localhost:11434/api/chat',"
echo "      json={'model':'gemma:latest','messages':[{'role':'user','content':'Hello!'}],'stream':False})"
echo "  print(r.json()['message']['content'])\""
echo ""
echo -e "${BOLD}VS Code setup:${NC}"
echo "  Install the 'Continue' extension → configure with setup/continue_config.json"
echo ""
echo -e "${GREEN}🌿 EduGreenLabs Green Metric:${NC}"
echo "  Run code/green_metrics.py after your first inference to log your CO₂ footprint."
echo ""
echo -e "Repository: ${BLUE}https://github.com/OVGU-VET-TechEd/EU_Green_Labs_Workshops${NC}"
