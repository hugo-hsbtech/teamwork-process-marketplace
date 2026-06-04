# Design Spec — `readiness-package` skill

**Date:** 2026-06-03
**Plugin:** `hsb-teamwork`
**Status:** Approved design, pending implementation plan
**Author:** Hugo Seabra

---

## 1. Purpose

Add a sibling skill `/hsb-teamwork:readiness-package` that automates the Product
Owner's **Act 2 — Racionalização**: transforming a `Product Ready` **origination-record**
(produced by the existing `origination-brainstorm` skill) into a frozen **Readiness
Package (RP)** as defined by `hsb-teamwork-process/templates/02-readiness-package.md`
and `personas/02-po.md`.

The skill reuses the origination engine's architecture (template-as-contract,
single-writer rule, read-modify-write, confidence gate, portable session folder,
Codex mirror) and adds an RP-specific template, three RP-specific agents, and a
**draft-then-confirm** authoring model.

It stops at RP freeze. The Technical Assessment (`templates/03`) and the PRD
(`templates/04`) are later cycles, but the RP honestly signals when a Technical
Assessment is owed.

### Why this stage

`plugin.json` already lists `readiness-package` as the next planned skill. In the
business process, the origination plugin covers `00-submitter-brief → 01-origination-record`
(the PO's Triagem). The PO's very next act is Racionalização, which produces the
RP — the "definição de pronto de produto" that, once fused with the CTO's Technical
Assessment, becomes the PRD that opens the downstream (`personas/02-po.md:311-316`).

---

## 2. Scope

**In scope:** `origination-record → readiness-package (RP)`, frozen, with humanized /
translated / enriched variants and a manifest — as its own sibling skill.

**Out of scope (later cycles):**
- The CTO **Technical Assessment** skill (`templates/03`).
- The **PRD** fusion skill (`templates/04`).
- The `reused_from_KB` authoring path (reusing prior RP sections / ADRs for similar
  demands, `personas/02-po.md:305`) — deferred to a later iteration of this skill.

---

## 3. Locked decisions

| # | Decision | Choice |
|---|----------|--------|
| 1 | Scope | Just the Readiness Package (`origination-record → RP`), as its own skill |
| 2 | Agent strategy | Reuse the engine; add only the RP-specific agents the roster genuinely lacks |
| 3 | Session model | Separate **linked** RP session folder; origination-record pulled in as an inherited source |
| 4 | Authoring model | **Draft-then-confirm** (engine pre-fills, PO judges); questions are a low-confidence fallback |
| 5 | Escalation / TA | Detect + flag; record `TechAssessmentRef` as `deferred`; TA itself out of scope |
| 6 | KB reuse | Deferred to a later iteration |
| — | Output language | pt-BR mirroring origination (default) |
| — | References | Shared-by-reference with origination's engine-level method docs; no duplication |
| — | Naming | New agents `readiness-*`; reused engine agents keep their legacy `origination-*` names |

---

## 4. Authoring model — draft-then-confirm

The documented PO model (`personas/02-po.md:246, 251, 324, 327`) is **AI drafts →
PO judges/confirms/freezes**, not section-by-section interviewing. The screen
"should not look like a form filled by hand … it should look like the system already
rationalized the demand and is asking for the PO's judgment" (`:324`).

Every RP entry carries an `origin` (`personas/02-po.md:149`):

| `origin` | Meaning | Confidence |
|----------|---------|------------|
| `inherited` | Carried from the origination-record, with `source` | Partial, traceable |
| `ai_drafted` | Engine pre-filled; PO reviews and confirms | Partial until confirmed |
| `po_authored` | PO decided directly | Full |
| `reused_from_KB` | Reused from a prior RP/ADR | *(deferred — out of scope)* |

And a `disposition` (`:150, 242-247`): `decided`, `inherited`, `ai_drafted`,
`discovery`. As with the Submitter's "I don't know," PO uncertainty never blocks —
`discovery` counts as *resolved-as-unknown, time-boxed*.

**Flow:**
1. **Draft pass** — no section starts empty. `readiness-inheritor` fills inheritable
   sections (`inherited`); `readiness-drafter` proposes the new product sections
   (`ai_drafted`). All at partial confidence with explicit origin + source.
2. **Confirm loop** — the PO reviews, edits, justifies; entries promote to
   `po_authored` / `decided`, raising confidence. The question-first machinery
   (`question-strategist` → human → `ledger-writer`) fires **only** for sections the
   engine could not draft confidently or that the PO opts to deepen.

**Freeze gate (`freezeReady`, `personas/02-po.md:161-163`):** every `blocksFreeze`
section is resolved (`po_authored` / `decided` / `discovery` / confirmed-`inherited`)
**and** `TechAssessmentRef.status ∈ {signed, not_requested}`. See §8 for the
temporary divergence on the TA condition.

---

## 5. Session & inheritance model

- New **linked** session folder: `SESSION_ROOT/<demand-slug>-readiness/`
  (`SESSION_ROOT` resolved exactly as in origination: `$ORIGINATION_HOME` → `<git-root>/origination`
  → `<cwd>/origination`).
- The origination stage's `output/humanized.md` (or `target-document.md`) is indexed as
  the **primary source** and treated specially: its already-graded sections
  (problem, personas, scope, metrics) are **carried forward with their
  `confidence / source / disposition` intact** by `readiness-inheritor`, not
  re-inferred from scratch.
- Resume-by-slug behaves as in origination: re-running continues the same `-readiness`
  folder; nothing duplicates (read-modify-write + stable-id keying).

**Folder contents:**
```
<SESSION_ROOT>/<demand-slug>-readiness/
├── contract.lock.md            # template-analyst (RP contract, hash-locked)
├── sources-index.md            # source-indexer
├── sources/                    # source-indexer (incl. the inherited origination-record)
├── qa-log.md                   # ledger-writer (the ledger)
├── readiness-document.md       # doc-updater (the RP being filled)
├── glossary.md                 # glossary-keeper (optional)
├── readiness-report.md         # readiness-reporter (optional, gap map)
└── output/
    ├── humanized.md            # humanizer
    ├── translated.pt-BR.md     # translator (one per language)
    ├── enriched.md             # visual-enricher
    └── manifest.md             # packager
```

---

## 6. The template (the contract)

A new annotated template ships as a swappable asset:

- `skills/readiness-package/assets/target-template.readiness-package.md`
- `skills/readiness-package/assets/target-template.readiness-package.guide.md`
- `skills/readiness-package/assets/golden-example.md`

It maps the **14 RP sections + the `TechAssessmentRef` bridge**
(`templates/02-readiness-package.md`, `personas/02-po.md:204-220`), each annotated
with `id / blocks / min-confidence / kind` plus a self-sufficient rubric
(`satisfiedWhen`).

| # | Section | Group | Blocks freeze | Origin note |
|---|---------|-------|---------------|-------------|
| 1 | Resumo Executivo | Contexto | ✅ | inherited |
| 2 | Contexto e Problema (a dor, não a solução) | Contexto | ✅ | inherited — golden rule |
| 3 | Objetivos e Resultado Esperado | Contexto | ✅ | inherited |
| 4 | Personas / Jobs-to-be-done | Contexto | ✅ | inherited |
| 5 | Escopo Incluído e Excluído | Escopo | ✅ | inherited |
| 6 | Regras de Negócio e Fluxos | Escopo | ✅ | ai_drafted |
| 7 | User Stories + Critérios de Aceite | Comportamento | ✅ | ai_drafted (Given/When/Then, non-dev verifiable) |
| 8 | Requisitos Não-Funcionais (NFRs) | Qualidade | ✅ | ai_drafted (ISO/IEC 25010 checklist) |
| 9 | Edge Cases e Modos de Falha | Qualidade | ✅ | ai_drafted |
| 10 | Métricas de Sucesso (primária · secundária · guardrail) | Sucesso | ✅ | inherited/enriched |
| 11 | Critérios de Sucesso e Aceite (do release) | Sucesso | ✅ | inherited |
| 12 | Riscos e Dependências (produto/negócio) | Riscos | ✅ | inherited (tech risks → TA) |
| 13 | Avaliação Preliminar de Esforço e Custo | Riscos | — | inherited (firm number from CTO/TA) |
| 14 | Roadmap Sugerido | Roadmap | — | inherited |
| — | Referência ao Technical Assessment | (bridge) | ✅ if requested | `TechAssessmentRef` — verdict + link, not content |

- **Golden rule:** problem before solution. Section 2 fails if it describes a
  solution (`personas/02-po.md:222`).
- **Scales down:** for a small improvement the RP compresses to the spine
  (Problema → Métrica-objetivo → Escopo in/out → 3–5 acceptance criteria → at-risk
  NFRs). The contract is a ceiling, not a mandatory floor (`:224`).

The template is hash-locked into `contract.lock.md` by the reused `template-analyst`;
changing the template restarts analysis exactly as in origination.

---

## 7. Agent roster

### 7.1 Reused engine agents (no code change)

These are template-driven and specialize purely through the new RP template + guide.
The `origination-` prefix is legacy naming; they are the shared engine.

`origination-template-validator`, `origination-source-indexer`, `origination-template-analyst`,
`origination-question-strategist`, `origination-file-extraction`, `origination-reconciler`,
`origination-ledger-writer`, `origination-doc-updater`, `origination-glossary-keeper`,
`origination-readiness-reporter`, `origination-confidence-auditor`, `origination-humanizer`,
`origination-translator`, `origination-visual-enricher`, `origination-packager`.

### 7.2 New `readiness-*` agents

| Agent | Origin it serves | Role | Read/write |
|-------|------------------|------|------------|
| `readiness-inheritor` | `inherited` | Carry the origination-record's already-graded sections into RP capture sections, preserving `confidence/source/disposition`; mark what the PO must deepen. Semantically distinct from `file-extraction` (fresh inference), so it earns its own agent. | Read-only proposer |
| `readiness-drafter` | `ai_drafted` | Propose the new product sections (business rules, user stories + Given/When/Then AC, NFRs/ISO-25010, edge cases) at partial confidence for PO judgment. | Read-only proposer; `doc-updater` remains the single writer |
| `readiness-escalation-flagger` | — | Scan the emerging RP for architectural triggers (infra, multi-tenancy, IA/runtime, security, integrations), ask the PO to confirm, set `escalation_required`, record `TechAssessmentRef` as `deferred`. No origination equivalent (origination does triage, not CTO-escalation). | Read-only proposer |

**Single-writer discipline preserved:** all three new agents are read-only proposers.
The existing `doc-updater` is still the sole writer of `readiness-document.md` and
`ledger-writer` the sole writer of `qa-log.md`. The drafter proposes `ai_drafted`
content; the doc-updater writes it with `origin=ai_drafted` at partial confidence;
PO confirmation flows through ledger-writer → doc-updater promotes to `po_authored`.

---

## 8. Orchestration — phases

1. **Setup** — `template-validator` → `template-analyst` (RP `contract.lock.md`);
   `source-indexer` in parallel (indexes the linked origination folder + any extra files);
   then `readiness-inheritor` pre-fills inheritable sections from the origination-record.
2. **Draft pass** — `readiness-drafter` proposes the `ai_drafted` sections;
   `doc-updater` writes them at partial confidence; `readiness-escalation-flagger`
   runs once scope/rules are known.
3. **Confirm loop** — `confidence-auditor` re-scores independently → `question-strategist`
   targets the lowest-confidence / unconfirmed blocking sections (fallback only) →
   PO reviews/edits/confirms → `ledger-writer` records → `doc-updater` promotes
   origins and raises confidence; `reconciler` on conflicts (e.g. origination said X, PO
   now says Y); optional `glossary-keeper` / `readiness-reporter`. Loops until
   `freezeReady`.
4. **Production** — `humanizer` → `translator` (pt-BR) ∥ `visual-enricher`
   (scope in/out table, persona/JTBD map, business-rule flow, metrics table).
5. **Wrap** — `packager` → `manifest.md` noting freeze state, the TA-pending flag,
   and the handoff to PRD/PM.

### Documented divergence — the TA freeze condition

The docs require `freezeReady` to also satisfy `TechAssessmentRef.status ∈ {signed,
not_requested}` (`personas/02-po.md:162`). Because the `tech-assessment` skill does
not exist yet, when escalation **is** required this skill will:
- freeze the RP's product sections,
- record `TechAssessmentRef` as **`deferred` (TA pending — out of current tooling
  scope)**, and
- mark the package **provisionally frozen**.

**Migration note:** when the `tech-assessment` skill lands, the gate tightens to
require `status = signed`. This divergence is deliberate and temporary, and must be
called out in the skill's README and manifest output.

---

## 9. Parity & portability

- **Codex mirror:** three new `.toml` wrappers (`hsb-readiness-inheritor`,
  `hsb-readiness-drafter`, `hsb-readiness-escalation-flagger`) that point at the
  shared `agents/readiness-*.md`; a new `codex/prompts/hsb-teamwork-readiness-package.md`;
  `codex/AGENTS.md` updated with the RP flow. Codex runs the roles sequentially;
  Claude parallelizes the read-only proposers. No duplicated logic.
- **Shared method, no duplication:** the RP `references/` adds only RP-specific docs
  (inheritance, draft-then-confirm, escalation, the freeze gate, questioning RP
  sections) and **cites** origination's engine-level references (single-writer, RMW,
  sessions, ledger-schema, grounding) rather than copying them.
- **`plugin.json`:** move `readiness-package` from "Planned" to implemented; bump
  version.

---

## 10. Deliverables

```
plugins/hsb-teamwork/
├── skills/readiness-package/
│   ├── SKILL.md
│   ├── README.md
│   ├── references/            # RP-specific docs; cite origination's shared method
│   └── assets/
│       ├── target-template.readiness-package.md
│       ├── target-template.readiness-package.guide.md
│       └── golden-example.md
├── agents/
│   ├── readiness-inheritor.md
│   ├── readiness-drafter.md
│   └── readiness-escalation-flagger.md
├── codex/
│   ├── agents/hsb-readiness-inheritor.toml
│   ├── agents/hsb-readiness-drafter.toml
│   ├── agents/hsb-readiness-escalation-flagger.toml
│   ├── prompts/hsb-teamwork-readiness-package.md
│   └── AGENTS.md              # updated
└── .claude-plugin/plugin.json # updated
```

Plus an eval suite mirroring `evals/origination-brainstorm/` (fixtures: an origination-record
golden as input; rubric scoring the frozen RP).

---

## 11. Open questions for the implementation plan

- Exact `min-confidence` thresholds per RP section (the high-stakes sections —
  business rules, acceptance criteria — likely warrant a higher bar than the default 70).
- Whether `readiness-reporter` output should surface the `origin` mix
  (inherited / ai_drafted / po_authored) as a "how much did the PO actually decide"
  signal, echoing the prototype's AI-impact metric (`personas/02-po.md:289`).
- The eval's reference dataset: reuse the origination golden's downstream, or author a
  dedicated origination-record → RP golden pair.

---

## 12. Source references

- `hsb-teamwork-process/personas/02-po.md` — the two acts, the decision/origin model,
  draft-then-confirm, the freeze gate, the CTO lateral relationship.
- `hsb-teamwork-process/templates/02-readiness-package.md` — the 14-section contract.
- `hsb-teamwork-process/02-happy-path.md:174` — RP freezes, then RP + TA fuse into PRD.
- `hsb-teamwork-process/interactions/05-po-to-cto.md`, `07-po-to-pm.md` — escalation
  and PRD handoff.
- `plugins/hsb-teamwork/skills/origination-brainstorm/` — the engine being reused.
```
