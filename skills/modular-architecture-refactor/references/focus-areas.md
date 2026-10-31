# Priority focus areas

Use this file in Phase 2 when designing the target architecture. Apply only the areas that are relevant to the codebase in front of you.

## Contents

- [Splitting mixed responsibilities](#splitting-mixed-responsibilities)
- [Data contracts and central models](#data-contracts-and-central-models)
- [Functional boundaries](#functional-boundaries)
- [State isolation](#state-isolation)
- [Parallel implementations](#parallel-implementations)
- [Correctness and security](#correctness-and-security)
- [Target design checklist](#target-design-checklist)

## Splitting mixed responsibilities

Start with the components that concentrate the most responsibility (see the diagnostics). For each one:

1. List what it does, grouped by reason to change.
2. List what it depends on and what depends on it.
3. Find the internal seams: groups of functions and data that are used together and rarely touch the rest.
4. Extract each logically independent mechanism into its own component with a clear interface. Leave closely related code together.
5. Keep the original entry point working (as a thin facade or re-export) until all callers have moved, then remove it unless it is a public contract.

## Data contracts and central models

- Identify the key data structures: domain models, intermediate representations, DTOs, API schemas, serialization and storage formats.
- Remove cycles and ambiguity around them. A central model usually belongs in a low-level module that imports nothing project-specific above it.
- Make structures consistent across components: one definition per concept, with explicit conversions where representations must differ.
- Separate internal representations from external exchange formats (network APIs, files, databases, inter-process and cross-language communication) where they evolve independently. Map at the boundary.
- Remove implicit conversions, silent information loss, and drift between implementations (units, encodings, time zones, precision, optional versus missing fields).
- If a persisted or transmitted format must change, version it or keep backward compatibility: readers accept old and new versions; writers change only after readers are deployed.

## Functional boundaries

Typical areas of responsibility. Use only those that actually exist, and add others when the project has them:

1. Integration with external systems (third-party applications, SDKs, OS APIs, hardware).
2. Input acquisition, parsing, and normalization.
3. Domain model, computations, and algorithms.
4. Business rules, validation, and analysis.
5. Producing results, reports, errors, and diagnostic messages.
6. Network transport and communication with servers and services.
7. Storage and loading of data.
8. User interface, CLI, or the application's external API.
9. State, session, document, and request management.
10. Caching and temporary resource management.
11. Configuration, logging, and infrastructure.

Do not create a subsystem for each item mechanically. The final split must match real responsibilities. In a small program several of these may live in one module.

A common, effective dependency shape:

```text
UI / CLI / API handlers ─┐
Network, storage, SDKs ──┼──► application services ──► domain model & rules
Config, logging ─────────┘          │                         ▲
                                    └── contracts (interfaces) ┘
         adapters implement contracts; the domain never imports adapters
```

## State isolation

- Separate the state of independent entities and operations: users, sessions, documents, tasks, processing runs, network requests.
- Never let results of independent operations mix (shared buffers, module-level accumulators, reused mutable defaults).
- Ensure correct behavior on re-runs, errors, cancellation, timeouts, concurrent execution, and switching the active context (for example, the active document or account).
- Define explicit lifecycles for temporary objects, caches, connections, file handles, and other resources: who creates them, who owns them, when they are released.
- Prevent state and resource leaks between independent operations: use scoped context objects, `with`/`using`/`defer`/RAII patterns, and per-operation instances instead of globals.

## Parallel implementations

When several implementations of the same functionality exist (different languages or platforms, native and managed, client and server, old and new, different front ends):

1. Analyze them and extract the shared contract and behavioral invariants.
2. Remove duplicated logic where practical: a single shared implementation, generated code from a single schema, or one source of truth for rules and constants.
3. Preserve each implementation's specifics that are required for compatibility and correctness.
4. Do not merge implementations artificially if that complicates the architecture or reduces reliability.
5. Add checks that the implementations behave consistently: shared test vectors, golden files, contract tests, or differential tests run against each implementation.

## Correctness and security

Fix significant defects found during the work, prioritizing:

- validity and completeness of the main results;
- safety of user data;
- correctness of computations and algorithms;
- handling of external-system, I/O, and network errors (timeouts, retries, partial failures);
- security: secrets, input validation, transport protection, injection, access control;
- consistency of UI state with processing results;
- resource leaks and concurrent access.

Rules:

- Do not report errors, incomplete data, or failed operations as success.
- Keep every behavior-changing fix separate from structural changes, cover it with a test, and list it in the final report.
- If a fix would change a public contract or user-visible behavior beyond the defect itself, ask first.

## Target design checklist

Before implementing, the design should state:

- [ ] Components and the single responsibility of each.
- [ ] Public contract of each component (functions, interfaces, data types, events).
- [ ] Allowed dependency directions, with no cycles.
- [ ] Where state lives and its lifecycle.
- [ ] Which mechanisms are pluggable and why; which are deliberately not.
- [ ] Compatibility strategy for public APIs and persisted or transmitted formats.
- [ ] Migration order: which steps come first and what each step's verification is.
