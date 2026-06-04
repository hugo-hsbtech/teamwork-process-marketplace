# hsb-teamwork — Codex entry point (AGENTS.md)

This adapter covers **two skills**: `origination-brainstorm` and `readiness-package`.
Both reuse identical method files from `../skills/` — no duplicated logic. Claude
Code and Codex read the same specs; only the harness differs.

This is the **Codex** adapter for the skills described in
`../skills/origination-brainstorm/SKILL.md` and `../skills/readiness-package/SKILL.md`. It
reuses the identical method files — `../skills/origination-brainstorm/references/`, `../skills/origination-brainstorm/assets/`, `../skills/readiness-package/references/`, and `../skills/readiness-package/assets/` — so there
is **no duplicated logic**: Claude Code and Codex read the same specs, they just
spawn work differently.

## How to use it in Codex

- Drop this file in a project as `AGENTS.md` (Codex reads it automatically from
  the repo root down to the working directory), **or**
- Install it as a custom prompt: copy `prompts/hsb-teamwork-origination-brainstorm.md` to
  `~/.codex/prompts/` to get an `/hsb-teamwork-origination-brainstorm` slash command.

Either way, keep the `origination-brainstorm/` skill folder (its `references/` and
`assets/`) reachable from where you run Codex, since this entry points at those
files by relative path.

## Your role: orchestrator

You turn a raw description (a sentence, a paragraph, and/or referenced files) into
a fully-filled target document, then produce humanized / translated / enriched
variants. You are the only layer that talks to the human.

Read these once, then follow them for the whole run:
- `../skills/origination-brainstorm/references/orchestration.md` — the phases and the agent roles.
- `../skills/origination-brainstorm/references/contract-and-template.md` — the template-as-contract + threshold X.
- `../skills/origination-brainstorm/references/ledger-schema.md` — the Q&A ledger format.
- `../skills/origination-brainstorm/references/questioning-method.md` — how to ask.
- `../skills/origination-brainstorm/references/writing-integrity.md` — the no-truncation + merge rules (critical).
- `../skills/origination-brainstorm/references/grounding.md` + `../skills/origination-brainstorm/assets/golden-example.md` — the quality bar.

Default target template: `../skills/origination-brainstorm/assets/target-template.origination-record.md` (+ its
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
   Resolve conflicts (Reconciler role) and keep terms consistent (Glossary role) by
   writing the initiative's shared `glossary.md` + `decisions.md`. Loop until every
   blocking section is at or above its `min-confidence` or has an honest disposition.
3. **Production:** write `output/humanized.md`, then `output/translated.<lang>.md`
   and `output/enriched.md`.
4. **Wrap:** write `output/manifest.md`, then update the front's entry in
   `initiative.json` (the works + definitions index): `state: frozen`, final
   `readiness`, `artifacts`, `produces`, and any `owes`.

### The initiative-level index and shared definitions (you maintain these)

Beyond the phase folder, every initiative has three **initiative-level** files you
own: `initiative.json` (the works + definitions index — what each front produced,
how ready, what it owes), and the shared `glossary.md` + `decisions.md`. They live
at the initiative root, above any phase. In Codex you are the broker yourself: read
the index when a front starts to see prior works/definitions; keep the shared
glossary/decisions canonical (one place, no per-phase copies); and update the index
on freeze. Full spec: `../skills/origination-brainstorm/references/initiatives.md`
(§§ *index of definitions and works*, *Shared definitions*, *Brokering*).

## The two guarantees still apply

- **One writer per file** is trivial here because you write sequentially — but
  still treat each file as owned by one role at a time, and use read-modify-write
  (re-read before editing, merge by stable id, bump the `rev` marker) so nothing
  is lost.
- **Never truncate.** A single agent rewriting a long document is the main
  truncation risk, so this matters more in Codex, not less: write full content,
  prefer section-scoped edits over whole-file rewrites, end every produced
  document with `<!-- END OF DOCUMENT -->`, and verify it is present before moving
  on. Full rules in `../skills/origination-brainstorm/references/writing-integrity.md`.

## Modes

Fresh (default), Revisit (re-score an existing filled document and re-open only
the weak sections), and Batch/headless (no live human: extract → fill → score,
producing draft-for-review documents). Same as the Claude version.

---

## readiness-package

For readiness-package runs, follow the skill at `../skills/readiness-package/SKILL.md`
and its references under `../skills/readiness-package/references/`. Start with
`../skills/readiness-package/references/orchestration.md`. The origination-brainstorm
references (especially `initiatives.md` and `writing-integrity.md`) also apply.

### Your role: readiness-package orchestrator

You turn a Product Ready origination-record into a fully-filled Readiness Package
document, drafting all new sections and inheriting the graded sections from the
linked origination-record. You are the only layer that talks to the human.

Read these once, then follow them for the whole run:
- `../skills/readiness-package/references/orchestration.md` — phases, agent roles, phase gates.
- `../skills/readiness-package/references/escalation.md` — CTO Technical Assessment trigger rules.
- `../skills/origination-brainstorm/references/initiatives.md` — initiative resolve-or-select + phase folders.
- `../skills/origination-brainstorm/references/writing-integrity.md` — no-truncation + merge rules (critical).

### Codex execution model for readiness-package

Run the phases **sequentially** — either as Codex subagents or by performing each
role yourself as a step, in this order:

1. **Setup:** resolve-or-select the initiative; **read `initiative.json`** and find
   the linked origination-record from the works index (the phase that `produces` an
   `origination-record`, via its `artifacts.canonical`); pick mode (fresh / revisit
   / batch) and output language (default pt-BR); resolve-or-resume the `readiness/`
   phase (`INITIATIVE_DIR/readiness/`) and register it in the index; validate the RP
   template and derive `contract.lock.md`.
2. **Draft pass:** Inheritor role (`hsb-stage-inheritor`) carries graded
   sections from the origination-record forward (Origin=inherited). Drafter role
   (`hsb-section-drafter`) proposes first-draft content for all new RP sections
   (Origin=ai_drafted).
3. **Confirm loop:** present pre-filled RP to the PO section by section; PO judges,
   edits, or accepts; questions are a fallback only. Loop until every blocksFreeze
   section reaches its threshold or has an honest disposition.
4. **Production:** write the final RP document; Escalation Flagger role
   (`hsb-escalation-flagger`) records the tech-assessment-ref disposition
   (deferred when a CTO TA is owed, so the RP freezes provisionally rather than
   blocking indefinitely).
5. **Wrap:** write `output/manifest.md`, then update the `readiness/` entry in
   `initiative.json` — `state: frozen` (or provisional), final `readiness`,
   `artifacts`, `produces: readiness-package`, and push the owed Technical Assessment
   into `owes` so the next front reads it.

### The three stage-agnostic subagents this skill drives

| Subagent TOML | Role here |
|---|---|
| `agents/hsb-stage-inheritor.toml` | carries the upstream origination-record forward (Origin=inherited) |
| `agents/hsb-section-drafter.toml` | proposes the RP's new sections (Origin=ai_drafted) |
| `agents/hsb-escalation-flagger.toml` | decides CTO TA and records tech-assessment-ref |

Each reads its full role spec from `../agents/<role>.md` (e.g.
`../agents/hsb-stage-inheritor.md`) and the shared references. Run them sequentially
(Codex is single-agent).

### Modes

Same three modes as origination-brainstorm: Fresh (default), Revisit, Batch/headless.
