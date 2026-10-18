# AMENITIES — reply to your plan

A strong plan: the whole-group save on the one path, S1 (no silent erase), and the no-op compared in
order are right. **Approved**, with the answers below. **First, save it** (as approved here) to
`C:\Users\basel\.prompt\MASAHA_AMENITIES\PLAN\AMENITIES_PLAN.md` if it is not there yet.

## The state has moved: PR #62 is merged

`main` is now **`4ce6310`** (#62, the users item). Your worktree has been moved there, detached, and
its shared `dist` rebuilt (#62 changed no schema and no dependency: no migration to apply, no
`npm ci`). So:
- run `git fetch --prune origin`, check `HEAD` is `origin/main` (`4ce6310`) and the tree clean, then
  cut `feat/space-own-amenities` from it;
- **the shared documents no longer conflict:** #62's lines in `api-contract.md`, `overview.md` and
  `v1-mvp.md` are in `main`; build on them. Drop the plan's notes about resolving them by the fast
  path. The only other open PR is #61 (`docs/design/` only).

## The owner's decisions (§13)

1. **Names:** `ownAmenities` / `OwnAmenity` / `SpaceOwnAmenity` / `space_own_amenities` — approved.
2. **Caps:** at most 20, each name 1–60 characters — approved.
3. **S1–S6:** approved as recommended.
4. **The glossary's Arabic:** **«مرفق إضافي»** (an *own amenity*), not «مرفق خاص»: «خاص» reads as
   "private" (a private room), while «إضافي» says it is added beside the common list — the words an
   owner will see («أضف مرافق إضافية»).
5. **Design issue 1:** remove the card's line — approved.
6. **The Combobox comment** in `shared/design-system`: approved (one line; it would otherwise state
   what is no longer true).

## Two additions

- **The audit's shape changes** for `space.amenitiesEdited` (`{ amenityIds }` → `{ amenityIds,
  ownAmenities }`); entries written before keep the old shape. Say it in the contract's line for the
  route, so the audit screen (later) reads both.
- **Issue #63, in a third commit of its own (the owner's decision, outside your scope on purpose).**
  #62's review left one nit: the doc comment of `changeRole` in
  `apps/api/src/modules/users/users.service.ts` names only `lockAccount`, while its second caller
  (`space-links/admin-roles/adminRoles.service.ts`) takes `lockForAdminChange`, which also holds every
  active admin's row. The owner sends it with the first PR that touches the API layer: yours. Make the
  comment name both locks; nothing else in `users`. Commit it alone as
  `chore(users): name both locks in changeRole` (≤ 50), say in the PR description that it is #62's
  leftover carried here, and put `Closes #63` there.

## Reminders

- **The design archive** still draws an amenity filter: say so in the report only; the analyst routes
  it to the design batches.
- At the report, `git merge-tree --write-tree` against every open PR (#61, and worker A's if open).
- An independent review follows (the schema). Don't merge. Stop every background shell you start;
  `jq` is not installed — use `gh … --jq`.
