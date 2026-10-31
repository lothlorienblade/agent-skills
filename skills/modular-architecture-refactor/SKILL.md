---
name: modular-architecture-refactor
description: Plans and performs behavior-preserving architectural refactoring of an existing codebase toward orthogonal, loosely coupled, highly cohesive, plugin-ready modules. Use when the user asks to restructure or modularize a project, split a god class or monolithic module, break circular dependencies, reduce coupling, separate UI, domain, I/O and integration concerns, isolate shared mutable state, introduce extension points or a plugin system, or consolidate duplicated parallel implementations. Diagnoses first, records a build and test baseline, designs the minimal sufficient target architecture, then refactors in small verified steps with characterization tests and compatibility guarantees. Language- and framework-agnostic. Do not use for small local edits, single bug fixes, new features, formatting, or ordinary code review unless the user explicitly asks for architectural restructuring.
license: MIT
metadata:
  author: lothlorienblade
  version: "1.0.0"
---

# Modular Architecture Refactor

Restructure an existing codebase so its components are independent, minimally coupled, internally cohesive, and extensible where extension pays off, **without changing what the program does**.

The goal is real independence, reliability, and lower cost of future change. It is not the number of changes made, and it is not conformance to a pattern catalog.

## The four principles (OLHP)

| Principle | One-line test |
| --- | --- |
| **Orthogonality** | Can this component be changed, replaced, or removed without editing unrelated components? |
| **Low Coupling** | Does it depend only on small, explicit, stable interfaces, with dependencies flowing in one direction? |
| **High Cohesion** | Does it have one clearly stated responsibility, with closely related code kept together? |
| **Plugin Architecture** | Where variation is real, can an implementation be added, swapped, or disabled without touching the core? |

These are goals, not dogma. Apply them in proportion to the size, maturity, and actual pain points of the codebase. Every new module, interface, or extension point must solve an observed problem. Details and anti-patterns: [references/principles.md](references/principles.md).

## Scope and mode

Decide these before touching code.

**Activation boundary.** This skill is for deliberate architectural work. If the user asked for a bug fix, a feature, or a local edit, do that task; at most, mention architectural issues you noticed. Never start a broad restructuring on your own initiative.

**Mode.**

- **Execute** (default when the user asks to refactor, restructure, modularize, decouple, or similar): implement the changes. Do not stop after a plan and do not ask for approval of each step.
- **Assess** (when the user asks only for an analysis, audit, review, or plan): run Phases 0–2, deliver findings and a staged plan, and change no code.

**Scope.** If the user named a path, module, layer, or concern, stay inside it and touch the rest only where the boundary itself must change. Otherwise, start with the highest-impact problems and expand only as far as verification allows.

**Scale.** Match depth to the project:

| Project | Appropriate depth |
| --- | --- |
| Script or small tool (≲ 2k lines) | Split mixed concerns into a few well-named modules or functions. Usually no interfaces and no plugins. |
| Medium application | Clear module boundaries, one dependency direction, explicit contracts at I/O and integration seams, isolated state. |
| Large or multi-team system | Enforced boundaries, versioned contracts, extension points for genuinely variable mechanisms, incremental migration paths. |

**Stop and ask** only before risky actions: possible loss of user data, incompatible changes to public contracts or persisted formats, destructive migrations, history rewrites, or anything irreversible. Otherwise proceed autonomously.

## Workflow

Work in phases. Keep the program working between steps.

### Phase 0 — Orient and record a baseline

1. Read project instructions and follow them: `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `README`, `docs/`, ADRs, editor and agent rule files. When they conflict with this skill, follow the stricter rule.
2. Identify languages, frameworks, build system, package managers, test runner, linters, type checkers, and CI configuration.
3. Identify external systems: third-party applications and APIs, SDKs, databases, network services, file formats, hardware, operating system features.
4. **Record the baseline before any change**: run the available build, tests, linters, and type checks, and save the results (pass/fail counts, notable failures). This separates pre-existing failures from regressions you introduce.
5. Check for an existing task tracker or agent memory (see [Task tracking and handoff](#task-tracking-and-handoff)).

### Phase 1 — Diagnose

Find real architectural problems, ranked by impact. Look for:

- disproportionately large files, classes, or functions;
- high fan-in or fan-out, and import cycles;
- mixed layers: UI, business rules, I/O, and integrations in one place;
- files that change together frequently (use Git history when available to find hotspots and hidden coupling);
- logic that cannot be tested without starting external systems;
- global or shared mutable state;
- duplicated logic and parallel implementations of the same behavior;
- ambiguous or drifting data contracts.

Also note significant defects in correctness, data safety, error handling, security, concurrency, and resource handling. Commands, heuristics, and a smell-to-remedy table: [references/diagnostics.md](references/diagnostics.md).

### Phase 2 — Design the target architecture

Define the components, the responsibility of each, their public contracts, and the allowed dependency directions. Dependencies point from volatile mechanisms (UI, network, storage, integrations, frameworks) toward stable contracts and domain logic.

Choose the **minimal sufficient** design that resolves the problems found in Phase 1. For each proposed abstraction, name the problem it solves; drop it if you cannot. Use only the functional boundaries that actually exist in the project. Guidance on boundaries, data contracts, state isolation, and parallel implementations: [references/focus-areas.md](references/focus-areas.md).

In **Assess** mode, stop here and deliver the report.

### Phase 3 — Refactor incrementally

- Order the work: foundational contracts and dependencies first, then the most problematic components.
- Before changing code that tests do not cover, add **characterization tests** that pin its current behavior.
- Make small, logically complete steps. Each step either restructures or changes behavior, never both.
- Use temporary adapters or shims when needed to keep callers working. Remove them before you finish unless they are part of a deliberate, documented compatibility promise.
- After each step, build and run the affected tests. Fix regressions before starting dependent changes.

Safe step-by-step techniques (seams, expand–contract, branch by abstraction, registries, dependency injection without frameworks): [references/refactoring-techniques.md](references/refactoring-techniques.md).

### Phase 4 — Verify

- Run existing tests and add tests where the restructuring created new contracts: contract, unit, and integration tests in the most critical areas.
- Test behavior, not just that imports resolve and files moved.
- Build every compilable component and target platform for which tools are available.
- When a scenario needs something unavailable here (third-party application, hardware, paid or production service), record that it was not verified automatically. Never claim it works.

### Phase 5 — Final review and report

Confirm that no duplicated logic, dead alternative implementations, or half-finished internal migrations remain. Compare build, test, lint, and type-check results with the Phase 0 baseline. Check contract compatibility and the main user scenarios. Then write the report described in [references/verification-and-reporting.md](references/verification-and-reporting.md).

## Non-negotiable constraints

- Preserve all existing functionality.
- Preserve compatibility with external systems, public APIs, CLIs, file and configuration formats, data schemas, network protocols, and server contracts. If a change is unavoidable, provide backward compatibility or a migration, and version persisted or transmitted formats.
- Change behavior only to fix confirmed defects. Keep each fix separate from structural changes, cover it with a test, and list it in the report.
- Never mask errors, partial data, or failed operations as success.
- Do not delete or overwrite user settings, credentials, logs, databases, saved results, or other user data.
- Do not create abstractions, classes, interfaces, or files only to satisfy a principle.
- Do not add dependencies without a clear need.
- Do not leave duplicated logic or unused alternative implementations behind.
- Do not replace real checks with assumptions that things work.
- Do not modify task-tracker files or agent configuration unless needed.
- Follow the project's Git policy. Do not commit agent scratch files. Do not commit, push, merge, rebase, or sync with remotes unless the user or the project rules allow it.

## Avoiding over-engineering

Prefer the simplest structure that removes the observed problem:

- A function or module boundary before a class hierarchy.
- A plain interface or protocol at a real seam before a framework.
- A registry or explicit composition root before a plugin loader.
- Constructor or parameter injection before a DI container.
- One implementation behind an interface only when a test double or a second implementation genuinely needs it.

Do not fragment cohesive code into many tiny files. Do not unify implementations that differ for good reasons if that makes the result more complex or less reliable.

## Task tracking and handoff

The work must be resumable by another agent with no access to this conversation.

**If the project already uses a tracker or agent memory** (Beads, an issue tracker, task files described in project instructions): restore context from it and check it against the code, create an epic with small subtasks, record dependencies and done criteria, keep statuses current, record key decisions and verification results, and close only finished, verified tasks. If the work cannot finish in this session, leave the code in a consistent working state and record what remains.

**If it does not**, do not introduce one without the user's agreement, and do not create parallel logs. Put a handoff section in the final report instead.

## Final report

Briefly cover:

1. Resulting architecture: components, responsibilities, dependency directions.
2. Key changes and the problems they removed.
3. Defects fixed (each with its test).
4. Verification results compared with the baseline.
5. Remaining limitations and unverified scenarios.
6. Task status and handoff context.

Template: [references/verification-and-reporting.md](references/verification-and-reporting.md).

## Success criteria

- Each component has a clear, cohesive responsibility.
- Independent components can be changed and tested largely in isolation.
- Cross-module dependencies are minimal, explicit, and mostly one-directional.
- Variable mechanisms can be replaced or disabled without core changes where that is practical.
- Duplication and mixed responsibilities are substantially reduced.
- State of independent entities and operations is reliably isolated.
- Existing functionality and external contracts are preserved.
- Checks pass at least as well as the baseline, and unverified scenarios are stated explicitly.
- The code is easier to maintain, extend, and hand over to other developers and agents.

## Reference files

Load only what the current phase needs:

| File | Load when |
| --- | --- |
| [references/principles.md](references/principles.md) | Weighing a design choice against OLHP, or checking for over-engineering |
| [references/diagnostics.md](references/diagnostics.md) | Phase 1: finding hotspots, cycles, mixed concerns, hidden coupling |
| [references/focus-areas.md](references/focus-areas.md) | Phase 2: boundaries, data contracts, state isolation, parallel implementations, correctness and security |
| [references/refactoring-techniques.md](references/refactoring-techniques.md) | Phase 3: executing changes safely in small steps |
| [references/verification-and-reporting.md](references/verification-and-reporting.md) | Phase 0 baseline, Phases 4–5, handoff, and the final report |
