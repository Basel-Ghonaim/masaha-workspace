# USERS — reply to your plan

A strong plan: the guard's design (a reader wired by the composition root), the admin-set lock in one
ordered statement, S4's gap in the password change, and finding 51 are exactly the kind of thing an
independent review would otherwise find. **Approved**, with the answers below. **First, save it** (as
approved here) to `C:\Users\basel\.prompt\MASAHA_WORKER_B\PLAN\USERS_PLAN.md` if it is not there yet,
then cut the branch and build.

## The owner's decisions (§13)

1. **S1–S7:** approved as recommended.
2. **Finding 39:** not folded; it stays for a small item of its own.
3. **The four codes:** names approved. Arabic approved for `OWN_ACCOUNT`, `LAST_ADMIN` and
   `ACCOUNT_HAS_LINKS`. **`GOOGLE_ONLY_ACCOUNT`, reworded** to match the catalogue's "باستخدام Google":
   «هذا الحساب يسجّل الدخول باستخدام Google فقط، وليست له كلمة مرور لاستبدالها.»
4. **Finding 51:** recorded as **Open**, with its *Resolves when* as you wrote it. 52 stays free.

## Reminders

- **D5 touches every signed-in request:** run the whole API lane, not only the new files, and say in
  the report any test whose expectation changed (the suspended case going from its code to 401, the
  token sites without `role`), each with why.
- **S3's 401:** in the real run, show the web-facing chain once with requests: the suspended account's
  next request 401, then its refresh refused, so the session ends.
- **Each race** made to fail once with its lock removed (testing §3 rule 7), the break named in the
  report; a break that does not fail as planned is reported as #60's B5a was.
- **The catalogue lines** are the only `apps/web` change; worker A stays out of the two files.
- **At the report:** `git merge-tree --write-tree` against every open PR (the design fixer's
  `design/admin-editor` will likely be open: it touches only `docs/design/`).
- **An independent review follows** (authorization, security, transactions). Don't merge.
- Stop every background shell you start; `jq` is not installed — use `gh … --jq`.
