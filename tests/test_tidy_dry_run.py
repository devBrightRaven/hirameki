"""Read-only fixture integration, including the actual command-line interface."""
from pathlib import Path
from copy import deepcopy
import hashlib
import json
import subprocess
import sys
import unittest

import test_task_view_cli as reader_tests
import task_view_cli as cli
from tidy_dry_run import dry_run, read_gate


class DryRunTests(unittest.TestCase):
    def setUp(self):
        self.fixture = reader_tests.CliTests('test_request_without_record_unverified')
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.root = self.fixture.root
        self.gate = self.root / 'gate.txt'
        self.gate.write_text('g1\n', encoding='utf-8')
        task = self.fixture.index['tasks']['t']
        task['state'] = 'active'
        task['criteria'] = [{'criterion_id': 'c1', 'description': 'Fixture accepted',
                             'result': 'met', 'evidence_refs': ['e1']}]
        task['evidence'] = [{'evidence_id': 'e1', 'source_id': 'note.md#task',
                             'outcome': 'Acceptance recorded'}]
        self.save()

    def save(self):
        self.fixture.index['revision'] = cli.digest(self.fixture.index, 'revision')
        self.fixture.write('index.json', self.fixture.index)

    def snapshots(self):
        return {p.relative_to(self.root).as_posix(): p.read_bytes()
                for p in self.root.rglob('*') if p.is_file()}

    def semantic_source(self):
        """Concrete synthetic acceptance, not a claim of independent semantics."""
        content = ('# Synthetic fixture only\n## task\n'
                   'Task identity: t; scope: fixture.\n'
                   'Required: export exactly rows A,B,C and preserve the source.\n'
                   'Observed output: rows A,B,C; count=3; duplicates=0.\n'
                   'Source before and after SHA256: ' + 'a' * 64 + '.\n'
                   'Synthetic owner acceptance: all required checks passed; no deployment required.\n')
        note = self.root / 'note.md'
        note.write_text(content, encoding='utf-8', newline='\n')
        sha = hashlib.sha256(note.read_bytes()).hexdigest()
        task = self.fixture.index['tasks']['t']
        task['sources'][0].update(raw_sha256=sha, lf_sha256=sha)
        task['criteria'][0].update(description='Export A,B,C, no duplicates, preserve source')
        task['evidence'][0].update(outcome='Observed A,B,C, count 3, duplicates 0; source unchanged')
        self.save()

    def test_A1_concrete_acceptance_is_only_readonly_structural_proposal(self):
        self.semantic_source()
        before = self.snapshots()
        report = dry_run(self.root, 'tasks', self.gate)
        proposal = report['proposals'][0]
        self.assertEqual('completion_candidate', proposal['classification'])
        self.assertEqual('assessor-declaration-only', proposal['semantic_verification'])
        self.assertFalse(report['write_authorized'])
        self.assertEqual(before, self.snapshots())

    def test_A3_stale_acceptance_blocks_proposal_even_with_preserved_mtime(self):
        import os
        self.semantic_source()
        note = self.root / 'note.md'
        stat = note.stat()
        note.write_text(note.read_text(encoding='utf-8').replace('count=3', 'count=2'), encoding='utf-8')
        os.utime(note, ns=(stat.st_atime_ns, stat.st_mtime_ns))
        before = self.snapshots()
        report = dry_run(self.root, 'tasks', self.gate)
        self.assertNotEqual('completion_candidate', report['proposals'][0]['classification'])
        self.assertEqual(before, self.snapshots())

    def test_E1_sync_conflict_path_visible_without_losing_normal_task(self):
        self.semantic_source()
        self.fixture.write('restore-requests/r.sync-conflict-20261009.json', self.fixture.request)
        before = self.snapshots()
        report = dry_run(self.root, 'tasks', self.gate)
        self.assertIn('t', [p['task_id'] for p in report['proposals']])
        self.assertTrue(any(e['reason'] == 'sync-conflict-copy' and
                            e['path'] == 'tasks/restore-requests/r.sync-conflict-20261009.json'
                            for e in report['exceptions']))
        self.assertNotEqual('completion_candidate', report['proposals'][0]['classification'])
        self.assertEqual(before, self.snapshots())

    def test_E2_gate_change_invalidates_archived_assessment_readonly(self):
        self.semantic_source()
        self.fixture.index['tasks']['t']['state'] = 'archived'
        self.save()
        self.gate.write_text('g2\n', encoding='utf-8')
        before = self.snapshots()
        report = dry_run(self.root, 'tasks', self.gate)
        self.assertEqual([], report['proposals'])
        self.assertEqual(['t'], [t['task_id'] for t in report['uncertain']])
        self.assertTrue(any('gate-unverified' in e.get('gate_reasons', [])
                            for e in report['exceptions']))
        self.assertEqual(before, self.snapshots())

    def test_E3_public_pagination_rejects_index_and_source_mutation(self):
        self.semantic_source()
        def query(*extra):
            run = subprocess.run([sys.executable, '-B', '-X', 'utf8', cli.__file__,
                                  '--vault', str(self.root), '--data', 'tasks',
                                  '--gate-version', 'g1', '--page-size', '1', *extra],
                                 capture_output=True, text=True, encoding='utf-8', timeout=15)
            return run, json.loads(run.stdout)
        for mutation, reason in [('index', 'page-index-revision-changed'),
                                 ('source', 'page-effective-view-changed')]:
            with self.subTest(mutation=mutation):
                self.semantic_source()
                run, first = query()
                self.assertEqual(0, run.returncode)
                if mutation == 'index':
                    self.fixture.index['tasks']['t']['summary'] = 'Changed revision'
                    self.save()
                else:
                    (self.root / 'note.md').write_text('Changed after page one', encoding='utf-8')
                before = self.snapshots()
                run, second = query('--offset', '1', '--expected-revision', first['index_revision'],
                                    '--expected-view-revision', first['view_revision'])
                self.assertNotEqual(0, run.returncode)
                self.assertEqual('unavailable', second['view_status'])
                self.assertTrue(any(e['reason'] == reason for e in second['exceptions']))
                self.assertEqual(before, self.snapshots())

    def test_complete_proposal_is_read_only(self):
        before = self.snapshots()
        report = dry_run(self.root, 'tasks', self.gate)
        self.assertEqual('completion_candidate', report['proposals'][0]['classification'])
        self.assertFalse(report['write_authorized'])
        self.assertEqual(before, self.snapshots())

    def test_semantic_and_malformed_exceptions_keep_actual_paths(self):
        task = self.fixture.index['tasks']['t']
        task.update(state='archived', assessment='unknown')
        self.save()
        self.fixture.write('restore-requests/bad.json', {})
        before = self.snapshots()
        report = dry_run(self.root, 'tasks', self.gate)
        self.assertTrue(any(e.get('path') == 'tasks/restore-requests/bad.json'
                            for e in report['exceptions']))
        semantic = [e for e in report['exceptions'] if e.get('task_id') == 't']
        self.assertTrue(semantic)
        self.assertTrue(all(e['path'] == 'note.md' for e in semantic))
        self.assertTrue(all(e['source_paths'] == ['note.md'] for e in semantic))
        self.assertEqual(before, self.snapshots())

    def test_large_index_uses_shared_snapshot_budget_and_remains_read_only(self):
        template = self.fixture.index['tasks']['t']
        self.fixture.index['tasks'] = {}
        for number in range(3668):
            task = deepcopy(template)
            task['task_id'] = f't-{number}'
            self.fixture.index['tasks'][task['task_id']] = task
        self.save()
        self.assertGreater((self.fixture.data / 'index.json').stat().st_size,
                           cli.RECORD_BYTE_LIMIT)
        before = self.snapshots()
        report = dry_run(self.root, 'tasks', self.gate)
        self.assertEqual(3668, len(report['proposals']))
        self.assertTrue(all(item['classification'] == 'completion_candidate'
                            for item in report['proposals']))
        self.assertFalse(report['write_authorized'])
        self.assertEqual(before, self.snapshots())

    def test_missing_empty_multiline_gate_stops(self):
        for content in ('', '\n', 'g1\ng2\n', 'g1\n\n', ' g1\n'):
            with self.subTest(content=content):
                self.gate.write_text(content, encoding='utf-8')
                with self.assertRaises(ValueError):
                    read_gate(self.gate)
        self.gate.unlink()
        with self.assertRaises(OSError):
            read_gate(self.gate)

    def test_changed_source_cannot_be_proposed_complete(self):
        (self.root / 'note.md').write_text('changed', encoding='utf-8')
        report = dry_run(self.root, 'tasks', self.gate)
        self.assertEqual('unknown', report['proposals'][0]['classification'])

    def test_unresolved_history_is_not_an_archival_candidate(self):
        self.fixture.index['tasks']['t'].update(state='unresolved', assessment='unknown')
        self.save()
        before = self.snapshots()
        report = dry_run(self.root, 'tasks', self.gate)
        self.assertEqual([], report['proposals'])
        self.assertEqual('unresolved', report['uncertain'][0]['state'])
        self.assertEqual([], report['exceptions'])
        self.assertEqual(before, self.snapshots())

    def test_unresolved_item_does_not_block_unrelated_completion_proposal(self):
        unknown = deepcopy(self.fixture.index['tasks']['t'])
        unknown.update(task_id='u', state='unresolved', assessment='unknown')
        self.fixture.index['tasks']['u'] = unknown
        self.save()
        before = self.snapshots()
        report = dry_run(self.root, 'tasks', self.gate)
        self.assertEqual(['t'], [p['task_id'] for p in report['proposals']])
        self.assertEqual('completion_candidate', report['proposals'][0]['classification'])
        self.assertEqual(['u'], [t['task_id'] for t in report['uncertain']])
        self.assertFalse(report['write_authorized'])
        self.assertEqual(before, self.snapshots())

    def test_broken_archive_is_visible_separately(self):
        self.fixture.index['tasks']['t']['state'] = 'archived'
        self.fixture.index['tasks']['t']['criteria'] = []
        self.save()
        report = dry_run(self.root, 'tasks', self.gate)
        self.assertEqual([], report['proposals'])
        self.assertEqual('t', report['uncertain'][0]['task_id'])
        self.assertEqual('partial', report['view_status'])

    def test_unidentified_broken_record_blocks_completion_proposals(self):
        folder = self.fixture.data / 'restore-requests'
        folder.mkdir()
        (folder / 'broken.json').write_text('{', encoding='utf-8')
        report = dry_run(self.root, 'tasks', self.gate)
        self.assertEqual('unknown', report['proposals'][0]['classification'])

    def test_pending_restore_is_not_rearchived(self):
        self.fixture.index['tasks']['t']['state'] = 'archived'
        self.save()
        self.fixture.write('restore-requests/r.json', self.fixture.request)
        self.fixture.write('restore-approvals/a.json', {
            'schema_version': 1, 'approval_id': 'a', 'request_id': 'r', 'task_id': 't',
            'request_digest': self.fixture.request['payload_digest'], 'operation': 'restore',
            'approved_at': '2026-10-01T10:00:00+09:00',
            'source_ref': 'fixture:approval', 'recorded_by': 'fixture-agent'})
        report = dry_run(self.root, 'tasks', self.gate)
        self.assertEqual('incomplete', report['proposals'][0]['classification'])
        self.assertEqual(['restore-awaiting-integration'], report['proposals'][0]['reasons'])

    def test_real_cli_reads_shared_gate_and_never_writes(self):
        shared = Path(__file__).parents[1] / 'scripts' / 'TASK_GATE_VERSION'
        version, gate_hash = read_gate(shared)
        self.fixture.index['gate_version'] = version
        self.fixture.index['tasks']['t']['assessed_gate_version'] = version
        self.save()
        before = self.snapshots()
        run = subprocess.run([sys.executable, '-B', '-X', 'utf8',
                              str(shared.with_name('tidy_dry_run.py')),
                              '--vault', str(self.root), '--data', 'tasks'],
                             capture_output=True, text=True, encoding='utf-8', timeout=20,
                             creationflags=(subprocess.CREATE_NO_WINDOW
                                            if sys.platform == 'win32' else 0))
        self.assertEqual(0, run.returncode, run.stderr)
        report = json.loads(run.stdout)
        self.assertEqual(version, report['gate_version'])
        self.assertEqual(gate_hash, report['gate_source_sha256'])
        self.assertFalse(report['write_authorized'])
        self.assertEqual(before, self.snapshots())


if __name__ == '__main__':
    unittest.main()
