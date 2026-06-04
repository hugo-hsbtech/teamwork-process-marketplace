# Readiness Package — Gestão de Assentos Self-Service para Admins Enterprise
<!-- rev: 0 · updated: 2026-06-03 -->

> Under-filled seed for the REVISIT eval: inherited sections carry plausible content
> from the intake; new product sections (business-rules, user-stories, NFRs,
> edge-cases) are blank or minimal so the skill must reopen and resolve them
> non-interactively. Revision must be bumped by the revisit pass.

> O Readiness Package (RP) é a **definição de pronto de produto** — o output do PO.
> Ele é auto-suficiente: visão, problema, escopo, regras, user stories, NFRs, edge
> cases, critérios e métricas. O RP **não** contém seções de autoria do CTO; a
> avaliação técnica vive no Technical Assessment (referenciado abaixo). O RP herda
> a camada de confiança do Intake vinculado; o que entrou como premissa ou incógnita
> é resolvido ou carregado explicitamente na seção "Prontidão herdada".

## Metadados
<!-- intake: id=meta; blocks=false; min-confidence=0; kind=meta -->

| Campo | Valor |
|---|---|
| **ID do Pacote** | RP-2026-014 |
| **Versão** | v0 |
| **Intake vinculado** | INT-2026-014 |
| **Responsável** | Ana Ribeiro (PO) |
| **Escalada ao CTO** | Sim — Technical Assessment TA-2026-014 (pendente) |
| **Status** | Rascunho |
| **Data de congelamento (freeze)** | — |
| **Output language** | pt-BR |

## Histórico de Revisão
<!-- intake: id=revisions; blocks=false; min-confidence=0; kind=meta -->

| Versão | Data | Autor | Status | Resumo |
|---|---|---|---|---|
| v0 | 2026-06-03 | Ana Ribeiro (PO) | Rascunho | Seed parcial — seções herdadas preenchidas; seções de produto a completar. |

---

## Prontidão herdada e dispositions em aberto
<!-- intake: id=inherited-readiness; blocks=false; min-confidence=0; kind=derived; inputs=exec-summary,context-problem,objectives,personas,scope,metrics,release-criteria,risks -->

| Campo | Valor |
|---|---|
| **Readiness Score no handoff do Intake** | 82 % |
| **Premissas ainda a validar** | Volume de 240 tickets/trimestre é representativo; breakdown por conta não disponível |
| **Incógnitas de Discovery** | Breakdown de tickets por conta (CS pode extrair em ~1 semana) |
| **Requisitos delegados (com dono)** | Arquitetura de provisionamento sync/async (CTO — TA-2026-014) |

---

## Seção 1 — Resumo Executivo
<!-- intake: id=exec-summary; blocks=true; min-confidence=70; kind=capture -->
> Rubric: 2–4 parágrafos curtos. Qual é o problema, o que será construído e qual é
> o resultado esperado de negócio. Deve ser legível por qualquer stakeholder sem
> contexto adicional. Herdado e expandido do intake quando possível.

Admins enterprise não conseguem adicionar ou remover assentos sem abrir um ticket de suporte. O lead time de 1–3 dias úteis cria dependência operacional que gera fricção em ondas de onboarding e em ciclos de renovação de contrato. Em Q1 2026, 240 tickets (18% do volume enterprise) foram desse tipo.

Esta entrega cria um painel de gestão de assentos self-service no produto. O resultado esperado é a eliminação da dependência operacional do CS para operações rotineiras de seat management.

`Confidence: 82 · Origin: inherited · Source: intake INT-2026-014 §problem + support export Q1 2026 · Status: resolved · Disposition: inherited · Hint: herdado do intake`

---

## Seção 2 — Contexto e Problema (a dor, não a solução)
<!-- intake: id=context-problem; blocks=true; min-confidence=80; kind=capture -->
> Rubric: cenário atual, limitações, dor do cliente e impacto de negócio — o
> problema, nunca a solução. Se descreve uma solução ("construir X"), NÃO está
> satisfeita: reformule para a dor subjacente. Herdada do intake quando possível.

### Cenário Atual

Toda alteração de assento exige abertura de ticket para o CS. O admin não tem acesso direto à gestão de licenças.

### Limitações

- Sem interface self-service.
- Latência de 1–3 dias úteis.

### Dor do Cliente

Admins enterprise dependem do CS para qualquer mudança de headcount. Em empresas com alta rotatividade isso gera múltiplos tickets por mês.

### Impacto de Negócio

- 240 tickets de seat management em Q1 2026 (18% do volume total enterprise).
- 3 contas sinalizaram insatisfação em entrevistas de renovação Q4 2025.

`Confidence: 86 · Origin: inherited · Source: intake INT-2026-014 §problem + support export Q1 2026 · Status: resolved · Disposition: inherited · Hint: herdado do intake`

---

## Seção 3 — Objetivos e Resultado Esperado
<!-- intake: id=objectives; blocks=true; min-confidence=70; kind=capture -->
> Rubric: objetivos numerados e observáveis que esta entrega deve alcançar após o
> release. Cada objetivo deve ser verificável: se não pode ser medido ou observado,
> não está satisfeito. Mínimo dois objetivos.

1. **Reduzir tickets de seat management em ≥ 75%** em 90 dias pós-rollout.
2. **Habilitar self-service para ≥ 85% das alterações de assento** sem intervenção do CS.

`Confidence: 80 · Origin: inherited · Source: intake INT-2026-014 §objectives · Status: resolved · Disposition: inherited · Hint: targets baseados no intake`

---

## Seção 4 — Personas Impactadas / Jobs-to-be-done
<!-- intake: id=personas; blocks=true; min-confidence=70; kind=capture -->
> Rubric: para cada persona, o job-to-be-done (o que está tentando realizar) e como
> é impactada por esta entrega. Sem persona definida, scope e critérios de aceite
> não têm âncora. Herdado do intake (campo reach) quando possível.

| Persona | Job-to-be-done | Impacto desta entrega |
|---|---|---|
| **Admin Enterprise** (role `billing_admin`) | Ajustar licenças do time de forma autônoma. | Passa a ter controle direto no painel. |
| **Analista de CS** | Resolver demandas de alta complexidade. | Fica liberado de ~240 tickets/trimestre repetitivos. |

`Confidence: 75 · Origin: inherited · Source: intake INT-2026-014 §reach · Status: resolved · Disposition: inherited · Hint: persona financeiro a confirmar escopo`

---

## Seção 5 — Escopo Incluído e Excluído
<!-- intake: id=scope; blocks=true; min-confidence=75; kind=capture -->
> Rubric: protege o downstream de scope creep. Deve listar explicitamente o que
> está FORA, não apenas o que está dentro. Itens adiados alimentam o Roadmap
> (Seção 14). Sem "excluído" preenchido, a seção NÃO está satisfeita.

### Incluído

- Painel de gestão de assentos para usuários com role `billing_admin`.
- Ação de adição e remoção de assentos com preview de custo.
- Log de auditoria das últimas 90 dias.

### Excluído

- API pública para automação de seat management — fase 2.
- Notificações por e-mail automáticas — fase 2.
- Integração com sistemas de HR — fase 3.

### Adiado (fases futuras)

- API pública de seat management (fase 2).
- Notificações e-mail/Slack (fase 2).

`Confidence: 80 · Origin: inherited · Source: intake INT-2026-014 §scope · Status: resolved · Disposition: inherited · Hint: exclusões validadas com CS`

---

## Seção 6 — Regras de Negócio e Fluxos
<!-- intake: id=business-rules; blocks=true; min-confidence=80; kind=capture -->
> Rubric: regras, validações e transições de estado que governam a funcionalidade.
> Cada regra deve ser verificável e atômica. Fluxos de transição de estado devem
> cobrir caminhos de erro, não apenas o caminho feliz.

### Regras de Gestão de Assentos

[fill]

### Fluxo de Transição de Estado

[fill]

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Seção 7 — User Stories + Critérios de Aceite
<!-- intake: id=user-stories; blocks=true; min-confidence=80; kind=capture -->
> Rubric: uma história por bloco de valor, "Como [persona], quero [ação], para
> [benefício]"; critérios de aceite em Given/When/Then, verificáveis por não-dev,
> com limites específicos. origin=ai_drafted no draft pass; o PO confirma.

[fill]

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Seção 8 — Requisitos Não-Funcionais (NFRs)
<!-- intake: id=nfrs; blocks=true; min-confidence=70; kind=capture -->
> Rubric: preencher apenas as dimensões aplicáveis (checklist ISO/IEC 25010 — não
> forçar as irrelevantes). O PO descreve o requisito de qualidade; viabilidade e
> *como* são do Technical Assessment. Sem ao menos uma dimensão preenchida,
> a seção NÃO está satisfeita.

[fill]

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Seção 9 — Edge Cases e Modos de Falha
<!-- intake: id=edge-cases; blocks=true; min-confidence=70; kind=capture -->
> Rubric: estados de erro, timeouts, permissões, concorrência. Para features de IA:
> comportamento do modelo e baixa-confiança. Primeira classe — não rodapé. Cada
> item descreve o comportamento esperado do sistema (não apenas o que pode dar errado).

[fill]

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Seção 10 — Métricas de Sucesso (primária · secundária · guardrail)
<!-- intake: id=metrics; blocks=true; min-confidence=70; kind=capture -->
> Rubric: valores projetados — o baseline que metrics.md confronta com o medido
> pós-rollout. Inclua indicadores leading e lagging e ao menos um guardrail (a
> métrica que não pode piorar). Cada meta carrega a confiança da projeção.

| Tipo | Métrica | Baseline | Target (90 dias pós-rollout) | Confiança da projeção |
|---|---|---|---|---|
| **Primária (lagging)** | Tickets de seat management / trimestre | 240 | ≤ 60 (−75%) | 62% |

`Confidence: 70 · Origin: inherited · Source: support export Q1 2026 + intake INT-2026-014 §metrics · Status: low_confidence · Disposition: inherited · Hint: baseline firme; projeção de −75% é estimativa`

---

## Seção 11 — Critérios de Sucesso e Aceite (do release)
<!-- intake: id=release-criteria; blocks=true; min-confidence=70; kind=capture -->
> Rubric: indicadores de alto nível que definem "concluído e valioso" para este
> release — distintos das métricas contínuas da Seção 10. Deve cobrir ao menos
> as dimensões Negócio, Qualidade e UX. Critérios genéricos ("funciona bem") NÃO
> estão satisfeitos: exija valor alvo mensurável.

[fill]

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Seção 12 — Riscos e Dependências (de produto e negócio)
<!-- intake: id=risks; blocks=true; min-confidence=70; kind=capture -->
> Rubric: riscos de produto, negócio, adoção, externos e compliance. Riscos
> técnicos migram para o Technical Assessment. Cada risco tem probabilidade,
> impacto e mitigação. Dependências de produto/negócio listadas separadamente.

[fill]

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Seção 13 — Avaliação Preliminar de Esforço e Custo
<!-- intake: id=effort-estimate; blocks=false; min-confidence=0; kind=capture -->
> Rubric: somente uso interno — o chute do PO para sustentar sequenciamento. O
> número firme vem do CTO no Technical Assessment. Não é compromisso contratual
> nem material para cliente. Confiança esperada: baixa (ai_drafted ou po_authored
> sem dados firmes).

[fill]

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Seção 14 — Roadmap Sugerido
<!-- intake: id=roadmap; blocks=false; min-confidence=0; kind=capture -->
> Rubric: visão de sequenciamento de valor além deste release. Items adiados da
> Seção 5 alimentam fases futuras. MVP é este release; Fase 2 e Fase 3 são
> backlog futuro. Não é compromisso de entrega.

### MVP (este release)

- Painel self-service de adição e remoção de assentos.
- Log de auditoria dos últimos 90 dias.

### Fase 2 (backlog futuro)

[fill]

### Fase 3 (backlog futuro)

[fill]

`Confidence: 60 · Origin: po_authored · Source: itens adiados §5 · Status: draft · Disposition: po_authored · Hint: roadmap tentativo`

---

## Referência ao Technical Assessment
<!-- intake: id=tech-assessment-ref; blocks=false; min-confidence=0; kind=derived; inputs=scope,business-rules,nfrs,risks -->
> Rubric: ponte para o artefato do CTO — status + veredito + link, NÃO conteúdo.
> Se a escalada for requisitada, congela só com Disposition=deferred (TA pendente,
> fora do escopo desta ferramenta) ou Status=Assinado quando o TA existir.

| Campo | Valor |
|---|---|
| **Status** | requested |
| **Veredito** | — |
| **Link** | TA-2026-014 (pendente) |
| **Escalada requisitada?** | Sim |

`Confidence: 40 · Origin: po_authored · Source: RP draft pass · Status: low_confidence · Disposition: deferred · Hint: TA pendente — congelamento provisório`

<!-- END OF DOCUMENT -->
