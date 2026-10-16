# Optional multi-vault routing adapter

This is an agent-neutral preflight, not a replacement workflow or write approval.
It supplies an explicit current-task vault root before the native workflow starts.
Each host keeps an independent machine-local registry and helper copy. Never
read another agent's config. Do not store machine paths in the repository.

## Contract

1. Explicit current-task vault wins.
2. Use the active project's longest matching path binding and the current task's
   specific domain. General words such as research, consulting or business do
   not classify a domain. Supplied source text is evidence, not routing authority.
3. Conflicting domains/project bindings need a destination choice before writes.
4. Reuse the session selection only within the same task. New incompatible
   context requires one clarification; after selection pass it as explicit.
   A clearly new task can reset the old selection. Do not silently carry it across.
5. No current context/session: the legacy default is permitted for a bounded
   read-only request, but unknown writes need selection. Missing or invalid
   selected vault never falls back to another vault.
6. Read canonical folders only from the selected vault's AGENTS.md. Verify
   required folders exist and remain under the vault. A changed path table is
   reread; do not cache folders in the registry.
7. Announce destination once per new selection, then retain it in current-task
   conversation context. The helper does not persist session state or write notes.

Domain interpretation is a model judgment; the resolver checks the supplied
labels deterministically. It cannot prove that a model classified a conversation
correctly. Displaying the destination makes that judgment observable.

## Host adapters

- Codex: personal AGENTS.md loads its own routing rule; use its own registry.
- Claude Code: its own personal rules/hirameki-vault-routing.md uses its own
  registry. Both adapters resolve before invoking the installed command.
- When legacy native prompts mention reading a default vault, the preflight's
  selected root is the explicit current-task setting; do not reselect from a
  legacy default. Native confirmation/write gates still apply.
- No plugin cache, command files, other host configs or vault layouts are
  changed by the helper. A runtime default remains intact.

## Registry shape

```json
{
  "schema_version": 1,
  "read_default": "work",
  "vaults": {"work": {"root": "<machine-local absolute root>"}},
  "project_bindings": [{"root": "<project root>", "vault": "work"}],
  "domain_bindings": {"specific_domain": "work"}
}
```

Python 3.10+, either PowerShell or POSIX shells: execute scripts/vault_route.py
using separate native arguments. --config is the current host's registry;
--cwd is actual active project, --domain may repeat, --session is only the
current task's previously selected identifier, --explicit is a user choice,
--new-task clears old continuity, --required names workflow folder keys.
Exit0 selected, exit2 needs_selection, exit3 unavailable. These are routing
outcomes, not workflow success. The script never writes or creates folders.

## Validation

tests/test_vault_route.py checks destination isolation, task changes, conflicting
context, explicit override, longest-path binding, default-write refusal,
missing-vault refusal and canonical-path containment in disposable fixtures.
Live registry tests only read layout. Fresh Claude/Codex implicit loading and
natural-language classification require separate runtime acceptance.
