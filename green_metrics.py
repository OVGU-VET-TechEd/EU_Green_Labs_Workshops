"""
green_metrics.py
────────────────
EduGreenLabs Workshop 3 — AI Implementation Sprint

Measure and log the energy consumption and CO₂ footprint of local
Ollama inference calls. Contributes to the EduGreenLabs carbon log
and validates the project's ≥ 25 % CO₂ reduction target.

Usage
-----
    # Single prompt measurement
    python3 green_metrics.py --prompt "Explain data minimisation in 3 points."

    # Run the full workshop benchmark suite
    python3 green_metrics.py --benchmark

    # Export results to CSV (for the shared EduGreenLabs log)
    python3 green_metrics.py --benchmark --export results.csv

    # Specify your hardware TDP (default: 65 W laptop CPU)
    python3 green_metrics.py --benchmark --tdp 15   # Apple M2
    python3 green_metrics.py --benchmark --tdp 1000 # DGX Spark

Licence: MIT · EduGreenLabs / OvGU Magdeburg · EU-GREEN Alliance
"""

import argparse
import csv
import json
import os
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional

import requests

OLLAMA_BASE = "http://localhost:11434"
DEFAULT_MODEL = "gemma:latest"

# ──────────────────────────────────────────────────────────────────
# EU national grid carbon intensity (gCO₂eq / kWh)
# Source: Ember Climate, 2024 European Electricity Review
# Update these values annually from: https://ember-climate.org/data/
# ──────────────────────────────────────────────────────────────────
CARBON_INTENSITY: dict[str, float] = {
    "AT": 100,   # Austria        — high hydro/wind share
    "BE": 150,   # Belgium
    "DE": 400,   # Germany        — significant coal/gas still present
    "DK": 130,   # Denmark        — high wind share
    "ES": 170,   # Spain
    "FI": 80,    # Finland        — nuclear + hydro
    "FR": 50,    # France         — nuclear dominant
    "HR": 160,   # Croatia
    "HU": 200,   # Hungary
    "IT": 250,   # Italy
    "NL": 270,   # Netherlands
    "PL": 750,   # Poland         — still coal-heavy
    "PT": 130,   # Portugal       — high hydro/wind
    "RO": 340,   # Romania
    "SE": 20,    # Sweden         — nuclear + hydro
    "SI": 210,   # Slovenia
    "EU": 300,   # EU average
    "US": 400,   # US average     — for cloud comparison
    "GLOBAL": 475,  # Global average
}

# Reference: cloud AI API carbon estimate (GPT-4 class)
# Rough estimate based on published data centre PUE and US grid mix
# Source: Patterson et al. (2022), Lottick et al. (2019)
CLOUD_ENERGY_PER_1K_TOKENS_KWH = 0.001   # ~1 Wh per 1000 tokens


@dataclass
class InferenceMetrics:
    """Stores all metrics for a single inference call."""
    timestamp:          str
    model:              str
    prompt_preview:     str   # first 60 chars of prompt
    prompt_tokens:      int
    gen_tokens:         int
    total_tokens:       int
    elapsed_sec:        float
    tokens_per_sec:     float
    hardware_tdp_w:     float
    assumed_load_pct:   float
    energy_wh:          float
    energy_kwh:         float
    country:            str
    grid_intensity:     float
    co2_local_g:        float
    co2_cloud_g:        float
    co2_saved_g:        float
    co2_saved_pct:      float
    response_preview:   str   # first 100 chars of response


def run_inference(
    prompt: str,
    model: str = DEFAULT_MODEL,
    system: str = "",
    temperature: float = 0.7,
    max_tokens: int = 512,
) -> dict:
    """Run a single Ollama inference and return the raw response dict."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens,
        }
    }
    response = requests.post(
        f"{OLLAMA_BASE}/api/chat",
        json=payload,
        timeout=300
    )
    response.raise_for_status()
    return response.json()


def measure(
    prompt: str,
    model: str = DEFAULT_MODEL,
    system: str = "",
    country: str = "EU",
    hardware_tdp_watts: float = 65.0,
    assumed_load_pct: float = 0.5,
    temperature: float = 0.7,
    max_tokens: int = 512,
    verbose: bool = True,
) -> InferenceMetrics:
    """
    Measure the energy and CO₂ footprint of a single inference call.

    Parameters
    ----------
    prompt : str
        The user prompt.
    model : str
        Ollama model name.
    system : str
        Optional system prompt.
    country : str
        ISO 2-letter country code (for grid carbon intensity lookup).
    hardware_tdp_watts : float
        Thermal Design Power of your hardware in watts.
        Typical values: 15 (Apple M2), 45 (laptop CPU), 65 (desktop CPU),
                        300 (laptop+GPU), 1000 (DGX Spark peak).
    assumed_load_pct : float
        Fraction of TDP assumed during inference (0.3–0.8 typical).
    verbose : bool
        Print the results to stdout.

    Returns
    -------
    InferenceMetrics
    """
    grid_g_kwh = CARBON_INTENSITY.get(country.upper(), CARBON_INTENSITY["EU"])

    start = time.time()
    data = run_inference(prompt, model, system, temperature, max_tokens)
    elapsed = time.time() - start

    prompt_tokens = data.get("prompt_eval_count", 0)
    gen_tokens    = data.get("eval_count", 0)
    total_tokens  = prompt_tokens + gen_tokens
    tok_per_sec   = gen_tokens / elapsed if elapsed > 0 else 0

    # Energy: TDP × load_fraction × time_in_hours → kWh
    active_power_w = hardware_tdp_watts * assumed_load_pct
    energy_wh      = active_power_w * (elapsed / 3600)
    energy_kwh     = energy_wh / 1000

    # CO₂ — local inference
    co2_local_g = energy_kwh * grid_g_kwh

    # CO₂ — equivalent cloud API call (US data centre estimate)
    cloud_energy_kwh = total_tokens * CLOUD_ENERGY_PER_1K_TOKENS_KWH / 1000
    co2_cloud_g      = cloud_energy_kwh * CARBON_INTENSITY.get("US", 400)

    # Savings
    co2_saved_g   = max(0, co2_cloud_g - co2_local_g)
    co2_saved_pct = (co2_saved_g / co2_cloud_g * 100) if co2_cloud_g > 0 else 0

    response_text = data.get("message", {}).get("content", "")

    metrics = InferenceMetrics(
        timestamp          = datetime.now().isoformat(),
        model              = model,
        prompt_preview     = prompt[:60].replace("\n", " "),
        prompt_tokens      = prompt_tokens,
        gen_tokens         = gen_tokens,
        total_tokens       = total_tokens,
        elapsed_sec        = round(elapsed, 2),
        tokens_per_sec     = round(tok_per_sec, 1),
        hardware_tdp_w     = hardware_tdp_watts,
        assumed_load_pct   = assumed_load_pct,
        energy_wh          = round(energy_wh, 6),
        energy_kwh         = round(energy_kwh, 8),
        country            = country.upper(),
        grid_intensity     = grid_g_kwh,
        co2_local_g        = round(co2_local_g, 6),
        co2_cloud_g        = round(co2_cloud_g, 6),
        co2_saved_g        = round(co2_saved_g, 6),
        co2_saved_pct      = round(co2_saved_pct, 1),
        response_preview   = response_text[:100].replace("\n", " "),
    )

    if verbose:
        print_metrics(metrics)

    return metrics


def print_metrics(m: InferenceMetrics) -> None:
    """Pretty-print a metrics object to stdout."""
    print("\n" + "─" * 60)
    print(f"  🌿 EduGreenLabs Green Metric Report")
    print("─" * 60)
    print(f"  Timestamp:       {m.timestamp}")
    print(f"  Model:           {m.model}")
    print(f"  Prompt:          {m.prompt_preview}...")
    print()
    print(f"  Tokens generated: {m.gen_tokens}")
    print(f"  Speed:            {m.tokens_per_sec} tok/s")
    print(f"  Time:             {m.elapsed_sec}s")
    print()
    print(f"  Hardware TDP:    {m.hardware_tdp_w}W × {m.assumed_load_pct*100:.0f}% load")
    print(f"  Energy used:     {m.energy_wh*1000:.4f} mWh ({m.energy_kwh:.8f} kWh)")
    print(f"  Grid intensity:  {m.grid_intensity} gCO₂/kWh ({m.country})")
    print()
    print(f"  CO₂ — local:     {m.co2_local_g*1000:.4f} mgCO₂")
    print(f"  CO₂ — cloud est: {m.co2_cloud_g*1000:.4f} mgCO₂")
    print(f"  CO₂ saved:       {m.co2_saved_g*1000:.4f} mgCO₂  ({m.co2_saved_pct:.1f}%)")
    print()
    print(f"  Response:        {m.response_preview}...")
    print("─" * 60)


def export_to_csv(results: list[InferenceMetrics], filepath: str) -> None:
    """Export metrics to a CSV file for the shared EduGreenLabs log."""
    if not results:
        return

    fieldnames = list(asdict(results[0]).keys())
    mode = "a" if os.path.exists(filepath) else "w"

    with open(filepath, mode, newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if mode == "w":
            writer.writeheader()
        for r in results:
            writer.writerow(asdict(r))

    print(f"\n✅ Results appended to: {filepath}")
    print(f"   Share this file in the workshop for collective CO₂ tracking.")


# ──────────────────────────────────────────────────────────────────
# Benchmark suite
# ──────────────────────────────────────────────────────────────────

BENCHMARK_PROMPTS = [
    {
        "label": "Short factual",
        "prompt": "What is data minimisation? One sentence.",
        "max_tokens": 60,
    },
    {
        "label": "Medium explanation",
        "prompt": "Explain the difference between pseudonymisation and anonymisation under GDPR in 3 bullet points.",
        "max_tokens": 200,
    },
    {
        "label": "Research advice",
        "prompt": (
            "I am running a 3-month study on AI-assisted writing in PhD programmes "
            "across 3 EU universities. What are the top 5 GDPR considerations I must address?"
        ),
        "max_tokens": 400,
    },
    {
        "label": "Code generation",
        "prompt": "Write a Python function that bins an exact datetime into time-of-day categories (morning/afternoon/evening/night). Include type hints and a docstring.",
        "max_tokens": 300,
    },
]


def run_benchmark(
    model: str = DEFAULT_MODEL,
    country: str = "DE",
    hardware_tdp_watts: float = 65.0,
) -> list[InferenceMetrics]:
    """Run the standard EduGreenLabs benchmark suite."""
    print(f"\n{'═'*60}")
    print(f"  EduGreenLabs Benchmark Suite")
    print(f"  Model: {model} | Country: {country} | TDP: {hardware_tdp_watts}W")
    print(f"{'═'*60}")

    results = []
    for i, task in enumerate(BENCHMARK_PROMPTS, 1):
        print(f"\n[{i}/{len(BENCHMARK_PROMPTS)}] {task['label']}")
        m = measure(
            prompt=task["prompt"],
            model=model,
            country=country,
            hardware_tdp_watts=hardware_tdp_watts,
            max_tokens=task["max_tokens"],
        )
        results.append(m)

    # Summary
    total_tokens  = sum(r.gen_tokens for r in results)
    total_energy  = sum(r.energy_wh for r in results)
    total_co2     = sum(r.co2_local_g for r in results)
    total_saved   = sum(r.co2_saved_g for r in results)
    avg_speed     = sum(r.tokens_per_sec for r in results) / len(results)

    print(f"\n{'═'*60}")
    print(f"  BENCHMARK SUMMARY")
    print(f"{'─'*60}")
    print(f"  Total tokens generated: {total_tokens}")
    print(f"  Average speed:          {avg_speed:.1f} tok/s")
    print(f"  Total energy:           {total_energy*1000:.3f} mWh")
    print(f"  Total CO₂ (local):      {total_co2*1000:.3f} mgCO₂")
    print(f"  Total CO₂ saved vs cloud: {total_saved*1000:.3f} mgCO₂")
    print(f"  CO₂ reduction:          {(total_saved / (total_co2 + total_saved)) * 100:.1f}%")
    print(f"{'═'*60}\n")

    return results


def run_from_json(filepath: str, model: str = DEFAULT_MODEL) -> list[InferenceMetrics]:
    """Load a JSON array of prompt entries and measure each one.

    Expected entry fields (per item):
      - prompt (str)               required
      - max_tokens (int)           optional
      - country (str)              optional
      - hardware_tdp_watts (float) optional
      - assumed_load_pct (float)   optional
      - system (str)               optional
      - model (str)                optional (overrides CLI model)
    """
    if not os.path.exists(filepath):
        print(f"❌ Input file not found: {filepath}")
        return []

    with open(filepath, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse JSON: {e}")
            return []

    results: list[InferenceMetrics] = []
    for i, entry in enumerate(data, 1):
        prompt = entry.get("prompt")
        if not prompt:
            print(f"Skipping entry #{i}: missing 'prompt'")
            continue

        entry_model = entry.get("model", model)
        max_tokens = entry.get("max_tokens", 512)
        country = entry.get("country", "EU")
        tdp = float(entry.get("hardware_tdp_watts", 65.0))
        load = float(entry.get("assumed_load_pct", 0.5))
        system = entry.get("system", "")

        print(f"\nRunning [{i}/{len(data)}] {entry.get('label','(no label)')}...")
        m = measure(
            prompt=prompt,
            model=entry_model,
            system=system,
            country=country,
            hardware_tdp_watts=tdp,
            assumed_load_pct=load,
            max_tokens=max_tokens,
        )
        results.append(m)

    return results


# ──────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="EduGreenLabs Green Metrics — measure CO₂ footprint of local AI inference"
    )
    parser.add_argument("--prompt", type=str, help="Single prompt to measure")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Ollama model (default: {DEFAULT_MODEL})")
    parser.add_argument("--country", default="DE", help="Country code for grid intensity (default: DE)")
    parser.add_argument("--tdp", type=float, default=65.0,
                        help="Hardware TDP in watts (default: 65W laptop)")
    parser.add_argument("--load", type=float, default=0.5,
                        help="Assumed load fraction 0.0–1.0 (default: 0.5)")
    parser.add_argument("--input", type=str,
                        help="Path to JSON file with an array of prompt entries to run")
    parser.add_argument("--benchmark", action="store_true", help="Run full benchmark suite")
    parser.add_argument("--export", type=str, metavar="FILE.csv",
                        help="Export results to CSV for EduGreenLabs shared log")
    parser.add_argument("--list-countries", action="store_true",
                        help="List available country carbon intensities")
    args = parser.parse_args()

    if args.list_countries:
        print("\nAvailable country codes and grid carbon intensity (gCO₂/kWh):\n")
        for code, intensity in sorted(CARBON_INTENSITY.items()):
            print(f"  {code:<10} {intensity:>4} gCO₂/kWh")
        return

    # Check Ollama
    try:
        requests.get(f"{OLLAMA_BASE}/api/version", timeout=3)
    except requests.exceptions.ConnectionError:
        print("❌ Ollama is not running. Start it with: ollama serve")
        return

    results = []

    if args.input:
        results = run_from_json(args.input, model=args.model)

    elif args.benchmark:
        results = run_benchmark(
            model=args.model,
            country=args.country,
            hardware_tdp_watts=args.tdp,
        )
    elif args.prompt:
        m = measure(
            prompt=args.prompt,
            model=args.model,
            country=args.country,
            hardware_tdp_watts=args.tdp,
            assumed_load_pct=args.load,
        )
        results = [m]
    else:
        parser.print_help()
        return

    if args.export and results:
        export_to_csv(results, args.export)


if __name__ == "__main__":
    main()
