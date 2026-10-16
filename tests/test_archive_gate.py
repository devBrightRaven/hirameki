"""Synthetic, read-only archive proposal tests; no live vault or scheduler."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))
from archive_gate import assess_candidate


class ArchiveGateTests(unittest.TestCase):
    def setUp(self):
        self.task = {
            'task_id': 'fixture', 'state': 'active', 'revision': 1,
            'assessment': 'confirmed', 'assessed_gate_version': 'fixture-gate',
            'criteria': [{'criterion_id': 'c1', 'description': 'Deployment accepted',
                          'result': 'met', 'evidence_refs': ['e1']}],
            'evidence': [{'evidence_id': 'e1', 'source_id': 'note.md#acceptance',
                          'outcome': 'Fixture acceptance reported'}],
            'source_digests': {'note.md#acceptance': 'a' * 64},
            'open_dependencies': [],
        }
        self.sources = dict(self.task['source_digests'])

    def assess(self):
        return assess_candidate(self.task, current_sources=self.sources,
                                gate_version='fixture-gate')

    def test_complete_is_only_proposal_and_no_mutation(self):
        before = deepcopy(self.task)
        result = self.assess()
        self.assertEqual('completion_candidate', result['classification'])
        self.assertFalse(result['write_authorized'])
        self.assertEqual(before, self.task)

    def test_partial_or_required_deployment_pending_is_not_complete(self):
        for state in ('unmet', 'unknown'):
            self.task['criteria'][0]['result'] = state
            self.assertNotEqual('completion_candidate', self.assess()['classification'])

    def test_legacy_checkbox_or_prose_is_not_structured_fulfillment(self):
        self.task['criteria'] = ['[x] Done']
        self.assertEqual('unknown', self.assess()['classification'])

    def test_source_change_is_conflict(self):
        self.sources['note.md#acceptance'] = 'b' * 64
        self.assertEqual('conflict', self.assess()['classification'])

    def test_missing_source_is_unknown(self):
        self.sources = {}
        self.assertEqual('unknown', self.assess()['classification'])

    def test_gate_change_is_unknown(self):
        self.task['assessed_gate_version'] = 'old-gate'
        self.assertEqual('unknown', self.assess()['classification'])

    def test_dependency_prevents_completion(self):
        self.task['open_dependencies'] = ['required production verification']
        self.assertEqual('incomplete', self.assess()['classification'])

    def test_unreferenced_or_missing_evidence_prevents_completion(self):
        self.task['criteria'][0]['evidence_refs'] = ['missing']
        self.assertEqual('unknown', self.assess()['classification'])

    def test_duplicate_criteria_and_evidence_are_invalid(self):
        for field in ('criteria', 'evidence'):
            original = deepcopy(self.task[field])
            self.task[field].append(deepcopy(original[0]))
            self.assertEqual('unknown', self.assess()['classification'])
            self.task[field] = original

    def test_evidence_must_match_known_source(self):
        self.task['evidence'][0]['source_id'] = 'other.md#missing'
        self.assertEqual('unknown', self.assess()['classification'])

    def test_conflicting_assessment_is_preserved(self):
        self.task['assessment'] = 'conflict'
        self.assertEqual('conflict', self.assess()['classification'])


if __name__ == '__main__':
    unittest.main()
