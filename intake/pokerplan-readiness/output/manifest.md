# Manifesto da Sessao — Readiness Package PokerPlan

| Campo | Valor |
|---|---|
| **Pacote** | RP-2026-001 — PokerPlan |
| **Intake vinculado** | INT-2026-001 |
| **Data** | 2026-06-03 |
| **Idioma de saida** | pt-BR |
| **Modo** | Fresh (sem contrato anterior) |
| **Nota de origem** | O intake INT-2026-001 foi triado como **Discovery** (nao "Product Ready"). O PO optou por prosseguir para o RP. Este RP e um rascunho honesto sobre base nao validada, congelado provisoriamente. O congelamento definitivo requer: (a) Discovery confirmar a aposta comercial e (b) Technical Assessment assinado pelo CTO. |

---

## 1. Artefatos produzidos

Nota: nenhum arquivo de traducao foi gerado. O idioma de saida (pt-BR) e igual ao idioma dos documentos-fonte; `output/humanized.md` e `output/enriched.md` sao variantes editoriais (legibilidade e enriquecimento visual), nao traducoes.

| Caminho (relativo a SESSION_DIR) | O que e | Idioma | Agente/autor |
|---|---|---|---|
| `contract.lock.md` | Contrato travado derivado do template; inventario de secoes, tipos, thresholds e gate | pt-BR | Template Analyst |
| `sources-index.md` | Indice de todas as fontes trazidas para a sessao; carry-forward das dispositions do intake | pt-BR | Source Indexer |
| `sources/intake-target-document.md` | Registro de intake canonico INT-2026-001 Rev 2 — fonte primaria | pt-BR | Intake pipeline |
| `sources/pokerplan-spec.md` | Especificacao original do Submitter — fluxos, regras de negocio, MVP V1/V1.1/V2 | pt-BR | Submitter |
| `sources/intake-humanized.md` | Re-render de leitura facil do intake (mesmos dados que a fonte primaria) | pt-BR | Intake pipeline |
| `sources/readiness-report.md` | Dashboard de prontidao computado a partir do intake (score 63 %, mapa de secoes, itens deliberadamente parkados) | pt-BR | Intake pipeline |
| `sources/glossary.md` | Glossario canonico do PokerPlan — 30 + termos normativos com definicoes e proibicoes | pt-BR | Intake pipeline |
| `sources/qa-log.md` | Copia de referencia do ledger de entrevista (versao trazida para sources/) | pt-BR | Source Indexer |
| `qa-log.md` | Ledger Q&A vivo da sessao — Rev 3; 29 entradas (6 respondidas, 23 parkadas/diferidas); auditoria de toda decisao do PO | pt-BR | Readiness pipeline (varios agentes) |
| `readiness-document.md` | Documento canonico do RP — Rev 5; 14 secoes + TechAssessmentRef; congelado provisoriamente | pt-BR | Readiness pipeline (varios agentes) |
| `output/humanized.md` | Variante humanizada do documento canonico — linguagem de leitura fluente, sem anotacoes de template | pt-BR | Humanizer |
| `output/enriched.md` | Variante enriquecida — adiciona painel de prontidao (Mermaid), painel de itens abertos e formatacao visual aprimorada | pt-BR | Enricher |
| `output/manifest.md` | **Este documento** — indice fechado da sessao; score final, gate, itens em aberto, proveniencia, proximo passo | pt-BR | Packager |

---

## 2. Prontidao

### Score e estado do portao

| Indicador | Valor |
|---|---|
| **Readiness score** | **78%** (handoff do intake: 63%) |
| **Estado do portao** | **CONGELAMENTO PROVISORIO** |
| **Secos bloqueantes (12)** | Todas resolvidas ou dispostas de forma honesta |
| **Threshold do template (X)** | 70 |
| **Hash do template** | `74cd7c34fc0d21a0e37ee6720a50418772f31f3fbaeddcc8696d833068ba30ef` |

### Resolucao das 12 secoes bloqueantes

| Secao (id) | Min-conf | Conf final | Origem | Disposicao |
|---|---|---|---|---|
| exec-summary | 70 | 75 | po_authored | assumption (Layer B nao validada — Discovery) |
| context-problem | 80 | 84 | po_authored | answered |
| objectives | 70 | 65 | po_authored | discovery (valores-alvo diferidos; deferred honesto, aceito pelo PO) |
| personas | 70 | 78 | po_authored | answered |
| scope | 75 | 90 | po_authored | decided (Excluido declarado pelo PO, Q017) |
| business-rules | 80 | 88 | po_authored | decided (A1–A7 resolvidas, Q018–Q022) |
| user-stories | 80 | 86 | po_authored | decided (ST-001–ST-011; A2 resolvida; Observer V1) |
| nfrs | 70 | 72 | po_authored | decided (latencia ~2s p95 firmada; mecanismos → TA) |
| edge-cases | 70 | 78 | po_authored | decided (EC-02/06/07 resolvidos; EC-02 mecanismo → TA) |
| metrics | 70 | 50 | po_authored | discovery (cifras suprimidas; diferido Discovery — deferred honesto, aceito pelo PO) |
| release-criteria | 70 | 80 | po_authored | decided (pass/fail aceito pelo PO, Q027) |
| risks | 70 | 78 | po_authored | decided (prob/impacto firmados, Q028) |

**Nota sobre objectives (conf 65 < min 70) e metrics (conf 50 < min 70):** ambas receberam disposicao `discovery` aceita pelo PO no confirm-loop (Q026). A disposicao e honesta, nao uma lacuna — o PO deliberadamente diferiu os valores-alvo mensuráveis para a Discovery. O portao nao foi derrubado por evasao; foi pela decisao informada de preservar a integridade dos dados ate a correcao do modelo aritmético (~10x). O portao permanece PROVISORIO e nao DEFINITIVO, conforme registrado.

### O que trava o congelamento definitivo

O portao de congelamento definitivo requer, cumulativamente:

1. **TechAssessmentRef.status = signed** — o Technical Assessment do CTO ainda nao existe (a skill `tech-assessment` nao esta disponivel).
2. **Discovery concluida** — validacao da aposta comercial, correcao da inconsistencia aritmetica (~10x), dimensionamento de TAM/SAM, teste de willingness-to-pay.

Enquanto qualquer dessas duas condicoes nao for satisfeita, o RP permanece congelado PROVISORIAMENTE.

---

## 3. AVISO CRITICO — Technical Assessment pendente (TA pendente)

> **tech-assessment-ref: deferred — TA pendente, fora do escopo atual da ferramenta.**
>
> Este aviso e OBRIGATORIO para qualquer handoff de PRD ou PM. O Technical Assessment NAO foi realizado. O congelamento e PROVISORIO. O PRD nao pode ser entregue ate que o TA esteja assinado.

### Gatilhos arquiteturais disparados (pelo readiness-escalation-flagger)

Dois clusters de gatilhos foram detectados e registrados no `readiness-document.md` (Secao TechAssessmentRef) e no `qa-log.md`:

**Gatilho 1 — Runtime / estado em tempo real**

Sincronizacao de estado entre multiplos participantes simultaneos, com alvo de latencia (~2 s p95), consistencia das transicoes de rodada (OPEN → REVEALED → CLOSED / CANCELLED) e reconexao sem voto fantasma ou duplicado (NFRs Performance/Reliability; EC-08; EC-11). Este e o maior risco tecnico em aberto do MVP V1.

**Gatilho 2 — Segurança / autenticacao / identidade**

(a) Sigilo do voto em transporte e no cliente (RN-001) — valores nao podem vazar por inspecao da rede ou do cliente antes da revelacao; durante a rodada OPEN apenas a contagem trafega.

(b) Identidade confiavel do Host SEM login (premissa b) — acoes exclusivas do Host (revelar/encerrar/cancelar: RN-003/005/009) e sucessao do Host em desconexao (EC-02, politica decidida pelo PO em Q023) dependem de um vinculo de identidade que o V1 nao autentica.

### Estado atual da referencia

| Campo | Valor |
|---|---|
| TechAssessmentRef.status | `requested` |
| TechAssessmentRef.verdict | — (pendente; populado quando status = signed) |
| TechAssessmentRef.disposition | `deferred` |
| TechAssessmentRef.link | — (skill `tech-assessment` ainda nao existe) |

### O que o TA deve responder (minimo obrigatorio)

1. **Viabilidade da sincronizacao de estado em tempo real** para participantes simultaneos, incluindo o modelo de concorrencia e a estrategia de reconexao.
2. **Garantia do sigilo do voto em transporte/cliente (RN-001)** — como impedir que valores sejam obtidos antes da revelacao por qualquer meio de inspecao.
3. **Vinculo de identidade do Host sem login** (RN-003/005/009 + EC-02) — mecanismo tecnico que permite ao Host original reassumir os direitos pelo mesmo link na reconexao, sem sistema de autenticacao.

Ate que o TA emita veredito sobre esses tres pontos e assine o documento, o PRD/PM handoff esta INCOMPLETO.

---

## 4. Itens em aberto (disposicoes pendentes)

Os itens abaixo foram carregados explicitamente do intake e do ledger Q&A. Nenhum foi "limpado" silenciosamente. Cada um tem dono e o que bloqueia.

### 4.1 Discovery — validacao da aposta comercial

| Item | Descricao | Dono | O que bloqueia |
|---|---|---|---|
| (g/h) Aderencia problema-mercado | Nao ha validacao formal de que o problema e suficientemente difundido para suportar um produto SaaS. Premissas g (sem validacao de mercado) e h (mercado endereçavel suficiente) sao ambas Discovery de risco ALTO/ALTO. | Discovery (entrevistas / testes de mercado) | Claims comerciais no exec-summary; Layer B da aposta SaaS; freeze definitivo |
| (f) Willingness-to-pay | O modelo de monetizacao (SaaS por organizacao) nao foi testado. Nao ha sinal de preco ou de disposicao a pagar. Risco: MEDIA probabilidade / ALTO impacto. | Discovery (teste de conceito / landing / perguntas de preco) | Projecoes de receita; validacao do modelo SaaS |
| (h) Dimensionamento de TAM/SAM | O mercado-alvo (equipes ageis em empresas de tecnologia, consultorias, fabricas de software) nao foi dimensionado. Sem TAM/SAM, a escala comercial do modelo SaaS e uma assuncao. | Discovery (pesquisa de mercado / bases publicas) | Claims de escala; prioridade de portfolio |
| Item 3 — Correcao da inconsistencia aritmetica (~10x) | O intake cita economia de "8–11 h-h/ano por squad"; o modelo derivado produz ~96–128 h-h/ano (discrepancia ~10x). **Nenhuma cifra de economia pode ser publicada em nenhum material ate a correcao.** Todas as cifras estao suprimidas. | Discovery + Submitter (correcao do calculo base) | Metricas (Secao 10); exec-summary Layer A; credibilidade do RP |
| Urgencia ausente | Nenhuma janela de mercado, prazo, competidor ou custo-de-esperar foi declarada no intake (id=urgency, conf 0). A ausencia foi registrada explicitamente. Nao inventar urgencia. | Discovery (item 5 — janela de entrada no mercado) | Priorizacao relativa no portfolio |

### 4.2 Submitter — confirmacao pendente

| Item | Descricao | Dono | O que bloqueia |
|---|---|---|---|
| RN-004 = V1.1 on-record | O PO confirmou RN-004 (auto reveal) como V1.1 no confirm-loop (Q018). A confirmacao do Submitter com o Submitter original ainda esta pendente — nao e bloqueante para o freeze provisorio, mas deve ser obtida antes do freeze definitivo e do handoff ao time de desenvolvimento. | Submitter | Roadmap V1.1 definitivo; finalizacao do backlog |

### 4.3 Technical Assessment — tres verditos obrigatorios

| Item | Descricao | Dono | O que bloqueia |
|---|---|---|---|
| (i) Viabilidade de sincronizacao de estado em tempo real | Definir modelo de concorrencia, estrategia de reconexao e garantia de consistencia de votos/rodadas para participantes simultaneos. | CTO (Technical Assessment) | NFR Performance/Reliability; EC-08; EC-11; estimativa de esforco; freeze definitivo |
| (ii) Sigilo do voto em transporte/cliente (RN-001) | Definir como valores de voto nao podem ser obtidos por inspecao de rede ou de cliente antes da revelacao. | CTO (Technical Assessment) | NFR Security/Confidentiality; RN-001; freeze definitivo |
| (iii) Identidade confiavel do Host sem login (RN-003/005/009 + EC-02) | Definir mecanismo tecnico que vincula a identidade do Host sem autenticacao, incluindo a reconexao (politica de produto decidida pelo PO em Q023 — o "como" tecnico e do CTO). | CTO (Technical Assessment) | NFR Security/Access-control; EC-02; freeze definitivo |

---

## 5. Proximos passos / Handoff

**O PRD e a soma: RP + Technical Assessment.** Este RP e a metade do PO; o Technical Assessment e a metade do CTO. Sem as duas metades, o PRD nao pode ser entregue.

### Sequencia recomendada

**Passo A — Executar a Discovery (paralelo ou imediato)**

Objetivo: validar a aposta comercial e corrigir a base de dados antes de qualquer compromisso de desenvolvimento.

- Conduzir 5–10 entrevistas com os segmentos-alvo (Discovery item 1: aderencia problema-mercado).
- Testar willingness-to-pay e modelo de monetizacao (Discovery item 2).
- Corrigir a inconsistencia aritmetica no modelo de eficiencia (Discovery item 3 — ~10x discrepancia).
- Dimensionar TAM/SAM (Discovery item 4).
- Investigar janela de entrada no mercado / urgencia (Discovery item 5).
- Time-box sugerido: 3 semanas (ate 2026-06-24, conforme brief de Discovery do intake).

Saida da Discovery: (a) premissas g/h/f validadas ou refutadas; (b) cifras de economia corrigidas; (c) TAM/SAM dimensionado; (d) urgencia avaliada; (e) decisao de re-triagem (Product Ready vs. arquivo).

**Passo B — Obter o Technical Assessment do CTO**

- Executar a skill `tech-assessment` (ainda nao disponivel) ou commissionar o TA diretamente ao CTO.
- O TA deve cobrir os tres verditos obrigatorios listados na Secao 3 acima.
- Quando o TA estiver assinado, atualizar `TechAssessmentRef.status = signed` e `TechAssessmentRef.verdict` no `readiness-document.md`.

**Passo C — Apertar o portao para congelamento definitivo**

Apos Discovery (Passo A) e TA assinado (Passo B):

- Revisar os scores de objectives e metrics com valores-alvo mensuráveis confirmados.
- Revisar o exec-summary com Layer B validada (ou honestamente archivada se Discovery refutar a aposta).
- Confirmar com o Submitter o posicionamento de RN-004 = V1.1 on-record.
- Apertar o portao: exigir `TechAssessmentRef.status = signed` antes do freeze definitivo.
- Emitir o PRD = RP (definitivo) + Technical Assessment.

---

## 6. Proveniencia

| Campo | Valor |
|---|---|
| **Template** | `target-template.readiness-package.md` |
| **Template version** | v1 |
| **Template hash** | `74cd7c34fc0d21a0e37ee6720a50418772f31f3fbaeddcc8696d833068ba30ef` |
| **Threshold padrao (X)** | 70 |
| **Thresholds elevados** | context-problem: 80; scope: 75; business-rules: 80; user-stories: 80 |
| **Data de geracao** | 2026-06-03 |
| **Sessao** | Fresh (nenhum `contract.lock.md` anterior existia) |
| **Revisoes do documento canonico** | Rev 5 (2026-06-03) |
| **Revisoes do ledger Q&A** | Rev 3 (2026-06-03) |
| **Entradas no ledger** | 29 total — 6 respondidas, 23 parkadas/diferidas, 0 abertas sem disposicao |

<!-- END OF DOCUMENT -->
