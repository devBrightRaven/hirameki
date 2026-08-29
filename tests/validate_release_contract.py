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

    workflow_lines = (ROOT / ".github" / "workflows" / "validate.yml").read_text(encoding="utf-8").splitlines()
    for trigger in ("push", "pull_request"):
        start = workflow_lines.index(f"  {trigger}:")
        end = next(
            (
                index
                for index in range(start + 1, len(workflow_lines))
                if workflow_lines[index] and not workflow_lines[index].startswith(" ")
            ),
            len(workflow_lines),
        )
        paths_start = next(
            index for index in range(start + 1, end) if workflow_lines[index].strip() == "paths:"
        )
        paths_indent = len(workflow_lines[paths_start]) - len(workflow_lines[paths_start].lstrip())
        paths_end = next(
            (
                index
                for index in range(paths_start + 1, end)
                if workflow_lines[index]
                and len(workflow_lines[index]) - len(workflow_lines[index].lstrip()) <= paths_indent
            ),
            end,
        )
        assert any(
            line.strip().lstrip("- ").strip("\"'") == "skills/**"
            for line in workflow_lines[paths_start + 1 : paths_end]
        ), f".github/workflows/validate.yml {trigger}.paths must include skills/**"

    print("PASS: package scripts.test mirrors the release test + verify chain")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
