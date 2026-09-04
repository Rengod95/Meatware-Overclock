# Reader-Friendly Technical Writing Contract

Apply this contract to project guides and substantial technical explanations. It governs the reader-facing result; planning notes such as the reader model, concept map, and coverage ledger remain internal.

## Write from Evidence

Inspect the current system before explaining it. Verify the user problem, entry points, representative flow, boundaries, inputs, outputs, state changes, errors, tests, generated sources, and governing documents. Read names as clues, not proof.

For every consequential claim, know whether its authority is:

- current runtime behavior shown by code or tests;
- a normative contract or policy;
- a generated artifact and its source;
- a historical decision;
- an inference from available evidence;
- a proposal or planned behavior.

Make conflicts and inference visible. Do not silently reconcile them or present a likely rationale as a recorded decision.

## Write for a Reader Outcome

Open with the document promise: what this guide covers, why it matters to this reader, what knowledge it assumes, and what reasonably expected topic it does not cover. Lead with the answer or model the reader needs, not the history of the project or the inventory of its files.

Use the provisional reader model from `calibration.md`. Keep depth local to each concept. Do not repeatedly announce the reader model or turn the prose into a personalized assessment.

## Build a Predictive Core Mental Model

The core mental model is not a summary of every subsystem. It is the smallest accurate model that lets the reader predict the representative behavior.

Include only the necessary:

- actors or callers;
- system boundaries;
- important state or data representations;
- transformations or decisions;
- observable result;
- highest-consequence failure boundary.

Use plain relationships before implementation names. Then attach real project terms to the model so later code has a place to land. Avoid an arbitrary time promise such as “five-minute.”

## Carry One Representative Case

Choose one realistic input, user action, request, failure, or change that crosses the important boundaries. Reuse it as concepts and modules appear. Show how the same value or intention changes representation and meaning at each stage.

Introduce another example only when it reveals a different boundary, invalidates an overgeneralization, or demonstrates transfer. Avoid toy examples that use a technology in a way real users normally would not.

## Explain Concepts in Place

Before depending on a consequential concept, use `explanation-method.md`. The reader should be able to answer:

- What is it, and what nearby thing is it not?
- Why does it exist generally, and why does it matter here?
- How does its mechanism work from input through decision to result?
- Which prerequisites does that mechanism depend on?
- How does this project use, adapt, narrow, or extend the conventional idea?
- Which real module, caller, input, output, error, and test embody it?
- What does it not guarantee, and how can the reader verify the boundary?

These answers may form a short inline bridge or a full chapter. Do not force visible `What`, `Why`, and `How` headings when connected prose reads better, but do not omit the reasoning behind a neat definition.

Teach prerequisites before use. If a prerequisite detour is necessary, tell the reader why, keep it bounded, and return explicitly to the original concept.

## Connect General Practice to Project Use

When the guide introduces a standard concept such as schema, adapter, registry, serialization, cache, event, transaction, or compiler stage:

1. Explain the conventional role and mechanism without claiming all systems implement it identically.
2. Identify the project evidence.
3. State what follows convention.
4. State what differs and why, only when the rationale is supported.
5. Show the operational consequence of the difference.

This general-to-project bridge prevents two failures: a generic textbook chapter with no codebase connection, and a codebase inventory that assumes the reader already owns the underlying concept.

## Make Code an Explained Piece of Evidence

Every teaching code block needs:

1. **Question before code:** what behavior the excerpt demonstrates and which value, branch, or state to watch.
2. **Fidelity label:** simplified example, actual project code, or abridged actual code.
3. **Small excerpt:** only the lines needed for one reasoning goal.
4. **Execution walkthrough:** what each important decision does in actual order.
5. **Observable result:** value, state, side effect, diagnostic, or output.
6. **Reasoning:** why the code has this step or shape, not a syntax paraphrase.
7. **Project connection:** module path, identifier, caller, and place in the larger model.
8. **Boundary:** what the excerpt leaves out or does not prove.

For actual code, verify the current path and identifier after implementation changes. Do not silently rewrite real code for readability. When syntax is not the point, use a value trace, concise pseudocode, or prose instead.

## Explain Names as Relationships

Preserve searchable identifiers and standard English terms. At first consequential use, explain the responsibility or relationship the name signals in this project.

For example, do not stop at `normalize` means “정규화.” Explain that this stage converts multiple accepted input forms into one internal form that later stages may treat uniformly, then show the actual input and output here.

When several stage names form a pipeline—such as `parse`, `validate`, `normalize`, `resolve`, `compile`, and `serialize`—explain the value change, unique decision, owned failure, and ordering between stages. A glossary supports lookup but never replaces the first meaningful explanation.

## Write Connected Prose

- Start each paragraph with its central claim, reader question, or necessary context.
- Keep one reasoning thread per paragraph and one primary idea per sentence.
- Put the real actor before a precise verb when behavior or ownership matters.
- Use concrete nouns in place of ambiguous pronouns.
- State causes, conditions, ordering, and consequences explicitly.
- Compare a new idea with familiar knowledge only when the relationship is accurate and useful.
- Use an analogy for one relationship, then return to literal facts before the analogy creates false predictions.
- Prefer natural language in the user's language while retaining identifiers and searchable technical terms.
- Avoid “simple,” “obvious,” “just,” “easy,” and “straightforward” when they replace a missing step or assumption.
- Do not make the voice childish or conversationally padded in an attempt to be friendly.

After drafting, read only the first sentence of each paragraph. They should form a coherent outline of the argument. Then read the transitions and verify that every new idea has a reason to appear where it does.

## Use Structure as a Reader Aid

Apply `information-architecture.md` at the whole-guide, chapter, and paragraph scales.

- Give each major section one primary reader question.
- Use headings as meaningful entry points, not labels for arbitrary chunks.
- Make sections understandable to readers who land from search by briefly locating them in the whole.
- Keep exact signatures and inventories in reference-shaped sections.
- Keep troubleshooting near the behavior or task that produces the symptom unless its volume warrants a dedicated section.
- Mix concept, procedure, rationale, reference, and diagnosis only when proximity helps the reader complete a coherent task or understand a mechanism.
- Do not expose the author's content taxonomy as the reader's main navigation.

## Use Tables and Diagrams Sparingly

A table earns its place when readers need repeated-field comparison or exact mapping across several items. Keep cells concise and parallel. Introduce the question the table answers, and explain the important relationship afterward.

Use prose or a flow for causal sequences. Use a list for independent items. Do not turn definitions or a chapter narrative into a matrix merely because Markdown supports tables.

Use a diagram only when hierarchy, direction, state, sequence, or ownership becomes materially easier to see. Label the meaning of arrows and explain how the diagram connects to the representative case.

## Separate Stable Understanding from Work History

The stable guide describes the current system. It should not narrate every edit or become a release log.

A work journal is optional. Create or update it only when requested or established by repository convention. If used, keep transient investigation and decisions there, promote durable explanations to the stable guide, and link rather than duplicate.

Do not add quizzes, recall questions, exercises, or prescribed next lessons unless the user requested a tutorial, curriculum, or practice material. A polished guide may end with boundaries, implications, or lookup links without adopting a tutor voice.

## Keep Authority, Time, and Confidence Visible

Use explicit language for differences among:

- “The current implementation does …”
- “The specification requires …”
- “The generator produces … from …”
- “The ADR records that …”
- “The available evidence suggests …”
- “The proposal would …”

When sources disagree, identify the exact claims and locations, assess authority and recency, explain current versus intended behavior, and request a decision only if the authorized task cannot resolve the conflict.

## Edit from Structure Down to Sentences

Revise in this order so polished sentences do not hide a structural defect:

1. **Promise:** every major section contributes to the document outcome and respects scope.
2. **Whole-guide arc:** the problem, predictive model, and representative case precede implementation inventory.
3. **Concept dependency:** prerequisites appear before the ideas that depend on them.
4. **Chapter logic:** each chapter resolves one question and reconnects to the whole.
5. **Causality:** what, why, how, general convention, and project adaptation form one explanation rather than disconnected fragments.
6. **Evidence:** code, tests, governing sources, and examples support the claims made.
7. **Paragraph logic:** openings, transitions, and conclusions form a coherent argument.
8. **Form:** code, lists, tables, diagrams, and reference blocks perform a reader task that prose would handle worse.
9. **Reader paths:** a less-prepared reader can find the missing bridge, while a prepared reader can skip familiar foundations without losing the project-specific model.

Finish only when exact facts remain easy to find and no section reads as a pasted spec, changelog, or tutoring script unless that is the requested form.
