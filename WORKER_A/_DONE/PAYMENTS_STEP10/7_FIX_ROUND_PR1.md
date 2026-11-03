# PAYMENTS_STEP10 PR 1 (#127) — the fix round, in full

You are worker A's executor, back on your own PR **#127** (`feat/payments`, head `27bcd1a0`). Its Claude review
(`C:\dev\masaha\workspace\WORKER_A\PAYMENTS_STEP10\6_REVIEW_PR1_CLAUDE_CODE.md`) says **mergeable after a fix round**.
**The owner's decision (2026-10-27):** **F1–F4 are fixed in this round**; **F5 is recorded as finding 173** in this
round (a finding only — the layer's `Calendar.tsx` is not changed); **finding 169 (the calendar in the site's first
download) is not fixed here** — it becomes an item of its own before PR 4; this round only corrects its wording (F4).
The supervisor confirmed F1 in the code (react-day-picker 10.0.1's `addToRange`: with `min` 0 an empty selection
becomes `{ from: day, to: day }`; `resetOnSelect` exists in `useRange` and the layer's `Calendar` spreads its props).
Read the review's *Findings* section whole, then this file; nothing else unless a fix needs it (search first, read
the section). Do not run the `start-work-item` skill.

## 0. The rule for this run — no stop until ready for review

**The autonomy rule applies** (`C:\dev\masaha\workspace\_SHARED\AUTONOMY_2026-10-25.md`): you do not stop and you do
not ask until #127 is ready for review again (pushed, CI green on the new head, `CLEAN`, the report and the PR's
description updated, the final reply sent). A choice a fix leaves open → decide, record under *Decisions taken
without the owner* (met, options, chose, why, undo), continue. The rule's hard limits hold: never merge, push to
`main` or force-push another branch; never change data through the app, API or database, never reseed; never skip
or weaken a test, config or lane; never print a secret; no tool attribution. Never stop for the file count — give it
in the reply.

## 1. First: the base

Worker B's FINANCE_AUDIT PR 1 (`feat/audit-log`: `apps/api`, `packages/shared`, documents — shared with yours as text
only: `api-contract.md`, `overview.md`, the findings index) may open or merge while you work.
1. `git fetch origin`; `gh pr list --state open`; `gh pr view 127 --json mergeStateStatus`.
2. If `main` has moved and #127 is not `CLEAN`: `git rebase origin/main` on `feat/payments` (no other branch
   touched). A text conflict in a document → keep both sides' lines, in PR order (B's findings 151–152…, yours
   165–173); record it. Then `npm run build -w @masaha/shared`, and if B's merge brought a migration, `npx prisma
   migrate deploy` and `npx prisma generate` in `apps/api` on `masaha_dev`, each exit code read.
3. Otherwise carry on from the current base; **check again just before the push** and rebase then if needed.
Never `git checkout -- <file>`, `stash` or `reset --hard` (restore from a backup copy); no rebase left in progress at
the end. Make a `backup/payments-pre-review-fix` branch at `27bcd1a0` before the first fold and name it in the reply.

## 2. The fixes — each folded into the commit that made the code

The owner's method: **a fix is folded into its original commit** (`git commit --fixup=<sha>` then
`GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash origin/main`), never a new fix commit; no `fixup!` left in the
pushed branch; every subject unchanged (check after each autosquash — your last fold lost a subject once). Expected
homes (check with `git log -L` / `git blame`): F1, F2, F4, F5 → `feat(payments): list the space's payments`; F3 →
`feat(desk): void a payment`.

1. **F1 — the period's calendar takes two clicks.** Pass `resetOnSelect` to the range `Calendar` in `RangeField`
   (`features/payments/components/ledger/LedgerFilters.tsx`): a click on an empty or full selection starts a new
   range `{ from, to: undefined }`, the second click completes and applies it, two clicks on the same day give one
   day. Check that `picking`'s logic still holds with it (the first click keeps the picker open and marks the start;
   reopening shows the applied range and the next click starts afresh). Correct the comment above `RangeField`.
   Test in `PaymentsLedger.component.test.tsx` (1440): open «Period», click one day → the picker still open, the
   address unchanged; click a second day → the address `?from=…&to=…` (the earlier first), the picker closed; then
   reopen with that range applied and click a day → the picker still open, nothing applied. **Red** with
   `resetOnSelect` removed (record the line), green with it. Correct `payments.md`'s period line if it says
   otherwise.
2. **F2 — test 11's zone case able to fail where the lanes run.** Run the web **unit** lane in a zone west of UTC
   (`test.env: { TZ: 'America/New_York' }` on the unit project in `apps/web/vite.config.ts`, or the lane's own
   equivalent — read how the projects are declared first). The lane-wide setting is preferred over a per-file
   `process.env.TZ` because it also makes the moved `dayText` zone case real; say which you chose and why. Then
   **break 11 again without changing the environment** (`timeZone: 'UTC'` dropped from `periodText`) → red; restore
   → green. A zone change can move other unit tests: **CI's unit lane on the pushed head judges them** (no full
   lane locally). A test it turns red is a real zone defect: fix and fold it if it is this PR's code, else record it
   as a finding (174 and on) and name it in the reply. Say in the commit body that the config line is shared.
3. **F3 — the statement's «⋯» and its focus fallback tested.** Add to `features/desk/components/statement/
   Statement.component.test.tsx`: an owner's statement draws «Payment actions: …» on the payment not voided and none
   on the voided one; reception's draws none; with the «⋯» focused, the void answered and the refetch returning the
   row voided → the focus on the «Payments» heading (`h4`). **Red** with the `h4`'s `tabIndex={-1}` removed (or
   `onGone` dropped), green restored.
4. **F4 — finding 169's wording.** In `docs/architecture/findings/169-…md`: "every component a page draws through
   the barrel" (not "serves"); the split: the `design-system` chunk +81,438 bytes, `jsx-runtime` +7,089, `routing`
   −4,809, the first download +84,506 in all; the cause the calendar library and its date helpers, as measured by
   size only. Its *fix* line stays (a layer entry of its own plus a library chunk `check:build` refuses), and add:
   the owner scheduled it as an item of its own before PAYMENTS_STEP10's PR 4.
5. **F5 → finding 173 (record only).** A new finding `docs/architecture/findings/173-…md` in the findings' form
   (read 172's): the layer's `Calendar.tsx:10` `DateRange` comment says `to` is missing until the second click,
   false for react-day-picker 10 (`addToRange` with `min` 0); a range-mode caller must pass `resetOnSelect` (as the
   ledger now does) or the layer default it; the fix belongs to a design-system change of its own. Add it to the
   index. `Calendar.tsx` itself is **not** changed.

## 3. What runs — the owner's rule for this round

- **Before each fold, only the test files the fix touches** (`npm run test:component -w @masaha/web -- <files>` /
  `test:unit -w @masaha/web -- <files>`), plus `npm run lint`, `npm run typecheck`, Prettier on the touched files,
  `npm run check:links` (F4, F5 touch documents). Each new test seen **red** before its fix (record the line), green
  after.
- **No full lane locally — forbidden this round.** No `test:unit`, `test:component` or `test:api` over the
  workspace, no build checks. **CI on the pushed head judges everything else.** A red CI lane → read why, fix, fold,
  push again.
- **No real run** this round (the fixes are proven by their tests); the local data stays as it is.

## 4. Push and the end

- `#127` is known: write it directly in finding 173 and the index; `git grep '#PRNUM'` on the head → nothing.
- `git push --force-with-lease=feat/payments:27bcd1a0faa664bbefdf4ae7010a40a958ddbbc8` (your own branch only; if
  you pushed in between, lease on that sha).
- Wait for CI on the new head (`gh pr checks 127 --watch`, bounded; no command timeout on it); green and `CLEAN`. A
  not-`CLEAN` state from `main` moving → §1's steps, push again.
- Update the PR's description (`gh pr edit 127 --body-file …`): a *Review fixes* section — F1–F4 and how each was
  fixed, F5 recorded as finding 173, finding 169 scheduled by the owner as its own item before PR 4, the rebase if
  done.
- Append to `4_REPORT_PR1.md` a section *The review's fix round (2026-10-27)*: the base, each fix (its commit, the
  red line, the green line), the runs, the push, CI, and *Decisions taken without the owner* for this round.
- Leave no rebase in progress; `git status --short` clean; name every `backup/*` branch you made.

## 5. Your final reply

```
Status: READY FOR REVIEW | INCOMPLETE (only if nothing at all could continue)
PR: #127 · head <sha> · CI <green/red> · <CLEAN/not CLEAN> · files <n>
Rebased: <yes, on <sha> / no, main unmoved>
Commits: <sha> <subject> (<chars>) — all, after the folds
Fixes: F1 … F4 — <folded into <sha>, its test red then green>; F5 — finding 173 in <sha>
Ran: <each command with its result line>   (no full lane, by the owner's rule)
CI on the head: <each lane>
New findings: <173, and any 174+ from F2's lane> 
Decisions taken without the owner: <each>   (or "none")
Backup branches: <names>
Report: C:\dev\masaha\workspace\WORKER_A\PAYMENTS_STEP10\4_REPORT_PR1.md
```
