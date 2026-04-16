---
description: >
  Analyze a GitHub repo to extract transferable techniques and evaluate adoption fit.
  Use when the user shares a GitHub URL and wants to understand, evaluate, or learn from
  a repository. Triggers on "analyze this repo", "is this worth installing", "check this out",
  "研究這個 repo", "這個對我們有沒有用", "分析這個專案", or any GitHub link with
  evaluation intent. Even a bare GitHub URL with no instruction counts.
---

Read `## Vault Structure` from `~/.claude/vault-local.md` (fall back to `~/.claude/CLAUDE.md` if not found) to get the vault path, content folders, and language.
If the section does not exist or required fields are missing, stop and respond: "Setup not complete. Please run `/hirameki:__init` first."

Input: $ARGUMENTS (a GitHub URL — required)
- If $ARGUMENTS is empty, ask: "Which repo? (GitHub URL or owner/repo)" and wait. Ask in the language specified in `## Vault Structure` → `language`.

A repo you won't adopt can still teach you something worth keeping.

## URL Parsing

Accept any of these and extract `owner` and `repo`:
- `https://github.com/owner/repo` or `https://github.com/owner/repo/tree/...`
- `owner/repo`

Strip prefix, take first two path segments, discard the rest.

## Phase 1: Fetch (parallel)

Launch these in parallel:

```bash
gh repo view owner/repo --json description,url,stargazerCount,primaryLanguage,updatedAt
gh api repos/owner/repo/readme -q .content | base64 -d
gh api repos/owner/repo/git/trees/HEAD?recursive=1 -q '.tree[].path' | head -150
```

After the tree is fetched, identify 3-5 key source files (entry points, config, main modules) and fetch them:

```bash
gh api repos/owner/repo/contents/path/to/file -q .content | base64 -d
```

## Phase 2: Analyze

Two tracks. Track A always runs. Track B runs unless the repo is a pure pattern/demo.

### Track A: Technique Extraction

For each interesting part of the repo, extract:

| Field | Fill |
|-------|------|
| **Pattern** | Short name |
| **What** | The technique in 1-2 sentences |
| **Why interesting** | What problem does it solve? |
| **Transferable to** | Which of the user's projects could use this? |
| **Action** | Concrete next step — not "keep in mind" or "remember" |

Skip standard practices (git flow, MIT license) and language-specific idioms that don't transfer.

### Track B: Adoption Evaluation

**Before writing the comparison table**, read the user's CLAUDE.md and project memory to identify their actual tools and workflows. The "We currently use" column must contain real tool names — never "existing solution" or "current approach".

Classify the repo:

| Type | Focus |
|------|-------|
| **Tool** | Feature-by-feature comparison table |
| **Framework** | Architecture comparison (rendering, state, build) |
| **Library** | Integration cost (API, deps, bundle size, maintenance) |
| **Pattern** | Skip Track B — Track A is the full analysis |

Comparison table format:

| Feature | Repo offers | We currently use | Delta |
|---------|-------------|------------------|-------|
| ... | ... | (real tool name) | (measurable difference) |

Verdict — one of:
- **adopt** — with specific next step and timeline
- **defer** — with trigger condition (what would change the decision)
- **reject** — acknowledge what IS good, state what to do instead

## Phase 3: Validate (subagent)

Dispatch a Sonnet subagent to check the Phase 2 output:

- **Completeness**: Track A has patterns (or explicit reasoning why none). All significant sections addressed.
- **Grounding**: No unverified claims. "We currently use" has real names. Delta is measurable.
- **Actionability**: Every verdict has a next step. Patterns have concrete actions. Adopt/defer has timeline or trigger.
- **Real-frequency check**: How often per week does the user encounter the problem this repo solves? If < 1 time per week, downgrade adopt to defer-with-test. Read `_policies/ai-philosophy.md` before finalizing verdict -- if the tool automates something the user believes should stay manual, flag as philosophical conflict.

If any check fails, fix before presenting.

**Sizing exception**: For small repos (< 10 files), skip the subagent and do a quick inline check instead.

## Output

Write output in the language specified in `## Vault Structure` → `language`.

```
# Mekiki: {repo name}

> Scan time: YYYY-MM-DD HH:MM
> Repo: owner/repo — {description}
> Stars: N | Language: X | Last updated: YYYY-MM-DD

## Extracted Patterns

### 1. {pattern name}
- **What:** ...
- **Why interesting:** ...
- **Transferable to:** ...
- **Action:** ...

(repeat)

## Adoption Evaluation

| Feature | Repo offers | We currently use | Delta |
|---------|-------------|------------------|-------|

**Verdict:** adopt / defer / reject
**Reason:** one sentence
**Next step:** ...

## Validation
PASS: N / FAIL: N
(only show details if any FAIL)
```

## After Analysis

- If **adopt**: offer to clone/install and save a vault note to `{research folder}/mekiki-{repo-name}.md` with frontmatter `tags: [mekiki, adopt]` and `status: reference`
- If **defer** or **reject**: save a brief vault note to `{research folder}/mekiki-{repo-name}.md` with frontmatter `tags: [mekiki, {verdict}]` and `status: reference`, recording the decision and rationale so future sessions don't re-evaluate

Use `[[wiki link]]` format for any vault note references.
