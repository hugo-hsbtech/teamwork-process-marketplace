<!--
GOLDEN EXAMPLE · Initiative ROI Report — calibration exemplar
A self-contained, realistic filled report for the `pokerplan` initiative
(origination frozen @63, readiness frozen @78, owes a deferred TechAssessmentRef;
assessment + prd phases not yet run). Rendered in pt-BR (the initiative's language).
This shows the quality bar: every number sourced, value extracted from the docs and
labeled estimate, the missing phases honestly "not captured". Numbers are
illustrative.
-->

# ROI da Iniciativa — pokerplan · 20260603-1833-pokerplan-a8432a
<!-- rev: 1 · updated: 2026-06-05 -->

> Analytics ponta-a-ponta desta iniciativa: o que **custou** levar a demanda do
> sinal bruto rumo ao PRD (tokens, modelos, US$, tempo — medidos) e o **valor** que
> ela carrega (extraído dos documentos, grau estimativa). Custo é medido; valor é
> estimativa; o que não foi capturado é declarado.

## 1 · Cabeçalho

| Campo | Valor |
|---|---|
| **Iniciativa** | `20260603-1833-pokerplan-a8432a` · projeto `pokerplan` |
| **Status** | open |
| **Idioma** | pt-BR |
| **Fases alcançadas** | origination → readiness *(assessment owed · prd não iniciado)* |
| **Lead time** | 2026-06-03 18:33 → 2026-06-04 11:20 (16h 47m) [artifact] |
| **Custo total** | **US$ 1.84** [ledger] |
| **Tokens totais** | 1.97M (in 0.21M · out 0.06M · cache-read 1.70M) [ledger] |
| **Mix de modelos** | claude-opus-4-8: 100% tokens / 100% US$ [ledger] |
| **Readiness final** | 78 / 100 (readiness) [artifact] |

## 2 · Detalhamento por fase

| Fase | Parede | Tokens | US$ | Spawns | Rounds | Readiness | Resultado | Dispositions (real/assm/disc/def) |
|---|---|---|---|---|---|---|---|---|
| origination | 2h 41m | 1.05M | 0.97 | 14 | 4 | 63 | — | 70 / 18 / 6 / 6 |
| readiness | 1h 12m | 0.92M | 0.87 | 11 | 3 | 78 | triagem: **Product Ready** | 74 / 14 / 6 / 6 |
| assessment | — | — | — | — | — | — | — | **não capturado (fase não iniciada — TA deferred)** |
| prd | — | — | — | — | — | — | — | **não capturado (fase não iniciada)** |

## 3 · Direcionadores de custo

- **Top agentes por US$:** orchestrator — $0.71 — 39%; hsb-doc-updater — $0.34 —
  18%; hsb-question-strategist — $0.21 — 11% *(split por agente é best-effort;
  orchestrator vs subagente é exato)*. [ledger]
- **Top modelos por US$:** claude-opus-4-8 — $1.84 — 100%. [ledger]
- **Disciplina de cache:** cache-hit ratio 89%; **economia de cache** US$ 6.12 (vs.
  pagar os cache-reads à tarifa de input). [ledger]
- **Alavancagem de automação:** compute ativo 0h 22m ÷ parede 3h 53m = 0.09 — o
  restante foi latência humana/assíncrona. [ledger]

## 4 · Painel de ROI

| Composto | Valor | Fonte |
|---|---|---|
| **Custo-por-readiness** | US$ 0.0236 / ponto | [ledger]+[artifact] |
| **Throughput — por dólar** | 42.4 pts/US$ | [ledger]+[artifact] |
| **Throughput — por hora** | 213 pts/h (compute ativo) | [ledger]+[artifact] |
| **Throughput — por Mtok** | 39.6 pts/Mtok | [ledger]+[artifact] |
| **ROI ancorado em valor** | +63% · **estimativa** | valor [artifact] ÷ custo [ledger] |
| **Economia de gate** | — *(nenhum gate barrou a cadeia)* | — |

### Quebra do valor (extraído dos documentos · estimativa)

| Dimensão | Peso | Score | Justificativa → citação |
|---|---|---|---|
| Reach | 25 | 72 | times de produto que rodam planning poker recorrente → `readiness/readiness-document.md` §personas |
| Impacto / severidade | 30 | 80 | dispersão e retrabalho na estimativa apontados como dor central → `origination/output/humanized.md` §problema |
| Objetivos estratégicos | 20 | 65 | acelerar cadência de planning, reduzir reuniões → `readiness/readiness-document.md` §objetivos |
| Mensurabilidade | 15 | 55 | métricas de tempo-de-rodada sugeridas, ainda não quantificadas → `readiness/…` §métricas |
| Confiança-do-valor | 10 | 60 | parte do impacto repousa em `assumption`/`deferred` → desconto aplicado |
| **Score de valor** | — | **70** | grau estimativa |

## 5 · Itens abertos

- **Dívidas pendentes (`owes`):** `TechAssessmentRef → tech-assessment → deferred`
  ("TA pendente — fora do escopo atual da ferramenta; congelamento provisório").
- **Dispositions parked (risco carregado):** origination — 2 assumptions (modelo de
  votação, anonimato), 1 deferred (integração com tracker); readiness — 1 discovery
  (limites de concorrência), 1 deferred (a própria TA).
- **Não capturado:** fases `assessment` e `prd` ainda não rodaram — sem ledger nem
  artefatos; ROI ponta-a-ponta cobre apenas origination + readiness.

<!-- END OF DOCUMENT -->
