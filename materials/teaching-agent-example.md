---
title: EduGreenLabs — Teaching-Agent LiaScript Example
author: EduGreenLabs Teaching-Agent
duration: 20min
language: en
---

# EduGreenLabs: Privacy-aware AI Workshop — Intro

---

## Learning Objectives (10 minutes)

1. Remember: list the main GDPR principles relevant to small research projects.
2. Understand: explain why local AI deployment reduces privacy risk.
3. Apply: run a pseudonymisation snippet using HMAC-SHA256 on sample identifiers.
4. Analyze: identify three potential data minimisation improvements for a toy dataset.

---

## Slide: Context & Motivation (3 minutes)

Why this workshop?

- Small-scale AI projects often handle sensitive research data.
- We emphasise privacy-by-design and local-first model hosting (Ollama/Gemma).
- Learning objectives focus on safe, practical steps you can take immediately.

---

## Slide: Quick Checklist (2 minutes)

- Audience: Early Career Researchers / educators
- Prerequisites: basic Python, familiarity with hashes
- Tools: Python 3.9+, local terminal, sample CSV file

---

## Exercise: Pseudonymise identifiers (8 minutes)

Task: Run the following pseudonymisation function on a small list of IDs.

```python
# EduGreenLabs MIT License header
# Copyright (c) EduGreenLabs (OvGU Magdeburg)
# SPDX-License-Identifier: MIT

import hmac
import hashlib

def pseudonymise(ids, secret_key):
    """Return HMAC-SHA256 pseudonyms for an iterable of identifier strings."""
    key = secret_key.encode('utf-8')
    return [hmac.new(key, id_.encode('utf-8'), hashlib.sha256).hexdigest() for id_ in ids]

if __name__ == '__main__':
    sample_ids = ['alice@example.org', 'bob@example.org', 'carol@example.org']
    pseudonyms = pseudonymise(sample_ids, secret_key='replace-with-secure-key')
    for orig, pseudo in zip(sample_ids, pseudonyms):
        print(orig, '→', pseudo)
```

Notes:
- Never use a hardcoded secret key in production — use environment variables or a secrets manager.
- HMAC provides irreversible pseudonyms when the secret is kept private.

---

## Short quiz (single best answer)

1) Which GDPR principle requires collecting only the data you really need?

- A) Accountability
- B) Data minimisation
- C) Integrity
- D) Storage limitation

Answer: B

2) True or False: Running models locally always removes the need for a data protection impact assessment (DPIA).

Answer: False — local deployment reduces risk but may still require a DPIA depending on scale and sensitivity.

---

## Wrap-up & Further Reading (2 minutes)

- See `data/gdpr-article-reference.md` for cited GDPR articles.
- For local model setup, follow `setup/install_ollama.sh` and `setup/continue_config.json`.
- If you'd like, ask the Teaching-Agent to `/promote-session 1` to expand this into a full LiaScript lesson with explanation paragraphs, additional exercises, and graded quizzes.

---

<!-- End of LiaScript example for EduGreenLabs Teaching-Agent -->
