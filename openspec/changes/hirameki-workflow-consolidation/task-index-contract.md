# Tidy task index contract v1

Status: implementation contract; not live archival authority.

## Storage and ownership

Resolve `{research}` from the vault's AGENTS.md. Proposed shared data root:
`{research}/tidy/tasks/`. This proposal does not create that directory in the
real vault. It is human knowledge / operational evidence, not agent runtime
configuration. Runtime paths and local receipt databases do not belong here.

Use one UTF-8 LF JSON snapshot `index.json`, immutable JSON requests under
`restore-requests/<request-id>.json`, and immutable receipts under
`receipts/<request-id>.json`. A small snapshot avoids rewriting narrative notes
or replaying all history at every next/tasks/triage call. Requests are one file
per approved operation, not one file per historical correction or task.

The designated Hygiene writer alone updates index and integration receipts.
Interactive agents may append explicitly approved restore requests only.
Syncthing is transport, not a lock or authorization service. The first release
supports one index writer; no automatic failover to another machine.

## Per-request approval records — user ruling B

Store approvals under `{research}/tidy/tasks/restore-approvals/<approval-id>.json`.
Each approval is a new immutable file: append to the collection, never overwrite
or edit an existing record. This avoids multi-machine append races on a shared
JSONL file. It does not eliminate semantic conflicts or provide a lock.

Required fields: schema_version (1), approval_id, request_id, task_id,
request_digest, operation (`restore`), approved_at (offset included), source_ref
(conversation/session and event reference), recorded_by (agent/machine).
Create only after the user's explicit approval of that exact request. A changed
request needs a new approval. Original records remain; any cancellation is a
separate event, never a rewrite. Cancellation handling must be implemented and
tested before live approval/cancellation workflows are enabled.

The read-only adapter accepts immutable `approval-cancellations/<id>.json`
records with schema_version, cancellation_id, approval_id, approval_digest
(canonical full approval SHA-256), operation (`cancel-approval`), source_ref
and recorded_by. The record must reflect explicit user authorization; matching
does not independently prove that authorization. An exact target cancellation
removes that approval's unintegrated overlay eligibility. It never reverses an
already integrated snapshot; that requires a separate authorized operation.
Invalid/missing/conflicting cancellation evidence disables restore overlays
and emits exceptions, preserving original active tasks. No timestamp precedence.
Additional approved records require their own exact user approval; old cancelled
approval files are never rewritten. The source-only restore writer consumes
this same cancellation-filtered reader result; live creation and deployment
remain unimplemented and must not be inferred from fixture tests.

The common CLI checks request canonical SHA-256 and that a matching record has
the same request ID, task ID, digest and operation. It does NOT independently
prove the human utterance occurred. Honest transcription at creation remains
the agent's responsibility; no programmatic “verified human consent” claim.
Standing scheduler authority does not substitute for per-request approval.

Requests additionally carry reason_kind: archival_error, scope_changed,
reopened, or unknown; reason and references explain the classification. Record
the original archival operation/gate version and task category when available;
missing values stay unknown. A restore is not automatically an archival error.
dream-RSI consumes these as evidence with provenance and uncertainty, not as
automatic labels or permission to change a gate. Error rates also need the
archival denominator and confirmed error outcomes, not restore count alone.

## Snapshot

Required top-level fields:

- `schema_version`: 1
- `revision`: opaque content digest of the snapshot (computed excluding itself)
- `parent_revision`: previous snapshot digest or null for genesis
- `gate_version`: exact gate identifier
- `writer`: declared owner identity
- `tasks`: mapping from stable task ID to the records below
- `applied_requests`: mapping of request ID to `payload_digest`, `task_id` and
  `task_revision` (positive integer, no later than that task's current revision)

Task fields:

- `task_id`, `scope`, `summary`, `revision` (monotonic integer per task)
- `state`: active, archived or unresolved; no task state is a decision-node status
- `sources`: relative vault path, anchor, raw and LF-normalized digests
- `criteria`, `evidence`, `open_dependencies`: structured lists
- `assessment`: confirmed, unknown or conflict; `reason`
- `assessed_gate_version`, `operation_id`, `previous_revision`

IDs are allocated once, not recomputed from mutable wording or line numbers.
Discovery retains source anchors/digests. Ambiguous fuzzy matches remain
separate candidates until evidence identifies the same task; no silent merge.
Summaries do not replace source narratives. Missing completion evidence is
unknown, not proof of active or archived completion.
The CLI derives source_digests from sources for the pure projection. Do not
persist the duplicate mapping in the snapshot.

`unresolved` is a historical import with no established current state. Its
assessment must be unknown or conflict. It stays in the same snapshot and is
returned in uncertain with its full summary, criteria and provenance; never
infer active or archived from its presence. It cannot receive a restore overlay
or an archival proposal. Reclassification requires source-backed reconciliation,
not an approval to restore an unestablished archival state. Existing active
tasks with unknown assessment remain active: do not downgrade ongoing work to
unresolved just because its evidence needs checking. This additive state is
not a new decision-node status or a second pending-task index. Older readers
reject it visibly, not as a successful empty view; consumers must use the
updated common reader before deploying a snapshot that contains it.

Snapshot loading is bounded at 16 MiB and 10,000 task records. Individual
requests, approvals, cancellations, receipts and source notes retain a 1 MiB
limit. The previous shared 1 MiB limit rejects even a 1,500-task fixture and
cannot accommodate the 3,668 allocated historical units. Exceeding either
snapshot limit is unavailable, never a successful empty view. Within one view
the adapter hashes each distinct source path once and keeps only raw/LF hashes;
every new invocation reads those sources again. This reduces repeated I/O but
does not establish a lock or a transaction across source files.

## Read-only completion proposal gate

`scripts/archive_gate.py` assesses structured completion declarations without
performing I/O or granting write authority. A criterion has `criterion_id`,
`description`, `result` (`met`, `unmet`, `unknown`) and, when met, nonempty
`evidence_refs`. Evidence has unique `evidence_id`, a nonblank `outcome`, and
`source_id` matching a verified path/anchor in the task's derived source digests.
Duplicate IDs, legacy checklist strings and absent references remain unknown;
they are not silently upgraded to verified completion.

The read-only result is completion_candidate, incomplete, unknown or conflict,
with reasons and `write_authorized: false` in every case. A completion candidate
requires all declared criteria met, traceable evidence, no open dependencies,
confirmed assessment and unchanged source/gate. This validates consistency of
assessor declarations, not semantic truth or independently proven acceptance.
Actual source reading and assessor judgment remain necessary. The future writer
must separately validate durable authorization and current revisions before an
operation. This module is not live scheduling, archival, restoration or recovery.

The reader continues to support existing descriptive structured lists; they do
not by themselves qualify as completion declarations for this proposal gate.
No live historical records are migrated by this source change.

Source gate v2 applies the same per-criterion completion consistency check before
the common reader hides an archived record. Legacy descriptions, unsupported
criterion results or missing evidence references remain uncertain; active tasks
remain visible. `TASK_GATE_VERSION` advances to v2 because this invalidates prior
completion conclusions, not because schema_version changes. A v1 archival
assessment is stale under v2. Updating source never rewrites that assessment or
resurrects the task as active. Deployment and reassessment are separate actions.

Read-only source CLI: `python3 -B -X utf8 scripts/tidy_dry_run.py --vault
<explicit-local-vault> --data <vault-relative-task-data>`. On Windows use the
verified Python executable rather than assuming `python3` exists. The command
prints JSON only. It reads sibling `TASK_GATE_VERSION` (one nonempty line);
missing/empty/multiline version or invalid snapshot stops the trial as unavailable.
It uses the common reader for source verification, uncertain records, exceptions
and restore overlays. Unidentified broken records block completion proposals;
pending restores remain incomplete until the single writer integrates them.
The report includes snapshot revision, raw gate hash and limitations. Comparing
the index before/after reading is not a cross-file lock. This source command is
not installed or wired to the live Hygiene scheduler and never writes a report
or modifies an index itself. Run it on an isolated fixture before any separately
authorized real-data trial.

## Restore request

The shared read-only CLI exposes `--task-id <exact-id>` for pre-restore inspection,
including healthy archived tasks absent from the effective active/uncertain lists.
It runs full index/source/record validation before selecting a task. The response
retains index/view revisions, full selected task, expected/current source digests,
target validation and all global exceptions plus uncertainty counts and IDs.
This is a query, not a complete inventory or proof of human consent. Unknown IDs
return `task-not-found` and nonzero, with global diagnostics retained. Paging
cannot be combined with this lookup. Default UTF-8 output ceiling is 16384 bytes;
`--max-output-bytes` permits 1024..65536. Oversize task/global diagnostics return
nonzero `output-limit-exceeded`, required size/counts and `details_returned=false`,
never a truncated success. Both native entries use this query before append-only
restore records and the effective reader immediately after each approved pair.

The executable wire schemas, required fields (including `reason_kind`), scalar
formats, matching rules and canonical-JSON digest recipe have one authority:
`scripts/task_restore_contract.py`, used by the reader itself. Obtain them through
the delivered reader's bounded `--restore-contract` interface; validate an
in-memory request/approval pair with read-only `--validate-restore` JSON stdin.
No source search, manually maintained second JSON format or writer broker is
needed. The shared delivered procedure is
`codex/skills/hirameki/references/task-restore/operation.md`.
Request IDs are ordinarily collision-resistant; created timestamps are audit
only. Query source digests are copied intact, not rehashed or normalized.

Approval must match a separate immutable record tied to the exact request,
not be accepted because the request says “approved”. The adapter supplies a
record-matching result to the shared reader, not independently proven human
consent. Missing evidence means pending verification.
An approved request can be created only after presenting the proposed scope.
No automatic approval from a task checkbox, agent consensus or mailbox text.

## Effective view: one algorithm for all readers

1. Read and validate one complete index snapshot and request payloads. Invalid
   or incomplete data produces a visible exception, never an empty “all done”.
2. Check archival sources and gate freshness. Archived records with stale or
   unconfirmed evidence remain in the separate uncertain list. Active tasks
   remain active when assessment is unknown or the archival gate changes;
   changed source is flagged source_changed rather than removing the task.
   Historical unresolved records always remain in uncertain and never become
   active merely because their source hashes match. Complete view_status means
   loading completed, not that uncertain work is resolved or every task is done.
3. A request already listed in `applied_requests` with the matching digest has
   no overlay effect, even if its receipt has not arrived.
4. For an unintegrated request, verify approval, payload and source digests.
   `base_task_revision` must equal the current task revision. A changed global
   index revision alone need not block it when that task and its sources match.
5. A valid restore changes only the effective view to active with
   `restore_pending: true`; it does not mutate the snapshot. Duplicate approved
   requests for the same task/base revision produce one visible task.
6. A later task revision or conflicting source makes an old request uncertain,
   not an override. Time of creation or arrival never establishes precedence.
   Requests for already active tasks have no restore effect and emit an
   exception. Any uncertain active task remains visible with a confirmation flag.
7. Return three explicit sections: active, uncertain, exceptions. Each result
   retains task IDs, pending request IDs and source links. Readers may filter
   by project but must disclose uncertain results in that scope.

### Authority and historical notes for both adapters

Authority is specific to a task identity and scope, not to a file's mtime or
how often its text occurs. With a readable index, the validated effective view
is the authoritative state: raw Wrap/Journal Open items add context only and
cannot override indexed closure. A restore requires the matching request and
approval checks above; a note saying "reopened" cannot bypass them.

Without an index, use traceable explicit status evidence for the same task:
an owner-approved status record or an explicit completed, withdrawn,
superseded or reopened event in a Wrap/Journal block. Establish order from
the task revision/supersession relation, or an unambiguous dated event and its
context. A filename, mtime, arrival time or copied text alone establishes
neither authority nor precedence. Preserve references to the competing events.
An unchecked Open item is discovery evidence, not a newer reopening event,
even in the newest Journal. An explicit current open statement without newer
closure may support a raw candidate, but is not validated indexed active state.

"Old" means superseded for that same identity by an evidenced later state
event, not merely a file older than a threshold. Completed, withdrawn or
superseded work remains closed unless there is a demonstrably later explicit
reopening; a replacement is a separate task. If identity, scope, event ordering,
source authority or evidence is missing/conflicting, report status uncertain
instead of resolving the conflict with mtime or repetition. A handoff's
frontmatter status describes that handoff; it is task evidence only when its
scope and explicit task statement establish the corresponding task status.

### Bounded reader presentation

The shared CLI supports optional `--page-size` (1..100) and nonnegative
`--offset`. Validation and effective-view computation still cover the full
index, sources, requests and exceptions. The default machine-readable output
remains complete; the dry-run/writer never uses a presentation page as input.
Each selected task retains its complete record, so this limits record count,
not the byte length of an unusually large record.

Each page includes per-section total, returned, earlier_not_displayed,
remaining and next_offset for active, uncertain and exceptions, plus
`pagination.all_displayed`. A successful `view_status: complete` means full
loading/validation completed, not that the presentation page contains everything
or all uncertainty is resolved. An empty later page is not an empty task list.
Unshown uncertainty and exceptions must remain visible through counts and next
offsets, never disappear from the user-facing scope claim.

Responses include `index_revision` and `view_revision`, the latter a canonical
digest of the full effective view before paging. Follow-up invocations pin both
with `--expected-revision` and `--expected-view-revision`: source, request,
approval, cancellation or exception changes can alter the effective view without
changing the index. Mismatch is unavailable, not an interpreter failure or
permission to combine incompatible pages. These tokens detect observed changes;
they do not provide a cross-file lock or atomic snapshot.

Codex next/tasks/triage start with twenty records per section. A bounded
orientation may report a preview plus totals and deferred offsets. A requested
comprehensive inventory needs all relevant pages at matching revisions before
claiming complete coverage; unseen tasks cannot be ranked or declared finished.
Claude's next/tasks/triage command source also adopts this presentation option;
both use the same full effective-view algorithm. This is source integration, not evidence
of either runtime's fresh-dialog paging behavior or deployed parity.

A receipt arriving before an index that lists its request is an inconsistent
snapshot: do not apply the request, hide the task or infer completion. Report
uncertainty until the corresponding index arrives. No wall-clock tie breaker.

## Integration and recovery

Writer validates current authorization, source hashes, task/base revisions and
index revision immediately before applying. It writes a new complete snapshot
via atomic replace, incrementing the task revision and recording request digest
in `applied_requests`, then appends its immutable receipt. A crash after the
snapshot but before receipt is recovered from applied_requests without replay.
Do not claim atomicity across files or machines.

The source-only `scripts/tidy_writer.py` prototype exposes `restore_once`;
it has no CLI, schedule or live deployment entry. Its caller supplies explicit
authority and the single writer's identity; neither is inferred from a mailbox
or created by this module. One task is integrated per call, with duplicate
approved requests sharing one task-revision increment. The common reader
supplies cancellation-filtered `restore_approval_refs` (approval ID, source
reference and canonical approval digest) for the pending request IDs. The writer
does not implement a second approval/cancellation decision algorithm.

Before replacing the index, append a bounded immutable integration intent under
`integration-intents/<hashed-intent-id>.json`. Its basis is pinned by a digest
in each applied-request entry; it retains receipt audit fields and exact before/
after snapshot revisions. The writer rechecks index, gate, authority, request
records and source freshness before commit. A local process-lifetime OS lock
prevents local concurrent writes and releases on process termination, but is
not a Syncthing or cross-machine lock. The index is flushed to a sibling temporary
file then atomically replaced. Original notes and requests are never modified.

Recover missing receipts before further index mutation. Recover only when the
intent basis matches the applied request and the current snapshot is the intent's
committed snapshot. A changed snapshot, corrupted intent, receipt conflict or
out-of-scope/revoked authority stops recovery; no invented receipt or replay.
Existing immutable receipts are checked, never overwritten. An orphan prepared
intent after a failed index replacement is not evidence that integration happened.
No automatic cleanup is authorized. An integrated restore sets assessment to
unknown so old completion evidence cannot immediately auto-archive it again.

These tests cover an actual isolated process exiting after index replacement,
as well as injected write/race failures. They do not prove power-loss durability,
real multi-machine synchronization, authority-file ownership or the authenticity
of the human approval. Production authority storage/ownership remains undecided.

Receipt fields: `request_id`, `payload_digest`, `task_id`,
`before_task_revision`, `after_task_revision`, `before_index_revision`,
`after_index_revision`, `operation` (`restore`), `owner`, `gate`,
`authorization_ref`, `evidence_refs` (nonempty string list) and
`recovery_outcome`. Task revision advances exactly one per operation; before
and after snapshot digests differ. Matching applied-request identity/digest/task
revision is checked; an older valid receipt is not forced to equal the latest
global snapshot after unrelated updates. Source changes stop only that item.
No original note rollback. Invalid/torn index keeps the last verified view
explicitly stale, not silently current. No verified baseline means unknown.

Later authorized archival advances task revision, so old requests cannot reopen
it. Failed write has no success receipt. Conflicting copies of an immutable
request are exceptions, not “latest wins”. Conflicting approval IDs or receipt
request IDs are also isolated with all affected paths. Identical duplicates
have one effect; conflicting records cannot grant a restore overlay. Original
active tasks remain visible, with affected tasks separately marked uncertain.

### Source-only archive integration

The same module also exposes `archive_once`. It requires the separate `archive`
operation in the caller-supplied authority; restore permission does not grant it.
It consumes the shared dry-run gate rather than implementing another completion
classifier, verifies exact approved sources and advances at most one active
completion candidate per call. Unresolved imports are not candidates and do not
block unrelated verified candidates. Unidentified malformed inputs block writing.
This remains assessor-declaration consistency, not independent semantic proof.

Archival changes only the index task state/revision, not source note content.
Append an immutable `archive-intents/<hashed-operation-id>.json` before atomic
snapshot replacement and an `archive-receipts/<hashed-operation-id>.json` after.
The task pins `archive_intent_id` and `archive_intent_digest`; the intent retains
authority/gate hashes and a receipt basis containing before/after task revisions,
before snapshot revision, operation ID, completion declaration digest and source
evidence references. Its after snapshot revision is separate to avoid a circular
digest. Receipts retain each actual archive operation for the dream-RSI denominator;
restore frequency alone still does not establish an archival error.

Recover a missing archive receipt only against its exact committed snapshot,
without replay or increment. Check existing receipts, never overwrite conflicting
records or Syncthing copies. A prepared intent after failed replace is not success.
Before another restore, an outstanding archive receipt must be recovered using
archive authority; restore-only authority cannot write that receipt. Conversely,
archive stops if a committed restore needs receipt recovery. New approvals,
cancellations, source/index changes, revocation and gate changes are rechecked
before replacement. Restored tasks still require a new completion assessment;
old applied requests cannot override later archival revisions.

There is no archive CLI, live scheduler, production authority designation or
new package inclusion. Fixture interruption/atomic-replace tests do not prove
power-loss durability, actual transport or independent human consent.

## Authorization and deployment

Standing authority data location remains a human-owned decision. Required
fields: ID/revision, approved sources and operations, designated writer,
schema/gate versions, approval provenance/date, validity and revocation.
The scheduler reads it every run; absent/revoked/out-of-scope is read-only.
No current Hygiene permission to write metadata reports implies task-index
permission. First deployment requires a read-only dry-run and separate approval.

The restore prototype tests a proposed authority payload with schema_version,
authority_id, integer revision, designated_writer, exact data directory,
operations, exact approved_sources paths, gate_version, index_schema_version,
source_ref, approved_at, not_before, expires_at and revoked. It re-reads it each
call and before commit/recovery; validity timestamps require offsets. This
fixture format is not a human designation of a production path or writer and
does not grant archive authority. No restore record is self-approved by the writer.

Suggested scheduler instruction: load canonical tidy task contract and current
authority; read the approved sources; process within the existing bounded
limit; preserve unknown/conflicts; report counts, exceptions and source/version
evidence. No embedded alternative gate or mtime-only completion rule.

## Required tests

Completed, partially completed, required deployment pending, mixed notes,
changed source, changed gate, approved restore before scheduling, duplicate
request, later archival, unrelated global revision, missing/revoked approval,
conflicting request payload, index-first/receipt-first synchronization,
partial write recovery, and the same effective view in next/tasks/triage.
Also cover a historical unresolved record alongside a valid active record:
only the latter is an archival proposal, both retain provenance, and even a
matching restore approval cannot turn the unresolved record into active work.
Unknown historical imports must not block unrelated confirmed candidates.

These are fixture contracts, not proof of real transport, live scheduling or
fresh-dialog skill routing. Historical semantic review remains its own gate;
no regex extraction may assert a task completed or a lesson ready for promotion.

Malformed request/approval/receipt files are isolated individually with relative
path and reason. Identifiable affected tasks are uncertain; original active
tasks remain visible. Syncthing conflict copies are exceptions, never official
records. Exhausting the record budget keeps active baseline visible but disables
restore overlays because omitted records may contain conflicts. Outputs declare
partial/unavailable status; consumers must not interpret either as “all done”.
An invalid index is a whole-view failure, not a successful empty task list.

User publishing ruling: keep both programs and tests in source, exclude both
programs from package files until next/tasks/triage integration and both-runtime
acceptance complete. This is a release gate, not permission to publish later
without authorization. New tests run inside npm test and the release test chain.

## Current prototype boundary

`scripts/task_view.py` is a pure projection prototype, not a disk parser,
writer, digest verifier or authorization service. `scripts/task_view_cli.py`
is the shared read-only adapter for both runtimes, loading bounded local files,
checking snapshot/request digests and matching approval records, and deriving
source digests. It never writes. It checks declared snapshot writer/gate/parent
revision, task contract field types and raw/LF source digests. Malformed task
records remain uncertain while unaffected active tasks survive. Writer identity
is metadata, not independently verified authority. Applied requests retain the
exact task identity/revision; receipts validate their complete required fields
and applied-index match. Restore requests validate positive base revision,
snapshot/source digest types, offset timestamp and scoped audit approval fields.
The embedded audit approval never grants eligibility without a separate matching
immutable approval. Writer cancellation/recovery has source-only restore tests;
automatic archival integration, live scheduling and real-machine recovery remain
live-deployment gates. approved_digests comes from
record matching, never the request's self-declared approval.
Fixture digest strings are substitutes, not cryptographic validation evidence.
The prototype currently covers the core view rules; historical audit, real
reader integration, bounded file loading and single-writer integration remain
required before deployment. It is not included in the published package yet.
