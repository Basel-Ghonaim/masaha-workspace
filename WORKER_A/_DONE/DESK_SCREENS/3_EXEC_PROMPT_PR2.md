# DESK_SCREENS — execute PR 2 only (`feat/desk-subscribers`, the desk's subscribers)

You are the **executor**, in a fresh conversation. You did not plan this item and you will not review it.
**The plan is approved; do not re-decide anything in it.**

**PR 2** is the plan's PR 2, **commits 1–4**: the desk's one search (the people present first, then the
customers from the server's search, then «تسجيل زيارة باسم «X»»); the customer card (current subscription,
status, balance); «حضور» — a subscriber checked in on the current subscription (a dialog first when there is
none, or it has expired or not started), the server's warnings after; a subscriber's one-tap check-out and what
the subscription then owes; «استلام» — a payment on one of a customer's items. It opens with **one commit carried
from #117's review**.

## 0. What to read — and only this (the owner's instruction)

The owner's instruction overrides the bootstrap's session checklist for this task, stated here: **do not run
the `start-work-item` skill** and do not read `docs/development/workflow.md` whole. `CLAUDE.md` is already in
your context. Read only:

1. `C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\0_CARRIED_FROM_117.md` whole, and in
   `6_REVIEW_PR1B_OPENCODE.md` (same folder) only its finding F1.
2. `C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\2_PLAN.md` — **these parts only:** the owner's approval note at
   its top (binding — it wins where the plan differs); the header; §1's PR 2 paragraph; §2 *Scope*, *Acceptance
   criteria* and *Out of scope* for **PR 2**; §3's *What the reading changed*; §4; §5 (S1–S13) as they touch PR
   2 (S6 above all: what the web may ask before a check-in and what it says after); §7's lines for PR 2 (finding
   160 and any other it names); §8 *PR 2 — the desk's subscribers* (its design issues, DI-14, DI-20, DI-21 among
   them); §9 *PR 2*'s files and *Shared with the other open items*; §10's opening and *PR 2 · Commits 1–4*; §11
   *PR 2* — **tests 42–53** (and 40, the catalogues' parity, again) and *Review Focus*; §12's PR 2 lines; §13
   (first checks, per commit, on the head, the real run's **PR 2** writes, push and the PR, the stop rule, *Stop
   and ask*).
3. `4_REPORT_PR1A.md` and `4_REPORT_PR1B.md` (same folder) — only their *Departures* (what PRs 1a and 1b built
   that this PR uses: `useDeskWrite`, `deskRefusal`, the money block, the toasts, `PresentList`'s row-action slot,
   `DeskAbilities`, the uncollected card).
4. In the repository: the code and documents a step touches, when that step needs them — search first
   (`git grep`), then read the section, not the whole file. The `open-pr` skill may help at the end.

Read each file once. If a step proves to need a document not named here, read the part it needs and say so in
the report.

## 1. Then begin

1. **Preconditions:** `gh pr view 117 --json state` → `MERGED`. `C:\dev\masaha\app` on `main`, clean, `git pull
   --ff-only` done; `npm run build -w @masaha/shared`; in `apps/api` `npx prisma migrate status` → up to date
   (pending → stop and ask).
2. Work in `C:\dev\masaha\app` only — never in `C:\dev\masaha\app-b` (worker B executes DESK_API there: API,
   `packages/shared`, docs, the web's two `errors.ts` — it adds `SESSION_IDLE`), `C:\dev\masaha\app-design` or
   `C:\dev\masaha\app-review` (the owner's test environment, ports 3324/5324).
3. **§13's first checks 1, 3, 4 and 5** (those that touch PR 2), each with its fallback. **The base diff** is
   from PR 1b's head `a1193e77` to `origin/main`. **Open PRs:** worker B's `feat/desk-api` may be open (API,
   `packages/shared`, documents, the web's `errors.ts`). This PR reads `@masaha/shared/customers`,
   `subscriptions` and `payments`; **if `feat/desk-api` is merged before you start, re-read those against §10**
   (it changes the subscribe's request — spec D — and the statement's read — spec B — neither of which PR 2
   uses; a difference that touches PR 2 → stop and ask). A shared code file other than `errors.ts` → **stop and
   ask**; only `errors.ts` or documents → text conflicts, whichever merges second rebases; say so.
4. **Carried from #117 — the first commit, before the plan's commit 1:** `0_CARRIED_FROM_117.md` item 1 (the
   uncollected card's page kept in range with `usePageInRange`; `empty` only when the total is 0), its test red
   first, its break red. The PR's description names it under "Carried from #117".
5. **Then the plan's PR 2 commits 1–4**, following §13: the branch `feat/desk-subscribers` from the latest
   `origin/main` (`--no-track`); per commit `lint` and `typecheck`, and the test files the commit touches; each
   test red before its code, green after; the head's checks; the breaks; the real run (**PR 2's writes only**,
   as §13 lists them); `#PRNUM`; push; the PR, titled as §12 says (commit 2's subject,
   **`feat(desk): find customers from the desk's search`**), `--label feat --label area:web --label area:docs`;
   CI green and `CLEAN`; the conflict check against any open PR. Stop at the plan's *Stop and ask*.
6. **Size:** the plan says ≈ 38 files, + the carried commit; **stop and ask only past 55 files**.
7. **Finding numbers:** 160 is the plan's (PR 2 writes it — a visit's check-in cannot name its customer); a new
   one takes the next free number from **165** on (check the findings index on `main` first), said in the
   report.
8. `docker start masaha-postgres-1` (never `db:up`; never `npm ci`; Docker Desktop not running → stop and ask the
   owner); API on 3320, web on 5320, worker A's `masaha_dev`.
9. **The demo data:** run §13's data inventory first (read-only `GET`s, a script in `scripts\`): «سارة» and her
   usage-based subscription, «يوسف», «رامي»'s unpaid visit, and who is present now. **Write only PR 2's listed
   writes** (as reception: search «سارة», «حضور», «خروج», «استلام» 5 ₪; «يوسف» checked in and out; «رامي»'s visit
   debt paid from «استلام دفعة»). A case the data does not hold → not performed only where §13 allows it, with
   the test that proves it; any other → stop and report. **Never change data through the app, the API, the
   database or the seed to get past a case** (a reseed of `masaha_dev` only on the owner's word, asked first).
10. **The real run** with real screenshots (local headless Chrome over CDP, as PR 1a's and 1b's scripts in this
    folder's `scripts\` do; Enter sent with `text: '\r'`): §13's cases for PR 2, as the owner and as reception,
    Arabic light and English dark at 390, 768 and 1440 for the layouts that change with width (the search and its
    groups, the customer card, the pay dialog); **the network log proving** the search asks the server only once
    typing pauses, a subscriber's check-in and «استلام» each send one key across a retry, and a subscriber's
    check-out sends none; the touch targets at 390; **the carried fix shown live** (the uncollected card's page
    past the last falls back to the last page — only if the data has more than one page, else not performed,
    its test proves it). Screenshots to `C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\shots\pr2\` — never inside
    the repository.
11. Write nothing outside the repository except this folder's `4_REPORT_PR2.md`, `shots\` and `scripts\`.

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
  memory) and go on; **CI's `test:component` is the judge** — if it fails there, stop.
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
   [money], [state], [warn] for tests 42–53, and the carried test's) and record its red output.
2. **Locally, on the head:** `npm run test:unit -w @masaha/web` · `npm run test:component -w @masaha/web --
   src/features/desk src/features/occupancy src/pages/dashboard src/shared/copy src/shared/lists` (the folders
   this PR touches; add any other whose files it changes, and say so) · `$env:NODE_ENV='production'; npm run
   build; Remove-Item Env:NODE_ENV` · `npm run check:build` · `npm run check:classes` · `npm run format:check` ·
   `npm run check:links` · `npm run check:conflicts`. Before each test run: no `vitest` of `C:\dev\masaha\app-b\`
   running, the free memory recorded.
3. **Not run locally — CI's run on the pushed head is the judge:** the full `test:component` lane, `test:unit`
   of `apps/api` and `packages/shared`, and `test:api` (no API change). Report them under "Not run locally (CI
   judges)", not under COULD NOT RUN. A red CI lane → fix it, fold the fix, push again.
4. **A fix after a lane passed** re-runs only the test files it touches, plus `typecheck` and `lint`; say so.

## 4. Limits and not losing work

- Write `4_REPORT_PR2.md` **as you go**: after the first checks, after each commit (sha, subject with its
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
holds PR 1b's adapted script — adapt its branch to `feat/desk-subscribers` and its expected number to the next
free one, checked with `gh pr list --state all --limit 1`, keep its checks), never in the working tree alone;
never print a secret, a password or a demo phone number; never merge, create an Issue, or comment on another PR.
**No rebase left in progress** at the end; `git status --short` clean; stop both servers by process id; ports
3320 and 5320 free. The local `backup/*` branches the script leaves: say their names.

## 6. Your final reply — this shape, finished or stopped

```
Status: DONE | STOPPED
PR: #<n> <url> · head <sha> · CI <green/red/pending> · <CLEAN/not CLEAN> · files <count>   (or "no PR")
Commits: <sha> <subject> (<chars>) — one line each, the carried one first
Carried from #117: <item 1: done in <sha>, red then green, its break red>
Ran and passed: <each command, with the result line you saw>
Ran and failed: <each, what failed, what you did>   (or "none")
Not run locally (CI judges): <each lane, and CI's result on the head once seen>
COULD NOT RUN: <each test, lane, break or real-run case not run, the exact command, the exact error,
               why>   (or "none" — only if every planned run happened)
Breaks: <each: red seen (in the red step or as its own break) / NOT red (why)>
First checks: <each of §13's checks used, and §1.3's open-PR check: ✔ or what it found>
Real run: <each case and its screenshot, or NOT PERFORMED (by design) with the test that proves it>
Network log: <the search's one request per pause; the check-in's and «استلام»'s one key across a retry; the
             check-out with no key>
Data left in masaha_dev: <each write the run made>
Open PRs and merge order: <each open PR, shared files, which merges first>
Departures from the plan: <each, with its reason>   (or "none")
Stopped at (if STOPPED): <the step, and what the owner must decide or fix>
Report: C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\4_REPORT_PR2.md
```
