# Golden exemplar (self-contained) — calibration reference

A condensed, fictional, repo-independent example of a *well-filled* capture. Use
it to calibrate quality: depth of problem statement, honest confidence numbers,
used dispositions, registered tensions, flagged derived sections. Do not copy its
content — copy its *bar*.

---

**Demand:** Self-service seat management for enterprise admins.

**Problem** — `Confidence: 88 · Source: Submitter direct + support export · Status: resolved · Disposition: answered · Hint: ticket volume is from the Q1 export; per-account breakdown would raise to ~95`
Enterprise admins cannot add or remove user seats themselves. Every change is a
support ticket; turnaround is 1–3 business days, and during onboarding waves admins
file 5–10 tickets each. Support logged 240 such tickets last quarter (18% of
enterprise volume). The pain is the dependency and the wait, not "a missing button".

**Originator & context** — `Confidence: 95 · Source: Submitter direct · Status: resolved · Disposition: answered · Hint: —`
Raised by the Head of CS in the Q1 account-health review, after two top accounts
cited it as a renewal friction.

**Reach** — `Confidence: 82 · Source: Submitter direct + inferred from account data · Status: resolved · Disposition: answered · Hint: exact admin count per tier not pulled; CS can quantify`
Enterprise admins (≈120 accounts), their end users (delayed access), and the support
team (carries the manual load).

**Business impact** — `Confidence: 68 · Source: inferred from support cost + two renewal calls · Status: low_confidence · Disposition: inferred · Hint: estimate, not calculated — pull support cost/ticket and the two at-risk ARR figures to firm up`
Retention: two accounts (~$140k ARR) named it a renewal blocker. Operational:
~240 tickets/quarter at an estimated 25 min each. Competitive: two rivals ship
self-serve seat management.

**Urgency** — `Confidence: 74 · Source: Submitter direct · Status: resolved · Disposition: answered · Hint: renewal date is firm; the "blocker" framing is verbal — worth an email to formalize`
One $90k renewal closes in ~75 days and the admin asked for this explicitly.

**Tensions registered:**
- Impact High + confidence 68 → accept as assumption; quantify with Finance before committing.
- Urgency High + effort unknown → if firm effort exceeds the renewal window, it's a business call to communicate to the account.

**Assumptions:**
1. Seat changes can reuse the existing billing-sync job without a new integration. — *To validate: Tech Lead.*
2. Admin role already has the permission scope to expose this safely. — *Accepted (low risk): confirm in build.*

**Triage (DRAFT — pending owner sign-off):** criteria 1–5 all supportive; blocking
capture answered directly; open items are technical-feasibility assumptions →
**proposed Product Ready**, escalation **No** (extension of existing billing/permission
surfaces, validated by Tech Lead). Flagged for the owner to confirm.

---

Note the texture: high where evidenced, honestly soft (68/74) where estimated,
every soft field hinted, dispositions used, tensions resolved, and the derived
triage clearly a flagged draft.
