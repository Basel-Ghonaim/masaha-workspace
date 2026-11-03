# #131 (`feat/backend-final`) — the fix round, in full

You are worker B's **fix-round executor**, running headless in `C:\dev\masaha\app-b` (API on 3321, `masaha_b_dev` /
`masaha_b_test`). Your PR is **#131** (head `c41a5397`). Its three Claude reviews, one per range:
`C:\dev\masaha\workspace\WORKER_B\BACKEND_FINAL\6_REVIEW_R1_CLAUDE_CODE.md` (the foundation and the items left —
mergeable, three nits), `…_R2_…` (finance — mergeable after a fix round), `…_R3_…` (the overviews and the closing
documents — mergeable after a fix round). **No blocker.** **The supervisor's decision for the owner, who is away
(2026-10-29): every finding of the three is fixed in this round** — this is worker B's last plan, nothing can carry to
a next PR. Read the three reviews' *Findings* and *Outside my range* sections whole, then this file; nothing else
unless a fix needs it (search first, read the section). Do not run the `start-work-item` skill.

## 0. The rule — you never stop until the whole task is done

No stop and no question, for any reason, until #131 is ready for review again (pushed, CI green on the new head,
`CLEAN`, the report and the PR's description updated, the final reply printed). Every decision you take on your own:
recorded (met, options, chose, why, undo). Hard limits: never merge, push to `main` or force-push another branch; no
migration; never change data through the app, the API or the database, never reseed; never skip or weaken a test,
check or lane; never print a secret; no tool attribution; never `git checkout -- <file>`, `stash` or `reset --hard`
(restore from a backup copy); stage by path. **A refused command** (the permission classifier, e.g. the force-push):
carry on with everything else, and print the exact command in the final reply.

## 1. The base

`git fetch origin`; `git switch feat/backend-final` (the local branch exists; its head must be `c41a5397` — if not,
`git switch -C feat/backend-final origin/feat/backend-final` after making `backup/backend-final-pre-review-fix` at the
local head); `gh pr view 131 --json mergeStateStatus` → **rebase only if not `CLEAN`**. Make
`backup/backend-final-pre-review-fix` at `c41a5397` before the first fold. `npm run build -w @masaha/shared`.

## 2. The fixes — each folded into the commit that made the lines

`git commit --fixup=<sha>` then `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash origin/main`; never a fix commit;
no `fixup!` left; **every subject unchanged** (check after each autosquash). The homes below are the reviewers'; check
with `git log -L` / `git blame`; a wrong home → the commit that made the lines, recorded.

**R2 — finance**
1. **R2-F1 (should-fix) — "owed" and "uncollected" overlap.** Option (a) now: correct `docs/api/api-contract.md:726`,
   `docs/features/finance.md:10` and the `DebtsMeta` comment (`packages/shared/src/finance/responses.ts:55`) to say what
   the code does — the uncollected count is the desk's list, which keeps an auto-closed visit left to a customer, so its
   rest is also in that customer's debt, and **the two figures are never added**. Pin it: a test in
   `debts.api.test.ts` — an auto-closed visit left to a customer appears in `owed` and in `uncollected`; red before (if
   the assertion is new behaviour-wise, its red step is a break that drops the visit from one of them), green after.
   **Record finding 193** for the owner's decision (b): whether finance's `uncollected` should leave out visits that
   have a customer (it would break AC-O2's "equal to the desk's list" for the overview's count; Q2 speaks of a walk-in's
   visit only) — options and the reviewer's notes in it; index line. → `71a18c1b` (docs, test), finding in the same.
   Also say the overview's consequence (R1's *Outside my range*: `uncollectedVisits` and `customersOwing` both count
   such a visit) in `docs/features/overview.md` and in finding 193.
2. **R2-F2 — `finance.md` says 45 windows; the code reads 46:** the document says what the code does. → its commit.
3. **R2-F3 — `todayWindow` is production code only a test uses:** remove it from production code (the project's rule:
   no test-only production code) and have the test build its window itself, or use it in production where the plan
   meant it; record which. → its commit.

**R3 — the overviews and the documents**
4. **R3-F1 (should-fix) — `announcements.md` says `runningTypes` is "one `DISTINCT` query"; Prisma issues none:** the
   document says what the query does (or the code makes it one query, if cheaper and as the plan meant — record which).
   → its commit.
5. **R3-F2 — conventions §9 still says the owner's overview "will read" `closures.summary`:** it reads it now. →
   `c41a5397`'s documents or the overview commit that made it true.
6. **R3-F3 — `occupancy.glance`'s default `at = clock()` used only by its test:** drop the default; callers pass the
   clock; the test passes it. → its commit.

**R1 — the foundation and the items left**
7. **R1-F1 — `visits.service.ts`: the new `page` split `terms`'s doc comment off `terms`:** put the comment back on its
   function. → `6d563549`.
8. **R1-F2 — `payments.md` *Who uses it*:** the desk's web sentences back under the desk's bullet, and the overview's
   "will count" made "counts" (true since `a12f928e`). → the commits that wrote those lines.
9. **R1-F3 — `apps/api/.env.example` still describes the seed's WhatsApp as any E.164 number:** say the seed now
   stores it in its one form through the phone rule (finding 153 resolved). → `62d76b81`.

## 3. What runs

- **While fixing:** only the test files each fix touches (`npm run test:api -w @masaha/api -- <files>` on
  `masaha_b_test`; `test:unit -- <files>`), each new test red first; `npm run lint` and `npm run typecheck` before each
  fold; Prettier on touched files; `npm run check:links` when documents change; `npm run build -w @masaha/shared` when
  shared changes.
- **Before the push, once, on the final head:** `npm run lint`; `npm run typecheck`; `npm run test:unit`; `npm run
  test:api` (≈ 10 minutes, **no command timeout**, in the background); `npm run format:check`; `npm run check:links`;
  `npm run check:conflicts`. Before each heavy run read the free memory (`(Get-CimInstance
  Win32_OperatingSystem).FreePhysicalMemory`): ≥ 4 GB → run; less → wait 2 minutes, bounded. A run killed for low
  memory: re-run once; killed again → run it in parts until every file has run green.
- **No real run** (documents, a test and two dead defaults; the behaviour is unchanged).

## 4. Push and the end

- `#131` is known: write it directly; `git grep '#PRNUM'` → nothing.
- `git push --force-with-lease=feat/backend-final:c41a539731fac0743de143fafa0ca8fbea41b95b origin feat/backend-final`
  (refused → §0: print the command).
- `gh pr checks 131 --watch` (bounded; no command timeout) → green; `CLEAN`. A red lane → fix, fold, re-run that lane in
  full, push, watch again.
- `gh pr edit 131 --body-file …`: a *Review fixes* section — each finding and how it was fixed; finding 193 recorded for
  the owner.
- Append to `C:\dev\masaha\workspace\WORKER_B\BACKEND_FINAL\4_REPORT_LEAD.md` a section *The reviews' fix round
  (2026-10-29)*: the base, each fix (its commit, red/green lines, its break), the runs (memory readings), the push, CI,
  decisions taken on your own. Write nothing else outside the repository except
  `C:\dev\masaha\workspace\WORKER_B\BACKEND_FINAL\scripts\`.
- `git status --short` clean; no rebase in progress; name every `backup/*` branch you made.

Print, as your last output:

```
Status: READY FOR REVIEW | INCOMPLETE (only if nothing at all could continue)
PR: #131 · head <sha> · CI <green/red> · <CLEAN/not CLEAN> · files <n>
Rebased: <yes/no>
Commits: <sha> <subject> (<chars>) — all, after the folds
Fixes: R1-F1 … R3-F3 — <folded into <sha>; test red then green where a test applies>
Finding 193: <recorded, its file>
Ran: <each command with its result line; memory readings>
CI on the head: <each lane>
Decisions taken on my own: <each>   (or "none")
Refused commands: <command>   (or "none")
Backup branches: <names>
```
