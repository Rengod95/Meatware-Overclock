#!/usr/bin/env python3
"""Build/check the portable text-only fallback from canonical skill instructions."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PARTS = ['SKILL.md', 'references/routing.md', 'references/teaching-writing.md',
         'references/curriculum.md', 'references/approval.md', 'references/artifact-debug.md',
         'references/review.md']

def render(root: Path = ROOT) -> str:
    source = (root/'SKILL.md').read_text(encoding='utf-8')
    body = source.split('---',2)[2].strip()
    before = body.split('## 필요한 참조만 선택한다')[0].strip()
    middle = '## 요청마다 수행할 판단' + body.split('## 요청마다 수행할 판단',1)[1].split('## 선택적 로컬 도구')[0]
    sections = [before,middle.strip()]
    for name in PARTS[1:]:
        text = (root/name).read_text(encoding='utf-8')
        if name == 'references/approval.md':
            text=text.split('## 선택적 검사')[0]
        sections.append(text.strip())
    settings=json.loads((root/'assets/settings.default.json').read_text(encoding='utf-8'))
    digest=hashlib.sha256(b''.join((root/p).read_bytes() for p in [*PARTS, 'assets/settings.default.json'])).hexdigest()
    header=f'''# Adaptive Learning Tutor — standalone 0.3.0

Generated from canonical package instructions. Source bundle SHA-256: `{digest}`.
This is the text-only alternative, not an additional instruction layer to load with SKILL.md.
파일 도구가 없는 환경에서는 아래 지침만 사용한다. 실제 파일 접근·실행·영속 기억을 제공하지 않는다.
설정의 기본값은 {settings['approval_mode']}/{settings['instruction_mode']}/한국어/장기 누적은 요청 시이며, 실제 사용자 선호가 우선한다.

'''
    text=header+'\n\n---\n\n'.join(sections)+'\n'
    text=text.replace('`assets/settings.default.json`은 운영 기본값이지 사용자 지식 관찰 기록이 아니다.',
                      '이 독립형 지침의 설정은 운영 기본값이지 사용자 지식 관찰 기록이 아니다.')
    text=text.replace('`assets/work-handoff.template.json`은 코드뿐 아니라 문서·개념·아키텍처·프로젝트 파운데이션에 사용할 수 있다.',
                      '업무 인계에는 코드뿐 아니라 문서·개념·아키텍처·프로젝트 파운데이션을 포함할 수 있다.')
    return text

def main(argv: list[str] | None=None) -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--write',action='store_true',help='Update SYSTEM_PROMPT.md; default only checks.')
    args=p.parse_args(argv)
    expected=render();target=ROOT/'SYSTEM_PROMPT.md'
    if args.write:
        target.write_text(expected,encoding='utf-8');print('SYSTEM_PROMPT.md generated.');return 0
    if not target.exists() or target.read_text(encoding='utf-8') != expected:
        print('Standalone prompt is missing or stale.',file=sys.stderr);return 2
    print('Standalone prompt matches canonical sources.');return 0

if __name__=='__main__':raise SystemExit(main())
