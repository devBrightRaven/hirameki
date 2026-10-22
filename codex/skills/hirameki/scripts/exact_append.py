"""Byte-exact local append. Consent belongs to the calling workflow, not this CLI.

Plans are private session artifacts, never vault notes. Local locks coordinate this
helper's writers; POSIX locks do not exclude arbitrary editors or remote sync.
No rollback, automatic retry, new-note creation or cross-machine guarantee.
"""
import argparse
import base64
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys

NOTE_LIMIT = 8 * 1024 * 1024
DRAFT_LIMIT = 1024 * 1024
PLAN_LIMIT = 2 * DRAFT_LIMIT


class Refused(Exception):
    pass


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def bounded(stream, limit):
    raw = stream.read(limit + 1)
    if len(raw) > limit:
        raise Refused('byte-limit')
    return raw


def utf8(raw):
    try:
        text = raw.decode('utf-8')
    except UnicodeError:
        raise Refused('unsupported-encoding') from None
    if '\0' in text:
        raise Refused('unsupported-encoding')
    return text


def linked(path):
    return path.is_symlink() or (hasattr(path, 'is_junction') and path.is_junction())


def target_path(root, relative):
    root = Path(root)
    if not root.is_absolute() or linked(root) or not root.is_dir():
        raise Refused('invalid-root')
    root = root.resolve(strict=True)
    rel = Path(relative)
    if not relative or rel.is_absolute() or rel.drive or '..' in rel.parts:
        raise Refused('invalid-target')
    path = root
    for part in rel.parts:
        path = path / part
        if linked(path):
            raise Refused('linked-target')
    if not path.is_file() or not path.resolve(strict=True).is_relative_to(root):
        raise Refused('target-unavailable')
    return root, path


def identity(info):
    return info.st_dev, info.st_ino


def unchanged_path(root, relative, stream):
    _, path = target_path(root, relative)
    info = os.fstat(stream.fileno())
    if (not stat.S_ISREG(info.st_mode) or info.st_nlink != 1
            or identity(info) != identity(path.stat())):
        raise Refused('target-identity-changed')


@contextmanager
def locked_target(root, relative):
    _, path = target_path(root, relative)
    flags = os.O_RDWR | os.O_APPEND | getattr(os, 'O_BINARY', 0) | getattr(os, 'O_NOFOLLOW', 0)
    flags |= getattr(os, 'O_NONBLOCK', 0)
    fd = os.open(path, flags)
    with os.fdopen(fd, 'r+b', buffering=0) as stream:
        unchanged_path(root, relative, stream)
        if os.name == 'nt':
            import msvcrt
            msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
        elif os.name == 'posix':
            import fcntl
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        else:
            raise Refused('locking-unavailable')
        try:
            unchanged_path(root, relative, stream)
            yield stream
        finally:
            stream.seek(0)
            if os.name == 'nt':
                msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(fd, fcntl.LOCK_UN)


def validate(plan):
    keys = {'schema_version', 'root', 'target', 'before_sha256', 'before_bytes',
            'draft_base64', 'draft_sha256', 'after_sha256'}
    if (not isinstance(plan, dict) or set(plan) != keys
            or type(plan['schema_version']) is not int or plan['schema_version'] != 1):
        raise Refused('invalid-plan')
    if not all(isinstance(plan[k], str) for k in keys - {'schema_version', 'before_bytes'}):
        raise Refused('invalid-plan')
    if type(plan['before_bytes']) is not int or not 0 <= plan['before_bytes'] <= NOTE_LIMIT:
        raise Refused('invalid-plan')
    if not all(re.fullmatch('[0-9a-f]{64}', plan[k]) for k in
               ('before_sha256', 'draft_sha256', 'after_sha256')):
        raise Refused('invalid-plan')
    try:
        draft = base64.b64decode(plan['draft_base64'], validate=True)
    except ValueError:
        raise Refused('invalid-plan') from None
    if not draft or len(draft) > DRAFT_LIMIT or digest(draft) != plan['draft_sha256']:
        raise Refused('invalid-draft')
    utf8(draft)
    return draft


def describe(plan, plan_hash):
    draft = validate(plan)
    _, path = target_path(plan['root'], plan['target'])
    return dict(status='prepared', target=str(path), plan_sha256=plan_hash,
                before_sha256=plan['before_sha256'], draft_sha256=digest(draft),
                draft_bytes=len(draft),
                leading_newline_bytes=len(draft) - len(draft.lstrip(b'\r\n')),
                trailing_newline_bytes=len(draft) - len(draft.rstrip(b'\r\n')),
                draft_text=utf8(draft))


def prepare(root, relative, draft_file, plan_file):
    root, path = target_path(root, relative)
    artifact = Path(plan_file).absolute()
    source = Path(draft_file).resolve(strict=True)
    if artifact.resolve().is_relative_to(root) or source.is_relative_to(root):
        raise Refused('session-artifacts-must-be-outside-vault')
    with source.open('rb') as stream:
        draft = bounded(stream, DRAFT_LIMIT)
    if not draft:
        raise Refused('empty-draft')
    utf8(draft)
    with locked_target(root, relative) as stream:
        original = bounded(stream, NOTE_LIMIT)
        utf8(original)
        unchanged_path(root, relative, stream)
    plan = dict(schema_version=1, root=str(root), target=path.relative_to(root).as_posix(),
                before_sha256=digest(original), before_bytes=len(original),
                draft_base64=base64.b64encode(draft).decode('ascii'),
                draft_sha256=digest(draft), after_sha256=digest(original + draft))
    raw = (json.dumps(plan, sort_keys=True, ensure_ascii=False) + '\n').encode('utf-8')
    fd = os.open(artifact, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_BINARY', 0), 0o600)
    with os.fdopen(fd, 'wb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    return describe(plan, digest(raw))


def load(plan_file, expected):
    if not re.fullmatch('[0-9a-f]{64}', expected):
        raise Refused('invalid-plan-hash')
    with Path(plan_file).open('rb') as stream:
        raw = bounded(stream, PLAN_LIMIT)
    if digest(raw) != expected:
        raise Refused('plan-changed')
    try:
        plan = json.loads(raw)
    except (ValueError, UnicodeError):
        raise Refused('invalid-plan') from None
    return plan, validate(plan)


def apply(plan_file, expected):
    plan, draft = load(plan_file, expected)
    attempted = False
    try:
        with locked_target(plan['root'], plan['target']) as stream:
            original = bounded(stream, NOTE_LIMIT + DRAFT_LIMIT)
            utf8(original)
            # Retry only acknowledges an exact completed result; never writes twice.
            if (len(original) == plan['before_bytes'] + len(draft)
                    and digest(original) == plan['after_sha256']
                    and original.endswith(draft)
                    and digest(original[:plan['before_bytes']]) == plan['before_sha256']):
                return dict(status='already_applied', after_sha256=digest(original), written_bytes=0)
            if len(original) != plan['before_bytes'] or digest(original) != plan['before_sha256']:
                raise Refused('target-changed-fresh-approval-required')
            if digest(original + draft) != plan['after_sha256']:
                raise Refused('invalid-result-hash')
            unchanged_path(plan['root'], plan['target'], stream)
            stream.seek(0, os.SEEK_END)
            attempted = True
            pending = memoryview(draft)
            while pending:
                count = stream.write(pending)
                if not count:
                    raise OSError('short-write')
                pending = pending[count:]
            os.fsync(stream.fileno())
            stream.seek(0)
            actual = bounded(stream, NOTE_LIMIT + DRAFT_LIMIT)
            unchanged_path(plan['root'], plan['target'], stream)
            if actual != original + draft:
                raise Refused('readback-mismatch')
        return dict(status='appended', after_sha256=digest(actual), written_bytes=len(draft))
    except (OSError, Refused) as error:
        if attempted:
            return dict(status='write_unverified', reason=str(error) if isinstance(error, Refused) else 'io-error',
                        write_may_have_occurred=True, retry_safe=False)
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    stage = sub.add_parser('prepare')
    for name in ('root', 'target', 'draft', 'plan'):
        stage.add_argument('--' + name, required=True)
    for name in ('show', 'apply'):
        action = sub.add_parser(name)
        action.add_argument('--plan', required=True)
        action.add_argument('--plan-sha256', required=True)
    args = parser.parse_args()
    try:
        if args.command == 'prepare':
            result = prepare(args.root, args.target, args.draft, args.plan)
        elif args.command == 'show':
            plan, _ = load(args.plan, args.plan_sha256)
            result = describe(plan, args.plan_sha256)
        else:
            result = apply(args.plan, args.plan_sha256)
    except (OSError, Refused) as error:
        result = dict(status='refused', reason=str(error) if isinstance(error, Refused) else 'io-error',
                      write_may_have_occurred=False)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result['status'] in ('prepared', 'appended', 'already_applied') else 3 if result['status'] == 'write_unverified' else 2


if __name__ == '__main__':
    sys.exit(main())
