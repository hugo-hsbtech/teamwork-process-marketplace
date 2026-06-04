# Golden exemplar (self-contained) — calibration reference

A condensed, fictional, repo-independent example of a *well-filled* Readiness
Package. Use it to calibrate quality: problem-not-solution depth, honest confidence
and origin per section, used dispositions, testable Given/When/Then acceptance
criteria, NFRs that don't claim feasibility, and an honestly-flagged Technical
Assessment reference. Do not copy its content — copy its *bar*.

---

**Demand:** Self-service seat management for enterprise admins (origination INT-2026-014).

---

**Contexto e Problema** — `Confidence: 86 · Origin: inherited · Source: origination INT-2026-014 §problem + support export Q1 · Status: resolved · Disposition: inherited · Hint: herdado do origination a 88; levemente rebaixado por falta de breakdown por conta — CS pode detalhar para ~93`

Enterprise admins não conseguem adicionar ou remover assentos sem abrir ticket de suporte; o lead time é de 1–3 dias úteis. Em ondas de onboarding, um único admin chega a abrir 5–10 tickets. No Q1, 240 tickets foram desse tipo (18% do volume enterprise). A dor é a dependência e a espera — não a ausência de um botão.

`Confidence: 86 · Origin: inherited · Source: origination INT-2026-014 §problem + support export Q1 · Status: resolved · Disposition: inherited · Hint: herdado do origination a 88; levemente rebaixado por falta de breakdown por conta — CS pode detalhar para ~93`

---

**User Stories + Critérios de Aceite** — `Confidence: 80 · Origin: ai_drafted · Source: drafted from scope + origination personas · Status: resolved · Disposition: ai_drafted · Hint: PO confirmou ST-001 e ST-002; AC verificáveis por QA sem acesso ao código`

**ST-001 — Self-service seat add/remove**
Como admin enterprise, quero adicionar ou remover assentos no painel de faturamento, para não depender do suporte para gestão de licenças.

*Given* um admin autenticado na tela de faturamento *when* ele aumenta o número de assentos em 1 *then* o novo assento fica ativo em até 60 segundos e aparece na prévia da próxima fatura antes de encerrar a sessão.

*Given* um admin autenticado *when* ele tenta reduzir assentos abaixo do número de usuários ativos *then* o sistema bloqueia a ação e exibe uma mensagem indicando quantos usuários precisam ser desativados primeiro.

**ST-002 — Auditoria de mudanças de assento**
Como admin enterprise, quero ver um log das alterações de assentos dos últimos 90 dias, para auditar mudanças sem depender do suporte.

*Given* um admin na tela de auditoria *when* ele abre o log de assentos *then* vê cada evento (quem alterou, de N para M, data/hora) em ordem cronológica reversa.

`Confidence: 80 · Origin: ai_drafted · Source: drafted from scope + origination personas · Status: resolved · Disposition: ai_drafted · Hint: PO confirmou ST-001 e ST-002; AC verificáveis por QA sem acesso ao código`

---

**Requisitos Não-Funcionais** — `Confidence: 65 · Origin: ai_drafted · Source: drafted from comparable billing flows + SLA padrão da plataforma · Status: low_confidence · Disposition: ai_drafted · Hint: targets são estimativa; viabilidade e como atingir são do CTO no Technical Assessment — não assumir factibilidade aqui`

*(ISO/IEC 25010 — apenas dimensões aplicáveis)*

- **Performance efficiency**: A confirmação de adição de assento deve ser devolvida ao cliente em ≤ 3 s (p95) sob carga normal da plataforma.
- **Reliability**: O fluxo de seat management deve ter disponibilidade ≥ 99,5% mensais; falhas intermediárias não podem resultar em cobrança sem provisionamento ou provisionamento sem cobrança.
- **Security**: Somente usuários com a role `billing_admin` podem executar mudanças de assento; cada ação deve ser registrada em audit trail imutável com atribuição de usuário.

O PO define o *requisito de qualidade*. Se os targets são atingíveis com a arquitetura atual ou exigem mudança de plataforma é questão para o Technical Assessment.

`Confidence: 65 · Origin: ai_drafted · Source: drafted from comparable billing flows + SLA padrão da plataforma · Status: low_confidence · Disposition: ai_drafted · Hint: targets são estimativa; viabilidade e como atingir são do CTO no Technical Assessment — não assumir factibilidade aqui`

---

**Métricas de Sucesso** — `Confidence: 62 · Origin: ai_drafted · Source: support export Q1 + inferred from two comparable feature rollouts · Status: low_confidence · Disposition: inferred · Hint: baseline de 240 tickets/trimestre é firme; projeção de redução é estimativa — confrontar com dado real 60 dias pós-rollout`

| Tipo | Métrica | Baseline | Target (90 dias pós-rollout) |
|---|---|---|---|
| **Primária** | Tickets de seat management / trimestre | 240 | ≤ 60 (−75%) |
| **Secundária** | % de alterações de assento feitas pelo admin sem suporte | ~0% | ≥ 85% |
| **Guardrail** | Taxa de erro de faturamento (cobrança sem provisionamento ou vice-versa) | < 0,1% | não piorar |

`Confidence: 62 · Origin: ai_drafted · Source: support export Q1 + inferred from two comparable feature rollouts · Status: low_confidence · Disposition: inferred · Hint: baseline de 240 tickets/trimestre é firme; projeção de redução é estimativa — confrontar com dado real 60 dias pós-rollout`

---

**Referência ao Technical Assessment**

| Campo | Valor |
|---|---|
| **Status** | not_requested |
| **Veredito** | — |
| **Link** | — |
| **Escalada requisitada?** | Sim — NFR de reliability (consistência billing ↔ provisionamento) requer avaliação de arquitetura |

`Confidence: 40 · Origin: ai_drafted · Source: RP draft pass · Status: low_confidence · Disposition: deferred · Hint: TA ainda não solicitado formalmente; congelamento do RP provisório até o CTO assinar — Disposition=deferred é o estado correto enquanto o TA skill não estiver disponível ou a escalada não for concluída`

---

*Textura: herdado onde o origination resolveu (Origin: inherited); rascunhado pela IA onde foi necessário derivar (Origin: ai_drafted); confiança alta só onde há evidência, honestamente rebaixada nas projeções; NFRs descrevem o requisito de qualidade — não afirmam viabilidade; TA referenciado com Disposition=deferred e motivo explícito.*

<!-- END OF DOCUMENT -->
