#!/usr/bin/env python3
"""Public-repo guard: fail if any tracked file contains credential-shaped strings
or a term from your private banned-terms file.

The banned-terms file is deliberately NOT part of this repo (see .gitignore) —
publishing the list would disclose exactly what it exists to protect. Sources,
in order:

  1. ./.check-terms                  repo-local, one lowercase term per line, # comments
  2. $PUBLIC_CHECK_TERMS             env var pointing at a terms file elsewhere

If neither exists, only the built-in credential patterns are checked and a
warning is printed. Run before every commit:  python3 scripts/check_public.py
"""
import os, subprocess, sys

# Safe to publish: generic credential shapes, no private vocabulary.
BUILTIN = ["api_key", "secret", "token=", "bearer ", "begin private key", "password="]
ALLOW_FILES = {"LICENSE"}  # personal name on the license is intentional


def load_terms():
    paths = [".check-terms", os.environ.get("PUBLIC_CHECK_TERMS", "")]
    for p in paths:
        if p and os.path.exists(p):
            terms = [l.strip().lower() for l in open(p)
                     if l.strip() and not l.startswith("#")]
            return terms, p
    return [], None


def tracked_files():
    r = subprocess.run(["git", "ls-files"], capture_output=True, text=True)
    files = r.stdout.split()
    return files or [os.path.join(dp, f) for dp, _, fs in os.walk(".")
                     for f in fs if ".git" not in dp]


private, src = load_terms()
if not src:
    print("warning: no .check-terms file found — checking credential patterns only")
banned = BUILTIN + private

SELF = "scripts/check_public.py"  # names the builtin patterns; check it for private terms only

bad = []
for path in tracked_files():
    if os.path.basename(path) in ALLOW_FILES:
        continue
    try:
        body = open(path, encoding="utf-8", errors="ignore").read().lower()
    except (IsADirectoryError, FileNotFoundError):
        continue
    for term in (private if path == SELF else banned):
        if term in body or term in path.lower():
            bad.append((path, term))

if bad:
    print("PUBLIC CHECK FAILED:")
    for p, t in bad:
        print(f"  {p}: contains a banned term")   # never echo private terms to logs
    sys.exit(1)
print(f"public check: CLEAN ({len(tracked_files())} files, "
      f"{len(banned)} terms, list: {src or 'builtin only'})")
