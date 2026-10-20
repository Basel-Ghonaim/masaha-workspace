# OWNER_SETUP — execute PR 1 (`feat/owner-space-profile`, the owner's space profile)

You are the **executor**, in a fresh conversation. You did not plan this item and you will not review it.
**The plan is approved; do not re-decide anything in it.** You build **PR 1 only**.

## 1. Read, then begin

1. **Precondition:** USERS (#93, `feat/admin-users`) is merged — `gh pr view 93 --json state`; if not,
   stop.
2. Work in `C:\dev\masaha\app` only — never in `C:\dev\masaha\app-b` (worker B) or
   `C:\dev\masaha\app-design`. Read `CLAUDE.md` at the repository's root.
3. Read the plan **whole**: `C:\dev\masaha\workspace\WORKER_A\OWNER_SETUP\2_PLAN.md` — **the owner's
   approval note at its top binds and wins where the plan differs**: three PRs; **this PR is the plan's
   commits 1–5** (shekels to `shared/lib`; the editor's place; the prices table at 1024 px; the public
   lookups; the owner's space profile), ≈ 70 files, titled with commit 5's subject; the refusal lines
   corrected (no cause on a 403; S6's 404 line kept); test 11's title as the note says. Commits 6–7 and
   everything of Packages & prices are **PR 2's — not here** (test 14 here covers the profile and
   reception's 403 only).
4. **Carried items:** if `C:\dev\masaha\workspace\WORKER_A\OWNER_SETUP\0_CARRIED_FROM_93.md` exists, its
   items are this PR's **first commit** (before the plan's commit 1), with its own red-then-green tests as
   the file says, and the PR's description names it ("Carried from #93"). If it does not exist, there is
   none — as of 2026-10-20 there is none: #93 merged at `7d48c9c3` with every review item fixed in its own
   fix round. Its fix round changed files this plan names (the one-time password dialog takes
   `returnFocus`; the users page holds the dialogs; the users list's core): check 3's base diff covers them.
5. Follow the plan's §13 in order for PR 1: the first checks (against the merged `origin/main`; the base
   diff from `4daedc94`; checks 5–8 — check 5's `useServerForm` point concerns PR 3, record what you read);
   the branch `feat/owner-space-profile` from the latest `origin/main` (`--no-track`); per commit `lint` and
   `typecheck`; on the head each lane once; the real run; `#PRNUM`; push; the PR; CI green and `CLEAN`; the
   conflict check against any open PR (worker B's DESK may be open: shared documents only). Stop at §13's
   *Stop and ask*.
6. `docker start masaha-postgres-1` (never `db:up`; never `npm ci`); API on 3320, web on 5320, worker A's
   `masaha_dev`. The real run with a browser tool that takes **real screenshots** — the `playwright` MCP
   tools if present, otherwise local headless Chrome over CDP; say which. Arabic light and English dark, at
   390, 768 and 1440: §13's **PR 1 cases for the profile only** (the head line, the checklist, each
   section, the switcher following the name, the photos, the leave guard; the prices row leading to
   Packages & prices — the link only; reception's 403; the network log with no `/admin/` request from the
   owner's pages; the admin's editor regression and its prices table at 768 as cards). The cases §13 names
   as not producible locally are proven by their component tests — not a stop. Screenshots to
   `C:\dev\masaha\workspace\WORKER_A\OWNER_SETUP\shots\pr1\` (moved there if saved elsewhere).
7. **Finding numbers start at 99:** 98 is reserved for worker B's DESK PR 2 (open in parallel); the plan's
   `<n>` is the first free number from 99 on the latest index.
8. If you are Claude Code, the project's skills may help (the plan's appendix is only a map). Write nothing
   outside the repository except this folder's `4_REPORT_PR1.md` and `shots\`.

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

**A plan that proves false against the code:** stop too, say exactly what and why, and offer the fix — do
not choose it yourself. **A break that stays green:** stop — unless it is plainly your own test's defect, or
the plan's break cannot change the outcome (as a bound already excluded by another); then make the break
that can, see it red, and state it as a departure.

**Never claim a result you did not see:** a command passed only if you saw its own output say so; copy that
line (read it by its exit code). A break counts only when you saw it red.

## 3. Limits, and not losing work

- Write `4_REPORT_PR1.md` **as you go**: after the first checks, after each commit (sha, subject with its
  length, the red line before the code, the green line after), after each break, after the real run, after
  the push. If you stop for any reason, the report already says where the work stands.
- **One full test run at a time on this machine:** before each full lane, check no `vitest` runs under
  `C:\dev\masaha\app-b\`; if one does, wait. Focused runs of one or two files are fine.
- Each full lane **once, on the head**; re-run only if a file it covers changed after it passed.
- Record the routes test's time (finding 87), as §13 says; a timeout stops (never raise a limit).

## 4. Discipline

Stage by path (never `-A` or `.`); each commit message written to a UTF-8 file **without a BOM, LF line
endings**, with a body saying why, and `git commit -F <file>`; subjects counted ≤ 50; **no tool
attribution**; a fix before the push folds into its commit (`--fixup` + `GIT_SEQUENCE_EDITOR=:`
autosquash); never print a secret or a password; never merge, create an Issue, or comment on another PR.
`git status --short` clean at the end; stop both servers by process id; ports 3320 and 5320 free.

## 5. Your final reply — this shape, finished or stopped

```
Status: DONE | STOPPED
PR: #<n> <url> · head <sha> · CI <green/red/pending> · <CLEAN/not CLEAN>   (or "no PR")
Commits: <sha> <subject> (<chars>) — one line each
Ran and passed: <each command, with the result line you saw>
Ran and failed: <each, what failed, what you did>   (or "none")
COULD NOT RUN: <each test, lane, break or real-run case not run, the exact command, the exact error,
               why>   (or "none" — only if every planned run happened)
Breaks: <each: red seen / NOT red (why)>
Real run: <each case and its screenshot, or NOT RUN (why)>
Departures from the plan: <each, with its reason>   (or "none")
Stopped at (if STOPPED): <the step, and what the owner must decide or fix>
Report: C:\dev\masaha\workspace\WORKER_A\OWNER_SETUP\4_REPORT_PR1.md
```
