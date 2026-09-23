#!/usr/bin/env python3
"""Read-only checks for optional lesson plans, approval records and file reviews.

No plan generation, consent authentication, semantic grading, or file writes.
The JSON schema is deliberately separate from the inherited learner state.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
from typing import Any
from tutor_state import StateError, _validate, read_json

ROOT = Path(__file__).resolve().parents[1]
CHECKS = ('scope', 'facts', 'learner_evidence', 'connections', 'meaning',
          'boundaries', 'artifact_mapping', 'interaction')

class ContractError(ValueError):
    pass

def fingerprint(plan: dict[str, Any]) -> str:
    text = json.dumps(plan, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False)
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def validate_relative(value: str) -> None:
    p = PurePosixPath(value)
    if not value.strip() or p.is_absolute() or '..' in p.parts or '\\' in value or re.match(r'^[A-Za-z]:', value):
        raise ContractError(f'Unsafe material path: {value!r}')
    if value in {'.', ''}:
        raise ContractError('Material path must name a file.')

def checked_path(workspace: Path, relative: str) -> Path:
    validate_relative(relative)
    original = workspace.expanduser().absolute()
    # Avoid silently following links in the selected root as well as below it.
    if any(p.is_symlink() for p in [original, *original.parents]):
        raise ContractError('Symlinked workspace path is not accepted for release checks.')
    root = original.resolve()
    if not root.is_dir():
        raise ContractError('Release workspace must be an existing directory.')
    path = root / relative
    current = path
    while current != root:
        if current.is_symlink():
            raise ContractError(f'Symlink in material path: {current}')
        current = current.parent
    if not path.resolve().is_relative_to(root) or not path.is_file():
        raise ContractError(f'Material is missing or outside the workspace: {relative}')
    return path

def check(data: Any, action: str = 'lint', workspace: Path | None = None,
          allow_example: bool = False) -> dict[str, Any]:
    if action not in {'lint','produce','release'}:
        raise ContractError('Unknown action.')
    schema = read_json(ROOT / 'assets/lesson-contract.schema.json')
    try:
        _validate(data, schema, schema)
    except StateError as exc:
        raise ContractError(str(exc)) from exc
    plan = data['plan']
    ids = [m['id'] for m in plan['materials']]
    if len(ids) != len(set(ids)):
        raise ContractError('Duplicate material ID.')
    if len(plan['entrypoints']) != len(set(plan['entrypoints'])):
        raise ContractError('Duplicate entrypoint.')
    if plan['scope'] == 'single' and len(ids) != 1:
        raise ContractError('A single scope must contain exactly one material.')
    paths = [m['path'] for m in plan['materials'] if m['path'] is not None]
    if len(paths) != len(set(paths)):
        raise ContractError('Duplicate material path.')
    for p in paths:
        validate_relative(p)
    approval = data['approval']
    digest = fingerprint(plan)
    if approval is not None and approval['plan_sha256'] != digest:
        raise ContractError('Approval is stale: the plan digest changed.')
    reviews = {r['material_id']:r for r in data['reviews']}
    if len(reviews) != len(data['reviews']) or set(reviews) - set(ids):
        raise ContractError('Review IDs must be unique and refer to planned materials.')
    for r in reviews.values():
        validate_relative(r['path'])
    needs_approval = plan['approval_mode'] == 'preview' or plan['scope'] == 'series'
    if action != 'lint':
        if data['example'] and not allow_example:
            raise ContractError('Synthetic examples cannot authorize real production.')
        if not plan['user_request_locator'] or not plan['user_request_locator'].strip():
            raise ContractError('A real user request locator is required.')
        if needs_approval and approval is None:
            raise ContractError('This scope requires a concrete plan approval or explicit one-off exception.')
        if approval and not approval['user_message_locator'].strip():
            raise ContractError('Approval needs a real user message locator.')
    if action == 'release':
        if workspace is None:
            raise ContractError('--workspace is required for release checks.')
        if set(reviews) != set(ids):
            raise ContractError('Every planned material needs a review.')
        for material in plan['materials']:
            review = reviews[material['id']]
            if material['path'] is None:
                raise ContractError('Chat-only materials have no file release check; do not claim file verification.')
            if review['path'] != material['path']:
                raise ContractError('Review path does not match the approved plan.')
            actual = hashlib.sha256(checked_path(workspace, material['path']).read_bytes()).hexdigest()
            if actual != review['sha256']:
                raise ContractError(f'Review hash is stale: {material["id"]}')
            for name in CHECKS:
                item = review['checks'][name]
                if item['verdict'] == 'pass':
                    if not item['location'] or not item['location'].strip():
                        raise ContractError(f'{name}: pass needs a concrete review location.')
                elif item['verdict'] == 'not_applicable':
                    if name != 'artifact_mapping' or 'artifact' in plan['entrypoints']:
                        raise ContractError(f'{name}: cannot bypass this required check as not_applicable.')
                else:
                    raise ContractError(f'{name}: release blocked by {item["verdict"]}.')
                if not item['reason'].strip():
                    raise ContractError(f'{name}: a nonblank reason is required.')
    return {'status':f'{action}_contract_valid','plan_sha256':digest,
            'requires_explicit_approval':needs_approval,'material_count':len(ids),
            'limits':'Structure and hashes only; not approval authenticity, content truth, or learning outcomes.'}

def main(argv: list[str] | None = None) -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('contract',type=Path)
    parser.add_argument('--action',choices=['lint','produce','release'],default='lint')
    parser.add_argument('--workspace',type=Path)
    parser.add_argument('--fingerprint',action='store_true',help='Print the plan digest after lint; does not approve it.')
    parser.add_argument('--allow-example',action='store_true',help='Synthetic tests only; never a user approval.')
    args=parser.parse_args(argv)
    try:
        data=read_json(args.contract)
        result=check(data,args.action,args.workspace,args.allow_example)
        print(result['plan_sha256'] if args.fingerprint else json.dumps(result,ensure_ascii=False,indent=2))
        return 0
    except (ContractError,StateError,OSError) as exc:
        print(f'Contract error: {exc}',file=sys.stderr)
        return 2

if __name__=='__main__':
    raise SystemExit(main())
