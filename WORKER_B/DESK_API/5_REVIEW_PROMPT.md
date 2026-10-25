# Review — DESK_API (`feat/desk-api`, #118), one independent reviewer (Claude Code)

You are the **independent reviewer** of worker B's DESK_API PR in Basel-Ghonaim/masaha: three API needs of the
desk's screens — **spec B**, a subscription's statement and a customer's file read from one `REPEATABLE READ`
snapshot (finding 124); **spec C**, reception's session ended after 15 minutes idle on the server (the access
token gains `sid`, the session family gains `last_activity_at` — migration `session_activity` — `requireAuth`
answers 401 `SESSION_IDLE`, the refresh deletes the idle family, the desk's polled occupancy read is passive);
**spec D**, a subscription made from the space's published week or month price, named by its key
(`published: { period, audience, shiftId?, name }`) — opened by four commits carried from #114's review.
**Authentication, money and the schema:** trust nothing you have not seen in the code. Find the PR: `gh pr view
118 --json number,headRefOid,mergeStateStatus`. Write the report to
`C:\dev\masaha\workspace\WORKER_B\DESK_API\6_REVIEW_CLAUDE_CODE.md`. **Work alone — no subagents.** This is a
review, not a Work Item: run no project skill, no branch.

## Rules

- **Read only, from `C:\dev\masaha\app-design`, commit objects only:** `git fetch origin` and `git fetch origin
  pull/118/head`; base = `origin/main`; **pin every read to the head's sha** (`git show <sha>:<path>`, `git diff
  origin/main...<sha>`; another process's fetch may overwrite `FETCH_HEAD`). No edits, checkout, switch or reset,
  no installs, no npm or test runs, no servers, no database commands, no comments on GitHub. The only file you
  write is the report. A `git` command failing on a `.lock` file: wait 30 s, retry once.
- First `gh pr checks 118` — a red or pending check: say so and stop. At the end, `gh pr view 118 --json
  headRefOid` again: say whether the head moved.
- Report **concrete problems only**, each verified in the code: file and line, the failing scenario (inputs →
  wrong result), severity (**blocker / should-fix / nit**), the fix. "Plausible" when unsure, with why. **Say
  what you saw in the code and what you only read in the executor's report.** No praise, no tool attribution.
- Think like: an attacker holding a stolen access token without `sid`, or an old one; a reception account
  trying to keep its session alive with the passive poll alone, or to revive an idle family through the
  refresh; an owner who is also reception at another space; a user with two devices; a race between the idle
  check, a request and a refresh; a statement read while a payment commits; reception subscribing a customer
  from a price the owner changes or deletes at the same moment; a published price with a shift, a student
  audience or a custom label.

## What to read

1. The project's rules: `git show origin/main:CLAUDE.md`.
2. The contract — **the three specs and the owner's approvals:** `C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\
   2_PLAN.md` — its approval note at the top (§14.4: the month 30 days and the week 7, the first day counted;
   the line on DESK_API's changed specs) and §6's **Spec B**, **Spec C**, **Spec D** only.
3. The executor's plan `C:\dev\masaha\workspace\WORKER_B\DESK_API\2_PLAN.md` — **the supervisor's approval note
   at its top binds** (O1: `requireAuth` refuses without deleting, the refresh deletes; O2: the price by its key;
   O3: the real run's one hand-written row; O4: the migration rule's place; size ≤ 60) — and the plan whole.
4. The carried file `0_CARRIED_FROM_114.md` (same folder; items 1–4) and, for its items, N1–N4 of
   `C:\dev\masaha\workspace\WORKER_B\PAYMENTS\6_REVIEW_CLAUDE_CODE.md`.
5. The executor's prompt `3_EXEC_PROMPT.md` and report `4_REPORT.md` (same folder): judge **every departure** —
   spec B's race tests locking `visits`, not `customers`; spec D's `name` inside `published`; the two extra
   breaks; **the idle time passed into `sessions` from `auth`/`app.ts`** (the lint level rule); the owner's
   two idle hours proven in the API lane only; 59 files; and **the first `test:api` run's timeout** in the
   customers-list scale test (1,000 subscriptions) — is spec B's `REPEATABLE READ` transaction a plausible cause
   (a long snapshot, a connection held), or is it the lane's load as the executor measured?

## Look hardest at

- **Spec C, the session:**
  - Who is idle-bound: at least one active `RECEPTION` link, no active `OWNER` link, not `ADMIN` — read from
    which rows, on every request? An owner who is reception elsewhere is never idle-ended.
  - `requireAuth`'s order: the token's checks first (signature, `sessionVersion`), then `sid` → the family →
    `last_activity_at`; a token without `sid` refused 401 as specified; a `sid` naming another user's family or a
    deleted one refused.
  - **O1:** `requireAuth` answers `SESSION_IDLE` and deletes nothing; the refresh deletes the idle family, clears
    the cookies, answers `SESSION_IDLE`, and **renews nothing**; nothing else can revive an idle family.
  - The renewal: written only when older than 60 s; never by a passive route; the passive mark covers **only**
    `GET …/occupancy` (placed in `app.ts` before the managed routes) — check no other route is caught by its
    matcher, and that the mark cannot be set by a client (a header, a query).
  - The rotation copies `last_activity_at` to the new token row; a second device's family untouched; the
    session version not raised.
  - The migration: one column, `NOT NULL DEFAULT CURRENT_TIMESTAMP` (existing families count from the
    migration), no PR number in its comments; the Prisma schema agrees.
  - `SESSION_IDLE`: 401, in the shared codes, both catalogues — **quote the Arabic line exactly in your report**
    (the owner approves it).
- **Spec B:** every read of `statement` and `customerFile` inside one read-only `RepeatableRead` transaction,
  `tx` passed to each; no lock taken; the transaction's duration bounded (no network or slow work inside); the
  race tests prove sums equal lists, and their break (`ReadCommitted`) went red.
- **Spec D:** exactly one of `packageId`, `published`, `custom`; the price found by the space and its key, with
  no custom label and period `WEEK` or `MONTH` only; the terms copied (billing `FIXED`, the price, the audience,
  the shift, no limits); the end `startsOn + 6` / `+ 29` days; no typed price and no reason, so reception may
  use it; a price changed or deleted between the desk's read and the subscribe — what the customer is charged
  and what the answer says; the idempotency key's rules unchanged for the subscribe.
- **Carried from #114:** each of 1–4 as decided; item 2's range now 92 days both ends, its test and contract
  line; item 3 in `data-model.md`.
- **Tests:** a behaviour the specs name with no test, or a test that would pass with the bug.
- **The documents:** `security.md` (*Tokens and cookies*, *Authorization*), ADR 0003's revision, the contract
  (auth, §6, the statement, the subscribe), `auth.md`, `desk.md`, `subscriptions.md`, `payments.md`,
  `data-model.md`, findings 124 resolved — true to the code, one home per fact, `#118` where the number goes.
- **Scope:** `apps/api`, `packages/shared`, `docs`, and the web's two `errors.ts` only. Commit subjects ≤ 50,
  each with a body.

## Your output

One file: the head, CI's state and whether the head moved; **a one-line verdict** (mergeable / mergeable after
a fix round / not mergeable); the findings, most severe first, each with **where its fix belongs** under the
owner's rule — **a serious or large fix: a fix round on this PR; a small one: worker B's next PR's first commit
(through `0_CARRIED_FROM_118.md`); or a finding to record (170 and on)**; `SESSION_IDLE`'s Arabic line quoted;
the departures, each judged; a short "Checked and fine" list. Then stop.
