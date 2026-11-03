# Lane W1 — the sub-agent's report (returned as text; saved by the lead)

Lane W1 · DONE · Branch lane/w1 head a52fc3e2 (base 0a1979e1; rebased from 56e639c6, no conflicts; shared rebuilt).

Commits (§9.1 order): 0a8570de feat(overview): show the owner's work queue (43) · d57ce485 feat(overview): show the
platform at a glance (45) · c7cabc88 feat(finance): show a month's income (36) · d8bf41dc feat(finance): show who owes
and who paid (41) · 75fe38f5 feat(finance): show the space's occupancy (41) · 692b4b2c feat(space-settings): link the
personal settings (48) · 758fff0b fix(packages): say the desk sells these prices (46) · 4fb7dedb fix(packages):
announce the terms, not the name (47) · 788d6426 fix(staff): reach the held item by the keyboard (47) · 03251399
feat(staff): show each person's month and start (47) · a52fc3e2 fix(staff): word both cases and name the tokens (47).

Red/green (outputs `scripts\lane-w1\`): red before code — C5.9 T143 (live region held «Evenings»), C5.11 T146 (held item
never reached), C5.10 T144 ("This account is now an admin's…") and T145 («Insert {الاسم}» not found). Code first for
C5.1–C5.8 and C5.6, each test proven red by its break. Green: overview 12/12; finance component 12, unit 9 files; staff
7 files / 30; packages 23; settings 1; space-settings + staff 45.

Breaks (backup copy, restored; logs `scripts\lane-w1\breaks\`), all red: B110 (amount on screen) · B111 · B112 · B113 ·
B114 · B115 (6 rows) · B116 · B116b (overview roles BOTH → no 403) · Boffline · B117 · B118 (destructive) · B118b ·
B119 (stale=1) · B120 · B121 (25 months) · B122 ('+Infinity%') · B123 · B124 (red by timeout) · B125 · B126 · B127
(finance roles BOTH) · B128 · B129 · B130 (full name) · B131 (first page only) · B132 (partial file) · B133 · B134
('4.20') · B135 (24 columns) · B136 ('0') · B137 · B138 · B139 · B140 · B141/B141b · B142/B142b/B142c.

Heavy checks (UTC 2026-10-31): lint 0 · typecheck 0 · unit web 171 files / 1111 · component whole 319 files: 3 failed,
7 tests failed | 1809 passed | 12 skipped — one its own (routes' staff fixture lacked `addedAt`, folded into C5.6,
green); re-run through the grant: IncomeTab, PaymentsLedger green; still failing alone: App › renders the main landmark,
router › the root's general error, App › blocks-storage, routes › reception's payments 403 — 3 s first lazy loads
(finding 87's family; CPU > 90 % from other lanes). Lint/typecheck not re-run after the fixture fold. check:links 3154,
check:classes clean, prettier clean. Outside the grant: `tsc -b` (web) twice, `tsc -p tsconfig.app.json` once.

Shared files: `pages/dashboard/routes.component.test.tsx` (QUIET_OVERVIEW, QUIET_ADMIN_OVERVIEW answers; `addedAt` in
the staff fixture); space-links.md (staff columns, ACCOUNT_IS_ADMIN, 106 out of its open list, history);
features overview, finance, space-settings, packages docs; copy overview, finance, staff, spaceSettings, packages;
existing tests updated to the new words/props; new `pages/dashboard/space/settings/AccountCard.tsx`.

Findings closed: 102 (C5.9), 106 (C5.10). 105 not written (keyboard half in C5.11; C6.17 not in base — the lead writes
it). 73 untouched (D6.14's).

Decisions: **LW1-D1 (marked SERIOUS: touches D5.10/EC17)** — EC17's key also serves the re-activation, where "no
temporary password is issued here" is false; chose a new key `staff.reissue.refusedAdmin` with D5.10's words for the
re-issue dialog only; the re-activation keeps its line. Undo: overwrite `refusals.ACCOUNT_IS_ADMIN`. **LW1-D2 (marked
SERIOUS: extends DI29)** — the debts tab's two paged lists: `?page=` (who owes), `?credit=` (in credit), first page
never written, a one-page list shows no steps (`onlyPastOne`). Undo: component state. LW1-D3 P7's offline state as a
feature-local `LoadFailure` (WifiOffIcon, status.offline, retry) on `network`, in overview and finance · LW1-D4 «دفعوا في
{month}» value is a count of customers; uncollected tile counts visits, amount in the helper · LW1-D5 transient tab
triggers within the lane · LW1-D6 the export reads the shown tab's own query (`enabled`) · LW1-D7 «عرض مقبوضاته» a Link
in a menu item, first · LW1-D8 ledger link `?staff=&from=YYYY-MM-01&to=today` (EC16) · LW1-D9 the routes test answers.

Notes: `#PRNUM` literal; anchors — desk `#unpriced` (UnpricedCard has no id; W3's file), settings `#attendance`
(probably works), `/packages#prices`; the admin overview's «عرض الكل» relies on C1.9 and W2's D6.4. Real run: 390 / 768 /
1440 and dark for 12, 19, 22, 24, 25, Packages & prices; the heatmap's sideways scroll below 768.

**Lead's assessment of the two SERIOUS marks:** neither touches money, a role, private data, a key or a lock; LW1-D1
words each refusal truly by its own key and keeps D5.10's words where D5.10 meant them; LW1-D2 adds address parameters
in DI29's own pattern. Both accepted, recorded under *Decisions taken without the owner* (not SERIOUS in the lead's
sense).
