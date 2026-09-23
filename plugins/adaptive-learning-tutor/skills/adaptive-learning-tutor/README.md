# Adaptive Learning Tutor 0.3.0

**개념 질문·독립 심화·낯선 분야·문제 해결·산출물 후학습을 위한 개인용 학습 스킬.**

기존 Learning Design Orchestrator와 Sustainable Learning Tutor의 규칙을 하나의 진입점으로 통합했다. 산출물이 없어도 시작하며, 몇 문단부터 긴 논증까지 이번 질문에 필요한 크기로 설명한다. 읽기 중심이고, 퀴즈·실습·장기 기록은 자동으로 요구하지 않는다.

이 폴더 자체가 설치 단위다. 표준 진입점은 [SKILL.md](SKILL.md), 파일 없는 환경은 [SYSTEM_PROMPT.md](SYSTEM_PROMPT.md)를 사용한다. 두 파일을 동시에 상위 지침으로 적재하지 않는다.

## 바로 설치하기

Python 3.10+는 **설치·검사·선택적 로컬 기록 도구에만** 필요하다. 스킬을 읽어 적용하는 데 Python이나 API 키가 필요하지 않다. 설치 프로그램은 네트워크·셸 프로필·호스트 설정 파일을 변경하지 않는다.

압축을 해제해 `adaptive-learning-tutor` 폴더가 보이는 상위 폴더에서 실행한다.

```bash
# Codex 사용자 스킬 경로: 먼저 목적지와 파일 수만 확인 (쓰기 없음)
python3 adaptive-learning-tutor/scripts/install.py --agent codex --scope user

# 확인한 경로에 실제 복사
python3 adaptive-learning-tutor/scripts/install.py --agent codex --scope user --apply
```

프로젝트 전용 설치는 프로젝트의 절대 경로를 명시한다.

```bash
python3 adaptive-learning-tutor/scripts/install.py --agent codex --scope project --project /absolute/path/to/project --apply
```

다른 호스트도 같은 본체를 사용한다.

```bash
python3 adaptive-learning-tutor/scripts/install.py --agent claude --scope user --apply
python3 adaptive-learning-tutor/scripts/install.py --agent gemini --scope user --apply
python3 adaptive-learning-tutor/scripts/install.py --agent pi --scope user --apply
```

Codex와 Pi 대상은 이 패키지에서 동일한 `.agents/skills` 부모를 사용한다. 같은 위치·같은 내용은 `already_installed`로 종료한다. Gemini도 `.agents/skills`를 발견할 수 있으므로 이미 공유 경로에 설치했다면 중복 설치 대신 호스트 목록에서 확인한다. 호스트 관리 정책에 따라 인식·사용이 제한될 수 있다. 경로와 공식 근거는 [호환성 안내](docs/COMPATIBILITY.md)에 있다.

일반 폴더 복사로 설치할 수도 있다. 최종 구조는 반드시 `호스트의-skills-폴더/adaptive-learning-tutor/SKILL.md`다. ZIP 파일 자체나 SKILL.md 한 파일만 넣으면 참조·도구를 놓칠 수 있다.

## 호출

Codex CLI/IDE에서는 `/skills`로 확인하거나 다음처럼 명시적으로 호출한다.

```text
$adaptive-learning-tutor
빌더 패턴을 현재 프로젝트와 무관하게 깊이 설명해 줘.
필요성과 의도, 표현의 차이, 적용하지 않는 조건까지 연결해 줘.
이번 설명은 제작안 없이 바로 제공하고, 장기 저장은 하지 마.
```

Claude Code는 `/adaptive-learning-tutor`, Pi는 `/skill:adaptive-learning-tutor`를 사용한다. Gemini CLI는 `/skills list`와 필요시 `/skills reload`로 확인하고, 자연어로 이 스킬의 사용을 요청한다. 발견과 활성화는 호스트가 담당하며 이 패키지가 이를 강제로 보장하지 않는다.

## 기본 동작과 개인화

| 항목 | 기본값 | 변경 방법 |
|---|---|---|
| 언어 | 한국어, 현재 사용자 언어 요청 우선 | 대화에서 지정 |
| 상호작용 | 읽기형 해설, 실습·퀴즈 강제 없음 | 해당 세션에서 선택적 점검 요청 |
| 분량 | 질문을 완결할 적정 크기, 고정 페이지 수 없음 | 몇 문단/몇 장/깊이 요구 지정 |
| 제작 전 확인 | 기존 선호를 보존하는 `preview` | `adaptive`를 명시적으로 선택하거나 이번 요청만 예외 지정 |
| 장기 경로 | 요청 시 연결 | 분야 지도·누적 학습을 요청 |
| 개인 저장 | 비활성 | 별도 경로와 보존을 실제로 승인한 경우만 초기화 |

기본 `preview`는 새 학습 자료 전에 크기에 맞는 짧은 제작안을 보여 준다. 승인한 범위의 작성·국소 복구에는 같은 승인을 반복하지 않는다. 선택 가능한 `adaptive`에서는 명시적으로 요청한 한 편·지도·국소 설명을 바로 제공하고, 여러 편 본제작·큰 경로 실행·범위 확대만 확인받는다. **단순 설치를 기존 선호 철회나 개인 정보 저장 동의로 취급하지 않는다.**

예: “이번 세션은 항상 짧은 제작안을 먼저 보여 줘”, “작은 설명은 바로 작성하고 과정 설계만 확인해 줘”, “기존 업무와 연결하지 말아 줘”라고 지정할 수 있다. 대화의 선택과 영속 설정 변경은 별개다. [정책 상세](references/approval.md)를 참조한다.

## 구성

`SKILL.md`는 짧은 핵심과 필요한 참조의 선택 규칙이다. `references/`는 진입점·진단·글쓰기·장르·누적·승인·업무/디버깅·검수·상태 모듈이다. `assets/`는 필수가 아닌 빈 양식과 기본값이다. `examples/`는 가상 독서 경험과 호출 예시, `evals/`는 행동 평가 입력이다.

선택적 코드 도구는 설치, 구조 검사, 제작 계약 검사, 로컬 상태 저장, 독립형 프롬프트 생성/동기 확인이다. 도구 실행을 학습 요청의 필수 단계로 만들지 않는다.

## 검증

스킬 폴더 안에서 실행한다.

```bash
python3 scripts/validate_package.py
# 배포본 파일 무결성도 확인
python3 scripts/validate_package.py --integrity
python3 -m unittest discover -s tests -v
python3 scripts/build_standalone.py
python3 scripts/check_contract.py assets/lesson-contract.template.json --action lint
```

마지막 템플릿은 가상 예시라 `--action produce`에서는 기본 거부된다. 이는 예상된 동작이다. 실제 테스트 결과와 하지 않은 검증은 [VALIDATION.md](VALIDATION.md)에 있다. 형식·코드 테스트는 실제 에이전트의 설명 품질이나 사용자의 이해를 보증하지 않는다.

## 로컬 누적 기록

사용자 요청과 보존 동의가 있을 때만 [상태 안내](references/state.md)에 따라 스킬 폴더 **밖의** 새 작업 공간을 만든다. 패키지 설치는 개인 기록을 만들지 않는다. 상태 스키마는 원본 Tutor 0.1.0을 유지하며, Orchestrator 상태와 자동 병합하지 않는다. [통합·이전 안내](docs/INTEGRATION.md)를 참조한다.

## 업데이트·제거

설치기는 다른 내용의 기존 폴더를 덮어쓰지 않는다. 수정한 파일을 보존하고 기존 폴더를 모든 스킬 검색 경로 밖으로 이동한 뒤 새 버전을 설치한다. 검색 경로 안에 `-backup`으로 남기면 중복 스킬로 발견될 수 있다. 제거는 설치 위치의 이 스킬 폴더만 호스트 방식으로 제거한다. 별도 개인 기록은 자동 삭제되지 않는다.

스킬 검색 목록에 이전 두 원본이 함께 있으면 같은 요청에 상충하는 승인/기록 정책이 적용될 수 있다. 새 통합본을 선택하고 이전 스킬은 필요에 따라 호스트에서 비활성화하거나 검색 경로 밖에 보관한다. 이 패키지는 원본을 임의로 삭제·비활성화하지 않는다.
