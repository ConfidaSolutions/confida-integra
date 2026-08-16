# Contributing

Thanks for your interest in Confida Integra. This repository holds the
**public contracts and reference clients**; the product engine is maintained
privately by Confida Solutions. That shapes what we can accept here.

## What we welcome

- **Typo and clarity fixes** in documentation and specs.
- **Example improvements** — better comments, fixes, additional runnable
  scenarios under `examples/`.
- **SDK fixes** — bug fixes, better error messages, test coverage for the
  Python client in `sdk/python/`.
- **Documentation translations** of the `spec/` and example docs.
- **UI language packs** in [`i18n/`](i18n/) — a translation of the product
  interface itself. This is the one part of the repository that is *authored*
  here rather than mirrored from the product, and an accepted pack ships in the
  next release with your name in its `_meta.translator`. See
  [`i18n/README.md`](i18n/README.md); run `python i18n/validate.py your.json`
  before opening the PR. Partial translations are welcome — untranslated keys
  render in English.

## What we cannot accept here

- **Changes to the API contract, label/notes conventions, or JSON Schema.**
  These are *mirrored* from the upstream product, which is the source of truth.
  Propose contract changes via the channels on the vendor site; if accepted they
  are made upstream and re-published here. A PR that edits `spec/openapi.yaml`,
  `spec/integration-node.schema.json` or the convention docs to change behaviour
  (rather than fix a typo) will be redirected.

## How to propose a change

1. Open an issue describing the problem before a large PR, so we can confirm it
   fits the scope above.
2. Fork, branch, make the change, and keep it focused (one logical change per PR).
3. For SDK changes, run the tests in `sdk/python/` and add coverage.
4. Open the PR against the default branch with a clear description.

## Developer Certificate of Origin (DCO)

Contributions are accepted under the [Developer Certificate of
Origin](https://developercertificate.org/). Sign off each commit:

```
git commit -s -m "Fix typo in proxmox convention"
```

The sign-off line (`Signed-off-by: Your Name <you@example.com>`) certifies that
you wrote the contribution or otherwise have the right to submit it under the
repository's license (Apache-2.0 for code, CC-BY-4.0 for docs/specs).

## Code of Conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md). By
participating you agree to uphold it.

## Security

**Do not report security vulnerabilities through public issues or PRs.** Follow
the private process in [`SECURITY.md`](SECURITY.md).
