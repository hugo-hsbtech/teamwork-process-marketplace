# Documento do Submitter — Queue Voting (Fila de Votação)

> **Este é o documento do Submitter** — o primeiro artefato da jornada (`00`) e o entregável da persona Submitter. Ele **tangibiliza** o modelo de [`personas/01-submitter.md`](../personas/01-submitter.md): o raciocínio (requisitos de compliance, geração de ToDos, fórmula de score) vive na persona; este documento o **instancia** por demanda, na **linguagem do Submitter** — problema, valor, dor, oportunidade. Cada resposta carrega o quão sólida ela é e de onde veio: a camada de confiança viaja *com* a captura.
>
> **Jornada:** `00 Documento do Submitter` → [`01 Intake Record (PO — triagem)`](./01-intake-record-queue-voting.md) → [`02 Readiness Package (PO)`](./02-readiness-package-queue-voting.md) → `03 Technical Assessment — não requisitado` → [`04 PRD (PO+CTO → PM)`](./04-prd-queue-voting.md). Ver [`README.md`](./README.md).
>
> **Nada antecede este documento como artefato.** O que vem antes é **sinal cru** — uma chamada trimestral de revisão com o cliente — que **não é artefato**. Esse sinal entra *aqui* como evidência/fonte (disposição `inferred`, com `source`); é a **captura** que o transforma neste primeiro documento formal.
>
> **Handoff:** congela quando `gateReady = true` (todo requisito bloqueante resolvido por uma disposição honesta) e é entregue ao **PO**, que o formaliza e tria no [`01 Intake Record`](./01-intake-record-queue-voting.md).

## As duas lentes (toda demanda é lida pelas duas ao mesmo tempo)

> Ver [`personas/01-submitter.md` §2](../personas/01-submitter.md). Os ToDos vivem onde as lentes se cruzam: "dado o que *esta* demanda significa, o que o contrato ainda precisa?"

| Lente | O que é | Onde aparece neste documento |
|---|---|---|
| **Contrato** (determinístico) | Os requisitos fixos de compliance que toda demanda precisa satisfazer para avançar | **Resumo de Prontidão** + os requisitos numerados (score + pendências) |
| **Semântica** (contextual) | O que *esta* demanda significa: falta de controle do facilitador no fluxo de estimativas — a dor real é a cerimônia desgovernada, não a ausência de um "botão" | **Enunciado do Problema**, **Impacto**, **Indicadores de Valor** e suas tensões |

## Metadados

| Campo | Valor |
|---|---|
| **Demanda** | Queue Voting (Fila de Votação) |
| **Registrado por** | Ana Costa (Customer Success) |
| **Data de captura** | 2026-03-12 |
| **Status** | Pronto para handoff (`gateReady`) |
| **Intake Record vinculado** | INT-2026-001 |

## Histórico de Revisão

| Versão | Data | Evento | Resumo |
|---|---|---|---|
| v1 | 2026-03-12 | Captura iniciada | Ana Costa registrou a demanda a partir de chamada trimestral de revisão com Banco Meridional. Todos os requisitos bloqueantes resolvidos. Handoff ao PO no mesmo dia. |

---

## Resumo de Prontidão (Readiness)

> Snapshot da captura. O score é derivado dos requisitos abaixo; `low_confidence` conta como parcial. A demanda só é entregue ao PO quando todos os requisitos bloqueantes estão resolvidos (`gateReady = Sim`).

| Campo | Valor |
|---|---|
| **Readiness Score** | 87 % |
| **Gate liberado (gateReady)** | Sim |
| **Requisitos bloqueantes pendentes** | — (todos os 4 bloqueantes resolvidos) |
| **Dispositions** | 5 respondidos · 1 inferido · 3 premissas · 0 discovery · 0 delegados |

### Legenda de confiança (aplica-se a cada seção respondida)

| Atributo | Valores |
|---|---|
| **Confiança** | 0–100 |
| **Fonte** | Submitter direto · Documento anexo (p.X) · Inferido · Premissa · Outro stakeholder |
| **Status** | Vazio · Baixa confiança · Resolvido |
| **Disposição** | Respondido · Inferido · Premissa (a validar) · Discovery (a investigar) · Delegado (dono: __) |
| **Hint** | Por que a confiança está baixa / o que a elevaria |

> **"Não sei" não bloqueia.** Um requisito atinge prontidão por qualquer disposição honesta — inclusive "ninguém sabe ainda, e este é o plano" (Discovery) ou "estamos assumindo X" (Premissa). Ver [`personas/01-submitter.md` §6](../personas/01-submitter.md).

---

## Origem  ·  *(Requisito 2 — Originador e contexto)*

| Campo | Valor |
|---|---|
| **Fonte** | Cliente |
| **Cliente / Solicitante** | Banco Meridional |
| **Originador e contexto** | Scrum Masters / facilitadores do Banco Meridional, chamada trimestral de revisão com CS em 2026-03-12. A dor foi levantada espontaneamente durante a pauta de renovação de contrato: "sem isso fica difícil justificar a renovação para os squads que ainda não aderiram." |
| **Reportado via** | Chamada trimestral de revisão (CS → cliente) |

`Confiança:` 95 · `Fonte:` Submitter direto (Ana Costa, presente na chamada) · `Status:` Resolvido · `Disposição:` Respondido · `Hint:` —

---

## Tipo

- [x] Funcionalidade
- [ ] Bug
- [ ] Melhoria
- [ ] Compliance
- [ ] Integração
- [ ] Operacional

---

## Enunciado do Problema  ·  *(Requisito 1 — bloqueia gate)*

> Qual a dor existente? Descreva o problema, não a solução. Se o enunciado contém solução proposta, ele volta para reformulação.

Durante cerimônias de sprint planning, os times do Banco Meridional utilizam a plataforma para estimar histórias de usuário. O facilitador (Scrum Master) não tem como controlar quais histórias serão apresentadas e em que ordem — todos os participantes veem o backlog completo simultaneamente.

A consequência direta: participantes leem itens futuros antes da hora, formam opiniões antecipadas e desestabilizam o fluxo de estimativa. A cerimônia perde cadência. Para contornar isso, os facilitadores enviam uma história por vez via chat — um workaround que adiciona 15–20 minutos de overhead por sessão.

Há uma segunda camada do problema: os votos aparecem em tempo real conforme são submetidos. Participantes que votam por último copiam os primeiros votos que veem, criando viés de ancoragem e degradando a qualidade das estimativas.

`Confiança:` 92 · `Fonte:` Submitter direto (relatado pelos Scrum Masters na chamada) · `Status:` Resolvido · `Disposição:` Respondido · `Hint:` —

---

## Quem é Impactado (Alcance)  ·  *(Requisito 3 — bloqueia gate)*

> Personas, segmentos ou times que sentem essa dor. É o "Reach" dos indicadores de valor.

| Persona / Segmento | Como é impactado |
|---|---|
| Scrum Masters / Facilitadores do Banco Meridional | Perdem o controle do fluxo da cerimônia. Recorrem a workarounds manuais custosos. São os usuários diretos que solicitam a mudança. |
| Desenvolvedores / Votantes do Banco Meridional | Expostos a viés de ancoragem. Estimativas menos precisas. Cerimônias mais longas. |
| 3 squads pendentes (não ativos na plataforma) | A ausência desta funcionalidade é o bloqueador de adoção citado explicitamente na chamada. |
| CS (Ana Costa) | Carrega o risco de renovação do maior contrato enterprise da carteira. |

`Confiança:` 88 · `Fonte:` Submitter direto + inferido a partir do contexto de conta (12 squads, 4 ativos, 3 bloqueados por esta lacuna) · `Status:` Resolvido · `Disposição:` Respondido · `Hint:` O número exato de usuários únicos por squad não foi coletado na chamada — a elevação para 95 requereria dados de uso da conta.

---

## Impacto de Negócio  ·  *(Requisito 4 — bloqueia gate)*

> Use as dimensões aplicáveis. Receita, Retenção, Operacional, Competitivo, Compliance, Mercado são os mais comuns. Não force dimensões irrelevantes. Quantifique quando possível.

| Dimensão | Detalhe |
|---|---|
| **Receita** | 3 squads do Banco Meridional não integrados; expansão bloqueada diretamente por esta lacuna de UX. ARR de expansão estimado: R$ 28.000/ano (premissa: mesmo ticket por squad que os 4 ativos). |
| **Retenção** | Renovação do contrato em 90 dias. CS sinalizou como risco de churn se a lacuna não for endereçada antes da conversa de renovação. ARR em risco: R$ 84.000 (4 squads ativos × R$ 21.000). |
| **Operacional** | Workaround de compartilhamento manual via chat adiciona 15–20 min por cerimônia. Custo estimado em horas perdidas de time não calculado na captura. |
| **Competitivo** | Duas ferramentas concorrentes já oferecem controle sequencial e ocultação de votos. Citado como lacuna de diferenciação na chamada de renovação — o cliente tem alternativa viável no mercado. |

`Confiança:` 80 · `Fonte:` Submitter direto (retenção e competitivo); inferido a partir de dados de conta (receita) · `Status:` Resolvido · `Disposição:` Respondido + Premissa (ARR de expansão assume mesmo ticket dos squads ativos) · `Hint:` Confirmar ticket por squad com CS / Finance antes do RP para firmar o número de expansão.

---

## Indicadores de Valor (RICE-lite)

> Espelho para desafiar o pensamento — **não** ranking automático. Pontue cada um (Baixo / Médio / Alto). A confiança reusa a coluna acima — não se pontua de novo. O Esforço fica *soft* (chute do Submitter, firmado depois pelo CTO).

| Indicador | Score | Justificativa (na linguagem dele) | Confiança |
|---|---|---|---|
| **Impacto** ("quanto move o negócio?") | Alto | Renovação de R$ 84k ARR em risco + expansão de R$ 28k bloqueada. Lacuna competitiva com alternativas no mercado. | 80 |
| **Alcance** ("quantos sentem isso?") | Médio | 4 squads ativos (usuários diretos da dor) + 3 squads bloqueados. Dentro de uma conta, mas é o maior cliente enterprise da carteira. | 75 |
| **Urgência** ("por que agora? custo de esperar?") | Alto | Renovação em 90 dias cria janela não-negociável. Cada mês sem entrega é um mês a mais de workaround e de risco de perder a conversa de renovação. | 90 |
| **Esforço** *(soft — adiado ao CTO)* | Médio | Chute inicial do CS: parece ser UI + estado de sessão, sem nova infraestrutura. CTO deve confirmar. | low_confidence |

> **Tensões registradas:**
> - **Alcance Médio + Impacto Alto:** tensão aparente — o alcance é limitado a uma conta. Resolução: o impacto financeiro é desproporcional ao alcance porque é o maior cliente enterprise. A renovação de R$ 84k mais a expansão de R$ 28k justificam o score alto de impacto mesmo com alcance concentrado.
> - **Urgência Alta + Esforço soft:** o prazo de 90 dias pressiona, mas o esforço não está firmado. Resolução honesta: se o CTO identificar bloqueador arquitetural, o prazo vira o constraint de corte de escopo, não de adiamento.

---

## Urgência  ·  *(Requisito 5)*

**Prazo / janela:** Renovação do contrato do Banco Meridional em 90 dias a partir de 2026-03-12 (vencimento ~2026-06-10). A funcionalidade precisa estar em produção antes da conversa de renovação.

**Custo de esperar:** Se a entrega não ocorrer antes da renovação, o cliente tem argumento concreto para não renovar ou reduzir o contrato — e tem alternativas no mercado. CS já sinalou que o assunto foi colocado explicitamente na pauta da chamada de renovação.

`Confiança:` 90 · `Fonte:` Submitter direto (Ana Costa) · `Status:` Resolvido · `Disposição:` Respondido · `Hint:` —

---

## Evidência e Documentos  ·  *(Requisito 6)*

> Anexos ou conversas anteriores que embasam a demanda. Fonte de pré-preenchimento por IA.

| Documento / Conversa | Tipo | Relevância |
|---|---|---|
| Chamada trimestral de revisão com Banco Meridional — 2026-03-12 | Call (notas de CS) | Fonte primária: dor levantada pelos Scrum Masters, menção ao risco de renovação e à lacuna competitiva. |
| Histórico de tickets de suporte do Banco Meridional | Registros internos | CS menciona que outros 3 clientes enterprise relataram dor similar de forma informal. Tickets não foram formalizados. |

`Confiança:` 70 · `Fonte:` Submitter direto (notas da chamada) + inferido (tickets informais) · `Status:` Resolvido · `Disposição:` Respondido + Inferido · `Hint:` Formalizar os tickets dos 3 outros clientes elevaria a confiança e reforçaria o caso de negócio para além do Banco Meridional.

---

## Stakeholders  ·  *(Requisito 8)*

| Stakeholder | Papel | Interesse | Influência |
|---|---|---|---|
| Ana Costa | Customer Success — registradora da demanda, dona do relacionamento | Retenção da renovação do Banco Meridional; evitar churn de R$ 84k ARR | Alta |
| Scrum Masters do Banco Meridional | Usuários finais (facilitadores) — originadores diretos da dor | Controle do fluxo da cerimônia e integridade dos votos | Alta — usuários que adotam ou não adotam |
| Desenvolvedores do Banco Meridional | Usuários finais (votantes) | Menos distração, estimativas mais focadas, cerimônias mais curtas | Média |
| Lucas Mendes | PO | Alinhamento do produto com a dor e qualidade da entrega | Alta — decide se avança e em qual forma |
| CEO | Sponsor executivo | Retenção de receita e saúde do relacionamento enterprise | Média — informado do risco, não envolvido no detalhe |

`Confiança:` 85 · `Fonte:` Submitter direto · `Status:` Resolvido · `Disposição:` Respondido · `Hint:` PM ainda não definido (a definir pelo PO na triagem).

---

## Premissas

Condições assumidas como verdadeiras na captura. Se uma premissa se provar falsa, a demanda deve ser retriada. Premissas são uma **disposição válida** para requisitos sem resposta direta.

1. A infraestrutura WebSocket existente suporta novos tipos de eventos sem requerer um novo broker ou camada de mensageria. — `a validar com:` CTO / Tech Lead durante racionalização
2. A persistência de estado de sessão pode ser estendida com novos campos (ordem da fila, estado de revelação) sem uma migração completa de schema. — `a validar com:` CTO / Tech Lead durante racionalização
3. Os Scrum Masters do Banco Meridional têm autonomia para adotar novos recursos sem aprovação de TI da organização deles. — `a validar com:` Ana Costa (CS) + contato direto com o cliente
4. Co-facilitação não é necessária neste release — modelo de facilitador único é suficiente para o Banco Meridional agora. — `a validar com:` Ana Costa (CS) na próxima chamada com o cliente
5. O ticket por squad dos 3 squads pendentes é equivalente ao dos 4 ativos (base do ARR de expansão estimado). — `a validar com:` Finance / CS antes do RP

---

## Constraints  ·  *(Requisito 7)*

Condições que limitam o espaço de solução, a respeitar independentemente do que for construído.

| Constraint | Tipo | Detalhe |
|---|---|---|
| Prazo de renovação | Tempo | Renovação em ~90 dias. A funcionalidade deve estar em produção antes da conversa de renovação do Banco Meridional. |
| Sem redesign mobile | Escopo | O layout mobile existente se aplica. Sem investimento em UI mobile neste release. |
| Modelo de facilitador único | Escopo | Co-facilitação está explicitamente fora do escopo neste release. A arquitetura não deve impossibilitá-la futuramente, mas não precisa implementá-la agora. |
| Deploy sem downtime | Técnico | A funcionalidade deve ser implantável sem interrupção de sessões ativas. |
| Sem novos serviços externos | Orçamento | Construída na infraestrutura existente. Nenhum novo serviço de terceiros pode ser contratado. |

`Confiança:` 88 · `Fonte:` Submitter direto (prazo + escopo) + inferido (deploy sem downtime, padrão da plataforma) · `Status:` Resolvido · `Disposição:` Respondido + Premissa (deploy sem downtime inferido como padrão operacional) · `Hint:` —

---

## Riscos Preliminares

Riscos identificados na captura — antes da avaliação técnica. Registro completo pertence ao Readiness Package.

| Risco | Categoria | Avaliação Inicial |
|---|---|---|
| Inconsistências de ordenação de eventos WebSocket sob carga | Técnico | Desconhecido — requer load testing durante QA |
| Bypass de ocultação de votos via inspeção client-side | Segurança | Provavelmente mitigável — servidor deve aplicar a ocultação, não o cliente |
| Perda de estado de sessão na reconexão do facilitador | Técnico | Requer design de resiliência — período de graça ou snapshot de sessão |
| Viés de ancoragem não totalmente eliminado (participantes ainda podem falar verbalmente) | Produto | Aceito — a plataforma controla apenas a visibilidade digital |
| Prazo de renovação não cumprido se a racionalização revelar bloqueadores | Prazo | Baixa probabilidade com base na avaliação inicial; demanda parece circunscrita a UI e estado de sessão |

---

## Limite de Escopo de Alto Nível

**Dentro:** Gerenciamento de fila pelo facilitador (adicionar, ordenar, revelar um a um), ocultação de votos até revelação explícita, revelação de votos controlada pelo facilitador, persistência de estado de sessão, controles básicos (pular, retornar, encerrar).

**Fora:** Temporizadores por item, revelação automática de votos, co-facilitação / controle multi-facilitador, redesign mobile, relatórios e analytics, integração Jira/Linear.

**Adiado:** Toggle de preferência de revelação automática, reuso de template de fila entre sessões, dashboard de analytics de cerimônias.

---

## Prioridade

**Nível:** Alta

**Motivo:** Renovação do contrato do Banco Meridional em 90 dias. CS sinalizou como potencial risco de churn se não resolvido antes da conversa de renovação.

---

## Critérios de Sucesso

Indicadores de alto nível que definem "concluído e valioso". Metas mensuráveis detalhadas pertencem ao Readiness Package; estes são os sinais no nível da captura. **Servem de baseline projetado** para o acompanhamento pós-handoff (ver [`metrics.md`](../metrics.md)).

| Critério | Tipo | Indicador | Valor projetado |
|---|---|---|---|
| Contrato do Banco Meridional renovado | Negócio | Renovação assinada antes da data de expiração | R$ 84.000 ARR retido |
| 3 squads pendentes integrados | Negócio | Contagem de ativação de squads no dashboard da conta em até 60 dias do release | +R$ 28.000 ARR de expansão |
| Duração das cerimônias reduzida | Operacional | Tempo médio de sessão para cerimônias com 10+ itens cai ≥ 20% vs. baseline | ≥ 20% redução |
| Workaround do facilitador eliminado | Operacional | Zero tickets de CS reportando compartilhamento manual de histórias pós-release | 0 tickets |
| Zero reclamações de ancoragem de votos | Qualidade | Zero tickets de CS citando visibilidade prematura de votos | 0 tickets |
| Funcionalidade adotada sem treinamento | UX | Facilitadores ativam fila e revelação sem intervenção de suporte | 0 chamados de onboarding |
