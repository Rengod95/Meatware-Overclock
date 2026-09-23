#!/usr/bin/env python3
"""Copy this skill to an explicitly selected local discovery directory.

Python 3.10+, standard library only. Default is a no-write preview.
No downloads, subprocesses, shell/profile edits, telemetry, or overwrite option.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
from typing import Any

NAME = 'adaptive-learning-tutor'
SOURCE = Path(__file__).resolve().parents[1]
PATHS = {'codex': '.agents/skills', 'claude': '.claude/skills',
         'gemini': '.gemini/skills', 'pi': '.agents/skills'}

class InstallError(ValueError):
    pass

def no_symlink_components(path: Path) -> None:
    for item in [path, *path.parents]:
        if item.is_symlink():
            raise InstallError(f'Symlink path component is not accepted: {item}')

def inventory(root: Path) -> dict[str, str]:
    """Hash ordinary package files, omitting Python caches only."""
    if root.is_symlink() or not root.is_dir():
        raise InstallError(f'Expected an ordinary directory: {root}')
    out: dict[str, str] = {}
    for base, dirs, files in os.walk(root, followlinks=False):
        here = Path(base)
        # Inspect symlinks even where a cache name would otherwise be ignored.
        for name in dirs + files:
            p = here / name
            if p.is_symlink():
                raise InstallError(f'Symlink in skill tree: {p}')
        dirs[:] = sorted(d for d in dirs if d != '__pycache__')
        for name in sorted(files):
            p = here / name
            if p.suffix in {'.pyc', '.pyo'}:
                continue
            if not p.is_file():
                raise InstallError(f'Not an ordinary file: {p}')
            out[p.relative_to(root).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out

def destination(agent: str, scope: str, project: Path | None = None,
                dest: Path | None = None, home: Path | None = None) -> Path:
    if agent == 'custom':
        if dest is None:
            raise InstallError('--agent custom requires --dest (the skills parent directory).')
        if project is not None:
            raise InstallError('--project cannot be combined with --agent custom.')
        parent = Path(os.path.abspath(dest.expanduser()))
    else:
        if agent not in PATHS:
            raise InstallError(f'Unknown agent: {agent}')
        if dest is not None:
            raise InstallError('--dest is only accepted with --agent custom.')
        if scope == 'project':
            if project is None:
                raise InstallError('--scope project requires --project with an existing directory.')
            base = project.expanduser().resolve()
            if not base.is_dir():
                raise InstallError(f'Project directory does not exist: {base}')
        elif scope == 'user':
            if project is not None:
                raise InstallError('--project requires --scope project.')
            base = (home or Path.home()).expanduser().resolve()
            if not base.is_dir():
                raise InstallError(f'Home directory does not exist: {base}')
        else:
            raise InstallError(f'Unknown scope: {scope}')
        parent = base / PATHS[agent]
    target = parent / NAME
    no_symlink_components(target)
    return target

def install(target: Path, apply: bool = False, source: Path = SOURCE) -> dict[str, Any]:
    source = source.resolve()
    no_symlink_components(target)
    target = Path(os.path.abspath(target))
    if target != source and (target.is_relative_to(source) or source.is_relative_to(target)):
        raise InstallError('Source and destination must not contain each other.')
    expected = inventory(source)
    if 'SKILL.md' not in expected:
        raise InstallError('Source does not contain SKILL.md.')
    result: dict[str, Any] = {'source': str(source), 'destination': str(target),
                              'file_count': len(expected), 'writes_performed': False}
    if target.exists():
        if target.is_dir() and inventory(target) == expected:
            result['status'] = 'already_installed'
            return result
        raise InstallError('A different installation already exists. Nothing was overwritten. '
                           'Move the old skill outside all discovery directories, then install again.')
    if not apply:
        result['status'] = 'preview_only'
        return result
    target.parent.mkdir(parents=True, exist_ok=True)
    no_symlink_components(target)
    lock = target.parent / f'.{NAME}.install.lock'
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise InstallError('An installation lock already exists; inspect it before retrying.') from exc
    stage: Path | None = None
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as handle:
            handle.write(f'pid={os.getpid()}\n')
        if target.exists() or target.is_symlink():
            raise InstallError('Destination appeared during installation; retry after inspection.')
        stage = Path(tempfile.mkdtemp(prefix=f'.{NAME}.stage-', dir=target.parent))
        shutil.copytree(source, stage, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '*.pyo'))
        if inventory(stage) != expected:
            raise InstallError('Staged files differ from the source snapshot.')
        no_symlink_components(target)
        if target.exists():
            raise InstallError('Destination appeared during staging; nothing was replaced.')
        os.rename(stage, target)
        stage = None
        result.update(status='installed', writes_performed=True)
        return result
    finally:
        if stage is not None:
            shutil.rmtree(stage)
        lock.unlink(missing_ok=True)

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--agent', choices=[*PATHS, 'custom'], required=True)
    parser.add_argument('--scope', choices=['user', 'project'], default='user')
    parser.add_argument('--project', type=Path)
    parser.add_argument('--dest', type=Path, help='Custom skills parent, NOT final skill folder.')
    parser.add_argument('--apply', action='store_true', help='Perform the copy; otherwise preview only.')
    args = parser.parse_args(argv)
    try:
        target = destination(args.agent, args.scope, args.project, args.dest)
        print(json.dumps(install(target, args.apply), ensure_ascii=False, indent=2))
        return 0
    except (OSError, InstallError) as exc:
        print(f'Install error: {exc}', file=sys.stderr)
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
