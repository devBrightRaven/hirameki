"""Archive writes use synthetic data and explicit fixture authority only."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

import test_task_view_cli as reader_tests
import task_view_cli as cli
from tidy_writer import archive_once, restore_once


class ArchiveWriterTests(unittest.TestCase):
    def setUp(self):
        self.fixture = reader_tests.CliTests('test_request_without_record_unverified')
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.root = self.fixture.root
        self.gate = self.root / 'gate.txt'
        self.gate.write_text('g1\n', encoding='utf-8')
        self.authority_path = self.root / 'authority.json'
        self.now = datetime(2026, 10, 4, tzinfo=timezone.utc)
        self.permission = {
            'schema_version': 1, 'authority_id': 'fixture', 'revision': 1,
            'designated_writer': 'fixture-writer', 'data': 'tasks',
            'operations': ['archive', 'restore'], 'approved_sources': ['note.md'],
            'gate_version': 'g1', 'index_schema_version': 1,
            'source_ref': 'fixture:explicit-archive-authority',
            'approved_at': '2026-10-01T00:00:00+00:00',
            'not_before': '2026-10-01T00:00:00+00:00',
            'expires_at': '2026-10-05T00:00:00+00:00', 'revoked': False}
        self.authority_path.write_text(json.dumps(self.permission), encoding='utf-8')
        self.fixture.index['tasks']['t']['state'] = 'active'
        self.save()

    def save(self):
        self.fixture.index['revision'] = cli.digest(self.fixture.index, 'revision')
        self.fixture.write('index.json', self.fixture.index)

    def run_writer(self, **kwargs):
        return archive_once(self.root, 'tasks', self.authority_path,
                            'fixture-writer', self.gate, now=self.now, **kwargs)

    def test_archive_preserves_note_and_appends_audit_receipt(self):
        note = (self.root / 'note.md').read_bytes()
        result = self.run_writer()
        self.assertEqual('archived', result['status'])
        index = cli.read_json(self.fixture.data / 'index.json')
        self.assertEqual('archived', index['tasks']['t']['state'])
        self.assertEqual(2, index['tasks']['t']['revision'])
        self.assertEqual(self.fixture.index['revision'], index['parent_revision'])
        self.assertEqual(note, (self.root / 'note.md').read_bytes())
        receipt = cli.read_json(next((self.fixture.data / 'archive-receipts').glob('*.json')))
        self.assertEqual('archive', receipt['operation'])
        self.assertEqual(index['revision'], receipt['after_index_revision'])
        view = cli.load_view(self.root, 'tasks', 'g1')
        self.assertEqual([], view['active'])
        self.assertEqual([], view['uncertain'])
        self.assertEqual([], view['exceptions'])
        before = (self.fixture.data / 'index.json').read_bytes()
        self.assertEqual('no-op', self.run_writer()['status'])
        self.assertEqual(before, (self.fixture.data / 'index.json').read_bytes())

    def test_restore_only_authority_cannot_archive(self):
        self.permission['operations'] = ['restore']
        self.authority_path.write_text(json.dumps(self.permission), encoding='utf-8')
        before = {p: p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual('read-only', self.run_writer()['status'])
        self.assertEqual(before, {p: p.read_bytes() for p in self.root.rglob('*') if p.is_file()})

    def test_invalid_authority_schema_and_task_container_fail_closed(self):
        self.permission['schema_version'] = 2
        self.authority_path.write_text(json.dumps(self.permission), encoding='utf-8')
        self.assertEqual('read-only', self.run_writer()['status'])
        self.permission['schema_version'] = 1
        self.authority_path.write_text(json.dumps(self.permission), encoding='utf-8')
        self.fixture.index['tasks'] = []
        self.save()
        before = (self.fixture.data / 'index.json').read_bytes()
        self.assertEqual('read-only', self.run_writer()['status'])
        self.assertEqual(before, (self.fixture.data / 'index.json').read_bytes())

    def test_unknown_does_not_block_other_confirmed_task(self):
        unknown = deepcopy(self.fixture.index['tasks']['t'])
        unknown.update(task_id='u', state='unresolved', assessment='unknown')
        self.fixture.index['tasks']['u'] = unknown
        self.save()
        self.assertEqual('archived', self.run_writer()['status'])
        view = cli.load_view(self.root, 'tasks', 'g1')
        self.assertEqual(['u'], [task['task_id'] for task in view['uncertain']])

    def test_incomplete_or_unverified_declaration_never_archives(self):
        for field, value in [('assessment', 'unknown'), ('open_dependencies', ['deployment']),
                             ('assessed_gate_version', 'old')]:
            with self.subTest(field=field):
                original = deepcopy(self.fixture.index['tasks']['t'])
                self.fixture.index['tasks']['t'][field] = value
                self.save()
                before = (self.fixture.data / 'index.json').read_bytes()
                self.assertEqual('no-op', self.run_writer()['status'])
                self.assertEqual(before, (self.fixture.data / 'index.json').read_bytes())
                self.fixture.index['tasks']['t'] = original

    def test_source_change_or_revocation_before_commit_blocks_write(self):
        before = (self.fixture.data / 'index.json').read_bytes()
        def change(stage):
            if stage == 'before-commit':
                (self.root / 'note.md').write_text('changed', encoding='utf-8')
        self.assertEqual('conflict', self.run_writer(fault=change)['status'])
        self.assertEqual(before, (self.fixture.data / 'index.json').read_bytes())
        self.assertFalse((self.fixture.data / 'archive-receipts').exists())

    def test_crash_recovers_without_second_task_revision(self):
        def crash(stage):
            if stage == 'after-index':
                raise RuntimeError('isolated interruption')
        with self.assertRaises(RuntimeError):
            self.run_writer(fault=crash)
        committed = (self.fixture.data / 'index.json').read_bytes()
        self.assertEqual('recovered', self.run_writer()['status'])
        self.assertEqual(committed, (self.fixture.data / 'index.json').read_bytes())
        self.assertEqual(2, cli.read_json(self.fixture.data / 'index.json')['tasks']['t']['revision'])

    def test_archive_process_exit_releases_lock_and_preserves_reader_recovery(self):
        code = '''
import os, sys
from pathlib import Path
from datetime import datetime, timezone
sys.path.insert(0, sys.argv[1])
from tidy_writer import archive_once
def stop(stage):
    if stage == 'after-index':
        os._exit(23)
archive_once(Path(sys.argv[2]), 'tasks', Path(sys.argv[3]), 'fixture-writer',
             Path(sys.argv[4]), now=datetime(2026, 10, 4, tzinfo=timezone.utc), fault=stop)
'''
        note = (self.root / 'note.md').read_bytes()
        run = subprocess.run([sys.executable, '-B', '-X', 'utf8', '-c', code,
                              str(Path(__file__).parents[1] / 'scripts'), str(self.root),
                              str(self.authority_path), str(self.gate)],
                             capture_output=True, timeout=15,
                             creationflags=(subprocess.CREATE_NO_WINDOW
                                            if sys.platform == 'win32' else 0))
        self.assertEqual(23, run.returncode, run.stderr.decode('utf-8'))
        committed = (self.fixture.data / 'index.json').read_bytes()
        self.assertFalse((self.fixture.data / 'archive-receipts').exists())
        self.assertEqual('recovered', self.run_writer()['status'])
        self.assertEqual(committed, (self.fixture.data / 'index.json').read_bytes())
        self.assertEqual('no-op', self.run_writer()['status'])
        self.assertEqual(2, cli.read_json(self.fixture.data / 'index.json')['tasks']['t']['revision'])
        self.assertEqual([], cli.load_view(self.root, 'tasks', 'g1')['active'])
        self.assertEqual(note, (self.root / 'note.md').read_bytes())

    def test_subprocess_readers_and_dry_run_follow_archive_restore_lifecycle(self):
        scripts = Path(__file__).parents[1] / 'scripts'
        gate_raw = (scripts / 'TASK_GATE_VERSION').read_bytes()
        gate = gate_raw.decode('utf-8').strip()
        self.gate.write_bytes(gate_raw)
        self.permission['gate_version'] = gate
        self.authority_path.write_text(json.dumps(self.permission), encoding='utf-8')
        self.fixture.index['gate_version'] = gate
        self.fixture.index['tasks']['t']['assessed_gate_version'] = gate
        unknown = deepcopy(self.fixture.index['tasks']['t'])
        unknown.update(task_id='u', state='unresolved', assessment='unknown')
        self.fixture.index['tasks']['u'] = unknown
        self.save()
        note = (self.root / 'note.md').read_bytes()

        def invoke(name):
            command = [sys.executable, '-B', '-X', 'utf8', str(scripts / name),
                       '--vault', str(self.root), '--data', 'tasks']
            if name == 'task_view_cli.py':
                command.extend(['--gate-version', gate])
            before = {p: p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
            result = subprocess.run(command, capture_output=True, timeout=15,
                                    creationflags=(subprocess.CREATE_NO_WINDOW
                                                   if sys.platform == 'win32' else 0))
            self.assertEqual(0, result.returncode, result.stderr.decode('utf-8'))
            self.assertEqual(before, {p: p.read_bytes() for p in self.root.rglob('*') if p.is_file()})
            return json.loads(result.stdout.decode('utf-8'))

        view = invoke('task_view_cli.py')
        self.assertEqual(['t'], [t['task_id'] for t in view['active']])
        self.assertEqual(['u'], [t['task_id'] for t in view['uncertain']])
        trial = invoke('tidy_dry_run.py')
        self.assertEqual('completion_candidate', trial['proposals'][0]['classification'])
        self.assertFalse(trial['write_authorized'])
        self.assertEqual('archived', self.run_writer()['status'])
        self.assertEqual([], invoke('task_view_cli.py')['active'])
        self.approve_restore()
        view = invoke('task_view_cli.py')
        self.assertTrue(view['active'][0]['restore_pending'])
        trial = invoke('tidy_dry_run.py')
        self.assertEqual('incomplete', trial['proposals'][0]['classification'])
        self.assertIn('restore-awaiting-integration', trial['proposals'][0]['reasons'])
        self.assertEqual('integrated', restore_once(
            self.root, 'tasks', self.authority_path, 'fixture-writer', self.gate, now=self.now)['status'])
        view = invoke('task_view_cli.py')
        self.assertEqual(['t'], [t['task_id'] for t in view['active']])
        self.assertEqual(['u'], [t['task_id'] for t in view['uncertain']])
        self.assertFalse(view['active'][0].get('restore_pending'))
        self.assertEqual('unknown', invoke('tidy_dry_run.py')['proposals'][0]['classification'])
        self.assertEqual('no-op', self.run_writer()['status'])
        self.assertEqual(note, (self.root / 'note.md').read_bytes())
        self.assertEqual(1, len(list((self.fixture.data / 'archive-receipts').glob('*.json'))))
        self.assertEqual(1, len(list((self.fixture.data / 'receipts').glob('*.json'))))

    def test_failed_replace_keeps_original_snapshot_and_no_success_receipt(self):
        before = (self.fixture.data / 'index.json').read_bytes()
        with patch('tidy_writer.os.replace', side_effect=OSError('fixture replace failure')):
            self.assertEqual('conflict', self.run_writer()['status'])
        self.assertEqual(before, (self.fixture.data / 'index.json').read_bytes())
        self.assertFalse((self.fixture.data / 'archive-receipts').exists())
        self.assertEqual('archived', self.run_writer()['status'])

    def test_corrupt_receipt_is_not_overwritten(self):
        self.run_writer()
        path = next((self.fixture.data / 'archive-receipts').glob('*.json'))
        path.write_text('{broken', encoding='utf-8')
        before = (self.fixture.data / 'index.json').read_bytes()
        self.assertEqual('conflict', self.run_writer()['status'])
        self.assertEqual(b'{broken', path.read_bytes())
        self.assertEqual(before, (self.fixture.data / 'index.json').read_bytes())

    def approve_restore(self):
        index = cli.read_json(self.fixture.data / 'index.json')
        request = deepcopy(self.fixture.request)
        request.update(base_index_revision=index['revision'],
                       base_task_revision=index['tasks']['t']['revision'])
        request['payload_digest'] = cli.digest(request, 'payload_digest')
        self.fixture.write('restore-requests/r.json', request)
        self.fixture.write('restore-approvals/a.json', {
            'schema_version': 1, 'approval_id': 'a', 'request_id': 'r', 'task_id': 't',
            'request_digest': request['payload_digest'], 'operation': 'restore',
            'approved_at': '2026-10-01T10:00:00+09:00',
            'source_ref': 'fixture:approved-restore', 'recorded_by': 'fixture-agent'})

    def test_pending_archive_receipt_blocks_restore_until_archive_recovery(self):
        def crash(stage):
            if stage == 'after-index':
                raise RuntimeError('fixture interruption')
        with self.assertRaises(RuntimeError):
            self.run_writer(fault=crash)
        self.approve_restore()
        committed = (self.fixture.data / 'index.json').read_bytes()
        result = restore_once(self.root, 'tasks', self.authority_path,
                              'fixture-writer', self.gate, now=self.now)
        self.assertEqual('conflict', result['status'])
        self.assertEqual(committed, (self.fixture.data / 'index.json').read_bytes())
        self.assertEqual('recovered', self.run_writer()['status'])
        result = restore_once(self.root, 'tasks', self.authority_path,
                              'fixture-writer', self.gate, now=self.now)
        self.assertEqual('integrated', result['status'])
        self.assertEqual(3, cli.read_json(self.fixture.data / 'index.json')['tasks']['t']['revision'])
        self.assertEqual('no-op', self.run_writer()['status'])

    def test_later_archive_does_not_replay_old_restore(self):
        self.run_writer()
        self.approve_restore()
        restore_once(self.root, 'tasks', self.authority_path,
                     'fixture-writer', self.gate, now=self.now)
        self.fixture.index = cli.read_json(self.fixture.data / 'index.json')
        self.fixture.index['tasks']['t'].update(assessment='confirmed',
                                                reason='Fixture new completion assessment')
        self.save()
        self.assertEqual('archived', self.run_writer()['status'])
        index = cli.read_json(self.fixture.data / 'index.json')
        self.assertEqual(4, index['tasks']['t']['revision'])
        self.assertEqual([], cli.load_view(self.root, 'tasks', 'g1')['active'])
        self.assertEqual(2, len(list((self.fixture.data / 'archive-receipts').glob('*.json'))))

    def test_revocation_or_new_restore_after_intent_blocks_commit(self):
        for mutation in ('revoked', 'restore'):
            with self.subTest(mutation=mutation):
                before = (self.fixture.data / 'index.json').read_bytes()
                def change(stage):
                    if stage == 'after-intent':
                        if mutation == 'revoked':
                            changed = dict(self.permission, revoked=True)
                            self.authority_path.write_text(json.dumps(changed), encoding='utf-8')
                        else:
                            self.fixture.write('restore-requests/new.json', self.fixture.request)
                self.assertEqual('conflict', self.run_writer(fault=change)['status'])
                self.assertEqual(before, (self.fixture.data / 'index.json').read_bytes())
                self.authority_path.write_text(json.dumps(self.permission), encoding='utf-8')
                self.assertFalse((self.fixture.data / 'archive-receipts').exists())

    def test_global_bad_record_blocks_write_not_successful_empty(self):
        self.fixture.write('restore-requests/broken.json', {})
        before = (self.fixture.data / 'index.json').read_bytes()
        self.assertEqual('unavailable', self.run_writer()['status'])
        self.assertEqual(before, (self.fixture.data / 'index.json').read_bytes())


if __name__ == '__main__':
    unittest.main()
