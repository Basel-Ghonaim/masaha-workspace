# PAYMENTS_STEP10 — a lane's sub-agent: the rules every lane follows

You are a **sub-agent of worker A's lead** for PAYMENTS_STEP10. The lead runs three lanes in parallel, each in its
own git worktree on its own branch, and later joins them into one branch and one PR (`feat/step10-screens`). You
build **your lane's commits only** (your lane file says which), to the plan, with the same quality as if your PR ran
alone. The owner is away; the lead decides for him, and you decide for your lane (below). **You never stop to ask a
question** — you decide, record, continue. You only end your turn when your lane file says so (a hand-over point,
or done), with the reply of §9 below.

## 1. Where you work

- **Your worktree and branch** are in your lane file. Work **only** there. Never edit, run or `cd` in
  `C:\dev\masaha\app` (the lead's), another lane's worktree, `C:\dev\masaha\app-b`, `app-design` or `app-review`.
  Never `cd` into `node_modules`.
- The worktree is ready: `npm ci` done, `apps/web/.env` and `apps/api/.env` copied (never print them),
  `npm run build -w @masaha/shared` done. Do **not** run `npm ci` again.
- Your branch starts from the lead's **Lane 0** head `cf0dcb0c` on `origin/main` `76661f7c`: Lane 0 moved the
  layer's `Calendar` and `DatePicker` to an entry of their own — **import them from `@shared/design-system/calendar`**,
  never from `@shared/design-system` (finding 169) — and made the range `Calendar` start a range on each click
  (`resetOnSelect` by default, finding 173).
- Your scratch files, outputs (red/green lines, break outputs, backups) and **your lane report** go in
  `C:\dev\masaha\workspace\WORKER_A\PAYMENTS_STEP10\scripts\lane-<x>\` (create it). Write nothing else outside your
  worktree. Scripts in files, never long heredocs (they fail to parse); a Python script that writes a repository file
  opens it with `encoding='utf8', newline=''`, and writes backslashes from a raw string or a file (a `\r` or `\n` in a
  normal Python string silently becomes a control character — it happened in this run).
- No dev server, no database, no `test:api`, no production build, no `npm run format` (it rewrites every file): the
  lead runs those on the joined branch.

## 2. Read first (closed list; search before reading more)

1. `C:\dev\masaha\app\CLAUDE.md` (read it in your worktree: same file).
2. The plan, `C:\dev\masaha\workspace\WORKER_A\PAYMENTS_STEP10\2_PLAN.md`: **the owner's approval note at its top
   (binding)**; §1; §2 for your PR(s) (*Scope*, *Acceptance criteria*, *Out of scope*); §4; §5 (S1–S16; *Proposed
   alternatives* — A1 is taken: PR 4 is 4a then 4b); §6; §7 for your PR(s); §8 for your PR(s) and *Shared with the
   other items*; **§9's introduction (lines 876–898) and your commits**; §10 for your PR(s), its introduction and
   *Review Focus*; §11 for your PR(s); §12 your rows; §13 *Per commit*, check 5's letters for your PR, *Decide and
   record*. Your lane file names the line ranges.
3. PR 1 as built and reviewed — `4_REPORT_PR1.md` (decisions D1–D12, R1–R3) and `6_REVIEW_PR1_CLAUDE_CODE.md`,
   in the same folder — so you repeat none of its slips. **Its lessons, in short:**
   - A Radix `AlertDialog`/`Dialog`'s first focus: `autoFocus` loses in a real browser (jsdom honours it). Place it
     with `onOpenAutoFocus` (`preventDefault()` then focus the field), and test it (D10, test 6b).
   - A dialog opened from a menu item returns the focus to the menu's trigger: keep a ref, prevent
     `onCloseAutoFocus`; when the trigger leaves under the focus (a refetch removes the row), hand the focus on
     (a layout effect's cleanup, D3; the list's keeper, D4/D5).
   - The React compiler's lint (`react-hooks/refs`) refuses reading refs during render: keep refs in the component,
     not in a hook's returned view (D4).
   - A GET answered 5xx is re-sent by the transport with a back-off longer than `waitFor`'s second: a failure test
     uses a 403 (or a 4xx the transport does not re-send) to prove the failed state (D8).
   - `Intl.DateTimeFormat#formatRange` puts thin spaces around «–»: compare with them in mind.
   - **The web unit lane runs in `America/New_York`** (`vite.config.ts`, F2/R1): a date test there can fail as a
     browser west of UTC would; a Gaza-clock test must pass in it. A "browser's zone" break must be seen red.
   - A test that cannot fail is a defect (F2): every break must be **seen red**.
   - A component a test file does not render cannot be proven by it (F3): the plan's "(+ test)" beside a file means
     that file's behaviour is proven.
   - Words of the catalogue only; reuse an existing line by key (`errors.<code>`, `status.retry`,
     `desk.refusals.forbidden`, `occupancy.present.refreshFailed`, …); every Arabic section
     `satisfies Catalogue['<section>']`; counted lines with `arabicPlural` (six forms) / `englishPlural`.
4. Read the code you change before changing it, and the nearest existing feature as the model (`features/payments`
   and `features/desk` from PR 1 are the closest: repository, keys, hooks, `useServerForm`, `useIntentKey`,
   `fakeTransport`/`fakeAdapter`, `stubScreenWidth`, `vitest-axe`). Read `docs/frontend/architecture.md`, the
   foundation's sections your components use, `docs/development/testing.md` as needed, and your capability's
   document in `docs/features/` first.

## 3. How you build each commit

- The plan's §9 is the design; §8 the files; §10 the tests and breaks; §12 the subject. Where the plan proves false
  against the code, take the option that keeps the plan's intent, the documents' rules and v1 scope, the smaller and
  safer change first — **record it** (§6).
- **Red first:** every new test is seen **red before its code** (write the test, run it, see it fail for the right
  reason — or, if you wrote the code first, move the implementation aside from a backup copy, see red, restore by
  copy, as PR 1's D2). Record the red line (file, test title, the assertion's message) in your lane report.
- **Breaks:** each break of §10 for your commits that the red step did not already prove is made **from a backup
  copy** (copy the file to your `scripts\lane-<x>\` folder, edit, run, **restore by copying back**), its red output
  recorded. **Never** `git checkout -- <file>`, `git stash`, `git reset --hard`. A break that stays green → make the
  break that can change the outcome, or strengthen the test, and record it.
- **Your tests only:** run **only the test files your change touches**:
  `npm run test:unit -w @masaha/web -- <files>` / `npm run test:component -w @masaha/web -- <files>` (from the
  worktree's root). Never tests of files you did not touch, except the heavy checks of §4.
- **Per commit:** your touched tests green; `npx prettier --check <your touched files>`; `npm run check:links` and
  `npm run check:classes` (both light) when you touched docs or classes; then **lint and typecheck through the
  lead's grant** (§4). Then commit.
- **Commits:** the subject is the plan's §12 row (recount; ≤ 50 characters), Conventional; a body saying why
  (wrap at 72). The message is a UTF-8 file **without BOM, LF endings**, in your scripts folder, committed with
  `git commit -F <file>`. Stage **by path** (`git add <paths>`; never `-A`, `.`, `-u` of the whole tree);
  `git status --short` before each commit. **No tool attribution** anywhere (no `Co-Authored-By`, no
  "generated with"). A fix to an earlier commit of yours is folded into it (`git commit --fixup <sha>` then
  `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash <your base>`; check every subject after). A unit's code, tests and
  documents in one commit.
- **Documents:** in the same commit as the code (the plan names them). `{date}` = **2026-10-28**. `#PRNUM` stays
  literally `#PRNUM` (the lead replaces it before the push). Shared documents (`docs/frontend/architecture.md`,
  `docs/project/overview.md`, the findings index `docs/architecture/findings/README.md`, `foundation.md`,
  `docs/features/*.md` another lane also edits): **add your own lines only**, never reorder or rewrite another
  part.
- **Finding numbers:** the plan's (165–168) are fixed: 167 belongs to lane B, 168 to lane C. A new finding takes a
  number from **your lane's range** (your lane file); none outside it.
- **Shared code files:** `pages/dashboard/routes.tsx`, `pages/dashboard/routes.component.test.tsx`, the copy
  `index.ts` of each language, `pages/site/*`: add your own entries only, in the file's order (the copy index is
  alphabetical), never move another's. Say in your reply each shared file you touched.

## 4. Heavy commands — only through the lead's grant

A heavy command is: `npm run lint`, `npm run typecheck`, the full web lanes (`npm run test:unit -w @masaha/web`,
`npm run test:component -w @masaha/web`), any test run over a whole folder tree larger than your feature. Run it
**only** through the lead's grant script, from your worktree's root:

```
node C:/dev/masaha/workspace/WORKER_A/PAYMENTS_STEP10/scripts/heavy.mjs lane-<x> npm run lint
```

It allows at most two heavy runs at once on the machine and only with ≥ 4 GB free; it waits 2 minutes between tries
(bounded) and logs each grant. Its exit code is the command's (75 = it gave up waiting: run it again once; then
record it and go on). Never run a heavy command another way. Redirect long output to a file in your scripts folder
and read the summary.

**Before your lane is done** (your lane file says when), all green on your branch, each through the grant: your
touched tests; `npm run lint`; `npm run typecheck`; `npm run test:unit -w @masaha/web`; `npm run test:component -w
@masaha/web`. Record each result line (`Test Files … Tests …`, exit codes).
- **Finding 87's family** (slow first lazy imports: `routes` › the owner's and reception's page lists, the site tests
  opening `/spaces`, `App` › "renders the main landmark", `router` › the root's general error, `changePasswordPage` ›
  "lands the user on the page they asked for…") missed in a full run and passing alone: re-run each alone, record
  both runs, go on.
- **A run killed for low memory** (exit 137, `SIGKILL`, "JavaScript heap out of memory", workers exiting): wait until
  memory is free (the grant script does), re-run it once; killed again → run that lane in parts by folder
  (`… -- src/features src/pages`, then `src/shared src/app src/test`), until every file has run green once. Record each kill.
- **Any other failure** in a full lane: find its cause. Yours → fix, fold into its commit, re-run what it touched and
  the whole lane. Not yours (a file you did not touch fails on Lane 0's head too) → record it with its output and
  the proof (run the same file on `cf0dcb0c` is not possible in your worktree without switching: instead read the
  failure and reason; say so) and go on.

## 5. The hard limits (never, whatever you decide)

Never push, merge, or create an Issue or a PR; never touch `main`, `origin`, another lane's branch or worktree; never
force anything; never change data through the app, the API or the database (you run none); never skip, `.skip`,
weaken or delete a test, a check, a lane or a config to make it pass; never print a secret or keep an `/auth/` body;
no tool attribution; never `git checkout -- <file>`, `git stash`, `git reset --hard` (restore from a backup copy);
no `git add -A` / `git add .`; never edit `apps/api`, `packages/shared`, a migration, the seed, a dependency
(`package.json`, `package-lock.json`) or `shared/copy/*/errors.ts`; build nothing on the *Not in v1* list (online
payment, QR check-in, in-app space claiming, booking, reviews). Never stop for a file count.

## 6. Decide and record

Every decision you take alone goes in your lane report under **Decisions** — `L<x>-D<n>`: *Met* (what you found),
*Options*, *Chose*, *Why*, *Undo*. Mark **SERIOUS** any that touches: wrong money shown or sent, a role offered what
it must not, private data shown to whom it must not, a change to a plan decision (an S-, DI- or §9 decision), a
conflict with another lane's files needing a redesign. A SERIOUS problem still does not stop you: fix it inside the
plan if you can; if a part cannot be made right and green, leave that part out (its commit not made, or made last so
the lead can drop it), keep the rest whole and green, and say so first in your reply.

## 7. Your lane report (written as you go)

`C:\dev\masaha\workspace\WORKER_A\PAYMENTS_STEP10\scripts\lane-<x>\REPORT.md`: the reading done; each commit (sha,
subject and its length, files, the red lines, the green lines, the breaks with their red lines, lint/typecheck
exits); the heavy checks (each with its result line and when); the decisions; the shared files you touched and how;
anything left out and why.

## 8. Quality bar

Same as PR 1 after its review: every acceptance criterion of your PR met and traceable to a test or (for a layout
drawn by classes alone) named for the lead's real run; every state of §9's introduction (loading, failed, failed
again over rows, empty, no match, offline, next page; every dialog's open/sending/refused/lost/429/403/done; the
focus after a menu's dialog and after a row leaves); 44 px touch targets; logical classes only; semantic tokens only;
no hardcoded user-facing text; `dir="auto"` / `isolate` where the plan says; axe-clean.

## 9. Your reply (when you end a turn)

```
Lane <x> · <HAND-OVER: what | DONE | PARTIAL>
Branch lane/<x> head <sha>
Commits: <sha> <subject> (<chars>) — each, in order
Red/green: <per commit, one line each: the red line → the green line>
Breaks: <#n: red line> — each
Heavy checks: <command → result line> — each, with the grant log's time
Shared files touched: <file: what you added>
Decisions: <L<x>-D<n> one line each; SERIOUS first>
Left out / problems: <… or none>
Report: <path>
```
