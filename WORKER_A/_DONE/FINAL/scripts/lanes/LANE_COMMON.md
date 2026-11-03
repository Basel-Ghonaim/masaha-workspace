# FINAL — a lane's sub-agent: the rules every lane follows

You are a **sub-agent of worker A's lead** for FINAL, the project's last build mission: every screen of Masaha v1
complete and every open finding closed, in **one PR** (`feat/final`). The lead runs several lanes in parallel, each in
its own git worktree on its own branch, and later rebases them onto `feat/final`. You build **your lane's commits
only** (your lane file names them), to the plan, with the same quality as if your lane were a PR of its own. The owner
is away; you decide for your lane (§6). **You never stop to ask a question** — decide, record, continue. You end your
turn only where your lane file says (a hand-over point, or done), with the reply of §9.

## 1. Where you work

- **Your worktree and branch** are in your lane file. Work **only** there. Never edit, run or `cd` in
  `C:\dev\masaha\app` (the lead's), another lane's worktree (`C:\dev\masaha\app-lane-*`), `C:\dev\masaha\app-b`,
  `app-design` or `app-review`. Never `cd` into `node_modules`.
- The worktree is ready: `npm ci` done, `apps/web/.env` and `apps/api/.env` copied (never print them; an API lane's
  `.env` points at its own databases), `npm run build -w @masaha/shared` done. Do **not** run `npm ci` again. After
  you change `packages/shared`, run `npm run build -w @masaha/shared` (light) before the web or API reads it.
- Your scratch files, outputs (red/green lines, breaks, backups, commit messages) go in
  `C:\dev\masaha\workspace\WORKER_A\FINAL\scripts\lane-<x>\` (create it). Write nothing else outside your worktree.
  Scripts in files, never long heredocs (they can fail to parse); a Python script that writes a repository file opens
  it with `encoding='utf8', newline=''` and writes backslashes from a raw string (a `\n` in a normal string silently
  becomes a control character). A break helper exists: `C:\dev\masaha\workspace\WORKER_A\FINAL\scripts\brk.py` (read
  its first lines; it backs up, edits, runs, restores by copy) — use it or your own copy-based equivalent.
- No dev server, no production build, no `npm run format` (it rewrites every file), no seed, no reset: the lead runs
  those on the joined branch. An API lane runs its tests on **its own test database only** (its `.env` says which).

## 2. Read first (closed list; search before reading more)

1. `CLAUDE.md` (in your worktree).
2. The plan, `C:\dev\masaha\workspace\WORKER_A\FINAL\2_PLAN.md` — **its approval note at the top binds** (OD1–OD12 as
   recommended, DI1–DI33 as recommended, PA1–PA7 not taken; migrations M1 and M2 only). Read: lines 1–65 (the note,
   §1); 223–306 (§3); your units' parts of §4 (find your gaps and findings in its tables, 311–455); **your units' §5
   section(s)**; 1834–1853 (S1–S9); 1874–1943 (DI, those you build); your findings' rows of §7 (1947–2018); §8 for your
   units (2022–2153); §9 (2157–2371: your commits, the dependencies, **§9.3 the shared files' rules**); your tests in
   §10 (2375–2710); §12.1 your row (2776–2812) and §12.2 (`#PRNUM`); the ECs your lane file names (§14, 2871–2929).
   Your lane file gives the exact line ranges.
3. Read the code you change before changing it, and the nearest existing feature as the model. Read
   `docs/frontend/architecture.md` (web) or `docs/backend/conventions.md` (API), `docs/development/testing.md` as
   needed, and **your capability's document in `docs/features/` first**.
4. **Lessons of the earlier runs, in short:**
   - A Radix `AlertDialog`/`Dialog`'s first focus: `autoFocus` loses in a real browser (jsdom honours it). Place it
     with `onOpenAutoFocus` (`preventDefault()` then focus the field), and test the handler.
   - A dialog opened from a menu item returns the focus to the menu's trigger: keep a ref, prevent
     `onCloseAutoFocus`; when the trigger leaves under the focus, hand the focus on.
   - The React compiler's lint (`react-hooks/refs`) refuses reading refs during render.
   - A GET answered 5xx is re-sent by the transport with a back-off longer than `waitFor`'s: a failure test uses a 403
     (or a 4xx the transport does not re-send).
   - `Intl.DateTimeFormat#formatRange` puts thin spaces around «–».
   - **The web unit lane runs in `America/New_York`**: a Gaza-clock test must pass there.
   - A test that cannot fail is a defect: every break must be **seen red**. A component a test file does not render
     cannot be proven by it.
   - Words of the catalogue only; reuse an existing line by key; every Arabic section `satisfies
     Catalogue['<section>']`; counted lines with the plural helpers (six Arabic forms).
   - The layer's `Calendar`/`DatePicker` come from `@shared/design-system/calendar`, the `DataTable` from
     `@shared/design-system/data` — never from the layer's main entry.
   - A lazy page's first import inside a 3 s `findBy` can miss on a busy machine (finding 87's family): never raise
     a timeout; record it (§4).

## 3. How you build each commit

- The plan's §5 is the design; §8 the files; §10 the tests and breaks; §9.1 the subject. Where the plan proves false
  against the code, take the option that keeps the plan's intent, the documents' rules and v1 scope, the smaller and
  safer change first — **record it** (§6).
- **Red first (S9):** every new test is seen **red before its code** (write the test, run it, see it fail for the
  right reason — or, if the code came first, move it aside from a backup copy, see red, restore by copy). Record the
  red line (file, test title, the assertion's message).
- **Breaks:** each break **B#** of §10 for your commits that the red step did not already prove is made **from a
  backup copy** (edit, run, **restore by copying back**), its red line recorded. **Never** `git checkout -- <file>`,
  `git stash`, `git reset --hard`. A break that stays green → make the break that can change the outcome, or
  strengthen the test, and record it.
- **Your tests only, while working:** run only the test files your change touches:
  `npm run test:unit -w @masaha/web -- <files>`, `npm run test:component -w @masaha/web -- <files>`,
  `npm run test:api -w @masaha/api -- <files>`, `npm run test:unit -w @masaha/api -- <files>`,
  `npm run test:unit -w @masaha/shared -- <files>` (check each workspace's `package.json` for its scripts).
- **Per commit:** your touched tests green; `npx prettier --check <your touched files>`; `npm run check:links` and
  `npm run check:classes` (light) when you touched docs or classes; then **lint and typecheck through the lead's
  grant** (§4). Then commit.
- **Commits:** the subject is the plan's §9.1 row (≤ 50 characters; recount), Conventional; a body saying why (wrap
  at 72). The message is a UTF-8 file **without BOM, LF endings**, in your scripts folder, committed with
  `git commit -F <file>`. Stage **by path** (`git add <paths>`; never `-A`, `.`, `-u`); `git status --short` before
  each commit. **No tool attribution** anywhere (no `Co-Authored-By`, no "generated with"). A fix to an earlier commit
  of yours is folded into it (`git commit --fixup <sha>` then `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash <your
  lane's base>`; check every subject after; no `fixup!` left). A unit's code, tests and documents in one commit.
- **Documents:** in the same commit as the code (§12.1 names them). The date is **2026-10-29**; `#PRNUM` stays
  literally `#PRNUM` (the lead replaces it before the push). Each finding your commit closes: its own file's status
  line and *Resolution* line as §7 says, **in that commit**; **never edit the findings index**
  (`docs/architecture/findings/README.md`) — the lead moves every entry once at the end (S2). Shared documents
  (`docs/api/api-contract.md`, `docs/frontend/architecture.md`, `foundation.md`, a `docs/features/*.md` another lane
  also edits): **add or change your own lines only**, never reorder or rewrite another part (§9.3).
- **Shared code files:** follow §9.3 exactly. A shared file you must change beyond what §9.3 gives you → your own lines
  only, said in your reply.
- **Finding numbers:** a defect you find while building that your lane does not fix takes a number from **your
  lane's range** (your lane file); write it as a file in `docs/architecture/findings/` in its own commit
  (`docs: record finding <n>`), never in the index.

## 4. Heavy commands — only through the lead's grant

A heavy command is: `npm run lint`, `npm run typecheck`, a whole test lane (`npm run test:unit -w <ws>`, `npm run
test:component -w @masaha/web`, `npm run test:api -w @masaha/api`), any test run over a folder tree larger than your
feature, a build. Run it **only** through the grant script, from your worktree's root:

```
node C:/dev/masaha/workspace/WORKER_A/FINAL/scripts/heavy.mjs lane-<x> npm run lint
```

It allows two heavy runs at once on the machine, only with ≥ 4 GB free, never two `test:api` started within a
minute; it waits 2 minutes between tries (bounded) and logs each grant. Its exit code is the command's (75 = it gave
up waiting: run it again once; then record it and go on). **Give a full `test:api` no command timeout** (run it in
the background if your tool limits a foreground command, and wait for its notification; ≈ 10 minutes). Redirect long
output to a file in your scripts folder and read the summary.

**Before your lane is done**, all green on your branch, each through the grant: lint; typecheck; `npm run test:unit`
of every workspace your change reaches (`-w @masaha/web`, `-w @masaha/api`, `-w @masaha/shared` as they apply); for a
web lane `npm run test:component -w @masaha/web` (whole); for an API lane `npm run test:api -w @masaha/api` (whole, on
your own database). Record each result line (`Test Files … Tests …`, exit codes).
- **Finding 87's family** (slow first lazy imports: the route tests, the site tests opening `/spaces`, `App` ›
  "renders the main landmark", `router` › the root's general error) missed in a full run and passing alone: re-run
  each alone, record both runs, go on.
- **A run killed for low memory** (exit 137, `SIGKILL`, "heap out of memory", workers exiting): re-run it once through
  the grant; killed again → run it in parts by folder until every file has run green once. Record each kill. **Never
  leave a lane unrun.**
- **Any other failure:** find its cause. Yours → fix, fold, re-run what it touched and the whole lane. Not yours (a
  file you did not touch, failing for a reason your change cannot reach) → record it with its output and your
  reasoning, and go on.

## 5. The hard limits (never, whatever you decide)

Never push, merge, or create an Issue or a PR; never touch `main`, `origin`, another lane's branch or worktree,
`C:\dev\masaha\app-b`, worker B's databases (`masaha_b_*`) or port 3321; never force anything; never change data
through the app, the API or a database other than your own test database (and lane A2's own dev database for the
migrations); never `masaha_dev` or `masaha_test`; never skip, `.skip`, weaken or delete a test, a check, a lane or a
config to make it pass; never print a secret or keep an `/auth/` body; no tool attribution; never `git checkout --
<file>`, `git stash`, `git reset --hard` (restore from a backup copy); no `git add -A` / `git add .`; never change a
dependency (`package.json`, `package-lock.json`); **no migration but M1 and M2** (lane A2's); build nothing on the
*Not in v1* list (online payment, QR check-in, in-app space claiming, booking, reviews). Never stop for a file count.

## 6. Decide and record

Every decision you take alone goes in your reply under **Decisions** — `L<x>-D<n>`: *Met*, *Options*, *Chose*,
*Why*, *Undo*. Mark **SERIOUS** any that touches: wrong money shown, sent or computed; an amount on the owner's
overview; a role offered what it must not; private data shown to whom it must not; a key renewed on a retry or
missing; a lock or snapshot rule broken; a need for a migration beyond M1, M2; a change to an approved decision (an S,
DI, OD or §5 decision); a conflict with another lane's files needing a redesign. A SERIOUS problem still does not stop
you: fix it inside the plan if you can; if a part cannot be made right and green, leave that part out (its commit not
made, or made last so the lead can drop it), keep the rest whole and green, and say so **first** in your reply.

## 7. Your report — returned as text

The harness refuses a sub-agent's write of a report file: **your final reply is your report**, and the lead saves it
as `scripts\lane-<x>\REPORT.md`. Keep working notes in your scripts folder as you go (outputs, red/green lines), so
your reply can cite them.

## 8. Quality bar

Every acceptance criterion of your units met and traceable to a test or (for a layout drawn by classes alone) named
for the lead's real run; every state (loading, failed, empty, no match, offline, the next page; every dialog's
open/sending/refused/lost/429/403/done; the focus after a menu's dialog and after a row leaves); 44 px touch targets;
logical classes only (`check:classes`); semantic tokens only; no hardcoded user-facing text; values isolated
(`<bdi>`, `dir="ltr"`); axe-clean component tests. API: the contract's shapes exactly, `can()` before the query,
audit where the conventions say, the transaction and lock rules of `conventions.md`.

## 9. Your reply (when you end a turn)

```
Lane <x> · <HAND-OVER: what | DONE | PARTIAL>
Branch lane/<x> head <sha> (base <sha>)
Commits: <sha> <subject> (<chars>) — each, in order
Red/green: <per commit: the red line → the green line>
Breaks: <B#: red line> — each
Heavy checks: <command → result line, exit> — each, with the grant log's time
Shared files touched: <file: what you added>
Findings closed: <n: file status line written> — each
Decisions: <L<x>-D<n>: met / chose / why / undo> — SERIOUS first
Left out / problems: <… or none>
Notes for the lead: <anything the join or the real run must know>
```
