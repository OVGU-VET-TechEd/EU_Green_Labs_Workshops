"""
pseudonymise.py
───────────────
EduGreenLabs Workshop 2 — Privacy-by-Design for Learning Systems
HMAC-SHA256 pseudonymisation utility for educational research data.

Usage
-----
    # Set the secret once (use a strong, random value in production)
    export PSEUDO_SECRET="$(python3 -c 'import secrets; print(secrets.token_hex(32))')"

    # Pseudonymise a single identifier
    python3 pseudonymise.py --id "alice.mueller@ovgu.de"

    # Pseudonymise a CSV file
    python3 pseudonymise.py --csv raw_data.csv --id-col email --out pseudonymised_data.csv

    # Verify (round-trip check — only works if you hold the secret)
    python3 pseudonymise.py --verify --id "alice.mueller@ovgu.de" --pseudo "PID_3A7F2B1C9E04D581"

GDPR note
---------
Pseudonymised data is still personal data under GDPR (recital 26).
Store the PSEUDO_SECRET separately from the research data store.
Treat the secret with the same care as a private key.

Licence: MIT · EduGreenLabs / OvGU Magdeburg · EU-GREEN Alliance
"""

import argparse
import csv
import hashlib
import hmac
import os
import sys


# ──────────────────────────────────────────────────────────────────
# Core pseudonymisation function
# ──────────────────────────────────────────────────────────────────

def _load_secret() -> bytes:
    """Load the institutional secret from the environment."""
    secret = os.environ.get("PSEUDO_SECRET", "")
    if not secret:
        sys.exit(
            "ERROR: Environment variable PSEUDO_SECRET is not set.\n"
            "Generate one with:\n"
            "  export PSEUDO_SECRET=\"$(python3 -c 'import secrets; "
            "print(secrets.token_hex(32))')\"\n"
            "Store it securely — do NOT commit it to version control."
        )
    return secret.encode("utf-8")


def pseudonymise(real_identifier: str, secret: bytes | None = None) -> str:
    """
    Generate a consistent, non-reversible pseudonym for a real identifier.

    Uses HMAC-SHA256 to prevent rainbow-table attacks. The same identifier
    always produces the same pseudonym with the same secret — enabling
    longitudinal linkage without storing the real identifier.

    Parameters
    ----------
    real_identifier : str
        The original identifier (e.g. email address, student ID).
    secret : bytes, optional
        The HMAC secret key. If None, loaded from PSEUDO_SECRET env var.

    Returns
    -------
    str
        A pseudonym of the form "PID_<16-char-hex>".
    """
    if secret is None:
        secret = _load_secret()

    h = hmac.new(
        secret,
        real_identifier.strip().lower().encode("utf-8"),  # normalise before hashing
        hashlib.sha256,
    )
    return "PID_" + h.hexdigest()[:16].upper()


def verify_pseudonym(real_identifier: str, claimed_pseudo: str, secret: bytes | None = None) -> bool:
    """
    Check whether a claimed pseudonym matches the real identifier.
    Uses hmac.compare_digest to prevent timing attacks.
    """
    if secret is None:
        secret = _load_secret()
    expected = pseudonymise(real_identifier, secret)
    return hmac.compare_digest(expected, claimed_pseudo)


# ──────────────────────────────────────────────────────────────────
# Data minimisation helpers
# ──────────────────────────────────────────────────────────────────

def bin_time_of_day(hour: int) -> str:
    """Convert an hour (0–23) to a time-of-day category."""
    if 6 <= hour < 12:
        return "morning"
    elif 12 <= hour < 18:
        return "afternoon"
    elif 18 <= hour < 23:
        return "evening"
    else:
        return "night"


def score_to_band(score: float, low: float = 50.0, high: float = 75.0) -> str:
    """Convert a numeric score to a low/mid/high band (reduces precision)."""
    if score < low:
        return "low"
    elif score < high:
        return "mid"
    else:
        return "high"


def strip_file_metadata_warning(filepath: str) -> None:
    """
    Print a reminder to strip metadata from files before sharing.
    (Actual stripping requires exiftool — not implemented here.)
    """
    print(
        f"⚠️  REMINDER: Before sharing '{filepath}', strip metadata with:\n"
        f"   exiftool -all= \"{filepath}\"\n"
        f"   (install exiftool: https://exiftool.org)\n"
    )


# ──────────────────────────────────────────────────────────────────
# CSV processing
# ──────────────────────────────────────────────────────────────────

def pseudonymise_csv(
    input_path: str,
    id_column: str,
    output_path: str,
    drop_columns: list[str] | None = None,
    secret: bytes | None = None,
) -> int:
    """
    Read a CSV, replace the id_column with pseudonyms, drop sensitive columns.

    Parameters
    ----------
    input_path : str
        Path to the raw CSV file.
    id_column : str
        Column name containing the real identifier.
    output_path : str
        Path to write the pseudonymised CSV.
    drop_columns : list[str], optional
        Additional columns to drop entirely (e.g. ['name', 'exact_timestamp']).
    secret : bytes, optional
        HMAC secret. Defaults to PSEUDO_SECRET env var.

    Returns
    -------
    int
        Number of records processed.
    """
    if secret is None:
        secret = _load_secret()
    if drop_columns is None:
        drop_columns = []

    records_processed = 0

    with open(input_path, newline="", encoding="utf-8") as infile, \
         open(output_path, "w", newline="", encoding="utf-8") as outfile:

        reader = csv.DictReader(infile)
        if reader.fieldnames is None:
            sys.exit(f"ERROR: Could not read headers from '{input_path}'")

        # Build output fieldnames: replace id_column, drop others
        out_fields = []
        for field in reader.fieldnames:
            if field == id_column:
                out_fields.append("pseudo_id")
            elif field in drop_columns:
                continue  # silently remove
            else:
                out_fields.append(field)

        writer = csv.DictWriter(outfile, fieldnames=out_fields)
        writer.writeheader()

        for row in reader:
            out_row = {}
            for field in reader.fieldnames:
                if field == id_column:
                    out_row["pseudo_id"] = pseudonymise(row[field], secret)
                elif field in drop_columns:
                    continue
                else:
                    out_row[field] = row[field]
            writer.writerow(out_row)
            records_processed += 1

    return records_processed


# ──────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="HMAC-SHA256 pseudonymisation utility for educational research data."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Single-ID pseudonymisation
    p_id = subparsers.add_parser("id", help="Pseudonymise a single identifier")
    p_id.add_argument("--id", required=True, help="The real identifier to pseudonymise")

    # CSV pseudonymisation
    p_csv = subparsers.add_parser("csv", help="Pseudonymise a CSV file")
    p_csv.add_argument("--input", required=True, help="Input CSV file path")
    p_csv.add_argument("--id-col", required=True, help="Column name containing real identifiers")
    p_csv.add_argument("--output", required=True, help="Output CSV file path")
    p_csv.add_argument("--drop", nargs="*", default=[], help="Additional columns to drop")

    # Verification
    p_verify = subparsers.add_parser("verify", help="Verify a pseudonym matches a real identifier")
    p_verify.add_argument("--id", required=True, help="The real identifier")
    p_verify.add_argument("--pseudo", required=True, help="The claimed pseudonym")

    args = parser.parse_args()

    if args.command == "id":
        pseudo = pseudonymise(args.id)
        print(f"Real:   {args.id}")
        print(f"Pseudo: {pseudo}")

    elif args.command == "csv":
        n = pseudonymise_csv(
            input_path=args.input,
            id_column=args.id_col,
            output_path=args.output,
            drop_columns=args.drop,
        )
        print(f"✅ Processed {n} records.")
        print(f"   Output: {args.output}")
        strip_file_metadata_warning(args.output)

    elif args.command == "verify":
        match = verify_pseudonym(args.id, args.pseudo)
        if match:
            print(f"✅ MATCH: '{args.pseudo}' is a valid pseudonym for '{args.id}'")
        else:
            print(f"❌ NO MATCH: pseudonym does not correspond to this identifier")


if __name__ == "__main__":
    main()
