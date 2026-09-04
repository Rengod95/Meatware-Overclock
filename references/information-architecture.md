# Reader-Centered Information Architecture

Use this reference to plan a long guide, chapter sequence, landing page, or index. The goal is not to fit content into a universal matrix. The goal is to make the reader's questions resolve in a coherent order while preserving fast lookup paths.

## Start with the Document Promise

Write one sentence that states what the reader will understand or be able to decide or do after reading. Add the intended reader, prerequisites, and reasonable non-scope. Remove sections that do not help fulfill that promise.

Before naming folders or APIs, answer:

1. What human or product problem exists?
2. What result does the system produce for whom?
3. What is the smallest accurate model that predicts the main behavior?
4. Which representative case will make that model concrete?
5. Which concepts and mechanisms must the reader understand to follow the case?
6. Where does the project behave conventionally, and where does it adapt or depart from convention?
7. What fails, how is failure represented, and how can the reader verify claims?

## Build the Guide at Three Scales

### Whole guide

A strong default progression is:

1. Reader problem, document promise, prerequisites, and non-scope.
2. **Core mental model:** the smallest sufficient set of actors, boundaries, state, and transformations needed to predict the representative behavior.
3. One realistic case from input or user action to observable result.
4. Concepts and mechanisms in prerequisite order, introduced when the case needs them.
5. The project map: responsibility boundaries, dependency direction, and the real modules that implement the model.
6. Common applications or maintenance tasks when the audience needs them.
7. Design reasons, alternatives, and consequences where understanding depends on them.
8. Failure, diagnosis, and verification paths.
9. Exact lookup reference for names, inputs, outputs, errors, lifecycle, and generated artifacts.

This is a decision pattern, not a mandatory table of contents. Omit, merge, or reorder parts to fit the document promise and repository conventions. Do not label the model by reading time; “five-minute” encourages compression even when the smallest accurate model needs more space.

### Chapter or major section

Each chapter should resolve one coherent reader question:

1. State the question and why it matters here.
2. Connect it to the core model or representative case.
3. Introduce prerequisites before the concept that depends on them.
4. Explain the mechanism or decision in a causal order.
5. Map it to actual project evidence.
6. Show a realistic trace, example, or failure when it clarifies the mechanism.
7. State the boundary, tradeoff, or verification point.
8. Close by reconnecting the result to the larger system—not with a quiz or compulsory “next lesson.”

### Paragraph and sentence

- Make the opening sentence establish the paragraph's central claim or reader question.
- Keep one reasoning thread per paragraph. Move side facts to a new paragraph, note, or reference.
- Progress from known context to new information.
- Name the actor and use a precise verb when behavior matters: “the validator returns diagnostics” is clearer than “diagnostics are returned.”
- Use causal connectives accurately: because, therefore, only when, before, after, unless, and in contrast.
- Resolve pronouns and vague words such as “this,” “it,” and “thing” when more than one referent is possible.
- Answer what, why, and how at the scale where the reader needs them. Do not mechanically force all three into every paragraph.

## Use Information Shapes Deliberately

Diátaxis categories remain useful as authoring checks, but they are not a complete visible architecture for every guide. Choose a primary reader question for each section and use the corresponding shape:

- **Orientation:** Where am I, what problem does this solve, and what is in or out of scope?
- **Concept and mechanism:** What is this, why does it exist, and how does it behave?
- **Trace or worked example:** What happens to one concrete case from start to result?
- **Procedure:** How do I achieve a specific real-world goal, under which starting conditions, and how do I verify it?
- **Rationale and decision:** Why did this project choose this design, what alternatives existed, and what consequences follow?
- **Diagnosis and troubleshooting:** Given this symptom, what evidence distinguishes likely causes, and what action is safe?
- **Reference:** What exactly is the name, signature, input, output, state, error, default, lifecycle, or compatibility rule?
- **Authority and status:** Is this current runtime behavior, a normative rule, generated output, historical context, or a proposal?

Examples, diagrams, callouts, and tables are supporting forms, not content purposes. A long article may combine several shapes when keeping context near the reader's task improves understanding. Signal transitions with headings and prose rather than exposing a classification matrix.

## Design Two Navigation Paths

Support both of these behaviors:

- **First read:** a continuous path that builds the model in dependency order.
- **Later lookup:** headings and links that let a reader land directly on a concept, task, failure, or exact reference without rereading the guide.

Write headings in the reader's vocabulary. For explanatory chapters, a specific question or claim is often more useful than an internal component name. Preserve exact component names in reference headings where searchability matters.

For a large guide, make the index reveal relationships:

- group by reader problem, concept family, or system responsibility before listing files;
- place foundational concepts before concepts that depend on them;
- keep task titles goal-oriented;
- keep troubleshooting discoverable by symptom or exact error text;
- keep exact APIs and files in a stable lookup section;
- add cross-links at real dependency points, not a generic wall of “related links.”

Readers may arrive from search in the middle. Make each major section locally orienting: state where it sits in the system, what it assumes, and which earlier foundation to consult if necessary.

## Control Disclosure Without Hiding the Truth

Progressive disclosure means ordering and linking detail, not deleting important constraints.

- Put the minimum accurate model and high-consequence boundaries in the main path.
- Move exhaustive variants, edge cases, historical detail, and full signatures to local notes or reference sections.
- Offer deeper layers at the point the reader encounters the need.
- Do not make a simple opening model false. Mark simplifications and state where they stop predicting behavior.
- Do not explain the entire field “from the beginning” when the reader only lacks one prerequisite link.

## Use Tables Only When Structure Earns Them

Use a table when readers must compare or map at least several items across the same stable fields, or when exact row-and-column lookup is materially faster than prose. Typical cases include option comparisons, state transitions, compatibility, or a value's repeated transformation across stages.

Prefer prose, a list, or a small flow when:

- the relationship is causal or narrative;
- cells would contain several sentences;
- the rows do not share truly parallel attributes;
- reading order matters more than cross-comparison;
- the table merely converts headings and paragraphs into boxes;
- accessibility or narrow screens would make the table harder to use.

Introduce every table with the question it answers. Explain the important relationship after the table. Never use a matrix as a substitute for reasoning.

## Use Diagrams Only for Relationships

Use a diagram when direction, hierarchy, state, sequence, or ownership is materially clearer than prose. Keep the scope small, label arrows by meaning, explain how to read the diagram, and reconnect it to the representative case. Do not add a diagram to decorate an otherwise spec-like page.

## Avoid Spec-First Failure Modes

Revise when the draft:

- opens with packages, files, schemas, or signatures before the problem and model;
- lists components without explaining relationships or causal behavior;
- presents every module at equal depth;
- uses a matrix as the main narrative;
- separates general concepts from project code so completely that the reader cannot connect them;
- gives exact rules without saying why they matter or how to recognize their effects;
- mixes current behavior, policy, and proposals in one voice;
- adds quizzes, review questions, or a learning path when the requested artifact is a guide or reference rather than a tutorial.
