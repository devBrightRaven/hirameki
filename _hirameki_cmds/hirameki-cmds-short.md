# Hirameki Commands

Use in Claude Code CLI. All commands start with `/hirameki:`.

---

## Session Start

### `/hirameki:catchup [days]`
Progress catchup. Reads recent Wrap progress + inbox items, suggests today's focus.
Optional input: number of days (default 1), e.g. `/hirameki:catchup 3` to review last 3 days.

## Session End

### `/hirameki:wrap [description]`
Progress snapshot. Records completed, in-progress, next steps — appends to today's daily note. Can run multiple times per day.
Optional input: focus description for this wrap.
Writes to: `{daily-notes}/YYYY-MM-DD.md`

## Vault State Check

### `/hirameki:status [week|patterns]`
Three modes:
- **`status`** — Vault overview: content topics, recent activity, stats. Good to run at session start.
- **`status week`** — Weekly gap analysis: stated priorities vs. actual file changes.
- **`status patterns`** — Undercurrents (recurring themes without articles) + idea clusters forming.

## Deep Work on a Specific Idea

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

All commands that write files show a preview and full path before writing.

Output language is configured on first run of `/hirameki:__init` and saved in `~/.claude/CLAUDE.md`.
