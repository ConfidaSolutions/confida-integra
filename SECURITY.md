# Security Policy

Confida Integra is a commercial product distributed by **Confida Solutions Oy**.
This document describes how to report security vulnerabilities and what response
to expect. It is the public mirror of the policy that ships with the product.

> **Status — placeholder fields.** Lines marked **TODO** below are placeholders
> awaiting vendor-side decisions (contact mailbox, PGP key, advisory channel,
> response-time commitments). They will be replaced before the v1.0 GA. The
> structure of this document is the version that ships.

---

## Reporting a Vulnerability

If you believe you have found a security vulnerability in Confida Integra,
**please do not open a public issue** (here or anywhere else). Report it
privately to the contact below; we will acknowledge receipt and coordinate
disclosure with you.

| Channel | Address |
|---|---|
| Primary email | `info@confida.solutions` |
| PGP key fingerprint | **TODO — `0x0000 0000 0000 0000 0000 0000 0000 0000 0000 0000`** |
| PGP public key | **TODO — vendor security page** |
| Backup contact | **TODO — secondary mailbox or responsible-disclosure platform** |

When reporting, please include where possible:

- The product **version** (visible in the dashboard footer or via `GET /api/version`)
- The **deployment surface** (Docker Compose, Kubernetes / OpenShift, direct Python)
- A **reproduction recipe** — minimal steps, request payloads, screenshots, logs
- The **observed impact** and any plausible exploit chain you have evaluated
- Whether you intend to publish a write-up, and the timeline you would prefer

We do not require a CVE ID at the time of reporting. We will request one from
the assigning CNA on your behalf if the issue warrants it.

---

## Response Times

Targets from the moment a report is received at the primary address above:

| Stage | Target |
|---|---|
| Acknowledgement of receipt | **TODO — e.g. 2 business days** |
| Initial triage and severity classification | **TODO — e.g. 5 business days** |
| Mitigation plan or accepted-risk decision | **TODO — e.g. 14 days for High / Critical** |
| Patch release for High / Critical | **TODO — e.g. 30 days from triage** |
| Public advisory after coordinated disclosure | **TODO — e.g. within 7 days of patch availability** |

Severity is classified using **CVSS v3.1**:

| Label | CVSS v3.1 base score |
|---|---|
| Critical | 9.0 – 10.0 |
| High | 7.0 – 8.9 |
| Medium | 4.0 – 6.9 |
| Low | 0.1 – 3.9 |

---

## Supported Versions

Security fixes are published only against versions inside the declared support
window. The full support-period statement (including the dates relevant to the
EU Cyber Resilience Act, Regulation (EU) 2024/2847, Article 13(8)) is published
on the vendor site; summarised here:

- **Product-line commitment:** at least 5 years from the GA date of each major
  version line (`1.x`, `2.x`, …).
- **Rolling minor support:** within the active major line, only the **two most
  recent minor releases** receive fixes.
- **Patch level:** fixes are released only against the **latest patch** of each
  supported minor.
- **Major transition:** the last minor of a previous major receives
  **security-only fixes for 12 months** after a new major ships, then is EOL.

| Version line | Status | Receives security fixes? |
|---|---|---|
| `1.x` — latest two minors | Active rolling support | Yes |
| `1.x` — older minors | EOL within line | No — upgrade to a supported minor |
| `0.9.x` (current pre-GA) | Pre-GA active development | Yes — rolled into the next release |
| ≤ `0.8.x` | End of life | No |

Back-porting to unsupported versions is available only under a separate paid
maintenance agreement — contact the address above.

---

## Coordinated Disclosure Policy

We follow a **coordinated disclosure** model:

1. **Receipt and acknowledgement** within the target window above.
2. **Triage** — reproduce, assign a CVSS score, decide a fix timeline, share it
   with the reporter.
3. **Fix and validation** on a private branch against the reproduction recipe.
4. **Release** as a patch in the supported version line(s); release notes note
   that a security fix is included without premature exploit detail.
5. **Advisory** within **TODO — e.g. 7 days** of the patch being available,
   crediting the reporter (unless anonymous), with affected versions, CVSS,
   workaround and upgrade path.
6. **CVE** requested from the relevant CNA and referenced in the advisory.

We ask reporters to allow **TODO — e.g. 90 days** between report and any public
write-up, extendable by mutual agreement.

If the vulnerability is **actively exploited** in the wild, the EU CRA Article 14
timeline (24 h early warning / 72 h notification / 14 d final report to ENISA and
the relevant CSIRT) applies in parallel and may compress this schedule.

---

## Advisory Channel

Published advisories are distributed via:

- **TODO — primary channel** (e.g. vendor website security page, mailing list)
- **TODO — backup channel** (e.g. RSS feed, in-product update banner)

Each advisory carries: CVE (if assigned), affected versions, CVSS v3.1 score,
description, mitigation, fixed-in version, reporter credit (when not anonymous),
and a link to the patch release notes.

---

## Out of Scope

The following are **not** considered security vulnerabilities under this policy:

- Bugs requiring an already-authenticated administrator (the threat model treats
  authenticated admins as trusted).
- Findings that depend on a misconfiguration documented as unsupported (e.g.
  running with mock data in production, or exposing the dashboard to the public
  internet without the read-only deployment mode).
- Issues in third-party dependencies already covered by a published CVE with no
  available upstream patch (handled by our dependency-scanning pipeline).
- Reports from automated scanners with no demonstrated exploit path.
- Self-XSS, missing security headers on health endpoints, and theoretical
  attacks with no impact on confidentiality / integrity / availability.

---

## Hall of Fame

Researchers who responsibly disclose vulnerabilities are credited here, with
their permission, after the corresponding advisory is published.

*(empty — credits will be added as advisories are published)*
