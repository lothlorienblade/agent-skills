# Report template

Use this structure for the final report. Write it in the user's language; the headings below may be translated.

````markdown
# Codebase audit: <project or area>

## Overall state

<Two to four sentences. How ready the project is for the next stage, the one or two things that matter most, and whether the rest can wait.>

## Baseline checks

| Check | Command | Result |
| --- | --- | --- |
| Tests | `<command>` | <N passed, M failed / not run: reason> |
| Types | `<command>` | <result> |
| Lint | `<command>` | <result> |
| Build | `<command>` | <result> |

## Summary

| ID | Priority | Problem | Location | Effort |
| --- | --- | --- | --- | --- |
| P0-1 | P0 | <short title> | `path:line` | S |
| P1-1 | P1 | <short title> | `path:line` | M |

## Findings

### [P0-1] <Short title>

- **Location:** `path/to/file:123`
- **Problem:** <What exactly is wrong, in one or two sentences.>
- **Why it matters:** <A concrete consequence: who is affected, when, how badly. Link it to the next stage when relevant.>
- **Recommendation:** <The approach to fix it, not a ready patch. Mention alternatives only when they differ materially.>
- **Effort:** S / M / L · **Confidence:** confirmed / likely

<Repeat for each finding, from P0 to P3.>

## Recommended order of work

1. <Fix or group of fixes, and why it goes first.>
2. <...>

<What can deliberately wait, and until when.>

## Open questions

- <A question only the user can answer, and what depends on it.>
````

## Effort scale

- **S** — a local change in one place, under an hour or two, low risk.
- **M** — several files or a component, needs new or updated tests, up to a day or two.
- **L** — crosses module boundaries, changes contracts or data formats, or needs a migration; plan it as its own piece of work.

## Example finding

```markdown
### [P0-1] Session file is overwritten in place and can be lost on crash

- **Location:** `app/storage/session.py:48`
- **Problem:** `save_session()` opens the session file with `"w"` and writes JSON directly. If the process is killed mid-write, the file is left truncated, and `load_session()` (`app/storage/session.py:21`) treats a parse error as "no session".
- **Why it matters:** The user is silently logged out and must sign in again; on a slow disk this happened in a test with a forced kill on 3 of 10 runs. The next stage adds multi-account support, which multiplies the number of session files at risk.
- **Recommendation:** Write to a temporary file in the same directory and replace the original atomically (`os.replace`); on parse error, keep the corrupt file aside and show a clear message instead of starting a new session.
- **Effort:** S · **Confidence:** confirmed
```

What makes it a good finding: an exact location, the mechanism of failure, a realistic consequence with evidence, a link to what comes next, and a fix described as an approach.
