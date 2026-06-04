# Inheritance — carry-forward from the intake-record

The intake-record is not just another source file. It is an **already-graded
artefact**: its sections have been scored, dispositioned, and (in many cases)
confirmed by the Submitter. Treating it as a source to re-infer from scratch
would lose that grading and inflate confidence. Instead, `readiness-inheritor`
carries it forward — preserving the intake's `confidence`, `source`, and
`disposition` — so the PO receives a traceable baseline rather than a
blank form.

`inherited = partial confidence, traceable` (`personas/02-po.md:245`).

## How the intake-record is indexed

`intake-source-indexer` indexes the initiative's `intake/` phase folder (its
`output/humanized.md` or `target-document.md`) into `sources/` alongside any
extra files the PO provides. The intake artefact is flagged as the **primary
source** in `sources-index.md`.

`readiness-inheritor` reads the indexed intake-record and the RP contract
(`contract.lock.md`). It does **not** perform fresh inference — it maps
intake sections to RP sections, preserving the intake's already-graded values.

## The section mapping

| Intake section | RP section | Inheritance note |
|---|---|---|
| `problem` (Problem statement) | `context-problem` (Contexto e Problema) | Direct carry. If the intake section describes a solution rather than a pain, the inheritor adds a hint flagging the golden rule violation. |
| `objectives` / `expected-outcome` | `objectives` (Objetivos e Resultado Esperado) | Direct carry. |
| `reach` / `personas` (Who is impacted) | `personas` (Personas / Jobs-to-be-done) | Direct carry; confidence preserved. |
| `scope` (Scope in/out, if present) | `scope` (Escopo Incluído e Excluído) | Direct carry; if the intake did not define scope explicitly, confidence is lowered and the PO is prompted to deepen. |
| `metrics` / `success-criteria` | `metrics` (Métricas de Sucesso) and `release-criteria` (Critérios de Sucesso e Aceite) | Split into two RP sections; each inherits the relevant intake entries. |
| `risks` / `dependencies` | `risks` (Riscos e Dependências) | Carry product/business risks only; the inheritor adds a hint that technical risks move to the Technical Assessment. |
| `effort-estimate` (if present) | `effort-estimate` (Avaliação Preliminar de Esforço e Custo) | Carry as preliminary; hint that the firm number comes from the CTO's Technical Assessment. |
| `roadmap` (if present) | `roadmap` (Roadmap Sugerido) | Direct carry. |

Sections with no intake coverage are left for `readiness-drafter` to propose
or for the PO to author. The inheritor never invents content for sections the
intake did not cover.

**The `exec-summary` (Resumo Executivo) section** is synthesized from the
intake's problem + objectives + scope rather than mapped from a single intake
field. The inheritor proposes it at partial confidence, sourced to those
constituent intake sections.

## What the inheritor preserves

For every proposed entry:

1. **Content** — restated in product terms for the RP section, without adding
   new substance.
2. **`confidence`** — the intake's graded value, never inflated. If the RP
   section needs more than the intake section provides (e.g. the intake was
   `ai_inferred` at 55% but the RP rubric requires more depth), the inheritor
   **lowers** the confidence and adds a hint naming what the PO must deepen.
3. **`source`** — the intake's source attribution (submitter statement,
   file reference, or inferred label).
4. **`disposition`** — if the intake section carried an open disposition
   (`assumption` / `discovery` / `deferred`), the inheritor carries it forward
   verbatim. The RP does not silently resolve intake uncertainty.

## Open dispositions and "Prontidão herdada"

The RP template includes a **"Prontidão herdada"** (inherited-readiness) section
that lists every open disposition carried forward from the intake. The inheritor
populates this section with the items it cannot resolve locally — gaps the PO
must address in the confirm loop.

This means the PO can see at a glance what the intake left unresolved and
decide whether to deepen, accept as `discovery`, or escalate. None of these
inherited open items silently disappear; each carries its original intake rationale.

## What the inheritor does not do

- It does not draft the new product sections (`business-rules`, `user-stories`,
  `nfrs`, `edge-cases`). Those are `readiness-drafter`'s job.
- It does not re-infer content the intake already graded — it carries forward,
  not re-analyzes.
- It does not write any shared files. It returns proposals to the orchestrator,
  which routes them through `intake-ledger-writer` → `intake-doc-updater`
  per the single-writer rule
  ([`../../intake-brainstorm/references/writing-integrity.md`](../../intake-brainstorm/references/writing-integrity.md)).
