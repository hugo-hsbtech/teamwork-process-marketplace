# Companion guide — filling the Intake Record template

Section-specific guidance for the default Intake Record template, keyed by
annotation `id`. The Doc Updater and Question Strategist read this; the Auditor
grades against it. A different template ships its own guide (or none, if the
rubrics in the annotations are sufficient).

## Capture sections (filled from answers)

- **`problem`** (blocks, min-conf 80) — the guardian section. Pain with observable
  symptoms, no solution. If the answer is "we need feature X", turn it back into
  the pain X would relieve; if you can't, it isn't satisfied.
- **`originator`** (blocks, 70) — who raised it, the situation, the channel.
- **`reach`** (blocks, 70) — personas/segments/teams + how each is affected.
- **`impact`** (blocks, 70) — value across applicable dimensions, quantified when
  possible; estimates allowed if marked low-confidence with a firming hint.
- **`urgency`** (70) — why now + cost of waiting.
- **`priority`** — level + reason.
- **`constraints`** (70) — time/budget/legal/technical/scope/external limits, or
  "none known".
- **`assumptions`** — each assumption with a **proposed** verdict and who validates.

## Derived sections (computed, flagged)

### `triage` — the routing draft (handle with care)

Triage is normally **human judgment**. The skill brainstorms with the Submitter,
who does not make that call, so you **draft** it from evidence and **flag it** for
the owner. Never present it as settled.

1. **Keep the ⚠️ banner** in the template. Set Metadata `Status` = *In triage*;
   leave *Triaged by* / *Date triaged* blank.
2. **Evaluate the 5 criteria from evidence** — each gets a verdict, a rationale,
   and a basis/source (trace-to-source). Only assert what the capture supports.
3. **Propose one routing decision:**

   | Propose… | When the capture shows… |
   |---|---|
   | **Discovery** | Open unknowns on the *blocking capture itself* or on product scope that prevent closing scope — not merely open *technical-feasibility* assumptions (those belong in rationalization). |
   | **Product Ready** | Blocking sections answered directly at solid confidence; the only open items are reasonable technical-feasibility assumptions. Don't hedge to Discovery here. |
   | **Backlog** | A good demand whose urgency/impact don't justify acting now. |
   | **Reject** | Out of strategy or low value. Be conservative — lean to flagging for review over a hard reject. |

   Don't over-claim *Product Ready* when the problem or impact itself is still a
   guess. When genuinely torn between two paths, state the tension and let the
   owner decide — that *is* the honest output.

### `cto_escalation`

Draft **Yes** only for genuine architectural impact (new infra/platform, payments,
multi-tenancy, security model, AI/runtime, integrations with real unknowns). Draft
**No** when it's an extension of existing UI/state carrying ordinary technical
assumptions validated by a Tech Lead during rationalization. Escalating every
routine assumption defeats the gate.

### `assumptions` verdicts

Calibrate by risk, don't default everything to "To validate":
- **Accepted** — reasonable, low-risk, doesn't block the routing decision (still
  travels forward to be confirmed).
- **To validate** — material to scope/value *and* genuinely uncertain.
- **Rejected** — evidence already contradicts it.

### `readiness`, `discovery`, `handoff`

- **`readiness`** — compute from the capture sections: score, gate Yes/No, counts
  of open assumption/discovery/deferred.
- **`discovery`** — fill only if the triage draft is Discovery; turn each open
  unknown into a row + a time-box; leave any log/result empty.
- **`handoff`** — state the next step implied by the (draft) decision.

## The bar

A good intake reads like a demand *understood*: the problem is pain not solution,
confidences are honest and hinted, assumptions/discovery are explicit with owners,
and every derived section is a defensible, flagged draft that never pretends to be
a human decision.
