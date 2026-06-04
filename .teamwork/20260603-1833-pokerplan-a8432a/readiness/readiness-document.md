<!--
TARGET TEMPLATE · Readiness Package (default)
This file is the contract. Each fillable section carries an annotation:
  <!-- intake: SECTION-ID; blocks=BOOL; min-confidence=N; kind=TYPE -->
and a self-sufficient rubric. The Template Analyst derives contract.lock.md from
these (the same engine as intake-brainstorm — the marker keyword stays `intake:`).
The confidence line adds an Origin field (inherited | ai_drafted | po_authored)
per personas/02-po.md. To use a different document type, copy this file, re-annotate,
and pass it as TEMPLATE. See references/contract-and-template.md (in intake-brainstorm).
Default confidence threshold (X) = 70. Raise per-section for high-stakes fields.
-->

# Readiness Package — PokerPlan
<!-- rev: 5 · updated: 2026-06-03 -->

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
| **ID do Pacote** | RP-2026-001 |
| **Versão** | v1 |
| **Intake vinculado** | INT-2026-001 |
| **Responsável** | — (PO) |
| **Escalada ao CTO / Technical Assessment** | requested / deferred (skill tech-assessment ainda não existe; ver seção Referência ao Technical Assessment) |
| **Status** | Congelado provisoriamente (Provisionally frozen) |
| **Data de congelamento (freeze)** | 2026-06-03 (provisório) |
| **Readiness score** | 78% |
| **Output language** | pt-BR |
| **Nota** | O intake de origem foi triado como "Discovery" (não "Product Ready"). O PO optou por prosseguir para o RP com as seções herdadas preenchidas e as seções de Fase 2 pendentes. |
| **Nota de freeze** | Congelamento PROVISÓRIO — seções de produto congeladas; freeze definitivo requer TechAssessmentRef.status = signed (Technical Assessment ainda devido). |

## Histórico de Revisão
<!-- intake: id=revisions; blocks=false; min-confidence=0; kind=meta -->

| Versão | Data | Autor | Status | Resumo |
|---|---|---|---|---|
| v1 | 2026-06-03 | Doc Updater (engine) | Rascunho | Instanciação a partir do template; seções herdadas preenchidas; seções de autoria do Drafter deixadas como placeholder explícito. |
| v2 | 2026-06-03 | Draft pass | Rascunho | Seções de produto (business-rules, user-stories, nfrs, edge-cases) preenchidas pelo readiness-drafter como ai_drafted em confiança parcial. |
| v3 | 2026-06-03 | Escalation flag | Rascunho | readiness-escalation-flagger detectou gatilhos arquiteturais (runtime/tempo real + segurança/identidade); TechAssessmentRef = requested/deferred (freeze provisório — skill tech-assessment ainda não existe). |
| v4 | 2026-06-03 | Confirm loop | Rascunho | Decisões do PO aplicadas (Q017–Q029): escopo Excluído declarado; ambiguidades A1–A7 resolvidas; Observador no V1; status CANCELLED; políticas EC-02/EC-06; alvo NFR ~2s p95; números diferidos à Discovery; cifras de economia suprimidas; riscos com prob/impacto firmes. Promoções a po_authored. |
| v5 | 2026-06-03 | Provisional freeze | Congelado provisoriamente | RP congelado provisoriamente (readiness 78%); 12 seções bloqueantes resolvidas/dispostas; TechAssessmentRef requested/deferred mantém o teto em freeze provisório. |

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
| **Readiness Score no handoff do Intake** | 63% |
| **Itens RESOLVIDOS pelo PO (confirm-loop Q017–Q029)** | A1 encerramento da sala (Host dispara); A2 consenso livre sem critério mínimo; A3 desempate = processo humano; A4 status CANCELLED criado; A5 sem limite rígido de participantes; A6 Observador no V1; A7 "todos votaram" diferida a V1.1 com RN-004. Escopo Excluído declarado. EC-02 política (Host reassume pelo mesmo link). EC-06 nomes duplicados (permitidos, desambiguados). RN-004 confirmado V1.1 (confirmação com o Submitter ainda pendente — Q018). |
| **Itens ABERTOS para Discovery** | (e) público já pratica Planning Poker → validar na Discovery; (f) willingness-to-pay não testado → discovery; (g/h) aderência problema-mercado e TAM NÃO validados → discovery (risco ALTO/ALTO). Cifras de economia suprimidas até correção do modelo aritmético (~10x — Discovery item 3). Urgência ausente: sem janela/prazo/competidor — não inventar. |
| **Itens pendentes para Technical Assessment** | (a) sincronização de estado em tempo real para múltiplos participantes simultâneos; (b) sigilo do voto em transporte/cliente (RN-001); (c) identidade confiável do Host sem login (RN-003/005/009; EC-02 mecanismo; EC-08 persistência de voto). |
| **Premissas aceitas (não-bloqueantes)** | (b) sem autenticação no MVP V1 — assumption V1; (c) escalas Fibonacci+T-Shirt customizáveis → aceitar; (d) integrações Jira/Linear são V2 → confirmado pelo PO. |

---

## Seção 1 — Resumo Executivo
<!-- intake: id=exec-summary; blocks=true; min-confidence=70; kind=capture -->
> Rubric: 2–4 parágrafos curtos. Qual é o problema, o que será construído e qual é
> o resultado esperado de negócio. Deve ser legível por qualquer stakeholder sem
> contexto adicional. Herdado e expandido do intake quando possível.

O PokerPlan endereça a falta de estrutura e rastreabilidade no processo de estimativa de tarefas em equipes ágeis. Hoje as sessões de Planning Poker são conduzidas de forma improvisada (chamadas de vídeo + chats + planilhas + ferramentas gratuitas desconectadas), o que gera perda de tempo operacional, ausência de histórico das rodadas, votos influenciados por falta de sigilo real e fragmentação entre ferramentas.

Será construída uma plataforma digital de Planning Poker que preserva as regras do método físico (votação secreta, revelação controlada pelo host, múltiplas rodadas, consenso registrado) e adiciona rastreabilidade: histórico consolidado das sessões e das rodadas por tarefa. O MVP V1 cobre o fluxo essencial (criar sala, entrar sem autenticação por nome, votar com sigilo, revelar, registrar consenso, histórico).

O resultado de negócio esperado tem duas camadas: (A) eficiência operacional por cliente — ganho de eficiência operacional por cliente, magnitude a quantificar na Discovery (cifras suprimidas até correção do modelo); (B) oportunidade comercial como produto SaaS para o mercado ágil — explicitamente NÃO validada no intake. A aposta comercial (Layer B) é premissa de mercado não validada; depende de Discovery (aderência problema-mercado, willingness-to-pay, TAM). O escopo Excluído do MVP V1 foi declarado pelo PO (ver Seção 5).

`Confidence:` 75 · `Origin:` po_authored · `Source:` Síntese do intake — id=problem(84), id=originator(85), Objetivo do Produto SRC-002, escopo/MVP V1, impact Camada B(70,discovery); confirm-loop Q017–Q029 · `Disposition:` assumption · `Hint:` Camada comercial (B) NÃO validada — não afirmar resultado de negócio firme; cifras de economia suprimidas até correção do modelo aritmético (Discovery item 3); escopo Excluído declarado (Q017)

---

## Seção 2 — Contexto e Problema (a dor, não a solução)
<!-- intake: id=context-problem; blocks=true; min-confidence=80; kind=capture -->
> Rubric: cenário atual, limitações, dor do cliente e impacto de negócio — o
> problema, nunca a solução. Se descreve uma solução ("construir X"), NÃO está
> satisfeita: reformule para a dor subjacente. Herdada do intake quando possível.

### Cenário Atual

As sessões de Planning Poker acontecem de forma improvisada, com ferramentas não projetadas para isso: chamadas de vídeo + chats corporativos + planilhas para registrar resultados + soluções gratuitas de Planning Poker desconectadas do restante do processo.

### Limitações

Esses workarounds resolvem só a votação pontual, não o fluxo completo. Faltam: histórico consolidado das sessões, registro das rodadas por tarefa, justificativas para divergências, exportação de resultados, organização das tarefas estimadas, integração com ferramentas de gestão e visibilidade da evolução das estimativas ao longo do tempo.

### Dor do Cliente

Sintomas observáveis:

- Perda de tempo organizando a dinâmica da votação (operação manual em vez de facilitação);
- Falta de registro das estimativas (sem histórico consolidado);
- Dificuldade de acompanhar a evolução do consenso dentro e entre sessões;
- Ausência de histórico para entender por que uma tarefa recebeu certa estimativa (equipes repetem discussões);
- Votos influenciados involuntariamente quando a votação não é verdadeiramente secreta;
- Fragmentação entre ferramentas, gerando retrabalho e perda de contexto.

Síntese: a estimativa, que deveria ser rápida e colaborativa, vira atividade operacionalmente desgastante, pouco rastreável e difícil de reproduzir — não por falta de método, mas por falta de ferramenta adequada.

### Impacto de Negócio

Camada A (eficiência operacional): o processo consome horas recorrentes de estimativa; a magnitude exata por squad/sessão carrega inconsistência aritmética no modelo do intake (~10x) e é diferida à Discovery (item 3). **NÃO usar cifras de economia em materiais até a correção.** O problema não é a existência dessas horas, mas o desperdício por falta de estrutura (ver Prontidão herdada).

`Confidence:` 84 · `Origin:` po_authored · `Source:` Submitter direct (Q006+Q007), intake id=problem; confirm-loop Q026/Q029 · `Disposition:` answered · `Hint:` Dor descrita com sintomas observáveis e sem prescrever solução — atende a rubrica (min 80); cifras de economia suprimidas até correção aritmética (Discovery item 3); PO revisou e confirmou

---

## Seção 3 — Objetivos e Resultado Esperado
<!-- intake: id=objectives; blocks=true; min-confidence=70; kind=capture -->
> Rubric: objetivos numerados e observáveis que esta entrega deve alcançar após o
> release. Cada objetivo deve ser verificável: se não pode ser medido ou observado,
> não está satisfeito. Mínimo dois objetivos.

1. Digitalizar a dinâmica do Planning Poker preservando as regras do método físico (votação secreta, revelação controlada, múltiplas rodadas, consenso registrado).
2. Prover rastreabilidade: histórico consolidado das sessões e registro das rodadas por tarefa, eliminando a repetição de discussões não documentadas.
3. Garantir sigilo real do voto até a revelação, removendo a influência involuntária entre participantes.
4. Reduzir o tempo operacional por sessão (desperdício por falta de estrutura).

Valores-alvo mensuráveis diferidos à Discovery (Q026). O objetivo 4 (tempo operacional) depende da correção do modelo de eficiência antes de receber alvo numérico.

`Confidence:` 65 · `Origin:` po_authored · `Source:` SRC-002 §Objetivo do Produto; intake id=impact, id=problem; confirm-loop Q026 · `Disposition:` discovery · `Hint:` Objetivos qualitativos confirmados pelo PO; valores-alvo mensuráveis diferidos à Discovery; NÃO usar cifras até correção aritmética

---

## Seção 4 — Personas Impactadas / Jobs-to-be-done
<!-- intake: id=personas; blocks=true; min-confidence=70; kind=capture -->
> Rubric: para cada persona, o job-to-be-done (o que está tentando realizar) e como
> é impactada por esta entrega. Sem persona definida, scope e critérios de aceite
> não têm âncora. Herdado do intake (campo reach) quando possível.

Demanda em duas camadas: personas internas (usuários diretos) e segmentos de mercado comercial (compradores do SaaS).

**Personas internas (JTBD / como são impactadas):**

- **Desenvolvedores** — votam; querem votar sem influência e ter histórico.
- **Product Owners** — conduzem/participam; querem rastreabilidade para priorizar.
- **Scrum Masters/Facilitadores** — gerenciam a dinâmica; querem facilitar sem operação manual fragmentada.
- **Tech Leads** — votações técnicas; querem histórico para justificar estimativas.
- **Gestores de produto/engenharia/gestão** — dependem das estimativas; querem visibilidade da evolução.

**Segmentos de mercado comercial (alvo SaaS):**

Empresas de tecnologia, consultorias de software, fábricas de software, times product-led, organizações Scrum/ágil.

Nota: o papel **Observador** (Host promove participante a Observador) é contemplado no V1 (A6 resolvida — Q021). Gestores e Stakeholders que queiram acompanhar sem votar usam esse papel.

`Confidence:` 78 · `Origin:` po_authored · `Source:` Submitter direct (Q008 personas; Q010 segmentos), intake id=reach; confirm-loop Q021 · `Disposition:` answered · `Hint:` Personas e segmentos claros (atende min 70); Observador confirmado no V1 pelo PO; SEM dimensionamento de TAM — item de Discovery; não inventar números de mercado

---

## Seção 5 — Escopo Incluído e Excluído
<!-- intake: id=scope; blocks=true; min-confidence=75; kind=capture -->
> Rubric: protege o downstream de scope creep. Deve listar explicitamente o que
> está FORA, não apenas o que está dentro. Itens adiados alimentam o Roadmap
> (Seção 14). Sem "excluído" preenchido, a seção NÃO está satisfeita.

### Incluído

MVP V1: Criar sala; compartilhar link; entrar sem autenticação (só nome); cadastro de tarefas; votação secreta; revelação de votos (controle do host); múltiplas rodadas; definição de consenso; histórico da sessão; papel Observador (Host promove participante a Observador).

### Excluído

Excluído (MVP V1):

- Autenticação / gestão de identidade de usuário.
- Contas / tenancy organizacional (org-level).
- TODAS as funcionalidades de V1.1: cronômetro; auto reveal (RN-004); estatísticas automáticas; exportação CSV.
- TODAS as funcionalidades de V2: integração Jira/Linear; times permanentes; histórico organizacional; dashboard de métricas; comparação entre rodadas; comentários anônimos por voto.

### Adiado (fases futuras)

V1.1 — cronômetro, auto reveal (RN-004), estatísticas automáticas, exportação CSV.

V2 — integração Jira e Linear, times permanentes, histórico organizacional, dashboard de métricas, comparação entre rodadas, comentários anônimos por voto.

`Confidence:` 90 · `Origin:` po_authored · `Source:` SRC-002 §Funcionalidades do MVP (V1/V1.1/V2); intake id=priority; constraints; confirm-loop Q017/Q021 · `Disposition:` decided · `Hint:` Excluído declarado explicitamente pelo PO (Q017) — rubrica satisfeita; Observador está IN no V1 (A6 resolvida — Q021); autenticação e org-level confirmados fora do V1

---

## Seção 6 — Regras de Negócio e Fluxos
<!-- intake: id=business-rules; blocks=true; min-confidence=80; kind=capture -->
> Rubric: regras, validações e transições de estado que governam a funcionalidade.
> Cada regra deve ser verificável e atômica. Fluxos de transição de estado devem
> cobrir caminhos de erro, não apenas o caminho feliz.

### Regras de Negócio do Planning Poker (RN-001..RN-010, +RN-004)

Regras restatadas a partir da especificação (SRC-002 §Regras de Negócio). Marcação: V1 = MVP V1; V1.1 = fase seguinte.

| ID | Regra (produto) | Versão | Observação |
|----|-----------------|--------|------------|
| RN-001 | Os votos permanecem secretos até a revelação. Durante a rodada aberta, o sistema exibe apenas a CONTAGEM de votos (ex.: "5 de 7 votaram"), nunca os valores. | V1 | Regra central. |
| RN-002 | Um Participante pode alterar seu voto enquanto a rodada estiver OPEN. | V1 | Complementa RN-008. |
| RN-003 | Somente o Host pode revelar os votos (OPEN → REVEALED). | V1 | Controle do Host. |
| RN-004 | Opcionalmente a sala pode usar Auto Reveal: a revelação dispara automaticamente quando TODOS os habilitados a votar tiverem votado, sem ação do Host. | V1.1 | Confirmado V1.1 pelo PO; confirmação com o Submitter pendente — Q018. |
| RN-005 | Somente o Host pode encerrar uma rodada (REVEALED → CLOSED). | V1 | Controle do Host. |
| RN-006 | Uma tarefa pode ter múltiplas rodadas; o Host pode abrir nova rodada para a mesma tarefa. | V1 | Re-votação. |
| RN-007 | O histórico de todas as rodadas (votos, valores revelados, consenso) é armazenado e consultável. | V1 | Rastreabilidade. |
| RN-008 | Participantes que entrarem após o encerramento da rodada não podem votar retroativamente. | V1 | Sem voto retroativo. |
| RN-009 | O Host pode cancelar uma rodada. | V1 | Ver A4 sobre estado resultante. |
| RN-010 | A estimativa final (consenso) é registrada SEPARADAMENTE dos votos; não precisa ser a média. | V1 | Consenso decidido livremente pelo Host; sem critério mínimo de sistema (A2 resolvida — Q019). |

### Fluxo de Transição de Estado

- Sala: CREATED → IN_PROGRESS → FINISHED. A sala vai a FINISHED por ação explícita do Host (A1 resolvida).
- Tarefa: PENDING → VOTING → ESTIMATED (recebe estimativa_final ao registrar consenso, RN-010).
- Rodada: OPEN → REVEALED → CLOSED (caminho feliz). OPEN —(RN-009 cancelar)→ CANCELLED (preservada no histórico sem consenso, A4 resolvida — Q020). Em REVEALED, o Host registra consenso (RN-010) ao encerrar OU abre nova rodada (RN-006).

**Enum de status de Rodada:** {OPEN, REVEALED, CLOSED, CANCELLED}

- CANCELLED — rodada cancelada pelo Host (RN-009); preservada no histórico (RN-007) sem consenso (A4 resolvida — Q020).

**RN-OBS (V1):** o Host pode promover um participante a Observador. O Observador vê apenas a contagem durante a rodada OPEN (RN-001) e os valores na revelação; é excluído da contagem de "todos votaram" (relevante para RN-004 em V1.1). (A6 resolvida — Q021.)

#### Decisões (A1–A7)

- **A1** — A sala vai a FINISHED por ação explícita do Host (resolvida).
- **A2** — O Host decide o consenso livremente, sem critério mínimo de sistema (RN-010 confirmado; resolvida — Q019).
- **A3** — Desempate é processo humano de discussão ("ouvir menor e maior voto"), não regra de sistema (resolvida).
- **A4** — Status CANCELLED criado; rodada cancelada é preservada no histórico sem consenso (resolvida — Q020).
- **A5** — Sem limite rígido de participantes no V1 (~8 é referência de produto, não constraint de sistema; resolvida).
- **A6** — Observador incluído no V1: Host promove participante a Observador (resolvida — Q021).
- **A7** — Definição de "todos votaram" diferida com RN-004 para V1.1 (resolvida para V1; pendente para V1.1).

`Confidence:` 88 · `Origin:` po_authored · `Source:` SRC-002 §Regras de Negócio; confirm-loop Q018/Q019/Q020/Q021 · `Disposition:` decided · `Hint:` Ambiguidades A1–A7 resolvidas pelo PO; RN-004 confirmado V1.1 (confirmação com o Submitter pendente — Q018); enum de rodada atualizado para incluir CANCELLED; RN-OBS adicionado para V1

---

## Seção 7 — User Stories + Critérios de Aceite
<!-- intake: id=user-stories; blocks=true; min-confidence=80; kind=capture -->
> Rubric: uma história por bloco de valor, "Como [persona], quero [ação], para
> [benefício]"; critérios de aceite em Given/When/Then, verificáveis por não-dev,
> com limites específicos. origin=ai_drafted no draft pass; o PO confirma.

User stories do fluxo MVP V1. Personas: Desenvolvedor, Product Owner, Scrum Master/Facilitador (Host), Tech Lead, Gestor.

**ST-001 — Criar sala e compartilhar link.** Como Facilitador, quero criar uma sala e receber um link compartilhável, para reunir o time sem configuração prévia.
- Given um Facilitador na tela inicial, when ele cria uma sala, then a sala é criada com status CREATED e um link compartilhável é exibido.
- Given uma sala recém-criada, when o Facilitador abre o link, then a mesma sala é acessada.

**ST-002 — Entrar na sala por nome (sem autenticação).** Como Desenvolvedor, quero entrar informando apenas meu nome, para participar sem criar conta.
- Given um link válido, when o participante informa um nome e entra, then é admitido como Participante e vê a tarefa atual e o estado da rodada.
- Given uma sessão em andamento, when alguém entra por nome, then nenhuma autenticação/senha é exigida (assumption b).

**ST-003 — Cadastrar tarefas.** Como Host, quero cadastrar as tarefas a estimar, para conduzir a sessão tarefa a tarefa.
- Given um Host numa sala, when adiciona uma tarefa, then ela aparece com status PENDING.
- Given uma lista de tarefas, when o Host inicia a votação de uma, then a tarefa vai a VOTING e é apresentada a todos.

**ST-004 — Votar com sigilo.** Como Desenvolvedor, quero escolher minha carta sem que os outros vejam, para estimar sem influência.
- Given uma rodada OPEN, when o participante seleciona uma carta da escala, then o voto é registrado e os demais não veem o valor (RN-001).
- Given rodada OPEN com votos parciais, when alguém olha o progresso, then vê apenas a contagem, nunca os valores (RN-001).

**ST-005 — Alterar o voto com a rodada aberta.** Como Desenvolvedor, quero mudar meu voto enquanto a rodada estiver aberta.
- Given rodada OPEN e voto registrado, when o participante escolhe outra carta, then o voto é atualizado (RN-002).
- Given rodada REVEALED ou CLOSED, when tenta alterar, then é bloqueado (RN-002/RN-008).

**ST-006 — Revelar os votos (Host).** Como Host, quero revelar quando estiver pronto, para abrir a discussão.
- Given rodada OPEN, when o Host aciona Revelar, then a rodada vai a REVEALED e todos os votos são exibidos (RN-003).
- Given rodada OPEN, when um não-Host procura revelar, then a ação não está disponível (RN-003).

**ST-007 — Nova rodada após discussão.** Como Host, quero abrir nova rodada para a mesma tarefa, para re-votar.
- Given tarefa com rodada REVEALED/CLOSED, when o Host inicia nova rodada, then uma nova rodada OPEN é criada para a mesma tarefa e os votos anteriores ficam no histórico (RN-006/RN-007).

**ST-008 — Registrar o consenso.** Como Host, quero registrar a estimativa final, para fechar a tarefa.
- Given rodada REVEALED, when o Host registra a estimativa final, then o Host registra a estimativa final livremente (sem critério mínimo de sistema, A2 resolvida — Q019); o consenso é gravado separadamente dos votos (RN-010) e a tarefa vai a ESTIMATED.
- Given divergência, when registra o consenso, then o valor não precisa ser a média (RN-010).

**ST-009 — Consultar histórico da sessão.** Como Tech Lead, quero consultar o histórico de rodadas e estimativas, para justificar estimativas e evitar repetir discussões.
- Given sessão com tarefas estimadas, when abre o histórico, then vê por tarefa as rodadas, votos revelados e consenso (RN-007).
- Given tarefa com múltiplas rodadas, when a inspeciona, then vê cada rodada na ordem em que ocorreu.

**ST-010 — Visibilidade para Gestor/PO.** Como PO/Gestor, quero ver as estimativas consolidadas, para priorizar e planejar.
- Given sessão com tarefas ESTIMATED, when o PO consulta a sessão, then vê a estimativa_final de cada tarefa. No V1, as estimativas consolidadas são visíveis via histórico da sessão (RN-007/ST-009); um dashboard de gestão dedicado é V2 (fora do escopo V1).

**ST-011 — Acompanhar como Observador.** Como Gestor/Stakeholder, quero acompanhar a sessão sem votar, para observar sem influenciar.
- Given um participante na sala, when o Host o promove a Observador, then ele passa a Observador e durante a rodada OPEN vê apenas a contagem (RN-001), e na revelação vê os valores; e não é contado em "todos votaram" (RN-OBS/A6 resolvida — Q021).

`Confidence:` 86 · `Origin:` po_authored · `Source:` SRC-002 §MVP V1; RN-001..RN-010; confirm-loop Q019/Q020/Q021 · `Disposition:` decided · `Hint:` ST-001..ST-011 cobrem o fluxo V1; ST-008 firmado (A2 resolvida); ST-010 clarificado (dashboard = V2); ST-011 adicionado para papel Observador (A6 resolvida); Auto Reveal RN-004 deliberadamente sem story (V1.1)

---

## Seção 8 — Requisitos Não-Funcionais (NFRs)
<!-- intake: id=nfrs; blocks=true; min-confidence=70; kind=capture -->
> Rubric: preencher apenas as dimensões aplicáveis (checklist ISO/IEC 25010 — não
> forçar as irrelevantes). O PO descreve o requisito de qualidade; viabilidade e
> *como* são do Technical Assessment. Sem ao menos uma dimensão preenchida,
> a seção NÃO está satisfeita.

NFRs no scaffold ISO/IEC 25010 — apenas as dimensões que a demanda plausivelmente precisa. Valores-alvo são REQUISITOS DE QUALIDADE do PO, não afirmações de viabilidade. Viabilidade (sobretudo estado em tempo real para participantes simultâneos — assumption a) pertence ao Technical Assessment.

- **Performance efficiency (sincronização de estado):** ao revelar (RN-003) ou registrar voto, a mudança reflete para todos os conectados em até ≈2 s p95 (alvo de produto definido pelo PO — Q025); a contagem de progresso atualiza em tempo quase real. [Viabilidade → Technical Assessment.]
- **Reliability (consistência da rodada):** estado (OPEN/REVEALED/CLOSED/CANCELLED) e votos não se perdem por falha intermitente; ao reconectar, o participante vê o estado correto (sem voto fantasma/duplicado). Disponibilidade-alvo na sessão: [a definir — refinamento não-bloqueante].
- **Security / Confidentiality (sigilo do voto — RN-001):** valores não podem ser obtidos por nenhum participante antes da revelação, inclusive por inspeção do cliente/rede; durante OPEN só trafega contagem. [O como → Technical Assessment.]
- **Security / Access control (controle do Host — RN-003/005/009):** revelar/encerrar/cancelar só pelo Host. Política de produto: o Host original reassume os direitos de Host pelo mesmo link na reconexão (EC-02/Q023); o mecanismo de vínculo de identidade sem login é questão do Technical Assessment.
- **Usability (entrada sem fricção):** novo participante pronto para votar fornecendo só um nome, sem cadastro. Alvo: [a definir — refinamento não-bloqueante].
- **Compatibility (acesso por navegador):** participantes entram pelo link em navegador, possivelmente em dispositivos diferentes. Navegadores/dispositivos suportados: [a definir — refinamento não-bloqueante].

Dimensões não propostas por falta de base: Maintainability, Portability (→ TA se relevantes). Functional suitability é coberta pelas Regras de Negócio.

`Confidence:` 72 · `Origin:` po_authored · `Source:` SRC-002 §NFRs; confirm-loop Q023/Q025 · `Disposition:` decided · `Hint:` Alvo de latência ≈2s p95 firmado pelo PO (Q025); política de identidade do Host firmada (EC-02/Q023); itens [a definir] são refinamentos não-bloqueantes; viabilidade e mecanismos → Technical Assessment`

---

## Seção 9 — Edge Cases e Modos de Falha
<!-- intake: id=edge-cases; blocks=true; min-confidence=70; kind=capture -->
> Rubric: estados de erro, timeouts, permissões, concorrência. Para features de IA:
> comportamento do modelo e baixa-confiança. Primeira classe — não rodapé. Cada
> item descreve o comportamento esperado do sistema (não apenas o que pode dar errado).

Edge cases ancorados nas RNs e no fluxo V1. Cada item: cenário + comportamento esperado; [DISCOVERY] onde a spec não dá base.

- **EC-01 Participante sai no meio da rodada (OPEN):** no V1 a contagem "X de Y" é informativa; o denominador conta os participantes atualmente na sala. O voto de um participante que reconecta persiste (EC-08). O gatilho "todos votaram" só importa para Auto Reveal (RN-004), diferido a V1.1 (A7 resolvida).
- **EC-02 Host desconecta/sai:** política de produto: o Host original reassume os direitos de Host pelo mesmo link ao reconectar (Q023). O mecanismo de identidade-sem-login para implementar essa política → Technical Assessment.
- **EC-03 Reveal com votos parciais (RN-003):** a rodada vai a REVEALED exibindo os votos existentes e marcando ausentes como "não votou". Representação de "não votou" é detalhe de UI (não-bloqueante para o release V1).
- **EC-04 Rodada com zero votos:** a revelação não produz consenso automático; o Host pode cancelar (RN-009, gerando status CANCELLED) ou registrar consenso manual (RN-010). Revelar com zero votos é permitido (controle do Host, RN-003).
- **EC-05 Late joiner após o encerramento (RN-008):** não pode votar retroativamente; pode participar da próxima rodada (RN-006).
- **EC-06 Nomes duplicados na entrada:** nomes duplicados são permitidos; o sistema desambigua internamente (id de sessão único por participante; sufixo/avatar opcional na UI), preservando a atribuição correta do voto (Q024).
- **EC-07 Rodada cancelada (RN-009):** cancelar uma rodada (RN-009) a leva ao status CANCELLED, preservada no histórico sem consenso (A4 resolvida — Q020).
- **EC-08 Refresh/reconexão do navegador:** ao reconectar, ver o estado atual; voto em rodada OPEN persiste (sem perder/duplicar). [O como (persistência sem login) → Technical Assessment.]
- **EC-09 Ação restrita por não-Host (RN-003/005/009):** negada/indisponível; só o Host executa.
- **EC-10 Alterar voto fora da rodada aberta (RN-002/008):** bloqueado.
- **EC-11 Votos simultâneos/concorrência:** a contagem converge para o total correto sem perder votos. [Garantia de concorrência → Technical Assessment.]

Nota: não há feature de IA neste escopo.

`Confidence:` 78 · `Origin:` po_authored · `Source:` SRC-002; RN-001..RN-OBS; confirm-loop Q020/Q021/Q023/Q024 · `Disposition:` decided · `Hint:` EC-01/02/06/07 resolvidos por decisão de produto do PO; EC-02 e EC-08/EC-11 ainda têm componente técnico roteado ao TA; EC-09/EC-10 firmes por RN

---

## Seção 10 — Métricas de Sucesso (primária · secundária · guardrail)
<!-- intake: id=metrics; blocks=true; min-confidence=70; kind=capture -->
> Rubric: valores projetados — o baseline que metrics.md confronta com o medido
> pós-rollout. Inclua indicadores leading e lagging e ao menos um guardrail (a
> métrica que não pode piorar). Cada meta carrega a confiança da projeção.

Métricas-proxy — alvos diferidos à Discovery (PO confirmou disposição):

- **Leading (eficiência):** redução do tempo operacional por sessão — ALVO diferido à Discovery (cifra suprimida até correção do modelo, Q026/Q029).
- **Leading (rastreabilidade):** % de rodadas com histórico armazenado e consultável (qualitativo/contável, não dependente do modelo aritmético).
- **Lagging (qualidade):** melhoria da previsibilidade/qualidade das estimativas via decisões registradas e divergências rastreáveis.
- **Guardrail:** nenhum guardrail firmado — diferido à Discovery.

`Confidence:` 50 · `Origin:` po_authored · `Source:` intake id=impact (proxies); Discovery brief item 3; confirm-loop Q026/Q029 · `Disposition:` discovery · `Hint:` Cifra de economia suprimida (inconsistência aritmética ~10x não corrigida); alvos diferidos à Discovery pelo PO (Q026); % de rodadas com histórico é métrica contável e não model-dependent; nenhum guardrail firmado

---

## Seção 11 — Critérios de Sucesso e Aceite (do release)
<!-- intake: id=release-criteria; blocks=true; min-confidence=70; kind=capture -->
> Rubric: indicadores de alto nível que definem "concluído e valioso" para este
> release — distintos das métricas contínuas da Seção 10. Deve cobrir ao menos
> as dimensões Negócio, Qualidade e UX. Critérios genéricos ("funciona bem") NÃO
> estão satisfeitos: exija valor alvo mensurável.

**Negócio:** o fluxo essencial de uma sessão de estimativa é executável fim-a-fim (criar sala → entrar por nome → votar com sigilo → revelar → consenso → histórico) sem ferramentas externas.

**Qualidade:** RNs centrais respeitadas e verificáveis — sigilo até a revelação (RN-001), voto alterável só com rodada aberta (RN-002), revelação/encerramento/cancelamento só pelo host (RN-003/005/009), múltiplas rodadas (RN-006), histórico completo (RN-007), sem voto retroativo (RN-008), consenso registrado separado dos votos (RN-010).

**UX:** entrada sem autenticação (só nome) funcional; progresso exibe apenas contagem de votos, nunca os valores antes da revelação.

Critério verificável como pass/fail; RN-004 (auto reveal) NÃO é critério do release V1 (é V1.1). Aceito pelo PO (Q027).

`Confidence:` 80 · `Origin:` po_authored · `Source:` SRC-002 §MVP V1; constraints RN-001–RN-010; Discovery brief §critério de saída; confirm-loop Q027 · `Disposition:` decided · `Hint:` Critérios pass/fail confirmados pelo PO; RN-004 explicitamente excluído do release V1; dimensões Negócio/Qualidade/UX cobertas

---

## Seção 12 — Riscos e Dependências (de produto e negócio)
<!-- intake: id=risks; blocks=true; min-confidence=70; kind=capture -->
> Rubric: riscos de produto, negócio, adoção, externos e compliance. Riscos
> técnicos migram para o Technical Assessment. Cada risco tem probabilidade,
> impacto e mitigação. Dependências de produto/negócio listadas separadamente.

Riscos de PRODUTO e NEGÓCIO (riscos técnicos migram para o Technical Assessment):

- **Aderência problema-mercado não validada** (premissas g/h) — Probabilidade: ALTA · Impacto: ALTO · mitigação: Discovery (5–10 entrevistas com segmentos-alvo). [discovery — Discovery]
- **Willingness-to-pay desconhecida / monetização não testada** (premissa f) — Probabilidade: MÉDIA · Impacto: ALTO · mitigação: teste de conceito/landing + perguntas de preço. [discovery]
- **Inconsistência aritmética no modelo de eficiência** (~10x) — Probabilidade: CONFIRMADA (ocorrida) · Impacto: MÉDIO (credibilidade) · mitigação: suprimir cifras até corrigir (Discovery item 3). [discovery]
- **Urgência ausente** — Probabilidade: N/A · Impacto: BAIXO-MÉDIO (enfraquece priorização) · mitigação: reavaliar via Discovery item 5.
- **Público pode não praticar Planning Poker** (premissa e) — Probabilidade: BAIXA-MÉDIA · Impacto: MÉDIO (posicionamento/onboarding) · mitigação: validar nas entrevistas. [assumption]

**Dependências de produto/negócio:** Jira/Linear são V2; o MVP V1 não depende delas.

`Confidence:` 78 · `Origin:` po_authored · `Source:` intake id=impact (hint), id=assumptions (f)(g)(h), id=urgency, triage; confirm-loop Q028 · `Disposition:` decided · `Hint:` Prob/Impacto firmados pelo PO; itens comerciais (g/h/f) validados na Discovery; inconsistência aritmética: cifras suprimidas até correção; Jira/Linear confirmadas como V2`

---

## Seção 13 — Avaliação Preliminar de Esforço e Custo
<!-- intake: id=effort-estimate; blocks=false; min-confidence=0; kind=capture -->
> Rubric: somente uso interno — o chute do PO para sustentar sequenciamento. O
> número firme vem do CTO no Technical Assessment. Não é compromisso contratual
> nem material para cliente. Confiança esperada: baixa (ai_drafted ou po_authored
> sem dados firmes).

Avaliação preliminar (interna, para sequenciamento — NÃO compromisso): O MVP V1 é caracterizado como extensão de UI/estado com regras bem definidas (RN-001–RN-010), sem pagamentos, sem multi-tenancy complexo, sem AI/runtime e sem integrações externas (V2). A entrada sem autenticação reduz a superfície. O ponto de esforço/risco técnico em aberto é o estado em tempo real para múltiplos participantes simultâneos (premissa a) — viabilidade a racionalizar pelo Tech Lead.

`Confidence:` 30 · `Origin:` inherited · `Source:` SRC-002 §MVP V1; intake id=cto_escalation · `Disposition:` deferred · `Hint:` Não-bloqueante; número firme vem do Technical Assessment do CTO; a premissa de tempo real (a) pode mover a estimativa

---

## Seção 14 — Roadmap Sugerido
<!-- intake: id=roadmap; blocks=false; min-confidence=0; kind=capture -->
> Rubric: visão de sequenciamento de valor além deste release. Items adiados da
> Seção 5 alimentam fases futuras. MVP é este release; Fase 2 e Fase 3 são
> backlog futuro. Não é compromisso de entrega.

### MVP (este release)

Criar sala, compartilhar link, entrar sem autenticação, cadastro de tarefas, votação secreta, revelação, múltiplas rodadas, definição de consenso, histórico da sessão.

### Fase 2 (backlog futuro)

V1.1 — Cronômetro, auto reveal (RN-004), estatísticas automáticas, exportação CSV.

### Fase 3 (backlog futuro)

V2 — Integração Jira, integração Linear, times permanentes, histórico organizacional, dashboard de métricas, comparação entre rodadas, comentários anônimos por voto.

`Confidence:` 65 · `Origin:` inherited · `Source:` SRC-002 §Funcionalidades do MVP; intake id=priority · `Disposition:` assumption · `Hint:` Não-bloqueante; o escalonamento V1>V1.1>V2 é priorização de escopo, não prioridade de portfólio; confirmar escopo de V2 (premissa d)

---

## Referência ao Technical Assessment
<!-- intake: id=tech-assessment-ref; blocks=false; min-confidence=0; kind=derived; inputs=scope,business-rules,nfrs,risks -->
> Rubric: ponte para o artefato do CTO — status + veredito + link, NÃO conteúdo.
> Se a escalada for requisitada, congela só com Disposition=deferred (TA pendente,
> fora do escopo desta ferramenta) ou Status=Assinado quando o TA existir.

**TechAssessmentRef**
- status: `requested`
- verdict: — (pendente; populado quando status = signed)
- disposition: `deferred`
- link: — (skill `tech-assessment` ainda não existe)

**Decisão:** Escalada ao CTO **requisitada**. O MVP V1, apesar de modesto em escopo de produto, carrega incógnitas de VIABILIDADE TÉCNICA que pertencem ao Technical Assessment (TA), não à decisão de produto do PO. Isto corrige o rascunho do intake ("Needed: No"), que subdimensionou as questões de tempo real, sigilo em transporte e identidade-sem-login como racionalização de Tech Lead em vez de gatilhos do CTO.

**Gatilhos arquiteturais disparados:**
1. **Runtime / estado em tempo real** (premissa (a)): sincronização de estado entre participantes simultâneos, com alvo de latência (~2s p95), consistência de rodada (OPEN/REVEALED/CLOSED) e reconexão sem voto fantasma/duplicado (NFR Performance/Reliability; EC-08; EC-11). Maior risco técnico em aberto do MVP.
2. **Segurança / autenticação / autorização**: (a) sigilo do voto em transporte (RN-001) — valores não podem vazar por inspeção do cliente/rede antes da revelação; (b) identidade confiável do Host SEM login (premissa (b)) — ações host-only (revelar/encerrar/cancelar, RN-003/005/009) e sucessão de Host em desconexão (EC-02) dependem de um vínculo de identidade que o V1 não autentica.

**Não são gatilhos no V1:** multi-tenancy / isolamento de dados (org-level é V2) e integrações externas Jira/Linear (V2).

**O TA deve emitir veredito sobre, no mínimo:** (i) viabilidade da sincronização de estado em tempo real para participantes simultâneos e o modelo de concorrência; (ii) como garantir o sigilo do voto em transporte/cliente (RN-001); (iii) como vincular identidade do Host de forma confiável sem autenticação (RN-003/005/009 + EC-02), incluindo o mecanismo que permite ao Host original reassumir os direitos pelo mesmo link na reconexão (política decidida pelo PO em Q023 — o "como" técnico é responsabilidade do TA).

**Distinção produto vs técnica:** o que conta como consenso (A2), nomes duplicados (EC-06) e papel Observador (A6) são decisões de PRODUTO do PO; tempo real, sigilo em transporte e identidade-sem-login são VIABILIDADE TÉCNICA do CTO.

**Freeze provisório:** a skill `tech-assessment` ainda não existe; por isso o TA fica `deferred` ("TA needed; tech-assessment skill not yet available") e o RP congela PROVISORIAMENTE — seções de produto congeladas, com o manifesto registrando `tech-assessment-ref: deferred (TA pendente — fora do escopo atual da ferramenta)`. Migração: quando a skill `tech-assessment` existir, apertar o portão para exigir `status = signed` antes do congelamento definitivo.

`Confidence:` computed · `Origin:` ai_drafted · `Source:` readiness-escalation-flagger; inputs: scope, business-rules, nfrs, risks · `Status:` requested · `Disposition:` deferred · `Hint:` TA disparado por gatilhos arquiteturais (runtime/tempo real + segurança/identidade); skill tech-assessment inexistente → deferred; freeze provisório do RP até TA signed

<!-- END OF DOCUMENT -->
