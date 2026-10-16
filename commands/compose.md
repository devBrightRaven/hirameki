---
description: >
  Select and assemble vault notes into sourced work, preserve author positions,
  or prepare a requested vault artifact. Ordinary writing uses language skills.
argument-hint: "[draft|edit|outline|voice|frame|review] <material or purpose>"
---

For a natural-language request, apply `${CLAUDE_PLUGIN_ROOT}/references/capabilities/natural-routing.md`; do not require the user to name this capability. Preserve the actual request as input.

Read `vault:` from `~/.claude/vault-local.md` for the vault root, then read `## Vault Structure` from `<vault>/AGENTS.md` (fall back to `~/.claude/vault-local.md`, then `~/.claude/CLAUDE.md` for setups predating 1.4.3) to get the vault path, the research folder location, and the list of content folders.
If a vault-dependent request lacks configuration, stop and respond: "Setup not complete. Please run `/hirameki:__init` first." A supplied draft can be edited without opening the vault or requiring setup.

Input: $ARGUMENTS. Preserve the requested operation: an edit is not a request for a new article, an outline is not a request for full prose, and a review is not publication authority.

## Purpose before procedure

Automatic selection is for cross-note source selection, author-position handling or requested vault artifact delivery. Ordinary supplied-text drafts and outlines use the relevant language-writing entry directly; an explicit compose request remains supported without requiring vault access.

Use the stated audience, purpose and acceptance criteria. Ask only when a missing fact materially changes the result. Do not run a mandatory voice → frame ritual, scan the full vault, or write a draft first merely to decide whether it deserves to exist.

- `draft` / `edit` / `outline`: use supplied material and the relevant installed language-writing entry when available. Preserve facts, uncertainty, quotation and URLs. If that entry is unavailable, disclose the limit and do not claim it ran.
- `voice`: use provided author samples or narrowly selected, authorized vault passages. Separate supplied/vault-supported positions from style inference; never invent personal anecdotes or beliefs.
- `frame`: assess audience, overlap, useful outcome and evidence before investing further. Apply narrative tension or the Only-I criterion only when the work's purpose warrants them.
- `review`: select the needed existing review pipeline, not a new mandatory panel.

Technical documentation is judged by correctness, reproducibility and usefulness. Do not KILL a useful tutorial merely because it lacks personal uniqueness, emotional stakes or a literary reversal. Recommendations to consolidate drafts are proposals, not deletion authority.

## Authorship and routing

Keep supplied material, vault provenance and new suggestions distinguishable. Contradictory author positions remain visible unless the user resolves them. Same author does not mean same brand voice. Brand checks, councils, Ravenquill and publishing gates apply only when explicitly requested or required by an approved project contract.

Use only relevant context. Do not require lens first. For an exploration rather than a creation request, use lens instead of duplicating its analysis.

## Independent review

Only when requested or required by an applicable contract, use the runtime's existing authorized independent-review pipeline. Record actual reviewer identity and model when observable, inspected artifact/version, findings and disagreements. A reviewer must not have produced the reviewed work. If unavailable, say there is no independent result; never simulate distinct reviewers in one model or treat an average score as consensus. Respect host delegation restrictions and approval boundaries; do not start external CLIs automatically.

## Result and save gate

Return the requested draft, outline or review plus material limitations when needed. For reply-only work, stop there; do not force a save menu.

If a vault save is requested, resolve the destination, show the full draft and target path, then ask `Action? (save this / skip / edit)`. Never write unless the user approves that displayed content. A changed draft must be displayed again. New analysis drafts may use `{research}/compose/YYYY-MM-DD-{slug}.md`; do not move, publish or retire source notes without separate approval. Print the full path after a successful write, and report partial failure accurately.

Use the requested language or the language specified in `## Vault Structure` when working with the vault.
