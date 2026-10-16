import importlib.util
from pathlib import Path
import unittest
from copy import deepcopy

spec = importlib.util.spec_from_file_location('task_view', Path(__file__).parents[1] / 'scripts/task_view.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.index = {'schema_version': 1, 'revision': 'index-1', 'applied_requests': {},
                      'tasks': {'t': {'task_id': 't', 'revision': 1, 'state': 'archived',
                                      'assessment': 'confirmed', 'assessed_gate_version': 'g1',
                                      'source_digests': {'note': 'hash'}}}}
        self.request = {'request_id': 'r', 'task_id': 't', 'payload_digest': 'digest',
                        'base_task_revision': 1, 'base_source_digests': {'note': 'hash'}}

    def view(self, requests=(), receipts=(), **kw):
        args = {'approved_digests': {'digest'}, 'gate_version': 'g1',
                'current_sources': {'t': {'note': 'hash'}}}
        args.update(kw)
        return module.effective_view(self.index, requests, receipts, **args)

    def test_archived_hidden_only_when_confirmed(self):
        self.assertEqual([], self.view()['active'])
        self.assertEqual([], self.view()['uncertain'])

    def test_restore_is_immediate_without_write(self):
        before = deepcopy(self.index)
        result = self.view([self.request])
        self.assertTrue(result['active'][0]['restore_pending'])
        self.assertEqual(before, self.index)

    def test_repeated_request_one_task(self):
        result = self.view([self.request, self.request])
        self.assertEqual(1, len(result['active']))
        self.assertEqual(['r'], result['active'][0]['pending_requests'])

    def test_later_archive_not_overridden(self):
        self.index['tasks']['t']['revision'] = 2
        result = self.view([self.request])
        self.assertEqual([], result['active'])
        self.assertEqual(1, len(result['uncertain']))

    def test_index_first_no_replay(self):
        self.index['applied_requests']['r'] = {'payload_digest': 'digest'}
        self.assertEqual([], self.view([self.request])['active'])

    def test_receipt_first_visible_uncertainty(self):
        result = self.view([self.request], [{'request_id': 'r', 'task_id': 't', 'payload_digest': 'digest'}])
        self.assertEqual([], result['active'])
        self.assertTrue(result['uncertain'])

    def test_missing_revoked_approval(self):
        result = self.view([self.request], approved_digests=())
        self.assertTrue(result['uncertain'])
        self.assertEqual([], result['active'])

    def test_gate_change_keeps_archived_uncertain(self):
        result = self.view(gate_version='g2')
        self.assertEqual('archived', result['uncertain'][0]['state'])

    def test_source_change_is_uncertain(self):
        self.assertTrue(self.view(current_sources={'t': {'note': 'new'}})['uncertain'])

    def test_unrelated_global_revision_allows_restore(self):
        self.index['revision'] = 'index-2'
        self.assertTrue(self.view([self.request])['active'])

    def test_conflicting_immutable_request(self):
        other = dict(self.request, payload_digest='different')
        result = self.view([self.request, other])
        self.assertEqual([], result['active'])
        self.assertTrue(result['uncertain'])

    def test_invalid_index_not_all_done(self):
        self.index = {}
        self.assertTrue(self.view()['exceptions'])

    def test_unverified_inputs_never_assume_fresh(self):
        result = module.effective_view(self.index)
        self.assertTrue(result['uncertain'])

    def test_active_unknown_remains_active(self):
        self.index['tasks']['t'].update(state='active', assessment='unknown')
        self.assertEqual(1, len(self.view()['active']))

    def test_active_gate_upgrade_remains_active(self):
        self.index['tasks']['t']['state'] = 'active'
        self.assertEqual(1, len(self.view(gate_version='g2')['active']))

    def test_active_source_change_remains_visible(self):
        self.index['tasks']['t']['state'] = 'active'
        self.assertTrue(self.view(current_sources={})['active'][0]['source_changed'])

    def test_restore_active_is_exception_not_pending(self):
        self.index['tasks']['t']['state'] = 'active'
        result = self.view([self.request])
        self.assertNotIn('restore_pending', result['active'][0])
        self.assertTrue(result['exceptions'])

    def test_unresolved_history_is_visible_without_asserting_active_or_archived(self):
        self.index['tasks']['t'].update(state='unresolved', assessment='unknown',
                                       summary='Historical ownership not established')
        result = self.view()
        self.assertEqual([], result['active'])
        self.assertEqual('unresolved', result['uncertain'][0]['state'])
        self.assertEqual('historical-state-unresolved',
                         result['uncertain'][0]['uncertainty_reason'])
        self.assertEqual([], result['exceptions'])

    def test_approval_cannot_restore_an_unresolved_history_record(self):
        self.index['tasks']['t'].update(state='unresolved', assessment='unknown')
        result = self.view([self.request])
        self.assertEqual([], result['active'])
        self.assertFalse(result['uncertain'][0].get('restore_pending', False))
        self.assertIn('restore-not-archived', [e['reason'] for e in result['exceptions']])


if __name__ == '__main__':
    unittest.main()
