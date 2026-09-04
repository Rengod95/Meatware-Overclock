# Semantic Pressure Scenarios

These scenarios evaluate decisions and artifacts, not exact wording or heading names. Run them in an isolated temporary project only when independent behavioral testing is authorized.

## Scenario 1: Unknown reader background at a validation boundary

Request:

> Use `$meatware-overclock` to explain how external configuration enters this service. It passes through declarative rules, runtime validation, normalization, and separate business checks. I need a maintainable guide, but I have not stated my background.

Pass criteria:

- Work continues under a provisional reader model instead of a questionnaire.
- Questions appear only if different answers materially change the guide.
- The guide distinguishes rule description, rule consumer, structural acceptance, normalization, and domain validation.
- General mechanisms remain distinct from the project's technology and error representation.
- The result is prose-first and does not default to a pipeline matrix.

## Scenario 2: Experienced maintainer, unfamiliar domain

Request:

> Use `$meatware-overclock` while documenting this billing-policy engine. I am comfortable with Kotlin, Gradle, and distributed systems, but the proration domain is new. I will review and extend policy rules.

Pass criteria:

- The reader model relies on demonstrated language and systems knowledge instead of explaining basic syntax.
- Domain invariants, policy ordering, failure boundaries, and test evidence receive the depth.
- Code explanations group ordinary syntax and focus on non-obvious decisions and values.
- No junior or senior label is stored or used.
- Headings let the reader skip familiar implementation mechanics.

## Scenario 3: A specification matrix must become an explanation

Request:

> Use `$meatware-overclock` to rewrite this subsystem guide. It opens with a 40-row package matrix and mostly copies configuration fields. Preserve exact facts, but make it readable for a new maintainer.

Pass criteria:

- The opening changes to the reader problem, core mental model, and representative flow.
- Exact lookup facts remain available in a reference-shaped section or authoritative link.
- Tables survive only where stable cross-item comparison is genuinely useful.
- Every retained table is introduced and interpreted in prose.
- Concepts are introduced outside table cells before reference detail relies on them.
- The result is not merely a reordered matrix.

## Scenario 4: Read-only concept explanation

Request:

> Review this pasted parser and use `$meatware-overclock` to explain `parse`, `validate`, and `normalize`. Do not change files.

Pass criteria:

- No repository, guide hierarchy, journal, or file is created.
- The explanation contrasts the terms through input, output, failure, and responsibility.
- General conventions are separated from what the pasted code proves.
- Inferences caused by missing callers or tests are labeled.
- The answer contains no tutoring quiz or next learning path.

## Scenario 5: Code and architecture source conflict

Request:

> Use `$meatware-overclock` to update the onboarding guide. The ADR says invalid input returns diagnostics, but the current implementation throws an exception.

Pass criteria:

- The guide does not silently choose one behavior.
- Current runtime behavior, normative intent, locations, and timestamps are separated.
- The documentation update stays within the user's mutation authority.
- The unresolved decision and its reader impact are explicit.

## Scenario 6: A how-to depends on unfamiliar concepts

Request:

> Use `$meatware-overclock` to document how to add a registry entry. The procedure touches canonicalization, aliases, generated manifests, and collision diagnostics.

Pass criteria:

- The procedure remains goal-focused with prerequisites, steps, success signals, failures, and verification.
- Consequential concepts receive what–why–how explanations nearby or through direct links.
- The generated manifest is not presented as the normal edit target.
- One entry is traced through canonicalization, registration, collision handling, and generation.
- Long conceptual digressions do not interrupt numbered steps.

## Scenario 7: Small mechanical change

Request:

> Use `$meatware-overclock` while renaming a private test helper. Behavior and public names do not change.

Pass criteria:

- The skill does not create a new guide, journal, tutorial, or architecture section.
- It checks whether an existing explanation became stale.
- The final report does not inflate the learning value of the change.
