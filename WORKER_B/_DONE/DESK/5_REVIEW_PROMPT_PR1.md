# Review — DESK PR 1 (`feat/live-status`), an independent reviewer, in two halves

You are the **independent reviewer** of worker B's DESK PR 1 in Basel-Ghonaim/masaha: presence and the
live status on the API — `occupancy`'s one definition of *present*, the pure live-status rule, the staff's
occupancy read, the manual override, the directory's live status. Claude Code executed it in another
conversation; you start fresh and trust nothing you have not seen in the code. Find the PR: `gh pr list
--head feat/live-status --json number,headRefOid,mergeStateStatus`. Write the report to
`C:\dev\masaha\workspace\WORKER_B\DESK\6_REVIEW_PR1_CLAUDE_CODE.md`: first the verdict and the five most
important findings, then the rest.

## How — two subagents in parallel, then you merge
**Run two subagents at once**, each with these Rules and its own half, each returning its findings in the
output's shape; then **verify every blocker and should-fix yourself in the code** before it enters the
report, merge the two lists, and drop duplicates.
- **Half 1 — the staff's side (C1–C3):** Gaza time (`gazaTime.ts`, the DST transitions, the owner-approved
  change to R3 allowing `@date-fns/tz` in shared core — only that package); the one definition of present
  (open visits plus open check-ins) and the live-status rule (ADR 0008; every branch); `GET …/occupancy`
  (who may read it, its whole answer); the override (`PUT`/`DELETE …/status-override`: who may, under the
  space's lock with `can()` again, refused while the space is not open, **ending at today's closing at the
  latest**, its durations, the clock); audit; the new modules' reads and their levels (R1, R5).
- **Half 2 — the public side (C4) and the documents:** the directory's `liveStatus` on cards and pins, the
  `availableNow` filter applied **before** the page is cut, `GET /spaces/:slug/occupancy` → `{ status }`
  only — **never a count or a person on any public answer** (ADR 0002, 0008); not listed or unverified → 404;
  public caching; the contract, `occupancy.md`, `directory.md`, the data model, conventions, the build map,
  `overview.md` true to the code, one home per fact.

## Rules
- **Run from `C:\dev\masaha\app-design`, read only commit objects:** `git fetch origin` and
  `git fetch origin pull/<n>/head`; base = `origin/main`; `git diff origin/main...<head>`, `git show
  <commit>`, `git show <head>:<file>`. No edits, checkouts, installs, npm or test runs, servers, database
  commands, no GitHub comments. Confirm `gh pr checks <n>` is green first; if a lane is red or pending, say
  so and stop. At the end, check the head has not moved.
- Report **concrete problems only**, each verified in the code: file and line, the failing scenario,
  severity (**blocker / should-fix / nit**), the fix. "Plausible" when unsure, with why. **Say what you saw
  in the code and what you only read in the executor's report.** Think like an attacker on every route. No
  praise, no tool attribution, no project skill.

## What the PR must be
The plan `C:\dev\masaha\workspace\WORKER_B\DESK\2_PLAN.md` — the owner's approval note at its top binds —
PR 1 only; the execution prompt `3_EXEC_PROMPT_PR1.md`; the report `4_REPORT_PR1.md`: judge every departure
(the R3 change among them) and every break that did not go red. Scope: `apps/api`, `packages/shared`,
`docs`, the two errors catalogues and the lockfile (`@date-fns/tz` only). The tests: each would fail with
its planned break. Commit subjects (≤ 50) and bodies.

## Your output
One file: the head; a one-line verdict; the findings, most severe first, each with **where its fix
belongs** (a fix round on this PR / PR 2 or 3 / a finding to record); a short "Checked and fine" list; then
stop.
