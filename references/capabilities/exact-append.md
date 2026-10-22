# Exact append

Use this procedure for existing-note appends in triage and journal, including
Lesson evidence and Journal clues. It does not authorize a save, create a new
note, modify earlier completion statuses, or bypass the calling workflow's gate.

Locate the delivered `scripts/exact_append.py`: Claude uses
`${CLAUDE_PLUGIN_ROOT}/scripts/exact_append.py`; Codex uses `../../scripts/exact_append.py`
relative to this capability file. Use Python 3.10+; pass each path/hash as a
separate argument and never embed draft text in executable shell code.
If Python, this helper, or the host's safe
execution capability is unavailable, keep the draft and refuse append. Never fall
back to Write/Edit, text-mode append, a hand-built shell/Python writer, or another
checkout. Do not install tools or weaken host permissions to make a save succeed.

## Freeze before display

1. Put the proposed UTF-8 append bytes in a private session temporary draft file
   **outside the vault**, with explicit LF separators and the intended final
   newline. Do not use a vault note as a staging file. Preserve existing BOM,
   CRLF/LF, frontmatter and the absence of a final newline in the original note.
2. Run `python -B -X utf8 <helper> prepare --root <resolved-vault> --target <relative-note>
   --draft <session-draft> --plan <new-session-plan.json>`. This reads/locks the
   existing note and creates only a private plan, never a vault note or sidecar.
3. Display its full `target` and `draft_text` verbatim in a Markdown code fence;
   use the helper's complete `display_markdown` value verbatim as the actual
   assistant reply block, rather than constructing a new fence or whitespace.
   Do not translate its metadata keys or add a blank line inside its fence.
   For a suffix without final LF or containing CR the renderer uses a JSON string: the decoded
   UTF-8 string is the exact suffix, not the fence's formatting newline.
   disclose `draft_bytes`, `draft_sha256`, `plan_sha256`, and
   `trailing_newline_bytes` (including zero). Leading separator newlines belong
   inside the fence. The fence's formatting is not permission to add/remove a
   final LF. The helper's prepared bytes are the draft; do not recompose them.
   A tool response is internal evidence, not a visible assistant reply: neither
   `prepare` nor `show` output counts as displaying a draft to the user. Before
   each apply, locate the actual assistant reply containing that plan's full
   target, draft text and hashes. If none exists, emit that complete reply first.
   With active save-all, show all remaining frozen drafts in one assistant reply
   before any remaining apply. Never claim a draft was shown merely because a
   tool returned it or a candidate summary mentioned its lesson.
4. Wait for the existing `save this / save all / skip / edit` action. Preparation
   is not consent. `edit` means a new draft and new plan, displayed before fresh
   approval. `skip` never calls apply. The helper cannot authenticate a human's
   approval: the host workflow must enforce it. A matching hash is not consent.

## Apply the displayed plan only

After approval, run `python -B -X utf8 <helper> apply --plan <same-session-plan.json>
--plan-sha256 <displayed-plan-sha256>`. No replacement text is accepted by apply.
For an active save-all, retain the current/remaining draft display order from
triage and apply only each displayed, unchanged plan. Do not request a new menu
merely because this helper is used.

- `appended`: exact original prefix and approved suffix were read back under the
  local file lock. Report the saved path and result.
- `already_applied`: the file is exactly that plan's completed result; no write
  occurred. Report it, do not append again. Later unrelated appends instead cause
  a conflict, not permission to replay an old suffix.
- `refused` (exit 2): no note write was attempted. Changed/unavailable targets,
  changed plans, unsupported encoding, links, busy/unavailable locks and limits
  stop the write. A changed target requires a new plan, redisplay and fresh
  approval; never reuse stale save-all authorization or automatically rebase.
- `write_unverified` (exit 3): a write may already have occurred. Report the path,
  uncertainty and stopped batch; do not retry, roll back, regenerate, or claim
  success. Inspect the actual state before proposing any recovery with approval.

On any failure stop the remaining batch. A timeout, killed process, malformed
result or lost response is also an unknown outcome: inspect before any further
write, never silently retry. `show --plan <plan> --plan-sha256 <hash>` can recover
the frozen draft for display; it neither writes notes nor renews approval.

## Limits

Existing UTF-8 regular single-link files only; maximum original 8 MiB and append
1 MiB. The tool preserves bytes, including BOM and mixed line endings. Local OS
locks coordinate cooperating helper writers. POSIX advisory locks do not prevent
arbitrary editors or remote sync; append mode avoids overwriting concurrent
appends, and readback detects observed interference. This is not race-free
exclusion against directory swaps, remote writers, power loss or arbitrary
noncooperating edits. No scheduler, persistent watcher or cross-machine lock.
