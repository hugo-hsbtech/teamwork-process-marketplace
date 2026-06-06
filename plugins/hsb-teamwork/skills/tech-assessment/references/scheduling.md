# Scheduling — the declarative pipeline graph (hybrid model)

Ordering is **declared as data**, not hard-coded in prose. The source of truth is the
per-skill `pipeline.yaml` (this skill's is [`../pipeline.yaml`](../pipeline.yaml));
`tools/pipeline_graph.py` validates it and computes the schedule. This file is the
**shared model doc** every skill's graph points to — origination-brainstorm,
readiness-package (two acts: `pipeline.intake.yaml` + `pipeline.readiness.yaml`),
tech-assessment, prd-generation, and initiative-analytics each ship a graph under the
same schema. `tools/check_pipelines.sh` validates all of them.

## Why declarative

The phase-by-phase prose in [`orchestration.md`](orchestration.md) is the *narrative*
view. The risk of prose-only ordering is that two agents quietly claim the same output,
or an agent runs before the thing it depends on exists, and nothing catches it. The
graph makes those failures **mechanical**: the validator fails the build, in CI or at
authoring time, instead of the conflict surfacing in a generated document.

## The two edge kinds (this is the hybrid)

Each node declares what it `reads` (consumes) and `decides` (logically authors). From
those, two kinds of dependency edge fall out:

- **`reads` — a HARD edge.** A node cannot run until every datum it reads exists.
  Topological order is computed from hard edges alone; independent nodes at the same
  depth run **in parallel** (one batch).

- **`provisional_on` — a SOFT edge.** The node runs **early**, in the parallel draft
  pass, *before* the named datum exists, so the CTO opens a fully pre-filled form. Its
  output is tagged **provisional**. When the named datum resolves, a `reconciliations`
  rule re-dispositions the provisional output.

The soft edge is the whole point of the hybrid: you keep the pre-fill UX (everything
drafted at once) **and** the safety (the conflict is reconciled by construction), and
the choice of which outputs are provisional is **data you can change**, not prose you
have to rewrite.

### The load-bearing example

`hsb-effort-estimator` and `hsb-adr-proposer` are `provisional_on: [feasibility-verdict]`.
The scheduler therefore runs them in the **same batch** as `hsb-feasibility-assessor`
(none reads the verdict, so none waits for it) — the draft pass stays parallel. Because
they are provisional, the validator **requires** a reconciliation rule for them; the one
in `pipeline.yaml` re-dispositions both to "N/A — vetoed" when the verdict is
`Infeasible as scoped`. Remove the rule and the build fails
(`[unreconciled-provisional]`). This is the same conflict the prose fix in
[`feasibility.md`](feasibility.md) § Verdict-conditioned closure describes — here it is
enforced, not just documented.

## Logical authorship vs physical writing

Two separate concerns, both checked:

- **`decides`** — *logical* authorship: which single node settles a datum's value. The
  validator enforces **one decider per datum**. A datum decided by two nodes is the
  override class (it would flag, e.g., a readiness score "decided" in four places, or a
  derived section authored by both the Synthesizer and the Doc Updater).
- **`file_writers` / `persists`** — *physical* ownership: which single agent writes a
  file on disk (the engine's single-writer rule for concurrency safety). Logical
  authorship still funnels through these writers: a proposer `decides` a section, but
  `hsb-doc-updater` `persists` `technical-assessment.md`. The validator checks each file
  has exactly one writer and that the writer node declares it.

## What the validator enforces

Run `python3 tools/pipeline_graph.py skills/tech-assessment/pipeline.yaml`:

1. **single physical writer** — one owner per file.
2. **single logical decider** — one decider per datum (the override guard).
3. **no dangling reads** — every datum read is decided, external, or a section.
4. **acyclic** on hard `reads` edges.
5. **provisional ⇒ reconciled** — every `provisional_on` edge has a matching
   reconciliation rule (the draft-before-the-verdict guard).

On success it prints the computed parallel schedule and (with `--mermaid`) a diagram.
Add `--quiet` for a CI gate (prints nothing on pass, exits non-zero on any violation).

## How the orchestrator uses it

1. Read `pipeline.yaml`. Run each computed **batch** as one turn, spawning the batch's
   agents in parallel (the existing "run independent agents in the same turn" rule, now
   derived rather than hand-listed).
2. For a node tagged **provisional**, route its draft output through the writer as usual
   but keep it flagged; when its `provisional_on` datum resolves, apply the matching
   `reconciliations` rule (route the re-disposition through `via:`).
3. `fanout: per-section` nodes still expand one spawn per `SECTION`, all in their batch.
4. `governs: true` (the Tech Classifier) means its output determines which path sections
   are in force downstream — unchanged from the prose, now marked in the graph.

The graph does not replace the orchestration prose; it makes the prose's ordering
claims checkable. When the two disagree, the graph is authoritative and the prose is the
bug.

## Loops and multi-act skills

A `pipeline.yaml` is a **single-pass dependency skeleton**, not an execution trace. Two
caveats follow:

- **Capture / confirm loops** (origination's capture phase, the RP/TA/PRD confirm loops)
  are repeated by the orchestrator until the gate clears. The graph does not draw the
  back-edges that the iteration implies, because a strict DAG cannot carry them and they
  are an orchestrator construct, not a data dependency. Nodes in a looped phase are
  tagged with that `phase`.
- **Multi-act skills** ship one graph per act. readiness-package has
  `pipeline.intake.yaml` (Act 1, triage — the routing gate) and `pipeline.readiness.yaml`
  (Act 2, the RP, which runs only on a `Product Ready` decision). Each act produces a
  different document and is validated independently.

## Modeling choices worth knowing

- **Datum granularity is a choice.** Some sections are modeled individually (the TA's
  in-force sections) and some are bundled (origination's `capture-content`, the RP's
  `inherited-sections`) when the per-section detail adds nothing to ordering. Bundle when
  one node decides the whole group; split when different nodes decide different members.
- **Logical decider ≠ physical writer.** A datum's `decides` names who settles its value;
  `persists` / `file_writers` name who writes the file. Derived sections are excluded from
  `section_datums` so a node with `reads_all_sections` never reads its own output.
