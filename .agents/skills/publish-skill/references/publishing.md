# Publishing mechanics

How a publication is carried out on the maintainer's machine, and the pitfalls already hit. The machine is Windows with Git (and Git Credential Manager), Node.js, and Python, but **no GitHub CLI (`gh`)**. Do not plan on `gh`, and do not ask the user to install it: everything below works without it.

## Contents

1. Commit
2. Push and tag
3. Wait for CI
4. GitHub Release
5. Verify the release
6. Update the local installs
7. Environment pitfalls

## 1. Commit

All commits are authored by the repository owner. Set the identity in the clone only, never globally:

```bash
git config user.name "lothlorienblade"
git config user.email "184647080+lothlorienblade@users.noreply.github.com"
```

Message style, as in the history: an imperative title of up to about 72 characters ("Add codex-imagegen: image generation through the Codex CLI"), a blank line, a short paragraph, bullets for the parts of the change, wrapped at about 72 characters, then the attribution trailer your agent uses (for example `Co-Authored-By: ...`).

Write the message to a file and commit with `git commit -F <file>`. In Windows PowerShell 5.1, piping a here-string into `git commit -F -` fails: the message is taken as a pathspec and **no commit is created**, while the commands after it still run.

Then confirm the commit exists and is the one you expect before tagging: `git log --oneline -1` and `git status --short` (clean).

## 2. Push and tag

```bash
git push origin main
git tag -a vX.Y.Z -m "vX.Y.Z — <headline>"     # on the commit just pushed
git push origin vX.Y.Z
```

Run these as separate steps and check each result. Never chain the tag after a commit whose success you did not check: a failed commit followed by a tag puts the release tag on the previous commit.

If a tag was pushed to the wrong commit, fix it at once, before anyone installs from it, and tell the user:

```bash
git push origin :refs/tags/vX.Y.Z
git tag -d vX.Y.Z
# commit correctly, then tag and push again
```

## 3. Wait for CI

Each publication starts two runs of "Validate skills": one for the branch push and one for the tag push. Check them through the public API, without authentication:

```text
https://api.github.com/repos/lothlorienblade/agent-skills/actions/runs?head_sha=<full commit sha>
```

Wait until every run has `"status": "completed"` and `"conclusion": "success"`. Poll in a single background loop (for example `curl` every 5 seconds with a cap of a few minutes); some agent harnesses block chained `sleep` commands.

## 4. GitHub Release

Every collection tag has a GitHub Release. Its title is `vX.Y.Z — <headline>` with an em dash, and its notes follow this outline (see v2.0.0 and v2.1.0 on GitHub):

~~~markdown
<One or two sentences: what this release brings.>

### Skills

| Skill | Version | What it does |
| --- | --- | --- |
| [<Title>](https://github.com/lothlorienblade/agent-skills/blob/main/docs/skills/<name>.md) | 1.0.0 (new) | <One sentence.> |
<one row per skill in the collection; mark new or changed versions>

### Install

```bash
npx skills add lothlorienblade/agent-skills --skill <name>
```

```text
/plugin marketplace add lothlorienblade/agent-skills
/plugin install <name>@lothlorienblade
```

<Requirements line, if the new skill has any.>

### What's new

- **<Bold lead>.** <What changed, for users.>

Full changelog: [CHANGELOG.md](https://github.com/lothlorienblade/agent-skills/blob/main/CHANGELOG.md)
~~~

Use absolute links: release notes do not resolve repository-relative paths.

Create the release with the bundled script, which reads the token Git Credential Manager stores for github.com, never prints it, and verifies the result:

```bash
python scripts/create_release.py --tag vX.Y.Z --title "vX.Y.Z — <headline>" --notes-file <notes.md>
```

The script path is relative to this skill's folder.

**Permission.** Reading the stored token is a credential access. Ask the user for explicit permission in chat first; some agent harnesses (Claude Code auto mode) block the access until the user has allowed it. Never extract the token in a way that shows it in the output.

**Fallbacks**, if the user does not allow token access:

- A prefilled form the user submits: open `https://github.com/lothlorienblade/agent-skills/releases/new?tag=vX.Y.Z&title=<url-encoded>&body=<url-encoded notes>` in the user's own browser; they press **Publish release**.
- Browser automation works only where the user is already signed in to GitHub. Claude in Chrome may be disconnected, and the built-in browser of the Claude desktop app is not signed in to GitHub. Never type the user's password.

## 5. Verify the release

```text
https://api.github.com/repos/lothlorienblade/agent-skills/releases/latest
```

Check `tag_name`, `name`, `author.login` (`lothlorienblade`), `draft: false`, `prerelease: false`, and that the body is complete. Decode the response as UTF-8 bytes: on this machine the console and default text decoding are cp1251, which turns `—` into mojibake (`вЂ”`) in your check even when the release itself is correct.

## 6. Update the local installs

Published skills are installed globally with the [skills CLI](https://github.com/vercel-labs/skills), which records the source in `~/.agents/.skill-lock.json` so later `npx skills update` calls pick up new versions. Claude Code reads `~/.claude/skills/`, Codex reads `~/.agents/skills/`.

```bash
# A published skill, for Claude Code and Codex
npx -y skills add lothlorienblade/agent-skills --skill <name> -g -a claude-code codex -y

# A maintainer skill with metadata.internal: true (hidden from normal discovery)
INSTALL_INTERNAL_SKILLS=1 npx -y skills add lothlorienblade/agent-skills --skill <name> -g -a claude-code codex -y
```

In PowerShell set the variable first: `$env:INSTALL_INTERNAL_SKILLS = "1"`.

If a hand-made copy of the skill is in the way (for example the draft the skill grew from), look at it, remove it, then install. Afterwards compare the installed files with the repository by hash and tell the user where the skill is installed.

## 7. Environment pitfalls

- **Python:** `python` on this machine is the Microsoft Store stub; use `py` (or the full interpreter path). Pass `-I` when running a script that reads downloaded or cloned files.
- **Short paths:** the user name contains Cyrillic, so `TEMP` resolves to an 8.3 short path (`C:\Users\D92A~1\...`). Some tools reject it; `os.path.realpath` or `(Get-Item <path>).FullName` gives the long form.
- **PowerShell 5.1:** no `&&`; native stderr turns into error records (exit status looks failed even on success); piping text to native programs uses an ASCII encoding unless `$OutputEncoding` is set to UTF-8, and piping into `git credential fill` fails with "missing protocol field". Do credential and encoding-sensitive work in Python.
- **Validation tool:** install `skills-ref==0.1.1` into a virtual environment outside the clone; it provides `agentskills validate`.
- **Caches:** `python -m py_compile` and test runs leave `__pycache__` inside the skill; there is no `.gitignore`, so delete them before `git add -A`.
- **Line endings:** `.gitattributes` normalizes everything to LF; write files with LF where you can.
