# Orchestration — phases, agents, and the single-writer guarantee

This skill is a **multi-agent pipeline**. The conversation you (the orchestrator)
run is **Layer 0** — the only layer that talks to the human. Everything else is a
**specialized subagent** you spawn with a focused prompt and tear down. This file
is the authoritative spec for *who runs when, who may write what, and what runs
in parallel*.

## The one rule that makes parallelism safe

**Every mutable file has exactly one writer agent.** Every other agent is
**read-only** and returns *proposals / findings / verdicts* to you (the
orchestrator), and **you** route them to the single writer. Two agents never hold
the pen on the same file, so concurrent writes are impossible by construction.

| Artifact | Sole writer | Everyone else |
|---|---|---|
| `contract.lock.md` | Template Analyst | read-only |
| `sources/`, `sources-index.md` | Source Indexer | read-only |
| `qa-log.md` | Ledger Writer | read-only |
| `target-document.md` | Doc Updater | read-only |
| `glossary.md` | Glossary Keeper | read-only |
| `readiness-report.md` | Readiness Reporter | read-only |
| `output/humanized.md` | Humanizer | read-only |
| `output/translated.<lang>.md` | Translator | read-only |
| `output/enriched.md` | Visual Enricher | read-only |
| `output/manifest.md` | Packager | read-only |

**Serialize, queue, and merge — never clobber.** Beyond one-writer-per-file: you
never spawn two writers on the *same* file at once, you **queue** pending changes
and drain them through that single writer in one commit pass (nothing is dropped),
and every writer does **read-modify-write** (re-read the file, merge the batch
keyed by stable id, bump the `rev` marker) so no change is lost and overlapping
edits surface as conflicts for the Reconciler rather than silent overwrites. The
full protocol — queue, RMW, merge, conflict handling, the `rev` marker, and the
no-truncation rules — is in
[`writing-integrity.md`](writing-integrity.md); every writer agent reads it.

## Paths are passed in, never hardcoded (portability)

The skill ships in the **`hsb-teamwork` plugin** and is repo-independent. Its
base directory varies by install (the plugin cache, or `.claude/skills/...` when
symlinked in-repo), so you inject paths into every agent's spawn prompt — never let
an agent assume a location:

- `SKILL_DIR` — this skill's base directory (you are told it at launch).
- `SESSION_DIR` — `<SESSION_ROOT>/<demand-slug>/`, resolved per [`sessions.md`](sessions.md) (resume if it exists).
- `TEMPLATE` — the target template file (default: `SKILL_DIR/assets/target-template.intake-record.md`, or a user-supplied template).

## The session folder

Resolve-or-resume at the start of every run (see [`sessions.md`](sessions.md)):
`SESSION_ROOT` anchors at `$INTAKE_HOME` or the project (git) root, **not** the
cwd, and if the demand's folder already exists you **resume** it rather than
creating a duplicate.

```
<SESSION_ROOT>/<demand-slug>/
├── contract.lock.md          # Template Analyst
├── sources-index.md          # Source Indexer
├── sources/                  # Source Indexer (copies/links of inputs)
├── qa-log.md                 # Ledger Writer
├── target-document.md        # Doc Updater
├── glossary.md               # Glossary Keeper
├── readiness-report.md       # Readiness Reporter
└── output/                   # Humanizer · Translator · Enricher · Packager
```

## Phase 0 — Intake (you + the human)

Collect, in the human's language: the opening statement, any **file references**,
the **desired output language(s)**, and (optional) a custom `TEMPLATE`. Decide the
**mode**: *fresh* (no `target-document.md` yet) or *revisit* (one exists — re-score
it). **Resolve-or-resume** the session ([`sessions.md`](sessions.md)): if the
demand's `SESSION_DIR` already exists, resume it instead of creating a second one.
Do not ask a wall of questions yet.

## Phase 1 — Setup (parallel, then gate)

First, **Template Validator** checks the template against the audit checklist;
proceed only once it passes (fix the template otherwise). Then spawn **in the same
turn** (independent → parallel):
- **Source Indexer** — only if files were referenced. Normalizes them into
  `sources/` and writes `sources-index.md`.
- **Template Analyst** — derives `contract.lock.md` (sections, rubrics, `blocks`,
  `min-confidence`) from the validated template and records the **template hash**.
  If a prior `contract.lock.md` exists with a *different* hash → it restarts
  analysis (see `contract-and-template.md` § Restart).

Gate: `contract.lock.md` must exist before looping.

## Phase 2 — Capture loop (iterate until the gate clears)

Each iteration:

1. Spawn **in the same turn** (both read-only proposers → parallel):
   - **Question Strategist** — reads contract + `qa-log.md` + `target-document.md`,
     returns the next batch of questions (≈1–3, one theme) each with rationale, the
     section it targets, a **`mode`** (`open` | `choice`), and — for `choice`
     questions — 2–4 hypothesis `options`, aimed at the lowest-confidence
     **blocking** gaps.
   - **File Extraction** — reads `sources/` + `qa-log.md` + contract, returns
     *proposed answers* to open questions it can satisfy from the files
     (`inferred`, with `source` + confidence).
2. **Ledger Writer** (serial) commits: the new questions+rationale, and any
   file-derived proposed answers.
3. **You** present to the human only the questions *not* already satisfied by File
   Extraction, **rendering each by its `mode`** (see `questioning-method.md` §
   *Rendering the questions*): `open` questions as free-text prose; `choice`
   questions via `AskUserQuestion` — the Strategist's hypotheses as options, the
   disposition hatches appended, "Other" for the open answer, `multiSelect` where
   several apply. Collect answers (the chosen option label / `Other:` text, or the
   prose reply). Hand them to the **Ledger Writer** to record, including which option
   was picked and the disposition it maps to. An answer may spawn follow-up questions
   → Strategist proposes, Ledger Writer records them with `spawned-by`.
4. **Doc Updater** (serial) fills/updates `target-document.md` from the committed
   answers, preserving each section's confidence/disposition line.
5. **Confidence Auditor** (read-only) re-scores every section against its rubric,
   checks the document for truncation, **flags** conflicts (it does not resolve
   them), and returns the **gap verdict** + readiness score.
   - On a flagged conflict, spawn the **Reconciler** (read-only): it recommends
     which value to keep (or a disambiguating question); you route that to the
     Ledger Writer.
   - To show the human where things stand, spawn the **Readiness Reporter** (writes
     `readiness-report.md`) — the live gap map.
   - When domain terms accumulate (typically after the first capture rounds, and
     again before production), spawn the **Glossary Keeper**: it reads `qa-log.md`
     and `target-document.md` and writes canonical terms to `glossary.md`. That
     file is then read by the **Doc Updater** (this phase) and by the **Humanizer**
     and **Translator** (Phase 3) so terminology never drifts. Optional for trivial
     demands with no special vocabulary.
6. Gate check: **stop** when every `blocks=true` section is either ≥ its
   `min-confidence` *or* honestly disposed (`assumption`/`discovery`/`deferred`).
   Otherwise loop — Strategist's next batch targets the Auditor's flagged gaps.

Parallelism inside the loop: Strategist ∥ Extraction (read-only). Ledger Writer →
Doc Updater run **serially** (each is a single-writer). Auditor is read-only after.

## Phase 3 — Production (isolated context, parallel variants)

Once the gate clears, hand off to isolated agents that need only the final doc —
this keeps your context lean ("isolate when satisfied"):

1. **Humanizer** writes `output/humanized.md` (must finish first — it is the
   canonical clean copy the others read).
2. Then spawn **in the same turn** (parallel variants, distinct files):
   - **Translator** → `output/translated.<lang>.md` for each requested language.
   - **Visual Enricher** → `output/enriched.md`.

   *(Per project choice: translated and enriched are independent variants; they do
   not combine into one file.)*

## Phase 4 — Wrap

- **Packager** assembles `output/`, writes `output/manifest.md` (artifact index,
  readiness score, open dispositions, template hash/version).
- You report to the human: what was produced, the readiness score, and every item
  still parked as assumption/discovery/deferred.

## The full roster (each a standalone agent)

- **Setup:** Template Validator, Source Indexer, Template Analyst.
- **Loop:** Question Strategist, File Extraction, Reconciler (read-only proposers);
  Ledger Writer, Doc Updater, Glossary Keeper, Readiness Reporter (writers);
  Confidence Auditor (read-only gate).
- **Production:** Humanizer, then Translator ∥ Visual Enricher.
- **Wrap:** Packager.

Every writer obeys the single-writer + serialize/queue/merge/RMW rules in
`writing-integrity.md`. Add any future capability as its own agent under the same
rules rather than overloading an existing one.
