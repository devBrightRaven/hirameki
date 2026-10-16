"""Fixture test: run the exact task-view command line from next/tasks/triage
against an isolated temp vault (never touches a real vault)."""
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import task_view_cli as cli
from workflow_routes import task_contract

COMMANDS = ('next', 'tasks', 'triage')
def _line_pattern(script):
    return re.compile(r'^`(python3 -B -X utf8 "\$\{CLAUDE_PLUGIN_ROOT\}/scripts/' + script + r'\.py".*)`$', re.M)


LINE = _line_pattern('task_view_cli')
TIDY_LINE = _line_pattern('tidy_dry_run')
GATE = (ROOT / 'scripts' / 'TASK_GATE_VERSION').read_text(encoding='utf-8').strip()


def command_line(name, pattern=LINE):
    found = pattern.findall(task_contract(ROOT / ('references' if name == 'tasks' else 'commands'), name).read_text(encoding='utf-8'))
    assert len(found) == 1, (name, found)
    return found[0]


class CommandViewTests(unittest.TestCase):
    def test_unmarked_items_are_visible_but_not_confirmed_active(self):
        # Contract regression only: fresh-model adherence needs separate acceptance.
        for folder in ('commands', 'codex/skills/hirameki/references'):
            for name in COMMANDS:
                text = task_contract(ROOT / ('references' if folder == 'commands' and name == 'tasks' else folder), name).read_text(encoding='utf-8')
                with self.subTest(folder=folder, command=name):
                    self.assertNotIn('Unmarked items stay open', text)
                    self.assertIn('`status uncertain`, not confirmed active tasks', text)
                    self.assertIn('separate uncertain list in default and stuck modes', text)
                    self.assertIn('never automatically archive them', text)
                    self.assertIn('Explicit unfinished or reopened evidence may establish active status', text)

    def test_raw_fallback_preserves_context_and_explicit_reopening(self):
        for name in COMMANDS:
            text = task_contract(ROOT / ('references' if name == 'tasks' else 'commands'), name).read_text(encoding='utf-8')
            for anchor in ('未完成 is not closed', 'only newer explicit reopening',
                           'unverified candidates', 'not authoritative active or completed state'):
                self.assertIn(anchor, text, name)

    def test_bounded_reader_contract_in_all_commands(self):
        for name in COMMANDS:
            with self.subTest(command=name):
                text = task_contract(ROOT / ('references' if name == 'tasks' else 'commands'), name).read_text(encoding='utf-8')
                self.assertIn('--page-size 20 --offset 0', command_line(name))
                self.assertTrue(command_line(name).startswith('python3 -B -X utf8 '))
                for token in ('pagination.all_displayed', '--expected-revision',
                              '--expected-view-revision', 'next_offset',
                              'tool truncation is not successful inspection'):
                    self.assertIn(token, text)

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.vault = Path(tmp.name)
        (self.vault / 'AGENTS.md').write_text('## Vault Structure\n- research: Research\n', encoding='utf-8')
        data = self.vault / 'Research' / 'tidy' / 'tasks'
        (data / 'restore-requests').mkdir(parents=True)
        (data / 'restore-approvals').mkdir()
        tasks = {}
        for tid, state in (('act', 'active'), ('arch', 'archived'), ('rest', 'archived')):
            note = self.vault / f'{tid}.md'
            note.write_text(tid, encoding='utf-8')
            h = hashlib.sha256(note.read_bytes()).hexdigest()
            tasks[tid] = {'task_id': tid, 'revision': 1, 'state': state, 'summary': tid,
                          'scope': 'fixture',
                          'criteria': [{'criterion_id': 'c1', 'description': 'Fixture completion',
                                        'result': 'met', 'evidence_refs': ['e1']}],
                          'evidence': [{'evidence_id': 'e1', 'source_id': f'{tid}.md#a',
                                        'outcome': 'Fixture acceptance'}],
                          'open_dependencies': [], 'reason': 'fixture state',
                          'operation_id': 'genesis', 'previous_revision': None,
                          'assessment': 'confirmed', 'assessed_gate_version': GATE,
                          'sources': [{'path': f'{tid}.md', 'anchor': 'a',
                                       'raw_sha256': h, 'lf_sha256': h}]}
        index = {'schema_version': 1, 'parent_revision': None, 'gate_version': GATE,
                 'writer': 'fixture-writer', 'applied_requests': {}, 'tasks': tasks}
        index['revision'] = cli.digest(index, 'revision')
        self.write(data / 'index.json', index)
        h = tasks['rest']['sources'][0]['raw_sha256']
        req = {'schema_version': 1, 'request_id': 'r1', 'task_id': 'rest',
               'base_index_revision': index['revision'], 'base_task_revision': 1,
               'base_source_digests': {'rest.md#a': h}, 'reason': 'reopened', 'reason_kind': 'reopened',
               'created': '2026-10-01T00:00:00+09:00',
               'approval': {'source_ref': 'fixture:1', 'approving_user': 'fixture-user',
                            'operation': 'restore', 'scope': 'rest'}}
        req['payload_digest'] = cli.digest(req, 'payload_digest')
        self.write(data / 'restore-requests' / 'r1.json', req)
        self.write(data / 'restore-approvals' / 'a1.json', {
            'schema_version': 1, 'approval_id': 'a1', 'request_id': 'r1', 'task_id': 'rest',
            'request_digest': req['payload_digest'], 'operation': 'restore',
            'approved_at': '2026-10-01T00:00:00+09:00', 'source_ref': 'fixture:1', 'recorded_by': 'test'})

    @staticmethod
    def write(path, value):
        path.write_text(json.dumps(value), encoding='utf-8')

    def run_command(self, name, extra_args=(), expected_code=0):
        return self._run_line(command_line(name), extra_args, expected_code)

    def _run_line(self, line, extra_args=(), expected_code=0):
        argv = shlex.split(line, posix=True)  # split first: Windows paths hold backslashes
        subs = {'<vault>': str(self.vault), '<research>': 'Research', '<G>': GATE,
                '${CLAUDE_PLUGIN_ROOT}': str(ROOT)}
        for key, value in subs.items():
            argv = [a.replace(key, value) for a in argv]
        self.assertEqual('python3', argv[0])
        argv[0] = shutil.which('python3') or shutil.which('python') or sys.executable
        argv.extend(extra_args)
        env = dict(os.environ, CLAUDE_PLUGIN_ROOT=str(ROOT))
        before = {str(p): p.read_bytes() for p in self.vault.rglob('*') if p.is_file()}
        proc = subprocess.run(argv, env=env, capture_output=True, text=True, encoding='utf-8',
                              timeout=15, creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
        self.assertEqual(expected_code, proc.returncode, proc.stderr)
        self.assertEqual(before, {str(p): p.read_bytes() for p in self.vault.rglob('*') if p.is_file()})
        return json.loads(proc.stdout)

    def test_entry_pages_reject_changed_source_with_unchanged_index(self):
        data = self.vault / 'Research' / 'tidy' / 'tasks'
        index = json.loads((data / 'index.json').read_text(encoding='utf-8'))
        for number in range(26):
            task = dict(index['tasks']['act'])
            task.update(task_id=f'u{number:02}', state='unresolved', assessment='unknown')
            index['tasks'][task['task_id']] = task
        index['revision'] = cli.digest(index, 'revision')
        self.write(data / 'index.json', index)
        for name in COMMANDS:
            with self.subTest(command=name):
                (self.vault / 'act.md').write_text('act', encoding='utf-8')
                first = self.run_command(name)
                self.assertEqual(20, len(first['uncertain']))
                self.assertEqual(6, first['pagination']['uncertain']['remaining'])
                pins = ('--offset', '20', '--expected-revision', first['index_revision'],
                        '--expected-view-revision', first['view_revision'])
                second = self.run_command(name, pins)
                self.assertEqual(6, len(second['uncertain']))
                self.assertEqual(26, len({t['task_id'] for t in first['uncertain'] + second['uncertain']}))
                (self.vault / 'act.md').write_text('changed after first page', encoding='utf-8')
                rejected = self.run_command(name, pins, expected_code=1)
                self.assertEqual('page-effective-view-changed', rejected['exceptions'][0]['reason'])

    def test_same_effective_view_in_all_commands(self):
        views = [self.run_command(n) for n in COMMANDS]
        for view in views:
            active = {t['task_id']: t for t in view['active']}
            self.assertEqual({'act', 'rest'}, set(active))
            self.assertNotIn('arch', active)
            self.assertTrue(active['rest'].get('restore_pending'))
            self.assertFalse(active['act'].get('restore_pending'))
            self.assertEqual('complete', view['view_status'])
        self.assertEqual(views[0], views[1])
        self.assertEqual(views[0], views[2])

    def test_gate_stop_rule_and_revision_mismatch_in_all_commands(self):
        for name in COMMANDS:
            with self.subTest(command=name):
                text = task_contract(ROOT / ('references' if name == 'tasks' else 'commands'), name).read_text(encoding='utf-8')
                for phrase in ('not exactly one line', 'never substitute a remembered or hard-coded value',
                               'report the mismatch and stop, with no raw-note fallback',
                               '`page-index-revision-changed` or `page-effective-view-changed`',
                               'do not run the reader, and use the raw-note fallback below as unverified candidates only',
                               'scripts/task_view_cli.py` exists. If it is missing',
                               'plugin payload limitation', 'never collapse records into ID ranges',
                               "Keep each item's own reason visible"):
                    self.assertIn(phrase, text)

    def test_tidy_tasks_mode_text(self):
        text = (ROOT / 'commands' / 'tidy.md').read_text(encoding='utf-8')
        self.assertIn('## Task proposals (`tidy tasks`)', text)
        self.assertIn('| `tidy tasks` |', text)
        for phrase in ('proposal only', 'never writes any file', 'never asks whether to save',
                       'never archives', 'never edits the formal index',
                       '尚無有效待辦索引，無法執行任務歸檔試算。', '任務歸檔試算無法執行',
                       '外掛目錄缺少任務歸檔試算腳本', 'plugin payload limitation',
                       'takes no `--gate-version`'):
            self.assertIn(phrase, text)
        self.assertNotIn('--gate-version', command_line('tidy', TIDY_LINE))

    def test_tasks_command_has_no_recurrence_as_signal(self):
        text = task_contract(ROOT / 'references', 'tasks').read_text(encoding='utf-8')
        for phrase in ('potential procrastination', 'signal potential', '⚠',
                       'occurrence count (descending)', 'fuzzy match'):
            self.assertNotIn(phrase, text)
        self.assertIn('Current state outranks repetition', text)
        self.assertIn('Status uncertain (recurrence only, no authoritative status):', text)
        self.assertIn('Y uncertain candidates', text)
        self.assertNotIn('Total: X stuck tasks', text)

    def test_tidy_tasks_command_runs_read_only_against_fixture(self):
        # run_command asserts the fixture bytes are unchanged after the run
        report = self._run_line(command_line('tidy', TIDY_LINE))
        self.assertEqual('dry-run', report['mode'])
        self.assertIs(False, report['write_authorized'])
        self.assertEqual({'act', 'rest'}, {p['task_id'] for p in report['proposals']})
        for proposal in report['proposals']:
            self.assertIs(False, proposal['write_authorized'])
        self.assertEqual(GATE, report['gate_version'])
        self.assertTrue(report['index_revision'])

    def test_missing_index_exits_nonzero(self):
        (self.vault / 'Research' / 'tidy' / 'tasks' / 'index.json').unlink()
        argv = [sys.executable, '-X', 'utf8', str(ROOT / 'scripts' / 'task_view_cli.py'),
                '--vault', str(self.vault), '--data', 'Research/tidy/tasks', '--gate-version', GATE]
        proc = subprocess.run(argv, capture_output=True, text=True, encoding='utf-8')
        self.assertNotEqual(0, proc.returncode)


if __name__ == '__main__':
    unittest.main()
