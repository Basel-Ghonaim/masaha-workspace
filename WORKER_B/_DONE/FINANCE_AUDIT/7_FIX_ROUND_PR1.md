# FINANCE_AUDIT PR 1 (#128) — the fix round, in full (short)

You are worker B's executor, back on your own PR **#128** (`feat/audit-log`, head `3f8a2184`). Its Claude review
(`C:\dev\masaha\workspace\WORKER_B\FINANCE_AUDIT\6_REVIEW_PR1_CLAUDE_CODE.md`) says **mergeable after a fix round**.
**The owner's decision (2026-10-28):** **F1, F2 and F3 are fixed in this round, nothing carried**; F1's writer change
may touch `users` and `space-links` (outside the plan's file list — allowed by the owner for this fix only). **Keep
the round short.** The supervisor confirmed F1 in the code. Read the review's *Findings* section whole, then this
file; nothing else unless a fix needs it (search first, read the section). Do not run the `start-work-item` skill.
Already decided by the owner, not to touch: the four `q`-over-all-time reads over 150 ms are accepted without an
index; finding 152 stays Open.

## 0. The rule for this run — no stop until ready for review

**The autonomy rule applies** (`C:\dev\masaha\workspace\_SHARED\AUTONOMY_2026-10-25.md`): you do not stop and you do
not ask until #128 is ready for review again (pushed, CI green on the new head, `CLEAN`, the report and the PR's
description updated, the final reply sent). A choice a fix leaves open → decide, record under *Decisions taken
without the owner* (met, options, chose, why, undo), continue. Hard limits: never merge, push to `main` or force-push
another branch; never change data through the app, API or database, never reseed (rows already written with no
space stay as they are); never skip or weaken a test, config or lane; never print a secret; no tool attribution; no
migration. Never stop for the file count — give it in the reply.

## 1. The base

`main` = `0ec43b61` (#127 merged: `apps/web` and documents; `git merge-tree` with your head was clean and #128 is
`CLEAN`). `git fetch origin`; `gh pr view 128 --json mergeStateStatus`. **Rebase only if it is not `CLEAN`** (then
`git rebase origin/main`, a document conflict → keep both sides' lines, record it; `npm run build -w
@masaha/shared`). Make `backup/audit-log-pre-review-fix` at `3f8a2184` before the first fold. Never `git checkout
-- <file>`, `stash` or `reset --hard` (restore from a backup copy); no rebase left in progress at the end.

## 2. The fixes — each folded into the commit that made it

The owner's method: **a fix is folded into its original commit** (`git commit --fixup=<sha>` then
`GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash origin/main`), never a new fix commit; no `fixup!` left; every
subject unchanged (check after each autosquash). Expected homes (check with `git log -L` / `git blame`): F1 →
`feat(audit): read the platform's audit log` (the allowlist's promise and T10–T14); F2 → `feat(audit): read a
space's audit log` (where `audit.md`'s *The target* was written); F3 → `fix(subscriptions): move unstarted renewals
too` (the lock line).

1. **F1 (blocker, privacy) — a space's staff account's events are the space's.**
   - **Sweep first:** every writer of each action in `PLATFORM_ACCOUNT_ACTIONS` (`git grep` the action names in
     `apps/api/src`) — for each, can it concern an owner's reception account? The review names two:
     `users.createWithTemporaryPassword`'s `user.created` (called by `staff.service.ts` `add` and by
     `adminOwners.service.ts:151`) and the forced change's `user.emailChanged` (`users.service.ts` ≈ 671–683). Any
     other found → fixed the same way, recorded.
   - **The writer names the space:** `createWithTemporaryPassword` takes an optional `spaceId` that `staff.service.ts`
     `add` passes (its space); the admin's owner creation passes none (the platform's). The forced change's
     `user.emailChanged` names the space of the account's **reception** link when it has one (one desk per person,
     ADR 0009 rule 4 / finding 84), read through `tx`; an owner's or a user's names none. Same for any other writer
     the sweep finds. `AuditEntry.spaceId` already exists — no schema change.
   - **Tests through the real routes** (not inserted rows), in the admin's audit API test file: an owner adds a
     reception account → `GET /admin/audit-log` does not list its `user.created`, and the owner's
     `GET /manage/spaces/:id/audit-log` does (actor the owner, named); that person's forced change with a corrected
     email → absent from the admin's log, present in the owner's; the admin creating an owner → still in the admin's
     log (unchanged). **Red before the fix** (record the line), green after; a break (the `spaceId` dropped from the
     staff call) red.
   - **Documents:** `audit.md`'s *Why* line (≈ 48, "An account's event is the platform's only when it names no
     space") to say the staff account's creation and its forced email correction name the space; the contract and
     conventions §6 if their wording needs it (they already say "never its staff" — check they are now true).
2. **F2 — `audit.md:35` says what the code does:** one `LEFT JOIN` per entity type, its type in the join's
   condition, so at most one matches (a visit's and a check-in's customer joined through them); the names by
   `coalesce`; not a lateral subquery — a search over a year reads each table once. One *API decisions* line for the
   choice (why: the measured `Memoize` miss), dated `2026-10-27, #128`.
3. **F3 — `subscriptions.md`'s lock line:** keep its `2026-10-26, #123` and append "The renewals not started with
   them, 2026-10-27, #128." (or split it as the key line does).

## 3. What runs — the owner's rule for this round

- **Only the test files the fixes touch** (`npm run test:api -w @masaha/api -- <files>` on `masaha_b_test`;
  `test:unit -- <files>` if a unit test is touched), plus `npm run lint`, `npm run typecheck`, Prettier on the
  touched files, `npm run check:links` (documents touched), `npm run build -w @masaha/shared` if shared changes. Each
  new test seen **red** before its fix, green after.
- **No full lane locally.** **CI on the pushed head judges the rest.** A red CI lane → read why, fix, fold, push
  again.
- **No real run** (the fixes are proven by their tests); the local data stays as it is.

## 4. Push and the end

- `#128` is known: write it directly; `git grep '#PRNUM'` on the head → nothing.
- `git push --force-with-lease=feat/audit-log:3f8a21845c3d435b845674d950dab2f5fc3bf7cd` (your own branch only; if you
  pushed in between, lease on that sha).
- Wait for CI on the new head (`gh pr checks 128 --watch`, bounded; no command timeout); green and `CLEAN`. Not
  `CLEAN` because `main` moved → §1, push again.
- Update the PR's description (`gh pr edit 128 --body-file …`): a *Review fixes* section — F1–F3 and how each was
  fixed (F1's sweep and the writers changed).
- Append to `4_REPORT_PR1.md` a section *The review's fix round (2026-10-28)*: the base, each fix (its commit, the red
  line, the green line), the runs, the push, CI, *Decisions taken without the owner* for this round.
- Leave no rebase in progress; `git status --short` clean; name every `backup/*` branch you made.

## 5. Your final reply

```
Status: READY FOR REVIEW | INCOMPLETE (only if nothing at all could continue)
PR: #128 · head <sha> · CI <green/red> · <CLEAN/not CLEAN> · files <n>
Rebased: <yes, on <sha> / no, CLEAN>
Commits: <sha> <subject> (<chars>) — all, after the folds
Fixes: F1 — <the writers changed, the sweep's result; folded into <sha>; test red then green, break red> ·
       F2 — <sha> · F3 — <sha>
Ran: <each command with its result line>   (touched files only, by the owner's rule)
CI on the head: <each lane>
Decisions taken without the owner: <each>   (or "none")
Backup branches: <names>
Report: C:\dev\masaha\workspace\WORKER_B\FINANCE_AUDIT\4_REPORT_PR1.md
```
