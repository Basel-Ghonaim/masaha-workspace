
## More decisions taken without the owner

- **D9 — finding 169: the calendar in the site's first download, recorded, not fixed.** *Met:* the head's first download is 1,140,210 bytes against base's 1,055,704 (+84,506): the shared `design-system` chunk 280,288 → 361,726 bytes (81,242 → 104,172 gzipped), all react-day-picker — the ledger's period is the first built use of the layer's `Calendar`, served through the one barrel. `check:build` passes (it guards dashboard code, data-table, Leaflet). *Options:* (a) a layer entry of its own (as `@shared/design-system/data` serves the table, finding 45) plus a library chunk `check:build` refuses — a design-system and build change beyond this PR; (b) a range without the calendar (two date inputs) — against DI-2 and §9's design; (c) record and go on. *Chose* (c): the smaller change, the plan's design kept, the fix named in the finding (169 is the next free number: 165–168 are this item's, 170–171 taken). *Undo:* do (a) in an item of its own.
- **D10 — the void's dialog places its own first focus.** *Met:* the real run showed the `AlertDialog`'s first focus on «رجوع», not the reason (`autoFocus` loses to Radix's alert dialog in a browser; jsdom honoured it, so test 6 was green): the reason typed went nowhere and the client refused the blank reason — nothing was sent. *Chose:* `onOpenAutoFocus` focuses the reason, `autoFocus` dropped; test 6 now fails without the handler (seen: `expect(element).toHaveFocus()`, `break-6b.txt`). Folded into commit 2. *Undo:* none needed.
- **D11 — finding 172: the desk's write-off dialog has the same first-focus defect, recorded, not fixed.** Checked in the real run (opened and cancelled, no write: "write-off dialog focus on opening: BUTTON رجوع", "writes: 0"). Existing #117 code outside this PR's files: recorded (172, the next free), not done; folded into commit 2 with a line in `desk.md`. *Undo:* fix it in a carried item.
- **D12 — the ledger's phone card no longer repeats the method.** *Met:* the 390 shots showed the method in the card's line and again under the amount. *Chose:* `PaymentAmount withMethod={false}` in the card (the flag is commit 4's, so folded into commit 4). *Undo:* drop the prop.

## Folds and the final commits

- Finding 169 folded into commit 3 (`--fixup=amend`, its message naming 169; the first amend lost the subject and was reworded at once by a rebase `exec git commit --amend -F`); the focus fix and finding 172 into commit 2; the card's method into commit 4 (`--fixup` + `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash origin/main`). After each: "no rebase in progress"; the diff against the backup branch only the folded files. Fix-round checks: touched tests "Tests 8 passed (8)", `lint` 0, `typecheck` 0, `format:check` 0, `check:links` "2887 links in 233 documents and 2090 source files all resolve.", `check:classes` "No physical direction or arbitrary-value classes in 1486 files."
- `#PRNUM` → `#127` by `scripts\prnum1.sh 127` ("PRNUM OK #127 27bcd1a0 (was 79fdf0cc)"); per commit tree `git grep -c '#PRNUM'` 0 in all four; 25 `#127` in `docs`.
- **The pushed commits:** `ee4d2504 refactor(lib): share the day's words` (36) · `4921c5f4 feat(desk): void a payment` (26) · `209a06ab feat(payments): list the space's payments` (41) · `27bcd1a0 feat(payments): show reception its payments today` (49). 83 files ("83 files changed, 3732 insertions(+), 52 deletions(-)").

## On the head (before the folds; the folds touched 7 files, re-checked above)

- Worker B: no `node.exe` of `C:\dev\masaha\app-b` running before each lane; free memory 5,819,760 KB (unit), 5,804,912 KB (component).
- `npm run test:unit -w @masaha/web` → "Test Files 143 passed (143) · Tests 1004 passed (1004)".
- `npm run test:component -w @masaha/web -- src/features/payments src/features/desk src/features/staff src/shared/lib src/pages/dashboard src/shared/copy` → "Test Files 54 passed (54) · Tests 272 passed (272)" (finding 87's family, in `src/pages/dashboard`, all passed).
- `NODE_ENV=production npm run build` exit 0; `npm run check:build` exit 0: "No showcase code in 59 build files (1011 strings checked).", "No dashboard code in the site's first download.", "No data-table or leaflet, nor Leaflet's stylesheet, in the site's first download."
- `check:classes` "No physical direction or arbitrary-value classes in 1486 files."; `format:check` "All matched files use Prettier code style!"; `check:links` "2885 links … all resolve."; `check:conflicts` "No conflict markers found."
- **The first download** (`scripts\firstDownload.mjs`, the model's): head 1,140,210 bytes in 6 chunks (`firstDownload-head.txt`), base (`origin/main` built in this worktree, detached, then back on the branch) 1,055,704 (`firstDownload-base.txt`); no `features/payments` or `features/desk` module, no `data-table`, no `dashboard` chunk in it; no site page chunk imports `data-table` or `dashboard` statically. The growth: D9, finding 169.

## The real run (2026-10-27, `scripts\run1.mjs` on `cdp1.mjs`, shots in `shots\pr1\`)

- API on 3320 and web on 5320 (`masaha_dev`), started for the run and stopped by process id (28684, 7676, 19316, 26876); ports 3320 and 5320 free after ("listening: 0").
- The script re-opens the landing page after writing the language (the account's language replaced the stored one on sign-in, so the first English shots came out Arabic — retaken).
- **pay** (reception, ar 1440): Sara's «استلام المتبقي» → ₪1 cash → toast «سارة خالد · امتحانات بالساعة · المتبقي 30.60 ₪ | استُلم 1 ₪ نقدًا»; Khalid's «تحصيل» → ₪1 → «خالد · زيارة 6 أكتوبر · المتبقي 14 ₪ | استُلم 1 ₪ نقدًا». Shots `1-pay-*`.
- **mine** (reception, ar light and en dark × 390, 768, 1440): «نقدًا للتسليم 2 ₪ · تحويل 0 ₪ (وصلت إلى حساب المساحة) · المجموع 2 ₪ · دفعتان», both rows. Shots `1-mine-reception-*`.
- **ledger** (owner, both languages × three widths): today «اليوم · المجموع 2 ₪ · نقدًا 2 ₪ · تحويل 0 ₪ · دفعتان»; 27 Sep–27 Oct with «إظهار الملغاة» «27 سبتمبر – 27 أكتوبر 2026 · المجموع 1,067 ₪ · نقدًا 967 ₪ · تحويل 100 ₪ · 17 دفعة | الملغاة: دفعة واحدة · 200 ₪», the seed's voided row struck «ألغاها أحمد الشوا: سُجّلت مرتين»; the 390 sheet («الفلاتر 1», the range counted; «عرض 18 دفعة», «مسح الفلاتر»); staff = the owner «أحمد الشوا (أنت)» → ₪180, 2 payments; a 119-day address falls back to today. Shots `1-ledger-*`.
- **voidLedger** (owner, ar 1440): «إجراءات الدفعة: 1 ₪ · خالد» → «إلغاء الدفعة…»; focus on opening TEXTAREA (after D10; the first try showed «رجوع» and sent nothing); the dialog «1 ₪ · خالد · اليوم · نقدًا. تبقى ظاهرة مشطوبة …»; toast «أُلغيت دفعة 1 ₪ · خالد | لا تُحسب في الدخل ولا في التسليم.»; the row left, **focus after: the next row's «⋯» (سارة خالد)**; totals «1 ₪ … دفعة واحدة | الملغاة: دفعة واحدة · 1 ₪». Shots `1-void-ledger-*`.
- **voidStatement** (owner, ar 1440): Sara's file → «عرض الكشف» → the ₪1's «⋯» (₪60, ₪5 and ₪1 offered; none on a voided one) → void → toast; **focus after: H4 «الدفعات»**. Shots `1-statement-*`, `1-void-statement-*`.
- **mineAfter** (reception, both × three widths): both rows struck «ملغاة · ألغاها أحمد الشوا: دفعة تجربة» / "Voided by أحمد الشوا: دفعة تجربة"; figures ₪0, «لا دفعات». Shots `1-mine-after-*`.
- **touch** (owner, 390, touch emulation): the ledger's «⋯» hit areas 44×44, 44×44, 44×44.
- **width break**: the filters' grid at 768 — 2 columns ("293px 293px", `1-width-owner-ar-light-768.png`); with `md:grid-cols-2` removed (backup copy) one column of 598px (`break-filters-grid-owner-ar-light-768.png`); restored from the copy.
- **writeOffFocus** (owner, the desk, read-only): finding 172's evidence (D11).
- **Not performed, by design:** a lost answer on the void (test 4 owns it); a 429 (the dialogs' tests own it); reception's 403 on the ledger (the routes test, and the inventory's direct 403).

## Network log

- The voids: `POST /api/v1/manage/spaces/7/payments/18/void 200 Idempotency-Key: none body: {"reason":"دفعة تجربة"}` (the visit's, from the ledger) and `POST …/payments/17/void 200 Idempotency-Key: none body: {"reason":"دفعة تجربة"}` (the subscription's, from the statement).
- The payments: `POST …/payments 201 Idempotency-Key: 3e22323c-… body: {"amountAgorot":100,"method":"CASH","subscriptionId":1}`; `POST …/payments 201 Idempotency-Key: 869a1e45-… body: {"amountAgorot":100,"method":"CASH","visitId":3}`.
- The ledger's queries: `GET …/payments?voided=EXCLUDE&page=1&limit=20`; `?from=2026-09-27&to=2026-10-27&voided=INCLUDE&page=1&limit=20`; `?from=2026-09-27&to=2026-10-27&recordedById=14&voided=EXCLUDE&page=1&limit=20`; the 119-day address → `?voided=EXCLUDE&page=1&limit=20`. Reception's: `GET …/payments?voided=INCLUDE&page=1&limit=20` (no range, no `recordedById`).

## Data left in `masaha_dev`

- Payment 17: ₪1 cash on subscription 1 (customer 1 «سارة خالد»), recorded by reception (15), voided by the owner (14), «دفعة تجربة».
- Payment 18: ₪1 cash on visit 3 (customer 8 «خالد»), recorded by reception, voided by the owner, «دفعة تجربة». Both are the plan's named writes; the balances are back where they were (a voided payment counts in nothing).

## Push and the PR

- The next number, just before the push: `gh api "repos/Basel-Ghonaim/masaha/issues?state=all&per_page=1" --jq '.[0].number'` → 126, so 127; no open PR. `git push -u origin feat/payments` (a new branch); `gh pr create … --assignee @me --label feat --label area:web --label area:docs` → https://github.com/Basel-Ghonaim/masaha/pull/127 — the number matches the commits'; no second push needed.
