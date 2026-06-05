# Golden example — Technical Assessment (calibration exemplar)

A self-contained, **already-filled** Technical Assessment used to calibrate quality
(the bar the `hsb-confidence-auditor` scores against, per
`../origination-brainstorm/references/grounding.md`). It is **brownfield** (modifies an
existing multi-tenant SaaS), with a security/multi-tenancy trigger — so the
`current-state` path is in force and `tech-foundation` is honestly N/A. It ends in a
`viável-com-ressalvas` verdict. Read it for *shape and depth*, not domain reuse.

> Demand: **"Filas de votação por turnos com isolamento por tenant"** — the RP (RP-2026-014)
> asks for time-windowed voting queues, scoped per tenant, with a guardrail that vote
> propagation latency must not exceed 500 ms. Escalated to the CTO for multi-tenancy /
> data-isolation impact.

---

## Metadados

| Campo | Valor |
|---|---|
| **ID da Avaliação** | TA-2026-009 |
| **Versão** | v1 |
| **RP vinculado** | RP-2026-014 v2 |
| **Intake vinculado** | INT-2026-031 |
| **Responsável** | C. Nunes (CTO) |
| **Status** | Assinado |
| **Veredito de viabilidade** | viável-com-ressalvas |
| **Data de assinatura** | 2026-05-28 |
| **Output language** | pt-BR |

---

## Veredito de Viabilidade

| Campo | Valor |
|---|---|
| **Veredito** | viável-com-ressalvas |
| **Rationale** | O isolamento por tenant já é garantido pela coluna `tenant_id` + RLS no Postgres; a demanda reusa esse contrato. A única ameaça é o guardrail de 500 ms sob fan-out de votos concorrentes, viável apenas com o caminho de propagação por eventos (não polling) descrito na Viabilidade dos NFRs. |
| **Terreno (terrain)** | `tech-landscape-voting-platform.md` (atualizado 2026-04) — terreno documentado e completo |
| **Ressalvas (se aplicável)** | Mantém-se viável **se** (1) a propagação migrar para o canal de eventos existente e (2) o índice parcial `idx_votes_open_window` for criado antes do rollout. Sem ambos, o guardrail de 500 ms é inviável. |
| **Gera (generates)** | hard_constraint (propagação por evento + índice pré-rollout) · adr (ADR-001, ADR-002) |

`Confidence:` 90 · `Origin:` cto_authored · `Source:` análise CTO + benchmark do canal de eventos · `Status:` resolved · `Disposition:` answered · `Hint:` —

---

## Classificação Técnica e Base de Conhecimento

| Campo | Valor |
|---|---|
| **Natureza (confirmada pelo CTO)** | Brownfield (existente) |
| **Caminho a preencher** | Estado atual (brownfield) |
| **Base de Conhecimento (KB)** | Existe → referência |
| **Referência da KB** | `tech-landscape-voting-platform.md` (atualizado 2026-04) |

`Confidence:` 92 · `Origin:` inherited · `Source:` Intake INT-2026-031 (natureza) + tech-landscape · `Status:` resolved · `Disposition:` answered · `Hint:` —

---

## Perguntas do PO Endereçadas

| # | Pergunta do PO | Resposta do CTO |
|---|---|---|
| 1 | Conseguimos garantir que um tenant nunca veja a fila de outro? | Sim — RLS por `tenant_id` já cobre `votes` e `queues`; a nova tabela `vote_windows` herda a mesma policy. Sem caminho de vazamento novo. |
| 2 | O guardrail de 500 ms de propagação é alcançável? | Com ressalva: só via o canal de eventos (item 1 das ressalvas). Polling não atinge o alvo sob concorrência. |

`Confidence:` 88 · `Origin:` cto_authored · `Source:` escalada do RP §8 + §6 · `Status:` resolved · `Disposition:` answered · `Hint:` —

---

## Caminho BROWNFIELD — Estado atual / Landscape técnico

### Padrões e convenções existentes a respeitar

| Aspecto | Como é hoje | Implicação para esta demanda |
|---|---|---|
| **Estrutura / organização do código** | Módulos por bounded context em `app/contexts/*`; voting em `contexts/voting` | Adicionar `vote_windows` dentro de `contexts/voting`, não um módulo novo |
| **Padrões de dados / persistência** | Postgres, `tenant_id` em toda tabela + RLS; migrations via Ecto | Nova tabela herda `tenant_id` + policy; migration reversível |
| **Padrões de API / contrato** | REST versionado (`/v3`) + eventos internos em RabbitMQ | Reusar o tópico `voting.events`; sem novo contrato externo |
| **Autenticação / autorização** | OIDC + escopos por papel; `tenant_id` no token | Sem mudança — o escopo `voting:write` já existe |

### Pontos de integração tocados

| Ponto de integração | Sistema/módulo | Natureza do acoplamento | Risco de mudar |
|---|---|---|---|
| `voting.events` (RabbitMQ) | Serviço de notificações | Evento (assíncrono) | Médio — aumenta volume de mensagens |
| `votes` (tabela) | Relatórios | DB compartilhado (read-replica) | Baixo |

### Dívida técnica e risco de regressão

| Área | Dívida / fragilidade conhecida | Risco de regressão | Cobertura de testes atual |
|---|---|---|---|
| `contexts/voting` | Contagem de votos recalcula tudo a cada voto (sem agregação incremental) | Médio | Boa (unit + integração) |

`Confidence:` 85 · `Origin:` cto_authored · `Source:` tech-landscape-voting-platform.md · `Status:` resolved · `Disposition:` answered · `Hint:` —

---

## Caminho GREENFIELD — Fundação técnica

N/A — brownfield (ver Classificação Técnica).

`Confidence:` 100 · `Origin:` cto_authored · `Source:` Classificação Técnica · `Status:` resolved · `Disposition:` decided · `Hint:` caminho não aplicável a esta demanda

---

## Sistemas e Componentes Afetados

| Sistema / Componente | Natureza do impacto |
|---|---|
| `contexts/voting` | Modificado (nova entidade `vote_windows`, agregação incremental) |
| Serviço de notificações | Consumido (novo volume no tópico `voting.events`) |
| Pipeline de relatórios | Apenas consumido (sem mudança de schema breaking) |

`Confidence:` 86 · `Origin:` ai_drafted→cto_authored · `Source:` escopo do RP §5 · `Status:` resolved · `Disposition:` answered · `Hint:` —

---

## Impacto Arquitetural

| Área | Impacto | Nota arquitetural |
|---|---|---|
| **Modelo de dados** | Nova tabela `vote_windows` + índice parcial `idx_votes_open_window` | Seguir o padrão `tenant_id` + RLS; índice parcial só sobre janelas abertas |
| **Eventos / mensageria** | +1 evento `vote.window.closed` em `voting.events` | Reusar o tópico; idempotência por `window_id` |
| **Multi-tenancy** | Nenhum novo caminho de vazamento — herda RLS | Testar a policy na nova tabela explicitamente |
| **Performance / Escalabilidade** | Agregação incremental remove o recálculo O(n) por voto | Pré-requisito do guardrail de 500 ms |
| **Observabilidade** | Métrica de latência de propagação por tenant | Histograma `vote_propagation_ms` com label `tenant` |

`Confidence:` 84 · `Origin:` ai_drafted→cto_authored · `Source:` RP §6/§8 + tech-landscape · `Status:` resolved · `Disposition:` answered · `Hint:` —

---

## Integrações Necessárias

| Sistema | Tipo | Protocolo | Viabilidade / Riscos conhecidos |
|---|---|---|---|
| Serviço de notificações | Interno / Evento | AMQP (RabbitMQ) | Viável — risco baixo; monitorar profundidade da fila sob pico |

`Confidence:` 82 · `Origin:` ai_drafted→cto_authored · `Source:` RP §7 + tech-landscape · `Status:` resolved · `Disposition:` answered · `Hint:` —

---

## Build vs. Buy

| Capacidade | Decisão | Rationale | Efeito em custo/prazo |
|---|---|---|---|
| Agendamento de janelas | Reuse | O cron interno (`Oban`) já cobre o caso | Custo zero, sem novo provedor |

`Confidence:` 80 · `Origin:` ai_drafted→cto_authored · `Source:` tech-landscape · `Status:` resolved · `Disposition:` answered · `Hint:` —

---

## Alternativas Consideradas

| Alternativa | Prós | Contras | Por que NÃO foi escolhida |
|---|---|---|---|
| Propagação por polling (cliente busca a cada 1s) | Simples; nenhum evento novo | Latência ≥ 1s; carga linear no DB | Viola o guardrail de 500 ms sob concorrência |
| Recálculo total por voto (status quo) | Já existe | O(n) por voto; não escala em janelas grandes | Não atinge o alvo de latência; substituído por agregação incremental |

`Confidence:` 83 · `Origin:` cto_authored · `Source:` análise CTO · `Status:` resolved · `Disposition:` answered · `Hint:` —

---

## Viabilidade dos NFRs  ·  *(mapeado ao RP, Seção 8)*

| NFR (do RP §8) | Viável? | Como será alcançado / abordagem | Risco / ressalva |
|---|---|---|---|
| Propagação de voto < 500 ms (guardrail) | Com ressalvas | Agregação incremental + propagação por evento `voting.events`; sem polling | Inviável por polling; depende do índice parcial |
| Isolamento total por tenant | Sim | RLS por `tenant_id` herdada na nova tabela | Teste explícito da policy obrigatório |
| Disponibilidade 99.9% | Sim | Sem novo SPOF; degrada para contagem eventual se o broker cair | — |

`Confidence:` 87 · `Origin:` cto_authored · `Source:` RP §8 · `Status:` resolved · `Disposition:` answered · `Hint:` —

---

## Testabilidade e Observabilidade

| Dimensão | Abordagem |
|---|---|
| **Estratégia de teste** | Unit (regras de janela), integração (RLS na nova tabela), e2e (fan-out concorrente medindo latência); regressão na contagem |
| **Dados / ambiente de teste** | Seed multi-tenant (2 tenants); cenário de concorrência (200 votos/s) cobrindo o edge case "janela fecha durante voto" (RP §9) |
| **Telemetria / métricas técnicas** | `vote_propagation_ms` (histograma, label tenant); profundidade da fila `voting.events` |
| **Logs / alertas** | Alerta se p95 de propagação > 400 ms; alerta de backlog do broker |

`Confidence:` 84 · `Origin:` ai_drafted→cto_authored · `Source:` RP §9/§8 · `Status:` resolved · `Disposition:` answered · `Hint:` —

---

## Restrições Inegociáveis (Hard Constraints)

| Restrição | Tipo | Detalhe | Efeito no escopo |
|---|---|---|---|
| Propagação deve ser por evento, não polling | Técnica | Necessário para o guardrail de 500 ms | Nenhum no escopo de produto; é decisão de implementação |
| Índice parcial criado antes do rollout | Plataforma | `idx_votes_open_window` é pré-condição de performance | Adiciona 1 passo ao plano de release |

`Confidence:` 85 · `Origin:` cto_authored · `Source:` análise CTO · `Status:` resolved · `Disposition:` answered · `Hint:` —

---

## Riscos Técnicos e Mitigações

| Risco | Categoria | Probabilidade | Impacto | Mitigação |
|---|---|---|---|---|
| Backlog no broker sob pico derruba latência | Infra | Média | Alto | Autoscaling do consumer + alerta de profundidade |
| Policy RLS não aplicada à nova tabela | Segurança | Baixa | Alto | Teste de integração que falha se a policy faltar |

`Confidence:` 86 · `Origin:` ai_drafted→cto_authored · `Source:` Impacto Arquitetural · `Status:` resolved · `Disposition:` answered · `Hint:` —

---

## Decisões de Arquitetura (ADRs)

| # | Decisão | Rationale | Sign-off do CTO |
|---|---|---|---|
| ADR-001 | Propagação de votos por evento (`voting.events`), não polling | Único caminho viável para o guardrail de 500 ms sob concorrência | ✓ |
| ADR-002 | Agregação incremental de contagem por janela | Remove o recálculo O(n) por voto; pré-requisito de performance | ✓ |
| ADR-003 | Reusar RLS por `tenant_id` na `vote_windows` (reused_from_KB) | Padrão de isolamento já validado no tech-landscape | ✓ |

`Confidence:` 88 · `Origin:` reused_from_KB→cto_authored · `Source:` tech-landscape (ADR-003) + proposta da IA · `Status:` resolved · `Disposition:` answered · `Hint:` —

---

## Avaliação de Esforço e Custo (firme)

### Esforço de Desenvolvimento

| Área | Estimativa | Senioridade |
|---|---|---|
| Backend (tabela, RLS, agregação, evento) | 6 dias | Sênior |
| QA (concorrência + RLS) | 2 dias | QA |
| **Total** | **8 dias** | |

### Impacto de Infraestrutura

Nenhum provisionamento novo — reusa Postgres e RabbitMQ existentes.

### Impacto de Custo de Terceiros

Nenhum.

### Impacto de Custo Operacional Recorrente

Marginal: +volume de mensagens em `voting.events` (estimado < 2% do tráfego atual).

### Avaliação de TCO

Cria uma fundação reutilizável: a agregação incremental beneficia toda contagem de votos, não só esta feature.

`Confidence:` 81 · `Origin:` cto_authored · `Source:` decomposição CTO · `Status:` resolved · `Disposition:` answered · `Hint:` refinável pelo Tech Lead no TB

---

## Caminho de Discovery (se uma incógnita técnica bloqueia a conclusão)

—

`Confidence:` 100 · `Origin:` cto_authored · `Source:` — · `Status:` resolved · `Disposition:` decided · `Hint:` nenhuma incógnita bloqueia o fechamento

<!-- END OF DOCUMENT -->
