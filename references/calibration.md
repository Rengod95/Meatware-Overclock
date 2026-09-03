# Reader Calibration

Use calibration to choose explanation depth, not to judge the person.

## Rules

- Reuse reliable evidence already present in the current conversation. Do not repeat a question the user has explicitly answered.
- On first activation, ask 4–6 actual short code, example, or situation questions across the early meaningful checkpoints. Avoid abstract self-ratings such as “Are you a junior or senior?”
- Begin with one or two questions, state that safe work will continue, and use one or two later checkpoints to complete the set. Do not present all questions as an up-front exam.
- Existing explicit answers may replace question slots only when re-asking would be redundant. Name the already-established slot and its conversational evidence; never invent filler merely to reach a count.
- Keep each question answerable in one or two sentences. If the user cannot answer immediately, retain the unanswered questions and continue under an explicit provisional assumption.
- If immediate work is safe, proceed using explicit provisional assumptions. Revise them when answers arrive.
- Ask only questions that will change the learning material. Skip irrelevant dimensions.
- Never infer general intelligence or a global level from one answer.
- Never persist raw answers or deficit-focused personal judgments in project files.

## Dimensions

| Dimension | Evidence to seek | Explanation decision |
|---|---|---|
| Code fluency | Reading types, branches, errors, and data transformations | How much syntax and execution detail to unpack |
| System mental models | Understanding boundaries, dependencies, and data flow | How much architecture scaffolding to provide |
| Domain familiarity | Familiarity with the problem space and its invariants | Which domain assumptions require examples |
| Technical English | Comfort with identifiers and English documentation | How often to annotate semantic and ordinary English words |
| Learning preference | Preference for overview, worked example, experimentation, or reference | The order and density of presentation |
| Task ownership | Need to maintain, review, extend, or merely use the result | Which decisions and failure modes must be retained |

## Question Bank

Adapt these to the current language and stack. Use a tiny real or representative snippet when possible.

### Code fluency

> 이 코드에서 `undefined`가 나올 수 있는 경우를 바로 찾을 수 있나요, 아니면 실행 순서부터 같이 따라가는 편이 좋을까요?

```ts
function findName(input: { user?: { name?: string } }) {
  return input.user?.name;
}
```

### System mental model

> 외부 API의 응답 모양이 바뀌었을 때, 호출하는 모든 기능을 고치는 것과 경계의 변환 모듈 한 곳에서 흡수하는 것 중 어느 구조가 더 자연스럽게 느껴지나요? 이유는 짧게만 적어도 됩니다.

### Domain familiarity

> 이번 시스템이 다루는 데이터나 업무 규칙 중 이미 익숙한 것과 처음 보는 것을 각각 하나씩 골라주세요.

### Technical English

> `default` 다음에 `override`가 적용된다는 문장을 보면 우선순위가 바로 떠오르나요, 아니면 짧은 한국어 주석과 값 변화 예시가 있으면 더 편한가요?

### Learning preference

> 먼저 전체 지도를 보고 작은 코드를 보는 방식과, 실행되는 예시 하나를 따라간 뒤 전체 구조로 넓히는 방식 중 어느 쪽이 기억에 더 잘 남나요?

### Task ownership

> 이번 결과물을 주로 사용하려는지, 직접 유지보수·확장하려는지에 따라 설명해야 할 실패 조건의 깊이가 달라집니다. 어느 쪽에 더 가깝나요?

## Store Only an Anonymous Reader Assumption

If a persistent assumption materially improves shared documentation, phrase it around the document—not the person.

Good:

> Reader assumption: comfortable with basic TypeScript syntax, new to schema and compiler concepts, and benefits from a system overview followed by a worked example.

Bad:

> The user is junior and weak at architecture.

Keep the assumption inside an existing learning guide section unless the repository already has a dedicated audience document. Do not create extra files solely to store calibration.

## Recalibrate Quietly

Treat later questions, corrections, and demonstrated fluency as better evidence than the initial answers. Adjust future detail without repeatedly announcing a new assessment. Ask again only after a major domain change or when the current explanation style clearly fails.
