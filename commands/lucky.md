---
description: Constellation reading — random notes reveal a hidden theme
---

Read `## Vault Structure` from `~/.claude/CLAUDE.md` to get the vault path and the list of content folders.
If the section does not exist or required fields are missing, stop and respond: "Setup not complete. Please run `/hirameki:__init` first."

Input: $ARGUMENTS (optional — number of notes to draw, default 5. Range: 2–20)

Randomly draw N notes from the vault and find the hidden theme at their intersection — without the user directing what to look for. The randomness is the feature.

## Selection logic

Draw N notes from content folders with the following weighting:

- **Prefer neglected notes** — not modified in the last 30 days (weight: 3×)
- **Include recent notes** — modified in the last 30 days (weight: 1×)
- **Exclude** system folders, `_hirameki_cmds/`, daily, inbox, research, journal

If the vault has fewer than N eligible notes, draw all available and note the actual count.

Read the content of each selected note (up to 500 words per note).

## Analysis

Find what sits at the **centre** of all N notes — not a surface keyword match, but the underlying tension, preoccupation, or unresolved question that could have generated all of them.

This is not bridge analysis (pairwise connection). It is constellation reading: what single concept or question could all these notes be circling around without any of them stating it directly?

Look for:
- Recurring tensions or contradictions across the notes
- A question none of the notes answer but all of them imply
- A theme the author seems to be approaching from multiple angles

## Output format

```
# Constellation: [date]

> Draw time: YYYY-MM-DD HH:MM
> Notes drawn: N

[[note1]], [[note2]], [[note3]], [[note4]], [[note5]]

## Hidden theme
[The concept or tension at the centre of these notes — 3 to 5 sentences.
Cite which notes point to which aspect using [[wiki links]].]

## The question you might be asking
[One question. Not an answer. Not a summary. The question that all these notes
are orbiting without stating directly.]
```

Rules:
- Use [[wiki link]] format for all note references
- The question must be one sentence — never a list
- Do not write "You should...", "I recommend...", or "The theme is simply..."
- If the notes have nothing in common, say so directly — do not fabricate a connection
- This command does not write to any file — output goes to the terminal only. To save, run `/hirameki:journal` afterward

Write output in the language specified in `## Vault Structure` → `language`.
