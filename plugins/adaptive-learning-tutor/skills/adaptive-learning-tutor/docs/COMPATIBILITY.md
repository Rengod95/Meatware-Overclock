# 호스트 호환성과 실제 검증 수준

문서 확인일: **2026-09-23**. 아래는 해당 날짜의 공식 문서가 안내한 로컬 스킬 규격과 경로다. 실제 설치된 호스트의 버전·관리 정책·파일 접근권한에 따라 다를 수 있다. 이 패키지는 마켓플레이스 등록 플러그인, MCP 서버, Codex 확장 런타임이 아니라 로컬 스킬 폴더다.

| 대상 | 사용자 설치 부모 | 프로젝트 설치 부모 | 호출/발견 |
|---|---|---|---|
| Codex CLI/IDE | `~/.agents/skills` | `<project>/.agents/skills` | `/skills`, `$adaptive-learning-tutor` |
| Claude Code | `~/.claude/skills` | `<project>/.claude/skills` | `/adaptive-learning-tutor` |
| Gemini CLI | `~/.gemini/skills` 또는 `~/.agents/skills` | `<project>/.gemini/skills` 또는 `.agents/skills` | `/skills list`, `/skills reload`, 자연어 활성화 |
| Pi | `~/.agents/skills` (공통 경로) | `<project>/.agents/skills` | `/skill:adaptive-learning-tutor`, 편집 뒤 `/reload` |
| 그 외 Agent Skills 호스트 | 해당 호스트가 실제로 읽는 경로 | 동일 | 호스트 명세 확인 후 폴더 복사 |
| 스킬 로더 없는 에이전트 | 파일을 읽을 수 있으면 SKILL.md 명시적 적용 | 불필요 | 불가능하면 SYSTEM_PROMPT.md를 지침으로 제공 |

OpenAI 문서의 기존 주소는 현재 공식 ChatGPT Learn 문서로 이동한다. Codex의 사용자 경로를 옛 경로로 추정하지 않고 현재 문서의 `.agents/skills`를 사용했다. `agents/openai.yaml`에는 표시 정보와 암시적 호출 허용만 있으며, 외부 도구 의존성·자동 실행 명령은 넣지 않았다.

Codex와 Pi를 같은 공통 경로에 설치하면 본체는 한 사본이다. Gemini는 공통 경로도 읽고 같은 범위 안에서는 공통 경로가 전용 경로보다 우선할 수 있으므로, 여러 사본을 두기 전에 목록을 확인한다. Claude Code는 전용 경로의 같은 본체를 사용한다. 사용자 로컬 폴더만으로 클라우드·원격 세션에 자동 동기화된다고 주장하지 않는다.

Oh My Pi 등 다른 파생 호스트의 경로를 Pi와 같다고 가정하지 않는다. 해당 버전의 설정을 확인해 `--agent custom --dest /actual/skills-parent`로 설치하거나 SKILL.md를 명시적으로 읽게 한다. 특정 호스트의 공식 설치 경로를 확인했다는 주장과 범용 텍스트 적용은 별개의 호환 수준이다.

## 필요한 권한

일반 해설은 읽기만으로 가능하다. 로컬 도구는 Python 3.10+와 파일 권한이 필요하다. 전문 사실 조사·문서 제작·실제 디버깅 실행은 호스트가 가진 도구를 이용한다. 스킬에는 API 키, 고정 모델, 자동 다운로드, telemetry, hooks, 임의 명령 실행 frontmatter를 포함하지 않았다.

설치기의 dry-run은 쓰지 않는다. `--apply`는 이 패키지만 복사하고 `AGENTS.md`, `CLAUDE.md`, shell 설정, 기존 스킬, 학습 기록을 수정하지 않는다. 심볼릭 링크가 있는 설치 경로는 보수적으로 거부한다. 사용자가 링크 기반 dotfiles를 쓰는 경우 실제 디렉터리를 확인해 custom 경로 또는 직접 복사를 선택한다. 이 제한은 악의적인 동시 파일시스템 공격을 막는 보안 샌드박스를 의미하지 않는다.

## 공식 확인 자료

아래 주소는 설치 위치와 규격의 근거다. 교육 효과의 근거가 아니다.

```text
Agent Skills specification
https://agentskills.io/specification

OpenAI — Build skills (공식 주소의 리다이렉트 포함)
https://developers.openai.com/codex/skills
https://learn.chatgpt.com/docs/build-skills

Anthropic — Claude Code skills
https://code.claude.com/docs/en/skills

Google — Gemini CLI Agent Skills
https://geminicli.com/docs/cli/skills/

Pi — maintainer documentation (기존 badlogic/pi-mono 주소에서 이동)
https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/skills.md
```

메타데이터·스킬 디렉터리 구조·설치 복사·계약·상태 테스트는 로컬에서 검사한다. Codex/Claude/Gemini/Pi 모델을 실제로 호출하는 종단 간 시험은 수행하지 않았다. 지원 경로를 구현했다는 사실을 모든 버전의 실행 인증으로 표현하지 않는다.
