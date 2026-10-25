# DESK_SCREENS — execute PR 3 only (`feat/customers-file`, Customers and Customer details)

You are the **executor**, in a fresh conversation. You did not plan this item and you will not review it.
**The plan is approved; do not re-decide anything in it.**

**PR 3** is the plan's PR 3, **commits 1–5**: «الزبائن» — the space's customers list (search, status chips,
kind and payment filters, a sheet below 768 px); «ملف الزبون» — a customer's file (header, unpaid visits, each
subscription's card with due, paid and left, «استلام المتبقي»); edit, archive and restore a customer; a
subscription's statement (check-ins and payments, a voided one struck) and ending a subscription; and the
sign-in page saying a session ended for idleness (`SESSION_IDLE`, #118). It opens with **two commits carried
from #119's review**.

## 0. What to read — and only this (the owner's instruction)

The owner's instruction overrides the bootstrap's session checklist for this task, stated here: **do not run
the `start-work-item` skill** and do not read `docs/development/workflow.md` whole. `CLAUDE.md` is already in
your context. Read only:

1. `C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\0_CARRIED_FROM_119.md` whole, and in
   `6_REVIEW_PR2_CODEX.md` (same folder) only its findings F1 and F2.
2. `C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\2_PLAN.md` — **these parts only:** the owner's approval note at
   its top (binding — it wins where the plan differs; its DESK_API line binds PR 3: the idle line comes from the
   **refresh's** answer); the header; §1's PR 3 paragraph; §2 *Scope*, *Acceptance criteria* and *Out of scope*
   for **PR 3**; §3's *What the reading changed*; §4; §5 (S1–S13) as they touch PR 3 (S3 — no key, never
   re-sent — and S11 above all); §6 **Spec B** and **Spec C** (what the web reads); §7's lines for PR 3
   (findings 123, 124, 162, 163); §8 *PR 3 — Customers and Customer details* (DI-39, DI-42–DI-47 among them);
   §9 *PR 3*'s files and *Shared with the other open items*; §10's opening and *PR 3 · Commits 1–5*; §11 *PR 3*
   — **tests 54–68** (and 40, the catalogues' parity, again) and *Review Focus*; §12's PR 3 lines; §13 (first
   checks — 5.i, 5.j and 5.n for PR 3 —, per commit, on the head, the real run's **PR 3** writes, push and the PR,
   the stop rule, *Stop and ask*).
3. `4_REPORT_PR2.md` (same folder) — only its departures (each *Departures in commit n*, *A fix after the head's
   lanes*) and *Decisions taken without the owner*: what PR 2 built that this PR uses (`useCustomerCard`, the
   card's `CustomerCard`, `BalanceBadge`, `balanceView`/`statusView`, `dayText`, `progressLines`,
   `useCustomerFileQuery`, `PayDialog` and its item keys, `useOpenCheckInsQuery`).
4. In the repository: the code and documents a step touches, when that step needs them — search first
   (`git grep`), then read the section, not the whole file. The `open-pr` skill may help at the end.

Read each file once. If a step proves to need a document not named here, read the part it needs and say so in
the report.

## 1. Then begin

1. **Preconditions:** #119 and DESK_API (#118) merged (`main` at `541f3e63` or later; `git grep -n
   SESSION_IDLE origin/main -- packages/shared` non-empty). `C:\dev\masaha\app` on `main`, clean, `git pull
   --ff-only` done; `npm run build -w @masaha/shared`; in `apps/api` `npx prisma migrate status` → up to date
   (the owner applied #118's and #120's migrations to `masaha_dev`; pending → `npx prisma migrate deploy` and
   `npx prisma generate`, and say so).
2. Work in `C:\dev\masaha\app` only — never in `C:\dev\masaha\app-b` (worker B executes ANNOUNCEMENTS PR 3,
   favourites, there: API, `packages/shared`, docs, the web's two `errors.ts`), `C:\dev\masaha\app-design` or
   `C:\dev\masaha\app-review` (the owner's test environment, ports 3324/5324).
3. **§13's first checks 1–6** (those that touch PR 3), each with its fallback. **The base diff** is from PR 2's
   head `8d087c5e` to `origin/main`: it holds #120 (data reports: `apps/api`, `packages/shared/src/data-reports`,
   the two `errors.ts` gaining `REPORT_ALREADY_DECIDED`, documents) — nothing this PR reads; re-read
   `packages/shared/src/{customers,subscriptions,payments}` against §10 anyway (spec B changed how the statement
   and the file are **read**, not their shapes; a shape difference that touches PR 3 → stop and ask). **Finding
   124's *Resolved* line** is DESK_API's: check it says so (§13 check 2). **Open PRs:** worker B's
   `feat/favorites` may open while you work (API, `packages/shared/src/{favorites,directory}`, the web's two
   `errors.ts`, documents). This PR edits no `errors.ts` (it **reads** `copy.errors.SESSION_IDLE`) and no
   `packages/shared`. A shared code file → **stop and ask**; shared documents (`docs/README.md`, `v1-mvp.md`,
   `overview.md`, the findings index) → text conflicts, whichever merges second rebases, keeping both sides;
   say so.
4. **Carried from #119 — the first two commits, before the plan's commit 1:** `0_CARRIED_FROM_119.md` items 1
   and 2, each test red first, its break red. Its rejected F3 is **not** built. The PR's description names them
   under "Carried from #119".
5. **Then the plan's PR 3 commits 1–5**, following §13: the branch `feat/customers-file` from the latest
   `origin/main` (`--no-track`); per commit `lint` and `typecheck`, and the test files the commit touches; each
   test red before its code, green after; the head's checks; the breaks; the real run (**PR 3's writes only**,
   below); `#PRNUM`; push; the PR, titled as §12 says (commit 2's subject, **`feat(desk): show a customer's
   file`**), `--label feat --label area:web --label area:docs`; CI green and `CLEAN`; the conflict check against
   any open PR. Stop at the plan's *Stop and ask*.
6. **Size:** the plan says ≈ 55 files, + the two carried commits; **stop and ask only past 72 files**.
7. **Finding numbers:** 162 and 163 are the plan's (commit 4 writes them; both free on `main`); 123 is resolved
   by commit 3. On `main` 160, 161, 164 and 170–171 are taken; a new one takes the next free number from **165**
   on (check the findings index on `main` first), said in the report.
8. `docker start masaha-postgres-1` (never `db:up`; never `npm ci`; Docker Desktop not running → stop and ask the
   owner); API on 3320, web on 5320, worker A's `masaha_dev`.
9. **The demo data:** run §13's data inventory first (read-only `GET`s, a script in `scripts\`): «نور حسن», the
   customer made in PR 1a (or «زائر تجربة 1»'s), «يوسف»'s subscription, a subscription with a voided payment if
   any, and the list's filters' cases. **Write only PR 3's listed writes** (the approval note's §14.11 includes
   ending «يوسف»'s subscription): as the owner — edit «نور حسن»'s phone to `+970599000304`, then back to none;
   archive the customer made in PR 1a (owes → the dialog), then restore; end «يوسف»'s subscription; as reception —
   the list's filters, a file, a statement. A case the data does not hold → not performed only where §13 allows
   it, with the test that proves it; any other → stop and report. **Never change data through the app, the API,
   the database or the seed to get past a case** (a reseed of `masaha_dev` only on the owner's word, asked
   first).
10. **The real run** with real screenshots (local headless Chrome over CDP, as PR 2's scripts in this folder's
    `scripts\` do; Enter sent with `text: '\r'`): §13's cases for PR 3, as the owner and as reception, Arabic
    light and English dark at 390, 768 and 1440 for the layouts that change with width (the customers list —
    table from 768 px, cards and the filters' sheet below —, the file and its cards' grid, the statement); **the
    width break** of §13 (the file's cards' grid removed once, `break-<what>.png`, restored); **the network log
    proving** the edit sends only what changed and is never re-sent after no answer, and the archive, restore and
    end carry no key; the touch targets at 390; **the carried fixes shown live** (item 1: the file's read made to
    fail — CDP request blocking of that one URL, not the data — shows the failure and its retry; item 2: a named
    visit from the search clears and focuses it — the visit it writes is checked out at once, paid, and named in
    the report); **the idle sign-out:** performed if the run can leave a reception session untouched for 15
    minutes (say the times), else not performed — test 67 owns it. Screenshots to
    `C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\shots\pr3\` — never inside the repository.
11. Write nothing outside the repository except this folder's `4_REPORT_PR3.md`, `shots\` and `scripts\`.

## 2. A test you cannot run stops the work

A test **failing** because its code is not written yet is the plan's red step — normal. A test, lane or
command you **cannot run** is not: it errors before any test runs (the database unreachable, Docker down, a
port taken, a module or `dist` missing, a migration pending, `No test files found`, a Vitest or TypeScript
startup error, the whole run timing out, a crash with no result); a break you could not make or run; a
real-run case you could not perform (other than those §1.9 and §1.10 allow). **Then stop at once** — never
skip, `.skip` or delete a test, never change a config, a timeout, `.env`, a script or a lane, never mock what
the plan does not, never run a narrower command and call it the lane, never call it "flaky" and move on. Write
the command, its exact error and where you were into the report, and reply with §6's shape, `Status: STOPPED`.

**The owner's standing exceptions:**
- **Finding 87's family** — `routes.component.test.tsx` › "lists the owner's eleven pages" and "lists
  reception's four pages", the two site tests that open `/spaces` first, `App.component.test.tsx` › "renders the
  main landmark" and `router.component.test.tsx` › "shows the root's general error…" — may miss their 3 s
  locally when the machine is loaded. If **only those** fail and each passes alone, record both runs (times, free
  memory) and go on; **CI's `test:component` is the judge** — if it fails there, stop. (This PR adds routes to
  `routes.component.test.tsx`: a test you add there that fails is **not** in the family.)
- A run **killed for low memory** (not your own command timeout) is re-run **once** when the machine is quieter
  (no `vitest` of `C:\dev\masaha\app-b\` running, the free memory recorded); killed again → record it, carry on,
  and CI's run of that lane on the pushed head is the judge — red there → stop.

**A plan that proves false against the code:** stop too, say exactly what and why, and offer the fix — do
not choose it yourself. **A break that stays green:** stop — unless it is plainly your own test's defect, or
the plan's break cannot change the outcome; then make the break that can, see it red, and state it as a
departure. **A design issue, a carried item or a review point you would leave undone: stop and ask** — never
silently.

**Never claim a result you did not see:** a command passed only if you saw its own output say so; copy that
line (read it by its exit code). A break counts only when you saw it red. A scoped lane with failures is not
green: name each failing file and test.

## 3. What runs where (the owner's rule: no run that only repeats another)

1. **A test seen red before its code is its own break.** Record that red line once. Make a **separate** break
   only where the plan's break targets a guard the red step did not prove (§11's breaks marked [key], [role],
   [money], [state] for tests 54–68, and the carried tests') and record its red output.
2. **Locally, on the head:** `npm run test:unit -w @masaha/web` · `npm run test:component -w @masaha/web --
   src/features/desk src/features/occupancy src/pages/dashboard src/pages/site/auth src/shared/session
   src/shared/copy src/shared/lists` (the folders this PR touches; add any other whose files it changes, and say
   so) · `$env:NODE_ENV='production'; npm run build; Remove-Item Env:NODE_ENV` · `npm run check:build` · `npm run
   check:classes` · `npm run format:check` · `npm run check:links` · `npm run check:conflicts`. Before each test
   run: no `vitest` of `C:\dev\masaha\app-b\` running, the free memory recorded.
3. **Not run locally — CI's run on the pushed head is the judge:** the full `test:component` lane, `test:unit`
   of `apps/api` and `packages/shared`, and `test:api` (no API change). Report them under "Not run locally (CI
   judges)", not under COULD NOT RUN. A red CI lane → fix it, fold the fix, push again.
4. **A fix after a lane passed** re-runs only the test files it touches, plus `typecheck` and `lint`; say so.

## 4. Limits and not losing work

- Write `4_REPORT_PR3.md` **as you go**: after the first checks, after each commit (sha, subject with its
  length, the red line before the code, the green line after), after each break, after the real run, after
  the push. If you stop for any reason, the report already says where the work stands.
- Keep a long command's output in a file under `scripts\` and read its exit code and the lines you need.
- Keep the scripts you write for the real run in this folder's `scripts\`, never committed.

## 5. Discipline

Stage by path (never `-A` or `.`); each commit message written to a UTF-8 file **without a BOM, LF line
endings**, with a body saying why, and `git commit -F <file>`; subjects counted ≤ 50 (your count decides); **no
tool attribution**; **no `fixup!`, `style:` or `wip` commit left in the pushed branch** — a fix before the push
folds into its commit (`--fixup` + `GIT_SEQUENCE_EDITOR=:` autosquash), and a fix after a push too, then
`--force-with-lease`; `#PRNUM` replaced in each commit's tree just before the push (this folder's `scripts\`
holds PR 2's adapted script — adapt its branch to `feat/customers-file` and its expected number to the next free
one, checked with `gh pr list --state all --limit 1`, keep its checks; worker B may open a PR meanwhile, so check
the number again just before the push), never in the working tree alone; never print a secret, a password or a
demo phone number; never merge, create an Issue, or comment on another PR. **No rebase left in progress** at the
end; `git status --short` clean; stop both servers by process id; ports 3320 and 5320 free. The local
`backup/*` branches the script leaves: say their names.

## 6. Your final reply — this shape, finished or stopped

```
Status: DONE | STOPPED
PR: #<n> <url> · head <sha> · CI <green/red/pending> · <CLEAN/not CLEAN> · files <count>   (or "no PR")
Commits: <sha> <subject> (<chars>) — one line each, the carried ones first
Carried from #119: <items 1–2: done in <sha>, red then green, its break red>
Ran and passed: <each command, with the result line you saw>
Ran and failed: <each, what failed, what you did>   (or "none")
Not run locally (CI judges): <each lane, and CI's result on the head once seen>
COULD NOT RUN: <each test, lane, break or real-run case not run, the exact command, the exact error,
               why>   (or "none" — only if every planned run happened)
Breaks: <each: red seen (in the red step or as its own break) / NOT red (why)>
First checks: <each of §13's checks used, and §1.3's open-PR check: ✔ or what it found>
Real run: <each case and its screenshot, or NOT PERFORMED (by design) with the test that proves it>
Network log: <the edit's changed fields only and no re-send; archive, restore and end with no key>
Data left in masaha_dev: <each write the run made>
Open PRs and merge order: <each open PR, shared files, which merges first>
Departures from the plan: <each, with its reason>   (or "none")
Decisions taken without the owner: <each, if the owner's autonomy rule was in force>   (or "none")
Stopped at (if STOPPED): <the step, and what the owner must decide or fix>
Report: C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\4_REPORT_PR3.md
```
