# Review — PR #78 (SESSIONS: a session ends when it should — findings 51, 20, 16, 39)

You are an **independent reviewer** of PR #78 in the Masaha repository (Basel-Ghonaim/masaha), a
security change to the identity layer with one migration. If two reviewers run, they work apart; do
not read the other's report.
Write your report to `C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\REVIEW78_<YOU>_REPORT.md`, where
`<YOU>` is your tool's name in capitals (`OPENCODE`, `COPILOT`).

## Rules

- **Run from `C:\Users\basel\masaha-b`** and **read only commit objects.** No edits, commits,
  checkouts, switches, installs, npm or test runs, servers, database or Docker commands, no GitHub
  comments. **Do not run the tests:** CI ran every lane on this head and passed; your job is to read.
  `git fetch origin`, then pin to **the PR's current head** (`gh pr view 78 --json headRefOid` —
  expected `fe233f8`; write it at the top of your report and check it again at the end). Base:
  `git merge-base origin/main <head>`. Use `git diff <base>...<head> -- <paths>` and
  `git show <head>:<file>`.
- **Never open or print** any `.env` file.
- **Report concrete problems only,** each verified in the code: file and line, the failing scenario,
  the severity (**blocker / should-fix / nit**) and the fix. No praise, no summary. If unsure, say
  "plausible" and why.
- **No tool attribution** in what you write.

## What the PR must be (the owner's decisions)

API and documents; one migration; no dependency; nothing in `apps/web` or `packages/shared`. The
prompt is `C:\Users\basel\.prompt\MASAHA_WORKER_B\PROMPT\SESSIONS_PROMPT.md`; the approved plan
`PLAN\SESSIONS_PLAN.md` with its reply `PROMPT\SESSIONS_PLAN_REPLY.md`; the worker's report
`REPORT\SESSIONS_REPORT.md` (read its departures, and **its mistake: a `git checkout` wiped the
deadline's uncommitted code mid-build, which was reapplied from backups** — check that code with
extra care).
- **51 — a session version:** `User.sessionVersion`, carried by every access token; `requireAuth`
  refuses a token whose version is not the account's (401), and a token without the claim. **One
  function, `users.endSessions`, is the only path to deleting an account's refresh tokens,** and it
  bumps the version in the same transaction, under the session lock its caller holds. Every path that
  ends all sessions uses it: password change (the changer gets a token under the new version and
  stays), reset by email, suspension (restoring bumps nothing), role change (the admin's, and one that
  follows owner links), the admin's temporary password, the Google link, a refused refresh of a
  suspended account. **Sign-out ends only its own session** and bumps nothing. **The older check for
  a pending temporary password is kept** beside the version (the owner's S1). ADR 0003 has a dated
  *Revised* line.
- **20 — 30 days:** each refresh token row carries its family's `sessionEndsAt`, set at sign-in and
  copied on rotation; a refresh at or past it is refused, the family deleted, the cookies cleared;
  families existing at the migration get the migration's time + 30 days; expired families swept on
  the existing path (S3).
- **16 — the wait:** a forgotten-password request or a resend that delivers no email waits a random
  1.5–3.0 s (an estimate, not a measurement: finding 65); a delivered email adds no wait; the timer is
  a port wired in `app.ts` (four lines — the owner's stated exception, `app.ts` is also edited by PR
  #77); tests drive it without real waiting.
- **39:** `createUsersService` has no `passwords` parameter; the hashing is the module's own.
- `schema.prisma` also drops "and photos" from `Space.profileUpdatedAt`'s comment (for the media
  item).

## Look at these, in this order

1. **No surviving token.** From the code, list every place that deletes an account's refresh tokens
   or changes what the account may do (password, reset, suspension, role, temporary password, Google,
   link changes that move the role, anything else you find). Does each go through `endSessions`, in
   the same transaction and under the session lock? Can any path delete refresh tokens without the
   bump, or bump outside the transaction (a crash between them)? Is the changer's new token signed
   with the version read **after** the bump?
2. **The guard.** `requireAuth` reads the account and compares the version on every signed-in request;
   a missing, non-integer, negative or forged claim is refused; the version cannot be supplied by the
   client in any other way; 401 (not 403) so the web refreshes. Races: a refresh waiting on a password
   change's lock; a sign-in waiting on a role change's lock — do the two race tests really race?
3. **The deadline.** Set at sign-in only, copied on every rotation (never renewed), checked under the
   lock at refresh, the family deleted and the cookies cleared past it; the boundary (at the deadline,
   and 1 ms before); the migration's backfill and `NOT NULL` order safe on a live table; the
   migration applies cleanly on PostgreSQL/Neon.
4. **The wait.** Every path that delivers nothing waits (no account, suspended, a cap refusal, a
   failed send, a resend with no account); a delivered email does not; the draw is uniform within the
   bounds and varies (`crypto.randomInt`); the timer port is the only seam (no parameter only tests
   pass — testing §3 rule 2); nothing runs after the response (ADR 0014); the dropped unit test of the
   draw — is the API lane's proof enough?
5. **Finding 39.** No parameter left; the unit tests moved or covered as the plan lists; no behaviour
   lost (a password-less account still spends a comparison).
6. **The tests.** Each security property's test would fail with its break (the report claims 15
   breaks made); expectations by hand; the fixture changes in `test/admin.ts`, `test/spaces.ts`,
   `spaces/space/space.api.test.ts` necessary and harmless.
7. **The documents.** security.md (*Tokens and cookies*: the version, both checks, sign-out's own
   15 minutes, 30 days; *Passwords*: the wait, its estimate, development's reversed tell, the accepted
   residual), ADR 0003's *Revised* line, the data model (two columns), conventions (the timer port,
   R5, §11, §12), the contract's 401 wording, `users.md`, `auth.md`, findings 51, 20, 16, 39 resolved
   and 65 recorded, the index — each true to the code, one home per fact.
8. **The commits:** four; count each subject's characters yourself (≤ 50, no exception).

## Your output

One file (the path above): a one-line verdict; the findings, most severe first (severity, file:line,
scenario, fix); a short "Checked and fine" list; then stop.
