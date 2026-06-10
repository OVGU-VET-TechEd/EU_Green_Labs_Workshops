# Data Management Plan Template
## EduGreenLabs Research Project

> **Instructions:** Complete this template before starting data collection.  
> This document fulfils the data management plan requirements for EU-GREEN seed-funded projects  
> and aligns with Horizon Europe DMP guidelines.  
> _Save a completed copy in your institutional research repository._

---

## 1. Project Information

| Field | Your Answer |
|-------|-------------|
| Project title | |
| Principal researcher | |
| Institution | |
| Partner institutions | |
| Project period | |
| Data controller (legal entity) | |
| Data Protection Officer contact | |
| Date of this DMP | |
| Version | |

---

## 2. Research Question and Data Necessity

**2.1 State your primary research question:**

> _[Write your research question here — 1–2 sentences]_

**2.2 Why is data collection necessary to answer this question?**  
_(Apply the data minimisation principle: could the question be answered with existing/published data?)_

> _[Your answer]_

**2.3 Could aggregate or synthetic data substitute for personal data?**

- [ ] Yes — explain: ___
- [ ] No — justify: ___

---

## 3. Data Inventory

> Complete one row per data variable. Use the T0–T4 tier system from Workshop 2.

| # | Variable name | Description | Tier | GDPR Category | Legal basis (Art. 6/9) | Necessary? | Minimisation applied |
|---|--------------|-------------|------|---------------|----------------------|------------|----------------------|
| 1 | | | T_ | | | Yes / No | |
| 2 | | | T_ | | | Yes / No | |
| 3 | | | T_ | | | Yes / No | |
| 4 | | | T_ | | | Yes / No | |
| 5 | | | T_ | | | Yes / No | |

**Data tier reference:**

| Tier | Label | Examples |
|------|-------|---------|
| T0 | Non-personal aggregate | Cohort average score, dropout rate % |
| T1 | Pseudonymous | Hashed ID + performance scores |
| T2 | Identifiable performance | Name + grade + essay text |
| T3 | Sensitive personal | Disability status, mental health flags |
| T4 | Biometric | Eye tracking, keystroke dynamics |

---
!?[](https://)
## 4. Legal Basis

**4.1 Primary legal basis under GDPR Art. 6:**

- [ ] Art. 6(1)(a) — Consent
- [ ] Art. 6(1)(b) — Contract (e.g. enrolled student)
- [ ] Art. 6(1)(c) — Legal obligation
- [ ] Art. 6(1)(e) — Public task (state university)
- [ ] Art. 6(1)(f) — Legitimate interests _(note: rarely valid for special categories)_

**4.2 If processing special category data (T3–T4), additional basis under Art. 9:**

- [ ] Art. 9(2)(a) — Explicit consent
- [ ] Art. 9(2)(j) — Scientific research exception + safeguards _(describe safeguards below)_
- [ ] Not applicable — no special category data collected

**4.3 Safeguards for Art. 9(2)(j) (if applicable):**

> _[Describe technical and organisational safeguards: pseudonymisation, access control, encryption, etc.]_

---

## 5. Consent Workflow

**5.1 How is consent obtained?**

- [ ] Written consent form (paper)
- [ ] Digital consent form (REDCap / institutional system)
- [ ] Verbal consent (recorded)
- [ ] Implied consent _(justify below — rarely appropriate for research)_

**5.2 What information is provided to participants?**

The consent form explains:

- [ ] Purpose of the study
- [ ] What data is collected and why
- [ ] Who has access to the data
- [ ] How long data is retained
- [ ] Right to withdraw at any time without consequences
- [ ] Right to access their own data (Art. 15)
- [ ] Right to erasure (Art. 17)
- [ ] Whether data will be shared or published
- [ ] Contact details for data controller and DPO

**5.3 Consent withdrawal procedure:**

> _[Describe how participants can withdraw, what happens to their data upon withdrawal, and the technical process for removing their records]_

---

## 6. Pseudonymisation and Anonymisation

**6.1 Pseudonymisation method:**

- [ ] HMAC-SHA256 (recommended — see `code/pseudonymise.py`)
- [ ] Random UUID assigned at enrolment
- [ ] Sequential numeric ID
- [ ] Other: ___

**6.2 Key management:**

| Element | Your answer |
|---------|-------------|
| Where is the HMAC/mapping key stored? | |
| Who has access to the key? | |
| Is the key stored separately from the research data? | Yes / No |
| How is the key backed up? | |
| When will the key be destroyed? | |

**6.3 When (if ever) will data be fully anonymised for publication?**

> _[Describe the anonymisation strategy: k-anonymity threshold, tools used (ARX, OpenDP), what columns are removed/generalised]_

---

## 7. Storage Architecture

**7.1 Primary data storage:**

| Tier | Location | Access control | Encryption | Backup |
|------|----------|----------------|------------|--------|
| Identity mapping (T3) | | | | |
| Research data (T1–T2) | | | | |
| Raw files / recordings | | | | |
| Published / OER data (T0) | | | | |

**7.2 Cloud storage assessment:**

- Is any data stored on US-hosted cloud services (Google Drive, Dropbox, OneDrive)?
  - [ ] No — all data on EU-hosted infrastructure
  - [ ] Yes — describe the legal mechanism (SCC, adequacy decision): ___

**7.3 Cross-border data transfers (for multi-institutional EU-GREEN studies):**

> _[Describe how data is transferred between partner institutions: anonymised aggregates only / encrypted transfer with DPA / federated approach]_

---

## 8. Access Control

| Role | Can access | Access method | Authentication |
|------|-----------|---------------|----------------|
| Data controller | All tiers | Direct DB + identity store | MFA + VPN |
| Lead researcher | T1–T2 research data | DB read role | MFA |
| Research team member | T1 pseudonymous | DB read role | MFA |
| External collaborator | T0 aggregates only | Shared report | N/A |
| IT administrator | Infrastructure only | No data access | — |

---

## 9. Retention Schedule

| Data category | Legal basis | Collection end | Planned deletion | Action | Responsible |
|--------------|-------------|----------------|-----------------|--------|-------------|
| T3 identity mapping | | | | Delete | |
| T2 raw research data | | | | Anonymise | |
| T1 pseudonymous data | | | | Archive / delete | |
| T0 published aggregates | | | | Indefinite (OER) | |
| Consent records | Legal obligation | N/A | +3 years after project | Delete | |

---

## 10. Data Breach Procedure

**10.1 Breach detection:** _(How will you know if data has been accessed improperly?)_

> _[Describe: audit log monitoring, intrusion detection, user alerts]_

**10.2 Breach response timeline (GDPR Art. 33: 72-hour notification to supervisory authority):**

| Time | Action |
|------|--------|
| 0–2 hours | Isolate affected system, preserve logs |
| 2–24 hours | Assess scope, notify data controller |
| 24–48 hours | Notify institutional DPO |
| 48–72 hours | Notify supervisory authority if required |
| 72+ hours | Notify affected data subjects if required |

**10.3 Contact details:**

| Role | Name | Contact |
|------|------|---------|
| Data controller | | |
| Institutional DPO | | |
| National supervisory authority | | |

---

## 11. OER and Open Data Publication

**11.1 What will be published as Open Educational Resources?**

- [ ] Code and analysis scripts (fully open, MIT licence)
- [ ] Anonymised aggregate statistics (T0 data)
- [ ] Synthetic dataset preserving statistical properties
- [ ] Pseudonymised individual records _(only if properly anonymised — see 6.3)_
- [ ] No data published — code only

**11.2 Planned publication platform:**

- [ ] Zenodo (EU-hosted, DOI minting, CC BY)
- [ ] EUDAT / B2SHARE (EU research infrastructure)
- [ ] GitHub (code only — no personal data)
- [ ] Institutional repository
- [ ] Other: ___

**11.3 Licence:**

- Code: [ ] MIT  [ ] Apache 2.0  [ ] GPL-3.0
- Data/content: [ ] CC BY 4.0  [ ] CC BY-SA 4.0  [ ] CC0

---

## 12. Approval and Version History

| Version | Date | Changes | Approved by |
|---------|------|---------|-------------|
| 1.0 | | Initial DMP | |
| | | | |

---

_This template was developed as part of the EduGreenLabs project (EU-GREEN Alliance, OvGU Magdeburg).  
Released under CC BY-SA 4.0. Adapt freely for your institution._
