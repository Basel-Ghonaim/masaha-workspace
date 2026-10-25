# FINANCE_AUDIT — execute PR 1 only (`feat/audit-log`)

You are worker B's **executor** of the first of this item's three pull requests, in a fresh conversation. You did not
plan it and you will not review it. **The plan is approved; do not re-decide anything in it.** You build PR 1 whole:
the four carried commits (finding 151 among them), the audit reader for the owner and the admin, the tests, the
breaks, the real run, the PR, CI. **PR 1 has no migration** and no `apps/web` change.

## 0. The rule for this run — no stop until ready for review

**The owner's autonomy rule applies to the whole run** (`C:\dev\masaha\workspace\_SHARED\AUTONOMY_2026-10-25.md` —
read it first). You do not stop and you do not ask until the work is **ready for review**: the PR open, CI green on
its pushed head, `CLEAN`, the report written, the final reply sent. Every "stop and ask" or "stop and report" in the
plan becomes **decide, record, continue**: choose the option that best keeps the plan's intent, the documents' rules
and v1 scope, the smaller and safer change first; record it as you go under *Decisions taken without the owner*
(what you met, the options, the choice and why, how to undo). A command or lane you cannot run → find the root cause
(up to three tries; Docker Desktop not running: `Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"`,
then wait for `docker info`), else record it under COULD NOT RUN with the exact error, continue every step it does
not block, and let CI judge on the pushed head. A real-run case the data cannot hold → not performed, with why and the
test that proves it. **The hard limits hold:** never merge, push to `main`, force-push another branch, create an Issue
or delete a remote branch; never change data through the app or the database to pass a case, never reseed; never
touch worker A's worktree (`C:\dev\masaha\app`), database (`masaha_dev`) or ports (3320, 5320); never skip, `.skip` or
weaken a test, config, timeout or lane; never print a secret; no tool attribution. **Never stop for the file count**
— report it.

## 1. What to read — and only this

The owner's instruction overrides the bootstrap's session checklist for this task, stated here: **do not run the
`start-work-item` skill** and do not read `docs/development/workflow.md` whole. `CLAUDE.md` is already in your
context. Read only:

1. `C:\dev\masaha\workspace\WORKER_B\FINANCE_AUDIT\0_CARRIED_FROM_123.md` whole, and in
   `C:\dev\masaha\workspace\WORKER_B\_DONE\ANNOUNCEMENTS\6_REVIEW_PR4_CLAUDE_CODE.md` only its findings 1–4.
2. `C:\dev\masaha\workspace\WORKER_B\FINANCE_AUDIT\2_PLAN.md` — **these parts only:** the owner's approval note at
   its top (binding, it wins where the plan differs) and the header; §1; §2 *Scope*, *Acceptance criteria* and *Out of
   scope* as they touch PR 1; §3; §4's owner's decisions as built, D1's PR 1 routes, D2, D3, D4, D5, D6, D14, D15's PR
   1 part; §5 S1, S4–S7, S12, *Rules the item touches*; §6; §7's PR 1 row; §9 *PR 1 — carried* and *PR 1 — the audit
   reader*, *Not tested, and said*; §10's audit lines; §11 *PR 1*; §12 (12.1–12.9 for PR 1); §13 (the decisions, all
   approved); Appendix A *PR 1*. Nothing of PRs 2–3 unless a step needs it.
3. In the repository: the code and documents a step touches, when that step needs them — search first (`git grep`),
   then read the section, not the whole file. The `open-pr` skill may help at the end.

Read each file once. A document a step proves to need: read the part it needs and say so in the report.

## 2. Then begin

1. **Preconditions:** `C:\dev\masaha\app-b` detached at the latest `origin/main` (`39ef0504`, #124, or later) and
   clean; `masaha_b_dev` / `masaha_b_test` at #123's migration `closure_extension_key` (`npx prisma migrate status`;
   pending → `npx prisma migrate deploy` + `generate` on both, and say so); `npm run build -w @masaha/shared`.
2. **12.1 first** — the base diff from `3855e37f` to `origin/main`: #123 (its tree equals `ff8743c8`, which the plan
   read) and #124 (worker A's web and documents — `features/subscriptions.md`, `overview.md`, the findings index among
   them: re-read each on `main` before editing it). A difference the plan does not cover → decide and record.
3. **Worker A runs beside you:** PAYMENTS_STEP10 PR 1 (`feat/payments`: `apps/web`, documents) in `C:\dev\masaha\app`.
   It shares no code file with you; shared documents (`api-contract.md`, `v1-mvp.md`, `overview.md`, `docs/README.md`,
   the findings index — you record 151 and 152, A 165): each side keeps its own lines; whichever merges second
   rebases. Its web lanes may overlap yours: before each full lane, record the free memory and whether a `vitest` of
   `C:\dev\masaha\app\` runs; never stop its processes; the memory rule (a lane killed for memory: re-run once when
   quieter, then CI judges).
4. **Build PR 1 as §12 says:** the branch `feat/audit-log` from the latest `origin/main` (`--no-track`); the carried
   commits C0a–C0c first (finding 151 written and resolved in C0a; C0b's `conflict`), then C1–C2; per commit `npm run
   lint`, `npm run typecheck` and the test files the commit touches, each test red before its code; on the head once
   `test:unit`, `test:api` (**no command timeout** — ≈ 10 minutes), `format:check`, `check:links`, `check:conflicts`,
   `npm run build -w @masaha/shared`; every break of 12.5 for PR 1, its red output recorded, restored **from a backup
   copy** (never `git checkout -- <file>`); the real run on 3321 (12.6's PR 1 cases and its named writes; the script
   self-judging, `ALL PASS`, and **never keeping an `/auth/` request's body**); **finding 152** (Q10) in C2.
5. **`#PRNUM`, push, the PR:** replaced per commit tree by a self-checking script (the model:
   `C:\dev\masaha\workspace\WORKER_B\_DONE\ANNOUNCEMENTS\scripts\`' PR 4 script, its branch adapted), the next
   number checked just before the push with `gh api "repos/Basel-Ghonaim/masaha/issues?state=all&per_page=1" --jq
   '.[0].number'` plus one — **Issues share the numbers** (#125 and #126 are this plan's and worker A's tracking
   Issues, so the next PR is #127 or later; `gh pr list` alone would miss them); **after `gh pr create`, compare the
   number it answered with the commits'** — if worker A opened first, redo `#PRNUM` on your own branch and push with
   `--force-with-lease=feat/audit-log:<the sha you pushed>`. The PR: title `feat(audit): read the owner's and admin's
   logs`, `--assignee @me --label feat --label area:api --label area:docs`, "Carried from #123" in its description
   (12.9); CI green and `CLEAN`; the conflict check against any open PR (12.8). A red CI lane → find why, fix, fold,
   push again.
6. Write nothing outside the repository except this folder's `4_REPORT_PR1.md` and `scripts\`.

## 3. Discipline

Write `4_REPORT_PR1.md` **as you go** (after the first checks, each commit — sha, subject with its length, the red
line, the green line —, each break, each decision taken, the real run, the push, CI). Keep long outputs in
`scripts\` and read exit codes. Stage by path (never `-A` or `.`); each commit message written to a UTF-8 file
**without a BOM, LF line endings**, with a body saying why, `git commit -F <file>`; subjects ≤ 50, your count
decides; **no tool attribution**; **no `fixup!`, `style:` or `wip` commit left** — a fix folds into its commit
(`--fixup` + `GIT_SEQUENCE_EDITOR=:` autosquash); **no rebase left in progress**; `git status --short` clean at the
end; stop the API by process id (the `tsx watch` child, the server, `pino-pretty`), port 3321 free; name every local
`backup/*` branch you leave. Never claim a result you did not see: copy the line, read the exit code.

## 4. Your final reply — this shape

```
Status: READY FOR REVIEW | INCOMPLETE (only if nothing at all could continue)
PR: #<n> <url> · head <sha> · CI <green/red> · <CLEAN/not CLEAN> · files <count>
Commits: <sha> <subject> (<chars>) — one line each, the carried ones first
Carried from #123: <items 1–4: done in <sha>, red then green, its break red>
Findings: 151 (resolved), 152 (recorded) — <their files>
Ran and passed: <each command, with the result line you saw>
Ran and failed: <each, what failed, what you did>   (or "none")
Not run locally (CI judges): <each lane, and CI's result on the head>
COULD NOT RUN: <each, the exact command, the exact error, why>   (or "none")
Breaks: <each: red seen / NOT red (why, and the break made instead)>
First checks: <each of §12.1 and §12.2 for PR 1>
Real run: <each case and its answer> · data changed: <each write, with ids>
Open PRs and merge order: <worker A's PR, shared files, which merges first>
Departures from the plan: <each, with its reason>   (or "none")
Decisions taken without the owner: <each: met, options, chose, why, undo>   (or "none")
Leftovers: <backup/* branches left; "no rebase in progress" checked>
Report: C:\dev\masaha\workspace\WORKER_B\FINANCE_AUDIT\4_REPORT_PR1.md
```
