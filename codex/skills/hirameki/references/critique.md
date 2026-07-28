---
description: Multi-reviewer writing critique for draft articles, with honest reviewer provenance
---

Resolve the vault through the Hirameki adapter, then run an independent writing review on a draft article.
If vault configuration is missing or incomplete, stop and respond: "Setup not complete. Please run `/hirameki:__init` first."

Input: `$ARGUMENTS` (file path, required)

- Resolve relative paths from the vault root.
- If empty, find the most recently modified Markdown file in configured draft folders, show it, and wait for confirmation.
- Stop if the file does not exist.
- Never modify the article during review.

## Review framework

Score 1-10:

1. 感官密度：具體感官細節與 show-versus-tell。
2. 結構張力：張力、轉折、節奏與結尾。
3. 觸動力：真實情感、脆弱性與讀者共鳴。

Each reviewer must also identify the three strongest sentences, three weakest sentences with reasons, and one structural suggestion. Write in Traditional Chinese.

## Initial review

Launch two independent native Codex reviewers in parallel when subagents are available. Give each reviewer the article content or a readable path, the framework above, and these constraints:

- read only;
- no file edits, network actions, publishing, or other external side effects;
- do not read unrelated vault content;
- return scores plus cited sentences and reasons.

If native subagents are unavailable, perform one inline Codex review and label it as a single-reviewer result.

An optional external model may be added only when its installed CLI is available and its current `--help` documents a non-interactive invocation that can be constrained to read-only work. Pass article input through documented stdin or a prompt file, never shell interpolation. Do not pass guessed or unsupported flags. Skip the reviewer when safe isolation is unclear and state the gap.

Record each reviewer's actual route and model when known. Two Codex reviewers are independent reviewers, not two different models.

## Compile

Use columns for the reviewers that actually ran:

```markdown
## 審閱對照

| 維度 | Reviewer A | Reviewer B | Optional external | 共識 |
|---|---:|---:|---:|---:|
| 感官密度 | X | X | X or N/A | X.X |
| 結構張力 | X | X | X or N/A | X.X |
| 觸動力 | X | X | X or N/A | X.X |

### 共識
- [issues flagged by more than half of reviewers]

### 各家獨有觀點
- Reviewer A: ...
- Reviewer B: ...
- Optional external: ...
```

Average only the valid scores from reviewers that actually ran. Never claim multi-model consensus from multiple reviewers using the same model.

## Save review

After showing the result, propose writing it to:

`{vault}/_writing_lab/benchmark/{YYYY-MM-DD}-{article-slug}-review.md`

Wait for confirmation before writing. Use this frontmatter, listing only actual reviewers:

```yaml
---
tags: [writing-lab, review]
status: reference
source: codex
created: YYYY-MM-DD
article: "article filename"
scores:
  sensory: X.X
  structure: X.X
  resonance: X.X
  overall: X.X
reviewers:
  - route: native-subagent
    model: known-model-or-unknown
phase: initial
---
```

Include the score table, consensus issues, strongest and weakest sentences with reviewer attribution, unique observations, and structural suggestions. Print the saved path and ask whether the user wants to revise or request a final review.

## Final review

On request after edits, launch two fresh independent reviewers under the same read-only rules. For every initial consensus issue, report `Fixed`, `Partially fixed`, `Not fixed`, or `New issue introduced`; then rescore the three dimensions and identify new weaknesses, strongest moments, and one remaining fix.

Show the final comparison. With confirmation, append it to the same benchmark file and update `phase` and scores. Preserve initial results and record the final reviewers' actual routes and models.

## Integrity rules

- Run independent reviewers in parallel when supported.
- Reviewer count and model count are separate facts.
- Consensus means more than half of reviewers agreed; a single review has no consensus claim.
- Skip unavailable or unsafe external reviewers and disclose the gap.
- Vault output is knowledge, not Codex runtime configuration.
