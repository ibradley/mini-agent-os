# Mini Agent OS

A tiny, self-contained operating system for agent-assisted work. One workspace format that
any coding agent can drive — GitHub Copilot, Claude Code, Codex, or whatever ships next.

You get a disciplined daily loop (capture → journal → synthesize → export) in 15 small files,
with nothing to install, no daemons, no cloud dependencies, and no agent lock-in.

## Why

- **Harness-agnostic.** The agent adapters are 4-line pointer files. Swap Copilot for
  Claude for Codex and nothing else changes.
- **Self-contained.** The workspace works alone, offline, forever. Everything is plain
  markdown you can read without any tooling.
- **Confidential by default.** Built for client and employer machines: no external calls,
  no credentials, no references to anything outside the folder. You decide what leaves,
  and you carry it out by hand.
- **Cheap discipline.** The end-of-day routine produces the standup you already owe your
  team as a by-product. The system pays for itself daily.

## Three folders, three verbs

| Folder | Verb | Nature |
|---|---|---|
| `journal/` | **what happened** | append-only, one file per day |
| `wiki/` | **what we know** | edited in place, few pages, linked |
| `wiki/sources/` | **what was said** | immutable, verbatim, dated |

A transcript lands verbatim in `sources/`, its digest becomes a `## Meeting` block in
today's journal, and if it changed what you know, a wiki page gets updated. Three layers,
one motion.

## Quick start

**Option A — use the template directly**

```bash
cp -r template ~/work && cd ~/work
code .        # or your editor of choice
```

**Option B — generate a customized zip to carry to another machine**

```bash
python3 scripts/make_workspace.py --title "Acme DS" --zip
# -> dist/workspace-<date>.zip ; unzip as ~/work on the target machine
```

Then open the folder with your agent and say **"run warmup"**. Copilot picks up
`.github/copilot-instructions.md`; Claude Code and Codex read `AGENTS.md`. Both point at
`context/operating.md`, which is the whole constitution.

## The tree

```
work/
├── AGENTS.md                     ← adapter: Claude Code / Codex / VS Code agent mode
├── .github/
│   └── copilot-instructions.md   ← adapter: GitHub Copilot
├── context/
│   ├── operating.md              write rules · routines · what-goes-where
│   └── playbooks/                your SOPs
├── journal/
│   └── YYYY-MM-DD.md             ## Session · ## Meeting · ## Decisions
├── projects/<slug>/
│   └── STATUS.md                 state · ONE next action · resume note
├── wiki/
│   ├── index.md · log.md · overview.md
│   ├── sources/
│   │   ├── transcripts/          raw transcripts, verbatim
│   │   └── docs/                 dropped files worth keeping
│   └── inbox/                    unfiled ideas
├── skills/
│   └── session-log/SKILL.md      portable capability, works under any agent
├── outbox/                       export bundles staged for carry-out
└── state/                        scratch, markers
```

## The three routines

No cron, no background jobs — you trigger, the agent executes.

| Routine | When | What |
|---|---|---|
| **warmup** | day start, ~30s | load `operating.md` + today's `STATUS.md` files + `wiki/inbox/` |
| **shutdown** | day end, ~2min | sessions → journal entry → wiki updates → `STATUS.md` next-actions → `outbox/export-<date>.md` → **drafts your standup from the same material** |
| **consolidate** | weekly | wiki lint: merge duplicates, refresh index, triage inbox, flag stale pages |

## What goes where

| Thing | Lives in |
|---|---|
| Raw transcript | `wiki/sources/transcripts/YYYY-MM-DD-<topic>.md` |
| Meeting summary | journal `## Meeting` (+ wiki page if durable) |
| Session log | journal `## Session` (via the session-log skill) |
| Decision | journal `## Decisions` — one line, claim + because |
| Unfiled idea | `wiki/inbox/` |
| Deliverable / code | `projects/<slug>/` |
| Synthesis | `wiki/` pages, edited in place |
| Raw audio/video | **stays wherever it was recorded — never enters the workspace** |

## Write rules (the short version)

1. Titles ≤80 characters, phrased as a claim — never a transcript fragment.
2. Every note names its project, or goes to `wiki/inbox/`.
3. Journal is append-only. History doesn't get rewritten.
4. `STATUS.md` carries exactly **one** next action. Not nine.

## Skills

`skills/<name>/SKILL.md` is a portable capability: frontmatter + instructions any agent can
follow. One ships with the template (`session-log`). Add your own; keep them generic to the
workspace — a skill should make sense on any machine you'd unzip this onto.

## Optional: feeding a personal hub

If you run a personal knowledge system elsewhere, the `outbox/` bundle is your one-way
export: the day's journal entry, changed wiki pages in full, artifacts produced, open
questions. Carry it by hand (browser upload, USB, whatever suits the machine's rules) and
ingest it on your side. This workspace never phones home — **you are the transport.** That's
a feature: there is nothing running, nothing to configure, and nothing to leak.

## Design doc

The full annotated design — tree walkthrough, a transcript's journey through the system,
and the confidentiality rules — is in [`docs/design.html`](docs/design.html). Open it
locally in a browser, or enable GitHub Pages on this repo to serve it.

## Repo layout

```
template/     the workspace, ready to copy       (generated — do not hand-edit)
scripts/      make_workspace.py (generator) · check_public.py (sanitization guard)
docs/         design.html
```

`template/` is emitted by the generator: edit `scripts/make_workspace.py`, then
`python3 scripts/make_workspace.py --title "Work" --emit template`.

## License

MIT — see [LICENSE](LICENSE).
