# Learning Document Quality Rubric

Use this rubric at meaningful checkpoints and before completion. Record only material failures in the work journal; do not turn the journal into a checklist dump.

## Gate 1: Source Accuracy

- [ ] Every named path and identifier exists in the inspected revision.
- [ ] Actual-code excerpts preserve behavior; omissions are labeled.
- [ ] Inputs, outputs, side effects, errors, and callers are supported by code or tests.
- [ ] Generated artifacts identify their source and are not presented as normal edit targets.
- [ ] Current behavior, normative policy, history, and future intent are distinguished.
- [ ] Source conflicts and provisional interpretations are visible.

Any failed item here blocks a claim that the guide is current.

## Gate 2: Mental Model and Flow

- [ ] The guide begins with the user or product problem, not a file inventory.
- [ ] The first section limits the initial model to three to seven essential ideas.
- [ ] A representative case travels through the whole system.
- [ ] Each detailed chapter reconnects to the system map or running example.
- [ ] Dependency direction and responsibility boundaries are explicit.
- [ ] The reading order follows conceptual dependencies.

## Gate 3: Concept Explanation

For each newly important foundational term:

- [ ] A familiar situation appears before or with the term.
- [ ] The problem solved by the concept is concrete.
- [ ] The original English term and contextual nuance appear at first meaningful use.
- [ ] A minimal example or code excerpt demonstrates behavior.
- [ ] Important lines and value changes are explained.
- [ ] The real project module, caller, input, and output are connected.
- [ ] The boundary and one common misconception are stated.

Definitions composed mostly of undefined technical words fail this gate.

## Gate 4: Code Pedagogy

- [ ] Each teaching code block has a before/after explanation.
- [ ] The reader is told what value or decision to watch.
- [ ] The result of execution or transformation is shown.
- [ ] Simplified, actual, and abridged actual code are clearly labeled.
- [ ] Examples are small enough to serve one learning goal.
- [ ] Exact project paths and identifiers are current.

## Gate 5: Language Accessibility

- [ ] Main prose follows the user's language and demonstrated comfort.
- [ ] Code identifiers and standard names remain searchable in their original form.
- [ ] Semantic word notes explain implied responsibility or relationship, not just translation.
- [ ] Consequential ordinary English words receive brief contextual notes when needed.
- [ ] Repeated parentheses and annotations do not overwhelm the sentence.
- [ ] A glossary supplements rather than replaces first-use explanations.

## Gate 6: Artifact Separation

- [ ] The stable guide describes the current system rather than narrating every edit.
- [ ] The work journal explains this work's decisions and learning delta rather than duplicating the guide.
- [ ] Timeless explanations promoted to the guide are linked from the journal.
- [ ] A small change does not create artificial architecture content.
- [ ] Both artifacts were checked for staleness even if only one required editing.

## Gate 7: Reader Calibration and Privacy

- [ ] Questions cover only missing dimensions and use code or situations instead of status labels.
- [ ] Safe work continued under explicit provisional assumptions.
- [ ] The material reflects demonstrated knowledge without becoming inconsistent in tone.
- [ ] No raw answers, ability judgment, or sensitive personal data entered project files.
- [ ] Any persistent reader assumption describes documentation needs, not personal deficits.

## Gate 8: Scope and Completion

- [ ] Learning work did not expand the underlying task's authority.
- [ ] Teaching did not block implementation except for a real user decision.
- [ ] Software and documentation were verified separately.
- [ ] The handoff identifies changed learning artifacts and the mental model they now teach.
- [ ] Remaining uncertainty, stale areas, and unverified examples are stated plainly.

## Red-Flag Search

Before completion, scan for:

- unexplained acronyms and English identifiers;
- definitions that use the term itself;
- paragraphs containing several newly introduced concepts;
- large code blocks without observation guidance;
- path or API names copied from an earlier revision;
- “simply,” “obviously,” or “just” where the omitted reasoning matters;
- exhaustive lists before the reader has a map;
- changelog prose in the stable guide;
- tutorial prose in exact API reference tables;
- personal labels such as junior, weak, slow, or non-technical.

## Compact Completion Report

Report the result in this order:

1. Underlying task outcome and verification.
2. Learning guide sections added or corrected.
3. Work journal created or updated.
4. The main mental model now available to the reader.
5. Unresolved source conflicts or provisional assumptions.

Do not paste this rubric into the final report.
