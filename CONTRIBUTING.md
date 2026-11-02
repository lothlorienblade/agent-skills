# Contributing

Thanks for helping improve these skills. The most useful contributions are reports from real use: a prompt where a skill activated when it should not have (or the reverse), or a session where the agent followed the skill and still did the wrong thing.

## Changing an existing skill

- Keep `SKILL.md` compact. Put long checklists, examples, and per-language detail in `references/` and link to them from the step that needs them.
- When you change a skill's `description`, run its prompts from `evals/<name>/trigger-cases.json` in fresh agent sessions and check that it still activates on the `should_trigger` prompts and stays silent on the `should_not_trigger` ones. Add a case for whatever prompted the change.
- Bump `metadata.version` in `SKILL.md` ([semantic versioning](https://semver.org): major for changed behavior users rely on, minor for new capability, patch for fixes and wording), update the matching `version` in `.claude-plugin/marketplace.json`, and add an entry to [CHANGELOG.md](CHANGELOG.md).

## Adding a skill

1. `skills/<name>/SKILL.md` with `name` (equal to the folder name), `description` (what it does, when to use it, when not to; at most 1024 characters), `license: MIT`, and `metadata.author` and `metadata.version`.
2. `skills/<name>/agents/openai.yaml` with the Codex display name, short description, and default prompt.
3. `evals/<name>/trigger-cases.json` with prompts that should and should not activate the skill, including requests that belong to neighbouring skills in this collection.
4. `docs/skills/<name>.md`: why the skill exists, what the agent does, example requests, files, related skills.
5. A row in the **Skills** table in [README.md](README.md) and a plugin entry in `.claude-plugin/marketplace.json`.
6. If the skill grew from a prompt, keep the original in `docs/original-prompts/<name>.<lang>.md`.

Do not put a `README.md` or other human-only files inside `skills/<name>/`: everything in that folder is installed into users' projects and may be read by the agent.

## Checks

CI runs both of these on every push and pull request. Run them locally before opening a PR:

```bash
pip install skills-ref==0.1.1
for skill in skills/*/; do agentskills validate "$skill"; done
python scripts/check_repo.py
```

`agentskills validate` checks each skill against the [Agent Skills specification](https://agentskills.io/specification). `check_repo.py` checks that every skill has docs, evals, a README row, and a marketplace entry with a matching version, and that relative links resolve.
