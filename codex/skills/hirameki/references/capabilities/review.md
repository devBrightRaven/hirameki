# Corrections and lessons review capability

Used by tidy review and the permanent journal review shortcut. Review is a proposal, not permission to change rules, archive tasks or persist review records.

## Collect and classify

For `review [N]` inspect the requested scope (default recent 7 days), reading actual Corrections text from `{journal}/YYYY-MM-DD-*.md` and lessons from `{journal}/lessons/YYYY-MM-DD-*.md`. Counts in frontmatter are not candidates. Say "No corrections or lesson candidates found" only when both inspected sets are empty; disclose missing or unreadable coverage.

Keep source path, block/passage anchor, source date and raw/LF digests when available. Deduplicate by event identity before meaning: copies and cross-agent reports of one event count once; Syncthing conflict copies remain explicit exceptions. Do not edit historical notes or infer motives from summaries.

Separate task-only, project, personal, shared and unresolved scope. Review the owning runtime's applicable rules and project AGENTS.md, never the other agent's private configuration. Report covered, duplicate, superseded, needs-evidence or proposed candidates with source support. Existing rules may already express the lesson; prefer an exact scoped merge over another broad rule.

## Incremental proposals

A rejected or deferred candidate with unchanged evidence, target-rule digest and review contract is not proposed again merely because time passed. New evidence or an explicit re-open can justify review. If prior review evidence cannot be verified, say so; do not invent review history or create records automatically.

Present proposed ADD, UPDATE, NARROW, EXCEPTION, WITHDRAW or KEEP actions with current → proposed wording, owning scope, reasons, counterexamples, uncertainty and source links. Unresolved scope remains needs-evidence.

LESSON CANDIDATES are a separate visible group. Offer a reusable lesson as a rule candidate, not an automatic rule. For manual card promotion, require at least two independent events, relevant existing-card checks and no unchanged rejection/deferral; load the shared concept-card contract only when needed.

## Approval and outcome

Stop at proposals unless the user explicitly approves exact changes and their scope. A triage `save all` approves only displayed note drafts, never rule changes. General agreement or an agent consensus is not the user's approval.

Before an approved rule edit, show the exact diff and target. Apply only selected changes under the acting runtime/project's ownership. Distinguish accepted, applied and verified; static checks are not behavior validation. An ineffective or withdrawn outcome remains visible. Report partial failures without replaying successful writes.

No new review ledger, permanent authorization or scheduler is established by this contract. Their serialization and activation require their own confirmed baseline and authorization.
