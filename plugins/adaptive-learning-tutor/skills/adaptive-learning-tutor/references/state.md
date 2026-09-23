# 선택적 기록: 하나의 로컬 상태 저장소

장기 저장은 기본 꺼져 있다. 일반 개념 설명에 저장소·프로필·상태 초기화가 필수가 아니다. 사용자에게 승인된 정확한 경로가 주어진 경우만 읽거나 쓴다. 스킬 폴더를 개인 기록 저장소로 사용하지 않는다.

## 스키마와 이전 자료

패키지 버전은 0.3.0이고 선택적 학습 상태는 원본 Tutor의 0.1.0 스키마를 유지한다. 포맷 버전은 패키지 버전과 다르다. 기존 Tutor 상태를 읽을 수 있는 구조를 보존했지만 실제 사용자 데이터 이전은 수행하지 않았다. Orchestrator 상태를 같은 JSON에 합치지 않는다. 제작안·승인·감사는 별도의 0.3.0 제작 계약으로 관리한다.

초기 프로필의 선호는 패키지 기본값이다. 도메인·지식 주장·사용자 응답·동의는 비어 있다. 원본 템플릿에 있던 과거 대화 위치를 새로운 사용자의 관찰 근거로 복제하지 않았다. 장기 목표는 미설정이며 독립 탐구도 가능하다. `long_term_foundations:false`는 기초 설명을 금지하는 것이 아니라 장기 경로를 자동 실행하지 않는 기본값이다.

## 명령

스킬 루트에서 실행한다. 실제 사용자 동의가 있는 새 폴더에만 다음을 쓴다.

```bash
python3 scripts/tutor_state.py init /chosen/new-workspace --consent
python3 scripts/tutor_state.py check /chosen/new-workspace
python3 scripts/tutor_state.py summary /chosen/new-workspace
```

부모 폴더는 존재하고 새 작업 폴더는 없어야 한다. 후보 상태를 별도로 만든 뒤 현재 revision N으로 검증한다.

```bash
python3 scripts/tutor_state.py commit /chosen/workspace /path/candidate.json --expected-revision N
# 해당 저장을 승인받았을 때만:
python3 scripts/tutor_state.py commit /chosen/workspace /path/candidate.json --expected-revision N --apply
```

기본 commit은 쓰지 않는다. 컬렉션 ID 삭제는 사용자 요청과 함께 `--allow-removals`가 필요하다. 모든 종류의 편집·텍스트 삭제를 이 플래그가 막는 것은 아니므로 변경 요약과 후보를 읽는다. 저장 도구의 플래그는 실제 사용자 동의를 인증하지 않는다. 읽기·쓰기에 경로와 접근 권한을 먼저 확인한다.

## 구분해서 기록할 것

개념 관계, 읽기 경로, 용어 참조, 자료·원본, 전달, 자기보고, 실제 반응을 분리한다. claim label은 기존 스키마의 unknown/self_report_only/supported_in_context/mixed_in_context/needs_recheck 등을 실제 enum에 맞춰 사용한다. 도움·정답 노출·참고자료·작성자·맥락·시점·대안 해석을 함께 남긴다. mastery나 숫자 이해도 필드를 임의로 추가하지 않는다. 검사기는 증거의 참조·형식만 확인하며 내용의 진실성은 인증하지 않는다.

새로운 장르 이름은 저장 enum에 임의 추가하지 않는다. 예를 들어 분야 조망은 실제 설명 성격에 맞는 explanation을 사용하고 제목·경로·관계로 구분한다. 학습 모드 read_only는 튜터의 상호작용 방식이며 파일 읽기 전용 OS 권한이라는 뜻이 아니다.

원본 버전 변경은 관련 자료의 needs_recheck 후보이며 지식 퇴보가 아니다. 서로 다른 에이전트가 같은 저장소를 사용할 수 있지만 동시 쓰기에는 revision 확인과 잠금이 필요하다. 호스트가 그 경로를 읽을 권한이 있어야 하고 자동 동기화는 없다.

## 제한과 삭제

이 저장소는 로컬 평문 JSON이며 암호화·신원 인증·외부 백업·예약 복습 기능이 없다. 필요한 기록만 저장하고 비밀을 넣지 않는다. 삭제 요청에는 합의한 상태 범위와 관련 자료를 확인해 일반 호스트 파일 도구로 처리한다. 이 CLI에는 전체 작업 공간 자동 삭제 명령이 없다. 자동 백업이 없으므로 중요한 기존 상태는 사용자 통제하에 백업한다. 외부 백업까지 지워졌다고 주장하지 않는다.
