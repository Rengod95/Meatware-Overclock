---
name: meatware-overclock
description: Use when a user explicitly asks to keep learning while an agent builds, changes, reviews, or investigates software and wants learner-calibrated project guides that evolve with the work.
---

# Meatware Overclock

Keep the authorized software task moving while maintaining learning material that helps the user understand and eventually own the result.

## Non-Negotiable Boundaries

- Activate only through explicit user invocation. The product metadata disables implicit invocation.
- Do not expand the authorization of the underlying task. A review request remains read-only; a build request permits only relevant implementation work.
- Do not pause safe implementation merely to teach. Ask only product or architecture decisions that genuinely require the user; treat calibration questions as non-blocking.
- Never persist raw calibration answers, personal judgments, or labels such as junior, middle, or senior in a repository.
- Do not invent project behavior. Derive learning material from the current source of truth and expose unresolved code/document conflicts.

## Load References Progressively

Read the supporting references when their stage becomes relevant:

- Read `references/calibration.md` before assessing or updating reader assumptions.
- Read `references/writing-contract.md` before creating or changing learning documents or delivering a substantial learner-facing explanation in chat.
- Read `references/quality-rubric.md` before claiming the learning material is complete.
- Read `references/master-prompt.md` only when the user asks for the standalone prompt or its rules need inspection.

## Run Two Lanes

Maintain two coordinated lanes:

1. **Work lane:** perform the requested implementation, review, investigation, test, and verification under the repository's rules.
2. **Learning lane:** capture the concepts, naming reasons, decisions, data flow, failure boundaries, and reading strategies needed to understand that work.

The learning lane observes the work lane; it does not control or enlarge it. Batch learning updates at meaningful checkpoints rather than after every file edit.

Meaningful checkpoints include a new subsystem, changed public API or data flow, settled design decision, verified task unit, completed task, or guide content made stale by the work. A typo or mechanically equivalent edit normally needs only a staleness check.

## Workflow

1. Confirm the underlying task, mutation permissions, repository instructions, and available source-of-truth documents.
2. Reuse reader information already established in the conversation. Apply `references/calibration.md` only to missing dimensions. On first activation, begin with one or two actual short questions and accumulate 4–6 across early meaningful checkpoints without blocking safe work. If explicit answers already in the conversation make a question redundant, identify which calibration slot they satisfy instead of repeating it or inventing filler. Proceed with provisional assumptions while answers are pending.
3. Inspect the real system before explaining it: entry points, representative flow, packages or modules, public boundaries, tests, generated sources, and relevant architecture documents.
4. Find existing learning-document conventions. Unless the repository establishes better locations, maintain:
   - `docs/learning/README.md` for the stable, top-down guide to the current system.
   - `docs/learning/journal/YYYY-MM-DD-<topic>.md` for the current work's learning record.
5. Continue the work lane. Keep a compact learning delta: concepts introduced, mental model changed, naming that needs explanation, exact examples worth preserving, and stale guide sections.
6. Before the first learning-document edit or substantial learner-facing chat explanation, read and apply `references/writing-contract.md`. Prefer a small running example that travels from user problem to system boundary to real code. Teach a foundational concept in place before relying on a glossary definition. For every learning code block, put the observation question or values to watch before the block, then explain the result and project connection after it.
7. At each meaningful checkpoint, update both artifacts only where their distinct purposes require it. Do not turn the guide into a changelog or the journal into a second architecture manual.
8. Verify the software using the task's normal gates. Separately verify the learning material using `references/quality-rubric.md`.
9. In the handoff, lead with the task outcome, then name the learning artifacts changed, the new mental model they teach, and any unresolved source conflict or provisional reader assumption.

## When No Repository Exists

If the task is a design discussion, pasted code, or a new project without document conventions, provide the guide and journal as clearly separated artifacts in the user's requested destination. Do not create a repository or files unless the underlying request authorizes writes.
