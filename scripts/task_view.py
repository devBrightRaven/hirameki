"""Pure task-view projection. No vault access, authorization inference or writes."""
from copy import deepcopy


def effective_view(index, requests=(), receipts=(), *, approved_digests=(),
                   current_sources=None, gate_version=None):
    """Caller supplies matched approval records and current source hashes.

    Record matching does not independently prove a human utterance or consent.

    None means not verified, never an empty successful scan. Stable task IDs
    and monotonic revisions are owned by the future single-writer integration.
    """
    result = {'active': [], 'uncertain': [], 'exceptions': []}
    if (not isinstance(index, dict) or index.get('schema_version') != 1
            or not isinstance(index.get('tasks'), dict)
            or not isinstance(index.get('applied_requests'), dict)):
        result['exceptions'].append({'reason': 'invalid-index'})
        return result
    tasks = deepcopy(index['tasks'])
    uncertain = set()

    def flag(task_id, reason):
        uncertain.add(task_id)
        result['exceptions'].append({'task_id': task_id, 'reason': reason})

    for task_id, task in tasks.items():
        if (not isinstance(task, dict) or task.get('task_id') != task_id
                or task.get('state') not in ('active', 'archived', 'unresolved')
                or type(task.get('revision')) is not int
                or task['revision'] < 1):
            tasks[task_id] = {'task_id': task_id}
            flag(task_id, 'invalid-task')
            continue
        archived = task['state'] == 'archived'
        if task['state'] == 'unresolved':
            uncertain.add(task_id)
            task['uncertainty_reason'] = 'historical-state-unresolved'
            if task.get('assessment') not in ('unknown', 'conflict'):
                flag(task_id, 'invalid-unresolved-assessment')
        if archived and task.get('assessment') != 'confirmed':
            flag(task_id, 'unconfirmed-assessment')
        if archived and (gate_version is None or task.get('assessed_gate_version') != gate_version):
            flag(task_id, 'gate-unverified')
        if (current_sources is None or task_id not in current_sources
                or task.get('source_digests') != current_sources[task_id]):
            if archived:
                flag(task_id, 'source-unverified')
            else:
                task['source_changed'] = True

    applied = index['applied_requests']
    for receipt in receipts:
        request_id = receipt.get('request_id')
        entry = applied.get(request_id)
        if not entry or entry.get('payload_digest') != receipt.get('payload_digest'):
            flag(receipt.get('task_id'), 'receipt-index-inconsistent')

    seen = {}
    for request in requests:
        task_id, request_id = request.get('task_id'), request.get('request_id')
        digest = request.get('payload_digest')
        if not request_id or not digest:
            flag(task_id, 'invalid-request')
            continue
        if request_id in seen and seen[request_id][0] != digest:
            flag(task_id, 'conflicting-request')
            flag(seen[request_id][1], 'conflicting-request')
            continue
        seen[request_id] = (digest, task_id)
        if request_id in applied:
            if applied[request_id].get('payload_digest') != digest:
                flag(task_id, 'applied-request-conflict')
            continue
        if task_id not in tasks:
            flag(task_id, 'unknown-task')
            continue
        if digest not in approved_digests:
            flag(task_id, 'approval-unverified')
            continue
        task = tasks[task_id]
        if task.get('state') == 'active':
            result['exceptions'].append({'task_id': task_id, 'reason': 'restore-already-active'})
            continue
        if task.get('state') != 'archived':
            flag(task_id, 'restore-not-archived')
            continue
        if (request.get('base_task_revision') != task.get('revision')
                or request.get('base_source_digests') != task.get('source_digests')):
            flag(task_id, 'request-base-conflict')
            continue
        if task_id in uncertain:
            continue
        task['effective_state'] = 'active'
        task['restore_pending'] = True
        pending = task.setdefault('pending_requests', [])
        if request_id not in pending:
            pending.append(request_id)

    for task_id, task in tasks.items():
        if task_id in uncertain:
            result['uncertain'].append(task)
        if task.get('state') == 'active' or (task_id not in uncertain and task.get('effective_state') == 'active'):
            if task_id in uncertain:
                task['needs_confirmation'] = True
            result['active'].append(task)
    return result
