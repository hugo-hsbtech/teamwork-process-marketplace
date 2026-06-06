# Inheritance — carry-forward from the origination-record

The origination-record is not just another source file. It is an **already-graded
artefact**: its sections have been scored, dispositioned, and (in many cases)
confirmed by the Submitter. Treating it as a source to re-infer from scratch
would lose that grading and inflate confidence. Instead, `hsb-stage-inheritor`
carries it forward — preserving the origination's `confidence`, `source`, and
`disposition` — so the PO receives a traceable baseline rather than a
blank form.

`inherited = partial confidence, traceable` (`personas/02-po.md:245`).

## How the origination-record is referenced

The orchestrator discovers the origination-record from the **works index** in
`initiative.json` (the phase whose `produces` is `origination-record`, via its
`artifacts.canonical` path) — not by assuming `origination/`. It hands that path to
`hsb-source-indexer`, which records it as an **in-place reference** in the readiness
phase's `sources-index.md`, flagging it as the **primary source**. The artefact is
**not copied** — it lives once in the `origination/` phase folder of the same
initiative, and the index points there; `sources/` holds only the extra files the PO
provides. Shared terms come from the brokered `PHASE_DIR/glossary.md` (seeded from
the initiative's glossary store), so the RP uses the same vocabulary the origination
settled on.

`hsb-stage-inheritor` reads the referenced origination-record and the RP contract
(`contract.lock.md`). It does **not** perform fresh inference — it maps
origination sections to RP sections, preserving the origination's already-graded values.

## The section mapping

| Origination section | RP section | Inheritance note |
|---|---|---|
| `problem` (Problem statement) | `context-problem` (Contexto e Problema) | Direct carry. If the origination section describes a solution rather than a pain, the inheritor adds a hint flagging the golden rule violation. |
| `objectives` / `expected-outcome` | `objectives` (Objetivos e Resultado Esperado) | Direct carry. |
| `reach` / `personas` (Who is impacted) | `personas` (Personas / Jobs-to-be-done) | Direct carry; confidence preserved. |
| `scope` (Scope in/out, if present) | `scope` (Escopo Incluído e Excluído) | Direct carry; if the origination did not define scope explicitly, confidence is lowered and the PO is prompted to deepen. |
| `metrics` / `success-criteria` | `metrics` (Métricas de Sucesso) and `release-criteria` (Critérios de Sucesso e Aceite) | Split into two RP sections; each inherits the relevant origination entries. |
| `risks` / `dependencies` | `risks` (Riscos e Dependências) | Carry product/business risks only; the inheritor adds a hint that technical risks move to the Technical Assessment. |
| `effort-estimate` (if present) | `effort-estimate` (Avaliação Preliminar de Esforço e Custo) | Carry as preliminary; hint that the firm number comes from the CTO's Technical Assessment. |
| `roadmap` (if present) | `roadmap` (Roadmap Sugerido) | Direct carry. |

Sections with no origination coverage are left for `hsb-section-drafter` to propose
or for the PO to author. The inheritor never invents content for sections the
origination did not cover. Note that `user-journey` (Seção 6.5) has no origination
counterpart — it is drafted fresh by `hsb-section-drafter`, and `user-stories`
derive from its steps.

**From the Intake Record (not the origination).** The RP `meta` also inherits the
**demand nature** (Greenfield / Brownfield / Híbrido) and the **Knowledge Base**
reference (`tech-landscape-[system].md`) the PO classified at triage. The inheritor
carries these forward verbatim into the RP metadata — it does not re-classify.

**The `exec-summary` (Resumo Executivo) section** is synthesized from the
origination's problem + objectives + scope rather than mapped from a single origination
field. The inheritor proposes it at partial confidence, sourced to those
constituent origination sections.

## What the inheritor preserves

For every proposed entry:

1. **Content** — restated in product terms for the RP section, without adding
   new substance.
2. **`confidence`** — the origination's graded value, never inflated. If the RP
   section needs more than the origination section provides (e.g. the origination was
   `ai_inferred` at 55% but the RP rubric requires more depth), the inheritor
   **lowers** the confidence and adds a hint naming what the PO must deepen.
3. **`source`** — the origination's source attribution (submitter statement,
   file reference, or inferred label).
4. **`disposition`** — if the origination section carried an open disposition
   (`assumption` / `discovery` / `deferred`), the inheritor carries it forward
   verbatim. The RP does not silently resolve origination uncertainty.

## Open dispositions and "Prontidão herdada"

The RP template includes a **"Prontidão herdada"** (inherited-readiness) section
that lists every open disposition carried forward from the origination. The inheritor
populates this section with the items it cannot resolve locally — gaps the PO
must address in the confirm loop.

This means the PO can see at a glance what the origination left unresolved and
decide whether to deepen, accept as `discovery`, or escalate. None of these
inherited open items silently disappear; each carries its original origination rationale.

## What the inheritor does not do

- It does not draft the new product sections (`business-rules`, `user-journey`,
  `user-stories`, `nfrs`, `edge-cases`). Those are `hsb-section-drafter`'s job.
- It does not re-infer content the origination already graded — it carries forward,
  not re-analyzes.
- It does not write any shared files. It returns proposals to the orchestrator,
  which routes them through `hsb-ledger-writer` → `hsb-doc-updater`
  per the single-writer rule
  ([`../../origination-brainstorm/references/writing-integrity.md`](../../origination-brainstorm/references/writing-integrity.md)).
