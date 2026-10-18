# SESSIONS — reply to your plan

A strong plan: every path that ends sessions found in the code (the Google link included, which the
prompt missed), one `endSessions` as the only way to `revokeAll`, the deadline that is not capped into
the token's own expiry for a reason you state, the wait only when nothing was delivered, and each
moved unit test accounted for. **Approved**, with the owner's answers and three changes below.
**First, save it** (as approved here, with these changes folded in) to
`C:\Users\basel\.prompt\MASAHA_WORKER_B\PLAN\SESSIONS_PLAN.md`, then cut the branch from
`origin/main` (check it is still the latest) and build.

## The owner's decisions (§13)

1. **O1 — (a), the three lines in `apps/api/src/app.ts` are allowed** (the owner's stated exception to
   workflow §9 rule 3; the media worker edits that file too). To keep the overlap small and its
   resolution cheap:
   - put them **in commit 4 only**, and nowhere else in `app.ts`;
   - **if the media PR merges first and yours then conflicts:** rebase, keep both sides, run
     **`lint` and `typecheck` only** (workflow §9 *Conflicts*: a conflict in code adds those two to
     the fast path), push once with `--force-with-lease`, and let CI run the lanes. **No local test
     lane for that rebase**, no new round: the owner does not want a conflict of three lines to cost a
     full verification. Target: about fifteen minutes. If the conflict reaches beyond `app.ts`'s
     lines, stop and say so.
2. **O2 — the SMTP keys are in your folder:** the analyst copied `SMTP_HOST`, `SMTP_PORT`,
   `SMTP_SECURE`, `SMTP_USER`, `SMTP_PASSWORD` and `EMAIL_FROM` into
   `C:\Users\basel\masaha-b\apps\api\.env` (values never printed). `EMAIL_MODE` is not set: set it to
   `smtp` only while measuring, then remove it. Each real send goes to a real inbox: use the seeded
   admin's or a demo account's address, about 8 sends, no more.
3. **S1 — keep the "account pending, token not" 401** as defence in depth (the owner: zero cost, and
   it still guards a future path that sets a temporary password without ending sessions, such as the
   owner's reception passwords). Its unit test stays; security.md names both checks.
4. **S2–S7 — approved** as recommended.

## Three changes

- **Commit 2's subject is 51 characters** (counted): `feat(sessions): end a session 30 days after
  sign-in`. Shorten it, for example `feat(sessions): end a session 30 days on` (41). Count every
  subject before each commit.
- **The measurement's place:** a send measured from this machine travels over the owner's connection
  in Gaza; online, the API sends from Vercel's data centre, likely much faster. Bounds taken from here
  could make an unknown email's answer **slower** than a real send online — the reverse tell. So:
  keep the bounds in the one constant `NO_SEND_WAIT`, say in security.md that they were measured
  locally, and **record finding 65**: "The forgotten password's wait was measured from a development
  machine" — *resolves when* the send is measured on the deployment and the bounds set from it.
- **Development's reverse tell** (your Review Focus, `EMAIL_MODE=log`): one sentence in security.md
  that it is development only.

## Reminders

- Every security property's break made once and restored (testing §3 rule 7); every new test seen
  failing first.
- **One full test run at a time:** before `test:api`, check that worker A (main folder, a review-fixes
  round now) and the media worker (`masaha-media`) run no lane; if one does, wait.
- Read the `.env` by keys only; never print a value, a token or the SMTP password; leave `EMAIL_MODE`
  as you found it.
- An independent review follows (security, the schema). Don't merge. At the report,
  `git merge-tree --write-tree` against every open PR (the media PR's `app.ts` will show; say so).
  Stop every background shell you start; `jq` is not installed — use `gh … --jq`.
