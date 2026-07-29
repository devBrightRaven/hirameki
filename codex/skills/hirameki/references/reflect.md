---
description: Answer a question in your own voice, drawing from your existing vault notes.
  Use when writing, thinking, or preparing — surfaces what you already believe.
argument-hint: "<question>"
---

Read `vault:` from `~/.claude/vault-local.md` for the vault root, then read `## Vault Structure` from `<vault>/AGENTS.md` (fall back to `~/.claude/vault-local.md`, then `~/.claude/CLAUDE.md` for setups predating 1.4.3) to get the vault path and the list of content folders.
If the section does not exist or required fields are missing, stop and respond: "Setup not complete. Please run `/hirameki:__init` first."

Input: $ARGUMENTS
- A question or prompt to answer in the vault author's voice.
- If $ARGUMENTS is empty, ask: "What do you want to reflect on?" in the language specified in `## Vault Structure` → `language`.

---

## Process

### Step 1 — Analyse writing style

Scan completed articles in content folders (exclude `drafts/` and `thoughts/` subdirectories if present).

Extract:
- Sentence patterns and typical length
- Vocabulary level and recurring phrasing
- Argument structure (how claims are introduced, supported, qualified)
- Rhetorical moves that appear repeatedly

### Step 2 — Extract positions

Search the full vault for notes relevant to the question. Prioritise:
- Notes in content folders that address the topic directly
- `0 Material/` permanent concept cards related to the question
- Journal entries where the author took a position on the topic
- Daily notes with relevant observations

Limit: 5 most relevant sources.

### Step 3 — Compose answer

Write an answer using the identified style and the extracted positions. Rules:
- Match the length of a typical paragraph from their writing
- Use the author's own arguments, not general knowledge
- Do not introduce positions the vault does not support
- If the vault has contradictory positions on the topic, surface the tension rather than resolving it

### Step 4 — Output

```
[Answer]
The answer in the author's voice. One to three paragraphs.

[Sources]
- [[note-title]] — the specific position or passage drawn from
(Limit: 5 sources)

[Confidence]
- Vault-supported: which parts have direct evidence
- Style-inferred: which parts extend the style without direct backing
- Tensions: any contradictions found across vault notes
```

Always print the full output to the terminal. Do not write to a file unless the user asks.
If the user asks to save, write to `{research}/reflect/YYYY-MM-DD-{question-summary}.md`. Print the full path after writing.

---

Write output in the language specified in `## Vault Structure` → `language`.
