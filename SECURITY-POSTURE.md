# Confida Integra — Security Posture

**Product:** Confida Integra
**Vendor:** Confida Solutions Oy
**Applies to:** 0.9.x and later

This is the **public** statement of what the product does about security: the
frameworks it is assessed against, the controls that ship in the binary, and the
limits of what it claims. It is written for the security architect reviewing
Confida Integra during procurement.

Two companion documents complete the picture:

| Document | Contents |
|---|---|
| [`SECURITY.md`](SECURITY.md) | How to report a vulnerability, response times, supported versions, coordinated-disclosure policy |
| Detailed security assessment | The full control-by-control mapping and the open-gap register. Vendor-internal; released to customers and prospects **on request** under NDA as part of a procurement review |

The detailed assessment is not published openly for the ordinary reason: a
line-by-line register of which controls are only partially implemented is a
roadmap for an attacker against every deployed instance. Ask for it and you will
get it — the claims below are the ones we are willing to stand behind in public,
and the assessment is what evidences them.

---

## 1. Deployment context

Confida Integra is designed for **private infrastructure**: a dedicated Linux
server, Docker Compose, Kubernetes/OpenShift, or a workstation, reached over a
VPN or LAN. It is not designed to be published on the open internet.

The product terminates plain HTTP; TLS is delegated to the reverse proxy in
front of it. A reference TLS configuration, mapped to BCP 195 / RFC 9325, NIST
SP 800-52 Rev. 2, BSI TR-02102-2 and the corresponding national profiles, ships
in the product's own Installation Guide.

It holds **integration metadata** — system names, protocols, owners, criticality
— plus the credentials it uses to read your platforms and the accounts of the
handful of people who use it. It is not a processor of bulk personal data.

---

## 2. Frameworks assessed against

| Framework | Scope of the assessment |
|---|---|
| **OWASP Top 10 (2021)** | Every category, application surface |
| **CIS Controls v8** | Controls 3, 4, 5, 6, 7, 8, 16 |
| **ISO/IEC 27001:2022** | Annex A organisational (A.5) and technological (A.8) controls applicable to a software product |
| **EU Cyber Resilience Act — Regulation (EU) 2024/2847** | Annex I Parts I and II; Articles 13–14 manufacturer obligations |
| **EU GDPR — Regulation (EU) 2016/679** | Art. 25, 32, 33–34, 15/17, 30 at the application level |
| **NIS2 — Directive (EU) 2022/2555** | Art. 21(2) controls relevant to a supplier's product |

National schemes restate the same requirements under local names. Finland's
Julkri T2 and Traficom cryptographic practices are the worked example in the
Installation Guide; equivalents in other member states map onto the same
controls.

**Not claimed:** Confida Integra is **not** accredited for nationally classified
information. Schemes such as Katakri or Julkri T3 require an accredited
environment, cleared personnel and physical controls that no software product
supplies on its own.

---

## 3. Controls that ship in the product

| Area | What is implemented |
|---|---|
| Authentication | Password login; bcrypt hashing at work factor 12; minimum length 15 characters for admin accounts, 12 for users, maximum 64; no plaintext password is stored or logged |
| Sessions | 256-bit CSPRNG token, server-side store, `httpOnly` + `SameSite=strict` cookie, 8-hour sliding expiry, explicit logout invalidation |
| Authorisation | Two roles (admin, user); server-side enforcement on every mutating endpoint; the system cannot be left without an admin |
| Brute force | Per-account and per-IP rate limiting on the login endpoint with lockout |
| CSRF | Double-submit token on every state-changing request |
| XSS | Output encoding in the frontend; Content-Security-Policy with `script-src 'self'` — no inline scripts and no inline event handlers |
| HTTP headers | CSP, `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy`, HSTS when served over TLS |
| Path traversal | Filename and path validation on every parameter that reaches the filesystem |
| API access | Northbound API (`/api/v1`) is read-only and requires a bearer token that is issued, listed and revoked by an admin |
| Credential handling | Platform tokens can be supplied by environment variable so they are never written to disk; the value is never echoed back to the browser |
| Audit trail | Structured audit log of logins, user management, settings changes, source switches, exports and token operations |
| Account hygiene | Dormant-account flagging for periodic access review (CIS v8 §5.3) |
| Availability | `/health/live` and `/health/ready` probes; resource limits in the shipped compose and chart definitions |

---

## 4. Vulnerability handling and supply chain

| Commitment | Detail |
|---|---|
| Coordinated disclosure | Published policy with a private reporting channel, CVSS v3.1 severity thresholds and response-time targets — see [`SECURITY.md`](SECURITY.md) |
| Support period | Five years for the product line, per CRA Art. 13(8), with rolling fixes at minor-version level and 12 months' advance notice of end of life |
| SBOM | Generated for every release in CycloneDX and SPDX form |
| Dependency scanning | Every pipeline run scans dependencies; the build fails on high or critical findings in the application's own dependency set |
| Base-image findings | Distinguished from application findings and handled on a scheduled base-image refresh. This distinction is deliberate and documented — a CVE in a base-image package that is not on the runtime path is not treated as a product vulnerability |

---

## 5. Known limitations

Published deliberately, because a security review will find them anyway and a
vendor that lists them is easier to trust than one that does not:

- **No built-in TLS.** The product serves plain HTTP and expects a reverse proxy
  to terminate TLS. Reference configurations are provided.
- **Sessions are held in memory.** They do not survive a restart, and the design
  targets single-instance deployments. Users log in again after an upgrade.
- **`style-src 'unsafe-inline'` remains in the CSP.** `script-src` is strict;
  inline styles in dynamically rendered markup still require the exception.
- **Certificate verification can be disabled** for a platform connection as an
  explicit, per-connection opt-in for closed lab environments. The UI warns when
  it is on, and it should never be used in production.
- **No SSO.** Authentication is local accounts only; SAML/OIDC is on the roadmap
  rather than in the product.
- **No independent penetration test yet.** Security work to date is internal
  review and automated scanning.

---

## 6. Asking for more

Send procurement security questions, requests for the detailed assessment, or a
security questionnaire to `info@confida.solutions`. Vulnerability reports go
through the private channel in [`SECURITY.md`](SECURITY.md) — please do not open
a public issue for them.
