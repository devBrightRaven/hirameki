import importlib.util
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import subprocess
import os
import unittest
from copy import deepcopy
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))
import task_view_cli as cli
import task_restore_contract as restore


class CliTests(unittest.TestCase):
    def pair(self):
        return {'request': deepcopy(self.request), 'approval_record': {
            'schema_version': 1, 'approval_id': 'a', 'request_id': 'r', 'task_id': 't',
            'request_digest': self.request['payload_digest'], 'operation': 'restore',
            'approved_at': '2026-10-01T10:00:00+09:00', 'source_ref': 'fixture:request',
            'recorded_by': 'synthetic-harness'}}

    def pair_command(self, pair):
        process = subprocess.run([sys.executable, '-B', '-X', 'utf8', cli.__file__,
                                  '--validate-restore'], input=json.dumps(pair, ensure_ascii=False),
                                 text=True, encoding='utf-8', capture_output=True, timeout=15)
        return process, json.loads(process.stdout)

    def test_public_restore_schema_is_the_actual_validator_schema(self):
        process = subprocess.run([sys.executable, '-B', '-X', 'utf8', cli.__file__,
                                  '--restore-contract'], text=True, encoding='utf-8',
                                 capture_output=True, timeout=15)
        self.assertEqual(0, process.returncode)
        contract = json.loads(process.stdout)
        self.assertEqual(restore.REQUEST_SCHEMA, contract['schemas']['request'])
        self.assertEqual(restore.APPROVAL_SCHEMA, contract['schemas']['approval_record'])
        self.assertLess(len(process.stdout.encode('utf-8')), 16384)
        self.assertTrue(contract['read_only'])

    def test_public_restore_pair_validates_without_writes_or_human_claim(self):
        before = {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        process, result = self.pair_command(self.pair())
        self.assertEqual(0, process.returncode)
        self.assertTrue(result['valid'])
        self.assertFalse(result['human_utterance_proven'])
        self.assertFalse(result['source_checks_performed'])
        self.assertEqual(before, {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()})

    def test_every_published_required_field_is_enforced_by_reader_validator(self):
        pair = self.pair()
        for name, schema in [('request', restore.REQUEST_SCHEMA), ('approval_record', restore.APPROVAL_SCHEMA)]:
            for field in schema['required']:
                with self.subTest(record=name, field=field):
                    invalid = deepcopy(pair)
                    del invalid[name][field]
                    self.assertTrue(restore.pair_errors(invalid['request'], invalid['approval_record']))
        for field in restore.REQUEST_SCHEMA['properties']['approval']['required']:
            invalid = deepcopy(pair);del invalid['request']['approval'][field]
            self.assertTrue(restore.pair_errors(invalid['request'], invalid['approval_record']))

    def test_public_pair_digest_and_binding_errors_are_explicit(self):
        for change in ('tampered-payload', 'mismatched-approval', 'boolean-version', 'invalid-offset'):
            with self.subTest(change=change):
                pair = self.pair()
                if change == 'tampered-payload': pair['request']['reason'] = 'changed'
                if change == 'mismatched-approval': pair['approval_record']['request_digest'] = '0' * 64
                if change == 'boolean-version': pair['request']['schema_version'] = True
                if change == 'invalid-offset': pair['approval_record']['approved_at'] = '2026-10-01'
                process, result = self.pair_command(pair)
                self.assertEqual(1, process.returncode)
                self.assertFalse(result['valid']);self.assertTrue(result['errors'])

    def test_canonical_digest_includes_unicode_and_extensions_not_file_formatting(self):
        request = deepcopy(self.request);request['reason'] = '重新開啟 日本語';request['extra'] = 'extension'
        request['payload_digest'] = restore.digest(request, 'payload_digest')
        self.assertTrue(restore.request_valid(request))
        self.assertEqual(request['payload_digest'], hashlib.sha256(json.dumps(
            {k: v for k, v in request.items() if k != 'payload_digest'},
            sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False
        ).encode('utf-8')).hexdigest())
        self.assertNotEqual(request['payload_digest'], hashlib.sha256(json.dumps(request, indent=2).encode()).hexdigest())

    def test_public_contract_output_limit_is_explicit(self):
        process = subprocess.run([sys.executable, '-B', '-X', 'utf8', cli.__file__,
                                  '--restore-contract', '--max-output-bytes', '1024'],
                                 text=True, encoding='utf-8', capture_output=True, timeout=15)
        self.assertEqual(1, process.returncode)
        self.assertEqual('output-limit-exceeded', json.loads(process.stdout)['query_status'])

    def test_global_cancellation_blocker_is_exposed_before_restore(self):
        self.write('approval-cancellations/bad.json', {'schema_version': 1})
        _, output = self.query_command('t')
        self.assertFalse(output['global_validation']['restore_matching_available'])
        self.assertTrue(output['exceptions'])

    def query_command(self, task_id, *extra):
        run = subprocess.run([sys.executable, '-B', '-X', 'utf8', str(Path(cli.__file__)),
                              '--vault', str(self.root), '--data', 'tasks', '--gate-version', 'g1',
                              '--task-id', task_id, *extra], capture_output=True, text=True,
                             encoding='utf-8', timeout=15)
        return run, json.loads(run.stdout)

    def test_task_query_archived_retains_complete_sources_without_writes(self):
        before = {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        run, output = self.query_command('t')
        self.assertEqual(0, run.returncode)
        self.assertEqual('archived', output['task']['state'])
        self.assertEqual(self.index['revision'], output['index_revision'])
        self.assertEqual('verified', output['validation']['status'])
        self.assertTrue(output['validation']['sources_match'])
        self.assertEqual(before, {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()})

    def test_task_query_unknown_is_nonzero_with_global_validation(self):
        run, output = self.query_command('missing')
        self.assertEqual(1, run.returncode)
        self.assertEqual('task-not-found', output['query_status'])
        self.assertIsNone(output['task'])
        self.assertTrue(output['global_validation']['full_index_checked'])

    def test_task_query_changed_source_is_unverified(self):
        (self.root / 'note.md').write_text('changed evidence', encoding='utf-8')
        _, output = self.query_command('t')
        self.assertEqual('unverified', output['validation']['status'])
        self.assertFalse(output['validation']['sources_match'])
        self.assertEqual('partial', output['view_status'])
        self.assertTrue(output['exceptions'])

    def test_task_query_preserves_unrelated_broken_record(self):
        (self.data / 'restore-requests').mkdir()
        (self.data / 'restore-requests/broken.json').write_text('{bad', encoding='utf-8')
        _, output = self.query_command('t')
        self.assertEqual('partial', output['view_status'])
        self.assertEqual('verified', output['validation']['status'])
        self.assertTrue(any(e.get('path', '').endswith('broken.json') for e in output['exceptions']))
        run, absent = self.query_command('missing')
        self.assertEqual(1, run.returncode)
        self.assertEqual(output['exceptions'], absent['exceptions'])

    def test_task_query_does_not_bypass_bad_index_digest(self):
        self.index['writer'] = 'changed-without-new-revision'
        self.write('index.json', self.index)
        run, output = self.query_command('t')
        self.assertEqual(1, run.returncode)
        self.assertEqual('unavailable', output['view_status'])
        self.assertNotIn('task', output)

    def test_task_query_oversize_is_explicit_not_truncated(self):
        self.index['tasks']['t']['summary'] = '大型' * 6000
        self.index['revision'] = cli.digest(self.index, 'revision')
        self.write('index.json', self.index)
        run, output = self.query_command('t')
        self.assertEqual(1, run.returncode)
        self.assertEqual('output-limit-exceeded', output['query_status'])
        self.assertGreater(output['required_bytes'], output['max_output_bytes'])
        self.assertFalse(output['details_returned'])
        self.assertLess(len(run.stdout.encode('utf-8')), 1024)

    def test_task_query_global_diagnostics_oversize_is_explicit(self):
        folder = self.data / 'restore-requests'
        folder.mkdir()
        for n in range(20):
            (folder / ('broken-' + str(n) + '.json')).write_text('{bad', encoding='utf-8')
        run, output = self.query_command('t', '--max-output-bytes', '1024')
        self.assertEqual(1, run.returncode)
        self.assertEqual('output-limit-exceeded', output['query_status'])
        self.assertEqual(20, output['global_validation']['exception_count'])

    def test_task_query_retains_restore_overlay_and_matching_approval_refs(self):
        self.write('restore-requests/r.json', self.request)
        self.write('restore-approvals/a.json', {
            'schema_version': 1, 'approval_id': 'a', 'request_id': 'r', 'task_id': 't',
            'request_digest': self.request['payload_digest'], 'operation': 'restore',
            'approved_at': '2026-10-01T10:00:00+09:00', 'source_ref': 'fixture:request',
            'recorded_by': 'fixture-agent'})
        run, output = self.query_command('t')
        self.assertEqual(0, run.returncode)
        self.assertTrue(output['task']['restore_pending'])
        self.assertEqual(['r'], output['task']['pending_requests'])
        self.assertIn('r', output['task']['restore_approval_refs'])

    def test_task_query_revision_tokens_match_full_validated_view(self):
        full = cli.load_view(self.root, 'tasks', 'g1')
        query = cli.load_view(self.root, 'tasks', 'g1', task_id='t')
        self.assertEqual(full['view_revision'], query['view_revision'])
        self.assertEqual(full['index_revision'], query['index_revision'])

    def test_task_query_existing_large_R3_fixture_is_bounded_without_reduction(self):
        configured = os.environ.get('HIRAMEKI_R3_FIXTURE')
        if not configured:
            self.skipTest('Local persistent synthetic fixture not installed on this host')
        fixture = Path(configured)
        before = {str(p): p.read_bytes() for p in fixture.rglob('*') if p.is_file()}
        run = subprocess.run([sys.executable, '-B', '-X', 'utf8', str(Path(cli.__file__)),
                              '--vault', str(fixture), '--data', 'research/tidy/tasks',
                              '--gate-version', 'tidy-task-gate-v2', '--task-id', 'arch'],
                             capture_output=True, text=True, encoding='utf-8', timeout=15)
        output = json.loads(run.stdout)
        self.assertEqual(0, run.returncode)
        self.assertEqual('archived', output['task']['state'])
        self.assertTrue(output['validation']['sources_match'])
        self.assertLess(len(run.stdout.encode('utf-8')), 16384)
        self.assertGreater(len(before[str(fixture / 'research/tidy/tasks/index.json')]), 40000)
        self.assertTrue(output['exceptions'])
        self.assertEqual(before, {str(p): p.read_bytes() for p in fixture.rglob('*') if p.is_file()})

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.data = self.root / 'tasks'
        self.data.mkdir()
        (self.root / 'note.md').write_text('evidence', encoding='utf-8')
        raw_hash = hashlib.sha256((self.root / 'note.md').read_bytes()).hexdigest()
        self.index = {'schema_version': 1, 'parent_revision': None,
                      'gate_version': 'g1', 'writer': 'fixture-writer', 'applied_requests': {},
                      'tasks': {'t': {'task_id': 't', 'revision': 1, 'state': 'archived',
                                      'scope': 'fixture', 'summary': 'fixture task',
                                      'criteria': [{'criterion_id': 'c1',
                                                    'description': 'Fixture task completed',
                                                    'result': 'met', 'evidence_refs': ['e1']}],
                                      'evidence': [{'evidence_id': 'e1',
                                                    'source_id': 'note.md#task',
                                                    'outcome': 'Fixture acceptance'}],
                                      'open_dependencies': [],
                                      'reason': 'fixture completion', 'operation_id': 'genesis',
                                      'previous_revision': None,
                                      'assessment': 'confirmed', 'assessed_gate_version': 'g1',
                                      'sources': [{'path': 'note.md', 'anchor': 'task',
                                                   'raw_sha256': raw_hash, 'lf_sha256': raw_hash}]}}}
        self.index['revision'] = cli.digest(self.index, 'revision')
        self.write('index.json', self.index)
        self.request = {'schema_version': 1, 'request_id': 'r', 'task_id': 't',
                        'base_index_revision': self.index['revision'], 'base_task_revision': 1,
                        'base_source_digests': {'note.md#task': raw_hash},
                        'reason': 'new requirement', 'reason_kind': 'scope_changed',
                        'created': '2026-10-01T10:00:00+09:00',
                        'approval': {'source_ref': 'fixture:request', 'approving_user': 'fixture-user',
                                     'operation': 'restore', 'scope': 't'}}
        self.request['payload_digest'] = cli.digest(self.request, 'payload_digest')

    def write(self, relative, value):
        path = self.data / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding='utf-8')

    def test_request_without_record_unverified(self):
        self.write('restore-requests/r.json', self.request)
        result = cli.load_view(self.root, 'tasks', 'g1')
        self.assertFalse(result['active'])
        self.assertTrue(result['uncertain'])

    def test_unresolved_history_uses_same_snapshot_without_completion_claim(self):
        self.index['tasks']['t'].update(state='unresolved', assessment='unknown',
                                       criteria=['Historical criterion, not completion proof'],
                                       evidence=[], reason='Original status not established')
        active = deepcopy(self.index['tasks']['t'])
        active.update(task_id='a', state='active', summary='Confirmed unfinished work')
        self.index['tasks']['a'] = active
        self.index['revision'] = cli.digest(self.index, 'revision')
        self.write('index.json', self.index)
        before = (self.data / 'index.json').read_bytes()
        result = cli.load_view(self.root, 'tasks', 'g1')
        self.assertEqual(['a'], [t['task_id'] for t in result['active']])
        self.assertEqual(['t'], [t['task_id'] for t in result['uncertain']])
        self.assertEqual('unresolved', result['uncertain'][0]['state'])
        self.assertEqual([], result['exceptions'])
        self.assertEqual('complete', result['view_status'])

    def test_historical_context_remains_visible_without_becoming_actionable(self):
        task = self.index['tasks']['t']
        task.update(state='unresolved', assessment='unknown',
                    summary='歷史決策脈絡（非待辦）：不安裝額外工具',
                    historical_record_kind='context',
                    historical_actionability='non-task-context',
                    execution_authority='none')
        self.index['revision'] = cli.digest(self.index, 'revision')
        self.write('index.json', self.index)
        before = (self.data / 'index.json').read_bytes()
        view = cli.load_view(self.root, 'tasks', 'g1')
        self.assertEqual([], view['active'])
        self.assertEqual('context', view['uncertain'][0]['historical_record_kind'])
        self.assertEqual('non-task-context', view['uncertain'][0]['historical_actionability'])
        self.assertEqual('none', view['uncertain'][0]['execution_authority'])
        self.assertIn('非待辦', view['uncertain'][0]['summary'])
        self.assertEqual(before, (self.data / 'index.json').read_bytes())
        self.assertEqual(before, (self.data / 'index.json').read_bytes())

    def test_unresolved_record_with_confirmed_assessment_is_rejected_visibly(self):
        self.index['tasks']['t']['state'] = 'unresolved'
        self.index['revision'] = cli.digest(self.index, 'revision')
        self.write('index.json', self.index)
        result = cli.load_view(self.root, 'tasks', 'g1')
        self.assertFalse(result['active'])
        self.assertTrue(result['uncertain'])
        self.assertIn('invalid-task-contract', [e['reason'] for e in result['exceptions']])

    def test_incomplete_archive_baseline_remains_visible(self):
        for field, value in (('criteria', []), ('evidence', []),
                             ('criteria', ['   ']), ('evidence', [None]),
                             ('criteria', [{}]), ('evidence', [{'source_ref': ''}]),
                             ('open_dependencies', ['waiting for acceptance'])):
            with self.subTest(field=field):
                original = self.index['tasks']['t'][field]
                self.index['tasks']['t'][field] = value
                self.index['revision'] = cli.digest(self.index, 'revision')
                self.write('index.json', self.index)
                result = cli.load_view(self.root, 'tasks', 'g1')
                self.assertEqual(['t'], [t['task_id'] for t in result['uncertain']])
                self.assertTrue(any(e['reason'] == 'incomplete-archive-baseline'
                                    for e in result['exceptions']))
                self.assertFalse(result['active'])
                self.index['tasks']['t'][field] = original

    def test_descriptive_structured_archive_baseline_is_supported(self):
        self.index['tasks']['t']['criteria'][0]['description'] = 'Structured fixture completed'
        self.index['tasks']['t']['evidence'][0]['outcome'] = 'Structured fixture acceptance'
        self.index['revision'] = cli.digest(self.index, 'revision')
        self.write('index.json', self.index)
        result = cli.load_view(self.root, 'tasks', 'g1')
        self.assertEqual([], result['uncertain'])
        self.assertEqual([], result['exceptions'])

    def test_archived_unmet_criterion_remains_visible(self):
        self.index['tasks']['t']['criteria'] = [
            {'criterion_id': 'c1', 'description': 'Deployment accepted',
             'result': 'unmet', 'evidence_refs': ['e1']}]
        self.index['tasks']['t']['evidence'] = [
            {'evidence_id': 'e1', 'source_id': 'note.md#task',
             'outcome': 'Source ready but deployment pending'}]
        self.index['revision'] = cli.digest(self.index, 'revision')
        self.write('index.json', self.index)
        result = cli.load_view(self.root, 'tasks', 'g1')
        self.assertEqual(['t'], [t['task_id'] for t in result['uncertain']])
        self.assertTrue(any(e['reason'] == 'archive-completion-unverified'
                            for e in result['exceptions']))

    def test_legacy_archive_prose_is_not_verified_completion(self):
        self.index['tasks']['t']['criteria'] = ['Completed']
        self.index['revision'] = cli.digest(self.index, 'revision')
        self.write('index.json', self.index)
        result = cli.load_view(self.root, 'tasks', 'g1')
        self.assertEqual(['t'], [t['task_id'] for t in result['uncertain']])
        self.assertFalse(result['active'])

    def test_snapshot_requires_declared_writer_and_gate(self):
        for field in ('writer', 'gate_version', 'parent_revision'):
            with self.subTest(field=field):
                index = dict(self.index)
                del index[field]
                index['revision'] = cli.digest(index, 'revision')
                self.write('index.json', index)
                with self.assertRaises(ValueError):
                    cli.load_view(self.root, 'tasks', 'g1')

    def test_malformed_task_contract_is_visible_not_archived_silently(self):
        self.index['tasks']['t']['criteria'] = 'not-a-list'
        self.index['revision'] = cli.digest(self.index, 'revision')
        self.write('index.json', self.index)
        result = cli.load_view(self.root, 'tasks', 'g1')
        self.assertEqual('partial', result['view_status'])
        self.assertTrue(any(e.get('reason') == 'invalid-task-contract'
                            for e in result['exceptions']))
        self.assertEqual('t', result['uncertain'][0]['task_id'])

    def test_missing_normalized_source_digest_is_not_silent_archive(self):
        del self.index['tasks']['t']['sources'][0]['lf_sha256']
        self.index['revision'] = cli.digest(self.index, 'revision')
        self.write('index.json', self.index)
        result = cli.load_view(self.root, 'tasks', 'g1')
        self.assertEqual('partial', result['view_status'])
        self.assertTrue(result['uncertain'])

    def test_invalid_task_revision_does_not_hide_other_active_task(self):
        self.make_active()
        malformed = dict(self.index['tasks']['t'], task_id='bad', revision='two',
                         previous_revision=1)
        self.index['tasks']['bad'] = malformed
        self.index['revision'] = cli.digest(self.index, 'revision')
        self.write('index.json', self.index)
        result = cli.load_view(self.root, 'tasks', 'g1')
        self.assertEqual(['t'], [task['task_id'] for task in result['active']])
        self.assertTrue(any(task['task_id'] == 'bad' for task in result['uncertain']))

    def test_matching_record_restores_without_writes(self):
        self.write('restore-requests/r.json', self.request)
        self.write('restore-approvals/a.json', {'schema_version': 1, 'approval_id': 'a',
                   'request_id': 'r', 'task_id': 't', 'request_digest': self.request['payload_digest'],
                   'operation': 'restore', 'approved_at': '2026-10-01T10:00:00+09:00', 'source_ref': 'session:event', 'recorded_by': 'agent'})
        before = {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertTrue(cli.load_view(self.root, 'tasks', 'g1')['active'])
        self.assertEqual(before, {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()})

    def test_modified_request_digest_rejected(self):
        self.request['reason'] = 'tampered'
        self.write('restore-requests/r.json', self.request)
        result = cli.load_view(self.root, 'tasks', 'g1')
        self.assertTrue(result['exceptions'])
        self.assertFalse(result['active'])

    def make_active(self):
        self.index['tasks']['t'].update(state='active', assessment='unknown')
        self.index['revision'] = cli.digest(self.index, 'revision')
        self.write('index.json', self.index)

    def test_bad_json_does_not_clear_valid_active(self):
        self.make_active()
        path = self.data / 'restore-requests/bad.json'
        path.parent.mkdir()
        path.write_text('{broken', encoding='utf-8')
        result = cli.load_view(self.root, 'tasks', 'g1')
        self.assertEqual(1, len(result['active']))
        self.assertTrue(any(item.get('path') == 'tasks/restore-requests/bad.json' for item in result['exceptions']))

    def test_conflict_copy_is_not_official_request(self):
        self.write('restore-requests/r.sync-conflict-date-id.json', self.request)
        result = cli.load_view(self.root, 'tasks', 'g1')
        self.assertFalse(result['active'])
        self.assertTrue(any(item['reason'] == 'sync-conflict-copy' for item in result['exceptions']))
        self.assertTrue(result['uncertain'])

    def test_bad_schema_does_not_clear_valid_active(self):
        self.make_active()
        invalid = dict(self.request, request_id={})
        self.write('restore-requests/bad.json', invalid)
        result = cli.load_view(self.root, 'tasks', 'g1')
        self.assertEqual(1, len(result['active']))
        self.assertTrue(result['exceptions'])

    def test_record_budget_does_not_clear_active(self):
        self.make_active()
        for i in range(2001):
            self.write(f'restore-approvals/{i}.json', {'schema_version': 1})
        result = cli.load_view(self.root, 'tasks', 'g1')
        self.assertTrue(result['active'])
        self.assertTrue(any(item['reason'] == 'record-budget' for item in result['exceptions']))

    def test_index_digest_rejected(self):
        self.index['tasks']['t']['state'] = 'active'
        self.write('index.json', self.index)
        with self.assertRaises(ValueError):
            cli.load_view(self.root, 'tasks', 'g1')

    def test_historical_sized_index_keeps_every_task_visible(self):
        self.make_active()
        template = self.index['tasks']['t']
        self.index['tasks'] = {}
        for number in range(3668):
            task = deepcopy(template)
            task['task_id'] = f'historical-{number}'
            self.index['tasks'][task['task_id']] = task
        self.index['revision'] = cli.digest(self.index, 'revision')
        self.write('index.json', self.index)
        self.assertGreater((self.data / 'index.json').stat().st_size, 1048576)
        result = cli.load_view(self.root, 'tasks', 'g1')
        self.assertEqual(3668, len(result['active']))
        self.assertEqual([], result['exceptions'])

    def test_oversized_snapshot_is_unavailable_not_truncated(self):
        self.index['padding'] = 'x' * cli.INDEX_BYTE_LIMIT
        self.index['revision'] = cli.digest(self.index, 'revision')
        self.write('index.json', self.index)
        with self.assertRaisesRegex(ValueError, 'file-budget'):
            cli.load_view(self.root, 'tasks', 'g1')

    def test_auxiliary_record_budget_is_not_raised_with_snapshot_budget(self):
        self.write('restore-requests/large.json', {'schema_version': 1, 'padding': 'x' * 1048576})
        with self.assertRaisesRegex(ValueError, 'file-budget'):
            cli.read_json(self.data / 'restore-requests/large.json')

    def test_shared_source_is_hashed_once_per_view_and_refreshed_next_view(self):
        self.make_active()
        self.index['tasks']['u'] = deepcopy(self.index['tasks']['t'])
        self.index['tasks']['u']['task_id'] = 'u'
        self.index['revision'] = cli.digest(self.index, 'revision')
        self.write('index.json', self.index)
        original_open = Path.open
        reads = []

        def observe(path, *args, **kwargs):
            if path == self.root / 'note.md' and args and args[0] == 'rb':
                reads.append(path)
            return original_open(path, *args, **kwargs)

        with patch.object(Path, 'open', observe):
            first = cli.load_view(self.root, 'tasks', 'g1')
        self.assertEqual(1, len(reads))
        self.assertFalse(any(task.get('source_changed') for task in first['active']))
        (self.root / 'note.md').write_text('changed source', encoding='utf-8')
        reads.clear()
        with patch.object(Path, 'open', observe):
            second = cli.load_view(self.root, 'tasks', 'g1')
        self.assertEqual(1, len(reads))
        self.assertTrue(all(task['source_changed'] for task in second['active']))

    def test_snapshot_task_count_is_bounded_before_projection(self):
        self.index['tasks'] = {str(number): {} for number in range(10001)}
        self.index['revision'] = cli.digest(self.index, 'revision')
        self.write('index.json', self.index)
        with self.assertRaisesRegex(ValueError, 'task-budget'):
            cli.load_view(self.root, 'tasks', 'g1')

    def test_malformed_applied_entry_is_invalid_index(self):
        self.index['applied_requests']['r'] = 'not-a-record'
        self.index['revision'] = cli.digest(self.index, 'revision')
        self.write('index.json', self.index)
        self.write('restore-requests/r.json', self.request)
        with self.assertRaises(ValueError):
            cli.load_view(self.root, 'tasks', 'g1')

    def test_truthy_nontext_approval_is_not_consent_evidence(self):
        self.write('restore-requests/r.json', self.request)
        self.write('restore-approvals/a.json', {'schema_version': 1, 'approval_id': 'a',
                   'request_id': 'r', 'task_id': 't', 'request_digest': self.request['payload_digest'],
                   'operation': 'restore', 'approved_at': '2026-10-01T10:00:00+09:00', 'source_ref': {'pretend': 'evidence'},
                   'recorded_by': 'agent'})
        result = cli.load_view(self.root, 'tasks', 'g1')
        self.assertFalse(result['active'])
        self.assertTrue(any(item.get('reason') == 'invalid-approval' for item in result['exceptions']))

    def test_parent_escape_rejected(self):
        with self.assertRaises(ValueError):
            cli.load_view(self.root, '../tasks', 'g1')

    def test_changed_source_visible(self):
        (self.root / 'note.md').write_text('changed', encoding='utf-8')
        self.assertTrue(cli.load_view(self.root, 'tasks', 'g1')['uncertain'])

    def test_approval_wrong_task_not_accepted(self):
        self.write('restore-requests/r.json', self.request)
        self.write('restore-approvals/a.json', {'schema_version': 1, 'approval_id': 'a',
                   'request_id': 'r', 'task_id': 'wrong', 'request_digest': self.request['payload_digest'],
                   'operation': 'restore', 'approved_at': '2026-10-01T10:00:00+09:00', 'source_ref': 'session:event', 'recorded_by': 'agent'})
        self.assertFalse(cli.load_view(self.root, 'tasks', 'g1')['active'])

    def test_active_unknown_not_disappearing(self):
        self.index['tasks']['t'].update(state='active', assessment='unknown')
        self.index['revision'] = cli.digest(self.index, 'revision')
        self.write('index.json', self.index)
        self.assertTrue(cli.load_view(self.root, 'tasks', 'g2')['active'])

    def test_conflicting_approval_identity_cannot_restore(self):
        self.write('restore-requests/r.json', self.request)
        record = {'schema_version': 1, 'approval_id': 'same', 'request_id': 'r',
                  'task_id': 't', 'request_digest': self.request['payload_digest'],
                  'operation': 'restore', 'approved_at': '2026-10-01T10:00:00+09:00',
                  'source_ref': 'fixture:first', 'recorded_by': 'agent'}
        self.write('restore-approvals/a.json', record)
        self.write('restore-approvals/b.json', dict(record, source_ref='fixture:other'))
        result = cli.load_view(self.root, 'tasks', 'g1')
        self.assertFalse(result['active'])
        errors = [e for e in result['exceptions'] if e.get('reason') == 'conflicting-approval']
        self.assertEqual({'tasks/restore-approvals/a.json', 'tasks/restore-approvals/b.json'},
                         {e['path'] for e in errors})

    def test_identical_duplicate_approval_has_one_effect(self):
        self.write('restore-requests/r.json', self.request)
        record = {'schema_version': 1, 'approval_id': 'same', 'request_id': 'r',
                  'task_id': 't', 'request_digest': self.request['payload_digest'],
                  'operation': 'restore', 'approved_at': '2026-10-01T10:00:00+09:00',
                  'source_ref': 'fixture:first', 'recorded_by': 'agent'}
        self.write('restore-approvals/a.json', record)
        self.write('restore-approvals/b.json', record)
        result = cli.load_view(self.root, 'tasks', 'g1')
        self.assertEqual(1, len(result['active']))
        self.assertEqual('complete', result['view_status'])

    def test_boolean_schema_version_is_not_version_one(self):
        self.index['schema_version'] = True
        self.index['revision'] = cli.digest(self.index, 'revision')
        self.write('index.json', self.index)
        with self.assertRaises(ValueError):
            cli.load_view(self.root, 'tasks', 'g1')

    def test_unknown_restore_reason_is_rejected(self):
        self.request['reason_kind'] = 'invented-state'
        self.request['payload_digest'] = cli.digest(self.request, 'payload_digest')
        self.write('restore-requests/r.json', self.request)
        result = cli.load_view(self.root, 'tasks', 'g1')
        self.assertTrue(any(e.get('reason') == 'request-digest-or-schema'
                            for e in result['exceptions']))

    def test_conflicting_receipt_identity_is_reported(self):
        self.make_active()
        receipt = {'schema_version': 1, 'request_id': 'r', 'task_id': 't',
                   'payload_digest': 'a' * 64, 'before_task_revision': 1,
                   'after_task_revision': 2, 'before_index_revision': 'b' * 64,
                   'after_index_revision': 'c' * 64, 'operation': 'restore',
                   'owner': 'fixture-writer', 'gate': 'g1',
                   'authorization_ref': 'fixture:approval', 'evidence_refs': ['fixture:source'],
                   'recovery_outcome': 'not-needed'}
        self.write('receipts/one.json', receipt)
        self.write('receipts/two.json', dict(receipt, payload_digest='d' * 64))
        result = cli.load_view(self.root, 'tasks', 'g1')
        self.assertTrue(result['active'])
        conflicts = [e for e in result['exceptions']
                     if e.get('reason') == 'conflicting-receipt']
        self.assertEqual({'tasks/receipts/one.json', 'tasks/receipts/two.json'},
                         {e['path'] for e in conflicts})

    def test_incomplete_receipt_cannot_suppress_restore(self):
        self.make_active()
        self.write('receipts/bad.json', {'schema_version': 1, 'request_id': 'r',
                                        'task_id': 't', 'payload_digest': 'a' * 64})
        result = cli.load_view(self.root, 'tasks', 'g1')
        self.assertTrue(result['active'])
        self.assertTrue(any(e.get('reason') == 'invalid-receipt' for e in result['exceptions']))

    def test_request_requires_audit_fields_and_typed_base(self):
        for change in ({'created': 'not-a-date'}, {'approval': {}},
                       {'base_index_revision': []}, {'base_task_revision': 0},
                       {'base_source_digests': {'note.md#task': True}}):
            with self.subTest(change=change):
                request = dict(self.request, **change)
                request['payload_digest'] = cli.digest(request, 'payload_digest')
                self.write('restore-requests/r.json', request)
                result = cli.load_view(self.root, 'tasks', 'g1')
                self.assertTrue(any(e.get('reason') == 'request-digest-or-schema'
                                    for e in result['exceptions']))

    def test_applied_request_requires_task_identity_and_revision(self):
        self.index['applied_requests']['r'] = {'payload_digest': self.request['payload_digest']}
        self.index['revision'] = cli.digest(self.index, 'revision')
        self.write('index.json', self.index)
        with self.assertRaises(ValueError):
            cli.load_view(self.root, 'tasks', 'g1')

    def integrated_restore(self, later_archive=False):
        task = self.index['tasks']['t']
        task.update(revision=3 if later_archive else 2, previous_revision=2 if later_archive else 1,
                    state='archived' if later_archive else 'active')
        self.index['applied_requests']['r'] = {
            'payload_digest': self.request['payload_digest'], 'task_id': 't', 'task_revision': 2}
        self.index['revision'] = cli.digest(self.index, 'revision')
        self.write('index.json', self.index)
        self.write('restore-requests/r.json', self.request)
        receipt = {'schema_version': 1, 'request_id': 'r', 'task_id': 't',
                   'payload_digest': self.request['payload_digest'], 'before_task_revision': 1,
                   'after_task_revision': 2, 'before_index_revision': self.request['base_index_revision'],
                   'after_index_revision': self.index['revision'] if not later_archive else 'a' * 64,
                   'operation': 'restore', 'owner': 'fixture-writer', 'gate': 'g1',
                   'authorization_ref': 'fixture:approval', 'evidence_refs': ['fixture:source'],
                   'recovery_outcome': 'not-needed'}
        return receipt

    def test_full_receipt_and_applied_index_have_no_replay(self):
        self.write('receipts/r.json', self.integrated_restore())
        result = cli.load_view(self.root, 'tasks', 'g1')
        self.assertEqual('complete', result['view_status'])
        self.assertEqual(1, len(result['active']))
        self.assertNotIn('restore_pending', result['active'][0])

    def test_old_integrated_request_does_not_reopen_later_archive(self):
        self.write('receipts/r.json', self.integrated_restore(later_archive=True))
        result = cli.load_view(self.root, 'tasks', 'g1')
        self.assertEqual('complete', result['view_status'])
        self.assertFalse(result['active'])

    def test_receipt_revision_mismatch_preserves_active_with_exception(self):
        receipt = self.integrated_restore()
        receipt.update(before_task_revision=2, after_task_revision=3)
        self.write('receipts/r.json', receipt)
        result = cli.load_view(self.root, 'tasks', 'g1')
        self.assertTrue(result['active'])
        self.assertTrue(result['uncertain'])
        self.assertTrue(any(e.get('reason') == 'receipt-index-inconsistent'
                            for e in result['exceptions']))

    def test_cancelled_approval_cannot_restore(self):
        self.write('restore-requests/r.json', self.request)
        approval = {'schema_version': 1, 'approval_id': 'a', 'request_id': 'r',
                    'task_id': 't', 'request_digest': self.request['payload_digest'],
                    'operation': 'restore', 'approved_at': '2026-10-01T10:00:00+09:00',
                    'source_ref': 'fixture:approval', 'recorded_by': 'agent'}
        self.write('restore-approvals/a.json', approval)
        self.write('approval-cancellations/c.json', {
            'schema_version': 1, 'cancellation_id': 'c', 'approval_id': 'a',
            'approval_digest': cli.digest(approval), 'operation': 'cancel-approval',
            'source_ref': 'fixture:cancel', 'recorded_by': 'agent'})
        result = cli.load_view(self.root, 'tasks', 'g1')
        self.assertFalse(result['active'])
        self.assertTrue(any(e.get('reason') == 'approval-unverified'
                            for e in result['exceptions']))

    def test_bad_cancellation_keeps_active(self):
        self.make_active()
        self.write('approval-cancellations/bad.json', {'schema_version': 1})
        result = cli.load_view(self.root, 'tasks', 'g1')
        self.assertTrue(result['active'])
        self.assertTrue(any(e.get('reason') == 'invalid-cancellation'
                            for e in result['exceptions']))

    def test_bad_cancellation_disables_otherwise_valid_restore(self):
        self.write('restore-requests/r.json', self.request)
        self.write('restore-approvals/a.json', {
            'schema_version': 1, 'approval_id': 'a', 'request_id': 'r',
            'task_id': 't', 'request_digest': self.request['payload_digest'],
            'operation': 'restore', 'approved_at': '2026-10-01T10:00:00+09:00',
            'source_ref': 'fixture:approval', 'recorded_by': 'agent'})
        self.assertTrue(cli.load_view(self.root, 'tasks', 'g1')['active'])
        self.write('approval-cancellations/bad.json', {'schema_version': 1})
        result = cli.load_view(self.root, 'tasks', 'g1')
        self.assertFalse(result['active'])
        self.assertEqual('partial', result['view_status'])

    def test_conflicting_cancellation_identity_is_not_silent(self):
        record = {'schema_version': 1, 'cancellation_id': 'same', 'approval_id': 'a',
                  'approval_digest': 'unknown', 'operation': 'cancel-approval',
                  'source_ref': 'fixture:one', 'recorded_by': 'agent'}
        self.write('approval-cancellations/one.json', record)
        self.write('approval-cancellations/two.json', dict(record, source_ref='fixture:two'))
        result = cli.load_view(self.root, 'tasks', 'g1')
        conflicts = [e for e in result['exceptions']
                     if e.get('reason') == 'conflicting-cancellation']
        self.assertEqual({'tasks/approval-cancellations/one.json',
                          'tasks/approval-cancellations/two.json'}, {e['path'] for e in conflicts})

    def test_approval_requires_real_offset_timestamp(self):
        self.write('restore-requests/r.json', self.request)
        for timestamp in ('date', '2026-10-01', '2026-10-01T10:00:00',
                          '2026-13-01T10:00:00+09:00'):
            with self.subTest(timestamp=timestamp):
                self.write('restore-approvals/a.json', {
                    'schema_version': 1, 'approval_id': 'a', 'request_id': 'r',
                    'task_id': 't', 'request_digest': self.request['payload_digest'],
                    'operation': 'restore', 'approved_at': timestamp,
                    'source_ref': 'fixture:approval', 'recorded_by': 'agent'})
                result = cli.load_view(self.root, 'tasks', 'g1')
                self.assertFalse(result['active'])
                self.assertTrue(any(e.get('reason') == 'invalid-approval'
                                    for e in result['exceptions']))


    def test_effective_view_revision_detects_source_change_with_same_index(self):
        first = cli.load_view(self.root, 'tasks', 'g1')
        (self.root / 'note.md').write_text('changed evidence', encoding='utf-8')
        second = cli.load_view(self.root, 'tasks', 'g1')
        self.assertEqual(first['index_revision'], second['index_revision'])
        self.assertNotEqual(first['view_revision'], second['view_revision'])


class PageTests(unittest.TestCase):
    def view(self):
        return {'view_status': 'partial', 'index_revision': 'r1',
                'active': [{'task_id': f'a{i}'} for i in range(5, -1, -1)],
                'uncertain': [{'task_id': f'u{i}', 'state': 'unresolved'} for i in range(7)],
                'exceptions': [{'path': f'bad{i}', 'reason': 'bad-record'} for i in range(4)]}

    def test_page_totals_remaining_and_stable_order_without_mutation(self):
        view = self.view()
        before = deepcopy(view)
        page = cli.page_view(view, 2, 0)
        self.assertEqual(view, before)
        self.assertEqual(['a0', 'a1'], [t['task_id'] for t in page['active']])
        self.assertEqual(7, page['pagination']['uncertain']['total'])
        self.assertEqual(5, page['pagination']['uncertain']['remaining'])
        self.assertEqual(2, page['pagination']['uncertain']['next_offset'])
        self.assertFalse(page['pagination']['all_displayed'])
        self.assertEqual('partial', page['view_status'])

    def test_all_pages_preserve_uncertainty_and_exception_paths(self):
        view = self.view()
        tasks, paths = [], []
        for offset in range(0, 8, 2):
            page = cli.page_view(view, 2, offset)
            tasks.extend(t['task_id'] for t in page['uncertain'])
            paths.extend(e['path'] for e in page['exceptions'])
        self.assertEqual([f'u{i}' for i in range(7)], tasks)
        self.assertEqual([f'bad{i}' for i in range(4)], paths)

    def test_empty_later_page_is_not_an_all_done_claim(self):
        page = cli.page_view(self.view(), 2, 50)
        self.assertFalse(page['uncertain'])
        self.assertEqual(7, page['pagination']['uncertain']['total'])
        self.assertFalse(page['pagination']['all_displayed'])

    def test_invalid_page_bounds_rejected(self):
        for size, offset in ((0, 0), (101, 0), (2, -1), (True, 0), (2, False)):
            with self.subTest(size=size, offset=offset), self.assertRaises(ValueError):
                cli.page_view(self.view(), size, offset)


if __name__ == '__main__':
    unittest.main()
