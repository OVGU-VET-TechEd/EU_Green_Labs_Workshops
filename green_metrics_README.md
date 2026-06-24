**Overview**
- **Purpose:** Concise usage notes for [green_metrics.py](green_metrics.py), the EduGreenLabs script that measures energy and CO₂ for local Ollama inference.

**Prerequisites**
- **Ollama:** Local Ollama server running and reachable at `http://localhost:11434` (start with `ollama serve`).
- **Python:** Python 3.9+ and the `requests` package (installed via `pip install -r requirements.txt`).

**Quick Start**
- **Single prompt:** Measure one prompt from the CLI.

```bash
python3 green_metrics.py --prompt "Explain data minimisation in 3 points."
```

- **Run benchmark suite:** Use the built-in benchmark prompts.

```bash
python3 green_metrics.py --benchmark
```

- **Use the JSON input file:** Run multiple prompts defined in a JSON array.

```bash
python3 green_metrics.py --input green_metrics_example_input.json
```

- **Export results to CSV:** Add `--export results.csv` to append results to a CSV file.

```bash
python3 green_metrics.py --input green_metrics_example_input.json --export results.csv
```

**JSON Input Format**
- **File:** Use a JSON array of objects (see [green_metrics_example_input.json](green_metrics_example_input.json)).
- **Supported fields per entry:** `prompt` (required), `max_tokens`, `country`, `hardware_tdp_watts`, `assumed_load_pct`, `system`, `model`.

Example entry:

```json
{
  "label": "Short factual",
  "prompt": "What is data minimisation? One sentence.",
  "max_tokens": 60,
  "country": "DE",
  "hardware_tdp_watts": 65,
  "assumed_load_pct": 0.5
}
```

**CLI Options (high level)**
- **`--prompt`**: single prompt to measure.
- **`--input`**: path to a JSON file with prompt entries.
- **`--benchmark`**: run the built-in benchmark suite.
- **`--export`**: path to CSV file to append results.
- **`--tdp` / `--load` / `--country` / `--model`**: override hardware/country/model defaults.

**Notes & Troubleshooting**
- **Connection error:** If the script prints `Ollama is not running`, start Ollama with `ollama serve` and retry.
- **Grid intensities:** Edit `CARBON_INTENSITY` in [green_metrics.py](green_metrics.py) to update country values.
- **Dry-run idea:** If you want to test parsing without contacting Ollama, open the JSON file and validate with `python -m json.tool green_metrics_example_input.json`.

**Files**
- [green_metrics.py](green_metrics.py) — main script
- [green_metrics_example_input.json](green_metrics_example_input.json) — example input

If you'd like, I can add a small unit test or a `--dry-run` mode to validate inputs without calling Ollama. Reply with which you'd prefer.
