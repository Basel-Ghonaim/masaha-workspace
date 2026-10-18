# Review — PR #64 (AMENITIES: no amenity filter, and a space's own amenities)

You are an **independent reviewer** of PR #64 in the Masaha repository (Basel-Ghonaim/masaha).
Write your report to `C:\Users\basel\.prompt\MASAHA_AMENITIES\REPORT\REVIEW64_<YOU>_REPORT.md`, where
`<YOU>` is your tool's name in capitals (`OPENCODE`, `CODEX`, `COPILOT`, `CLAUDE`).

## Rules

- **Run from `C:\Users\basel\masaha`** (the main folder), never from `masaha-amenities` (the worker's)
  or any other worktree.
- **Read-only.** No edits, commits, checkouts, switches, installs, npm or test runs, database or
  Docker commands, and no GitHub comments. Read only from commit objects: `git fetch origin`, then pin
  to **the PR's current head**: `gh pr view 64 --json headRefOid`, written at the top of your report;
  check it again at the end, and if it changed, say so. Base: `git merge-base origin/main <head>`.
  Use `git diff <base>...<head> -- <paths>` and `git show <head>:<file>`.
- **Report concrete problems only,** each verified in the code: file and line, the failing scenario
  (input or interleaving → wrong result), the severity (**blocker / should-fix / nit**) and the fix.
  No praise, no summary. If unsure, say "plausible" and why.
- **No tool attribution** in what you write.

## What the PR must be (the owner's decisions)

The approved plan is `C:\Users\basel\.prompt\MASAHA_AMENITIES\PLAN\AMENITIES_PLAN.md` with its reply
`PROMPT\AMENITIES_PLAN_REPLY.md`; the worker's report is `REPORT\AMENITIES_REPORT.md`.
- **No amenity filter:** `amenities.is_filterable` dropped by a migration; the flag gone from
  `@masaha/shared/lookups`, `POST`/`PATCH /admin/amenities`, the public catalogue, the mappers, the
  repositories and the seed; the web's amenities tab without its «In filters» switch, badge, hook and
  copy; the documents (contract, data model, `lookups.md`, overview's *Directory* line, the plan's
  `GET /spaces` row, foundation, the root README) without an amenity filter; #16's decision recorded as
  superseded.
- **A space's own amenities:** a new table (`space_own_amenities`: Arabic name required, English
  optional, an order, `@@unique([spaceId, nameAr])`, cascading from the space), part of the amenities
  fact group. `PUT /admin/spaces/:spaceId/amenities` takes `{ amenityIds, ownAmenities }`, **both
  required** (a body without `ownAmenities` is 422, never a silent erase); replaced whole in order, on
  the one save path (the space's lock, `can()`, the date, the audit); at most 20, each name 1–60
  characters under the shared user-text rule; a repeated Arabic name 422 `not_unique` on its field; a
  save that changes nothing writes nothing, a new order is a change; the audit's `before`/`after` the
  whole group, older entries keeping `{ amenityIds }` (said in the contract). `AdminSpace` answers
  `ownAmenities` in order. Glossary: «مرفق إضافي».
- **Issue #63** in its own commit: `changeRole`'s comment names both locks; nothing else in `users`.
- No dependency; the web changes only what the shared types broke (the lookups feature, its copy, one
  fixture line elsewhere, one Combobox comment).

## Look at these, in this order

1. **The migrations:** the first one was **written by hand** (the worker generated its SQL with
   `prisma migrate diff`, because `migrate dev --create-only` refused a data-dropping migration). Check
   both against `schema.prisma` at the head: names, types, nullability, the unique index, the cascade,
   the foreign key's name, and that nothing else is altered or dropped. Order and timestamps.
2. **The amenities save path:** the own list read and replaced **under the caller's transaction and
   the space's lock** (the worker says no test can catch a write outside the transaction — judge the
   code itself); the no-op comparison (in order, `nameEn` absent vs `null`); the retired-amenity rule
   unchanged; the audit entry's shape; a missing group's first save.
3. **The read:** `facts.ts` and `space.mapper.ts` give `ownAmenities` in order under the share-locked
   read; nothing else of the space's read changed.
4. **The flag's removal is complete:** no `isFilterable` / `is_filterable` / "filter" left in code,
   tests, seed, copy or documents where it meant the amenity filter; a request still sending it is
   stripped, never stored.
5. **The shared rules:** the caps, `textSchema`, the repeat refusal path (`ownAmenities.<i>.nameAr`),
   `ownAmenities` required.
6. **The web:** the amenities tab still works (the Active switch, names, icon, order) with nothing
   orphaned (hooks, keys, copy lines, the `switches` slot removed everywhere it was used); the two
   catalogues have the same keys.
7. **The tests:** each would fail if its code broke; the worker says two tests could not be seen
   failing — judge whether anything is then unproven; expectations written by hand.
8. **The documents:** each states the code truly, one home per fact: the contract, the data model,
   `lookups.md`, `spaces.md`, conventions §7, the glossary, the overview, the plan, foundation, the
   README.
9. **The commits:** three; count each subject (≤ 50); `Closes #63` in the PR description.

## Your output

One file (the path above): a one-line verdict; the findings, most severe first (severity, file:line,
scenario, fix); a short "Checked and fine" list; then stop.
