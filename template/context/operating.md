# Operating Notes — Work

How I keep this workspace disciplined. Load this at the start of every agent session.

## Write rules
- Titles ≤80 characters, phrased as a claim, never a transcript fragment.
- Every note names the project it belongs to, or goes to `wiki/inbox/`.
- Journal: one file per day, `journal/YYYY-MM-DD.md`. Append, never rewrite history.
- Wiki pages are synthesis: edited, linked, few. Sources are immutable: dated, many.

## Daily routines
- **warmup** — read this file, today's project STATUS.md files, anything in `wiki/inbox/`.
- **shutdown** (end of day, ~2 min) — summarize the day's sessions into `journal/<today>.md`;
  update any wiki page the day's work changed; update STATUS.md next-action lines;
  write `outbox/export-<today>.md` containing: the journal entry, changed wiki pages in
  full, artifacts produced, open questions. Then draft the team standup from the same
  material.
- **consolidate** (weekly) — merge duplicate wiki pages, refresh `wiki/index.md`,
  flag anything stale, triage `wiki/inbox/`.

## Project status format (`projects/<slug>/STATUS.md`)
State: active | cooling | parked | done
Next action: exactly one thing
Resume: two sentences that would let me pick this up cold

## What goes where

| Thing | Lives in | Why |
|---|---|---|
| Raw call/meeting transcript | `wiki/sources/transcripts/YYYY-MM-DD-<topic>.md` | immutable input, kept verbatim |
| Meeting summary | today's `journal/` entry under `## Meeting`, + a wiki page if durable | the journal is the narrative, not the archive |
| Agent session log | today's `journal/` entry under `## Session` | via the session-log skill |
| Decision | one line in today's journal under `## Decisions` | claim + because-clause |
| Idea, unfiled | `wiki/inbox/` | triaged during weekly consolidate |
| Deliverable / code | `projects/<slug>/` | work product stays with its project |
| Synthesis ("what we know") | `wiki/` pages, edited in place | few, linked, current |
| Raw audio / video | stays wherever it was recorded | never enters the workspace |

Rule of thumb: **journal = what happened (append-only, dated). wiki = what we know
(edited, linked). sources = what was said (immutable, verbatim).**
