# DESK_SCREENS — execute PR 1a only (`feat/desk-visits`, the desk's visits)

You are the **executor**, in a fresh conversation. You did not plan this item and you will not review it.
**The plan is approved; do not re-decide anything in it.**

**PR 1a** is the plan's PR 1 **commits 1–4** (A1 taken): one idempotency key per intent; the page's bottom
action bar; the desk's present list and the live status's control; a visitor's check-in and check-out with the
money block, a typed price with its reason, an unpriced close, the unpaid rest left to a phone; «تبديل الموظف».
**Not here — PR 1b, another prompt:** commits 5–6 (the uncollected visits — collect, «تسجيل دين», the write-off
and its undo — and the unpriced visits' pricing) and their tests.

## 0. What to read — and only this (the owner's instruction)

The owner's instruction overrides the bootstrap's session checklist for this task, stated here: **do not run
the `start-work-item` skill** and do not read `docs/development/workflow.md` whole. `CLAUDE.md` is already in
your context. Read only:

1. `C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\2_PLAN.md` — **these parts only:** the owner's approval note at
   its top (binding, it wins where the plan differs — **above all its first point: PR 1a starts now, without
   the public fix PR**); the header; §1; §2 *Scope*, *Acceptance criteria* and *Out of scope* for PR 1; §3's
   *What the reading changed*; §4; §5 (S1–S13) and *Proposed alternatives* as they touch PR 1; §7; §8 *PR 1 —
   the desk's visits* (the design issues it names for commits 1–4); §9 *PR 1*'s files of commits 1–4 and
   *Shared with the other open items*; §10's opening and *PR 1 · Commits 1–4*; §11 *PR 1* — **the tests of
   commits 1–4** (by §10's per-commit lists; the uncollected, collect, debt, write-off and unpriced tests are
   1b's) and *Review Focus*; §12's PR 1a lines; §13 whole (first checks, per commit, on the head, the real run's
   **PR 1a** writes, push and the PR, the stop rule, *Stop and ask*).
2. In the repository: the code and documents a step touches, when that step needs them — search first
   (`git grep`), then read the section, not the whole file. The `open-pr` skill may help at the end; no other
   skill is needed.

Read each file once. If a step proves to need a document not named here, read the part it needs and say so in
the report.

## 1. Then begin

1. **Preconditions:** `C:\dev\masaha\app` on `main`, clean, `git pull --ff-only` done; `npm run build -w
   @masaha/shared`. **§13's first check 2 for PR 1(a) is replaced by the approval note:** nothing must have
   merged first. No `0_CARRIED_FROM_*.md` in this folder: nothing is carried into this PR.
2. Work in `C:\dev\masaha\app` only — never in `C:\dev\masaha\app-b` (worker B executes PAYMENTS there: API,
   `packages/shared/src/payments`, docs) or `C:\dev\masaha\app-design`.
3. **§13's first checks 1, 3, 4 and 5 (a–m)**, each with its fallback; a "stop" there stops you. **Open PRs:**
   worker B's `feat/payments` may be open. It changes `packages/shared/src/payments` (new exports) and the web's
   two `errors.ts` lines of `VISIT_WRITTEN_OFF`; this PR reads `@masaha/shared/payments` and may add catalogue
   lines beside those: **a shared code file is a stop-and-ask** (§13 check 4) — if only the catalogues'
   `errors.ts` overlap, say so and carry on (text conflicts only; whichever merges second rebases).
4. **Then the plan's PR 1 commits 1–4**, following §13: the branch `feat/desk-visits` from the latest
   `origin/main` (`--no-track`); per commit `lint` and `typecheck`, and the test files the commit touches; each
   test red before its code, green after; the head's checks; the breaks; the real run (**PR 1a's writes only**,
   as §13 lists them); `#PRNUM`; push; the PR, titled as §12 says (commit 4's subject,
   **`feat(desk): check visitors in and out at the desk`**), `--label feat --label area:web --label area:docs`
   (and `area:design-system` only if a layer file changes — check 5d's fallback would); CI green and `CLEAN`; the
   conflict check against any open PR. Stop at the plan's *Stop and ask*.
5. **Size:** the plan says ≈ 58 files; **stop and ask only past 72 files**.
6. **Finding numbers:** 160–164 are the plan's (PR 1 writes those §2 names); a new one takes the next free
   number of **160** and on, said in the report.
7. `docker start masaha-postgres-1` (never `db:up`; never `npm ci`; if Docker Desktop is not running, stop and
   ask the owner to start it); in `apps/api` `npx prisma migrate status` → up to date (pending → stop and ask);
   API on 3320, web on 5320, worker A's `masaha_dev`.
8. **The demo data:** run §13's data inventory first (read-only `GET`s, a script in `scripts\`). **Write only
   PR 1a's listed writes** (the test visitors, the override, the closure and FULL check-ins as §13 names them,
   their phones). A case the data does not hold → **not performed, by design** only where §13 allows it (FULL as
   reception), with the test that proves it; any other → stop and report. **Never change data through the app,
   the API, the database or the seed to get past a case.**
9. **The real run** with real screenshots (local headless Chrome over CDP, as
   `C:\dev\masaha\workspace\WORKER_A\PUBLIC\scripts\run2b.mjs` does; **send Enter with its text** — `text: '\r'`
   — or a native button never activates): §13's cases for PR 1a, as the owner and as reception, Arabic light and
   English dark at 390, 768 and 1440 for the layouts that change with width; **the network log proving one key
   across an offline first send and «إعادة المحاولة»**; the width break; the touch targets at 390. Screenshots to
   `C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\shots\pr1a\` — never inside the repository.
10. Write nothing outside the repository except this folder's `4_REPORT_PR1A.md`, `shots\` and `scripts\`.

## 2. A test you cannot run stops the work

A test **failing** because its code is not written yet is the plan's red step — normal. A test, lane or
command you **cannot run** is not: it errors before any test runs (the database unreachable, Docker down, a
port taken, a module or `dist` missing, a migration pending, `No test files found`, a Vitest or TypeScript
startup error, the whole run timing out, a crash with no result); a break you could not make or run; a
real-run case you could not perform (other than those §1.8 allows). **Then stop at once** — never skip,
`.skip` or delete a test, never change a config, a timeout, `.env`, a script or a lane, never mock what the plan
does not, never run a narrower command and call it the lane, never call it "flaky" and move on. Write the
command, its exact error and where you were into the report, and reply with §6's shape, `Status: STOPPED`.

**The owner's standing exceptions:**
- `routes.component.test.tsx` › "lists the owner's eleven pages" (finding 87), and the two site tests that open
  `/spaces` first, may miss their 3 s locally when the machine is loaded. If **only those** fail and each passes
  alone, record both runs (times, free memory) and go on; **CI's `test:component` is the judge** — if it fails
  there, stop.
- A run **killed for low memory** is re-run **once** when the machine is quieter (no `vitest` of
  `C:\dev\masaha\app-b\` running — worker B runs its API lane in parallel — the free memory recorded); killed
  again → record it, carry on, and CI's run of that lane on the pushed head is the judge — red there → stop.

**A plan that proves false against the code:** stop too, say exactly what and why, and offer the fix — do
not choose it yourself. **A break that stays green:** stop — unless it is plainly your own test's defect, or
the plan's break cannot change the outcome; then make the break that can, see it red, and state it as a
departure. **A design issue or a review point you would leave undone: stop and ask** — never silently.

**Never claim a result you did not see:** a command passed only if you saw its own output say so; copy that
line (read it by its exit code). A break counts only when you saw it red. A scoped lane with failures is not
green: name each failing file and test.

## 3. What runs where (the owner's rule: no run that only repeats another)

1. **A test seen red before its code is its own break.** Record that red line once. Make a **separate** break
   only where the plan's break targets a guard the red step did not prove (§11's breaks marked [key], [role],
   [money], [state], [warn], the width and the accessibility ones) and record its red output.
2. **Locally, on the head:** `npm run test:unit -w @masaha/web` · `npm run test:component -w @masaha/web --
   src/shared/api src/features/occupancy src/features/desk src/pages/dashboard src/shared/copy` (the folders
   this PR touches; add any other whose files it changes, and say so) · `$env:NODE_ENV='production'; npm run
   build; Remove-Item Env:NODE_ENV` · `npm run check:build` · `npm run check:classes` · `npm run format:check` ·
   `npm run check:links` · `npm run check:conflicts` (if it is on `main` by then). Before each test run: no
   `vitest` of `C:\dev\masaha\app-b\` running, the free memory recorded.
3. **Not run locally — CI's run on the pushed head is the judge:** the full `test:component` lane, `test:unit`
   of `apps/api` and `packages/shared`, and `test:api` (no API change). Report them under "Not run locally (CI
   judges)", not under COULD NOT RUN. A red CI lane → fix it, fold the fix, push again.
4. **A fix after a lane passed** re-runs only the test files it touches, plus `typecheck` and `lint`; say so.

## 4. Limits and not losing work

- Write `4_REPORT_PR1A.md` **as you go**: after the first checks, after each commit (sha, subject with its
  length, the red line before the code, the green line after), after each break, after the real run, after
  the push. If you stop for any reason, the report already says where the work stands.
- Keep a long command's output in a file under `scripts\` and read its exit code and the lines you need.
- Keep the scripts you write for the real run in this folder's `scripts\`, never committed.

## 5. Discipline

Stage by path (never `-A` or `.`); each commit message written to a UTF-8 file **without a BOM, LF line
endings**, with a body saying why, and `git commit -F <file>`; subjects counted ≤ 50 (your count decides); **no
tool attribution**; **no `fixup!`, `style:` or `wip` commit left in the pushed branch** — a fix before the push
folds into its commit (`--fixup` + `GIT_SEQUENCE_EDITOR=:` autosquash), and a fix after a push too, then
`--force-with-lease`; `#PRNUM` replaced in each commit's tree just before the push (§13; `C:\dev\masaha\workspace\
WORKER_A\PUBLIC\scripts\prnum3b.sh` the model — copy it into this folder's `scripts\`, adapt its branch to
`feat/desk-visits` and its expected number to the next free one, checked with `gh pr list --state all --limit 1`,
keep its checks), never in the working tree alone; never print a secret or a password; never merge, create an
Issue, or comment on another PR. **No rebase left in progress** (`git status` says none) at the end; `git status
--short` clean; stop both servers by process id; ports 3320 and 5320 free. The local `backup/*` branch the
script leaves: say its name.

## 6. Your final reply — this shape, finished or stopped

```
Status: DONE | STOPPED
PR: #<n> <url> · head <sha> · CI <green/red/pending> · <CLEAN/not CLEAN> · files <count>   (or "no PR")
Commits: <sha> <subject> (<chars>) — one line each
Ran and passed: <each command, with the result line you saw>
Ran and failed: <each, what failed, what you did>   (or "none")
Not run locally (CI judges): <each lane, and CI's result on the head once seen>
COULD NOT RUN: <each test, lane, break or real-run case not run, the exact command, the exact error,
               why>   (or "none" — only if every planned run happened)
Breaks: <each: red seen (in the red step or as its own break) / NOT red (why)>
First checks: <each of §13's checks 1, 3, 4, 5a–m: ✔ or what it found and the fallback taken>
Real run: <each case and its screenshot, or NOT PERFORMED (by design) with the test that proves it>
Network log: <the offline-then-retry case: the two requests, their one key, the one visit>
Data left in masaha_dev: <each write the run made>
Open PRs and merge order: <each open PR, shared files, which merges first>
Departures from the plan: <each, with its reason>   (or "none")
Stopped at (if STOPPED): <the step, and what the owner must decide or fix>
Report: C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\4_REPORT_PR1A.md
```
