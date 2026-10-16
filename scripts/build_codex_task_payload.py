"""Build an isolated acceptance payload; not a release or installer."""
import argparse
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
DEPENDENCIES = (
    'task_view.py', 'task_view_cli.py', 'archive_gate.py',
    'task_contract_primitives.py', 'TASK_GATE_VERSION', 'tidy_dry_run.py',
    'task_restore_contract.py',
)


def build(destination):
    destination = Path(destination).resolve()
    if destination == ROOT or ROOT in destination.parents:
        raise ValueError('Acceptance payload must be outside the source repository')
    if destination.exists():
        raise ValueError('Destination must not already exist; existing work is preserved')
    source = ROOT / 'codex'
    # Check every dependency before creating any output.
    for name in DEPENDENCIES:
        path = ROOT / 'scripts' / name
        if not path.is_file() or path.is_symlink():
            raise ValueError('Missing or linked payload dependency: ' + name)
    shutil.copytree(source, destination)
    scripts = destination / 'skills' / 'hirameki' / 'scripts'
    scripts.mkdir(exist_ok=True)
    for name in DEPENDENCIES:
        target = scripts / name
        if target.exists():
            if target.is_symlink() or not target.is_file() or target.read_bytes() != (ROOT / 'scripts' / name).read_bytes():
                raise ValueError('Preserve divergent bundled dependency: ' + name)
        else:
            shutil.copyfile(ROOT / 'scripts' / name, target)
    return scripts.parent


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    options = parser.parse_args()
    print(build(options.output))
