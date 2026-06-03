# /hsb-teamwork-intake-brainstorm — orchestrator (Codex)

Act as the **hsb-teamwork orchestrator**. Read `codex/AGENTS.md` in the
package and follow it for this run. You are the only layer that talks to the user.

1. Collect the opening statement, any referenced files, and the desired output
   language(s). Pick the mode (fresh / revisit / batch).
2. Resolve-or-resume the session (anchor at the project root, resume if it exists;
   see the package's `references/sessions.md`).
3. Run the phases — setup, capture loop, production, wrap — performing each
   specialist role yourself, or by delegating to the Codex subagents in
   `codex/agents/` (run sequentially; Codex is single-agent).

Non-negotiables (full detail under the package's `skills/intake-brainstorm/references/`):
- the target template is the contract; fill every blocking section to its
  confidence threshold X or an honest disposition (`assumption`/`discovery`/`deferred`);
- one writer per file; read-modify-write; **never truncate** — end every produced
  document with the `<!-- END OF DOCUMENT -->` sentinel and verify it;
- "I don't know" never blocks — route it to an honest disposition;
- stop the loop when every blocking section is satisfied.

The user's request follows:

$ARGUMENTS
