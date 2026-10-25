# OWNER_SETUP — execute PR 3 (`feat/owner-staff-settings`, Staff and Settings)

You are the **executor**, in a fresh conversation. You did not plan this item and you will not review it.
**The plan is approved; do not re-decide anything in it.** You build **PR 3 only**, the item's last.

## 1. Read, then begin

1. **Precondition:** PR 2 (#98, `feat/owner-packages`) is merged — `gh pr view 98 --json state` → `MERGED`
   (at `cf3190a4`, 2026-10-20); if not, stop.
2. Work in `C:\dev\masaha\app` only — never in `C:\dev\masaha\app-b` (worker B) or
   `C:\dev\masaha\app-design` (reviews and planners read there). Read `CLAUDE.md` at the repository's root.
3. Read the plan **whole**: `C:\dev\masaha\workspace\WORKER_A\OWNER_SETUP\2_PLAN.md` — **the owner's
   approval note at its top binds and wins where the plan differs**: this PR is the plan's **"PR 2"** (its
   commits 1–6: the handover at a space; the staff page; deactivate, reactivate and reissue; the settings;
   the attendance card; the debt reminder), tests 21–41; **A3 replaces S4** — USERS' one-time password
   dialog takes a required `recordHandover` from its caller, `staff` owns the space's handover call (test 21
   in `staffRepository.unit.test.ts`; test 22 retitled as the note says); the refusal lines as the note
   corrects them (a staff member's 404 names both causes; a 403 none); `staff.count` zero «لا يوجد موظفون»;
   design issue 15 folded (the forced change's line).
4. **Carried from #98 — this PR's first commit(s), before the plan's commit 1:** read
   `C:\dev\masaha\workspace\WORKER_A\OWNER_SETUP\0_CARRIED_FROM_98.md` whole and the review it cites
   (`6_REVIEW_PR2_CLAUDE_CODE.md`), and build it as it says — each code fix red first, then green, with its
   break; finding 102 recorded. The PR's description says "Carried from #98". If an item proves larger than
   the file says, stop and ask.
5. **Read #96's and #98's reports** (`4_REPORT_PR1.md`, `4_REPORT_PR2.md`) for what PRs 1–2 built and their
   departures (`SPACE_PAGES`, `spacePagePath`, `meanwhileLines`, `useRowWrite`, `RefusalText`'s `lines` from
   the carried commit); build on them as merged.
6. Follow the plan's §13 for its "PR 2": the first checks against the merged `origin/main` (`git diff
   --name-status 8c429ff4 origin/main`: worker B's DESK PR 4 may have merged API and docs changes — a code
   file this PR names changed in a way not covered → stop and ask; **check 5's `useServerForm` reads
   `failureTitle` on every render**, which the attendance card needs — else stop and ask; `packages/shared`'s
   staff, settings and occupancy types against §9 — a difference → stop); the branch
   `feat/owner-staff-settings` from the latest `origin/main` (`--no-track`); per commit `lint` and
   `typecheck`; on the head each lane once; the real run; `#PRNUM`; push; the PR; CI green and `CLEAN`; the
   conflict check against any open PR (worker B's DESK PR 4 may be open: shared documents only). Stop at
   §13's *Stop and ask*.
7. **Finding numbers:** 102 is the carried one; any further finding takes **103** and on.
8. `docker start masaha-postgres-1` (never `db:up`; never `npm ci`); API on 3320, web on 5320, worker A's
   `masaha_dev` (migrate it to `main` first if `prisma migrate status` says a migration is pending —
   `npx prisma migrate deploy` in `apps/api`, then `prisma generate`). The real run with a browser tool that
   takes **real screenshots** — the `playwright` MCP tools if present, otherwise local headless Chrome over
   CDP; say which. Arabic light and English dark, at 390, 768 and 1440: §13's **PR 2 cases** (the staff page,
   add with a new email and with an existing one, the one-time dialog and its handover, the re-issue held
   and offered, deactivate and reactivate; the settings' cards, the attendance card's one save, visit
   pricing, the reception switch, the reminder's inserts, refusals and restore; reception refused `/staff`
   and `/settings`). Screenshots to `C:\dev\masaha\workspace\WORKER_A\OWNER_SETUP\shots\pr3\`.
9. **The demo accounts:** if one refuses `SEED_DEMO_PASSWORD`, **stop and report** — never reset passwords
   or change data through the app to get past it. Undo what your run changes where the app allows it; say
   what remains (receptionists you add stay, deactivated).
10. If you are Claude Code, the project's skills may help (the plan's appendix is only a map). Write nothing
    outside the repository except this folder's `4_REPORT_PR3.md`, `shots\` and `scripts\`.

## 2. A test you cannot run stops the work

A test **failing** because its code is not written yet is the plan's red step — normal. A test, lane or
command you **cannot run** is not: it errors before any test runs (the database unreachable, Docker down, a
port taken, a module or `dist` missing, a migration pending, `No test files found`, a Vitest or TypeScript
startup error, the whole run timing out, a crash with no result); a break you could not make or run; a
real-run case you could not perform (other than those the plan names). **Then stop at once** — never skip,
`.skip` or delete a test, never change a config, a timeout, `.env`, a script or a lane, never mock what the
plan does not, never run a narrower command and call it the lane, never call it "flaky" and move on. Write
the command, its exact error and where you were into the report, and reply with §5's shape,
`Status: STOPPED`.

**Known exceptions (the owner's decisions on #96 and #98):**
- `routes.component.test.tsx` › "lists the owner's eleven pages" (finding 87) may miss its 3 s locally when
  the machine is loaded. If **only that test** fails and it passes alone, record both runs (times, free
  memory) and go on; **CI's `test:component` is the judge** — if it fails there, stop.
- If the full component lane is **killed for memory**, re-run it once when the machine is quieter; killed
  again → record it, carry on, and CI's `test:component` is the judge on the pushed head.

**A plan that proves false against the code:** stop too, say exactly what and why, and offer the fix — do
not choose it yourself. **A break that stays green:** stop — unless it is plainly your own test's defect, or
the plan's break cannot change the outcome (as a bound already excluded by another); then make the break
that can, see it red, and state it as a departure.

**Never claim a result you did not see:** a command passed only if you saw its own output say so; copy that
line (read it by its exit code). A break counts only when you saw it red.

## 3. Limits, memory, and not losing work

- Write `4_REPORT_PR3.md` **as you go**: after the first checks, after each commit (sha, subject with its
  length, the red line before the code, the green line after), after each break, after the real run, after
  the push. If you stop for any reason, the report already says where the work stands.
- **Memory:** before each full lane: no `vitest`, `tsc` or dev server of `C:\dev\masaha\app-b\` runs (worker
  B's — never stop its processes; wait), and the free memory written into the report. One full lane at a
  time.
- Each full lane **once, on the head**; re-run only if a file it covers changed after it passed.

## 4. Discipline

Stage by path (never `-A` or `.`); each commit message written to a UTF-8 file **without a BOM, LF line
endings**, with a body saying why, and `git commit -F <file>`; subjects counted ≤ 50; **no tool
attribution**; a fix before the push folds into its commit (`--fixup` + `GIT_SEQUENCE_EDITOR=:`
autosquash); never print a secret or a password (the one-time passwords of the real run included — never in
the report or a screenshot's file name); never merge, create an Issue, or comment on another PR.
`git status --short` clean at the end; stop both servers by process id; ports 3320 and 5320 free.

## 5. Your final reply — this shape, finished or stopped

```
Status: DONE | STOPPED
PR: #<n> <url> · head <sha> · CI <green/red/pending> · <CLEAN/not CLEAN>   (or "no PR")
Commits: <sha> <subject> (<chars>) — one line each, the carried one(s) first
Carried from #98: <each item 1–8: done, its test and break red seen / not done (why)>
Ran and passed: <each command, with the result line you saw>
Ran and failed: <each, what failed, what you did>   (or "none")
COULD NOT RUN: <each test, lane, break or real-run case not run, the exact command, the exact error,
               why>   (or "none" — only if every planned run happened)
Breaks: <each: red seen / NOT red (why)>
Real run: <each case and its screenshot, or NOT RUN (why)>
Data left in masaha_dev: <what the run changed and did not undo>
Departures from the plan: <each, with its reason>   (or "none")
Stopped at (if STOPPED): <the step, and what the owner must decide or fix>
Report: C:\dev\masaha\workspace\WORKER_A\OWNER_SETUP\4_REPORT_PR3.md
```
