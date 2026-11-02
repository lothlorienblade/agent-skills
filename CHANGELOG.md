# Changelog

Changes to each skill, newest first. Versions follow [semantic versioning](https://semver.org) per skill and match `metadata.version` in its `SKILL.md`. Repository releases (`vX.Y.Z` tags) are snapshots of the whole collection.

## v2.0.0 — 2026-11-02

### Repository

- The repository became a collection of skills: `lothlorienblade/modular-architecture-refactor` was renamed to `lothlorienblade/agent-skills`. Old links redirect.
- Added a Claude Code plugin marketplace (`.claude-plugin/marketplace.json`), with one plugin per skill.
- Per-skill documentation moved to `docs/skills/`, trigger evals to `evals/<skill>/`, and original prompts to `docs/original-prompts/`.
- CI validates every skill and checks repository consistency with `scripts/check_repo.py`.

### codebase-audit 1.0.0

- First release: read-only codebase audit with verified findings ranked P0–P3, an audit checklist by dimension and ecosystem, and a report template.

### modular-architecture-refactor 1.0.0

- Added a trigger eval case that keeps general codebase audits out of this skill. The skill itself is unchanged.

## v1.0.0 — 2026-10-31

### modular-architecture-refactor 1.0.0

- First release, published as `lothlorienblade/modular-architecture-refactor`.
