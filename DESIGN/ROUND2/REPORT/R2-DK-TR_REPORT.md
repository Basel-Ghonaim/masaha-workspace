# R2-DK-TR — desk, truth to product, data and API

1. Commit SHAs
- Main (origin/main): `1efe2b8afa6a81866a8440246b6258475e5ccb7a`
- design/desk: branch deleted after PR #80 merged; reviewed desk pages from `origin/main` (update 2026-10-14). The worktree HEAD at review start was `a82541b`, not `origin/main`; files used to match `origin/main`.
- Worktree HEAD before review: `a82541b1435366854d253f88cfe9258f87d36b8d` (mismatch, as found).

2. Verdict
The desk batch is mostly reconciled with the settled truth; the remaining gaps are exposure of staff-only figures on an outward-facing screen and a couple of role/data-model edges, not ledger logic.

3. Five most important points
- The front desk repeats capacity as `present / capacity`, which the model keeps private from anyone but staff.
- Money sums on the desk (uncollected total, handover figures) sit on a screen shown in customer view.
- Role handling itself is sound: archive, restore, write-off, void and Finance stay owner-only.
- The payment ledger rules (one item, never edited/deleted, void struck and counted nowhere) are followed as designed.
- Check-in warnings are count-based, not weekday-based, as K5 requires.

4. Issues

**R2-DK-TR-001** — Present-now line exposes the space's capacity on a publicly visible screen
type: defect · level: page · impact: high
where: INDEX §21 `Desk — reception — desktop 1440` (main), `Desk.html?role=reception`, 1440 desktop, screenshot `docs/design/screens/21-front-desk-reception-vs-owner/02-desk-reception-desktop-1440.webp`
evidence: `C:\Users\basel\Downloads\r2-shots\DK-TR\R2-DK-TR-001.png`
what is wrong: the present count is written as `N / capacity`, so the private capacity leaks through a screen the desk leaves in view of customers.
proposal: show the present count alone on the desk line; keep the capacity in the one place staff open, or behind the same state control.
why: only staff may know capacity (ADR 0008); customers still see the live state.
cost: S
rule: data-model “Capacity is private from the public”; ADR 0008.

**R2-DK-TR-002** — Uncollected total aggregates debt on the open desk screen
type: defect · level: page · impact: medium
where: INDEX §21, `Desk.html?unpaid=all`, 1440 desktop, `docs/design/screens/31-batch-3a-fixes/03-open-desktop-1440.webp`
evidence: `C:\Users\basel\Downloads\r2-shots\DK-TR\R2-DK-TR-002.png`
what is wrong: the uncollected card's title sums every uncollected visit's charge, an income-type total left in customer view.
proposal: keep the count in the open desk line and move the total to the single details view Finance owns, or show it only when the desk is not in customer view.
why: aggregate money belongs where the ledger is read as income (O3).
cost: S
rule: TR axis point 4; settled K4 (count is enough to act).

**R2-DK-TR-003** — Reception can trigger archive/restore through the customer menu surface
type: defect · level: pattern · impact: medium
where: INDEX §26, `Customers.html?role=reception`, 1440 desktop.
evidence: Customer menu in reception view (annualised from settled DK-013).
what is wrong: `CustomerMenuItems` is guarded by `IS_OWNER` for archive and restore, but not inside the desk provider's action surface in a way the API can enforce as a separate control; the contract must still reject it.
proposal: confirm `can()` checks the OWNER role on archive and restore, and that reception's copy exposes no archive affordance end to end.
why: ADR 0009 separates edit (both roles) from archive/restore (owner only).
cost: S
rule: ADR 0009, revised line.

**R2-DK-TR-004** — Present read leans on a hand-rolled usage line instead of the K8 bounded read
type: improvement · level: component · impact: low
where: INDEX §20, `Desk.html?q=???`, 1440 desktop.
what is wrong: the desk shows only the first usage line per subscription for brevity, which leaves the customer's own copy of the composed read (K8) without a named source.
proposal: fix the contract's composed present read to its K8 shape and let the desk pick the line; today's usage line is the bound field.
why: the API may serve only a bounded read.
cost: M
rule: K8, api-contract §4 exception.

**R2-DK-TR-005** — Bank-transfer method is shown as a separate handover total despite being in the space account
type: improvement · level: page · impact: low
where: INDEX §27, `My payments.html?role=reception`, 1440 desktop.
what is wrong: the handover card keeps cash and transfer as separate totals even though transfer is received in the space's account and does not need handing over.
proposal: present transfer as “received in the space's account” without a handover total, cash as the handover.
why: less mental arithmetic at close of shift.
cost: S
rule: My payments copy already states this.

5. Decisions in doubt
- Settled K4 puts the uncollected count and total in the card's title. With O3's “money in view of others”, that total is still customer-visible. Consider removing the total from the open line as in R2-DK-TR-002.
- P9's toast undo for a newly archived settled customer is a scoped exception; the API never deletes, which the prototype respects.

6. Not reviewed
- Dark and English variants were not needed: TR concerns do not rely on theme or locale.
- Tablet 768 for privacy/numeric exposure was not run separately; the mobile desk (390) is the customer-visible case, covered by the same points.
- Customer file, Payments and Finance pages were checked against settled rules by doc and code, without exhaustive screen capture, because no new TR defect was found beyond the patterns above.
- Business flow length, visual choices, breakage, removals, wording quality handled by other DK reviews.
- Origin/ahead mismatch recorded in section 1; no branch checkout or file edit was performed.
