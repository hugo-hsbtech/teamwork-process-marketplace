# Q&A Ledger — pokerplan (readiness phase)

> Phase: .teamwork/20260603-1833-pokerplan-a8432a/readiness · Template: readiness-package-v1 · Rev: 3 · Updated: 2026-06-03
> Readiness: 78% (PO confirm-loop Phase 3 completed) · Gate: PROVISIONAL FREEZE · Open blocking: effort-estimate (deferred/TA), nfrs (partial — browser matrix TBD), tech-assessment-ref (requested/deferred); commercial items (objectives/metrics target values, risks f/g/h, exec-summary Layer B) honestly disposed as discovery

<!-- rev: 3 · updated: 2026-06-03 -->

**Entry counts:** 29 total · 6 answered · 23 parked (assumption/discovery/deferred) · 0 open · Sections promoted to po_authored by Phase 3: scope, release-criteria, risks (firm ratings assigned); business-rules, edge-cases, user-stories, nfrs substantially resolved; objectives/metrics confirmed as honest discovery disposition; arithmetic inconsistency resolved by suppression (Discovery item 3). Gate capped at PROVISIONAL FREEZE pending Technical Assessment.

---

## Q001 · targets: exec-summary · status: parked

- **Rationale:** The executive summary is the first gate section; it must convey a firm, verifiable business outcome. The readiness-inheritor synthesized this from intake problem, originator statement, SRC-002 product objective, MVP V1 scope, and impact Layer B. Confidence fell below the section minimum (70) because Layer B (commercial/SaaS opportunity) is entirely unvalidated — no TAM, no revenue projection, no willingness-to-pay signal. Recording here to make the gap auditable and to drive the PO to confirm verifiable objectives and close scope before the RP is submitted.
- **Spawned-by:** readiness-inheritor
- **Asked:** 2026-06-03
- **Mode:** open
- **Question:** What is the firm, verifiable executive summary — including a concrete business outcome — for the Planning Poker product?
- **Choice:** —
- **Answer:** Synthesized draft: a real-time collaborative Planning Poker tool enabling remote agile squads to run estimation sessions without leaving their existing workflow. Commercial (SaaS per-org) opportunity posited but not validated. No firm revenue projection or TAM available at intake.
- **Disposition:** assumption
- **Confidence:** 68
- **Source:** synthesis of intake id=problem (conf 84) + intake id=originator (conf 85) + SRC-002 product objective + SRC-002 MVP V1 scope + intake id=impact Layer B (conf 70, discovery)
- **Hint:** conf 68 < section min 70. Commercial Layer B unvalidated; cannot assert firm business outcome. PO must confirm verifiable objectives and close scope to raise confidence above threshold. Carry into Discovery for market validation.
- **Follow-ups:** —

## Q002 · targets: context-problem · status: answered

- **Rationale:** The context-and-problem section needs a direct, well-sourced description of the pain the product solves — ideally from the submitter's own words. The inheritor confirmed this section was answered directly by the submitter (Q006 + Q007 in the intake interview) and confidence meets the section minimum.
- **Spawned-by:** readiness-inheritor
- **Asked:** 2026-06-03
- **Mode:** open
- **Question:** What is the concrete problem this product solves, in the target user's context?
- **Choice:** —
- **Answer:** Remote/distributed agile teams struggle to run Planning Poker estimation sessions: tool-switching friction, lack of real-time synchronous participation, no native lightweight option. Pain well-described by submitter with direct examples. Quantification (8–11 h-h/year per squad) is present but carries an arithmetic inconsistency (~10x discrepancy vs model-derived figure); numbers must not be used in materials until corrected in Discovery.
- **Disposition:** answered
- **Confidence:** 84
- **Source:** Submitter direct — intake id=problem (Q006 + Q007)
- **Hint:** Pain is well-described and no solution is prescribed (good intake hygiene). The ~10x arithmetic inconsistency in the efficiency model (8–11 h-h/year cited vs ~96–128 h-h/year model-derived) must be resolved in Discovery before using any savings figure. This inconsistency is carried forward explicitly; see Q011 (inherited-readiness).
- **Follow-ups:** Q011

## Q003 · targets: objectives · status: parked

- **Rationale:** The RP rubric requires at least 2 verifiable, numbered objectives with measurable target values. The intake had no dedicated objectives section; the inheritor inferred objectives from SRC-002 product objective and intake impact/problem signals. Confidence is well below the section minimum (70) because none of the inferred objectives carry confirmed target values, and objective-4 depends on a broken efficiency model.
- **Spawned-by:** readiness-inheritor
- **Asked:** 2026-06-03
- **Mode:** open
- **Question:** What are the 2+ verifiable, measurable objectives for the Planning Poker product (with stated target values per objective)?
- **Choice:** —
- **Answer:** Inferred from SRC-002 product objective and intake id=impact + id=problem. Draft candidates: (1) enable real-time collaborative estimation for remote squads; (2) reduce estimation-session friction/tool-switching; (3) achieve SaaS adoption at org level; (4) reduce estimation overhead by X h-h/squad/year (figure blocked pending arithmetic fix). No target values confirmed by PO.
- **Disposition:** assumption
- **Confidence:** 60
- **Source:** SRC-002 product objective; intake id=impact; intake id=problem
- **Hint:** conf 60 < section min 70. LOWERED from intake: intake had no graded objectives section; inferred only. PO must (a) confirm and number each objective, (b) assign measurable target values, (c) not use the efficiency figure until the arithmetic inconsistency is resolved (Discovery item 3). Objective-4 target is blocked until then.
- **Follow-ups:** Q011

## Q004 · targets: personas · status: answered

- **Rationale:** Persona and market-segment clarity is required for RP reach section. The inheritor confirmed this was directly answered by the submitter across two intake questions (Q008 personas, Q010 market segments). Confidence meets the section minimum (70). TAM is intentionally left unsized — Discovery handles that.
- **Spawned-by:** readiness-inheritor
- **Asked:** 2026-06-03
- **Mode:** open
- **Question:** Who are the primary personas and target market segments for the Planning Poker product?
- **Choice:** —
- **Answer:** Primary persona: Scrum Master / Agile Coach running estimation sessions. Secondary: Development team members (estimators). Market segments: distributed/remote agile teams, software development squads in mid-to-large orgs. TAM is unsized at intake; do not invent market numbers.
- **Disposition:** answered
- **Confidence:** 78
- **Source:** Submitter direct — intake id=reach (Q008 personas + Q010 market segments)
- **Hint:** Personas and segments are clear from submitter. TAM left unsized intentionally — sizing is a Discovery deliverable. Do not invent or project TAM until Discovery is complete.
- **Follow-ups:** Q011

## Q005 · targets: scope · status: parked

- **Rationale:** Scope clarity (included AND explicitly excluded items) is mandatory for the RP, with a minimum confidence of 75. The intake declared MVP V1/V1.1/V2 phases but contained no explicit Excluded list. The inheritor lowered confidence from ~80 to 62 because the RP rubric makes Excluded mandatory, and two constraints (no-auth in MVP, hard vs. soft constraint status) are unconfirmed assumptions.
- **Spawned-by:** readiness-inheritor
- **Asked:** 2026-06-03
- **Mode:** open
- **Question:** What is explicitly IN scope for MVP V1, and what is explicitly OUT of scope (excluded) — including hard vs. preference-based constraints?
- **Choice:** —
- **Answer:** Included (V1 from SRC-002): real-time session creation, Fibonacci + T-Shirt scales, name-only participation (no auth), room/link sharing, basic result reveal. Excluded: Jira/Linear integrations (V2 per spec assumption d), user authentication system (assumption b — confirm if MVP-only or permanent exclusion), V1.1 auto-reveal (RN-004 — see Q011). Hard vs. preference constraints not yet distinguished for assumptions b and d.
- **Disposition:** assumption
- **Confidence:** 62
- **Source:** SRC-002 MVP V1/V1.1/V2 phase definitions; intake id=priority; intake id=constraints
- **Hint:** conf 62 < section min 75. LOWERED: intake lacked explicit Excluded list. PO must (a) formally declare what is OUT of MVP V1, (b) confirm whether no-auth (assumption b) is MVP-only or a permanent product decision, (c) confirm whether Jira/Linear exclusion (assumption d) is a hard constraint or a preference. Deferred items feed the Roadmap section. RN-004 (auto-reveal) is V1.1 not V1 — see Q011.
- **Follow-ups:** Q011

## Q006 · targets: metrics · status: parked

- **Rationale:** The RP metrics section requires measurable baselines, at least one leading and one lagging indicator, and at least one guardrail metric. None of these exist as discrete entries in the intake; only proxy signals embedded in the impact section (with an arithmetic inconsistency). Confidence is well below the section minimum (70) and the disposition is discovery because the metrics must be defined with the PO and validated before use.
- **Spawned-by:** readiness-inheritor
- **Asked:** 2026-06-03
- **Mode:** open
- **Question:** What are the measurable baseline metrics, leading/lagging indicators, and guardrail metric(s) for the Planning Poker product?
- **Choice:** —
- **Answer:** No discrete metrics section exists in intake. Proxies found in intake id=impact: estimation session duration, h-h/squad/year reduction, adoption rate. Arithmetic inconsistency in efficiency model (8–11 h-h/year cited vs ~96–128 h-h/year model-derived) means the key savings figure cannot be used. No baseline, no guardrail metric, no leading indicator defined.
- **Disposition:** discovery
- **Confidence:** 45
- **Source:** intake id=impact proxies; Discovery brief item 3
- **Hint:** conf 45 < section min 70. LOWERED: no dedicated metrics section in intake. PO must define (a) measurable baselines for each metric, (b) at least 1 leading indicator, (c) at least 1 lagging indicator, (d) at least 1 guardrail metric. The efficiency savings figure MUST NOT be used in any material until the arithmetic inconsistency is corrected (Discovery item 3). This is a blocking gap.
- **Follow-ups:** Q011

## Q007 · targets: release-criteria · status: parked

- **Rationale:** Release criteria must cover Business, Quality, and UX dimensions with measurable acceptance targets per dimension. The intake lacked this level of definition; the inheritor derived a draft from Discovery exit criteria, MVP V1 scope, and constraints (RN-001..RN-010). Confidence is below the section minimum (70). Note: RN-004 (auto-reveal) was found to be missing from the intake constraints table — it is a V1.1 feature, not a V1 release criterion.
- **Spawned-by:** readiness-inheritor
- **Asked:** 2026-06-03
- **Mode:** open
- **Question:** What are the measurable release-acceptance criteria for MVP V1, covering Business, Quality, and UX dimensions?
- **Choice:** —
- **Answer:** Draft derived from SRC-002 MVP V1 and constraints RN-001..RN-010 (noting RN-004 gap — see Q011). No PO-confirmed measurable targets per dimension. No separation between continuous metrics and release gate criteria. RN-004 (auto-reveal) erroneously absent from intake constraints table; treated as V1.1 feature.
- **Disposition:** assumption
- **Confidence:** 55
- **Source:** SRC-002 MVP V1; constraints RN-001..RN-010; Discovery brief exit criteria
- **Hint:** conf 55 < section min 70. LOWERED: intake lacked measurable release acceptance across Business/Quality/UX. PO must (a) separate release criteria from continuous product metrics, (b) assign measurable target per dimension (e.g. error rate, session completion rate, user satisfaction threshold), (c) confirm RN-004 is V1.1 not a V1 release criterion. Flag RN-004 gap to Drafter and confirm with Submitter.
- **Follow-ups:** Q011

## Q008 · targets: risks · status: parked

- **Rationale:** The RP risks section covers PRODUCT and BUSINESS risks only (technical risks migrate to the Technical Assessment). The inheritor composed a risk register from parked/discovery items in the intake. Confidence is below the section minimum (70) because open dispositions remain across all material risks and no firm probability/impact assignments exist from the PO.
- **Spawned-by:** readiness-inheritor
- **Asked:** 2026-06-03
- **Mode:** open
- **Question:** What are the product and business risks (probability + impact) for the Planning Poker product? (Technical risks are out of scope here — they go to the Technical Assessment.)
- **Choice:** —
- **Answer:** Risk candidates from intake: (f) monetization/SaaS willingness-to-pay untested — discovery, high risk; (g) no formal market validation or revenue projection — discovery, high risk; (h) problem distribution assumed broad but market base unsized — discovery; urgency window absent (no competitor, no deadline declared). Real-time synchronous session risk (assumption a) is EXCLUDED here — it migrates to Technical Assessment.
- **Disposition:** discovery
- **Confidence:** 60
- **Source:** intake id=impact hint; intake id=assumptions (f)(g)(h); intake id=urgency; triage
- **Hint:** conf 60 < section min 70. Composite of parked/discovery items; all carry open dispositions. PO must assign firm probability and impact to each risk. Assumption (a) re: real-time sessions is a TECHNICAL risk — do not include here; route to Tech Lead / Technical Assessment. Discovery must address (f)(g)(h) before risks can be rated with confidence.
- **Follow-ups:** Q011

## Q009 · targets: effort-estimate · status: parked

- **Rationale:** A preliminary effort estimate is required as a non-blocking RP input. The inheritor flagged this as deferred: no firm engineering estimate exists and the real-time architecture assumption (a) may shift the estimate materially. The CTO Technical Assessment is the authoritative source.
- **Spawned-by:** readiness-inheritor
- **Asked:** 2026-06-03
- **Mode:** open
- **Question:** What is the effort estimate (in person-weeks or equivalent) for MVP V1 of the Planning Poker product?
- **Choice:** —
- **Answer:** Preliminary internal sizing from SRC-002 MVP V1 and intake id=cto_escalation. No firm number available. Estimate is highly sensitive to real-time architecture decision (assumption a) — a WebSocket/multiplayer implementation vs. a simpler polling model could move the estimate materially.
- **Disposition:** deferred
- **Confidence:** 30
- **Source:** SRC-002 MVP V1 sizing; intake id=cto_escalation
- **Hint:** Non-blocking; conf 30 acknowledged. Firm number must come from CTO Technical Assessment. Real-time assumption (a) may move estimate materially — do not lock estimate until architecture is confirmed. This entry will be superseded once the Technical Assessment is received.
- **Follow-ups:** —

## Q010 · targets: roadmap · status: parked

- **Rationale:** The roadmap section captures the V1/V1.1/V2 phasing for the product and any portfolio-level priority signals. The inheritor sourced V1/V1.1/V2 directly from SRC-002; the priority escalation signal from intake is low-confidence (conf 40). V2 scope (assumption d: Jira/Linear integrations) requires PO confirmation.
- **Spawned-by:** readiness-inheritor
- **Asked:** 2026-06-03
- **Mode:** open
- **Question:** What is the intended roadmap phasing (V1 / V1.1 / V2+) and what is the portfolio priority relative to other active demands?
- **Choice:** —
- **Answer:** V1: core real-time Planning Poker (name-only, Fibonacci+T-Shirt, room sharing). V1.1: auto-reveal (RN-004 — see Q011), scale customization, minor UX improvements. V2: Jira/Linear integrations (assumption d), extended authentication options. Portfolio priority: escalated in intake but no explicit window or portfolio ranking confirmed.
- **Disposition:** assumption
- **Confidence:** 65
- **Source:** SRC-002 MVP phases; intake id=priority
- **Hint:** Non-blocking; conf 65. V1>V1.1>V2 is scope prioritization, not a confirmed portfolio priority ranking. PO must confirm (a) V2 scope — specifically whether Jira/Linear (assumption d) is a hard V2 commitment or a preference, (b) whether there is a delivery window or milestone driving V1. RN-004 auto-reveal confirmed as V1.1 (not V1) — see Q011.
- **Follow-ups:** Q011

## Q011 · targets: inherited-readiness · status: parked

- **Rationale:** This entry is the full open-disposition carry-forward from the intake triage into the RP session. It consolidates all assumptions, discovery flags, urgency absence, arithmetic inconsistency, and the RN-004 gap so that every downstream agent (Drafter, Auditor, Reconciler) has a single auditable reference for what was inherited, at what confidence, and why it must be validated before the RP can be finalized.
- **Spawned-by:** readiness-inheritor
- **Asked:** 2026-06-03
- **Mode:** open
- **Question:** What is the complete set of open items, assumptions, and discovery flags carried forward from the intake triage into this RP session?
- **Choice:** —
- **Answer:** Intake handoff readiness score: 63% (gate cleared honestly; triaged Discovery NOT Product Ready; PO chose to proceed).

  **Assumptions (a)–(h):**
  - (a) Remote synchronous simultaneous sessions — architecture unconfirmed; TECHNICAL RISK → route to Tech Lead / Technical Assessment; do not include in product/business risk register.
  - (b) No auth in MVP V1, name-only participation — unconfirmed whether this is MVP-only or a permanent product decision; PO must clarify.
  - (c) Fibonacci + T-Shirt scales are customizable — accepted as working assumption; low risk.
  - (d) Jira/Linear integrations are V2 — confirm this is a hard phasing decision not a preference; PO must confirm V2 scope.
  - (e) Audience already practices Planning Poker — validate in Discovery; if assumption is wrong, product framing changes.
  - (f) Monetization = SaaS per org, willingness-to-pay untested — Discovery item, high risk; do not assert revenue projections.
  - (g) No formal market validation or revenue projection; adherence to confirm — Discovery item, high risk; blocks exec-summary commercial claim.
  - (h) Problem broadly distributed across agile teams, market base sufficient — Discovery item; size TAM before making market-scale claims.

  **Commercial / Market discovery flag — impact Layer B:**
  SaaS opportunity is an unvalidated market assumption. No TAM, no revenue projection, no willingness-to-pay data at intake. Layer B confidence: 70 (discovery). Do not include as a firm business outcome in exec-summary until Discovery validates.

  **Urgency — absent (intake id=urgency, conf 0, non-blocking):**
  No delivery window, deadline, or competitor signal was declared in the intake. Absence is recorded explicitly. Do NOT invent urgency or imply competitive pressure where none was stated.

  **Arithmetic inconsistency in efficiency model (impact Layer A):**
  Submitter cited 8–11 h-h/year per squad. The model-derived figure is approximately 96–128 h-h/year (roughly 10x discrepancy). Root cause unknown (unit confusion, frequency assumption, or calculation error). This figure MUST NOT appear in any RP materials, exec summary, or metrics section until the PO/Submitter corrects it. Flagged as Discovery item 3.

  **RN-004 gap — auto-reveal feature:**
  The constraints table in the intake jumps from RN-003 directly to RN-005 — RN-004 (auto-reveal feature per SRC-002 spec) was dropped. This feature is confirmed as V1.1 scope, not V1. Carried into RP roadmap (Q010) as V1.1 item. Drafter must include RN-004 in the V1.1 section and Submitter must confirm placement.
- **Disposition:** discovery
- **Confidence:** 63
- **Source:** intake triage; intake id=assumptions (a)–(h); intake id=impact (Layers A+B); intake id=urgency (conf 0); SRC-002 spec; Discovery brief
- **Hint:** This is the master carry-forward record. Downstream agents must not treat any assumption here as confirmed without explicit PO sign-off. Priority resolution order: (1) arithmetic inconsistency — blocks metrics + exec-summary; (2) assumptions (f)(g)(h) — block commercial claims; (3) RN-004 placement — confirm with Submitter; (4) assumption (b) auth — confirm scope boundary; (5) TAM sizing — Discovery deliverable. Urgency: record absence, never invent.
- **Follow-ups:** —

## Q012 · targets: business-rules · status: parked

- **Rationale:** The readiness-drafter synthesized business rules RN-001..RN-010 from SRC-002 and the intake spec. This entry records that synthesized draft, notes that RN-004 (auto-reveal, tagged V1.1) was absent from the intake constraints table and was reintroduced by the drafter, and surfaces 7 open ambiguities the spec is silent on. The PO must confirm RN-004 placement and resolve ambiguities A1–A7 before business rules can reach the section minimum confidence.
- **Spawned-by:** readiness-drafter
- **Origin:** ai_drafted
- **Asked:** 2026-06-03
- **Mode:** open
- **Question:** Are the restated business rules RN-001..RN-010 (including RN-004 as a V1.1 item) accurate and complete, and how should ambiguities A1–A7 be resolved?
- **Choice:** —
- **Answer:** [CORRECTION applied Rev 3 — see Hint] ai_drafted draft: RN-001 (vote secrecy until reveal), RN-002 (change vote while round OPEN), RN-003 (host-only reveal), RN-004 (auto-reveal — V1.1, was absent from intake constraints table; reintroduced by drafter; confirmed V1.1 by PO in Q018), RN-005..RN-010 restated from SRC-002. Seven ambiguities the spec does not resolve: A1 — what triggers room-finish (explicit action, all voted, timeout, or combination); A2 — what constitutes consensus (unanimous, majority, host decision, or threshold); A3 — tie-breaking mechanism (human host decision vs. system rule); A4 — cancelled-round state behaviour (no CANCELLED status in spec enum); A5 — maximum participants per room; A6 — whether Observer role is included in V1 scope; A7 — definition of "all voted" for RN-004 auto-reveal (does "all" include late joiners and Observers).
- **Disposition:** answered
- **Confidence:** 82
- **Source:** SRC-002 spec; intake constraints table (RN-001..RN-003, RN-005..RN-010); readiness-drafter Phase 2 synthesis; PO confirm-loop Phase 3 (Q017–Q022)
- **Hint:** CORRECTION (Rev 3): the original Rev 2 Answer mislabeled RN-002 as "host-only reveal" and RN-003 as "Fibonacci + T-Shirt scales". The correct document-table mapping is RN-002 = change vote while round OPEN; RN-003 = host-only reveal. The old labels are superseded here for the audit trail — no entries were deleted. All A1–A7 ambiguities resolved or deferred by PO in Q019–Q022. A1: Sala -> FINISHED on explicit host action. A2: host decides freely, no system-enforced criterion (RN-010, Q019). A3: human discussion process, not a system rule (Q022). A4: CANCELLED round status introduced; preserved in history (Q020). A5: no hard cap in V1 (~8 reference, Q022). A6: Observer included in V1 (Q021). A7: deferred to V1.1 with RN-004 (Q022). Section confidence raised; remaining open item is Submitter on-record confirmation of RN-004 V1.1 placement.
- **Follow-ups:** Q014

## Q013 · targets: user-stories · status: parked

- **Rationale:** The readiness-drafter produced user stories ST-001..ST-010 with Given/When/Then acceptance criteria covering the full V1 user journey. This entry records that draft and surfaces two scope-boundary gaps: the consensus criterion (AC depends on unresolved A2 from Q012) and whether a manager visibility story belongs to V1 or V2. The Observer story is split out as a separate discovery entry (Q014).
- **Spawned-by:** readiness-drafter
- **Origin:** ai_drafted
- **Asked:** 2026-06-03
- **Mode:** open
- **Question:** Are user stories ST-001..ST-010 (create room, join by name, register task, secret vote, change vote, host reveal, new round, record consensus, history, manager visibility) accurate, complete, and scoped to V1?
- **Choice:** —
- **Answer:** ai_drafted draft: ST-001 create room, ST-002 join by name, ST-003 register/describe task, ST-004 secret vote, ST-005 change vote before reveal, ST-006 host reveal, ST-007 start new round, ST-008 record consensus, ST-009 session history, ST-010 manager visibility. ACs written in Given/When/Then form. Gaps: ST-008 consensus AC is blocked on A2 (consensus criterion from Q012); ST-010 manager visibility — drafter flagged as V1 vs. V2 question (no basis in spec); RN-004 deliberately has no V1 story (V1.1 only); Observer story deferred to Q014.
- **Disposition:** assumption
- **Confidence:** 72
- **Source:** SRC-002 MVP V1 scope; intake constraints table; readiness-drafter Phase 2 synthesis
- **Hint:** conf 72 < section min 80. ST-008 AC cannot be finalised until A2 (consensus criterion) is resolved — see Q012. ST-010 manager visibility must be explicitly placed in V1 or V2 by PO; no spec evidence for V1 inclusion found. Observer story excluded here — see Q014. RN-004 correctly absent from V1 stories; drafter must not backfill it. Resolve A2 first, then revisit ST-008 and ST-010.
- **Follow-ups:** Q014

## Q014 · targets: user-stories · status: parked

- **Rationale:** The readiness-drafter identified that the Observer role is explicitly defined in the SRC-002 spec but the V1 user flow contains no Observer journey. This is a discovery item: there is no basis for writing a verifiable AC without the PO first deciding whether Observer is in V1 scope. The entry is split from Q013 because it changes the scope and state-machine of the session, not just an AC detail.
- **Spawned-by:** readiness-drafter
- **Origin:** ai_drafted (discovery)
- **Asked:** 2026-06-03
- **Mode:** open
- **Question:** Is the Observer role (defined in the SRC-002 spec) in scope for V1, and if so what does an Observer see and do during an OPEN round?
- **Choice:** —
- **Answer:** Discovery gap: Observer role is named in the spec but no V1 flow exists for it. Three sub-questions must be answered before a story can be written: (1) does role-selection appear on the name-entry screen in V1?; (2) what does an Observer see during an OPEN round (votes, participant list, nothing)?; (3) does an Observer count toward "all voted" for RN-004 auto-reveal (A7 in Q012)?  Without these answers no verifiable AC can be written and the story cannot be included in V1 scope.
- **Disposition:** discovery
- **Confidence:** 35
- **Source:** SRC-002 spec (Observer role definition); readiness-drafter Phase 2 discovery sub-item
- **Hint:** conf 35 — genuine scope uncertainty. If PO confirms Observer is V1: add role-selection screen to scope (impacts ST-002 join flow), define Observer view behaviour, resolve A7 in Q012. If PO defers Observer to V1.1 or V2: move to roadmap and mark A6 resolved as "not V1". This decision also affects A4 (cancelled-round state) if Observers are present when a round is cancelled. Block ST-OBS creation until PO decides.
- **Follow-ups:** —

## Q015 · targets: nfrs · status: parked

- **Rationale:** The readiness-drafter scaffolded non-functional requirements against the ISO/IEC 25010 quality model. Confidence is well below the section minimum (70) because all numeric targets are PO-set placeholders and real-time session feasibility is a Technical Assessment concern, not a product concern. This entry records the scaffold and flags what the PO must confirm vs. what routes to the Tech Lead.
- **Spawned-by:** readiness-drafter
- **Origin:** ai_drafted
- **Asked:** 2026-06-03
- **Mode:** open
- **Question:** What are the confirmed non-functional requirements for the Planning Poker product (performance, reliability, security, usability, compatibility) with measurable targets?
- **Choice:** —
- **Answer:** ai_drafted scaffold (ISO/IEC 25010): Performance — state-sync latency target ~2 s p95 (PO to confirm; real-time feasibility routes to Technical Assessment); Reliability — round consistency during reconnect (no votes lost on brief disconnect), mechanism unspecified; Security/Confidentiality — vote secrecy until reveal per RN-001; Security/Access-control — host identity without login is a working assumption (assumption b from Q011 — confirm if permanent); Usability — frictionless name-only join (no registration friction); Compatibility — browser matrix undefined (modern desktop browsers assumed; PO to define). All numeric targets are PO-set placeholders; none are confirmed.
- **Disposition:** assumption
- **Confidence:** 58
- **Source:** SRC-002 spec; intake constraints (RN-001, assumption b); readiness-drafter Phase 2 synthesis; ISO/IEC 25010 scaffold
- **Hint:** conf 58 < section min 70. Real-time latency target (~2 s p95) must be confirmed by PO and validated by Technical Assessment — do not treat it as an accepted spec value. Browser compatibility matrix is undefined; PO must declare supported browsers before usability testing can be designed. Assumption b (no-auth/host identity) is still unconfirmed from Q011 — resolving it unblocks the access-control NFR. Reliability mechanism (reconnect behaviour, vote persistence) requires Technical Assessment input. Route latency and reconnect NFRs to Tech Lead; return confirmed PO-owned targets here.
- **Follow-ups:** —

## Q016 · targets: edge-cases · status: parked

- **Rationale:** The readiness-drafter produced edge-case scenarios EC-01..EC-11 anchored to the business rules. Four are marked DISCOVERY because they depend on unresolved ambiguities (Q012 A4, A7) or require Technical Assessment input. This entry records the full set and separates the RN-anchored firm cases from the discovery cases so the PO can triage them.
- **Spawned-by:** readiness-drafter
- **Origin:** ai_drafted
- **Asked:** 2026-06-03
- **Mode:** open
- **Question:** Are edge cases EC-01..EC-11 correct and complete, and how should the four DISCOVERY edge cases (EC-01, EC-02, EC-06, EC-07) be resolved?
- **Choice:** —
- **Answer:** ai_drafted draft — RN-anchored cases considered firm: EC-05 late joiner during OPEN round, EC-09 non-host attempting restricted action, EC-10 participant changing vote outside an OPEN round. Four cases marked DISCOVERY: EC-01 disconnected participant counting (affects RN-001 vote-secrecy and RN-004 auto-reveal "all voted" — linked to A7 in Q012); EC-02 host disconnect / succession (worsened by no-login; has Technical Assessment component because session state must persist without authenticated host); EC-06 duplicate participant names (name-only join with no auth creates collision risk; resolution rule undefined); EC-07 cancelled-round behaviour (no CANCELLED status in the spec enum ties directly to A4 in Q012 — undefined state machine transition).
- **Disposition:** assumption
- **Confidence:** 60
- **Source:** SRC-002 spec; intake constraints (RN-001..RN-010); readiness-drafter Phase 2 synthesis
- **Hint:** conf 60 < section min 70. EC-01 and EC-07 are blocked on resolving A4 and A7 in Q012 — address business-rules ambiguities first. EC-02 host succession has a TA component: route the session-state-persistence question to Tech Lead, but PO must decide the product policy (e.g. does host transfer automatically or does the session freeze?). EC-06 duplicate names must be decided by PO: first-come wins, suffix disambiguation, or rejection with error message. Firm cases (EC-05, EC-09, EC-10) can be written into ACs immediately once business-rules section is confirmed.
- **Follow-ups:** —

## Q017 · targets: scope · status: answered

- **Rationale:** The scope section was the single remaining hard-blocker at the RP gate (conf 62 < min 75, placeholder disposition). Without a PO-declared Excluded list the RP could not be submitted. This question captures the PO's definitive scope decision from the Phase 3 confirm-loop, promoting scope to po_authored and unblocking the gate condition.
- **Spawned-by:** orchestrator (PO confirm loop)
- **Asked:** 2026-06-03
- **Mode:** open
- **Question:** What is the PO's definitive scope decision for MVP V1 — specifically the Excluded list and the placement of all V1.1/V2 features?
- **Choice:** —
- **Answer:** MVP V1 Excluído (PO-declared): user authentication / identity management; org-level tenancy / accounts; ALL V1.1 features (timer, auto-reveal RN-004, auto-stats, CSV export); ALL V2 features (Jira/Linear integration, persistent teams, org history, metrics dashboard, round comparison, anonymous per-vote comments). Observer role IS included in V1 (see Q021 for detail).
- **Disposition:** answered
- **Confidence:** 90
- **Source:** PO confirm-loop Phase 3 — orchestrator decision record
- **Hint:** Scope now po_authored; hard-blocker resolved. Prior Q005 parked entry remains for audit trail (assumption disposition from intake). Observer V1 inclusion is elaborated in Q021. Jira/Linear exclusion confirmed hard V2 (not preference) — resolves intake assumption (d) from Q011.
- **Follow-ups:** Q021

---

## Q018 · targets: business-rules · status: answered

- **Rationale:** RN-004 (auto-reveal) was flagged at intake as absent from the constraints table and reintroduced by the drafter as a V1.1 item. The PO needed to confirm this placement on record so that the business-rules section and roadmap section can be finalised and the Submitter confirmation can be tracked.
- **Spawned-by:** orchestrator (PO confirm loop)
- **Asked:** 2026-06-03
- **Mode:** open
- **Question:** Is RN-004 (auto-reveal) confirmed as V1.1 scope, and does V1 reveal remain host-controlled per RN-003?
- **Choice:** —
- **Answer:** Confirmed: RN-004 (auto-reveal) is V1.1, not a V1 rule. V1 reveal remains host-controlled (RN-003). Submitter on-record confirmation still pending — flagged for follow-up.
- **Disposition:** answered
- **Confidence:** 85
- **Source:** PO confirm-loop Phase 3 — orchestrator decision record
- **Hint:** Submitter on-record confirmation pending. Until received, treat as PO-confirmed but not fully closed for Auditor purposes. Links to Q012 RN-004 placement and Q011 inherited-readiness carry-forward.
- **Follow-ups:** —

---

## Q019 · targets: business-rules, user-stories · status: answered

- **Rationale:** Ambiguity A2 (consensus criterion) from Q012 was blocking ST-008 (record consensus) acceptance criteria. Without a defined rule the AC could not be written as a pass/fail test. PO decision closes this gap.
- **Spawned-by:** orchestrator (PO confirm loop)
- **Asked:** 2026-06-03
- **Mode:** open
- **Question:** How is consensus defined in V1? Is there a system-enforced criterion, or does the host decide freely?
- **Choice:** —
- **Answer:** Host decides the final estimate freely; no system-enforced minimum criterion. Consensus value is stored separately from individual votes per RN-010.
- **Disposition:** answered
- **Confidence:** 88
- **Source:** PO confirm-loop Phase 3 — orchestrator decision record
- **Hint:** Resolves A2 from Q012. ST-008 AC can now be written: "Given all votes revealed, When host enters consensus value, Then value is stored separately from individual votes (RN-010) and round is CLOSED." No system validation of the consensus value against votes.
- **Follow-ups:** —

---

## Q020 · targets: business-rules, edge-cases · status: answered

- **Rationale:** Ambiguity A4 (cancelled-round state) and EC-07 from Q016 were both blocked on the absence of a CANCELLED status in the spec state-machine enum. The spec had no explicit cancelled-round transition or history policy. PO decision introduces the state and defines its history behaviour.
- **Spawned-by:** orchestrator (PO confirm loop)
- **Asked:** 2026-06-03
- **Mode:** open
- **Question:** How should a cancelled round be handled — should a CANCELLED status be introduced, and are cancelled rounds preserved in session history?
- **Choice:** —
- **Answer:** A CANCELLED round status is introduced. Cancelled rounds are preserved in session history (per RN-007) with no consensus value recorded.
- **Disposition:** answered
- **Confidence:** 88
- **Source:** PO confirm-loop Phase 3 — orchestrator decision record
- **Hint:** Resolves A4 from Q012 and EC-07 from Q016. State-machine must be updated to include CANCELLED as a terminal state alongside FINISHED. Drafter must add CANCELLED to the enum and write the AC for EC-07 accordingly.
- **Follow-ups:** —

---

## Q021 · targets: business-rules, user-stories, scope · status: answered

- **Rationale:** Ambiguity A6 (Observer role in V1) from Q012 and the discovery entry Q014 were blocking an Observer user story and the A7 definition. PO decision includes Observer in V1 with explicit behaviour rules, enabling the Observer story and resolving the A6/A7 chain.
- **Spawned-by:** orchestrator (PO confirm loop)
- **Asked:** 2026-06-03
- **Mode:** open
- **Question:** Is the Observer role included in V1? If so, how does a participant become an Observer, what does an Observer see during OPEN and REVEALED rounds, and does an Observer count toward "all voted"?
- **Choice:** —
- **Answer:** Observer role included in V1. Host promotes a participant to Observer. During an OPEN round, Observers see only the vote count (not values), consistent with RN-001 vote secrecy. On reveal, Observers see full values. Observers are excluded from the "all voted" count (relevant when RN-004 lands in V1.1).
- **Disposition:** answered
- **Confidence:** 88
- **Source:** PO confirm-loop Phase 3 — orchestrator decision record
- **Hint:** Resolves A6 from Q012 and closes Q014. ST-002 (join flow) must be updated to include role-selection (participant vs. Observer). A new Observer story (ST-OBS) can now be written. A7 ("all voted" definition for RN-004) is partially resolved here — Observers excluded — but full resolution is deferred to V1.1 with RN-004 per Q022.
- **Follow-ups:** —

---

## Q022 · targets: business-rules · status: answered

- **Rationale:** Ambiguities A1, A3, A5, and the remaining part of A7 from Q012 were lower-stakes items the PO could resolve by default rule rather than requiring a bespoke design decision. Recording PO acceptance of the defaults closes these gaps cleanly.
- **Spawned-by:** orchestrator (PO confirm loop)
- **Asked:** 2026-06-03
- **Mode:** open
- **Question:** How are lower-stakes ambiguities A1 (session-end trigger), A3 (tie-breaking), A5 (participant cap), and A7 (remaining "all voted" detail) resolved?
- **Choice:** —
- **Answer:** A1 — session ends by explicit host action (Sala -> FINISHED state); no timeout, no auto-end on all-voted. A3 — tie-breaking is a human discussion process ("ouvir menor/maior voto"), not a system rule; no system tie-break mechanism. A5 — no hard participant cap in V1; ~8 is a reference figure only. A7 — definition of "all voted" is deferred alongside RN-004 to V1.1.
- **Disposition:** answered
- **Confidence:** 90
- **Source:** PO confirm-loop Phase 3 — orchestrator decision record
- **Hint:** All four ambiguities resolved or explicitly deferred. A7 deferral is safe because RN-004 is V1.1; no V1 story depends on the "all voted" definition. A5 absence of hard cap should be noted in NFRs as a scalability consideration for Technical Assessment.
- **Follow-ups:** —

---

## Q023 · targets: edge-cases, nfrs · status: parked

- **Rationale:** EC-02 (host disconnect / succession) from Q016 had two components: a product policy decision (PO-owned) and an identity-binding mechanism (Technical Assessment-owned). Splitting them here enables the PO policy to be recorded now while routing the TA question correctly.
- **Spawned-by:** orchestrator (PO confirm loop)
- **Asked:** 2026-06-03
- **Mode:** open
- **Question:** What is the product policy for host disconnection — does the original host reclaim host rights on reconnect, and how is identity verified without a login system?
- **Choice:** —
- **Answer:** Product policy: original host reclaims host rights via the same link on reconnect. The identity-binding-without-login mechanism (how the system recognises the returning host without authentication) is a Technical Assessment question, not a product policy question.
- **Disposition:** deferred
- **Confidence:** 72
- **Source:** PO confirm-loop Phase 3 — orchestrator decision record
- **Hint:** Product policy is answered (conf 88 for policy component). Overall entry is parked/deferred because the identity-binding mechanism is unresolved and must be addressed in the Technical Assessment. EC-02 cannot be marked fully closed until TA returns an answer. Links to NFR access-control and intake assumption (b) from Q011.
- **Follow-ups:** —

---

## Q024 · targets: edge-cases · status: answered

- **Rationale:** EC-06 (duplicate display names) from Q016 was a product decision: three options existed (first-come wins, suffix disambiguation, or rejection with error). Without a PO decision, the AC for name-only join could not be written safely.
- **Spawned-by:** orchestrator (PO confirm loop)
- **Asked:** 2026-06-03
- **Mode:** open
- **Question:** How are duplicate display names handled in a name-only join session?
- **Choice:** —
- **Answer:** Duplicate display names are allowed. The system auto-disambiguates internally using a unique per-participant session id. An optional UI suffix or avatar distinction may be applied so vote attribution remains correct and visible.
- **Disposition:** answered
- **Confidence:** 85
- **Source:** PO confirm-loop Phase 3 — orchestrator decision record
- **Hint:** Resolves EC-06 from Q016. ST-002 join AC must note that duplicate names are permitted and that vote attribution is guaranteed by internal session id, not by display name uniqueness. Drafter should reflect the optional UI suffix/avatar in the UX notes.
- **Follow-ups:** —

---

## Q025 · targets: nfrs · status: answered

- **Rationale:** The NFR scaffold in Q015 had all numeric targets as PO-set placeholders (conf 58 < min 70). A confirmed state-sync latency target from the PO is the minimum required to raise NFR confidence above threshold, with feasibility deferred to the Technical Assessment.
- **Spawned-by:** orchestrator (PO confirm loop)
- **Asked:** 2026-06-03
- **Mode:** open
- **Question:** What is the PO's target for state-sync latency (vote/reveal propagation to all connected participants)?
- **Choice:** —
- **Answer:** PO sets state-sync latency target at ~2 s p95 for vote/reveal propagation to all connected participants. Near-real-time vote-count progress is also expected. Feasibility of this target belongs to the Technical Assessment.
- **Disposition:** answered
- **Confidence:** 80
- **Source:** PO confirm-loop Phase 3 — orchestrator decision record
- **Hint:** This is the minimum firm PO target needed to unlock nfrs above threshold. The ~2 s p95 figure is a product requirement; the Technical Assessment must validate feasibility. Browser compatibility matrix remains undefined — PO must still declare supported browsers. NFR section confidence raised but not fully closed until browser matrix is confirmed and TA returns feasibility verdict.
- **Follow-ups:** —

---

## Q026 · targets: objectives, metrics · status: parked

- **Rationale:** Both the objectives section (Q003) and the metrics section (Q006) were parked at discovery dispositions due to missing measurable target values and the unresolved arithmetic inconsistency in the efficiency model. The PO's Phase 3 decision is to keep these sections qualitative-but-clear and defer all quantitative targets to Discovery, explicitly suppressing the broken savings figure.
- **Spawned-by:** orchestrator (PO confirm loop)
- **Asked:** 2026-06-03
- **Mode:** open
- **Question:** What is the PO's resolution for objectives and metrics target values given the arithmetic inconsistency in the efficiency model?
- **Choice:** —
- **Answer:** PO decision: defer ALL quantitative target values to Discovery. Objectives and metrics should be qualitative-but-clear in the current RP. No savings figure (neither 8–11 h-h/yr nor ~96–128 h-h/yr) should be published in any RP section until the ~10x arithmetic discrepancy is corrected with real data. Each target value is recorded as an explicit Discovery item. This resolves the disposition question for the provisional gate: discovery disposition is honest and accepted.
- **Disposition:** discovery
- **Confidence:** 75
- **Source:** PO confirm-loop Phase 3 — orchestrator decision record
- **Hint:** This entry formally closes the gate question for objectives and metrics: the honest discovery disposition is PO-accepted, not a gap. The RP will state objectives qualitatively and flag metrics target values as Discovery items. The ~10x arithmetic inconsistency is addressed in Q029. Confidence 75 reflects that the PO has made a deliberate deferral decision (not an evasion) — this is an honest disposition for a provisional freeze gate.
- **Follow-ups:** Q029

---

## Q027 · targets: release-criteria · status: answered

- **Rationale:** The release-criteria section was parked at conf 55 < min 70 because no PO-confirmed measurable targets existed across Business/Quality/UX dimensions. PO acceptance of the functional + RN-compliance bar in the Phase 3 confirm-loop promotes this section to po_authored.
- **Spawned-by:** orchestrator (PO confirm loop)
- **Asked:** 2026-06-03
- **Mode:** open
- **Question:** Does the PO accept the functional + RN-compliance acceptance bar as the V1 release criteria?
- **Choice:** —
- **Answer:** PO accepts the following V1 release criteria: (1) end-to-end V1 flow completes without external tools; (2) core RNs are verifiable; (3) name-only join works; (4) vote count is shown before reveal (not values, per RN-001); (5) all criteria are testable as pass/fail. RN-004 (auto-reveal) is explicitly NOT a V1 release gate.
- **Disposition:** answered
- **Confidence:** 88
- **Source:** PO confirm-loop Phase 3 — orchestrator decision record
- **Hint:** Section promoted to po_authored. Drafter must ensure release criteria are written as pass/fail tests against each accepted criterion. RN-004 absence from V1 gate is explicit and auditable. Measurable targets per Business/Quality/UX dimension remain to be assigned by Drafter based on these criteria; PO has set the bar, not the specific metrics.
- **Follow-ups:** —

---

## Q028 · targets: risks · status: answered

- **Rationale:** The risks section was parked at conf 60 < min 70 because no firm probability/impact assignments existed from the PO. The Phase 3 confirm-loop asked the PO to assign ratings to all product/business risks. PO confirmed the assignments, promoting risks to po_authored. The Jira/Linear V2 dependency status also needed clarification.
- **Spawned-by:** orchestrator (PO confirm loop)
- **Asked:** 2026-06-03
- **Mode:** open
- **Question:** What are the PO-confirmed probability/impact ratings for all product and business risks, and is the Jira/Linear dependency still present for MVP V1?
- **Choice:** —
- **Answer:** PO-confirmed risk ratings: (1) market adherence not validated (risks g/h) — Prob Alta / Impacto Alto [discovery]; (2) willingness-to-pay unknown (risk f) — Prob Média / Impacto Alto [discovery]; (3) ~10x arithmetic credibility risk — Prob Confirmada (already occurred) / Impacto Médio; (4) urgency absent — Prob N/A / Impacto Baixo-Médio; (5) audience may not practice Planning Poker (risk e) — Prob Baixa-Média / Impacto Médio. Dependency clarification: Jira/Linear are V2; MVP V1 does NOT depend on them.
- **Disposition:** answered
- **Confidence:** 85
- **Source:** PO confirm-loop Phase 3 — orchestrator decision record
- **Hint:** Risks section promoted to po_authored. Commercial items (g/h/f) still require Discovery validation before confidence can exceed 85. The arithmetic credibility risk (3) is marked Prob Confirmada because the discrepancy has already been identified — its impact is on RP credibility and is being mitigated by suppression (see Q029). Jira/Linear V2 dependency confirmation resolves intake assumption (d) from Q011.
- **Follow-ups:** Q029

---

## Q029 · targets: exec-summary, context-problem, metrics · status: parked

- **Rationale:** Three co-existing savings figures in the RP materials are mutually inconsistent: 8–11 h-h/yr (submitter-cited), ~96–128 h-h/yr (model-derived, ~10x higher), and 15–20 min/session (session-level proxy). Publishing any of these without reconciliation would undermine RP credibility. The PO's Phase 3 decision resolves this by suppression pending Discovery.
- **Spawned-by:** orchestrator (PO confirm loop)
- **Asked:** 2026-06-03
- **Mode:** open
- **Question:** How should the three co-existing and mutually inconsistent savings figures be handled in the RP?
- **Choice:** —
- **Answer:** PO resolution: suppress ALL published savings figures in the RP body. Replace any efficiency/savings claim with a Discovery-pending note. The ~10x arithmetic discrepancy (8–11 h-h/yr vs ~96–128 h-h/yr) is not reconciled and must not appear until corrected with real data. This is recorded as Discovery item 3. The 15–20 min/session figure may be cited as an observed session-duration proxy without extrapolating to annual savings.
- **Disposition:** discovery
- **Confidence:** 90
- **Source:** PO confirm-loop Phase 3 — orchestrator decision record; prior Q002 (conf 84) and Q011 (conf 63) entries on arithmetic inconsistency
- **Hint:** This entry supersedes the arithmetic-inconsistency hint carried in Q002 and Q011 — those entries remain for audit trail but the resolution is recorded here. Drafter must: (a) remove all savings figures from exec-summary and metrics sections, (b) insert a Discovery-pending note wherever a savings figure appeared, (c) the 15–20 min/session proxy may be cited as an observed reference only. Confidence 90 reflects the PO's clear decision; the underlying data gap remains (hence discovery disposition).
- **Follow-ups:** —

<!-- END OF DOCUMENT -->

