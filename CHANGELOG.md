# Changelog

Changes to each skill, newest first. Versions follow [semantic versioning](https://semver.org) per skill and match `metadata.version` in its `SKILL.md`. Repository releases (`vX.Y.Z` tags) are snapshots of the whole collection.

## v4.0.0 — 2026-11-10

### text-distill 3.0.0

- **Changed default:** phone numbers, addresses, emails, usernames, links, and account, contract, and order numbers stay in the document exactly as the source gives them. Version 2.0.0 removed contact data, account IDs, and links with tokens by default; now that happens only when the user asks for anonymization.
- Passwords, access tokens, and API keys are kept too, and the report warns about them so the user can decide before sharing the document.
- The check before saving compares contacts, addresses, and links with the source character for character.

## v3.0.0 — 2026-11-10

### text-distill 2.0.0

- **Changed default:** participants' names in dialogues, interviews, meetings, and chats are kept, so every fact, plan, and task shows whose it is. Version 1.0.0 replaced people with roles by default; that now happens only when the user asks for anonymization.
- Contact data, account IDs, and links with access tokens are still removed. A lone narrator's self-introduction in a tutorial or lecture is still dropped as filler.
- A chat export that labels its owner only as "self" uses the name from the conversation when it appears there.

### Repository

- `publish-skill` 1.0.1: `create_release.py` retries verifying a new release for about a minute, because the public API can return 404 for a few seconds after creation, and exits with the new code 4 (`CREATED_UNVERIFIED`) instead of 1 when the release was created but did not verify in time.

## v2.2.0 — 2026-11-10

### text-distill 1.0.0

- First release: rewrites transcripts, lectures, essays, interviews, meeting recordings, and chat exports into impersonal, factual, structured documents with no filler, with an output template per genre and a report of what was removed, fixed, and needs verifying against the source.

### Repository

- The collection now covers work beyond code: the README intro and the marketplace description mention distilling texts.
- Added the maintainer skill `publish-skill` in `.agents/skills/`: the collection's publication criteria and the publishing workflow (commit, tag, CI, GitHub Release, local installs), with a script that creates GitHub Releases without the GitHub CLI. It is internal (`metadata.internal: true`) and not part of the published collection.
- CI validates maintainer skills in `.agents/skills/` too; CONTRIBUTING describes publishing.

## v2.1.0 — 2026-11-02

### codex-imagegen 1.0.0

- First release: generates raster images through the OpenAI Codex CLI's built-in image generator on a ChatGPT plan, with a helper script that runs Codex in a read-only sandbox and collects the images, prompt guidance with aspect ratios by asset type, and rules for reviewing results and spending the plan's quota.

### Repository

- The README describes the `scripts/` folder a skill may include, and the portability principle allows the dependencies a skill's job requires.

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
