# Review — ANNOUNCEMENTS PR 4 (`feat/closure-extension`), one independent reviewer (Claude Code)

You are the **independent reviewer** of worker B's closure-extension PR in Basel-Ghonaim/masaha (build map step
10, PR 4 of 4, the last): once a closure has started, the owner previews the days the server proposes and how
many subscriptions it covers (`GET …/announcements/:id/extend-subscriptions`), then extends them once under one
key (`POST`, `{ days }` 1–365): every covered subscription's `ends_on` moves by the days typed, one link each,
audited. An extended closure is guarded **by a database trigger** (no new type or start, no deletion, no later
end; its text and an earlier end pass — `CLOSURE_EXTENDED`); a second extension is `CLOSURE_ALREADY_EXTENDED`.
**One migration** (`closure_extension_key`: the key column, its unique index, the trigger). It opens with items
carried from #121's review. **Money (subscriptions' ends move), authorization, transactions, locks and the
schema:** trust nothing you have not seen in the code. Find the PR: `gh pr list --head feat/closure-extension
--state open --json number,headRefOid,mergeStateStatus`. Write the report to
`C:\dev\masaha\workspace\WORKER_B\ANNOUNCEMENTS\6_REVIEW_PR4_CLAUDE_CODE.md`. **Work alone — no subagents.**
This is a review, not a Work Item: run no project skill, no branch.

## Rules

- **Read only, from `C:\dev\masaha\app-design`, commit objects only:** `git fetch origin` and `git fetch origin
  pull/<n>/head`; base = `origin/main`; **pin every read to the head's sha** (`git show <sha>:<path>`, `git diff
  origin/main...<sha>`; another process's fetch may overwrite `FETCH_HEAD`). No edits, checkout, switch or reset,
  no installs, no npm or test runs, no servers, no database commands, no comments on GitHub. The only file you
  write is the report. A `git` command failing on a `.lock` file: wait 30 s, retry once.
- First `gh pr checks <n>` — a red or pending check: say so and stop. At the end, `gh pr view <n> --json
  headRefOid` again: say whether the head moved.
- Report **concrete problems only**, each verified in the code: file and line, the failing scenario (inputs →
  wrong result), severity (**blocker / should-fix / nit**), the fix. "Plausible" when unsure, with why. **Say
  what you saw in the code and what you only read in the executor's report.** No praise, no tool attribution.
- Think like: an owner extending twice (two tabs, two keys; one key retried; a key reused for another closure);
  reception or a stranger calling the extension; an owner whose link ends while waiting; a closure still
  upcoming, deleted, of another type or another space; a subscription that ends during the closure, starts after
  it, was ended early, has no end, is another space's, or is renewed or ended while the extension waits; a closure
  ending at midnight (Gaza vs UTC days); days 0, 365, 366; after the extension — the owner editing the closure's
  type, start, end (later, earlier, now) or deleting it; the trigger's error reaching the client as a 500.

## What to read

1. The project's rules: `git show origin/main:CLAUDE.md`.
2. The plan `C:\dev\masaha\workspace\WORKER_B\ANNOUNCEMENTS\2_PLAN.md` — **the owner's approval note at its top
   binds** (Q1's `CLOSURE_EXTENDED` Arabic, Q3, Q4) — and for PR 4 only: §2 *Scope* and *Acceptance criteria*;
   §4 decision 6, D1–D2's PR 4 parts, D10, D11, D12's PR 4 part, D13, D14's PR 4 lines; §5 S2, S3, S4, S11; §9
   *PR 4* (U1–U3, D1–D2, T1–T13, breaks B1–B20) and *Not tested, and said*; §12.2's PR 4 checks; Appendix A *PR 4*.
3. The carried file `0_CARRIED_FROM_121.md` (same folder; items 1–5) and, for its items, findings 1–5 of
   `6_REVIEW_PR3_CLAUDE_CODE.md` (same folder).
4. The executor's prompt `3_EXEC_PROMPT_PR4.md`, the supervisor's `3_EXEC_PROMPT_PR4_APPROVAL.md` and the report
   `4_REPORT_PR4.md` (same folder). The executor ran phase 2 **under the owner's autonomy rule**
   (`C:\dev\masaha\workspace\_SHARED\AUTONOMY_2026-10-25.md`): judge **every departure and every decision taken
   without the owner** — at least `daysFrom` moved from `subscriptionStatus.ts` to `packages/shared`'s
   `gazaTime.ts` (does `subscriptionStatus` behave exactly as before?), `lockClosure` built on `repository.lockIn`,
   the migration made by `migrate diff`.

## Look hardest at

- **The migration's SQL** (read it whole): existing rows keyed before `NOT NULL`; the unique index; the trigger
  function's condition exactly as D12 (S3: an earlier end and end-now allowed, a later end refused, `NULL` end
  handled both ways); `BEFORE UPDATE OF … WHEN (OLD."type" = 'CLOSURE')` — can a closure's `type` be changed **to**
  something else in the same statement and escape? Can any route soft-delete or edit without firing it? No PR
  number in the SQL; the Prisma schema matches the SQL (no drift).
- **The apply's transaction, in D11's order:** the space's lock, then `can()` with the links read under the
  transaction; the key's lookup (same closure → the first result, 201, moving nothing; another → 409); the
  closure's lock; already extended → `CLOSURE_ALREADY_EXTENDED`; started; the span; the covered rows locked `ORDER
  BY id FOR UPDATE`; one `UPDATE … ends_on + days::integer` over exactly those ids; the extension and its links;
  the audit. **Every read goes through `tx`** (conventions §8; #121's lesson). A retry answers the stored
  extension, not a recomputation.
- **The covered rule** (one SQL fragment shared by the preview and the apply): `ended_at IS NULL`, `ends_on IS
  NOT NULL`, `ends_on >= first`, `starts_on IS NULL OR starts_on <= last`, the space filter. The preview writes
  nothing and takes no lock.
- **The days:** `closureSpan` (Gaza days; an end at midnight covers the day before; a running one to today);
  `daysFrom`; `proposedDays = min(days, max)`; the request's bounds (1–365) in `packages/shared`.
- **Authorization:** the owner only (`subscriptions.extendAfterClosure`), reception 403 before the key or body is
  read; a stranger and the admin `not_found`.
- **The codes:** `CLOSURE_EXTENDED` (409, from the trigger through `constraintCodes.ts`, never a 500) and
  `CLOSURE_ALREADY_EXTENDED` (409), in the shared codes, both catalogues, contract §6 — **quote both Arabic lines
  exactly** (the owner approved `CLOSURE_EXTENDED`'s «مُدّدت الاشتراكات بسبب هذا الإغلاق، فلا يمكن حذفه ولا تغيير
  نوعه أو بدايته ولا تأخير نهايته.» in Q1).
- **Carried from #121:** item 1 — the listed read before `runInTransaction`, the answers' order unchanged; item 4's
  two tests real (would fail under their breaks); items 2, 3, 5 true to the code.
- **Tests:** a behaviour the plan names with no test, or a test that would pass with the bug (T5's retry, T6's
  race, T9–T11's `whileHeld`, D1's trigger cases, T12's 409 vs 500).
- **The documents:** the contract (the two routes, §6), data model (*Constraints*, *Derived values*,
  *ClosureExtension*), ADR 0009's row and *Revised*, conventions §6 and §13, security, `announcements.md`,
  `subscriptions.md` (#122 changed it too: both sides kept?), `v1-mvp.md`, `overview.md` — true to the code, one
  home per fact, the PR's number where it goes.
- **Scope:** `apps/api`, `packages/shared`, `docs`, and the web's two `errors.ts` only; one migration; no
  dependency. Commit subjects ≤ 50, each with a body; no `fixup!`, no tool attribution.

## Your output

One file: the head, CI's state and whether the head moved; **a one-line verdict** (mergeable / mergeable after
a fix round / not mergeable); the findings, most severe first, each with **where its fix belongs** under the
owner's rule — **a serious or large fix: a fix round on this PR; a small one: worker B's next PR's first commit
(through `0_CARRIED_FROM_<n>.md`); or a finding to record (151 and on)**; both Arabic lines quoted; the departures
and the decisions taken without the owner, each judged; a short "Checked and fine" list. Then stop.
