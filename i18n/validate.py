#!/usr/bin/env python3
"""
Validate a Confida Integra language pack.

    python validate.py de.json
    python validate.py *.json --min-coverage 80

Standalone on purpose: no dependencies, no product source, so a translator can
run it before opening a pull request and CI can run the same check on it.

What it reports:

  coverage            how much of the English base the pack translates
  missing             keys the pack has no value for (these render in English)
  unused              keys the product no longer has (safe to delete)
  identical           values still the same as English - fine for product names
                      and status codes, a to-do list otherwise
  placeholder errors  a renamed or dropped {placeholder}

Only the last of those fails the check. A partial translation is a valid
translation: every key a pack does not cover renders in English.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

BASE_FILE = Path(__file__).resolve().parent / "en.json"
PLACEHOLDER_RE = re.compile(r"\{(\w+)\}")
LANG_RE = re.compile(r"^[a-z]{2,3}(-[a-z0-9]{2,8})*$")


def strings(pack: dict) -> dict[str, str]:
    """Translatable entries. Keys starting with _ are metadata."""
    return {k: v for k, v in pack.items()
            if not k.startswith("_") and isinstance(v, str)}


def load(path: Path) -> dict | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"{path.name}: cannot be read - {exc}")
        return None
    if not isinstance(data, dict):
        print(f"{path.name}: the file must contain a JSON object")
        return None
    return data


def check_meta(path: Path, pack: dict) -> list[str]:
    problems = []
    meta = pack.get("_meta")
    if not isinstance(meta, dict):
        return [f"no _meta block - copy the one from en.json and fill it in"]
    code = meta.get("code", "")
    if not LANG_RE.match(str(code)):
        problems.append(f"_meta.code {code!r} is not a lowercase BCP 47 code (de, sv, pt-br)")
    elif code != path.stem:
        problems.append(f"_meta.code is {code!r} but the file is named {path.name}")
    if not meta.get("label"):
        problems.append("_meta.label is empty - it is the name shown in the language "
                        "menu, in that language (Deutsch, not German)")
    return problems


def validate(path: Path, base: dict[str, str], min_coverage: int) -> bool:
    pack = load(path)
    if pack is None:
        return False
    values = strings(pack)
    meta_problems = check_meta(path, pack)

    missing = sorted(set(base) - set(values))
    unused = sorted(set(values) - set(base))
    shared = set(values) & set(base)
    identical = sorted(k for k in shared if values[k] == base[k])
    coverage = round(100 * len(shared) / len(base)) if base else 0

    bad_placeholders = []
    for key in sorted(shared):
        want = set(PLACEHOLDER_RE.findall(base[key]))
        got = set(PLACEHOLDER_RE.findall(values[key]))
        if want != got:
            bad_placeholders.append(
                f"    {key}\n      English: {base[key]}\n      yours:   {values[key]}\n"
                f"      expected {sorted(want) or 'no placeholders'}, found {sorted(got) or 'none'}")

    label = (pack.get("_meta") or {}).get("label") or path.stem
    print(f"\n{path.name} ({label}): {coverage}% - {len(shared)}/{len(base)} keys")
    for problem in meta_problems:
        print(f"  metadata: {problem}")
    if missing:
        print(f"  missing ({len(missing)}) - these render in English:")
        print("\n".join(f"    {k}" for k in missing[:15]))
        if len(missing) > 15:
            print(f"    ... and {len(missing) - 15} more")
    if unused:
        print(f"  not used by the product ({len(unused)}) - safe to delete:")
        print("\n".join(f"    {k}" for k in unused[:15]))
    if identical:
        print(f"  identical to English ({len(identical)}) - expected for product "
              f"names and codes, a to-do list otherwise")
    if bad_placeholders:
        print(f"  PLACEHOLDER ERRORS ({len(bad_placeholders)}) - these break the interface:")
        print("\n".join(bad_placeholders))

    ok = not bad_placeholders and not meta_problems and coverage >= min_coverage
    print("  " + ("OK" if ok else "NOT OK"))
    return ok


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a Confida Integra language pack")
    parser.add_argument("packs", nargs="+", help="pack files to check (de.json ...)")
    parser.add_argument("--min-coverage", type=int, default=0,
                        help="fail below this percentage (default 0: any coverage is valid)")
    args = parser.parse_args(argv)

    base_pack = load(BASE_FILE)
    if base_pack is None:
        print(f"cannot read the English base at {BASE_FILE}", file=sys.stderr)
        return 2
    base = strings(base_pack)

    ok = True
    for name in args.packs:
        path = Path(name)
        if path.resolve() == BASE_FILE:
            continue                      # the base is not checked against itself
        if not path.is_file():
            print(f"{name}: no such file")
            ok = False
            continue
        ok = validate(path, base, args.min_coverage) and ok
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
