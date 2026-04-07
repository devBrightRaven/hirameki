# Hirameki Commands

Use in Claude Code CLI. All commands start with `/hirameki:`.

---

## Session Start

### `/hirameki:catchup [days]`
Progress catchup. Reads recent Wrap progress + inbox items, suggests today's focus.
Optional input: number of days (default 1), e.g. `/hirameki:catchup 3` to review last 3 days.

### `/hirameki:next`
Orient after resuming a session. Summarises what was done, what's open, and what to do next.

## Session End

### `/hirameki:wrap [description]`
Progress snapshot. Records completed, in-progress, next steps — appends to today's daily note. Can run multiple times per day.
Optional input: focus description for this wrap.
Writes to: `{daily-notes}/YYYY-MM-DD.md`

## Vault State

### `/hirameki:pulse [week|patterns]`
Three modes:
- **`pulse`** — Vault overview: content topics, recent activity, stats. Good to run at session start.
- **`pulse week`** — Weekly gap analysis: stated priorities vs. actual file changes.
- **`pulse patterns`** — Undercurrents (recurring themes without articles) + idea clusters forming.

### `/hirameki:tasks [days|stuck]`
Aggregate next actions from daily notes and journal. Deduplicates and ranks by recurrence. Items appearing 3+ times flagged as potential procrastination.
- **`tasks`** — default: last 3 days
- **`tasks N`** — look back N days
- **`tasks stuck`** — find recurring unfinished tasks that never appeared in a Done section

## Deep Work

### `/hirameki:lucky [n]`
Constellation reading — picks N random notes (default 5, range 2–20), weighted toward neglected notes (not modified in 30+ days). Finds the hidden theme at their intersection and one question the vault is orbiting without stating directly. Output goes to terminal only.

### `/hirameki:explore {input} [save]`
Concept excavation — mode detected from input shape:
- **Single concept** → Arc: evolution timeline across your vault
- **A and B** (or A 與 B / A と B) → Bridge: hidden connections between two topics
- **Ends with `?`** → Ghost: answer in your voice, with vault evidence marked
- **Starts with `test:`** → Stress-test: find contradictions, gaps, unverified assumptions

Add `save` to write result to file.
Writes to: `{analysis}/arc/`, `{analysis}/bridge/`, `{analysis}/ghost/`, `{analysis}/stress-test/`

## Action Planning

### `/hirameki:harvest [save]`
Harvest actionable ideas from existing content. Seven categories (max 5 each):
articles to write / tools to build / topics to research / people to contact / ideas for different media / value not transacted / ideas ready to graduate

Graduate category: two-phase — confirms candidates, then creates files after your selection.
Add `save` to write summary to file.
Writes to: `{analysis}/harvest/`; graduates to user content folder

## Creation

### `/hirameki:frame {idea} [save]`
Pre-creation checkpoint. Five questions (Only-I test, collision scan, stakes, tension, evidence). Four verdicts: PROCEED / RETHINK / KILL / CONSOLIDATE. Does not generate content — only evaluates whether it should exist.
Add `save` to write result to file.
Writes to: `{research}/frame/YYYY-MM-DD-{idea-slug}.md`

### `/hirameki:critique {file|text}`
Multi-model writing critique. Three reviewers in parallel (Opus / Codex / Gemini), each scoring sensory density, structural tension, and resonance (1–10). Synthesises into comparison table. Highlights disagreements (3+ point gaps).
Writes to: `{vault}/_writing_lab/benchmark/`

## External

### `/hirameki:mekiki {github-url}`
GitHub repo analysis. Extracts transferable techniques + evaluates adoption fit. Two tracks: technique extraction (patterns with concrete next steps) and adoption evaluation (feature comparison + adopt/defer/reject verdict).
Saves result to: `{research}/mekiki-{repo-name}.md`

## Decision Support

### `/hirameki:decide {topic}`
Pre-decision scan. Scans vault for relevant context, outputs three layers: Current State (with reversibility check), Friction (inversion: what would make this fail?), Key Question (one question, not a recommendation).
Does not write to file. To save, run `/hirameki:journal` afterward.

## Maintenance

### `/hirameki:tidy [tags|fix|full]`
Frontmatter health check. Default runs missing fields + consistency only (lightweight).
- **`tidy`** — missing fields + consistency check
- **`tidy tags`** — tag convergence analysis (top tags, singletons, merge suggestions)
- **`tidy fix`** — missing fields + consistency + auto-correct
- **`tidy full`** — all checks

Writes to: `{analysis}/tidy/`

## Work Reasoning Log

### `/hirameki:journal {description}`
Work log with reasoning. Records what was done, why, inspiration connections, open follow-ups. Same topic same day appends.
Example: `/hirameki:journal renamed slash command prefixes`
Writes to: `{logs}/YYYY-MM-DD-HHMM-{topic}.md`

---

## Write Behavior Overview

| Command | Writes to | Trigger | Same-day repeat |
|---------|-----------|---------|-----------------|
| `/hirameki:wrap` | daily-notes | Always | Appends new Wrap block |
| `/hirameki:journal` | logs | Always | Same topic appends, different topic creates new |
| `/hirameki:explore` | analysis/arc, bridge, ghost, stress-test | With `save` | Same concept/question appends |
| `/hirameki:harvest` | analysis/harvest | With `save` | Appends update |
| `/hirameki:harvest` (graduate) | content folder | After confirm | New file each time |
| `/hirameki:tidy` | analysis/tidy | Always | Appends update |
| `/hirameki:frame` | research/frame/ | With `save` | New file per idea |
| `/hirameki:critique` | _writing_lab/benchmark/ | Always | New file per critique |
| `/hirameki:mekiki` | research/ | Always | New file per repo |
| `/hirameki:tasks` | none | — | — |
| `/hirameki:lucky` | none | — | — |

All commands that write files show a preview and full path before writing.

Output language is configured on first run of `/hirameki:__init` and saved in `~/.claude/CLAUDE.md`.
