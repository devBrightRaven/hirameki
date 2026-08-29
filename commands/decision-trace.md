---
description: >
  Start the unified decision-trace workflow for forming a decision and, only
  after explicit confirmation, optionally preserving it as a lifecycle-managed node.
argument-hint: "<decision question or context>"
---

Pass `$ARGUMENTS` to the `decision-trace` skill. The skill owns the full workflow;
do not duplicate or shortcut its state, trace, promotion, lifecycle, or save rules.

It must begin with `Establish the decision state`, which identifies `unresolved`,
`forming`, `decided`, or `reviewing`, then `Build the trace`, including viable options,
evidence, assumptions and unknowns, constraints, consequences, and reversal cost.
Only move to `decided` after the user explicitly confirms a choice;
the agent must not choose for the user. Apply the Promotion gate and preserve
`active`, `superseded`, and `closed` lifecycle behavior.

The skill must resolve `vault:` from `~/.claude/vault-local.md`, read the canonical
`## Vault Structure` from `<vault>/AGENTS.md`, and stop with the `/hirameki:__init`
setup message when required configuration is missing. Use the configured language.

Keep the workflow read-only until the user explicitly selects `save this`. Before
that action, show promotion-gate evidence, every affected full path, the complete
draft, the proposed `status: active` frontmatter, and exact status changes, then ask:

```text
Action? (save this / skip / edit)
```

Print every written path only after `save this`; `skip` writes nothing and `edit`
must show the revised complete draft and affected paths before asking again.
The `decision-trace` skill does not authorize a write until `save this` is selected.
