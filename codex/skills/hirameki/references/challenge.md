---
description: >
  Expose the weaknesses in an argument: scan the vault for every claim on the topic,
  then surface contradictions, unverified assumptions, logic gaps, missing evidence.
  Use when the user wants a position stress-tested, or says
  "幫我挑毛病", "這說法站得住嗎", "反駁我", "有什麼漏洞",
  "poke holes in this", "what am I missing", "argue against this", "is this defensible".
  Not for questioning a plan or offer interactively (grill-me), not for a choice (decide).
argument-hint: "<argument or topic>"
---

Read `vault:` from `~/.claude/vault-local.md` for the vault root, then read `## Vault Structure` from `<vault>/AGENTS.md` (fall back to `~/.claude/vault-local.md`, then `~/.claude/CLAUDE.md` for setups predating 1.4.3) to get the vault path, the research folder location, and the list of content folders.
If the section does not exist or required fields are missing, stop and respond: "Setup not complete. Please run `/hirameki:__init` first."

Input: $ARGUMENTS
- If $ARGUMENTS is empty, ask: "Challenge which argument or topic?" in the language specified in `## Vault Structure` → `language`. Wait for the answer.
- If $ARGUMENTS ends with `save`, strip `save` and write the result to a file after analysis.

Scan scope: all vault files that mention the topic.

---

## Analysis steps

1. Collect all claims and arguments about the topic from the vault
2. Examine the logical structure and evidence base of each claim
3. For each claim, check only what applies:
   - **Internal contradiction**: conflicting statements across vault files
   - **Unverified assumption**: claim rests on an unproven premise
   - **Logic gap**: missing steps in the argument
   - **Evidence gap**: claim lacks supporting data or examples
4. Cite `[[filename]]` and relevant passage for each weakness found

---

## Output structure

```
## Claims
All major claims about this topic found in the vault.
For each: claim (one sentence) — source [[filename]]

## Weaknesses
For each claim that has weaknesses:

### Claim: {claim}
- Internal contradiction: {details, cite [[filename]]} (omit if none)
- Unverified assumption: {details} (omit if none)
- Logic gap: {details} (omit if none)
- Evidence gap: {details} (omit if none)

(Omit entirely any claim with no weaknesses)

## Assessment
Overall: solid / mostly solid with gaps / needs major work
Top 1–3 weaknesses worth addressing first.
```

---

## Write logic

Write target: `{research}/challenge/YYYY-MM-DD-{topic-summary}.md`

Always print the full output to the terminal first.

If `save` was in the input (or user requests saving):
- Show filename and full path — wait for confirmation before writing
- Print the full path after writing

---

## Rules

- If search results exceed 20 files, list only the 20 most relevant
- Use `[[wiki link]]` format for all file references
- Timestamps use local time in HH:MM (24-hour)
- Write output in the language specified in `## Vault Structure` → `language`
