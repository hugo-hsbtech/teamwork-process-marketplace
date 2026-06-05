<!--
TARGET TEMPLATE · Technical Assessment (default)
This file is the contract. Each fillable section carries an annotation:
  <!- - origination: SECTION-ID; blocks=BOOL; min-confidence=N; kind=TYPE - ->
and a self-sufficient rubric. The Template Analyst derives contract.lock.md from
these (the same engine as origination-brainstorm / readiness-package — the marker
keyword stays `origination:`).
The confidence line adds an Origin field (inherited | ai_drafted | cto_authored)
per personas/02-po.md §2/§10 and templates/03-technical-assessment.md. The TA is
the CTO's output: it RESPONDS to the RP and is authored ALONE by the CTO — it
never edits the RP. To use a different document type, copy this file, re-annotate,
and pass it as TEMPLATE. See references/contract-and-template.md (in origination-brainstorm).
Default confidence threshold (X) = 70. Raise per-section for high-stakes fields.

TWO PATHS, ONE TEMPLATE. The `tech-classification` section governs which path is
required: Greenfield (the TA DEFINES the foundation — fill `tech-foundation`) or
Brownfield/Hybrid (the TA DISCOVERS the current system — fill `current-state`).
Fill the applicable path; the other is dispositioned `Disposition: decided` with
content "N/A — see Classificação Técnica" (an honest disposition that clears the
gate). See references/classification.md.
-->

# Technical Assessment — [Nome da demanda]
<!-- rev: 0 · updated: AAAA-MM-DD -->

> O Technical Assessment (TA) é o **output do CTO** — e vai **além da arquitetura**:
> estabelece o **terreno técnico** sobre o qual a engenharia decide. Como a camada de
> execução (humana ou agente de IA) **não tem conhecimento implícito do código-fonte**,
> o TA torna explícito o que normalmente fica tácito: a natureza da demanda (software
> novo vs. existente), o estado atual ou a fundação a criar, a base de conhecimento, a
> viabilidade de cada NFR, as alternativas descartadas, testabilidade e observabilidade.
> É escrito **sozinho** pelo CTO, **em paralelo** ao Readiness Package, e **responde** a
> ele: o CTO **nunca edita o RP**. O TA não redefine o produto — pode **vetar** a
> viabilidade do escopo, e então o PO revisa o escopo do RP. A fusão do RP (produto) com
> este TA (técnico) acontece no PRD. Ver `personas/02-po.md` §2 e §10 e
> `interactions/05-po-to-cto.md` / `interactions/06-cto-to-po.md`.

## Metadados
<!-- origination: id=meta; blocks=false; min-confidence=0; kind=meta -->

| Campo | Valor |
|---|---|
| **ID da Avaliação** | TA-AAAA-NNN |
| **Versão** | v1 |
| **RP vinculado** | RP-AAAA-NNN vX |
| **Intake vinculado** | INT-AAAA-NNN |
| **Responsável** | [Nome] (CTO) |
| **Status** | Requisitado / Em andamento / Assinado / Vetado |
| **Veredito de viabilidade** | viável / viável-com-ressalvas / inviável-como-escopado |
| **Data de assinatura** | — |
| **Output language** | [e.g. pt-BR] |

## Histórico de Revisão
<!-- origination: id=revisions; blocks=false; min-confidence=0; kind=meta -->

| Versão | Data | Autor | Status | Resumo |
|---|---|---|---|---|
| v1 | AAAA-MM-DD | [Nome] (CTO) | Em andamento | Avaliação inicial. |

---

## Veredito de Viabilidade
<!-- origination: id=feasibility-verdict; blocks=true; min-confidence=85; kind=capture -->
> Rubric: a **decisão de primeira classe do CTO** (`personas/03-cto.md` §3 — *feasibility
> is first class*: todo juízo carrega `verdict` + `rationale` + **`terrain`** + `confidence`
> + `source` + `generates`). Carrega rationale — nunca um carimbo — e o **terreno** em que
> repousa: *"viabilidade não se avalia em terreno desconhecido"* (`03-cto.md` §3, a regra de
> ouro do CTO). Se **inviável-como-escopado**, o CTO retorna com veto + rationale; o PO
> revisa o escopo do RP e re-escala. O CTO não redefine o produto. Esta seção só se resolve
> em confiança alta (a viabilidade é o juízo central do CTO).

| Campo | Valor |
|---|---|
| **Veredito** | viável / viável-com-ressalvas / inviável-como-escopado |
| **Rationale** | [Por quê — defensável] |
| **Terreno (terrain)** | `tech-landscape-[sistema].md` (KB em que repousa) · "não documentado → Discovery" |
| **Ressalvas (se aplicável)** | [O que precisa ser verdade para o veredito se sustentar] |
| **Gera (generates)** | hard_constraint · adr · discovery_spike · kb_update · — |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Classificação Técnica e Base de Conhecimento
<!-- origination: id=tech-classification; blocks=true; min-confidence=80; kind=capture -->
> Rubric: **a decisão que governa o resto do documento.** Herda a natureza da demanda do
> Intake e a confirma sob a lente técnica. Define qual caminho preencher (greenfield vs.
> brownfield) e ancora o TA na base de conhecimento — o que existe, o que falta, o que
> será criado. Se a KB não existe/está incompleta (brownfield), documentar o sistema
> atual é **pré-requisito**: registre como spike no *Caminho de Discovery* e produza/
> atualize o `tech-landscape`. Se greenfield, os ADRs fundacionais **semeiam** um novo
> `tech-landscape`.

| Campo | Valor |
|---|---|
| **Natureza (confirmada pelo CTO)** | Greenfield (novo) · Brownfield (existente) · Híbrido (novo dentro de existente) |
| **Caminho a preencher** | Fundação técnica (greenfield) · Estado atual (brownfield) · Ambos (híbrido) |
| **Base de Conhecimento (KB)** | Existe → referência · Parcial → referência + lacunas · Não existe → criar (Discovery) |
| **Referência da KB** | `tech-landscape-[sistema].md` · link · — |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Perguntas do PO Endereçadas
<!-- origination: id=po-questions; blocks=true; min-confidence=70; kind=capture -->
> Rubric: *trace-to-source.* As incógnitas técnicas específicas que o PO escalou — e a
> resposta a cada uma. Mantém a avaliação ancorada ao que foi perguntado (herdadas do
> RP / da escalada). Sem ao menos uma pergunta endereçada (ou "nenhuma pergunta
> específica foi escalada"), a seção NÃO está satisfeita.

| # | Pergunta do PO | Resposta do CTO |
|---|---|---|
| 1 | [Incógnita técnica] | [Resposta] |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Caminho BROWNFIELD — Estado atual / Landscape técnico
<!-- origination: id=current-state; blocks=true; min-confidence=75; kind=capture -->
> Rubric: **documentar o sistema antes de mudá-lo** (preencher se a demanda modifica
> software existente). Em brownfield, a decisão de implementação depende do que já existe
> — padrões, convenções, integrações, dívida. Equivalente ao *document-project* do BMAD.
> Quando há um `tech-landscape` atualizado, **referencie-o** e registre aqui só o
> específico desta demanda. **Se greenfield:** não se aplica — `Disposition: decided`,
> conteúdo "N/A — greenfield (ver Classificação Técnica)".

### Padrões e convenções existentes a respeitar

| Aspecto | Como é hoje | Implicação para esta demanda |
|---|---|---|
| **Estrutura / organização do código** | [Onde as coisas ficam] | [O que seguir] |
| **Padrões de dados / persistência** | [Modelo, migrations] | |
| **Padrões de API / contrato** | [REST/eventos, versionamento] | |
| **Autenticação / autorização** | [Como é aplicada] | |

### Pontos de integração tocados

| Ponto de integração | Sistema/módulo | Natureza do acoplamento | Risco de mudar |
|---|---|---|---|
| [Interface/serviço] | [Quem] | [Síncrono / evento / DB compartilhado] | Alto / Médio / Baixo |

### Dívida técnica e risco de regressão

| Área | Dívida / fragilidade conhecida | Risco de regressão | Cobertura de testes atual |
|---|---|---|---|
| [Módulo] | [O que é frágil] | Alto / Médio / Baixo | [Boa / parcial / nenhuma] |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Caminho GREENFIELD — Fundação técnica
<!-- origination: id=tech-foundation; blocks=true; min-confidence=75; kind=capture -->
> Rubric: **decidir a fundação — com critério, não por reflexo** (preencher se a demanda
> constrói software/módulo novo). Em greenfield não há terreno a descobrir: o TA o
> **cria**. Registre as escolhas-base e o *porquê*, para sustentar ADRs e tornar-se o
> ponto de partida do novo `tech-landscape`. **Se brownfield puro:** não se aplica —
> `Disposition: decided`, conteúdo "N/A — brownfield (ver Classificação Técnica)".

### Seleção de stack (com critério)

| Camada | Escolha | Critério de decisão | Alternativa descartada |
|---|---|---|---|
| **Linguagem / runtime** | [Escolha] | [Por quê — time, ecossistema, performance] | [Qual e por que não] |
| **Framework / app** | | | |
| **Persistência / dados** | | | |
| **Infra / deploy** | | | |

### Arquitetura-alvo

> Diagrama de contexto e container (estilo C4 — só os níveis que agregam valor). Texto ou referência ao diagrama.

```text
[Diagrama de contexto/container — sistemas, usuários, containers e como se comunicam]
```

### Estrutura e convenções de repositório

- **Organização de pastas / módulos:** [padrão a adotar]
- **Convenções de nomeação / lint / teste:** [padrão a adotar]
- **Estratégia de branching / CI:** [padrão a adotar]

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Sistemas e Componentes Afetados
<!-- origination: id=affected-systems; blocks=true; min-confidence=70; kind=capture -->
> Rubric: mapa do raio de impacto. Cada serviço/módulo tocado e a natureza do impacto.
> Herda os sistemas/integrações que o RP nomeou no escopo.

| Sistema / Componente | Natureza do impacto |
|---|---|
| [Serviço / módulo] | [Novo / modificado / apenas consumido] |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Impacto Arquitetural
<!-- origination: id=architectural-impact; blocks=true; min-confidence=75; kind=capture -->
> Rubric: território exclusivo do CTO (migrado da antiga Seção 8 do RP). Para cada área
> tocada, o impacto e a nota arquitetural (padrão a seguir/evitar). Preencher apenas as
> áreas relevantes — não forçar as irrelevantes.

| Área | Impacto | Nota arquitetural |
|---|---|---|
| **Modelo de dados** | [Descrição] | [Padrão a seguir/evitar] |
| **Eventos / mensageria** | [Descrição] | |
| **Frontend** | [Descrição] | |
| **Segurança** | [Descrição] | |
| **Multi-tenancy** | [Descrição] | |
| **Performance / Escalabilidade** | [Descrição] | |
| **Observabilidade** | [Descrição] | |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Integrações Necessárias
<!-- origination: id=integrations; blocks=true; min-confidence=70; kind=capture -->
> Rubric: as integrações do RP, agora sob a lente de **viabilidade técnica** (migrado da
> antiga Seção 7 do RP). Para cada sistema: tipo, protocolo e viabilidade / riscos
> conhecidos. Se a demanda não tem integrações, registre "nenhuma" com `Disposition: decided`.

| Sistema | Tipo | Protocolo | Viabilidade / Riscos conhecidos |
|---|---|---|---|
| [Sistema 1] | Interno / Externo / API / Evento / Webhook / DB | [REST / OIDC / gRPC / …] | [Viável / limitações de terceiro / risco] |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Build vs. Buy
<!-- origination: id=build-vs-buy; blocks=false; min-confidence=0; kind=capture -->
> Rubric: para cada capacidade não-trivial — construir, comprar/integrar um terceiro, ou
> reusar algo existente? A decisão afeta diretamente custo, prazo e risco. Pular (com
> `Disposition: decided`, "sem decisão make-or-buy relevante") se não houver decisão.

| Capacidade | Decisão | Rationale | Efeito em custo/prazo |
|---|---|---|---|
| [Capacidade] | Build / Buy / Reuse | [Por quê] | [Resumo] |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Alternativas Consideradas
<!-- origination: id=alternatives; blocks=true; min-confidence=70; kind=capture -->
> Rubric: **o rationale, não só a conclusão** (padrão design doc Google/RFC). Registrar o
> que foi avaliado e **por que foi descartado** dá ao downstream o contexto para decidir
> a implementação — e evita re-litigar a mesma alternativa depois. Uma linha por
> alternativa significativa.

| Alternativa | Prós | Contras | Por que NÃO foi escolhida |
|---|---|---|---|
| [Abordagem A] | [Prós] | [Contras] | [Razão da rejeição] |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Viabilidade dos NFRs  ·  *(mapeado ao RP, Seção 8)*
<!-- origination: id=nfr-feasibility; blocks=true; min-confidence=75; kind=capture -->
> Rubric: **fecha o laço produto ↔ técnico.** O PO declarou requisitos de qualidade no RP
> (Seção 8); aqui o CTO responde, NFR a NFR, se são **viáveis** e **como** — os *quality
> scenarios* do arc42. Um NFR inviável é veto ou sinal de re-escopo, não um detalhe. Uma
> linha por NFR herdado do RP §8.

| NFR (do RP §8) | Viável? | Como será alcançado / abordagem | Risco / ressalva |
|---|---|---|---|
| [ex.: propagação < 500ms] | Sim / Com ressalvas / Não | [Mecanismo técnico] | [O que ameaça] |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Testabilidade e Observabilidade
<!-- origination: id=testability-observability; blocks=true; min-confidence=70; kind=capture -->
> Rubric: como **provar** que funciona e como **ver** em produção. Sem isto, os critérios
> de aceite do RP não podem ser verificados e o comportamento não pode ser monitorado.

| Dimensão | Abordagem |
|---|---|
| **Estratégia de teste** | [Unitário / integração / e2e — o que cobre o quê; áreas de risco de regressão] |
| **Dados / ambiente de teste** | [Como reproduzir cenários, incl. edge cases do RP §9] |
| **Telemetria / métricas técnicas** | [O que instrumentar para observar a feature] |
| **Logs / alertas** | [Sinais de falha e como serão detectados] |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Restrições Inegociáveis (Hard Constraints)
<!-- origination: id=hard-constraints; blocks=true; min-confidence=75; kind=capture -->
> Rubric: condições não-negociáveis que limitam o espaço de solução. O PO não as suaviza
> nem reinterpreta — se discordar, escala explicitamente (`interactions/06-cto-to-po.md`).
> Se não há restrições rígidas, registre "nenhuma" com `Disposition: decided`.

| Restrição | Tipo | Detalhe | Efeito no escopo |
|---|---|---|---|
| [Restrição 1] | Técnica / Plataforma / Segurança / Multi-tenancy / Externa | [Detalhe] | [O que muda no RP, se algo] |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Riscos Técnicos e Mitigações
<!-- origination: id=tech-risks; blocks=true; min-confidence=75; kind=capture -->
> Rubric: riscos **técnicos** vivem aqui (migrados do RP). Riscos de produto/negócio
> permanecem no RP (Seção 12). Cada risco tem categoria, probabilidade, impacto e mitigação.

| Risco | Categoria | Probabilidade | Impacto | Mitigação |
|---|---|---|---|---|
| [Risco 1] | Técnico / Segurança / Infra / Integração / Dados | Alto / Médio / Baixo | Alto / Médio / Baixo | [Mitigação] |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Decisões de Arquitetura (ADRs)
<!-- origination: id=adrs; blocks=true; min-confidence=75; kind=capture -->
> Rubric: direção arquitetural no nível do CTO. A IA pode chegar com **ADRs sugeridos**
> (reusados da base de conhecimento) — o CTO aprova/ajusta (o WOW moment de §10). O
> detalhamento fino e ADRs de implementação ficam no Tech Backlog do Tech Lead. Cada ADR
> carrega decisão, rationale e o sign-off do CTO.

| # | Decisão | Rationale | Sign-off do CTO |
|---|---|---|---|
| ADR-001 | [Decisão] | [Por que esta abordagem] | ✓ |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Avaliação de Esforço e Custo (firme)
<!-- origination: id=effort-cost; blocks=true; min-confidence=70; kind=capture -->
> Rubric: uso interno. São as estimativas **firmes** do CTO — substituem a estimativa
> preliminar do PO (RP Seção 13). Serão refinadas pelo Tech Lead no Tech Backlog. Não é
> compromisso contratual nem material para cliente.

### Esforço de Desenvolvimento

| Área | Estimativa | Senioridade |
|---|---|---|
| [Backend / Frontend / QA] | [X dias] | Sênior / Pleno / Júnior / QA |
| **Total** | **X dias** | |

### Impacto de Infraestrutura

[Novo provisionamento, mudanças de cluster, regiões adicionais — ou "Nenhum"]

### Impacto de Custo de Terceiros

[Novos provedores, licenças, APIs pagas — ou "Nenhum"]

### Impacto de Custo Operacional Recorrente

[Storage, observabilidade, bandwidth — quantificar se possível]

### Avaliação de TCO

[A feature é custo-neutro, adiciona custo recorrente, ou cria uma fundação reutilizável para fases futuras?]

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Caminho de Discovery (se uma incógnita técnica bloqueia a conclusão)
<!-- origination: id=discovery-path; blocks=false; min-confidence=0; kind=capture -->
> Rubric: preencher apenas se uma incógnita técnica impede o fechamento da avaliação. O
> CTO define o spike/investigação; o PO determina o time-box. A demanda volta ao
> Discovery (`interactions/05-po-to-cto.md`). Se nada bloqueia, registre "—" com
> `Disposition: decided`.

| Incógnita | Spike / Investigação | Quem | Time-box sugerido |
|---|---|---|---|
| [Incógnita técnica] | [O que investigar] | [CTO / time] | [N dias] |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

<!-- END OF DOCUMENT -->
