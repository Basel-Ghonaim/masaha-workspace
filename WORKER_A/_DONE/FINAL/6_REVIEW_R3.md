# Review of #132 — R3: the owner's and the admin's screens (overviews, finance, audit logs, platform settings, admin pages) — Claude Code, Opus 5.5
Head: a12c0790 · commits 28 · checks: green (10 pass, CodeRabbit skipping) · head moved during the review: no
Verdict for my range: **mergeable after a fix round** (no blocker; four should-fix, one plausible should-fix)

Everything below was read from commit objects at `a12c0790` (files at the head; each commit's diff where it mattered).
No fetch was needed (`git cat-file -t a12c0790` → commit).

## Findings (verified defects only, most severe first)

### R3-F1 — should-fix · The owners page's held «ربط بمساحة» is still `disabled`, so the keyboard skips it (105)
- Where: apps/web/src/features/space-links/components/owner-actions/OwnerActionsMenu.tsx:36 at a12c0790
- Seen in the code: `<DropdownMenuItem disabled={actions.link.disabled} …>`, with its reason ("The account is
  suspended — restore it first") inside the item. The plan's own reading (§1: Radix's `focusable: !disabled`) and
  105's *Resolution* ("a held item is no longer disabled … Both menus use it") are true only for the staff menu and
  `MenuActionItem`. `git grep` finds this the only `disabled` menu item left in the dashboard that carries a reason.
  Its test (`OwnerActionsMenu.component.test.tsx:52-60`) checks `aria-disabled` and the reason with the pointer,
  never with the arrow keys, so it cannot catch this.
- Scenario: admin, keyboard only, owners page (screen 27) → a suspended owner's «⋯» → arrow keys: the focus goes from
  the trigger straight to «فك الربط من …». «ربط بمساحة» and the reason it is held are never reached or read
  (foundation §10, the rule finding 105 closes).
- Fix: `held={actions.link.disabled}` (the layer's D3.3), plus a test that ArrowDown lands on it; 105's *Resolution* and
  space-links.md:161 name the owners page too. · Belongs: a fix round on #132 (folded into `0913363b fix(admin):
  reach a held user action by keyboard`).

### R3-F2 — should-fix · Finance: counted Arabic tile values sit in a `dir="ltr"` box, so they read backwards
- Where: apps/web/src/features/finance/components/DebtsTab.tsx:92 and apps/web/src/features/finance/components/OccupancyTab.tsx:57 at a12c0790
- Seen in the code: every debts and occupancy tile wraps its value in `<span dir="ltr">`. That is right for an
  amount, but these values hold Arabic words:
  - the debts tab's «دفعوا في {month}» value is `words.customers(…)` («5 زبائن»);
  - the «زيارات غير محصّلة» value is `words.visits(…)` («3 زيارات»);
  - occupancy's «متوسط مدة الجلوس» is `«{time} س»` («4:12 س»).
  D5.5 asks for `dir="ltr"` on the peak hour only. Copy: `shared/copy/arabic/finance.ts` (`customers`, `visits`,
  `stay.value`).
- Scenario: an owner in Arabic opens Finance › الديون. In an LTR box the digit is drawn left of the word, so an Arabic
  reader reads «زبائن 5» and «زيارات 3». Finance › الإشغال reads «س 4:12». English is unaffected. Only in a report:
  the lead's real run saw finance in Arabic on the income tab only, so this was never seen.
- Fix: keep `dir="ltr"` on the money values and the peak hour only (or isolate just the number inside the counted
  phrase), and add a component test in Arabic for the paid, uncollected and stay tiles. · Belongs: a fix round on #132
  (folded into `c4c431c9` and `947629fd`).

### R3-F3 — should-fix · The owner's overview's «… بلا سعر» row links to `#unpriced`, an anchor nothing carries
- Where: apps/web/src/pages/dashboard/space/overview/OverviewPage.tsx:17 → apps/web/src/features/desk/components/unpriced/UnpricedCard.tsx:45 at a12c0790
- Seen in the code: the overview sets `deskUnpriced: …/desk#unpriced`. `git grep` finds no element with
  `id="unpriced"`; the «بدون سعر» `Card` has no id, while the uncollected card carries `UNCOLLECTED_ID`
  (`useUncollectedCard.ts:14`). Lane W1's report already noted it ("UnpricedCard has no id; W3's file") and it was
  never closed. T111 checks the `href` string only. `docs/features/overview.md:35` says the row leads to "the desk …
  `#unpriced`", which is not true of the code.
- Scenario: an owner with an unpriced visit → overview → «1 visit with no price» › «فتح المكتب» → the desk opens at its
  top, and the hash focuses nothing (D0.4 finds no element). On a phone, «بدون سعر» is below the search, the present
  list and «غير محصّل», out of sight. That is a gap on screen 12, whose link is meant to lead "where it is acted on".
- Fix: give the card `id="unpriced"` (with `scroll-mt-*`, like the editor's cards; an exported constant as
  `UNCOLLECTED_ID`), and add a desk routes test that lands on `#unpriced`. · Belongs: a fix round on #132 (the card is
  W3's desk file; fold it into the desk commit that owns `UnpricedCard`, with the test in `7edd61a4`).

### R3-F4 — should-fix · The debts CSV writes cells that can run as formulas, and every phone opens as a number
- Where: apps/web/src/shared/lib/csv/csvOf.ts:9-11 and apps/web/src/features/finance/services/debtsCsv.ts:28-35 at a12c0790
- Seen in the code: `fieldOf` quotes only `"`, `,`, CR and LF. `debtsCsv` writes `customer.name` (typed at the desk)
  and `customer.phone` as they are. The phone is stored in E.164 (`packages/shared/src/core/phone.ts:3`), so it always
  starts with `+970` or `+972`. Finding 204 (lane L's, recorded by this PR) is open for the owner.
- Scenario: (1) Reception creates a customer named `=HYPERLINK("http://x","Pay")` who then owes. The owner exports
  «تصدير الديون (CSV)» and opens it in Excel → the name cell runs as a formula. (2) Every debtor's `+970591234567` opens
  as the number 970591234567, with the `+` lost and shown as `9.70592E+11`. D5.4 promises "the phone as stored", and
  that is not what the owner reads. Plausible on the exact display: it depends on Excel's own parsing, which was not
  run.
- Fix: the owner's line on 204 sets the rule. Then `csvOf` puts a `'` (or a tab) before any value that starts with
  `=`, `+`, `-`, `@`, TAB or CR (OWASP), with its unit test; this also keeps the phone as text. · Belongs: a fix round
  on #132, once the owner decides 204 (nothing carries; 204 is this PR's own finding).

### R3-F5 — should-fix (plausible) · «تعديل الحقل» lands on the section's heading, so the report's notice above it can be off-screen
- Where: apps/web/src/pages/dashboard/fieldSections.ts:20-27, apps/web/src/features/spaces/hooks/editor/useHashLanding.ts:31-39 at a12c0790
- Seen in the code:
  - The link is `?report={id}#{group}`. `useHashLanding` scrolls `#{group}`'s heading to the top
    (`scroll-mt-28 lg:scroll-mt-20`) once, as soon as the editor's read answers.
  - The notice is drawn as the section's previous sibling (SpaceEditor test "shows its notice above its section"),
    from its own read, often after the landing.
  - For «أخرى», the hash is `#report`. If the editor's read answers first (always, when the editor's query is cached
    from an earlier visit), the landing finds no `#report` element, and since it runs once per opening it is never
    retried.
- Scenario: an owner in data reports → a «ساعات العمل» report → «تعديل الحقل» → the profile scrolls «ساعات العمل» to
  the top. The notice «بلاغ مفتوح على …», with «تم التصحيح», sits above the viewport, at most its bottom edge
  showing. Plausible: the offsets were not measured, and the real run did not do R-cases with reports.
- Fix: when `?report=` names an open report, land on `#report` (the notice already has `tabIndex={-1}`), and let the
  landing wait for the notice's read (or re-run it when the notice appears); add a test for an «أخرى» report with a
  cached editor. · Belongs: a fix round on #132 (folded into `e3b8a3ab`).

## The checklist (lines 1–7, each answered)

**1. Every commit of my range read** (diff and stat; the files at the head where a later commit changed them):
- U5:
  - `7edd61a4` the owner's overview: work queue, present, announcements tile, ending card, states;
  - `0d5eb142` the admin's overview: five tiles, completeness, privacy note;
  - `b8029521` finance: address, month, income tab, income CSV, `useMonthCollections`;
  - `c4c431c9` debts tab: four tiles, owes and credit paging, payers, debts CSV;
  - `947629fd` occupancy tab: stay, peak, attendance, heatmap, 14 days, CSV;
  - `9491efeb` «حسابي» card and the two helpers;
  - `8720f77c` the desk's five lines and the row's price;
  - `f8eeac35` the live region without the name (102);
  - `fd266d46` the staff menu's held item;
  - `c56dca3c` «أُضيف في», «مقبوضاته هذا الشهر», «عرض مقبوضاته»;
  - `32178078` `refusedAdmin` and the insert buttons' names (106).
- U6:
  - `06425a84` the audit feature and the owner's log (14);
  - `3cfaac2f` the admin's log;
  - `7454f2f1` the three platform-settings cards;
  - `6412e22b` the public contact from the API, env removed;
  - `ca41fdeb` receptionist named in the person option (94);
  - `4e010aa8` the link dialog worded from a fresh read (95);
  - `cfac6125` «يعالجه» filter and the sheet's title;
  - `9309a221` `editable` offered (158);
  - `34520e2f` exact-email read, its failure state (89);
  - `0e83d63d` `ALREADY_OWNER` → «اربطه بالمساحة» (83);
  - `fb5adcd9` owners and users gaps (G27.1–G27.4, G29.1);
  - `0913363b` `MenuActionItem` held (105, the admin's side);
  - `21bfe2a5` upload bar (73), prototype limits (74);
  - `3f61eb7c` spaces list and editor gaps (G26.1–G26.5, G26.8, G20.2);
  - `de0a9eb9` lookups: no active switch, position, arrow names, hints;
  - `e145a9e4` retired amenities on the owner's checklist (99);
  - `e3b8a3ab` report notice, `?open=`, hash landing (184).

**2. The plan's decisions built as approved:**
- D5.1–D5.11 and D6.1–D6.15 are built as §5 says, except what F1, F2, F3 and F5 name.
- D5.5's `dir="ltr"` reaches past the peak hour (F2).
- D5.3's «حتى {time}» is the time the browser received the answer (`dataUpdatedAt`), not a server instant. The answer
  carries none, so this is acceptable.
- D6.1: the admin's deleted space is never a link (L-W2-D2), against D6.1's "→ spaces `?status=deleted`". It agrees
  with T157, so the plan contradicts itself and the build followed the test; acceptable.

**3. Money, roles, privacy, keys and locks:**
- *Money:*
  - The owner's overview answer type (`packages/shared/src/overview/responses.ts`) has no amount field. The page
    renders counts only; no amount in text, attributes or names (verified by reading every component of the feature).
  - Finance draws the server's figures. The only browser arithmetic is the month's % change (`monthChange`), the CSVs'
    shekel conversion (`toFixed(2)`), and the ledger range's dates.
  - Owed and uncollected are separate tiles, never added (193).
  - The debts export reads every page at `limit=50` until `hasNextPage` is false.
- *Roles:* finance, the audit log and the overview are `roles: OWNER` in `SPACE_NAV`/the guard (`navigation.ts:30-41`).
  The admin's pages are the admin branch. The API's authorization is outside my range.
- *Privacy:* the owner's log types `MASAHA` with no id or name (`AuditActor`) and draws «فريق مساحة». The admin's log
  filters by persons only. The debts CSV's phones leave the device only by the owner's download.
- *Keys and locks:* none in my range.

**4. Planned tests and breaks** (lane W1 and W2 reports for the breaks; the tests read):
- T110–T190: each is present under its name or an equivalent.
- Weaker:
  - T110 checks `container.textContent` in English only. It is safe today because the type holds no amount, but an
    amount placed in an `aria-label` or `title` would pass it.
  - T111 checks hrefs only, so it cannot see F3.
  - The `OwnerActionsMenu` test (F1) checks by pointer only.
  - T177 covers a field group, not «أخرى»/`#report` (F5).
- No test renders the debts or occupancy tiles in Arabic (F2).
- Breaks: only in a report — W1 lists B110–B142 red, W2 B150–B190 red. Not re-run (no test runs allowed).

**5. Each screen of my range:**
- **12** complete but for F3.
- **19** complete but for F2 and F4.
- **25** complete. It differs from the prototype only as the DIs decided: five tiles (DI7) and the stale helper (DI8).
- **O13 / 31** complete: intro, search, the three filters with P5's sheet, count, table from 768 and cards below,
  empty, no-match, failure, paging.
- **32** complete: three cards, each with its own GET, skeleton, failure, save, unsaved badge and discard; contact
  normalised from the answer, and the public contact invalidated.
- **20–24 and 26–30** gaps closed as §4.1 lists, except F1 (screen 27) and F5 (screens 20, 21, 26). The staff
  screen's collections show «—» while loading as well as on failure: acceptable.
- Seen in the code only: dark, 390 / 768 / 1440 and real-browser rendering were not seen by me. Only in a report: the
  lead's tour (owner 15/15, admin 9/10) at 1440/390 in English dark and 1440 Arabic light.

**6. Findings my range closes:**
- Built as *Resolves when* says: 14, 73, 74, 83, 89, 94, 95, 99, 102, 106, 158, 184.
- Not as its *Resolution* says: **105** only for two of the three menus (F1).
- 193: accepted with the owner's line (U10's commit), and the tile keeps it.

**7. Documents:**
- `features/overview.md:35` states `#unpriced` lands (false, F3).
- Finding 105's *Resolution* and `space-links.md:161` say "both menus" / "the users page", and leave out the owners
  page (F1).
- The rest read true to the code: `finance.md`, `audit.md`, `platform-settings.md`, the space-links, spaces, lookups
  and data-reports History lines, `architecture.md` §3's contact paragraph, `setup.md`, and CHANGES.md's D6.14 row.
- `#132` is in place of `#PRNUM` in the lines read.

## Decisions taken without the owner in my range, judged
- **LEAD-D6 / LW1-D1** (a new key `staff.reissue.refusedAdmin`) — **sound.** D5.10's EC17 key would have made the
  re-activation's line false.
- **LW1-D2** (`?page=` / `?credit=` for the debts lists) — **sound**, DI29's own pattern; month and tab changes reset
  both.
- **LW1-D3** (a feature-local `LoadFailure` for P7's offline) — **acceptable.** It is duplicated in `overview` and
  `finance` (two copies of `LoadFailure` and `useLoadFailure`): a nit, not a defect.
- **LW1-D4** (the paid tile a count, the uncollected tile visits with the amount in its helper) — **sound** as words,
  but the box it is drawn in is wrong (F2).
- **LW1-D5–D9** — **acceptable.**
- **L-W2-D1** (`ALREADY_OWNER` opens the link dialog in place) — **acceptable** (no user-by-id read).
- **L-W2-D2** (a deleted target never a link) — **acceptable** (T157).
- **L-W2-D3** (the admin's actor filter persons only) — **sound** (the contract). Small inconsistency: the filter
  shows when `meta.actors` has ≥ 2 entries before persons are filtered, so the admin can be offered «الكل» plus one
  person. A nit, not reported.
- **L-W2-D4–D9** — **acceptable.**
- **L-W2-D10–D13** (lookups' position through the order route, the live region per row) — **acceptable.**
- **L-W2-D14** (the retired amenities after the catalogue's) — **sound.**
- **L-W2-D15** — **acceptable.**
- **L-W2-D16** («أخرى» lands on `#report`) — **sound in intent, not robust** (F5).
- **L-W2-D17** — **acceptable.**

## Outside my range
- `UnpricedCard` (W3's desk) lacks the anchor the overview needs; the fix is placed in F3.
- `csvOf` and finding 204 are lane L's; the defect is placed in F4 because D5.4's CSV is in my range.

## Not checked, and why
- No test, build or browser run (the rules). Layout at 390 / 768 / 1440, dark mode and Excel's parsing are judged from
  the code and named "plausible" where it matters (F4, F5).
- The API's routes behind these screens (authorization, the overview's counts equalling their lists, `editable`'s
  schema): other reviewers' commits. Only the web's use of them was read.
- The finance and audit copy were read in Arabic; the English catalogues were only sampled. Every lookups and
  platform-settings sub-component was not read line by line (their stats and hooks were).
