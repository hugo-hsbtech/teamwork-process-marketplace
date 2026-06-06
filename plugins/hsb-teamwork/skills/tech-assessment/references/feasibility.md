# Feasibility — the CTO's first-class decision and the freeze gate

The CTO's first-class model is **feasibility** (`personas/03-cto.md` §3 — *feasibility
is first class*, the technical analogue of the Submitter's confidence and the PO's
decision). The `feasibility-verdict` section is the headline of the TA: the defensible
ruling on whether the RP's scope can be built, **on what terrain**, and under what
conditions. The CTO is the *feasibility authority* and the *terrain-setter*: a verdict on
unknown terrain is a guess, not a verdict (`03-cto.md` §3, the golden rule — *"feasibility
before commitment, terrain before feasibility"*).

`hsb-feasibility-assessor` is the **gate proposer** (analogous to the
`hsb-triage-assessor` for the PO's routing decision). It reads the drafted
architectural impact, NFR feasibility, integrations, risks, and hard constraints and
proposes one verdict — never a rubber stamp. The CTO commits the final verdict.

## The verdict scale

| Verdict | Meaning | Effect |
|---|---|---|
| `Feasible` | The scope is buildable as specified | TA proceeds to sign-off; PRD can merge RP + TA |
| `Feasible with caveats` | Buildable **if** stated conditions hold (e.g. a specific mechanism, a pre-condition, a hard constraint) | TA signs with the caveats recorded; the PO must honour the hard constraints in scope |
| `Infeasible as scoped` | Not buildable as scoped — the **veto** | TA freezes as a signed veto; the PO revises the RP scope and re-escalates |

## The decision model (first-class, not annotation)

The verdict carries the CTO's **feasibility-on-terrain layer** (`personas/03-cto.md` §3)
— structured, never optional prose:

| Field | Meaning |
|---|---|
| `verdict` | the ruling itself (`Feasible` / `Feasible with caveats` / `Infeasible as scoped`) |
| `rationale` | **why** — the defensible reasoning; never optional |
| `terrain` | **the knowledge base the verdict rests on** — a reference to the `tech-landscape-<system>.md`, or an honest "undocumented → Discovery". The new first-class attribute: a verdict on undocumented terrain is a guess, not a verdict. |
| `confidence` | 0–100 against the section threshold (reuses the engine's confidence layer) |
| `caveats` | for `Feasible with caveats`: exactly what must be true for the verdict to hold (each typically also a `hard-constraint`) |
| `basis` / `source` | the evidence it rests on (which NFR-feasibility row, architectural-impact area, risk) + its trace-to-source (e.g. "RP question #2", "tech-landscape §5", "reused ADR-102") |
| `generates` | what the verdict **creates downstream** — `hard_constraint` / `adr` / `discovery_spike` / `kb_update` — linking the judgment to the sections it drives |

High threshold by design (`min-confidence 85`): this is the central CTO judgment, so
it resolves only at high confidence and is always `cto_authored` — the assessor
proposes; the **CTO commits**.

## The veto path (`Infeasible as scoped`)

The veto is a **first-class, valid outcome**, not a failure of the run
(`interactions/05-po-to-cto.md`, `interactions/06-cto-to-po.md`):

1. The verdict carries the veto + a defensible rationale (which constraint or NFR makes
   the scope unbuildable).
2. The TA **still freezes** — the CTO's decision is complete and signed (`Status: Vetoed`).
3. The orchestrator pushes a **scope-revision signal** back to the `readiness/` phase
   (a note in `initiative.json` / `decisions.md`) so the PO revises the RP scope and
   **re-escalates**. The CTO **does not redefine the product** — they veto and state
   why; the PO owns the scope change.
4. On re-escalation, this skill runs again (Revisit mode) against the revised RP and
   bumps the TA version.

A veto is not a discovery gap — it is a signed conclusion. Do not park it as
`discovery`.

## The Discovery exit (a technical unknown blocks the assessment)

Distinct from the veto: if a technical unknown prevents the assessment from **closing
at all** (you cannot reach *any* defensible verdict yet), fill `discovery-path`:

- The CTO defines the **spike / investigation**; the PO determines the **time-box**.
- The demand returns to Discovery; the TA does not sign until the spike resolves.
- The KB-does-not-exist case (brownfield/hybrid, see [`classification.md`](classification.md))
  is the most common Discovery exit — documenting the current system is the spike.

The difference: **veto** = "I assessed it; it's infeasible as scoped." **Discovery** =
"I cannot assess it yet; here's what to investigate first."

## The freeze gate (`signOffReady`)

`signOffReady = true` (`personas/03-cto.md` §4/§10 — *every `blocksSignoff` section
resolved, the terrain documented, and any Discovery spike defined*) requires:

1. The `feasibility-verdict` is committed — `cto_authored` at its `min-confidence`
   (85). A verdict is mandatory; the TA never freezes without one.
2. **The terrain is documented.** The `tech-classification` KB is `Exists` / `Partial`,
   **or** the `tech-landscape` was created/updated for this demand (greenfield seed /
   brownfield document). *The TA does not sign a feasibility verdict on undocumented
   brownfield terrain* (`03-cto.md` §4) — an absent KB makes `discovery` the only honest
   disposition until `hsb-landscape-keeper` produces it.
3. Every other `blocksFreeze` section is either resolved (`cto_authored` /
   confirmed-`inherited`) **or** honestly disposed:
   - the non-applicable path → `Disposition: decided` ("N/A — <nature>");
   - "none" sections (integrations / hard-constraints / build-vs-buy when none
     apply) → `Disposition: decided`;
   - an unclosable unknown → `discovery` (owner + time-box).
4. **Verdict-conditioned closure:**
   - `Feasible` → all in-force technical sections resolved.
   - `Feasible with caveats` → the caveats are recorded as `hard-constraints`.
   - `Infeasible as scoped` → the veto rationale is recorded, **and** the draft-pass
     sections that depend on a buildable scope (`effort-cost`, `adrs`) are reconciled to
     `Disposition: decided` ("N/A — scope vetoed, see Verdict") rather than left fully
     drafted. Because those two run in parallel **before** the verdict exists (see
     [`orchestration.md`](orchestration.md) Phase 3/4), this is an explicit gate step,
     not a guess the proposers make: the orchestrator routes the re-disposition through
     `hsb-doc-updater` so a signed veto never carries a confident estimate or ADR set.

**Clearing the gate is not the same as choosing to sign.** When the gate clears on an honest
`discovery` for a section the CTO could actually firm now, that is permission for the gate to
clear, not permission to freeze. Before production the orchestrator runs the **Phase 4.5
assessment checkpoint** ([`orchestration.md`](orchestration.md) § Phase 4.5): it separates
*CTO-closeable-now* residuals from *genuine spikes* and asks the CTO whether to close them now
(end-to-end) or defer. Deferring any closeable item is the **CTO's explicit decision**, never
the skill's. The two outcomes above — a **veto** and a **genuine Discovery exit** — are not
re-litigated at the checkpoint: the veto is a signed conclusion and the spike is real terrain
work; both stand. Headless / batch has no CTO to ask, so honest dispositions stand.

When `signOffReady` **and the checkpoint is settled**, the TA freezes (`Status: Signed off`
or `Status: Vetoed`) and the orchestrator discharges the RP's `TechAssessmentRef` debt in the
initiative index
(`status: signed` / `vetoed`, with the verdict and link). This is the migration the
readiness-package's `references/escalation.md` anticipated: with the tech-assessment
skill present, the RP's freeze gate tightens to require a **signed** TA instead of the
temporary `deferred` path.

## Headless / batch

No live CTO means **no questions** and **honest dispositions** — not skipping the
verdict. The `hsb-feasibility-assessor` proposes the verdict under honest dispositions;
any section it cannot draft to threshold is disposed `assumption` (owner: CTO, "to
confirm") or `discovery`. The output is always "draft for CTO sign-off," never a real
`signOffReady` on its own — a feasibility verdict is the CTO's to commit.
