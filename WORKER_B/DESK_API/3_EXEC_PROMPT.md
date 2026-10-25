# DESK_API — the three API needs of the desk's screens, on the API (`feat/desk-api`) — plan briefly, then build

You are worker B's **executor** of one pull request, in a fresh conversation, in **two phases**: first a short
plan, then **stop**; the supervisor reviews it and writes the approval at its top; then you build it whole —
the carried fixes, the migration, the code, the tests, the breaks, the real run, the PR, CI. **What to build is
decided** (three specs, approved by the owner on 2026-10-24); do not re-decide it. Phase 1 decides only *how*,
in the code, and names what the specs leave open.

## 0. What to read — and only this (the owner's instruction)

The owner's instruction overrides the bootstrap's session checklist for this task, stated here: **do not run
the `start-work-item` skill** and do not read `docs/development/workflow.md` whole. `CLAUDE.md` is already in
your context. Read only:

1. `C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\2_PLAN.md` — **only:** the owner's approval note at its top
   (its §14.4 line: **the month is 30 days and the week 7, the first day counted**; §14.5: this item); §6's
   **Spec B** (the statement and the file from one snapshot, finding 124), **Spec C** (reception's session ends
   after 15 minutes idle) and **Spec D** (subscribe from a published week or month price). Spec A is **not**
   built. These three specs are this PR's contract.
2. `C:\dev\masaha\workspace\WORKER_B\DESK_API\0_CARRIED_FROM_114.md` whole, and in
   `C:\dev\masaha\workspace\WORKER_B\PAYMENTS\6_REVIEW_CLAUDE_CODE.md` only N1–N4.
3. `C:\dev\masaha\workspace\WORKER_B\PAYMENTS\2_PLAN.md` §12 — as the model of the procedure (its commands and
   checks), nothing else of it.
4. In the repository: the code and documents a step touches, when that step needs them — search first
   (`git grep`), then read the section, not the whole file. For spec C at least: `docs/backend/security.md`
   (*Tokens and cookies*, *Authorization*), ADR 0003, `apps/api/src/shared/auth/` (the access token,
   `requireAuth`, the session's refresh), the `RefreshToken` model in `schema.prisma`, `docs/features/auth.md`,
   the auth API tests and the clock port. The `add-error-code` skill applies to `SESSION_IDLE`; `open-pr` may
   help at the end.

## 1. Phase 1 — the plan, then stop

Work in `C:\dev\masaha\app-b` (detached at the latest `origin/main`, clean — `b7fe343e` or later). Read only;
no branch, no edit. Write `C:\dev\masaha\workspace\WORKER_B\DESK_API\2_PLAN.md` (two to four pages):

- **The commits, in order, subjects counted (≤ 50):** the four carried items first (`0_CARRIED_FROM_114.md`
  1–4: documents; the check-ins range aligned with its test red first; the conventions line; the cosmetics),
  then spec B, spec C, spec D — one commit each unless a spec needs two; the PR's title (spec C's subject).
- **Spec B:** the functions wrapped, how `tx` reaches each read, the test's interleaving with
  `apps/api/test/locks.ts` and its break (`ReadCommitted`).
- **Spec C — the hardest; be exact:** where `lastActivityAt` lives (the family: which row, how a rotation copies
  it), the migration's SQL (the column, its default for existing rows, no PR number in its comments — carried
  item 3); how the access token gains `sid` and what an old token without it does; where in `requireAuth` the
  check runs (after which existing check), how "idle-bound" is decided **from the links the request already
  reads** (no extra query per request if one can be avoided — say the cost), how a route is marked passive and
  which routes are; the refresh's check; the 60-second write throttle; `SESSION_IDLE` (status, both catalogue
  lines as the spec gives them); each test and each break the spec lists, with the clock port.
- **Spec D:** the schema change to `subscribeSchema` (exactly one of `packageId`, `priceId`, `custom`), the terms
  copied from the price, the 6 / 29 days added to `startsOn`, who may use it, its tests.
- **What the specs leave open**, each with your recommendation (for example: an owner who is reception
  elsewhere; a session that predates the column; what the web does today on a 401 it does not know).
- **Files** (≈ 30 expected), the migration's name, the documents per commit (the specs list them), finding
  numbers (**170** and on, none planned), the real-run cases on 3321 with the demo data, and the stop rules
  you will follow (§3 below).

Then **stop** and reply only: `PLAN READY: C:\dev\masaha\workspace\WORKER_B\DESK_API\2_PLAN.md` with the commit
count and the open points. Do not edit the repository before the approval note is at the plan's top.

## 2. Phase 2 — after the approval note

1. **§12.1 of the PAYMENTS plan, adapted:** `git fetch`; the base diff from the sha your plan names; open PRs
   (`gh pr list --state open`) — worker A's `feat/desk-visits` (web only: `apps/web`, `docs`) may be open; a
   shared code file → **stop and ask**; shared documents → re-read on the merged tree before editing, each side
   keeps its own lines.
2. The branch `feat/desk-api` from the latest `origin/main` (`--no-track`); `npm run build -w @masaha/shared`;
   the commits in your plan's order (per commit `npm run lint`, `npm run typecheck`, and the test files it
   touches; each test **red before its code**, green after); **the migration** by `migrate dev --create-only`
   **once**, then `ls` the folder; non-interactive or refused → `migrate diff --script`; read the SQL before
   applying; both B databases migrated; **never** a `#PRNUM` or PR number inside the migration.
3. **On the head, once:** `npm run lint`, `npm run typecheck`, `npm run test:unit`, `npm run test:api` (**run it
   with no command timeout** — it takes ≈ 10 minutes; PAYMENTS' executor mistook its own 600 s timeout for a
   memory kill), `npm run format:check`, `npm run check:links`, `npm run check:conflicts`, and the plan's `git`
   checks. **Not run locally — CI judges:** `test:component`, the web build, `check:build`, `check:classes`.
4. **Every break** your plan lists, each red recorded, restored from a backup copy (never `git checkout` a file
   with uncommitted work).
5. **The real run** on 3321 (`masaha_b_dev`, the demo data; a self-judging script `PASS|FAIL`, `ALL PASS`): a
   statement and a file read; reception idle past 15 minutes **only with the clock** — the real 15 minutes is
   not waited (say so); reception subscribing a customer from the demo space's published month price; the
   owner's session never idle-ended. **A demo account or data that does not hold a case → stop and report;
   never change data through the app to get past it** (no reset or reseed of `masaha_b_dev` without the owner's
   word, asked first).
6. `#PRNUM` replaced in each commit's tree just before the push (copy
   `WORKER_B\SUBSCRIPTIONS\scripts\prnum-fix109.sh` into this folder's `scripts\`, adapt its branch to
   `feat/desk-api` and its expected number to the next free one, checked with `gh pr list --state all --limit
   1`, keep its checks); push; `gh pr create --assignee @me --label feat --label area:api --label area:docs
   --label area:web` (the catalogues gain `SESSION_IDLE`); the description names "Carried from #114" and the
   three specs; CI green and `CLEAN`; the conflict check.
7. **Size:** ≈ 30 files expected; **stop and ask past 45**.

## 3. A test you cannot run stops the work

A test **failing** because its code is not written yet is the red step — normal. A test, lane or command you
**cannot run** is not: it errors before any test runs (the database unreachable, Docker down, a port taken, a
module or `dist` missing, a migration pending, `No test files found`, a Vitest or TypeScript startup error, a
crash with no result); a break you could not make or run; a real-run case you could not perform. **Then stop at
once** — never skip, `.skip` or delete a test, never change a config, a timeout, `.env`, a script or a lane,
never mock what the plan does not, never run a narrower command and call it the lane, never call it "flaky".
Write the command, its exact error and where you were into the report, and reply with §6's shape, `Status:
STOPPED`.

**The owner's standing exception — memory:** a full lane **killed for low memory** (not your own timeout) is
re-run **once** when the machine is quieter (no `vitest` of `C:\dev\masaha\app\` running — worker A runs its
web lanes in parallel — the free memory recorded); killed again → record it, carry on, and **CI's run of that
lane on the pushed head is the judge** — red there → stop.

**A spec that proves false against the code:** stop, say exactly what and why, and offer the fix — do not
choose it yourself. **A break that stays green:** stop — unless it is plainly your own test's defect, or the
break cannot change the outcome; then make the break that can, see it red, and state it as a departure.
**Anything you would leave undone: stop and ask** — never silently. **Never claim a result you did not see:**
copy the line that says it, read by its exit code.

## 4. Not losing work

Write `C:\dev\masaha\workspace\WORKER_B\DESK_API\4_REPORT.md` **as you go** (after the first checks, each
commit with its sha, subject length, red and green lines, each break, the real run, the push). Long outputs in
`scripts\`, read by exit code. Scripts never committed. Docker: `docker start masaha-postgres-1` (never
`db:up`, never `npm ci`; Docker Desktop not running → stop and ask the owner).

## 5. Discipline

Stage by path (never `-A` or `.`); each commit message a UTF-8 file **without a BOM, LF endings**, with a body
saying why, `git commit -F <file>`; subjects ≤ 50, your count decides; **no tool attribution**; **no `fixup!`,
`style:` or `wip` commit left in the pushed branch**, and **no rebase left in progress** at the end; never
print a secret, a token or a demo phone number; never merge, create an Issue, or comment on another PR. `git
status --short` clean at the end; the API stopped by process id; port 3321 free; say the name of the local
`backup/*` branch the script leaves.

## 6. Your final reply — this shape, finished or stopped

```
Status: PLAN READY | DONE | STOPPED
PR: #<n> <url> · head <sha> · CI <green/red/pending> · <CLEAN/not CLEAN> · files <count>   (or "no PR")
Commits: <sha> <subject> (<chars>) — one line each, the carried ones first
Carried from #114: <each of items 1–4: done in <sha>, red then green / docs>
Migration: <name> · applied to masaha_b_dev and masaha_b_test · migrate status <line>
New error codes: <SESSION_IDLE with its Arabic and English lines>
Ran and passed: <each command, with the result line you saw>
Ran and failed: <each, what failed, what you did>   (or "none")
Not run locally (CI judges): <each lane, and CI's result on the head once seen>
COULD NOT RUN: <each, the exact command, the exact error, why>   (or "none")
Breaks: <each: red seen / NOT red (why)>
Real run: <each case and its answer> · data changed: <what>
Open PRs and merge order: <each open PR, shared files, which merges first>
Departures from the plan: <each, with its reason>   (or "none")
Stopped at (if STOPPED): <the step, and what the owner must decide or fix>
Report: C:\dev\masaha\workspace\WORKER_B\DESK_API\4_REPORT.md
```
