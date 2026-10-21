# PUBLIC — execute PR 1a only (`feat/directory-list`, the Directory's list)

You are the **executor**, in a fresh conversation. You did not plan this item and you will not review it.
**The plan is approved; do not re-decide anything in it.** You build **PR 1a only**, the first of five.

## 1. Read, then begin

1. **Precondition:** OWNER_SETUP PR 3 (#99, `feat/owner-staff-settings`) is merged — `gh pr view 99 --json
   state` → `MERGED` (at `2c4d78f9`, 2026-10-21); if not, stop.
2. Work in `C:\dev\masaha\app` only — never in `C:\dev\masaha\app-b` (worker B) or `C:\dev\masaha\app-design`
   (reviews read there). Read `CLAUDE.md` at the repository's root.
3. Read the plan **whole**: `C:\dev\masaha\workspace\WORKER_A\PUBLIC\2_PLAN.md` — **the owner's approval note at
   its top binds and wins where the plan differs**: **A13 taken — this PR is the plan's PR 1 commits 1–5 only**
   (share the list's pages; share the name and clock rules; the skip link and focus; the public areas; the list
   page by page), ≈ 63 files, titled with commit 5's subject. Commits 6–7 (the filters and near me) are **PR
   1b's — not here**; PR 1's tests, acceptance criteria and real-run cases split the same way (say in the
   report which you took and why, where the plan does not say).
4. **Carried items:** if a `0_CARRIED_FROM_99.md` exists in `C:\dev\masaha\workspace\WORKER_A\PUBLIC\` or
   `…\OWNER_SETUP\` when you start, its items are this PR's first commit. As of 2026-10-21 there is none: #99's
   review items were fixed in its own fix round.
5. **The platform's contact (approval note, decision 4)** belongs to PR 4; nothing of it here.
6. Follow the plan's §13 for this PR: the first checks against the merged `origin/main` (`git diff
   --name-status cf3190a4 origin/main`: #99's and worker B's #100 changes are merged since the plan — a code file
   this PR names changed in a way the plan does not cover → stop and ask; the plan's checks a–… for PR 1, each
   with its fallback); the branch `feat/directory-list` from the latest `origin/main` (`--no-track`); per commit
   `lint` and `typecheck`; on the head each lane once; the real run; `#PRNUM`; push; the PR (labels as the
   approval note says, `area:design-system` included since S6 changes the layer's barrel); CI green and
   `CLEAN`; the conflict check against any open PR (worker B's SUBSCRIPTIONS PR 1 may be open: shared documents
   only). Stop at the plan's *Stop and ask*.
7. **Finding numbers:** this item's start at **130** (the plan records 130 and 131 where it says); any further
   one takes the next free number in that range.
8. `docker start masaha-postgres-1` (never `db:up`; never `npm ci`; if Docker Desktop is not running, stop and
   ask the owner to start it); in `apps/api` `npx prisma migrate status` — pending → `npx prisma migrate
   deploy`, then `npx prisma generate`; API on 3320, web on 5320, worker A's `masaha_dev`. **The real run** with
   real screenshots (the `playwright` MCP tools if present, else local headless Chrome over CDP; say which),
   Arabic light and English dark at 390, 768 and 1440: PR 1a's cases — the list, its pages, the card (cover or
   mark, the live status), the search, the sort, the skip link and the focus on a page change, the first
   download free of dashboard code and Leaflet. **The demo data:** `masaha_dev` may hold only the demo space —
   the directory demo set is worker B's DEMO_SEED item, due **before PR 1b**. A PR 1a case the data cannot show
   (e.g. a second page) → record it as not performed for lack of data, with the component test that proves it;
   **never add or change data through the app or the database** to get past it. Screenshots to
   `C:\dev\masaha\workspace\WORKER_A\PUBLIC\shots\pr1a\`.
9. If you are Claude Code, the project's skills may help (the plan's appendix is only a map). Write nothing
   outside the repository except this folder's `4_REPORT_PR1A.md`, `shots\` and `scripts\`.

## 2. A test you cannot run stops the work

A test **failing** because its code is not written yet is the plan's red step — normal. A test, lane or
command you **cannot run** is not: it errors before any test runs (the database unreachable, Docker down, a
port taken, a module or `dist` missing, a migration pending, `No test files found`, a Vitest or TypeScript
startup error, the whole run timing out, a crash with no result); a break you could not make or run; a
real-run case you could not perform (other than those §1.8 allows). **Then stop at once** — never skip,
`.skip` or delete a test, never change a config, a timeout, `.env`, a script or a lane, never mock what the
plan does not, never run a narrower command and call it the lane, never call it "flaky" and move on. Write
the command, its exact error and where you were into the report, and reply with §5's shape,
`Status: STOPPED`.

**The owner's standing exceptions:**
- `routes.component.test.tsx` › "lists the owner's eleven pages" (finding 87) may miss its 3 s locally when the
  machine is loaded. If **only that test** fails and it passes alone, record both runs (times, free memory) and
  go on; **CI's `test:component` is the judge** — if it fails there, stop.
- A full lane **killed for low memory** is re-run **once** when the machine is quieter (no `vitest` of
  `C:\dev\masaha\app-b\` running, the free memory recorded); killed again → record it, carry on, and CI's run
  of that lane on the pushed head is the judge — red there → stop.

**A plan that proves false against the code:** stop too, say exactly what and why, and offer the fix — do
not choose it yourself. **A break that stays green:** stop — unless it is plainly your own test's defect, or
the plan's break cannot change the outcome (as a bound already excluded by another); then make the break
that can, see it red, and state it as a departure. **A design issue or a review point you would leave
undone: stop and ask** — never silently.

**Never claim a result you did not see:** a command passed only if you saw its own output say so; copy that
line (read it by its exit code). A break counts only when you saw it red.

## 3. Limits and not losing work

- Write `4_REPORT_PR1A.md` **as you go**: after the first checks, after each commit (sha, subject with its
  length, the red line before the code, the green line after), after each break, after the real run, after
  the push. If you stop for any reason, the report already says where the work stands.
- One full lane at a time; each **once, on the head**; re-run only if a file it covers changed after it passed.
- Keep the scripts you write for the real run in this folder's `scripts\`, never committed.

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
Real run: <each case and its screenshot, or NOT PERFORMED (no data) with the test that proves it>
Data left in masaha_dev: <what the run changed>   (expected: nothing)
Departures from the plan: <each, with its reason>   (or "none")
Stopped at (if STOPPED): <the step, and what the owner must decide or fix>
Report: C:\dev\masaha\workspace\WORKER_A\PUBLIC\4_REPORT_PR1A.md
```
