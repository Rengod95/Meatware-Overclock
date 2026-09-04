# Technical Guide Quality Rubric

Use these gates at meaningful checkpoints and before completion. A failed source-accuracy gate blocks a claim that the guide is current. Record only material failures; do not paste the rubric into the guide or turn an optional journal into a checklist dump.

## Gate 1 Source and Authority

- [ ] Every named path, identifier, input, output, error, caller, and test exists in the inspected revision.
- [ ] Actual and abridged code preserves behavior; omissions and simplifications are labeled.
- [ ] Generated artifacts identify their source and are not presented as normal edit targets.
- [ ] Runtime behavior, normative rules, history, inference, and future proposals remain distinct.
- [ ] Project rationale is supported or clearly labeled as inference.
- [ ] Source conflicts and unverified areas are visible.

## Gate 2 Reader Model and Prerequisite Closure

- [ ] The reader model describes documentation needs per task and concept, not a global rank.
- [ ] Existing conversational and document evidence was used before asking questions.
- [ ] Questions were asked only when the answer changed depth, structure, examples, or terminology.
- [ ] Each consequential concept's direct prerequisites were checked recursively.
- [ ] No basic term is overexplained while a harder prerequisite is silently assumed.
- [ ] Persistent assumptions contain no raw answers, personal judgments, or sensitive data.

## Gate 3 Whole-Guide Architecture

- [ ] The guide opens with the reader's problem, document promise, prerequisites, and relevant non-scope.
- [ ] The core mental model is the smallest accurate predictive model, not a package summary or timed pitch.
- [ ] A realistic case travels through the important boundaries to an observable result.
- [ ] Concepts appear in dependency order when the representative case needs them.
- [ ] The project map follows the mental model rather than preceding it.
- [ ] First-read and later-lookup paths are both usable.
- [ ] A reader landing mid-guide can locate the section in the whole.

## Gate 4 Concept Explanation

For each consequential introduced concept:

- [ ] **What:** plain meaning, technical term, type of thing, scope, and nearest useful distinction are clear.
- [ ] **Why:** the general problem, project relevance, and supported tradeoff or rationale are clear.
- [ ] **How:** actors, inputs, decisions, state or value changes, outputs, and failures form a causal explanation.
- [ ] General convention is connected to the project's use, adaptation, or deviation.
- [ ] Required foundations appear before use or are bridged and linked.
- [ ] A realistic example, trace, or code excerpt demonstrates the mechanism when needed.
- [ ] A boundary, non-guarantee, misconception, and verification point are present where consequential.
- [ ] The explanation returns to the core model or representative case.

## Gate 5 Code and Example Pedagogy

- [ ] Every teaching code block has a question or observation target before it.
- [ ] Simplified, actual, and abridged actual examples are distinguishable.
- [ ] Important decisions are explained in execution order, including why they exist.
- [ ] Resulting values, state, side effects, diagnostics, or output are shown.
- [ ] Examples are realistic and small enough to serve one reasoning goal.
- [ ] Project paths, identifiers, and test claims were rechecked after changes.
- [ ] Large code blocks were replaced by a smaller excerpt or trace when syntax was not the point.

## Gate 6 Information Shape and Navigation

- [ ] Each section has one primary reader question and an appropriate orientation, concept, trace, procedure, rationale, diagnosis, reference, or authority shape.
- [ ] Different shapes are combined only when proximity improves understanding or task flow.
- [ ] Procedures start from a real goal, state prerequisites, and show verification and likely failure.
- [ ] Troubleshooting is discoverable by symptom or exact error and distinguishes evidence from guesses.
- [ ] Exact reference facts are concise, authoritative, and scannable.
- [ ] The visible index is organized by reader needs and conceptual dependencies before file structure.
- [ ] Quizzes, recall prompts, and prescribed next lessons appear only in requested tutorial material.

## Gate 7 Table and Diagram Discipline

- [ ] Every table performs repeated-field comparison or exact mapping that prose or a list would handle worse.
- [ ] Table cells are concise, parallel, and introduced by the question the table answers.
- [ ] Causal or narrative reasoning was not flattened into a matrix.
- [ ] Each diagram makes direction, hierarchy, state, sequence, or ownership materially clearer.
- [ ] Diagram labels and surrounding prose explain how to read it and connect it to the real case.
- [ ] Accessibility and narrow-screen use were considered.

## Gate 8 Prose and Terminology

- [ ] Paragraph openings form a coherent outline when read alone.
- [ ] Each paragraph advances one reasoning thread in a known-to-new order.
- [ ] Sentences name actors, use precise verbs, and expose conditions and consequences.
- [ ] Undefined terms, acronyms, vague pronouns, and circular definitions are absent.
- [ ] Searchable technical terms remain available while the main prose follows the user's language.
- [ ] Analogies illuminate one relationship and exit before becoming misleading.
- [ ] “Simply,” “obviously,” “just,” “easy,” and “straightforward” do not hide reasoning.
- [ ] The tone respects an adult reader and does not become childish, padded, or condescending.

## Gate 9 Artifact and Scope

- [ ] The stable guide describes the current system rather than narrating every edit.
- [ ] A work journal exists only because the user requested it or the repository requires it.
- [ ] Durable explanations are not duplicated across guide, journal, and reference.
- [ ] Documentation work did not expand the underlying task's authority.
- [ ] Software and documentation were verified separately.
- [ ] The handoff identifies changed guide artifacts, the main model now available, and remaining uncertainty.
- [ ] A small mechanical change did not trigger a new guide, journal, tutorial, or inflated learning claim when the existing model remained current.

## Reader Outcome Spot Checks

Select several high-consequence concepts and verify that a reader can answer, without reconstructing the author's planning matrix:

1. What is this concept and what is it not?
2. Why does it exist, and why does this project use it here?
3. How does one real value or action move through it?
4. Which prerequisite ideas make that mechanism understandable?
5. Where is it implemented, and what project-specific adaptation matters?
6. What can fail or remain unproved, and how would I verify it?

Select one chapter and verify that its opening, body, example, and close all resolve the same reader question. Select each table and require a one-sentence justification for why rows and columns outperform prose.

## Red-Flag Search

Before completion, scan for:

- exhaustive file or function inventories before the reader has a model;
- matrices that replace narrative reasoning;
- definitions that use the term itself or several undefined terms;
- “A calls B” descriptions with no value, decision, or state change;
- generic textbook explanations with no project mapping;
- project-specific facts with no conceptual foundation;
- actual code presented without provenance or observation guidance;
- rationale inferred from naming alone;
- conflicting reader assumptions between adjacent sections;
- tutorial devices in a guide or reference that was not meant to teach by practice;
- personal rank labels or raw calibration answers.

## Completion Report

Lead with the authorized task outcome and verification. Then identify the guide artifacts changed, the core mental model and major concepts now explained, any optional provenance artifact created, and unresolved source conflicts or provisional reader assumptions.
