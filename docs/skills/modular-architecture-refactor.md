# Modular Architecture Refactor

[← All skills](../../README.md) · [Skill source](../../skills/modular-architecture-refactor/SKILL.md) · [Trigger evals](../../evals/modular-architecture-refactor/trigger-cases.json)

Guides AI coding agents through **behavior-preserving architectural refactoring**: turning tangled codebases into orthogonal, loosely coupled, highly cohesive, plugin-ready modules.

```bash
npx skills add lothlorienblade/agent-skills --skill modular-architecture-refactor
```

Other installation options (Claude Code plugin marketplace, manual copy) are in the [main README](../../README.md#installation).

## Why

Asking an agent to "clean up the architecture" often produces one of two failures: a shallow list of recommendations with no code changes, or an over-engineered rewrite that breaks behavior and adds layers nobody needs. This skill gives the agent a disciplined method that sits between the two:

- **It acts.** When you ask for a refactoring, the agent implements it, not just a plan.
- **It preserves behavior.** A build and test baseline comes first, characterization tests pin uncovered code, and every step is verified before the next one.
- **It stays proportionate.** Principles are applied to the size and real problems of the project. Every new abstraction has to name the problem it solves.
- **It is honest about verification.** Scenarios that cannot be tested in the current environment are reported as unverified, never assumed to work.
- **It can be handed over.** The work and its context can be picked up by another agent or developer without the original conversation.

## The four principles (OLHP)

| Principle | What it means here |
| --- | --- |
| **Orthogonality** | Components can be changed, replaced, or removed without editing unrelated ones. State, configuration, and side effects stay local. |
| **Low Coupling** | Few, explicit, stable interfaces. No cycles or hidden globals. Dependencies flow from UI, network, storage, and integrations toward contracts and domain logic. |
| **High Cohesion** | Each module has one clearly stated responsibility, without fragmenting code into pointless tiny pieces. |
| **Plugin Architecture** | Where variation is real (formats, providers, backends, platforms), implementations sit behind a contract and a simple registry, not a heavyweight framework. |

## What the agent does

1. **Orient and record a baseline.** Reads project instructions (`AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, docs, ADRs), identifies the toolchain and external systems, and runs the existing build, tests, linters, and type checks before changing anything.
2. **Diagnose.** Finds god modules, mixed layers, import cycles, hidden and shared mutable state, duplicated or parallel implementations, leaky data contracts, and Git change hotspots. Notes correctness and security defects along the way.
3. **Design.** Defines the minimal sufficient target architecture: components, responsibilities, contracts, dependency directions, state ownership, and compatibility strategy.
4. **Refactor incrementally.** Small structural steps, each built and tested; behavior-changing defect fixes kept separate and covered by tests; temporary adapters removed at the end.
5. **Verify.** Behavior-level tests, contract and integration tests at critical seams, builds of all available targets, comparison with the baseline.
6. **Report and hand off.** Resulting architecture, key changes, fixed defects, verification versus baseline, unverified scenarios, and remaining work. Uses the project's existing task tracker if there is one.

It asks before risky actions only: possible data loss, incompatible changes to public contracts or persisted formats, destructive migrations, history rewrites. It follows the project's Git policy and does not commit or push unless allowed.

## Usage

The skill activates automatically when a request is about architectural restructuring. It is designed **not** to activate for ordinary bug fixes, features, small edits, or routine code review.

Explicit invocation:

| Agent | Command |
| --- | --- |
| Claude Code | `/modular-architecture-refactor [optional scope]` |
| Codex | `$modular-architecture-refactor [optional scope]` |

Example requests:

```text
Refactor this project into a modular architecture. main.py mixes the GUI, database access and business rules.
```

```text
Our services package has circular imports. Untangle the dependencies without changing behavior.
```

```text
Make export formats pluggable instead of editing the switch in ReportService every time.
```

```text
Analyze the architecture of src/billing and propose a staged plan to reduce coupling. Don't change code yet.
```

The last example runs in **assess** mode: diagnosis and a plan, no code changes. Requests to refactor, restructure, or decouple run in **execute** mode.

## Files

```text
skills/modular-architecture-refactor/
├── SKILL.md                         # Core workflow, loaded on activation
├── agents/openai.yaml               # Codex UI metadata
└── references/                      # Loaded on demand
    ├── principles.md                  # OLHP in practice, over-engineering test
    ├── diagnostics.md                 # Hotspots, cycles, smell-to-remedy table
    ├── focus-areas.md                 # Boundaries, data contracts, state, parallel implementations
    ├── refactoring-techniques.md      # Seams, expand–contract, branch by abstraction, registries
    └── verification-and-reporting.md  # Baseline, testing, handoff, report template
```

The skill follows the [Agent Skills specification](https://agentskills.io/specification): a compact `SKILL.md` with the essential rules, and detailed references loaded only when a phase needs them. It has no runtime dependencies and no scripts.

## Language and framework support

The method is language-agnostic. Reference material includes commands and tool suggestions for JavaScript/TypeScript, Python, Java/Kotlin, .NET, Go, Rust, and C/C++, and the agent uses whatever tools the project already has.

## Related skills

- [Codebase Audit](codebase-audit.md) — a broader, read-only health check of the whole project. Run it first to find out whether architecture is the main problem; its architectural findings are a natural input for this skill.

## Origin

This skill is an English adaptation and extension of the author's original architectural refactoring prompt, preserved in [`docs/original-prompts/modular-architecture-refactor.ru.md`](../original-prompts/modular-architecture-refactor.ru.md).
