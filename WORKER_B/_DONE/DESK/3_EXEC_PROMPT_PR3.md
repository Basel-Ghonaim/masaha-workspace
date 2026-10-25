# DESK — execute PR 3 only (`feat/auto-checkout`)

You are the **executor** of the third of DESK's pull requests, in a fresh conversation. You did not plan it
and you will not review it. **The plan is approved; do not re-decide anything in it.**

## 1. Read, then begin

1. **Precondition:** PR 2 (#95, `feat/desk-visits`) is merged — `gh pr view 95 --json state` → `MERGED`
   (merged at `f77d2012`, 2026-10-20); if not, stop.
2. Work in `C:\dev\masaha\app-b` only — never in `C:\dev\masaha\app` (worker A builds OWNER_SETUP there) or
   `C:\dev\masaha\app-design`. Read `CLAUDE.md` at the repository's root.
3. Read the plan **whole**: `C:\dev\masaha\workspace\WORKER_B\DESK\2_PLAN.md` — **the owner's approval note
   at its top binds**. **A1 was taken:** the unpriced close (`VISIT_NOT_PRICED`, Q4's branch, T14–T17) was
   built in PR 2 — PR 3's C3 keeps only what PR 2 did not build (the reads and the pricing A1 names); read
   what #95 holds before writing C3, and if C3's remainder is unclear, stop and ask. PR 4 (collecting and
   writing off) and finding 17's sweep come later, each from its own prompt.
4. **Carried from #95 — this PR's first commit, before the plan's C1:** read
   `C:\dev\masaha\workspace\WORKER_B\DESK\0_CARRIED_FROM_95.md` whole and build it as it says — items 1–4
   (the check-out before its check-in refused with 422; `security.md`; `visits.md`; the review's small nits),
   **item 5 taken by the owner** (a check-out that lost the race and carries a payment refused with 409, its
   Arabic line listed in the PR's description for the owner's approval), item 6 recorded as **finding 100**
   (reserved for you). Each red first, then green, with its break. The PR's description says "Carried from
   #95". Read the review `6_REVIEW_PR2_CLAUDE_CODE.md` for the details.
5. **Then build PR 3 only** — the scheduler and the auto check-out: §4's *The code, PR by PR* for PR 3,
   *Decisions taken for PR 3*, §9 *PR 3*, §11 *PR 3* (C1–C4, as amended by A1), §12 for PR 3, Appendix A
   *PR 3*. Nothing of PR 4.
6. Follow §12 in order for PR 3: 12.1 (the base diff from `eff0a3d1`: PR 1's and PR 2's files must match what
   the plan says they hold — read A1's move into account; #93 and worker A's merged changes are web and docs);
   the branch `feat/auto-checkout` from the latest `origin/main` (`--no-track`); `npm run build -w
   @masaha/shared`; 12.2's first checks for PR 3; the commits (12.3, per commit `lint` and `typecheck`);
   `JOBS_SECRET` set in `apps/api/.env` as 12.6 says (a random value, **never printed**); the head's
   verification (12.4); **every break of 12.5 for PR 3 made and seen red**; the real run on 3321 (12.6);
   `#PRNUM`; push; the PR (12.7); CI green and `CLEAN`; the conflict check (12.8: worker A's OWNER_SETUP PR 1
   may be open — shared documents only); the description (12.9); `_SHARED\OPEN_DECISIONS.md` as 12.8 says.
   Stop at §14's points.
7. `masaha_b_dev` / `masaha_b_test`, already migrated to `main`; `docker start masaha-postgres-1` (never
   `db:up`). No new dependency; no migration in this PR (if one seems needed, stop and ask).
8. If you are Claude Code, the project's skills may help (the plan's Appendix B is only a map). Write
   nothing outside the repository except this folder's `4_REPORT_PR3.md`.

## 2. A test you cannot run stops the work

A test **failing** because its code is not written yet is the plan's red step — normal. A test, lane or
command you **cannot run** is not: it errors before any test runs (the database unreachable, Docker down, a
port taken, a module or `dist` missing, a migration pending, `No test files found`, a Vitest or TypeScript
startup error, the whole run timing out, a crash with no result); a break you could not make or run; a
real-run case you could not perform. **Then stop at once** — never skip, `.skip` or delete a test, never
change a config, a timeout, `.env` (but `JOBS_SECRET` as 12.6 says), a script or a lane, never mock what the
plan does not, never run a narrower command and call it the lane, never call it "flaky" and move on. Write
the command, its exact error and where you were into the report, and reply with §5's shape,
`Status: STOPPED`.

**A plan that proves false against the code:** stop too, say exactly what and why, and offer the fix — do
not choose it yourself. **A break that stays green:** stop — unless it is plainly your own test's defect, or
the plan's break cannot change the outcome (a bound already excluded by another rule); then make the break
that can, see it red, and state it as a departure.

**Never claim a result you did not see:** a command passed only if you saw its own output say so; copy that
line (read it by its exit code, not the tail). A break counts only when you saw it red.

## 3. Limits, memory, and not losing work

- Write `4_REPORT_PR3.md` **as you go**: after the first checks, after each commit (sha, subject with its
  length, the red line before the code, the green line after), after each break, after the real run, after
  the push. If you stop for any reason, the report already says where the work stands.
- **Memory:** the machine is shared and has run low. Before each full lane: no `vitest`, `tsc` or dev server
  of `C:\dev\masaha\app\` runs (worker A's — never stop its processes; wait), and the free memory written
  into the report. One full lane at a time. A lane killed for memory: stop at once, no retry.
- Each full lane **once, on the head**; re-run only if a file it covers changed after it passed.
- Keep the scripts you write for breaks and the real run in this task folder's `scripts\` (not a session
  scratchpad), so a resume can use them; never commit them.

## 4. Discipline

Stage by path (never `-A` or `.`); each commit message written to a UTF-8 file **without a BOM, LF line
endings**, with a body saying why, and `git commit -F <file>`; subjects counted ≤ 50; **no tool
attribution**; a fix before the push folds into its commit (`--fixup` + `GIT_SEQUENCE_EDITOR=:`
autosquash); never print a secret; never merge, create an Issue, or comment on another PR. `git status
--short` clean at the end; stop the API by process id; port 3321 free.

## 5. Your final reply — this shape, finished or stopped

```
Status: DONE | STOPPED
PR: #<n> <url> · head <sha> · CI <green/red/pending> · <CLEAN/not CLEAN>   (or "no PR")
Commits: <sha> <subject> (<chars>) — one line each, the carried one first
Carried from #95: <each of items 1–6: done, its test and break red seen / not done (why)>
New error codes: <each, with its Arabic and English lines>   (or "none")
Ran and passed: <each command, with the result line you saw>
Ran and failed: <each, what failed, what you did>   (or "none")
COULD NOT RUN: <each test, lane, break or real-run case not run, the exact command, the exact error,
               why>   (or "none" — only if every planned run happened)
Breaks: <each: red seen / NOT red (why)>
First checks: <each of §12.2 for PR 3, ✔ or what it found>
Real run: <each case and its answer, or NOT RUN (why)>
Departures from the plan: <each, with its reason>   (or "none")
Stopped at (if STOPPED): <the step, and what the owner must decide or fix>
Report: C:\dev\masaha\workspace\WORKER_B\DESK\4_REPORT_PR3.md
```
