# Learning Document Writing Contract

Apply this contract whenever creating or changing learner-facing project documentation. Also apply its concept-teaching, code-sandwich, terminology, cognitive-load, accuracy, and authority sections to a substantial learner-facing chat explanation.

The artifact-maintenance sections apply only when a guide or journal is authorized and relevant. A read-only chat explanation does not gain file-write permission and does not require artificial guide or journal creation. Adapt paths and headings to repository conventions, but preserve the distinction between learning, procedures, design explanations, and lookup reference.

## Start from the Reader's Journey

Write top-down. A first-time reader should always know:

1. What human or product problem the system solves.
2. What the smallest useful mental model is.
3. How one representative case moves through that model.
4. Where the current chapter sits in the whole.
5. Which real code implements the idea.
6. What can fail, what remains outside the boundary, and what to learn next.

Do not begin with an exhaustive package, directory, class, or function inventory. Introduce the map first, then reveal details at the point the running example reaches them.

## Maintain Two Different Artifacts

### Stable Learning Guide

Default: `docs/learning/README.md`

This describes the current system, not the history of how it got there. Recommended structure:

1. **Start here:** problem, intended reader, prerequisites, and how to use the guide.
2. **Five-minute mental model:** three to seven essential ideas and one compact flow.
3. **Running example:** one realistic input or user action from boundary to outcome.
4. **System map:** major layers, packages, directories, and dependency direction.
5. **Learn chapters:** concepts in dependency order, attached to the running example.
6. **How-to paths:** common tasks such as adding an input, tracing an error, or extending a rule.
7. **Design explanations:** important choices, alternatives, and tradeoffs.
8. **Reference:** modules, public APIs, inputs, outputs, error forms, and generated artifacts.
9. **Glossary and next path:** retrieval aid and a deliberate next learning sequence.

The four information modes serve different reader needs:

| Mode | Reader question | Writing shape |
|---|---|---|
| Learn | “How do I understand this?” | Ordered narrative and worked examples |
| How-to | “How do I accomplish this?” | Goal-oriented steps with verification |
| Explanation | “Why is it designed this way?” | Context, forces, alternatives, consequences |
| Reference | “What exactly is available?” | Precise, scannable facts and signatures |

### Work Learning Journal

Default: `docs/learning/journal/YYYY-MM-DD-<topic>.md`

This preserves the learning context of one work unit. Recommended structure:

1. One-sentence goal.
2. The problem before the change.
3. What changed and why.
4. Concepts introduced or clarified.
5. A real code path through the change.
6. Alternatives considered and why they were not selected.
7. How verification works and how to read its output.
8. What moved into the stable guide.
9. Remaining uncertainty and next learning step.

Do not copy the Git diff into prose. Explain changes that alter the reader's model. Link to stable guide sections instead of duplicating timeless explanations.

## Teach a Concept Before Depending on Its Name

For a foundational or unfamiliar concept, follow this ladder:

1. **Familiar situation:** use a mental model the reader likely already owns.
2. **Problem:** show what becomes unreliable or repetitive without the concept.
3. **Name and meaning:** introduce the technical term, original English, and contextual nuance.
4. **Minimal example:** show the smallest data or code that demonstrates the behavior.
5. **Line-by-line explanation:** describe value changes and decisions, not merely syntax.
6. **Project mapping:** point to the real module, caller, input, and output.
7. **Boundary:** state what the concept does not guarantee and the common misconception.

Avoid circular explanations such as “a schema is a schema definition for data.”

### Example: explaining schema

Begin with a familiar situation: an application form specifies required fields and which kinds of answers are accepted. Then introduce the technical idea:

> 스키마(`schema`: 데이터가 갖춰야 할 모양과 허용 조건을 기계가 검사할 수 있게 표현한 규칙)는 실행 데이터 그 자체가 아니라, 그 데이터를 판정하는 기준이다.

Label the code honestly:

**단순화한 예시 — 특정 프로젝트의 실제 API가 아님**

```json
{
  "type": "object",
  "required": ["name"],
  "properties": {
    "name": { "type": "string", "minLength": 1 }
  }
}
```

Explain the important lines:

- `type: object` means the input must be a key/value object.
- `required: ["name"]` means an omitted `name` is rejected.
- `type: string` rejects a number or object in that field.
- `minLength: 1` rejects an empty string even though it is technically a string.

Then map it to the current project: identify which validator loads which schema, what data it checks, what diagnostic it returns, and whether the schema guarantees business meaning or only structural validity.

## Use a Code Sandwich

Never drop an unexplained code block into a learning chapter.

1. **Before:** tell the reader what question the code answers and what values to watch.
2. **Code:** keep the excerpt small enough to hold in working memory.
3. **Walkthrough:** explain important lines in execution order.
4. **Result:** show the resulting value, state, diagnostic, or side effect.
5. **Connection:** reconnect the excerpt to the system map and running example.

If the real function is large, show a small exact excerpt or a separate simplified example. Do not silently rewrite real code for readability.

## Label the Fidelity of Every Example

Use one of these labels whenever a reader could mistake teaching code for a supported API:

- **Simplified example:** invented or reduced to teach one concept; not a project API.
- **Actual project code:** verified against the current source and presented without semantic alteration.
- **Abridged actual code:** real code with irrelevant sections explicitly omitted.

For actual code, include the current module path and exact identifier. Re-check both after implementation changes.

## Explain Names as Design Signals

Names communicate expected responsibility. Translate them, then explain what relationship the English word implies in this codebase.

Examples to adapt, not blindly copy:

- `contract.ts`: `contract` commonly signals a boundary other modules may rely on—types, inputs, outputs, diagnostics, and compatibility promises—rather than the implementation of the work itself.
- `authoring`: the human- or tool-facing stage where an intent is written before it is validated, resolved, compiled, or rendered.
- `registry`: a controlled lookup that gives known items stable identities and metadata; it is more than an arbitrary array.
- `manifest`: a serializable inventory describing what a package or process contains, produced, or expects.
- `normalize`: converting several acceptable representations into one canonical internal representation.
- `serialize`: turning an in-memory value into a transferable or storable representation under defined rules. It does not automatically imply validation or persistence.

When a project's use differs from convention, explain the project's actual meaning rather than forcing the conventional one.

## Annotate English Without Drowning the Prose

Write the main explanation in the user's language. Preserve code identifiers, paths, protocol names, and standardized terms.

### Semantic words

At first meaningful use, annotate an English term when translation alone would lose the relationship or implied responsibility:

> 계약(`contract`: 두 모듈이 서로 기대해도 되는 입력·출력·오류 규칙의 경계)

The note must explain contextual meaning, not merely provide a bilingual pair.

### Ordinary English in technical roles

Briefly annotate common words when their technical use determines behavior:

- `default`: no more-specific choice was supplied, so this value applies.
- `override`: a more-specific rule replaces an earlier effective value.
- `source`: the origin side of a read, copy, or transformation.
- `target`: the destination or intended representation.
- `owner`: the component or team with final change responsibility.
- `raw`: not yet interpreted, validated, or normalized in the current pipeline.
- `stable`: safe for downstream reliance under a stated compatibility policy.

Annotate the first consequential occurrence, not every repetition. Prefer a short callout or glossary table when inline parentheses would make a sentence hard to parse.

The glossary supports recall and lookup. It never replaces the first in-place explanation.

## Explain Structure at Four Resolutions

Move through these resolutions only after the previous one is clear:

| Resolution | Explain | Reader should be able to answer |
|---|---|---|
| System | Purpose, actors, end-to-end flow | “What happens from request to result?” |
| Package/directory | Ownership and dependency direction | “Why does this folder exist, and who may depend on it?” |
| Module | One responsibility and collaborators | “What enters, what leaves, and whom does it call?” |
| Function/method | Input, output, side effects, errors, invariants | “When should I call it, and what can go wrong?” |

For modules and functions, cover only facts supported by code:

- purpose and non-responsibilities;
- caller and downstream collaborator;
- input and output shapes;
- state mutation, I/O, caching, or other side effects;
- validation and failure representation;
- ordering or lifecycle constraints;
- a representative use;
- tests that demonstrate the contract.

Avoid describing every private helper at equal depth. Group mechanical helpers and expand the ones that carry policy, transform meaning, cross a boundary, or commonly fail.

## Manage Cognitive Load

- Introduce three to seven core ideas in the first mental model, not the entire ontology.
- Use one running example across chapters so new concepts attach to familiar data.
- Preview an idea, teach it when needed, then recap it in relation to the whole.
- Put optional edge cases and exhaustive signatures in reference sections.
- After a dense section, include a short “what to remember” recap and one retrieval question the reader can answer without rereading.
- Use a diagram only when relationships, direction, state, or sequence are materially clearer than prose. Explain how to read it.
- Prefer precise everyday Korean over literal translation for Korean readers; keep English only where it preserves identification or nuance.

## Keep Authority and Time Clear

Distinguish explicitly among:

- current runtime behavior;
- normative design or policy;
- generated output and its source;
- historical decision;
- proposed future behavior.

If sources conflict, state the conflict and the evidence. Do not reconcile code and documentation without authorization. A learner must not leave believing a proposal is already implemented.
