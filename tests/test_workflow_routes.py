"""Deterministic migration evidence, not fresh-model behavior or deployment."""
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from workflow_routes import load_routes, resolve


class RouteTests(unittest.TestCase):
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
