# Manifesto da Sessão — PokerPlan
<!-- rev: 1 · updated: 2026-06-03 -->

> Índice de encerramento da sessão de intake para a demanda **PokerPlan**.
> Data: 2026-06-03. Idioma de saída: pt-BR. Modo: fresh (nenhuma sessão anterior).
> Produzido pelo Packager como artefato final. Documento autossuficiente.

---

## 1. Artefatos produzidos

A tabela abaixo indexa todos os arquivos existentes na fase. Caminhos relativos à raiz da fase (`.teamwork/20260603-1833-pokerplan-a8432a/origination/`).

| Caminho (relativo à sessão) | O que é | Idioma | Autor (agente) |
|---|---|---|---|
| `contract.lock.md` | Contrato derivado do template `target-template.intake-record.md`: define seções, campos bloqueantes, thresholds de confiança e condições de derivação para esta sessão | pt-BR / EN (metadados) | Template Analyst |
| `sources-index.md` | Índice da única fonte primária (SRC-001), com mapa de seções e localização de evidências dentro do arquivo-fonte | pt-BR | File Extraction |
| `sources/pokerplan-spec.md` | Especificação fonte original colada pelo Submitter: papéis, escalas, fluxo tradicional, regras de negócio RN-001–RN-010, modelo conceitual, fluxo digital, estatísticas, escopo MVP V1/V1.1/V2, diferenciais recomendados, objetivo do produto | pt-BR | Submitter (fonte bruta) |
| `raw/pokerplan-spec.md` | Cópia bruta da especificação fonte (idêntica ao arquivo em `sources/`); preservada como trilha de auditoria da ingestão | pt-BR | File Extraction |
| `qa-log.md` | Ledger de perguntas e respostas da sessão: Rev 6, 11 questões (Q001–Q011), disposições, confiança e trilhas de auditoria para cada campo capturado | pt-BR | Interviewer / Doc Updater |
| `target-document.md` | Registro canônico de intake preenchido — Rev 2, INT-2026-001. Contém todas as seções do template: metadata, histórico de revisões, prontidão recebida, problema, originador, reach, impacto, urgência, prioridade, triagem (draft), escalada arquitetural, premissas, restrições, Discovery brief (5 itens) e handoff | pt-BR | Doc Updater |
| `glossary.md` | Glossário canônico com 34 termos do domínio PokerPlan: forma canônica, definição, sinônimos proibidos e notas de uso | pt-BR | Glossary Keeper |
| `readiness-report.md` | Relatório de prontidão — Rev 1: dashboard com score (63 %), estado do portão (ABERTO / cleared), mapa de seções com confiança por campo, itens deliberadamente parqueados com owners e time-boxes, conflitos resolvidos | pt-BR | Confidence Auditor |
| `output/humanized.md` | Variante humanizada do registro canônico: linguagem fluida, anotações técnicas de intake removidas, mantendo fidelidade integral ao conteúdo | pt-BR | Humanizer |
| `output/enriched.md` | Variante enriquecida do registro canônico: conteúdo editorial expandido (contexto adicional, análise de implicações), preservando a estrutura do documento base | pt-BR | Enricher |
| `output/manifest.md` | Este documento — índice de encerramento da sessão: artefatos, prontidão, itens em aberto, proveniência e próximo passo | pt-BR | Packager |

> **Nota sobre traduções:** nenhuma tradução foi produzida nesta sessão. O idioma de saída solicitado é pt-BR; `humanized.md` e `enriched.md` são variantes editoriais do documento canônico no mesmo idioma, não traduções.

---

## 2. Prontidão

| Campo | Valor |
|---|---|
| **Score de prontidão** | **63 %** |
| **Estado do portão** | **ABERTO** (gate cleared) |
| **Decisão de triagem (draft)** | **Discovery** — validar aderência problema-mercado |
| **Confirmação humana** | Pendente — owner não assinou |
| **Fórmula aplicada** | Média simples dos 5 campos de captura gradeados: (problem 84 + originator 85 + reach 78 + impact 70 + urgency 0) / 5 = 317 / 5 = 63 % |

### Campos bloqueantes — situação final

| id | Seção | Confiança final | Limiar | Situação |
|---|---|---|---|---|
| `problem` | Problema (a dor) | 84 | 80 | Cleared — acima do limiar |
| `originator` | Originador e contexto | 85 | 70 | Cleared — acima do limiar |
| `reach` | Quem é impactado | 78 | 70 | Cleared — acima do limiar |
| `impact` | Impacto de negócio | 70 | 70 | Cleared — no limiar (premissa honesta) |

Todos os quatro campos bloqueantes atendem ou superam seu `min-confidence`. O portão está ABERTO. O score de 63 % reflete honestamente que urgência não foi capturada (conf 0, não-bloqueante) e que impacto é estimativa/premissa, não dado medido. Discovery é o próximo passo correto, não sinal de fragilidade.

### Seções bloqueantes ainda em aberto

Nenhuma. Todos os campos com `blocks=true` foram resolvidos acima de seu limiar. O portão não possui seções bloqueantes remanescentes.

---

## 3. Itens em aberto (disposições pendentes)

Os itens abaixo foram conscientemente parqueados — não são gaps de captura. Cada um tem owner e time-box. Devem ser retomados na Discovery ou antes do re-triage.

### 3.1 Impacto — inconsistência aritmética no modelo de eficiência

| Campo | Valor |
|---|---|
| **Tipo** | Assumption (conf 70) + item a verificar |
| **Descrição** | O Submitter citou "8–11 h-h/ano por squad" como ganho com redução de ineficiência. O modelo de base (15–20 min × ~48 sessões/ano × 8 pessoas) produz ~96–128 h-h/ano — discrepância de ~10x. Origem: Q009 (Submitter direct). |
| **Por que parqueado** | Não bloqueia o portão (impacto conf 70 ≥ limiar). O número exato importa para materiais de triagem e validação comercial, não para a decisão de triage em si. |
| **Owner** | Submitter |
| **Time-box** | Início da Discovery — 2026-06-03 → 2026-06-24 (item 3 do Discovery brief) |
| **Critério de fechamento** | Dados reais de frequência e duração de sessões coletados nas entrevistas de Discovery; número corrigido com fonte declarada |

### 3.2 Urgência — não declarada

| Campo | Valor |
|---|---|
| **Tipo** | Campo `urgency` — conf 0, `blocks=false`, não-bloqueante |
| **Descrição** | Nenhuma janela, prazo, competidor ou custo de espera foi declarado pelo Submitter. Campo permanece aberto. Impacto: contribui para score 63 % em vez de valor maior. |
| **Por que parqueado** | `urgency` tem `blocks=false` — não impede o portão nem a triagem. Ausência de urgência não invalida a demanda; enfraquece a prioridade relativa. |
| **Owner** | Submitter |
| **Time-box** | Pode ser respondida a qualquer momento antes do re-triage pós-Discovery. Se a Discovery revelar janela de mercado, urgência é reavaliada automaticamente (item 5 do Discovery brief). |
| **Critério de fechamento** | Resposta direta do Submitter: "Há um prazo, um competidor, um evento de mercado, ou um custo que cresce a cada mês sem solução?" |

### 3.3 Dimensionamento de mercado — TAM não quantificado

| Campo | Valor |
|---|---|
| **Tipo** | Discovery — validação comercial/mercado |
| **Descrição** | Reach identificou personas e segmentos com clareza (conf 78), mas não quantificou o mercado endereçável: quantos times, quantas organizações, TAM/SAM/SOM. Dimensionamento de TAM é validação comercial, não captura de intake. |
| **Por que parqueado** | Rubric de `reach` exige personas e segmentos afetados — não projeção de mercado. Parqueado para não inflar artificialmente a confiança de reach. |
| **Owner** | Submitter / time de produto (item 4 do Discovery brief) |
| **Time-box** | 1 semana paralela às entrevistas de Discovery — 2026-06-03 → 2026-06-10 (pesquisa desk) |
| **Critério de fechamento** | Estimativa de ordem de grandeza: "X mil organizações praticam Planning Poker regularmente no segmento Y" — suficiente para avaliar viabilidade do SaaS |

### 3.4 Monetização SaaS — premissa a validar

| Campo | Valor |
|---|---|
| **Tipo** | Assumption (premissas f, g, h) + Discovery |
| **Descrição** | Modelo de monetização SaaS por organização declarado pelo Submitter como "provável" — não testado com potenciais clientes. Willingness-to-pay desconhecido. Sem validação formal de mercado, sem projeção de receita. |
| **Por que parqueado** | O próprio Submitter declarou que o objetivo inicial é "validar se existe aderência suficiente ao problema para justificar evoluir para produto comercial." Registrar a premissa honestamente e delegá-la à Discovery é o tratamento correto. |
| **Owner** | Submitter / Discovery (item 2 do Discovery brief) |
| **Time-box** | Simultâneo às entrevistas de descoberta — 2026-06-03 → 2026-06-24 |
| **Critério de fechamento** | Evidência qualitativa de: (a) a dor é real e sentida com intensidade suficiente para motivar troca de ferramenta; (b) há disposição para pagar em faixa viável para o modelo SaaS |

### 3.5 Premissas (a)–(h) — sign-off e validação pendentes

As premissas abaixo foram capturadas no campo `assumptions` do registro canônico (Q005 + Q010). As premissas (a)–(e) aguardam sign-off do Submitter; as premissas (f)–(h) aguardam validação via Discovery.

| # | Premissa | Tipo | Validador |
|---|---|---|---|
| (a) | Sessões são remotas e síncronas com participantes simultâneos conectados ao mesmo tempo | To validate | Submitter |
| (b) | Sem autenticação no MVP V1 — identificar-se por nome é suficiente para o caso de uso inicial | To validate | Submitter |
| (c) | As escalas relevantes são Fibonacci e T-Shirt (customizáveis); outras escalas são secundárias | Accepted (baixo risco) | Submitter (confirmar em build) |
| (d) | Integrações com Jira, Linear e similares ficam para V2 — MVP V1 não depende delas | Accepted | Submitter (confirmar escopo V2) |
| (e) | O público-alvo são equipes ágeis que já praticam Planning Poker — não há onboarding de método novo | To validate | Submitter |
| (f) | Monetização provável = SaaS por organização, com planos por nº de usuários, equipes ou funcionalidades avançadas | To validate | Submitter / Discovery |
| (g) | Não há validação formal de mercado nem projeção de receita — premissa de que há aderência suficiente ao problema a confirmar | To validate (risco alto) | Discovery (entrevistas / testes de mercado) |
| (h) | O problema é amplamente distribuído entre times ágeis (base de mercado suficientemente grande para sustentar um SaaS) | To validate | Discovery (market sizing) |

---

## 4. Proveniência

| Campo | Valor |
|---|---|
| **Template** | `target-template.intake-record.md` |
| **Template version** | `v1` |
| **Template hash** | `7d95916c27cef9200f18c5c754b84941efa1ec5267be61604833a3aa224194d9` |
| **Iniciativa** | `20260603-1833-pokerplan-a8432a` |
| **Fase** | `.teamwork/20260603-1833-pokerplan-a8432a/origination` |
| **Record ID** | INT-2026-001 |
| **Data de geração** | 2026-06-03 |
| **Modo da fase** | Fresh — nenhuma fase anterior, nenhum delta de restart |
| **Idioma de saída** | pt-BR |
| **Revisão do ledger na coleta** | Rev 6 |
| **Número de questões no ledger** | 11 (Q001–Q011) |
| **Número de termos no glossário** | 34 |

---

## 5. Próximo passo

A decisão de triagem draft é **Discovery**. A ação imediata é do owner humano:

1. **Confirmar ou ajustar o triage draft** no campo `triage` do registro canônico (`target-document.md`).
2. **Atribuir-se como triador** e registrar a data de triage em Metadata (campo "Triaged by" e "Date triaged").
3. **Abrir o Discovery brief** com o Submitter / time de produto e agendar o início das entrevistas de descoberta.

O Discovery brief está pronto com 5 itens, owners e time-boxes definidos, e critérios de saída explícitos (ver seção "Discovery brief" em `target-document.md`). Time-box total: 3 semanas (2026-06-03 → 2026-06-24).

**Se a Discovery confirmar aderência e willingness-to-pay:** re-triage para Product Ready é imediato — sem nova rodada de intake completa. Todos os campos bloqueantes já estão acima do limiar; a racionalização focará nas premissas técnicas (a)–(e) e nas premissas comerciais confirmadas.

**Se a Discovery revelar ausência de aderência:** registrar aprendizado, arquivar a demanda com evidência, e decidir entre versão reduzida (ferramenta interna) ou descarte.

Esta demanda não está em Discovery por gaps de captura (todos fechados) — está em Discovery porque é o próximo passo honesto antes de comprometer capacidade de desenvolvimento em um mercado ainda não validado.

---

<!-- END OF DOCUMENT -->
