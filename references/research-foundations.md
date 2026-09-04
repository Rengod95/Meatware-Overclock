# Research Foundations and Adopted Decisions

Read this file only when maintaining `meatware-overclock` or reviewing why a writing rule exists. Ordinary guide production should use the operational references instead of loading these sources again.

The evidence has three roles:

- official content and style guidance from organizations that maintain large technical documentation sets;
- information architecture patterns from widely used explanatory documentation;
- primary research on prior knowledge, text coherence, worked examples, and cognitive load.

Learning research does not prove that one document shape works for every reader. Use it to identify likely failure modes and editorial questions, not to turn the skill into a universal teaching formula.

## 1. Information types are editing lenses, not a visible matrix

Diátaxis distinguishes tutorial, how-to, reference, and explanation because they serve different reader needs. Its application guidance also warns against starting by creating four empty structures. The useful result is content that performs the right function, not a taxonomy displayed to readers.

Adopted decision: use information shapes to diagnose sections and transitions. Do not generate a mandatory four-part navigation or expose the planning taxonomy as the reader's main model.

Sources:

- [Diátaxis map](https://diataxis.fr/map/)
- [Diátaxis as a guide to work](https://diataxis.fr/how-to-use-diataxis/)
- [Diátaxis explanation](https://diataxis.fr/explanation/)
- [Tutorials and how-to guides](https://diataxis.fr/tutorials-how-to/)

## 2. Start from audience, purpose, and conceptual order

Google Technical Writing distinguishes a reader's role, existing knowledge, purpose, and intended outcome. Its large-document guidance emphasizes outlines, introductions, navigation, and progressive disclosure. GitHub and Microsoft similarly prioritize user needs, important information first, scannable headings, and usable hierarchy.

Adopted decision: form a document promise and concept dependency order before mapping files. Support both a coherent first read and later lookup.

Sources:

- [Google Technical Writing: Audience](https://developers.google.com/tech-writing/one/audience)
- [Google Technical Writing: Documents](https://developers.google.com/tech-writing/one/documents)
- [Google Technical Writing: Organizing large documents](https://developers.google.com/tech-writing/two/large-docs)
- [GitHub Docs content design principles](https://docs.github.com/en/contributing/writing-for-github-docs/content-design-principles)
- [GitHub Docs content model](https://docs.github.com/en/contributing/style-guide-and-content-model/about-the-content-model)
- [Microsoft content planning](https://learn.microsoft.com/en-us/style-guide/content-planning)
- [Microsoft scannable content](https://learn.microsoft.com/en-us/style-guide/scannable-content/)

## 3. Explanation density must vary by concept and prior knowledge

Kintsch's work on text comprehension reports that explicit, coherent text is especially important when background knowledge is low, while knowledgeable readers may construct useful inferences from some gaps. Expertise-reversal research likewise describes how guidance that helps novices can become redundant for experienced readers.

Adopted decision: never assign one global reader level. Calibrate prerequisite depth per concept, preserve causal relationships for everyone, and make familiar foundations skippable through headings and linked layers.

Sources:

- [Kintsch, Text comprehension, memory, and learning](https://pubmed.ncbi.nlm.nih.gov/8203801/)
- [Kalyuga et al., The Expertise Reversal Effect](https://doi.org/10.1207/S15326985EP3801_4)

## 4. Worked examples should expose reasoning without imposing tutoring

Self-explanation research associates successful worked-example learning with connecting actions to principles and conditions. Pre-training research examines the value of establishing component names and characteristics before presenting a complex system.

Adopted decision: examples should expose decisions, value changes, results, and governing principles. Do not infer that every guide needs exercises, recall questions, or a prescribed next lesson.

Sources:

- [Chi et al., Self-Explanations](https://doi.org/10.1207/s15516709cog1302_1)
- [Mayer, Mathias, and Wetzell, Fostering understanding through pre-training](https://pubmed.ncbi.nlm.nih.gov/12240927/)

## 5. Keep mutually dependent evidence and explanation close

Split-attention research studies the extra integration work created when mutually referring information is separated. It does not mandate one universal page layout, but it supports keeping a code excerpt near its walkthrough, a diagram near its interpretation, and a table near the conclusion readers should draw from it.

Adopted decision: place observation guidance before evidence and interpretation immediately after it. Avoid making readers shuttle between distant artifacts to reconstruct one claim.

Source:

- [Chandler and Sweller, The split-attention effect as a factor in the design of instruction](https://doi.org/10.1111/j.2044-8279.1992.tb01017.x)

## 6. Tables are for comparison and lookup, not narrative

Google's table guidance recommends lists or description lists for simpler relationships and tables for repeated multi-attribute information. It discourages one-row, one-column, layout, and code tables. Image guidance similarly expects a visual to communicate information that prose would handle poorly.

Adopted decision: require a real cross-item comparison or exact mapping, concise parallel cells, and prose before and after. Treat the number of attributes as a heuristic rather than a universal threshold.

Sources:

- [Google developer documentation style guide: Tables](https://developers.google.com/style/tables)
- [Google developer documentation style guide: Images](https://developers.google.com/style/images)

## 7. Good documentation supports more than one reading path

The Rust Book explicitly supports concept-first and project-first readers. Django's documentation guidance distinguishes topic guides from reference and asks topic guides to provide background and examples without duplicating exhaustive reference. MDN identifies prerequisites and learning outcomes and organizes foundations before extensions.

Adopted decision: do not copy one publication's hierarchy. State prerequisites, establish the main reading path, provide alternate entry points, and keep conceptual explanation connected to project evidence.

Sources:

- [The Rust Programming Language: Introduction](https://doc.rust-lang.org/stable/book/ch00-00-introduction.html)
- [Django: Writing documentation](https://docs.djangoproject.com/en/dev/internals/contributing/writing-documentation/)
- [MDN Learn web development](https://developer.mozilla.org/en-US/docs/Learn_web_development)

## 8. Friendly explanations remain precise and searchable

Well-regarded learning documents often reuse one realistic example and introduce concepts where that example needs them. React's “Thinking in React” develops a component and data model step by step; the Rust guessing-game chapter introduces language mechanisms in the context of a working program. Julia Evans argues for preserving useful jargon and filling specific knowledge gaps without condescension.

Adopted decision: keep searchable technical terms, reuse a representative case, and explain one missing relationship at a time. Plain language must not replace technical accuracy or become childish.

Sources:

- [React: Thinking in React](https://react.dev/learn/thinking-in-react)
- [The Rust Programming Language: Programming a Guessing Game](https://doc.rust-lang.org/stable/book/ch02-00-guessing-game-tutorial.html)
- [Julia Evans: Simple explanations without sounding condescending](https://jvns.ca/blog/2020/11/15/simple-explanations-without-sounding-condescending/)
- [Julia Evans: Teaching by filling in knowledge gaps](https://jvns.ca/blog/2021/09/20/teaching-by-filling-in-knowledge-gaps/)

## 9. Rejected simplifications

Do not adopt these interpretations:

- documentation must always have four top-level folders;
- novice-facing documentation must always be short;
- every concept needs an everyday analogy;
- worked examples imply that every chapter needs a quiz;
- tables are inherently more scannable than prose;
- current code automatically outranks normative documents and recorded decisions;
- one worked technology example should become a universal operational rule.

The governing principle is to connect reader purpose, prerequisite dependencies, causal mechanisms, project evidence, and usable navigation in one coherent explanation.
