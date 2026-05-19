"""
workshop3_exercise.py
──────────────────────
EduGreenLabs Workshop 3 — AI Implementation Sprint
Hands-On Exercise: Privacy-Aware Data Processing with Local AI

Instructions
────────────
Complete all three tasks below. Use your AI assistant
(Continue + Ollama or GitHub Copilot) to help you code.

After completing each task, run:
    /privacy-check   (in Continue sidebar)
to have Gemma audit your code for GDPR issues.

Licence: MIT · EduGreenLabs / OvGU Magdeburg · EU-GREEN Alliance
"""

import hashlib
import hmac
import os
from datetime import datetime


# ══════════════════════════════════════════════════════════════════
# TASK 1 — Pseudonymisation
# ══════════════════════════════════════════════════════════════════
#
# Complete the `pseudonymise` function so that:
# 1. It reads the secret key from the PSEUDO_SECRET environment variable
# 2. It uses HMAC-SHA256 (not plain SHA256) to generate the pseudonym
# 3. It returns a string of the form "PID_<16-char-uppercase-hex>"
# 4. Calling it twice with the same input returns the same pseudonym
#
# The docstring tells you everything else you need.
#
# ──────────────────────────────────────────────────────────────────

def pseudonymise(real_identifier: str) -> str:
    """
    Generate a consistent, non-reversible pseudonym for a real identifier.

    Uses HMAC-SHA256 with an institutional secret loaded from the
    PSEUDO_SECRET environment variable.

    Parameters
    ----------
    real_identifier : str
        The real identifier to pseudonymise (e.g. student email address).
        Will be normalised to lowercase and stripped of whitespace.

    Returns
    -------
    str
        A pseudonym of the form "PID_<16-char-uppercase-hex>".

    Raises
    ------
    ValueError
        If PSEUDO_SECRET is not set in the environment.

    Examples
    --------
    >>> import os; os.environ['PSEUDO_SECRET'] = 'test-secret-123'
    >>> p = pseudonymise('alice@university.de')
    >>> p.startswith('PID_')
    True
    >>> len(p) == 20  # "PID_" + 16 hex chars
    True
    >>> pseudonymise('alice@university.de') == pseudonymise('alice@university.de')
    True  # deterministic
    """
    # ── YOUR CODE HERE ──────────────────────────────────────────
    # Hint: use hmac.new(key, msg, digestmod) and h.hexdigest()
    # Remember: the secret must be bytes, not str
    # Remember: HMAC-SHA256 is NOT the same as hashlib.sha256()
    pass
    # ── END YOUR CODE ───────────────────────────────────────────


# ══════════════════════════════════════════════════════════════════
# TASK 2 — Data Minimisation
# ══════════════════════════════════════════════════════════════════
#
# Complete the `minimise_record` function so that it:
# 1. Pseudonymises the 'email' field (use your function from Task 1)
# 2. Removes the 'name' field entirely
# 3. Converts 'login_datetime' (ISO format string) to a time-of-day
#    category: 'morning' (6–11), 'afternoon' (12–17),
#              'evening' (18–21), 'night' (22–5)
# 4. Converts 'score' (float 0–100) to a band:
#    'low' (<50), 'mid' (50–74), 'high' (>=75)
# 5. Returns a new dict with ONLY these keys:
#    pseudo_id, time_of_day, score_band, task_type
#
# ──────────────────────────────────────────────────────────────────

def minimise_record(raw_record: dict) -> dict:
    """
    Apply data minimisation to a raw educational research record.

    Input record keys (all may be present):
        email         : str — real identifier (must be pseudonymised)
        name          : str — must be REMOVED
        login_datetime: str — ISO 8601 format, e.g. "2026-04-15T14:23:11"
        score         : float — 0.0 to 100.0
        task_type     : str — kept as-is
        ip_address    : str — must be REMOVED
        device_id     : str — must be REMOVED

    Output record keys (only these, no others):
        pseudo_id   : str — HMAC pseudonym of email
        time_of_day : str — 'morning' | 'afternoon' | 'evening' | 'night'
        score_band  : str — 'low' | 'mid' | 'high'
        task_type   : str — unchanged from input

    Parameters
    ----------
    raw_record : dict
        A single raw data record.

    Returns
    -------
    dict
        The minimised, pseudonymised record.
    """
    # ── YOUR CODE HERE ──────────────────────────────────────────
    pass
    # ── END YOUR CODE ───────────────────────────────────────────


# ══════════════════════════════════════════════════════════════════
# TASK 3 — Quasi-Identifier Check
# ══════════════════════════════════════════════════════════════════
#
# Complete `check_k_anonymity` so that it:
# 1. Groups the records by the combination of: time_of_day, score_band, task_type
# 2. Finds any group with fewer than k members (default k=3 for this exercise)
# 3. Returns a list of dicts describing the risky groups:
#    {'group': {time_of_day: ..., score_band: ..., task_type: ...},
#     'count': <n>, 'risk': 'FAIL k-anonymity'}
# 4. Returns an empty list if all groups meet the threshold
#
# ──────────────────────────────────────────────────────────────────

def check_k_anonymity(records: list[dict], k: int = 3) -> list[dict]:
    """
    Check whether a list of minimised records satisfies k-anonymity.

    Groups records by (time_of_day, score_band, task_type) and flags
    any group where the count is less than k.

    Parameters
    ----------
    records : list[dict]
        Minimised records (output of minimise_record).
    k : int
        Minimum group size for k-anonymity (default: 3 for exercise,
        use k=5 or k=10 in production research).

    Returns
    -------
    list[dict]
        List of risky group descriptors, empty if all groups are safe.
    """
    # ── YOUR CODE HERE ──────────────────────────────────────────
    pass
    # ── END YOUR CODE ───────────────────────────────────────────


# ══════════════════════════════════════════════════════════════════
# TEST SUITE — run to verify your implementation
# ══════════════════════════════════════════════════════════════════

def run_tests() -> None:
    """Run automated tests for all three tasks."""
    import os

    # Set a test secret (not a real secret — for testing only)
    os.environ["PSEUDO_SECRET"] = "edugreenlab-test-secret-do-not-use-in-production"

    print("=" * 60)
    print("  Workshop 3 Exercise — Test Suite")
    print("=" * 60)

    passed = 0
    failed = 0

    def check(name: str, condition: bool, detail: str = "") -> None:
        nonlocal passed, failed
        if condition:
            print(f"  ✅ {name}")
            passed += 1
        else:
            print(f"  ❌ {name}" + (f" — {detail}" if detail else ""))
            failed += 1

    # ── Task 1 tests ──────────────────────────────────────────────
    print("\nTask 1: Pseudonymisation")

    try:
        p1 = pseudonymise("alice@university.de")
        check("Returns a string", isinstance(p1, str))
        check("Starts with PID_", p1.startswith("PID_"))
        check("Length is 20", len(p1) == 20, f"got {len(p1)}")
        check("Uppercase hex suffix", p1[4:].isupper() or p1[4:].isdigit(),
              f"got {p1[4:]}")

        p2 = pseudonymise("alice@university.de")
        check("Deterministic (same input → same output)", p1 == p2)

        p3 = pseudonymise("bob@university.de")
        check("Different inputs → different pseudonyms", p1 != p3)

        p_upper = pseudonymise("ALICE@UNIVERSITY.DE")
        check("Case-insensitive (normalised to lowercase)", p1 == p_upper,
              "Should normalise before hashing")

    except NotImplementedError:
        check("Function implemented (not just 'pass')", False, "Returns None/NotImplemented")

    # ── Task 2 tests ──────────────────────────────────────────────
    print("\nTask 2: Data Minimisation")

    sample_records = [
        {"email": "alice@ovgu.de", "name": "Alice M.", "login_datetime": "2026-04-15T09:15:00",
         "score": 88.5, "task_type": "essay", "ip_address": "134.76.1.1", "device_id": "dev-001"},
        {"email": "bob@ovgu.de", "name": "Bob K.", "login_datetime": "2026-04-15T14:30:00",
         "score": 62.0, "task_type": "quiz", "ip_address": "134.76.1.2", "device_id": "dev-002"},
        {"email": "carol@ovgu.de", "name": "Carol S.", "login_datetime": "2026-04-15T22:45:00",
         "score": 41.0, "task_type": "essay", "ip_address": "134.76.1.3", "device_id": "dev-003"},
    ]

    try:
        minimised = [minimise_record(r) for r in sample_records]
        m = minimised[0]

        check("Output has 'pseudo_id'", "pseudo_id" in m)
        check("Output has 'time_of_day'", "time_of_day" in m)
        check("Output has 'score_band'", "score_band" in m)
        check("Output has 'task_type'", "task_type" in m)
        check("'name' is removed", "name" not in m)
        check("'email' is removed", "email" not in m)
        check("'ip_address' is removed", "ip_address" not in m)
        check("'device_id' is removed", "device_id" not in m)
        check("'login_datetime' is removed", "login_datetime" not in m)
        check("Only 4 keys in output", len(m) == 4, f"got {len(m)}: {list(m.keys())}")

        # Time of day checks
        check("Morning (09:15) → 'morning'", minimised[0]["time_of_day"] == "morning",
              f"got '{minimised[0]['time_of_day']}'")
        check("Afternoon (14:30) → 'afternoon'", minimised[1]["time_of_day"] == "afternoon",
              f"got '{minimised[1]['time_of_day']}'")
        check("Night (22:45) → 'night'", minimised[2]["time_of_day"] == "night",
              f"got '{minimised[2]['time_of_day']}'")

        # Score band checks
        check("Score 88.5 → 'high'", minimised[0]["score_band"] == "high",
              f"got '{minimised[0]['score_band']}'")
        check("Score 62.0 → 'mid'", minimised[1]["score_band"] == "mid",
              f"got '{minimised[1]['score_band']}'")
        check("Score 41.0 → 'low'", minimised[2]["score_band"] == "low",
              f"got '{minimised[2]['score_band']}'")

    except NotImplementedError:
        check("Function implemented", False, "Returns None")

    # ── Task 3 tests ──────────────────────────────────────────────
    print("\nTask 3: k-Anonymity Check")

    # Minimised records with one risky singleton group
    test_records = [
        {"pseudo_id": "PID_A", "time_of_day": "morning",   "score_band": "high", "task_type": "essay"},
        {"pseudo_id": "PID_B", "time_of_day": "morning",   "score_band": "high", "task_type": "essay"},
        {"pseudo_id": "PID_C", "time_of_day": "morning",   "score_band": "high", "task_type": "essay"},
        {"pseudo_id": "PID_D", "time_of_day": "afternoon", "score_band": "low",  "task_type": "quiz"},
        # ↑ This is a singleton — should fail k=2 anonymity
    ]

    try:
        risky_k3 = check_k_anonymity(test_records, k=2)
        check("Returns a list", isinstance(risky_k3, list))
        check("Detects the singleton group", len(risky_k3) == 1,
              f"Expected 1 risky group, got {len(risky_k3)}")
        if risky_k3:
            check("Risky group has 'count' key", "count" in risky_k3[0])
            check("Risky group count is 1", risky_k3[0]["count"] == 1,
                  f"got {risky_k3[0].get('count')}")

        risky_k1 = check_k_anonymity(test_records, k=1)
        check("No risk with k=1 (all groups ≥ 1)", len(risky_k1) == 0,
              f"Expected 0 risky groups with k=1, got {len(risky_k1)}")

    except NotImplementedError:
        check("Function implemented", False, "Returns None")

    # ── Summary ───────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"  Results: {passed} passed, {failed} failed")
    if failed == 0:
        print("  🎉 All tests passed! Run /privacy-check in Continue next.")
    else:
        print("  📝 Fix the failing tests, then re-run.")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()
