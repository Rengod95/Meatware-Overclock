# Reader Model and Recursive Calibration

Use calibration to decide what must be explained, what can be bridged briefly, and what can be assumed. Do not use it to judge or rank the person.

## Model Knowledge Locally

A reader does not have one technical level. They can understand a framework's API while lacking the runtime model beneath it, know the product domain while being new to its data representation, or read code fluently while finding architecture prose unfamiliar.

Track only the dimensions that affect the current document:

- **Purpose:** use, review, debug, extend, operate, or decide.
- **Code fluency:** syntax, execution order, types, state changes, errors, and transformations.
- **System model:** actors, boundaries, dependencies, lifecycle, concurrency, and data flow.
- **Domain knowledge:** business rules, invariants, terminology, and failure consequences.
- **Concept familiarity:** the specific concepts required by this guide, not a general technology rank.
- **Technical language:** comfort with identifiers, acronyms, and English documentation.
- **Reading behavior:** continuous first read, search landing, task-time lookup, or review.
- **Ownership horizon:** immediate use versus future maintenance, extension, or architecture decisions.

Express the result as documentation needs, for example:

> Reader assumption: can follow TypeScript control flow and interfaces, is new to schema-driven validation, needs an overview before exact module details, and will maintain the validation boundary.

Do not write labels such as “junior,” “weak at architecture,” or “non-technical.”

## Gather Evidence Before Asking

Use evidence already available in this order:

1. The user's stated goal, corrections, vocabulary, and requested depth.
2. Questions and decisions the user has already handled in the conversation.
3. The audience statement and conventions in existing documentation.
4. The work the reader must perform with the result.
5. Small, real examples from the current system.

Ask a question only if different answers would change the outline, prerequisite depth, terminology, example choice, or failure coverage. Prefer an actual situation over a self-rating.

Useful early questions include:

- “이 문서를 읽은 뒤 직접 수정·디버깅해야 하나요, 아니면 구조를 검토하고 판단하는 것이 주목적인가요?”
- “이 실제 입력이 어느 단계에서 형태가 바뀌는지 바로 따라갈 수 있나요, 아니면 단계별 값부터 함께 보는 편이 좋을까요?”

Later, ask only at a genuine ambiguity in the concept map:

- “여기서 `schema` 자체보다 validator가 schema를 읽어 진단을 만드는 과정이 더 낯선가요?”
- “이 오류를 호출 순서 문제로 보시나요, 데이터 경계 문제로 보시나요? 답에 따라 앞부분의 모델을 다르게 보강하겠습니다.”

Do not fill a question quota. A demonstrated answer may settle several dimensions, and a long questionnaire often measures patience rather than understanding.

## Recurse Through Prerequisites

Calibrate at the concept level while outlining and drafting:

1. Identify the consequential concept the reader must understand.
2. List only its direct prerequisites—the ideas required to understand the mechanism, not everything historically related to it.
3. Mark each prerequisite provisionally:
   - **owned:** evidence shows the reader can use it;
   - **bridge:** likely familiar, but its role here needs one or two clarifying sentences;
   - **foundation:** the guide must teach it before relying on it;
   - **outside:** not needed for this document's promise.
4. For every `foundation`, repeat the same check on its prerequisites.
5. Stop when the explanation reaches an evidence-backed familiar idea, an accurate everyday causal model, or the declared scope boundary.
6. Re-run the check whenever a draft introduces a new unexplained term or mechanism.

This recursion prevents a common failure: carefully explaining an easy surface term while silently relying on a harder concept underneath it.

### Example prerequisite chain for schema

The chain may be:

1. A runtime value has a shape and value kinds.
2. A program can express allowed shapes and constraints as data.
3. A schema is such a machine-readable rule description.
4. A validator interprets the schema and compares an input against it.
5. Validation produces a result or structured diagnostics.
6. A project may use the same schema for additional jobs such as editor support, code generation, or compatibility checks.

Do not teach every step automatically. Expand only the steps marked `bridge` or `foundation` for this reader and this project.

## Allocate Explanation Depth

Use four local depth choices:

- **Name only:** the concept is owned and incidental.
- **Inline bridge:** define its role here and distinguish it from a nearby concept.
- **Full concept unit:** explain what, why, general mechanism, project use, prerequisites, example, and boundary.
- **Linked foundation:** the concept is important but would derail the current chapter; provide a short bridge and link to a dedicated explanation.

Do not equate plain language with low expertise. Experts also benefit from explicit actors, causal steps, project-specific deviations, and precise boundaries; they simply need less foundational unpacking.

## Recalibrate from the Draft

Treat the guide itself as a diagnostic surface. Recalibrate when:

- one section assumes knowledge that an earlier section explained as unfamiliar;
- a definition introduces two or more undefined terms;
- an example can be followed syntactically but not causally;
- the reader asks a question that reveals a missing relationship rather than a missing fact;
- a later correction demonstrates that an earlier bridge is unnecessary or inaccurate;
- a domain change introduces a new prerequisite graph.

Adjust the affected concept and its dependents, not the entire document. Keep the voice and terminology consistent after the change.

## Privacy and Persistence

Persist only an anonymous reader assumption when it materially helps maintain the shared document. Never store raw answers, ability judgments, sensitive data, or conversational speculation. Later demonstrated behavior is better evidence than an early assumption; update the document need quietly.
