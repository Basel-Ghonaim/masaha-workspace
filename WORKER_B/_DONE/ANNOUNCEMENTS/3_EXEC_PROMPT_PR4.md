# ANNOUNCEMENTS — execute PR 4 only (`feat/closure-extension`), in two phases

You are the **executor** of the last of step 10's four pull requests, in a fresh conversation. You did not plan
it and you will not review it. **The plan is approved; do not re-decide anything in it.** PR 4 touches money
(subscriptions' ends move) and the schema (one migration with a trigger), so it runs in **two phases**: phase 1
writes the migration's SQL and the first checks, then **stops** for the supervisor to read the SQL; phase 2
builds the rest whole — the carried items, the code, the tests, the breaks, the real run, the PR, CI.

## 0. What to read — and only this (the owner's instruction)

The owner's instruction overrides the bootstrap's session checklist for this task, stated here: **do not run
the `start-work-item` skill** and do not read `docs/development/workflow.md` whole. `CLAUDE.md` is already in
your context. Read only:

1. `C:\dev\masaha\workspace\WORKER_B\ANNOUNCEMENTS\0_CARRIED_FROM_121.md` whole, and in
   `6_REVIEW_PR3_CLAUDE_CODE.md` (same folder) only the findings it cites (1–5).
2. `C:\dev\masaha\workspace\WORKER_B\ANNOUNCEMENTS\2_PLAN.md` — **these parts only:** its header and the owner's
   approval note at its top (lines 1–55, binding, it wins where the plan differs — Q1's `CLOSURE_EXTENDED`
   Arabic, Q3, Q4 above all); §1; §2 *Scope*, *Acceptance criteria* and *Out of scope* as they touch PR 4; §4's
   owner's decisions as they name PR 4 (decision 6 and its S3 refinement), D1 and D2's PR 4 parts
   (`extendSubscriptionsSchema`, `ClosureExtension`), D10, D11, D12's PR 4 part, D13 and D14's PR 4 lines, D15's
   PR 4 part; §5 S2, S3, S4, S11, *Rules the item touches*; §6; §7's PR 4 row; §9 *PR 4* and *Not tested, and
   said*; §10's extension lines; §11's C0 rule and *PR 4*; §12 (12.1–12.9 for PR 4, the stop rule, *Stop and
   ask*); §13 Q1's `CLOSURE_EXTENDED` and `CLOSURE_ALREADY_EXTENDED` lines, Q3, Q4; Appendix A *PR 4*. Nothing of
   PRs 1–3 unless a step needs it.
3. `4_REPORT_PR3.md` (same folder) — only its departures, for what PR 3 built that this PR meets.
4. In the repository: the code and documents a step touches, when that step needs them — search first
   (`git grep`), then read the section, not the whole file. The `add-error-code` skill applies to
   `CLOSURE_EXTENDED` and `CLOSURE_ALREADY_EXTENDED`; the `open-pr` skill may help at the end; no other skill is
   needed.

Read each file once. If a step proves to need a document not named here, read the part it needs and say so in
the report.

## 1. Preconditions and what changed since the plan

1. **Preconditions:** `C:\dev\masaha\app-b` detached at the latest `origin/main` (`1a89da5d`, #121, or later) and
   clean. If not, stop. Work in `C:\dev\masaha\app-b` only — never in `C:\dev\masaha\app` (worker A's),
   `app-design` or `app-review`.
2. **12.1 first:** the base diff from `befd96f9` to `origin/main`, read against what PR 4 names. **Merged since
   the plan was written** (adapt to their contract, or stop): #102–#110 (subscriptions), #112 (PR 1), #114
   (payments), #118 (DESK_API: reception's idle sign-out — **`demo-reception` is idle-bound**: the script's
   requests renew it; a pause past 15 minutes → sign in again, and say so; and subscribing from a published
   price), #120 (PR 2), #121 (PR 3), and worker A's web PRs. **The supervisor checked on `1a89da5d`:**
   - `ClosureExtension` (`closure_extensions`) and `SubscriptionExtension` (`subscription_extensions`) exist in
     `schema.prisma`; `can.ts` holds `'subscriptions.extendAfterClosure': 'owner'`; `ANNOUNCEMENT_NOT_STARTED`
     exists in `packages/shared` and both catalogues; `CLOSURE_EXTENDED`, `CLOSURE_ALREADY_EXTENDED`,
     `extendSubscriptionsSchema` and `EXTENSION_MAX_DAYS` do not.
   - `subscriptions/closures/` holds the managed list and summary (`closures.{controller,manage.routes,mapper,
     repository,service}.ts`), mounted under `/manage/spaces/:spaceId/announcements`; the preview and the apply
     join them.
   - **`daysFrom(from, to)` already exists, private, in `apps/api/src/modules/subscriptions/
     subscriptionStatus.ts:27`.** The plan's D10 adds one to `core/gazaTime.ts`. **Keep one function, never a
     copy:** move it to `core/gazaTime.ts` (exported, U1 its test) and import it in `subscriptionStatus.ts`, if
     its meaning is the plan's (whole calendar days from `a` to `b`); if it differs, stop and ask. Say it as a
     departure.
   - `announcements.service.ts` already answers an upcoming announcement's end with `ANNOUNCEMENT_NOT_STARTED`
     and locks a row with `repository.lockIn(spaceId, id, tx)`: reuse what serves `closureIn` / `lockClosure`
     rather than writing a second lock of the same row; say what you reused.
   Re-read each where you use it. **A difference the plan does not cover → stop and ask.**
3. **The carried file is C0** (§11): `0_CARRIED_FROM_121.md`'s items 1–5 are this PR's **first commits**, before
   C1 (its suggested subjects; recount). Item 1 moves the listed read before the lock with no answer changed; item
   4 its two tests, each red under its break, then green; items 2, 3, 5 documents. `0_CARRIED_FROM_120.md` item
   4 only if a commit touches `apps/api/test/app.ts`; otherwise say it stays. The description names "Carried from
   #121". An item that contradicts the plan, proves larger than the file says, or that you would leave → **stop
   and ask**.
4. **Open PRs:** worker A's **#122** (`feat/customers-file`, open) touches only `apps/web` and `docs`; of PR 4's
   files it shares **`docs/features/subscriptions.md`** and **`docs/architecture/findings/README.md`** (text
   only). Re-check its files (`gh pr view 122 --json files`) when you start phase 2 and before the push; a
   **code** file shared → stop and ask. Shared documents: each side keeps its own lines; whichever merges second
   rebases, keeping both.
5. `docker start masaha-postgres-1` (never `db:up`, never `npm ci`; if Docker Desktop is not running, stop and ask
   the owner to start it); `masaha_b_dev` / `masaha_b_test` at #120's migration `data_report_rules` (`prisma
   migrate status` first; anything pending → stop and ask). No new dependency. **Finding numbers:** none planned;
   a new finding takes **151** and on.
6. Write nothing outside the repository except this folder's `4_REPORT_PR4.md` and `scripts\`.

## 2. Phase 1 — the migration's SQL and the first checks, then stop

1. The branch `feat/closure-extension` from the latest `origin/main` (`--no-track`); `npm run build -w
   @masaha/shared`.
2. 12.1 (above) and 12.2's checks for PR 4 **that need no code yet**: check 3 (the demo data: at least one
   subscription of the demo space covered by a closure started two days ago — read with `GET`s or a read-only
   `SELECT`; none → stop and report). Checks 1 and 2 run in phase 2, when their code exists.
3. **The migration `closure_extension_key`** (D12's PR 4 part): the schema's change, then **`npx prisma migrate
   dev --create-only --name closure_extension_key` run once** (a second run applies it — never twice; then `ls`
   the migrations folder). If it refuses as non-interactive or on data loss, use `prisma migrate diff
   --script` into the new folder instead and say so. Then edit the SQL as D12 says: the key added nullable,
   existing rows given `gen_random_uuid()`, `SET NOT NULL`, the unique index; the trigger function and the
   trigger, word for word as D12 unless the code proves a name wrong (then say which). **No PR number in the
   SQL** (no `#PRNUM`, no `#123`: the rewrite would change an applied checksum). **Do not apply it** (no `migrate
   dev` again, no `migrate deploy`), do not commit.
4. Write the report's first part (`4_REPORT_PR4.md`): preconditions, 12.1's findings (the `daysFrom` and
   lock-reuse decisions above), check 3's data (which subscriptions, their ends), the migration's path and its
   full SQL, and anything the SQL departs from D12.
5. **Stop** and reply only:
   ```
   PHASE 1 READY: <path of migration.sql>
   Branch: feat/closure-extension at <sha> · nothing committed, nothing applied
   First checks: <each ✔ or what it found>
   SQL departures from D12: <each, or "none">
   Questions: <each, or "none">
   Report: C:\dev\masaha\workspace\WORKER_B\ANNOUNCEMENTS\4_REPORT_PR4.md
   ```
   The supervisor reads the SQL and writes `3_EXEC_PROMPT_PR4_APPROVAL.md` in this folder; the owner then tells
   you to continue. **Phase 2 starts only after that file exists** — read it whole; it wins where this prompt
   differs.

## 3. Phase 2 — build PR 4 whole

C0, then the plan's C1–C3, following §12 in order for PR 4: the migration applied (`npx prisma migrate dev` on
`masaha_b_dev`, then the test database as the lanes do); 12.2's checks 1 and 2 when their code exists (the
trigger's error read as `CLOSURE_EXTENDED`, never a 500; `ends_on + ${days}::integer` a date — either failing →
stop and ask); the commits (12.3, per commit `npm run lint` and `npm run typecheck`, and the test files the
commit touches, in their lanes); the head's verification (12.4); every break of 12.5 for PR 4 (B1–B20, the
database breaks B5–B6 restored by re-running the migration's statements, as the plan says); the real run on 3321
(12.6's *PR 4* case, on the demo data); `#PRNUM`; push; the PR (12.7, titled `feat(subscriptions): extend them
after a closure`; labels `feat`, `area:api`, `area:docs`, `area:web` — the catalogues gain the two codes); CI
green and `CLEAN`; the conflict check (12.8); the description (12.9). Stop at the plan's *Stop and ask*.

- **The two new error codes** with the `add-error-code` skill, in `packages/shared` and both web catalogues'
  `errors.ts`, word for word as approved — `CLOSURE_EXTENDED`'s Arabic «مُدّدت الاشتراكات بسبب هذا الإغلاق، فلا
  يمكن حذفه ولا تغيير نوعه أو بدايته ولا تأخير نهايته.» (Q1), its English and `CLOSURE_ALREADY_EXTENDED`'s two
  lines as §13 Q1 writes them; list them in the reply. `apps/web` changes beyond the two `errors.ts` → stop and
  ask.
- **Size — the owner's new rule (2026-10-26): never stop for the file count.** The plan says ≈ 30 files, C0 adds
  ≈ 8. Whatever the count, carry on; write it in the report and the reply (`files <n>`), and if it passes 45, say
  in one line why it grew. The supervisor tells the owner.
- **The demo data:** a case the data cannot show → **stop and report**; never change data through the app to get
  past it, and no reset or reseed without the owner's word. **The real run's writes, named now:** reception's
  closure announcement (started two days ago, ending in an hour), the extension (the covered subscriptions' ends
  moved three days), the extension's rows, the closure's end. Say each in the report with the ids.

## 4. What runs where (the owner's rule: no run that only repeats another)

- A test seen red before its code is its own break — record that red line once. A **separate** break only for a
  guard the red step did not prove (each permission; the space and covered filters; the locks and their order;
  the key; the trigger and the unique index; the started check).
- **On the head, once:** `npm run lint`, `npm run typecheck`, `npm run test:unit`, `npm run test:api` (**run it
  with no command timeout** — it takes ≈ 10 minutes; a timeout you set is not a memory kill), `npm run
  format:check`, `npm run check:links`, `npm run check:conflicts`, `npm run build -w @masaha/shared`, and 12.4's
  `git` checks. **Not run locally — CI judges:** `test:component`, the web build, `check:build`,
  `check:classes`; report them under "Not run locally (CI judges)", not under COULD NOT RUN.
- **A fix after a lane passed** re-runs only the test files it touches, plus `typecheck` and `lint`; say so.

## 5. A test you cannot run stops the work

A test **failing** because its code is not written yet is the plan's red step — normal. A test, lane or command
you **cannot run** is not: it errors before any test runs (the database unreachable, Docker down, a port taken, a
module or `dist` missing, a migration pending, `No test files found`, a Vitest or TypeScript startup error, a
crash with no result); a break you could not make or run; a real-run case you could not perform. **Then stop at
once** — never skip, `.skip` or delete a test, never change a config, a timeout, `.env`, a script or a lane, never
mock what the plan does not, never run a narrower command and call it the lane, never call it "flaky" and move
on. Write the command, its exact error and where you were into the report, and reply with §8's shape, `Status:
STOPPED`.

**The owner's standing exception — memory:** a full lane **killed for low memory** (not your own timeout) is
re-run **once** when the machine is quieter (no `vitest` of `C:\dev\masaha\app\` running — never stop worker A's
processes — the free memory recorded); killed again → record it, carry on, and **CI's run of that lane on the
pushed head is the judge** — red there → stop. **Finding 87's family** (worker A's slow web tests) is not in your
lanes; if a web test fails in CI, read which before acting, and stop and ask unless it is one of them.

**A plan that proves false against the code:** stop, say exactly what and why, and offer the fix — do not choose
it yourself. **A break that stays green:** stop — unless it is plainly your own test's defect, or the plan's
break cannot change the outcome; then make the break that can, see it red, and state it as a departure.
**Anything you would leave undone — a carried item, a break, a real-run case: stop and ask** — never silently.

**Never claim a result you did not see:** a command passed only if you saw its own output say so; copy that line
(read it by its exit code, not the tail). A break counts only when you saw it red.

## 6. Limits and not losing work

- Write `4_REPORT_PR4.md` **as you go**: after phase 1, after each commit (sha, subject with its length, the red
  line before the code, the green line after), after each break, after the real run, after the push.
- Keep a long command's output in a file under `scripts\` and read its exit code and the lines you need.
- One full lane at a time; each **once, on the head**. Breaks are restored **from a backup copy** (SHA-256 before
  and after, no CRLF change — Python writes with `newline=""`), **never `git checkout -- <file>`** (it loses
  uncommitted work). The scripts stay in this folder's `scripts\`, never committed. The real-run script judges
  itself (`PASS|FAIL` per case, `ALL PASS` and exit 0), and **never keeps an `/auth/` request's body** (a
  password reached a log on 2026-10-26).

## 7. Discipline

Stage by path (never `-A` or `.`); each commit message written to a UTF-8 file **without a BOM, LF line endings**,
with a body saying why, and `git commit -F <file>`; subjects counted ≤ 50, your count decides; **no tool
attribution**; **no `fixup!`, `style:` or `wip` commit left in the pushed branch** — a fix before the push folds
into its commit (`--fixup` + `GIT_SEQUENCE_EDITOR=:` autosquash) — and **no rebase left in progress** at the end.
`#PRNUM` replaced in each commit's tree just before the push (PR 3's script in this folder's `scripts\`, its
branch adapted, its expected number checked with `gh pr list --state all --limit 1` **just before the push** —
worker A may open a PR meanwhile; **never in the migration's SQL**). The PR opened with `gh pr create --assignee
@me`. Never print a secret, a token or a demo phone number; never merge, create an Issue, or comment on another
PR. `git status --short` clean at the end; stop the API by process id (the `tsx watch` child, the server,
`pino-pretty`); port 3321 free; say the name of every local `backup/*` branch you leave.

## 8. Your final reply — this shape, finished or stopped

```
Status: DONE | STOPPED
PR: #<n> <url> · head <sha> · CI <green/red/pending> · <CLEAN/not CLEAN> · files <count>   (or "no PR")
Commits: <sha> <subject> (<chars>) — one line each, the carried ones first
Carried from #121: <each of items 1–5: done in <sha>>; #120 item 4: <done / left, why>
Migration: closure_extension_key — <applied; the SQL as approved / its departures>
New error codes: CLOSURE_EXTENDED, CLOSURE_ALREADY_EXTENDED, with their Arabic and English lines
Ran and passed: <each command, with the result line you saw>
Ran and failed: <each, what failed, what you did>   (or "none")
Not run locally (CI judges): <each lane, and CI's result on the head once seen>
COULD NOT RUN: <each test, lane, break or real-run case not run, the exact command, the exact error,
               why>   (or "none" — only if every planned run happened)
Breaks: <each: red seen (in the red step or as its own break) / NOT red (why)>
First checks: <each of §12.1 and §12.2 for PR 4, ✔ or what it found>
Real run: <each case and its answer, or NOT RUN (why)> · data changed: <what, with ids>
Open PRs and merge order: <#122 and others, shared files, which merges first>
Departures from the plan: <each, with its reason — daysFrom's move and the reused lock included>   (or "none")
Leftovers: <backup/* branches left; "no rebase in progress" checked>
Stopped at (if STOPPED): <the step, and what the owner must decide or fix>
Report: C:\dev\masaha\workspace\WORKER_B\ANNOUNCEMENTS\4_REPORT_PR4.md
```
