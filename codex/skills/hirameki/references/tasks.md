---
description: "Compatibility redirect only: tasks now uses next tasks; prefer the primary entry."
argument-hint: "[original arguments]"
---

# tasks: compatibility redirect

This name is retained for the first consolidation release only. It is not an independent workflow or a write authorization.

Resolve vault configuration through the umbrella Hirameki adapter. Read `## Vault Structure` from `<vault>/AGENTS.md` only when this task needs vault material; use explicit supplied material without a vault scan.
Resolve setup only before a vault read/write; missing required `Vault Structure` settings use `/hirameki:__init`. Use the user's language.

Continue immediately under `next tasks`, preserving $ARGUMENTS and the supplied scope. Load the destination contract `references/next.md` under the currently loaded Hirameki skill root (the directory containing its SKILL.md); do not run the former workflow or ask an extra migration confirmation.

When the first argument is `stuck`, use `next stuck` instead, consume that mode word once and preserve the remaining arguments. Load `references/next.md`.

Follow the destination's display-before-write, scope, language and safety gates unchanged. An old `save` argument is intent to propose, not approval for an unseen draft. Do not create, update, move or delete files in this redirect.
