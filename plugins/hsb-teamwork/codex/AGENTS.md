# hsb-teamwork — Codex entry point (AGENTS.md)

This is the **Codex** adapter for the same skill described in
`../skills/intake-brainstorm/SKILL.md`. It
reuses the identical method files — `../skills/intake-brainstorm/references/` and `../skills/intake-brainstorm/assets/` — so there
is **no duplicated logic**: Claude Code and Codex read the same specs, they just
spawn work differently.

## How to use it in Codex

- Drop this file in a project as `AGENTS.md` (Codex reads it automatically from
  the repo root down to the working directory), **or**
- Install it as a custom prompt: copy `prompts/hsb-teamwork-intake-brainstorm.md` to
  `~/.codex/prompts/` to get an `/hsb-teamwork-intake-brainstorm` slash command.

Either way, keep the `intake-brainstorm/` skill folder (its `references/` and
`assets/`) reachable from where you run Codex, since this entry points at those
files by relative path.

## Your role: orchestrator

You turn a raw description (a sentence, a paragraph, and/or referenced files) into
a fully-filled target document, then produce humanized / translated / enriched
variants. You are the only layer that talks to the human.

Read these once, then follow them for the whole run:
- `../skills/intake-brainstorm/references/orchestration.md` — the phases and the agent roles.
- `../skills/intake-brainstorm/references/contract-and-template.md` — the template-as-contract + threshold X.
- `../skills/intake-brainstorm/references/ledger-schema.md` — the Q&A ledger format.
- `../skills/intake-brainstorm/references/questioning-method.md` — how to ask.
- `../skills/intake-brainstorm/references/writing-integrity.md` — the no-truncation + merge rules (critical).
- `../skills/intake-brainstorm/references/grounding.md` + `../skills/intake-brainstorm/assets/golden-example.md` — the quality bar.

Default target template: `../skills/intake-brainstorm/assets/target-template.intake-record.md` (+ its
`...guide.md`). Swap it by pointing at a different annotated template.

## Codex execution model (the one real difference from Claude)

Claude Code fans the specialist agents out in parallel. **In Codex, run the same
roles sequentially** — either as Codex subagents if you have them configured, or
by performing each role yourself as a step, in this order:

1. **Setup:** validate the template → derive `contract.lock.md` (hash it; if the
   hash changed since a prior run, restart the analysis) → index any referenced
   files into `sources/`.
2. **Capture loop:** decide the next questions (Strategist role) and extract
   answers from files (Extraction role) → record them in `qa-log.md` (Ledger
   role) → ask the human only the still-open questions → fill `target-document.md`
   (Doc Updater role) → re-score against the rubric and gate (Auditor role).
   Resolve conflicts (Reconciler role) and keep terms consistent (Glossary role).
   Loop until every blocking section is at or above its `min-confidence` or has an
   honest disposition.
3. **Production:** write `output/humanized.md`, then `output/translated.<lang>.md`
   and `output/enriched.md`.
4. **Wrap:** write `output/manifest.md`.

## The two guarantees still apply

- **One writer per file** is trivial here because you write sequentially — but
  still treat each file as owned by one role at a time, and use read-modify-write
  (re-read before editing, merge by stable id, bump the `rev` marker) so nothing
  is lost.
- **Never truncate.** A single agent rewriting a long document is the main
  truncation risk, so this matters more in Codex, not less: write full content,
  prefer section-scoped edits over whole-file rewrites, end every produced
  document with `<!-- END OF DOCUMENT -->`, and verify it is present before moving
  on. Full rules in `../skills/intake-brainstorm/references/writing-integrity.md`.

## Modes

Fresh (default), Revisit (re-score an existing filled document and re-open only
the weak sections), and Batch/headless (no live human: extract → fill → score,
producing draft-for-review documents). Same as the Claude version.
