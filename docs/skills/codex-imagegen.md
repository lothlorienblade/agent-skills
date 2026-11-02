# Codex Image Generation

[← All skills](../../README.md) · [Skill source](../../skills/codex-imagegen/SKILL.md) · [Trigger evals](../../evals/codex-imagegen/trigger-cases.json)

Lets any coding agent **generate raster images through the OpenAI Codex CLI**: sprites, textures, icons, backgrounds, illustrations, concept art. The images come from the generator built into Codex and are billed to your ChatGPT plan, not to a paid API key. The agent gets the files back, checks them, and fits them into your project.

```bash
npx skills add lothlorienblade/agent-skills --skill codex-imagegen
```

Other installation options (Claude Code plugin marketplace, manual copy) are in the [main README](../../README.md#installation).

## Why

Most coding agents cannot draw raster images, and the usual workaround, an image API key, is billed separately from the ChatGPT subscription many people already pay for. The Codex CLI can generate images on that subscription, but an agent that just shells out to it runs into problems:

- **Wasted quota.** Codex loads your global config, starts your MCP servers, and by default may run a frontier model at high reasoning effort only to relay a prompt. The skill runs a lighter model at medium effort and skips the user config: the image comes from the same `image_gen` tool either way.
- **Lost files.** Codex saves images under `~/.codex/generated_images/<thread>/`, not in the working folder. The script finds this run's folder and copies the images where you want them.
- **Surprise bills.** An `OPENAI_API_KEY` in the environment silently switches Codex to paid API billing. The script removes it from Codex's environment and refuses to run unless Codex is signed in with ChatGPT.
- **Default composition.** Without an explicit aspect ratio the generator draws a square. The skill makes the agent choose the ratio from where the image will be used.
- **Unchecked output.** Generated assets often have a colored fringe on the alpha edge, stray pixels, and seams that do not tile. The agent reviews every image before showing it.

## What the agent does

1. **Writes the prompt** in English: asset and purpose, subject, style, view, lighting, background, and an aspect ratio chosen for the destination.
2. **Runs `scripts/generate.py`**, which calls `codex exec` in a read-only sandbox in a temporary folder and copies the generated images to the output folder.
3. **Reviews the images**, cleans edge artifacts, crops and scales to the target size, and checks the seams of tiles.
4. **Shows the result**, and puts into the project only what you approved.
5. **Guards the quota**: announces batches of more than three images, does not regenerate in a loop, and stops when the plan's usage limit is reached, telling you when it resets.

For a set of assets that must match, the agent passes approved images from the set as references to every next call.

## Requirements

- [OpenAI Codex CLI](https://github.com/openai/codex) (`npm i -g @openai/codex`), signed in with `codex login` using a ChatGPT account whose plan includes image generation. Newer agent models are offered only to newer CLI versions; keep it updated.
- Python 3.8 or newer. The script uses the standard library only.

## Usage

The skill activates automatically when a task needs a new raster image. It is designed **not** to activate for SVG or vector graphics, charts, visuals built in code (CSS, canvas, shaders), or plain processing of existing image files. Do not use it inside Codex itself, which has image generation built in; the Codex metadata turns off implicit activation there.

| Agent | Command |
| --- | --- |
| Claude Code | `/codex-imagegen [what to draw]` |
| Codex | Not needed: use Codex's built-in image generation |

Example requests:

```text
I need a sprite for the apple pickup in my snake game, transparent background.
```

```text
Generate a main menu background for the game: a misty pine forest at dusk, it should fill a 1920x1080 screen.
```

```text
Here's the approved worm sprite in assets/worm.png. Make a matching cherry and banana in the same style.
```

## Script

```bash
python scripts/generate.py --prompt "<prompt>" --out-dir art --name apple [--reference style.png] [--model M] [--effort E]
```

| Exit code | Meaning |
| --- | --- |
| 0 | Images copied; each is printed as `IMAGE: <path>` |
| 1 | Other failure; the error and the path to the full Codex log are printed |
| 2 | The ChatGPT plan's usage limit is reached; `USAGE_LIMIT:` gives the reset time |
| 3 | The model is not offered to this Codex CLI version; update the CLI or pass `--model` |

The default agent model is `gpt-6.1-sol` at `medium` effort. Override it per call with `--model` and `--effort`, or for every call with the `CODEX_IMAGEGEN_MODEL` and `CODEX_IMAGEGEN_EFFORT` environment variables.

## Files

```text
skills/codex-imagegen/
├── SKILL.md                 # Workflow, prompt rules, review, quota and safety rules
├── agents/openai.yaml       # Codex UI metadata (implicit activation off)
├── scripts/generate.py      # Runs Codex and collects the images
└── references/
    └── prompting.md           # Aspect ratios by asset type, prompt structure, recipes, matching sets
```

## Limitations

- The image model is chosen by OpenAI inside Codex's `image_gen` tool and cannot be selected here. Only the agent model that relays the prompt can.
- Exact pixel sizes in a prompt are ignored, and aspect ratios narrower than 3:1 are not supported; the agent crops and scales afterwards.
- Image generation uses the plan's usage limit much faster than text, so a long series may have to wait for the limit to reset.
