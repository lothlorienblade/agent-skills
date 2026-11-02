"""Generate raster images through the OpenAI Codex CLI and copy them into a folder.

Codex's built-in image_gen tool draws the images and bills them to the ChatGPT plan
the CLI is signed in with. This script runs `codex exec` non-interactively in a
read-only sandbox, finds the images Codex saved under $CODEX_HOME/generated_images,
and copies them to --out-dir. Standard library only.

Usage:
  python generate.py --prompt "A glossy red apple game sprite, square 1:1, transparent background" \
      --out-dir art --name apple [--reference style.png ...]

Prints `IMAGE: <path>` for every copied file. Exit codes:
  0  images copied
  1  any other failure (the tail of the Codex log is printed)
  2  the ChatGPT plan's usage limit is reached (`USAGE_LIMIT: <when it resets>`)
  3  the model is not offered to this Codex CLI version (`MODEL_NOT_AVAILABLE: ...`)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

DEFAULT_MODEL = "gpt-6.1-sol"
DEFAULT_EFFORT = "medium"
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}

INSTRUCTION = """Call your built-in image_gen tool to create the image described below. Do not read
skills, do not run shell commands and do not write files: the tool saves the image by itself.
When done, reply with one short line.

"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--prompt", help="image prompt")
    source.add_argument("--prompt-file", type=Path, help="UTF-8 file with the image prompt")
    parser.add_argument("--out-dir", type=Path, required=True, help="folder to copy the images into")
    parser.add_argument("--name", default="image", help="file name without extension (default: image)")
    parser.add_argument("--reference", type=Path, action="append", default=[],
                        help="reference image for style or content; repeat for several")
    parser.add_argument("--model", default=os.environ.get("CODEX_IMAGEGEN_MODEL", DEFAULT_MODEL),
                        help=f"Codex agent model (default: $CODEX_IMAGEGEN_MODEL or {DEFAULT_MODEL})")
    parser.add_argument("--effort", default=os.environ.get("CODEX_IMAGEGEN_EFFORT", DEFAULT_EFFORT),
                        help=f"reasoning effort (default: $CODEX_IMAGEGEN_EFFORT or {DEFAULT_EFFORT})")
    parser.add_argument("--keep-user-config", action="store_true",
                        help="load ~/.codex/config.toml; skipped by default because its MCP servers "
                             "and plugins slow the run and spend quota")
    parser.add_argument("--timeout", type=int, default=600, help="seconds to wait for Codex (default: 600)")
    return parser.parse_args()


def fail(message: str, code: int = 1) -> int:
    print(message)
    return code


def find_session_dir(images_root: Path, log: str, started: float) -> Path | None:
    """The folder Codex saved this run's images to: by thread id, else the newest one created since start."""
    match = re.search(r'"thread_id"\s*:\s*"([0-9a-fA-F-]{36})"', log)
    if match and (images_root / match.group(1)).is_dir():
        return images_root / match.group(1)
    if not images_root.is_dir():
        return None
    fresh = [p for p in images_root.iterdir() if p.is_dir() and p.stat().st_ctime >= started - 5]
    return max(fresh, key=lambda p: p.stat().st_ctime, default=None)


def main() -> int:
    args = parse_args()
    prompt = args.prompt if args.prompt is not None else args.prompt_file.read_text(encoding="utf-8")

    codex = shutil.which("codex")
    if not codex:
        return fail("FAILED: the codex CLI is not on PATH. Install it with: npm i -g @openai/codex")

    # An API key in the environment makes Codex bill the paid API instead of the ChatGPT plan.
    env = {k: v for k, v in os.environ.items() if k not in ("OPENAI_API_KEY", "CODEX_API_KEY")}
    status = subprocess.run([codex, "login", "status"], env=env, capture_output=True,
                            text=True, encoding="utf-8", errors="replace")
    if "chatgpt" not in (status.stdout + status.stderr).lower():
        return fail("FAILED: Codex is not signed in with a ChatGPT account (run `codex login`). "
                    "Image generation through an API key is billed separately and not used here.")

    codex_home = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")
    images_root = codex_home / "generated_images"
    # realpath expands Windows 8.3 short names, which the Codex sandbox rejects.
    work_dir = Path(os.path.realpath(tempfile.mkdtemp(prefix="codex-imagegen-")))
    last_message = work_dir / "last-message.txt"

    command = [codex, "exec", "-m", args.model, "-c", f"model_reasoning_effort={args.effort}",
               "--enable", "image_generation", "--sandbox", "read-only", "--skip-git-repo-check",
               "--json", "--cd", str(work_dir), "-o", str(last_message)]
    if not args.keep_user_config:
        command.append("--ignore-user-config")
    for reference in args.reference:
        command += ["-i", str(reference.resolve())]
    command.append("-")

    started = time.time()
    try:
        run = subprocess.run(command, input=INSTRUCTION + prompt, env=env, capture_output=True,
                             text=True, encoding="utf-8", errors="replace", timeout=args.timeout)
    except subprocess.TimeoutExpired:
        return fail(f"FAILED: Codex did not finish in {args.timeout} s. Work folder: {work_dir}")
    log = run.stdout + "\n" + run.stderr
    log_path = work_dir / "codex.log"
    log_path.write_text(log, encoding="utf-8")

    session_dir = find_session_dir(images_root, run.stdout, started)
    images = []
    if session_dir:
        images = sorted((p for p in session_dir.iterdir() if p.suffix.lower() in IMAGE_SUFFIXES),
                        key=lambda p: p.stat().st_mtime)

    if images:
        args.out_dir.mkdir(parents=True, exist_ok=True)
    if last_message.is_file():
        print("codex: " + last_message.read_text(encoding="utf-8").strip())
    for index, image in enumerate(images):
        suffix = "" if index == 0 else f"-{index + 1}"
        target = args.out_dir / f"{args.name}{suffix}{image.suffix.lower()}"
        shutil.copy2(image, target)
        print(f"IMAGE: {target.resolve()}")
    if images:
        return 0

    if re.search(r"usage limit", log, re.IGNORECASE):
        reset = re.search(r"try again at ([^.\n\"]+)", log)
        return fail("USAGE_LIMIT: " + (reset.group(1).strip() if reset else "reset time unknown"), 2)
    if "model_not_found" in log or "is not supported when using Codex" in log:
        version = subprocess.run([codex, "--version"], capture_output=True, text=True).stdout.strip()
        return fail(f"MODEL_NOT_AVAILABLE: {args.model!r} is not offered to {version}. Update the CLI "
                    "(npm i -g @openai/codex@latest) or pass --model with a model it lists.", 3)
    errors = [json.loads(line).get("message", "") for line in run.stdout.splitlines()
              if line.startswith('{"type":"error"')]
    print(f"FAILED (codex exit {run.returncode}). Full log: {log_path}")
    print("\n".join(errors[-3:]) if errors else "\n".join(log.strip().splitlines()[-15:]))
    return 1


if __name__ == "__main__":
    sys.exit(main())
