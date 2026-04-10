---
description: >
  Structured ingestion of external content into the vault.
  Use when the user shares a URL, pastes article text, or references an external document
  they want to digest into the vault. Triggers on "read this", "digest this", "save this to vault",
  "把這個存進 vault", "這篇文章不錯", or any URL/text with vault-storage intent.
---

Read `## Vault Structure` from `~/.claude/vault-local.md` (fall back to `~/.claude/CLAUDE.md` if not found) to get the vault path, inbox folder, and the list of content folders.
If the section does not exist or required fields are missing, stop and respond: "Setup not complete. Please run `/hirameki:__init` first."

Input: $ARGUMENTS (required — URL, pasted text, or file path)
- If $ARGUMENTS is empty, ask: "What to ingest? (URL, paste text, or file path)" in the language specified in `## Vault Structure` → `language`. Wait for the answer.

## Phase 1: Capture

Create an immutable source note in the inbox folder.

### URL input
Use WebFetch or Defuddle (if available) to extract clean content from the URL. If the tool is not available, instruct the user to paste the content.

### Pasted text input
Use the text directly.

### File path input
Read the file content.

### Source note format

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

{full extracted content or summary if too long (>3000 words → summarise to ~800 words, preserve key claims and data)}

## Key Concepts

- {concept 1}: one-sentence description
- {concept 2}: one-sentence description
- (3-7 concepts)
```

## Phase 2: Cross-reference scan

Scan all content folders for notes related to the key concepts extracted in Phase 1.

For each related note found:
1. What it covers that relates to the ingested content
2. What the ingested content adds (new perspective, contradiction, evidence, update)
3. Suggested action: add `[[wiki link]]` to the ingested note, or update existing note's content

## Phase 3: Present suggestions

Output format:

```
# Ingest: {title}

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
- {concept with no matches — potential new standalone note?}
```

**Wait for user confirmation before making any changes to existing notes.**

After confirmation:
- Add `[[wiki link]]` references to the confirmed existing notes
- For concepts with no matches: ask if the user wants to create a new standalone note

## Rules

- The source note in inbox/ is created immediately (Phase 1) — it is the immutable raw capture
- Existing notes are NEVER modified without explicit confirmation
- Use [[wiki link]] format for all references
- Do not summarise the content unless it exceeds 3000 words
- Show the source note content and path, and wait for confirmation before writing
- Print the full path after writing each file
- All output in the language specified in `## Vault Structure` → `language`
