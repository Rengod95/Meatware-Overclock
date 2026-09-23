#!/usr/bin/env python3
"""Offline structural validation for this package (not a universal Skill/YAML linter)."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any
from build_standalone import render
from check_contract import check
from tutor_state import StateError, read_json, validate_state

ROOT=Path(__file__).resolve().parents[1]

class PackageError(ValueError):
    pass

def yaml_subset(text: str) -> dict[str,Any]:
    """Read the scalar/nested-map YAML subset deliberately used by this package.

Reject unsupported constructs rather than silently ignoring them. No YAML tags,
anchors, arrays, scripts, block scalars or dynamic interpolation are executed.
"""
    root: dict[str,Any]={}
    stack: list[tuple[int,dict[str,Any]]]=[(-2,root)]
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith('#'):continue
        indent=len(line)-len(line.lstrip(' '))
        if '\t' in line or indent%2:raise PackageError('Unsupported YAML indentation.')
        match=re.fullmatch(r' *([A-Za-z_][A-Za-z0-9_-]*):(?: (.*))?',line)
        if not match:raise PackageError(f'Unsupported YAML syntax: {line!r}')
        key,value=match.groups()
        while stack and stack[-1][0]>=indent:stack.pop()
        if not stack or indent!=stack[-1][0]+2:raise PackageError('Invalid YAML nesting.')
        parent=stack[-1][1]
        if key in parent:raise PackageError(f'Duplicate YAML key: {key}')
        if value is None or value=='':
            child: dict[str,Any]={};parent[key]=child;stack.append((indent,child));continue
        if value.startswith('"'):
            try:parsed=json.loads(value)
            except json.JSONDecodeError as exc:raise PackageError('Invalid quoted YAML scalar.') from exc
            if not isinstance(parsed,str):raise PackageError('Expected string scalar.')
        elif value in ('true','false'):parsed=value=='true'
        elif re.fullmatch(r'[A-Za-z0-9_.-]+',value):parsed=value
        else:raise PackageError(f'Quote this YAML scalar: {value!r}')
        parent[key]=parsed
    return root

def visible_markdown(text: str) -> str:
    out=[];fence: str|None=None
    for line in text.splitlines():
        m=re.match(r'^\s*(`{3,}|~{3,})',line)
        if m:
            mark=m.group(1)
            if fence is None:fence=mark
            elif mark[0]==fence[0] and len(mark)>=len(fence):fence=None
            continue
        if fence is None:out.append(line)
    if fence is not None:raise PackageError('Unclosed Markdown code fence.')
    return '\n'.join(out)

def verify_hashes(root: Path) -> int:
    path=root/'SHA256SUMS'
    if not path.is_file():raise PackageError('SHA256SUMS is missing.')
    recorded=set()
    for line in path.read_text(encoding='utf-8').splitlines():
        match=re.fullmatch(r'([0-9a-f]{64})  (.+)',line)
        if not match:raise PackageError('Invalid checksum record.')
        expected,relative=match.groups();p=root/relative
        if relative in recorded or not p.resolve().is_relative_to(root.resolve()) or p.is_symlink():
            raise PackageError('Duplicate or unsafe checksum path.')
        recorded.add(relative)
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=expected:
            raise PackageError(f'Checksum mismatch: {relative}')
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()
            and '__pycache__' not in p.parts and p.suffix not in {'.pyc','.pyo'} and p.name!='SHA256SUMS'}
    if actual != recorded:raise PackageError('Checksum inventory differs from package file inventory.')
    return len(recorded)

def validate(root: Path=ROOT, integrity: bool=False) -> dict[str,Any]:
    required=['SKILL.md','SYSTEM_PROMPT.md','README.md','agents/openai.yaml',
              'assets/settings.default.json','assets/default-state.json','assets/state.schema.json',
              'assets/lesson-contract.schema.json','assets/lesson-contract.template.json',
              'evals/cases.json','docs/COMPATIBILITY.md','docs/PROVENANCE.md','VALIDATION.md']
    for relative in required:
        if not (root/relative).is_file():raise PackageError(f'Missing required file: {relative}')
    source=(root/'SKILL.md').read_text(encoding='utf-8')
    parts=source.split('---',2)
    if len(parts)!=3 or parts[0].strip():raise PackageError('Expected YAML frontmatter at start.')
    meta=yaml_subset(parts[1])
    if set(meta)-{'name','description','compatibility','metadata','license','allowed-tools'}:
        raise PackageError('Unexpected frontmatter keys.')
    name=meta.get('name','');description=meta.get('description','')
    if not isinstance(name,str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',name) or len(name)>64 or name!=root.name:
        raise PackageError('Skill name must match its directory and portable naming constraints.')
    if not isinstance(description,str) or not 1<=len(description)<=1024:raise PackageError('Invalid description length.')
    if not 1<=len(meta.get('compatibility',''))<=500:raise PackageError('Invalid compatibility length.')
    if len(source.splitlines())>=500:raise PackageError('Keep this SKILL.md below 500 lines.')
    if meta.get('metadata',{}).get('version')!='0.3.0':raise PackageError('Unexpected package version.')
    ui=yaml_subset((root/'agents/openai.yaml').read_text(encoding='utf-8'))
    if '$adaptive-learning-tutor' not in ui['interface']['default_prompt']:raise PackageError('UI prompt must name this skill.')
    if not isinstance(ui['policy']['allow_implicit_invocation'],bool):raise PackageError('Invocation policy must be boolean.')
    settings=read_json(root/'assets/settings.default.json')
    if settings['approval_mode'] not in {'adaptive','preview'}:raise PackageError('Invalid approval mode.')
    if settings['persistent_storage'] or settings['require_artifact'] or settings['require_fixed_length']:
        raise PackageError('Defaults must not require persistence, artifacts, or fixed length.')
    state=read_json(root/'assets/default-state.json');validate_state(state)
    if state['authorization']['persistent_storage'] or state['claims'] or state['evidence'] or state['profile']['provenance']:
        raise PackageError('Default learner state must contain no personal claims, evidence or consent.')
    check(read_json(root/'assets/lesson-contract.template.json'),'lint')
    if (root/'SYSTEM_PROMPT.md').read_text(encoding='utf-8')!=render(root):raise PackageError('Standalone prompt is stale.')
    links=0;json_count=0;md_count=0
    for p in root.rglob('*'):
        if p.is_symlink():raise PackageError(f'Unexpected symlink: {p}')
        if '__pycache__' in p.parts:continue
        if p.is_file() and p.suffix=='.json':read_json(p);json_count+=1
        if p.is_file() and p.suffix=='.md':
            md_count+=1;text=p.read_text(encoding='utf-8')
            if '\ufffd' in text or '\x00' in text:raise PackageError(f'Invalid text: {p}')
            for target in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)',visible_markdown(text)):
                if re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:',target) or target.startswith('#'):continue
                linked=p.parent/target.split('#')[0]
                if not linked.resolve().is_relative_to(root.resolve()) or not linked.exists():
                    raise PackageError(f'Missing or escaping link: {p.relative_to(root)} -> {target}')
                links+=1
    cases=read_json(root/'evals/cases.json')['cases'];ids=[c['id'] for c in cases]
    if len(ids)!=len(set(ids)) or len(cases)<20:raise PackageError('Behavior cases must be unique and sufficiently broad.')
    checksum_count=verify_hashes(root) if integrity else None
    return {'status':'structural_checks_passed','skill':name,'version':'0.3.0',
            'skill_lines':len(source.splitlines()),'markdown_files':md_count,'json_files':json_count,
            'relative_links':links,'behavioral_cases_designed':len(cases),'checksum_records_verified':checksum_count,
            'limits':'Not an official host certification, semantic evaluation, or learning-outcome test.'}

def main(argv: list[str] | None=None) -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--integrity',action='store_true',help='Also verify SHA256SUMS and exact package inventory.')
    args=parser.parse_args(argv)
    try:
        print(json.dumps(validate(integrity=args.integrity),ensure_ascii=False,indent=2));return 0
    except (ValueError,OSError,KeyError,TypeError) as exc:
        print(f'Package validation error: {exc}',file=sys.stderr);return 2

if __name__=='__main__':raise SystemExit(main())
