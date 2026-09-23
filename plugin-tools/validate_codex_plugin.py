#!/usr/bin/env python3
"""Offline checks for this skills-only distribution; not an official host validator."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
NAME = 'adaptive-learning-tutor'


def local_path(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative.startswith('./'):
        raise ValueError('Path must start with ./')
    parts = Path(relative).parts
    if '..' in parts or Path(relative).is_absolute():
        raise ValueError('Path traversal is not allowed')
    current = root
    for part in parts:
        current = current / part
        if current.is_symlink():
            raise ValueError('Symlinks are not allowed in distribution paths')
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()) or not path.exists():
        raise ValueError('Path missing or outside distribution root')
    return path


def validate(root: Path = ROOT) -> dict:
    root = root.resolve()
    catalog = json.loads((root / '.agents/plugins/marketplace.json').read_text(encoding='utf-8'))
    if catalog['name'] != 'rengod95-learning' or not catalog['interface']['displayName']:
        raise ValueError('Unexpected marketplace identity')
    entries = catalog['plugins']
    if len(entries) != 1 or entries[0]['name'] != NAME:
        raise ValueError('Expected exactly the requested plugin')
    entry = entries[0]
    if entry['source']['source'] != 'local':
        raise ValueError('Expected repository-local plugin source')
    if entry['policy'] != {'installation': 'AVAILABLE', 'authentication': 'ON_INSTALL'}:
        raise ValueError('Unexpected marketplace policy')
    if entry['category'] != 'Productivity':
        raise ValueError('Unexpected category')
    plugin = local_path(root, entry['source']['path'])
    manifest = json.loads((plugin / '.codex-plugin/plugin.json').read_text(encoding='utf-8'))
    if manifest['name'] != NAME or manifest['version'] != '0.3.1':
        raise ValueError('Unexpected plugin identity/version')
    if {'apps', 'mcpServers', 'hooks'} & manifest.keys():
        raise ValueError('This distribution must remain skills-only')
    for p in plugin.rglob('*'):
        if p.is_symlink():
            raise ValueError('Unexpected symlink')
        if p.name in {'.app.json', '.mcp.json', 'mcp.json', 'hooks.json'}:
            raise ValueError('Unexpected server or hook configuration')
    skill_root = local_path(plugin, manifest['skills'])
    skill = skill_root / NAME
    if not (skill / 'SKILL.md').is_file():
        raise ValueError('Skill entrypoint missing')
    settings = json.loads((skill / 'assets/settings.default.json').read_text(encoding='utf-8'))
    if settings.get('approval_mode') != 'preview':
        raise ValueError('Original preview policy must be preserved')
    checksum_file = skill / 'SHA256SUMS'
    listed = set()
    for line in checksum_file.read_text(encoding='utf-8').splitlines():
        match = re.fullmatch(r'([a-f0-9]{64})  (.+)', line)
        if not match:
            raise ValueError('Malformed core checksum record')
        digest, relative = match.groups()
        path = local_path(skill, './' + relative)
        if relative in listed or not path.is_file():
            raise ValueError('Duplicate or invalid core checksum path')
        listed.add(relative)
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError('Core checksum mismatch: ' + relative)
    actual = {p.relative_to(skill).as_posix() for p in skill.rglob('*')
              if p.is_file() and '__pycache__' not in p.parts
              and p.suffix not in {'.pyc', '.pyo'} and p.name != 'SHA256SUMS'}
    if actual != listed or len(listed) != 45:
        raise ValueError('Original core inventory was changed')
    return {'status': 'passed', 'plugin': NAME, 'plugin_version': manifest['version'],
            'core_files_verified': len(listed) + 1, 'marketplace': catalog['name'],
            'host_installation_tested': False, 'model_behavior_tested': False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        print(json.dumps(validate(args.root), ensure_ascii=False, indent=2))
        return 0
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print('ERROR: ' + str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
