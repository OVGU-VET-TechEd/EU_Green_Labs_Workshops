# EduGreenLabs — System Cheat Sheet

> How the scripts, database, AI inference, and green metrics work together.
> All paths are relative to the repository root.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        EduGreenLabs Toolchain                           │
│                                                                         │
│  RAW DATA                                                               │
│  participants.csv  ──►  pseudonymise.py  ──►  pseudonymised_data.csv   │
│                              │                         │                │
│                         PSEUDO_SECRET              workshop3_exercise.py│
│                         (env var, never             (Task 1 / 2 / 3)   │
│                          in the DB)                     │               │
│                                                          ▼              │
│  schema.sql  ──────────────────────────►  PostgreSQL (edugreenlab DB)  │
│  (psql -f schema.sql)                     identity_mapping    [CTRL]    │
│                                           performance_records [TEAM]    │
│                                           consented_pseudonyms          │
│                                           audit_log                     │
│                                           green_log                     │
│                                                │                        │
│                          ┌─────────────────────┘                        │
│                          ▼                                              │
│  ollama serve  ──────►  Ollama daemon (localhost:11434)                 │
│  ollama pull gemma:latest       │                                       │
│                                 │  HTTP REST / OpenAI-compat API        │
│              ┌──────────────────┼──────────────────────┐               │
│              │                  │                       │               │
│    ollama_api_examples.py  workshop3_exercise.py  green_metrics.py      │
│    (8 API patterns)        (Tasks 1‒3 exercise)   (CO₂ measurement)     │
│              │                  │                       │               │
│              └──────────────────┼───────────────────────┘               │
│                                 ▼                                       │
│                         results.csv  (green_log table)                  │
│                         shared CO₂ log for WP2 reporting               │
│                                                                         │
│  DEPLOYMENT LAYER (institutional server):                               │
│  docker-compose.yml  →  ollama container + nginx TLS proxy             │
│                                                                         │
│  FALLBACK (no local GPU):                                               │
│  .devcontainer/setup.sh  →  GitHub Codespaces  (CPU, gemma:2b)         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 0 · Environment Setup

**Required environment variables — set once per session before running anything:**

```bash
# HMAC secret for pseudonymisation (Workshop 2 pipeline)
export PSEUDO_SECRET="$(python3 -c 'import secrets; print(secrets.token_hex(32))')"

# PostgreSQL connection (Workshop 2 database)
export EGL_DB_URL="postgresql://egl_app:yourpassword@localhost:5432/edugreenlab"

# Optional: override Ollama URL (default: localhost:11434)
export OLLAMA_HOST="http://localhost:11434"
```

> **Never commit `PSEUDO_SECRET` to git.** A leaked secret de-anonymises all participants.

**Install all Python dependencies:**

```bash
pip install -r requirements.txt
```

`requirements.txt` installs: `requests`, `openai`, `pandas`, `numpy`,
`psycopg2-binary`, `sqlalchemy`, `cryptography`, `psutil`, `pytest`, `jupyterlab`.

---

## 1 · `pseudonymise.py` — Identity Protection Layer

**What it does:** Converts real identifiers (email, student ID) into stable, keyed tokens using HMAC-SHA256. This is the first step in the data pipeline — no raw identifier ever enters the database.

**How `pseudonymise()` works internally:**

```
PSEUDO_SECRET (env var)  +  real_identifier.strip().lower()
          │                              │
          └──────────  hmac.new(key, msg, sha256)  ──────────────►
                                                    "PID_" + hexdigest[:16].upper()
                                                    e.g. "PID_3A7F2B1C9E04D581"
```

The identifier is normalised (`.strip().lower()`) before hashing, so
`Alice@OVGU.de` and `alice@ovgu.de` always produce the same token.

### CLI — single ID

```bash
python3 pseudonymise.py id --id "alice@ovgu.de"
# Real:   alice@ovgu.de
# Pseudo: PID_3A7F2B1C9E04D581
```

### CLI — CSV batch

```bash
python3 pseudonymise.py csv \
  --input  raw_data.csv \
  --id-col email \
  --output pseudonymised_data.csv \
  --drop   name ip_address device_id
```

The `--drop` flag removes columns before writing — **these fields never appear
in the output CSV**. The output contains `pseudo_id` in place of `email`.

### CLI — verification (round-trip check)

```bash
python3 pseudonymise.py verify \
  --id    "alice@ovgu.de" \
  --pseudo "PID_3A7F2B1C9E04D581"
# ✅ MATCH  (or ❌ NO MATCH)
```

Uses `hmac.compare_digest()` internally to prevent timing attacks.

### As a Python import (used by `workshop3_exercise.py`)

```python
from pseudonymise import pseudonymise, verify_pseudonym, bin_time_of_day, score_to_band

pid   = pseudonymise("alice@ovgu.de")          # → "PID_3A7F2B1C9E04D581"
ok    = verify_pseudonym("alice@ovgu.de", pid)  # → True

tod   = bin_time_of_day(14)    # → "afternoon"   (6–11 = morning, 12–17 = afternoon,
                                #                  18–21 = evening, 22–5 = night)
band  = score_to_band(88.5)    # → "high"         (< 50 = low, 50–74 = mid, ≥ 75 = high)
```

---

## 2 · `schema.sql` — Database Layer

**Apply once to the empty PostgreSQL database:**

```bash
psql -U egl_app -d edugreenlab -f schema.sql
```

### Table map

```
identity_mapping          ← DATA CONTROLLER ONLY (separate system in production)
  pseudo_id  CHAR(20) PK  ← the PID_ token (shared key with research store)
  real_id_hash CHAR(64)   ← HMAC of the real ID (not reversible without secret)
  consent_given BOOLEAN
  consent_date  TIMESTAMPTZ
  consent_scope TEXT[]    ← e.g. {'performance_data', 'survey'}
  withdrawal_date TIMESTAMPTZ    ← Art. 7(3) GDPR
  erasure_request_date TIMESTAMPTZ ← Art. 17 GDPR

performance_records       ← RESEARCH TEAM (read-only via egl_read role)
  pseudo_id  CHAR(20)     ← links to identity_mapping; NOT a FK (different systems)
  session_date DATE        ← date only, no exact time
  time_of_day TEXT         ← 'morning' | 'afternoon' | 'evening' | 'night'
  score_band  TEXT         ← 'low' | 'mid' | 'high' (never raw score)
  task_type   TEXT
  ai_tool_used BOOLEAN
  study_arm   TEXT         ← 'control' | 'treatment_A' etc.

consented_pseudonyms      ← maintained by controller, read by RLS policy
  pseudo_id  CHAR(20) PK
  scope      TEXT[]
  valid_until TIMESTAMPTZ

audit_log                 ← append-only, filled by DB trigger on every SELECT
  accessed_by TEXT
  table_name  TEXT
  pseudo_id   TEXT
  access_ts   TIMESTAMPTZ

green_log                 ← CO₂ records written by green_metrics.py
  pseudo_id       TEXT
  model           TEXT
  tokens          INT
  energy_kwh      FLOAT
  co2_local_g     FLOAT
  co2_saved_pct   FLOAT
  ts              TIMESTAMPTZ
```

### Row-Level Security

```sql
-- Only rows where consent is active are visible to the research team role
ALTER TABLE performance_records ENABLE ROW LEVEL SECURITY;

CREATE POLICY consented_only ON performance_records
  FOR SELECT TO egl_read
  USING (pseudo_id IN (
    SELECT pseudo_id FROM consented_pseudonyms
    WHERE (valid_until IS NULL OR valid_until > NOW())
  ));
```

The research team role (`egl_read`) cannot see records for withdrawn participants —
the RLS policy enforces this at the database engine level, not in application code.

---

## 3 · `workshop3_exercise.py` — Exercise Scaffold (Workshop 3)

This file contains the three coding tasks participants implement during the workshop.
It uses `pseudonymise.py` functions as building blocks and targets the data structures
that feed into `performance_records`.

### Task 1 — `pseudonymise(real_identifier: str) → str`

Participants implement HMAC-SHA256 pseudonymisation from scratch.
- Reads `PSEUDO_SECRET` from env, calls `hmac.new(key, msg, sha256).hexdigest()`
- Returns `"PID_" + hexdigest[:16].upper()`

### Task 2 — `minimise_record(raw_record: dict) → dict`

Transforms a raw LMS export row into a schema-compliant minimised record.

```
Input keys (raw LMS export):        Output keys (4 only — no others):
  email          → pseudonymise()    pseudo_id
  name           → DROPPED           time_of_day  (from login_datetime via bin_time_of_day)
  login_datetime → bin_time_of_day() score_band   (from score via score_to_band)
  score          → score_to_band()   task_type    (kept as-is)
  ip_address     → DROPPED
  device_id      → DROPPED
  task_type      → kept
```

### Task 3 — `check_k_anonymity(records: list[dict], k: int = 3) → list[dict]`

Groups minimised records by `(time_of_day, score_band, task_type)` and flags
any group with fewer than `k` members. Returns a list of risk descriptors:

```python
[{'group': {'time_of_day': 'night', 'score_band': 'low', 'task_type': 'quiz'},
  'count': 1,
  'risk': 'FAIL k-anonymity'}]
```

### Run the test suite

```bash
python3 workshop3_exercise.py
# Runs 25 automated checks across all three tasks.
# Target: all ✅ before moving to the /privacy-check step in Continue.
```

---

## 4 · `ollama_api_examples.py` — AI Inference Patterns

### Start Ollama first

```bash
ollama serve          # starts daemon on localhost:11434
# (already running on macOS app / systemd / Codespaces)
```

### Run all 8 sections

```bash
python3 ollama_api_examples.py
# or one section:
python3 ollama_api_examples.py --section 4 --model gemma:latest
```

### The 8 sections and what they demonstrate

| § | Function | Key concept |
|---|---|---|
| 1 | `section_1_basic_chat()` | `POST /api/chat`, `stream: false`, raw `requests` |
| 2 | `section_2_openai_compatible()` | OpenAI SDK pointed at `localhost:11434/v1` |
| 3 | `section_3_streaming()` | `stream: true`, `iter_lines()` yields tokens live |
| 4 | `section_4_batch()` | Loop over list, low `temperature=0.3` for determinism |
| 5 | `section_5_embeddings()` | `POST /api/embeddings`, cosine similarity, RAG prep |
| 6 | `section_6_model_management()` | `GET /api/tags`, list sizes, CLI cheatsheet |
| 7 | `section_7_research_assistant()` | Multi-turn conversation, persistent system prompt |
| 8 | `section_8_document_analysis()` | Privacy audit + research insights on same document |

### Key API shapes

**Chat (non-streaming):**
```python
requests.post("http://localhost:11434/api/chat", json={
    "model":   "gemma:latest",
    "messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}],
    "stream":  False,
    "options": {"temperature": 0.7, "num_predict": 512}
})
# Response: .json()["message"]["content"]  ← the reply text
#           .json()["eval_count"]          ← tokens generated
#           .json()["prompt_eval_count"]   ← prompt tokens
```

**Embeddings:**
```python
requests.post("http://localhost:11434/api/embeddings", json={
    "model":  "nomic-embed-text",
    "prompt": "text to embed"
})
# Response: .json()["embedding"]  ← list[float], length = model dim
```

**OpenAI SDK (identical thereafter):**
```python
from openai import OpenAI
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
# Switch to cloud: base_url="https://api.openai.com/v1", api_key=os.environ["OPENAI_API_KEY"]
```

### Multi-turn conversation pattern (§7)

Each turn appends the assistant reply to the `messages` list and sends the full
history in the next request. Ollama has no session memory — the full context is
the only memory:

```python
conversation = [{"role": "system", "content": SYSTEM_PROMPT}]
for user_msg in turns:
    conversation.append({"role": "user", "content": user_msg})
    reply = call_ollama(conversation)          # sends full list every time
    conversation.append({"role": "assistant", "content": reply})
```

---

## 5 · `green_metrics.py` — CO₂ Measurement Layer

### CLI usage

```bash
# Single prompt, default hardware (65 W laptop, Germany grid)
python3 green_metrics.py --prompt "Explain data minimisation in 3 bullet points."

# Full 4-prompt benchmark suite
python3 green_metrics.py --benchmark

# Benchmark + export for the shared EduGreenLabs CO₂ log
python3 green_metrics.py --benchmark --export results.csv

# Specify your actual hardware
python3 green_metrics.py --benchmark --tdp 15 --country PT   # Apple M2, Portugal
python3 green_metrics.py --benchmark --tdp 1000 --country DE  # DGX Spark, Germany

# List all available country grid intensities
python3 green_metrics.py --list-countries
```

### How `measure()` calculates CO₂

```python
measure(
    prompt             = "...",
    model              = "gemma:latest",
    country            = "DE",          # grid intensity lookup
    hardware_tdp_watts = 65.0,          # your hardware's TDP in watts
    assumed_load_pct   = 0.5,           # 50 % of TDP during inference
    max_tokens         = 512,
)
```

The calculation chain inside `measure()`:

```
1. Call run_inference() → starts timer, POSTs to Ollama, stops timer
2. elapsed_sec = time.time() - start
3. active_power_w = hardware_tdp_watts × assumed_load_pct
4. energy_wh     = active_power_w × (elapsed_sec / 3600)
5. energy_kwh    = energy_wh / 1000
6. co2_local_g   = energy_kwh × CARBON_INTENSITY[country]
7. cloud_kwh     = total_tokens × CLOUD_ENERGY_PER_1K_TOKENS_KWH / 1000
8. co2_cloud_g   = cloud_kwh × CARBON_INTENSITY["US"]      ← US data-centre estimate
9. co2_saved_pct = (co2_cloud_g - co2_local_g) / co2_cloud_g × 100
```

### Grid intensity reference (from `CARBON_INTENSITY` dict)

| Code | Country | g CO₂/kWh |
|---|---|---|
| `SE` | Sweden | 20 |
| `FR` | France | 50 |
| `FI` | Finland | 80 |
| `PT` | Portugal | 130 |
| `DK` | Denmark | 130 |
| `DE` | Germany | 400 |
| `RO` | Romania | 340 |
| `PL` | Poland | 750 |
| `EU` | EU average | 300 |
| `US` | US (cloud baseline) | 400 |

### `InferenceMetrics` dataclass — all fields

```python
@dataclass
class InferenceMetrics:
    timestamp          # ISO 8601 string
    model              # e.g. "gemma:latest"
    prompt_preview     # first 60 chars of prompt
    prompt_tokens      # from Ollama's prompt_eval_count
    gen_tokens         # from Ollama's eval_count
    total_tokens       # prompt + gen
    elapsed_sec        # wall-clock seconds
    tokens_per_sec     # gen_tokens / elapsed_sec
    hardware_tdp_w     # your --tdp value
    assumed_load_pct   # your --load value (default 0.5)
    energy_wh          # computed
    energy_kwh         # computed
    country            # your --country code
    grid_intensity     # g CO₂/kWh for that country
    co2_local_g        # local inference footprint
    co2_cloud_g        # cloud equivalent estimate
    co2_saved_g        # absolute saving
    co2_saved_pct      # % reduction — project target: ≥ 25 %
    response_preview   # first 100 chars of reply
```

### Write a result to the database

```python
import psycopg2, os
from green_metrics import measure

m = measure("Explain k-anonymity.", country="DE", hardware_tdp_watts=65)

conn = psycopg2.connect(os.environ["EGL_DB_URL"])
with conn.cursor() as cur:
    cur.execute("""
        INSERT INTO green_log
            (pseudo_id, model, tokens, energy_kwh, co2_local_g, co2_saved_pct, ts)
        VALUES (%s, %s, %s, %s, %s, %s, NOW())
    """, ("PID_ANONYMOUS", m.model, m.gen_tokens,
          m.energy_kwh, m.co2_local_g, m.co2_saved_pct))
conn.commit()
```

### Benchmark prompts (the 4-task suite)

| Label | Max tokens | Purpose |
|---|---|---|
| "Short factual" | 60 | Baseline speed / energy per token |
| "Medium explanation" | 200 | GDPR pseudo vs. anonymisation |
| "Research advice" | 400 | Multi-constraint reasoning |
| "Code generation" | 300 | Python function with type hints |

---

## 6 · Deployment: `docker-compose.yml` + `nginx.conf`

For institutional servers (DGX Spark, shared HPC node) rather than a laptop.

### Start the full stack

```bash
docker compose up -d
docker compose ps                          # check health status
docker compose logs ollama                 # tail Ollama logs
```

### Pull models after the stack is healthy

```bash
docker compose exec ollama ollama pull gemma:latest
docker compose exec ollama ollama pull nomic-embed-text
# For DGX Spark (uncomment in docker-compose.yml first):
docker compose exec ollama ollama pull gemma2:27b
```

### Service map

```
Port 80  → nginx  → redirect to 443
Port 443 → nginx  → TLS termination → proxy_pass → ollama:11434 (internal)
Port 11434 (internal only, bound to 127.0.0.1 on host)
```

### Key Ollama environment variables (set in `docker-compose.yml`)

```yaml
OLLAMA_NUM_PARALLEL=8          # concurrent requests (tune to GPU VRAM)
OLLAMA_MAX_LOADED_MODELS=4     # models kept hot in VRAM
OLLAMA_FLASH_ATTENTION=1       # reduces VRAM for long contexts
OLLAMA_KEEP_ALIVE=5m           # model eviction timeout
```

### Model storage volume

```yaml
volumes:
  ollama_models:
    device: /data/ollama-models   # ← change to your NVMe path
```

Models are large (5–40 GB each). Point `device` at fast dedicated storage,
not the OS disk.

### TLS certificate setup (self-signed for testing)

```bash
mkdir -p certs
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout certs/key.pem -out certs/cert.pem \
  -subj "/CN=ai-research.your-uni.de"
docker compose up -d
```

---

## 7 · Codespaces Fallback: `.devcontainer/setup.sh`

For participants without a local GPU. The script runs automatically on container
creation and performs four steps:

```
[1/4] pip install -r requirements.txt
[2/4] curl | sh → ollama install → ollama serve & (background PID saved)
      polls http://localhost:11434/api/version every 1s (up to 30s)
[3/4] ollama pull gemma:2b           ← 2B not latest (CPU speed limit)
[4/4] cp workshop3/setup/continue_config.json ~/.continue/config.json
      sed replaces "gemma:latest" → "gemma:2b" in config
```

After the container is ready, `ollama_api_examples.py`, `green_metrics.py`, and
`workshop3_exercise.py` all work identically to the local setup — just slower
(~2 tok/s CPU-only vs. ~18+ tok/s on a GPU laptop).

---

## 8 · End-to-End Workflow (Workshop Day)

```bash
# ── 0. One-time setup ─────────────────────────────────────────────
pip install -r requirements.txt
export PSEUDO_SECRET="$(python3 -c 'import secrets; print(secrets.token_hex(32))')"
export EGL_DB_URL="postgresql://egl_app:pw@localhost:5432/edugreenlab"

# ── 1. Start AI daemon ────────────────────────────────────────────
ollama serve &             # or: the Ollama app / systemd
ollama pull gemma:latest   # skip if already done

# ── 2. Apply database schema (Workshop 2) ─────────────────────────
psql -U egl_app -d edugreenlab -f schema.sql

# ── 3. Pseudonymise raw participant data ──────────────────────────
python3 pseudonymise.py csv \
  --input raw_data.csv --id-col email \
  --output pseudonymised.csv --drop name ip_address device_id

# ── 4. Minimise + validate k-anonymity (Workshop 3 exercise) ──────
python3 workshop3_exercise.py    # implement tasks 1‒3, then run tests

# ── 5. Explore all AI API patterns ────────────────────────────────
python3 ollama_api_examples.py

# ── or one section at a time:
python3 ollama_api_examples.py --section 4   # batch GDPR classification
python3 ollama_api_examples.py --section 7   # multi-turn research assistant
python3 ollama_api_examples.py --section 8   # privacy audit on your document

# ── 6. Measure your CO₂ footprint ─────────────────────────────────
python3 green_metrics.py --benchmark --country DE --tdp 65 --export results.csv

# ── 7. Share results ──────────────────────────────────────────────
# Add results.csv rows to the shared green_log table, or upload the CSV
# to the workshop shared drive for collective WP2 CO₂ tracking.
```

---

## 9 · Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `PSEUDO_SECRET is not set` | Env var missing | `export PSEUDO_SECRET="..."` before running |
| `ConnectionError: localhost:11434` | Ollama not running | `ollama serve` in a separate terminal |
| Inference < 1 tok/s | CPU-only mode | Normal on machines without GPU — use `gemma:2b` |
| `psycopg2.OperationalError` | DB not running or wrong URL | Check `EGL_DB_URL`, `sudo systemctl start postgresql` |
| `RLS blocks all rows` | No active consent rows in `consented_pseudonyms` | Insert a consent record for your test `pseudo_id` |
| `ollama pull` hangs | DNS issue | `echo "1.1.1.1" >> /etc/resolv.conf` |
| Codespaces: model too slow | CPU inference, gemma:latest | `setup.sh` auto-selects `gemma:2b` — intended |
| Docker: GPU not detected | Missing NVIDIA Container Toolkit | Install from [docs.nvidia.com](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit) |
| `hmac.compare_digest` type error | Passing `str` not `bytes` | `.encode("utf-8")` both arguments |

---

*EduGreenLabs · EU-GREEN University Alliance · OvGU Magdeburg · MIT / CC BY-SA 4.0*
