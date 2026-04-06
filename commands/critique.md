---
description: >
  Multi-model writing critique — three AI models review in parallel, then a final
  judge synthesises. Use when the user wants writing reviewed, asks for feedback on
  an article/essay/draft, says "critique this", "review my writing", "幫我評審",
  or references /critique. Works on vault notes, local files, or pasted text.
---

Read `## Vault Structure` from `~/.claude/vault-local.md` (fall back to `~/.claude/CLAUDE.md` if not found) to get the vault path, research folder, and language.
If the section does not exist or required fields are missing, stop and respond: "Setup not complete. Please run `/hirameki:__init` first."

Input: $ARGUMENTS (a file path, [[wikilink]], or pasted text — required)
- If $ARGUMENTS is empty, ask: "Which piece of writing? (file path, wikilink, or paste the text)" and wait. Ask in the language specified in `## Vault Structure` → `language`.

## Purpose

Surface blind spots in writing by gathering independent perspectives from different model families. Different models have different aesthetic biases — the value is in where they disagree, not where they agree.

## Phase 1: Load the text

Resolve the input:
- File path → Read the file
- [[wikilink]] → find in vault, Read
- Pasted text → use directly

If the text is too long for a single CLI prompt (> 3000 chars), write it to a temp file and pass the path to each reviewer.

## Phase 2: Three-model parallel review

Launch three reviews in parallel. Each reviewer scores three dimensions on a 1-10 scale and provides specific feedback.

**Dimensions:**
- **Sensory density** (感官密度) — can the reader see, hear, smell, taste, touch what's described?
- **Structural tension** (結構張力) — does the piece pull the reader forward? Is there a question that needs answering?
- **Resonance** (觸動力) — does it land emotionally? Will the reader remember it tomorrow?

### Reviewer 1: Claude (Agent tool, model: "opus")

Dispatch a subagent with the text and scoring instructions. Focus: overall quality, structural flow, emotional landing.

### Reviewer 2: Codex CLI

```bash
codex exec "Review this writing. Score three dimensions (sensory density, structural tension, resonance) each 1-10. Then list: strongest line, weakest line, one structural suggestion, one thing to cut. Be specific with line references. Output in the vault language. Text: $(cat /tmp/critique-input.txt)"
```

If Codex fails (not installed, auth error, quota), fall back to a second Claude subagent (model: "sonnet") and note "[Codex unavailable, using Claude Sonnet]".

### Reviewer 3: Gemini CLI

```bash
gemini -p "Review this writing. Score three dimensions (sensory density, structural tension, resonance) each 1-10. Then list: strongest line, weakest line, one structural suggestion, one thing to cut. Be specific with line references. Output in the vault language." < /tmp/critique-input.txt
```

If Gemini fails, fall back to a Claude subagent (model: "haiku") and note "[Gemini unavailable, using Claude Haiku]".

## Phase 3: Synthesis

After all three reviews return, build a comparison table and final assessment:

```
# Critique: {title or first line}

> Date: YYYY-MM-DD HH:MM
> Source: {file path or "pasted text"}
> Reviewers: Opus / Codex / Gemini (or fallback noted)

## Scores

| Dimension | Opus | Codex | Gemini | Mean |
|-----------|------|-------|--------|------|
| Sensory density | X | X | X | X.X |
| Structural tension | X | X | X | X.X |
| Resonance | X | X | X | X.X |
| **Total** | X | X | X | **X.X** |

## Consensus (all three agree)
- ...

## Disagreements (where scores differ by 3+)
- ...

## Strongest line
- Opus: "..."
- Codex: "..."
- Gemini: "..."

## Weakest line
- Opus: "..."
- Codex: "..."
- Gemini: "..."

## Recommended edits
1. ...
2. ...
3. ...
```

## Phase 4: Save

Save the critique to `{vault}/_writing_lab/benchmark/YYYY-MM-DD-{title-slug}-critique.md` with frontmatter:

```yaml
---
tags:
  - critique
  - writing-lab
status: reference
source: claude-code
scores:
  sensory: X.X
  structure: X.X
  resonance: X.X
  total: X.X
---
```

Report the save location to the user.

## Rules

- Disagreements are the most valuable part — highlight them, don't average them away
- Never soften scores to be polite. A 3 is a 3
- "Strongest line" and "weakest line" must quote the actual text, not describe it
- If the writing is short (< 500 chars), skip the temp file and pass inline
- Write output in the language specified in `## Vault Structure` → `language`
