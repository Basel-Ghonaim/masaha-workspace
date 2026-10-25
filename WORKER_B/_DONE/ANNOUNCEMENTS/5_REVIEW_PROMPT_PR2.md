# Review — ANNOUNCEMENTS PR 2 (`feat/data-reports`, #120), one independent reviewer (Claude Code)

You are the **independent reviewer** of worker B's data-reports PR in Basel-Ghonaim/masaha (build map step 10,
PR 2 of 4): a signed-in user reports a listed space's wrong data (a field group; «أخرى» with a message; 10 an
hour by the user; a repeat while one is open answers the open one, 200); their own list with the reply and
`repliedBy`; the owner's list (**the reporter never shown**) and decision on a verified space; the admin's list
(with the reporter) and decision on an unverified one; a decided report final (`REPORT_ALREADY_DECIDED`, an
identical retry answers as it is); migration `data_report_rules` (the enum `DataReportResolver`,
`data_reports.resolved_as`, a partial unique index of one open report per user, space and field, three
`CHECK`s). It opens with five items carried from #118's review (two tests proven by breaks, ADR 0003's line,
the test helper's session clock, findings 170–171). **Authorization, privacy and the schema:** trust nothing
you have not seen in the code. Find the PR: `gh pr view 120 --json number,headRefOid,mergeStateStatus` (head
expected `36718fde`). Write the report to
`C:\dev\masaha\workspace\WORKER_B\ANNOUNCEMENTS\6_REVIEW_PR2_CLAUDE_CODE.md`. **Work alone — no subagents.**
This is a review, not a Work Item: run no project skill, no branch.

## Rules

- **Read only, from `C:\dev\masaha\app-design`, commit objects only:** `git fetch origin` and `git fetch origin
  pull/120/head`; base = `origin/main`; **pin every read to the head's sha** (`git show <sha>:<path>`, `git diff
  origin/main...<sha>`; another process's fetch may overwrite `FETCH_HEAD`). No edits, checkout, switch or reset,
  no installs, no npm or test runs, no servers, no database commands, no comments on GitHub. The only file you
  write is the report. A `git` command failing on a `.lock` file: wait 30 s, retry once.
- First `gh pr checks 120` — a red or pending check: say so and stop. At the end, `gh pr view 120 --json
  headRefOid` again: say whether the head moved.
- Report **concrete problems only**, each verified in the code: file and line, the failing scenario (inputs →
  wrong result), severity (**blocker / should-fix / nit**), the fix. "Plausible" when unsure, with why. **Say
  what you saw in the code and what you only read in the executor's report.** No praise, no tool attribution.
- Think like: **an owner trying to learn who reported their space** (every field of every answer, the error
  bodies, the audit's `after`, a decided report's answer, a count or order that leaks it); a user flooding
  reports (bad bodies, repeats, other spaces — does each count, and is the count per user, not per address);
  two identical reports at once; the owner and the admin deciding one report at once while the space gains or
  loses its owner; an owner unlinked while a decision waits; a report of a space later hidden, deleted or moved
  to an inactive area; reception (a `RECEPTION` link only) reading or deciding; an idle reception session
  (#118) on these routes.

## What to read

1. The project's rules: `git show origin/main:CLAUDE.md`.
2. The plan `C:\dev\masaha\workspace\WORKER_B\ANNOUNCEMENTS\2_PLAN.md` — **the owner's approval note at its top
   binds** (Q1's code, Q4's schema, Q5's identical retry) — and for PR 2 only: §2 *Scope* and *Acceptance
   criteria*; §4 decisions 9–11, D1–D2's PR 2 parts, D8, D12's PR 2 part, D13, D14, D15's PR 2 part; §5 S6, S7,
   S8, S12; §9 *PR 2* (tests U1–U2, D1–D3, T1–T19, breaks B1–B24); §12.2's PR 2 checks; Appendix A *PR 2*.
3. The carried file `0_CARRIED_FROM_118.md` (same folder; items 1–5) and, for its items, findings 1–6 of
   `C:\dev\masaha\workspace\WORKER_B\DESK_API\6_REVIEW_CLAUDE_CODE.md`.
4. The executor's prompt `3_EXEC_PROMPT_PR2.md` and report `4_REPORT_PR2.md` (same folder): judge **every
   departure** — `spaces.namesWithDeleted` added in C1, not C2; the service's `now` dependency; the
   `SpacesService` fake gaining a line in `space-links.service.unit.test.ts`; the migration made with `migrate
   diff --script`, and Prisma's partial index with `where: { status: "OPEN" }`; C0's subject shortened; B15's
   first break that stayed green, and the one rerun as the plan names it; B5's restore that deleted a leftover
   row on `masaha_b_test`; lint and typecheck not rerun after the Prettier-only fixup.

## Look hardest at

- **Privacy (B-privacy, the plan's main rule):** the owner's routes never read or answer the reporter — no
  `userId`, name, email or id, in the list, the decision's answer, an error, or the audit line. Read
  `REPORT`/`WITH_PEOPLE` in `data-reports.repository.ts`, every place each is used, `toSpaceReport`, and that
  `findWithPeople` is reached only from the admin's path. Does T9 search the **decision's** answer too?
- **Authorization:** the owner's list `requireCan('space.dataReports.read')` (reception 403 before the query is
  read); the decision `can(actor, 'dataReports.resolve', { links })` on links read **under the space's lock**,
  on both the manage and the admin path; the admin's decision refused for a verified space; the manage path's
  report of another space → 404 (`findSpaceOf` compared); a stranger, another space's owner and the admin on
  the manage routes → not found.
- **The create:** the limiter counts at the route before the body is read, by the user, repeats and invalid
  bodies included (the plan's decision 9); the space found by `findShown` + `isActiveArea` (404 otherwise); the
  user's row lock serialises one user's reports; the repeat answers 200 with the open one and writes nothing;
  the partial unique index the backstop (a violation would be a 500 — is that path reachable?).
- **The decision:** lock order the space's row, then the report's; `decisionOf` — same status, same note and
  same decider → as-is, else 409; a dismissal without a note 422; `resolved_as` `OWNER` on the manage route,
  `ADMIN` on the admin's; audit `dataReport.resolved` / `dataReport.dismissed` in the same transaction.
- **The user's list:** `repliedBy` from `resolved_as` (never from the space's verification now); `listed` via
  `publicListing.upTo` with `onlyIds` and `verifiedIds: []` (the executor says `verifiedIds` only marks:
  check it); a soft-deleted space's name read through `namesWithDeleted`.
- **The admin's list:** reports of soft-deleted spaces left out (ADR 0007); the filters (status, field, space)
  in one query; the reporters' and deciders' names; `verified` per space.
- **The migration:** read the SQL whole — the enum, the column, the partial index's `WHERE ("status" =
  'OPEN')`, the three `CHECK`s exactly as D12; no PR number in it; the Prisma schema agrees (the partial index
  declared, so a later migration keeps it). Are existing rows (none in dev, but any in production-like data)
  safe under the new `CHECK`s?
- **`REPORT_ALREADY_DECIDED`:** 409, in the shared codes, both catalogues, contract §6 — **quote the Arabic line
  exactly in your report** (the owner approved «سبق البتّ في هذا البلاغ.»).
- **Carried from #118:** item 1's test (a refresh at T+10 renews no idle clock; T+15:01 → 401 `SESSION_IDLE`)
  and its break; item 2's shift-price test and its break; item 3's ADR 0003 and `security.md` lines true to the
  code; item 4's `lastActivityAt: FAR_AHEAD`; findings 170 and 171 accurate to the #118 review and indexed.
- **Tests:** a behaviour the plan names with no test, or a test that would pass with the bug (especially the
  race tests T4, T15, T18, T19 and the privacy test T9).
- **The documents:** the contract's *Data reports* section, `data-model.md`, `conventions.md`, `security.md`
  (the limit moved to *Built*), `data-reports.md` (new, the capability template), `spaces.md`, `v1-mvp.md`,
  `overview.md`, `docs/README.md` — true to the code, one home per fact, `#120` where the number goes.
- **Scope:** `apps/api`, `packages/shared`, `docs`, and the web's two `errors.ts` only; 46 files. Commit
  subjects ≤ 50, each with a body.

## Your output

One file: the head, CI's state and whether the head moved; **a one-line verdict** (mergeable / mergeable after
a fix round / not mergeable); the findings, most severe first, each with **where its fix belongs** under the
owner's rule — **a serious or large fix: a fix round on this PR; a small one: worker B's next PR's first commit
(ANNOUNCEMENTS PR 3, `feat/favorites`, through `0_CARRIED_FROM_120.md`); or a finding to record (150 and on —
B's block; 170–171 are taken)**; `REPORT_ALREADY_DECIDED`'s Arabic line quoted; the departures, each judged; a
short "Checked and fine" list. Then stop.
