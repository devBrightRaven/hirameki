"""Read-only tidy completion proposals from an explicit local fixture/index.

No writer, archive operation, authority creation or live scheduler integration.
Python 3.10+. Gate version is read from the shared source file, not a CLI value.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

from archive_gate import assess_candidate
from task_view_cli import INDEX_BYTE_LIMIT, contained, load_view, read_json


def read_gate(path):
    raw = path.read_bytes()
    if len(raw) > 4096:
        raise ValueError('gate-file-budget')
    lines = raw.decode('utf-8').splitlines()
    if len(lines) != 1 or not lines[0] or lines[0] != lines[0].strip():
        raise ValueError('invalid-gate-file')
    return lines[0], hashlib.sha256(raw).hexdigest()


def dry_run(root, data, gate_path):
    gate, gate_digest = read_gate(gate_path)
    root = root.resolve()
    index_path = contained(root, str(Path(data) / 'index.json'))
    before = read_json(index_path, byte_limit=INDEX_BYTE_LIMIT)
    view = load_view(root, data, gate)
    after = read_json(index_path, byte_limit=INDEX_BYTE_LIMIT)
    if before != after:
        raise ValueError('index-changed-during-read')
    proposals = []
    uncertain_ids = {task.get('task_id') for task in view['uncertain']}
    global_uncertainty = any(not error.get('task_id') for error in view['exceptions'])
    for task in view['active']:
        if task.get('restore_pending'):
            assessment = {'task_id': task['task_id'], 'classification': 'incomplete',
                          'reasons': ['restore-awaiting-integration'], 'write_authorized': False}
        elif global_uncertainty or task['task_id'] in uncertain_ids:
            assessment = {'task_id': task['task_id'], 'classification': 'unknown',
                          'reasons': ['reader-exceptions-require-resolution'], 'write_authorized': False}
        else:
            # The shared reader checked these hashes. Missing/changed sources
            # on active tasks are explicitly flagged; never self-assert freshness.
            current = None if task.get('source_changed') else task.get('source_digests')
            assessment = assess_candidate(task, current_sources=current, gate_version=gate)
        proposals.append(assessment)
    exceptions = []
    for error in view['exceptions']:
        item = dict(error)
        if not item.get('path'):
            task = before.get('tasks', {}).get(item.get('task_id'), {})
            paths = sorted({s['path'] for s in task.get('sources', []) if s.get('path')})
            item['path'] = paths[0] if len(paths) == 1 else index_path.relative_to(root).as_posix()
            if paths:
                item['source_paths'] = paths
        exceptions.append(item)
    return {'mode': 'dry-run', 'write_authorized': False,
            'index_revision': before.get('revision'),
            'gate_version': gate, 'gate_source_sha256': gate_digest,
            'view_status': view['view_status'], 'proposals': proposals,
            'uncertain': view['uncertain'], 'exceptions': exceptions,
            'limitations': ['Assessor declarations are not independent semantic proof.',
                            'Read consistency is not a lock or cross-file atomicity.',
                            'No archive, restore integration or authorization is performed.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--vault', type=Path, required=True)
    parser.add_argument('--data', required=True, help='Vault-relative task data directory')
    args = parser.parse_args()
    try:
        report = dry_run(args.vault, args.data, Path(__file__).with_name('TASK_GATE_VERSION'))
    except (OSError, ValueError, KeyError, TypeError):
        print(json.dumps({'mode': 'dry-run', 'write_authorized': False,
                          'view_status': 'unavailable', 'proposals': [],
                          'exceptions': [{'reason': 'invalid-or-unavailable-input'}]}))
        return 1
    print(json.dumps(report, ensure_ascii=False, allow_nan=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
