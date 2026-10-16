"""Pure archival completion proposal gate. No I/O, scheduling or write authority.

Criterion results and outcomes are an assessor's declarations, not independent
proof of semantic truth. The writer must separately verify authority and current
source/index revisions immediately before any authorized integration.
"""
from task_contract_primitives import text, sha256


def assess_candidate(task, *, current_sources, gate_version):
    """Classify one immutable input; never turn a proposal into an operation."""
    result = {'task_id': task.get('task_id') if isinstance(task, dict) else None,
              'classification': 'unknown', 'reasons': [],
              'write_authorized': False, 'gate_version': gate_version,
              'semantic_verification': 'assessor-declaration-only'}

    def finish(classification, reason):
        result['classification'] = classification
        result['reasons'].append(reason)
        return result

    if (not isinstance(task, dict) or not text(task.get('task_id'))
            or task.get('state') not in ('active', 'archived')
            or type(task.get('revision')) is not int or task['revision'] < 1):
        return finish('unknown', 'invalid-task-identity')
    if task.get('assessment') == 'conflict':
        return finish('conflict', 'conflicting-assessment')
    if task.get('assessment') != 'confirmed':
        return finish('unknown', 'unconfirmed-assessment')
    if not text(gate_version) or task.get('assessed_gate_version') != gate_version:
        return finish('unknown', 'gate-unverified')
    expected = task.get('source_digests')
    if (not isinstance(expected, dict) or not expected
            or not all(text(key) and sha256(value) for key, value in expected.items())
            or not isinstance(current_sources, dict)
            or any(key not in current_sources for key in expected)):
        return finish('unknown', 'source-unverified')
    if any(expected[key] != current_sources[key] for key in expected):
        return finish('conflict', 'source-changed')
    dependencies = task.get('open_dependencies')
    if not isinstance(dependencies, list):
        return finish('unknown', 'invalid-dependencies')
    if dependencies:
        return finish('incomplete', 'open-dependencies')
    criteria, evidence = task.get('criteria'), task.get('evidence')
    if not isinstance(criteria, list) or not criteria or not isinstance(evidence, list) or not evidence:
        return finish('unknown', 'missing-completion-baseline')
    evidence_ids = set()
    for item in evidence:
        if (not isinstance(item, dict) or not text(item.get('evidence_id'))
                or not text(item.get('outcome')) or not text(item.get('source_id'))
                or item['source_id'] not in expected or item['evidence_id'] in evidence_ids):
            return finish('unknown', 'invalid-or-unanchored-evidence')
        evidence_ids.add(item['evidence_id'])
    criterion_ids = set()
    unmet = False
    for item in criteria:
        if (not isinstance(item, dict) or not text(item.get('criterion_id'))
                or not text(item.get('description')) or item['criterion_id'] in criterion_ids
                or item.get('result') not in ('met', 'unmet', 'unknown')):
            return finish('unknown', 'invalid-completion-criterion')
        criterion_ids.add(item['criterion_id'])
        if item['result'] == 'unknown':
            return finish('unknown', 'criterion-unconfirmed')
        if item['result'] == 'unmet':
            unmet = True
            continue
        refs = item.get('evidence_refs')
        if (not isinstance(refs, list) or not refs
                or not all(text(ref) and ref in evidence_ids for ref in refs)):
            return finish('unknown', 'criterion-evidence-unverified')
    if unmet:
        return finish('incomplete', 'criterion-not-met')
    result['criterion_ids'] = sorted(criterion_ids)
    result['evidence_ids'] = sorted(evidence_ids)
    return finish('completion_candidate', 'declared-criteria-supported-by-current-sources')
