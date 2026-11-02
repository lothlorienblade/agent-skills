---
name: publish-skill
description: Maintainer workflow for publishing an Agent Skill to the lothlorienblade/agent-skills collection on GitHub. Brings a new or changed skill up to the collection's publication criteria, wires it into the repository (docs, trigger evals, README, plugin marketplace, changelog, versions), validates it, pushes it, tags a collection release, publishes the GitHub Release, and updates the local installs. Use whenever the user wants to publish, upload, release, or add a skill to their skills repository or to agent-skills, to update a published skill there, or to check whether a skill is ready for publication, even if they only say "залей скилл в репозиторий" or "опубликуй скилл". Do not use for creating or improving a skill's own content when publication is not the goal, or for publishing to other repositories.
license: MIT
metadata:
  author: lothlorienblade
  version: "1.0.0"
  internal: true
---

# Publish a skill to lothlorienblade/agent-skills

Take a skill from "it works for me" to a published, released, and installed part of the collection at https://github.com/lothlorienblade/agent-skills. The repository is public and every skill in it is installed into other people's projects, so the bar is the collection's criteria, not the draft's.

The repository's own `CONTRIBUTING.md`, `CHANGELOG.md`, and `README.md` are authoritative. Read them at the start of every publication. If they disagree with this skill, follow the repository and update this skill in the same change.

## 1. Get a clean clone

Clone the repository into a temporary or scratch folder, never inside the user's project, and work only there:

```bash
git clone https://github.com/lothlorienblade/agent-skills.git <scratch>/agent-skills
```

If a clone exists, `git pull --ff-only` and check `git status` is clean. Read `CONTRIBUTING.md`, `CHANGELOG.md`, `README.md`, `.claude-plugin/marketplace.json`, and one published skill with its docs page and evals: the new skill must look like its neighbours.

## 2. Bring the skill to publishable form

Go through every item in [references/criteria.md](references/criteria.md). The items that most often need work on a draft:

- **Language.** Skills, docs, and evals are in English. Trigger evals also include Russian prompts.
- **Generalization.** Remove the author's personal details: paths, user names, project names, personal model or tool preferences. Turn preferences into documented defaults that a flag or environment variable overrides.
- **Portability.** Scripts are standard-library Python, cross-platform, with distinct exit codes. Not PowerShell or Bash only.
- **Agent-neutral wording.** No tool names of one agent ("call SendUserFile"); say what to do ("show the result to the user").
- **Honest claims.** Something observed once is stated as observed, not as a rule. What was not tested is not presented as working.

If the draft is installed locally under a different form (another language, another script), the repository version replaces it at step 6.

## 3. Wire it into the repository

For a new skill `<name>` (details and formats in [references/criteria.md](references/criteria.md)):

1. `skills/<name>/` with `SKILL.md`, `agents/openai.yaml`, and `references/` or `scripts/` as needed.
2. `evals/<name>/trigger-cases.json`.
3. `docs/skills/<name>.md`.
4. A row in the README **Skills** table and an install line in the plugin marketplace section; widen the README intro and `marketplace.json` top-level description if the collection's scope grew.
5. A plugin entry in `.claude-plugin/marketplace.json`.
6. A `CHANGELOG.md` entry under the new collection version, and the original prompt in `docs/original-prompts/<name>.<lang>.md` if the skill grew from one.

For a change to a published skill: bump `metadata.version`, the marketplace `version`, and add a changelog entry; if the `description` changed, add a trigger case for what prompted the change.

Choose versions with [semantic versioning](https://semver.org): a new skill starts at `1.0.0`. The collection release is minor for a new skill or capability, patch for fixes and wording, major for behaviour users rely on. Changes to repository tooling only (CI, maintainer skills like this one) go under `## Unreleased` and ship with the next release.

## 4. Validate

Run the same checks as CI, in a virtual environment outside the clone:

```bash
python -m venv <scratch>/venv
<scratch>/venv/bin/pip install skills-ref==0.1.1      # Scripts\ on Windows
for skill in skills/*/ .agents/skills/*/; do <scratch>/venv/bin/agentskills validate "$skill"; done
python scripts/check_repo.py
```

Exercise every bundled script on its success path and on each error path you can trigger without spending the user's money or quota. Delete `__pycache__` folders and other run artifacts, then check `git status` shows only intended files. Report anything you could not test.

## 5. Publish and release

Pushing to a public repository and publishing a release are outward-facing. Do it when the user asked to publish; otherwise show the summary and ask first. Follow [references/publishing.md](references/publishing.md) exactly; it records the pitfalls of this environment. In short:

1. Commit as the repository author, with the message in a file. Verify the commit exists before anything else.
2. Push `main`, then tag `vX.Y.Z` on that commit and push the tag.
3. Wait for both CI runs (branch and tag) to succeed.
4. Publish the GitHub Release `vX.Y.Z — <headline>` with notes in the established format, using [scripts/create_release.py](scripts/create_release.py). It reads the token Git stores for github.com, which needs the user's explicit permission in chat.
5. Verify the release through the public API.

## 6. Update the local installs

Reinstall the published version for Claude Code and Codex, replacing any hand-made local copy, and check that the installed files match the repository. Commands are in [references/publishing.md](references/publishing.md#update-the-local-installs).

## 7. Report

Tell the user, in their language: what was published (skill, version, collection release), links to the commit, release, and docs page, the CI result, what was installed where, anything that went wrong and how it was fixed, and what remains untested.
