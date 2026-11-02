---
name: codebase-audit
description: Performs a comprehensive, read-only audit of an existing codebase and produces a prioritized list of the significant problems that should be fixed before development continues, each with its location, why it matters, and a recommended fix. Covers correctness, reliability, security and privacy, architecture, tests, build and dependencies, diagnosability, performance, and maintainability, and verifies every finding before reporting it. Use when the user asks for a codebase audit, health check, technical review, or readiness assessment of a project, asks what must be fixed before the next stage, release, or feature, or wants a prioritized technical-debt list. Changes no code. Do not use for reviewing a specific diff or pull request, for fixing a known bug, or for architecture-only analysis or restructuring (modular-architecture-refactor covers that).
license: MIT
metadata:
  author: lothlorienblade
  version: "1.0.0"
---

# Codebase Audit

Find the **significant** problems that remain in a codebase and must be addressed before development continues, then turn them into a prioritized plan of action.

The value of the audit is accuracy and prioritization, not volume. Ten verified, important findings are worth more than fifty mixed remarks.

## Analysis only

Change nothing at this stage.

- Do not edit, create, or delete project files. Do not commit, install or upgrade dependencies, or change configuration.
- Allowed: reading and searching code, `git status`/`log`/`diff`/`blame`, and running the project's existing tests, linters, type checkers, and build, as long as they do not modify tracked files. Put any temporary file, such as a probe script, in a temporary directory outside the project.
- Even an obvious one-line fix goes into the report, not into the code.

## Scope and context

1. **Requested scope.** If the user named an area (a path, module, or subsystem) or a goal ("before the release", "before adding PDF export"), focus on it and touch the rest only where it affects that area. Otherwise audit the whole project.
2. **Project instructions.** Read `AGENTS.md`, `CLAUDE.md`, `README`, `CONTRIBUTING`, `docs/`, ADRs, and agent or editor rule files. Their principles and rules are audit criteria: violating a rule the project states is a finding.
3. **The next stage.** Work out what will be developed next: from the user's words, recent commits, uncommitted changes, TODOs, issues, or a roadmap. If it is unclear, assess general readiness for further development. Judge each problem's significance relative to that stage.

## Workflow

### 1. Orient

Identify the stack, entry points, module structure and dependency directions, build and packaging, tests, CI, and external integrations (APIs, SDKs, file formats, operating system features, hardware). Use `git status` and `git log` to see what changed recently and what is unfinished. Uncommitted changes are in scope; mark findings in them as such.

Match depth to size: a small tool needs a focused pass over its few critical paths, a large system needs a pass per subsystem, starting with the riskiest.

### 2. Run the baseline checks

Run the available tests, linters, type checks, and build. Record the results: failures and warnings are findings in their own right. If something cannot be run (missing environment, secrets, hardware, or too long), say so in the report rather than assuming it passes.

### 3. Sweep the dimensions

Spend effort by risk: critical paths and external boundaries thoroughly, auxiliary code briefly. Detailed questions and tool suggestions for each dimension: [references/audit-checklist.md](references/audit-checklist.md).

| Dimension | What to look for |
| --- | --- |
| Correctness | Logic errors, edge cases, wrong error handling, races, resource leaks, inconsistent state |
| Reliability | Network and timeouts, retries, cancellation of long operations, partial failures, loss or corruption of user data |
| Security and privacy | Secrets in code, logs, or history, injection, unsafe deserialization, token and session storage, permissions |
| Architecture | High coupling, dependency cycles, god objects, UI mixed with logic and I/O, global mutable state, duplicated parallel implementations, violations of the project's own principles |
| Tests | Untested critical paths, tests that assert nothing, flaky or environment-dependent tests |
| Build and dependencies | Reproducibility, unpinned or vulnerable versions, platform differences, packaging and distribution |
| Diagnosability and error UX | Swallowed exceptions, unhelpful messages to the user, missing logs where failures must be investigated |
| Performance | Only where it is noticeable: blocked UI, quadratic work on large inputs, redundant I/O |
| Maintainability | Dead code, accumulated TODO/FIXME, documentation that contradicts the code |

### 4. Verify every finding

Before a problem goes into the report:

- read the surrounding code and trace the calls, to make sure it is not handled elsewhere;
- confirm it where possible: with an existing test, by running the code, or with a probe script in a temporary directory;
- state the confidence: **confirmed** (reproduced, or follows unambiguously from the code) or **likely** (a plausible scenario that was not verified).

Leave out style and naming, matters of taste, micro-optimizations, hypothetical problems without a realistic scenario, and "rewrite it in another framework" without a concrete pain point.

### 5. Prioritize

| Priority | Criterion |
| --- | --- |
| **P0 — blocker** | Breaks a core function, loses or corrupts data, is a security vulnerability, or the build or tests fail. Fix before any new work |
| **P1 — high** | Gets in the way of the next stage of development, or is likely to hit users; an architectural obstacle to planned work |
| **P2 — medium** | A real risk or debt that grows more expensive over time but does not block |
| **P3 — low** | Worth doing when convenient. Keep this list short |

Within a level, order by impact × likelihood relative to the cost of the fix, and respect dependencies: if fixing A simplifies or removes B, A comes first.

## Report

Write in the user's language. Back every claim about the code with a `path:line` reference. Full template with an example: [references/report-template.md](references/report-template.md).

1. **Overall state** — two to four sentences: how ready the project is for further development and what matters most.
2. **Baseline checks** — what was run and with what result; what could not be run.
3. **Summary table** — `ID | Priority | Problem | Location | Effort (S/M/L)`.
4. **Findings**, from P0 to P3, each with: location, the problem, why it matters (a concrete consequence and its link to the next stage), the recommended fix (an approach, not a ready patch; alternatives when they differ materially), effort, and confidence.
5. **Recommended order of work** — the sequence of fixes, respecting the dependencies between them; what can deliberately wait.
6. **Open questions** — what cannot be decided without the user: unclear requirements, whether a behavior is intended.

If no significant problems were found, say so. Do not pad the list with trivia.

End by suggesting where to start fixing, and do not start without the user's explicit confirmation. When the main problems are architectural and call for restructuring, say so and suggest a dedicated, behavior-preserving refactoring pass as the next step.
