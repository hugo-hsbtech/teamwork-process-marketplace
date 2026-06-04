<!--
TARGET TEMPLATE · Intake Record (default)
This file is the contract. Each fillable section carries an annotation:
  <!- - intake: id=...; blocks=...; min-confidence=...; kind=... - ->
and a self-sufficient rubric. The Template Analyst derives contract.lock.md from
these. To use a different document type, copy this file, re-annotate, and pass it
as TEMPLATE. See references/contract-and-template.md.
Default confidence threshold (X) = 70. Raise per-section for high-stakes fields.
-->

# Intake Record: PokerPlan
<!-- rev: 2 · updated: 2026-06-03 -->

> O artefato formal de intake. Reúne a demanda capturada, registra a prontidão
> com que ela chegou e carrega um **rascunho de triagem** (decisão de
> roteamento) que está sempre marcado para aprovação humana. Este documento é
> autossuficiente.

## Metadata
<!-- intake: id=meta; blocks=false; min-confidence=0; kind=meta -->

| Field | Value |
|---|---|
| **Record ID** | INT-2026-001 |
| **Version** | v1 |
| **Originator (Submitter)** | Origem coletiva/bottom-up (times de produto, engenharia e gestão); formalizada como aposta de produto comercial (SaaS) |
| **Triaged by (owner)** | (AI draft; pending owner assignment) |
| **Date registered** | 2026-06-03 |
| **Date triaged** | (pending human confirmation) |
| **Status** | In triage |
| **Output language** | pt-BR |
| **Source** | Especificação colada pelo Submitter (sources/pokerplan-spec.md) |

## Revision history
<!-- intake: id=revisions; blocks=false; min-confidence=0; kind=meta -->

| Version | Date | Event | Summary |
|---|---|---|---|
| v1 | 2026-06-03 | Intake drafted | Registro criado a partir da especificação fonte e da sessão de perguntas com o Submitter (Q001 a Q008). Seções bloqueantes: problem e reach acima do limiar; originator parked (conf 60); impact abaixo do limiar (conf 30, open). |
| v2 | 2026-06-03 | Intake updated (Rev 2) | Impact atualizado com modelo de duas camadas (Q009 + Q010, conf 70, assumption + discovery flag). Originator atualizado para origem coletiva/bottom-up (Q011, conf 85, answered). Reach enriquecido com segmentos de mercado comercial (Q008/Q010, conf 78). Assumptions (f) a (h) adicionadas (Q005 + Q010). Readiness recomputado: score 63 %, gate CLEARED (os quatro bloqueantes ≥ limiar). Triage recomputado; Discovery brief atualizado. |

---

## Readiness received
<!-- intake: id=readiness; blocks=false; min-confidence=0; kind=derived; inputs=problem,reach,impact,originator,urgency -->

> Um retrato calculado a partir das seções capturadas. Não é recapturado aqui.

| Field | Value |
|---|---|
| **Readiness score** | 63 % |
| **Blocking requirements** | All resolved by honest disposition (gate): **Yes, CLEARED** |
| **Open dispositions** | 8 assumptions a validar (a) a (h) · 1 discovery flag (validação comercial/mercado em impact) · urgency ausente (não-bloqueante) |

> **Nota de cálculo (Rev 2):** a fórmula é a média simples dos 5 campos de captura gradeados = (problem + originator + reach + impact + urgency) / 5.
> - problem: 84 / min 80 · **acima** ✓
> - originator: 85 / min 70 · **acima** ✓ (atualizado via Q011, de conf 60 parked para conf 85 answered)
> - reach: 78 / min 70 · **acima** ✓ (atualizado via Q008/Q010, de conf 72 para conf 78)
> - impact: 70 / min 70 · **no limiar** ✓ (atualizado via Q009/Q010, de conf 30 inferred para conf 70 assumption; libera o portão honestamente)
> - urgency: 0 / min 70 · abaixo, mas `blocks=false`; não bloqueia o portão
>
> Score: (84 + 85 + 78 + 70 + 0) / 5 = 317 / 5 = **63 %**
>
> **Portão:** CLEARED. Os quatro campos bloqueantes (problem, originator, reach, impact) atendem ou superam seu `min-confidence`. Urgência permanece sem resposta (não-bloqueante); o impacto comercial/mercado é flag de discovery explícita, não gap de captura. DRAFT, pendente de confirmação humana.

---

## Consolidated demand

> Leitura da demanda em uma tela, com cada dimensão carregando a confiança que herdou.

### Problem (the pain, not the solution)
<!-- intake: id=problem; blocks=true; min-confidence=80; kind=capture -->
> Rubric: describe the existing pain with observable symptoms: what hurts, for
> whom, how it shows up today. If it names a solution ("build X"), it is NOT
> satisfied: reframe to the pain underneath.

A dor principal não é a votação em si, mas a **falta de estrutura e rastreabilidade no processo de estimativa de tarefas em equipes ágeis**. As sessões de Planning Poker acontecem de forma improvisada, com ferramentas que não foram projetadas para isso.

**Sintomas observáveis recorrentes:**
- Perda de tempo organizando a dinâmica da votação (operação manual em vez de facilitação).
- Falta de registro das estimativas: não há histórico consolidado das sessões.
- Dificuldade em acompanhar a evolução do consenso dentro de uma sessão e entre sessões.
- Ausência de histórico para entender por que uma tarefa recebeu certa estimativa. As equipes precisam repetir discussões porque a sessão anterior não ficou registrada.
- Votos influenciados involuntariamente: quando a votação não é realmente secreta, os participantes influenciam os demais antes da revelação.
- Fragmentação entre várias ferramentas (chamadas de vídeo, chats, planilhas, soluções de Planning Poker sem integração), o que gera retrabalho e perda de contexto.

**Workaround atual e o que ele não entrega:** o processo é conduzido com chamadas de vídeo, chats corporativos, planilhas para registrar resultados e soluções gratuitas de Planning Poker desconectadas do restante do processo. Essas abordagens resolvem apenas a votação pontual, não o fluxo completo. Falta histórico consolidado das sessões, registro das rodadas por tarefa, justificativas para divergências, exportação de resultados, organização das tarefas estimadas, integração com ferramentas de gestão de produto e visibilidade da evolução das estimativas ao longo do tempo.

**Síntese:** a estimativa, que deveria ser rápida e colaborativa, vira uma atividade operacionalmente desgastante, pouco rastreável e difícil de reproduzir. O motivo não é falta de método, e sim falta de uma ferramenta adequada para conduzi-lo.

`Confidence:` 84 · `Source:` Submitter direct (Q006 + Q007) · `Status:` answered · `Disposition:` answered · `Hint:` Dor descrita com sintomas observáveis e sem prescrever solução, o que atende o rubric. Ainda não quantificada (tempo perdido por sessão, número de sessões): a quantificação pertence a `impact` (Q003, open).

### Originator & context
<!-- intake: id=originator; blocks=true; min-confidence=70; kind=capture -->
> Rubric: who raised it and in what situation (e.g. "COO, Q2 planning"), and the
> channel it came through.

A iniciativa do PokerPlan tem **origem coletiva e bottom-up**: partiu dos próprios membros dos times de produto, engenharia e gestão que vivenciam o processo de estimativa de forma recorrente. Ao longo de sessões de refinamento e planejamento, esses participantes demonstraram insatisfação crescente com a condução do processo via ferramentas improvisadas ou soluções incompletas.

**Reclamações recorrentes que motivaram a iniciativa:**
- Falta de rastreabilidade das estimativas.
- Dificuldade de registrar decisões tomadas nas sessões.
- Ausência de histórico das rodadas de votação.
- Pouca integração com o fluxo de trabalho existente.

Dessas dores recorrentes surgiu, entre os próprios participantes, a discussão sobre a necessidade de uma ferramenta mais adequada para suportar o Planning Poker de forma estruturada. Esse reconhecimento coletivo do problema motivou conceber o PokerPlan, que depois foi **formalizado como aposta de produto comercial (SaaS)**, já que o mesmo problema é amplamente distribuído entre equipes de tecnologia ágil e não se restringe a um time ou empresa.

**Canal/situação:** concepção interna de produto, a partir de dor observada coletivamente. Não há um sponsor individual nomeado, o que é coerente com a origem bottom-up e não é uma lacuna. Pode ser confirmado se for necessário para o handoff.

`Confidence:` 85 · `Source:` Submitter direct (Q011, 2026-06-03) · `Status:` answered · `Disposition:` answered · `Hint:` Originador bem caracterizado: origem bottom-up (times de produto, engenharia e gestão), formalizada como aposta de produto comercial. Clears originator gate ≥ 70. Sponsor individual (pessoa) não nomeado, mas não bloqueia; pode ser confirmado se necessário para handoff. Supersede assumption conf 60 registrada anteriormente (Q008 intermediário, Rev 1).

### Who is impacted (reach)
<!-- intake: id=reach; blocks=true; min-confidence=70; kind=capture -->
> Rubric: the personas / segments / teams who feel the pain, each with *how* they
> are affected.

A dor é percebida principalmente por **equipes de desenvolvimento de software que usam métodos ágeis** e fazem estimativas de backlog regularmente. A demanda tem duas camadas: personas internas (usuários diretos) e segmentos de mercado comercial (organizações que comprariam o produto SaaS).

**Personas internas afetadas e como cada uma é impactada:**

| Persona | Como é afetada |
|---|---|
| **Desenvolvedores** | Participam das sessões de votação; sofrem com a falta de sigilo do voto, com a ausência de histórico e com o tempo operacional perdido. |
| **Product Owners (PO)** | Conduzem ou participam das sessões; perdem rastreabilidade das estimativas passadas e contexto para a priorização futura. |
| **Scrum Masters / Facilitadores** | Gerenciam a dinâmica da sessão; hoje fazem isso de forma manual e fragmentada, sem ferramenta dedicada. |
| **Tech Leads** | Participam de votações técnicas; precisam de histórico para justificar estimativas e comparar rodadas. |
| **Gestores de produto / Engenharia / Gestão** | Dependem das estimativas para o planejamento; ficam sem visibilidade da evolução, sem dados consolidados e sem integração com ferramentas de gestão. |

**Segmentos de mercado comercial (organizações-alvo do SaaS):**

| Segmento | Caracterização |
|---|---|
| **Empresas de tecnologia** | Squads internos de desenvolvimento com backlog regular; frequência mais alta de sessões de estimativa. |
| **Consultorias de software** | Múltiplos times, múltiplos clientes; precisam de rastreabilidade e histórico por projeto. |
| **Fábricas de software** | Alto volume de sessões; precisam padronizar o processo entre times. |
| **Times de produto (product-led companies)** | Estimativa frequente ligada a ciclos de produto; precisam de integração com ferramentas de gestão (Jira, Linear). |
| **Organizações Scrum/ágil** | Qualquer organização que adotou Scrum ou métodos ágeis com rituais de estimativa recorrentes. |

> **Nota de escopo:** personas e segmentos identificados e confirmados pelo Submitter (Q008 + Q010). **Sem dimensionamento de TAM**: quantos times, quantas organizações, número de orgs no mercado endereçável: nada disso foi quantificado. O dimensionamento de mercado (TAM) é item de discovery.

`Confidence:` 78 · `Source:` Submitter direct (Q008, personas 2026-06-03; segmentos de mercado via Q010, 2026-06-03) · `Status:` answered · `Disposition:` answered · `Hint:` Personas claras (Devs, PO, SM, Tech Lead, gestores) e segmentos de mercado claros (empresas tech, consultorias, fábricas de software, times de produto, organizações Scrum/ágil). SEM dimensionamento de TAM: quantos times, quantas organizações, nº de orgs no mercado endereçável; isso permanece não-quantificado e é item de discovery. Supersede Q002 (reach inferred conf 45, mantido como trilha de auditoria).

### Business impact
<!-- intake: id=impact; blocks=true; min-confidence=70; kind=capture -->
> Rubric: value across the applicable dimensions (revenue, retention, operational,
> competitive, compliance), quantified when possible. Estimates are fine if
> marked low-confidence with a hint on what would firm them up.

O impacto de negócio tem **duas camadas distintas**, com graus diferentes de validação.

---

### Camada A · Eficiência operacional por cliente (modelo estimado)

Baseado em uma aproximação do Submitter para equipes ágeis tradicionais (Q009):

**Modelo de horas-homem:**

| Variável | Valor assumido |
|---|---|
| Tamanho do time | 8 pessoas |
| Duração da sessão | ~1 h |
| Frequência | ~4 sessões/mês por time |
| Horas-homem por sessão | 8 h-h |
| Horas-homem/mês por time | 32 h-h/mês |
| Org com 10 squads | ~320 h-h/mês em estimativa |

O problema não é a existência dessas horas (estimar é necessário), e sim o **desperdício por falta de estrutura**: ausência de histórico, repetição de discussões não documentadas, dificuldade de registrar decisões e fragmentação de ferramentas.

**Ganho estimado com redução de ineficiência:**
- Reduzindo 15 a 20 min de ineficiência por sessão, um squad economizaria horas-homem/ano por time (valor exato a confirmar; ver inconsistência aritmética abaixo).
- Em orgs com dezenas de squads, o ganho acumulado é significativo.

**Benefício adicional (menos visível, mais relevante):** melhoria da **qualidade e previsibilidade das estimativas**. Com decisões registradas e divergências rastreáveis, o time evolui o processo e reduz desalinhamentos. Visão do produto: PokerPlan como ferramenta de **governança e rastreabilidade** do processo de estimativa, não apenas de votação.

> **Inconsistência aritmética a validar:** 15 a 20 min × ~48 sessões/ano × 8 pessoas = ~96 a 128 h-h/ano por squad. O Submitter citou "8 a 11 h-h/ano", e há uma discrepância (a base do cálculo de economia precisa ser confirmada antes de usar o número em materiais de triagem). Esta inconsistência não bloqueia o portão, mas deve ser resolvida na Discovery.

---

### Camada B · Oportunidade comercial (produto SaaS) · NÃO VALIDADA

O PokerPlan está sendo concebido como **produto comercial SaaS** (Q010). O problema é amplamente distribuído entre equipes de tecnologia ágil e não se restringe a um time ou empresa.

**Mercado potencial:**
- Equipes de desenvolvimento de software, empresas de tecnologia, consultorias de software, fábricas de software, times de produto, organizações Scrum/ágil.

**Monetização provável:**
- SaaS por organização, com planos por nº de usuários, equipes ou funcionalidades avançadas.

**Estado atual da validação comercial:**
- **Sem validação formal de mercado.**
- **Sem projeções de receita.**
- **Sem TAM quantificado.**
- O objetivo declarado pelo Submitter é: "validar se existe aderência suficiente ao problema para justificar evoluir para produto comercial."

> Esta camada é uma **premissa de mercado a validar**, não uma projeção. Nenhuma projeção de receita nem validação de aderência foi feita. É item explícito de Discovery.

`Confidence:` 70 · `Source:` Submitter direct (Q009 + Q010, 2026-06-03) · `Status:` parked · `Disposition:` assumption (eficiência: modelo estimado, conf 70, libera portão honestamente) + discovery flag (validação comercial/mercado: explicitamente não-validada) · `Hint:` Modelo de eficiência é estimativa, não medição real; libera o portão como assumption conf 70. INCONSISTÊNCIA ARITMÉTICA: 15 a 20 min × ~48 sessões/ano × 8 pessoas ≈ 96 a 128 h-h/ano por squad (vs. "8 a 11 h-h/ano" citado pelo Submitter); confirmar base do cálculo. Validação comercial (TAM, aderência ao problema, projeção de receita, willingness-to-pay) é item de Discovery, não gap de captura.

### Urgency · why now
<!-- intake: id=urgency; blocks=false; min-confidence=70; kind=capture -->
> Rubric: why now and the cost of waiting: a window, a deadline, a compounding
> cost.

Sem resposta capturada. O Submitter não declarou nenhuma janela, prazo, competidor chegando ou custo de espera.

`Confidence:` 0 · `Source:` (vazio) · `Status:` open · `Disposition:` (vazio) · `Hint:` "Por que agora" não foi declarado. Perguntar ao Submitter: há um prazo, um competidor, um evento de mercado, ou um custo que cresce a cada mês sem solução? Sem urgência declarada, o triage tende a Backlog ou Discovery; isso não invalida a demanda, mas enfraquece a prioridade.

### Declared priority
<!-- intake: id=priority; blocks=false; min-confidence=0; kind=capture -->
> Rubric: the Submitter's priority call **and** the reason behind it (why this
> level, not just the label).

**Level:** Não declarado pelo Submitter. **Reason:** o Submitter não declarou prioridade relativa. O documento sugere um escalonamento de escopo implícito:

- **MVP V1** (maior prioridade implícita): fluxo essencial. Criar sala, votar com sigilo, revelar, registrar consenso, histórico de rodadas, entrada sem autenticação (só nome).
- **V1.1**: funcionalidades incrementais (não detalhadas na especificação).
- **V2**: integrações externas (Jira, Linear e similares).

> Atenção: isso é **priorização de escopo** (o que entra em qual versão), não nível de prioridade de negócio em relação a outros projetos da organização. Confirmar com o Submitter se há prioridade relativa a declarar.

---

## Triage · routing decision
<!-- intake: id=triage; blocks=false; min-confidence=0; kind=derived; inputs=problem,reach,impact,urgency,assumptions -->

> ⚠️ **TRIAGE DRAFT · AI-generated from the capture, pending owner confirmation.**
> The verdicts and routing below are a *proposal* grounded in captured evidence,
> not a final call. A human owner must review, adjust, and sign off. Until then
> `Status` = *In triage* and this section's disposition is `low_confidence`.
> See the template's companion guide for how to draft this responsibly.

### Criteria assessed

| # | Criterion | Verdict | Rationale | Basis / source |
|---|---|---|---|---|
| 1 | A real problem (not an isolated symptom)? | **Yes** | Dor descrita com múltiplos sintomas observáveis (falta de sigilo real, ausência de histórico, fragmentação de ferramentas, retrabalho, repetição de discussões). Não é desejo de feature: é dor existente no processo atual, descrita pelo Submitter com experiência direta. | Q006 + Q007, Submitter direct, conf 84 |
| 2 | Recurring / has volume? | **Yes (assumed)** | O Submitter descreve recorrência observada coletivamente em times de produto, engenharia e gestão (Q011). Origem bottom-up: múltiplos times reclamaram. Mas sem dimensionamento (quantos times, frequência por semana): recorrência plausível, porém não quantificada. | Q008 conf 78; Q011 conf 85; premissas (e) e (h) |
| 3 | Fits the product vision? | **Yes (assumed)** | Produto comercial SaaS para equipes ágeis; Planning Poker é prática estabelecida no mercado; visão explicitada pelo Submitter (Q010). Alinhamento assumido, sem visão de produto formalizada acessível para verificação independente. | Q010, Submitter direct, conf 80; file:sources/pokerplan-spec.md |
| 4 | Technical & business impact? | **Medium (modeled, unvalidated commercially)** | Eficiência operacional modelada (Q009): 32 h-h/mês por squad, ganho por redução de ineficiência: assumption conf 70, libera o portão honestamente. Oportunidade comercial (Q010): produto SaaS com mercado endereçável declarado. Porém: (a) há inconsistência aritmética no modelo de economia a resolver; (b) validação de aderência problema-mercado, TAM e willingness-to-pay estão explicitamente ausentes, e isso é item de Discovery. | Q009 conf 70 (assumption); Q010 conf 80; premissas (f) a (h) |
| 5 | Do urgency & impact justify *now*? | **Partial (impact modeled; urgency absent)** | Impacto operacional modelado a conf 70, o que justifica investigação. Oportunidade comercial real, mas não validada. Urgência: sem janela, prazo, competidor ou custo de espera declarados (conf 0, não-bloqueante). O próprio Submitter declarou que o objetivo é "validar aderência ao problema antes de evoluir para produto comercial", o que alinha com Discovery, não com Product Ready imediato. | Urgency conf 0; impact conf 70 assumption; Q010 Submitter direct |

### Decision

| Field | Value |
|---|---|
| **Decision** | **Discovery** (DRAFT) |
| **Rationale** | O problema é real e bem descrito (conf 84), o reach é claro, com personas e segmentos de mercado identificados (conf 78), o originator está resolvido com origem bottom-up coletiva (conf 85), e o impacto operacional está modelado como assumption (conf 70, libera o portão honestamente). Os quatro campos bloqueantes estão acima do limiar. Ainda assim, o roteamento correto é **Discovery**, não por gaps de captura, mas pela natureza do estágio do produto: (1) o mercado comercial está explicitamente NÃO validado (sem TAM, sem willingness-to-pay, sem projeção de receita; premissas f, g, h); (2) o modelo de eficiência contém inconsistência aritmética a resolver; (3) o próprio Submitter declarou que o objetivo inicial é "validar aderência ao problema" antes de escalar para produto comercial. Discovery aqui não é sinal de fragilidade da demanda: é o passo honesto para validar a aderência problema-mercado antes de comprometer capacidade de desenvolvimento. Se a Discovery confirmar aderência e resolver as premissas comerciais, o re-triage para Product Ready é imediato. |
| **Reversible?** | Yes |
| **Originator notified** | Pending (human action; date TBD) |

---

## Architectural escalation
<!-- intake: id=cto_escalation; blocks=false; min-confidence=0; kind=derived; inputs=impact,constraints,assumptions -->
> Rubric: whether the demand needs CTO/architectural review before scope can
> freeze (new infra, payments, multi-tenancy, security, AI/runtime, integrations
> with unknowns), with a one-line reason. A flagged draft signal pending owner
> confirmation, not a final call.

**Needed:** No (DRAFT). O MVP V1 é uma extensão de UI/estado com regras de negócio bem definidas (RN-001 a RN-010), sem pagamentos, sem multi-tenancy complexo, sem AI/runtime, sem integrações externas (as integrações Jira/Linear ficam para V2). A premissa de "entrada sem autenticação" (MVP V1) simplifica a superfície de segurança. As suposições técnicas remanescentes (estado em tempo real para múltiplos participantes simultâneos, premissa a) são de viabilidade e pertencem à racionalização pelo Tech Lead, não a uma escalada arquitetural antes do congelamento de escopo. Pendente de confirmação do owner.

---

## Assumptions
<!-- intake: id=assumptions; blocks=false; min-confidence=0; kind=capture -->

> Conditions assumed true at capture. Each carries a proposed verdict (draft) and
> who validates it. If one proves false, the demand is re-triaged.

| Assumption | Verdict (draft) | Validate with |
|---|---|---|
| (a) Sessões são remotas e síncronas, com participantes conectados ao mesmo tempo | To validate: material para a arquitetura de estado em tempo real; se for async, o modelo muda | Submitter |
| (b) Sem autenticação no MVP V1; identificar-se por nome basta para o caso de uso inicial | To validate: pode ser preferência de design, não restrição permanente; confirmar se há requisito de identidade futura | Submitter |
| (c) As escalas relevantes são Fibonacci e T-Shirt (customizáveis); outras escalas são secundárias | Accepted: risco baixo; padrão da indústria para Planning Poker; confirmável em build | Submitter |
| (d) Integrações com Jira, Linear e similares ficam para V2; o MVP V1 não depende delas | Accepted: declarado explicitamente na especificação como V2; baixo risco de reversão | Submitter (confirmar escopo V2) |
| (e) O público-alvo são equipes ágeis que já praticam Planning Poker; não há onboarding de método novo | To validate: impacta posicionamento e copy do produto; se for público novo, o onboarding muda | Submitter |
| (f) Monetização provável = SaaS por organização, com planos por nº de usuários, equipes ou funcionalidades avançadas | To validate: modelo de monetização declarado pelo Submitter, mas não testado com potenciais clientes; willingness-to-pay desconhecido | Submitter / Discovery |
| (g) NÃO há validação formal de mercado nem projeção de receita; premissa de que há aderência suficiente ao problema, a confirmar | To validate: premissa central para a viabilidade comercial; risco alto se a aderência for menor do que o esperado | Discovery (entrevistas / testes de mercado) |
| (h) O problema é amplamente distribuído entre times ágeis (base de mercado grande o suficiente para sustentar um SaaS) | To validate: premissa de mercado; distribuição qualitativa observada pelo Submitter, mas sem dados de TAM/SAM/SOM | Discovery (market sizing) |

---

## Constraints
<!-- intake: id=constraints; blocks=false; min-confidence=70; kind=capture -->

> Conditions that limit the solution space, to respect regardless of what is built.

| Constraint | Type | Note |
|---|---|---|
| RN-001: Sigilo do voto (votação secreta) até a revelação; o progresso exibe apenas a contagem de votos, não os valores | Technical / Scope | Regra de negócio central do Planning Poker; violá-la destrói o propósito do método |
| RN-002: Voto alterável apenas com a rodada aberta; sem voto retroativo após o encerramento | Technical / Scope | Garante a integridade da rodada |
| RN-003: Controle exclusivo do Host para revelar votos | Scope | O Host/Facilitador é o único autorizado a revelar |
| RN-005: Controle exclusivo do Host para encerrar rodadas | Scope | Mesmo princípio: controle de fluxo da sessão |
| RN-006: Múltiplas rodadas por tarefa permitidas | Scope | Suporta a re-votação após discussão |
| RN-007: Histórico completo de todas as rodadas | Technical / Scope | A rastreabilidade é um objetivo central do produto |
| RN-008: Sem voto retroativo após o encerramento da rodada | Technical / Scope | Complementa a RN-002 |
| RN-009: Controle exclusivo do Host para cancelar rodadas | Scope | Consistência do controle do Facilitador |
| RN-010: Estimativa final registrada separada dos votos individuais; o consenso não precisa ser a média | Scope | Facilita o registro do valor acordado pelo grupo |
| Entrada sem autenticação (MVP V1): participantes identificados apenas por nome | Technical / Scope | Simplifica o onboarding; confirmar se é restrição permanente ou só do MVP |
| Preservar as regras do Planning Poker físico | Scope | O produto é uma versão digital fiel do método existente |

`Confidence:` 80 · `Source:` file:sources/pokerplan-spec.md §"Regras de Negócio" RN-001 a RN-010, §"Fluxo Digital", §"Objetivo do Produto" (Q001) · `Status:` answered · `Disposition:` inferred · `Hint:` Confirmar com o Submitter quais são restrições rígidas vs. preferências de design, especialmente "sem autenticação" (pode ser só MVP V1, não permanente) e quais RNs são inegociáveis vs. configuráveis.

---

## Discovery brief
<!-- intake: id=discovery; blocks=false; min-confidence=0; kind=derived; inputs=triage; condition=triage.decision==Discovery -->

> Preenchido porque o triage draft propõe **Discovery**. O foco é validar a aderência problema-mercado e resolver as premissas comerciais declaradas pelo Submitter, não coletar mais dados de captura (os campos bloqueantes estão todos acima do limiar). Pendente de confirmação do owner antes de abrir formalmente.
>
> **Objetivo central:** confirmar se existe aderência suficiente ao problema no mercado endereçável para justificar evoluir o PokerPlan para produto comercial (SaaS). Este é o próprio objetivo declarado pelo Submitter (Q010).

| # | Unknown / hipótese a testar | Owner | Método sugerido | Time-box |
|---|---|---|---|---|
| 1 | **Aderência ao problema (problem-market fit):** o problema de falta de estrutura/rastreabilidade em estimativas ágeis é sentido com intensidade suficiente por potenciais clientes para que paguem por uma solução? | Submitter / produto | Entrevistas de descoberta com 5 a 10 pessoas representando os segmentos-alvo (tech, consultoria, fábricas de software); foco em dor, workarounds e disposição para mudar | 2 a 3 semanas |
| 2 | **Willingness-to-pay / validação de monetização:** potenciais clientes pagariam por uma ferramenta SaaS de Planning Poker com histórico, rastreabilidade e integração? Em qual faixa de preço? | Submitter / produto | Teste de conceito / landing page com proposta de valor + formulário de interesse; ou perguntas diretas nas entrevistas (Q1) | Simultâneo ao Q1; 2 a 3 semanas |
| 3 | **Validação e correção do modelo de impacto operacional:** resolver a inconsistência aritmética (15 a 20 min × ~48 sessões × 8 pessoas ≈ 96 a 128 h-h/ano vs. "8 a 11 h-h/ano" citado); obter dados reais de frequência e duração de sessões de potenciais usuários | Submitter / produto | Perguntas específicas nas entrevistas (Q1): "Quantas sessões por sprint/mês? Quanto dura cada uma? Qual parte você considera ineficiente?" | Simultâneo ao Q1 |
| 4 | **Dimensionamento de mercado (TAM/ordem de grandeza):** quantas organizações no Brasil/global praticam Planning Poker com frequência? Qual o segmento de maior penetração inicial? | Submitter / produto | Pesquisa desk (dados de adoção de Scrum/ágil, surveys do mercado: State of Agile, etc.); estimativa de ordem de grandeza (não precisa ser exata neste estágio) | 1 semana paralela |
| 5 | **Urgência / janela de entrada:** há uma janela de mercado, um evento ou um custo de espera que justifique agir agora vs. em 2 a 3 meses? (Competidores chegando? Demanda reprimida crescendo?) | Submitter | Análise dos competidores existentes; pergunta direta nas entrevistas sobre as ferramentas atuais e a satisfação com elas | Simultâneo ao Q1 |

**Owner sugerido:** Submitter / time de produto.

**Time-box total:** 3 semanas (2026-06-03 a 2026-06-24). Os itens 1 a 3 podem ser cobertos em uma rodada de 5 a 10 entrevistas de 30 a 45 min cada. O item 4 pode ser paralelo (pesquisa desk). Se os itens 1 a 3 confirmarem aderência e willingness-to-pay, o re-triage para **Product Ready** é imediato, sem nova rodada de intake completa.

**Critério de saída da Discovery (para re-triage):** (a) pelo menos 5 entrevistas realizadas com personas do segmento-alvo; (b) evidência qualitativa de que a dor é real e há disposição para pagar; (c) modelo de impacto operacional corrigido com dados reais; (d) premissas (f) a (h) de assumptions revisadas com base nas entrevistas.

---

## Handoff
<!-- intake: id=handoff; blocks=false; min-confidence=0; kind=derived; inputs=triage -->

- **Se Discovery (proposta atual, DRAFT):** executar o Discovery brief acima. Objetivo: validar a aderência problema-mercado e a willingness-to-pay e corrigir o modelo de impacto operacional. Time-box: 3 semanas. Ao fechar os critérios de saída definidos no brief, o re-triage para **Product Ready** é imediato, sem nova rodada de intake completa.
- **Se o owner re-triar para Product Ready após a Discovery:** prosseguir para a racionalização (Readiness Package). Todos os campos bloqueantes já estão acima do limiar; a racionalização focará nas premissas técnicas (a) a (e) e nas premissas comerciais confirmadas pela Discovery. A urgência pode ser reavaliada se a Discovery revelar uma janela de mercado.
- **Se o owner re-triar para Backlog:** registrar o rationale e notificar os originadores (times de produto, engenharia e gestão que levantaram a demanda coletivamente).
- **Se a Discovery revelar ausência de aderência:** registrar o aprendizado, arquivar a demanda com evidência, e decidir se ela volta como versão reduzida (ferramenta interna) ou é descartada.

> ⚠️ **Ação imediata:** o owner deve (1) confirmar ou ajustar o triage draft acima, (2) atribuir-se como triador e registrar a data de triage em Metadata, (3) abrir o Discovery brief com o Submitter/time de produto e agendar o início das entrevistas de descoberta. Esta demanda não está em Discovery por gaps de captura (todos fechados); está em Discovery por ser o próximo passo honesto antes de comprometer capacidade de desenvolvimento em um mercado ainda não validado.

<!-- END OF DOCUMENT -->
