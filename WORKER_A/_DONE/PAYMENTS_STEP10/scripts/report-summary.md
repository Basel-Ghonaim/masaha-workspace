# PAYMENTS_STEP10 — PR 1 (`feat/payments`) — the executor's report

## Final report (2026-10-27)

**Status: READY FOR REVIEW.** Never merged; no Issue created.

1. **The pull request:** #127 https://github.com/Basel-Ghonaim/masaha/pull/127 — `feat(payments): list the space's payments`, head **`27bcd1a0faa664bbefdf4ae7010a40a958ddbbc8`**; CI green on that head (build, lint, typecheck, test:unit, test:component, test:api, check:classes, check:links, check:conflicts, format:check — all SUCCESS; CodeRabbit skipped); `mergeStateStatus` **CLEAN**; 83 files (plan ≈ 83).
2. **The commits:** `ee4d2504 refactor(lib): share the day's words` (36) · `4921c5f4 feat(desk): void a payment` (26) · `209a06ab feat(payments): list the space's payments` (41) · `27bcd1a0 feat(payments): show reception its payments today` (49).
3. **Run:** `lint`, `typecheck` exit 0; `test:unit -w @masaha/web` 143 files / 1004 tests passed; scoped `test:component` (`src/features/payments src/features/desk src/features/staff src/shared/lib src/pages/dashboard src/shared/copy`) 54 files / 272 tests passed; the production build; `check:build`, `check:classes`, `format:check`, `check:links`, `check:conflicts` passed; after the folds, the touched tests (8 passed), lint, typecheck, format, links, classes. **Not run locally (CI judges):** the full `test:component` lane, `test:unit` of `apps/api` and `packages/shared`, `test:api` — no API or shared change; all green in CI on the head.
4. **Breaks and red-first:** every new test seen red before its code (commits 2–4 by moving the implementation aside from backups — D2); §10's breaks 2–23 each seen red and restored from a backup copy, plus 6b (the void dialog's first focus) and the real run's width break (the filters' grid at 768: one 598 px column). Details below, per commit.
5. **Problems met and solved:** the React compiler's lint flagged reads of a view carrying refs (D4); `formatRange`'s thin spaces in a test; the transport's 5xx back-off in the failure tests (D8); a heredoc that would not parse (files written instead); the run's English shots came out Arabic until the page was reopened after writing the language; the Arabic amount's marks and no-break space in the «⋯»'s label; the void dialog's first focus on «رجوع» in a browser (D10, fixed and now tested); the phone card's repeated method (D12); an `--fixup=amend` that dropped commit 3's subject (reworded at once).
6. **Unexpected, not solved here:** the site's first download grew by 84,506 bytes (react-day-picker in the shared `design-system` chunk) — finding 169 (D9); the desk's existing write-off dialog has the same first-focus defect — finding 172 (D11).
7. **Early conflict check:** `gh pr list --state open` → only #127; worker B's FINANCE_AUDIT PR not open yet: nothing to compare.
8. **Departures from the prompt:** none beyond the decisions D1–D12 (each recorded below). The `start-work-item` skill not run and `workflow.md` not read whole, as the prompt said. Read beyond the plan, as steps needed: the desk's write-off, statement, file and customers-list code and tests; `shared/lists`, `shared/forms`; the layer's `Calendar`, `DatePicker`, `DataTable`, `StatCard`, `Badge`, `Button`, `EmptyState`, `Sheet`; `vite.config.ts` and `scripts/libraryChunks.ts` (finding 169); `payments.md`, `desk.md`, `space-links.md`, `architecture.md` §2, `overview.md`, findings 162, 164 and the index.

**Findings:** 165, 166 (planned), 169 (the calendar in the first download), 172 (the write-off's first focus) — new; 162 — evidence added. **Data left in `masaha_dev`:** payments 17 and 18 (₪1 each, voided «دفعة تجربة»). **Leftovers:** local branches `backup/payments-pre-169`, `backup/payments-pre-fold`, `backup/payments-pre-prnum` (mine; `backup/feat-audit-log-pre-joins` is not mine, untouched); no rebase in progress; `git status --short` clean; ports 3320 and 5320 free.

---

The log below was written as the work went; commit SHAs in it are those before the folds and `#PRNUM` (the final ones are above).

