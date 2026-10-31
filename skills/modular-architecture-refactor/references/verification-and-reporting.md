# Verification, handoff, and reporting

Use this file to record the Phase 0 baseline, during Phases 4–5, and when writing the final report.

## Contents

- [Recording the baseline](#recording-the-baseline)
- [Testing strategy](#testing-strategy)
- [Unverifiable scenarios](#unverifiable-scenarios)
- [Final review checklist](#final-review-checklist)
- [Working with a task tracker](#working-with-a-task-tracker)
- [Final report template](#final-report-template)

## Recording the baseline

Before any change, run every check the project defines (look in CI configuration, `package.json` scripts, `Makefile`, `justfile`, `pyproject.toml`, `build.gradle`, `*.csproj`, `Cargo.toml`, `go.mod`, and so on):

| Check | Record |
| --- | --- |
| Build / compile | success or failure, per component and target |
| Tests | passed / failed / skipped counts; names of failing tests |
| Linters | number and kind of findings |
| Type checks | number of errors |

Keep the raw output or a concise summary (in the session scratch area, not in the repository). Pre-existing failures are not yours to hide or to "fix" silently; note them and, if they block verification, report that.

If a check cannot run here (missing toolchain, private registry, unavailable service), record why.

## Testing strategy

- **Characterization tests** before changing uncovered code (see `refactoring-techniques.md`).
- **Unit tests** for extracted domain logic, now testable without external systems.
- **Contract tests** for each new or changed boundary: every implementation of a contract passes the same suite.
- **Integration tests** for the most critical end-to-end paths, especially around storage, network, and external systems, using fakes or local instances when real ones are unavailable.
- **Consistency tests** for parallel implementations: shared vectors, golden files, or differential tests.
- **Round-trip and compatibility tests** for persisted and transmitted formats.

Verify behavior, not structure. A test that only checks that a module can be imported proves little.

Build every compilable component and every target platform for which tools are available. Run the full suite at the end, not only the affected tests.

## Unverifiable scenarios

Some scenarios need a third-party application, hardware, a paid or production service, specific operating systems, or credentials that are not available. For each:

- state that it was not verified automatically and why;
- describe what was verified instead (fakes, contract tests, static checks);
- give the user a short manual check to run.

Never present an unverified scenario as working.

## Final review checklist

- [ ] Components have clear, cohesive responsibilities; dependencies are explicit and mostly one-directional; no import cycles remain in refactored areas.
- [ ] No duplicated logic, unused alternative implementations, or half-finished migrations remain.
- [ ] Temporary adapters are removed or documented as deliberate compatibility layers.
- [ ] Public APIs, CLIs, file and configuration formats, schemas, protocols, and server contracts are compatible or migrated.
- [ ] User data, settings, credentials, logs, and saved results were not touched destructively.
- [ ] Build, tests, linters, and type checks are at least as good as the baseline.
- [ ] Behavior-changing fixes are separate, tested, and listed.
- [ ] Main user scenarios were exercised where possible.
- [ ] No agent scratch files, logs, or local configuration were added to the repository.

## Working with a task tracker

When the project already uses a tracker or agent memory (for example Beads, GitHub or GitLab issues, Jira, task files described in project instructions):

1. Restore context from it and check it against the current code.
2. Create one epic for the refactoring and small, meaningful subtasks.
3. Record dependencies between subtasks, done criteria, and important technical constraints.
4. Work through subtasks in order, keeping statuses current.
5. Record significant architectural decisions, verification results, and discovered limitations.
6. Close only tasks that are finished and verified.
7. If the work cannot finish in this session, leave the code consistent and working, and record the remaining tasks and context in the tracker.

Use the tracker's own CLI or API. Do not create a parallel tracking system, and do not duplicate tracker content in separate logs. If the project has no tracker, do not introduce one without the user's agreement; use the handoff section of the report instead.

## Final report template

Keep it concise. Omit sections that do not apply.

```markdown
## Architecture refactoring report

### Resulting architecture
- <component>: <responsibility>. Depends on: <components/contracts>.
- Dependency direction: <e.g. ui, cli, adapters → services → domain; no cycles>.
- Extension points: <contract + registry/composition root>, and why.

### Key changes
- <change> — removed <problem> (evidence: <before/after>).

### Defects fixed
- <defect> — <fix> — covered by <test>.

### Verification vs. baseline
| Check | Baseline | Now |
| --- | --- | --- |
| Build | ... | ... |
| Tests | ... | ... |
| Lint | ... | ... |
| Types | ... | ... |

### Not verified
- <scenario> — why — suggested manual check.

### Limitations and deliberate non-changes
- <what was left as is and why>.

### Handoff
- Done: <tasks>.
- Remaining: <tasks, in dependency order, with done criteria>.
- Decisions and constraints: <short list>.
- Tracker: <links/IDs, or "no tracker in project">.
```
