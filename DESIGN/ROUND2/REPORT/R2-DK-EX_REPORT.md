# R2-DK-EX — Report

## Commit SHAs

- `main` (checked-out `HEAD`): `a82541b1435366854d253f88cfe9258f87d36b8d` — **not** `origin/main`.
- `origin/main`: `1efe2b8afa6a81866a8440246b6258475e5ccb7a`.
- `origin/design/desk`: (absent — PR #80 merged into `main` per the prompt's update; descriptor checked at run time).

The reviewer did not check out `origin/main`; its tree was read read-only via `git show`/existing extracted copies. Because `HEAD ≠ origin/main` (divergent, neither ancestor of the other), this is recorded here as required by §2.

## Verdict (one line)

The desk's §56 batch already removed most of the obvious doubles; what remains is repetition at the row/dialog/block boundary and a few " mówi same thing twice" lines, all small.

## Five most important points

1. The present list's header (`الحاضرون الآن 27 / 40`) and the `DataTable` label repeat the same name in a stack; one heading suffices.
2. The uncollected card's title already carries count and total; its description line restates the same items' origin.
3. `Customer file` payment rows plus void details risk restating the same money in the row, the void details, and (for owners) handover cards.
4. Desk search shows both "visit" and "new customer" actions at every non-empty result even when a match exists; the common path should stay primary and the rest one click away.
5. `My payments` handover recap should not repeat voided payments that are already struck through on the same screen.

## Issues (most important first)

### R2-DK-EX-001 — Title and labelled table repeat the same name
- **type:** improvement · **level:** component · **impact:** low
- **where:** `## 21 · Front desk (main, §56 uses same)` · `Desk.html?role=reception` · 1440 light (phone 390 confirmed) · no capture
- **what:** `PresentList` renders `<h2>الحاضرون الآن 27 / 40</h2>` directly above a `DataTable` whose `label` is also «الحاضرون الآن».
- **proposal:** keep the heading, drop the table's `label` (or the reverse); one name.
- **why:** less visual noise at rush hour; seconds saved scanning.
- **cost:** S
- **rule:** REVIEW_LENS §3.B.1 (one job per section).

### R2-DK-EX-002 — Uncollected card double-tells
- **type:** improvement · **level:** component · **impact:** low
- **where:** `## 21` · `Desk.html?role=reception` (or `Desk.html#unpaid`) · 1440 · no capture
- **what:** card title «N غير محصّل · total» followed by a description that explains the same unpaid visits.
- **proposal:** drop the description line (keep the title + rows); the row itself carries the reason.
- **why:** shorter card, debt clearer at a glance.
- **cost:** S
- **rule:** axis §5.1 (duplicated information).

### R2-DK-EX-003 — Desk actions shown twice on empty-ish screens
- **type:** improvement · **level:** pattern · **impact:** medium
- **where:** `## 22` style empty state · `Desk.html?role=reception&q=سليم` (no match) · 390 · no capture
- **what:** on "no one by this name" both «تسجيل زيارة» and «زبون جديد» appear as full buttons; they also exist in the page's actions/`⋯`.
- **proposal:** keep one primary (visit, per K1) and a link-style secondary, not two equal buttons.
- **why:** fewer mis-taps on a phone.
- **cost:** S
- **rule:** P1, amended.

### R2-DK-EX-004 — Secondary search remnants
- **type:** defect · **level:** pattern · **impact:** low
- **where:** any `## 26` Customers list with the old toolbar · checked in source only
- **what:** K1 settled "one search"; verify no remaining second search input on the present/customers list of the §56 batch (prompt's §4b asks specifically).
- **status:** looked for; none in `Desk.html`; Customers list keeps its single P5 bar. Reported as a check item, not a defect found here.
- **rule:** DK-001/DK-002.

### R2-DK-EX-005 — Handover recap restating voided payments
- **type:** improvement · **level:** pattern · **impact:** medium
- **where:** `## 28 · Reception only` · `My payments.html?role=reception` · 1440/390 · no capture
- **what:** the handover cards re-sum figures whose voided items are already struck through above.
- **proposal:** handover shows only the cash to hand over; voided payments excluded (K4), no per-item recap line.
- **why:** a clearer debt/handover with fewer mis-counts.
- **cost:** S
- **rule:** K4.

### R2-DK-EX-006 — Payment metadata duplication at row level
- **type:** improvement · **level:** component · **impact:** low
- **where:** `## 27 · Customer file` · `Customer file.html?id=m6&tab=pays` · 768/390 · no capture
- **what:** amount, item and method repeated in the row, its expanded detail and the toast (K7); K7 keeps the toast but the row should carry the minimum.
- **proposal:** keep amount+item in the row and method only in detail/toast.
- **why:** row stays scannable on 390.
- **cost:** S
- **rule:** K7, axis §5.1.

### R2-DK-EX-007 — Attendance log "mode" column merges two duties on mobile
- **type:** improvement · **level:** component · **impact:** low
- **where:** `## 21` (log tab) · `Desk.html?role=reception&tab=log` · 390 · no capture
- **what:** the log card shows name, time range, duration and «طريقة الانتهاء» all stacked; on a phone the last adds noise for a read-only log.
- **proposal:** move «Manual/Auto» into a muted caption line, not a Badge, when it is not actionable.
- **why:** faster log scanning; the colour is not an action.
- **cost:** S
- **rule:** axis §5.4 (decoration without meaning).

## Decisions in doubt

- **K7 (success toasts at the desk) vs. P8 amended (no toast when the result shows in the row):** §56's "Paid → toast, list updated" frames still toast on a list change. Under excess this doubles; but the prompt's §5 says settled doubles are "decisions in doubt", so reported here as a doubt, not a defect (rule K7).
- **K4 (voided payments shown struck through) vs. handover simplicity:** keeping them visible prevents a hidden money trap; excess reduction (issue EX-005) proposes excluding them only from the handover recap.

## What was not reviewed and why

- No visual captures: the reviewer had no usable browser/MCP tooling in this run and port 5432 is currently occupied by a `postgres` process (PID 8364) that could not be stopped from this session. Evidence field references the INDEX frame labels instead of cropped PNGs.
- Subtle spacing/colour/type issues that require rendered inspection are out of this report's reach.
- Retained off the desk pages' OW cross-references per §4b.

(End of report)
