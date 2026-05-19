"""
ollama_api_examples.py
──────────────────────
EduGreenLabs Workshop 3 — AI Implementation Sprint

Complete set of Ollama API interaction patterns for educational research.
All inference runs locally — no data leaves your machine.

Sections
--------
1.  Basic chat completion (requests)
2.  OpenAI-compatible API (drop-in replacement)
3.  Streaming responses
4.  Batch processing (multiple prompts)
5.  Embeddings (for semantic search / RAG)
6.  Model management (list, pull, delete)
7.  Research assistant with system prompt
8.  Privacy-aware document analysis

Run all examples:
    python3 ollama_api_examples.py

Run one section:
    python3 ollama_api_examples.py --section 2

Requirements:
    pip install requests openai

Licence: MIT · EduGreenLabs / OvGU Magdeburg · EU-GREEN Alliance
"""

import argparse
import json
import sys
import time
from typing import Iterator

import requests

OLLAMA_BASE = "http://localhost:11434"
DEFAULT_MODEL = "gemma:latest"


# ──────────────────────────────────────────────────────────────────
# Utility
# ──────────────────────────────────────────────────────────────────

def check_ollama_running() -> bool:
    """Return True if the Ollama service is reachable."""
    try:
        r = requests.get(f"{OLLAMA_BASE}/api/version", timeout=3)
        return r.status_code == 200
    except requests.exceptions.ConnectionError:
        return False


def section_header(n: int, title: str) -> None:
    print(f"\n{'═'*60}")
    print(f"  Section {n}: {title}")
    print(f"{'═'*60}\n")


# ──────────────────────────────────────────────────────────────────
# Section 1: Basic chat completion
# ──────────────────────────────────────────────────────────────────

def section_1_basic_chat(model: str = DEFAULT_MODEL) -> None:
    section_header(1, "Basic chat completion (requests)")

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": (
                    "In one paragraph, explain why data minimisation "
                    "is important for educational AI research."
                )
            }
        ],
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": 256,
        }
    }

    print(f"Model: {model}")
    print(f"Prompt: {payload['messages'][0]['content']}\n")
    print("Response:")
    print("─" * 40)

    start = time.time()
    response = requests.post(
        f"{OLLAMA_BASE}/api/chat",
        json=payload,
        timeout=120
    )
    response.raise_for_status()
    elapsed = time.time() - start

    data = response.json()
    print(data["message"]["content"])
    print("─" * 40)
    print(f"\n⏱  {elapsed:.2f}s | "
          f"{data.get('eval_count', '?')} tokens | "
          f"{data.get('eval_count', 0) / elapsed:.1f} tok/s")


# ──────────────────────────────────────────────────────────────────
# Section 2: OpenAI-compatible API
# ──────────────────────────────────────────────────────────────────

def section_2_openai_compatible(model: str = DEFAULT_MODEL) -> None:
    section_header(2, "OpenAI-compatible API (drop-in replacement)")

    try:
        from openai import OpenAI
    except ImportError:
        print("Install the OpenAI SDK: pip install openai")
        return

    # Point the OpenAI client at local Ollama — zero code change needed
    # to switch back to the real OpenAI API: just change base_url and api_key
    client = OpenAI(
        base_url=f"{OLLAMA_BASE}/v1",
        api_key="ollama",   # Ollama ignores this value
    )

    print(f"Using OpenAI SDK pointed at local Ollama ({OLLAMA_BASE})\n")

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a GDPR compliance assistant for educational research. "
                    "Be concise and practical."
                )
            },
            {
                "role": "user",
                "content": "List 3 data minimisation strategies for a learning analytics study."
            }
        ],
        temperature=0.7,
        max_tokens=300,
    )

    print("Response:")
    print("─" * 40)
    print(response.choices[0].message.content)
    print("─" * 40)
    print(f"\n✅ To switch to real OpenAI API, change:")
    print(f"   base_url='https://api.openai.com/v1'")
    print(f"   api_key=os.environ['OPENAI_API_KEY']")
    print(f"   model='gpt-4o'   ← or any OpenAI model")
    print(f"   All other code stays identical.")


# ──────────────────────────────────────────────────────────────────
# Section 3: Streaming responses
# ──────────────────────────────────────────────────────────────────

def section_3_streaming(model: str = DEFAULT_MODEL) -> None:
    section_header(3, "Streaming responses (token-by-token)")

    def stream_chat(prompt: str) -> Iterator[str]:
        """Yield tokens as they are generated."""
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": True
        }
        with requests.post(
            f"{OLLAMA_BASE}/api/chat",
            json=payload,
            stream=True,
            timeout=120
        ) as resp:
            for line in resp.iter_lines():
                if line:
                    chunk = json.loads(line)
                    if not chunk.get("done", False):
                        yield chunk["message"]["content"]

    print("Streaming response (tokens appear as generated):\n")
    print("─" * 40)
    for token in stream_chat(
        "Describe the NVIDIA DGX Spark and its use case for educational AI research in 3 sentences."
    ):
        print(token, end="", flush=True)
    print("\n" + "─" * 40)
    print("\n✅ Use streaming for web UIs and interactive terminals.")


# ──────────────────────────────────────────────────────────────────
# Section 4: Batch processing
# ──────────────────────────────────────────────────────────────────

def section_4_batch(model: str = DEFAULT_MODEL) -> None:
    section_header(4, "Batch processing (multiple research queries)")

    # Example: classify a list of data variables by GDPR sensitivity
    variables = [
        "student full name",
        "pseudonymous hash ID",
        "exact login timestamp",
        "cohort average score",
        "disability status",
        "essay word count",
        "IP address",
        "time-of-day category",
    ]

    system_prompt = (
        "You are a GDPR data classification assistant. "
        "Classify the given educational data variable into one of these tiers: "
        "T0 (non-personal aggregate), T1 (pseudonymous), T2 (identifiable), "
        "T3 (sensitive personal), T4 (biometric). "
        "Respond with ONLY: 'Tier: TX — one sentence justification'. "
        "Be concise."
    )

    print(f"Classifying {len(variables)} variables by GDPR sensitivity tier...\n")
    print(f"{'Variable':<30} {'Classification'}")
    print("─" * 80)

    for var in variables:
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": var}
            ],
            "stream": False,
            "options": {"temperature": 0.3, "num_predict": 60}
        }
        r = requests.post(f"{OLLAMA_BASE}/api/chat", json=payload, timeout=60)
        r.raise_for_status()
        answer = r.json()["message"]["content"].strip()
        print(f"{var:<30} {answer}")

    print("\n✅ Batch processing complete — all inference ran locally.")


# ──────────────────────────────────────────────────────────────────
# Section 5: Embeddings (for semantic search / RAG)
# ──────────────────────────────────────────────────────────────────

def section_5_embeddings() -> None:
    section_header(5, "Embeddings for semantic search")

    # Note: use a dedicated embedding model for production
    # nomic-embed-text is fast and open-source
    embed_model = "nomic-embed-text"

    # Check if embedding model is available
    r = requests.get(f"{OLLAMA_BASE}/api/tags", timeout=10)
    models_available = [m["name"] for m in r.json().get("models", [])]

    if embed_model not in models_available:
        print(f"Embedding model '{embed_model}' not found.")
        print(f"Pull it with: ollama pull {embed_model}")
        print("Skipping embedding section.\n")
        return

    def embed(text: str) -> list[float]:
        """Generate a text embedding using the local model."""
        payload = {"model": embed_model, "prompt": text}
        r = requests.post(f"{OLLAMA_BASE}/api/embeddings", json=payload, timeout=60)
        r.raise_for_status()
        return r.json()["embedding"]

    def cosine_similarity(a: list[float], b: list[float]) -> float:
        """Compute cosine similarity between two vectors."""
        dot = sum(x * y for x, y in zip(a, b))
        mag_a = sum(x ** 2 for x in a) ** 0.5
        mag_b = sum(x ** 2 for x in b) ** 0.5
        return dot / (mag_a * mag_b) if mag_a and mag_b else 0.0

    # Example: find most semantically similar GDPR article to a query
    gdpr_snippets = {
        "Art. 5 – Principles": "Personal data shall be collected for specified, explicit and legitimate purposes and not further processed in a manner incompatible with those purposes.",
        "Art. 6 – Lawfulness": "Processing shall be lawful only if the data subject has given consent or processing is necessary for the performance of a contract.",
        "Art. 9 – Special categories": "Processing of personal data revealing racial or ethnic origin, political opinions, religious beliefs, health data is prohibited.",
        "Art. 17 – Right to erasure": "The data subject shall have the right to obtain from the controller the erasure of personal data concerning him or her without undue delay.",
        "Art. 25 – Data protection by design": "The controller shall implement data-protection principles in an effective manner and integrate safeguards into processing.",
    }

    query = "What must a researcher do if a study participant wants to delete their data?"
    print(f"Query: '{query}'\n")
    print("Semantic similarity to GDPR articles:")
    print("─" * 70)

    query_vec = embed(query)
    scores = []
    for title, text in gdpr_snippets.items():
        vec = embed(text)
        score = cosine_similarity(query_vec, vec)
        scores.append((score, title))

    for score, title in sorted(scores, reverse=True):
        bar = "█" * int(score * 30)
        print(f"  {score:.3f} {bar:<30} {title}")

    print("\n✅ Embeddings generated locally — no text sent to any external service.")


# ──────────────────────────────────────────────────────────────────
# Section 6: Model management
# ──────────────────────────────────────────────────────────────────

def section_6_model_management() -> None:
    section_header(6, "Model management (list, info, pull)")

    # List available models
    r = requests.get(f"{OLLAMA_BASE}/api/tags", timeout=10)
    models = r.json().get("models", [])

    print("Downloaded models:")
    print(f"  {'NAME':<30} {'SIZE':<12} {'MODIFIED'}")
    print("  " + "─" * 60)
    for m in models:
        size_gb = m.get("size", 0) / 1e9
        name = m.get("name", "?")
        mod = m.get("modified_at", "?")[:10]
        print(f"  {name:<30} {size_gb:<12.1f} {mod}")

    if not models:
        print("  No models downloaded yet.")
        print("  Pull one with: ollama pull gemma:latest")

    print(f"\nOllama API version: {requests.get(f'{OLLAMA_BASE}/api/version').json().get('version', '?')}")
    print(f"\nUseful commands:")
    print(f"  ollama pull gemma:latest        # Download/update model")
    print(f"  ollama pull gemma:2b            # Smaller model for 8 GB RAM")
    print(f"  ollama pull gemma2:27b          # Larger model for DGX Spark")
    print(f"  ollama pull nomic-embed-text    # Embedding model")
    print(f"  ollama rm gemma:2b              # Remove a model")
    print(f"  ollama list                     # Same as above via CLI")


# ──────────────────────────────────────────────────────────────────
# Section 7: Research assistant with system prompt
# ──────────────────────────────────────────────────────────────────

def section_7_research_assistant(model: str = DEFAULT_MODEL) -> None:
    section_header(7, "Research assistant with persistent system prompt")

    system = """You are the EduGreenLabs Research Assistant, part of the EU-GREEN University Alliance.

Your expertise covers:
- Privacy-by-Design for educational AI systems (GDPR Art. 5, 6, 9, 25)
- UNESCO AI Ethics principles and their application to research
- Open Educational Resources (OER) and the 5R framework
- Data minimisation strategies for learning analytics
- Green and low-energy AI deployment

Rules:
1. Always suggest data minimisation before recommending data collection
2. Flag GDPR implications clearly
3. Recommend open-source alternatives when possible
4. Note the energy cost of AI solutions when relevant
5. Never recommend collecting data beyond what is strictly necessary"""

    # Simulate a multi-turn conversation
    conversation = [
        {"role": "system", "content": system}
    ]

    turns = [
        "I want to track student engagement in an online course. What data should I collect?",
        "The course has 200 students across 3 EU countries. How does this affect my data strategy?",
        "Can I use this data to fine-tune a local Gemma model for personalised feedback?",
    ]

    print("Simulating a multi-turn research consultation:\n")

    for user_message in turns:
        conversation.append({"role": "user", "content": user_message})
        print(f"👤 Researcher: {user_message}\n")

        payload = {
            "model": model,
            "messages": conversation,
            "stream": False,
            "options": {"temperature": 0.7, "num_predict": 400}
        }
        r = requests.post(f"{OLLAMA_BASE}/api/chat", json=payload, timeout=120)
        r.raise_for_status()

        assistant_reply = r.json()["message"]["content"]
        conversation.append({"role": "assistant", "content": assistant_reply})

        print(f"🤖 Assistant:\n{assistant_reply}\n")
        print("─" * 60 + "\n")


# ──────────────────────────────────────────────────────────────────
# Section 8: Privacy-aware document analysis
# ──────────────────────────────────────────────────────────────────

def section_8_document_analysis(model: str = DEFAULT_MODEL) -> None:
    section_header(8, "Privacy-aware document analysis")

    # Simulated research document (already pseudonymised)
    document = """
    RESEARCH SUMMARY — EduGreenLabs Pilot Study (Pseudonymised)
    
    Participant PID_3A7F2B1C9E04D581 (treatment arm A):
    - Completed 8/10 modules (completion band: high)
    - Average quiz score band: high
    - AI assistant interactions: 47 sessions
    - Primary session time: afternoon
    - Essay quality improvement: significant (pre/post rubric)
    
    Participant PID_7C2E4A1B8F0D3E92 (control arm):
    - Completed 6/10 modules (completion band: mid)
    - Average quiz score band: mid
    - No AI assistant access
    - Primary session time: morning
    - Essay quality improvement: moderate
    
    Key finding: Treatment arm shows higher completion rates and 
    essay quality scores. Further analysis required.
    """

    tasks = [
        {
            "label": "Privacy audit",
            "prompt": (
                f"Audit the following research summary for privacy risks. "
                f"Check for: direct identifiers, quasi-identifiers, "
                f"special category data, and re-identification risks.\n\n{document}"
            )
        },
        {
            "label": "Research insights",
            "prompt": (
                f"Based on this pseudonymised research summary, what are the "
                f"key research insights, and what additional data (if any) "
                f"would be needed to draw firm conclusions?\n\n{document}"
            )
        }
    ]

    for task in tasks:
        print(f"Task: {task['label']}")
        print("─" * 40)

        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a research assistant specialising in educational data analysis and GDPR compliance."
                },
                {"role": "user", "content": task["prompt"]}
            ],
            "stream": False,
            "options": {"temperature": 0.5, "num_predict": 350}
        }
        r = requests.post(f"{OLLAMA_BASE}/api/chat", json=payload, timeout=120)
        r.raise_for_status()
        print(r.json()["message"]["content"])
        print("─" * 40 + "\n")


# ──────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────

SECTIONS = {
    1: ("Basic chat completion", section_1_basic_chat),
    2: ("OpenAI-compatible API", section_2_openai_compatible),
    3: ("Streaming responses",   section_3_streaming),
    4: ("Batch processing",      section_4_batch),
    5: ("Embeddings",            section_5_embeddings),
    6: ("Model management",      section_6_model_management),
    7: ("Research assistant",    section_7_research_assistant),
    8: ("Document analysis",     section_8_document_analysis),
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Ollama API examples for EduGreenLabs Workshop 3")
    parser.add_argument("--section", type=int, choices=SECTIONS.keys(),
                        help="Run a specific section only (1–8)")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help=f"Ollama model to use (default: {DEFAULT_MODEL})")
    args = parser.parse_args()

    if not check_ollama_running():
        print("❌ Ollama is not running. Start it with: ollama serve")
        print("   Or on macOS/Linux: the Ollama app / systemd service")
        sys.exit(1)

    print(f"\n✅ Ollama is running at {OLLAMA_BASE}")
    print(f"   Model: {args.model}\n")

    run_sections = [args.section] if args.section else list(SECTIONS.keys())

    for n in run_sections:
        label, fn = SECTIONS[n]
        try:
            # Pass model to functions that accept it
            import inspect
            sig = inspect.signature(fn)
            if "model" in sig.parameters:
                fn(model=args.model)
            else:
                fn()
        except requests.exceptions.ReadTimeout:
            print(f"⚠️  Section {n} timed out — model may be slow on your hardware.")
        except Exception as exc:
            print(f"⚠️  Section {n} failed: {exc}")

    print("\n" + "═" * 60)
    print("  All sections complete.")
    print("  🌿 All inference ran locally — zero data left your machine.")
    print("  Run code/green_metrics.py to measure your CO₂ footprint.")
    print("═" * 60 + "\n")


if __name__ == "__main__":
    main()
