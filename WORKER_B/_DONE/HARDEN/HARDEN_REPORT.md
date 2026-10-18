# HARDEN — report

**Work Item:** HARDEN · **Worker:** B · **Executor:** Claude Code (Opus 5.5, effort medium), 2026-10-17
**Plan:** `C:\Users\basel\.prompt\MASAHA_WORKER_B\PLAN\HARDEN_PLAN.md` (S1–S6 approved)
**Branch:** `fix/space-api-hardening`, from `origin/main` = `93f152fe`, in `C:\Users\basel\masaha-b`

## 1. Start (§12.1)

- The branch already existed at `93f152fe`, untracked, clean (cut before this session); `origin/main` had
  not moved (`git diff 93f152fe origin/main` empty); `gh pr list --state open` was `[]`.
- Docker Desktop was not running: started it, then `docker start masaha-postgres-1` (never `db:up`).
- `apps/api/.env` checked by names only: `PORT=3321`, `DATABASE_URL` → `masaha_b_dev`,
  `TEST_DATABASE_URL` → `masaha_b_test`. The file was never printed.
- Worker A ran its component lane (`C:\Users\basel\masaha\…vitest … --project component`) during
  the first checks; only focused runs (one or two files) were made then.

## 2. First checks (§12.2)

1. **D4's type:** `npm run typecheck` accepted `can({…}, action, spaceOf(req))` with
   `action: SpaceAction` as written. No generic needed.
2. **The helper:** with `waitingOnLock` written and only `whileHeld` converted,
   `photosRace.api.test.ts` passed three times running (2/2 each).
3. **A1's determinism (S2):** with A1 written and D1 not applied, three runs, each red on
   `namesWaiter` only:
   - `AssertionError: expected 3412 to be 3415 // Object.is equality`
   - `AssertionError: expected 3484 to be 3493 // Object.is equality`
   - `AssertionError: expected 3560 to be 3569 // Object.is equality`

   D1 applied: green three times. `to_regclass(${on})` takes the text parameter and the test role may
   `LOCK TABLE users IN ACCESS EXCLUSIVE MODE`. **A1 is kept; finding 71 is not recorded.**
4. **S5:** `readOneStatementAtATime.api.test.ts` (admin `GET` of a space with an owner, then the
   owner's managed `PUT …/contacts` changing the group and again unchanged) was **green twice on
   `origin/main`'s `Promise.all`**: the adapter queued the two statements, as finding 11's probe
   found. Per S5 the file was deleted; D2 has no failing test and stands on conventions §8's rule.

## 3. The tests — red first, and each break (§9)

Breaks were made from a backup copy in `%TEMP%\harden-breaks\`, the named file run, the file restored
from the copy (checked byte-identical), never `git checkout`.

**C1 — the converted race tests.** `sessionLock` + `adminOwners` (54 tests), `hours` + `prices` (22),
`space` (104): each green three times running. Evidence that a race which never interleaves now fails:
T4's helper break (below).

**A1** (`space.api.test.ts`, *reads the owners' names on the read's own connection, inside its
transaction*): red three times before D1 (§2 above). **Break (D1):** `namesFor(…)` without `tx` →
`AssertionError: expected 4034 to be 4043 // Object.is equality`.

**U2** (`spaceAccess.unit.test.ts`, *reads the space's links again with the transaction it is given*):
**break** `linksUnder: () => loader(id)` →
`AssertionError: expected [ { id: 12, tx: undefined }, …(1) ] to deeply equal [ { id: 12, tx: undefined }, …(1) ]`.
D3 itself changes nothing observable (plan §4): the matrix stayed green (`manage.api.test.ts` 6/6).

**U1** (`requireCan.unit.test.ts`): against a stub calling `next()`, three of four red —
`expected undefined to match object { type: 'forbidden', code: undefined }`, the same for
`unauthorized` and `not_found`. Real body: 4/4. **Break** `next()` before the check → the same three
red: `expected "vi.fn()" to not be called at all, but actually been called 1 times`.

**T5** (*refuses reception's photo writes before reading them, and counts no upload*): before D4's
routers → `AssertionError: expected 422 to be 403`. Breaks:
- `requireCan` after `receiveFile` → `expected 1 to be +0` (the count). *Departure from the plan's
  prediction (422):* `receiveFile` lets a request with no file through to the controller, so
  `requireCan` still answered 403, but the limiter had counted it. Red all the same.
- `requireCan` between `limitRequests` and `receiveFile` → `expected 1 to be +0`.
- `requireCan` dropped from the order → `expected 422 to be 403`; from the removal →
  `expected 404 to be 403`.

**T6** (*counts an upload before reading its file…*): the executor check held — an unreadable upload
(`attach('other', …)`) answers 400 `bad_request`. **Break** `receiveFile` before `limitRequests` in
`photos.manage.routes.ts` → `AssertionError: expected 201 to be 429`.

**A2** (S4, `photos.api.test.ts`, *counts an admin's upload before reading its file…*): **break** the
same swap in `spaces.admin.routes.ts` → `AssertionError: expected 201 to be 429`.

**T1** (*answers the owner and reception the same whole space…*): the executor check — `createSpace()`
dates the profile, so `missingGroups` is `['prices', 'amenities', 'contacts']` as planned. Breaks:
`ownersFor` answering `[]` → `AssertionError: expected { id: 1, slug: 'focus-hub', …(21) } to match
object { id: 1, isVerified: true, …(9) }`; the read with `NO_FACTS` instead of its facts → the same
assertion.

**T2** (*answers not_found for an unknown or malformed space id, and 401 to a guest*):
- `Number(req.params.spaceId)` for `parseId` → `AssertionError: expected 500 to be 404`.
- **The plan's second break stayed green** (the boundary reading the caller as optional and refusing a
  guest with 404): `requireAuth()` is mounted before `requireSpaceAccess` on
  `/manage/spaces/:spaceId` (`app.ts`), so a guest is refused 401 before the boundary runs. Per §14 I
  stopped and asked, with two diagnostic breaks (both restored): `requireAuth()` dropped from the mount
  alone → red, `expected 401 to be 404` (the owner's unknown id: the boundary's `signedIn` answers
  401); `requireAuth()` dropped **and** the optional-caller boundary → red on the guest,
  `expected 404 to be 401`. **The owner chose the combined break** as T2's guest break; recorded here
  as a departure.

**T3** (*keeps a hidden space open to its owner and reception*): **break** `findSummaries` filtering
`isHidden: false` → `AssertionError: expected 404 to be 200`.

**T4** (*decides a managed save on the links under the space's lock: an owner unlinked meanwhile is
refused*): **break** D8.6 (`const locked = { links: space.links };`) → `expected 200 to be 403`.
**Helper break (D7's evidence):** T4's hold replaced by `() => Promise.resolve()` →
`Error: 1 request(s) never waited on a lock`.

## 4. #83's deliberate breaks, run on the head (D8, §12.5)

Each made once on the head (`5d5f0084`'s tree), the named files run, restored from the backup copy
(byte-identical), `git status` clean after all seven.

| # | Break | Red |
|---|---|---|
| 8.1 | `can.ts`: `'space.facts.update': 'staff'` | `can.unit`: 4 failed (*on an unverified space, for a reception left linked to it: false* — `expected true to be false`; *…for an ADMIN: true*; *on a verified space, for the reception of this space: false*; *follows the link's role…*). `manage.api`: *lets reception read photos but refuses every mutation* — `expected 200 to be 403` |
| 8.2 | `can.ts`: `'space.profile.update': 'staff'` | `can.unit`: the same 4 for `space.profile.update`. `manage.api`: *lets the owner read and update, while reception can read only* — `expected 200 to be 403`; *lets reception read photos but refuses every mutation* |
| 8.3 | `can.ts`: `'space.photos.manage': 'staff'` | `can.unit`: the same 4 for `space.photos.manage`. `manage.api`: *lets reception read photos…* — `expected 204 to be 403`; T5 — `expected 422 to be 403` |
| 8.4 | `spaceAccess.ts`: the `if (!can(…)) throw AppError.notFound();` line deleted | *refuses every protected route for strangers, unrelated owners and unlinked admins* — `expected 200 to be 404`; *does not admit a deactivated link or a deleted space* |
| 8.5 | `spaceAccess.ts`: `if (role !== 'ADMIN' && !can(…))` | *refuses every protected route for strangers, unrelated owners and unlinked admins* — `expected 200 to be 404` |
| 8.6 | `groupEdit.ts`: `const locked = { links: space.links };` | T4 — `expected 200 to be 403`; `hours.api`'s *refuses the admin when an owner joined while the save waited for the space's lock (finding 43)* |
| 8.7 | `photos.service.ts` `lockFor`: `can(actor, 'space.photos.manage', space)` | `photosRace`: *decides on the links under the space's lock: an owner linked meanwhile refuses the admin* — `expected 201 to be 403` |

## 5. Verification on the head (§12.4)

Before each full lane, the process check found no vitest of worker A's folder running.

| Command | Result |
|---|---|
| `npm run lint`, `npm run typecheck` | clean at each of the six commits (`git rebase -x`), and on the head |
| `npm run test:unit` | every file passed in each of its three runs (12 files / 208 tests, 44 / 736, 75 files) |
| `npm run test:api` | 48 files, 809 tests passed (323 s) |
| `npm run format:check` | all files use Prettier code style (after the fix in §7) |
| `npm run check:links` | 2077 links in 117 documents and 1158 source files resolve |
| `git grep -n "WAIT_MS\|aWhile\|setTimeout(resolve, " -- apps/api` | no race wait: `app.ts:223` (the timer port's default `wait`) and `test/locks.ts` (the helper's own 20 ms poll) only |

**Not run**, as the plan says (§5, *Rules the item touches*): `test:component`, `build`,
`check:build`, `check:classes` — no file in `apps/web` or `packages/shared` changed; CI runs them.

## 6. The real run (§12.6, API on 3321, `masaha_b_dev`)

`GET /health` → `{"status":"ok","db":"up"}`. Data through the API (the seeded admin; a space in the
first active area; `POST /admin/owners` → its temporary password; the owner's sign-in and
`POST /me/password`; two registrations), reception linked by the one SQL insert. No password or token
was printed.

| Request | Status |
|---|---|
| owner `GET /manage/spaces/<id>` | 200, `owners = [{ id: 13, name: 'Owner Run' }]` |
| reception, the same | 200, the same body (`==` true) |
| reception `POST …/photos` with no file | 403 |
| reception `POST …/photos` with a JPEG | 403 |
| `rate_limits` rows `photo-upload:%` before / after | 0 / 0 |
| owner `PUT …/contacts` `{ "contacts": [] }` | 200 |
| admin `GET /manage/spaces/<id>` | 404 |
| stranger | 404 |
| owner `/manage/spaces/999999`, `/abc` | 404, 404 |
| no token | 401 |

Stopped by process id (four node processes); `Get-NetTCPConnection -LocalPort 3321` showed only
`TimeWait` entries with no owning process at first, and nothing once they expired.

## 7. Problems and their solutions; anything unexpected

- **Docker Desktop was not running:** started it; `docker start masaha-postgres-1`.
- **Lint refused `${count}` in a template literal** (`restrict-template-expressions`): the helper's
  message uses `${String(count)}`; the text is the plan's.
- **`format:check` flagged `test/locks.ts`** (the line grown by `String(count)`, from C1): fixed in C1
  itself by an `edit` rebase (the throw in braces), no fix commit; lint and typecheck then re-run at
  every commit.
- **The real run's first attempts:** the script read `accessToken` outside the `data` envelope, then a
  random password once missed the policy (422). Fixed in the script; the leftovers are only extra dev
  rows in `masaha_b_dev` (a space and an owner from the aborted runs).
- **T5's first break** went red on the count, not on 422 (§3).
- **T2's planned guest break stayed green** — stopped and asked; the owner chose the combined break
  (§3).
- **`git grep '#86'` matches four binary files** (fonts and screenshots) by chance; the replacement
  touched only files that held `#PRNUM` (`grep -rl` on docs), and `git diff origin/main` lists only
  the item's 31 files.

## 8. Departures from the plan, each with its reason

1. **T2's guest break** is "`requireAuth()` dropped from the mount + the boundary reading the caller as
   optional" instead of the boundary alone, which cannot be seen (`requireAuth()` refuses a guest
   first). The owner's decision, 2026-10-17.
2. **Finding 52's resolution line** is written `**Resolution (2026-10-17, #86):** …`, the form every
   resolved finding uses, instead of the plan's `*Resolved (<today>, #PRNUM):*`; its text is the
   plan's.
3. **The helper's message** builds the count with `String(count)` (lint), and its throw is braced
   (Prettier).
4. **S5's guard** drives the group save through the owner's managed `PUT …/contacts`, since the admin
   is refused on a space with an owner; it stayed green, so per S5 it is not kept.
5. **A2** asserts the 400 status of the thirty unreadable uploads and that nothing was stored, as T6
   does; the plan named only the shape.
6. **`docs/project/overview.md`'s date** was set to 2026-10-15 at C6, when no PR was open. GALLERY's
   #85 opened before the push and edits `overview.md`'s body but not its header line; the merge with
   #85 is clean, so the edit was kept.

## 9. Commits, PR and conflicts

| SHA | Commit |
|---|---|
| `c95da502` | `test(api): wait for a race to reach its lock` |
| `b0470302` | `fix(spaces): read owner names in the transaction` |
| `2d672818` | `refactor(api): let can() decide managed access` |
| `5cacdf29` | `fix(spaces): guard managed routes with requireCan` |
| `e2ba7302` | `test(spaces): cover the managed read and races` |
| `e2a34570` | `docs(spaces): correct the managed API's records` |

31 files, +423 −189. No schema, migration or dependency; nothing in `apps/web` or `packages/shared`.

**PR #86** — https://github.com/Basel-Ghonaim/masaha/pull/86, labels `fix`, `area:api`, `area:docs`.
The number was checked just before the push (latest issue/PR 85 → 86) and GitHub gave 86.
**GALLERY's plan assumed #85**, and GALLERY did open as #85, so its references hold.

**Conflict check:** `git merge-tree --write-tree HEAD b40a69b8` (#85's head) → exit 0, clean. Shared
files with #85: `docs/features/spaces.md`, `docs/features/space-links.md`,
`docs/architecture/findings/README.md`, `docs/project/overview.md` — all merge cleanly today.

## 10. CI and state (§12.8)

On the pushed head `e2a34570a03172cfb42cf285898335ceae390e15` (run 39037505746): `lint`, `typecheck`,
`test:unit`, `test:api`, `test:component`, `build`, `check:classes`, `check:links`, `format:check` all
**pass**; CodeRabbit skipped (manual review). `mergeStateStatus`: **`CLEAN`**. Not merged; not rebased.
