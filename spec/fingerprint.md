# Integration ID Fingerprint

Every `IntegrationNode` carries an `id` that is a **deterministic fingerprint**
of seven of its attributes. Anyone holding the same attributes computes the same
id without asking Confida Integra. That is what lets a tool outside the product
produce records that line up with the ones Integra observes, whether it is a CI
check emitting declared state, a CMDB sync or a customer's own reporting.

This document is normative and describes **fingerprint version 1**. The test
vectors in [`fingerprint-vectors.json`](fingerprint-vectors.json) are part of
it: an implementation conforms when it reproduces every id in that file.

## 1. Inputs

Seven strings, in this order:

| # | Component | What it holds |
|---|---|---|
| 1 | `namespace` | Where the integration was found: a source-specific locator (§3.1) |
| 2 | `source_system` | The sending system |
| 3 | `destination_system` | The receiving system |
| 4 | `data_model` | The data models carried, as written |
| 5 | `protocol` | The two interfaces combined (§3.2) |
| 6 | `environment` | `dev`, `test`, `qa`, `production` or as labelled (§3.3) |
| 7 | `org` | The owning organisation |

A component that is not set is the empty string. Nothing else enters the hash:
owner, criticality, status, description, classification and every other field
can change without changing the id.

## 2. Algorithm

1. **Canonicalise** each component: remove leading and trailing whitespace
   (§2.1), then lowercase (§2.2). Nothing else: no Unicode normalisation
   (§2.3), no collapsing of inner whitespace, no reordering of list values.
2. **Join** the seven canonical components with `|` (U+007C VERTICAL LINE).
   The separator is not escaped.
3. **Encode** the joined string as UTF-8.
4. **Hash** it with SHA-256.
5. The id is the **first 16 characters** of the lowercase hexadecimal digest,
   that is, the leading 64 bits.

Reference implementation. On Python 3, `str.strip()` and `str.lower()` have
exactly the semantics of §2.1 and §2.2:

```python
import hashlib

def integration_id(namespace, source_system, destination_system,
                   data_model, protocol, environment, org):
    parts = [namespace, source_system, destination_system,
             data_model, protocol, environment, org]
    canonical = "|".join(p.strip().lower() for p in parts)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]
```

Worked example, the `basic` vector:

```text
namespace           billing-sync
source_system       billing
destination_system  crm
data_model          Invoice
protocol            rest-json → sql
environment         production
org                 finance

canonical  billing-sync|billing|crm|invoice|rest-json → sql|production|finance
sha256     0e9ce633d2b74cbe03e4e5050123021c0e485389f82f99e00363d1767797c7c4
id         0e9ce633d2b74cbe
```

### 2.1 Whitespace

The characters removed from both ends are exactly these 29 code points, the set
for which Python's `str.isspace()` is true:

```text
U+0009..U+000D  U+001C..U+001F  U+0020  U+0085  U+00A0  U+1680
U+2000..U+200A  U+2028  U+2029  U+202F  U+205F  U+3000
```

Do not substitute your platform's trim. JavaScript's `String.prototype.trim()`,
for one, also removes U+FEFF and keeps U+001C..U+001F and U+0085. U+200B ZERO
WIDTH SPACE and U+FEFF are outside the set and are hashed (vectors
`zero-width-not-stripped`, `bom-not-stripped`).

### 2.2 Lowercase

The Unicode **full default lowercase mapping** (Unicode Standard §3.13,
*toLowercase*): `UnicodeData.txt` plus the unconditional mappings of
`SpecialCasing.txt`, plus the `Final_Sigma` condition, with **no language
tailoring**. Two consequences catch implementations out:

- U+0130 LATIN CAPITAL LETTER I WITH DOT ABOVE becomes two code points,
  U+0069 U+0307. Not U+0069 alone (simple case mapping), and not the
  Turkish-locale result (vector `turkish-dotted-capital-i`).
- A capital sigma that ends a word becomes U+03C2 ς; elsewhere it becomes
  U+03C3 σ (vector `greek-final-sigma`).

This is lowercasing, not case folding: U+00DF ß stays ß and is distinct from
`ss` (vectors `sharp-s`, `double-s`). The reference collector runs on CPython
3.12, Unicode 15.0.

### 2.3 No normalisation

Text is hashed as it arrives. `ä` as one code point (U+00E4) and as `a` followed
by U+0308 produce different ids (vectors `precomposed-a-umlaut`,
`decomposed-a-umlaut`). Write metadata in NFC, which is what nearly every editor
and terminal produces.

## 3. Components by source

Card fields are read under the configured label prefix (for example
`ict.example.org/`). The **prefix is configuration, not input**: changing it
changes no id (vector `openshift-other-prefix`). Field names are those of
[`ocp-label-convention.md`](ocp-label-convention.md) and
[`proxmox-metadata-convention.md`](proxmox-metadata-convention.md).

| Component | OpenShift Project | Kubernetes Namespace | Proxmox VM / container |
|---|---|---|---|
| `namespace` | `metadata.name` | `kubernetes:<cluster>/<metadata.name>` | `proxmox:<instance>/<vmid>` |
| `source_system` | annotation `source-system` | annotation `source-system` | card `source-system` |
| `destination_system` | annotation `destination-system` | annotation `destination-system` | card `destination-system` |
| `data_model` | annotation `data-models` | annotation `data-models` | card `data-models` |
| `protocol` | §3.2 | §3.2 | §3.2 |
| `environment` | label `environment`, else §3.3 | label `environment`, else §3.3 | card `environment`, else tag `env-<value>`, else `production` |
| `org` | label `org` | label `org` | card `org` |

Values are used as written. `data_model` is not split, sorted or respaced, so
`HRModel;PersonModel` and `HRModel; PersonModel` are different ids (vectors
`data-model-compact`, `data-model-spacing`). `environment` is not mapped onto the
documented values: a label `Prod` contributes `prod`.

Integra collects only objects whose team label matches its configured team. The
team is a filter, not an input; the `derive` vectors carry it in `context` only
so that their objects are collected.

### 3.1 The namespace locator

- **OpenShift**: the bare project name. There is **no cluster segment**, so the
  same project name carrying an identical card in two OpenShift instances yields
  one id. That requires all seven components to be equal, which describes one
  logical integration deployed twice, such as a disaster-recovery pair. In
  exchange, a repository can compute the ids of its OpenShift projects without
  knowing which cluster they will be applied to.
- **Kubernetes**: `kubernetes:`, the cluster name, `/`, the namespace name.
  The cluster name is the **name the Integra administrator gave that Kubernetes
  instance** in Integra's source configuration (`kubernetes` if left unnamed),
  not a value read from the cluster. A tool computing ids outside Integra must
  be told this name. Without it, the right behaviour is to omit the id rather
  than guess, because a wrong id is worse than none.
- **Proxmox**: `proxmox:`, the instance name, `/`, the guest's numeric VMID.
  As with Kubernetes, the instance name is the **name given to that Proxmox
  source** in Integra's configuration (`proxmox` if left unnamed). The node the
  guest runs on is deliberately not part of it: VMIDs are unique across a
  Proxmox cluster, so the id survives a migration between nodes (vector
  `proxmox-migrated`). The current node is reported in `extra.node`.

### 3.2 Protocol

Let `si` and `di` be the `source-interface` and `destination-interface` values
as written.

- Both non-empty: `si`, then ` → `, then `di`. The joiner is U+0020 U+2192
  U+0020, and the arrow is part of the hashed text.
- Exactly one non-empty: that value.
- Neither: the empty string.

`si` and `di` are joined untrimmed, and only the whole `protocol` is trimmed by
§2, so inner whitespace survives: `rest` followed by a space, joined with `sql`,
gives `rest  → sql` with two spaces (vector `openshift-interface-whitespace`).
"Non-empty" is tested before any trimming.

### 3.3 Environment inference

When the `environment` label is absent or empty, OpenShift and Kubernetes infer
it from the **namespace name**, never from the cluster name (vector
`kubernetes-cluster-not-inferred`). Lowercase the name (§2.2) and split it on
`-` into words, then apply the first rule with a word among them:

| If the name has the word | `environment` |
|---|---|
| `dev`, `development` or `kehitys` | `dev` |
| `test`, `testi` or `staging` | `test` |
| `qa` | `qa` |
| none of these | `production` |

Only whole words count, in any position: `dev-billing` infers `dev`, while
`billing-devices` infers `production` (vectors
`openshift-environment-leading-word`, `openshift-environment-whole-word`).
Rule order decides, not position: `app-test-dev` is `dev`. Setting the label
explicitly avoids inference altogether and is recommended.

## 4. Stability

Any change that gives a different id for the same inputs, whether to the
separator, hash, truncation, canonicalisation or a derivation rule, is a
**breaking change** to the public surface
([`versioning-policy.md`](versioning-policy.md)). It would ship as a new
fingerprint version, never silently.

Changing any of the seven inputs produces a new id by design: renaming a system,
correcting a typo in an annotation, adding an `org` label, or renaming a
Kubernetes or Proxmox source in Integra. An id identifies
an integration *as currently described*; it is not a permanent serial number.

## 5. Known properties of version 1

Deliberate, documented, and pinned by the vectors:

| Property | Consequence |
|---|---|
| The separator is not escaped | `a\|b` to `c` and `a` to `b\|c` collide (vectors `pipe-in-source`, `pipe-in-destination`). System names containing `\|` are rare enough that this is accepted. |
| 64-bit truncation | Collision probability about 1 in 3.7 × 10⁹ across 100,000 integrations. |
| OpenShift has no cluster segment | Identical integrations in two OpenShift instances share an id (§3.1). |
| Values are used as written | Spacing and order in `data_model`, and spellings of `environment`, give distinct ids (§3). |
| No Unicode normalisation | NFC and NFD spellings of the same text give distinct ids (§2.3). |

## 6. Test vectors

[`fingerprint-vectors.json`](fingerprint-vectors.json) is generated from
Integra's collector code and checked against it, and against an independent
implementation of this document, in every build. Every non-ASCII character in
it is a `\uXXXX` escape, so nothing invisible can hide in the file.

- **`hash`**: seven `components`, the `canonical` string and the `id`. Tests §2
  alone. `equals` and `differs` name other vectors that must produce the same
  or a different id.
- **`derive`**: a source object as Integra receives it (`object` for an
  OpenShift Project or a Kubernetes Namespace; `resource` and `config` for a
  Proxmox guest, as the Proxmox API returns them), the `context` Integra
  supplies (label prefix, team, cluster name), the `components` derived from it
  by §3, and the `id`. Tests §3.

An implementation conforms to fingerprint version 1 when it reproduces every
`id` in both lists. One that takes the seven components from elsewhere and
needs only §2 conforms when it reproduces the `hash` list.
