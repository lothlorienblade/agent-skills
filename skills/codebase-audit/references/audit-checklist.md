# Audit checklist

Questions to ask in each dimension, and tools that help answer them. Use what fits the project; skip what does not apply. Prefer the tools the project already has over new ones, and never install anything into the project.

## Contents

- [Where to look first](#where-to-look-first)
- [Correctness](#correctness)
- [Reliability](#reliability)
- [Security and privacy](#security-and-privacy)
- [Architecture](#architecture)
- [Tests](#tests)
- [Build and dependencies](#build-and-dependencies)
- [Diagnosability and error UX](#diagnosability-and-error-ux)
- [Performance](#performance)
- [Maintainability](#maintainability)
- [Tooling by ecosystem](#tooling-by-ecosystem)

## Where to look first

Problems cluster. Start where they are most likely and most expensive:

- **Change hotspots** — files that change most often are where bugs and coupling accumulate:
  `git log --since=1.year --name-only --format= | sort | uniq -c | sort -rn | head -20`
- **Recent and unfinished work** — `git log -20 --stat`, `git status`, `git diff`. Half-done changes often break invariants.
- **External boundaries** — network calls, file and database I/O, subprocesses, third-party SDKs, user input, IPC.
- **Long or central units** — the largest files and functions, and the modules most others import.
- **Known debt markers** — `TODO`, `FIXME`, `HACK`, `XXX`, disabled tests, broad `except`/`catch`, `# type: ignore`, `eslint-disable`, `@SuppressWarnings`.

## Correctness

- Does each function handle empty, missing, zero, negative, very large, and malformed inputs?
- Are errors handled or propagated, or silently converted into wrong results?
- Is shared state accessed from several threads, tasks, or callbacks without synchronization?
- Are files, sockets, handles, and locks always released, including on error paths?
- Can an operation be interrupted halfway and leave inconsistent state?
- Do time zones, locales, encodings, and path separators behave correctly on every target platform?
- Do the types and contracts at module boundaries match what callers actually pass?

## Reliability

- Do network calls have timeouts? Are retries bounded, with backoff, and only for idempotent operations?
- Can the user cancel long operations, and does cancellation clean up?
- What happens on partial failure: half-written files, half-applied migrations, interrupted downloads?
- Are user data and settings written atomically (temporary file and rename), with backups where loss would hurt?
- Does the program survive a restart in the middle of work, and resume or fail clearly?
- Are rate limits, quotas, and flood-control responses from external services handled?

## Security and privacy

- Are secrets (API keys, tokens, passwords, session files) in the code, config, logs, or Git history?
  Look at `.env*`, config files, test fixtures, and `git log -p -S'<suspicious string>'` for history.
- Is untrusted input used in shell commands, SQL, file paths, templates, `eval`, or deserialization (`pickle`, `yaml.load`, `BinaryFormatter`)?
- Are credentials and sessions stored with appropriate protection (OS keychain, file permissions), not in plain text next to user documents?
- Is personal data logged, sent to third parties, or kept longer than needed?
- Are TLS verification and certificate checks left enabled?
- Do dependencies have known vulnerabilities (see [Tooling by ecosystem](#tooling-by-ecosystem))?

## Architecture

- Can a component be changed or replaced without editing unrelated ones?
- Do dependencies flow in one direction, from UI and I/O toward domain logic? Are there import cycles?
- Are there god objects or god modules that everything depends on?
- Is UI code mixed with business rules, persistence, or network calls, so that logic cannot be tested without the UI?
- Is there global mutable state, singletons with hidden state, or implicit initialization order?
- Are there two or more implementations of the same rule, format, or protocol that can drift apart?
- Does the structure contradict the principles stated in `AGENTS.md`, `CLAUDE.md`, or ADRs?
- Will the next planned feature require editing many unrelated places? That is the clearest sign an architectural finding matters now.

## Tests

- Are the critical paths (the core user scenario, data handling, external integrations) covered at all?
- Do tests assert outcomes, or only that code runs without exceptions?
- Do tests depend on network, real accounts, the current date, ordering, or the local machine?
- Are there skipped, disabled, or permanently failing tests?
- Is there a fast way to run the suite, and does CI run it?

## Build and dependencies

- Can a clean checkout be built and run by following the README?
- Are dependency versions pinned or locked? Is the lock file committed?
- Are there unused, duplicated, abandoned, or vulnerable dependencies?
- Do builds differ between platforms in ways that are not tested (paths, case sensitivity, line endings, native libraries)?
- Is packaging and distribution reproducible, and are build artifacts kept out of version control?

## Diagnosability and error UX

- Are exceptions swallowed (`except: pass`, empty `catch`) or logged without context?
- When something fails, does the user get a message that says what happened and what to do?
- Are there logs where failures need to be investigated, and do they avoid secrets and personal data?
- Can a user-reported problem be reproduced from the information the program records?

## Performance

Report only what is noticeable or will become noticeable at realistic scale:

- long work on the UI thread or event loop;
- quadratic or worse work on inputs that can be large;
- repeated I/O or network calls that could be batched or cached;
- unbounded memory growth: caches without limits, whole files loaded into memory.

## Maintainability

- Is there dead code: unused modules, functions, flags, or feature toggles?
- Do TODO/FIXME comments describe real outstanding problems? Group them rather than listing each.
- Does the documentation (README, docstrings, comments) contradict the code?
- Is naming consistent enough that the same concept is not called three different things?

## Tooling by ecosystem

Run these only if they are already configured in the project or can run without modifying it. Report what was run.

| Ecosystem | Tests and types | Lint and static analysis | Dependencies and security |
| --- | --- | --- | --- |
| Python | `pytest`, `mypy`, `pyright` | `ruff`, `pylint`, `bandit` | `pip-audit`, `pip list --outdated` |
| JavaScript / TypeScript | `npm test`, `tsc --noEmit` | `eslint` | `npm audit`, `npm outdated` |
| Java / Kotlin | `./gradlew test`, `mvn test` | SpotBugs, detekt, ktlint | OWASP Dependency-Check |
| .NET | `dotnet test`, `dotnet build -warnaserror` | Roslyn analyzers | `dotnet list package --vulnerable --outdated` |
| Go | `go test ./...`, `go vet ./...` | `staticcheck`, `golangci-lint` | `govulncheck ./...` |
| Rust | `cargo test`, `cargo check` | `cargo clippy` | `cargo audit`, `cargo outdated` |
| C / C++ | the project's CTest or test target | `clang-tidy`, `cppcheck`, compiler warnings | — |

Generic: `gitleaks` or `trufflehog` for secrets in history; `madge` (JS/TS), `pydeps` or `import-linter` (Python), `jdeps` (Java) for dependency cycles.
