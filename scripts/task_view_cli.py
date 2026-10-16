"""Shared read-only task adapter for Claude and Codex. Python 3.10+."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

from task_view import effective_view
from task_contract_primitives import text, sha256
from archive_gate import assess_candidate
from task_restore_contract import (offset_timestamp, digest, request_valid,
                                   approval_valid, public_contract,
                                   approval_matches_request, pair_errors)

RECORD_BYTE_LIMIT = 1024 * 1024
INDEX_BYTE_LIMIT = 16 * RECORD_BYTE_LIMIT
INDEX_TASK_LIMIT = 10000


def has_descriptive_content(value):
    """Presence check only; does not establish truth, fulfillment or provenance."""
    if isinstance(value, str):
        return text(value)
    if isinstance(value, dict):
        return any(has_descriptive_content(item) for item in value.values())
    if isinstance(value, list):
        return any(has_descriptive_content(item) for item in value)
    return False


def task_contract(task_id, task):
    if not isinstance(task, dict):
        return False
    return (text(task_id) and task.get('task_id') == task_id
            and type(task.get('revision')) is int and task['revision'] > 0
            and task.get('state') in ('active', 'archived', 'unresolved')
            and (task.get('state') != 'unresolved'
                 or task.get('assessment') in ('unknown', 'conflict'))
            and all(text(task.get(key)) for key in
                    ('scope', 'summary', 'reason', 'assessed_gate_version', 'operation_id'))
            and all(isinstance(task.get(key), list) for key in
                    ('criteria', 'evidence', 'open_dependencies'))
            and task.get('assessment') in ('confirmed', 'unknown', 'conflict')
            and 'previous_revision' in task
            and (task['previous_revision'] is None
                 or (type(task['previous_revision']) is int
                     and 0 < task['previous_revision'] < task['revision'])))


def receipt_contract(record):
    return (all(text(record.get(key)) for key in
                ('request_id', 'task_id', 'owner', 'gate', 'authorization_ref', 'recovery_outcome'))
            and all(sha256(record.get(key)) for key in
                    ('payload_digest', 'before_index_revision', 'after_index_revision'))
            and record['before_index_revision'] != record['after_index_revision']
            and record.get('operation') == 'restore'
            and type(record.get('before_task_revision')) is int
            and type(record.get('after_task_revision')) is int
            and record['before_task_revision'] > 0
            and record['after_task_revision'] == record['before_task_revision'] + 1
            and isinstance(record.get('evidence_refs'), list)
            and bool(record['evidence_refs']) and all(text(ref) for ref in record['evidence_refs']))


def contained(root, relative):
    path = Path(relative)
    if path.is_absolute() or '..' in path.parts:
        raise ValueError('unsafe-path')
    target = root / path
    for part in (target, *target.parents):
        if part == root.parent:
            break
        junction = getattr(part, 'is_junction', lambda: False)()
        if part.is_symlink() or junction:
            raise ValueError('linked-path')
    if not target.resolve().is_relative_to(root.resolve()):
        raise ValueError('escaped-path')
    return target


def no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate-key')
        result[key] = value
    return result


def read_json(path, *, byte_limit=RECORD_BYTE_LIMIT):
    with path.open('rb') as stream:
        raw = stream.read(byte_limit + 1)
    if len(raw) > byte_limit:
        raise ValueError('file-budget')
    value = json.loads(raw.decode('utf-8'), object_pairs_hook=no_duplicates,
                       parse_constant=lambda _: (_ for _ in ()).throw(ValueError('nonfinite')))
    if (not isinstance(value, dict)
            or type(value.get('schema_version')) is not int
            or value['schema_version'] != 1):
        raise ValueError('invalid-schema')
    return value


def records(root, directory, errors):
    folder = contained(root, directory)
    if not folder.exists():
        return []
    files = sorted(folder.glob('*.json'))
    if len(files) > 2000:
        errors.append({'path': directory, 'reason': 'record-budget', 'unprocessed': len(files)-2000})
    result = []
    for path in files[:2000]:
        relative = path.relative_to(root).as_posix()
        try:
            record = read_json(contained(root, relative))
            if '.sync-conflict-' in path.name:
                errors.append({'path': relative, 'task_id': record.get('task_id'),
                               'reason': 'sync-conflict-copy'})
                continue
            result.append((relative, record))
        except (OSError, ValueError, TypeError):
            errors.append({'path': relative, 'reason': 'sync-conflict-copy'
                           if '.sync-conflict-' in path.name else 'invalid-record'})
    return result


def load_view(root, data, gate, *, task_id=None):
    """No writes. root/data are explicit local paths, not runtime config in vault."""
    requested_id = task_id  # Existing validation loops use task_id locally.
    root = root.resolve()
    data_path = contained(root, data)
    index = read_json(contained(root, str((data_path / 'index.json').relative_to(root))),
                      byte_limit=INDEX_BYTE_LIMIT)
    if index.get('revision') != digest(index, 'revision'):
        raise ValueError('index-digest-mismatch')
    if not isinstance(index.get('tasks'), dict) or not isinstance(index.get('applied_requests'), dict):
        raise ValueError('invalid-index')
    if len(index['tasks']) > INDEX_TASK_LIMIT:
        raise ValueError('task-budget')
    if (not text(index.get('writer')) or not text(index.get('gate_version'))
            or 'parent_revision' not in index
            or (index['parent_revision'] is not None and not sha256(index['parent_revision']))):
        raise ValueError('invalid-index-contract')
    for request_id, applied in index['applied_requests'].items():
        if (not isinstance(request_id, str) or not request_id
                or not isinstance(applied, dict)
                or not sha256(applied.get('payload_digest'))
                or not text(applied.get('task_id'))
                or applied['task_id'] not in index['tasks']
                or type(applied.get('task_revision')) is not int
                or applied['task_revision'] < 1
                or not isinstance(index['tasks'][applied['task_id']], dict)
                or type(index['tasks'][applied['task_id']].get('revision')) is not int
                or applied['task_revision'] > index['tasks'][applied['task_id']]['revision']):
            raise ValueError('invalid-applied-request')
    errors, approved, sources = [], set(), {}
    request_records = records(root, str((data_path / 'restore-requests').relative_to(root)), errors)
    approvals, approval_groups = [], {}
    for relative, record in records(root, str((data_path / 'restore-approvals').relative_to(root)), errors):
        if not approval_valid(record):
            errors.append({'path': relative, 'task_id': record.get('task_id'),
                           'reason': 'invalid-approval'})
            continue
        approval_groups.setdefault(record['approval_id'], []).append((relative, record))
    for group in approval_groups.values():
        if len({digest(record) for _, record in group}) > 1:
            for relative, record in group:
                errors.append({'path': relative, 'task_id': record['task_id'],
                               'reason': 'conflicting-approval'})
        else:
            approvals.append(group[0][1])
    cancelled = set()
    cancellation_directory = str((data_path / 'approval-cancellations').relative_to(root))
    cancellation_records = records(root, cancellation_directory, errors)
    known_approvals = {(a['approval_id'], digest(a)) for a in approvals}
    cancellation_groups = {}
    for relative, record in cancellation_records:
        fields = ('cancellation_id', 'approval_id', 'approval_digest', 'source_ref', 'recorded_by')
        if (record.get('operation') != 'cancel-approval'
                or not all(isinstance(record.get(k), str) and record[k].strip() for k in fields)):
            errors.append({'path': relative, 'reason': 'invalid-cancellation'})
            continue
        cancellation_groups.setdefault(record['cancellation_id'], []).append((relative, record))
    for group in cancellation_groups.values():
        if len({digest(record) for _, record in group}) > 1:
            errors.extend({'path': relative, 'reason': 'conflicting-cancellation'}
                          for relative, _ in group)
            continue
        relative, record = group[0]
        target = (record['approval_id'], record['approval_digest'])
        if target not in known_approvals:
            errors.append({'path': relative, 'reason': 'cancellation-target-unavailable'})
            continue
        cancelled.add(target)
    approvals = [a for a in approvals if (a['approval_id'], digest(a)) not in cancelled]
    receipts, receipt_groups = [], {}
    for relative, record in records(root, str((data_path / 'receipts').relative_to(root)), errors):
        if not receipt_contract(record):
            errors.append({'path': relative, 'task_id': record.get('task_id'), 'reason': 'invalid-receipt'})
        else:
            receipt_groups.setdefault(record['request_id'], []).append((relative, record))
    for group in receipt_groups.values():
        if len({digest(record) for _, record in group}) > 1:
            for relative, record in group:
                errors.append({'path': relative, 'task_id': record['task_id'],
                               'reason': 'conflicting-receipt'})
        else:
            relative, record = group[0]
            applied = index['applied_requests'].get(record['request_id'])
            if applied and (applied['task_id'] != record['task_id']
                            or applied['task_revision'] != record['after_task_revision']
                            or applied['payload_digest'] != record['payload_digest']):
                errors.append({'path': relative, 'task_id': record['task_id'],
                               'reason': 'receipt-index-inconsistent'})
            else:
                receipts.append(record)
    requests, approval_evidence = [], {}
    for relative, request in request_records:
        if not request_valid(request):
            errors.append({'path': relative, 'task_id': request.get('task_id'), 'reason': 'request-digest-or-schema'})
            continue
        requests.append(request)
        matches = [a for a in approvals if approval_matches_request(a, request)]
        if matches:
            approved.add(request['payload_digest'])
            approval_evidence[request['request_id']] = [
                {'approval_id': a['approval_id'], 'source_ref': a['source_ref'],
                 'approval_sha256': digest(a)} for a in matches]
    source_hashes = {}  # Per invocation only; no persistent mtime-based cache.
    for task_id, task in index['tasks'].items():
        if not task_contract(task_id, task):
            errors.append({'task_id': task_id, 'reason': 'invalid-task-contract'})
        elif task['state'] == 'archived' and (
                not task['criteria'] or not task['evidence'] or task['open_dependencies']
                or not all(has_descriptive_content(item) for item in task['criteria'])
                or not all(has_descriptive_content(item) for item in task['evidence'])):
            # Necessary evidence presence only: this is not semantic acceptance
            # verification or permission to archive. Keep deficient records visible.
            errors.append({'task_id': task_id, 'reason': 'incomplete-archive-baseline'})
        if not isinstance(task, dict) or not isinstance(task.get('sources'), list) or not task['sources']:
            errors.append({'task_id': task_id, 'reason': 'invalid-task-sources'})
            if isinstance(task, dict):
                task['source_digests'] = {}
            continue
        expected, current = {}, {}
        for source in task['sources']:
            try:
                path, anchor = source['path'], source['anchor']
                if (not text(path) or not text(anchor)
                        or not sha256(source.get('raw_sha256'))
                        or not sha256(source.get('lf_sha256'))):
                    raise ValueError('invalid-source-contract')
                identity = path + '#' + anchor
                if identity in expected:
                    raise ValueError('duplicate-source')
                expected[identity] = source['raw_sha256']
                source_path = contained(root, path)
                if source_path not in source_hashes:
                    with source_path.open('rb') as stream:
                        raw = stream.read(RECORD_BYTE_LIMIT + 1)
                    if len(raw) > RECORD_BYTE_LIMIT:
                        raise ValueError('source-budget')
                    source_hashes[source_path] = (
                        hashlib.sha256(raw).hexdigest(),
                        hashlib.sha256(raw.replace(b'\r\n', b'\n')).hexdigest())
                raw_digest, normalized_digest = source_hashes[source_path]
                current[identity] = raw_digest
                if normalized_digest != source['lf_sha256']:
                    errors.append({'task_id': task_id, 'reason': 'normalized-source-mismatch'})
            except (OSError, ValueError, KeyError, TypeError):
                errors.append({'task_id': task_id, 'reason': 'source-unavailable'})
        task['source_digests'] = expected  # derived, never persisted twice
        sources[task_id] = current
        if task_contract(task_id, task) and task['state'] == 'archived':
            completion = assess_candidate(task, current_sources=current, gate_version=gate)
            if completion['classification'] != 'completion_candidate':
                errors.append({'task_id': task_id, 'reason': 'archive-completion-unverified',
                               'classification': completion['classification'],
                               'gate_reasons': completion['reasons']})
    restore_matching_available = not any(error['reason'] == 'record-budget'
           or str(error.get('path', '')).startswith(cancellation_directory.replace('\\', '/') + '/')
           for error in errors)
    if not restore_matching_available:
        approved.clear()  # Missing records may contain conflicting integration evidence.
    result = effective_view(index, requests, receipts, approved_digests=approved,
                            current_sources=sources, gate_version=gate)
    for task in result['active']:
        if task.get('restore_pending'):
            task['restore_approval_refs'] = {
                request_id: approval_evidence[request_id]
                for request_id in task['pending_requests']}
    result['exceptions'].extend(errors)
    affected = {error['task_id'] for error in errors
                if isinstance(error.get('task_id'), str) and error['task_id'] in index['tasks']}
    for task_id in affected:
        task = index['tasks'][task_id]
        if not isinstance(task, dict):
            continue
        if not any(item.get('task_id') == task_id for item in result['uncertain']):
            result['uncertain'].append(task)
        # No restore overlay from conflicting/invalid records. Active originals stay visible.
        result['active'] = [item for item in result['active']
                            if item.get('task_id') != task_id or item.get('state') == 'active']
    result['approval_limit'] = 'Recorded approval matches payload; human utterance is not independently proven.'
    result['view_status'] = 'partial' if result['exceptions'] else 'complete'
    result['index_revision'] = index['revision']
    result['view_revision'] = digest(result)
    if requested_id is not None:
        task_id = requested_id
        # Select only after all index, source and overlay checks have completed.
        found = task_id in index['tasks']
        selected = index['tasks'].get(task_id)
        selected = next((row for row in result['active']
                         if row.get('task_id') == task_id), selected)
        uncertain_ids = [row.get('task_id') for row in result['uncertain']]
        target_errors = [error for error in result['exceptions']
                         if error.get('task_id') == task_id]
        expected = selected.get('source_digests', {}) if isinstance(selected, dict) else {}
        current = sources.get(task_id, {})
        return {
            'query_status': 'found' if found else 'task-not-found',
            'task_id': task_id, 'task': selected,
            'index_revision': result['index_revision'],
            'view_revision': result['view_revision'],
            'view_status': result['view_status'],
            'approval_limit': result['approval_limit'],
            'validation': {
                'status': ('unavailable' if not found else 'unverified'
                           if task_id in uncertain_ids or target_errors else 'verified'),
                'expected_source_digests': expected,
                'current_source_digests': current,
                'sources_match': bool(expected) and expected == current,
                'exceptions': target_errors,
            },
            'global_validation': {
                'full_index_checked': True,
                'restore_matching_available': restore_matching_available,
                'active_count': len(result['active']),
                'uncertain_count': len(result['uncertain']),
                'uncertain_task_ids': uncertain_ids,
                'exception_count': len(result['exceptions']),
                'scope': 'task query, not a complete task inventory',
            },
            'exceptions': result['exceptions'],
        }
    return result


def page_view(view, page_size, offset=0):
    """Bound presentation only; full reader validation and uncertainty stay intact.

    Pages of all three sections use the same offset. Consumers must retain totals,
    follow each non-null next_offset, and pin index_revision between invocations.
    No byte-budget claim: individual task records retain complete evidence.
    """
    if (type(page_size) is not int or not 1 <= page_size <= 100
            or type(offset) is not int or offset < 0):
        raise ValueError('invalid-page-bounds')
    result = dict(view)
    pages = {}
    for section in ('active', 'uncertain', 'exceptions'):
        rows = sorted(view[section], key=lambda row: json.dumps(
            [row.get('task_id', ''), row.get('path', ''), row],
            sort_keys=True, ensure_ascii=False))
        selected = rows[offset:offset + page_size]
        remaining = max(0, len(rows) - offset - len(selected))
        result[section] = selected
        pages[section] = {'total': len(rows), 'returned': len(selected),
                          'earlier_not_displayed': min(offset, len(rows)),
                          'remaining': remaining,
                          'next_offset': offset + len(selected) if remaining else None}
    result['pagination'] = {'page_size': page_size, 'offset': offset,
                            'all_displayed': offset == 0 and all(
                                page['remaining'] == 0 for page in pages.values()),
                            **pages}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--vault', type=Path)
    parser.add_argument('--data', help='Vault-relative task data directory')
    parser.add_argument('--gate-version')
    parser.add_argument('--restore-contract', action='store_true',
                        help='Return bounded canonical restore schemas/digest rules; no vault access')
    parser.add_argument('--validate-restore', action='store_true',
                        help='Read request/approval_record JSON from stdin; validate only, no writes')
    parser.add_argument('--page-size', type=int, help='Optional 1..100 records per section; default full output')
    parser.add_argument('--offset', type=int, default=0)
    parser.add_argument('--expected-revision', help='Reject changed index between page reads')
    parser.add_argument('--expected-view-revision', help='Also reject source/restore/error changes between pages')
    parser.add_argument('--task-id', help='Read-only lookup, including archived tasks; validates the full index first')
    parser.add_argument('--max-output-bytes', type=int, default=16384,
                        help='Task-query UTF-8 output ceiling, 1024..65536 (default 16384); never truncates')
    args = parser.parse_args()
    if args.task_id is not None and (not args.task_id.strip() or args.page_size is not None or args.offset):
        parser.error('--task-id must be nonblank and cannot be combined with paging')
    if not 1024 <= args.max_output_bytes <= 65536:
        parser.error('--max-output-bytes must be between 1024 and 65536')
    if args.restore_contract or args.validate_restore:
        if args.restore_contract and args.validate_restore:
            parser.error('Choose --restore-contract or --validate-restore')
        if any(value is not None for value in (args.vault, args.data, args.gate_version,
                                               args.task_id, args.page_size,
                                               args.expected_revision, args.expected_view_revision)) or args.offset:
            parser.error('--restore-contract cannot be combined with vault/query options')
        if args.restore_contract:
            result = public_contract()
            exit_code = 0
        else:
            try:
                raw = sys.stdin.buffer.read(RECORD_BYTE_LIMIT + 1)
                if len(raw) > RECORD_BYTE_LIMIT: raise ValueError('input-budget')
                records_input = json.loads(raw.decode('utf-8'), object_pairs_hook=no_duplicates,
                                          parse_constant=lambda _: (_ for _ in ()).throw(ValueError('nonfinite')))
                errors = pair_errors(records_input['request'], records_input['approval_record'])
                result = {'valid': not errors, 'errors': errors, 'read_only': True,
                          'source_checks_performed': False, 'human_utterance_proven': False}
                if not errors:
                    result.update(request_digest=records_input['request']['payload_digest'],
                                  approval_record_digest=digest(records_input['approval_record']))
            except (OSError, ValueError, KeyError, TypeError):
                result = {'valid': False, 'errors': ['invalid-or-unavailable-record-pair'], 'read_only': True}
            exit_code = 0 if result['valid'] else 1
        encoded = json.dumps(result, ensure_ascii=False, allow_nan=False)
        size = len((encoded + '\n').encode('utf-8'))
        if size > args.max_output_bytes:
            print(json.dumps({'view_status': 'unavailable', 'query_status': 'output-limit-exceeded',
                              'required_bytes': size, 'max_output_bytes': args.max_output_bytes,
                              'details_returned': False}))
            return 1
        print(encoded)
        return exit_code
    if args.vault is None or args.data is None or args.gate_version is None:
        parser.error('--vault, --data and --gate-version are required for task queries')
    if args.offset < 0 or (args.offset and args.page_size is None):
        parser.error('--offset must be nonnegative and requires --page-size')
    if args.page_size is not None and not 1 <= args.page_size <= 100:
        parser.error('--page-size must be between 1 and 100')
    try:
        output = load_view(args.vault, args.data, args.gate_version, task_id=args.task_id)
        if args.expected_revision is not None and output.get('index_revision') != args.expected_revision:
            print(json.dumps({'view_status': 'unavailable', 'active': [], 'uncertain': [],
                              'exceptions': [{'reason': 'page-index-revision-changed'}]}))
            return 1
        if args.expected_view_revision is not None and output.get('view_revision') != args.expected_view_revision:
            print(json.dumps({'view_status': 'unavailable', 'active': [], 'uncertain': [],
                              'exceptions': [{'reason': 'page-effective-view-changed'}]}))
            return 1
        if args.page_size is not None:
            output = page_view(output, args.page_size, args.offset)
    except (OSError, ValueError, KeyError, TypeError):
        print(json.dumps({'view_status': 'unavailable', 'active': [], 'uncertain': [], 'exceptions': [{'reason': 'invalid-or-unavailable-index'}]}, ensure_ascii=False))
        return 1
    encoded = json.dumps(output, ensure_ascii=False, allow_nan=False)
    if args.task_id is not None and len((encoded + '\n').encode('utf-8')) > args.max_output_bytes:
        print(json.dumps({'view_status': 'unavailable', 'query_status': 'output-limit-exceeded',
                          'task_id': args.task_id, 'required_bytes': len((encoded + '\n').encode('utf-8')),
                          'max_output_bytes': args.max_output_bytes,
                          'index_revision': output['index_revision'], 'view_revision': output['view_revision'],
                          'global_validation': {'full_index_checked': True,
                                                'uncertain_count': output['global_validation']['uncertain_count'],
                                                'exception_count': len(output['exceptions'])},
                          'details_returned': False,
                          'reason': 'Complete task or global diagnostics exceed output ceiling; no truncated result.'},
                         ensure_ascii=False))
        return 1
    print(encoded)
    return 1 if output.get('query_status') == 'task-not-found' else 0


if __name__ == '__main__':
    sys.exit(main())
