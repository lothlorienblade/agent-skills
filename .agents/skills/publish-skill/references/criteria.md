# Publication criteria

A skill is published only when every item below holds. Items marked *new skill* apply to the first publication; the rest apply to every change.

## Contents

1. Skill folder
2. Frontmatter
3. Description
4. Body of SKILL.md
5. Bundled scripts
6. Generalization and honesty
7. Codex metadata
8. Trigger evals
9. Documentation page
10. Catalog entries
11. Versions and changelog
12. Verification

## 1. Skill folder

- Lives in `skills/<name>/`. `<name>` is lowercase kebab-case, at most 64 characters, and says what the skill does (`codebase-audit`, `codex-imagegen`).
- Contains only what an agent needs: `SKILL.md`, `agents/openai.yaml`, and optionally `references/`, `scripts/`, `assets/`. Everything in the folder is installed into users' projects and may be read by the agent, so there is no `README.md`, changelog, test data, or other human-only file inside.
- Maintainer-only skills (like this one) live in `.agents/skills/<name>/` instead, with `metadata.internal: true`, and get no docs page, evals, README row, or marketplace entry.

## 2. Frontmatter

```yaml
---
name: <name>                     # equal to the folder name
description: <see below>
license: MIT
compatibility: <only if the skill needs something beyond a coding agent>
metadata:
  author: lothlorienblade
  version: "1.0.0"               # quoted semver
---
```

`compatibility` names external requirements in one sentence: a CLI, an account, a runtime ("Requires the OpenAI Codex CLI signed in with a ChatGPT account ..., and Python 3.8+").

## 3. Description

The description is how agents decide to load the skill, so it carries all "when to use" information. It:

- is at most 1024 characters (checked by `check_repo.py`);
- is written in the third person, in English;
- says **what the skill does**, then **when to use it**, with the kinds of phrases users actually say, including requests that do not name the skill or its tool ("even if the user does not mention Codex");
- says **when not to use it**, naming the neighbouring skill in this collection that covers the near-miss ("modular-architecture-refactor covers that");
- mentions side effects that matter for the decision ("Changes no code.").

## 4. Body of SKILL.md

- English, imperative, addressed to the agent.
- Compact: the workflow and the rules that matter. The published skills run 90 to 180 lines. Long checklists, templates, per-language detail, and examples go to `references/` and are linked from the step that needs them, one level deep.
- Explains why a rule exists instead of shouting MUST: the agent applies the reason to cases the rule did not foresee.
- Agent-neutral: no tool names of a particular agent; describe the action ("show the image to the user", "ask the user").
- States limits and safety rules explicitly: what the skill never does (edit project files during an audit, use an API key, change a global config).
- Ends the workflow with what to report to the user, including what was not verified.
- Relative links resolve.

## 5. Bundled scripts

When a step is deterministic and repeated, ship a script rather than leaving each agent to rewrite it.

- Python 3.8+ with the standard library only (`from __future__ import annotations` for modern type hints). No PowerShell- or Bash-only scripts.
- Cross-platform. On Windows, remember: `python` may be the Microsoft Store stub (document `python`, `python3`, or `py`); `TEMP` may be an 8.3 short path that sandboxes reject (`os.path.realpath` expands it); npm CLIs are `.cmd` shims found by `shutil.which`; read and write text as UTF-8 explicitly.
- A docstring with purpose, usage, and exit codes. Distinct exit codes for the failures the agent must handle differently, and machine-readable output lines (`IMAGE: <path>`, `USAGE_LIMIT: <when>`).
- Never prints or stores secrets. Never spends the user's money or quota beyond what was asked (refuse rather than fall back to a paid path).
- Does not change the user's global configuration; passes settings per call.
- Creates output folders only when there is output.

## 6. Generalization and honesty

- No personal details from the draft: absolute paths, user and machine names, private project names, the author's own preferences presented as universal. A preference becomes a documented default with an override (flag or environment variable).
- Facts observed once are written as observations ("a request for 512×512 came back as 1254×1254"), not as guarantees.
- Nothing untested is presented as working. Claims from third-party sources are not stated as fact unless verified.

## 7. Codex metadata

`skills/<name>/agents/openai.yaml`:

```yaml
interface:
  display_name: "<Title Case Name>"
  short_description: "<one line, under ~60 characters>"
  default_prompt: "Use $<name> to <typical request>."
policy:
  allow_implicit_invocation: true
```

Set `allow_implicit_invocation: false` when implicit activation inside Codex would be wrong (for example, a skill that drives Codex itself).

## 8. Trigger evals (new skill)

`evals/<name>/trigger-cases.json`:

```json
{
  "skill": "<name>",
  "purpose": "Activation test prompts. Use them to check that the description triggers on ... and stays silent on .... Run each prompt in a fresh agent session with the skill installed and record whether the skill was loaded.",
  "should_trigger": ["..."],
  "should_not_trigger": ["..."]
}
```

- About 8 to 10 prompts in each list, phrased as real users write them, including one or two in Russian.
- `should_trigger` covers different phrasings and requests that do not name the skill.
- `should_not_trigger` holds near-misses: shared keywords with a different need, and requests that belong to the other skills in the collection. Obviously unrelated prompts test nothing.
- When a description changes, add a case for whatever prompted the change.

## 9. Documentation page (new skill)

`docs/skills/<name>.md`, in this order, as in the existing pages:

1. `# <Title>` and the navigation line: `[← All skills](../../README.md) · [Skill source](../../skills/<name>/SKILL.md) · [Trigger evals](../../evals/<name>/trigger-cases.json)`.
2. One paragraph saying what the skill does, with the key phrase in bold.
3. The install command `npx skills add lothlorienblade/agent-skills --skill <name>` and the line pointing to other installation options in the main README.
4. `## Why`: the failure modes of doing this without the skill, as bullets with a bold lead.
5. `## What the agent does`: numbered steps.
6. `## Requirements`, when the skill needs anything external.
7. `## Usage`: when it activates and when it is designed not to, the command table (Claude Code `/<name>`, Codex `$<name>`), and example requests in `text` blocks.
8. Format or script reference when the skill has one (report format, exit codes).
9. `## Files`: the tree of the skill folder with a comment per file.
10. `## Related skills`, `## Limitations`, `## Origin`, as applicable. If the skill grew from a prompt, keep the original in `docs/original-prompts/<name>.<lang>.md` and link it from Origin.

## 10. Catalog entries (new skill)

- README **Skills** table: `| [**<Title>**](docs/skills/<name>.md) | <what it does, one or two sentences> | <Changes code: Yes / No / No, adds X only> |`.
- README Claude Code marketplace block: `/plugin install <name>@lothlorienblade`.
- README intro sentence, design principles, and repository layout: update when the new skill widens the collection's scope or introduces a new kind of file.
- `.claude-plugin/marketplace.json` plugin entry with `name`, `description`, `version` (equal to `metadata.version`), `author`, `homepage` (the docs page URL on `main`), `repository`, `license`, `category`, `keywords`, `"source": "./"`, `"strict": false`, `"skills": ["./skills/<name>"]`; and the top-level `description` if the scope grew.

## 11. Versions and changelog

- `metadata.version` and the marketplace `version` are equal.
- `CHANGELOG.md`, newest first: `## vX.Y.Z — YYYY-MM-DD`, then `### <skill> <version>` with bullets saying what changed for users, then `### Repository` for repository-wide changes. Pending repository-only changes sit under `## Unreleased` and move into the next release's section.

## 12. Verification

- `agentskills validate` (skills-ref 0.1.1) passes for every folder in `skills/` and `.agents/skills/`.
- `python scripts/check_repo.py` prints `OK`.
- Bundled scripts were run on their success path and on each error path that can be triggered for free; what could not be run is reported.
- `git status` shows only intended files: no `__pycache__`, logs, or test output.
