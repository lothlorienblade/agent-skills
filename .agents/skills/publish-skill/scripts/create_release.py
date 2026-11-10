"""Publish a GitHub Release for an existing tag, without the GitHub CLI.

Reads the token that Git's credential helper stores for github.com (`git credential fill`),
never prints it, creates the release through the REST API, and verifies the result through
the public API. A new release can take a few seconds to appear there, so verification
retries for about a minute before giving up. Standard library only.

Usage:
  python create_release.py --tag v2.1.0 --title "v2.1.0 — Codex Image Generation" --notes-file notes.md
  python create_release.py --tag v2.1.0 --title "..." --notes-file notes.md --dry-run   # checks only, no token

Exit codes:
  0  release published and verified (or, with --dry-run, ready to publish)
  1  any other failure
  2  precondition failed: the tag is not on GitHub, or a release for it already exists
  3  no stored GitHub token, or GitHub rejected it
  4  the release was created, but the public API still did not show it correctly after
     retrying; do not create it again, check the printed URL and the API a little later
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

API = "https://api.github.com"
# Seconds to wait before each verification attempt; about a minute in total.
VERIFY_DELAYS = (2, 3, 5, 10, 15, 25)


def api(path: str, token: str | None = None, payload: dict | None = None) -> tuple[int, dict]:
    headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    data = None
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if payload is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(API + path, data=data, headers=headers,
                                     method="POST" if data else "GET")
    try:
        with urllib.request.urlopen(request) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", "replace")
        try:
            return error.code, json.loads(body)
        except json.JSONDecodeError:
            return error.code, {"message": body}


def stored_token() -> str:
    env = dict(os.environ, GCM_INTERACTIVE="never", GIT_TERMINAL_PROMPT="0")
    fill = subprocess.run(["git", "credential", "fill"], input="protocol=https\nhost=github.com\n\n",
                          capture_output=True, text=True, encoding="utf-8", env=env)
    for line in fill.stdout.splitlines():
        if line.startswith("password="):
            return line[len("password="):]
    return ""


def verify(repo: str, tag: str, title: str, notes: str,
           delays: tuple[float, ...] = VERIFY_DELAYS) -> tuple[list[str], dict]:
    """Check the release through the public API, retrying while it is not visible yet."""
    problems: list[str] = []
    public: dict = {}
    for delay in delays:
        time.sleep(delay)
        status, public = api(f"/repos/{repo}/releases/tags/{tag}")
        problems = []
        if status != 200:
            problems.append(f"public API returned HTTP {status}")
        else:
            if public.get("name") != title:
                problems.append("title differs")
            if public.get("body") != notes:
                problems.append("notes differ")
            if public.get("draft") or public.get("prerelease"):
                problems.append("marked draft or prerelease")
        if not problems:
            break
    return problems, public


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--repo", default="lothlorienblade/agent-skills", help="owner/name")
    parser.add_argument("--tag", required=True, help="existing tag, e.g. v2.1.0")
    parser.add_argument("--title", required=True, help='release title, e.g. "v2.1.0 — <headline>"')
    parser.add_argument("--notes-file", type=Path, required=True, help="UTF-8 Markdown release notes")
    parser.add_argument("--dry-run", action="store_true", help="check preconditions only; no token is read")
    args = parser.parse_args()
    notes = args.notes_file.read_text(encoding="utf-8")

    status, _ = api(f"/repos/{args.repo}/git/ref/tags/{args.tag}")
    if status != 200:
        print(f"PRECONDITION: tag {args.tag} is not on GitHub (HTTP {status}). Push it first.")
        return 2
    status, existing = api(f"/repos/{args.repo}/releases/tags/{args.tag}")
    if status == 200:
        print(f"PRECONDITION: a release for {args.tag} already exists: {existing.get('html_url')}")
        return 2
    if args.dry_run:
        print(f"READY: {args.repo} {args.tag} has no release yet; notes are {len(notes)} characters.")
        return 0

    token = stored_token()
    if not token:
        print("NO_TOKEN: Git has no stored credential for github.com. Push once over HTTPS to store one.")
        return 3
    status, created = api(f"/repos/{args.repo}/releases", token, {
        "tag_name": args.tag, "name": args.title, "body": notes,
        "draft": False, "prerelease": False, "make_latest": "true"})
    token = ""
    if status in (401, 403):
        print(f"NO_TOKEN: GitHub rejected the stored credential (HTTP {status}): {created.get('message')}")
        return 3
    if status != 201:
        print(f"FAILED: HTTP {status}: {created.get('message')} {created.get('errors', '')}")
        return 1

    problems, public = verify(args.repo, args.tag, args.title, notes)
    if problems:
        print(f"CREATED_UNVERIFIED ({', '.join(problems)}): {created.get('html_url')}")
        return 4
    print(f"RELEASE: {public['html_url']} | {public['name']} | author {public['author']['login']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
