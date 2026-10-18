# AMENITIES — the database refuses a price of zero too (a fifth commit)

The fourth commit is approved as built: **`out_of_range` is the right code** (the shared vocabulary
has no `too_small`; the analyst's prompt was wrong there).

**The owner's decision on your second point: yes.** The database must refuse a price of 0 itself, as
the payments' check already does (ADR 0015: the database owns the amounts' rules). This PR is the
only one in flight allowed to change the schema (workflow §9, the new rule's condition 1), so it is
done here, now, in a **fifth commit of its own**.

- **The migration:** `space_prices_amount_check` changes from `"amount_agorot" >= 0` to
  `"amount_agorot" > 0`. Prisma does not model check constraints, so `migrate dev --create-only` will
  find no change: create the migration folder by hand, its timestamp after
  `20261012123800_space_own_amenities`, named `…_space_price_above_zero`, its `migration.sql`
  dropping the constraint and adding it again with `> 0`, one comment line saying why. No other
  table changes (the desk's packages, subscriptions and visits keep `>= 0`: their steps decide).
- **Apply and check:** `migrate deploy` to `masaha_amenities_dev`; `migrate status` clean; the API
  lane applies it to `masaha_amenities_test`; a clean run on an empty scratch database as before
  (`createdb`, `migrate deploy`, `dropdb`); `prisma migrate diff` from the migrations to the schema
  shows no drift.
- **The test:** in the API lane, a raw insert of a price of 0 into `space_prices` (through `prisma`,
  bypassing the API) is refused by the database's check; seen failing first against the old
  constraint.
- **The documents:** `data-model.md` › *Conventions* › *Prices*: "Amounts are integers in agorot, above
  zero, …" (one home; the contract's line already says 1 to 10,000,000).
- **Commit:** `feat(db): refuse a zero price in the database` (≤ 50), alone, after the four; add it
  to the PR description beside the fourth.
- **Checks:** `test:api`, `lint`, `typecheck`, `format:check`, `check:links` once on the new head;
  say why the unit and component lanes and the build are not rerun (no code outside the migration
  and its test; CI runs them). Plain push, CI green and `CLEAN`, a section in
  `REPORT\AMENITIES_REPORT.md`, `git merge-tree` against every open PR (#64 is the only one now).
  The analyst reviews this commit. Don't merge. Stop every background shell you start; `jq` is not
  installed — use `gh … --jq`.
