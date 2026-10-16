"""Source-only single-writer restore/archive integration. No CLI or scheduler entry.

Explicit authority is supplied by the caller, never created here. File matching
does not independently prove user consent. Local OS locking and atomic replace
do not prove cross-machine exclusion or crash/power-loss durability.
"""
from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import os
from pathlib import Path
import tempfile
import uuid

from task_contract_primitives import text
from task_view_cli import (INDEX_BYTE_LIMIT, RECORD_BYTE_LIMIT, contained, digest,
                           load_view, offset_timestamp, read_json, records)
from tidy_dry_run import read_gate


def encoded(record):
    import json
    return (json.dumps(record, sort_keys=True, ensure_ascii=False,
                       separators=(',', ':'), allow_nan=False) + '\n').encode('utf-8')


def bytes_hash(path, limit=RECORD_BYTE_LIMIT):
    with path.open('rb') as stream:
        raw = stream.read(limit + 1)
    if len(raw) > limit:
        raise ValueError('file-budget')
    return hashlib.sha256(raw).hexdigest()


def authority(root, path, writer, data, gate, now, operation='restore'):
    record = read_json(path)
    if (record.get('schema_version') != 1 or record.get('revoked') is not False
            or type(record.get('revision')) is not int or record['revision'] < 1
            or not all(text(record.get(k)) for k in ('authority_id', 'source_ref'))
            or record.get('designated_writer') != writer or record.get('data') != data
            or record.get('gate_version') != gate or record.get('index_schema_version') != 1
            or not isinstance(record.get('operations'), list) or operation not in record['operations']
            or not isinstance(record.get('approved_sources'), list) or not record['approved_sources']
            or not all(text(p) for p in record['approved_sources'])
            or not all(offset_timestamp(record.get(k)) for k in
                       ('approved_at', 'not_before', 'expires_at'))):
        raise ValueError('authority-unavailable-or-out-of-scope')
    parse = lambda key: datetime.fromisoformat(record[key].replace('Z', '+00:00'))
    if not parse('approved_at') <= now or not parse('not_before') <= now < parse('expires_at'):
        raise ValueError('authority-outside-validity')
    for relative in record['approved_sources']:
        contained(root, relative)
    return record


@contextmanager
def local_lock(path):
    """Process-lifetime lock released by OS on exit; not a Syncthing lock."""
    with path.open('a+b') as stream:
        if stream.tell() == 0:
            stream.write(b'0')
            stream.flush()
        stream.seek(0)
        if os.name == 'nt':
            import msvcrt
            msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            yield
        finally:
            stream.seek(0)
            if os.name == 'nt':
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def record_path(root, data, folder, identity):
    name = hashlib.sha256(identity.encode('utf-8')).hexdigest() + '.json'
    return contained(root, str(Path(data) / folder / name))


def immutable(path, value):
    raw = encoded(value)
    if len(raw) > RECORD_BYTE_LIMIT:
        raise ValueError('record-budget')
    if path.parent.exists() and any(path.parent.glob(path.stem + '.sync-conflict-*.json')):
        raise ValueError('immutable-conflict-copy')
    if path.exists():
        if read_json(path) != value:
            raise ValueError('immutable-record-conflict')
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())


def snapshot_replace(path, value):
    raw = encoded(value)
    if len(raw) > INDEX_BYTE_LIMIT:
        raise ValueError('snapshot-budget')
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix='.tidy-index-',
                                         suffix='.tmp', delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def record_stamp(root, data):
    result = {}
    for folder in ('restore-requests', 'restore-approvals', 'approval-cancellations', 'receipts'):
        directory = contained(root, str(Path(data) / folder))
        paths = sorted(directory.glob('*.json')) if directory.exists() else []
        if len(paths) > 2000:
            raise ValueError('record-budget')
        for path in paths:
            relative = path.relative_to(root).as_posix()
            result[relative] = bytes_hash(contained(root, relative))
    return result


def eligible(view, allowed_sources):
    return {task['task_id']: task for task in view['active']
            if task.get('restore_pending')
            and all(s['path'] in allowed_sources for s in task['sources'])}


def archive_receipts(root, data, index):
    """Validate pinned archive audit records, returning missing receipts only.

    Completed receipts may outlive later snapshots; missing receipts require the
    exact committed snapshot for recovery. Never infer a receipt from state alone.
    """
    missing = []
    for task_id, task in index['tasks'].items():
        intent_id = task.get('archive_intent_id')
        if not intent_id:
            continue
        path = record_path(root, data, 'archive-intents', intent_id)
        if any(path.parent.glob(path.stem + '.sync-conflict-*.json')):
            raise ValueError('archive-intent-conflict-copy')
        intent = read_json(path)
        basis = intent['basis']
        receipt = dict(basis['receipt'], after_index_revision=intent['after_index_revision'])
        if (digest(basis) != task.get('archive_intent_digest')
                or basis.get('intent_id') != intent_id
                or receipt.get('operation') != 'archive'
                or receipt.get('task_id') != task_id
                or receipt.get('operation_id') != intent_id):
            raise ValueError('archive-intent-index-conflict')
        receipt_path = record_path(root, data, 'archive-receipts', intent_id)
        if any(receipt_path.parent.glob(receipt_path.stem + '.sync-conflict-*.json')):
            raise ValueError('archive-receipt-conflict-copy')
        if receipt_path.exists():
            if read_json(receipt_path) != receipt:
                raise ValueError('archive-receipt-conflict')
        else:
            if (intent['after_index_revision'] != index['revision']
                    or task['revision'] != receipt['after_task_revision']
                    or task['state'] != 'archived'):
                raise ValueError('archive-recovery-snapshot-changed')
            missing.append((task, receipt_path, receipt))
    return missing


def archive_once(root, data, authority_path, writer, gate_path, *, now=None, fault=None):
    """Source-only authorized archive of at most one task; no live CLI/schedule.

    Completion declarations still need human/assessor semantic review. Authority
    to restore does not authorize archive. No narrative notes are edited.
    """
    from tidy_dry_run import dry_run
    root = root.resolve()
    clock = lambda: now if now is not None else datetime.now(timezone.utc)
    fault = fault or (lambda stage: None)
    try:
        gate, gate_hash = read_gate(gate_path)
        permission = authority(root, authority_path, writer, data, gate, clock(), 'archive')
        authority_hash = bytes_hash(authority_path)
        index_path = contained(root, str(Path(data) / 'index.json'))
        index = read_json(index_path, byte_limit=INDEX_BYTE_LIMIT)
        if (index.get('writer') != writer or index.get('gate_version') != gate
                or not isinstance(index.get('tasks'), dict)
                or not isinstance(index.get('applied_requests'), dict)):
            raise ValueError('writer-or-gate-mismatch')
    except (OSError, ValueError, KeyError, TypeError):
        return {'status': 'read-only', 'reason': 'archive-authority-or-index-unavailable'}
    committed = False
    try:
        with local_lock(contained(root, str(Path(data) / '.writer.lock'))):
            index = read_json(index_path, byte_limit=INDEX_BYTE_LIMIT)
            if (index.get('revision') != digest(index, 'revision')
                    or index.get('writer') != writer or index.get('gate_version') != gate):
                raise ValueError('index-unverified')
            before_hash = bytes_hash(index_path, INDEX_BYTE_LIMIT)
            def recheck():
                if (authority(root, authority_path, writer, data, gate, clock(), 'archive') != permission
                        or bytes_hash(authority_path) != authority_hash
                        or read_gate(gate_path) != (gate, gate_hash)
                        or bytes_hash(index_path, INDEX_BYTE_LIMIT) != before_hash):
                    raise ValueError('archive-input-changed')
            recheck()
            missing = archive_receipts(root, data, index)
            if missing:
                for task, path, receipt in missing:
                    if not all(s['path'] in permission['approved_sources'] for s in task['sources']):
                        raise ValueError('archive-recovery-source-scope')
                    fault('before-recovery')
                    recheck()
                    immutable(path, receipt)
                return {'status': 'recovered', 'index_replayed': False,
                        'operation_ids': [r['operation_id'] for _, _, r in missing]}
            # Do not supersede a committed restore awaiting its immutable receipt.
            for request_id, entry in index['applied_requests'].items():
                if entry.get('intent_id') and not record_path(root, data, 'receipts', request_id).exists():
                    raise ValueError('restore-recovery-required-first')
            stamp = record_stamp(root, data)
            report = dry_run(root, data, gate_path)
            if any(not error.get('task_id') for error in report['exceptions']):
                return {'status': 'unavailable', 'exceptions': report['exceptions']}
            allowed = sorted(row['task_id'] for row in report['proposals']
                             if row['classification'] == 'completion_candidate'
                             and all(s['path'] in permission['approved_sources']
                                     for s in index['tasks'][row['task_id']]['sources']))
            if not allowed:
                return {'status': 'no-op', 'exceptions': report['exceptions']}
            task_id = allowed[0]
            original = index['tasks'][task_id]
            intent_id = uuid.uuid4().hex
            receipt = {'schema_version': 1, 'operation_id': intent_id,
                       'operation': 'archive', 'task_id': task_id,
                       'before_task_revision': original['revision'],
                       'after_task_revision': original['revision'] + 1,
                       'before_index_revision': index['revision'],
                       'owner': writer, 'gate': gate,
                       'authorization_ref': permission['source_ref'],
                       'assessment_digest': digest(original),
                       'evidence_refs': [e['source_id'] for e in original['evidence']],
                       'recovery_outcome': 'committed-once'}
            basis = {'schema_version': 1, 'intent_id': intent_id,
                     'authority_sha256': authority_hash, 'gate_source_sha256': gate_hash,
                     'receipt': receipt}
            updated = deepcopy(index)
            updated['tasks'][task_id].update(
                state='archived', revision=original['revision'] + 1,
                previous_revision=original['revision'], operation_id=intent_id,
                archive_intent_id=intent_id, archive_intent_digest=digest(basis))
            updated['parent_revision'] = index['revision']
            updated['revision'] = digest(updated, 'revision')
            def verify_candidate():
                recheck()
                if record_stamp(root, data) != stamp:
                    raise ValueError('restore-records-changed')
                latest = dry_run(root, data, gate_path)
                if (latest['index_revision'] != index['revision']
                        or latest['gate_source_sha256'] != gate_hash
                        or any(not e.get('task_id') for e in latest['exceptions'])
                        or not any(p['task_id'] == task_id and p['classification'] == 'completion_candidate'
                                   for p in latest['proposals'])):
                    raise ValueError('archive-candidate-changed')
            fault('before-commit')
            verify_candidate()
            immutable(record_path(root, data, 'archive-intents', intent_id),
                      {'schema_version': 1, 'basis': basis,
                       'after_index_revision': updated['revision']})
            fault('after-intent')
            verify_candidate()
            snapshot_replace(index_path, updated)
            committed = True
            fault('after-index')
            immutable(record_path(root, data, 'archive-receipts', intent_id),
                      dict(receipt, after_index_revision=updated['revision']))
            return {'status': 'archived', 'task_id': task_id,
                    'operation_id': intent_id, 'revision': updated['revision'],
                    'semantic_verification': 'assessor-declaration-only'}
    except (OSError, ValueError, KeyError, TypeError):
        return {'status': 'conflict', 'reason': 'archive-or-recovery-input-unverified',
                'index_may_be_committed': committed, 'retry': 'Inspect intent and index; never replay.'}


def restore_once(root, data, authority_path, writer, gate_path, *, now=None, fault=None):
    """Integrate at most one task per call; duplicate approved requests share it.

    This is a source prototype: callers must establish real identity, authority
    ownership and deployment. No automatic archival or live entry is provided.
    fault is a fixture-only crash/race injection callback, not a retry facility.
    """
    root = root.resolve()
    current_time = lambda: now if now is not None else datetime.now(timezone.utc)
    fault = fault or (lambda stage: None)
    try:
        gate, gate_hash = read_gate(gate_path)
        permission = authority(root, authority_path, writer, data, gate, current_time())
        authority_hash = bytes_hash(authority_path)
        directory = contained(root, data)
        index_path = contained(root, str(Path(data) / 'index.json'))
        index = read_json(index_path, byte_limit=INDEX_BYTE_LIMIT)
        if index.get('writer') != writer or index.get('gate_version') != gate:
            raise ValueError('writer-or-gate-mismatch')
    except (OSError, ValueError, TypeError, KeyError):
        return {'status': 'read-only', 'reason': 'authority-or-index-unavailable',
                'consent_verification': 'recorded-only'}
    try:
        with local_lock(contained(root, str(Path(data) / '.writer.lock'))):
            index = read_json(index_path, byte_limit=INDEX_BYTE_LIMIT)
            if (index.get('writer') != writer or index.get('gate_version') != gate
                    or authority(root, authority_path, writer, data, gate, current_time()) != permission):
                raise ValueError('authority-or-owner-changed')
            if index.get('revision') != digest(index, 'revision'):
                raise ValueError('index-digest-mismatch')
            if archive_receipts(root, data, index):
                raise ValueError('archive-recovery-required-first')
            before_hash = bytes_hash(index_path, INDEX_BYTE_LIMIT)
            # Recover outstanding receipts before any later index mutation.
            recovered = []
            for request_id, entry in index['applied_requests'].items():
                if not entry.get('intent_id'):
                    continue  # Legacy applied entries are not invented recovery evidence.
                intent_path = record_path(root, data, 'integration-intents', entry['intent_id'])
                if any(intent_path.parent.glob(intent_path.stem + '.sync-conflict-*.json')):
                    raise ValueError('intent-conflict-copy')
                intent = read_json(intent_path)
                basis = intent['basis']
                if (digest(basis) != entry.get('intent_basis_digest')
                        or basis.get('intent_id') != entry['intent_id']):
                    raise ValueError('intent-index-conflict')
                receipt = next((r for r in basis['receipts'] if r['request_id'] == request_id), None)
                if (receipt is None or receipt['payload_digest'] != entry['payload_digest']
                        or receipt['task_id'] != entry['task_id']
                        or receipt['after_task_revision'] != entry['task_revision']):
                    raise ValueError('intent-request-conflict')
                receipt = dict(receipt, after_index_revision=intent['after_index_revision'])
                path = record_path(root, data, 'receipts', request_id)
                if path.exists():
                    if read_json(path) != receipt:
                        raise ValueError('receipt-conflict')
                    continue
                if intent['after_index_revision'] != index['revision']:
                    raise ValueError('recovery-index-changed')
                task = index['tasks'][entry['task_id']]
                if not all(s['path'] in permission['approved_sources'] for s in task['sources']):
                    raise ValueError('recovery-source-out-of-scope')
                fault('before-recovery')
                if authority(root, authority_path, writer, data, gate, current_time()) != permission:
                    raise ValueError('recovery-authority-changed')
                if (bytes_hash(authority_path) != authority_hash
                        or read_gate(gate_path) != (gate, gate_hash)
                        or bytes_hash(index_path, INDEX_BYTE_LIMIT) != before_hash):
                    raise ValueError('recovery-input-changed')
                immutable(path, receipt)
                recovered.append(request_id)
            if recovered:
                return {'status': 'recovered', 'request_ids': recovered, 'index_replayed': False}
            stamp = record_stamp(root, data)
            view = load_view(root, data, gate)
            if any(not e.get('task_id') for e in view['exceptions']):
                return {'status': 'unavailable', 'exceptions': view['exceptions']}
            candidates = eligible(view, permission['approved_sources'])
            if not candidates:
                return {'status': 'no-op', 'exceptions': view['exceptions']}
            task_id = sorted(candidates)[0]
            task = candidates[task_id]
            request_ids = task['pending_requests']
            errors = []
            requests = dict((r['request_id'], r) for _, r in
                            records(root, str(Path(data) / 'restore-requests'), errors)
                            if text(r.get('request_id')))
            intent_id = uuid.uuid4().hex
            receipt_bases = []
            for request_id in request_ids:
                request = requests[request_id]
                approval = task['restore_approval_refs'][request_id][0]
                receipt_bases.append({
                    'schema_version': 1, 'request_id': request_id,
                    'payload_digest': request['payload_digest'], 'task_id': task_id,
                    'before_task_revision': task['revision'],
                    'after_task_revision': task['revision'] + 1,
                    'before_index_revision': index['revision'], 'operation': 'restore',
                    'owner': writer, 'gate': gate,
                    'authorization_ref': permission['source_ref'],
                    'evidence_refs': [approval['source_ref'],
                                      'approval-sha256:' + approval['approval_sha256']],
                    'recovery_outcome': 'committed-once'})
            basis = {'schema_version': 1, 'intent_id': intent_id,
                     'authority_sha256': authority_hash, 'gate_source_sha256': gate_hash,
                     'receipts': receipt_bases}
            updated = deepcopy(index)
            updated_task = updated['tasks'][task_id]
            updated_task.update(state='active', previous_revision=task['revision'],
                                revision=task['revision'] + 1, operation_id=intent_id,
                                assessment='unknown', reason='Approved restore; new completion assessment required.')
            for request_id in request_ids:
                updated['applied_requests'][request_id] = {
                    'payload_digest': requests[request_id]['payload_digest'], 'task_id': task_id,
                    'task_revision': updated_task['revision'], 'intent_id': intent_id,
                    'intent_basis_digest': digest(basis)}
            updated['parent_revision'] = index['revision']
            updated['revision'] = digest(updated, 'revision')
            intent = {'schema_version': 1, 'basis': basis,
                      'after_index_revision': updated['revision']}
            fault('before-commit')
            if authority(root, authority_path, writer, data, gate, current_time()) != permission:
                raise ValueError('integration-authority-changed')
            if (bytes_hash(authority_path) != authority_hash
                    or read_gate(gate_path) != (gate, gate_hash)
                    or bytes_hash(index_path, INDEX_BYTE_LIMIT) != before_hash
                    or record_stamp(root, data) != stamp):
                raise ValueError('integration-input-changed')
            latest = eligible(load_view(root, data, gate), permission['approved_sources'])
            if (task_id not in latest or latest[task_id].get('pending_requests') != request_ids
                    or latest[task_id].get('source_digests') != task['source_digests']):
                raise ValueError('source-or-request-changed')
            immutable(record_path(root, data, 'integration-intents', intent_id), intent)
            snapshot_replace(index_path, updated)
            fault('after-index')
            # Reuse recovery path on the next call if interruption occurs here.
            for receipt in receipt_bases:
                immutable(record_path(root, data, 'receipts', receipt['request_id']),
                          dict(receipt, after_index_revision=updated['revision']))
            return {'status': 'integrated', 'task_id': task_id, 'request_ids': request_ids,
                    'revision': updated['revision'], 'consent_verification': 'recorded-only'}
    except (OSError, ValueError, KeyError, TypeError, StopIteration):
        return {'status': 'conflict', 'reason': 'integration-or-recovery-input-unverified',
                'index_may_be_committed': True, 'retry': 'Inspect index and intent; never replay blindly.'}
