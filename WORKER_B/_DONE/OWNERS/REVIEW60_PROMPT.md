# Review — PR #60 (OWNERS: the admin's owner accounts and their links to spaces, API)

You are an **independent reviewer** of PR #60 in the Masaha repository (Basel-Ghonaim/masaha).
Three reviewers work on it separately; this prompt is for each.
- **If you are Copilot,** write your report to
  `C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\REVIEW60_COPILOT_REPORT.md`.
- **If you are OpenCode,** to `C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\REVIEW60_OPENCODE_REPORT.md`.
- **If you are Codex,** to `C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\REVIEW60_CODEX_REPORT.md`.

## Rules

- **Run from `C:\Users\basel\masaha`** (the main folder), not `masaha-b` or `masaha-design`.
- **Read-only.** No edits, commits, checkouts, switches, installs, npm or test runs, database or
  Docker commands, and no GitHub comments. Read only from commit objects: `git fetch origin`, then
  pin to the head **`ca3d42b`** (`gh pr view 60 --json headRefOid` must still say
  `ca3d42b98167fbbced18e976bfbbc15a92033b66`; if it does not, stop and say so). Base: `b66ddfe`.
  Use `git diff b66ddfe...ca3d42b -- <paths>` and `git show ca3d42b:<file>`.
- **Report concrete problems only,** each verified in the code: file and line, the failing scenario
  (input or interleaving → wrong result), the severity (**blocker / should-fix / nit**) and the fix.
  No praise, no summary of the PR. If you are not sure, say "plausible" and why.
- **No tool attribution** in what you write.

## What the PR must be (the owner's decisions)

API only (plus the error codes' lines in the web's two catalogues). 6 commits, 55 files, no schema
change, no new dependency.
- **Add an owner** — `POST /admin/owners`: creates an account with a **temporary password** (Node's
  `crypto`, meets the password policy, `mustChangePassword`), returned **once**, in that answer only
  (`Cache-Control: no-store`), never in a log, an audit entry or an error; **or**, when the email has
  an account, refuses with 409 `EMAIL_HAS_ACCOUNT`, and upgrades it only when the request says so
  (`upgradeExisting: true`), keeping its name and password. Either way it links **one** space, in
  **one transaction**, and the space becomes verified. The body's space unknown or soft-deleted →
  422 `errors.spaceId = ["invalid_choice"]`.
- **Refusals:** already an owner (409 `ALREADY_OWNER`), an admin (409 `ACCOUNT_IS_ADMIN`), a
  suspended account (409, the existing `ACCOUNT_SUSPENDED`), an active reception link at that space
  (409 `RECEPTION_LINK_ACTIVE`); a path's space unknown or deleted → 404.
- **Link** — `POST /admin/spaces/:spaceId/owners`: any person (owner or user); a user becomes an owner.
  Re-linking an active link is idempotent (204, nothing written). A deactivated row of the same
  `(spaceId, userId)` is reactivated; a deactivated **reception** row becoming an owner's is audited
  with `before: { role: "RECEPTION" }`.
- **Unlink** — `DELETE /admin/spaces/:spaceId/owners/:userId`: sets `deactivatedAt`, never deletes;
  unlinking the last owner is allowed and the space is unverified again.
- **The global role follows the links (ADR 0009 revised):** the first active owner link makes a
  person `OWNER`, the end of their last makes them `USER`; each such change **ends their sessions**.
  An unlink that leaves other owner links changes no role and ends no session (the links loader reads
  the links on every request).
- **Handover** — `POST /admin/users/:userId/temporary-password/handover` `{ channel: WHATSAPP |
  IN_PERSON | OTHER }`, written to the audit; refused once the temporary password is no longer pending
  (409 `TEMPORARY_PASSWORD_NOT_PENDING`).
- **Read** — `GET /admin/users`: paged (20), composed, `q` on name or email, `role` and state filters;
  each row its active owner links only (a deleted space's link counts for nothing).
- **Finding 43 resolved:** every link change takes the space's row lock (`FOR NO KEY UPDATE`), so
  `can()` decides on the links under it; the space's read takes a share lock (`FOR SHARE`) — the
  owner's choice over a snapshot. **Lock order:** the space's row, then the person's row.
- **Finding 25 folded** (last commit): the signed-in claims read from `shared/auth`, one helper.
- **Every endpoint** is behind `/admin`'s one guard; audited in the change's own transaction.
- **Project rules:** module levels (`users` L1, `space-links` L2; a lower level never imports a
  higher); no repository injected for tests, no parameter only tests pass, no `vi.mock`; one
  behaviour in one lane; every authorization rule tested as guest, USER, OWNER, ADMIN with a pending
  password change, and ADMIN; commit subjects ≤ 50 characters.

## Look at these, in this order

1. **Security of the temporary password:** generation (entropy, the policy, no modulo bias); every
   path it could leak by — the request log and its redaction, the audit's `before`/`after`, error
   envelopes, a thrown error's message, the idempotent replay, the upgrade path; `no-store`.
2. **Authorization:** each new route really behind the admin guard and the pending-change gate; an
   admin cannot be linked or demoted through these routes; a suspended account cannot be made an
   owner; nothing lets an OWNER act here.
3. **Transactions and races (the core):** the lock order everywhere (link, unlink, add, a facts save,
   a session refresh, the handover) — can any two of them deadlock or interleave wrongly? Two
   concurrent unlinks of a person's two last links; a link racing an unlink of the same person; a
   sign-in or refresh racing a role change (does a session opened meanwhile survive the role change?);
   `ownerRoleFor` and the role write; the re-activation of a deactivated row.
4. **Session revocation:** every role change ends the sessions, in the same transaction, after the
   role is written; nothing else ends them.
5. **The users list:** the composed read (one query per module, no N+1), the filters, the total right,
   deactivated and deleted-space links excluded, an unknown `role` or state.
6. **Finding 25's refactor** and the loader taking `tx`: any route left on the old helper or a caller
   not passing its transaction.
7. **History rewrites — check the content survived:** the worker reports (a) `spaceLinks.ts` was
   **rewritten from memory** after a `git checkout` lost an edit, (b) the PR number was rewritten
   #59 → #60 across all six commits with a tree filter, (c) Python edits wrote **CRLF** and were
   converted back. Look for lost or duplicated code, CRLF in any file, and a stray citation of #59.
8. **The tests:** each would fail if its code broke; the race tests really interleave (not just run
   in sequence); titles true to their assertions. The worker says the remaining assertions of the
   list and refusal tests were not each broken one by one — name any that would pass with its code
   removed.
9. **The documents:** `api-contract.md` (endpoints, payloads, codes §6), `security.md` (revocation,
   the temporary password), `conventions.md` §13, ADR 0009's *Revised* line, `data-model.md`,
   `features/space-links.md`, `users.md`, `spaces.md`, `plans/v1-mvp.md`'s API table, `overview.md`,
   findings 43 (resolved), 25, 49 (new) and the index — each states the code truly, one home per fact.
10. **The commits:** six; count each subject. Four already look over 50 characters.

## Your output

One file (the path above): a one-line verdict; the findings, most severe first (severity, file:line,
scenario, fix); a short "Checked and fine" list; then stop.
