# Relatório de Prontidão — PokerPlan
<!-- rev: 1 · updated: 2026-06-03 -->

> Dashboard de trabalho — visão em tempo real da sessão. Distinto do cabeçalho do ledger (uma linha) e do manifesto final (índice de encerramento). Atualizar incrementalmente; nunca reescrever por completo.

---

## Manchete

| Campo | Valor |
|---|---|
| **Score de prontidão** | 63 % |
| **Estado do portão** | **ABERTO** (gate cleared) |
| **Data** | 2026-06-03 |
| **Decisão de triagem (draft)** | Discovery — validar aderência problema-mercado |
| **Confirmação humana** | Pendente — owner não assinado |

> Todos os quatro campos bloqueantes estão acima do limiar. O portão está ABERTO para avanço. O score de 63 % reflete honestamente que urgência não foi capturada (conf 0, não-bloqueante) e que impacto é uma estimativa/premissa, não dado medido. Discovery não é sinal de fragilidade — é o próximo passo correto antes de comprometer capacidade em um mercado ainda não validado.

---

## Mapa de seções

_Ordenado: bloqueantes primeiro (por confiança crescente), depois não-bloqueantes (por confiança crescente)._

| id | Seção | Bloqueante? | Confiança atual | Limiar | Status | O que elevaria a confiança |
|---|---|---|---|---|---|---|
| `impact` | Impacto de negócio | **Sim** | 70 (assumption) | 70 | Portão cleared — premissa | Medir desperdício real em entrevistas de Discovery (Q1/Q3); resolver inconsistência aritmética; obter dados de willingness-to-pay |
| `reach` | Quem é impactado | **Sim** | 78 | 70 | Answered | Dimensionar TAM (quantas orgs, quantos squads no mercado endereçável) — item de Discovery |
| `problem` | Problema (a dor) | **Sim** | 84 | 80 | Answered | Quantificar a dor em horas/sessão e número de sessões (pertence a `impact`, não reabre `problem`) |
| `originator` | Originador e contexto | **Sim** | 85 | 70 | Answered | Nomear o sponsor individual se necessário para handoff — não bloqueia |
| `urgency` | Urgência — por que agora | Não | 0 | 70 | Open (não-bloqueante) | Perguntar ao Submitter: há prazo, competidor chegando, evento de mercado ou custo crescente sem solução? |
| `constraints` | Restrições | Não | 80 | 70 | Answered (inferred) | Confirmar com Submitter quais RNs são inegociáveis vs. configuráveis; especialmente "sem autenticação" (só MVP V1?) |
| `priority` | Prioridade declarada | Não | 40 | 0 | Answered (inferred) | Confirmar com Submitter se há prioridade relativa a outros projetos — o atual é priorização de escopo, não de portfólio |
| `assumptions` | Premissas | Não | 35 | 0 | Parked (assumption) | Sign-off do Submitter nas premissas (a)–(e); Discovery para validar (f)–(h) |
| `meta` | Metadata | Não | — | 0 | Preenchida | — |
| `revisions` | Histórico de revisões | Não | — | 0 | Preenchida | — |
| `readiness` | Prontidão recebida | Não | — | 0 | Derivada | Recomputada automaticamente |
| `triage` | Decisão de triagem | Não | — | 0 | Draft (pending sign-off) | Confirmação do owner humano |
| `cto_escalation` | Escalada arquitetural | Não | — | 0 | Draft (No) | Confirmação do owner |
| `discovery` | Brief de Discovery | Não | — | 0 | Preenchida (5 itens) | Execução pelo Submitter / time de produto |
| `handoff` | Handoff | Não | — | 0 | Preenchida | Ação do owner: confirmar triage e abrir Discovery |

---

## O que foi respondido e como

### Portão liberado — campos bloqueantes

**`problem` — conf 84 / limiar 80 — CLEARED**
Respondido diretamente pelo Submitter (Q006 + Q007). Dor descrita com sintomas observáveis, sem prescrever solução: falta de estrutura e rastreabilidade nas sessões de Planning Poker, fragmentação entre ferramentas, ausência de histórico, repetição de discussões não documentadas, influência involuntária de votos. Contraste com workaround atual (Q007) confirma e reforça a dor. Atende o rubric integralmente.

**`originator` — conf 85 / limiar 70 — CLEARED**
Respondido via Q011 (Submitter direct). Origem coletiva e bottom-up: times de produto, engenharia e gestão que vivem o processo de estimativa; dor observada de forma recorrente em sessões de refinamento e planejamento; formalizada como aposta de produto comercial (SaaS). Sponsor individual não nomeado — coerente com a origem bottom-up, não é lacuna. Supersede assumption conf 60 registrada em Q008 Rev 1.

**`reach` — conf 78 / limiar 70 — CLEARED**
Respondido via Q008 + Q010 (Submitter direct). Personas internas identificadas: Desenvolvedores, Product Owners, Scrum Masters, Tech Leads, Gestores de produto/engenharia. Segmentos de mercado confirmados: empresas de tecnologia, consultorias de software, fábricas de software, times de produto, organizações Scrum/ágil. Sem dimensionamento de TAM — quantificação de mercado é item de Discovery, não gap de captura. Supersede Q002 (inferred conf 45).

**`impact` — conf 70 / limiar 70 — CLEARED (como premissa honesta)**
Respondido via Q009 + Q010 (Submitter direct). Duas camadas: (A) eficiência operacional modelada — squad de 8 pessoas, ~4 sessões/mês, 32 h-h/mês, ganho estimado por redução de ineficiência; (B) oportunidade comercial SaaS explicitamente não validada. Confiança 70 como premissa/estimativa — libera o portão honestamente. Inconsistência aritmética identificada (ver seção de itens parqueados). Supersede Q003 (inferred conf 30).

---

## Itens deliberadamente parqueados

Os itens abaixo foram conscientemente estacionados — não são lacunas de captura. Cada um tem owner ou time-box definidos.

### 1. Impacto — inconsistência aritmética no modelo de eficiência

**O que é:** O Submitter citou "8–11 h-h/ano por squad" como ganho com redução de ineficiência. O modelo de base (15–20 min × ~48 sessões/ano × 8 pessoas) produz ~96–128 h-h/ano — uma discrepância de ~10x.

**Por que foi parqueado:** A inconsistência não bloqueia o portão (impacto está conf 70, acima do limiar 70 como assumption). O número exato importa para materiais de triagem e validação comercial, não para a decisão de triage em si.

**Owner:** Submitter.

**Time-box:** Resolver no início da Discovery (item 3 do Discovery brief, 2026-06-03 → 2026-06-24). Perguntas a fazer: "Qual a base do cálculo de economia? São 15–20 min sobre o total da sessão ou sobre o tempo de setup/registro? É por sessão ou por sprint?"

**O que fecha:** Dados reais de frequência e duração de sessões coletados nas entrevistas de Discovery (Q1/Q3 do brief). Meta: número corrigido com fonte declarada, não estimativa do Submitter sem verificação.

---

### 2. Urgência — não declarada

**O que é:** Nenhuma janela, prazo, competidor chegando ou custo de espera foi declarado pelo Submitter. Conf 0, campo não preenchido.

**Por que foi parqueado:** `urgency` tem `blocks=false` — não bloqueia o portão nem a triagem. A ausência de urgência declarada não invalida a demanda; apenas enfraquece a prioridade relativa e contribui para o score de 63 % (em vez de um score maior se urgência fosse respondida).

**Owner:** Submitter.

**Time-box:** Pode ser respondida a qualquer momento antes do re-triage pós-Discovery. Se a Discovery revelar uma janela de mercado (competidor chegando, demanda reprimida crescendo, evento), urgência é reavaliada automaticamente (item 5 do Discovery brief).

**O que fecha:** Uma resposta direta do Submitter a: "Há um prazo, um competidor, um evento de mercado, ou um custo que cresce a cada mês sem solução?"

---

### 3. Dimensionamento de mercado — TAM não quantificado

**O que é:** Reach identificou personas e segmentos com clareza, mas não quantificou o mercado endereçável: quantos times no Brasil/global, quantas organizações, TAM/SAM/SOM. Conf 78 de reach reflete que personas e segmentos estão respondidos, não que o dimensionamento esteja feito.

**Por que foi parqueado:** Dimensionamento de TAM é validação comercial, não captura de intake. O rubric de `reach` exige personas e segmentos afetados — não projeção de mercado. Parqueado como item de Discovery para não inflar artificialmente a confiança de reach.

**Owner:** Submitter / time de produto (item 4 do Discovery brief).

**Time-box:** 1 semana paralela às entrevistas de Discovery (2026-06-03 → 2026-06-10, pesquisa desk). Fontes sugeridas: State of Agile (VersionOne/Digital.ai), dados de adoção de Scrum, relatórios de tamanho do mercado de ferramentas ágeis.

**O que fecha:** Estimativa de ordem de grandeza (não precisa ser exata nesta fase). Meta: "X mil organizações praticam Planning Poker regularmente no segmento Y" — suficiente para avaliar viabilidade do SaaS.

---

### 4. Monetização SaaS — premissa a validar

**O que é:** O modelo de monetização (SaaS por organização, planos por nº de usuários/equipes/funcionalidades) foi declarado pelo Submitter como "provável" — não testado com potenciais clientes. Willingness-to-pay é desconhecido. Premissas (f)–(h) em `assumptions`.

**Por que foi parqueado:** O próprio Submitter declarou que o objetivo inicial é "validar se existe aderência suficiente ao problema para justificar evoluir para produto comercial." Registrar a premissa honestamente e delegá-la à Discovery é o tratamento correto — não seria honesto qualificar como respondido algo que o Submitter explicitamente diz que ainda não foi validado.

**Owner:** Submitter / Discovery (item 2 do Discovery brief).

**Time-box:** Simultâneo às entrevistas de descoberta (2026-06-03 → 2026-06-24). Método: perguntas diretas nas entrevistas sobre ferramentas atuais, satisfação, e disposição para pagar; teste de conceito / landing page com proposta de valor.

**O que fecha:** Evidência qualitativa de que (a) a dor é real e sentida com intensidade suficiente para motivar troca de ferramenta, e (b) há disposição para pagar em uma faixa de preço viável para o modelo SaaS.

---

## Discovery como prontidão — o que já está pronto

O roteamento para Discovery não é sinal de fragilidade da captura. Os quatro campos bloqueantes estão todos acima do limiar — o intake cumpriu seu papel. A Discovery foi proposta porque é o próximo passo honesto dado o estágio do produto:

1. O problema está bem descrito e validado pelo Submitter (conf 84).
2. Reach está claro com personas e segmentos confirmados (conf 78).
3. Originator está resolvido com origem bottom-up documentada (conf 85).
4. Impacto tem um modelo de eficiência honestamente marcado como estimativa (conf 70).
5. O próprio Submitter declarou que o objetivo é "validar aderência ao problema antes de escalar para produto comercial."

**O Discovery brief está pronto** (5 itens, owners e time-boxes definidos, critérios de saída explícitos). Se os itens 1–3 do brief confirmarem aderência e willingness-to-pay, re-triage para **Product Ready é imediato** — sem nova rodada de intake completa. Todos os campos bloqueantes já estão acima do limiar e não precisam ser reabertos.

**Critérios de saída da Discovery (para re-triage):**
- (a) Pelo menos 5 entrevistas realizadas com personas do segmento-alvo.
- (b) Evidência qualitativa de que a dor é real e há disposição para pagar.
- (c) Modelo de impacto operacional corrigido com dados reais (inconsistência aritmética resolvida).
- (d) Premissas (f)–(h) revisadas com base nas entrevistas.

---

## Conflitos em aberto

Nenhum conflito de evidências aguardando o Reconciler. Todos os itens conflitantes do ledger foram resolvidos internamente:

- **Originator conf 60 (assumption, Q008 Rev 1) vs. conf 85 (answered, Q011 Rev 2):** Resolvido. Q011 supersede Q008 intermediário. Q008 mantido como trilha de auditoria.
- **Reach conf 45 (inferred, Q002) vs. conf 78 (answered, Q008/Q010):** Resolvido. Q008/Q010 supersede Q002. Q002 mantido como trilha de auditoria.
- **Impact conf 30 (inferred, Q003) vs. conf 70 (assumption, Q009/Q010):** Resolvido. Q009/Q010 supera Q003. Q003 mantido como trilha de auditoria. Inconsistência aritmética documentada e parqueada (ver seção acima) — não é conflito de evidências, é item a verificar com o Submitter.

---

<!-- END OF DOCUMENT -->
