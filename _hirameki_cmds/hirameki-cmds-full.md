# Hirameki — five purpose-based entries — Detailed guide

> Version 2.2.0 consolidates the workflow entries; source validation, model acceptance, installation and scheduling are separate.

Every command reads its own `~/.claude/vault-local.md` only when vault access is needed, then `<vault>/AGENTS.md` (`## Vault Structure`) for canonical folders. Explicit task settings take precedence. Never read another agent's private configuration. Missing setup uses `/hirameki:__init`; setup writes require approval.

## Primary entries

| Entry | Purpose |
|---|---|
| `next` | Continue work, inspect effective tasks or blockers; `next tasks [N]`, `next stuck [N]`, `next week [N]`. |
| `lens` | Explore only the requested history, positions, relationships, weaknesses, opportunities or patterns; `lens cards` discovers concept cards and `lens random` requires an explicit request. |
| `compose` | Draft, edit, outline, voice, frame or review according to purpose; supplied drafts do not require a vault scan. |
| `decision-trace` | Form and preserve consequential choices without choosing for the user. |
| `triage` | Close with only useful wrap, journal, lesson or handoff drafts; no new confirmation before the first draft. |

## Specialized tools and permanent shortcuts

| Entry | Purpose |
|---|---|
| `tidy` | Maintenance: `tidy tasks` is read-only archive proposals; `tidy review` reviews corrections/lessons; `tidy snapshot` is read-only inventory. Claude bare tidy retains metadata checks; Codex bare tidy retains task proposals. |
| `mekiki` | External research intake; it does not start automatically during other workflows. |
| `init (`__init`)` | Configure the current machine and canonical folder layout; do not borrow another agent's setup. |
| `wrap` | Record one progress checkpoint without full triage. |
| `journal` | Record or append work, judgments or a qualified lesson. `journal review` uses the same `tidy review` capability. |
| `handoff` | Prepare a direct handoff without running full triage. |

## Migration redirects

Ten names remain as redirects for the first consolidation release only; eleven permanent callable names remain. Direct shortcuts do not expire. Host metadata hiding has not been verified.

| Old name | Destination |
|---|---|
| `arc` | lens history |
| `bridge` | lens bridge |
| `challenge` | lens challenge |
| `harvest` | lens opportunities |
| `graduate` | lens cards |
| `reflect` | compose voice |
| `frame` | compose frame |
| `critique` | compose review |
| `tasks` | next tasks; stuck → next stuck |
| `pulse` | next week; patterns → lens patterns; snapshot → tidy snapshot |

## Safety and evidence

Show complete content and target path before saving. `save all` covers only displayed drafts; display all remaining drafts before further writes. A changed draft needs a new display and approval. Analysis, redirect, rule-review proposal or a decision reminder is not write authority. Preserve partial success and retry only unfinished approved operations under the applicable contract.

An unresolved or forming trace may persist across sessions only after `save this`; it remains a discussion trace, not a decided node.

◆ **決策可記錄｜decision-trace** : reminder only, not saved or approved.

## Operational details

- The bundled task reader provides separately labelled active, uncertain and exceptions lists. State omitted counts and revision pins; never infer all done from an empty or partial page.
- Unmarked items without explicit status evidence stay visible as status uncertain, not confirmed active tasks, and are never automatically archived. A newer evidenced closure wins over an old Open item.
- Restore uses the delivered small operation guide, `--restore-contract`, `--validate-restore` and `--task-id`. Never print the entire index or search the implementation to discover schema. After separately approved immutable request/approval records, read back immediate visibility.
- Lens produces one coherent sourced result, not four mandatory reports. Atomic cards require provenance, existing-card checks, full draft approval and separately approved MOC updates.
- Compose preserves uncertainty, quotations, URLs and authored positions. Technical usefulness is not rejected for lacking literary tension. Independent review uses the actual authorized host pipeline, not simulated panels.
- Triage keeps zero-artifact and existing-spec exits, display-before-save and partial-save recovery. Review proposals never change rules through `save all`.
- The five-entry layout does not enable a scheduler, add hooks, deploy runtime copies or integrate akegarasu-no-yume automatically. Existing acceptance evidence retains its tested version and scope.

Executable contracts are in `commands/` and the Codex adapter's `references/`. Shared card/review capabilities live in package `references/capabilities/`; task capabilities preserve their host-specific reader roots. These summaries are not runtime configuration.
