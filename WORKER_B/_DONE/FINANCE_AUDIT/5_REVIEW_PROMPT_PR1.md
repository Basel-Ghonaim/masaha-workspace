# Review — FINANCE_AUDIT PR 1 (`feat/audit-log`), one independent reviewer (Claude Code)

You are the **independent reviewer** of worker B's first FINANCE_AUDIT PR in Basel-Ghonaim/masaha (build map step
11's API, PR 1 of 3), **API only** (`apps/api`, `packages/shared`, `docs`; **no migration** planned): it opens with
the items **carried from #123** — finding 151 option A (the closure extension also moves each covered subscription's
**not-yet-started renewal chain**, start and end, by the same days, under the same locks, linked and audited), a key
that extended **another space's** closure refused as a `conflict`, and two document fixes — then **the audit
reader**: `GET /manage/spaces/:spaceId/audit-log` (the owner's, `requireCan('space.auditLog.read')`; the admin shown
as «Masaha», never named) and `GET /admin/audit-log` (the admin's, through the `platformEvents.ts` allowlist,
default deny), with filters (period, actions, actor, target search), paging and `meta.actors`. **Money (the
extension moves subscriptions' dates), authorization, privacy, transactions and locks:** trust nothing you have not
seen in the code. Find the PR: `gh pr list --head feat/audit-log --state open --json
number,headRefOid,mergeStateStatus`. Write the report to
`C:\dev\masaha\workspace\WORKER_B\FINANCE_AUDIT\6_REVIEW_PR1_CLAUDE_CODE.md`, **as you go** (a section per part).
**Work alone — no subagents.** This is a review, not a Work Item: run no project skill, no branch.

> **The owner's decisions before this review (2026-10-28), binding:** the four `q`-over-all-time reads over
> 150 ms (the owner's page and count, the admin's page and count) are **accepted — no index, no migration** (the
> default 30-day read is fast; an index waits for real use); **finding 152** (the audit's retention) stays **Open**.
> Do not report either as a finding; do judge whether the joins return the same answer and whether the
> measurement holds.

## Rules

- **Read only, from `C:\dev\masaha\app-design`, commit objects only:** `git fetch origin` and `git fetch origin
  pull/<n>/head`; base = `origin/main`; **pin every read to the head's sha** (`git show <sha>:<path>`, `git diff
  origin/main...<sha>`; another process's fetch may overwrite `FETCH_HEAD`). No edits, checkout, switch or reset, no
  installs, no npm or test runs, no servers, no database commands, no comments on GitHub. The only file you write is
  the report. A `git` command failing on a `.lock` file: wait 30 s, retry once.
- First `gh pr checks <n>` — a red or pending check: say so and stop. At the end, `gh pr view <n> --json
  headRefOid` again: say whether the head moved.
- Report **concrete problems only**, each verified in the code: file and line at the head, the failing scenario
  (inputs → wrong result), severity (**blocker** — a subscription's dates moved wrongly or twice, an entry or a
  person shown to whom it must not be, a role let through, a 500 a client can cause, a test that cannot fail ·
  **should-fix** — a real defect a client can meet, a missing planned test, a document that says something false ·
  **nit**), the fix. "Plausible" when unsure, with why. **Say what you saw in the code and what you only read in the
  executor's report.** A point whose own conclusion is "no change needed" is not a finding. No praise, no tool
  attribution.
- Think like: an owner extending a closure whose covered subscription has a renewal not yet started, two renewals
  chained, a renewal already started, a renewal of another customer or space, a renewal ended early; the same key
  retried, retried for another closure of the same space, used by another space's owner; the owner of space A asking
  `?actorId=` of an admin, of space B's reception, of a deleted account; reception or a stranger asking the owner's
  log; an admin asking a space's log; the admin's log asked for an event type not on the allowlist; a target search
  with `%`, `_`, a backslash, Arabic with diacritics, 200+ characters; a period across Gaza's midnight and the
  clock change; `page` past the end, `limit` 0 and over the maximum; an entry whose target was deleted.

## What to read

1. The project's rules: `git show origin/main:CLAUDE.md`.
2. The plan `C:\dev\masaha\workspace\WORKER_B\FINANCE_AUDIT\2_PLAN.md` — **the owner's approval note at its top
   binds** (Q1–Q12 as recommended; Q5: a read over 150 ms recorded, not indexed — no migration; Q10: finding 152) —
   and for PR 1 only: §2 *Scope* and *Acceptance criteria* (PR 1's); §4 the owner's decisions, D1–D6, D13, D14,
   D15's PR 1 part; §5 S1, S4, S5, S6, S7, S12 and *Rules the item touches*; §9 *PR 1* (carried and the reader) and
   *Not tested, and said*; §10; §11 *PR 1*; §12.2's PR 1 checks; §12.5.
3. The carried file `0_CARRIED_FROM_123.md` (same folder) and, for its items,
   `C:\dev\masaha\workspace\WORKER_B\_DONE\ANNOUNCEMENTS\6_REVIEW_PR4_CLAUDE_CODE.md` (findings 1–4).
4. The executor's prompt `3_EXEC_PROMPT_PR1.md` and report `4_REPORT_PR1.md` (same folder). The executor ran **under
   the owner's autonomy rule** (`C:\dev\masaha\workspace\_SHARED\AUTONOMY_2026-10-25.md`): judge **every departure
   and every decision taken without the owner** — at least: the lateral subquery replaced by one `LEFT JOIN` per
   target type (folded into C1 — is the answer the same for every target type, including a deleted target and an
   entry with no entity id?); the four reads over 150 ms recorded, not indexed; T-C2 rewritten on an ended closure
   at the file's clock (does it still prove "a started renewal is not moved"?); repeated `actions` counted once
   instead of refused; an actor id out of range answering `out_of_range`; `OPEN_DECISIONS.md` left to the
   supervisor; the carried real-run case not performed; and how the breaks and full lanes ended after the low-memory
   stop (were all 25 breaks seen red?).

## Look hardest at

- **Finding 151's chain (money):** which renewals move — only those not started on the extension's day (Gaza),
  following `renewal_of_id` to the end of the chain, the same customer and space; locked with the covered rows in
  one `ORDER BY id FOR UPDATE` order (no deadlock against a renewal or a check-out); one update each, start **and**
  end by the same days; linked to the extension and listed in the audit (`renewalIds`); the preview's count says the
  same as the apply. A started renewal never moved; a renewal moved once even if reachable twice. **Every read
  through `tx`** (conventions §8).
- **The key's space:** a retry of the same key for the same closure → the stored answer (201, nothing moved); the
  same key for another closure of the same space → as before; a key that extended **another space's** closure → 409
  `conflict`, checked before anything is read or moved, and not a leak of that space's data.
- **The owner's log (privacy):** only that space's entries; the admin and any non-member actor shown as «Masaha»
  (S1: decided by links, not by the role); `meta.actors` and the actor filter never name an admin (S4); reception
  403 before anything is read; a stranger and the admin `not_found` per AD-028.
- **The admin's log:** only allowlisted event types (default deny, S5) — check the allowlist line by line against
  the audit writer's actions: nothing space-private (a customer's name, a payment's amount, a reason) reaches the
  admin unless the plan allows it.
- **The queries:** the target search escaped for `LIKE`/`ILIKE` (`%`, `_`, `\`), bounded in length, inside the
  page's statement (S6); the period on Gaza's calendar; paging bounds; the count and the page from one consistent
  filter; the `LEFT JOIN`s don't multiply rows.
- **The shared schemas** (`@masaha/shared/audit`): the codes each refusal gives match the contract (`invalid_choice`,
  `too_long`, `out_of_range`, `invalid_format`); the actions and entity types lists match what the writer writes.
- **Tests:** a behaviour the plan names with no test, or a test that would pass with the bug (T-C1–T-C4, T1–T14,
  U1–U3; the breaks B-C1–B-C6, B1–B18, B12a — which were seen red, by the report).
- **The documents:** the contract (*Audit log*, the extension's preview, `201`, errors, `renewalIds`), data model
  (*AuditLog*, *ClosureExtension*, line 23), conventions §6 and §7, security, `features/audit.md` (new),
  `subscriptions.md` (#124 changed it too: both sides kept?), `v1-mvp.md`, `overview.md`, `docs/README.md`, findings
  151 (resolved) and 152 and the index — true to the code, one home per fact, the PR's number where it goes.
- **Scope:** `apps/api`, `packages/shared`, `docs` only; **no migration**, no dependency, no `apps/web` change.
  Commit subjects ≤ 50, each with a body; no `fixup!`, no tool attribution.

## Your output

```
# Review — FINANCE_AUDIT PR 1 (#<n>) — Claude Code
Head: <sha> · checks: <green/red> · head moved during the review: <yes/no>
Verdict: <mergeable | mergeable after a fix round | not mergeable>

## Findings (verified defects only, most severe first)
### F1 — <blocker|should-fix|nit> · <title>
- Where: <file>:<line> at <sha>
- Seen in the code: <what>      (or: Only in the report: <what>)
- Scenario: <inputs → wrong result>
- Fix: <what to change> · Belongs: <a fix round on this PR | worker B's next PR's first commit (0_CARRIED_FROM_<n>.md) | a finding (153 and on)>
(None → "None.")

## Carried items 1–4 as built
## Tests and breaks (one line each: present / missing / weaker; seen red per the report)
## Departures and decisions taken without the owner, judged
## Checked and fine
## Not checked, and why
```

Then stop.
