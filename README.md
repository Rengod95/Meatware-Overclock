# Meatware Overclock

`meatware-overclock` is an explicit-invocation Codex skill for producing reader-calibrated, project-grounded software guides. It helps an agent turn inspected code, tests, and design sources into connected explanations that move from a predictive mental model to real behavior and exact reference.

The skill is designed to avoid three common failures:

- a repository inventory that reads like a specification;
- a generic textbook explanation that never connects to the project;
- a tutoring script imposed on readers who asked for a polished guide.

## Invocation

```text
Use $meatware-overclock to explain this system from the user problem through the core mental model and real code. Calibrate prerequisite depth from the conversation, and explain every consequential concept with what, why, how, project use, and boundaries.
```

The skill remains explicit-only through `agents/openai.yaml`.

## Package Map

- `SKILL.md`: activation boundary, process, and progressive reference routing.
- `references/calibration.md`: per-concept reader model and recursive prerequisite calibration.
- `references/information-architecture.md`: whole-guide, chapter, paragraph, and index design.
- `references/explanation-method.md`: detailed what–why–how concept method and schema pattern.
- `references/writing-contract.md`: reader-facing prose, code, terminology, structure, and authority rules.
- `references/quality-rubric.md`: source, explanation, navigation, table, prose, privacy, and completion gates.
- `references/master-prompt.md`: standalone project-neutral version of the behavior contract.
- `agents/openai.yaml`: UI metadata and explicit-only invocation policy.

## Default Artifact

When a repository has no better convention and guide creation is authorized, the default stable guide is `docs/learning/README.md`. A work journal is optional and is created only when the user, repository, or decision-provenance need justifies it.

## Validation

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py /path/to/meatware-overclock
```

The validator checks package structure and frontmatter. Behavioral review must also verify that the references are reachable, the explicit-only policy remains intact, and realistic output satisfies the quality rubric.
