"""Deterministic migration evidence, not fresh-model behavior or deployment."""
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from workflow_routes import load_routes, resolve


class RouteTests(unittest.TestCase):
    def test_exact_append_contract_and_host_delivery(self):
        relative = 'references/capabilities/exact-append.md'
        self.assertEqual((ROOT / relative).read_bytes(),
                         (ROOT / 'codex/skills/hirameki' / relative).read_bytes())
        body = (ROOT / relative).read_text(encoding='utf-8')
        for phrase in ('freeze', 'plan_sha256', 'trailing_newline_bytes', 'save this / save all / skip / edit',
                       'helper cannot authenticate', 'write_unverified', 'never silently retry',
                       'POSIX advisory locks', 'outside the vault'):
            self.assertIn(phrase.lower(), body.lower())
        for directory in ('commands', 'codex/skills/hirameki/references'):
            for name in ('triage', 'journal'):
                self.assertIn('capabilities/exact-append.md',
                              (ROOT / directory / (name + '.md')).read_text(encoding='utf-8'))

    def test_lesson_lookup_and_append_contract(self):
        for root, entries in ((ROOT, ROOT / 'commands'),
                              (ROOT / 'codex/skills/hirameki', ROOT / 'codex/skills/hirameki/references')):
            contract = (root / 'references/capabilities/session-traces.md').read_text(encoding='utf-8')
            for phrase in ('## Bounded lesson lookup and disposition',
                           'Search across dates', 'three literal queries',
                           '20 matching files', 'read a selected match in\nfull',
                           '**reference-existing**', '**append**', '**unresolved**',
                           '## Lesson append procedure',
                           'all original bytes, frontmatter',
                           'original bytes remain an unchanged prefix',
                           'suffix equals the\napproved block',
                           'fresh approval', 'never overwrite on a filename collision'):
                self.assertIn(phrase, contract)
            self.assertIn('include those line breaks in the displayed block itself', contract)
            self.assertIn('block as UTF-8 with LF line endings', contract)
            self.assertIn('disclose before approval', contract)
            self.assertIn('Never normalize the original', contract)
            self.assertIn('verify the target is UTF-8', contract)
            self.assertIn('unresolved and refuse append', contract)
            triage = (entries / 'triage.md').read_text(encoding='utf-8')
            baseline = next(line for line in triage.splitlines() if line.startswith('**Already saved**'))
            self.assertIn('`{journal}/lessons/` across dates', baseline)
            lesson = triage.split('## Sub-flow — Lesson', 1)[1].split('## Completion summary', 1)[0]
            self.assertIn('**Append**', lesson)
            self.assertIn('existing target', lesson)
            self.assertIn('**Reference-existing**', lesson)
            self.assertIn('target is absent', lesson)
            journal = (entries / 'journal.md').read_text(encoding='utf-8')
            lesson = journal.split('## Lesson entries', 1)[1].split('## Review mode', 1)[0]
            self.assertIn('bounded lesson lookup', lesson)
            self.assertIn('Lesson append procedure', lesson)
            self.assertIn('template below is for new entries, not append mode', lesson)

    def test_session_trace_contract_delivery_and_entrypoints(self):
        relative = 'references/capabilities/session-traces.md'
        source = (ROOT / relative).read_bytes()
        self.assertEqual(source, (ROOT / 'codex/skills/hirameki' / relative).read_bytes())
        for directory in ('commands', 'codex/skills/hirameki/references'):
            for name in ('triage', 'journal', 'handoff'):
                body = (ROOT / directory / (name + '.md')).read_text(encoding='utf-8')
                self.assertIn('Before candidate selection, load and apply', body)
                self.assertIn('capabilities/session-traces.md', body)
                if name != 'handoff':
                    self.assertIn('## Emerging clues', body)
            triage = (ROOT / directory / 'triage.md').read_text(encoding='utf-8')
            self.assertNotIn("Skip when wrap's Next covers it.", triage)
            self.assertNotIn('the lesson applies beyond this task', triage)
            self.assertIn('One event can qualify within a narrow scope', triage)
            self.assertIn('written bytes must equal the displayed draft', triage)
            journal = (ROOT / directory / 'journal.md').read_text(encoding='utf-8')
            self.assertIn('### Emerging clues', journal)
            self.assertIn('one event may qualify without cross-project generalization', journal)
        contract = source.decode('utf-8')
        for boundary in ('coverage unknown', 'do not manufacture',
                         'separate judgment-update evidence gate',
                         'does not\ncreate unfinished work',
                         'a saved note alone never proves it was ingested'):
            self.assertIn(boundary.lower(), contract.lower())

    def test_natural_input_is_preserved_and_bounded(self):
        for base in ('commands', 'codex/skills/hirameki/references'):
            for name in ('next', 'lens', 'compose'):
                body = (ROOT / base / (name + '.md')).read_text(encoding='utf-8')
                self.assertIn('references/capabilities/natural-routing.md', body)
                self.assertIn('Preserve the actual request as input', body)
        contract = (ROOT / 'references/capabilities/natural-routing.md').read_text(encoding='utf-8')
        self.assertIn('installed language-writing', contract)
        self.assertIn('does not authorize saving', contract)
        self.assertIn('No hook is required', contract)

    def test_public_roster_and_copies(self):
        routes = load_routes()
        self.assertEqual(['next', 'lens', 'compose', 'decision-trace', 'triage'], routes['primary'])
        self.assertEqual(['wrap', 'journal', 'handoff'], routes['shortcuts'])
        self.assertEqual(10, len(routes['redirects']))
        self.assertEqual(routes, load_routes(ROOT / 'codex/skills/hirameki'))
        expected = set(routes['primary'] + routes['shortcuts'] + routes['specialized']) | set(routes['redirects'])
        self.assertEqual(21, len(expected))
        for directory in (ROOT / 'commands', ROOT / 'codex/skills/hirameki/references'):
            self.assertEqual(expected, {p.stem for p in directory.glob('*.md')})
            for name, route in routes['redirects'].items():
                body = (directory / (name + '.md')).read_text(encoding='utf-8')
                self.assertLess(len(body.encode('utf-8')), 2300, name)
                self.assertIn('compatibility redirect', body)
                self.assertIn('preserving $ARGUMENTS', body)
                self.assertIn('not an independent workflow or a write authorization', body)
                self.assertIn(route['target'] + ' ' + route['mode'], body)
                if directory == ROOT / 'codex/skills/hirameki/references':
                    self.assertIn('currently loaded Hirameki skill root', body)
                targets = [route, *route.get('variants', {}).values()]
                for target in targets:
                    self.assertTrue((directory / (target['target'] + '.md')).is_file())

    def test_redirect_preserves_scope_and_modes(self):
        cases = [('arc', 'topic A', 'lens', 'history topic A'),
                 ('bridge', 'A and B', 'lens', 'bridge A and B'),
                 ('tasks', 'stuck 14 Project X', 'next', 'stuck 14 Project X'),
                 ('tasks', '3', 'next', 'tasks 3'),
                 ('pulse', 'patterns agency', 'lens', 'patterns agency'),
                 ('pulse', 'snapshot', 'tidy', 'snapshot'),
                 ('pulse', 'week 7', 'next', 'week 7'),
                 ('graduate', 'Notes/with spaces.md', 'lens', 'cards Notes/with spaces.md'),
                 ('critique', 'draft.md', 'compose', 'review draft.md')]
        for name, arguments, target, translated in cases:
            self.assertEqual((target, translated), resolve(name, arguments))
        self.assertEqual(('wrap', 'mid-session'), resolve('wrap', 'mid-session'))
        with self.assertRaises(ValueError):
            resolve('nonexistent')

    def test_redirect_mode_accepts_whitespace_without_changing_scope(self):
        for root in (ROOT, ROOT / 'codex/skills/hirameki'):
            for arguments in ('stuck\t14 Project X', 'stuck\n14 Project X',
                              'stuck  \t14 Project X'):
                self.assertEqual(('next', 'stuck 14 Project X'),
                                 resolve('tasks', arguments, root))
            self.assertEqual(('lens', 'patterns Notes/with  spaces.md'),
                             resolve('pulse', 'patterns\nNotes/with  spaces.md', root))
            self.assertEqual(('next', 'tasks stuckness 14 Project X'),
                             resolve('tasks', 'stuckness 14 Project X', root))

    def test_shared_body_and_no_forced_stages(self):
        for name in ('lens', 'compose'):
            canonical = (ROOT / 'commands' / (name + '.md')).read_text(encoding='utf-8')
            adapter = (ROOT / 'codex/skills/hirameki/references' / (name + '.md')).read_text(encoding='utf-8')
            def omit_config(text):
                return '\n'.join(line for line in text.splitlines() if not line.startswith(
                    ('Read `vault:` from', 'Resolve vault configuration through', 'For a natural-language request, apply')))
            self.assertEqual(omit_config(canonical), omit_config(adapter))
            self.assertNotIn('## [1/', canonical)
            self.assertIn('full draft and target path', canonical)
        for name in ('concept-card', 'review', 'task-status', 'natural-routing'):
            self.assertEqual((ROOT / 'references/capabilities' / (name + '.md')).read_bytes(),
                (ROOT / 'codex/skills/hirameki/references/capabilities' / (name + '.md')).read_bytes())
        for directory in ('commands', 'codex/skills/hirameki/references'):
            next_body = (ROOT / directory / 'next.md').read_text(encoding='utf-8')
            self.assertNotIn('## Lucky mode', next_body)
            self.assertIn('Bare next never runs random exploration', next_body)
            self.assertIn('Translate capability input once', next_body)


if __name__ == '__main__':
    unittest.main()
