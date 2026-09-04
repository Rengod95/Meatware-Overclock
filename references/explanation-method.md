# Explanation Method

Use this method for every consequential technical concept introduced by the guide. “Consequential” means that misunderstanding the concept would prevent the reader from predicting behavior, making a decision, performing a task, diagnosing a failure, or interpreting the project correctly.

Do not create a separate heading for every term or explain every token. Give incidental familiar terms a name or inline bridge; give consequential concepts the full treatment their prerequisite depth requires.

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

## Worked Pattern for Schema

Adapt this pattern to the actual schema technology and project. Do not copy it as a generic lecture.

### Relevance and prerequisites

Start with the project input whose shape must be trusted. If the reader lacks the foundation, establish these ideas first:

1. A runtime value has a shape: fields, nesting, and value kinds.
2. A constraint says which shapes or values are allowed.
3. A program can represent those constraints as machine-readable data.
4. Another program can interpret the constraints and compare real input against them.

### What

A schema is a machine-readable description of allowed structure and constraints. It is not the runtime data itself and is not automatically the code that enforces the rules. The enforcing actor is usually a validator, compiler, database, or other consumer that interprets the schema.

Distinguish the relevant neighboring ideas:

- a static language type may check source code before runtime;
- a schema can describe data crossing a runtime or system boundary;
- validation checks a value against rules;
- business validation may require facts or relationships that structural validation cannot prove.

### Why

Generally, a schema centralizes a contract so multiple inputs can be checked consistently and tooling can inspect the rules. A project may also use the same schema to generate forms, editors, types, documentation, migrations, or compatibility checks. Verify which of these jobs actually exist here.

For the current project, explain the failure or duplication the schema prevents and why a code-only check, handwritten parser, or static type is not sufficient at this boundary—if the evidence supports that rationale.

### How generally

Show the mechanism:

1. An author or tool produces a schema document.
2. A validator loads or compiles the schema.
3. Runtime input reaches the validation boundary.
4. The validator evaluates relevant constraints.
5. It returns success, throws, or produces structured diagnostics.
6. Downstream code receives either trusted-enough input or a failure representation.

Then show a minimal example only if it clarifies the mechanism. Explain `required`, value kind, and value constraints as separate decisions; show both a passing and failing input; identify the resulting diagnostic form.

### Project adaptation

Name the actual schema file, consumer, call site, input source, output or diagnostic, and tests. Explain whether the project:

- compiles schemas ahead of time or at runtime;
- uses a standard dialect or project extensions;
- validates only structure or also domain invariants;
- derives types or documentation from the schema;
- treats generated files as outputs rather than edit targets;
- converts validator-native errors into project diagnostics.

If the project uses “schema” for something materially different, explain that difference instead of forcing conventional meaning onto the code.

### Boundary

State what a successful schema check cannot prove—for example, that an identifier exists, a transaction is authorized, two fields are semantically consistent, or the data remains valid after later mutation. Point to the component that owns those guarantees when one exists.

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
