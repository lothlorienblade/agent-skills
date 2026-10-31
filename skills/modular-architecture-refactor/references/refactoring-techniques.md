# Safe refactoring techniques

Use this file in Phase 3. Each technique keeps the program working between steps.

## Contents

- [Step discipline](#step-discipline)
- [Characterization tests](#characterization-tests)
- [Creating seams](#creating-seams)
- [Moving and extracting code](#moving-and-extracting-code)
- [Expand–contract (parallel change)](#expandcontract-parallel-change)
- [Branch by abstraction](#branch-by-abstraction)
- [Breaking import cycles](#breaking-import-cycles)
- [Dependency injection without a framework](#dependency-injection-without-a-framework)
- [Simple plugin registries](#simple-plugin-registries)
- [Changing persisted or transmitted formats](#changing-persisted-or-transmitted-formats)
- [Temporary adapters](#temporary-adapters)

## Step discipline

- One step = one logically complete change that builds and passes the affected tests.
- A step is either **structural** (behavior unchanged) or **behavioral** (a defect fix with its test). Never mix them.
- Prefer automated, tool-supported refactorings (rename, move, extract) from the IDE or language server when available.
- If a step turns out larger than expected, revert to the last green state and split it.
- If the user allows commits, commit after each green step with a message describing the structural intent.

## Characterization tests

Before changing code without adequate tests, pin its current behavior:

1. Choose the observable outputs: return values, written files, emitted messages, database rows, HTTP calls.
2. Call the code with representative inputs, including edge cases and error paths.
3. Assert the **current** output, even if it looks wrong. If it is a defect, note it and fix it later in a separate, behavioral step.
4. For large or complex outputs, use golden files or snapshot tests, with stable ordering and no timestamps or random IDs.
5. Keep the tests after the refactoring if they still describe intended behavior; replace them with clearer tests if not.

## Creating seams

A seam is a place where behavior can be changed without editing the code around it. To test or decouple code that calls external systems:

- Turn hard-coded construction (`new Client()`, module-level connections) into a parameter with a default.
- Wrap static or global calls (time, randomness, environment, filesystem, network) in a small function or object that can be replaced.
- Extract pure logic out of methods that also perform I/O; test the pure part directly.

## Moving and extracting code

- Extract function → extract module → extract package, in that order of escalation.
- When moving a public symbol, leave a re-export or alias at the old location until callers are updated; remove it at the end unless it is a public API.
- Move tests together with the code they cover.
- Update build files, module manifests, and package exports in the same step as the move.

## Expand–contract (parallel change)

To change an interface used in many places:

1. **Expand**: add the new form alongside the old one (new function, new parameter with a default, new field).
2. **Migrate**: move callers to the new form in small batches, verifying after each.
3. **Contract**: remove the old form once nothing uses it, unless it is a public contract that must remain for compatibility.

## Branch by abstraction

To replace an implementation that many callers depend on:

1. Introduce a contract that captures what callers actually use.
2. Make the existing implementation satisfy it; route callers through the contract.
3. Build the new implementation behind the same contract; switch over (configuration, composition root, or registry).
4. Remove the old implementation and any switch that is no longer needed.

## Breaking import cycles

Options, from least to most invasive:

1. Move the shared type or function into a lower-level module that both sides import.
2. Merge the two modules if they really form one cohesive unit.
3. Invert one dependency: the lower module defines a contract; the higher module implements it and is wired in at the composition root.
4. Replace a direct call with an event or callback when the dependency is a notification rather than a request.

Avoid "fixing" cycles with deferred or function-local imports unless the language idiom calls for it; that hides the coupling rather than removing it.

## Dependency injection without a framework

- Pass collaborators through constructors or function parameters.
- Build the object graph in one **composition root** (the entry point, `main`, app factory, or server startup).
- Give parameters defaults only where that keeps public call sites stable; do not use defaults to hide real dependencies.
- Introduce a DI container only if the project already uses one or the graph is large enough that manual wiring is a real burden.

## Simple plugin registries

Prefer a plain registry over a dynamic loader:

```python
# Contract owned by the core
class Exporter(Protocol):
    def export(self, report: Report, path: Path) -> None: ...

# Registry built at the composition root
EXPORTERS: dict[str, Exporter] = {
    "csv": CsvExporter(),
    "json": JsonExporter(),
}

def export(report: Report, fmt: str, path: Path) -> None:
    try:
        exporter = EXPORTERS[fmt]
    except KeyError:
        raise UnsupportedFormat(fmt) from None
    exporter.export(report, path)
```

The same shape works in any language: an interface or function type, a map from key to implementation, and registration in one place. Adding a format means adding one implementation and one registry entry. Use ecosystem entry points (package entry points, service loaders, dependency-injection modules) only when third parties must add implementations without changing the application.

## Changing persisted or transmitted formats

- Add an explicit version field if none exists.
- Readers accept both old and new versions; writers switch only when all readers are ready.
- Provide a migration for stored data, never a destructive one without the user's agreement, and keep a backup path.
- Add round-trip tests (read old → write new → read again) and fixtures for every supported version.

## Temporary adapters

Adapters, shims, re-exports, and compatibility layers are acceptable during migration. Before finishing:

- remove those that only served the migration;
- keep and document those that protect a public contract;
- make sure no logic is duplicated between the adapter and the new component.
