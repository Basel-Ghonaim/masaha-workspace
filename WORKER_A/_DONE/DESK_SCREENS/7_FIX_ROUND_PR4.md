# DESK_SCREENS PR 4 (#124) — the fix round, in full

You are worker A's executor, back on your own PR **#124** (`feat/subscription-sheet`, head `bc8fe86a`). Its Claude
review (`C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\6_REVIEW_PR4_CLAUDE_CODE.md`) says **mergeable after a fix
round**. The owner's decision: **every finding, F1–F6, is fixed in this round — nothing is carried to a later PR.**
The supervisor confirmed F1 and F3 in the code. Read the review's findings section whole, then this file; nothing
else unless a fix needs it (search first, read the section). Do not run the `start-work-item` skill.

## 0. The rule for this run — no stop until ready for review

The owner is away. **The autonomy rule applies** (`C:\dev\masaha\workspace\_SHARED\AUTONOMY_2026-10-25.md`): you do
not stop and you do not ask until #124 is ready for review again (pushed, CI green on the new head, `CLEAN`, the
report and the PR's description updated, the final reply sent). A choice a fix leaves open → decide, record under
*Decisions taken without the owner* (met, options, chose, why, undo), continue. The rule's hard limits hold: never
merge, push to `main` or force-push another branch; never change data through the app, API or database, never
reseed; never skip or weaken a test, config or lane; never print a secret; no tool attribution. Never stop for the
file count — give it in the reply.

## 1. First: bring the branch up to `main`

The owner is merging worker B's **#123** (the closure extension: `apps/api`, `packages/shared`, a migration, the
two `errors.ts`, documents — `subscriptions.md` and `overview.md` shared with yours as text; `git merge-tree` was
clean). **Before any fix:**
1. `git fetch origin`; `gh pr view 123 --json state,mergeCommit`.
2. If it is `MERGED`: `git rebase origin/main` on `feat/subscription-sheet` (no other branch touched). A text
   conflict in a document → keep both sides' lines, in PR order; record it. Then `npm run build -w
   @masaha/shared` and, in `apps/api`, `npx prisma migrate deploy` and `npx prisma generate` on `masaha_dev` (#123's
   migration `closure_extension_key`), each exit code read.
3. If it is still open: carry on from the current base; **check again just before the push**, and if it merged by
   then, rebase onto `origin/main` then (same steps), before pushing.
Never `git checkout -- <file>`, `stash` or `reset --hard`; no rebase left in progress at the end.

## 2. The fixes — each folded into the commit that made the code

The owner's method: **a fix is folded into its original commit** (`git commit --fixup=<sha>` then
`GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash <base>`), never a new fix commit; no `fixup!` left in the pushed
branch. Find each finding's commit with `git log -L` / `git blame` on the head. Expected homes (check them): F1,
F3, F4 → `feat(desk): subscribe a new or known customer` or `feat(desk): renew a subscription with its debts`
(where the lines were born); F2 → the commit that added `SubscriptionSheet` and its opener; F5 → the commit that
added `useSpacePrices`' sheet use; F6 → the commit that touched `desk.md`'s code map for the sheet.

1. **F1 (money) — a lost answer is not a refusal.** The half state (`half.title`, the submit's «حفظ الاشتراك» label
   and `close()`'s «… في الزبائن بدون اشتراك.» toast) only when the subscribe was **refused** (the server answered
   4xx). A lost answer (network, timeout, no answer) keeps the lost line «لم يصل الرد…» and «إعادة المحاولة» with
   **the same key** (the transport's own rule), says nothing definite on close, and never offers a path to a second
   subscription under a new key. Test (red before the fix, green after): create 201, subscribe network failure → no
   «لم يُحفظ الاشتراك», no "with no subscription" toast on close, the retry sends the same `Idempotency-Key`; and the
   refused case keeps today's DI-37 behaviour.
2. **F2 — the focus returns after the sheet**, opened from a «⋯» menu item (the card's, the file's, the desk's
   phone «⋯»): the opener records the trigger (a ref or the element focused when opened), and `SubscriptionSheet`
   returns the focus to it on close when it is still connected (as `PayDialog` does with `isConnected`), else
   Radix's default. Fix the sheet's comment to say what it does. Test: from `CustomerActions`' «⋯» → «اشتراك جديد» →
   Escape → the focus on «⋯» (red before).
3. **F3 (money) — a renewal preselects what it renews.** A subscription made from a published price is matched back
   to its line (by its name — your decision 4 made it the line's title — or by period from its span, audience and
   shift) and offered as the renewal's `current`; **none matching → no preselection**: the choice empty and the
   submit blocked until chosen, never `options[0]`. Update the report's departure that said "offers no current line:
   the choices start at the first". Tests in 76's file: a published «شهري» renewed → «شهري» chosen, its amount on the
   submit; an unmatched one → nothing chosen, the submit disabled.
4. **F4 — test 72's money claim made able to fail:** a hook test where ₪200 is typed on a fixed ₪150 → the body's
   `payment.amountAgorot` is 15000; ₪100 typed → 10000 (a known customer). Seen red under a break that sends the
   typed amount (`money.amount`), then green.
5. **F5 — no empty choices on a focus refetch:** the published choices hide only until a read **since the sheet
   opened** answered (`isFetchedAfterMount`, or this query's `refetchOnWindowFocus: false` — choose the smaller and
   say why); the re-read after a refusal keeps its own loading. Finding 171's rule stands (a fresh read on every
   opening). Test it if a test can reach it cheaply; else say why not.
6. **F6 — `desk.md`'s web code map** names the sheet's hooks, services (`endOf`, `packageLine`, `publishedChoices`,
   `sheetRequest`), component, and the page's `SubscriptionSheetSlot` / `useSheetOpener`. Write `#124` directly (the
   number is known).

## 3. What runs — the owner's rule for this round

- **Before each fold, only the test files the fix touches** (`npx vitest run <file> …` in their lane through `npm
  run test:component -w @masaha/web -- <files>` / `test:unit -- <files>`), plus `npm run lint` and `npm run
  typecheck`, and Prettier on the touched files. Each new test seen **red** before its fix (record the line), green
  after.
- **No full lane locally — forbidden this round.** No `test:unit`, `test:component` or `test:api` over the whole
  workspace, no build checks. **CI on the pushed head judges everything else.** A red CI lane → read why, fix,
  fold, push again.
- **No real run** this round (the fixes are proven by their tests); the local data stays as it is.

## 4. Push and the end

- `git push --force-with-lease=feat/subscription-sheet:bc8fe86a9859b27ece1f86c3947c0046fffabb4a` (your own branch
  only; if you pushed in between, lease on that sha). Check no `#PRNUM` is left (`git grep '#PRNUM'`).
- Wait for CI on the new head (`gh pr checks 124 --watch`, bounded); green and `CLEAN`. A not-`CLEAN` state from
  `main` moving → rebase on `origin/main`, the steps of §1, push again.
- Update the PR's description (`gh pr edit 124 --body-file …`): a *Review fixes* section — each of F1–F6 and how it
  was fixed, the rebase onto #123 if done.
- Append to `4_REPORT_PR4.md` a section *The review's fix round (2026-10-26)*: the rebase, each fix (its commit, the
  red line, the green line), the runs, the push, CI, and *Decisions taken without the owner* for this round.
- Leave no rebase in progress; `git status --short` clean; name any new `backup/*` branch.

## 5. Your final reply

```
Status: READY FOR REVIEW | INCOMPLETE (only if nothing at all could continue)
PR: #124 · head <sha> · CI <green/red> · <CLEAN/not CLEAN> · files <n>
Rebased on #123: <yes, at <sha> / no, #123 not merged at push time>
Commits: <sha> <subject> (<chars>) — all, after the folds
Fixes: F1 … F6 — <folded into <sha>, its test red then green>
Ran: <each command with its result line>   (no full lane, by the owner's rule)
CI on the head: <each lane>
Decisions taken without the owner: <each>   (or "none")
Report: C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\4_REPORT_PR4.md
```
