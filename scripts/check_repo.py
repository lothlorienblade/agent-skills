"""Consistency checks for the skill collection.

The Agent Skills specification itself is checked by `agentskills validate`.
This script checks what ties the repository together: every skill has docs,
trigger evals, a marketplace entry and a README row, versions agree, and
relative links resolve. Standard library only.

Usage: python scripts/check_repo.py
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
MAX_DESCRIPTION = 1024

errors: list[str] = []


def error(message: str) -> None:
    errors.append(message)


def frontmatter(skill_md: Path) -> dict[str, str]:
    """Return top-level scalar fields and `metadata.version` from SKILL.md."""
    text = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        error(f"{skill_md.relative_to(ROOT)}: missing YAML frontmatter")
        return {}
    fields: dict[str, str] = {}
    in_metadata = False
    for line in match.group(1).splitlines():
        if line.startswith("metadata:"):
            in_metadata = True
            continue
        nested = re.match(r"^\s+(\w[\w-]*):\s*(.*)$", line)
        if in_metadata and nested:
            fields[f"metadata.{nested.group(1)}"] = nested.group(2).strip().strip('"')
            continue
        in_metadata = False
        top = re.match(r"^(\w[\w-]*):\s*(.*)$", line)
        if top:
            fields[top.group(1)] = top.group(2).strip().strip('"')
    return fields


def check_skill(name: str, plugins: dict[str, dict], readme: str) -> None:
    fields = frontmatter(SKILLS / name / "SKILL.md")
    if fields.get("name") != name:
        error(f"skills/{name}: frontmatter name {fields.get('name')!r} differs from directory name")
    description = fields.get("description", "")
    if not description:
        error(f"skills/{name}: empty description")
    elif len(description) > MAX_DESCRIPTION:
        error(f"skills/{name}: description is {len(description)} characters, limit is {MAX_DESCRIPTION}")
    version = fields.get("metadata.version")
    if not version:
        error(f"skills/{name}: metadata.version is missing")

    if not (ROOT / "docs" / "skills" / f"{name}.md").is_file():
        error(f"docs/skills/{name}.md is missing")
    if f"docs/skills/{name}.md" not in readme:
        error(f"README.md does not link to docs/skills/{name}.md")

    evals = ROOT / "evals" / name / "trigger-cases.json"
    if not evals.is_file():
        error(f"{evals.relative_to(ROOT)} is missing")
    else:
        cases = json.loads(evals.read_text(encoding="utf-8"))
        if cases.get("skill") != name:
            error(f"{evals.relative_to(ROOT)}: skill is {cases.get('skill')!r}, expected {name!r}")
        for key in ("should_trigger", "should_not_trigger"):
            if not cases.get(key):
                error(f"{evals.relative_to(ROOT)}: {key} is empty")

    plugin = plugins.get(name)
    if plugin is None:
        error(f".claude-plugin/marketplace.json has no plugin named {name!r}")
        return
    if plugin.get("skills") != [f"./skills/{name}"]:
        error(f"marketplace plugin {name!r}: skills should be ['./skills/{name}']")
    if version and plugin.get("version") != version:
        error(f"marketplace plugin {name!r}: version {plugin.get('version')!r} differs from SKILL.md {version!r}")


def check_links(markdown: Path) -> None:
    text = markdown.read_text(encoding="utf-8")
    for target in re.findall(r"\]\(([^)\s]+)\)", text):
        if re.match(r"^[a-z]+:", target) or target.startswith("#"):
            continue
        path = target.split("#", 1)[0]
        if path and not (markdown.parent / path).exists():
            error(f"{markdown.relative_to(ROOT)}: broken link {target}")


def main() -> int:
    marketplace = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    plugins = {plugin["name"]: plugin for plugin in marketplace["plugins"]}
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    skill_names = sorted(p.name for p in SKILLS.iterdir() if (p / "SKILL.md").is_file())
    for name in skill_names:
        check_skill(name, plugins, readme)
    for name in sorted(set(plugins) - set(skill_names)):
        error(f".claude-plugin/marketplace.json lists {name!r}, but skills/{name}/SKILL.md does not exist")

    for markdown in [ROOT / "README.md", ROOT / "CONTRIBUTING.md", *sorted((ROOT / "docs").rglob("*.md"))]:
        if markdown.is_file():
            check_links(markdown)

    for message in errors:
        print(f"error: {message}")
    print(f"Checked {len(skill_names)} skills: {'FAILED' if errors else 'OK'}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
