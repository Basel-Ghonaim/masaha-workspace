# DESK_SCREENS — execute PR 4 only (`feat/subscription-sheet`, New / renew subscription)

You are the **executor**, in a fresh conversation. You did not plan this item and you will not review it.
**The plan is approved; do not re-decide anything in it.**

**PR 4** is the plan's PR 4, **commits 1–4**: the end sheet full width below 768 px (S12, design system); the
desk reading the space's offered packages; **the subscription sheet** (screen 16) — a new customer then their
subscription, or a known customer's new subscription, from a package, a **published week or month price** (spec
D, #118) or «مخصّص», with the prior debts and the payment; and **the renewal** with its debts. It opens with
**commits carried from #122's review**. It is the last PR of this plan.

## 0. The owner's rule for this run — no stop until ready for review

The owner is away. **You do not stop and you do not ask** until the work is **ready for review**: the PR open,
CI green on its pushed head, `CLEAN`, the report written, the final reply sent. **The autonomy rule applies to the
whole run:** read `C:\dev\masaha\workspace\_SHARED\AUTONOMY_2026-10-25.md` first and follow it. Every "stop and
ask", "stop and report" or "stop" in this prompt's sources (the plan's §13 *stop rule* and *Stop and ask*, its
approval note) becomes **decide, record, continue**:
- a choice the plan leaves open, a plan false against the code, a contract difference, a break that stays green,
  a carried item larger than its file, a design issue you cannot build as written → choose the option that best
  keeps the plan's intent, the documents' rules and v1 scope, the smaller and safer change first; record it as
  you go under *Decisions taken without the owner* (what you met, the options, the choice and why, how to undo);
- a command or lane you cannot run → find the root cause (up to three tries; Docker Desktop not running: start it
  with `Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"` and wait for `docker info`), else
  record it under COULD NOT RUN with the exact error, continue every step it does not block, and let CI judge on
  the pushed head;
- a real-run case the demo data cannot hold → record it as not performed, with why and the test that proves it,
  and continue.
**The hard limits still hold** (the rule's list): never merge, push to `main`, force-push another branch, create
an Issue or delete a remote branch; never build a *Not in v1* item; never change data through the app, API,
database or seed to pass a case, never reseed; never touch worker B's worktree (`C:\dev\masaha\app-b`), databases
(`masaha_b_*`) or port 3321; never skip or weaken a test, config, timeout or lane; never print a secret, a password
or a demo phone number; no tool attribution. **Size: never stop for the file count** (the owner's rule,
2026-10-26): give `files <n>` in the report and the reply, and if it passes the plan's ≈ 40 + the carried files,
one line saying why it grew.

## 1. What to read — and only this

The owner's instruction overrides the bootstrap's session checklist for this task, stated here: **do not run the
`start-work-item` skill** and do not read `docs/development/workflow.md` whole. `CLAUDE.md` is already in your
context. Read only:

1. `C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\0_CARRIED_FROM_122.md` whole, and in
   `6_REVIEW_PR3_CLAUDE_CODE.md` (same folder) only F1–F4.
2. `C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\2_PLAN.md` — **these parts only:** the owner's approval note at
   its top (binding; its DESK_API line binds PR 4: spec D's request is **`published: { period, audience,
   shiftId?, name }`**, the name inside `published`, never a `priceId`); the header; §1's PR 4 paragraph; §2
   *Scope*, *Acceptance criteria* and *Out of scope* for **PR 4**; §3's *What the reading changed*; §4 (decision 3:
   finding 125 (c), no preview); §5 (S1–S13) as they touch PR 4 (S4's one key per intent, S12); §6 **Spec D**; §7's
   lines for PR 4 (finding 125); §8 *PR 4 — the subscription sheet* (DI-37, DI-45, DI-50–DI-53); §9 *PR 4*'s
   files; §10's opening and *PR 4 · Commits 1–4* (the words table); §11 *PR 4* — **tests 69–77** (and 40, the
   catalogues' parity) and *Review Focus*; §12's PR 4 lines; §13 (first checks for PR 4, per commit, on the head,
   the real run's **PR 4** writes, push and the PR).
3. `4_REPORT_PR3.md` (same folder) — only its *Departures in commit n*, *The real run*'s two folded fixes and
   *Decisions taken without the owner*: what PR 3 built that this PR uses (`CustomerActions` and `CustomerMenu`
   with `menu: { owner, fileLink }`, `useCustomerFile` with no `abilities`, `CustomersList`'s empty actions column
   waiting for «زبون جديد», `useStatement`'s own open state, the statement's `renewal`).
4. In the repository: the contract's *Subscriptions (managed)* (`POST …/customers/:customerId/subscriptions`,
   its `published` form, `CUSTOMER_HAS_DEBT`, `SUBSCRIPTION_ALREADY_RENEWED`), `POST …/customers`, and where the
   space's prices are read (`git grep`); the code and documents a step touches, when that step needs them — search
   first, then read the section. The `open-pr` skill may help at the end.

Read each file once. A document a step proves to need: read the part it needs and say so in the report.

## 2. Then begin

1. **Preconditions:** #122 merged (`origin/main` = `3855e37f` or later). The owner already moved
   `C:\dev\masaha\app` to `main` (clean, pulled), deleted PR 3's branches, ran `npm run build -w @masaha/shared`
   and found `prisma migrate status` up to date. Check: `git status --short` empty, `git log -1` at `origin/main`.
2. Work in `C:\dev\masaha\app` only — never in `app-b` (worker B builds ANNOUNCEMENTS PR 4 there now: the closure
   extension — `apps/api`, `packages/shared`, a migration, the web's two `errors.ts` gaining `CLOSURE_EXTENDED`
   and `CLOSURE_ALREADY_EXTENDED`, documents), `app-design` or `app-review` (the owner's environment, 3324/5324).
3. **§13's first checks for PR 4**, each with its fallback. **The base diff** is from PR 3's head `358765e3` to
   `origin/main` (#122's merge: nothing new) and, for the plan's assumptions, from `104d9d07`: **merged since the
   plan was written** — #118 (spec D **as built**: `published`, not `priceId`; the end 6 or 29 days after the
   start; reception may use it), #119, #120, #121, #122. Re-read `packages/shared/src/{customers,subscriptions,
   payments,desk,spaces}` against §10 (`subscribeSchema`, `SubscribeRequest`, `NewSubscription`, the prices'
   shape) and adapt to the contract as built; record each difference as a departure.
4. **Open PRs:** worker B's `feat/closure-extension` will open while you work. It shares **no code file** with
   this PR except possibly the web's two `errors.ts` — **this PR adds no error code** and should not edit them; if
   it must, say why. Shared documents (`subscriptions.md`, the findings index, `v1-mvp.md`, `overview.md`,
   `docs/README.md`): re-read on the latest `origin/main` before the push; each side keeps its own lines; whichever
   merges second rebases, keeping both.
5. **Carried from #122 — the first commits, before the plan's commit 1:** `0_CARRIED_FROM_122.md` items 1–4, each
   test red first, its break red. The PR's description names them under "Carried from #122".
6. **Then the plan's PR 4 commits 1–4**, following §13: the branch `feat/subscription-sheet` from the latest
   `origin/main` (`--no-track`); per commit `lint` and `typecheck`, and the test files the commit touches; each
   test red before its code, green after; the head's checks; the breaks; the real run (**PR 4's writes only**);
   `#PRNUM`; push; the PR titled as §12 says (commit 3's subject, **`feat(desk): subscribe a new or known
   customer`**), `--label feat --label area:web --label area:docs --label area:design-system`; CI green and
   `CLEAN`; the conflict check against any open PR.
7. **Spec D on the web (commit 4's "with spec D" part is in force — the owner took spec D):** the sheet offers the
   space's published WEEK and MONTH prices first under «منشورة للزوار» («أسبوعي» / «شهري», «· للطلاب»), each sent
   as `published: { period, audience, shiftId?, name }` with `name` the chosen word in the desk's language — never
   a `priceId`. Finding **165** is **not** written (it was only for spec D declined).
8. **Finding 171 — the supervisor's decision for this run, for the owner to confirm on return** (record it under
   *Decisions taken without the owner* as the supervisor's, and say it in the PR's description): the API is not
   changed in this PR (web only). The sheet **reads the space's prices afresh each time it opens** (no stale
   cache: the query refetched on opening), and the done toast states the **amount the server charged**, from the
   answer, never the form's; if the subscribe from a published price is refused (`invalid_choice` on `published`,
   or `PAYMENT_EXCEEDS_DUE`), the sheet words the refusal, keeps every field and reads the prices again. Finding
   171 **stays Open** (its other option — an `amountAgorot` the server compares — is API work for later); add no
   line to it. A test proves the toast's amount comes from the answer.
9. **Finding numbers:** 125 is resolved by commit 3 (its line as §10 says). On `main` 160–164 and 170–171 are
   taken; a new finding takes the next free number from **165** on (check the index on `main` first).
10. `docker start masaha-postgres-1` (never `db:up`; never `npm ci`); API on 3320, web on 5320, worker A's
    `masaha_dev`.
11. **The demo data:** a read-only inventory first (`GET`s, a script in `scripts\`): the space's offered packages,
    its published WEEK and MONTH prices (and for students), «محمد عوض»'s file and whether his subscription can be
    renewed (its statement's `renewal`), a customer for the owner's «مخصّص». **Write only PR 4's listed writes**
    (§13): as reception — a new customer «مشترك تجربة» (`+970599000305`) on «أسبوعي», paid in full; «محمد عوض»'s
    renewal with his debt, paid in part (the toast's parts); as owner — «مخصّص» with a reason, on a customer you
    name in the report; and, if needed for DI-37, one refused subscribe that keeps the new customer (name it). A
    case the data does not hold → not performed, with why and its test (the autonomy rule), never a data change.
12. **The real run** with real screenshots (local headless Chrome over CDP, as PR 3's scripts in this folder's
    `scripts\` do; Enter with `text: '\r'`; **the script never keeps an `/auth/` request's body** — a password
    reached a log on 2026-10-26): §13's PR 4 cases, as owner and as reception, Arabic light and English dark at
    390, 768 and 1440 for the layouts that change with width (the sheet full width below 768 px — S12 — and its
    groups); the width break (`Sheet`'s `w-full` removed once at 390, `break-sheet-width.png`, restored from a
    copy); **the network log proving** the new customer and the subscribe carry **two different keys**, a retry
    keeps each, the published subscribe sends `published` with its `name` and no `priceId`, and the payment is the
    recorded amount; the touch targets at 390; the carried F1 shown live (the focus back on «⋯» after the edit and
    after the archive dialog). Screenshots to `C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\shots\pr4\` — never
    inside the repository.
13. Write nothing outside the repository except this folder's `4_REPORT_PR4.md`, `shots\` and `scripts\`.

## 3. What runs where (the owner's rule: no run that only repeats another)

1. **A test seen red before its code is its own break.** Record that red line once. A **separate** break only
   where §11's break targets a guard the red step did not prove ([key], [role], [money], [state] for tests 69–77,
   and the carried tests') — record its red output.
2. **Locally, on the head:** `npm run test:unit -w @masaha/web` · `npm run test:component -w @masaha/web --
   src/features/desk src/features/packages src/shared/design-system src/pages/dashboard src/shared/session
   src/shared/copy` (add any other folder whose files it changes, and say so) · `$env:NODE_ENV='production'; npm
   run build; Remove-Item Env:NODE_ENV` · `npm run check:build` · `npm run check:classes` · `npm run format:check`
   · `npm run check:links` · `npm run check:conflicts`. Before each test run: the free memory recorded, and whether
   a `vitest` of `C:\dev\masaha\app-b\` runs (worker B's lanes may overlap yours; never stop its processes).
3. **Not run locally — CI judges:** the full `test:component` lane, `test:unit` of `apps/api` and
   `packages/shared`, `test:api`. Report them under "Not run locally (CI judges)". A red CI lane → find why, fix,
   fold the fix, push again (`--force-with-lease` on your own branch only).
4. **Finding 87's family** (`routes` › "lists the owner's eleven pages" and "lists reception's four pages", the
   two site tests opening `/spaces`, `App` › "renders the main landmark", `router` › "shows the root's general
   error…", and since #122 `changePasswordPage` › "lands the user on the page they asked for…"): a local miss of
   only those, each passing alone → record both runs (times, free memory) and go on; CI judges.
5. **Memory:** a run killed for low memory is re-run once when quieter; killed again → record it, carry on, CI
   judges.
6. **A fix after a lane passed** re-runs only the test files it touches, plus `typecheck` and `lint`; say so.

**Never claim a result you did not see:** a command passed only if you saw its own output say so; copy that line
(read it by its exit code). A break counts only when you saw it red. A scoped lane with failures is not green:
name each failing file and test.

## 4. Limits and not losing work

- Write `4_REPORT_PR4.md` **as you go**: after the first checks, after each commit (sha, subject with its length,
  the red line before the code, the green line after), after each break, each decision taken, the real run, the
  push, CI.
- Keep a long command's output in a file under `scripts\` and read its exit code and the lines you need.
- Breaks restored **from a backup copy**, **never `git checkout -- <file>`** while work is uncommitted.

## 5. Discipline

Stage by path (never `-A` or `.`); each commit message written to a UTF-8 file **without a BOM, LF line endings**,
with a body saying why, and `git commit -F <file>`; subjects counted ≤ 50 (your count decides); **no tool
attribution**; **no `fixup!`, `style:` or `wip` commit left in the pushed branch** — a fix folds into its commit
(`--fixup` + `GIT_SEQUENCE_EDITOR=:` autosquash); **no rebase left in progress** at the end.

**`#PRNUM` and the number:** replaced in each commit's tree just before the push (PR 3's `scripts\prnum3.sh`,
adapted to `feat/subscription-sheet`, its checks kept). Worker B will likely open first (as **#123**): check
`gh pr list --state all --limit 1` **just before the push**. **After `gh pr create`, compare the number it answered
with the one in the commits;** if they differ, re-run the replacement with the right number and push with
`git push --force-with-lease=feat/subscription-sheet:<the sha you pushed>`; record it. That is the only force-push,
on your own branch only.

Never merge, create an Issue, or comment on another PR. `git status --short` clean at the end; stop both servers
by process id; ports 3320 and 5320 free; say the name of every local `backup/*` branch you leave.

## 6. Your final reply — this shape (ready for review)

```
Status: READY FOR REVIEW | INCOMPLETE (only if nothing at all could continue)
PR: #<n> <url> · head <sha> · CI <green/red/pending> · <CLEAN/not CLEAN> · files <count>
Commits: <sha> <subject> (<chars>) — one line each, the carried ones first
Carried from #122: <items 1–4: done in <sha>, red then green, its break red>
Spec D and finding 171: <what the sheet sends; the toast's amount from the answer; 171 left Open>
Ran and passed: <each command, with the result line you saw>
Ran and failed: <each, what failed, what you did>   (or "none")
Not run locally (CI judges): <each lane, and CI's result on the head>
COULD NOT RUN: <each, the exact command, the exact error, why>   (or "none")
Breaks: <each: red seen (in the red step or as its own break) / NOT red (why)>
First checks: <each of §13's checks used, and the open-PR check>
Real run: <each case and its screenshot, or NOT PERFORMED with why and the test that proves it>
Network log: <two keys, kept on retry; `published` with its name, no priceId; the payment recorded>
Data left in masaha_dev: <each write the run made, with ids>
Open PRs and merge order: <worker B's PR, shared files, which merges first>
Departures from the plan: <each, with its reason>   (or "none")
Decisions taken without the owner: <each: met, options, chose, why, undo — finding 171's first>
Leftovers: <backup/* branches left; "no rebase in progress" checked>
Report: C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\4_REPORT_PR4.md
```
