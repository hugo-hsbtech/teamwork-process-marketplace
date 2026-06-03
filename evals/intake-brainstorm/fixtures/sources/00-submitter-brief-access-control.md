# Documento do Submitter — Room Access Control (Controle de Acesso à Sala)

> **Este é o documento do Submitter** — o primeiro artefato da jornada (`00`) e o entregável da persona Submitter. Ele **tangibiliza** o modelo de [`personas/01-submitter.md`](../personas/01-submitter.md): o raciocínio (requisitos de compliance, geração de ToDos, fórmula de score) vive na persona; este documento o **instancia** por demanda, na **linguagem do Submitter** — problema, valor, dor, oportunidade. Cada resposta carrega o quão sólida ela é e de onde veio: a camada de confiança viaja *com* a captura.
>
> **Jornada:** `00 Documento do Submitter` → [`01 Intake Record (PO — triagem)`](./01-intake-record-access-control.md) → [`02 Readiness Package (PO)`](./02-readiness-package-access-control.md) → [`03 Technical Assessment (CTO)`](./03-technical-assessment-access-control.md) → [`04 PRD (PO+CTO → PM)`](./04-prd-access-control.md). Ver [`README.md`](./README.md).
>
> **Nada antecede este documento como artefato.** O que vem antes é **sinal cru** — chamada de pré-fechamento com o cliente, thread de email com Vendas, anotação de reunião — que **não é artefato**. Esse sinal entra *aqui* como evidência/fonte (disposição `inferred`, com `source`); é a **captura** que o transforma neste primeiro documento formal.
>
> **Handoff:** congela quando `gateReady = true` (todo requisito bloqueante resolvido por uma disposição honesta) e é entregue ao **PO**, que o formaliza e tria no [`01 Intake Record`](./01-intake-record-access-control.md).

## As duas lentes (toda demanda é lida pelas duas ao mesmo tempo)

> Ver [`personas/01-submitter.md` §2](../personas/01-submitter.md). Os ToDos vivem onde as lentes se cruzam: "dado o que *esta* demanda significa, o que o contrato ainda precisa?"

| Lente | O que é | Onde aparece neste documento |
|---|---|---|
| **Contrato** (determinístico) | Os requisitos fixos de compliance que toda demanda precisa satisfazer para avançar | **Resumo de Prontidão** + os requisitos numerados (score + pendências) |
| **Semântica** (contextual) | O que *esta* demanda significa: a dor real (acesso aberto expõe identidades em cerimônias mistas), sua tese de valor (deal de R$ 42k bloqueado), suas incógnitas (Azure AD, LGPD, Jira) | **Enunciado do Problema**, **Impacto**, **Indicadores de Valor** e suas tensões |

## Metadados

| Campo | Valor |
|---|---|
| **Demanda** | Room Access Control — Controle de Acesso à Sala |
| **Registrado por** | Rafael Souza (Vendas) |
| **Data de captura** | 2026-03-15 |
| **Status** | Pronto para handoff (`gateReady`) |
| **Intake Record vinculado** | INT-2026-002 (atribuído pelo PO na triagem) |

## Histórico de Revisão

| Versão | Data | Evento | Resumo |
|---|---|---|---|
| v1 | 2026-03-15 | Captura iniciada e concluída | Vendas (Rafael Souza) capturou a demanda imediatamente após chamada de pré-fechamento com a Construtora Ágil. Todos os requisitos bloqueantes resolvidos por disposição honesta; 3 incógnitas de integração registradas como Discovery. |

---

## Resumo de Prontidão (Readiness)

> Snapshot da captura. O score é derivado dos requisitos abaixo; `low_confidence` conta como parcial. A demanda só é entregue ao PO quando todos os requisitos bloqueantes estão resolvidos (`gateReady = Sim`).

| Campo | Valor |
|---|---|
| **Readiness Score** | 84 % |
| **Gate liberado (gateReady)** | Sim |
| **Requisitos bloqueantes pendentes** | — (todos resolvidos por disposição honesta) |
| **Dispositions** | 5 respondidos · 1 inferido · 4 premissas · 3 discovery · 0 delegados |

> **Como ler o score:** os requisitos bloqueantes (1, 2, 3, 4) estão todos resolvidos. O score fica abaixo de 100% porque urgência (req. 5) e constraints (req. 7) têm campos com `low_confidence` e as 3 incógnitas de integração entram como `discovery` — disposição honesta que conta parcialmente no cálculo. Isso não bloqueia o gate; apenas sinaliza o que o PO precisa observar.

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
| **Cliente / Solicitante** | Construtora Ágil (mid-market, processo de onboarding em andamento) |
| **Originador e contexto** | Rafael Souza (Vendas), chamada de pré-fechamento em 2026-03-15. TI Lead da Construtora Ágil (Fernanda Ramos) e Scrum Masters participaram da chamada. |
| **Reportado via** | Chamada de vídeo de pré-fechamento — notas registradas por Rafael imediatamente após a ligação |

`Confiança:` 95 · `Fonte:` Submitter direto · `Status:` Resolvido · `Disposição:` Respondido · `Hint:` —

---

## Tipo

- [x] Funcionalidade
- [ ] Bug
- [ ] Melhoria
- [x] Compliance
- [x] Integração
- [ ] Operacional

---

## Enunciado do Problema  ·  *(Requisito 1 — bloqueia gate)*

> Qual a dor existente? Descreva o problema, não a solução.

A Construtora Ágil realiza cerimônias de planejamento ágil com equipes mistas: desenvolvedores internos, prestadores externos e gestores de produto. O modelo atual da plataforma é completamente aberto — qualquer pessoa com o link da sala entra, vê os nomes de todos os participantes e pode votar. Isso cria três dores concretas:

1. **Ausência de controle de entrada:** prestadores externos com o link conseguem entrar sem aprovação do facilitador, violando a política interna de governança de dados da empresa.
2. **Falta de anonimato entre votantes:** em sessões com prestadores, a visibilidade cruzada de identidades é proibida pela política interna. Hoje não há como ocultar quem está na sala.
3. **Sem distinção de papéis:** gerentes de produto e executivos que querem acompanhar a cerimônia sem influenciar as estimativas não têm um modo de observação — ou entram como votantes ou ficam de fora.

O resultado é que a Construtora Ágil **não pode fazer onboarding** sem que essas lacunas sejam endereçadas. O deal está condicionado à funcionalidade.

`Confiança:` 92 · `Fonte:` Submitter direto · `Status:` Resolvido · `Disposição:` Respondido · `Hint:` —

---

## Quem é Impactado (Alcance)  ·  *(Requisito 3 — bloqueia gate)*

> Personas, segmentos ou times que sentem essa dor.

| Persona / Segmento | Como é impactado |
|---|---|
| **Scrum Masters da Construtora Ágil** | Precisam de controle granular de quem entra e o que vê; hoje gerenciam o acesso fora da plataforma (workaround manual). |
| **Prestadores externos da Construtora Ágil** | Participam de sessões mas não devem ver identidades dos colegas; hoje veem tudo. |
| **Product Managers / Executivos** | Querem observar as cerimônias sem votar; hoje ou entram como votantes (influenciam o processo) ou não entram. |
| **TI Lead da Construtora Ágil (Fernanda Ramos)** | Responsável por compliance LGPD e integração Azure AD; precisa de garantias técnicas antes do go-live. |
| **Deals enterprise em pipeline (2 identificados)** | Outros 2 prospects com o mesmo requisito sinalizado por Vendas em Q1. |

`Confiança:` 88 · `Fonte:` Submitter direto + inferido da chamada · `Status:` Resolvido · `Disposição:` Respondido · `Hint:` Os 2 deals em pipeline são sinalizações de Vendas, sem confirmação escrita do cliente — confiança ligeiramente abaixo do deal principal.

---

## Impacto de Negócio  ·  *(Requisito 4 — bloqueia gate)*

> Dimensões aplicáveis quantificadas quando possível.

| Dimensão | Detalhe |
|---|---|
| **Receita** | Deal da Construtora Ágil: R$ 42.000/ano (ARR). Condicionado a esta funcionalidade — sem ela, o contrato não fecha. Vendas fez compromisso informal de entrega em 60 dias (a validar com o PM antes de confirmar ao cliente). |
| **Mercado** | Outros 2 deals enterprise em pipeline com o mesmo requisito sinalizados por Vendas em Q1. Potencial de R$ 84.000+ em ARR adicional se a funcionalidade for genérica o suficiente. |
| **Retenção** | Não aplicável — cliente ainda não integrado. Passa a ser relevante após o onboarding. |
| **Operacional** | Scrum Masters usam workarounds manuais hoje (controle de quem recebe o link, notificação fora da plataforma). Impacto operacional real para o facilitador. |
| **Compliance** | A Construtora Ágil opera sob políticas internas de governança de dados. Requisito LGPD: dados de identidade de participantes devem residir no Brasil. Não é negociável para este cliente. |

`Confiança:` 90 · `Fonte:` Submitter direto (deal principal) + inferido (pipeline) · `Status:` Resolvido · `Disposição:` Respondido · `Hint:` O valor dos 2 deals em pipeline não está quantificado — premissa de que seguem perfil similar à Construtora Ágil. O compromisso de 60 dias de Vendas não tem validação de capacidade; PO deve investigar antes de confirmar.

---

## Indicadores de Valor (RICE-lite)

> Espelho para desafiar o pensamento — **não** ranking automático. O Esforço fica *soft* (chute do Submitter; firmado depois pelo CTO).

| Indicador | Score | Justificativa (na linguagem dele) | Confiança |
|---|---|---|---|
| **Impacto** ("quanto move o negócio?") | Alto | R$ 42k ARR bloqueado + 2 deals em pipeline com mesmo requisito. Funcionalidade destrava um segmento enterprise que hoje não consegue fazer onboarding. | 88 |
| **Alcance** ("quantos sentem isso?") | Médio | Afeta diretamente Construtora Ágil + os 2 deals em pipeline. Na plataforma atual, impacta o segmento enterprise/regulado — minoria do volume total mas alto valor por conta. | 75 |
| **Urgência** ("por que agora? custo de esperar?") | Alto | Cada semana sem a funcionalidade atrasa o fechamento do deal e aumenta o risco de o cliente procurar alternativa. Vendas já fez compromisso informal de 60 dias. | 85 |
| **Esforço** *(soft — adiado ao CTO)* | Alto | Intuição de Vendas: envolve controle de acesso, integração Azure AD e compliance LGPD. Provavelmente maior do que parece. | low_confidence |

> **Tensões registradas:**
> - **Impacto alto + Alcance médio:** o impacto unitário por conta é alto (R$ 42k), mas o alcance imediato é restrito a um segmento específico. Resolução: o valor por conta é suficiente para justificar; o padrão criado serve de base para o segmento enterprise mais amplo.
> - **Urgência alta + Esforço (soft) alto:** risco real de o prazo informal de 60 dias não ser viável se o esforço for maior do que o esperado. Disposição: Discovery técnico antes de qualquer compromisso externo de data.

---

## Urgência  ·  *(Requisito 5)*

**Prazo / janela:** Vendas fez um compromisso informal ao cliente de entrega em 60 dias a partir de meados de março. Nenhuma data é confirmada até o PM executar avaliação de capacidade. Janela crítica: se o deal não fechar em Q2, entra em risco de churn de prospect.

**Custo de esperar:** A Construtora Ágil não inicia onboarding sem essa funcionalidade. Cada semana de atraso é uma semana de MRR perdida. Além disso, os 2 deals em pipeline podem procurar alternativas se a entrega atrasar muito.

`Confiança:` 80 · `Fonte:` Submitter direto · `Status:` Baixa confiança · `Disposição:` Premissa (a validar) · `Hint:` O prazo de 60 dias é compromisso informal de Vendas, sem validação de capacidade do PM. A confiança sobe após o PM confirmar viabilidade do prazo.

---

## Evidência e Documentos  ·  *(Requisito 6)*

> Anexos ou conversas anteriores que embasam a demanda.

| Documento / Conversa | Tipo | Relevância |
|---|---|---|
| Notas da chamada de pré-fechamento (2026-03-15) | Notas internas de Vendas | Fonte primária: dor descrita pelos Scrum Masters e pela TI Lead da Construtora Ágil |
| Email de follow-up de Fernanda Ramos (TI Lead) | Thread de email | Confirmação escrita dos requisitos LGPD e da necessidade de integração Azure AD |
| Sinalizações de pipeline Q1 (Vendas) | CRM interno | 2 deals com requisito similar identificados por Rafael Souza |

`Confiança:` 78 · `Fonte:` Submitter direto + documento · `Status:` Baixa confiança · `Disposição:` Respondido · `Hint:` Notas de chamada são da percepção de Vendas, não transcrição. O email de Fernanda eleva a confiança no requisito LGPD/Azure AD. Os sinalizamentos de pipeline são CRM sem detalhamento — PO deve confirmar com Vendas se são requisitos análogos ou apenas similares.

---

## Stakeholders  ·  *(Requisito 8)*

| Stakeholder | Papel | Interesse | Influência |
|---|---|---|---|
| Rafael Souza | Vendas — reportador da demanda | Fechar o contrato da Construtora Ágil | Alta |
| Fernanda Ramos (TI Lead — Construtora Ágil) | Autoridade técnica do cliente | Integração Azure AD e conformidade LGPD confirmadas antes do go-live | Alta |
| Scrum Masters da Construtora Ágil | Usuários finais primários | Controle de acesso em conformidade para cerimônias com prestadores | Alta |
| Ana Costa | Customer Success — dona do relacionamento pós-venda | Onboarding tranquilo e saúde pós-fechamento | Média |
| Lucas Mendes | PO — dono da racionalização | Alinhamento de produto e definição de escopo | Alta |
| Rodrigo Lima | CTO — avaliação técnica | Integridade arquitetural, conformidade LGPD, viabilidade Azure AD | Alta |
| CEO | Sponsor executivo | Receita do novo contrato e postura de compliance | Média |

`Confiança:` 92 · `Fonte:` Submitter direto · `Status:` Resolvido · `Disposição:` Respondido · `Hint:` —

---

## Premissas

Condições assumidas como verdadeiras na captura. Se uma premissa se provar falsa, a demanda deve ser retriada.

1. A Construtora Ágil está disposta e é capaz de registrar a plataforma como aplicação aprovada no seu tenant Azure AD — `a validar com:` Fernanda Ramos (TI Lead) no início do Discovery
2. A equipe de TI do cliente pode completar o registro Azure AD dentro da janela de entrega após as especificações técnicas serem fornecidas — `a validar com:` Fernanda Ramos no início do projeto
3. A camada de autenticação existente (OAuth2) pode ser estendida para validação de group-claim OIDC sem substituição ou reescrita — `a validar com:` CTO (spike técnico)
4. Conformidade LGPD pode ser alcançada com roteamento por tenant (sem migração completa da plataforma) — `a validar com:` CTO (revisão de infraestrutura)
5. Integração Jira não é obrigatória para fechar o deal — `a validar com:` Construtora Ágil (chamada com o cliente)
6. Aliases no modo anônimo são suficientes para compliance — sem necessidade de mascaramento adicional a nível de banco de dados além do que é exibido — `a validar com:` PO + CTO
7. O escopo do controle de acesso é por sala, não por conta de organização — `a validar com:` PO na racionalização

---

## Constraints  ·  *(Requisito 7)*

Condições que limitam o espaço de solução, a respeitar independentemente do que for construído.

| Constraint | Tipo | Detalhe |
|---|---|---|
| Prazo do deal (informal) | Tempo | Vendas fez compromisso informal de 60 dias ao cliente. Sem confirmação até avaliação de capacidade do PM. |
| Conformidade LGPD | Legal / Regulatório | Dados de identidade de participantes de clientes brasileiros devem residir em `sa-east-1`. Inegociável para este cliente. |
| Dependência Azure AD (lado do cliente) | Externo | A Construtora Ágil controla seu próprio tenant Azure AD. Integração não pode ser completada sem ação do TI deles. O prazo está parcialmente fora do nosso controle. |
| Sem SSO enterprise completo | Escopo | Apenas validação de group-claim OIDC para este release — não uma implementação SSO/SAML completa. |
| Compatibilidade retroativa | Técnico | Salas com link aberto existentes devem continuar funcionando sem alterações. Controle de acesso é opt-in por sala, não uma mudança breaking a nível de plataforma. |
| Sem novos provedores de auth externos | Orçamento | Nenhum novo provedor de identidade (Okta, Auth0, etc.) pode ser contratado. Apenas extensão da camada de auth existente. |

`Confiança:` 85 · `Fonte:` Submitter direto (constraints de negócio) + inferido (técnicas) · `Status:` Resolvido · `Disposição:` Respondido · `Hint:` As constraints técnicas (compatibilidade retroativa, sem SSO completo) foram confirmadas na chamada pelo TI do cliente. O constraint de prazo tem confiança mais baixa porque é compromisso informal.

---

## Riscos Preliminares

Riscos identificados na captura — antes da avaliação técnica. Registro completo pertence ao Readiness Package.

| Risco | Categoria | Avaliação Inicial |
|---|---|---|
| Registro Azure AD atrasado pelo TI do cliente | Externo / Prazo | Médio — dependência fora do nosso controle; mitigação: fornecer spec e checklist ao TI do cliente cedo |
| Postura LGPD requer trabalho de infraestrutura além do esperado | Compliance | Médio — CTO deve confirmar escopo antes do compromisso |
| Compromisso informal de prazo de Vendas conflita com capacidade real | Operacional | Alto — PM deve executar avaliação de capacidade antes de qualquer comunicação externa |
| Integração Jira escalada para obrigatória durante a entrega | Escopo | Baixo — a ser encerrado definitivamente em chamada com o cliente |
| Pressão de expansão de escopo (audit logs, SSO, guest access) | Escopo | Médio — exclusões explícitas devem ser documentadas e aplicadas pelo PO |

---

## Limite de Escopo de Alto Nível

**Dentro:** Modos de acesso (Aberto / Somente convite / Aprovação obrigatória), modo anônimo, atribuição de papel Votante/Observador, remoção de participante, mapeamento de group-claim Azure AD OIDC, roteamento de residência de dados `sa-east-1` por cliente com flag LGPD.

**Fora:** SSO / SAML completo, audit logs, integração Jira, guest access sem registro de conta, configurações padrão a nível de organização, proteção de sala com senha.

**Adiado:** Convite em massa via CSV, atribuição automática de observador por papel organizacional, exportação de compliance para governança — alimenta o backlog.

---

## Prioridade

**Nível:** Alta

**Motivo:** Bloqueador pré-fechamento do deal da Construtora Ágil (R$ 42.000 ARR). Urgência validada pela dependência do deal e pelo compromisso informal de Vendas. Sem resolução das incógnitas de integração, não é possível confirmar prazo.

---

## Critérios de Sucesso

Indicadores de alto nível que definem "concluído e valioso". Metas mensuráveis detalhadas pertencem ao Readiness Package.

| Critério | Tipo | Indicador | Valor projetado |
|---|---|---|---|
| Contrato da Construtora Ágil fechado | Negócio | Contrato assinado após o release | R$ 42.000 ARR |
| Zero incidentes de acesso não autorizado | Segurança / Compliance | Sem reportados após go-live | 0 incidentes |
| Conformidade LGPD confirmada pelo cliente | Legal | TI da Construtora Ágil confirma residência de dados antes do go-live | Sign-off de Fernanda Ramos |
| Mapeamento Azure AD funcionando end-to-end | Técnico | Funcionários e prestadores recebem papéis corretos automaticamente | 100% na homologação |
| Pelo menos 1 deal adicional em pipeline desbloqueado | Negócio | Um dos 2 deals sinalizados avança para fechamento | Em até 90 dias do release |
| Modo anônimo adotado em sessões enterprise | Produto | Adoção em ≥ 30% das sessões enterprise | Em até 60 dias do release |
