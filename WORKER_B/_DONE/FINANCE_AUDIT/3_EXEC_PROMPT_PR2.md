# FINANCE_AUDIT — execute PR 2 only (`feat/platform-settings`)

You are worker B's **executor** of the second of this item's three pull requests, in a fresh conversation, in
`C:\dev\masaha\app-b` (API on 3321, `masaha_b_dev` / `masaha_b_test`). You did not plan it and you will not review
it. **The plan is approved; do not re-decide anything in it.** You build PR 2 whole: the platform's settings — the
admin's three cards (the new spaces' defaults, the staleness thresholds, the contact), each its own resource and save,
audited and on the admin's log; the public contact (`GET /settings/public`); finding 40 resolved — with the tests, the
breaks, the real run, the PR and CI. **PR 2 has no migration and no `apps/web` change.**

## 0. The rule for this run — you never stop until the whole task is done

- **No stop, no question, for any reason**, until the PR is open, CI is green on its pushed head, it is `CLEAN`, the
  report is written and the final reply is sent (the owner, 2026-10-28; stricter than
  `C:\dev\masaha\workspace\_SHARED\AUTONOMY_2026-10-25.md`, which you read first and which otherwise applies). Every
  "stop and ask" in the plan becomes **decide, record, continue**: the option that best keeps the plan's intent, the
  documents' rules and v1 scope, the smaller and safer change first; recorded as you go under *Decisions taken without
  the owner* (met, options, chose, why, undo). A decision touching money, authorization, privacy or a plan decision is
  marked **SERIOUS** and listed first in the report and the reply — you still continue.
- **A command you cannot run** → find the root cause (up to three tries; Docker Desktop not running:
  `Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"`, then wait for `docker info`); still failing →
  record it under COULD NOT RUN with the exact error and continue every step it does not block. **A command the
  permission classifier refuses** (a force-push) → carry on with everything else and write the exact command in the
  report and the reply.
- **The hard limits hold:** never merge, push to `main`, force-push another branch, create an Issue or delete a remote
  branch; never change data through the app or the database beyond the real run's named writes, never reseed; never
  touch worker A's worktree (`C:\dev\masaha\app`), its database (`masaha_dev`), its ports (3320, 5320) or its
  processes; never skip, `.skip` or weaken a test, config, timeout or lane; never print a secret or keep an `/auth/`
  body; no tool attribution; no migration. **Never stop for the file count** — report it.

## 1. What to read — and only this

Do not run the `start-work-item` skill and do not read `docs/development/workflow.md` whole (the owner's instruction,
overriding the bootstrap's checklist for this task). `CLAUDE.md` is already in your context. Read only:

1. `C:\dev\masaha\workspace\WORKER_B\FINANCE_AUDIT\2_PLAN.md` — **these parts only:** the owner's approval note at its
   top (binding) and the header; §1; §2 *Scope*, *Acceptance criteria* and *Out of scope* as they touch PR 2; §3's PR
   2 lines; §4's owner's decisions as built (11 among them), D1's PR 2 routes, D3's and D4's PR 2 lines, **D7**, D13,
   D14, D15's PR 2 part; §5 **S8, S9, S10, S11** and *Rules the item touches*; §6 (finding 40); §7's PR 2 rows; §9
   *PR 2*, *Not tested, and said*; §10's settings lines; §11 *PR 2*; §12 (12.1–12.9 for PR 2); §13; Appendix A *PR 2*.
   Nothing of PR 3 unless a step needs it.
2. PR 1 as built and reviewed, so you build on it and repeat none of its slips: `4_REPORT_PR1.md` (its decisions, its
   fix round) and `6_REVIEW_PR1_CLAUDE_CODE.md` (findings 1–3) in this folder.
3. In the repository: the code and documents a step touches, when it needs them — search first (`git grep`), then
   read the section, not the whole file.

## 2. What changed since the plan was written (adapt to it; record each adaptation)

- **`main` = `76661f7c` or later.** **#128** (PR 1) merged as built and reviewed: `audit/platformEvents.ts` holds
  `PLATFORM_ACTIONS` and `PLATFORM_ACCOUNT_ACTIONS` (an account action is the platform's only when it names no
  space); `users.service` takes `receptionSpaceOf`; the target joins are one `LEFT JOIN` per entity type (no lateral)
  — **PR 2's `platformSettings` target type joins that shape**, and an entry with no entity id (S8) must read as
  `name: null` there; the audit actions and entity types in `@masaha/shared/audit` are the lists PR 2 extends.
  **#127** (worker A's payments screens) merged: `apps/web` and documents only.
- **Worker A runs beside you:** its PR (`feat/step10-screens`: `apps/web`, `docs`) is open or about to be; it may
  merge while you work. **It shares no code file with you**; shared documents only (`overview.md`, `v1-mvp.md` if it
  touches it, `docs/README.md`, `architecture.md`, the findings index — A's numbers 174+, yours **153** and on). Each
  side keeps its own lines; whichever merges second rebases (only when not `CLEAN`).
- **Finding numbers:** 151 and 152 are taken; yours start at **153**.

## 3. Build it

1. **Preconditions:** `C:\dev\masaha\app-b` detached at the latest `origin/main` and clean (`git fetch origin`; `git
   switch --detach origin/main`); `npx prisma migrate status` on `masaha_b_dev` and `masaha_b_test` (nothing pending
   expected; pending → `migrate deploy` + `generate` on both, and say so); `npm run build -w @masaha/shared`. §12.1's
   base diff from the plan's base to `origin/main` — a difference the plan does not cover → decide and record.
2. **The branch** `feat/platform-settings` from `origin/main` (`--no-track`). Commits as §11 *PR 2* gives them (C1
   `feat(platform-settings): read and save its cards`, C2 `feat(platform-settings): answer the public contact` —
   recount, ≤ 50, each with a body saying why); a unit's code, tests and documents in its commit; finding 40 resolved
   in C1 with its *Resolution* line and the index.
3. **Per commit:** each new test **red before its code** (copy the red line), green after; the test files the commit
   touches; `npm run lint`; `npm run typecheck`; `npm run build -w @masaha/shared` when shared changes; Prettier on the
   touched files; `npm run check:links` when documents change.
4. **Every break of §9 *PR 2* (B1–B12)** run from a backup copy and restored by copy (never `git checkout -- <file>`),
   its red line recorded; a break that stays green → find why, make the break that does catch it, record both.
5. **Memory (worker A may be running):** before each heavy command (a full lane, `lint`, `typecheck`), read the free
   memory (`(Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory`) and record it: **≥ 4 GB** → run; less → wait
   2 minutes and read again (bounded: 45 tries, then run anyway and record it). Never stop worker A's processes. A
   lane killed for low memory → wait for memory, re-run it once; killed again → run it in parts (by directory) until
   every file has run green once. Never leave a lane unrun.

## 4. The complete verification — on the head, before the PR is opened (the owner's rule)

Nothing reaches CI untested. On the head, all green before the push: `npm run build -w @masaha/shared`; `npm run
lint`; `npm run typecheck`; `npm run test:unit` (every workspace); `npm run test:api` (**no command timeout** — about
10 minutes; run it in the background and wait for it); `npm run test:component` (no web file changes, but the whole
suite runs once); `npm run format:check`; `npm run check:links`; `npm run check:conflicts`; `git grep -l '#PRNUM'`
documents only. A failure: simple (a test, a type, a lint rule, a document line) → fix, fold into its commit
(`--fixup` + `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash origin/main`), re-run what it touched and the whole lane
it failed in; SERIOUS → still no stop: find the cause, take the safest course within the plan, record it first.
Finding 87's family (web, slow first lazy imports) missed in a full run and passing alone: re-run alone, record, go on.

## 5. The real run (API on 3321, `masaha_b_dev`)

§12.6's PR 2 cases, a self-judging script (`ALL PASS`; the model: `scripts\realrun1.mjs`, its own check of an actor's
id corrected as PR 1's report says), **never keeping an `/auth/` body**: the admin reads each card; saves each card
(the values chosen so the run can put them back), the audit entry on the admin's log with no entity id and only what
changed, the same values again writing nothing; a new space after a default changed gets it and an old one keeps its
own (only if §12.6 names that write; else proven by T3); a threshold applied at once; `GET /settings/public` with its
`Cache-Control`; a guest, a user and an owner refused on the admin's routes. **Every write named, and each setting put
back to its value before the run** (record before and after). Stop the API by process id (the `tsx watch` child, the
server, `pino-pretty`); port 3321 free.

## 6. Push, the PR, CI

- **The PR number:** just before the push, `gh api "repos/Basel-Ghonaim/masaha/issues?state=all&per_page=1" --jq
  '.[0].number'` plus one (Issues share the numbers; worker A's PR takes one too); replace `#PRNUM` per commit tree
  with a self-checking script (the model: `scripts\prnum-pr1.sh`); after `gh pr create`, compare the number it
  answered with the commits'; if it differs, redo `#PRNUM` on your branch and `git push
  --force-with-lease=feat/platform-settings:<the sha you pushed>` (refused → §0).
- `git push -u origin feat/platform-settings`; `gh pr create` — title `feat(platform-settings): edit defaults and
  contact` (recount), `--assignee @me --label feat --label area:api --label area:docs`; the description: the summary,
  the acceptance criteria and how each is met, finding 40 resolved, the verification run locally (each command and its
  result), the real run, the decisions taken without the owner (SERIOUS first).
- `gh pr checks <n> --watch` (bounded; no command timeout) → all green; `gh pr view <n> --json mergeStateStatus` →
  `CLEAN`. Not `CLEAN` because worker A's PR merged → `git rebase origin/main` (a document conflict keeps both sides),
  re-run lint, typecheck and the touched tests, push with the lease on your own head, watch again. A red CI lane →
  find why, fix, fold, re-run that lane locally in full, push, watch again.

## 7. Discipline and the reply

Write `C:\dev\masaha\workspace\WORKER_B\FINANCE_AUDIT\4_REPORT_PR2.md` **as you go** (first checks; each commit —
sha, subject and its length, the red line, the green line; each break; memory readings; each decision; the
verification; the real run; push; CI). Write nothing else outside the repository except this folder's `scripts\`.
Stage by path (never `-A` or `.`); commit messages from a UTF-8 file without a BOM, LF endings, `git commit -F
<file>`; no `fixup!`, `style:` or `wip` commit left; no rebase in progress at the end; `git status --short` clean;
name every `backup/*` branch you leave. Scripts in files (heredocs can fail to parse); Python writing a file uses
`newline=""`; `jq` is absent — use `gh --jq`. Never claim a result you did not see: copy the line, read the exit code.

```
Status: READY FOR REVIEW | INCOMPLETE (only if nothing at all could continue)
SERIOUS decisions: <each, one line>   (or "none")
PR: #<n> <url> · head <sha> · CI <green/red> · <CLEAN/not CLEAN> · files <count>
Commits: <sha> <subject> (<chars>) — one line each
Findings: 40 (resolved), <new 153+>
Verification (local, on <sha>): <each command with its result line>
Breaks: <B1–B12: red seen / NOT red (why, and the break made instead)>
Real run: <each case and its answer> · writes <each, and put back>
Memory: <readings, waits, kills>
CI on the head: <each lane>
Open PRs and merge order: <worker A's PR, shared files, rebase if done>
Decisions taken without the owner: <count>, in the report
COULD NOT RUN / refused commands: <each>   (or "none")
Leftovers: <backup/* branches; "no rebase in progress" checked>
Report: C:\dev\masaha\workspace\WORKER_B\FINANCE_AUDIT\4_REPORT_PR2.md
```
