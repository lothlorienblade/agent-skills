# Agent Skills by lothlorienblade

[![Validate skills](https://github.com/lothlorienblade/agent-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/lothlorienblade/agent-skills/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-6f42c1.svg)](https://agentskills.io)
[![skills.sh](https://img.shields.io/badge/skills.sh-lothlorienblade%2Fagent--skills-black.svg)](https://skills.sh/lothlorienblade/agent-skills)

[Agent Skills](https://agentskills.io) that give AI agents a disciplined method for real work: auditing a codebase before you build on it, restructuring it without breaking what it does, generating the images it needs, and distilling transcripts, recordings, and chats into documents you can act on.

Each skill is a self-contained folder that works with Claude Code, OpenAI Codex, Cursor, GitHub Copilot, Gemini CLI, OpenCode, and other agents that support the Agent Skills standard.

```bash
npx skills add lothlorienblade/agent-skills
```

## Skills

| Skill | What it does | Changes code |
| --- | --- | --- |
| [**Codebase Audit**](docs/skills/codebase-audit.md) | Read-only audit of a project. Finds the significant problems to fix before development continues, verifies each one, and ranks them P0–P3 with reasons and recommended fixes. | No |
| [**Modular Architecture Refactor**](docs/skills/modular-architecture-refactor.md) | Behavior-preserving architectural refactoring toward orthogonal, loosely coupled, highly cohesive, plugin-ready modules, in small verified steps. | Yes |
| [**Codex Image Generation**](docs/skills/codex-imagegen.md) | Generates raster images (sprites, textures, icons, backgrounds) through the OpenAI Codex CLI on a ChatGPT plan, then reviews and fits them to their purpose. | No, adds images only |
| [**Text Distill**](docs/skills/text-distill.md) | Rewrites transcripts, recordings, essays, and chat exports into factual, structured documents (guides, notes, minutes, summaries of agreements) with no filler, keeping who said what and every contact and link, and reports what to verify against the source. | No, adds documents only |

They work well together: run **Codebase Audit** to find out what matters most, then **Modular Architecture Refactor** when the main problems are architectural.

## Installation

### Any agent: skills CLI

The [skills CLI](https://github.com/vercel-labs/skills) (requires Node.js) installs skills for the agents you choose. The collection is also listed on [skills.sh](https://skills.sh/lothlorienblade/agent-skills).

```bash
# Interactive: choose skills, agents, and scope
npx skills add lothlorienblade/agent-skills

# List the skills in this repository without installing
npx skills add lothlorienblade/agent-skills --list

# One skill, Claude Code, current project
npx skills add lothlorienblade/agent-skills --skill codebase-audit -a claude-code

# One skill, Codex, available in all projects
npx skills add lothlorienblade/agent-skills --skill modular-architecture-refactor -a codex -g
```

### Claude Code: plugin marketplace

This repository is also a Claude Code plugin marketplace. Each skill is a separate plugin.

```text
/plugin marketplace add lothlorienblade/agent-skills
/plugin install codebase-audit@lothlorienblade
/plugin install modular-architecture-refactor@lothlorienblade
/plugin install codex-imagegen@lothlorienblade
/plugin install text-distill@lothlorienblade
```

Plugin skills are namespaced, so the explicit command becomes `/codebase-audit:codebase-audit`. Automatic activation works the same either way.

### Manual

Copy a folder from [`skills/`](skills) into your agent's skills directory, for example `.claude/skills/` (Claude Code) or `.agents/skills/` (Codex and other agents), in a project or in your home directory.

## Usage

Skills activate automatically when a request matches their description. To invoke one explicitly:

| Agent | Command |
| --- | --- |
| Claude Code | `/codebase-audit [optional scope]` |
| Codex | `$codebase-audit [optional scope]` |

Each skill's page describes its workflow, example requests, and what it deliberately does not do.

## Design principles

Every skill in this collection follows the same rules:

- **A method, not a prompt dump.** A compact `SKILL.md` holds the workflow and the rules that matter; detail lives in `references/` and is loaded only when a step needs it.
- **Precise activation.** Descriptions say when to use the skill and when not to, and every skill ships [trigger evals](evals) with prompts that should and should not activate it.
- **Honest verification.** Agents record a baseline, verify their claims, and report what they could not check instead of assuming it works.
- **Proportionate.** Depth matches the size and real problems of the task. No ceremony for a small tool or a short text.
- **Portable.** No runtime dependencies beyond what a skill's job requires (Codex Image Generation needs the Codex CLI and Python), no agent-specific lock-in; validated in CI against the [Agent Skills specification](https://agentskills.io/specification).

## Repository layout

```text
skills/<name>/                   # The skill itself: what gets installed
├── SKILL.md                       # Core workflow, loaded on activation
├── agents/openai.yaml             # Codex UI metadata
├── references/                    # Detail loaded on demand
└── scripts/                       # Helper scripts, where a skill needs them
docs/skills/<name>.md            # Human documentation for each skill
docs/original-prompts/           # The author's original prompts (Russian) the skills grew from
evals/<name>/trigger-cases.json  # Activation tests for each skill
.claude-plugin/marketplace.json  # Claude Code plugin marketplace
scripts/check_repo.py            # Repository consistency checks, run in CI
.agents/skills/                  # Maintainer skills for working on this repository (internal, not published)
```

## Contributing

Issues and pull requests are welcome: bug reports from real use, better trigger cases, and new ideas for skills. See [CONTRIBUTING.md](CONTRIBUTING.md) for how skills are structured and checked.

## License

[MIT](LICENSE) © lothlorienblade
