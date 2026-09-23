# Adaptive Learning Tutor plugin

이 브랜치는 기존 `meatware-overclock` 스킬을 덮어쓰지 않고 Adaptive Learning Tutor를 별도 Codex 플러그인으로 추가합니다.

- 플러그인: `plugins/adaptive-learning-tutor/`
- 스킬 본체: `plugins/adaptive-learning-tutor/skills/adaptive-learning-tutor/`
- 마켓플레이스: `.agents/plugins/marketplace.json`
- 플러그인 버전: `0.3.1` / 보존한 스킬 버전: `0.3.0`

```bash
codex plugin marketplace add Rengod95/Meatware-Overclock --ref codex/adaptive-learning-tutor-plugin
codex plugin marketplace list
```

등록 후 데스크톱 앱을 재시작하고 Plugins Directory의 **Rengod95 Learning → Adaptive Learning Tutor**에서 설치합니다. 위 명령은 마켓플레이스 등록이며 플러그인 설치 완료가 아닙니다. [설치·사용·권한·검증 안내](plugins/adaptive-learning-tutor/README.md)를 참고하세요.

원본의 승인 정책과 상태 저장 기본값은 유지했습니다. 새 MCP·OAuth·hook 의존성이나 자동 개인 기록은 추가하지 않았습니다. 기존 저장소 파일과 main 브랜치는 이번 배포 변경의 대상이 아닙니다.
