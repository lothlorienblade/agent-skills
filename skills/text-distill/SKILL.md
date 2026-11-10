---
name: text-distill
description: Rewrites any text into an impersonal, factual, logically structured document with no filler. Handles video and audio transcripts, monologues, lectures, essays, interviews, dialogues, Zoom or Teams meeting recordings, and chat exports, and turns them into a step-by-step guide, lecture notes, meeting minutes, or a summary of agreements. Keeps every fact, number, condition, decision, and warning; removes greetings, repetition, personal data, and speech noise, and reports what to double-check against the source. Use when the user asks to "remove the fluff", turn a transcript into instructions or notes, clean up a rambling text, anonymize it, write minutes from a call recording, or extract what was agreed in a chat, even if they just paste a long text or point to a .txt, .srt, or .md file without naming the skill. Writes a new Markdown file and never changes the source. Do not use for a one-line summary, translation, literary editing that keeps the author's voice, or transcribing audio or video itself.
license: MIT
metadata:
  author: lothlorienblade
  version: "1.0.0"
---

# Text Distill

Rewrite the source so that a reader can understand it and act on it **without opening the original**. Every fact from the source is there, nothing is invented, nothing is superfluous.

A good result is not a short retelling but a complete document of smaller size: it holds everything that changes the reader's understanding or actions, and nothing that does not.

## Principles

**1. Facts are untouchable.** Keep every number, amount, deadline, condition, exception, sequence of actions, name of a product, service, section, or button, every warning and pitfall. Add nothing of your own: knowledge you have about the topic must not appear in the document as if the source said it.

**A guess is not a fact.** If you inferred something the source does not say directly (where a countdown starts, an intention like "I'll order it today" turned into "ordered", what an estimate includes), do not state it in the document. Either leave it out or mark the spot with a short "(to verify)" and put the details in the report. The reader of the document does not see the report, so a guess written as a fact misleads them.

**2. Filler is everything that does not change understanding:**
- greetings, self-introductions, goodbyes, thanks;
- "as you can see", "so, yeah", "hope that's clear", "no big deal";
- the same point said twice, thinking aloud, digressions;
- data from a demonstration: someone's balance, the specific date on the presenter's screen, how many people are in their team. The general rule stays; the example goes;
- incidental details that affect nothing: where the keys were picked up, who passed whom a phone number, who joined the call late. The test: if the line were deleted, would anything change for the reader? If not, delete it.

**Each fact once.** Repeating a point in another section is filler too. Do not restate a fact in a summary, a table, and a recommendations list. A "Key points" block belongs only in a long document (more than two screens). A "(to verify)" mark goes in one place, where the fact is written.

**3. Depersonalization** (the default; keep names only if the user asks).
- Remove names of private individuals and personal data: phone numbers, addresses, card and wallet numbers, personal amounts.
- Replace people with roles: "curator", "new member", "project manager". If the role is unclear, use "Participant 1", "Participant 2".
- Keep names of organizations, products, services, and interface elements: they are facts.
- In minutes and chat summaries, who is responsible for what is a fact too. Replace names with roles, and give the role-to-name mapping only in the report, not in the document, so the user can restore it.

**4. Speech-recognition errors.** Automatic transcripts confuse similar-sounding words, mangle names, and lose punctuation. Whisper-style models also add phrases nobody said, especially at the end of a recording and in pauses: credits such as "Subtitles by …" or "Thanks for watching", "To be continued…", and their equivalents in the source's language.
- Fix obvious errors and list them in the report.
- Do not silently guess at doubtful ones: pick the most likely reading and list it in the report as "to verify".
- Spell the same name the same way everywhere.

**5. Contradictions and questionable advice.**
- If numbers or statements in the source contradict each other, do not silently pick one. Either keep both with a note, or drop them and say so in the report.
- If the source recommends something risky or dishonest (entering knowingly false data in an official form, bypassing a check, an unsafe action), do not turn it into the document's recommendation. Keep the neutral fact ("a tax ID is required") and raise it in the report: it is the user's call.

**6. Structure serves the reader, not the order of speech.** Speech jumps between topics; the document follows a logical order: conditions → actions → result, or context → decisions → tasks. Choose the form by genre.

## Workflow

1. **Read the whole source and look around it.** Read long texts in parts and keep a running list of facts so that nothing is lost. Check whether a file with the same name and a `.srt` or `.vtt` extension sits next to it: transcripts often come with subtitles, which give timestamps for the places to verify. If there are several files, write one document per file by default. If they form one topic, number the results in logical order and cross-reference them by number.

2. **Identify the genre and the form.** Read the matching section of [references/genres.md](references/genres.md). If the user named the form ("write minutes"), follow it.

3. **List the facts:** actions, conditions, numbers, terms, decisions, tasks, open questions, warnings.

4. **Build the structure.**
   - The title names the subject of the document, not the source: "Buying products in store X", not "Video transcript".
   - Sections follow a logical order.
   - Actions go in a numbered list, one action per item.
   - Uniform data (form fields, options, plans, deadlines, owners) goes in a table.
   - Important warnings go in a blockquote (`>`) so that they stand out.
   - **Bold** marks interface elements and key values.
   - No introductions like "This document describes…".

5. **Write.**
   - Guides: impersonal imperative ("Click", "Enter").
   - Notes and summaries: neutral statements.
   - Short sentences, the same term for the same thing throughout.
   - The source's language, unless the user asks for another.

6. **Check** before saving:
   - every listed fact is in the document;
   - every statement in the document has support in the source, and guesses are marked or removed;
   - no fact is repeated across sections;
   - the numbers match the source;
   - no personal data and no leftovers of speech remain.

7. **Save.**
   - Write a `.md` file next to the source or where the user said.
   - Name it by content: `<Topic> — <aspect>.md`, in the document's language, without characters that file names forbid.
   - Number a series: `01 …`, `02 …`.
   - Never modify or rename the source files.
   - If the text was pasted into the chat, return the result in the chat; if it is longer than a couple of screens, also save it as a file in the working folder.

8. **Report to the user, briefly.** Do not repeat the document; it is in the file.
   - which files were created and what each one covers;
   - what was removed (by category, not as a list of phrases);
   - which recognition errors were fixed;
   - **what to verify against the source**: contradictions, guesses, questionable advice. If a subtitle file or timestamps exist, give the time of each place;
   - the role-to-name mapping, if people were replaced with roles.
