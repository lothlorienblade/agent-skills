# Codebase Audit

[← All skills](../../README.md) · [Skill source](../../skills/codebase-audit/SKILL.md) · [Trigger evals](../../evals/codebase-audit/trigger-cases.json)

A **read-only audit** of an existing codebase that ends in a prioritized list of the significant problems to fix before development continues, each with its location, why it matters, and a recommended fix.

```bash
npx skills add lothlorienblade/agent-skills --skill codebase-audit
```

Other installation options (Claude Code plugin marketplace, manual copy) are in the [main README](../../README.md#installation).

## Why

Asking an agent to "check the project" usually gets one of two results: a long list of style nitpicks mixed with real bugs, or a confident summary that nobody verified. Neither tells you what to do next. This skill makes the agent produce something you can act on:

- **It changes nothing.** The audit only reads code and runs existing checks. Even a one-line fix goes into the report, so you decide what happens and when.
- **It verifies before reporting.** Every finding is traced through the code and, where possible, reproduced. Each one is marked *confirmed* or *likely*.
- **It prioritizes for your next step.** Significance is judged against what you are about to build, not in the abstract. P0 blockers come first, and P3 stays short.
- **It filters noise.** Style, taste, micro-optimizations, and hypothetical problems without a realistic scenario are left out.
- **It respects your rules.** Principles from `AGENTS.md`, `CLAUDE.md`, and ADRs become audit criteria.

## What the agent does

1. **Orients.** Reads project instructions, identifies the stack, entry points, module structure, tests, CI, and external integrations, and works out what the next stage of development is.
2. **Runs baseline checks.** Existing tests, linters, type checks, and build. Failures are findings; anything that cannot run is reported, not assumed to pass.
3. **Sweeps nine dimensions.** Correctness, reliability, security and privacy, architecture, tests, build and dependencies, diagnosability and error UX, performance, maintainability. Effort goes where the risk is: change hotspots, external boundaries, critical paths.
4. **Verifies each finding** by tracing calls and, where possible, reproducing it with a test or a probe script outside the project.
5. **Prioritizes** from P0 (blocker) to P3 (low), ordering by impact, likelihood, cost, and dependencies between fixes.
6. **Reports** an overall verdict, baseline results, a summary table, detailed findings, the recommended order of work, and open questions. It then suggests where to start and waits for your go-ahead.

## Usage

The skill activates automatically when you ask for an audit, health check, readiness review, or technical-debt list. It is designed **not** to activate for diff or PR reviews, bug fixes, feature work, or architecture-only refactoring.

| Agent | Command |
| --- | --- |
| Claude Code | `/codebase-audit [optional scope or goal]` |
| Codex | `$codebase-audit [optional scope or goal]` |

Example requests:

```text
Audit this codebase and tell me what has to be fixed before we continue development. Don't change anything yet.
```

```text
We're about to build offline mode on top of src/sync. Do a readiness review of that module first.
```

```text
Give me a technical debt inventory for this project, ordered by priority.
```

## Report format

Each finding looks like this:

```markdown
### [P0-1] Session file is overwritten in place and can be lost on crash

- **Location:** `app/storage/session.py:48`
- **Problem:** `save_session()` writes JSON directly over the existing file…
- **Why it matters:** The user is silently logged out after a crash…
- **Recommendation:** Write to a temporary file and replace atomically…
- **Effort:** S · **Confidence:** confirmed
```

The full template is in [`references/report-template.md`](../../skills/codebase-audit/references/report-template.md).

## Files

```text
skills/codebase-audit/
├── SKILL.md                    # Workflow, priorities, report outline
├── agents/openai.yaml          # Codex UI metadata
└── references/                 # Loaded on demand
    ├── audit-checklist.md        # Questions per dimension, hotspots, tooling by ecosystem
    └── report-template.md        # Report structure, effort scale, example finding
```

## Related skills

- [Modular Architecture Refactor](modular-architecture-refactor.md) — when the audit shows that the main problems are architectural, use it for a behavior-preserving restructuring.

## Origin

This skill is an English adaptation and extension of the author's original audit prompt, preserved in [`docs/original-prompts/codebase-audit.ru.md`](../original-prompts/codebase-audit.ru.md).
