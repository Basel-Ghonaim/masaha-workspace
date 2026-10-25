# DESK_SCREENS — execute PR 1b only (`feat/desk-uncollected`, the uncollected and the unpriced visits)

You are the **executor**, in a fresh conversation. You did not plan this item and you will not review it.
**The plan is approved; do not re-decide anything in it.**

**PR 1b** is the plan's PR 1 **commits 5–6** (A1 taken): «غير محصّل» — the uncollected visits, collect one
(«تحصيل»), «تسجيل دين» (leave it to a customer by phone), the owner's «لن يُحصَّل…» with its reason and its undo
(«تراجع» in the toast); and «بدون سعر» — the unpriced visits, priced with a reason by whoever may type a price.
PR 1a (#116) built the desk around them; this PR adds these two cards to it.

## 0. What to read — and only this (the owner's instruction)

The owner's instruction overrides the bootstrap's session checklist for this task, stated here: **do not run
the `start-work-item` skill** and do not read `docs/development/workflow.md` whole. `CLAUDE.md` is already in
your context. Read only:

1. `C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\2_PLAN.md` — **these parts only:** the owner's approval note at
   its top (binding); the header; §2 *Scope*, *Acceptance criteria* and *Out of scope* for PR 1 (the uncollected
   and unpriced parts); §4; §5 (S1–S13) as they touch commits 5–6; §7's lines for findings 110, 115 and 164; §8
   *PR 1 — the desk's visits* (the design issues of commits 5–6: DI-3, DI-9, DI-11, DI-19, DI-29 and any other
   it names for them); §9 *PR 1*'s files of commits 5–6; §10's opening and *PR 1 · Commit 5* and *Commit 6*;
   §11 *PR 1* — **tests 31–39 and 41** (and 40, the catalogues' parity, again); §12's PR 1b lines; §13 (first
   checks, per commit, on the head, the real run's **PR 1b** writes, push and the PR, the stop rule, *Stop and
   ask*).
2. `C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\4_REPORT_PR1A.md` — only its *Departures* and *First checks*
   (what PR 1a built that this PR uses: `useDeskWrite`, `deskRefusal`, the money block, the toasts, the page's
   slots).
3. In the repository: the code and documents a step touches, when that step needs them — search first
   (`git grep`), then read the section, not the whole file. The `open-pr` skill may help at the end.

Read each file once. If a step proves to need a document not named here, read the part it needs and say so in
the report.

## 1. Then begin

1. **Preconditions:** `gh pr view 116 --json state` → `MERGED` (if not, stop: PR 1b is cut from `main` once
   1a has merged). `C:\dev\masaha\app` on `main`, clean, `git pull --ff-only` done; `npm run build -w
   @masaha/shared`. No `0_CARRIED_FROM_116.md` in this folder: #116's two reviews (Codex, OpenCode) found nothing
   to fix, so nothing is carried.
2. **Worker A's database first** (merged since its last run; the owner's approval, 2026-10-25):
   ```powershell
   docker start masaha-postgres-1
   cd C:\dev\masaha\app\apps\api
   npx prisma migrate status
   npx prisma migrate deploy        # #114's payment_void_guard is pending here; nothing else is expected
   npx prisma generate
   npx prisma migrate status        # must say: Database schema is up to date!
   cd C:\dev\masaha\app
   $env:SEED_DEMO='true'; npm run db:seed; Remove-Item Env:SEED_DEMO
   ```
   A migration other than `payment_void_guard` pending → stop and ask. The seed renews the directory set's
   day-bound states (#115) and adds nothing to the demo space; record its output.
3. Work in `C:\dev\masaha\app` only — never in `C:\dev\masaha\app-b` (worker B executes DESK_API there: API,
   `packages/shared`, docs, the web's two `errors.ts`), `C:\dev\masaha\app-design` or `C:\dev\masaha\app-review`
   (the owner's test environment).
4. **§13's first checks 1, 3, 4 and 5** (those that touch commits 5–6), each with its fallback. **The base
   diff** is from PR 1a's head `30c48633` to `origin/main`. **Two merged changes the plan predates — check them
   and say what you found:**
   - **#114 widened the uncollected visits:** besides the auto check-out's unpaid visits, the list now holds a
     **priced visit closed by hand with no customer that owes again after its payment was voided**
     (`api-contract.md` › `GET …/uncollected-visits`). The plan's §3 says "the uncollected list holds the auto
     check-out's visits only". **The web lists what the server answers and never filters by checkout method**;
     such a row has no customer, so «تحصيل» with a remainder asks a phone and «تسجيل دين» applies, as for an
     auto-closed one. If the plan's code or tests assume `AUTO` only (a filter, a test fixture, a line), adapt
     them to the contract and state it as a departure; if a design issue's words would be false, **stop and
     ask**.
   - **#114 reworded `VISIT_WRITTEN_OFF`'s two catalogue lines** (they now cover a void too); reuse them as
     they are.
   **Open PRs:** worker B's `feat/desk-api` may be open (API, `packages/shared`, docs, the web's `errors.ts` —
   it adds `SESSION_IDLE`): a shared code file other than the catalogues' `errors.ts` → **stop and ask**; only
   `errors.ts` → text conflicts, whichever merges second rebases; say so.
5. **Then the plan's PR 1 commits 5–6**, following §13: the branch `feat/desk-uncollected` from the latest
   `origin/main` (`--no-track`); per commit `lint` and `typecheck`, and the test files the commit touches; each
   test red before its code, green after; the head's checks; the breaks; the real run (**PR 1b's writes only**,
   as §13 lists them); `#PRNUM`; push; the PR, titled as §12 says (commit 5's subject,
   **`feat(desk): collect the uncollected visits`**), `--label feat --label area:web --label area:docs`; CI green
   and `CLEAN`; the conflict check against any open PR. Stop at the plan's *Stop and ask*.
6. **Size:** the plan says ≈ 32 files; **stop and ask only past 45 files**.
7. **Finding numbers:** 164 is the plan's (PR 1b writes it — a written-off visit is listed nowhere); a new one
   takes the next free number from **165** on, said in the report (check the findings index on `main` first).
8. **The demo data:** run §13's data inventory first (read-only `GET`s, a script in `scripts\`). **Write only PR
   1b's listed writes:** as the owner, on the uncollected visit «خالد», «لن يُحصَّل…» with a reason, then
   «تراجع»; as reception, «تسجيل دين» with phone `+970599000303`, then «تحصيل» 10 ₪ cash; the unpriced case
   **only if** the inventory finds a visit with no charge — else **not performed, by design**, test 38 proves
   it. A case the data does not hold → not performed only where §13 allows it; any other → stop and report.
   **Never change data through the app, the API, the database or the seed to get past a case.**
9. **The real run** with real screenshots (local headless Chrome over CDP, as PR 1a's scripts in this folder's
   `scripts\` do; Enter sent with `text: '\r'`): §13's cases for PR 1b, as the owner and as reception, Arabic
   light and English dark at 390, 768 and 1440 for the layouts that change with width (the uncollected card's
   rows and its «⋯» menu, the `xl` side column); **the network log proving** «تحصيل» sends one key across a retry
   and the write-off and its undo send **none** and are never re-sent by themselves (test 41, finding 115); the
   touch targets at 390. Screenshots to `C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\shots\pr1b\` — never
   inside the repository.
10. Write nothing outside the repository except this folder's `4_REPORT_PR1B.md`, `shots\` and `scripts\`.

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
- **Finding 87's family** — `routes.component.test.tsx` › "lists the owner's eleven pages", the two site tests
  that open `/spaces` first, `App.component.test.tsx` › "renders the main landmark" and
  `router.component.test.tsx` › "shows the root's general error…" — may miss their 3 s locally when the machine
  is loaded. If **only those** fail and each passes alone, record both runs (times, free memory) and go on;
  **CI's `test:component` is the judge** — if it fails there, stop.
- A run **killed for low memory** (not your own command timeout) is re-run **once** when the machine is quieter
  (no `vitest` of `C:\dev\masaha\app-b\` running, the free memory recorded); killed again → record it, carry on,
  and CI's run of that lane on the pushed head is the judge — red there → stop.

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
   [money], [state] for tests 31–39 and 41) and record its red output.
2. **Locally, on the head:** `npm run test:unit -w @masaha/web` · `npm run test:component -w @masaha/web --
   src/features/desk src/features/occupancy src/pages/dashboard src/shared/copy` (the folders this PR touches;
   add any other whose files it changes, and say so) · `$env:NODE_ENV='production'; npm run build; Remove-Item
   Env:NODE_ENV` · `npm run check:build` · `npm run check:classes` · `npm run format:check` · `npm run
   check:links` · `npm run check:conflicts`. Before each test run: no `vitest` of `C:\dev\masaha\app-b\` running,
   the free memory recorded.
3. **Not run locally — CI's run on the pushed head is the judge:** the full `test:component` lane, `test:unit`
   of `apps/api` and `packages/shared`, and `test:api` (no API change). Report them under "Not run locally (CI
   judges)", not under COULD NOT RUN. A red CI lane → fix it, fold the fix, push again.
4. **A fix after a lane passed** re-runs only the test files it touches, plus `typecheck` and `lint`; say so.

## 4. Limits and not losing work

- Write `4_REPORT_PR1B.md` **as you go**: after the first checks, after each commit (sha, subject with its
  length, the red line before the code, the green line after), after each break, after the real run, after
  the push. If you stop for any reason, the report already says where the work stands.
- Keep a long command's output in a file under `scripts\` and read its exit code and the lines you need.
- Keep the scripts you write for the real run in this folder's `scripts\`, never committed.

## 5. Discipline

Stage by path (never `-A` or `.`); each commit message written to a UTF-8 file **without a BOM, LF line
endings**, with a body saying why, and `git commit -F <file>`; subjects counted ≤ 50 (your count decides); **no
tool attribution**; **no `fixup!`, `style:` or `wip` commit left in the pushed branch** — a fix before the push
folds into its commit (`--fixup` + `GIT_SEQUENCE_EDITOR=:` autosquash), and a fix after a push too, then
`--force-with-lease`; `#PRNUM` replaced in each commit's tree just before the push (§13; this folder's
`scripts\` holds PR 1a's adapted script — adapt its branch to `feat/desk-uncollected` and its expected number to
the next free one, checked with `gh pr list --state all --limit 1`, keep its checks), never in the working tree
alone; never print a secret or a password; never merge, create an Issue, or comment on another PR. **No rebase
left in progress** at the end; `git status --short` clean; stop both servers by process id; ports 3320 and 5320
free. The local `backup/*` branch the script leaves: say its name.

## 6. Your final reply — this shape, finished or stopped

```
Status: DONE | STOPPED
PR: #<n> <url> · head <sha> · CI <green/red/pending> · <CLEAN/not CLEAN> · files <count>   (or "no PR")
Commits: <sha> <subject> (<chars>) — one line each
Database: migrate deploy <result> · seed <result line>
Ran and passed: <each command, with the result line you saw>
Ran and failed: <each, what failed, what you did>   (or "none")
Not run locally (CI judges): <each lane, and CI's result on the head once seen>
COULD NOT RUN: <each test, lane, break or real-run case not run, the exact command, the exact error,
               why>   (or "none" — only if every planned run happened)
Breaks: <each: red seen (in the red step or as its own break) / NOT red (why)>
First checks: <each of §13's checks used, and the two merged changes of §1.4: ✔ or what it found>
Real run: <each case and its screenshot, or NOT PERFORMED (by design) with the test that proves it>
Network log: <«تحصيل»'s one key across a retry; the write-off and its undo with no key, never re-sent>
Data left in masaha_dev: <each write the run made>
Open PRs and merge order: <each open PR, shared files, which merges first>
Departures from the plan: <each, with its reason>   (or "none")
Stopped at (if STOPPED): <the step, and what the owner must decide or fix>
Report: C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\4_REPORT_PR1B.md
```
