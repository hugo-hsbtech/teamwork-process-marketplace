<!--
TARGET TEMPLATE · Readiness Package (default)
This file is the contract. Each fillable section carries an annotation:
  <!- - origination: SECTION-ID; blocks=BOOL; min-confidence=N; kind=TYPE - ->
and a self-sufficient rubric. The Template Analyst derives contract.lock.md from
these (the same engine as origination-brainstorm — the marker keyword stays `origination:`).
The confidence line adds an Origin field (inherited | ai_drafted | po_authored)
per personas/02-po.md. To use a different document type, copy this file, re-annotate,
and pass it as TEMPLATE. See references/contract-and-template.md (in origination-brainstorm).
Default confidence threshold (X) = 70. Raise per-section for high-stakes fields.
-->

# Readiness Package — [Demand name]
<!-- rev: 0 · updated: AAAA-MM-DD -->

> O Readiness Package (RP) é a **definição de pronto de produto** — o output do PO.
> Ele é auto-suficiente: visão, problema, escopo, regras, user stories, NFRs, edge
> cases, critérios e métricas. O RP **não** contém seções de autoria do CTO; a
> avaliação técnica vive no Technical Assessment (referenciado abaixo). O RP herda
> a camada de confiança do Origination vinculado; o que entrou como premissa ou incógnita
> é resolvido ou carregado explicitamente na seção "Prontidão herdada".

## Metadados
<!-- origination: id=meta; blocks=false; min-confidence=0; kind=meta -->

| Campo | Valor |
|---|---|
| **ID do Pacote** | RP-AAAA-NNN |
| **Versão** | v1 |
| **Origination vinculado** | INT-AAAA-NNN |
| **Responsável** | [Nome] (PO) |
| **Natureza da demanda** | Greenfield / Brownfield / Híbrido (herdado do Intake) |
| **Base de conhecimento** | `tech-landscape-[sistema].md` · Parcial · A criar · N/A (greenfield) |
| **Escalada ao CTO** | — |
| **Status** | Rascunho |
| **Data de congelamento (freeze)** | — |
| **Output language** | [e.g. pt-BR] |

## Histórico de Revisão
<!-- origination: id=revisions; blocks=false; min-confidence=0; kind=meta -->

| Versão | Data | Autor | Status | Resumo |
|---|---|---|---|---|
| v1 | AAAA-MM-DD | [Nome] (PO) | Rascunho | Submissão inicial. |

---

## Prontidão herdada e dispositions em aberto
<!-- origination: id=inherited-readiness; blocks=false; min-confidence=0; kind=derived; inputs=exec-summary,context-problem,objectives,personas,scope,metrics,release-criteria,risks -->

> Resumo do que o Origination entregou e do que continua *soft* na entrada da execução.
> Premissas, incógnitas de Discovery e respostas delegadas que sobreviveram à
> racionalização precisam estar visíveis — não enterradas nas seções. Se uma
> premissa carregada aqui se provar falsa durante a execução, a demanda deve ser
> reavaliada (o mesmo gatilho de retriagem do origination se aplica downstream).

| Campo | Valor |
|---|---|
| **Readiness Score no handoff do Origination** | __ % |
| **Premissas ainda a validar** | [lista ou —] |
| **Incógnitas de Discovery** | [resolvidas / ainda abertas — ] |
| **Requisitos delegados (com dono)** | [lista ou —] |

---

## Seção 1 — Resumo Executivo
<!-- origination: id=exec-summary; blocks=true; min-confidence=70; kind=capture -->
> Rubric: 2–4 parágrafos curtos. Qual é o problema, o que será construído e qual é
> o resultado esperado de negócio. Deve ser legível por qualquer stakeholder sem
> contexto adicional. Herdado e expandido do origination quando possível.

[fill]

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Seção 2 — Contexto e Problema (a dor, não a solução)
<!-- origination: id=context-problem; blocks=true; min-confidence=80; kind=capture -->
> Rubric: cenário atual, limitações, dor do cliente e impacto de negócio — o
> problema, nunca a solução. Se descreve uma solução ("construir X"), NÃO está
> satisfeita: reformule para a dor subjacente. Herdada do origination quando possível.

### Cenário Atual

[fill]

### Limitações

[fill]

### Dor do Cliente

[fill]

### Impacto de Negócio

[fill]

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Seção 3 — Objetivos e Resultado Esperado
<!-- origination: id=objectives; blocks=true; min-confidence=70; kind=capture -->
> Rubric: objetivos numerados e observáveis que esta entrega deve alcançar após o
> release. Cada objetivo deve ser verificável: se não pode ser medido ou observado,
> não está satisfeito. Mínimo dois objetivos.

[fill]

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Seção 4 — Personas Impactadas / Jobs-to-be-done
<!-- origination: id=personas; blocks=true; min-confidence=70; kind=capture -->
> Rubric: para cada persona, o job-to-be-done (o que está tentando realizar) e como
> é impactada por esta entrega. Sem persona definida, scope e critérios de aceite
> não têm âncora. Herdado do origination (campo reach) quando possível.

[fill]

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Seção 5 — Escopo Incluído e Excluído
<!-- origination: id=scope; blocks=true; min-confidence=75; kind=capture -->
> Rubric: protege o downstream de scope creep. Deve listar explicitamente o que
> está FORA, não apenas o que está dentro. Itens adiados alimentam o Roadmap
> (Seção 14). Sem "excluído" preenchido, a seção NÃO está satisfeita.

### Incluído

[fill]

### Excluído

[fill]

### Adiado (fases futuras)

[fill]

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Seção 6 — Regras de Negócio e Fluxos
<!-- origination: id=business-rules; blocks=true; min-confidence=80; kind=capture -->
> Rubric: regras, validações e transições de estado que governam a funcionalidade.
> Cada regra deve ser verificável e atômica. Fluxos de transição de estado devem
> cobrir caminhos de erro, não apenas o caminho feliz.

### [Bloco de Regras 1]

[fill]

### Fluxo de Transição de Estado

[fill]

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Seção 6.5 — Jornada(s) do Usuário (ponta-a-ponta)
<!-- origination: id=user-journey; blocks=true; min-confidence=70; kind=capture -->
> Rubric: a peça entre "o que" e "as histórias". A definição precisa de uma noção do
> que o usuário faz **de ponta a ponta** — o caminho completo, não fragmentos. As
> User Stories (Seção 7) **derivam** dos passos desta jornada. Território do PO
> (produto, não UX detalhado de tela). Padrão: *user journey map* (happy path +
> caminhos alternativos) e, quando há bastidor relevante, *service blueprint*
> (opcional). Compressão: melhoria pequena = jornada de 3–5 passos do happy path,
> sem blueprint. Sem ao menos o happy path da jornada principal, NÃO está satisfeita.

### Jornada principal (happy path) — [Nome da jornada]

> Os passos que o usuário percorre para alcançar o resultado de valor. Cada passo gera (ou valida) uma User Story na Seção 7.

| # | Gatilho / Ação do usuário | Resultado esperado | Touchpoint / Tela | Pré-condição |
|---|---|---|---|---|
| 1 | [O que o usuário faz] | [O que o sistema entrega/responde] | [Onde acontece] | [O que precisa ser verdade antes] |

### Caminhos alternativos e de saída

> Desvios, cancelamentos, estados vazios. Ligam-se aos Edge Cases (Seção 9).

- **[Caminho alternativo]:** [quando ocorre → para onde leva]
- **[Saída / cancelamento]:** [o que acontece com o estado]

### Service Blueprint *(opcional — só quando há bastidor/ops/integração humana relevante)*

> Expõe o que sustenta a jornada "por trás do palco". Pular quando a jornada é puramente self-service.

| Camada | [Passo 1] | [Passo 2] | [Passo 3] |
|---|---|---|---|
| **Frontstage** (o que o usuário vê) | | | |
| **Backstage** (ações internas/time) | | | |
| **Sistemas de apoio** (serviços, dados, terceiros) | | | |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Seção 7 — Épicos e User Stories + Critérios de Aceite
<!-- origination: id=user-stories; blocks=true; min-confidence=80; kind=capture -->
> Rubric: as histórias **agrupam-se sob Épicos** — cada épico é um **entregável**
> coerente de valor (o bloco que o time entrega e que o stakeholder reconhece como
> resultado). Um épico tem ID (`EPIC-NNN`), título e objetivo/valor; sob ele vêm as
> user stories que o compõem. Cada história: "Como [persona], quero [ação], para
> [benefício]"; critérios de aceite em Given/When/Then, verificáveis por não-dev,
> com limites específicos. **Épicos e histórias derivam da Jornada (Seção 6.5) e do
> Escopo (Seção 5)** — cada passo do happy path gera ou valida uma história, e as
> histórias que entregam o mesmo resultado de valor formam um épico. origin=ai_drafted
> no draft pass; o PO confirma os épicos e as histórias. **Regra de evidência dos
> entregáveis:** toda história pertence a exatamente um épico e nenhuma história fica
> órfã — se uma história não cabe em nenhum épico, falta um épico.

### EPIC-001 — [Título do entregável]

> Objetivo / valor: [o resultado de negócio que este épico entrega de ponta a ponta]

**ST-001 — [título curto da história]**
Como [persona], quero [ação], para [benefício].

*Given* [contexto] *when* [ação] *then* [resultado verificável].

**ST-002 — [título curto da história]**
Como [persona], quero [ação], para [benefício].

*Given* [contexto] *when* [ação] *then* [resultado verificável].

### EPIC-002 — [Título do entregável]

> Objetivo / valor: [o resultado de negócio que este épico entrega de ponta a ponta]

**ST-003 — [título curto da história]**
Como [persona], quero [ação], para [benefício].

*Given* [contexto] *when* [ação] *then* [resultado verificável].

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Seção 8 — Requisitos Não-Funcionais (NFRs)
<!-- origination: id=nfrs; blocks=true; min-confidence=70; kind=capture -->
> Rubric: preencher apenas as dimensões aplicáveis (checklist ISO/IEC 25010 — não
> forçar as irrelevantes). O PO descreve o requisito de qualidade; viabilidade e
> *como* são do Technical Assessment. Sem ao menos uma dimensão preenchida,
> a seção NÃO está satisfeita.

[fill]

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Seção 9 — Edge Cases e Modos de Falha
<!-- origination: id=edge-cases; blocks=true; min-confidence=70; kind=capture -->
> Rubric: estados de erro, timeouts, permissões, concorrência. Para features de IA:
> comportamento do modelo e baixa-confiança. Primeira classe — não rodapé. Cada
> item descreve o comportamento esperado do sistema (não apenas o que pode dar errado).

[fill]

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Seção 10 — Métricas de Sucesso (primária · secundária · guardrail)
<!-- origination: id=metrics; blocks=true; min-confidence=70; kind=capture -->
> Rubric: valores projetados — o baseline que metrics.md confronta com o medido
> pós-rollout. Inclua indicadores leading e lagging e ao menos um guardrail (a
> métrica que não pode piorar). Cada meta carrega a confiança da projeção.

[fill]

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Seção 11 — Critérios de Sucesso e Aceite (do release)
<!-- origination: id=release-criteria; blocks=true; min-confidence=70; kind=capture -->
> Rubric: indicadores de alto nível que definem "concluído e valioso" para este
> release — distintos das métricas contínuas da Seção 10. Deve cobrir ao menos
> as dimensões Negócio, Qualidade e UX. Critérios genéricos ("funciona bem") NÃO
> estão satisfeitos: exija valor alvo mensurável.

[fill]

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Seção 12 — Riscos e Dependências (de produto e negócio)
<!-- origination: id=risks; blocks=true; min-confidence=70; kind=capture -->
> Rubric: riscos de produto, negócio, adoção, externos e compliance. Riscos
> técnicos migram para o Technical Assessment. Cada risco tem probabilidade,
> impacto e mitigação. Dependências de produto/negócio listadas separadamente.

[fill]

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Seção 13 — Avaliação Preliminar de Esforço e Custo
<!-- origination: id=effort-estimate; blocks=false; min-confidence=0; kind=capture -->
> Rubric: somente uso interno — o chute do PO para sustentar sequenciamento. O
> número firme vem do CTO no Technical Assessment. Não é compromisso contratual
> nem material para cliente. Confiança esperada: baixa (ai_drafted ou po_authored
> sem dados firmes).

[fill]

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Seção 14 — Roadmap Sugerido
<!-- origination: id=roadmap; blocks=false; min-confidence=0; kind=capture -->
> Rubric: visão de sequenciamento de valor além deste release. Items adiados da
> Seção 5 alimentam fases futuras. MVP é este release; Fase 2 e Fase 3 são
> backlog futuro. Não é compromisso de entrega.

### MVP (este release)

[fill]

### Fase 2 (backlog futuro)

[fill]

### Fase 3 (backlog futuro)

[fill]

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Referência ao Technical Assessment
<!-- origination: id=tech-assessment-ref; blocks=false; min-confidence=0; kind=derived; inputs=scope,business-rules,nfrs,risks -->
> Rubric: ponte para o artefato do CTO — status + veredito + link, NÃO conteúdo.
> Se a escalada for requisitada, congela só com Disposition=deferred (TA pendente,
> fora do escopo desta ferramenta) ou Status=Assinado quando o TA existir.

| Campo | Valor |
|---|---|
| **Status** | not_requested / requested / in_progress / signed / vetoed |
| **Veredito** | viável / viável-com-ressalvas / inviável-como-escopado / — |
| **Link** | — |
| **Escalada requisitada?** | Não / Sim |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

<!-- END OF DOCUMENT -->
