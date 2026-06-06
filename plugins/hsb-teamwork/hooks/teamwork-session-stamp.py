#!/usr/bin/env python3
"""hsb-teamwork session-stamp hook.

Fired on `SessionStart`. Records the current `session_id` to a stable, per-root
marker so the skills can write the session binding the cost-capture hook needs.

Why this exists
---------------
The cost-capture hook (`teamwork-cost-capture.py`) attributes token usage by
reading `<TEAMWORK_ROOT>/.sessions/<session_id>.json` — a binding each skill
writes once it resolves the active initiative/phase. But the skill orchestrator
does NOT otherwise know its own `session_id`; only the hook payload carries it.
This SessionStart hook closes that gap: it stamps the id to
`<TEAMWORK_ROOT>/.sessions/.current`, which the skills read to learn the id and
then write `<TEAMWORK_ROOT>/.sessions/<session_id>.json`.

Design rules (mirror teamwork-cost-capture.py):
- Best-effort and crash-safe: every step is wrapped; the hook ALWAYS exits 0 so
  a telemetry failure can never break the user's run.
- Stateless about initiatives: at SessionStart the active initiative is not yet
  known, so this hook writes ONLY the session id, never a binding.
"""

import json
import os
import sys


def resolve_teamwork_root(cwd):
    """$TEAMWORK_HOME | <git-root>/.teamwork | <cwd>/.teamwork — same rule the
    skills and the cost-capture hook use."""
    home = os.environ.get("TEAMWORK_HOME")
    if home:
        return home
    d = os.path.abspath(cwd or os.getcwd())
    while True:
        if os.path.isdir(os.path.join(d, ".git")):
            return os.path.join(d, ".teamwork")
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return os.path.join(os.path.abspath(cwd or os.getcwd()), ".teamwork")


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    session_id = payload.get("session_id") or payload.get("sessionId")
    cwd = payload.get("cwd") or os.getcwd()
    if not session_id:
        return 0

    root = resolve_teamwork_root(cwd)
    sessions_dir = os.path.join(root, ".sessions")
    try:
        os.makedirs(sessions_dir, exist_ok=True)
        with open(os.path.join(sessions_dir, ".current"), "w", encoding="utf-8") as f:
            json.dump({"session_id": session_id, "cwd": cwd}, f, ensure_ascii=False)
    except Exception:
        # Never break the run over a telemetry stamp.
        return 0
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main() or 0)
    except Exception:
        sys.exit(0)
