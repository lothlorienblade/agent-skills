# Diagnosing architectural problems

Use this file in Phase 1. The aim is a short, ranked list of real problems with evidence, not an exhaustive inventory.

## Contents

- [Process](#process)
- [Quick measurements](#quick-measurements)
- [Git history signals](#git-history-signals)
- [Dependency structure](#dependency-structure)
- [Smell-to-remedy table](#smell-to-remedy-table)
- [Correctness and safety scan](#correctness-and-safety-scan)
- [Ranking problems](#ranking-problems)

## Process

1. Map the top-level structure: entry points, main packages or modules, and where external systems are touched.
2. Take quick measurements (size, churn, dependencies) to find candidates.
3. Read the top candidates. Measurements point to places; only reading tells you whether there is a problem.
4. For each confirmed problem, record: location, symptom, evidence, impact, and proposed remedy.
5. Rank and pick a starting point.

Use whatever tools the project already has. Do not install new analysis tools unless they are clearly worth it, and never add them to the project's dependencies just for this task.

## Quick measurements

Adapt to the shell and the languages present. Exclude vendored, generated, and build output directories.

Largest source files (POSIX shell):

```bash
git ls-files | grep -E '\.(py|ts|tsx|js|jsx|go|rs|java|kt|cs|cpp|cc|c|h|hpp|rb|php|swift|scala)$' \
  | xargs wc -l 2>/dev/null | sort -rn | head -25
```

PowerShell equivalent:

```powershell
git ls-files | Where-Object { $_ -match '\.(py|ts|js|go|rs|java|cs|cpp|c|h)$' } |
  ForEach-Object { [pscustomobject]@{ Lines = (Get-Content $_ | Measure-Object -Line).Lines; File = $_ } } |
  Sort-Object Lines -Descending | Select-Object -First 25
```

Also look for: very long functions, classes with many public methods, files with very many imports, and modules imported from almost everywhere.

## Git history signals

Only when the project is a Git repository with meaningful history.

Change hotspots (most frequently changed files over the last year):

```bash
git log --since="12 months ago" --format= --name-only | grep -v '^$' \
  | sort | uniq -c | sort -rn | head -25
```

Change coupling (pairs of files that are often committed together):

```bash
git log --since="12 months ago" --format='--%H' --name-only \
  | awk '/^--/ {n=0; delete f; next} NF {f[++n]=$0; for (i=1;i<n;i++) print (f[i] < $0 ? f[i]" | "$0 : $0" | "f[i])}' \
  | sort | uniq -c | sort -rn | head -25
```

Interpretation:

- **Large and frequently changed** files are the strongest refactoring candidates.
- **Frequently co-changed files in different modules** indicate hidden coupling: a shared concept with no single owner, a leaky contract, or duplicated logic.
- Ignore co-change caused by mechanical edits (formatting, mass renames, dependency bumps, lockfiles).

## Dependency structure

Find import cycles and dependency direction violations. Prefer tools already configured in the project. Common options, if available:

| Ecosystem | Examples |
| --- | --- |
| JavaScript / TypeScript | `madge --circular`, `dependency-cruiser`, ESLint `import/no-cycle` |
| Python | `import-linter`, `pydeps`, `pylint` cyclic-import check |
| Java / Kotlin | `jdeps`, ArchUnit tests, Gradle/Maven module graphs |
| .NET | project reference graph, NDepend, architecture tests |
| Go | `go list -deps`, `go vet` (the compiler already forbids package cycles) |
| Rust | `cargo tree`, `cargo modules` |
| C / C++ | include graphs from the build system, `include-what-you-use` |

Without tools, grep imports and sketch the module graph by hand for the top-level packages. Check whether domain modules import UI, transport, storage, or framework code.

## Smell-to-remedy table

| Smell | Typical evidence | Usual remedy |
| --- | --- | --- |
| God module or class | Very large; many unrelated imports; many reasons to change | Split by responsibility; extract cohesive modules with narrow interfaces |
| Mixed layers | UI handlers contain SQL, HTTP calls, or business rules | Move rules into domain functions; put I/O behind small adapters |
| Import cycle | A imports B imports A (directly or via a chain) | Extract the shared concept into a lower module, or invert one dependency through a contract |
| Hidden dependency | Globals, singletons, service locators, ad hoc environment or config reads deep in the code | Pass dependencies and configuration explicitly from a composition root |
| Shared mutable state | Module-level caches, static fields, state reused across requests, sessions, or runs | Scope state to its owner (request, session, document, job) with explicit lifecycle |
| Shotgun surgery | One feature change touches many modules | Gather the scattered concept into one cohesive component |
| Divergent change | One module changes for many unrelated reasons | Split along the reasons for change |
| Switch on type in core | Long `if/switch` over formats, providers, or kinds, repeated in several places | Contract plus registry of implementations |
| Untestable logic | Tests need a database, network, UI, or hardware to exercise pure rules | Extract pure logic; isolate side effects behind seams |
| Duplicated or parallel logic | Same rule implemented in several places or languages | One source of truth, or a shared contract with conformance tests |
| Leaky data contract | Internal models serialized directly; callers depend on storage layout | Separate internal models from exchange formats; map at the boundary |
| Swallowed errors | Broad catches returning defaults or "success" | Propagate or report explicitly; distinguish partial results from success |

## Correctness and safety scan

While reading, note significant defects. Prioritize those affecting:

- validity and completeness of the program's main results;
- safety of user data;
- correctness of computations and algorithms;
- handling of external-system, I/O, and network failures (timeouts, retries, partial failures);
- security: secret handling, input validation, transport protection, injection, access control;
- consistency between UI state and processing results;
- resource leaks and concurrency bugs.

Record each defect separately. Fix it in its own step with a test, as required by the constraints in `SKILL.md`.

## Ranking problems

Rank by: **impact on change cost and correctness** × **frequency of change** ÷ **risk and effort of fixing**. Start where a fix unlocks other fixes, usually central contracts and the most entangled module. Leave cosmetic issues for last or out of scope.
