# ANNOUNCEMENTS — execute PR 2 only (`feat/data-reports`)

You are the **executor** of the second of step 10's four pull requests, in a fresh conversation. You did not
plan it and you will not review it. **The plan is approved; do not re-decide anything in it.** You build it
whole: the carried items, the migration, the code, the tests, the breaks, the real run, the PR, CI.

## 0. What to read — and only this (the owner's instruction)

The owner's instruction overrides the bootstrap's session checklist for this task, stated here: **do not run
the `start-work-item` skill** and do not read `docs/development/workflow.md` whole. `CLAUDE.md` is already in
your context. Read only:

1. `C:\dev\masaha\workspace\WORKER_B\ANNOUNCEMENTS\0_CARRIED_FROM_118.md` whole, and in
   `C:\dev\masaha\workspace\WORKER_B\DESK_API\6_REVIEW_CLAUDE_CODE.md` only the review points it cites (1–6 and
   departure 8).
2. `C:\dev\masaha\workspace\WORKER_B\ANNOUNCEMENTS\2_PLAN.md` — **these parts only:** its header and the owner's
   approval note at its top (lines 1–55, binding, it wins where the plan differs); §1; §2 *Scope*, *Acceptance
   criteria* and *Out of scope* as they touch PR 2; §4's owner's decisions 9–11, D1 and D2 as they name PR 2,
   D8, D12's PR 2 part, D13, D14, D15's PR 2 part; §5 S6, S7, S8, S12, *Rules the item touches*; §6; §7's PR 2
   row; §9 *PR 2* and *Not tested, and said*; §10's report lines; §11's C0 rule and *PR 2*; §12 (12.1–12.9 for
   PR 2, the stop rule, *Stop and ask*); §13 Q1's `REPORT_ALREADY_DECIDED` line; Appendix A *PR 2*. Nothing of
   PRs 1, 3 and 4 unless a step needs it.
3. In the repository: the code and documents a step touches, when that step needs them — search first
   (`git grep`), then read the section, not the whole file. The `add-error-code` skill applies to
   `REPORT_ALREADY_DECIDED`; the `open-pr` skill may help at the end; no other skill is needed.

Read each file once. If a step proves to need a document not named here, read the part it needs and say so in
the report.

## 1. Then begin

1. **Preconditions:** PR 1 (#112) and DESK_API (#118) merged (`main` at `7f724dd5` or later).
   `C:\dev\masaha\app-b` detached at the latest `origin/main` and clean. If either fails, stop.
2. Work in `C:\dev\masaha\app-b` only — never in `C:\dev\masaha\app` (worker A) or `C:\dev\masaha\app-design`.
3. **12.1 first:** the base diff from `befd96f9` to `origin/main`, read against what PR 2 names. **Since the plan
   was written, also merged** (the plan did not know them; adapt to their contract, or stop):
   - **#112** (PR 1): `announcements`, `subscriptions/closures/`, the `PublicSpace` fixtures. PR 2's files must
     find what the plan says PR 1 left.
   - **#114** (PAYMENTS): `payments/`, the payments list; `users.namesFor` is also called there.
   - **#118** (DESK_API): **reception's session ends after 15 minutes idle** — `shared/auth/idle.ts`,
     `requireAuth` now reads the session's state (`SESSION_IDLE`, 401) for an idle-bound account (an active
     `RECEPTION` link and no `OWNER` link), and renews it unless the route is `markPassive`; the access token
     carries the session's id; migration `session_activity`. **`demo-reception`, the real run's reporter, is
     idle-bound:** the script's requests renew it, so it stays live; a pause past 15 minutes between its sign-in
     and its cases → sign in again, and say so. PR 2's routes are not passive.
   - The supervisor checked on `7f724dd5`: `users.lockAccount(id, tx)` exists (the user's row, the session
     lock — §12.2 PR 2 check 2 holds as written); `publicListing.upTo(filter, ceiling)` takes a
     `PublicListingFilter` with `onlyIds` and `verifiedIds` (check 3 stays an executor check);
     `publicSpace.findShown`, `lookups.isActiveArea`, `lookups.listedAreaIds`, `spaceLinks.linksAt`,
     `spaceLinks.verifiedSpaceIds`, `users.namesFor` exist; `can.ts` holds `dataReports.resolve`,
     `space.dataReports.read`, `platform.dataReports.read`, `dataReports.readOwn`; `spaces.namesWithDeleted`
     does not exist yet (PR 2 adds it). Re-read each where you use it. **A difference the plan does not
     cover → stop and ask**; any other change to a code file this PR names → stop and ask.
4. **The carried file is C0** (§11): `0_CARRIED_FROM_118.md`'s items 1–5 are this PR's **first commits**, before
   C1, as it says (its suggested subjects; recount). Each new test is proven by **its break** (the code is right
   today): red under the break, restored, green. Item 5 records findings **170** and **171** in
   `docs/architecture/findings/` with their index lines. The description names "Carried from #118". An item
   that contradicts the plan, proves larger than the file says, or that you would leave → **stop and ask**.
5. **Open PRs:** worker A's DESK_SCREENS PR 2 (`feat/desk-subscribers`, `apps/web` and `docs`) may be open. It
   touches no `packages/shared` code and should not touch `errors.ts`; check its files (`gh pr view <n> --json
   files`). A code file shared with it → **stop and ask**. Shared documents (`desk.md`, the findings index — it
   records finding 160, you 170–171 — `docs/README.md`, `v1-mvp.md`, `overview.md`): re-read them on the merged
   tree before editing, each side keeps its own lines; whichever merges second rebases, keeping both.
6. **Then build PR 2 only** — C0, then the plan's C1–C4, following §12 in order for PR 2: the branch
   `feat/data-reports` from the latest `origin/main` (`--no-track`); `npm run build -w @masaha/shared`; 12.2's
   first checks for PR 2 (1–4); the commits (12.3, per commit `npm run lint` and `npm run typecheck`, and the
   test files the commit touches, in their lanes); **the migration `data_report_rules`** (C1) — the plan's
   D12 SQL, `migrate dev --create-only` **once**, then `ls` the folder (a second run applies it to
   `masaha_b_dev`); non-interactive or a data-loss refusal → `migrate diff --script`, and say so; read the SQL
   before applying; **no `#PRNUM` or PR number anywhere in the migration's SQL** (#114's checksum lesson,
   `data-model.md`); the head's verification (12.4); every break of 12.5 for PR 2 (B1–B24) and C0's breaks; the
   real run on 3321 (12.6's *PR 2* cases, on the demo data); `#PRNUM`; push; the PR (12.7, titled
   `feat(data-reports): report and decide wrong data`; labels `feat`, `area:api`, `area:docs`, `area:web` —
   the catalogues gain `REPORT_ALREADY_DECIDED`); CI green and `CLEAN`; the conflict check (12.8); the
   description (12.9). Stop at the plan's *Stop and ask*.
7. **Size:** the plan says ≈ 40 files, C0 adds ≈ 8; **stop and ask only past 60 files**.
8. `docker start masaha-postgres-1` (never `db:up`, never `npm ci`; if Docker Desktop is not running, stop and
   ask the owner to start it); `masaha_b_dev` / `masaha_b_test` at #118's migration `session_activity`
   (`prisma migrate status` first; anything else pending → stop and ask). No new dependency. **Finding
   numbers:** C0 records 170 and 171; a new finding of this item takes **150** and on, in order (none planned).
9. **The new error code** `REPORT_ALREADY_DECIDED` (§13 Q1, 409): with the `add-error-code` skill, in
   `packages/shared` and both web catalogues' `errors.ts`, word for word as approved — English «This report was
   already decided.», Arabic «سبق البتّ في هذا البلاغ.»; list it in the reply.
10. **The demo data:** `masaha_b_dev` holds the demo set and the earlier items' real runs' rows. Read what you
    need with `GET`s first (a verified set space and an unverified one for 12.6). A case the data cannot show →
    **stop and report**; never change data through the app to get past it, and no reset or reseed without the
    owner's word. What the run itself writes (the reports, their decisions, the rate-limit rows), say in the
    report.
11. Write nothing outside the repository except this folder's `4_REPORT_PR2.md` and `scripts\`.

## 2. What runs where (the owner's rule: no run that only repeats another)

- A test seen red before its code is its own break — record that red line once. A **separate** break only for
  a guard the red step did not prove (each permission; the privacy rule; the limit and its key; each database
  rule; each race §12.5 names). C0's tests are proven by their breaks only.
- **On the head, once:** `npm run lint`, `npm run typecheck`, `npm run test:unit`, `npm run test:api` (**run it
  with no command timeout** — it takes ≈ 10 minutes; a timeout you set is not a memory kill), `npm run
  format:check`, `npm run check:links`, `npm run check:conflicts`, `npm run build -w @masaha/shared`, and
  12.4's `git` checks. **Not run locally — CI judges:** `test:component`, the web build, `check:build`,
  `check:classes`; report them under "Not run locally (CI judges)", not under COULD NOT RUN — the web change is
  the two `errors.ts` lines only; if `apps/web` changes beyond them, stop and ask.
- **A fix after a lane passed** re-runs only the test files it touches, plus `typecheck` and `lint`; say so.

## 3. A test you cannot run stops the work

A test **failing** because its code is not written yet is the plan's red step — normal. A test, lane or
command you **cannot run** is not: it errors before any test runs (the database unreachable, Docker down, a
port taken, a module or `dist` missing, a migration pending, `No test files found`, a Vitest or TypeScript
startup error, a crash with no result); a break you could not make or run; a real-run case you could not
perform. **Then stop at once** — never skip, `.skip` or delete a test, never change a config, a timeout,
`.env`, a script or a lane, never mock what the plan does not, never run a narrower command and call it the
lane, never call it "flaky" and move on. Write the command, its exact error and where you were into the report,
and reply with §6's shape, `Status: STOPPED`.

**The owner's standing exception — memory:** a full lane **killed for low memory** (not your own timeout) is
re-run **once** when the machine is quieter (no `vitest` of `C:\dev\masaha\app\` running — worker A runs its
web lanes in parallel; never stop its processes — the free memory recorded); killed again → record it, carry
on, and **CI's run of that lane on the pushed head is the judge** — red there → stop.

**Finding 87's family** (worker A's slow web tests) is not in your lanes; if a web test fails in CI, read which
before acting, and stop and ask unless it is one of them.

**A plan that proves false against the code:** stop, say exactly what and why, and offer the fix — do not
choose it yourself. **A break that stays green:** stop — unless it is plainly your own test's defect, or the
plan's break cannot change the outcome; then make the break that can, see it red, and state it as a departure.
**Anything you would leave undone — a carried item, a break, a real-run case: stop and ask** — never silently.

**Never claim a result you did not see:** a command passed only if you saw its own output say so; copy that
line (read it by its exit code, not the tail). A break counts only when you saw it red.

## 4. Limits and not losing work

- Write `4_REPORT_PR2.md` **as you go**: after the first checks, after each commit (sha, subject with its
  length, the red line before the code or under its break, the green line after), after each break, after the
  real run, after the push. If you stop for any reason, the report already says where the work stands.
- Keep a long command's output in a file under `scripts\` and read its exit code and the lines you need, not
  the whole output.
- One full lane at a time; each **once, on the head**. Breaks are restored **from a backup copy** (SHA-256
  before and after, no CRLF change — Python writes with `newline=""`), never `git checkout` a file with
  uncommitted work. The scripts stay in this folder's `scripts\`, never committed. The real-run script judges
  itself (`PASS|FAIL` per case against the expected status and code, `ALL PASS` and exit 0), as
  `WORKER_B\SUBSCRIPTIONS\scripts\realrun2.mjs` does.

## 5. Discipline

Stage by path (never `-A` or `.`); each commit message written to a UTF-8 file **without a BOM, LF line
endings**, with a body saying why, and `git commit -F <file>`; subjects counted ≤ 50, your count decides; **no
tool attribution**; **no `fixup!`, `style:` or `wip` commit left in the pushed branch** — a fix before the push
folds into its commit (`--fixup` + `GIT_SEQUENCE_EDITOR=:` autosquash) — and **no rebase left in progress** at
the end (`git status` says so). `#PRNUM` replaced in each commit's tree just before the push: copy
`C:\dev\masaha\workspace\WORKER_B\DESK_API\scripts\prnum.sh` (the latest model) into this folder's `scripts\`,
adapt its branch to `feat/data-reports` and its expected number to the next free one, checked with `gh pr list
--state all --limit 1`, keep its checks; never in the working tree alone, never in the migration. The PR opened
with `gh pr create --assignee @me`. Never print a secret, a token or a demo phone number; never merge, create an
Issue, or comment on another PR. `git status --short` clean at the end; stop the API by process id (the `tsx
watch` child, the server, `pino-pretty`); port 3321 free; say the name of every local `backup/*` branch you
leave.

## 6. Your final reply — this shape, finished or stopped

```
Status: DONE | STOPPED
PR: #<n> <url> · head <sha> · CI <green/red/pending> · <CLEAN/not CLEAN> · files <count>   (or "no PR")
Commits: <sha> <subject> (<chars>) — one line each, the carried ones first
Carried from #118: <each of items 1–5: done in <sha>, its break red then green / docs / findings 170–171>
Migration: data_report_rules · applied to masaha_b_dev and masaha_b_test · migrate status <line>
New error codes: REPORT_ALREADY_DECIDED, with its Arabic and English lines
Ran and passed: <each command, with the result line you saw>
Ran and failed: <each, what failed, what you did>   (or "none")
Not run locally (CI judges): <each lane, and CI's result on the head once seen>
COULD NOT RUN: <each test, lane, break or real-run case not run, the exact command, the exact error,
               why>   (or "none" — only if every planned run happened)
Breaks: <each: red seen (in the red step or as its own break) / NOT red (why)>
First checks: <each of §12.1 and §12.2 for PR 2 (1–4), ✔ or what it found>
Real run: <each case and its answer, or NOT RUN (why)> · requests sent to reach 429: <n> · data changed: <what>
Open PRs and merge order: <worker A's open PR, shared files, which merges first>
Departures from the plan: <each, with its reason>   (or "none")
Leftovers: <backup/* branches left; "no rebase in progress" checked>
Stopped at (if STOPPED): <the step, and what the owner must decide or fix>
Report: C:\dev\masaha\workspace\WORKER_B\ANNOUNCEMENTS\4_REPORT_PR2.md
```
