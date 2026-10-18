# S2b-3a — reply: alternative 2, and the data for the screenshots

**Alternative 2 (the "{name} restored" toast): approved** — it is the one the earlier reply already
listed under "approved". Keep it.

## The admin's sign-in
Reset the dev admin's password to `SEED_ADMIN_PASSWORD` **through the app's own forgotten-password
flow**, with `EMAIL_MODE=log` (the link in the API's log). `masaha_dev` only. Never print, paste or
quote the password or the reset link anywhere — not in your messages, the PR, the commits or a file.

## Real data before any interception
The screenshots should show the real server's answer wherever the data can be made:
- **Verified:** the demo seed already gives one — `SEED_DEMO=true` adds "Demo Space", verified, with
  its owner (`npm run db:seed`, which leaves existing rows unchanged). If `SEED_DEMO_PASSWORD` is not
  set in `apps/api/.env`, set it there yourself (never committed, never shown).
- **Stale:** move one or two fact dates back in `masaha_dev` by hand, with a one-off SQL statement
  (for example through `npm run db:studio` or `psql`): e.g. a space's `prices_updated_at` and
  `contacts_updated_at` a year back. No script in the repository, no change to the thresholds. The
  server then computes "stale" itself.
- **Unverified, hidden, missing groups:** through the API, as planned.
- **Interception** in headless Chrome only for what still can't be made this way (if anything);
  say in the PR which shots, if any, show an intercepted answer.

Then carry on as planned: the full lanes once on the head, the build with `check:build` and the
manifest's check for finding 27, the shots, the push, the PR. Stop every server afterwards.
