<!--
author:   EduGreenLabs / OvGU Magdeburg – WP2 Training Lab
email:    edugreenlab@ovgu.de
version:  1.0.0
language: en
narrator: US English Female

comment:  Workshop 2 of the EduGreenLabs Training Lab Series (EU-GREEN Alliance).
          90-minute hands-on lab for Early Career Researchers on Privacy-by-Design
          and Data Minimisation in AI-powered Learning Systems.
          Grounded in UNESCO AI Ethics principles and Open Educational Resources (OER).

logo:     https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/OvGU_Logo.svg/320px-OvGU_Logo.svg.png

@style
.highlight { background-color: #e8f4f8; border-left: 4px solid #1a73e8; padding: 0.5em 1em; }
.warn      { background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 0.5em 1em; }
.success   { background-color: #d4edda; border-left: 4px solid #28a745; padding: 0.5em 1em; }
.timer     { font-size: 0.85em; color: #6c757d; font-style: italic; }
@end
-->

# Workshop 2 – Privacy-by-Design & Data Minimisation for Learning Systems

> **EduGreenLabs · WP2 Training Lab · Magdeburg 2026**
>
> _Funded by the European Union – EU-GREEN University Alliance_

---

**⏱ Duration:** 90 minutes  
**👥 Audience:** Early Career Researchers (Post-Docs) in Informatics, Education & Social Sciences  
**🌍 Language:** English  
**📁 Deliverable:** Methodological template linking legal compliance, technical design, and educational value

---

## 🗺️ Agenda Overview

| Block | Time | Topic |
|-------|------|-------|
| 0 | 0:00 – 0:05 | Welcome, goals & logistics |
| 1 | 0:05 – 0:20 | Theoretical foundation: UNESCO principles & OER rationale |
| 2 | 0:20 – 0:38 | Privacy issues in AI and learning systems |
| 3 | 0:38 – 0:55 | Data minimisation – what to collect, what to skip |
| 4 | 0:55 – 1:10 | Secure identification: linking performance data to individuals |
| 5 | 1:10 – 1:25 | Data strategy & storage architecture |
| 6 | 1:25 – 1:30 | Wrap-up, quiz & next steps |

---

## Block 0 – Welcome & Setup _(0:00–0:05)_

### 🎯 Learning Objectives

By the end of this lab you will be able to:

1. Explain why privacy-by-design is a **legal obligation** under GDPR and an **ethical imperative** under UNESCO principles.
2. Classify educational data by **sensitivity level** and apply the **data minimisation principle**.
3. Design a **pseudonymisation workflow** for classroom or research performance data.
4. Choose an appropriate **storage architecture** for a given educational AI use case.
5. Map technical design decisions to **OER principles** to ensure reusability and openness.

---

### 🛠️ Pre-Lab Check

Before we start, make sure you have:

- [ ] A laptop / device with a browser
- [ ] Access to the shared Miro / Whiteboard link (posted in the chat)
- [ ] The EU AI Act risk classification card (handed out or downloadable below)
- [ ] Your institution's data policy document (if available)

> 📥 **Download resources:** [EduGreenLabs GitHub Repository](https://github.com/edugreenlab/workshop-materials) _(placeholder — replace with actual repo)_

---

## Block 1 – Theoretical Foundation _(0:05–0:20)_

### 1.1 Why UNESCO Principles Matter for AI in Education

The **UNESCO AI Competency Framework for Teachers (2024)** identifies five core dimensions. Two of them are especially relevant to privacy:

> **Dimension 2 – Ethics of AI:** Teachers and researchers must understand ethical principles, apply safe and responsible AI use, and contribute to co-creating ethical rules.
>
> **Dimension 3 – AI Foundations and Applications:** Evaluating appropriateness of AI tools includes assessing their data practices and privacy implications.

UNESCO's **Recommendation on the Ethics of Artificial Intelligence (2022)** articulates four core governance principles:

| Principle | Meaning for Learning Systems |
|-----------|------------------------------|
| **Human agency** | Learners retain control over their own data |
| **Proportionality** | Data collected must not exceed what is necessary |
| **Do no harm** | Sensitive data must not expose or disadvantage learners |
| **Transparency** | AI decisions about learners must be explainable |

The **2025 UNESCO Guidance for Generative AI in Education** adds a further accountability layer: institutional users (universities, schools) bear responsibility for auditing AI algorithms and validating that data practices protect learner well-being.

---

### 1.2 Why Open Educational Resources (OER) Principles Are Critical for AI Training & Research

OER principles — **retain, reuse, revise, remix, redistribute** (the 5Rs, Wiley 2014) — intersect with AI privacy in ways that are often overlooked.

```
┌─────────────────────────────────────────────────────────┐
│           OER Principles × AI Data Ethics               │
├─────────────┬───────────────────────────────────────────┤
│ OER Pillar  │ AI/Privacy Implication                    │
├─────────────┼───────────────────────────────────────────┤
│ Retain      │ Who actually OWNS the training data?      │
│             │ Learner-generated content is NOT freely   │
│             │ retainable by AI providers.               │
├─────────────┼───────────────────────────────────────────┤
│ Reuse       │ Reusing learner interaction logs for AI   │
│             │ model training requires explicit consent. │
├─────────────┼───────────────────────────────────────────┤
│ Revise      │ Fine-tuning models on institutional data  │
│             │ must comply with data residency rules.    │
├─────────────┼───────────────────────────────────────────┤
│ Remix       │ Combining datasets from different schools │
│             │ creates new re-identification risks.      │
├─────────────┼───────────────────────────────────────────┤
│ Redistribute│ Sharing AI models trained on learner data │
│             │ may inadvertently expose private records. │
└─────────────┴───────────────────────────────────────────┘
```

> 💡 **Key insight:** OER without privacy-by-design is not truly open — it transfers risk onto learners who did not consent to become AI training data.

---

### 🧠 Quick Check: UNESCO Principles

What is the primary purpose of the **data minimisation** principle in UNESCO's AI ethics framework?

[( )] To reduce the cost of data storage
[( )] To speed up AI model training
[(X)] To collect only what is strictly necessary, protecting learner privacy and agency
[( )] To enable faster sharing of datasets between institutions

---

### 🧠 Quick Check: OER & AI

Which of the following data practices are consistent with both OER and privacy-by-design principles?

[[X]] Pseudonymising student performance records before using them in research
[[ ]] Using raw learning management system (LMS) logs to fine-tune a commercial AI model without consent
[[X]] Publishing synthetic datasets that preserve statistical properties but contain no real learner data
[[X]] Obtaining explicit, granular consent before logging learner interactions with an AI tutor
[[ ]] Sharing model weights trained on identifiable student essays as an open-source release

---

## Block 2 – Privacy Issues in AI and Learning Systems _(0:20–0:38)_

### 2.1 The Privacy Landscape in Educational AI

Educational AI systems operate in a uniquely sensitive environment. Unlike general-purpose AI, they process data about **minors, vulnerable groups, and performance metrics** that have real-world consequences (grades, scholarships, employment).

```
                   ┌──────────────────────────┐
                   │   Educational AI System  │
                   └────────────┬─────────────┘
                                │ ingests
         ┌──────────────────────┼──────────────────────┐
         ▼                      ▼                      ▼
   ┌──────────┐          ┌──────────────┐       ┌─────────────┐
   │ Learner  │          │ Interaction  │       │ Assessment  │
   │ Profiles │          │ Logs (LMS)   │       │ Results     │
   └────┬─────┘          └──────┬───────┘       └──────┬──────┘
        │                       │                      │
        ▼                       ▼                      ▼
   Name, age,            Click patterns,          Grades, essays,
   disability,           time-on-task,            quiz scores,
   language,             dropout signals,         peer ratings
   SES proxy             navigation paths
```

Each data type carries a **different risk profile**:

| Data Category | GDPR Category | Risk Level | Example |
|--------------|---------------|------------|---------|
| Name + student ID | Personal data | Medium | Can identify individual |
| Health/disability status | **Special category** | **High** | Requires explicit consent |
| Performance scores | Personal data | Medium-High | Context-dependent |
| Click / navigation logs | Personal data | Low-Medium | Often underestimated |
| Socioeconomic proxies | Sensitive inference | **High** | AI can infer from behaviour |
| Biometric (eye tracking) | Special category | **Very High** | Strict legal basis needed |

---

### 2.2 The GDPR Legal Bases for Educational Research

Under **GDPR Art. 6**, processing learner data in research requires one of:

```
GDPR Art. 6 Legal Bases for Educational AI Research
─────────────────────────────────────────────────────
Art. 6(1)(a)  │ CONSENT         │ Best for voluntary participation
Art. 6(1)(b)  │ CONTRACT        │ Enrolled students – with limits
Art. 6(1)(c)  │ LEGAL OBLIGATION│ Accreditation reporting
Art. 6(1)(e)  │ PUBLIC TASK     │ State university research
Art. 6(1)(f)  │ LEGIT. INTEREST │ Rarely valid for special categories
─────────────────────────────────────────────────────
For special category data (Art. 9): EXPLICIT CONSENT
or SCIENTIFIC RESEARCH EXCEPTION (Art. 9(2)(j)) + safeguards
```

> ⚠️ **Common mistake by researchers:** Assuming that "anonymisation" removes GDPR obligations. If re-identification is _reasonably possible_, data is still personal data under GDPR.

---

### 2.3 The Re-identification Problem in Learning Analytics

Learning analytics data is notoriously difficult to truly anonymise because:

1. **Temporal uniqueness:** A student who logs in at 02:14 AM every Wednesday is likely unique in a cohort.
2. **Behavioural fingerprinting:** Navigation patterns in an LMS can identify an individual with high accuracy.
3. **Quasi-identifier accumulation:** Combining year of study + field + nationality + grade can be unique.
4. **AI inference amplification:** A model trained on one dataset can infer sensitive attributes from seemingly neutral data.

**The k-anonymity principle** requires that each record is indistinguishable from at least _k-1_ others. For educational data, k ≥ 5 is a common minimum; k ≥ 10 is preferred.

---

### ✏️ Mini-Exercise: Identify the Privacy Risk _(5 minutes)_

> _Work individually, then compare with your neighbour._

You are given a dataset from an online learning platform containing:

```
student_id | country | age | programme | login_time | quiz_score | forum_posts | disability_flag
```

**Question 1:** Which columns alone are unlikely to identify an individual?

[[ ]] student_id
[[X]] quiz_score (if common score range)
[[X]] forum_posts (if aggregated count)
[[ ]] disability_flag
[[X]] age (broad range)
[[ ]] login_time (exact timestamp)

**Question 2:** Which combination of columns creates the highest re-identification risk?

[( )] country + quiz_score
[( )] age + programme
[(X)] student_id + country + disability_flag + exact login_time
[( )] forum_posts + quiz_score

---

### 2.4 Privacy Risks Specific to AI-Powered Learning Systems

Beyond standard data privacy, AI-powered systems introduce **new categories of risk**:

1. **Model memorisation:** LLMs and neural networks can memorise and reproduce training examples verbatim, including student essays.
2. **Inference attacks:** Even a published model (weights) can be queried to reconstruct training data.
3. **Embedding exposure:** Sentence embeddings of student text can be reversed to approximate the original text.
4. **Differential vulnerability:** Students with unusual performance patterns are at higher re-identification risk than average performers.
5. **Proxy discrimination:** A model that doesn't use protected attributes (gender, SES) may still discriminate via proxies (login time, device type).

---

## Block 3 – Data Minimisation: What to Collect, What to Skip _(0:38–0:55)_

### 3.1 The Data Minimisation Principle (GDPR Art. 5(1)(c))

> _"Personal data shall be adequate, relevant and **limited to what is necessary** in relation to the purposes for which they are processed."_

Translated into a practical decision framework:

```
┌──────────────────────────────────────────────────────────────┐
│            DATA MINIMISATION DECISION TREE                   │
└─────────────────────────────┬────────────────────────────────┘
                              │
              ┌───────────────▼───────────────┐
              │  Is this data item NECESSARY   │
              │  for the stated research aim?  │
              └───────────────┬───────────────┘
                    NO ───────┘ ───────── YES
                    │                         │
              ┌─────▼──────┐       ┌──────────▼─────────┐
              │ DO NOT     │       │ Can a DERIVED or   │
              │ COLLECT    │       │ AGGREGATED metric  │
              └────────────┘       │ serve instead?     │
                                   └──────────┬─────────┘
                                    YES ──────┘ ─── NO
                                    │                  │
                              ┌─────▼──────┐   ┌──────▼──────┐
                              │ Use derived │   │ Apply STRICT│
                              │ metric only │   │ safeguards  │
                              └────────────┘   └─────────────┘
```

---

### 3.2 Data Taxonomy for Educational AI Research

Use this taxonomy to classify your variables before collection:

| Tier | Label | Examples | Strategy |
|------|-------|----------|----------|
| **T0** | Non-personal aggregate | Average cohort score, dropout rate % | Freely usable |
| **T1** | Pseudonymous | student_id (hash) + scores | Pseudonymise, store key separately |
| **T2** | Identifiable performance | Name + grade + essay text | Strict access control + encryption |
| **T3** | Sensitive personal | Disability status, mental health flags | Explicit consent + special handling |
| **T4** | Biometric | Eye tracking, keystroke dynamics | Highest safeguards, minimal retention |

> 🎯 **Design goal:** Operate at the **lowest possible tier** that still allows the research question to be answered.

---

### 3.3 What Data Is Actually Needed? A Classroom Research Example

**Scenario:** You are studying whether an AI writing assistant improves essay quality in a Master's programme.

**What you might think you need vs. what you actually need:**

| Variable | Initially Assumed Necessary | Minimised Alternative |
|----------|----------------------------|----------------------|
| Student full name | For tracking progress | Pseudonymous hash ID |
| Student email | For follow-up surveys | Anonymous survey link |
| Full essay text (drafts) | For qualitative analysis | Consent-gated, encrypted vault |
| LMS session logs (all) | For engagement analysis | Aggregate: time-on-task + edit count |
| Grade history (all courses) | For baseline ability | Self-reported proficiency level |
| IP address | For geolocation analysis | Country/region only |
| Exact timestamps | For temporal analysis | Binned: morning/afternoon/night |

---

### ✏️ Group Exercise: Design a Minimal Dataset _(7 minutes)_

> _In groups of 3–4, use the shared Miro board._

**Your research question:** _"Does an AI-powered quiz generator reduce cognitive load for post-doctoral students preparing for viva examinations?"_

Draft the **minimal dataset** you need. For each variable, justify:

1. Why it is necessary (or can be dropped)
2. What tier (T0–T4) it falls in
3. What pseudonymisation or aggregation strategy you would apply

Use this template:

```
| Variable | Necessary? | Tier | Minimisation Strategy |
|----------|-----------|------|-----------------------|
|          |           |      |                       |
```

---

## Block 4 – Secure Identification: Linking Performance Data to Individuals _(0:55–1:10)_

### 4.1 The Core Challenge: Research Needs Linkage, Ethics Demands Separation

Educational research often requires longitudinal tracking — you need to know that "student A at time 1" is the same as "student A at time 3". But you must simultaneously protect identity. This creates a fundamental tension that **pseudonymisation** resolves.

---

### 4.2 Pseudonymisation Architecture

**Pseudonymisation** replaces direct identifiers with artificial identifiers (pseudonyms), while storing the mapping securely and separately.

```
┌───────────────────────────────────────────────────────────────────┐
│                    PSEUDONYMISATION ARCHITECTURE                  │
│                                                                   │
│  ┌─────────────────┐     ┌─────────────────┐                      │
│  │  IDENTITY STORE │     │  RESEARCH DATA  │                      │
│  │  (Secure, Auth) │     │  STORE (Open)   │                      │
│  │                 │     │                 │                      │
│  │  Name  → PID001 │     │  PID001 + score │                      │
│  │  Email → PID001 │     │  PID001 + time  │                      │
│  │  ID    → PID001 │     │  PID002 + score │                      │
│  └────────┬────────┘     └────────┬────────┘                      │
│           │ KEY SEPARATION        │                               │
│           └───────────────────────┘                               │
│           │ Never stored in the same system                       │
│           │ Access to Identity Store: RESTRICTED                  │
│           │ Access to Research Store: controlled                  │
└───────────────────────────────────────────────────────────────────┘
```

**Technical implementation — hashed pseudonym:**

```python
import hashlib
import hmac
import os

# Institutional secret — never stored with data!
# Generate once and store in a secure key vault
INSTITUTIONAL_SECRET = os.environ.get("PSEUDO_SECRET", "").encode()

def pseudonymise(real_identifier: str) -> str:
    """
    Generates a consistent, non-reversible pseudonym.
    Uses HMAC-SHA256 to prevent rainbow table attacks.
    """
    if not INSTITUTIONAL_SECRET:
        raise ValueError("PSEUDO_SECRET environment variable must be set")
    
    h = hmac.new(
        INSTITUTIONAL_SECRET,
        real_identifier.encode("utf-8"),
        hashlib.sha256
    )
    # Return first 16 chars (64-bit security, sufficient for cohort sizes)
    return "PID_" + h.hexdigest()[:16].upper()

# Example usage
student_email = "alice.mueller@ovgu.de"
pseudo_id = pseudonymise(student_email)
print(f"Pseudonym: {pseudo_id}")
# Output: PID_3A7F2B1C9E04D581 (deterministic for same input + secret)
```

> ⚠️ **Critical:** The same student must receive the **same pseudonym** across time-points. Using a secret-keyed HMAC ensures this while preventing reverse lookup.

---

### 4.3 Pseudonymisation vs. Anonymisation: The Legal Distinction

| Property | Pseudonymous Data | Anonymised Data |
|----------|------------------|-----------------|
| GDPR applicability | **Still personal data** (recital 26) | No longer personal data |
| Re-identification possible? | Yes, with the key | Should be practically impossible |
| Research utility | High (linkable over time) | Limited (no longitudinal tracking) |
| Typical use in education | Longitudinal studies | Published aggregate statistics |
| Key management required? | **Yes, mandatory** | Not applicable |

> 🔑 **Rule of thumb for ECR research:** Always use pseudonymisation for longitudinal performance tracking. True anonymisation for publication-ready datasets.

---

### 4.4 Detecting "Smuggled" Identifiers in Research Data

A common but underappreciated problem: researchers inadvertently include quasi-identifiers that allow re-identification of individuals even in supposedly pseudonymised datasets. This is sometimes called **identifier smuggling**.

**Common smuggled identifiers in classroom/research data:**

```
HIGH RISK quasi-identifiers often overlooked:
─────────────────────────────────────────────
✗ Exact submission timestamps (unique per person)
✗ Free-text fields (writing style is a fingerprint)
✗ File metadata (author name in .docx properties!)
✗ Exact geographic location (GPS in uploaded images)
✗ Unusual performance patterns (top/bottom 1%)
✗ Combination: year + department + nationality + age
✗ LMS session IDs (if cross-referenced with server logs)
```

**Mitigation checklist before data sharing:**

- [ ] Strip all metadata from uploaded files (`exiftool -all= file.pdf`)
- [ ] Bin continuous variables (timestamps → time-of-day category)
- [ ] Apply k-anonymity check (k ≥ 5) to all quasi-identifier combinations
- [ ] Review free-text fields for name mentions
- [ ] Remove columns not needed for the research question (data minimisation)
- [ ] Apply differential privacy noise if publishing aggregate statistics

---

### ✏️ Case Study: Identify the Smuggled Identifier _(5 minutes)_

> _Individual reflection, then brief group discussion_

You receive this dataset for peer review. Identify all potential smuggled identifiers:

```csv
pid,programme,year,nationality,login_dt,essay_words,grade,disability
PID_001,CS-MSc,2,German,2026-04-15 02:17:33,4821,A+,dyslexia
PID_002,CS-MSc,1,Italian,2026-04-14 14:02:11,2103,B,none
PID_003,CS-MSc,3,Spanish,2026-04-15 09:44:58,1892,C,none
PID_004,CS-MSc,2,German,2026-04-15 02:19:04,4819,A+,dyslexia
```

Which fields must be modified before this dataset can be shared? Select all that apply:

[[X]] `login_dt` — exact timestamp is a quasi-identifier
[[X]] `essay_words` — unusual word count (4800+) is rare and distinctive
[[X]] `disability` — special category data under GDPR Art. 9
[[ ]] `programme` — alone, not identifying
[[ ]] `grade` — alone, not identifying
[[X]] `nationality + year + grade combination` — may be unique in cohort
[[ ]] `pid` — correctly pseudonymised

---

## Block 5 – Data Strategy & Storage Architecture _(1:10–1:25)_

### 5.1 Choosing a Storage Architecture

The right storage solution depends on **data sensitivity, access patterns, and team size**. Here is a practical decision map for educational AI research:

```
┌─────────────────────────────────────────────────────────────────┐
│           STORAGE ARCHITECTURE DECISION MAP                     │
│           for Educational AI Research Data                      │
└───────────────────────────┬─────────────────────────────────────┘
                            │
          ┌─────────────────▼─────────────────┐
          │   Dataset size & sensitivity?      │
          └─────┬──────────────────┬──────────┘
                │                  │
         Small + T0/T1        Large or T2-T4
                │                  │
    ┌───────────▼──────┐  ┌────────▼──────────────┐
    │  CSV / Parquet   │  │  Institutional DB or  │
    │  in encrypted    │  │  Research Data Repo   │
    │  folder          │  │  (PostgreSQL + roles) │
    │  (OK for pilots) │  └────────┬──────────────┘
    └──────────────────┘           │
                                   │
                    ┌──────────────▼──────────────┐
                    │  Multi-site / EU project?   │
                    └──────────────┬──────────────┘
                                   │
                         ┌─────────▼──────────┐
                         │  Federated or      │
                         │  Data Clean Room   │
                         │  approach          │
                         └────────────────────┘
```

---

### 5.2 Practical Options: Pros, Cons, and GDPR Fit

| Solution | Good for | GDPR considerations | Recommended for ECRs? |
|----------|----------|--------------------|-----------------------|
| **Excel/CSV on local disk** | Pilot, N<50 | Encryption mandatory; no audit trail | Only for T0/T1 pilots |
| **Encrypted folder (VeraCrypt)** | Small team, offline | Good for pseudonymous local storage | Yes, with key mgmt |
| **PostgreSQL on uni server** | Medium research projects | Role-based access, audit logs | **Recommended** |
| **Nextcloud (institutional)** | File-based sharing | EU-hosted, GDPR compliant | Yes |
| **GitHub (public repo)** | Code + aggregate data only | Never store personal data! | Yes, for code/OER |
| **REDCap** | Survey + clinical research | Audit trails, consent workflows | For survey data |
| **EUDAT / Zenodo** | Open data publication | For anonymised data only | For publication |

> 🚫 **Never use:** Google Drive, Dropbox, or US-cloud services for T2–T4 data without an EU Standard Contractual Clause (SCC) Data Processing Agreement.

---

### 5.3 Practical Database Schema for Educational Research

Here is a minimal, privacy-compliant PostgreSQL schema for a learning analytics research project:

```sql
-- ============================================================
-- IDENTITY STORE (access: data controller only, encrypted)
-- ============================================================
CREATE TABLE identity_mapping (
    real_identifier  TEXT NOT NULL,          -- hashed with app-level HMAC
    pseudo_id        CHAR(20) PRIMARY KEY,   -- e.g. PID_3A7F2B1C9E04D581
    consent_given    BOOLEAN NOT NULL DEFAULT FALSE,
    consent_date     TIMESTAMPTZ,
    consent_scope    TEXT[],                  -- e.g. {'performance_data','qualitative'}
    withdrawal_date  TIMESTAMPTZ,            -- set when consent withdrawn
    CONSTRAINT require_consent CHECK (consent_given = TRUE OR withdrawal_date IS NOT NULL)
);

-- ============================================================
-- RESEARCH DATA STORE (access: research team, pseudonymous)
-- ============================================================
CREATE TABLE performance_records (
    record_id        SERIAL PRIMARY KEY,
    pseudo_id        CHAR(20) NOT NULL,       -- FK to identity_mapping (in separate system)
    session_date     DATE NOT NULL,           -- binned to day, not exact time
    time_of_day      TEXT CHECK (time_of_day IN ('morning','afternoon','evening','night')),
    task_type        TEXT NOT NULL,
    completion_pct   NUMERIC(5,2),            -- 0.00 – 100.00
    score_band       TEXT CHECK (score_band IN ('low','mid','high')),  -- NOT exact score
    interaction_count INTEGER,
    collected_at     TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- AUDIT LOG (immutable, tracks all access)
-- ============================================================
CREATE TABLE data_access_log (
    log_id           SERIAL PRIMARY KEY,
    accessor_role    TEXT NOT NULL,
    action           TEXT NOT NULL,           -- e.g. 'SELECT', 'EXPORT'
    table_accessed   TEXT,
    pseudo_ids_count INTEGER,                 -- how many records touched
    accessed_at      TIMESTAMPTZ DEFAULT NOW(),
    justification    TEXT                     -- researcher notes required
);

-- Row Level Security: researchers can only see consented, active records
ALTER TABLE performance_records ENABLE ROW LEVEL SECURITY;
CREATE POLICY active_consent_only ON performance_records
    USING (pseudo_id IN (
        SELECT pseudo_id FROM identity_mapping
        WHERE consent_given = TRUE AND withdrawal_date IS NULL
    ));
```

---

### 5.4 Data Retention and Deletion Strategy

GDPR Art. 5(1)(e) — **storage limitation**: data must be kept no longer than necessary.

For educational research, a practical retention schedule:

```
Project Phase        Retention Period          Action at End
─────────────────────────────────────────────────────────────
Data collection      Duration of study         Keep; review consent
Active analysis      Project duration + 2 yr   Keep; re-verify basis
Publication          10 years (good practice)  Anonymise or delete
OER release          Indefinite                Anonymised data only
─────────────────────────────────────────────────────────────
Identity mapping     AS SHORT AS POSSIBLE      Delete as soon as
(the key!)           — ideally same as         linkage no longer
                     active analysis           needed
```

---

### 📋 Data Management Plan Template

Use this checklist for your EduGreenLabs project data management plan:

- [ ] **Purpose statement:** What specific research question justifies this data collection?
- [ ] **Legal basis:** Which GDPR Art. 6 basis applies? (Document it.)
- [ ] **Data inventory:** List all variables, their tier (T0–T4), and source.
- [ ] **Consent workflow:** How is consent obtained, recorded, and withdrawal handled?
- [ ] **Pseudonymisation method:** HMAC-SHA256 with institutional key? Who holds the key?
- [ ] **Storage location:** Institutional server or approved research infrastructure?
- [ ] **Access control:** Who has access to T2–T4 data? Role-based?
- [ ] **Retention schedule:** When will data be deleted or anonymised?
- [ ] **Breach procedure:** What happens if data is lost or accessed improperly?
- [ ] **OER alignment:** What, if anything, will be published as open data? Only T0/anonymised?

---

### ✏️ Final Exercise: Design a Privacy-Compliant Research Setup _(5 minutes)_

> _In your group, sketch a data flow for this scenario:_

**Scenario:** You are running a 3-month pilot study across 3 EU-GREEN partner universities. You want to track whether using an AI writing assistant (offline Ollama + Gemma model) improves draft quality for doctoral students. You need to compare pre/post scores, collect writing samples, and run a survey.

Sketch:

1. What data is collected, in which tier
2. Where it is stored (which system, which location)
3. How pseudonymisation links the three time-points
4. What gets published as OER at the end

> _Share your sketch on the Miro board._

---

## Block 6 – Wrap-Up & Summary Quiz _(1:25–1:30)_

### 🔑 Key Takeaways

1. **Privacy-by-Design is not a bureaucratic hurdle** — it is a research quality standard and a legal obligation (GDPR) and an ethical imperative (UNESCO).

2. **OER principles interact with privacy** — you cannot "open" data that contains personal information without proper anonymisation.

3. **Pseudonymisation ≠ anonymisation** — pseudonymised data is still personal data under GDPR; keep the identity key strictly separate.

4. **Data minimisation reduces risk** — the best defence against a data breach is not collecting data you don't need.

5. **Quasi-identifiers accumulate** — combinations of innocuous variables can uniquely identify individuals; always check k-anonymity.

6. **Storage architecture matters** — choose the right tool for the sensitivity tier; GitHub is for code, not personal data.

---

### 🎓 Final Quiz

**Q1:** Under GDPR, pseudonymised data is classified as:

[( )] Fully anonymised — no restrictions apply
[(X)] Still personal data — GDPR obligations remain
[( )] Special category data — requires explicit consent always
[( )] Public data — can be freely published

---

**Q2:** Which of the following correctly applies data minimisation?

[( )] Collecting all available LMS logs because storage is cheap
[( )] Recording exact timestamps because "we might need them later"
[(X)] Using binned time-of-day categories instead of exact login timestamps
[( )] Storing student names alongside pseudonyms in the same table

---

**Q3:** A doctoral student withdraws consent from your study. According to GDPR, you must:

[(X)] Stop processing their data and delete or anonymise their records
[( )] Keep their data but flag the record as withdrawn
[( )] Keep their data since deletion would harm research integrity
[( )] Ask their supervisor for permission to continue

---

**Q4:** Which storage solution is appropriate for T3 (sensitive personal) educational research data in an EU-GREEN project?

[( )] Public GitHub repository
[( )] Google Drive with sharing link
[(X)] Institutional server with role-based access, encryption, and audit logging
[( )] Personal laptop without encryption

---

### 📚 Further Reading & Resources

| Resource | Link |
|----------|------|
| UNESCO AI Competency Framework for Teachers (2024) | [unesdoc.unesco.org](https://unesdoc.unesco.org/ark:/48223/pf0000389029) |
| UNESCO Guidance for Generative AI in Education (2023) | [unesdoc.unesco.org](https://unesdoc.unesco.org/ark:/48223/pf0000386693) |
| EU AI Act (2024) — Education provisions | [artificialintelligenceact.eu](https://artificialintelligenceact.eu) |
| GDPR text — Art. 5 (principles), Art. 9 (special categories) | [gdpr-info.eu](https://gdpr-info.eu) |
| UK ICO Anonymisation Guide | [ico.org.uk](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/anonymisation-and-pseudonymisation/) |
| ARX Data Anonymisation Tool (open source) | [arx.deidentifier.org](https://arx.deidentifier.org) |
| REDCap for Research Data | [project-redcap.org](https://www.project-redcap.org) |
| OpenDP — Differential Privacy Library | [opendp.org](https://opendp.org) |

---

### ➡️ Next Workshop Preview

**Workshop 3 – AI Implementation Sprint: From Metrics to Deployment Scenarios**

In the next lab you will move from principles to practice: setting up a fully local AI stack with **Ollama + Gemma**, configuring **VS Code + GitHub Copilot for Educators**, and simulating deployment scenarios across different hardware tiers — from a laptop to an **NVIDIA DGX Spark** unit.

> 📋 **Pre-lab homework:** Install [Ollama](https://ollama.ai) on your machine and run `ollama pull gemma:latest` before the next session.

---

_This workshop was produced as an Open Educational Resource under CC BY-SA 4.0 by the EduGreenLabs consortium (EU-GREEN Alliance, OvGU Magdeburg). Funded by the European Union._

> **🌿 Green metric:** This workshop was designed to run in a hybrid format, reducing CO₂ emissions by ≥ 25 % compared to a fully in-person event. All tools used are open-source or institution-licensed.
