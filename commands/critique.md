---
description: Multi-agent writing critique for draft articles — 3-model consensus scoring on sensory density, structure, and emotional resonance
---

Read `## Vault Structure` from `~/.claude/vault-local.md` (fall back to `~/.claude/CLAUDE.md` if not found) to get the vault path.
If the section does not exist or required fields are missing, stop and respond: "Setup not complete. Please run `/hirameki:__init` first."

Run a multi-agent writing review on a draft article. Uses three models (Claude Opus, Codex GPT via codex CLI, Gemini Pro via gemini CLI) to score and critique, then optionally runs an Opus final review.

Input: $ARGUMENTS (file path — required)
- If $ARGUMENTS is a relative path, resolve it from the vault root.
- If $ARGUMENTS is empty, check for the most recently modified .md file in the vault's draft folders. Show the candidate and ask for confirmation.
- If the file does not exist, stop and respond with the error.

---

## Review Framework

Three dimensions, scored 1-10:
1. **感官密度** (Sensory density): How vivid and specific are physical details? Where does it show vs tell?
2. **結構張力** (Structural tension): Does tension build and release? Are transitions smooth? Does the ending land?
3. **觸動力** (Emotional resonance): Does the reader feel something real? Is vulnerability authentic or performed?

Each reviewer also identifies:
- Top 3 strongest sentences (with reason)
- Top 3 weakest sentences (with reason)
- One structural suggestion

---

## Execution

### Phase 1: Initial Review (3 models in parallel)

Launch three reviewers **in parallel** using Agent tool and Bash:

**Reviewer 1 — Claude Opus (Agent, model: opus)**
Prompt template:
```
Read the file at "{file_path}" and evaluate it as a writing critic.
Score on three dimensions (1-10 each):
1. 感官密度 (Sensory density)
2. 結構張力 (Structural tension)
3. 觸動力 (Emotional resonance)
Also identify: Top 3 strongest sentences, Top 3 weakest sentences (and why), One structural suggestion.
Write in 繁體中文. Be brutally honest.
```

**Reviewer 2 — Codex GPT (Bash, codex CLI)**
```bash
codex exec "Read the essay below and evaluate it as a writing critic.
Score on three dimensions (1-10 each):
1. 感官密度 (Sensory density)
2. 結構張力 (Structural tension)
3. 觸動力 (Emotional resonance)
Also identify: Top 3 strongest sentences, Top 3 weakest sentences (and why), One structural suggestion.
Write in 繁體中文. Be honest and critical.

$(cat '{file_path}')"
```

**Reviewer 3 — Gemini Pro (Bash, gemini CLI)**
```bash
gemini -p "$(cat <<'PROMPT'
Read the essay below and evaluate it as a writing critic.
Score on three dimensions (1-10 each):
1. 感官密度 (Sensory density)
2. 結構張力 (Structural tension)
3. 觸動力 (Emotional resonance)
Also identify: Top 3 strongest sentences, Top 3 weakest sentences (and why), One structural suggestion.
Write in 繁體中文. Be honest and critical.

$(cat '{file_path}')
PROMPT
)" --allowed-mcp-server-names none
```

### Phase 2: Compile Results

After all three return, compile into a comparison table:

```
## 三模型評審對照

| 維度 | Opus | Codex GPT | Gemini Pro |
|------|------|-----------|------------|
| 感官密度 | X | X | X |
| 結構張力 | X | X | X |
| 觸動力 | X | X | X |

### 共識（2/3 以上一致）
- [issues all or most reviewers flagged]

### 最強句（多家選中）
- [sentences selected by 2+ reviewers]

### 最弱句（多家選中）
- [sentences flagged by 2+ reviewers]

### 各家獨有觀點
- Opus: ...
- GPT-5.4: ...
- Gemini: ...
```

### Phase 2.5: Write Review File

Calculate consensus score for each dimension: average of all three models, rounded to one decimal.

Write the review to `{vault}/_writing_lab/benchmark/{YYYY-MM-DD}-{article-slug}-review.md`:

```markdown
---
tags:
  - writing-lab
  - review
status: reference
source: claude-code
created: {YYYY-MM-DD}
article: "{article filename}"
scores:
  sensory: {consensus average}
  structure: {consensus average}
  resonance: {consensus average}
  overall: {average of three consensus scores}
models:
  - opus
  - codex
  - gemini
phase: initial
---

# Review: {article title}

## 評分對照

| 維度 | Opus | Codex GPT | Gemini Pro | **共識** |
|------|------|-----------|------------|----------|
| 感官密度 | X | X | X | **X.X** |
| 結構張力 | X | X | X | **X.X** |
| 觸動力 | X | X | X | **X.X** |
| | | | | **總分: X.X** |

## 共識（2/3 以上一致）
- [issues all or most reviewers flagged]

## 最強句（多家選中）
- [sentences selected by 2+ reviewers, with which models selected them]

## 最弱句（多家選中）
- [sentences flagged by 2+ reviewers, with reasons]

## 各家獨有觀點
- **Opus**: ...
- **GPT-5.4**: ...
- **Gemini**: ...

## 結構建議
- **Opus**: ...
- **GPT-5.4**: ...
- **Gemini**: ...
```

Print the file path after writing. Then ask: "要根據這些意見改稿嗎？還是先跑終審？"

### Phase 3: Final Review (optional, on user request)

After edits are made, run a final review with **Opus + Codex in parallel**:

**Opus Final (Agent, model: opus)**
Prompt template:
```
Read the file at "{file_path}" and do a final review.
The following issues were identified in the initial review: [list issues from Phase 2 consensus]
For each, report: Fixed / Partially fixed / Not fixed / New issue introduced.
Then do a fresh read: overall impression, score all three dimensions, any NEW weaknesses, top 3 strongest moments, one remaining fix if the author has energy.
Write in 繁體中文. Be honest.
```

**Codex Final (Bash, codex CLI)**
Same prompt structure as Opus Final, via `codex exec`.

Compile both into a final comparison. Then **append** the final review results to the same benchmark file created in Phase 2.5:

```markdown

---

## 終審（Phase 3）

**終審模型**: Opus + Codex GPT

| 維度 | Opus | Codex GPT | **共識** |
|------|------|-----------|----------|
| 感官密度 | X | X | **X.X** |
| 結構張力 | X | X | **X.X** |
| 觸動力 | X | X | **X.X** |
| | | | **總分: X.X** |

### 第一輪問題修正狀態
| 問題 | 狀態 |
|------|------|
| [issue] | Fixed / Partially fixed / Not fixed |

### 新問題
- [any new issues introduced by edits]

### 最強句（終審版）
- [top 3 from final version]

### 剩餘建議
- [one remaining fix if any]
```

Also update the frontmatter `phase` field to `final` and update the scores to the final review scores.

Print the updated file path. Present the results to the user.

---

## Rules

- All reviewers run in **parallel** (use background agents/commands).
- Never modify the article file during review — read only.
- Present results in 繁體中文.
- Opus reviewers use `model: opus` parameter. Do NOT use Sonnet for writing review — writing critique requires judgment depth.
- If codex or gemini CLI is not available, skip that reviewer and note it in output.
- Focus on **consensus signals**: issues flagged by 2+ models are high priority; single-model flags are informational.
