<!--
TARGET TEMPLATE · Intake Record (default) — Act 1 of the PO journey (triage)
This file is the contract for the TRIAGE phase. Each fillable section carries an annotation:
  <!- - origination: id=SECTION-ID; blocks=BOOL; min-confidence=N; kind=TYPE - ->
and a self-sufficient rubric. The Template Analyst derives intake/contract.lock.md from
these (the same engine as the RP — the marker keyword stays `origination:`).
The triage criteria and the routing decision carry the PO decision model
(verdict | rationale | basis | source | reversible) per personas/02-po.md §4-6.
To use a different intake template, copy this file, re-annotate, and pass it as TEMPLATE.
See references/triage.md and references/contract-and-template.md (in origination-brainstorm).
Default confidence threshold (X) = 70. Raise per-section for high-stakes fields.
-->

# Intake Record — [Demand name]
<!-- rev: 0 · updated: AAAA-MM-DD -->

> O Intake Record é o **artefato do Ato 1 do PO: a triagem**. Ele recebe o
> origination-record (`Product Ready`-candidato), atribui o ID `INT-AAAA-NNN` e
> registra a **decisão de roteamento** (Product Ready / Discovery / Backlog /
> Rejeitar) com justificativa rastreável. Ele **não** reescreve a captura — a
> referencia e a consolida. O aprofundamento de produto é o Ato 2 (Readiness
> Package). Só `Product Ready` abre o Ato 2.

## Metadados
<!-- origination: id=meta; blocks=false; min-confidence=0; kind=meta -->

| Campo | Valor |
|---|---|
| **ID do Registro** | INT-AAAA-NNN |
| **Versão** | v1 |
| **Origination vinculado (origem)** | [caminho do origination-record] |
| **Registrado por (Submitter)** | [Nome] ([Vendas / CS / CEO / Marketing]) |
| **Triado por (PO)** | [Nome] (PO) |
| **Data de triagem** | AAAA-MM-DD |
| **Status** | Novo / Em triagem / Triado |
| **Readiness Package vinculado** | RP-AAAA-NNN (após Product Ready) |

## Histórico de Revisão
<!-- origination: id=revisions; blocks=false; min-confidence=0; kind=meta -->

| Versão | Data | Evento | Resumo |
|---|---|---|---|
| v1 | AAAA-MM-DD | Intake formalizado | [Breve descrição] |

---

## Prontidão recebida do origination
<!-- origination: id=inherited-readiness; blocks=false; min-confidence=0; kind=derived; inputs=demand-summary -->

> Snapshot herdado do origination-record no handoff. O PO não recalcula a captura —
> registra o que recebeu e o que segue *soft*.

| Campo | Valor |
|---|---|
| **Readiness Score no handoff** | __ % |
| **Requisitos bloqueantes** | Todos resolvidos por disposição honesta (`gateReady`) — Sim / Não |
| **Dispositions em aberto** | __ premissas a validar · __ discovery · __ delegados |

---

## Demanda consolidada
<!-- origination: id=demand-summary; blocks=true; min-confidence=70; kind=capture -->

> Resumo de uma tela, validado pelo PO contra o origination-record (não é
> re-digitação — é a leitura do PO). Cada dimensão herda a confiança da captura.
> ⚠️ Problema = a dor, não a solução.

| Dimensão | Síntese | Confiança herdada |
|---|---|---|
| **Problema** (a dor, não a solução) | [Síntese] | __ |
| **Alcance** (quem é impactado) | [Personas/segmentos] | __ |
| **Impacto de negócio** | [Quantificado quando possível] | __ |
| **Urgência** (por que agora) | [Janela + custo de esperar] | __ |
| **Prioridade declarada** | Crítico / Alto / Médio / Baixo | — |

`Confidence: __ · Origin: inherited · Source: __ · Status: __ · Disposition: __ · Hint: __`

---

## Triagem — critérios avaliados  ·  *(Ato 1 do PO)*
<!-- origination: id=triage-criteria; blocks=true; min-confidence=70; kind=capture; inputs=demand-summary -->

> O PO avalia cada critério (todos avaliados = `triageReady`). Cada veredito carrega
> o modelo de decisão: **verdict · rationale · basis · source**. Ver
> [`references/triage.md`](../references/triage.md) e `personas/02-po.md` §6.1.

| # | Critério | Veredito | Justificativa (rationale) | Base / Fonte |
|---|---|---|---|---|
| 1 | É um problema real (não sintoma isolado)? | Sim / Não | [por quê] | [origination / dado] |
| 2 | É recorrente / tem volume? | Sim / Não | | |
| 3 | Encaixa na visão do produto? | Sim / Não | | |
| 4 | Qual o impacto técnico e de negócio? | Alto / Médio / Baixo | | |
| 5 | Urgência e impacto justificam agora? | Sim / Não | | |

`Confidence: __ · Origin: ai_drafted · Source: __ · Status: __ · Disposition: __ · Hint: __`

---

## Triagem — decisão de roteamento
<!-- origination: id=triage-decision; blocks=true; min-confidence=80; kind=capture; inputs=triage-criteria -->

> **Uma** decisão de caminho, com justificativa obrigatória. Só `Product Ready`
> abre o Ato 2; as demais encerram a passagem pelo PO neste momento (curto-circuito).

| Campo | Valor |
|---|---|
| **Decisão (verdict)** | Product Ready / Discovery / Backlog de Oportunidades / Rejeitar |
| **Justificativa (rationale)** | [Por que esta decisão — defensável] |
| **Base / Fonte (basis / source)** | [registro de intake / disposição / dado de portfólio] |
| **Reversível?** | Sim (Discovery/Backlog — porta lateral) / Não (Rejeitar — fecha) |
| **Submitter notificado** | Sim — AAAA-MM-DD |

> **Gate da triagem (`triageReady`):** todos os critérios avaliados. Não força uma
> decisão específica — força que a decisão seja **informada**.

`Confidence: __ · Origin: po_authored · Source: __ · Status: __ · Disposition: __ · Hint: __`

---

## Escalada arquitetural ao CTO
<!-- origination: id=cto-escalation; blocks=false; min-confidence=0; kind=derived; inputs=triage-decision -->

**Necessária:** Sim / Não — [breve justificativa]

> Sinaliza se a racionalização (Ato 2) provavelmente precisará de Technical
> Assessment. A decisão autoritativa do `tech-assessment-ref` é tomada no RP pelo
> `hsb-escalation-flagger`; aqui é só um early flag herdado adiante.

---

## Premissas validadas na triagem
<!-- origination: id=validated-assumptions; blocks=false; min-confidence=0; kind=capture; inputs=demand-summary -->

> Premissas do origination que o PO revisou e o veredito de cada uma. As que
> sobrevivem viajam adiante explicitamente para o RP.

| Premissa (do origination) | Veredito do PO | A validar com |
|---|---|---|
| [Premissa] | Aceita / Rejeitada / A validar | [Quem] |

---

## Constraints reconhecidos
<!-- origination: id=constraints; blocks=false; min-confidence=0; kind=capture; inputs=demand-summary -->

> Constraints que o downstream deve considerar desde o primeiro dia (herdados do
> origination, validados aqui).

| Constraint | Tipo | Nota do PO |
|---|---|---|
| [Constraint] | Tempo / Orçamento / Legal / Técnico / Escopo / Externo | [Nota] |

---

## Discovery Brief
<!-- origination: id=discovery; blocks=false; min-confidence=0; kind=derived; inputs=triage-decision; condition=triage-decision==Discovery -->

> Preencher **apenas** se a decisão de roteamento for **Discovery**; caso
> contrário, remover esta seção.

### O que está faltando

| # | Incógnita | Quem pode responder | Método |
|---|---|---|---|
| 1 | [Incógnita] | [PO / CTO / Cliente / Vendas] | [Spike / Chamada com cliente / Revisão de infra] |

**Time-box do Discovery:** [N dias] (AAAA-MM-DD → AAAA-MM-DD)

### Resultado do Discovery

| # | Incógnita | Resolução | Impacto no escopo |
|---|---|---|---|
| 1 | [Incógnita] | [Resolução] | Adicionado / Removido / Movido para backlog |

**Novo caminho de decisão:** Discovery → Product Ready / Rejeitado / Backlog
**Discovery encerrado:** AAAA-MM-DD ([N dias — dentro / fora do time-box])

---

## Handoff
<!-- origination: id=handoff; blocks=false; min-confidence=0; kind=derived; inputs=triage-decision -->

- **Se `Product Ready`:** o PO inicia o Ato 2 → racionalização (Readiness Package).
- **Se `Discovery`:** abre o Discovery Brief acima; ao encerrar, retria.
- **Se `Backlog` / `Rejeitar`:** encerra a passagem pelo PO; Submitter notificado com justificativa.

<!-- END OF DOCUMENT -->
