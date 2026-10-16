# Restore operation: delivered read-only interfaces and native file saves

This is the shared Claude/Codex procedure, not a second schema authority.
The reader's `--restore-contract` response is generated from the same definitions
used to validate request and approval records. Never search implementation source
to discover fields. Do not derive approval from a task checkbox or an agent claim.

## Resolve and inspect

Resolve the vault and language through the loaded entry. Resolve the bundled
reader root using that entry, then read its `scripts/TASK_GATE_VERSION` as UTF-8.
Use the verified Python interpreter with `-B -X utf8` and separate native arguments.
All executable/document paths are relative to the delivered package, not a source
checkout or private configuration. This guide is at `references/task-restore/operation.md`
for a Codex skill root, or `codex/skills/hirameki/references/task-restore/operation.md`
for the package root.

1. Call `scripts/task_view_cli.py --restore-contract`, without vault options.
   It returns both schemas, digest recipe, field sources, binding rules, record
   locations and save order. This response and task-ID queries use a 16384-byte
   UTF-8 ceiling; oversize returns nonzero `output-limit-exceeded`, never truncation.
2. Call the same reader with `--vault <vault> --data <research>/tidy/tasks
   --gate-version <G> --task-id <id>`. This validates the full index and records.
   Require a found, archived task, verified target, matching sources and
   `global_validation.restore_matching_available=true`. Retain all global
   uncertainty and exceptions. `partial` alone is not a failed CLI call, and
   selected verification alone is not global success. Do not act on invalid,
   unavailable or unknown targets, missing evidence, or ambiguous global blockers.
3. Obtain the user's approved task/scope and a reference to that approval in the
   current conversation. Use actual user identity, intent/reason and timestamp;
   do not fabricate human approval. A synthetic trial must label these synthetic.
   The program verifies record matching, not the authenticity of human consent.

## Build in memory and save

Required values and sources:

| Value | Source |
|---|---|
| Exact record fields/types and allowed reason kinds | `--restore-contract` schemas |
| Task ID, task revision, index revision | task-ID response |
| `base_source_digests` | `validation.expected_source_digests`; require current match |
| Request/approval IDs and allowed target paths | user's write scope; collision-resistant IDs ordinarily |
| Reason, reason kind, approving user, approval reference | actual approved intent; do not infer from index |
| Created/approved time | offset-bearing current/approval timestamp; audit, not precedence |
| `recorded_by` | actual recording runtime, or explicitly synthetic harness identity |
| Request payload digest | canonical complete request excluding only `payload_digest` |
| Approval `request_digest` | that exact request payload digest |

Build the entire request in memory, compute its digest, then build the separate
approval record bound to the same request ID/task/digest. Canonical digest means
SHA-256 of UTF-8 Python JSON with sorted keys, `ensure_ascii=False`, separators
`(',', ':')`, `allow_nan=False`, excluding only `payload_digest`. It is not the
SHA-256 of the pretty-printed file bytes. Do not normalize or rehash source digests.
Additional JSON fields are included in the digest, not silently discarded.

Precheck both authorized paths are absent. Exclusive-create the approval file
first, then the request file; never overwrite, mkdir an unapproved directory or
update index. If either write fails, stop and report exactly which file exists;
leave partial records as audit evidence, do not delete or retry a write.
Before saving, call `--validate-restore` with JSON stdin containing `request` and
`approval_record`. It uses the same reader validators and matching rules, writes
nothing, and returns nonzero on schema/digest/binding error. This validates the
in-memory pair only; it does not replace task/source checks or user approval.

## Immediate readback and repeated restore

Immediately query the same task ID again. Require `restore_pending=true`, this
request ID in `pending_requests`, and its approval in `restore_approval_refs`.
Preserve global diagnostics and report the task as immediately actionable,
pending index integration. This does not authorize executing the underlying task.
For a second independently approved request, repeat the query/build/save/readback
steps with new IDs. Keep the first pair's file SHA-256 unchanged, verify both
pending IDs and their separate approval references. Do not wait for scheduled
integration or replace the first pair.

## Standard-library recipe (inputs supplied by the caller)

The caller supplies `reader`, `vault`, `data`, `gate`, `task_id`, approved user and
reference, reason/reason_kind, timestamp, recorded_by, and exact authorized paths
and IDs. This recipe uses only the documented public reader and native file I/O.
It imports no implementation or test helpers. Call once per separately approved
pair; capture and report errors/partial state without rerunning a failed save.
The recipe is for ordinary-program delivery rehearsal. In a model runtime whose
entry prohibits nested interpreter orchestration, issue each public CLI command
directly as a native tool call, then use the same canonical-JSON expression and
exclusive native file saves. Do not use `runpy`, change interpreter after denial,
or wrap a denied launch to evade permissions. The schema and save order are the same.

```python
import hashlib, json, subprocess, sys
from pathlib import Path

def restore_once(reader, vault, data, gate, task_id, request_id, approval_id,
                 request_path, approval_path, user, authorization_ref,
                 reason, reason_kind, timestamp, recorded_by):
    def cli(*arguments):
        run = subprocess.run([sys.executable, '-B', '-X', 'utf8', str(reader),
                              *arguments], capture_output=True, text=True,
                             encoding='utf-8', timeout=30)
        if run.returncode != 0:
            raise RuntimeError({'exit_code': run.returncode,
                                'stdout': run.stdout, 'stderr': run.stderr})
        if len(run.stdout.encode('utf-8')) > 16384:
            raise RuntimeError('reader response exceeds delivery ceiling')
        return json.loads(run.stdout)
    contract = cli('--restore-contract')
    arguments = ['--vault', str(vault), '--data', data, '--gate-version', gate,
                 '--task-id', task_id]
    before = cli(*arguments)
    if (before['query_status'] != 'found' or before['task']['state'] != 'archived'
            or before['validation']['status'] != 'verified'
            or not before['validation']['sources_match']
            or not before['global_validation']['restore_matching_available']):
        raise RuntimeError({'restore_preconditions_failed': before})
    request = dict(schema_version=1, request_id=request_id, task_id=task_id,
                   base_index_revision=before['index_revision'],
                   base_task_revision=before['task']['revision'],
                   base_source_digests=before['validation']['expected_source_digests'],
                   reason=reason, reason_kind=reason_kind, created=timestamp,
                   approval=dict(source_ref=authorization_ref, approving_user=user,
                                 operation='restore', scope=task_id))
    request['payload_digest'] = hashlib.sha256(json.dumps(
        request, sort_keys=True, ensure_ascii=False, separators=(',', ':'),
        allow_nan=False).encode('utf-8')).hexdigest()
    approval = dict(schema_version=1, approval_id=approval_id, request_id=request_id,
                    task_id=task_id, request_digest=request['payload_digest'],
                    operation='restore', approved_at=timestamp,
                    source_ref=authorization_ref, recorded_by=recorded_by)
    for name, record in [('request', request), ('approval_record', approval)]:
        if not set(contract['schemas'][name]['required']).issubset(record):
            raise RuntimeError('documented recipe differs from delivered schema')
    checked = subprocess.run([sys.executable, '-B', '-X', 'utf8', str(reader),
                              '--validate-restore'], input=json.dumps(
        {'request': request, 'approval_record': approval}, ensure_ascii=False,
        allow_nan=False), capture_output=True, text=True, encoding='utf-8', timeout=30)
    if checked.returncode != 0:
        raise RuntimeError({'record_validation_failed': checked.stdout,
                            'stderr': checked.stderr})
    request_path, approval_path = Path(request_path), Path(approval_path)
    if request_path.exists() or approval_path.exists():
        raise FileExistsError('preserve existing records')
    for path, record in [(approval_path, approval), (request_path, request)]:
        with path.open('x', encoding='utf-8', newline='\n') as stream:
            json.dump(record, stream, ensure_ascii=False, allow_nan=False)
            stream.write('\n')
    after = cli(*arguments)
    task = after['task']
    if (not task.get('restore_pending') or request_id not in task['pending_requests']
            or approval_id not in [a['approval_id']
                                  for a in task['restore_approval_refs'][request_id]]):
        raise RuntimeError({'restore_not_verified': after})
    return {'before': before, 'after': after,
            'request_file_sha256': hashlib.sha256(request_path.read_bytes()).hexdigest(),
            'approval_file_sha256': hashlib.sha256(approval_path.read_bytes()).hexdigest()}
```

## Stop boundary

The current authorized trial stops on any failed/incomplete inspection. This
guide does not authorize a retry after truncation or a fresh model invocation.
A proposed distinction between smaller read-only inspection and rerunning a
model trial must be separately approved; never weaken existing approval or
filesystem/network/write limits to recover. Explicit data/schema/permission
errors and output-limit-exceeded remain visible failures.
