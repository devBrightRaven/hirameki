"""Synthetic byte/CLI acceptance; approval itself remains a host workflow gate."""
from contextlib import contextmanager
import hashlib
import json
import os
import re
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import exact_append as writer


class ExactAppend(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='exact append ')
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.root = self.base / 'synthetic vault'
        self.root.mkdir()
        self.note = self.root / '舊 lesson.md'
        self.note.write_bytes(b'---\r\nstatus: reference\r\n---\r\noriginal without final newline')
        self.before = self.note.read_bytes()
        self.draft = self.base / 'draft.bin'
        self.draft.write_bytes('\n\n## 證據追加\n- 未知：尚未確認。\n'.encode())
        self.plan = self.base / 'plan.json'

    def prepare(self):
        return writer.prepare(str(self.root), self.note.name, self.draft, self.plan)

    def cli(self, *args, expected=0):
        run = subprocess.run([sys.executable, '-B', '-X', 'utf8',
                              str(ROOT / 'scripts/exact_append.py'), *args],
                             capture_output=True, text=True, encoding='utf-8', timeout=15)
        self.assertEqual(expected, run.returncode, run.stderr or run.stdout)
        return json.loads(run.stdout)

    def test_prepare_show_no_vault_write_and_apply_exact_replay(self):
        result = self.cli('prepare', '--root', str(self.root), '--target', self.note.name,
                          '--draft', str(self.draft), '--plan', str(self.plan))
        self.assertEqual(self.note.read_bytes(), self.before)
        self.assertEqual(list(self.root.iterdir()), [self.note])
        self.assertEqual(result['draft_text'].encode(), self.draft.read_bytes())
        self.assertEqual(result['trailing_newline_bytes'], 1)
        args = ('--plan', str(self.plan), '--plan-sha256', result['plan_sha256'])
        self.assertEqual(self.cli('show', *args), result)
        self.assertEqual(self.note.read_bytes(), self.before)
        receipt = self.cli('apply', *args)
        self.assertEqual(receipt['status'], 'appended')
        self.assertEqual(receipt['target'], self.note.as_posix())
        self.assertEqual(receipt['plan_sha256'], result['plan_sha256'])
        self.assertEqual(receipt['before_sha256'], hashlib.sha256(self.before).hexdigest())
        self.assertEqual(receipt['draft_sha256'], hashlib.sha256(self.draft.read_bytes()).hexdigest())
        self.assertEqual(receipt['after_sha256'], hashlib.sha256(self.note.read_bytes()).hexdigest())
        stamp = self.note.stat().st_mtime_ns
        self.assertEqual(self.note.read_bytes(), self.before + self.draft.read_bytes())
        replay = self.cli('apply', *args)
        self.assertEqual(replay, dict(receipt, status='already_applied', written_bytes=0))
        self.assertEqual(stamp, self.note.stat().st_mtime_ns)

    def test_bom_crlf_empty_and_no_final_newline_preserved(self):
        for original in (b'', b'\xef\xbb\xbf# BOM\r\n', b'# LF\n', b'# no newline'):
            for suffix in (b'\n\n# suffix\n', b'\r\n# suffix\r\n', b'\n# no final'):
                with self.subTest(original=original, suffix=suffix):
                    self.plan.unlink(missing_ok=True)
                    self.note.write_bytes(original)
                    self.draft.write_bytes(suffix)
                    staged = self.prepare()
                    self.assertEqual(writer.apply(self.plan, staged['plan_sha256'])['status'], 'appended')
                    self.assertEqual(self.note.read_bytes(), original + suffix)

    def test_rendered_display_preserves_boundary_bytes_and_nested_fences(self):
        self.note = self.note.rename(self.root / '[lesson](link)`note.md')
        for suffix in (b'\n\n## evidence\n', b'\n## evidence\n\n', b'\n## no final', b'\r\n## CRLF\r\n',
                       b'\n## example\n```python\nprint(1)\n```\n'):
            with self.subTest(suffix=suffix):
                self.plan.unlink(missing_ok=True)
                self.draft.write_bytes(suffix)
                result = self.prepare()
                display = result['display_markdown']
                match = re.search(r'(?m)^(`{3,})(markdown|json)\n', display)
                self.assertIsNotNone(match)
                body = display[match.end():].removesuffix(match[1] + '\n')
                actual = json.loads(body).encode() if match[2] == 'json' else body.encode()
                self.assertEqual(actual, suffix)
                self.assertIn(result['plan_sha256'], display)
                self.assertIn(result['draft_sha256'], display)
                self.assertIn(self.note.as_posix(), display)
                metadata = re.match(r'(`{3,})text\n(.*?)\n\1\n', display, re.S)
                self.assertIsNotNone(metadata)
                self.assertIn(json.dumps(self.note.as_posix(), ensure_ascii=False), metadata[2])

    def test_target_conflict_and_fresh_approval_plan(self):
        old = self.prepare()
        external = b'\nEXTERNAL-77\n'
        self.note.write_bytes(self.before + external)
        with self.assertRaisesRegex(writer.Refused, 'fresh-approval'):
            writer.apply(self.plan, old['plan_sha256'])
        self.assertEqual(self.note.read_bytes(), self.before + external)
        self.plan = self.base / 'rebased.json'
        fresh = self.prepare()
        self.assertNotEqual(fresh['plan_sha256'], old['plan_sha256'])
        self.assertEqual(self.note.read_bytes(), self.before + external)
        writer.apply(self.plan, fresh['plan_sha256'])
        self.assertEqual(self.note.read_bytes(), self.before + external + self.draft.read_bytes())

    def test_tampered_plan_and_wrong_hash_refused(self):
        staged = self.prepare()
        with self.assertRaisesRegex(writer.Refused, 'plan-changed'):
            writer.apply(self.plan, '0' * 64)
        self.plan.write_bytes(self.plan.read_bytes() + b' ')
        self.cli('apply', '--plan', str(self.plan), '--plan-sha256', staged['plan_sha256'], expected=2)
        self.assertEqual(self.note.read_bytes(), self.before)

    def test_modified_draft_file_does_not_recompose_frozen_plan(self):
        staged = self.prepare()
        approved = self.draft.read_bytes()
        self.draft.write_bytes(b'not approved')
        writer.apply(self.plan, staged['plan_sha256'])
        self.assertEqual(self.note.read_bytes(), self.before + approved)

    def test_invalid_inputs_refuse_without_mutating_note(self):
        for suffix in (b'', b'\xff', b'\x00x'):
            self.draft.write_bytes(suffix)
            with self.assertRaises(writer.Refused):
                self.prepare()
            self.assertFalse(self.plan.exists())
        self.draft.write_bytes(b'valid\n')
        for relative in ('../outside.md', str(self.note), 'missing.md'):
            with self.assertRaises(writer.Refused):
                writer.prepare(str(self.root), relative, self.draft, self.plan)
        with self.assertRaises(writer.Refused):
            writer.prepare(str(self.root), self.note.name, self.draft, self.root / 'plan.json')
        self.note.write_bytes(b'\xff\xfe\x00\x00')
        with self.assertRaisesRegex(writer.Refused, 'unsupported-encoding'):
            self.prepare()
        self.assertEqual(self.note.read_bytes(), b'\xff\xfe\x00\x00')

    def test_same_base_different_draft_cannot_overwrite_new_append(self):
        first = self.prepare()
        self.plan = self.base / 'second.json'
        self.draft.write_bytes(b'\nsecond evidence\n')
        second = self.prepare()
        writer.apply(self.base / 'plan.json', first['plan_sha256'])
        saved = self.note.read_bytes()
        with self.assertRaises(writer.Refused):
            writer.apply(self.plan, second['plan_sha256'])
        self.assertEqual(self.note.read_bytes(), saved)

    def test_busy_lock_fails_closed_without_vault_sidecars(self):
        staged = self.prepare()
        with writer.locked_target(str(self.root), self.note.name):
            result = self.cli('apply', '--plan', str(self.plan), '--plan-sha256', staged['plan_sha256'], expected=2)
            self.assertFalse(result['write_may_have_occurred'])
        self.assertEqual(self.note.read_bytes(), self.before)
        self.assertEqual(list(self.root.iterdir()), [self.note])

    def test_partial_write_reported_without_rollback_or_retry(self):
        staged = self.prepare()
        original_lock = writer.locked_target
        @contextmanager
        def faulty(*args):
            with original_lock(*args) as stream:
                class Partial:
                    def __getattr__(self, name):
                        return getattr(stream, name)
                    def write(self, data):
                        stream.write(data[:3])
                        raise OSError('synthetic failure')
                yield Partial()
        with patch.object(writer, 'locked_target', faulty):
            result = writer.apply(self.plan, staged['plan_sha256'])
        self.assertEqual(result['status'], 'write_unverified')
        self.assertFalse(result['retry_safe'])
        self.assertEqual(self.note.read_bytes(), self.before + self.draft.read_bytes()[:3])
        with self.assertRaises(writer.Refused):
            writer.apply(self.plan, staged['plan_sha256'])

    def test_readback_failure_never_reports_success(self):
        staged = self.prepare()
        read = writer.bounded
        reads = []
        def corrupted(stream, limit):
            raw = read(stream, limit)
            reads.append(1)
            return raw if len(reads) == 1 else raw + b'phantom'
        # Inject only target's second read, after plan decoding.
        plan, suffix = writer.load(self.plan, staged['plan_sha256'])
        with patch.object(writer, 'load', return_value=(plan, suffix)), patch.object(writer, 'bounded', corrupted):
            result = writer.apply(self.plan, staged['plan_sha256'])
        self.assertEqual(result['status'], 'write_unverified')
        self.assertEqual(result['reason'], 'readback-mismatch')

    def test_hardlinked_target_refused(self):
        alias = self.base / 'other.md'
        os.link(self.note, alias)
        with self.assertRaisesRegex(writer.Refused, 'identity'):
            self.prepare()
        self.assertEqual(alias.read_bytes(), self.before)

    def test_linked_target_and_parent_refused(self):
        alias = self.root / 'alias.md'
        try:
            alias.symlink_to(self.note)
        except OSError as error:
            self.skipTest('symlink creation unavailable: ' + str(error))
        with self.assertRaisesRegex(writer.Refused, 'linked'):
            writer.prepare(str(self.root), alias.name, self.draft, self.plan)
        folder = self.root / 'linked-folder'
        folder.symlink_to(self.base, target_is_directory=True)
        with self.assertRaisesRegex(writer.Refused, 'linked'):
            writer.prepare(str(self.root), 'linked-folder/draft.bin', self.draft, self.plan)

    def test_create_freezes_bytes_and_returns_readback_receipt(self):
        target = self.root / '新候選.md'
        staged = self.cli('prepare', '--create', '--root', str(self.root), '--target', target.name,
                          '--draft', str(self.draft), '--plan', str(self.plan))
        self.assertFalse(target.exists())
        frozen = self.draft.read_bytes()
        self.draft.write_bytes(b'changed after preparation')
        args = ('--plan', str(self.plan), '--plan-sha256', staged['plan_sha256'])
        self.assertEqual(self.cli('show', *args), staged)
        receipt = self.cli('apply', *args)
        self.assertEqual(receipt['status'], 'created')
        self.assertEqual(receipt['target'], target.as_posix())
        self.assertEqual(receipt['plan_sha256'], staged['plan_sha256'])
        self.assertEqual(receipt['before_sha256'], hashlib.sha256(b'').hexdigest())
        self.assertEqual(receipt['after_sha256'], hashlib.sha256(target.read_bytes()).hexdigest())
        self.assertEqual(receipt['draft_sha256'], receipt['after_sha256'])
        self.assertEqual(target.read_bytes(), frozen)
        # Even identical content cannot prove a prior invocation created this file.
        self.assertEqual(self.cli('apply', *args, expected=2)['status'], 'refused')
        self.assertEqual(target.read_bytes(), frozen)

    def test_create_collision_before_prepare_and_between_prepare_apply(self):
        with self.assertRaisesRegex(writer.Refused, 'target-exists'):
            writer.prepare(str(self.root), self.note.name, self.draft, self.plan, create=True)
        target = self.root / 'collision.md'
        staged = writer.prepare(str(self.root), target.name, self.draft, self.plan, create=True)
        target.write_bytes(b'OTHER WRITER')
        self.cli('apply', '--plan', str(self.plan), '--plan-sha256', staged['plan_sha256'], expected=2)
        self.assertEqual(target.read_bytes(), b'OTHER WRITER')
        self.assertEqual(self.note.read_bytes(), self.before)

    def test_two_create_processes_only_one_writes(self):
        target = self.root / 'race.md'
        staged = writer.prepare(str(self.root), target.name, self.draft, self.plan, create=True)
        argv = [sys.executable, '-B', str(ROOT / 'scripts/exact_append.py'), 'apply',
                '--plan', str(self.plan), '--plan-sha256', staged['plan_sha256']]
        processes = [subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE) for _ in range(2)]
        results = [p.communicate(timeout=15) for p in processes]
        self.assertEqual(sorted(p.returncode for p in processes), [0, 2], results)
        self.assertEqual(sorted(json.loads(out)['status'] for out, _ in results), ['created', 'refused'])
        self.assertEqual(target.read_bytes(), self.draft.read_bytes())

    def test_create_readback_failure_keeps_unknown_file_without_retry(self):
        target = self.root / 'unknown.md'
        staged = writer.prepare(str(self.root), target.name, self.draft, self.plan, create=True)
        plan, draft = writer.load(self.plan, staged['plan_sha256'])
        with patch.object(writer, 'load', return_value=(plan, draft)), patch.object(writer, 'bounded', side_effect=[b'', b'bad']):
            result = writer.apply(self.plan, staged['plan_sha256'])
        self.assertEqual(result['status'], 'write_unverified')
        self.assertFalse(result['retry_safe'])
        self.assertEqual(target.read_bytes(), draft)

    def test_create_preserves_append_that_wins_before_create_lock(self):
        target = self.root / 'create-append-race.md'
        staged = writer.prepare(str(self.root), target.name, self.draft, self.plan, create=True)
        other_draft = self.base / 'other.bin'
        other_draft.write_bytes(b'APPEND\n')
        other_plan = self.base / 'other.json'
        fdopen = writer.os.fdopen
        def racing_open(*args, **kwargs):
            stream = fdopen(*args, **kwargs)
            prepared = self.cli('prepare', '--root', str(self.root), '--target', target.name,
                                '--draft', str(other_draft), '--plan', str(other_plan))
            self.assertEqual(self.cli('apply', '--plan', str(other_plan), '--plan-sha256',
                                      prepared['plan_sha256'])['status'], 'appended')
            return stream
        with patch.object(writer.os, 'fdopen', side_effect=racing_open):
            outcome = writer.apply(self.plan, staged['plan_sha256'])
        self.assertEqual(outcome['status'], 'write_unverified')
        self.assertEqual(outcome['reason'], 'create-target-changed')
        self.assertEqual(target.read_bytes(), b'APPEND\n')

    def test_create_holds_same_lock_as_append(self):
        target = self.root / 'create-locked.md'
        staged = writer.prepare(str(self.root), target.name, self.draft, self.plan, create=True)
        write_verified = writer.write_verified
        def during_write(*args):
            result = self.cli('prepare', '--root', str(self.root), '--target', target.name,
                              '--draft', str(self.draft), '--plan', str(self.base / 'blocked.json'), expected=2)
            self.assertEqual(result['status'], 'refused')
            write_verified(*args)
        with patch.object(writer, 'write_verified', side_effect=during_write):
            self.assertEqual(writer.apply(self.plan, staged['plan_sha256'])['status'], 'created')
        self.assertEqual(target.read_bytes(), self.draft.read_bytes())

    def test_create_invalid_scope_and_plan_refused(self):
        for relative in ('../outside.md', '.', 'missing-parent/note.md'):
            with self.assertRaises(writer.Refused):
                writer.prepare(str(self.root), relative, self.draft, self.plan, create=True)
        with self.assertRaisesRegex(writer.Refused, 'outside-vault'):
            writer.prepare(str(self.root), 'candidate.md', self.draft, self.root / 'plan.json', create=True)
        staged = writer.prepare(str(self.root), 'candidate.md', self.draft, self.plan, create=True)
        plan, _ = writer.load(self.plan, staged['plan_sha256'])
        for changes in (dict(before_bytes=1), dict(after_sha256='0' * 64), dict(operation='append')):
            with self.assertRaises(writer.Refused):
                writer.validate(dict(plan, **changes))

    def test_create_partial_write_and_fsync_failure_are_unknown(self):
        for failure in ('partial', 'fsync'):
            with self.subTest(failure=failure):
                target = self.root / (failure + '.md')
                plan_path = self.base / (failure + '.json')
                staged = writer.prepare(str(self.root), target.name, self.draft, plan_path, create=True)
                def partial(stream, draft, original, plan):
                    stream.write(draft[:3])
                    raise OSError('synthetic partial write')
                injected = (patch.object(writer, 'write_verified', side_effect=partial) if failure == 'partial'
                            else patch.object(writer.os, 'fsync', side_effect=OSError('synthetic fsync failure')))
                with injected:
                    result = writer.apply(plan_path, staged['plan_sha256'])
                self.assertEqual(result['status'], 'write_unverified')
                self.assertTrue(result['write_may_have_occurred'])
                self.assertFalse(result['retry_safe'])
                saved = target.read_bytes()
                self.assertEqual(saved, self.draft.read_bytes()[:3] if failure == 'partial' else self.draft.read_bytes())
                self.cli('apply', '--plan', str(plan_path), '--plan-sha256', staged['plan_sha256'], expected=2)
                self.assertEqual(target.read_bytes(), saved)

    def test_create_rejects_linked_target_or_parent_without_writes(self):
        outside = self.base / 'outside.md'
        outside.write_bytes(b'PROTECTED')
        alias = self.root / 'linked.md'
        folder = self.root / 'linked-dir'
        try:
            alias.symlink_to(outside)
            folder.symlink_to(self.base, target_is_directory=True)
        except OSError as error:
            self.skipTest('symlink creation unavailable: ' + str(error))
        for relative in (alias.name, 'linked-dir/new.md'):
            with self.assertRaisesRegex(writer.Refused, 'linked'):
                writer.prepare(str(self.root), relative, self.draft, self.plan, create=True)
        self.assertEqual(outside.read_bytes(), b'PROTECTED')
        self.assertFalse((self.base / 'new.md').exists())
        self.assertFalse(self.plan.exists())

    def test_create_rejects_link_substitution_after_prepare(self):
        target = self.root / 'replaced.md'
        staged = writer.prepare(str(self.root), target.name, self.draft, self.plan, create=True)
        outside = self.base / 'protected.md'
        outside.write_bytes(b'PROTECTED')
        try:
            target.symlink_to(outside)
        except OSError as error:
            self.skipTest('symlink creation unavailable: ' + str(error))
        result = self.cli('apply', '--plan', str(self.plan), '--plan-sha256', staged['plan_sha256'], expected=2)
        self.assertFalse(result['write_may_have_occurred'])
        self.assertEqual(outside.read_bytes(), b'PROTECTED')


if __name__ == '__main__':
    unittest.main()
