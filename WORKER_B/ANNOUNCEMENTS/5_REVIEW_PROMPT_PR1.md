# Review — ANNOUNCEMENTS PR 1 (`feat/announcements`, #112), one independent reviewer

You are the **independent reviewer** of worker B's ANNOUNCEMENTS PR 1 in Basel-Ghonaim/masaha: a space's
announcements on the API (step 10) — posted and edited with an idempotency key (migration `announcement_key`),
ended, started or deleted (`ANNOUNCEMENT_NOT_STARTED`), the managed list and its summary composed by
`subscriptions` with each closure's extension, the public space page's `announcements`, and the
`CLOSURE_IN_FORCE` warning at both check-ins (visit and subscriber). Claude Code built it in another
conversation; you start fresh and **trust nothing you have not seen in the code**. Find the PR: `gh pr view 112
--json number,headRefOid,mergeStateStatus`. Write the report to
`C:\dev\masaha\workspace\WORKER_B\ANNOUNCEMENTS\6_REVIEW_PR1_CLAUDE_CODE.md`. **Work alone — no subagents.**
This is a review, not a Work Item: run no project skill, no branch.

## Rules

- **Read only, from `C:\dev\masaha\app-design`, commit objects only:** `git fetch origin` and `git fetch origin
  pull/112/head`; base = `origin/main`; `git diff origin/main...FETCH_HEAD`, `git show <commit>`, `git show
  <sha>:<path>`. No edits, checkout, switch or reset (another task may hold a branch there), no installs, no npm
  or test runs, no servers, no database commands, no comments on GitHub. The only file you write is the report.
- First `gh pr checks 112` — a red or pending check: say so and stop. At the end, `gh pr view 112 --json
  headRefOid` again: say whether the head moved.
- Report **concrete problems only**, each verified in the code: file and line, the failing scenario (inputs →
  wrong result), severity (**blocker / should-fix / nit**), the fix. "Plausible" when unsure, with why. **Say
  what you saw in the code and what you only read in the executor's report.** No praise, no tool attribution.
- Think like: a reception account of another space guessing an announcement's id; a reception account reaching
  an owner-only action; two desks posting the same closure on a weak connection and retrying; a closure whose
  start or end sits at Gaza's midnight or a DST change; an anonymous visitor reading the public page of an
  unlisted space; a space announced closed while subscribers check in.

## What to read

1. The project's rules: `git show origin/main:CLAUDE.md`.
2. The approved plan `C:\dev\masaha\workspace\WORKER_B\ANNOUNCEMENTS\2_PLAN.md` — **only these parts:** the header
   and the owner's approval note (lines 1–55, it binds and wins); §2 for PR 1; §3 *Assumptions*; §4's owner's
   decisions, D1–D7, D12–D15 as they name PR 1; §5 S1, S4, S5, S10, S12; §9 *PR 1*; §10; §11 *PR 1*; §12.2,
   12.5, 12.6 for PR 1; §13; Appendix A *PR 1*.
3. The executor's prompt `3_EXEC_PROMPT_PR1.md` and report `4_REPORT_PR1.md` (same folder): judge **every
   departure** — the migration written by `migrate diff`; the demo seed's closure gaining a key;
   `liveStatus.api.test.ts`'s page keys; T10 and T18 widened; B18's test fix folded into C3; the line for
   `_SHARED\OPEN_DECISIONS.md` left in the report §9; and **(7) the instant and `since`/`take` passed between
   modules** (report §11) — is that a module boundary the conventions allow?

## Look hardest at

- **Authorization:** every route under the space-access check and the right permission (reception keeps the
  closure — the owner's decision; what is owner-only stays so); nothing of another space reachable by id; the
  public page shows only a listed space's running and upcoming announcements as D5 says, nothing private.
- **Idempotency and races (D13, S1):** the key's unique scope; a retry answering the same row; a key reused with
  another body refused as the plan says; locks in the order the other desk writes take them.
- **The state (D3) and Gaza time:** upcoming / running / ended computed from Gaza's instant; end, start, delete
  each allowed only from the states the plan names; `ANNOUNCEMENT_NOT_STARTED`; S4 (a closure ending at
  midnight covers the day before); S5's bounds.
- **The managed list and summary (D4, S10, Q6):** composed by `subscriptions`; `extension: null` today; the
  summary counting only closures started within 30 days with no extension — a 31-day-old one not counted.
- **The closure warning (D6):** `CLOSURE_IN_FORCE` at both check-ins, never blocking, in the warnings' order;
  the live status `CLOSED` and the directory's sum unchanged otherwise; *present* still defined once.
- **The migration:** the SQL against D12 (column, unique index, nullability, existing rows); no other schema
  change; the seed's key.
- **Tests:** a behaviour §9 *PR 1* names with no test, or a test that would pass with the bug; breaks B1–B24.
- **The documents:** the contract, data model, conventions, security, `announcements.md` (new), `directory.md`,
  `occupancy.md`, `desk.md`, `subscriptions.md`, v1-mvp, overview, `docs/README.md` — true to the code, one
  home per fact, only what this PR built, `#112` where the number goes.
- **Scope:** `apps/api`, `packages/shared`, `docs`, the web's two `errors.ts` and the one fixture
  `apps/web/src/test/publicSpace.ts`. Commit subjects ≤ 50, each with a body.

## Your output

One file: the head, CI's state and whether the head moved; **a one-line verdict** (mergeable / mergeable after
a fix round / not mergeable); the findings, most severe first, each with **where its fix belongs** under the
owner's rule — **a serious or large fix: a fix round on this PR; a small one: ANNOUNCEMENTS PR 2's first
commit (through `0_CARRIED_FROM_112.md`); or a finding to record (150 and on)**; the departures, each judged; a
short "Checked and fine" list. Then stop.
