---
description: "Compatibility redirect only: pulse now uses next week; prefer the primary entry."
argument-hint: "[original arguments]"
---

# pulse: compatibility redirect

This name is retained for the first consolidation release only. It is not an independent workflow or a write authorization.

Read `vault:` from `~/.claude/vault-local.md` for the vault root, then read `## Vault Structure` from `<vault>/AGENTS.md` (fall back to `~/.claude/vault-local.md`, then `~/.claude/CLAUDE.md` for setups predating 1.4.3) to get the vault path, the research folder location, and the list of content folders.
Resolve setup only before a vault read/write; missing required `Vault Structure` settings use `/hirameki:__init`. Use the user's language.

Continue immediately under `next week`, preserving $ARGUMENTS and the supplied scope. Load the destination contract `commands/next.md` under the package root; do not run the former workflow or ask an extra migration confirmation.

When the first argument is `patterns`, use `lens patterns` instead, consume that mode word once and preserve the remaining arguments. Load `commands/lens.md`.

When the first argument is `week`, use `next week` instead, consume that mode word once and preserve the remaining arguments. Load `commands/next.md`.

When the first argument is `snapshot`, use `tidy snapshot` instead, consume that mode word once and preserve the remaining arguments. Load `commands/tidy.md`.

Follow the destination's display-before-write, scope, language and safety gates unchanged. An old `save` argument is intent to propose, not approval for an unseen draft. Do not create, update, move or delete files in this redirect.
