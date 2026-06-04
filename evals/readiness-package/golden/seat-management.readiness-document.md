# Readiness Package — Gestão de Assentos Self-Service para Admins Enterprise
<!-- rev: 1 · updated: 2026-06-03 -->

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
| **Versão** | v1 |
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
| v1 | 2026-06-03 | Ana Ribeiro (PO) | Rascunho | Submissão inicial com base no intake INT-2026-014. |

---

## Prontidão herdada e dispositions em aberto
<!-- intake: id=inherited-readiness; blocks=false; min-confidence=0; kind=derived; inputs=exec-summary,context-problem,objectives,personas,scope,metrics,release-criteria,risks -->

> Resumo do que o Intake entregou e do que continua *soft* na entrada da execução.
> Premissas, incógnitas de Discovery e respostas delegadas que sobreviveram à
> racionalização precisam estar visíveis — não enterradas nas seções. Se uma
> premissa carregada aqui se provar falsa durante a execução, a demanda deve ser
> reavaliada (o mesmo gatilho de retriagem do intake se aplica downstream).

| Campo | Valor |
|---|---|
| **Readiness Score no handoff do Intake** | 82 % |
| **Premissas ainda a validar** | Volume de 240 tickets/trimestre é representativo do custo total; impacto no CS confirmado mas breakdown por conta não disponível |
| **Incógnitas de Discovery** | Breakdown de tickets por conta (abertas — CS pode extrair em ~1 semana) |
| **Requisitos delegados (com dono)** | Arquitetura de provisionamento sync/async (CTO — Technical Assessment TA-2026-014) |

---

## Seção 1 — Resumo Executivo
<!-- intake: id=exec-summary; blocks=true; min-confidence=70; kind=capture -->
> Rubric: 2–4 parágrafos curtos. Qual é o problema, o que será construído e qual é
> o resultado esperado de negócio. Deve ser legível por qualquer stakeholder sem
> contexto adicional. Herdado e expandido do intake quando possível.

Admins enterprise não conseguem adicionar ou remover assentos sem abrir um ticket de suporte. O lead time de 1–3 dias úteis cria dependência operacional que gera fricção em ondas de onboarding e em ciclos de renovação de contrato. Em Q1 2026, 240 tickets (18% do volume enterprise) foram desse tipo.

Esta entrega cria um painel de gestão de assentos self-service no produto, permitindo que admins com a role `billing_admin` adicionem e removam assentos imediatamente, com preview da fatura e log de auditoria dos últimos 90 dias. O suporte fica como canal de exceção, não de operação rotineira.

O resultado esperado é a eliminação de pelo menos 75% dos tickets de seat management em 90 dias pós-rollout, reduzindo o volume trimestral de 240 para ≤ 60 tickets, e liberando a equipe de CS para demandas de maior complexidade.

`Confidence: 82 · Origin: inherited · Source: intake INT-2026-014 §problem + support export Q1 2026 · Status: resolved · Disposition: inherited · Hint: herdado do intake a 88; rebaixado levemente por ausência de breakdown por conta — CS pode refinar para ~90`

---

## Seção 2 — Contexto e Problema (a dor, não a solução)
<!-- intake: id=context-problem; blocks=true; min-confidence=80; kind=capture -->
> Rubric: cenário atual, limitações, dor do cliente e impacto de negócio — o
> problema, nunca a solução. Se descreve uma solução ("construir X"), NÃO está
> satisfeita: reformule para a dor subjacente. Herdada do intake quando possível.

### Cenário Atual

Toda alteração de assento (adição ou remoção de licença) exige abertura de ticket para o CS. O admin não tem acesso direto à gestão de licenças no produto; o processo passa inteiramente pelo suporte humano, que executa a mudança no backend e confirma por e-mail.

### Limitações

- Sem interface self-service: o admin não pode alterar assentos sem intermediário.
- Visibilidade zero: o admin não vê o estado atual das licenças nem o histórico de alterações sem pedir ao CS.
- Latência estrutural: mesmo com SLA interno de 1 dia útil, o CS acumula filas em ondas de onboarding e o lead time real chega a 3 dias.
- Sem preview de custo: o admin não consegue estimar o impacto financeiro de uma alteração antes de abrir o ticket.

### Dor do Cliente

Admins enterprise vivem uma dependência operacional: qualquer mudança de time (contratação, desligamento, reestruturação) exige uma solicitação de suporte. Em empresas com alta rotatividade ou onboarding contínuo, isso gera entre 5–10 tickets por admin por mês. A frustração não é com o CS — é com a ausência de autonomia para uma operação que o admin considera trivial.

### Impacto de Negócio

- 240 tickets de seat management em Q1 2026 (18% do volume total enterprise).
- Custo estimado de CS por ticket: R$ 120–180 (tempo de analista + overhead). Estimativa trimestral: R$ 29k–43k em custo de suporte evitável.
- Risco de churn: 3 contas enterprise sinalizaram insatisfação com o processo em entrevistas de renovação Q4 2025.
- Bloqueio de expansão: admins que não conseguem adicionar assentos rapidamente adiaram contratações — receita de expansão potencialmente represada.

`Confidence: 86 · Origin: inherited · Source: intake INT-2026-014 §problem + support export Q1 2026 + entrevistas CS Q4 2025 · Status: resolved · Disposition: inherited · Hint: baseline de 240 tickets/trimestre é firme; estimativa de custo por ticket é aproximada — CS pode refinar`

---

## Seção 3 — Objetivos e Resultado Esperado
<!-- intake: id=objectives; blocks=true; min-confidence=70; kind=capture -->
> Rubric: objetivos numerados e observáveis que esta entrega deve alcançar após o
> release. Cada objetivo deve ser verificável: se não pode ser medido ou observado,
> não está satisfeito. Mínimo dois objetivos.

1. **Reduzir tickets de seat management em ≥ 75%** em 90 dias pós-rollout (de ~240 para ≤ 60 por trimestre), medido no painel de CS.
2. **Habilitar self-service para ≥ 85% das alterações de assento** sem intervenção do CS, medido pela proporção de eventos de seat change originados no painel vs. tickets.
3. **Não piorar a confiabilidade de faturamento**: taxa de erro de cobrança (cobrança sem provisionamento ou vice-versa) deve permanecer < 0,1% após o rollout.
4. **Fornecer rastreabilidade de auditoria**: 100% das alterações de assento realizadas pelo painel devem aparecer no log de auditoria com atribuição de usuário, timestamp e delta (N→M).

`Confidence: 80 · Origin: inherited · Source: intake INT-2026-014 §objectives + suporte export Q1 2026 · Status: resolved · Disposition: inherited · Hint: targets de redução baseados em intake; confirmar com CS 30 dias pós-rollout`

---

## Seção 4 — Personas Impactadas / Jobs-to-be-done
<!-- intake: id=personas; blocks=true; min-confidence=70; kind=capture -->
> Rubric: para cada persona, o job-to-be-done (o que está tentando realizar) e como
> é impactada por esta entrega. Sem persona definida, scope e critérios de aceite
> não têm âncora. Herdado do intake (campo reach) quando possível.

| Persona | Job-to-be-done | Impacto desta entrega |
|---|---|---|
| **Admin Enterprise** (role `billing_admin`) | Ajustar o número de licenças do time de forma autônoma e imediata, sem depender de terceiros. | Passa a ter controle direto: adiciona/remove assentos no painel, vê preview de custo, consulta histórico de alterações sem abrir ticket. |
| **Analista de CS** | Resolver solicitações de suporte de alta complexidade; não querer desperdício em operações triviais. | Fica liberado de ~240 tickets/trimestre repetitivos; atua como escalonamento de exceção. |
| **Contador / Responsável Financeiro** (viewer, sem ação) | Entender o custo de licenças e reconciliar cobranças. | Ganha visibilidade no log de auditoria e preview de fatura; sem necessidade de solicitar extratos ao CS. |

`Confidence: 75 · Origin: inherited · Source: intake INT-2026-014 §reach + entrevistas CS Q4 2025 · Status: resolved · Disposition: inherited · Hint: persona financeiro inferida; validar se role viewer está no escopo deste release ou é fase 2`

---

## Seção 5 — Escopo Incluído e Excluído
<!-- intake: id=scope; blocks=true; min-confidence=75; kind=capture -->
> Rubric: protege o downstream de scope creep. Deve listar explicitamente o que
> está FORA, não apenas o que está dentro. Itens adiados alimentam o Roadmap
> (Seção 14). Sem "excluído" preenchido, a seção NÃO está satisfeita.

### Incluído

- Painel de gestão de assentos para usuários com role `billing_admin`.
- Ação de adição de assentos com confirmação de preview de custo (próxima fatura).
- Ação de remoção de assentos com validação de usuários ativos (bloqueio se assento em uso).
- Log de auditoria das últimas 90 dias com eventos de seat change (quem alterou, de N para M, data/hora).
- Feedback imediato (≤ 60 s) após adição de assento: assento ativo + preview atualizado.
- Mensagem de erro explicativa quando tentativa de remoção violaria a regra de usuários ativos.

### Excluído

- Transferência de assentos entre organizações ou contas — fora de escopo (requer lógica de multi-tenancy).
- Self-service de upgrades/downgrades de plano — gerenciados por contrato; processo separado.
- API pública para automação de seat management por scripts do admin — fase 2.
- Notificações por e-mail automáticas ao alterar assentos — fase 2.
- Gestão de roles (quem tem `billing_admin`) — fora de escopo; gerenciado pelo Owner da conta.
- Integração com ERP/HR systems para sincronização automática de headcount — fase 3.

### Adiado (fases futuras)

- API pública de seat management (fase 2) — alimenta casos de automação de onboarding.
- Notificações e-mail/Slack ao alterar assentos (fase 2) — melhora rastreabilidade para gestores.
- Sincronização com sistemas de HR para seat management automatizado (fase 3).

`Confidence: 80 · Origin: inherited · Source: intake INT-2026-014 §scope + alinhamento PO/CS · Status: resolved · Disposition: inherited · Hint: exclusões validadas com CS; API pública é pedido recorrente mas fora do MVPs`

---

## Seção 6 — Regras de Negócio e Fluxos
<!-- intake: id=business-rules; blocks=true; min-confidence=80; kind=capture -->
> Rubric: regras, validações e transições de estado que governam a funcionalidade.
> Cada regra deve ser verificável e atômica. Fluxos de transição de estado devem
> cobrir caminhos de erro, não apenas o caminho feliz.

### Regras de Gestão de Assentos

1. Somente usuários com a role `billing_admin` na conta podem executar ações de adicionar ou remover assentos. Usuários com outras roles veem o painel em modo leitura (somente log).
2. Não é permitido remover assentos se o número resultante de assentos for menor que o número atual de usuários ativos (status = `active` ou `invited`). A validação ocorre no servidor antes de qualquer cobrança.
3. A adição de um assento deve ser refletida no estado da conta em no máximo 60 segundos após confirmação pelo admin.
4. Toda ação de seat change (adição ou remoção) deve gerar um evento de auditoria imutável contendo: ID do admin executor, timestamp UTC, valor anterior (N) e novo valor (M), e canal de origem (`self_service_panel`).
5. O preview de custo mostrado antes da confirmação deve refletir o impacto na próxima fatura com base no plano vigente e no ciclo de cobrança atual (proporcional se ciclo em andamento).
6. O log de auditoria deve reter eventos por no mínimo 90 dias, acessível apenas a usuários com role `billing_admin` ou `owner` na conta.
7. Falhas intermediárias (timeout, erro de gateway de pagamento) não podem resultar em estado inconsistente: ou o assento é provisionado E cobrado, ou nenhum dos dois ocorre (atomicidade). Regra de idempotência: reenvio do mesmo request de adição dentro de 5 minutos não deve gerar dupla cobrança.

### Fluxo de Transição de Estado — Adição de Assento

```text
[Admin inicia adição]
       │
       ▼
[Sistema valida role billing_admin]
       │ falha → Erro 403: "Permissão insuficiente"
       ▼
[Sistema calcula preview de custo (próxima fatura)]
       │
       ▼
[Admin confirma adição]
       │ cancela → nenhuma alteração
       ▼
[Sistema tenta provisionar assento + registrar cobrança]
       │ erro de gateway → rollback; exibe "Falha temporária — tente novamente"
       │ timeout > 60s → rollback; exibe "Tempo excedido — nenhuma alteração foi feita"
       ▼
[Assento ativo; evento de auditoria gerado]
       │
       ▼
[Preview de fatura atualizado na tela]
```

`Confidence: 82 · Origin: ai_drafted · Source: escopo §5 + regras de billing da plataforma (inferidas) + golden-example.md · Status: draft · Disposition: ai_drafted · Hint: regras 2, 4, 7 e fluxo de erro validados conceitualmente pelo PO; regra de idempotência (item 7) precisa de confirmação com CTO no TA`

---

## Seção 7 — User Stories + Critérios de Aceite
<!-- intake: id=user-stories; blocks=true; min-confidence=80; kind=capture -->
> Rubric: uma história por bloco de valor, "Como [persona], quero [ação], para
> [benefício]"; critérios de aceite em Given/When/Then, verificáveis por não-dev,
> com limites específicos. origin=ai_drafted no draft pass; o PO confirma.

### ST-001 — Self-service de adição de assento

**Como** admin enterprise com role `billing_admin`,
**quero** adicionar assentos diretamente no painel de faturamento,
**para que** novos membros do time possam ser provisionados imediatamente, sem esperar o suporte.

**Critérios de Aceite:**

- *Given* um admin autenticado com role `billing_admin` na tela de gestão de assentos *when* ele aumenta o número de assentos em 1 e confirma *then* o novo assento fica com status `active` em até 60 segundos e o preview da próxima fatura é atualizado na mesma tela antes de o admin encerrar a sessão.
- *Given* o mesmo admin na tela de confirmação *when* ele visualiza o preview de custo antes de confirmar *then* o valor exibido é proporcional ao ciclo de faturamento corrente (dias restantes no mês/ciclo atual).
- *Given* uma falha temporária no gateway de pagamento durante a confirmação *when* o sistema detecta o erro *then* nenhum assento é provisionado, nenhuma cobrança é lançada, e o admin vê a mensagem "Falha temporária — tente novamente" sem necessidade de contatar o suporte.

### ST-002 — Self-service de remoção de assento

**Como** admin enterprise com role `billing_admin`,
**quero** remover assentos no painel de faturamento,
**para que** eu possa ajustar custos de licença quando membros saem do time.

**Critérios de Aceite:**

- *Given* um admin autenticado tentando reduzir assentos abaixo do número de usuários com status `active` ou `invited` *when* ele tenta confirmar a remoção *then* o sistema bloqueia a ação antes de qualquer cobrança e exibe mensagem indicando quantos usuários precisam ser desativados primeiro (ex: "3 usuários ativos precisam ser removidos antes de reduzir assentos").
- *Given* um admin removendo assentos quando o número resultante ≥ usuários ativos *when* ele confirma *then* os assentos são reduzidos, evento de auditoria é gerado, e a redução aparece no preview da próxima fatura.

### ST-003 — Log de auditoria de alterações de assento

**Como** admin enterprise,
**quero** ver o histórico das alterações de assentos dos últimos 90 dias,
**para que** eu possa auditar mudanças sem depender do suporte ou solicitar extratos.

**Critérios de Aceite:**

- *Given* um admin na tela de auditoria *when* ele abre o log de seat changes *then* vê cada evento em ordem cronológica reversa, com: nome/e-mail do executor, valor anterior (N), novo valor (M), data e hora UTC.
- *Given* o mesmo log *when* o admin filtra por período *then* apenas eventos dentro do intervalo selecionado são exibidos, com contagem visível.
- *Given* um usuário sem role `billing_admin` ou `owner` *when* tenta acessar o log de auditoria *then* recebe erro 403 e não vê nenhum dado de seat change.

`Confidence: 80 · Origin: ai_drafted · Source: escopo §5 + regras §6 + golden-example.md · Status: draft · Disposition: ai_drafted · Hint: PO revisou ST-001 e ST-002; AC verificáveis por QA sem acesso ao código; ST-003 derivado do req de auditoria`

---

## Seção 8 — Requisitos Não-Funcionais (NFRs)
<!-- intake: id=nfrs; blocks=true; min-confidence=70; kind=capture -->
> Rubric: preencher apenas as dimensões aplicáveis (checklist ISO/IEC 25010 — não
> forçar as irrelevantes). O PO descreve o requisito de qualidade; viabilidade e
> *como* são do Technical Assessment. Sem ao menos uma dimensão preenchida,
> a seção NÃO está satisfeita.

*(ISO/IEC 25010 — apenas dimensões aplicáveis)*

| Dimensão | Requisito | Como será verificado |
|---|---|---|
| **Performance efficiency** | A confirmação de adição de assento (do clique de confirmar até o assento estar `active`) deve ser devolvida ao admin em ≤ 60 s (p95) sob carga normal da plataforma. | Teste de fumaça pós-deploy: 10 adições consecutivas medidas; p95 < 60 s. |
| **Reliability** | O fluxo de seat management deve ter disponibilidade ≥ 99,5% mensais. Falhas intermediárias não podem resultar em estado inconsistente: cobrança sem provisionamento ou provisionamento sem cobrança. | Monitoramento de uptime (alerta se < 99,5%). Teste de injeção de falha: simular erro de gateway e verificar que nem cobrança nem provisionamento ocorrem. |
| **Security** | Somente usuários com role `billing_admin` ou `owner` podem executar ou visualizar seat changes. Cada ação deve ser registrada em audit trail imutável com atribuição de usuário e timestamp. | Teste de permissão: usuário sem a role não consegue acessar ações de seat management (HTTP 403). Log de auditoria não pode ser deletado nem alterado por nenhuma role. |
| **Usability** | Um admin que nunca usou o painel deve conseguir adicionar um assento e localizar o log de auditoria sem treinamento formal ou consulta à documentação. | Teste de usabilidade com 3 admins novos: taxa de conclusão ≥ 90% sem assistência. |

O PO descreve o *requisito de qualidade*. Se os targets são atingíveis com a arquitetura atual ou exigem mudança de plataforma é questão para o Technical Assessment (TA-2026-014).

`Confidence: 70 · Origin: ai_drafted · Source: escopo §5 + SLA padrão da plataforma + golden-example.md · Status: low_confidence · Disposition: assumption · Hint: targets são estimativa do PO; viabilidade e implementação são do CTO no TA — não assumir factibilidade`

---

## Seção 9 — Edge Cases e Modos de Falha
<!-- intake: id=edge-cases; blocks=true; min-confidence=70; kind=capture -->
> Rubric: estados de erro, timeouts, permissões, concorrência. Para features de IA:
> comportamento do modelo e baixa-confiança. Primeira classe — não rodapé. Cada
> item descreve o comportamento esperado do sistema (não apenas o que pode dar errado).

- **Admin sem role `billing_admin`**: o painel de gestão de assentos não exibe os controles de adição/remoção; o usuário vê apenas o log de auditoria em modo leitura (se tiver role `owner`) ou uma mensagem de acesso negado (qualquer outra role). Nenhuma ação é possível.
- **Tentativa de remoção abaixo do mínimo de usuários ativos**: o sistema valida server-side antes de processar qualquer cobrança. A interface bloqueia o botão de confirmação e exibe a mensagem de erro com o número exato de usuários que precisam ser desativados.
- **Concorrência: dois admins adicionando assentos simultaneamente**: o sistema deve garantir que ambas as operações sejam processadas corretamente; o estado final deve refletir a soma das duas adições. Não deve haver condição de corrida que resulte em apenas uma das adições sendo efetivada.
- **Concorrência: remoção simultânea a um usuário sendo convidado**: se um usuário aceita convite (status `invited` → `active`) enquanto um admin tenta remover o último assento disponível, o sistema deve revalidar o número de usuários ativos no momento da confirmação e bloquear a remoção se necessário.
- **Timeout do gateway de pagamento (> 30 s)**: o sistema faz rollback completo; nenhum assento é provisionado e nenhuma cobrança é lançada. O admin vê mensagem "Tempo excedido — tente novamente" com opção de contatar o suporte se o problema persistir.
- **Idempotência — reenvio acidental**: se o mesmo request de adição for reenviado dentro de uma janela de 5 minutos (ex: duplo clique, retry automático do browser), o sistema deve reconhecer o request duplicado e não gerar segunda cobrança nem segundo evento de provisão.
- **Conta com trial ou status especial**: admins de contas em período de trial ou com cobrança suspensa devem ver mensagem explicando que alterações de assento requerem contato com o CS enquanto a conta estiver nesse estado. O painel não deve permitir ações que alterem o ciclo de cobrança enquanto o status não for normalizado.
- **Log de auditoria vazio (conta nova)**: a tela de auditoria exibe estado vazio com mensagem "Nenhuma alteração de assento registrada nos últimos 90 dias" — sem erro, sem dado confuso.

`Confidence: 72 · Origin: ai_drafted · Source: regras §6 + padrões de billing + analogia com features similares · Status: draft · Disposition: ai_drafted · Hint: casos de concorrência precisam de confirmação com CTO no TA; os demais são derivados das regras de negócio`

---

## Seção 10 — Métricas de Sucesso (primária · secundária · guardrail)
<!-- intake: id=metrics; blocks=true; min-confidence=70; kind=capture -->
> Rubric: valores projetados — o baseline que metrics.md confronta com o medido
> pós-rollout. Inclua indicadores leading e lagging e ao menos um guardrail (a
> métrica que não pode piorar). Cada meta carrega a confiança da projeção.

| Tipo | Métrica | Baseline | Target (90 dias pós-rollout) | Confiança da projeção |
|---|---|---|---|---|
| **Primária (lagging)** | Tickets de seat management / trimestre | 240 | ≤ 60 (−75%) | 62% |
| **Secundária (leading)** | % de seat changes feitas pelo admin sem suporte | ~0% | ≥ 85% | 70% |
| **Secundária (leading)** | Tempo médio para provisionamento de assento (ticket → ativo) | 1–3 dias úteis | ≤ 60 segundos | 80% |
| **Guardrail** | Taxa de erro de faturamento (cobrança sem provisionamento ou vice-versa) | < 0,1% | não piorar (< 0,1%) | 80% |
| **Guardrail** | CSAT de CS (tickets enterprise) | 4,2/5 | não piorar (≥ 4,0/5) | 55% |

`Confidence: 70 · Origin: inherited · Source: support export Q1 2026 + intake INT-2026-014 §metrics · Status: low_confidence · Disposition: inherited · Hint: baseline de 240 tickets/trimestre é firme; projeção de −75% é estimativa — confrontar com dado real 60 e 90 dias pós-rollout; CSAT baseline precisa de confirmação com CS`

---

## Seção 11 — Critérios de Sucesso e Aceite (do release)
<!-- intake: id=release-criteria; blocks=true; min-confidence=70; kind=capture -->
> Rubric: indicadores de alto nível que definem "concluído e valioso" para este
> release — distintos das métricas contínuas da Seção 10. Deve cobrir ao menos
> as dimensões Negócio, Qualidade e UX. Critérios genéricos ("funciona bem") NÃO
> estão satisfeitos: exija valor alvo mensurável.

| Critério | Tipo | Indicador | Valor alvo |
|---|---|---|---|
| Admins conseguem adicionar assentos sem suporte | Negócio | Taxa de conclusão do fluxo de adição sem erro ou contato com CS | ≥ 95% nas primeiras 2 semanas pós-rollout |
| Faturamento permanece íntegro | Qualidade | Taxa de inconsistência billing/provisionamento nos primeiros 30 dias | 0 ocorrências de cobrança sem provisionamento ou vice-versa |
| Auditoria está disponível e completa | Compliance | % de seat changes com evento de auditoria correspondente | 100% dos eventos registrados com atribuição correta |
| Fluxo é concluído sem suporte | UX | Taxa de admins que completam adição/remoção sem abrir ticket de suporte dentro de 7 dias | ≥ 90% |
| Performance dentro do SLA | Qualidade | p95 de tempo de confirmação de adição de assento | ≤ 60 segundos |

`Confidence: 75 · Origin: inherited · Source: intake INT-2026-014 §success-criteria + alinhamento PO · Status: resolved · Disposition: inherited · Hint: critério de faturamento é não-negociável; critério de UX requer monitoramento ativo nas 2 primeiras semanas`

---

## Seção 12 — Riscos e Dependências (de produto e negócio)
<!-- intake: id=risks; blocks=true; min-confidence=70; kind=capture -->
> Rubric: riscos de produto, negócio, adoção, externos e compliance. Riscos
> técnicos migram para o Technical Assessment. Cada risco tem probabilidade,
> impacto e mitigação. Dependências de produto/negócio listadas separadamente.

| Risco | Tipo | Probabilidade | Impacto | Mitigação |
|---|---|---|---|---|
| Admins não adotam o painel e continuam abrindo tickets por hábito | Adoção | Média | Médio | Campanha de comunicação pré-rollout; CS orienta ativamente nas primeiras 4 semanas; tutorial in-app no primeiro acesso ao painel |
| Contas enterprise com contratos especiais têm regras de billing fora do padrão e o preview de custo fica incorreto | Produto | Baixa | Alto | Mapear contas com billing especial antes do rollout; exibir disclaimer "confirme com CS se você tem contrato personalizado" para essas contas na fase 1 |
| Mudança de plano de faturamento do provedor de pagamento impacta a lógica de proporcionalidade | Externo | Baixa | Médio | Monitorar changelogs do provedor; lógica de proporcionalidade isolada em módulo para facilitar ajuste |
| Regulatório: LGPD — log de auditoria contém dados de usuários (nome/e-mail) | Compliance | Baixa | Alto | Alinhar com DPO antes do rollout: confirmar que log de auditoria está dentro da política de retenção de dados vigente; incluir na DPA se necessário |
| Resistência do CS à mudança: equipe pode perceber a feature como ameaça ao volume de trabalho | Adoção | Baixa | Baixo | Comunicação interna antecipada posicionando como liberação para trabalho de maior valor; sem impacto em headcount |

**Dependências (de produto/negócio):**
- Technical Assessment TA-2026-014 (CTO) — avaliação da arquitetura de provisionamento sync/async e da lógica de idempotência.
- Alinhamento com DPO sobre retenção de dados no log de auditoria (LGPD).
- Mapeamento de contas com billing especial (CS/Finance) — necessário antes do rollout para definir tratamento de edge cases de proporcionalidade.

`Confidence: 72 · Origin: inherited · Source: intake INT-2026-014 §risks + alinhamento PO/CS · Status: draft · Disposition: inherited · Hint: risco de compliance (LGPD) requer ação pré-rollout; risco técnico de idempotência migra para o TA`

---

## Seção 13 — Avaliação Preliminar de Esforço e Custo
<!-- intake: id=effort-estimate; blocks=false; min-confidence=0; kind=capture -->
> Rubric: somente uso interno — o chute do PO para sustentar sequenciamento. O
> número firme vem do CTO no Technical Assessment. Não é compromisso contratual
> nem material para cliente. Confiança esperada: baixa (ai_drafted ou po_authored
> sem dados firmes).

| Área | Estimativa preliminar | Confiança |
|---|---|---|
| Backend (painel de gestão + log de auditoria + regras de billing) | 8–12 dias | 35% |
| Frontend (painel de gestão + log de auditoria + preview de fatura) | 5–8 dias | 35% |
| QA (testes de billing, permissão, auditoria, edge cases) | 3–5 dias | 40% |
| **Total preliminar** | **16–25 dias** | 35% |

**Sinais de custo a confirmar pelo CTO:** lógica de idempotência pode exigir mudança de arquitetura de billing (potencial opex recorrente se usar fila); integração com gateway de pagamento pode ter custo de transação adicional.

`Confidence: 35 · Origin: po_authored · Source: analogia com features de billing de complexidade similar · Status: low_confidence · Disposition: assumption · Hint: estimativa do PO sem dados de velocidade do time; número firme vem do CTO no TA-2026-014`

---

## Seção 14 — Roadmap Sugerido
<!-- intake: id=roadmap; blocks=false; min-confidence=0; kind=capture -->
> Rubric: visão de sequenciamento de valor além deste release. Items adiados da
> Seção 5 alimentam fases futuras. MVP é este release; Fase 2 e Fase 3 são
> backlog futuro. Não é compromisso de entrega.

### MVP (este release)

- Painel self-service de adição e remoção de assentos (role `billing_admin`).
- Preview de custo antes da confirmação.
- Log de auditoria dos últimos 90 dias.
- Validações de consistência billing/provisionamento.
- Tratamento de edge cases de permissão e estado de conta.

### Fase 2 (backlog futuro)

- API pública de seat management para automação por scripts do admin.
- Notificações por e-mail/Slack ao adicionar ou remover assentos.
- Dashboard de tendência de uso de assentos (crescimento, pico, ociosidade).

### Fase 3 (backlog futuro)

- Integração com sistemas de HR (SCIM/HRIS) para sincronização automática de headcount e seat management.
- Sugestão proativa de ajuste de assentos baseada em padrões de uso (seats ociosos, crescimento projetado).

`Confidence: 60 · Origin: po_authored · Source: itens adiados §5 + entrevistas com admins Q4 2025 · Status: draft · Disposition: po_authored · Hint: roadmap reflete wishlist do PO; priorização de fases é tentativa — depende do TA e feedback dos primeiros admins`

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
| **Escalada requisitada?** | Sim — NFR de reliability (atomicidade billing ↔ provisionamento) e lógica de idempotência requerem avaliação de arquitetura |

`Confidence: 40 · Origin: po_authored · Source: RP draft pass · Status: low_confidence · Disposition: deferred · Hint: TA pendente — tech-assessment skill ainda não existe; congelamento do RP provisório até o CTO assinar o TA-2026-014`

<!-- END OF DOCUMENT -->
