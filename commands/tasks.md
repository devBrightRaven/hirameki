---
description: "Compatibility redirect only: tasks now uses next tasks; prefer the primary entry."
argument-hint: "[original arguments]"
---

# tasks: compatibility redirect

This name is retained for the first consolidation release only. It is not an independent workflow or a write authorization.

Read `vault:` from `~/.claude/vault-local.md` for the vault root, then read `## Vault Structure` from `<vault>/AGENTS.md` (fall back to `~/.claude/vault-local.md`, then `~/.claude/CLAUDE.md` for setups predating 1.4.3) to get the vault path, the research folder location, and the list of content folders.
Resolve setup only before a vault read/write; missing required `Vault Structure` settings use `/hirameki:__init`. Use the user's language.

Continue immediately under `next tasks`, preserving $ARGUMENTS and the supplied scope. Load the destination contract `commands/next.md` under the package root; do not run the former workflow or ask an extra migration confirmation.

When the first argument is `stuck`, use `next stuck` instead, consume that mode word once and preserve the remaining arguments. Load `commands/next.md`.

Follow the destination's display-before-write, scope, language and safety gates unchanged. An old `save` argument is intent to propose, not approval for an unseen draft. Do not create, update, move or delete files in this redirect.
