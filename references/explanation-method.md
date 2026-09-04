# Explanation Method

Use this method for every consequential technical concept introduced by the guide. “Consequential” means that misunderstanding the concept would prevent the reader from predicting behavior, making a decision, performing a task, diagnosing a failure, or interpreting the project correctly.

Do not create a separate heading for every term or explain every token. Give incidental familiar terms a name or inline bridge; give consequential concepts the full treatment their prerequisite depth requires.

Treat a concept as consequential when later reasoning depends on it, it changes a value's meaning or a component's responsibility, it owns an important failure or tradeoff, its technical meaning differs from ordinary use, this project adapts the convention, or misunderstanding it could cause a bad change or diagnosis. A technical concept introduced by the guide and relied on later is consequential by default; exclude it only when the reader model already owns it or it is genuinely incidental to the document promise.

## Keep an Internal Concept Coverage Note

For each consequential concept, record privately while drafting:

- the reader question it resolves;
- direct prerequisites and their calibration state;
- the project evidence that supports the explanation;
- general convention versus project-specific use;
- the example or trace that demonstrates the mechanism;
- the important boundary, failure, or misconception;
- whether the guide already covers what, why, and how.

Use bullets or another compact form. Do not publish this as a matrix unless readers genuinely need a comparison.

## The Full Concept Unit

Adapt these moves to the concept. They may span several paragraphs and examples; they are not mandatory visible headings.

### 1. Establish relevance

Start with the reader's real question, a representative failure, or the point in the running case where the concept becomes necessary. A familiar situation can help, but do not invent a long analogy merely to make the prose feel friendly.

### 2. Explain what it is

Give a plain-language meaning and the searchable technical term. Then make the meaning precise enough for this document:

- name the thing's role or mechanism;
- distinguish it from the nearest confusable concept;
- state whether it is data, a rule, a process, an interface, a runtime object, or a document;
- define the scope and important non-scope.

Avoid circular definitions and definitions composed mainly of new jargon.

### 3. Explain why it exists

Describe the concrete problem that appears without the concept and the constraint or tradeoff it addresses. Separate:

- why the concept exists in software generally;
- why this project needs it;
- why this project chose this form instead of a relevant alternative.

Do not invent rationale from file names. Label inference and verify decisions against ADRs, tests, history, or maintainers when available.

### 4. Explain how it works generally

Describe the causal mechanism, not only the public surface:

- what enters;
- which actor interprets, decides, or transforms it;
- in what order important decisions occur;
- what state or value changes;
- what comes out;
- how failure appears.

Use a value trace, before-and-after state, or short flow when that is clearer than prose. Explain implementation details only to the depth needed to make the mechanism predictive.

### 5. Close prerequisite gaps recursively

Before relying on another concept, apply `calibration.md` to that prerequisite. Insert an inline bridge, teach the foundation first, or link to a dedicated foundation. Return explicitly to the original concept after the detour so the reader knows why the prerequisite mattered.

### 6. Map the general concept to this project

Show both continuity and adaptation:

- what follows common usage;
- what this project adds, narrows, renames, or omits;
- which module owns the behavior;
- who calls it and what it calls next;
- actual input, output, state, diagnostics, and side effects;
- which tests or generated artifacts demonstrate the contract.

Write the mapping as connected prose or a trace, not as a bare path list.

### 7. Demonstrate it

Choose the smallest realistic evidence that reveals the mechanism:

- **Simplified example:** invented or reduced to isolate one behavior; not a project API.
- **Actual project code:** verified in the current source without semantic alteration.
- **Abridged actual code:** real code with irrelevant regions explicitly omitted.

Before code, state the question and values to watch. After code, walk through important decisions in execution order, show the result or failure, and reconnect it to the project model. If syntax is not the learning goal, prefer a value trace or pseudocode over a large code block.

### 8. State boundaries and verification

End the unit by saying what the concept does not guarantee, one likely misconception or failure boundary, and how the reader can verify the behavior. This turns a memorable description into a model that can survive real work.

### 9. Reconnect to the whole

State how this concept changes the representative case or larger system model. The reader should not have to infer why the detour mattered.

## Explain Relationships, Not Dictionaries

Names such as `parse`, `validate`, `normalize`, `resolve`, `compile`, and `serialize` become meaningful when the reader sees how the value changes between them. Explain:

- the input and output representation of each stage;
- the decision or transformation unique to it;
- why the order matters;
- what failure each stage owns;
- what the next stage may assume.

A short value trace usually teaches more than six isolated glossary definitions.

## Use Analogies with an Exit

An analogy should illuminate one relationship already present in the mechanism. Keep it to one or two sentences, then return to literal technical facts. State the mismatch if extending the analogy would create a false prediction. Do not build an entire explanation around decorative characters, stories, or metaphors unrelated to the real causal flow.

## Make Examples Carry Reasoning

A good example exposes the decision points an expert might otherwise skip. Include the reason for an important line or choice, not only a paraphrase of syntax. When useful, contrast one nearby failing case with the successful case so the boundary becomes visible.

Use several examples only when variation reveals what is general and what is incidental. Do not add exercises, faded examples, or retrieval questions unless the user requested tutorial or practice material.

## Keep the Tone Adult and Precise

Plain language is not childish language. Preserve searchable terms, acknowledge real complexity, and omit filler. Avoid “simply,” “obviously,” “just,” “easy,” and “straightforward” when they hide work or assumptions. Friendly writing comes from relevance, explicit reasoning, accurate examples, and respect for the reader's time.
