---
name: codex-imagegen
description: Generates raster images (game sprites, textures, icons, backgrounds, illustrations, concept art, mockups) through the OpenAI Codex CLI's built-in image generator, billed to the user's ChatGPT plan instead of a paid API key, and returns the files to the calling agent to review and post-process. Use when a task needs a new bitmap image or a variant of an existing one from references, even if the user does not mention Codex or ChatGPT, for example "generate an image", "draw a sprite", "make a texture, icon or background", "I need art for the game", "generate it with ChatGPT". Do not use for SVG or vector graphics, charts, visuals that are simpler to build in code (CSS, canvas, shaders, procedural generation), editing existing vector assets, or inside Codex itself, which has image generation built in.
license: MIT
compatibility: Requires the OpenAI Codex CLI signed in with a ChatGPT account whose plan includes image generation, and Python 3.8+.
metadata:
  author: lothlorienblade
  version: "1.0.0"
---

# Codex Image Generation

Generate raster images with the image generator built into the OpenAI Codex CLI. The images are billed to the ChatGPT plan the CLI is signed in with, so no API key is needed. [scripts/generate.py](scripts/generate.py) runs Codex non-interactively, finds the images it saved, and copies them into a folder you choose.

## Generate

```bash
python scripts/generate.py --prompt "<prompt>" --out-dir <folder> --name <file name without extension>
```

The script path is relative to this skill's folder. Use `python3` or `py` where `python` is not the interpreter. A run takes one to two minutes, so allow a command timeout of about 10 minutes.

Options:

- `--reference a.png --reference b.png`: reference images for style, palette, or shape. For a series that must look like one set, pass images from the series that are already approved: without references every call draws in its own style.
- `--model` and `--effort`: the Codex agent model, `gpt-6.1-sol` at `medium` by default, or `CODEX_IMAGEGEN_MODEL` and `CODEX_IMAGEGEN_EFFORT` when set. The agent only relays the prompt to the `image_gen` tool, which draws the same way whichever model calls it, so a frontier model at high effort only spends quota. Change these when the user asks or when the default is not available.
- `--keep-user-config`: load `~/.codex/config.toml`. It is skipped by default because the user's MCP servers and plugins slow the run and spend quota. Use it only if `image_gen` is unavailable without it.
- `--prompt-file`: read a long prompt from a UTF-8 file instead of `--prompt`.

The script prints `IMAGE: <path>` for every copied file and exits with:

| Code | Meaning | What to do |
| --- | --- | --- |
| 0 | Images copied | Review them |
| 1 | Other failure; the tail of the log and the full log path are printed | Read the error, fix the cause, do not retry blindly |
| 2 | The plan's usage limit is reached; `USAGE_LIMIT:` gives the reset time | Do not retry. Tell the user when the limit resets |
| 3 | The model is not offered to this CLI version | Suggest updating the CLI (`npm i -g @openai/codex@latest`) instead of silently switching models |

## Write the prompt

Write prompts in English, which the generator follows most precisely. State:

- what is shown and what it is for (game sprite, seamless texture, app icon, menu background);
- style, view angle, lighting, palette;
- background: `transparent background` for sprites and icons, which gives a real alpha channel;
- **the aspect ratio, chosen for where the image will be used**, such as `square 1:1` for a sprite or `landscape 16:9` for a screen background. Without it the generator draws a square, and a square cropped to a banner loses its composition.

The generator does not honor exact pixel sizes: pick the closest supported aspect ratio and get the exact size by cropping and scaling afterwards. Aspect ratios by asset type, the 3:1 limit, and prompt recipes: [references/prompting.md](references/prompting.md).

Generate one image per call and give each a descriptive `--name`, so a weak result can be redone alone.

## After generating

1. **Look at every image yourself** before showing it: does it match the prompt, is the background really transparent, are there artifacts? The generator often leaves a colored fringe along the alpha edge and stray pixels; clean them before the image goes into a game or UI.
2. **Fit it to its purpose**: trim empty margins, scale to the target size, slice into tiles. Check the seams of tiles and walls: the generator rarely makes truly seamless edges, and corners and joins are often easier to finish by hand or procedurally.
3. **Show the result to the user.**
4. **Put into the project only what the user approved or asked for**, where the project keeps its assets. Keep drafts in a temporary folder.

## Spend the quota carefully

Every image uses the ChatGPT plan's usage limit, and image generation uses it much faster than text.

- Before a batch of more than three images, tell the user how many calls you plan.
- Do not regenerate in a loop. If a result is wrong, change the prompt for a specific reason.
- On exit code 2, stop and report when the limit resets.

## Limits

- **Never use an API key for this.** The script removes `OPENAI_API_KEY` from Codex's environment and refuses to run unless Codex is signed in with ChatGPT; Codex's own API fallback (`image_gen.py`) is billed separately.
- **Do not edit `~/.codex/config.toml`**: it is the user's own Codex setup. Every setting is passed as a flag for one call.
- **Codex gets no write access to the project.** It runs in a read-only sandbox in a temporary folder; the script copies the images itself.
