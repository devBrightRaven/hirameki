"""Delivery checks use a temporary payload, never installed runtime."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest
from test_task_view_commands import CommandViewTests, GATE

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('payload_builder', ROOT / 'scripts/build_codex_task_payload.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def package_stage(base):
    """Snapshot only package-owned sources, never runtime or personal files."""
    stage = base / 'pack source'
    stage.mkdir()
    shutil.copyfile(ROOT / 'package.json', stage / 'package.json')
    for name in ('commands', 'skills', 'references', 'codex', '.claude-plugin'):
        shutil.copytree(ROOT / name, stage / name)
    scripts = stage / 'scripts'
    scripts.mkdir()
    for name in (*builder.DEPENDENCIES, 'build_package_payload.mjs'):
        shutil.copyfile(ROOT / 'scripts' / name, scripts / name)
    return stage


def node_npm():
    node, npm = shutil.which('node'), shutil.which('npm')
    if not node or not npm:
        raise AssertionError('Actual package validation requires Node and npm')
    candidates = (Path(npm).resolve(),
                  Path(node).parent / 'node_modules/npm/bin/npm-cli.js',
                  Path(npm).parent / 'node_modules/npm/bin/npm-cli.js')
    cli = next((p for p in candidates if p.suffix == '.js' and p.is_file()), None)
    if cli is None:
        raise AssertionError('Cannot resolve native npm CLI')
    return node, str(cli)


class PayloadTests(unittest.TestCase):
    def test_actual_npm_tarball_runs_from_relocated_plugin_roots(self):
        persistent = os.environ.get('HIRAMEKI_PACKAGE_EVIDENCE_ROOT')
        if persistent:
            base = Path(persistent)
            base.mkdir(parents=True, exist_ok=False)
        else:
            directory = tempfile.TemporaryDirectory(prefix='hirameki package ')
            self.addCleanup(directory.cleanup)
            base = Path(directory.name)
        stage = package_stage(base)
        node, npm = node_npm()
        packed = subprocess.run([node, npm, 'pack', '--json', '--pack-destination', str(base)],
                                cwd=stage, capture_output=True, text=True, encoding='utf-8', timeout=60)
        (base / 'npm-pack-log.json').write_text(json.dumps(dict(exit_code=packed.returncode,
            stdout=packed.stdout, stderr=packed.stderr), ensure_ascii=False), encoding='utf-8')
        self.assertEqual(0, packed.returncode, packed.stderr)
        tarballs = list(base.glob('*.tgz'))
        self.assertEqual(1, len(tarballs))
        relocated = base / 'relocated 隔離 consumer'
        relocated.mkdir()
        with tarfile.open(tarballs[0], 'r:gz') as archive:
            names = archive.getnames()
            self.assertFalse(any(m.issym() or m.islnk() for m in archive.getmembers()))
            archive.extractall(relocated, filter='data')
        (base / 'tarball-files.json').write_text(json.dumps(names, indent=2), encoding='utf-8')
        package = relocated / 'package'
        self.assertTrue((package / 'codex/.codex-plugin/plugin.json').is_file())
        self.assertTrue((package / '.claude-plugin/plugin.json').is_file())
        for relative in ('references/capabilities/tasks.md',
                         'references/capabilities/session-traces.md',
                         'references/capabilities/natural-routing.md',
                         'references/capabilities/concept-card.md',
                         'references/capabilities/review.md',
                         'references/workflow-routing.json'):
            self.assertTrue((package / relative).is_file(), relative)
            self.assertTrue((package / 'codex/skills/hirameki' / relative).is_file(), relative)
        plugin = json.loads((package / '.claude-plugin/plugin.json').read_text(encoding='utf-8'))
        self.assertTrue(all((package / relative).is_dir() for relative in plugin['skills']))
        # Remove the source snapshot from its old path. Consumer cannot import it.
        moved = base / 'source snapshot retired'
        stage.rename(moved)
        fixture = CommandViewTests()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        before = {str(p): p.read_bytes() for p in fixture.vault.rglob('*') if p.is_file()}
        env = {k: v for k, v in os.environ.items() if k not in ('PYTHONPATH', 'PYTHONHOME')}
        checks = []
        for relative in ('.', 'codex/skills/hirameki'):
            root = package / relative
            for name in builder.DEPENDENCIES:
                self.assertEqual((ROOT / 'scripts' / name).read_bytes(),
                                 (root / 'scripts' / name).read_bytes())
            gate = (root / 'scripts/TASK_GATE_VERSION').read_text(encoding='utf-8').strip()
            for name in ('task_view_cli.py', 'tidy_dry_run.py'):
                argv = [sys.executable, '-B', '-X', 'utf8', str(root / 'scripts' / name),
                        '--vault', str(fixture.vault), '--data', 'Research/tidy/tasks']
                if name == 'task_view_cli.py': argv += ['--gate-version', gate]
                run = subprocess.run(argv, cwd=relocated, env=env, capture_output=True,
                                     text=True, encoding='utf-8', timeout=15)
                self.assertEqual(0, run.returncode, run.stderr)
                result = json.loads(run.stdout)
                if name == 'task_view_cli.py':
                    self.assertEqual({'act', 'rest'}, {i['task_id'] for i in result['active']})
                    self.assertEqual('Recorded approval matches payload; human utterance is not independently proven.', result['approval_limit'])
                else:
                    self.assertFalse(result['write_authorized'])
                checks.append(dict(root=relative,argv=argv,exit_code=run.returncode,result=result))
            query_vault = Path(os.environ.get('HIRAMEKI_R3_FIXTURE', str(fixture.vault)))
            query_data = 'research/tidy/tasks' if os.environ.get('HIRAMEKI_R3_FIXTURE') else 'Research/tidy/tasks'
            query_id = 'arch' if os.environ.get('HIRAMEKI_R3_FIXTURE') else 'rest'
            query_before = {str(p): p.read_bytes() for p in query_vault.rglob('*') if p.is_file()}
            argv = [sys.executable, '-B', '-X', 'utf8', str(root / 'scripts/task_view_cli.py'),
                    '--vault', str(query_vault), '--data', query_data, '--gate-version', gate,
                    '--task-id', query_id]
            for selected, expected_code in ((query_id, 0), ('nonexistent-packed-task', 1)):
                argv[-1] = selected
                run = subprocess.run(argv, cwd=relocated, env=env, capture_output=True,
                                     text=True, encoding='utf-8', timeout=15)
                self.assertEqual(expected_code, run.returncode, run.stderr)
                result = json.loads(run.stdout)
                self.assertTrue(result['global_validation']['full_index_checked'])
                self.assertEqual('found' if expected_code == 0 else 'task-not-found', result['query_status'])
                self.assertLess(len(run.stdout.encode('utf-8')), 16384)
                checks.append(dict(root=relative, argv=list(argv), exit_code=run.returncode, result=result))
            self.assertEqual(query_before, {str(p): p.read_bytes() for p in query_vault.rglob('*') if p.is_file()})
            guide = package / 'codex/skills/hirameki/references/task-restore/operation.md'
            delivered = guide.read_text(encoding='utf-8')
            self.assertLess(len(delivered.encode('utf-8')), 16384)
            namespace = {}
            # Execute the shipped recipe, not an independently authored saving implementation.
            exec(compile(delivered.split('```python\n', 1)[1].split('```', 1)[0],
                         str(guide), 'exec'), namespace)
            case = base / ('operation-' + ('root' if relative == '.' else 'codex'))
            shutil.copytree(query_vault, case)
            existing = {str(p): p.read_bytes() for p in case.rglob('*') if p.is_file()}
            transactions = []
            first_hashes = None
            for number in (1, 2):
                request_id = 'delivered-request-' + str(number)
                approval_id = 'delivered-approval-' + str(number)
                request = case / query_data / 'restore-requests' / (request_id + '.json')
                approval = case / query_data / 'restore-approvals' / (approval_id + '.json')
                response = namespace['restore_once'](
                    root / 'scripts/task_view_cli.py', case, query_data, gate, query_id,
                    request_id, approval_id, request, approval, 'synthetic-user',
                    'synthetic:explicit-delivery-trial-' + str(number), '合成取回演練',
                    'reopened', '2026-10-08T00:00:00+09:00', 'synthetic-delivery-harness')
                self.assertTrue(response['after']['task']['restore_pending'])
                self.assertIn(request_id, response['after']['task']['pending_requests'])
                self.assertTrue(response['before']['global_validation']['full_index_checked'])
                self.assertEqual(response['before']['exceptions'], response['after']['exceptions'])
                self.assertTrue(all(p.read_bytes() == content for name, content in existing.items()
                                    for p in [Path(name)]))
                if first_hashes is None:
                    first_hashes = {request: request.read_bytes(), approval: approval.read_bytes()}
                else:
                    self.assertTrue(all(p.read_bytes() == content for p, content in first_hashes.items()))
                transactions.append(response)
            # Existing-record and schema failures must happen before any new save.
            after_files = {str(p): p.read_bytes() for p in case.rglob('*') if p.is_file()}
            arguments = [root / 'scripts/task_view_cli.py', case, query_data, gate, query_id,
                         request_id, approval_id, request, approval, 'synthetic-user',
                         'synthetic:delivery-trial', '合成取回', 'reopened',
                         '2026-10-08T00:00:00+09:00', 'synthetic-delivery-harness']
            with self.assertRaises(FileExistsError):
                namespace['restore_once'](*arguments)
            arguments[5:9] = ['invalid-request', 'invalid-approval',
                              request.parent / 'invalid-request.json', approval.parent / 'invalid-approval.json']
            arguments[12] = 'not-a-reason-kind'
            with self.assertRaises(RuntimeError):
                namespace['restore_once'](*arguments)
            self.assertEqual(after_files, {str(p): p.read_bytes() for p in case.rglob('*') if p.is_file()})
            (base / ('operation-' + ('root' if relative == '.' else 'codex') + '-results.json')).write_text(
                json.dumps(dict(recipe_source=str(guide),only_public_CLI_and_stdlib=True,
                                transactions=transactions,existing_records_unchanged=True,
                                bad_schema_before_write=True,collision_before_write=True), ensure_ascii=False), encoding='utf-8')
        self.assertEqual(before, {str(p): p.read_bytes() for p in fixture.vault.rglob('*') if p.is_file()})
        (base / 'relocated-reader-results.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')

    def test_formal_prepack_preserves_divergent_existing_dependency(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            stage = package_stage(base)
            destination = stage / 'codex/skills/hirameki/scripts'
            destination.mkdir(exist_ok=True)
            protected = destination / 'task_view.py'
            protected.write_bytes(b'OTHER_OWNER_MODIFICATION')
            before = {p.name: p.read_bytes() for p in destination.iterdir()}
            node, _ = node_npm()
            run = subprocess.run([node, str(stage / 'scripts/build_package_payload.mjs')],
                                 cwd=base, capture_output=True, text=True, encoding='utf-8',timeout=15)
            self.assertNotEqual(0, run.returncode)
            self.assertEqual(b'OTHER_OWNER_MODIFICATION', protected.read_bytes())
            self.assertEqual(before, {p.name: p.read_bytes() for p in destination.iterdir()})

    def test_delivered_dry_run_uses_shared_reader_and_gate_without_writes(self):
        fixture = CommandViewTests()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            skill = builder.build(base / 'payload')
            before = {str(p): p.read_bytes() for p in fixture.vault.rglob('*') if p.is_file()}
            result = subprocess.run(
                [sys.executable, '-B', '-X', 'utf8',
                 str(skill / 'scripts/tidy_dry_run.py'), '--vault', str(fixture.vault),
                 '--data', 'Research/tidy/tasks'], cwd=base,
                capture_output=True, text=True, encoding='utf-8', timeout=10,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0)
            self.assertEqual(0, result.returncode, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(GATE, report['gate_version'])
            self.assertFalse(report['write_authorized'])
            self.assertEqual({'act', 'rest'}, {p['task_id'] for p in report['proposals']})
            restored = next(p for p in report['proposals'] if p['task_id'] == 'rest')
            self.assertEqual(['restore-awaiting-integration'], restored['reasons'])
            self.assertTrue(all(not p['write_authorized'] for p in report['proposals']))
            self.assertEqual(before, {str(p): p.read_bytes() for p in fixture.vault.rglob('*') if p.is_file()})

    def test_delivered_reader_preserves_active_archive_and_restore(self):
        fixture = CommandViewTests()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            skill = builder.build(base / 'payload')
            before = {str(p): p.read_bytes() for p in fixture.vault.rglob('*') if p.is_file()}
            result = subprocess.run(
                [sys.executable, '-B', '-X', 'utf8',
                 str(skill / 'scripts/task_view_cli.py'), '--vault', str(fixture.vault),
                 '--data', 'Research/tidy/tasks', '--gate-version', GATE],
                cwd=base, capture_output=True, text=True, encoding='utf-8', timeout=10,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0)
            self.assertEqual(0, result.returncode, result.stderr)
            view = json.loads(result.stdout)
            self.assertEqual('complete', view['view_status'])
            active = {item['task_id']: item for item in view['active']}
            self.assertEqual({'act', 'rest'}, set(active))
            self.assertTrue(active['rest']['restore_pending'])
            self.assertEqual([], view['uncertain'])
            self.assertEqual([], view['exceptions'])
            self.assertEqual(before, {str(p): p.read_bytes() for p in fixture.vault.rglob('*') if p.is_file()})

    def test_delivered_reader_runs_without_source_checkout(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            skill = builder.build(base / 'payload')
            for name in builder.DEPENDENCIES:
                self.assertEqual((ROOT / 'scripts' / name).read_bytes(),
                                 (skill / 'scripts' / name).read_bytes())
            vault = base / 'vault'
            vault.mkdir()
            gate = (skill / 'scripts/TASK_GATE_VERSION').read_text().strip()
            result = subprocess.run(
                [sys.executable, '-B', '-X', 'utf8',
                 str(skill / 'scripts/task_view_cli.py'), '--vault', str(vault),
                 '--data', 'Research/tidy/tasks', '--gate-version', gate],
                cwd=base, capture_output=True, text=True, encoding='utf-8', timeout=10,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0)
            self.assertNotIn('ModuleNotFoundError', result.stderr)
            self.assertTrue(result.stdout.strip(), result.stderr)
            self.assertEqual(1, result.returncode)
            response = json.loads(result.stdout)
            self.assertEqual('unavailable', response['view_status'])
            self.assertEqual([], response['active'])
            self.assertEqual('invalid-or-unavailable-index', response['exceptions'][0]['reason'])
            self.assertEqual([], list(vault.iterdir()))

    def test_existing_target_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                builder.build(directory)
            self.assertEqual([], list(Path(directory).iterdir()))

    def test_repository_target_is_rejected(self):
        with self.assertRaises(ValueError):
            builder.build(ROOT / 'candidate-payload')


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(PayloadTests)
    raise SystemExit(not unittest.TextTestRunner().run(suite).wasSuccessful())
