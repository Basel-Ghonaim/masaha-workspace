# OWNERS — review fixes for PR #60

From the independent review of head `ca3d42b` (`REPORT\REVIEW60_CLAUDE_REPORT.md`). Every item below
was verified against the code by the analyst. No blocker; the temporary password, the guard, the
lock order, the revocation, finding 25 and the history rewrites were checked and hold.

**How:** each fix folds into the commit it corrects (fixup + autosquash), then `git push
--force-with-lease`; ONE "Review fixes" comment on the PR; a "Review fixes" section in
`REPORT\OWNERS_REPORT.md` (`open-pr` step 8, `final-report` step 5). Every new or changed test is
seen failing first, by breaking the code it names once (testing §3 rules 5–7). **Checks:**
`test:unit`, `test:api`, `lint`, `typecheck`, `format:check`, `check:links` — once each on the new
head (no web code changes, so no component lane or build). Then `git merge-tree` against the open
PRs. Stop every background shell you start; `jq` is not installed — use `gh … --jq`.

## R1 — Four commit subjects are over 50 characters

`af24445` (57), `ca3d42b` (57), `d84f500` (53), `49bdb41` (51). Reword them in the same rebase
(non-interactively), keeping each its type and scope, e.g.:
- `feat(space-links): add an owner's account` (41)
- `refactor(api): share the signed-in claims helper` (48)
- `feat(space-links): link and unlink owners` (41)
- `feat(users): record the password's handover` (43)

Count each after the rebase.

## R2 — The users list's total under a filter is never asserted

`users.repository.ts:98` counts with the list's `where`, but only the unfiltered paging test checks
`meta`. `db.user.count()` would pass every test. **Fix:** in the role/state `it.each`
(`adminUsers.api.test.ts:194-207`) and one `q` case, also assert `meta.totalRecords` (written by
hand). Break: drop `where` from the count once.

## R3 — The order of the add refusals is untested without `upgradeExisting`

The contract (§5, `POST /admin/owners`) gives the order `ACCOUNT_IS_ADMIN` → `ACCOUNT_SUSPENDED` →
`ALREADY_OWNER` → `EMAIL_HAS_ACCOUNT` → `RECEPTION_LINK_ACTIVE`, but every refusal test sends
`upgradeExisting: true`. **Fix:** run the admin/suspended/owner `it.each`
(`adminOwners.api.test.ts:505-520`) with and without the flag, expecting the same code; add a
reception account **without** the flag expecting `EMAIL_HAS_ACCOUNT`. Break: move the
`!upgradeExisting` check above `assertMayOwn` once.

## R4 — Two adds of the same email at once: the documented 409 has no test

`adminOwners.service.ts:154-157` answers `EMAIL_HAS_ACCOUNT` when another creation took the email
between `findByEmail` and the insert (contract: "also when another creation took the email
meanwhile"). Removing it turns the 409 into a 500 (`account.id` on `null`) with nothing failing.
**Fix:** interleave as the file's lock tests do: hold the chosen space's row in a test transaction,
send `add(NEW)` (it passes `findByEmail` and waits on the space), insert that email through `prisma`
and commit, release; expect 409 `EMAIL_HAS_ACCOUNT`, no new link, no audit entry. Break: remove the
branch once.

## R5 — The log test does not prove the redaction; and the report claims it did

pino-http logs no request or response body, so the API test "no log line and no audit entry" passes
with `'temporaryPassword'` removed from `SECRET_FIELDS`. It proves that nothing logs the password, not
that the redaction works, which security.md states. **Fix:** add `temporaryPassword` to the `it.each`
of `apps/api/src/shared/http/requestLogging.unit.test.ts` (which logs the field through the real
logger), and check every entry of `SECRET_FIELDS` has its case there (the verifier saw `newPassword`
missing). Keep the API test, its title true to what it proves. **In the report**, correct the break
row "The answer logged with the redaction removed": say exactly what was changed to make it fail.

## R6 — An owner whose only space is deleted cannot be made a user again

`countOwnerLinks` counts a soft-deleted space's links for the role (by decision); unlink answers 404
on a deleted space; the users row shows `spaces: []`; no role change exists. The only way out is
restore → unlink → delete again, and nothing says so. The documents also contradict themselves:
`space-links.md:72` ("A link to a deleted space counts for nothing, in the session's links too") and
`api-contract.md:362` (DELETE space, "every link to it counts for nothing") are unqualified, while
`space-links.md:82` and the contract's line 402 make the role an exception.

**The owner's decision: option A — keep the behaviour, fix the documents, record the finding.**
Narrow line 72 and the contract's line 362 to access and the lists (the role still counts the link);
write the consequence and its way out (restore → unlink → delete again) into the decision at line 82;
record **finding 50** (open) for it, with the index line. No code change.

## R7 — Documents the PR left stale (all in words — a code map never lists symbols, documentation §5–§6)

- `space-links.md` *Authority* (line 4): add the users list and the owners (add, link, unlink), and
  link the contract's new sections, not only *Managed spaces*. *Who uses it* (line 23): adding an
  owner is not a route on one space. *Shared* code map (line 107): "…, the users list's query and its
  rows, and the owner's add and link requests and the added owner". Line 38: the lock sentence holds
  for a link change on an existing account; a new account's row is inserted under the space's lock.
- `users.md` *Authority* (line 4): add the admin's accounts and the handover, and link the contract's
  *Users (the admin)*. *Who uses it*: add the admin (the handover). *Shared* code map (line 72): add
  "the handover's request". Line 9: "for the admin with a temporary password" reads as an admin's
  account — say "an account the admin creates".
- `conventions.md` header (line 3): §13's built parts gain "the space's lock". Line 343: "A link
  change on an existing account takes the person's row…".
- `adminOwners.service.ts:22-25`, the doc comment: the same scoping as line 343.

## The owner's answers

- The Arabic of the five new codes: **approved**.
- R6: **option A**, finding 50 recorded.
