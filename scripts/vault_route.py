"""Read-only vault selection. Caller supplies current-task context, never raw keywords."""
import argparse
import json
import re
from pathlib import Path


class RouteError(ValueError):
    pass


def _within(child, parent):
    return child == parent or parent in child.parents


def select(config, *, cwd=None, explicit=None, domains=(), session=None,
           reset=False, access="write"):
    if config.get("schema_version") != 1:
        raise RouteError("Unsupported routing schema")
    vaults = config.get("vaults", {})
    def chosen(key, reason):
        if key not in vaults:
            raise RouteError("Unknown vault identifier: " + str(key))
        return {"status": "selected", "vault_id": key,
                "vault_root": vaults[key]["root"], "reason": reason}
    def ambiguous(reason):
        return {"status": "needs_selection", "reason": reason}
    if explicit:
        return chosen(explicit, "explicit_current_task")
    candidates = set()
    if cwd:
        current = Path(cwd).expanduser().resolve()
        matches = [(len(Path(b["root"]).expanduser().resolve().parts), b["vault"])
                   for b in config.get("project_bindings", [])
                   if _within(current, Path(b["root"]).expanduser().resolve())]
        if matches:
            depth = max(d for d, _ in matches)
            candidates.update(v for d, v in matches if d == depth)
        for key, entry in vaults.items():
            if _within(current, Path(entry["root"]).expanduser().resolve()):
                candidates.add(key)
    domain_map = config.get("domain_bindings", {})
    for domain in domains:
        if domain not in domain_map:
            raise RouteError("Unknown domain; do not invent classification: " + domain)
        candidates.add(domain_map[domain])
    if len(candidates) > 1:
        return ambiguous("current_context_conflict")
    if candidates:
        key = next(iter(candidates))
        if session and not reset and key != session:
            return ambiguous("context_changed_confirm_destination_once")
        return chosen(key, "current_project_or_domain")
    if session and not reset:
        return chosen(session, "same_task_session")
    if access == "read" and config.get("read_default"):
        return chosen(config["read_default"], "read_only_default")
    return ambiguous("no_specific_context_do_not_write_to_default")


def layout(result, required):
    """Return only existing, vault-contained canonical folders; never create them."""
    if result["status"] != "selected":
        return result
    root = Path(result["vault_root"]).expanduser().resolve()
    if not root.is_dir() or not (root / ".obsidian").is_dir():
        raise RouteError("Selected vault unavailable; no fallback")
    agents = root / "AGENTS.md"
    text = agents.read_text(encoding="utf-8-sig")
    match = re.search(r"^## Vault Structure\s*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not match:
        raise RouteError("Missing Vault Structure; no fallback")
    block = re.search(r"```yaml\s*\n(.*?)```", match[1], re.S)
    if not block:
        raise RouteError("Missing canonical YAML path block")
    keys = {}
    for key in required:
        rows = re.findall(r"^" + re.escape(key) + r":\s*(.*?)\s*$", block[1], re.M)
        if len(rows) != 1:
            raise RouteError("Missing or duplicate canonical key: " + key)
        raw = rows[0].strip().strip('"\'')
        if not raw or Path(raw).is_absolute() or re.match(r"^[A-Za-z]:", raw) or "\\" in raw:
            raise RouteError("Canonical folder must be relative: " + key)
        target = (root / raw).resolve()
        if not _within(target, root) or target == root:
            raise RouteError("Canonical folder escapes vault: " + key)
        if not target.is_dir():
            raise RouteError("Canonical folder unavailable: " + key)
        keys[key] = str(target)
    return dict(result, folders=keys)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--cwd")
    parser.add_argument("--explicit")
    parser.add_argument("--domain", action="append", default=[])
    parser.add_argument("--session")
    parser.add_argument("--new-task", action="store_true")
    parser.add_argument("--access", choices=("read", "write"), default="write")
    parser.add_argument("--required", nargs="*", default=[])
    args = parser.parse_args()
    try:
        config = json.loads(args.config.read_text(encoding="utf-8-sig"))
        result = select(config, cwd=args.cwd, explicit=args.explicit,
                        domains=args.domain, session=args.session,
                        reset=args.new_task, access=args.access)
        result = layout(result, args.required)
        print(json.dumps(result, ensure_ascii=False))
        return 0 if result["status"] == "selected" else 2
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"status": "unavailable", "reason": str(exc)}, ensure_ascii=False))
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
