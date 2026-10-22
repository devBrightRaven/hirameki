"""Synthetic byte/CLI acceptance; approval itself remains a host workflow gate."""
from contextlib import contextmanager
import hashlib
import json
import os
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
        self.assertEqual(self.cli('apply', *args)['status'], 'appended')
        stamp = self.note.stat().st_mtime_ns
        self.assertEqual(self.note.read_bytes(), self.before + self.draft.read_bytes())
        self.assertEqual(self.cli('apply', *args)['status'], 'already_applied')
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


if __name__ == '__main__':
    unittest.main()
