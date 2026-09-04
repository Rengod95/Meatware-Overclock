---
name: meatware-overclock
description: Use only when explicitly invoked to create or maintain reader-calibrated, project-grounded software guides that connect a clear mental model to real code, design reasons, and failure boundaries.
---

# Meatware Overclock

Produce technical guides that a reader can understand as connected explanations rather than as a file inventory, specification dump, or tutoring script. Keep any authorized software task moving, but treat the inspected system as evidence for the guide—not as a separate named workflow.

## Boundaries

- Activate only through explicit user invocation. Preserve `policy.allow_implicit_invocation: false`.
- Do not enlarge the underlying task's authority. A review remains read-only; a build permits only relevant implementation and documentation changes.
- Do not invent project behavior. Verify code, tests, generated sources, and governing documents, and expose conflicts among them.
- Do not pause safe work for reader calibration. Ask only questions whose answers would materially change the guide.
- Never persist raw calibration answers, personal judgments, or rank labels such as junior, middle, senior, or non-technical.
- Do not force a learning guide, journal, tutorial, matrix, or fixed table of contents when the requested artifact or repository convention needs a different form.

## Load References When Needed

- Read `references/calibration.md` before establishing or revising reader assumptions.
- Read `references/information-architecture.md` before outlining a long guide, chapter sequence, or index.
- Read `references/explanation-method.md` before explaining foundational or consequential technical concepts.
- Read `references/schema-example.md` only when a schema is consequential to the requested guide and a worked application of the generic concept method would help.
- Read `references/writing-contract.md` before creating or substantially revising reader-facing material.
- Read `references/quality-rubric.md` before claiming the material is complete.
- Read `references/research-foundations.md` only when maintaining this skill or reviewing why a writing rule exists; it is not required during ordinary guide production.
- Read `references/master-prompt.md` only when the user requests the standalone prompt or its rules need inspection.

## Process

1. Confirm the requested outcome, write permissions, repository instructions, source-of-truth order, intended readers, and what the document must help them understand or do.
2. Establish an evidence-based, provisional reader model using `references/calibration.md`. Model knowledge per concept and task rather than assigning one global level.
3. Inspect the real system before explaining it: user problem, actors, entry points, one representative execution path, responsibility boundaries, data transformations, failure forms, tests, generated artifacts, and relevant design sources.
4. Build a compact internal concept map. Record the consequential concepts, their prerequisite concepts, their relationships, the reader question each resolves, and the project evidence that supports it. Do not dump this planning structure into the guide.
5. Design the document at three scales using `references/information-architecture.md`:
   - the whole guide grows from problem and core mental model to real behavior and exact detail;
   - each chapter resolves one coherent reader question and reconnects to the whole;
   - each paragraph advances one claim in a known-to-new order.
6. Explain every consequential introduced concept at the depth required by the reader model. Apply the concept unit in `references/explanation-method.md`: what it is, why it exists and matters, how it works generally, how this project uses or adapts it, which prerequisites it depends on, and what it does not guarantee.
7. Use realistic examples and verified project traces. Label simplified, actual, and abridged actual code. Put the observation point before code and the result, reasoning, and project connection after it.
8. Use information types as authoring tools, not as a visible matrix the reader must decode. Keep exact lookup facts precise; weave context, mechanism, rationale, procedure, diagnosis, and examples together only where the reader's question benefits.
9. Update an existing stable guide when authorized. Create a work journal only when the user requests one or the repository already requires one. Do not create a journal merely because this skill is active or because provenance might be useful.
10. Verify software with the repository's gates and verify the guide separately with `references/quality-rubric.md`. Report source conflicts, provisional reader assumptions, and unverified examples plainly.

## Artifact Placement

When guide creation is authorized, follow the user's destination and the repository's existing documentation architecture. If neither establishes a destination, choose a location only after inspecting repository conventions; do not impose a universal `docs/learning/README.md` path.

When no repository exists or writes are not authorized, provide the requested explanation in chat or in the user-selected artifact without creating repository files.
