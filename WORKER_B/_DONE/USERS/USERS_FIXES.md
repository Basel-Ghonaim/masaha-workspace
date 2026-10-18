# USERS — review fixes for PR #62

From the independent review of head `50fdcea` (`REPORT\REVIEW62_CLAUDE_REPORT.md`); the two
should-fix items were verified in the code by the analyst. No blocker.

**How:** each fix folds into the commit it corrects (fixup + autosquash), then
`git push --force-with-lease`; ONE "Review fixes" comment; a "Review fixes" section in
`REPORT\USERS_REPORT.md`. New or changed tests seen failing first. **Checks:** `test:unit`,
`test:api` (the whole lane: the guard touches every route), `lint`, `typecheck`, `format:check`,
`check:links`, once each on the new head. Then `git merge-tree` against every open PR (#61, and the
amenities item's PR if it is open by then). Stop every background shell; `jq` is not installed — use
`gh … --jq`.

## R1 — A person issued a temporary password while signed in is stuck for up to 15 minutes

`requireAuth.ts`: `pending = claims.mustChangePassword || account.mustChangePassword` answers 403
`PASSWORD_CHANGE_REQUIRED`. When only the **account** says so, the token predates the temporary
password, whose issue ended every session; the web acts only on its session's pending flag and
refreshes only on a 401, so the tab shows errors until the token expires, and the change page asks
for a current password the person no longer has. **Fix:** account pending and token not pending →
**401** (as for a suspended account: the web's refresh then fails and the session ends); token pending
→ 403 as today. Update the guard's unit and API tests (including the one that sets the flag without
replacing the password), `security.md` and the contract's guard line.

## R2 — The test trigger can outlive its test

`governorates.api.test.ts` › `whileAuditRefused` creates the function and the trigger outside the
`try`, without `OR REPLACE` / `IF EXISTS`; a killed run leaves them, the reset only empties tables,
and every later audit write fails in every run. **Fix:** `DROP TRIGGER IF EXISTS` and
`DROP FUNCTION IF EXISTS` first, then `CREATE OR REPLACE FUNCTION` and the trigger **inside** the
`try`; the `finally` drops both with `IF EXISTS`.

## R3 — The documents (the review's nits)

- **A restore revives old tokens.** Finding 51 and `security.md` say a suspension cuts existing tokens
  at once; that holds only while it lasts: restored within 15 minutes, a token signed before the
  suspension works again. Say so in both, and add it to finding 51's evidence (its *Resolves when*
  — a stored "sessions ended at" — covers it).
- **Conventions §13** says a link change never takes an admin's row; it takes it briefly before
  refusing the admin. Correct the sentence.
- **A demoted admin's open dashboard** shows 403s until the token expires: the server is right; the
  web's handling is recorded in finding 51's evidence too (no new finding).

## R4 — The race tests wait a fixed time (record, do not fix)

The race tests (this PR's and #60's) wait a fixed 2 s for the request to block, rather than checking
it is waiting on the lock; a slow run could pass a race with no interleaving. Record **finding 52**
(Open): *Resolves when* the race tests wait until the request is seen waiting on a lock (for example
`pg_stat_activity.wait_event_type = 'Lock'` for its backend), with a timeout. One helper for every
race test is its own small item.
