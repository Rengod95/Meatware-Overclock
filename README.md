# Meatware Overclock

`meatware-overclock` is an explicit-invocation Codex skill for people who want software work to continue while their understanding catches up with the agent's implementation speed.

It maintains two complementary learning artifacts:

- A stable, top-down guide to the current system.
- A work-specific learning journal covering new concepts, decisions, verification, and changes to the reader's mental model.

The skill calibrates explanation depth with short code and situation questions. It teaches unfamiliar concepts through a familiar situation, the problem being solved, a minimal example, line-by-line explanation, real project mapping, and responsibility boundaries. For Korean readers, it keeps searchable English identifiers while explaining semantic nuance and consequential ordinary English words in natural Korean.

## Invocation

The skill does not activate implicitly. Invoke it by name:

```text
Use $meatware-overclock while refactoring this module. Keep implementation moving, and maintain a top-down learning guide plus a work learning journal that I can follow.
```

## Default Project Artifacts

Unless a repository has a different documentation convention:

```text
docs/learning/README.md
docs/learning/journal/YYYY-MM-DD-<topic>.md
```

The first file teaches the current system. The second preserves the learning context of one work unit without turning the stable guide into a changelog.

## Package Map

| Path | Role |
|---|---|
| `SKILL.md` | Trigger, boundaries, two-lane workflow, and reference routing |
| `agents/openai.yaml` | UI metadata and explicit-only invocation policy |
| `references/calibration.md` | Multi-dimensional reader calibration without personal ranking |
| `references/writing-contract.md` | Top-down guide structure, concept teaching, code sandwich, terminology rules |
| `references/quality-rubric.md` | Accuracy, cognitive-load, privacy, and scope completion gates |
| `references/master-prompt.md` | Standalone, project-neutral prompt containing the complete behavior contract |
| `tests/scenarios.md` | Reusable pressure scenarios and observable pass criteria |
| `tests/evidence/` | Baseline and skill-applied behavior evidence |

## Validation

```bash
python "$CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py" .
git diff --check
```

The behavior evidence includes an executable TypeScript fixture, a no-skill baseline, all five pressure scenarios, complete agent outputs, verifiable Git bundles, and a targeted code-sandwich check.

## Standalone Prompt

Use `references/master-prompt.md` when a full copy-paste prompt is preferable to installing the skill. It contains placeholders for the current project, task authority, source-of-truth order, reader context, documentation conventions, and verification commands.
