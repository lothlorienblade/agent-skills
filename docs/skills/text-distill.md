# Text Distill

[← All skills](../../README.md) · [Skill source](../../skills/text-distill/SKILL.md) · [Trigger evals](../../evals/text-distill/trigger-cases.json)

Rewrites any text (a video transcript, a lecture, an essay, an interview, a meeting recording, a chat export) into an **impersonal, factual, structured document with no filler**: a step-by-step guide, notes, minutes, or a summary of agreements. Every fact stays; greetings, repetition, personal data, and speech noise go.

```bash
npx skills add lothlorienblade/agent-skills --skill text-distill
```

Other installation options (Claude Code plugin marketplace, manual copy) are in the [main README](../../README.md#installation).

## Why

Asking an agent to "clean up this transcript" usually gets a short retelling: it reads well, but the numbers, conditions, and exceptions that made the original useful are gone, and some sentences are the agent's own guesses. This skill makes the agent produce a document you can act on without the original:

- **Nothing factual is lost.** Every number, deadline, condition, warning, and interface name is kept; the agent lists the facts first and checks them against the result.
- **Nothing is invented.** Inferences are not written as facts: they are left out or marked "(to verify)", and the details go into the report.
- **Filler is defined, not guessed.** Greetings, repetition, demo-only data, and incidental details are removed by a simple test: would deleting the line change anything for the reader?
- **People become roles.** Names and personal data leave the document; the role-to-name mapping goes only to you, so minutes and task lists stay usable.
- **Transcript noise is handled.** Recognition errors are fixed or flagged, and phrases speech-recognition models add on their own (subtitle credits, "Thanks for watching") are dropped.
- **You know what to double-check.** The report lists contradictions, guesses, and questionable advice from the source, with timestamps when subtitles are available.

## What the agent does

1. **Reads the whole source** and looks for a subtitle file (`.srt`, `.vtt`) with the same name next to it.
2. **Identifies the genre** and picks the form: tutorial → step-by-step guide, lecture → notes, essay → thesis outline, interview → summary by topic, meeting → minutes, chat → summary of agreements.
3. **Lists the facts**: actions, conditions, numbers, decisions, tasks, open questions, warnings.
4. **Builds the structure** in logical order, with numbered steps, tables for uniform data, and blockquotes for warnings.
5. **Writes and checks** the document: every fact present, every statement supported, nothing repeated, no personal data.
6. **Saves** a Markdown file named by its content next to the source, numbering a series of documents. The source is never changed.
7. **Reports** what was created and removed, which recognition errors were fixed, what to verify against the source, and the role-to-name mapping.

## Usage

The skill activates automatically when you ask to remove the fluff from a text, turn a transcript into a guide or notes, write minutes from a recording, or pull the agreements out of a chat. It is designed **not** to activate for one-line summaries, translation, style editing that keeps the author's voice, or transcribing audio and video.

| Agent | Command |
| --- | --- |
| Claude Code | `/text-distill [file, folder, or pasted text] [form]` |
| Codex | `$text-distill [file, folder, or pasted text] [form]` |

Example requests:

```text
Here's the transcript of a training video, transcripts/onboarding-03.txt. Strip the fluff and turn it into a proper step-by-step guide, no names, keep all the details.
```

```text
Turn the recording of yesterday's Zoom call into minutes I can send around: decisions, who does what, deadlines.
```

```text
I exported our chat with the contractor to chat.txt. Pull out what we agreed on, what it costs, and what's still open.
```

To keep people's names in the document, say so in the request.

## Files

```text
skills/text-distill/
├── SKILL.md                 # Principles, workflow, report
├── agents/openai.yaml       # Codex UI metadata
└── references/
    └── genres.md              # Output template per genre, with a before → after example
```

## Limitations

- The skill was tried on three sources before publication: a Russian tutorial-video transcript produced by Whisper, a synthetic Zoom meeting transcript, and a synthetic Telegram chat export. Other genres follow the same templates but were not tested separately.
- Recognition errors in names the agent cannot know (a company or product name it has never seen) are flagged for you to verify, not corrected.
- Very long sources are read in parts; the fact list keeps the result complete, but a source of several hundred pages may be better split first.

## Origin

The skill grew from rewriting a series of tutorial-video transcripts into impersonal guides. The author's original requests are preserved in [`docs/original-prompts/text-distill.ru.md`](../original-prompts/text-distill.ru.md).
