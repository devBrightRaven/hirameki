---
description: >
  Analyze external content and evaluate its value. GitHub repos get full adoption
  analysis (adopt/defer/reject verdict). Articles and text get structured vault
  capture with a lightweight integration verdict.
  Triggers on: GitHub URL, "analyze this repo", "is this worth installing", "check this out",
  "研究這個 repo", article URL, "read this", "digest this", "把這個存進 vault", "這篇文章不錯",
  or any URL / pasted text with evaluation or vault-storage intent.
---

Read `vault:` from `~/.claude/vault-local.md` for the vault root, then read `## Vault Structure` from `<vault>/AGENTS.md` (fall back to `~/.claude/vault-local.md`, then `~/.claude/CLAUDE.md` for setups predating 1.4.3) to get the vault path, content folders, inbox folder, research folder, and language.
If the section does not exist or required fields are missing, stop and respond: "Setup not complete. Please run `/hirameki:__init` first."

Input: $ARGUMENTS (required — GitHub URL, article URL, pasted text, or file path)
- If $ARGUMENTS is empty, ask: "What to analyze? (GitHub URL, article URL, pasted text, or file path)" in the language specified in `## Vault Structure` → `language`. Wait for the answer.

A repo you won't adopt can still teach you something worth keeping.

---

## Input routing

Detect input type using this priority order. Apply the first rule that matches:

1. Input matches `github\.com/[^/]+/[^/?#]+` or looks like `owner/repo` (two segments separated by `/`, no protocol, no spaces) → **Repo branch**
2. Input starts with `http://` or `https://` → **Article branch** (URL)
3. Input starts with `/`, `C:`, `D:`, `./`, `..\` or is a recognisable file path → **Article branch** (file)
4. Anything else (multi-line text, single-line prose, paste) → **Article branch** (paste)

Print one line before proceeding:
- Repo branch: `→ Repo analysis: owner/repo`
- Article branch: `→ Article ingest: {title or first 60 chars of input}`

---

## Repo branch

### URL Parsing

Accept any of these and extract `owner` and `repo`:
- `https://github.com/owner/repo` or `https://github.com/owner/repo/tree/...`
- `owner/repo`

Strip prefix, take first two path segments, discard the rest.

### Phase 1: Fetch (parallel)

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

### Phase 2: Analyze

Two tracks. Track A always runs. Track B runs unless the repo is a pure pattern/demo.

#### Track A: Technique Extraction

For each interesting part of the repo, extract:

| Field | Fill |
|-------|------|
| **Pattern** | Short name |
| **What** | The technique in 1-2 sentences |
| **Why interesting** | What problem does it solve? |
| **Transferable to** | Which of the user's projects could use this? |
| **Action** | Concrete next step — not "keep in mind" or "remember" |

Skip standard practices (git flow, MIT license) and language-specific idioms that don't transfer.

#### Track B: Adoption Evaluation

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

### Phase 3: Validate (subagent)

Dispatch a Sonnet subagent to check the Phase 2 output:

- **Completeness**: Track A has patterns (or explicit reasoning why none). All significant sections addressed.
- **Grounding**: No unverified claims. "We currently use" has real names. Delta is measurable.
- **Actionability**: Every verdict has a next step. Patterns have concrete actions. Adopt/defer has timeline or trigger.
- **Real-frequency check**: How often per week does the user encounter the problem this repo solves? If < 1 time per week, downgrade adopt to defer-with-test. Read `_policies/ai-philosophy.md` before finalizing verdict — if the tool automates something the user believes should stay manual, flag as philosophical conflict.

If any check fails, fix before presenting.

**Sizing exception**: For small repos (< 10 files), skip the subagent and do a quick inline check instead.

### Repo branch output

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

After analysis:
- If **adopt**: offer to clone/install and save a vault note to `{research folder}/mekiki-{repo-name}.md` with frontmatter `tags: [mekiki, adopt]` and `status: reference`
- If **defer** or **reject**: save a brief vault note to `{research folder}/mekiki-{repo-name}.md` with frontmatter `tags: [mekiki, {verdict}]` and `status: reference`, recording the decision and rationale so future sessions don't re-evaluate

Use `[[wiki link]]` format for any vault note references.

---

## Article branch

### Phase 1: Capture

Fetch or read the content based on input type:

- **URL**: Use WebFetch to extract clean content. If not available, ask the user to paste the content.
- **File path**: Read the file content.
- **Pasted text**: Use the text directly.

If the content exceeds 3000 words, summarise to ~800 words while preserving key claims and data.

Create an immutable source note:

Write target: `{inbox}/YYYY-MM-DD-{source-slug}.md`

```markdown
---
tags:
  - ingest
  - {topic-tag}
status: reference
source: external
ingested: YYYY-MM-DD HH:MM
original_url: {url if applicable}
---

# {title}

> Ingested: YYYY-MM-DD HH:MM
> Source: {url or "pasted text" or file path}

## Content

{full extracted content or ~800 word summary if >3000 words}

## Key Concepts

- {concept 1}: one-sentence description
- {concept 2}: one-sentence description
- (3-7 concepts)
```

Show the source note content and target path. Wait for confirmation before writing.

### Phase 2: Cross-reference scan

Scan all content folders for notes related to the key concepts from Phase 1.

For each related note found:
1. What it covers that relates to the ingested content
2. What the ingested content adds (new perspective, contradiction, evidence, update)
3. Suggested action: add `[[wiki link]]` to the ingested note, or update existing note

### Phase 3: Integration verdict

After cross-reference scan, assess whether the article's main claims or methods are worth integrating into work or thinking:

```
## Worth integrating?

**Verdict:** integrate / revisit-later / skip
**Reason:** one sentence
**Next step:** one concrete action (e.g. "draft a concept card on {X}", "add to {writing outline}", "no further action")
```

Base the verdict on:
- Whether the article's claims conflict with or extend existing vault notes
- Whether the methods or frameworks described are applicable to current projects
- Frequency of relevance: if the problem the article addresses comes up less than once a week, lean toward revisit-later

### Article branch output

```
# Mekiki: {title}

> Source note: {inbox}/YYYY-MM-DD-{slug}.md
> Key concepts: {list}
> Related notes found: N

## Cross-references

1. [[existing-note-1]]
   - Relation: {what connects them}
   - Suggested: add [[YYYY-MM-DD-{slug}]] as reference

2. [[existing-note-2]]
   - Relation: {what connects them}
   - Suggested: {specific update}

## No related notes found for
- {concept with no matches}

## Worth integrating?

**Verdict:** integrate / revisit-later / skip
**Reason:** ...
**Next step:** ...
```

Always print the full output to the terminal.

**Wait for user confirmation before making any changes to existing notes.**

After confirmation:
- Write the source note to inbox (if not already done in Phase 1)
- Add `[[wiki link]]` references to the confirmed existing notes
- Print the full path after writing each file

---

## Shared rules

- Do not hardcode vault paths — resolve the root from `vault-local.md` and folders from `<vault>/AGENTS.md` every time
- Use `[[wiki link]]` format for all vault note references
- Show filename, branch taken, and full path — wait for confirmation before any vault write
- Print the full path after writing
- Write output in the language specified in `## Vault Structure` → `language`
