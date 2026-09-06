#!/usr/bin/env python3
"""Generate a Mini Agent OS workspace.

  python3 scripts/make_workspace.py --title "Acme DS" --zip          -> dist/workspace-<date>.zip
  python3 scripts/make_workspace.py --title "Work" --emit template   -> writes files into ./template/

The zip unpacks as `work/` — drop it anywhere (e.g. ~/work), open it in your editor,
and any supported agent picks up its adapter file automatically.
"""
import argparse, datetime, os, zipfile

parser = argparse.ArgumentParser()
parser.add_argument("--title", default="Work", help="human name used inside the files")
parser.add_argument("--zip", action="store_true", help="write dist/workspace-<date>.zip")
parser.add_argument("--emit", metavar="DIR", help="write files into DIR instead of a zip")
args = parser.parse_args()

TODAY = datetime.date.today().isoformat()
T = args.title

OPERATING = f"""# Operating Notes — {T}

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
"""

AGENTS_MD = f"""# {T} workspace

Read `context/operating.md` first — it defines the write rules and daily routines.
Work lives in `projects/`, synthesis in `wiki/`, chronology in `journal/`.
Run the **shutdown** routine at the end of every working day.
"""

COPILOT = """Read context/operating.md before assisting. Follow its write rules.
Journal entries go to journal/YYYY-MM-DD.md; project state to projects/*/STATUS.md.
At end of day, run the shutdown routine defined in context/operating.md.
"""

WIKI_INDEX = f"""# Wiki Index

Living synthesis for {T}. Update me when pages are added.

| Page | About |
|---|---|
| overview.md | current state of play |
"""

SKILL_SESSION_LOG = """---
name: session-log
description: Summarize an agent working session into a journal-ready block
---
# Session Log

Given the conversation/work just completed, produce:

1. **What happened** — 3–6 bullets, concrete (files, decisions, results).
2. **Decisions** — each as a one-line claim with a because-clause.
3. **Next action** — exactly one, for each project touched.
4. **Open questions** — only ones a future session must answer.

Append the result to today's `journal/YYYY-MM-DD.md` under a `## Session` heading.
"""

FILES = {
    "AGENTS.md": AGENTS_MD,
    ".github/copilot-instructions.md": COPILOT,
    "context/operating.md": OPERATING,
    "context/playbooks/.keep": "",
    f"journal/{TODAY}.md": f"# {TODAY}\n\nWorkspace initialized.\n",
    "projects/.keep": "",
    "wiki/index.md": WIKI_INDEX,
    "wiki/log.md": f"# Wiki Log\n\n- {TODAY}: initialized\n",
    "wiki/overview.md": f"# Overview\n\nState of play for {T}. Keep me current.\n",
    "wiki/sources/transcripts/.keep": "",
    "wiki/sources/docs/.keep": "",
    "wiki/inbox/.keep": "",
    "skills/session-log/SKILL.md": SKILL_SESSION_LOG,
    "outbox/.keep": "",
    "state/.keep": "",
}

if args.emit:
    for path, content in FILES.items():
        full = os.path.join(args.emit, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as f:
            f.write(content)
    print(f"emitted {len(FILES)} files into {args.emit}/")
elif args.zip:
    os.makedirs("dist", exist_ok=True)
    out = f"dist/workspace-{TODAY}.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for path, content in FILES.items():
            z.writestr(f"work/{path}", content)
    print(f"wrote {out} — unzip as ~/work on the target machine")
else:
    parser.print_help()
