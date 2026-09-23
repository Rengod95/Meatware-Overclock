# Adaptive Learning Tutor — Codex plugin 0.3.1

기존 Adaptive Learning Tutor 0.3.0 스킬을 변경하지 않고 Codex 플러그인으로 포장한 배포판입니다. 스킬 본체·참조·선택적 Python 도구·테스트·기존 검증 기록 46개 파일을 `skills/adaptive-learning-tutor/`에 보존했습니다. 플러그인 포장 버전과 학습 코어 버전은 별개입니다.

## Codex 데스크톱에 등록하고 설치

터미널에서 실행합니다. 아래 명령은 마켓플레이스 등록이며 설치·활성화 완료를 뜻하지 않습니다.

```bash
codex plugin marketplace add Rengod95/Meatware-Overclock --ref codex/adaptive-learning-tutor-plugin
codex plugin marketplace list
```

그다음 Codex/ChatGPT 데스크톱 앱을 완전히 종료한 뒤 다시 실행합니다. Plugins Directory에서 소스 **Rengod95 Learning**을 선택하고 **Adaptive Learning Tutor**를 설치합니다. 설치한 플러그인을 새 대화의 사용 플러그인 목록에서 선택합니다. 화면 명칭과 사용 가능 여부는 앱 버전·계정·워크스페이스 정책에 따라 다를 수 있습니다.

`codex plugin marketplace` 명령을 지원하지 않는 설치에서는 이 브랜치를 체크아웃한 저장소를 Codex 프로젝트로 열어 저장소 범위의 `.agents/plugins/marketplace.json`을 사용합니다. 명령 지원 여부는 `codex plugin marketplace --help`로 확인합니다. 존재가 확인되지 않은 별도의 `plugin install` 명령이나 캐시 설정을 직접 쓰지 않습니다.

ZIP으로 받은 경우에는 압축을 푼 **마켓플레이스 루트**를 `codex plugin marketplace add /absolute/path/to/marketplace-root`로 등록할 수 있습니다. `.agents/plugins` 하위 경로나 스킬 폴더를 루트 대신 전달하지 마세요.

## 사용

```text
Adaptive Learning Tutor를 사용해 빌더 패턴의 의도와 표현을 구분해서 설명해 줘.
현재 프로젝트가 아니라 독립적인 개념 학습으로 진행하고,
이번 한 편은 제작안 없이 바로 설명해 줘. 장기 저장은 하지 마.
```

기본 제작 정책은 `preview`입니다. 이번 요청에 한정한 예외와 지속적인 설정 변경은 다릅니다. 학습자료 전달은 이해 증거가 아니며, 개인 상태 초기화·저장은 별도 요청과 권한이 있어야 합니다.

## 범위와 권한

이 배포판은 skills-only 플러그인입니다. MCP 서버, 외부 앱 의존성, OAuth, lifecycle hook, 자동 실행·자동 저장 기능을 추가하지 않았습니다. 패키지 설치 자체는 Python 스크립트를 실행하거나 개인 학습 상태를 만들지 않습니다. 선택적 검사·설치·기록 도구를 직접 실행하려면 Python 3.10 이상이 필요합니다.

기존 단독 설치 스킬과 플러그인 안의 동일한 스킬을 동시에 로드하면 중복 지침이 생길 수 있습니다. 기존 설치를 자동 삭제하지 않으므로 사용자가 로더 목록을 확인하고 하나의 배포 경로를 선택하세요. 저장소 루트의 `meatware-overclock` 스킬은 변경하지 않았습니다.

## 개발·검증

마켓플레이스 저장소 루트에서 실행합니다.

```bash
python3 plugin-tools/validate_codex_plugin.py
python3 -m unittest discover -s plugins/adaptive-learning-tutor/skills/adaptive-learning-tutor/tests -v
python3 plugins/adaptive-learning-tutor/skills/adaptive-learning-tutor/scripts/validate_package.py
python3 plugins/adaptive-learning-tutor/skills/adaptive-learning-tutor/scripts/build_standalone.py
```

[기존 스킬 사용법](skills/adaptive-learning-tutor/README.md), [학습 핵심 지침](skills/adaptive-learning-tutor/SKILL.md), [독립형 프롬프트](skills/adaptive-learning-tutor/SYSTEM_PROMPT.md), [새 배포 검증 기록](VALIDATION.md)을 참고하세요.

## 출처·배포

[출처와 권리 고지](skills/adaptive-learning-tutor/NOTICE.md)를 유지합니다. 별도 오픈소스 라이선스를 임의로 부여하지 않았습니다. 사용자가 요청한 GitHub 브랜치 배포와 로컬 마켓플레이스 구성이지 OpenAI 공개 디렉터리 등록·심사·인증 완료가 아닙니다.

공식 형식 확인일: 2026-09-23. [플러그인 패키징](https://developers.openai.com/plugins/build/plugins), [플러그인 구조](https://developers.openai.com/plugins/concepts/plugins), [사용 및 계정별 제한](https://help.openai.com/en/articles/20001256/). Plugin Management의 이 대화에 제공된 기능에는 로컬 패키지 생성·업로드·사용자 데스크톱 설치 액션이 없으므로, 해당 도구로 설치했다고 주장하지 않습니다.
