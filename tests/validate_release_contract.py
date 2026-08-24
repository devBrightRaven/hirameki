#!/usr/bin/env python3
"""Validate that package.json exposes the complete release test chain."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    release = json.loads((ROOT / ".release.json").read_text(encoding="utf-8"))
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    expected = f'{release["test"]} && {release["verify"]}'
    actual = package.get("scripts", {}).get("test")
    if actual != expected:
        print(f"FAIL: package scripts.test must equal release test + verify\nexpected: {expected}\nactual:   {actual}")
        return 1
    print("PASS: package scripts.test mirrors the release test + verify chain")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
