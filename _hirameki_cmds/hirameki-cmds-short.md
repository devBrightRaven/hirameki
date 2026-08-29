# Hirameki Commands

Use in Claude Code CLI. All commands start with `/hirameki:`.

---

## Orchestrators

Start here — each orchestrator bundles related primitives into a single guided flow. The individual primitives remain available for standalone use.

### `/hirameki:triage`
End-of-session bundle: wrap → journal → handoff in sequence. Shows a full draft for each step; choose save this / save all / skip / edit. `save all` batch-approves the remaining drafts.
No arguments. Run when wrapping up a session.

### `/hirameki:lens <concept>`
Topic understanding flow: arc → positions → bridge → challenge. Each step can be saved or skipped independently.
Input: a single concept or topic (required).

### `/hirameki:compose <topic>`
Topic creation flow: voice composition in your style → five-question frame test. Each step can be saved or skipped independently.
Input: a topic or question (required). Standalone — does not require `/hirameki:lens` to have run first.

### `/hirameki:mekiki <input>`
External resource capture. Auto-detects input type:
- GitHub URL or `owner/repo` → repo analysis (technique extraction + adopt/defer/reject verdict)
- Article URL → web article capture + vault cross-reference
- Pasted text or local file → article capture + vault cross-reference

Repo output: `{research}/mekiki-{repo-name}.md`
Article output: `{inbox}/YYYY-MM-DD-{slug}.md`

---

## Session

### `/hirameki:next`
Orient after resuming a session. Summarises what was done, what's open, and what to do next. No input required. Does not write to file.

### `/hirameki:wrap [description]`
Progress snapshot. Records completed, in-progress, next steps — appends to today's wrap log. Can run multiple times per day.
Optional input: focus description for this wrap.
Writes to: `{daily}/YYYY-MM-DD.md`

### `/hirameki:journal <description>`
Work log with reasoning and judgment trajectory: earlier view, evidence, change, unknowns, and revisit trigger. It does not invent a change when none occurred.
Input: topic description (required).
Writes to: `{journal}/YYYY-MM-DD-HHMM-{topic}.md`

### `/hirameki:decision-trace <decision question or context>`
Read-only formation identifies `unresolved`, `forming`, `decided`, or `reviewing` and presents the decision question, viable options, evidence and source, assumptions and unknowns, constraints, consequences, reversal cost, and one key unresolved question. It does not choose for the user or write.
Conditional write starts only after the user explicitly states or confirms a choice: show the promotion evidence, full draft, affected paths, and status changes, then write only on `save this`. Preserves `active`/`superseded`/`closed` lifecycle behavior.
Writes to: `{journal}/decisions/YYYY-MM-DD-{slug}.md` only after `save this`

### `/hirameki:handoff`
End-of-session handoff document. Keeps current decisions separate from judgment changes that affect the next session.
Writes to: `{handoff}/YYYY-MM-DD-{slug}.md`

---

## Understanding (standalone)

These are the primitives that `/hirameki:lens` bundles. Use them directly for quick, focused lookups.

### `/hirameki:arc <concept>`
Concept evolution tracker. Shows first appearance, timeline, current state, and unexplored angles for a concept across the full vault.
Writes to: `{research}/arc/YYYY-MM-DD-{concept}.md`. Same concept same day appends.

### `/hirameki:bridge <A> and <B>`
Hidden connections between two topics. Finds direct intersections, bridge notes, and proposes hypotheses about deeper links.
Writes to: `{research}/bridge/YYYY-MM-DD-{A}-{B}.md`. Same pair same day appends.

### `/hirameki:challenge <topic>`
Argument weakness analysis. Checks each vault claim about the topic for internal contradictions, unverified assumptions, logic gaps, and evidence gaps.
Writes to: `{research}/challenge/YYYY-MM-DD-{topic}.md`.

### `/hirameki:reflect <question>`
Vault-voice answer. Analyses your writing style, extracts your positions, then writes an answer in your voice with source attribution and confidence notes.
Add `save` to write result.
Writes to: `{research}/reflect/YYYY-MM-DD-{question}.md`

---

## Creation (standalone)

These are the primitives that `/hirameki:compose` bundles.

### `/hirameki:frame <idea>`
Pre-creation checkpoint. Five questions (Only-I test, collision scan, stakes, tension, evidence). Four verdicts: PROCEED / RETHINK / KILL / CONSOLIDATE. Does not generate content — only evaluates whether it should exist.
Add `save` to write result.
Writes to: `{research}/frame/YYYY-MM-DD-{idea-slug}.md`

### `/hirameki:critique <file>`
Multi-model writing review. Three reviewers in parallel (Opus / Codex GPT / Gemini Pro), each scoring sensory density, structural tension, and resonance (1–10). Synthesises into a comparison table; highlights disagreements.
Writes to: `{vault}/_writing_lab/benchmark/`

---

## Vault

### `/hirameki:pulse [week|patterns]`
Three modes:
- **`pulse`** — Vault overview: content topics, recent activity, stats.
- **`pulse week`** — Weekly gap analysis: stated priorities vs. actual file changes.
- **`pulse patterns`** — Undercurrents (recurring themes without articles) + idea clusters forming.
Does not write to file.

### `/hirameki:harvest [save]`
Harvest actionable ideas from existing content. Seven categories (max 5 each): articles to write / tools to build / topics to research / people to contact / ideas for different media / untransacted value / ideas ready to graduate.
Graduate category: two-phase — confirms candidates, then creates files.
Add `save` to write summary. Writes to: `{research}/harvest/`

### `/hirameki:graduate <note>`
Promote a note to a stable concept card. Validates frontmatter, adds permanent status, links to related cards.

### `/hirameki:tasks [days|stuck]`
Aggregate next actions from wrap logs and journal. Deduplicates and ranks by recurrence. Items appearing 3+ times flagged as potential procrastination.
- **`tasks`** — last 3 days
- **`tasks N`** — look back N days
- **`tasks stuck`** — recurring tasks that never appeared in a Done section
Does not write to file.

---

## Maintenance

### `/hirameki:tidy [tags|fix|full|lint]`
Frontmatter health check. Default runs missing fields + consistency only.
- **`tidy`** — missing fields + consistency check
- **`tidy tags`** — tag convergence analysis (top tags, singletons, merge suggestions)
- **`tidy fix`** — missing fields + consistency + auto-correct
- **`tidy full`** — all checks
- **`tidy lint`** — content health (contradictions, stale claims, orphan notes, dead links)

Writes to: `{research}/tidy/`

### `/hirameki:__init`
First-time setup: detect vault, set language, resolve folders, write `~/.claude/vault-local.md` (vault path, language) and `<vault>/AGENTS.md` (folder layout). Run once per machine. Reconfigure with Mode B (run again when config exists).

---

## Write Behavior Overview

| Command | Writes to | Trigger | Same-day repeat |
|---------|-----------|---------|-----------------|
| `triage` | daily + journal + handoff | Per step (save this/save all/skip) | `save all` batch-approves remaining drafts |
| `lens` | research/lens/ | Per step (save/skip) | Each step is a separate file |
| `compose` | research/compose/ | Per step (save/skip) | Each step is a separate file |
| `wrap` | daily | Always | Appends new Wrap block |
| `journal` | journal | Always | Same topic appends; different creates new |
| `decision-trace` | journal/decisions | After explicit choice and `save this` | Promote only after gate; lifecycle active/superseded/closed |
| `handoff` | handoff | Always | Same date replaces |
| `arc` | research/arc/ | Always | Same concept appends |
| `bridge` | research/bridge/ | Always | Same pair appends |
| `challenge` | research/challenge/ | Always | Same topic appends |
| `reflect` | research/reflect/ | With `save` | Same question appends |
| `frame` | research/frame/ | With `save` | New file per idea |
| `mekiki` (repo) | research/ | Always | New file per repo |
| `mekiki` (article) | inbox/ | Always | New file per article |
| `graduate` | content folder | After confirm | New file each time |
| `harvest` | research/harvest/ | With `save` | Appends update |
| `tidy` | research/tidy/ | Always | Appends update |
| `critique` | _writing_lab/benchmark/ | Always | New file per critique |
| `tasks` | none | — | — |
| `next` | none | — | — |
| `pulse` | none | — | — |

All commands that write files show a preview and full path before writing.

Output language is configured on first run of `/hirameki:__init` and saved in `~/.claude/vault-local.md`.
