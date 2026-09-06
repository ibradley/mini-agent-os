# Working on this repo

This is a **public** repository. Two rules dominate everything else:

1. **Run `python3 scripts/check_public.py` before every commit.** It fails the build if any
   tracked file contains client names, employer names, personal-system internals, or
   credential-shaped strings. The term list lives in `.check-terms` — gitignored, because
   publishing the list would disclose exactly what it protects. New private term in your
   life → add it there; the master copy lives outside this repo.
2. **Never hand-edit `template/`.** It is generated. Change `scripts/make_workspace.py`,
   then re-emit: `python3 scripts/make_workspace.py --title "Work" --emit template`.
   This keeps the zip generator and the browsable template identical.

## Layout

- `scripts/make_workspace.py` — single source of truth for the workspace contents.
- `scripts/check_public.py` — sanitization guard. Terms come from gitignored `.check-terms`.
- `template/` — generated, browsable copy of the workspace (also usable via
  GitHub's "Use this template").
- `docs/design.html` — the annotated design document. Self-contained HTML, no external
  assets, renders in light and dark.

## Conventions

- Keep the workspace harness-agnostic: anything added must work equally under Copilot,
  Claude Code, and Codex. Adapter files stay ≤5 lines and only point at
  `context/operating.md`.
- Keep the file count small. Every file in the template must justify itself; the target
  is "understandable in one sitting."
- Examples in docs use fictional names (Acme, generic topics). No real clients, ever.

## Testing a change

```bash
python3 scripts/make_workspace.py --title "Test" --zip
unzip -o dist/workspace-*.zip -d /tmp/mos-test && ls -R /tmp/mos-test/work
python3 scripts/check_public.py
```
