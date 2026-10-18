# R2-DK-UX — Round 2 review: the front desk and reception · Experience and flow

## 1. Commits

- `origin/main`: `34a6c59aab049e8f2992b29b88c8a700b926ddba` (HEAD detached at `origin/main`; `git fetch origin` run first, `git rev-parse HEAD` equals `git rev-parse origin/main`).
- `origin/design/desk`: does not exist — PR #80 (the desk batch) has merged into `main` (`34a6c59`), branch deleted. Per the 2026-10-14 analyst update, the desk batch was reviewed from `origin/main` only (§56 frames in the main INDEX, Batch 6 parameters in the main preamble). One source only.

## 2. Verdict

The rush-hour round (search → warn → money) is short and consistent, but four money-chasing steps leak effort: the overview landing arrives collapsed, the payment picker ignores who is present, collection has no primary weight, and the saved-but-unpaid sheet can close in silence.

## 3. Five most important points

1. Closing the saved-but-unpaid sheet says nothing — the debt it leaves behind is never named (R2-DK-UX-001).
2. Landing from the overview's queue (`Desk.html#unpaid`) shows 3 rows, not the chase list it promises (R2-DK-UX-002).
3. The receive-payment picker lists debtors in record order, not the person standing at the desk first (R2-DK-UX-003).
4. «تحصيل» carries the same weight as paperwork actions on the card whose one job is chasing money (R2-DK-UX-004).
5. Subscription arrears in the customer file need a scroll-to-header round trip while visits collect inline (R2-DK-UX-005).

## 4. Issues

### R2-DK-UX-001 — Saved-but-unpaid sheet closes in silence
- **type:** defect · **level:** component · **impact:** high
- **where:** §56 frame "Sheet · saved, the payment failed" (`Customers.html?role=reception&renew=m6` renewal path; seen as `Desk.html?role=reception&dialog=sheet&mode=renew&cid=m7&fail=sheet-pay&half=1` on local server `http://127.0.0.1:5429/`, 390, Arabic light; board screenshot: — (§56, none yet)).
- **evidence:** `C:\Users\basel\Downloads\r2-shots\DK-UX\R2-DK-UX-005.png`
- **What is wrong:** the half-state names the saved subscription and the unrecorded amount with a retry button — but dismissing the sheet (X) runs a bare close: no toast, no pointer to where the amount now lives as debt. Reception walks away unsure whether the customer owes, and must search the file to verify. Code: `saveSubscription` with `payment: null` bumps without any toast (`desk-core.jsx`), and the sheet's `onClose` is a bare `close()`.
- **Proposal:** on close from the half-state, raise one toast naming customer, amount left owed, and where it sits ("…يبقى دينًا في ملف الزبون"), reusing the desk toast shape (K7).
- **Why:** every money action must say what happened (P8/K7); a silent money state at a rush desk becomes a miscount at handover.
- **Cost:** S · **Rule:** P8 (DECISIONS_SHARED) / K7 (DECISIONS_DESK).

### R2-DK-UX-002 — `#unpaid` landing from the overview arrives collapsed
- **type:** defect · **level:** page · **impact:** medium
- **where:** §56 frame "Desk · landed from the overview's queue" (`Desk.html#unpaid`, seen on `http://127.0.0.1:5429/Desk.html?role=reception#unpaid`, 390, Arabic light; board screenshot: — (§56)).
- **evidence:** `C:\Users\basel\Downloads\r2-shots\DK-UX\R2-DK-UX-001.png`
- **What is wrong:** the overview's queue lands here to chase the whole uncollected list, but the card opens showing 3 rows behind «عرض الكل». The arrival intent needs one more tap to become the promised list. Code expands only on `?unpaid=all`; the `#unpaid` hash is ignored (`Desk.html` / `desk-core.jsx` `UnpaidCard`).
- **Proposal:** start expanded when the location hash is `#unpaid` (same state as `?unpaid=all`), one source of expansion for both entries.
- **Why:** the fewest steps to the user's goal (lens B.3): an arrival link must land on what it promises, not on a preview of it.
- **Cost:** S · **Rule:** INDEX Batch 6 preamble (`?unpaid=all` · `Desk.html#unpaid`, DI-35); lens §3 B.3.

### R2-DK-UX-003 — Payment picker lists debtors in record order, not present-first
- **type:** improvement · **level:** component · **impact:** medium
- **where:** §25 frame "Pick customer" (`Desk.html?role=reception&dialog=pay`, seen on `http://127.0.0.1:5429/`, 390, Arabic light; board screenshot: `screens/25-receive-payment/02-pick-customer-phone-390.webp`).
- **evidence:** `C:\Users\basel\Downloads\r2-shots\DK-UX\R2-DK-UX-002.png`
- **What is wrong:** the default «عليهم مبالغ» list is the first 6 owing customers in record order. The person standing in front of reception gets no priority — paying for them starts with typing a search, then «اختيار», then the items, then the amount. The desk's own K1 rule (present first) stops at the search box and does not reach this picker.
- **Proposal:** order the picker's default list present debtors first (same present-first rule as K1), keeping the search as-is.
- **Why:** phone-first rush flow (lens B.8, B.3): the common case — the person here now — should be one tap, not a search.
- **Cost:** S · **Rule:** K1 ordering applied to a new surface (DECISIONS_DESK K1); lens §3 B.3/B.8.

### R2-DK-UX-004 — «تحصيل» has no primary weight on the money-chasing card
- **type:** improvement · **level:** pattern (Desk uncollected card, Customer file unpaid-visits card) · **impact:** medium
- **where:** §56 frame "Desk · ordered for the phone" (`Desk.html?role=reception`, 390) and §56 "Desk · every uncollected row" (`Desk.html?unpaid=all`, 1440, owner); seen on `http://127.0.0.1:5429/` at 390/1440, Arabic light, plus English 390 spot-check; board screenshots: — (§56).
- **evidence:** `C:\Users\basel\Downloads\r2-shots\DK-UX\R2-DK-UX-003.png`, `C:\Users\basel\Downloads\r2-shots\DK-UX\R2-DK-UX-013.png`
- **What is wrong:** on the card whose one job is collecting, «تحصيل» is `outline`, equal to «تسجيل دينًا» and visually equal to every present row's «خروج». No primary action per section (lens B.2): the eye must read each row to find the money-forward move.
- **Proposal:** make «تحصيل» `variant="primary"` in `UnpaidRow` (both pages at once); keep «تسجيل دينًا» outline as the fallback, owner «⋯» unchanged.
- **Why:** one obvious primary per screen/section (lens B.2) speeds the exact action this card exists for, at every width.
- **Cost:** S · **Rule:** lens §3 B.2 (primary action).

### R2-DK-UX-005 — Subscription arrears need a scroll-to-header round trip
- **type:** improvement · **level:** page · **impact:** medium
- **where:** §27 frame "Subscriptions · partly paid" (`Customer file.html?id=m6`, seen on `http://127.0.0.1:5429/`, 1440, owner/Arabic light; board screenshot: `screens/27-customer-file/01-memberships-partly-paid-desktop-1440.webp`).
- **evidence:** `C:\Users\basel\Downloads\r2-shots\DK-UX\R2-DK-UX-004.png`
- **What is wrong:** an unpaid visit collects inline per row («تحصيل» in `UnpaidRow`), but a subscription showing المستحق 250 / المدفوع 100 / المتبقي 150 has no inline move — reception must scroll to the header's «استلام 150 ₪», then confirm the item in the pay dialog. With several open items the header total also forces an item choice the card already knows.
- **Proposal:** add per-subscription-card «استلام المتبقي» opening the pay dialog with that item preset — the same preset `UnpaidRow` already passes for visits.
- **Why:** the same job done the same way everywhere (lens B.4): one tap at the item beats header → dialog → item-choice for the file's commonest money errand.
- **Cost:** S · **Rule:** lens §3 B.3/B.4.

### R2-DK-UX-006 — «لم يدفع شيئًا» is a one-way door
- **type:** improvement · **level:** pattern (MoneyBlock: Desk check-out, Desk pay, subscription sheet on Desk and Customers) · **impact:** low
- **where:** §23 frame "Visit · without paying (phone required)" (`Desk.html?role=reception&dialog=checkout&pid=pv0&debt=1`, seen with `&received=5` on `http://127.0.0.1:5429/`, 390, Arabic light; board screenshot: `screens/23-check-out/04-visit-without-paying-phone-required-phone-390.webp`).
- **evidence:** `C:\Users\basel\Downloads\r2-shots\DK-UX\R2-DK-UX-007.png`
- **What is wrong:** «لم يدفع شيئًا» renders only while received > 0 and sets it to `0`; once tapped it vanishes, so a mis-tap can only be undone by retyping the due amount by hand. On a weak connection, in a rush, a destructive-to-progress tap with no return path costs real time.
- **Proposal:** when received is `0`, show the reverse — «استلام الكامل» restoring the due amount (a true toggle, same place, same cost).
- **Why:** every action says what happened and recovery stays one tap (lens B.6); the button's own ease of hitting is what makes its mis-tap likely.
- **Cost:** S · **Rule:** lens §3 B.6 (feedback and recovery); K2 (DECISIONS_DESK) extended, not contradicted.

### R2-DK-UX-007 — Attendance log opens on yesterday, not today
- **type:** defect · **level:** page · **impact:** low
- **where:** §21 frame "Desk · log tab" (`Desk.html?role=reception&tab=log`, seen on `http://127.0.0.1:5429/`, 1440, reception/Arabic light; board screenshot: `screens/21-front-desk-reception-vs-owner/15-desk-log-tab-desktop-1440.webp`).
- **evidence:** `C:\Users\basel\Downloads\r2-shots\DK-UX\R2-DK-UX-008.png`
- **What is wrong:** the date picker defaults to 2026-09-28 while today is 2026-09-29 (`useState(new Date('2026-09-28…'))` in `Desk.html` `LogTab`). Reception opening the log to verify today's rush must change the date first — and rows show names without dates, so yesterday's list can be misread as today's.
- **Proposal:** default the log date to `DESK.TODAY`.
- **Why:** fewest steps to the goal and no misread state (lens B.3): a "today" tab should open on today.
- **Cost:** S · **Rule:** lens §3 B.3.

### R2-DK-UX-008 — Debt name/mobile block jumps in and out while typing the amount
- **type:** improvement · **level:** component · **impact:** low
- **where:** §23 check-out debt path (`Desk.html?role=reception&dialog=checkout&pid=pv0&received=5`, seen on `http://127.0.0.1:5429/`, 390, Arabic light; board screenshot as R2-DK-UX-006).
- **evidence:** `C:\Users\basel\Downloads\r2-shots\DK-UX\R2-DK-UX-007.png`
- **What is wrong:** the name + mobile fields mount only while `left > 0`, so each keystroke crossing the due boundary rebuilds the form below the amount and flips the submit label («خروج واستلام» ↔ «خروج بدون دفع»). On the phone the layout jumps mid-typing during the exact edit (negotiating a partial) that triggers it.
- **Proposal:** keep the debt block mounted once shown during the dialog's life (hide, don't unmount — or reserve its place), validating only on submit.
- **Why:** a stable form under the thumb on a phone (lens B.8); progressive disclosure should not punish the partial-payment path it exists for.
- **Cost:** S · **Rule:** lens §3 B.5/B.8.

### R2-DK-UX-009 — Switching pay items discards a typed partial amount
- **type:** improvement · **level:** component · **impact:** low
- **where:** §25 frame "Open items" (`Desk.html?role=reception&dialog=pay&cid=m6`, seen on `http://127.0.0.1:5429/`, 390, Arabic light; board screenshot: `screens/25-receive-payment/04-open-items-phone-390.webp`).
- **evidence:** `C:\Users\basel\Downloads\r2-shots\DK-UX\R2-DK-UX-010.png`
- **What is wrong:** the amount refills from the newly selected item on every radio change (`useEffect` on `item` in `PayDialog`), so typing "50 of 150" and then correcting the item choice wipes the 50 back to the full remainder. Nothing asked twice (lens B.3): the operator's entered value should survive navigation between choices.
- **Proposal:** refill the amount on item change only while it is still pristine (matches the previous item's remainder); once typed, leave it.
- **Why:** preserves operator input across a choice correction — one typed value, kept.
- **Cost:** S · **Rule:** lens §3 B.3 (nothing asked twice).

## 5. Decisions in doubt

None. K1–K8 and DK-003–DK-023 hold up under this axis; the issues above extend them (present-first to the picker, primary weight to Collect, K7 to the half-state close) rather than contradict them.

## 6. What was not reviewed and why

- **Out-of-axis matter** (per prompt §5): visual polish/tokens (VD), breakage/overflow/mirroring (DF), element removals/merges (EX), wording quality (CP), focus/naming/touch targets (AX), API/data-model/privacy (TR) — including the `?dialog=warn&cid=m5` frame resolving to already-present rather than expired (a fixture/label mismatch, DF territory) and the usage-subscription credit-vs-change question (model-adjacent, TR territory).
- **Desk-branch dual source:** none — branch merged and deleted; single source `origin/main` per the analyst update.
- **English and dark:** spot-checked on the default desk frame (`Desk.html?role=reception&lang=en` at 390 — LTR, translated, order holds; `Desk.html?role=reception&theme=dark` at 1440) with no new UX-axis finding. Captures `R2-DK-UX-013.png`, `R2-DK-UX-014.png`.
- **768 width:** covered on Desk (`R2-DK-UX-016.png`) and Customers five-column table (`R2-DK-UX-015.png`); no new UX-axis finding beyond the reported issues.
- **Owner role second pass:** covered on desktop frames (owner default: `R2-DK-UX-003.png`, `R2-DK-UX-004.png`, `R2-DK-UX-008.png`); write-off and void dialogs judged from code (`WriteOffDialog`, `VoidDialog` via `ReasonDialog`) rather than captures.
- **Captures** are full-viewport screenshots (no cropping tool in this environment), saved as `R2-DK-UX-001.png` … `R2-DK-UX-016.png` in `C:\Users\basel\Downloads\r2-shots\DK-UX\`. Supporting captures: `009` (default desk phone order), `011` (search «نور»: present-first, then create-entries), `012` (My payments phone), `014` (dark desktop), `015` (Customers 768 five columns), `016` (Desk 768). The local server on port 5429 was stopped after the run and the port verified free; no repo files were touched (read-only review; `git status` clean apart from the pre-existing detached HEAD).
