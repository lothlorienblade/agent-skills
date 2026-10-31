# The OLHP principles in practice

Use this file when a design decision needs to be weighed against the four principles, or when you suspect a proposed change is over-engineered.

## Contents

- [Orthogonality](#orthogonality)
- [Low Coupling](#low-coupling)
- [High Cohesion](#high-cohesion)
- [Plugin Architecture](#plugin-architecture)
- [How the principles interact](#how-the-principles-interact)
- [The "pays its rent" test](#the-pays-its-rent-test)

## Orthogonality

**Goal.** Functional components are independent. Changing, replacing, or removing one does not require editing others unless there is a direct functional dependency between them.

**Do:**

- Isolate each component's internal state, configuration, and implementation details.
- Keep side effects local; contain error propagation at component boundaries.
- Give each piece of configuration one owner and pass it in explicitly.

**Violation signals:**

- A small change in one feature forces edits in several unrelated places ("shotgun surgery").
- Components read each other's internals, private fields, or configuration keys.
- One component's failure leaves another in a corrupted or inconsistent state.

## Low Coupling

**Goal.** Components depend on each other as little as possible, through explicit, minimal, stable interfaces.

**Do:**

- Remove import cycles, hidden dependencies (globals, singletons, service locators, implicit environment reads), and unnecessary global state.
- Apply dependency injection and dependency inversion where they actually reduce coupling, typically at I/O, integration, and framework seams.
- Keep dependencies flowing in one direction: from volatile mechanisms (UI, network, storage, integrations, frameworks) toward stable contracts and domain logic. Domain code should not import UI, transport, or storage code.
- Narrow interfaces: expose what callers need, not everything a component can do.

**Violation signals:**

- Modules import each other directly or through a chain (cycles).
- Domain logic constructs its own database clients, HTTP clients, or UI objects.
- Callers depend on concrete types, internal data layouts, or call order that is not part of a contract.

## High Cohesion

**Goal.** Every module, class, and function has one clearly stated area of responsibility, and closely related code lives together.

**Do:**

- Split components that combine several logically independent functions.
- Merge or co-locate code that always changes together and serves one purpose.
- Name each component after its responsibility; if you cannot name it without "and" or "manager/utils/helpers", it probably needs splitting or a clearer purpose.

**Do not:**

- Fragment code into many files, classes, or abstractions without practical benefit. Ten tiny files that must always be read together are less cohesive than one well-organized file.

**Violation signals:**

- "God" files or classes that mix parsing, validation, computation, I/O, and presentation.
- `utils`/`common`/`helpers` modules that grow without a theme.
- Related logic scattered across distant modules.

## Plugin Architecture

**Goal.** Functionally independent, potentially replaceable mechanisms can be added, swapped, or disabled with minimal changes to the core.

**Do:**

- Hide implementations behind a stable contract (interface, protocol, abstract base, function signature, trait).
- Prefer simple composition and registration: a dictionary or table of implementations, a list of handlers built at a composition root, an entry-point registry already supported by the ecosystem.
- Keep the contract owned by the core; implementations depend on the contract, never the reverse.

**Do not:**

- Build a general-purpose plugin framework, dynamic loader, or configuration DSL when a registry would do.
- Turn functionality into a plugin when there is no realistic second implementation, no need to disable it, and no test benefit.

**Good candidates:** export or import formats, storage backends, transport clients, payment or notification providers, rule sets, analyzers, renderers, platform-specific integrations, feature modules that are deployed selectively.

**Violation signals:**

- Adding a new format or provider requires editing a long `if/elif`/`switch` chain in core code plus several other files.
- Optional integrations are imported unconditionally and break the core when unavailable.

## How the principles interact

- Low coupling and high cohesion pull together: grouping related code reduces the dependencies that cross boundaries.
- Orthogonality is the outcome you check for; coupling and cohesion are the levers.
- Plugin architecture is a targeted application of low coupling to points of genuine variation. It is the principle most often over-applied.
- When principles conflict with simplicity, prefer the design that a new maintainer would understand fastest while still removing the observed problem.

## The "pays its rent" test

Before adding a module, interface, class, layer, or extension point, answer all three:

1. **Which observed problem does it remove?** Name the specific coupling, mixed responsibility, untestable logic, or duplication.
2. **What breaks or gets harder without it?** If nothing, do not add it.
3. **Is there a simpler form?** A function instead of a class, a module boundary instead of an interface, a registry instead of a loader.

If an abstraction fails the test, leave the code more direct. Record notable decisions not to abstract in the report so the next maintainer does not redo the analysis.
