---
template: target-template.readiness-package.md
template_path: /home/hugo/Dropbox/DevProjects/HSB/teamwork-process-marketplace/.claude/skills/readiness-package/assets/target-template.readiness-package.md
template_hash: 74cd7c34fc0d21a0e37ee6720a50418772f31f3fbaeddcc8696d833068ba30ef
template_version: v1
default_min_confidence: 70
generated: 2026-06-03
---

# Contract — Readiness Package

Locked snapshot of the target template. The template is the source of truth; this
file is the parsed contract the RP pipeline runs against. Default confidence
threshold **X = 70** (from the template header). A *direct* answer below a
section's `min-confidence` is `low_confidence` and does not clear a blocking gate
on its own — it must improve or take an honest disposition.

## Sections

| id | section | kind | blocks | min-confidence | inputs | rubric (one line) |
|----|---------|------|--------|----------------|--------|-------------------|
| meta | Metadados | meta | false | 0 | — | package IDs, linked intake, status, output language |
| revisions | Histórico de Revisão | meta | false | 0 | — | version/date/author/status changelog rows |
| inherited-readiness | Prontidão herdada e dispositions em aberto | derived | false | 0 | exec-summary, context-problem, objectives, personas, scope, metrics, release-criteria, risks | surface intake readiness score + surviving assumptions/unknowns/delegated reqs |
| exec-summary | Seção 1 — Resumo Executivo | capture | true | 70 | — | 2–4 paragraphs: problem, what is built, expected business outcome |
| context-problem | Seção 2 — Contexto e Problema | capture | true | 80 | — | current scenario, limits, customer pain, business impact — pain not solution |
| objectives | Seção 3 — Objetivos e Resultado Esperado | capture | true | 70 | — | ≥2 numbered, observable, verifiable post-release objectives |
| personas | Seção 4 — Personas Impactadas / JTBD | capture | true | 70 | — | per persona: job-to-be-done + how impacted by this delivery |
| scope | Seção 5 — Escopo Incluído e Excluído | capture | true | 75 | — | explicit in/out (out is mandatory) + deferred feeding roadmap |
| business-rules | Seção 6 — Regras de Negócio e Fluxos | capture | true | 80 | — | atomic verifiable rules + state transitions covering error paths |
| user-stories | Seção 7 — User Stories + Critérios de Aceite | capture | true | 80 | — | story per value block + Given/When/Then AC, non-dev verifiable |
| nfrs | Seção 8 — Requisitos Não-Funcionais | capture | true | 70 | — | applicable ISO/IEC 25010 dimensions; ≥1 filled; PO states quality req |
| edge-cases | Seção 9 — Edge Cases e Modos de Falha | capture | true | 70 | — | error/timeout/permission/concurrency states + expected system behavior |
| metrics | Seção 10 — Métricas de Sucesso | capture | true | 70 | — | projected baseline values; leading+lagging + ≥1 guardrail |
| release-criteria | Seção 11 — Critérios de Sucesso e Aceite | capture | true | 70 | — | high-level done&valuable criteria; ≥Business/Quality/UX, measurable |
| risks | Seção 12 — Riscos e Dependências | capture | true | 70 | — | product/business/adoption/external/compliance risks w/ prob·impact·mitigation |
| effort-estimate | Seção 13 — Avaliação Preliminar de Esforço | capture | false | 0 | — | internal PO guess for sequencing; firm number is CTO's TA |
| roadmap | Seção 14 — Roadmap Sugerido | capture | false | 0 | — | value sequencing beyond release: MVP + Phase 2/3 backlog |
| tech-assessment-ref | Referência ao Technical Assessment | derived | false | 0 | scope, business-rules, nfrs, risks | bridge to CTO artifact: status + verdict + link, not content |

## Gate

- **Default threshold X:** 70
- **Blocking sections (blocks=true), 12:** exec-summary, context-problem, objectives, personas, scope, business-rules, user-stories, nfrs, edge-cases, metrics, release-criteria, risks
- The gate (`freezeReady`) cannot clear until every blocking section reaches its
  `min-confidence` or carries an honest disposition.

## Elevated thresholds (above default X=70)

- context-problem · 80
- scope · 75
- business-rules · 80
- user-stories · 80

## Derived sections and their inputs

- **inherited-readiness** (non-blocking) ← exec-summary, context-problem, objectives, personas, scope, metrics, release-criteria, risks. Signals confidence through its own surfacing of inherited score, open assumptions, Discovery unknowns, and delegated requirements rather than a confidence line.
- **tech-assessment-ref** (non-blocking) ← scope, business-rules, nfrs, risks. Bridge to the CTO's Technical Assessment (status/verdict/link only). If escalation is requested, freezes only with Disposition=deferred (TA pending, outside this tool) or Status=signed when the TA exists.

## Notes

- Fresh session: no prior contract.lock.md existed. Derived from scratch; no restart delta.
- This template adds an `Origin` field (inherited | ai_drafted | po_authored) to the
  confidence line on capture sections, per personas/02-po.md.
- The RP carries no CTO-authored sections; technical evaluation lives in the
  referenced Technical Assessment (tech-assessment-ref).

<!-- END OF DOCUMENT -->
