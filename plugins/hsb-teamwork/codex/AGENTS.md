# hsb-teamwork — Codex entry point (AGENTS.md)

This adapter covers **two skills**: `intake-brainstorm` and `readiness-package`.
Both reuse identical method files from `../skills/` — no duplicated logic. Claude
Code and Codex read the same specs; only the harness differs.

This is the **Codex** adapter for the skills described in
`../skills/intake-brainstorm/SKILL.md` and `../skills/readiness-package/SKILL.md`. It
reuses the identical method files — `../skills/intake-brainstorm/references/`, `../skills/intake-brainstorm/assets/`, `../skills/readiness-package/references/`, and `../skills/readiness-package/assets/` — so there
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

---

## readiness-package

For readiness-package runs, follow the skill at `../skills/readiness-package/SKILL.md`
and its references under `../skills/readiness-package/references/`. Start with
`../skills/readiness-package/references/orchestration.md`. The intake-brainstorm
references (especially `initiatives.md` and `writing-integrity.md`) also apply.

### Your role: readiness-package orchestrator

You turn a Product Ready intake-record into a fully-filled Readiness Package
document, drafting all new sections and inheriting the graded sections from the
linked intake-record. You are the only layer that talks to the human.

Read these once, then follow them for the whole run:
- `../skills/readiness-package/references/orchestration.md` — phases, agent roles, phase gates.
- `../skills/readiness-package/references/escalation.md` — CTO Technical Assessment trigger rules.
- `../skills/intake-brainstorm/references/initiatives.md` — initiative resolve-or-select + phase folders.
- `../skills/intake-brainstorm/references/writing-integrity.md` — no-truncation + merge rules (critical).

### Codex execution model for readiness-package

Run the phases **sequentially** — either as Codex subagents or by performing each
role yourself as a step, in this order:

1. **Setup:** resolve-or-select the initiative; its `intake/` phase is the linked
   intake-record; pick mode (fresh / revisit / batch) and output language (default
   pt-BR); resolve-or-resume the `readiness/` phase
   (`INITIATIVE_DIR/readiness/`); validate the RP template and derive
   `contract.lock.md`.
2. **Draft pass:** Inheritor role (`hsb-readiness-inheritor`) carries graded
   sections from the intake-record forward (Origin=inherited). Drafter role
   (`hsb-readiness-drafter`) proposes first-draft content for all new RP sections
   (Origin=ai_drafted).
3. **Confirm loop:** present pre-filled RP to the PO section by section; PO judges,
   edits, or accepts; questions are a fallback only. Loop until every blocksFreeze
   section reaches its threshold or has an honest disposition.
4. **Production:** write the final RP document; Escalation Flagger role
   (`hsb-readiness-escalation-flagger`) records the tech-assessment-ref disposition
   (deferred when a CTO TA is owed, so the RP freezes provisionally rather than
   blocking indefinitely).
5. **Wrap:** write `output/manifest.md`.

### The three readiness-* subagents

| Subagent TOML | Role |
|---|---|
| `agents/hsb-readiness-inheritor.toml` | carries intake sections forward (Origin=inherited) |
| `agents/hsb-readiness-drafter.toml` | proposes new RP sections (Origin=ai_drafted) |
| `agents/hsb-readiness-escalation-flagger.toml` | decides CTO TA and records tech-assessment-ref |

Each reads its full role spec from `../agents/readiness-<role>.md` and the shared
references. Run them sequentially (Codex is single-agent).

### Modes

Same three modes as intake-brainstorm: Fresh (default), Revisit, Batch/headless.
