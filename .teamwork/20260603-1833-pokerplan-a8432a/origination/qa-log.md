# Q&A Ledger — PokerPlan

> Phase: .teamwork/20260603-1833-pokerplan-a8432a/origination · Template: v1 · Rev: 6 · Updated: 2026-06-03
> Readiness: 63% · Gate: Cleared · Open blocking: — (todas resolvidas) · Qualidade pendente (não-bloqueante): validação de mercado é item de discovery (TAM/aderência problema-mercado não validados), não gap de captura

---

## Q001 · targets: constraints · status: answered

- **Rationale:** Restrições/regras invariáveis que a solução deve respeitar, extraídas da especificação. Fechar esse campo evita que o design viole regras de negócio já definidas.
- **Spawned-by:** —
- **Asked:** 2026-06-03
- **Question:** Quais são as restrições rígidas (regras de negócio) que qualquer solução para o PokerPlan deve respeitar, independentemente de como o produto evoluir?
- **Answer:** Sigilo do voto até a revelação (RN-001), progresso mostra só a contagem de votos; controle exclusivo do host para revelar (RN-003), encerrar (RN-005) e cancelar (RN-009) rodadas; voto alterável apenas com rodada aberta (RN-002), sem voto retroativo após encerramento (RN-008); múltiplas rodadas por tarefa (RN-006) com histórico completo (RN-007); estimativa final registrada separada dos votos individuais (RN-010), consenso não precisa ser média; entrada sem autenticação, só nome (MVP V1); preservar todas as regras do Planning Poker físico.
- **Disposition:** inferred
- **Confidence:** 80
- **Source:** file:sources/pokerplan-spec.md §"Regras de Negócio" RN-001–RN-010, §"Fluxo Digital", §"Objetivo do Produto"
- **Hint:** Confirmar com o Submitter quais são restrições rígidas vs. preferências de design — especialmente "sem autenticação" (pode ser só do MVP V1, não permanente).
- **Follow-ups:** —

---

## Q005 · targets: assumptions · status: parked

- **Rationale:** Premissas implícitas embutidas na especificação, cada uma a validar com o Submitter. Assumptions tem min-confidence 0 (não-bloqueante); disposition assumption é honesta e suficiente para parked.
- **Spawned-by:** —
- **Asked:** 2026-06-03
- **Question:** Quais premissas estão implícitas na especificação e precisam de sign-off do Submitter para não virarem riscos?
- **Answer:** (a) Sessões remotas e síncronas com participantes simultâneos; (b) sem autenticação no MVP V1, identificar-se por nome basta; (c) escalas relevantes são Fibonacci e T-Shirt; (d) integrações (Jira, Linear) ficam para V2; (e) público são equipes ágeis que já praticam Planning Poker. Todas inferidas da solução, nenhuma declarada explicitamente pelo Submitter. ADICIONADAS VIA Q010 (Submitter direct, 2026-06-03): (f) modelo de monetização provável = SaaS por organização, com planos por nº de usuários, equipes ou funcionalidades avançadas — a validar; (g) NÃO há validação formal de mercado nem projeções de receita ainda — premissa de que há aderência suficiente ao problema a confirmar via discovery; (h) o problema é amplamente distribuído entre times ágeis — premissa de mercado a validar. Premissas (f)–(h) declaradas pelo Submitter, não inferidas; validador: Submitter / Discovery.
- **Disposition:** assumption
- **Confidence:** 35
- **Source:** file:sources/pokerplan-spec.md §"Visão Geral", §"Fluxo Digital", §"Escalas de Estimativa", §"MVP V2" (premissas a–e); Submitter direct via Q010 (premissas f–h)
- **Hint:** Premissas (a)–(e) precisam de sign-off do Submitter. Premissas (f)–(h) são declaradas pelo Submitter mas ainda não validadas no mercado — especialmente (g) (ausência de validação de mercado) e (h) (distribuição do problema) são as que mais impactam a viabilidade comercial. Validador: Submitter / Discovery.
- **Follow-ups:** —

---

## Q002 · targets: reach · status: superseded

- **Rationale:** O documento define papéis de produto, mas não segmentos reais que sentem a dor. Reach é bloqueante (min-confidence 70); a resposta original estava abaixo desse limiar porque identificava apenas papéis internos à ferramenta, não personas/times do mundo real.
- **Spawned-by:** —
- **Asked:** 2026-06-03
- **Question:** Quem, no mundo real, sente a dor que o PokerPlan resolve? Quais times, organizações ou segmentos são afetados, e como cada um é impactado?
- **Answer:** O produto define três papéis numa sessão: Host/Facilitador (cria sala, conduz, revela, define consenso), Participante (vota e discute) e Observador (acompanha, não vota). Público genérico mencionado: "equipes" que estimam de forma remota.
- **Disposition:** inferred
- **Confidence:** 45
- **Source:** file:sources/pokerplan-spec.md §"Participantes", §"Visão Geral", §"Objetivo"
- **Hint:** SUPERSEDIDO por Q008 (resposta direta do Submitter, conf 72, acima do min-confidence 70). Esta entrada preservada como trilha de auditoria. Papéis identificados aqui (Host, Participante, Observador) são papéis DENTRO do produto; Q008 confirma as personas reais do mundo externo.
- **Follow-ups:** Q008

---

## Q003 · targets: impact · status: parked

- **Rationale:** O documento cita dimensões de valor mas nada quantificado. Impact é bloqueante (min-confidence 70); a resposta atual estava muito abaixo desse limiar porque era puramente qualitativa e sem baseline. Atualizado via Q009 (modelo estimado pelo Submitter, conf 70 como assumption — libera o portão honestamente).
- **Spawned-by:** —
- **Asked:** 2026-06-03
- **Question:** Qual é o impacto de negócio esperado com o PokerPlan — em termos de tempo, custo, receita, risco ou outro indicador mensurável?
- **Answer:** Valor declarado é qualitativo/direcional: ganho de produtividade nas sessões, rastreabilidade do histórico de rodadas e transparência das estimativas. Nenhum impacto quantificado (sem números de tempo, custo, receita ou volume). Ver Q009 para o modelo quantificado como assumption (conf 70).
- **Disposition:** inferred
- **Confidence:** 30
- **Source:** file:sources/pokerplan-spec.md §"Objetivo do Produto", §"Visão Geral"
- **Hint:** Supersedido em substância por Q009 (modelo estimado, conf 70, assumption). Esta entrada preservada como trilha de auditoria da resposta original puramente qualitativa.
- **Follow-ups:** Q007, Q009

---

## Q004 · targets: priority · status: answered

- **Rationale:** Não há prioridade declarada; há escalonamento de escopo por valor implícito na especificação. Priority tem min-confidence 0 (não-bloqueante), portanto a resposta inferida é suficiente para fechar o campo.
- **Spawned-by:** —
- **Asked:** 2026-06-03
- **Question:** Qual é a prioridade declarada do PokerPlan em relação a outras iniciativas, e qual é a razão?
- **Answer:** Sem prioridade declarada pelo Submitter. O documento sugere escalonamento de escopo: MVP V1 (fluxo essencial: criar sala, votar, revelar, consenso, histórico) como conjunto de maior prioridade implícita; V1.1 e V2 são incrementos posteriores.
- **Disposition:** inferred
- **Confidence:** 40
- **Source:** file:sources/pokerplan-spec.md §"Funcionalidades do MVP"
- **Hint:** É priorização de ESCOPO (o que entra em qual versão), não nível de prioridade de negócio em relação a outros projetos. Confirmar com o Submitter. Confiança baixa é aceitável aqui porque min-confidence é 0.
- **Follow-ups:** —

---

## Q006 · targets: problem · status: answered

- **Rationale:** A seção `problem` é bloqueante (min-confidence 80) e o arquivo-fonte não oferece sintomas observáveis — só descreve a solução. Esta pergunta força a mudança de linguagem-solução para experiência vivida, exatamente o que o rubric de `problem` exige. Sem ela, o portão não pode ser avaliado.
- **Spawned-by:** —
- **Asked:** 2026-06-03
- **Answered:** 2026-06-03
- **Question:** Hoje, quando suas equipes precisam estimar tarefas (ou fazem Planning Poker do jeito que fazem atualmente), o que dá errado ou incomoda na prática? Pensa no último mês: teve alguma sessão que foi frustrante, demorada ou que gerou retrabalho? Me conta o que você viu acontecer — não a solução, mas o sintoma.
- **Answer:** A principal dor não é a votação em si, mas a falta de estrutura e rastreabilidade durante o processo de estimativa. Hoje as sessões acontecem de forma improvisada, com ferramentas não projetadas para isso. Problemas recorrentes: perda de tempo organizando a dinâmica da votação; falta de registro das estimativas; dificuldade em acompanhar a evolução do consenso; ausência de histórico para entender por que uma tarefa recebeu certa estimativa; necessidade de repetir discussões porque a sessão anterior não ficou registrada; participantes influenciando involuntariamente os votos dos demais quando a votação não é realmente secreta. A reunião acaba consumindo mais tempo do que deveria — não pela discussão técnica, mas pela falta de uma ferramenta simples para conduzir o processo. Sintoma: a estimativa, que deveria ser rápida e colaborativa, vira uma atividade operacionalmente desgastante, pouco rastreável e difícil de reproduzir depois.
- **Disposition:** answered
- **Confidence:** 84
- **Source:** Submitter direct
- **Hint:** Dor descrita com sintomas observáveis e sem prescrever solução — atende o rubric de `problem`. Ainda não quantificada (tempo perdido por sessão, número de sessões) — a quantificação pertence a `impact` (Q003, que permanece open/blocking conf 30).
- **Follow-ups:** Q007, Q008

---

## Q007 · targets: problem · status: answered

- **Rationale:** A dor fica mais nítida quando contrastada com o workaround atual. Esta pergunta separa "seria bom ter" de "o status quo dói" e levanta indícios de impact e urgency. É spawned pela pergunta de problem (Q006) porque só faz sentido perguntar sobre o workaround depois de confirmar que há dor.
- **Spawned-by:** Q006
- **Asked:** 2026-06-03
- **Answered:** 2026-06-03
- **Question:** E como vocês fazem isso hoje, sem o PokerPlan? Usam alguma ferramenta improvisada, chat, planilha, ou fazem presencial? O que essa solução de quebra-galho atual não entrega — o que escapa, atrasa ou fica impreciso por causa dela?
- **Answer:** O processo é feito com ferramentas genéricas: chamadas de vídeo, chats corporativos, ferramentas genéricas de colaboração, planilhas para registrar resultados, e soluções gratuitas de Planning Poker sem integração com o restante do processo. Essas abordagens resolvem só a votação, não o fluxo completo. Fica faltando: histórico consolidado das sessões, registro das rodadas, justificativas para divergências, exportação dos resultados, organização das tarefas estimadas, integração com ferramentas de gestão de produto, e visibilidade da evolução das estimativas ao longo do tempo. Na prática há fragmentação do processo entre várias ferramentas, gerando retrabalho e perda de contexto.
- **Disposition:** answered
- **Confidence:** 84
- **Source:** Submitter direct
- **Hint:** O contraste com o workaround confirma e reforça a dor descrita em Q006. A fragmentação entre ferramentas é indício concreto de custo do status quo — alimenta `impact` (Q003) e `urgency`. Quantificação do custo (horas, nº de equipes) ainda ausente e continua bloqueante em Q003.
- **Follow-ups:** —

---

## Q008 · targets: reach, originator · status: answered (reach) / answered (originator)

- **Rationale:** Fecha terreno em `reach` (segmentos que sentem a dor + como afetados) e abre `originator` (quem levantou, em que situação, por qual canal). Reach é o maior fator de oscilação para a futura quantificação de impact; originator é bloqueante (min-confidence 70). Spawned por Q006 porque reach e originator só ficam nítidos depois de identificar quem sente a dor.
- **Spawned-by:** Q006
- **Asked:** 2026-06-03
- **Answered:** 2026-06-03

- **Question:** Essa dor é sentida por quem exatamente? São times de produto/engenharia específicos, todos os squads, clientes externos? E essa ideia do PokerPlan — partiu de você, de um time que reclamou, de um cliente, ou de uma reunião? Quem foi a pessoa ou grupo que disse "precisamos resolver isso"?

**Reach — Answer:** A dor é percebida principalmente por equipes de desenvolvimento de software que usam métodos ágeis e fazem estimativas de backlog regularmente. Personas internas ao produto: Desenvolvedores, Product Owners, Scrum Masters, Tech Leads e Gestores de produto. Segmentos de mercado (confirmados via Q010): empresas de tecnologia, consultorias de software, fábricas de software, times de produto, organizações Scrum/ágil.

- **Disposition (reach):** answered
- **Confidence (reach):** 78
- **Source (reach):** Submitter direct (personas: 2026-06-03 anterior; segmentos de mercado: Q010 resp. 2026-06-03)
- **Hint (reach):** Personas claras (Devs, PO, SM, Tech Lead, gestores) e segmentos de mercado claros (empresas tech, consultorias, fábricas de software, times de produto, organizações Scrum/ágil). SEM dimensionamento de TAM: quantos times, quantas organizações, nº de orgs no mercado endereçável — isso permanece não-quantificado e é o fator crítico para projeções comerciais. Market sizing (TAM/nº de orgs) é item de discovery. Esta resposta SUPERSEDE Q002 (reach inferred conf 45); Q002 mantido como trilha de auditoria.

**Originator — Answer (atualizado via Q011):** A iniciativa partiu da própria equipe/empresa por trás do PokerPlan como aposta de produto comercial — não de um cliente externo específico nem de um único time interno reclamante. Motivação: recorrência do problema (falta de estrutura/rastreabilidade na estimativa) observada em diferentes times de tecnologia ágil, vista como oportunidade de mercado. Canal/situação: concepção interna de produto.

- **Disposition (originator):** answered
- **Confidence (originator):** 78 — superseded by Q011 (conf 85, Submitter direct, 2026-06-03); Q011 is the authoritative originator answer.
- **Source (originator):** Submitter direct (Q011, 2026-06-03) — SUPERSEDE assumption conf 60 registrada anteriormente
- **Hint (originator):** Originador é concreto o suficiente para a seção (aposta de produto interna da empresa). O indivíduo/sponsor específico (pessoa) não está nomeado — não bloqueia; pode ser confirmado se necessário para handoff. Disposição anterior de originator como assumption conf 60 foi supersedida por esta resposta direta conf 78.
- **Follow-ups:** Q011

---

## Q009 · targets: impact · status: parked

- **Rationale:** `impact` era o único bloqueante ainda abaixo do limiar (conf 30, inferred). Quantificar — mesmo que estimado — é o que libera o portão de forma honesta e alimenta a triagem. Escape hatch: estimativa de trabalho como assumption, marcada a validar. Spawned-by bateria de perguntas Batch-2 (2026-06-03).
- **Spawned-by:** Q003
- **Asked:** 2026-06-03
- **Answered:** 2026-06-03
- **Question:** Dá pra dimensionar a dor em números? Quantas sessões por semana/sprint, duração de cada sessão (atual vs. ideal), quantos times/pessoas impactados — transformar "perde-se tempo" em "X horas/mês entre Y times".
- **Answer:** Aproximação baseada em equipes ágeis tradicionais. Squad típico: 5–10 pessoas, ao menos 1 sessão de refinamento/estimativa por sprint (em ambientes de produto, frequentemente semanal). Sessão dura de 30 min a 2 h conforme o nº de itens; em processos pouco estruturados, parte do tempo é gasta organizando a votação, registrando resultados ou retomando discussões não documentadas. Modelo: time de 8 pessoas × 1 h = 8 horas-homem/sessão; ~4 sessões/mês = 32 horas-homem/mês por time; org com 10 squads ≈ 320 horas-homem/mês em estimativa. O problema não é a existência dessas horas (estimar é necessário), mas o DESPERDÍCIO por falta de estrutura, ausência de histórico, repetição de discussões e dificuldade de registrar decisões. Reduzindo 15–20 min de ineficiência por sessão, um squad economizaria entre 8 e 11 horas-homem/ano (estimativa do Submitter); em orgs com dezenas de squads o ganho acumulado é significativo. Benefício adicional menos visível e mais relevante: melhoria da QUALIDADE das estimativas — com decisões registradas e divergências rastreáveis, o time evolui o processo, reduz desalinhamentos e aumenta previsibilidade das entregas. Visão: PokerPlan como ferramenta de GOVERNANÇA e RASTREABILIDADE do processo de estimativa, não apenas votação.
- **Disposition:** assumption
- **Confidence:** 70
- **Source:** Submitter direct
- **Hint:** É um modelo/estimativa, não medição real. Confiança 70 como assumption — libera o portão honestamente, mas deve ser validada. INCONSISTÊNCIA ARITMÉTICA A VERIFICAR: 15–20 min × ~48 sessões/ano × 8 pessoas daria ~96–128 horas-homem/ano por squad (e não "8–11 horas-homem/ano") — confirmar a base do cálculo de economia com o Submitter antes de usar o número em triagem. DUAS CAMADAS DE IMPACT (esclarecidas via Q010): (a) eficiência operacional por cliente — modelo de horas-homem acima, assumption conf 70; (b) oportunidade comercial/mercado — produto SaaS, não-validada → item de discovery (validar aderência problema-mercado, TAM, projeções de receita). Quantificação comercial (TAM, receita, conversão) explicitamente não-validada pelo Submitter.
- **Follow-ups:** Q010

---

## Q010 · targets: impact · status: answered

- **Rationale:** Determina a NATUREZA do valor (receita vs. eficiência), que é o maior fator de oscilação na quantificação de impacto. Produto comercial → impacto é receita/mercado (clientes/assinaturas); ferramenta interna → impacto é eficiência (horas economizadas, retrabalho evitado). Sem essa definição, qualquer número de Q009 pode estar na unidade errada. Escape hatch: deferred (dono define) se ainda não decidido.
- **Spawned-by:** Q009
- **Asked:** 2026-06-03
- **Answered:** 2026-06-03
- **Question:** PokerPlan é produto comercial ou ferramenta interna? Comercial → impacto é receita/mercado (clientes/assinaturas); interno → eficiência (horas economizadas, retrabalho evitado).
- **Answer:** PokerPlan está sendo concebido como PRODUTO COMERCIAL (SaaS). Pode ser usado internamente por qualquer organização, mas a motivação principal não é uma necessidade de um único time/empresa — o problema é amplamente distribuído entre equipes de tecnologia ágeis. Já existem ferramentas de Planning Poker no mercado, mas muitas focam só na votação; a visão é expandir para uma plataforma que preserve a dinâmica tradicional e adicione histórico, rastreabilidade, métricas, integração com ferramentas de gestão e colaboração entre equipes. O valor não está só na economia de tempo da reunião, mas na melhoria da previsibilidade e da qualidade do processo de planejamento. Mercado potencial: equipes de desenvolvimento de software, empresas de tecnologia, consultorias de software, fábricas de software, times de produto e organizações que usam Scrum/ágil. Monetização provável: SaaS por organização, com planos por nº de usuários, equipes ou funcionalidades avançadas. ESTÁGIO ATUAL: ainda NÃO há validação formal de mercado nem projeções de receita — o objetivo inicial é validar se existe aderência suficiente ao problema para justificar evoluir para produto comercial.
- **Disposition:** answered
- **Confidence:** 80
- **Source:** Submitter direct
- **Hint:** Define a natureza do valor (receita/mercado, não só eficiência interna). A quantificação comercial (TAM, receita, conversão) é EXPLICITAMENTE não-validada pelo Submitter → alimenta item de discovery (validar aderência problema-mercado). A eficiência operacional (modelo de Q009) permanece como prova de valor por cliente. Premissas associadas declaradas pelo Submitter e registradas em Q005 (atualizado): (1) modelo de monetização provável = SaaS por organização (planos por usuários/equipes/funcionalidades) — a validar; (2) NÃO há validação de mercado nem projeção de receita — premissa de que há aderência suficiente a confirmar; (3) o problema é amplamente distribuído entre times ágeis — premissa de mercado a validar.
- **Follow-ups:** —

---

## Q011 · targets: originator · status: answered

- **Rationale:** O Auditor apontou que `originator` (conf 60, parked como assumption) se resolve com uma pergunta de 2 minutos. Fechar com nome concreto elevaria a confiança de 60 para ~85 e removeria um item parqueado pendente de confirmação. Escape hatch: deferred (owner: Submitter) se não puder responder agora.
- **Spawned-by:** Q008
- **Asked:** 2026-06-03
- **Answered:** 2026-06-03
- **Question:** De quem partiu a ideia, concretamente? Foi você, um time interno de produto, a iniciativa é sua/da sua empresa? Para fechar o originador com nome em vez de suposição.
- **Answer:** A demanda NÃO partiu de uma iniciativa isolada de uma única pessoa, mas de uma necessidade percebida COLETIVAMENTE por membros dos times de produto, engenharia e gestão que vivenciam o processo de estimativa de forma recorrente. Ao longo das sessões de refinamento e planejamento, os participantes demonstraram insatisfação com a condução do processo via ferramentas improvisadas ou soluções incompletas — principais reclamações: falta de rastreabilidade das estimativas, dificuldade de registrar decisões, ausência de histórico das sessões e pouca integração com o fluxo de trabalho. Dessas dores recorrentes surgiu, entre os próprios participantes, a discussão sobre a necessidade de uma ferramenta mais adequada para suportar o Planning Poker de forma estruturada. Esse reconhecimento coletivo do problema é o que motivou conceber o PokerPlan — depois enquadrado como aposta de PRODUTO COMERCIAL (SaaS), dado que o mesmo problema é amplamente distribuído entre equipes de tecnologia ágil (não exclusivo de um time/empresa).
- **Disposition:** answered
- **Confidence:** 85
- **Source:** Submitter direct
- **Hint:** Originador agora bem caracterizado: origem bottom-up (times de produto, engenharia e gestão que vivem o processo), formalizada como aposta de produto comercial — clears originator gate ≥70 com confiança 85. Não há um sponsor individual nomeado — e isso é coerente com a origem coletiva, não é uma lacuna; pode ser confirmado se necessário para handoff. TRILHA DE AUDITORIA: resposta anterior (Rev 4) enquadrava a iniciativa como "aposta de produto interna da empresa, conf 78"; substituída por esta versão mais completa (bottom-up, coletiva, times produto/engenharia/gestão) com conf 85 via Submitter direct (2026-06-03). A resposta anterior em Q008 (originator conf 78) permanece como registro intermediário.
- **Follow-ups:** —

<!-- END OF DOCUMENT -->
