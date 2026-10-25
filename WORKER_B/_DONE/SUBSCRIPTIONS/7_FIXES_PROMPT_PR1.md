# SUBSCRIPTIONS PR 1 (#102) — fix round: the balance query, and the ids' bound

You are worker B's executor, in a fresh conversation (or the one that built #102). **#102 is reopened** by the
owner's rule: its review found one serious fix — the balance query decision 6 rests on — and the test beside it
is fixed in the same round. Every other review item is deferred to SUBSCRIPTIONS PR 2 through
`0_CARRIED_FROM_102.md` — **not here**. Read `CLAUDE.md`, then the review
`C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS\6_REVIEW_PR1_CLAUDE_CODE.md` whole (findings 1 and 2), then your
report `4_REPORT_PR1.md`. Work in `C:\dev\masaha\app-b` only, on `feat/customers`.

## 1. First

1. `git status --short` clean; `git fetch origin`; `docker start masaha-postgres-1` (never `db:up`, never
   `npm ci`; if Docker Desktop is not running, stop and ask the owner to start it).
2. If `origin/main` moved past `befd96f9`: `git rebase origin/main` (text conflicts in shared documents only —
   keep both sides, workflow §9; a conflict in a code file → stop and ask), then `npm run build -w
   @masaha/shared`, and in `apps/api` `npx prisma migrate status` on both B databases — pending → `migrate
   deploy` and `generate`.

## 2. The fixes (each folded into the commit that owns the code: `git commit --fixup <sha>`, then
`GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash origin/main`; bodies kept, a line added where the *why*
changes)

1. **The balance query joins by equality and reads only what it is asked** (review 1, into C4 `feat(payments):
   compute debts in the database` and wherever C5 calls it):
   - `balancesOf` joins two equi-joined aggregates — the visits' payments grouped by `visit_id`, the
     subscriptions' grouped by `subscription_id`, each `LEFT JOIN … ON i.kind = '…' AND x.id = i.id` — or a
     `LEFT JOIN LATERAL` per branch on the existing indexes; recommend one, say why.
   - `customerBalances` and the customer's file pass **the customers asked** into the items (the visits branch
     through one array parameter, `unnest`, as the list does); the file reuses its own items' balances rather
     than a second whole-space query if that is simpler. `customerIdsByPayment` stays whole-space by nature (a
     filter over every customer) but on the equi-joined form.
   - `subscription_usage(space, NULL, …)` filtered by customer after the call: **check with `EXPLAIN` whether
     PostgreSQL pushes the filter inside**. If it does not and the function itself must take the ids, **stop and
     ask** — the function's signature is not changed in this round without the owner.
   - **Prove it at scale:** T26's seed (or a new test beside it) holds a payment per subscription and the plan's
     scale of paid visits (≈ 40,000, one `INSERT … SELECT`), and the list, `?payment=OWES` and a file answer
     inside the test's budget. Record `EXPLAIN (ANALYZE, BUFFERS)` of the three queries at that scale in the
     report (a script in `scripts\`, on `masaha_b_test`). **Break:** the `OR` join restored → the test red (or,
     if the time budget cannot tell, the plan shows the nested loop — say which proved it). B32–B37 re-run red
     then green on the new form.
2. **The ids' bound is proven again** (review 2, into C5's test file): a test calls the repository's list (or
   the route with a filter resolving to them) with **70,000 ids that do not exist** and asserts an empty page —
   no seed needed; keep the 20,000-row seed only if it still catches a revert to `= ANY`, else drop it and say
   so. **Break:** B43 (`Prisma.join`, one parameter per id) → red in the lane, not in a scratch run.

If an item proves larger than this says, **stop and ask** — never leave one undone silently.

## 3. Verify, push, report

- **Run what the change touches** (the owner's rule for fix rounds; no run that only repeats another): `lint`,
  `typecheck` on the head; `npm run test:api -w @masaha/api -- src/modules/payments src/modules/desk
  src/modules/customers` (add any other folder whose files change, and say so); `npm run test:unit -w
  @masaha/api` if a unit file changes; `format:check`, `check:links` if a document changes. **A test seen red
  before its fix is its own break**; a separate break only where the red step did not prove the guard. CI runs
  the rest on the pushed head and judges it.
- **Memory (the owner's standing rule):** before each test run, no `vitest` of `C:\dev\masaha\app\` running and
  the free memory recorded; a run killed for memory: re-run once when quieter, then carry on with CI as its
  judge.
- A short real run on 3321 (`masaha_b_dev`): the customers list, `?payment=OWES` and one file answer as before
  (the same rows and sums as the report's first real run).
- `#PRNUM` is already `#102`; `git push --force-with-lease`; `gh pr checks 102` green on the new head and
  `CLEAN`. Edit the PR description: "Fix round (review of #102)" with both items, and "Deferred to PR 2: review
  items 3, 4, 7, 9; findings 5, 6, 8 to record" pointing at `0_CARRIED_FROM_102.md`.
- **A test you cannot run stops the work**; never skip, never change a config, a timeout, `.env` or a lane;
  never claim a result you did not see. Stage by path; messages from a UTF-8 file without BOM, LF; no tool
  attribution; never print a secret; never merge.
- Append *Fix round 1* to `4_REPORT_PR1.md` as you go. Final reply: Status, PR head, CI, CLEAN, the commits
  (subjects ≤ 50), each item done (red/green, break), the three plans' timings, ran and passed, COULD NOT RUN,
  departures, report path.
