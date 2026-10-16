"""Source command execution, not fresh-model routing acceptance."""
import json
import os
import re
import shlex
import subprocess
import sys
import unittest
from test_task_view_commands import CommandViewTests, ROOT, GATE, cli
from workflow_routes import task_contract


class CodexCommandViewTests(CommandViewTests):
    def test_triage_save_contract_matches_canonical(self):
        canonical = (ROOT / 'commands/triage.md').read_text(encoding='utf-8')
        adapter = (ROOT / 'codex/skills/hirameki/references/triage.md').read_text(encoding='utf-8')
        def action_model(text):
            return text.split('## Action model\n', 1)[1].split('\n---', 1)[0]
        self.assertEqual(action_model(canonical), action_model(adapter))
        for line in canonical.splitlines():
            if ('An active `save all`' in line
                    or line.startswith('- Show the FULL draft')
                    or 'no undisplayed draft exists' in line):
                self.assertIn(line, adapter)

    def test_tidy_proposal_entry_executes_delivered_shared_cli_read_only(self):
        import importlib.util
        import tempfile
        from pathlib import Path
        spec = importlib.util.spec_from_file_location('payload', ROOT / 'scripts/build_codex_task_payload.py')
        builder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(builder)
        with tempfile.TemporaryDirectory() as directory:
            skill = builder.build(Path(directory) / 'payload')
            text = (skill / 'references/tidy.md').read_text(encoding='utf-8')
            command = re.findall(r'^`(python3 -B -X utf8 .*tidy_dry_run.py".*)`$', text, re.M)
            self.assertEqual(1, len(command))
            argv = shlex.split(command[0])
            replacements = {'<HIRAMEKI_TASK_ROOT>': str(skill), '<vault>': str(self.vault), '<research>': 'Research'}
            for key, value in replacements.items():
                argv = [part.replace(key, value) for part in argv]
            argv[0] = sys.executable
            before = {str(p): p.read_bytes() for p in self.vault.rglob('*') if p.is_file()}
            result = subprocess.run(argv, capture_output=True, text=True, encoding='utf-8', timeout=15,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            self.assertEqual(0, result.returncode, result.stderr)
            report = json.loads(result.stdout)
            self.assertFalse(report['write_authorized'])
            self.assertEqual({'act', 'rest'}, {p['task_id'] for p in report['proposals']})
            self.assertEqual(before, {str(p): p.read_bytes() for p in self.vault.rglob('*') if p.is_file()})

    def test_recurrence_is_context_not_judgment(self):
        text = task_contract(ROOT / 'codex/skills/hirameki/references', 'tasks').read_text(encoding='utf-8')
        self.assertNotIn('signal potential procrastination', text)
        self.assertNotIn('Sort by: occurrence count', text)
        self.assertIn('Recurrence is context, not priority or procrastination evidence', text)
        self.assertIn('Ambiguous identity matches remain separate candidates', text)

    def test_raw_fallback_closure_contract(self):
        # Text contract coverage only; not a fresh-model behavior test.
        for name in ('next', 'tasks', 'triage'):
            text = task_contract(ROOT / 'codex/skills/hirameki/references', name).read_text(encoding='utf-8')
            for anchor in ('[x]', '✓ Done', 'withdrawn', 'superseded',
                           '未完成 is not closed', 'Unmarked items without explicit status evidence',
                           'only newer explicit reopening does'):
                self.assertIn(anchor, text, name)

    def run_command(self, name, extra_args=(), expected_code=0):
        text = task_contract(ROOT / 'codex/skills/hirameki/references', name).read_text(encoding='utf-8')
        self.assertNotIn('CLAUDE_PLUGIN_ROOT}/scripts', text)
        matches = re.findall(r'^`(python3 -X utf8 "<HIRAMEKI_TASK_ROOT>/scripts/task_view_cli.py".*)`$', text, re.M)
        self.assertEqual(1, len(matches))
        argv = shlex.split(matches[0])
        for token, value in {'<HIRAMEKI_TASK_ROOT>': str(ROOT), '<vault>': str(self.vault),
                             '<research>': 'Research', '<G>': GATE}.items():
            argv = [arg.replace(token, value) for arg in argv]
        argv[0] = sys.executable
        argv.extend(extra_args)
        before = {str(p): p.read_bytes() for p in self.vault.rglob('*') if p.is_file()}
        result = subprocess.run(argv, capture_output=True, text=True, encoding='utf-8', timeout=10,
                                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
        self.assertEqual(expected_code, result.returncode, result.stderr)
        self.assertEqual(before, {str(p): p.read_bytes() for p in self.vault.rglob('*') if p.is_file()})
        return json.loads(result.stdout)

    def test_paged_consumer_contract_preserves_scope_and_revision_pins(self):
        for name in ('next', 'tasks', 'triage'):
            text = task_contract(ROOT / 'codex/skills/hirameki/references', name).read_text(encoding='utf-8')
            for anchor in ('--page-size 20 --offset 0', '--expected-revision',
                           '--expected-view-revision', 'bounded preview',
                           'not a complete baseline', 'do not claim all done'):
                self.assertIn(anchor, text, name)

    def test_exact_entry_commands_page_large_uncertainty_and_errors(self):
        data = self.vault / 'Research' / 'tidy' / 'tasks'
        index = json.loads((data / 'index.json').read_text())
        for number in range(26):
            task = dict(index['tasks']['act'])
            task.update(task_id=f'u{number:02}', state='unresolved', assessment='unknown')
            index['tasks'][task['task_id']] = task
        index['revision'] = cli.digest(index, 'revision')
        self.write(data / 'index.json', index)
        for number in range(23):
            self.write(data / 'restore-requests' / f'bad-{number:02}.json', {'invalid': True})
        for name in ('next', 'tasks', 'triage'):
            first = self.run_command(name)
            self.assertEqual(20, len(first['uncertain']), name)
            self.assertEqual(26, first['pagination']['uncertain']['total'])
            self.assertEqual(6, first['pagination']['uncertain']['remaining'])
            self.assertEqual(23, first['pagination']['exceptions']['total'])
            self.assertFalse(first['pagination']['all_displayed'])
            second = self.run_command(name, ('--offset', '20',
                '--expected-revision', first['index_revision'],
                '--expected-view-revision', first['view_revision']))
            self.assertEqual(6, len(second['uncertain']))
            self.assertEqual(3, len(second['exceptions']))
            self.assertEqual(26, len({t['task_id'] for t in first['uncertain'] + second['uncertain']}))

    def test_gate_source_not_constant(self):
        for name in ('next', 'tasks', 'triage'):
            text = task_contract(ROOT / 'codex/skills/hirameki/references', name).read_text(encoding='utf-8')
            self.assertIn('scripts/TASK_GATE_VERSION', text)
            self.assertNotIn(GATE, text)

    def test_payload_root_resolution_preserves_explicit_configuration(self):
        # Contract coverage only: a model still needs fresh-payload acceptance.
        for name in ('next', 'tasks', 'triage'):
            text = task_contract(ROOT / 'codex/skills/hirameki/references', name).read_text(encoding='utf-8')
            self.assertIn('actually loaded Hirameki SKILL.md', text)
            self.assertIn('If an explicit root is invalid, report unavailable', text)
            self.assertIn('rather than silently switching roots', text)

    def test_indexed_status_lists_are_separate(self):
        for name in ('next', 'tasks', 'triage'):
            text = task_contract(ROOT / 'codex/skills/hirameki/references', name).read_text(encoding='utf-8')
            self.assertIn('three separately labelled lists', text, name)
            self.assertIn('Do not blend uncertain items into the active list', text, name)
            self.assertIn('do not nest interpreter subprocesses or replace the CLI with runpy', text, name)
            self.assertIn('do not rewrite the launch to evade the denial', text, name)
            self.assertIn('do not require waiting for scheduled integration', text, name)
            self.assertIn('Restoring visibility does not grant permission', text, name)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(CodexCommandViewTests)
    raise SystemExit(not unittest.TextTestRunner().run(suite).wasSuccessful())
