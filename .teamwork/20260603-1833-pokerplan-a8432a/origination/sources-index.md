# Sources Index — PokerPlan

<!-- rev: 1 · updated: 2026-06-03 -->

## Summary

| # | id | file | type | origin | language | likely contents | status |
|---|-----|------|------|--------|----------|-----------------|--------|
| 1 | SRC-001 | `sources/pokerplan-spec.md` | Requirements / business-rules document | Submitter-pasted spec (no file attachment) | pt-BR | Full specification for PokerPlan, a virtual Planning Poker platform: roles, estimation scales, traditional flow, business rules RN-001–RN-010, conceptual data model, digital flow, post-reveal statistics, MVP scope tiers, recommended differentiators, and product objective | indexed |

---

## SRC-001 — Section Map

Use this map to locate evidence quickly when extracting requirements.

| Section heading (pt-BR) | Line range (approx.) | Key content |
|-------------------------|----------------------|-------------|
| **Visão Geral** | 1–6 | One-paragraph platform overview: remote collaborative estimation, preserves physical Planning Poker rules |
| **Conceitos Fundamentais / Objetivo** | 8–14 | Product objective: estimate effort, complexity, or relative size via secret voting and collaborative consensus |
| **Participantes** | 15–43 | Three roles — Host/Facilitador (create room, manage participants, start/reveal/close votes, set consensus), Participante (enter room, view tasks, vote, change vote before reveal), Observador (view only, cannot vote) |
| **Escalas de Estimativa** | 45–73 | Two scales: Fibonacci (0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, ?, ∞, coffee-break) and T-Shirt (PP, P, M, G, GG) |
| **Fluxo Tradicional** | 75–127 | Eight-step physical flow: task presentation → initial discussion → secret vote → simultaneous reveal → divergence discussion (hear lowest/highest) → new round (optional) → consensus (not necessarily a mean) → closure |
| **Regras de Negócio** | 129–170 | Ten rules: RN-001 votes secret until reveal; RN-002 participant may change vote while round open; RN-003 only host reveals; RN-004 optional auto-reveal when all voted; RN-005 only host closes round; RN-006 task may have multiple rounds; RN-007 full round history stored; RN-008 late joiners cannot vote retroactively; RN-009 host may cancel a round; RN-010 final estimate stored separately from individual votes |
| **Modelo Conceitual** | 172–253 | Five entities with suggested fields and status enums: Sala (CREATED/IN_PROGRESS/FINISHED), Participante (HOST/PARTICIPANT/OBSERVER), Tarefa (PENDING/VOTING/ESTIMATED), Rodada (OPEN/REVEALED/CLOSED), Voto |
| **Fluxo Digital** | 255–305 | Ten-step digital flow: room creation with shareable link → participants join by name only (no auth) → task registration (manual or integrations) → voting start → card selection → progress indicator (votes received count, not values) → simultaneous reveal → discussion → optional new round → host sets final estimate |
| **Estatísticas** | 307–319 | Post-reveal calculations: min, max, mean, median, mode, spread/deviation |
| **Funcionalidades do MVP** | 321–351 | Three tiers — MVP V1 (core session flow, no auth, history), MVP V1.1 (timer, auto-reveal, auto-stats, CSV export), MVP V2 (Jira/Linear integrations, permanent teams, org history, metrics dashboard, round comparison, anonymous vote comments) |
| **Diferenciais Recomendados** | 353–383 | Four differentiators: vote-level comment/justification, round-comparison visualization, system-suggested consensus (mean/mode/median), multi-format export (CSV, Excel, PDF) |
| **Objetivo do Produto** | 385–388 | Closing statement: fully digitalize traditional Planning Poker preserving all collaboration/secrecy/consensus rules while adding productivity, traceability, and estimation transparency features |

---

<!-- END OF DOCUMENT -->
