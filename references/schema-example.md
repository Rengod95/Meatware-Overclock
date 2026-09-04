# Optional Worked Concept Example: Schema

Read this reference only when a schema is consequential to the requested guide. It demonstrates how to apply the technology-neutral method in `explanation-method.md`; it is not a required section, a universal schema definition, or part of the standalone master prompt.

## Relevance and prerequisites

Start with the project input whose shape must be trusted. If the reader lacks the foundation, establish these ideas first:

1. A runtime value has a shape: fields, nesting, and value kinds.
2. A constraint says which shapes or values are allowed.
3. A program can represent those constraints as machine-readable data.
4. Another program can interpret the constraints and compare real input against them.

## What

A schema is a machine-readable description of allowed structure and constraints. It is not the runtime data itself and is not automatically the code that enforces the rules. The enforcing actor is usually a validator, compiler, database, or other consumer that interprets the schema.

Distinguish the relevant neighboring ideas:

- a static language type may check source code before runtime;
- a schema can describe data crossing a runtime or system boundary;
- validation checks a value against rules;
- business validation may require facts or relationships that structural validation cannot prove.

## Why

Generally, a schema centralizes a contract so multiple inputs can be checked consistently and tooling can inspect the rules. A project may also use the same schema to generate forms, editors, types, documentation, migrations, or compatibility checks. Verify which of these jobs actually exist here.

For the current project, explain the failure or duplication the schema prevents and why a code-only check, handwritten parser, or static type is not sufficient at this boundary—if the evidence supports that rationale.

## How generally

Show the mechanism:

1. An author or tool produces a schema document.
2. A validator loads or compiles the schema.
3. Runtime input reaches the validation boundary.
4. The validator evaluates relevant constraints.
5. It returns success, throws, or produces structured diagnostics.
6. Downstream code receives either trusted-enough input or a failure representation.

Use a minimal example only if it clarifies the mechanism. Explain required fields, value kinds, and value constraints as separate decisions; show both a passing and failing input; identify the resulting diagnostic form.

## Project adaptation

Name the actual schema file, consumer, call site, input source, output or diagnostic, and tests. Explain whether the project:

- compiles schemas ahead of time or at runtime;
- uses a standard dialect or project extensions;
- validates only structure or also domain invariants;
- derives types or documentation from the schema;
- treats generated files as outputs rather than edit targets;
- converts validator-native errors into project diagnostics.

If the project uses “schema” for something materially different, explain that difference instead of forcing conventional meaning onto the code.

## Boundary

State what a successful schema check cannot prove—for example, that an identifier exists, a transaction is authorized, two fields are semantically consistent, or the data remains valid after later mutation. Point to the component that owns those guarantees when one exists.
