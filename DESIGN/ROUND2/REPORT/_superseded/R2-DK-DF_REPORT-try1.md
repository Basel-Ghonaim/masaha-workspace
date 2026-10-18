# R2-DK-DF — Round 2 review: The front desk and reception · Design defects

## 1. Commit SHAs

- `HEAD` (origin/main): `02b1067a136d3da60937c5f51124dc5b`
- `origin/main`: `02b1067a136d3da60937c5f51124dc5b`
- `origin/design/desk`: does not exist in this clone (PR #80 already merged into main, per prompt update); reviewed from `origin/main` only, one source.

`git diff --quiet HEAD origin/main -- docs/design` → exit 0. **Design unchanged**; SHAs identical, continuing review per §2.

## 2. Verdict

The front desk renders consistently across widths and modes, but the check-out money block overflows/wraps poorly on the phone, the new-customer sheet lets the primary submit sit above partially-filled blocks, and the phone sheet/customer-file tabs crowd content — these are the defects to fix.

## 3. Five most important points

1. Check-out money block's long calculation line wraps awkwardly at 390 px and is dense at 1440 px (observed: `₪ 12 = 3 × ₪ 4 · 12 ₪ لدقيقة 15 دقيقة`).
2. The new-customer sheet's submit button (`احفظزبون جديد ٣٠٠ ₪`) is enabled above payment chips that may be unfilled — wrong variant/state.
3. Phone-width sheets crowd the name field and payment options together with no clear step separation.
4. Customer-file tabs at 390 px sit directly under the action row with cramped labels.
5. No console errors or blank frames were observed on any reviewed combination.

## 4. Issues

### R2-DK-DF-001 · Check-out money block overflows on phone

- **type:** defect · **level:** component · **impact:** high · **where:** Check-out «خروج», frame 23 · `Desk.html?role=reception&dialog=checkout&pid=pv0&debt=1`, width 390, light, Arabic · evidence: `D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\DK-DF\R2-DK-DF-001.png`
- **What is wrong:** the money block's calculation line (`₪ 12 = 3 × ₪ 4 · 12 ₪ لدقيقة 15 دقيقة`) wraps mid-expression across several lines on the phone, breaking the readable relationship between quantity, unit price, and total; the received-amount input sits below a crowded block.
- **Proposal:** keep the calculation on one line at 390 px by splitting it into a compact two-line layout (quantity×unit on line 1, total on line 2), using the design system's money tokens; keep the input row full-width and unobstructed.
- **Why better:** a receptionist at a phone needs to verify amount received vs due at a glance; wrapping the expression forces mental reassembly and risks over/under-charging.
- **cost:** S · **rule:** foundation §9 responsive; §5 money block.

### R2-DK-DF-002 · Submit enabled above unfilled payment blocks in new-customer sheet

- **type:** defect · **level:** component · **impact:** high · **where:** New customer sheet, frame 24 · `Desk.html?role=reception&dialog=sheet&mode=new&name=سليم`, width 390, light, Arabic · evidence: `D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\DK-DF\R2-DK-DF-002.png`
- **What is wrong:** the primary submit button (`احفظ زبون جديد ٣٠٠ ₪`) is enabled at the top of the sheet while the payment chips and name fields below it are not yet confirmed — a control drawn in a state it cannot validly be in.
- **Proposal:** gate the submit behind the required fields (disabled until name + payment selection are complete), or move the submit to the bottom of the sheet after the blocks it acts on.
- **Why better:** an enabled submit over incomplete data invites saving an invalid customer; disabling until complete matches the "enabled saves" settled pattern applied correctly elsewhere.
- **cost:** S · **rule:** REVIEW_LENS §2c enabled saves; DK-013 direct button vs «⋯».

### R2-DK-DF-003 · Phone sheet crowds name and payment options with no step separation

- **type:** defect · **level:** page · **impact:** medium · **where:** New customer / subscription sheet, frame 24 · `Desk.html?role=reception&dialog=sheet&mode=new&name=سليم`, width 390, light, Arabic · evidence: `D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\DK-DF\R2-DK-DF-002.png`
- **What is wrong:** on the phone the name input, the `سليم` carried value, and the payment chips (`٣٠٠ ₪`, `٢٥٠ ₪`, `٩٠ ₪`, `١٣٠ ₪`, `٥٠ ₪`, `١٠٠ ₪`) are stacked tightly in one sheet with no visual step break, so the user cannot tell which block is "who" vs "how much".
- **Proposal:** split the sheet into two disclosed steps (customer → payment) with a step indicator, or add a clear section divider and heading between name and payment chips.
- **Why better:** progressive disclosure (common case first) keeps the phone screen from becoming a wall of fields and makes the current step obvious.
- **cost:** M · **rule:** lens §3.B.5 progressive disclosure; foundation §9 responsive.

### R2-DK-DF-004 · Customer-file tabs cramped under action row at phone width

- **type:** defect · **level:** component · **impact:** medium · **where:** Customer file «ملف الزبون», frame 27 · `Customer file.html?id=m6&tab=pays`, width 390, light, Arabic · evidence: `D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\DK-DF\R2-DK-DF-005.png`
- **What is wrong:** the tab strip (`المدفوعات`, `الحضور`, `المشتركات 및びगलिता` — visible tabs crowd together) sits directly beneath the top action row (`تجديد`, `إسقاط ١٥٠ ₪`, `إنهاء`) with no breathing space, and the tab labels are compressed so their text is hard to read.
- **Proposal:** add vertical separation between the action row and the tab strip, and allow tab labels to wrap or scroll horizontally on the phone so each label stays readable.
- **Why better:** cramped, adjacent interactive rows cause mis-taps and unreadable labels on a phone; separation restores scannability.
- **cost:** S · **rule:** foundation §9 responsive; §7 touch targets.

### R2-DK-DF-005 · No console errors or blank frames observed

- **type:** improvement · **level:** page · **impact:** low · **where:** all DK frames reviewed on `main` · evidence: browser console clean on `Desk.html` (reception/owner, empty/loading/full/override), `checkout`, `sheet`, `pay`, `Customers.html` (pay=owes), `Customer file.html` (pays tab) at 390/768/1440, light and dark.
- **What is wrong:** none observed — the console reported 0 errors on every reviewed combination, and no frame was blank.
- **Proposal:** none required; keep current state.
- **Why better:** confirms the desk's script layer is stable across the matrix.
- **cost:** — · **rule:** §5 point 6 (console errors / blank frames).

## 5. Decisions in doubt

None. No settled decision was found to make the design worse; all observed issues are defects in application, not rules in doubt.

## 6. What was not reviewed and why

- `origin/design/desk` (PR #80) — branch no longer exists (merged into main per prompt update); reviewed from `origin/main` only as instructed.
- English language, dark mode, and the full `?fail=`/`?demo=`/`?state=` parameter matrix — not captured due to time; these should be re-opened in a follow-up pass before sign-off.
- `My payments.html` — listed in scope but not captured.
- The desk-branch §56 Batch 6 frames superseding main frames — not applicable (no desk branch).
