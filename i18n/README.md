# Language packs

The Confida Integra interface is translated by **language packs** — one JSON
file per language. A customer can drop a pack into their own installation and
use it immediately, without a rebuild, a restart, or anything from us.

This directory exists so those packs do not have to stay private. **Contribute
one here and, if it passes review, it ships with the product** — every
installation gets it, and you are credited.

| File | What |
|---|---|
| `en.json` | The English base: every key the product has. Your starting file. |
| `fi.json` | Finnish, complete — a worked example of a finished pack. |
| `validate.py` | Checks a pack. No dependencies; run it before you open a PR. |

---

## Contributing a translation

### 1. Copy the base

```bash
cp en.json de.json
```

Then fill in `_meta`:

```json
"_meta": {
  "code": "de",
  "label": "Deutsch",
  "english_label": "German",
  "base_version": "0.9.9",
  "translator": "Your Name or Organisation",
  "updated": "2026-09-01"
}
```

`code` is a lowercase BCP 47 tag (`de`, `sv`, `pt-br`) and must match the
filename. `label` is the name shown in the language menu **in that language** —
`Deutsch`, not `German`.

### 2. Translate the values

Two rules, and only two:

1. **Never change a key.** `menu.graph` is an identifier, not text.
2. **Never change what is inside `{braces}`.** `Try again in {seconds} seconds`
   may become `Versuchen Sie es in {seconds} Sekunden erneut` — the word order
   is yours, the placeholder name is not. A renamed or dropped placeholder is
   the one mistake that breaks the interface rather than just reading oddly.

Leave alone, deliberately: product names (`OpenShift`, `Zabbix`, `Proxmox`),
`Confida Integra` itself, HTTP status text, and the `EN` marker.

**A partial translation is welcome.** Anything you do not translate renders in
English, per key — 200 translated strings out of 500 is a useful pack, not a
broken one. Send it, and finish it later.

You may add your own metadata under a leading underscore. `_notes` is a good
place for decisions a future translator should keep:

```json
"_notes": {
  "panel.last_seen": "Short form on purpose - the label column is narrow"
}
```

### 3. Check it

```bash
python validate.py de.json
```

```
de.json (Deutsch): 63% - 316/503 keys
  missing (187) - these render in English:
    admin.license_edition
    ...
  identical to English (12) - expected for product names and codes
  PLACEHOLDER ERRORS (1) - these break the interface:
    err.auth.rate_limited
      English: Too many login attempts. Try again in {seconds} seconds.
      yours:   Zu viele Anmeldeversuche. Versuchen Sie es in {sekunden} Sekunden.
      expected ['seconds'], found ['sekunden']
  NOT OK
```

Only placeholder and metadata errors fail the check. Missing keys never do.

### 4. Open a pull request

One language per PR, commits signed off (`git commit -s`) per the DCO in
[`../CONTRIBUTING.md`](../CONTRIBUTING.md). Say in the description whether you
are a native speaker of the language and, if the translation was
machine-assisted, that a human reviewed it — we would rather know.

---

## What happens after you submit

1. **Automated check** — `validate.py` runs on the PR.
2. **Review** — we read `_meta`, spot-check terminology consistency, and look
   for strings that changed meaning rather than language. We cannot judge the
   prose in every language, which is why we ask who reviewed it.
3. **Adoption** — an accepted pack is copied into the product and ships in the
   next release. It appears in the language menu of every installation, with
   `_meta.translator` intact.
4. **Maintenance** — a release that adds features adds keys. Your pack keeps
   working: new keys render in English until someone translates them. We will
   open an issue listing what is new; you are welcome to take it, and so is
   anyone else.

A pack that no one maintains is not removed. Half a translation is better than
none, and English is always underneath.

## Licensing

Contributions here are made under the DCO, and packs are published under the
repository's licence terms — see [`../LICENSE`](../LICENSE) and
[`../CONTRIBUTING.md`](../CONTRIBUTING.md). That is what lets an accepted pack
be shipped inside the commercial product. If your organisation cannot agree to
that, you can still keep the pack privately in your own installation's
`config/i18n/` — nothing about the product requires the pack to be public.

## Using a pack without contributing it

Drop the file into your installation's mounted configuration directory:

```
config/i18n/de.json
```

Reload the browser. It appears in the language menu — no rebuild, no restart. A
pack whose code matches one that ships (`fi.json`) overrides it key by key, so
you can change a single term to your organisation's vocabulary without
maintaining a copy of the rest.

The in-product **Adding a Language** documentation page covers the same ground,
plus the pseudo-locale generator for testing layout in a longer language before
a translation exists.
