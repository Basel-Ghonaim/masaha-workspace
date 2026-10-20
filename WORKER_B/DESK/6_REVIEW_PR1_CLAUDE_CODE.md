# Review — DESK PR 1 (#94, `feat/live-status`)

**Head:** `e07308b4e6099283572ff9c4dbf9a4c1cb5673b3` — CI green on it (lint, format:check, typecheck,
test:unit, test:component, check:classes, check:links, build, test:api; CodeRabbit skipped), `CLEAN`.
The head was the same at the start and at the end of the review.

**How:** one reviewer, both halves in order, with no subagents (the owner's change to the prompt, to save
tokens). I read `git diff origin/main...e07308b4` once, then the head's own files where a finding needed
them (`directory.service.ts` `page`, `can.ts`, `hours.repository.ts`, ADR 0008, `v1-mvp.md`,
`security.md`, `conventions.md` §9). This ran from `C:\dev\masaha\app-b`, not `app-design`: the owner
pointed this conversation there, and I only read commit objects (`git show`/`git diff`). Nothing was
checked out, run or edited.
**Seen in the code** unless marked *(report only)*: the red runs, the breaks and the real run were read in
`4_REPORT_PR1.md` and are not re-proven here.

## Verdict

**Ready to merge after a small fix round:** no blocker. Two documents now say what the code no longer
does, and the directory's own path has two live-status inputs (closures and overrides) that no test can
catch.

## The five most important findings

1. **should-fix · test gap — the directory's closure and override inputs are untested.**
   `apps/api/src/modules/occupancy/occupancy.service.ts:142` (`closureNow: closed.has(id)`) and `:146`
   (`override: state?.override ?? null`) inside `liveStatusFor`. These are the only inputs the public path
   builds on its own; the staff's `now()` builds its inputs separately. `directory/liveStatus.api.test.ts`
   (setup at `:49`) has no `CLOSURE` announcement and no override. *Failing scenario:* replace either line
   with `false` / `null`. Every test stays green, and the directory then shows a closed space as
   `AVAILABLE` (and `availableNow` lists it), or ignores the desk's override. The rule itself is
   unit-proven, but this wiring is not. *Fix:* in T17's setup, add one space open by its hours with an
   active `CLOSURE` (expected `CLOSED`) and one with an override in force (e.g. `FULL` with capacity room),
   and both breaks to 12.5. **Where:** a fix round on this PR.
2. **should-fix · document untrue — `docs/plans/v1-mvp.md:218`.** The paragraph whose *Built* line this PR
   edits still says "An active owner or reception link is required; **reception is read-only**." Reception
   now writes (`PUT`/`DELETE …/status-override`, `can.ts:70` `'space.liveStatus.override': 'staff'`).
   *Fix:* e.g. "reception reads, and sets the live status's override". **Where:** a fix round on this PR.
3. **should-fix · document untrue — `docs/backend/security.md:82`.** "Each write is then decided by its own
   **owner-only** `can()` action, in its service, under the space's lock." The same sentence now lists the
   override as "the staff's", so it contradicts itself. *Fix:* "by its own `can()` action (owner-only, but
   the override, the staff's)". **Where:** a fix round on this PR.
4. **nit · plausible gap in S6 — an override is accepted where the rule will ignore it.**
   `occupancy.service.ts:209`: refused only when the space is not open by its hours. Two cases still store a
   silent no-op, which is exactly what S6's reason ("a silent no-op") was meant to prevent:
   - while an active `CLOSURE` is in force: the rule's step 2 wins, so the answer shows `status: 'CLOSED'`
     with the override echoed as "in force";
   - on an unverified space (reception linked, the owner's link ended): the status is `null`.

   The plan scoped S6 to the hours only, so the code matches the plan. The desk sees the result in the same
   answer, so nothing is lost. *Fix (owner's call):* refuse with `SPACE_NOT_OPEN` under a closure too, or
   record it as accepted. **Where:** a finding to record, or PR 2 (the desk's screen will meet it first).
5. **nit · the override echoes as "in force" while it counts for nothing.** In the same closure case,
   `SpaceOccupancyNow.override` returns the stored override (`occupancy.service.ts`, `now()`:
   `override.until > now`), while `status` is `CLOSED`. The contract says "the manual override in force"
   (`api-contract.md`, *Occupancy (managed)*). That is literally true, but the desk could show "AVAILABLE
   until 12:00" beside "CLOSED". *Fix:* only a sentence in the contract ("a closure outranks it"), or fold
   it into finding 4's decision. **Where:** with finding 4.

## The rest

6. **nit · `GET /spaces/:slug/occupancy` answers an unverified listed space `{ status: null }`.** The old
   v1-mvp row (removed) said "verified spaces only". The PR follows the plan's §4 C4 line ("not listed →
   404, as `page`"), ADR 0008 ("unverified spaces … show no live state") is still honoured, and nothing
   leaks. The departure is stated in the report and is sound. Nothing to fix; noted for the record.
7. **nit · the absent-field code for the override is `invalid_choice`, not `required`** (the plan's U14
   said `required`). This is the project's `toFieldErrors` rule for enums, and the contract says
   "`invalid_choice` when absent". It is consistent and the departure is stated. Nothing to fix.

## Departures and breaks, judged

- **R3 changed** (`shared-package.md` R3 plus its *Revised* line; `eslint.config.js` adds one `allow` for
  module source `@date-fns/tz` only). The owner approved it on 2026-10-19, and C1's body says so. The lint
  rule still disallows every other external module. The probe that `date-fns` is refused is *report
  only*. Sound.
- **Lockfile:** only the two workspaces' `"@date-fns/tz": "^1.5.0"` lines (seen); no package entry
  changed.
- **Reads moved from C2 to C4** (`openCountsIn`, `openCheckInCountsIn`, `weeksFor`, `statesFor`,
  `liveStatusFor`, `availableAmong`): they arrive with their first user, which is sound. Every commit was
  linted and typechecked through `rebase -x` *(report only)*.
- **Files outside §7** (`space-links.service.unit.test.ts` fake, the `list`/`pins` exact-shape tests):
  forced by the types and the new field. Sound.
- **Breaks:** 33 reported red, none reported green *(report only)*. The two breaks this review adds (finding
  1) are the ones that would stay green.
- **Commits:** subjects 33/39/41/37, all ≤ 50; each body says why; no tool attribution (seen).

## Checked and fine

- `gazaTime.ts`: `TZDate` both ways; minute 1440 → the next midnight; the 2026 transitions are pinned, and
  each test states its offset. It never reads the clock.
- `liveStatus` follows the data model's order on every branch: unverified → closure → outside hours →
  override in force → no hours / no capacity → `FULL`/`AVAILABLE`. `openRangeAt` uses `opens ≤ m <
  closes`, so the closing minute is `CLOSED`.
- *Present* has one definition: `checkedOutAt: null` on both tables, scoped by space, counted with
  `groupBy` for the directory and listed for the staff. Customer names are read with `spaceId` in the
  `where` (no cross-space name).
- `GET …/occupancy`: behind `requireSpaceAccess` only (P3). Owner and reception are allowed; a stranger,
  another space's owner and the admin get 404. It answers whole: status, capacity, present, override and
  people, in a stable order.
- The override:
  - `requireCan` comes before `validate`. Under the transaction, it takes `spaces.lock`, then `can()` on
    `linksUnder(tx)`; the clock is read after the lock.
  - It is refused (409 `SPACE_NOT_OPEN`) when the space has no hours, is outside them, or is on a closed
    day.
  - `until = min(now + d, gazaInstant(today, closesMinute))`, and `UNTIL_CLOSING` is the closing time.
  - The upsert writes only the three override columns, and creates the row with `capacity: null`.
  - Clearing writes and audits only when an override is in force.
  - The audit names `space.statusOverridden` (before/after) and `space.statusOverrideCleared`.
- The directory:
  - `liveStatus` is on both the card and the pin, from the listing's own `days`, with set-based queries
    and no N+1.
  - `availableNow` → `onlyIds` sits in `listed()`'s conditions before the order and the page; an empty
    list is truthy and narrows to nothing.
  - `/spaces/:slug/occupancy` uses the page's own listed check (`findShown` plus `isActiveArea`) and
    answers `{ status }` only (an exact-body test). `cachePublicly` sets `public, max-age=30`.
  - The exact-key tests prove that no card, pin or page carries a count, a capacity or an override.
- Levels: `directory` (L5) → `occupancy` (L4) → `visits`/`subscriptions` (L3), `customers`/`announcements`
  (L2), `spaces`. Each new module reads only its own table. The week comes through `spaces` (its
  `hours.repository`).
- `SPACE_NOT_OPEN` appears in `core/errors.ts`, in both catalogues and in the contract's code list.
- Docs: the contract (§4 exception, *Occupancy (managed)*, the directory's intro, filter and shapes),
  `occupancy.md`, `directory.md`, data model *Live status* 3, conventions header and §11, `overview.md`'s
  two lines and `docs/README.md` are true to the code. Each fact has one home, and the rest link to it.
  The two exceptions are findings 2 and 3.
