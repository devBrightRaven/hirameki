"""Isolated single-writer integration; never uses the real vault or authority."""
from copy import deepcopy
from datetime import datetime, timezone
import json
import subprocess
import sys
from pathlib import Path
import unittest
from unittest.mock import patch

import test_task_view_cli as reader_tests
import task_view_cli as cli
from tidy_writer import restore_once


class WriterTests(unittest.TestCase):
    def setUp(self):
        self.fixture = reader_tests.CliTests('test_request_without_record_unverified')
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.root = self.fixture.root
        self.gate = self.root / 'gate.txt'
        self.gate.write_text('g1\n', encoding='utf-8')
        self.authority_path = self.root / 'authority.json'
        self.now = datetime(2026, 10, 4, tzinfo=timezone.utc)
        self.authority = {
            'schema_version': 1, 'authority_id': 'fixture-authority', 'revision': 1,
            'designated_writer': 'fixture-writer', 'data': 'tasks',
            'operations': ['restore'], 'approved_sources': ['note.md'],
            'gate_version': 'g1', 'index_schema_version': 1,
            'source_ref': 'fixture:explicit-authorization',
            'approved_at': '2026-10-01T10:00:00+09:00',
            'not_before': '2026-10-01T00:00:00+09:00',
            'expires_at': '2026-10-05T00:00:00+09:00', 'revoked': False}
        self.save_authority()
        self.fixture.write('restore-requests/r.json', self.fixture.request)
        self.fixture.write('restore-approvals/a.json', {
            'schema_version': 1, 'approval_id': 'a', 'request_id': 'r', 'task_id': 't',
            'request_digest': self.fixture.request['payload_digest'], 'operation': 'restore',
            'approved_at': '2026-10-01T10:00:00+09:00',
            'source_ref': 'fixture:request-approval', 'recorded_by': 'fixture-agent'})

    def save_authority(self):
        self.authority_path.write_text(json.dumps(self.authority), encoding='utf-8')

    def snapshots(self):
        return {p.relative_to(self.root).as_posix(): p.read_bytes()
                for p in self.root.rglob('*') if p.is_file()}

    def run_writer(self, **kw):
        return restore_once(self.root, 'tasks', self.authority_path,
                            'fixture-writer', self.gate, now=self.now, **kw)

    def test_valid_restore_updates_index_then_immutable_receipt(self):
        before_note = (self.root / 'note.md').read_bytes()
        result = self.run_writer()
        self.assertEqual('integrated', result['status'])
        index = cli.read_json(self.fixture.data / 'index.json')
        self.assertEqual('active', index['tasks']['t']['state'])
        self.assertEqual(2, index['tasks']['t']['revision'])
        self.assertEqual(self.fixture.index['revision'], index['parent_revision'])
        self.assertEqual(self.fixture.request['payload_digest'],
                         index['applied_requests']['r']['payload_digest'])
        self.assertNotIn('source_digests', index['tasks']['t'])
        receipt = cli.read_json(next((self.fixture.data / 'receipts').glob('*.json')))
        self.assertEqual(index['revision'], receipt['after_index_revision'])
        self.assertTrue(cli.receipt_contract(receipt))
        self.assertEqual(before_note, (self.root / 'note.md').read_bytes())
        view = cli.load_view(self.root, 'tasks', 'g1')
        self.assertEqual(['t'], [t['task_id'] for t in view['active']])
        self.assertFalse(view['active'][0].get('restore_pending', False))

    def test_second_run_does_not_replay_or_change_receipt(self):
        self.run_writer()
        before = self.snapshots()
        self.assertEqual('no-op', self.run_writer()['status'])
        self.assertEqual(before, self.snapshots())

    def test_unrelated_global_revision_does_not_invalidate_matching_request(self):
        original_base = self.fixture.request['base_index_revision']
        other = deepcopy(self.fixture.index['tasks']['t'])
        other.update(task_id='other', summary='Independent task')
        self.fixture.index['tasks']['other'] = other
        self.fixture.index['parent_revision'] = original_base
        self.fixture.index['revision'] = cli.digest(self.fixture.index, 'revision')
        self.fixture.write('index.json', self.fixture.index)
        self.assertNotEqual(original_base, self.fixture.index['revision'])
        result = self.run_writer()
        self.assertEqual('integrated', result['status'])
        index = cli.read_json(self.fixture.data / 'index.json')
        self.assertEqual(other, index['tasks']['other'])
        receipt = cli.read_json(next((self.fixture.data / 'receipts').glob('*.json')))
        self.assertEqual(self.fixture.index['revision'], receipt['before_index_revision'])

    def test_later_task_revision_rejects_old_approved_request(self):
        self.fixture.index['tasks']['t']['revision'] = 2
        self.fixture.index['revision'] = cli.digest(self.fixture.index, 'revision')
        self.fixture.write('index.json', self.fixture.index)
        before_index = (self.fixture.data / 'index.json').read_bytes()
        result = self.run_writer()
        self.assertEqual('no-op', result['status'])
        self.assertIn('request-base-conflict', [e['reason'] for e in result['exceptions']])
        self.assertEqual(before_index, (self.fixture.data / 'index.json').read_bytes())
        self.assertFalse((self.fixture.data / 'receipts').exists())

    def test_crash_after_index_recovers_receipt_without_replaying(self):
        def crash(stage):
            if stage == 'after-index':
                raise RuntimeError('fixture crash')
        with self.assertRaisesRegex(RuntimeError, 'fixture crash'):
            self.run_writer(fault=crash)
        committed = (self.fixture.data / 'index.json').read_bytes()
        self.assertFalse((self.fixture.data / 'receipts').exists())
        view = cli.load_view(self.root, 'tasks', 'g1')
        self.assertEqual(['t'], [t['task_id'] for t in view['active']])
        self.assertFalse(view['active'][0].get('restore_pending', False))
        self.assertEqual('recovered', self.run_writer()['status'])
        self.assertEqual(committed, (self.fixture.data / 'index.json').read_bytes())
        self.assertEqual(2, cli.read_json(self.fixture.data / 'index.json')['tasks']['t']['revision'])
        self.assertEqual([], cli.load_view(self.root, 'tasks', 'g1')['exceptions'])

    def test_missing_revoked_expired_or_wrong_scope_never_writes(self):
        for key, value in [('revoked', True), ('designated_writer', 'other'),
                           ('data', 'another'), ('operations', ['archive']),
                           ('approved_sources', []), ('gate_version', 'old'),
                           ('expires_at', '2026-10-03T00:00:00+00:00')]:
            with self.subTest(key=key):
                original = deepcopy(self.authority)
                self.authority[key] = value
                self.save_authority()
                before = self.snapshots()
                self.assertEqual('read-only', self.run_writer()['status'])
                self.assertEqual(before, self.snapshots())
                self.authority = original
        self.authority_path.unlink()
        before = self.snapshots()
        self.assertEqual('read-only', self.run_writer()['status'])
        self.assertEqual(before, self.snapshots())

    def test_revocation_between_plan_and_commit_stops_index_write(self):
        before = (self.fixture.data / 'index.json').read_bytes()
        def revoke(stage):
            if stage == 'before-commit':
                self.authority['revoked'] = True
                self.save_authority()
        result = self.run_writer(fault=revoke)
        self.assertEqual('conflict', result['status'])
        self.assertEqual(before, (self.fixture.data / 'index.json').read_bytes())
        self.assertFalse((self.fixture.data / 'receipts').exists())

    def test_source_change_between_plan_and_commit_stops_index_write(self):
        before = (self.fixture.data / 'index.json').read_bytes()
        def change(stage):
            if stage == 'before-commit':
                (self.root / 'note.md').write_text('changed fixture', encoding='utf-8')
        self.assertEqual('conflict', self.run_writer(fault=change)['status'])
        self.assertEqual(before, (self.fixture.data / 'index.json').read_bytes())

    def test_cancelled_request_is_not_integrated(self):
        approval = cli.read_json(self.fixture.data / 'restore-approvals/a.json')
        self.fixture.write('approval-cancellations/c.json', {
            'schema_version': 1, 'cancellation_id': 'c', 'approval_id': 'a',
            'approval_digest': cli.digest(approval), 'operation': 'cancel-approval',
            'source_ref': 'fixture:cancel', 'recorded_by': 'fixture-agent'})
        before = (self.fixture.data / 'index.json').read_bytes()
        self.assertEqual('no-op', self.run_writer()['status'])
        self.assertEqual(before, (self.fixture.data / 'index.json').read_bytes())

    def test_corrupt_receipt_is_not_overwritten(self):
        self.run_writer()
        path = next((self.fixture.data / 'receipts').glob('*.json'))
        path.write_text('{', encoding='utf-8')
        before = path.read_bytes()
        self.assertEqual('conflict', self.run_writer()['status'])
        self.assertEqual(before, path.read_bytes())

    def test_new_approval_after_cancellation_is_the_receipt_source(self):
        approval = cli.read_json(self.fixture.data / 'restore-approvals/a.json')
        self.fixture.write('approval-cancellations/c.json', {
            'schema_version': 1, 'cancellation_id': 'c', 'approval_id': 'a',
            'approval_digest': cli.digest(approval), 'operation': 'cancel-approval',
            'source_ref': 'fixture:cancel-old', 'recorded_by': 'fixture-agent'})
        replacement = dict(approval, approval_id='b', source_ref='fixture:new-approval')
        self.fixture.write('restore-approvals/b.json', replacement)
        self.assertEqual('integrated', self.run_writer()['status'])
        receipt = cli.read_json(next((self.fixture.data / 'receipts').glob('*.json')))
        self.assertIn('fixture:new-approval', receipt['evidence_refs'])
        self.assertNotIn(approval['source_ref'], receipt['evidence_refs'])

    def test_restored_task_needs_new_completion_assessment(self):
        self.run_writer()
        task = cli.load_view(self.root, 'tasks', 'g1')['active'][0]
        from archive_gate import assess_candidate
        self.assertEqual('unknown', assess_candidate(
            task, current_sources=task['source_digests'], gate_version='g1')['classification'])

    def test_failed_snapshot_replace_has_no_success_receipt(self):
        before = (self.fixture.data / 'index.json').read_bytes()
        with patch('tidy_writer.os.replace', side_effect=OSError('fixture replace denied')):
            self.assertEqual('conflict', self.run_writer()['status'])
        self.assertEqual(before, (self.fixture.data / 'index.json').read_bytes())
        self.assertFalse((self.fixture.data / 'receipts').exists())
        self.assertEqual([], list(self.fixture.data.glob('.tidy-index-*.tmp')))
        self.assertEqual('integrated', self.run_writer()['status'])

    def test_process_exit_releases_local_lock_and_recovers_without_replay(self):
        code = '''
import os, sys
from pathlib import Path
from datetime import datetime, timezone
sys.path.insert(0, sys.argv[1])
from tidy_writer import restore_once
def stop(stage):
    if stage == 'after-index':
        os._exit(23)
restore_once(Path(sys.argv[2]), 'tasks', Path(sys.argv[3]), 'fixture-writer',
             Path(sys.argv[4]), now=datetime(2026, 10, 4, tzinfo=timezone.utc), fault=stop)
'''
        run = subprocess.run([sys.executable, '-B', '-X', 'utf8', '-c', code,
                              str(Path(__file__).parents[1] / 'scripts'), str(self.root),
                              str(self.authority_path), str(self.gate)],
                             capture_output=True, timeout=15,
                             creationflags=(subprocess.CREATE_NO_WINDOW
                                            if sys.platform == 'win32' else 0))
        self.assertEqual(23, run.returncode, run.stderr.decode('utf-8'))
        committed = (self.fixture.data / 'index.json').read_bytes()
        self.assertEqual('recovered', self.run_writer()['status'])
        self.assertEqual(committed, (self.fixture.data / 'index.json').read_bytes())

    def test_duplicate_approved_requests_increment_task_only_once(self):
        request = dict(self.fixture.request, request_id='r2', reason='Same approved task scope')
        request['payload_digest'] = cli.digest(request, 'payload_digest')
        self.fixture.write('restore-requests/r2.json', request)
        approval = cli.read_json(self.fixture.data / 'restore-approvals/a.json')
        approval.update(approval_id='a2', request_id='r2', request_digest=request['payload_digest'])
        self.fixture.write('restore-approvals/a2.json', approval)
        self.assertEqual('integrated', self.run_writer()['status'])
        index = cli.read_json(self.fixture.data / 'index.json')
        self.assertEqual(2, index['tasks']['t']['revision'])
        self.assertEqual({'r', 'r2'}, set(index['applied_requests']))
        self.assertEqual(2, len(list((self.fixture.data / 'receipts').glob('*.json'))))

    def test_corrupt_intent_is_not_replaced_during_recovery(self):
        def crash(stage):
            if stage == 'after-index':
                raise RuntimeError('fixture crash')
        with self.assertRaises(RuntimeError):
            self.run_writer(fault=crash)
        path = next((self.fixture.data / 'integration-intents').glob('*.json'))
        path.write_text('{', encoding='utf-8')
        before = self.snapshots()
        self.assertEqual('conflict', self.run_writer()['status'])
        self.assertEqual(before, self.snapshots())

    def test_cancellation_between_plan_and_commit_stops_integration(self):
        before = (self.fixture.data / 'index.json').read_bytes()
        approval = cli.read_json(self.fixture.data / 'restore-approvals/a.json')
        def cancel(stage):
            if stage == 'before-commit':
                self.fixture.write('approval-cancellations/c.json', {
                    'schema_version': 1, 'cancellation_id': 'c', 'approval_id': 'a',
                    'approval_digest': cli.digest(approval), 'operation': 'cancel-approval',
                    'source_ref': 'fixture:late-cancel', 'recorded_by': 'fixture-agent'})
        self.assertEqual('conflict', self.run_writer(fault=cancel)['status'])
        self.assertEqual(before, (self.fixture.data / 'index.json').read_bytes())

    def test_concurrent_index_change_is_not_overwritten(self):
        changed = deepcopy(self.fixture.index)
        changed['tasks']['t']['summary'] = 'Newer independent fixture edit'
        changed['revision'] = cli.digest(changed, 'revision')
        def edit(stage):
            if stage == 'before-commit':
                self.fixture.write('index.json', changed)
        self.assertEqual('conflict', self.run_writer(fault=edit)['status'])
        self.assertEqual(changed, cli.read_json(self.fixture.data / 'index.json'))

    def test_syncthing_intent_conflict_is_visible_without_overwrite(self):
        def crash(stage):
            if stage == 'after-index':
                raise RuntimeError('fixture crash')
        with self.assertRaises(RuntimeError):
            self.run_writer(fault=crash)
        path = next((self.fixture.data / 'integration-intents').glob('*.json'))
        conflict = path.with_name(path.stem + '.sync-conflict-fixture.json')
        conflict.write_bytes(path.read_bytes())
        before = self.snapshots()
        self.assertEqual('conflict', self.run_writer()['status'])
        self.assertEqual(before, self.snapshots())


if __name__ == '__main__':
    unittest.main()
