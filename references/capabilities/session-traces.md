# Session traces

Shared by triage, journal and handoff. Collect candidates before deciding which
artifact to propose. This contract changes selection, not write authorization.

## Candidate-first gap check

Use the current conversation and its named evidence to identify worthwhile clues:
an emerging idea, explicit hesitation or preference, a rejected alternative,
a correction, changed judgment, unresolved question, counterexample, or a pickup
constraint. Keep a clue when losing its context would make later understanding or
continuation harder. Routine progress alone belongs in wrap. Do not manufacture
clues, infer private motives, fill a quota, or force every artifact each session.

Compare each candidate with the bounded saved baseline already authorized by the
calling workflow. Read the relevant record and section before claiming coverage.
A matching title, final decision, closeout report or link alone does not establish
that the rationale, alternative, uncertainty and pickup constraints are covered.
Choose new, append, reference-existing, or skip for each candidate. Prefer a small
append to a clearly matching note over duplicating its event narrative. Show a
concise candidate/disposition summary with the source and coverage reason before
the artifact plan or draft; this summary adds no confirmation stop. If a relevant
record is unavailable, mark coverage unknown, never fully covered. Do not broaden
the search to the whole vault or quietly discard a candidate to avoid duplication.

## Emerging clues in journal

A clue need not qualify as a decision, judgment update, lesson or concept card.
In create or append mode, use an optional `Emerging clues` section (translated to
the vault language, for example `未成形線索`). Omit it when there is no material.
For each retained clue preserve:

- Source and context: speaker or operation, minimal quote or evidence locator,
  and the question or situation that prompted it. Label compaction-only evidence.
- Observation: what was actually stated or observed, including explicit doubts,
  preferences or alternatives considered; a statement is not proof of its claim.
- Interpretation: any inference, explicitly labeled; omit if none is warranted.
- Unknown: what remains unresolved and what would make revisiting useful; do not
  invent a deadline, owner, commitment or action just to complete the format.

These fields do not weaken the separate judgment-update evidence gate. Keep an
immature clue here rather than constructing a nonexistent before/after judgment.
Do not silently turn a clue into an Open item, accepted decision or personal rule.

## Handoff and lesson selection

Completed authorized work can still leave pickup value: a deferred validation,
authorization boundary, environment constraint, recovery caveat or revisit trigger.
Propose handoff when that context is needed for future pickup and is not adequately
preserved. A wrap Next line is sufficient only when the required context is also
present or linked to a verified relevant section. If it is fully covered, reference
that record without making a duplicate handoff. An uncommitted idea alone does not
create unfinished work; keep it in journal unless it has actual pickup relevance.

A single traceable event may justify a narrowly scoped lesson. State the evidence
count, scope, uncertainty, counterexample (or that none is known), and recheck
condition. It need not generalize across projects. The lesson must add a useful
reusable point or boundary beyond the raw event; if that point is already fully
recorded, reference or append there instead. An untested hunch stays a journal clue.
No lesson proposal automatically promotes a global rule or proves repeated success.

## Bounded lesson lookup and disposition

Before deciding a lesson candidate is new, check whether `{journal}/lessons/`
exists, then search file names and Markdown bodies there for the candidate's
specific topic, event identifier or distinctive phrase. Search across dates:
today's journal and the newest handoff are not a lesson inventory. Use at most
three literal queries derived from the candidate, never a vault-wide scan.
Inspect at most 20 matching files per run, once each; read a selected match in
full before using it. Report the queries, inspected paths and any remaining
matches or read errors. A missing directory confirmed by a direct check means
no saved lessons there; a failed listing/search or truncated result means
coverage unknown, not absence. Do not follow links outside this folder.

Compare the evidence identity, reusable point and scope, not just title or word
overlap. A copied event is not another independent observation. Choose:

- **reference-existing**: the same evidence and boundary are fully covered.
  Show the existing path/section and do not propose a write.
- **append**: exactly one verified existing lesson covers the same topic and
  scope, but the candidate adds evidence, a counterexample, a narrower boundary
  or a recheck outcome. Keep that existing file as the target, regardless of date.
- **new**: completed bounded lookup found no suitable lesson. Use the new-entry
  format and today's filename; do not overwrite a file already at that path.
- **unresolved**: coverage is partial/unreadable or multiple plausible targets
  remain. Show that limitation and the alternatives. Do not choose an append
  target or claim deduplication passed. Preserve the candidate in the journal
  draft as unresolved when useful; let the normal edit/action interaction
  resolve the target rather than silently creating a duplicate lesson.

## Lesson append procedure

Before an append disposition, verify the target is UTF-8 (an existing UTF-8 BOM
may remain in its original prefix). If encoding is unknown or not UTF-8, report
unresolved and refuse append; do not transcode it or mix encodings.
For an append disposition, show `mode: append`, the existing full target path,
and the complete append block before requesting the normal save action. Preserve
all original bytes, frontmatter, title, creation date and earlier claims. The
displayed draft is the append block, not a regenerated replacement file. Use:

```markdown
---

## Evidence addendum — YYYY-MM-DD HH:MM
- Source and event identity: <quote/output locator; distinguish copy from new event>
- New evidence or counterexample: <observation, interpretation and unknown separated>
- Effect on the earlier lesson: <supports, narrows, contradicts or unresolved; why>
- Scope and evidence limits: <independent event count where known; unknown otherwise>
- Recheck condition: <observable trigger, or explicitly unknown>
```

Translate headings and labels into the vault language. Do not rewrite an earlier
claim even when contradicted; the dated addendum records the correction and links
to the earlier section. No new evidence means reference-existing, not an empty
addendum. Before saving, re-read the target and compare it with the full original
read for this draft. If changed or unavailable, stop that write and redisplay a
rebased draft for fresh approval; do not reuse an earlier save-all approval.
On approval append exactly the displayed block (including the shown separator),
including any leading line breaks needed to separate it from an original without
a final newline; include those line breaks in the displayed block itself. Keep
the original bytes and line endings untouched. Serialize the displayed append
block as UTF-8 with LF line endings; do not promise CRLF conversion. If the
original uses CRLF, disclose before approval that the appended LF block will
leave mixed line endings. Never normalize the original to make them match.
Then verify original bytes remain an unchanged prefix and the suffix equals the
approved block. Report the existing path and append result. New-entry saves must
check the target is absent and never overwrite on a filename collision.

## Persistence and downstream readers

Candidate collection, bounded comparison and drafting may proceed automatically.
Saving still requires the calling workflow's visible draft, full target path and
user approval. Do not add background saves, hooks, source registration, ingestion,
rule promotion or new confirmation menus. Preserve save-this/save-all boundaries.
Downstream readers require their own configured sources, filters and section
mappings; a saved note alone never proves it was ingested. Preserve evidence types
in the note rather than calling the entire mixed narrative an observation.
