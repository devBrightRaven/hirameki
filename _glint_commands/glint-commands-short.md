# Glint Commands

Use in Claude Code CLI. All commands start with `/glint-`.

---

## Daily Rhythm

### `/glint-status`
Vault overview. Scans content topics, recent activity across all folders.
No input needed. Good to run at the start of a session.

### `/glint-catchup [days]`
Progress catchup. Reads recent Wrap progress + inbox items, suggests today's focus.
Optional input: number of days (default 1), e.g. `/glint-catchup 3` to review last 3 days.

### `/glint-wrap [description]`
Progress snapshot. Records completed, in-progress, next steps — appends to today's daily note. Can run multiple times per day.
Optional input: focus description for this wrap.
Writes to: `{daily-notes}/YYYY-MM-DD.md`

### `/glint-weekreview`
Weekly review. Compares stated priorities against actual file changes, flags gaps between intentions and actions.
No input needed. Requires at least 3 days of daily notes for gap analysis.

---

## Concept Archaeology

### `/glint-arc {concept}`
Track a concept's evolution across the vault. Timeline from first appearance to current state. Same concept same day appends update.
Examples: `/glint-arc agency`, `/glint-arc minimalism`
Writes to: `{analysis}/arc/`

### `/glint-bridge {topicA} and {topicB}`
Find hidden connections between two topics. Lists direct intersections, bridge notes, potential deep-link hypotheses. Same pair same day appends update.
Example: `/glint-bridge accessibility and prompt engineering`
Writes to: `{analysis}/bridge/`

### `/glint-undercurrent [scope]`
Surface latent themes. Finds recurring topics that never got a dedicated article. Same day appends update.
Optional input: focus on a specific directory.
Writes to: `{analysis}/undercurrent/`

### `/glint-cluster [scope]`
Thought cluster analysis. Finds groups of notes converging on an unnamed theme. Same day appends update.
Optional input: focus on a specific scope.
Writes to: `{analysis}/cluster/`

---

## Thinking Tools

### `/glint-ghost {question} [save]`
Answer a question in your voice. Based on your writing style and existing positions.
Example: `/glint-ghost How much autonomy should AI agents have?`
Marks which parts have vault evidence vs speculative extension.
Append `save` to write to file: `/glint-ghost How much autonomy? save`
Writes to: `{analysis}/ghost/`

### `/glint-stress-test {topic} [save]`
Pressure-test arguments. Finds contradictions, unverified assumptions, logical gaps, evidence gaps.
Example: `/glint-stress-test the limits of prompt engineering`
Append `save` to write to file.
Writes to: `{analysis}/stress-test/`

### `/glint-harvest [save]`
Harvest actionable ideas from existing content. Four categories: articles to write, tools to build, topics to research, people to contact.
No input needed. Up to 5 per category, with source notes.
Input `save` to write to file: `/glint-harvest save`
Writes to: `{analysis}/harvest/`

### `/glint-graduate`
Graduate half-formed ideas into standalone notes. Scans recent 14 days of daily notes, logs, inbox, drafts, thoughts.
No input needed. Two phases: candidate list first, then execution after confirmation.
Writes to: user-specified content folder

---

## Maintenance

### `/glint-tidy [fix]`
Frontmatter properties audit. Checks all vault files for missing fields, inconsistent tags, redundant properties. Reports health score.
No input needed for report only. Input `fix` to auto-correct after confirmation: `/glint-tidy fix`
Writes to: `{analysis}/tidy/`

---

## Logging

### `/glint-journal {description}`
Work log and thinking article. Records what was done, why, inspiration connections, possible improvements. Same topic same day auto-appends.
Example: `/glint-journal slash command naming refactor`
Writes to: `{logs}/YYYY-MM-DD-{topic}.md`

---

## Write Behavior Overview

| Command | Writes to | Trigger | Same-day repeat |
|---|---|---|---|
| `/glint-wrap` | daily-notes | Always | Appends new Wrap block |
| `/glint-journal` | logs | Always | Same topic appends, different topic creates new |
| `/glint-arc` | analysis/arc | Always | Same concept appends, different creates new |
| `/glint-bridge` | analysis/bridge | Always | Same pair appends |
| `/glint-undercurrent` | analysis/undercurrent | Always | Appends update |
| `/glint-cluster` | analysis/cluster | Always | Appends update |
| `/glint-ghost` | analysis/ghost | Only with `save` | Same question appends |
| `/glint-stress-test` | analysis/stress-test | Only with `save` | Same topic appends |
| `/glint-harvest` | analysis/harvest | Only with `save` | Appends update |
| `/glint-graduate` | content folder | After confirmation | Independent each time |
| `/glint-tidy` | analysis/tidy | Always | Appends update |

All commands that write files show a preview and full path before writing.

Output language is configured on first run and saved in your vault's CLAUDE.md.
