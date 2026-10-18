# PACKAGES — executor report

**Work Item:** PACKAGES (step 5b) · **Worker:** B · **Executor:** OpenCode · **Plan:** `2_PLAN.md`
**Branch:** `feat/space-packages` · **Base:** `origin/main` = `5e8c979d` (Merge pull request #85 …)
**Started:** 2026-10-18 · **Ports:** API 3321 · **Databases:** `masaha_b_dev`, `masaha_b_test`

## §12.1 — before the branch

```
Set-Location C:\Users\basel\masaha-b
git fetch origin                      → no output (already current)
git status --short --branch           → ## HEAD (no branch)          (clean, detached)
gh pr view 85 --json state,mergedAt   → {"state":"MERGED","mergedAt":"2026-10-17T14:50:06Z"}
git log --oneline -5 origin/main      → 5e8c979d Merge pull request #85 from Basel-Ghonaim/feat/space-gallery
                                         4f5bc294 fix(spaces): correct the gallery after review
                                         1a355404 fix(space-links): hide an empty badge list
                                         c977137b fix(web): harden the shared upload layer
                                         a21b7ed6 feat(spaces): upload photos in the gallery
gh pr list --state open --json …      → []                            (no open PR)
git diff --name-status 44b8ac7b origin/main → 64 files
```

The 64 files are `apps/web/**` (54) and `docs/**` (10) — exactly what §7 predicts for #85. **No code file
of §7 rows 5–19 moved**, and no `apps/api/src/modules/packages/` exists. The four shared documents
(`docs/features/spaces.md`, `docs/project/overview.md`, `docs/architecture/findings/README.md`,
`docs/architecture/data-model.md`) changed and are **re-read on the merged tree before they are edited**;
`data-model.md` is not edited at all (S1 approved). No stop-and-ask condition from §12.1 / §14.

```
git switch --no-track -c feat/space-packages origin/main   → Switched to a new branch 'feat/space-packages'
docker start masaha-postgres-1                             → masaha-postgres-1
```

`apps/api/.env` checked by **variable names only** (never printed): `DATABASE_URL` →
`postgresql://masaha:***@localhost:5433/masaha_b_dev`, `TEST_DATABASE_URL` → `…/masaha_b_test`,
`PORT=3321`. Correct databases, correct port.

**Frozen folders read:** `D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_OWNER.md` (O6, O8, DI-10 the price
above zero, *Rules changed*: a space's packages answered whole) and
`D:\masahaWorkspace\WORKER_B\_DONE\HARDEN\REVIEW86_OPENCODE_REPORT.md` (findings 77–79: the race helper,
the owners' names test, the optional transaction in `namesFor`).

## §12.2 — first checks

1. **The level rule (`npm run lint` after C2's files).** First run flagged one error of my own in the new
   test (`Unsafe member access .meta on an any value`); written as `(body as { meta?: unknown }).meta`.
   Then: `> eslint .` with no output — **passes**. No `boundaries` refusal: the API module `packages`
   (L2) imports `@masaha/shared/packages` (its own level) and `shared/auth` + `db` through their
   `index.ts`; `packages/shared/src/packages` (L2) imports `../spaces/index.ts` (L1, lower). The
   `../spaces/index.ts` import from the API module arrives with C3; lint is run again there.
2. **`id_spaceId`.** `apps/api/src/generated/prisma/models/Package.ts` gives
   `PackageWhereUniqueInput = Prisma.AtLeast<{ id?: number; spaceId_name?: …; id_spaceId?: Prisma.PackageIdSpaceIdCompoundUniqueInput … }>` —
   the plan's name is the generated client's. Confirmed at C2 (before its use in C4), so no deviation.
3. **P2002's meta** — see T5 below. Not needed: T5 answered 409, not 500.
4. **P2003 on a write** — see T6 below. Not needed: T6 answered 422, not 500.
5. **Audit `before`** — `null` when not given: `auditEntries()` in T3 shows `before: null` for
   `package.created`. What the model gives, written as given.

## The commits

The ids below are the **final** ones, after both rewrites (§12.7's `#PRNUM` replacement and this fix
round). Each commit was made under an earlier id; the ids moved when the history was rewritten, not
because the content did.

| # | final sha | subject | chars |
|---|---|---|---|
| C1 | `0f28d9a5` | `docs(findings): record three review findings` | 44 |
| C2 | `32ad98f7` | `feat(packages): list a space's packages` | 39 |
| C3 | `5cfa09d4` | `feat(packages): add the owner's packages` | 40 |
| C4 | `8d84be6d` | `feat(packages): edit and retire a package` | 41 |

The ids the sections below quote are the ones **current at the time that step ran** — `edcb9dc4`, `76c35068`
and `cc54fe4c` are what the commits were called while §12.4, §12.5 and §12.6 ran, before §12.7 replaced
`#PRNUM` and re-identified them as `bfcab517`, `130487fc` and `9567da9a`, and before this fix round folded
the review's changes into them.

### C1 — findings 77, 78, 79 and the index

Every `file:line` in Appendix A.1 re-verified on the tree the branch is cut from (`origin/main`
= `5e8c979d`), and **none had moved**: `apps/api/test/locks.ts` (`waitingOnLock` 19–41, `REACH_MS`
10, `wait_event_type = 'Lock'` 30, `whileHeld`'s call 65), `space.api.test.ts` (test 404–449,
`readWaiter` 419, `namesWaiter` 437), `space.service.ts` (`get` 92–105, lock 97, links 99, facts 101,
owners 102), `users.service.ts:372`, `users.repository.ts:78`, `adminSpaces.service.ts:31-34` and `:61`.
No correction needed. The four index lines go under *Open*, after 74 (#85's).

One thing to record: PowerShell 5.1's `Set-Content -Encoding utf8` writes a **BOM**, and the first
C1 commit carried one in its subject. The commit was never pushed, so it was amended at once with a
BOM-free file written through `[System.IO.File]::WriteAllText(…, UTF8Encoding($false))`, which is what
every later commit message uses. Recorded here because it would have shown in the PR's history.

### C2 — the read

**Test first, red.** `packages.api.test.ts` with T1 and T2's GET half:
```
npm run test:api -w @masaha/api -- src/modules/packages/packages.api.test.ts
 ❯ |api| src/modules/packages/packages.api.test.ts (2 tests | 1 failed) 1383ms
   × answers the owner and reception every package of the space, retired ones included, by place then name, whole
AssertionError: expected 404 to be 200 // Object.is equality
- Expected  + Received
- 200      + 404
 ❯ src/modules/packages/packages.api.test.ts:62:30
 Test Files  1 failed (1)
      Tests  1 failed | 1 passed (2)
```
T2 is **∅** and was green before its code (the boundary already answers 404), exactly as §9 says; its
proof is break B3.

**Then the code, green:**
```
 Test Files  1 passed (1)
      Tests  2 passed (2)
```

Files (C2): shared `index.ts`, `responses.ts`, `requests.ts` (the billings only); the module's
`index.ts`, `packages.manage.routes.ts` (GET), `packages.controller.ts`, `packages.service.ts`
(`list`), `packages.repository.ts` (`listFor`), `packages.mapper.ts`; `app.ts`; `packages.api.test.ts`;
`docs/api/api-contract.md` (§4's fourth exception, §5 *Packages (managed)*, the date),
`docs/features/packages.md` (new), `docs/README.md`, `docs/backend/conventions.md` (§7's row and its
date). `npm run lint`, `npm run typecheck`, `npm run check:links` and `npm run format:check` all clean
after the commit's content.

**Note on prettier:** the first `format:check` flagged every new file. The cause was one byte, not the
content: the tool that writes a file here does not append a final newline, so each new file ended on its
last character and Prettier wanted the newline (`packages/shared/src/packages/index.ts` was 62 bytes,
Prettier's own output 63). `npx prettier --write` over the new paths added it, and `format:check` then
reported `All matched files use Prettier code style!`. Every later file is written with its final
newline.

---

# STOPPED — §14, "anything in this plan proves false against the code at execution time"

## The exact command

```
npm run test:unit -w @masaha/shared -- src/packages/requests.unit.test.ts --reporter=verbose
```
run from `C:\Users\basel\masaha-b` on Windows PowerShell 5.1, Node 24.19.0, at commit `edcb9dc4` with
`packages/shared/src/packages/requests.ts` and `requests.unit.test.ts` as the working tree holds them.

## The exact error (the first lines that say why)

```
 ❯ src/packages/requests.unit.test.ts (6 tests | 1 failed) 39ms
   × createPackageSchema > requires the name, the validity, the billing, the price and the audience 18ms
     → expected { name: [ 'required' ], …(4) } to deeply equal { name: [ 'required' ], …(4) }

 FAIL  src/packages/requests.unit.test.ts > createPackageSchema > requires the name, the validity, the billing, the price and the audience
AssertionError: expected { name: [ 'required' ], …(4) } to deeply equal { name: [ 'required' ], …(4) }
@@ -1,11 +1,11 @@
    "audience": [
-     "required",
+     "invalid_choice",
    ],
    "billing": [
-     "required",
+     "invalid_choice",
      "required",
    ]
 Test Files  1 failed (1)
      Tests  1 failed | 5 passed (6)
```

**What is about to be done:** R6 (§9) says `{}` on `createPackageSchema` must answer `required` on each
of the five required terms, `billing` and `audience` among them. It answers `invalid_choice` on those
two.

## Why it cannot be built as planned

The rule from a Zod issue to a field-error code is one map, and it is not this item's:
`packages/shared/src/core/fieldErrors.ts`.

```ts
case 'invalid_type':
  return valueAt(input, issue.path) === undefined ? 'required' : 'invalid_format';
case 'invalid_value':
  return 'invalid_choice';
```

`required` comes only from `invalid_type` on a value that is absent. **Zod 4 does not emit
`invalid_type` for an absent `z.enum` field** — it emits `invalid_value`. Measured on the repository's
own zod (`4.6.5`, run through `tsx` inside `packages/shared/src`):

| schema for `a` | issue for `z.object({ a }).safeParse({})` |
|---|---|
| `z.enum(['X','Y'])` | `invalid_value` |
| `z.literal('X')` | `invalid_value` |
| `z.union([z.enum(['X','Y'])])` | `invalid_value` |
| `z.custom(…)` | `custom` → `invalid_format` |

No construct reachable from `packages/shared/src/packages/` yields `required` for a required choice
field. The only fix is `packages/shared/src/core/fieldErrors.ts`, which:

- is **not** in §7's file list for this item, so this item may not edit it;
- is named in **§12.1's** re-read list (`packages/shared/src/core/*`), which this item freezes;
- is shared by every enum in the system — `updateSpacePricesSchema`'s `period` and `audience`,
  `updateSpaceAmenitiesSchema`, `updateSpaceHoursSchema`, the contacts' `type`, and more. Changing it
  would change what every existing endpoint answers for a body that leaves a choice out.

So R6 as written is false against the code, and reaching it would mean a change this item is not
allowed to make. That is §14's last stop rule, and the executor prompt's "a test you cannot run …
stop at once; never work around it".

## RESUMED — the owner approved option 1 (2026-10-18)

The plan's approval note now carries an *Amended 2026-10-18 (the executor's stop at R6)* bullet: an
absent `billing` or `audience` answers **`invalid_choice`**, not `required`, because the shared
`toFieldErrors` maps an enum's failure — absent or not — to `invalid_choice`, as the prices' `period`
and `audience` already answer (`PUT /manage/spaces/:spaceId/prices`, api-contract line 504: *"`period`
and `audience` from their lists (`invalid_choice`)"*). R6 expects `invalid_choice` on those two fields
and `required` on the others; Appendix A's terms lines say "from their lists (`invalid_choice`)".
**`packages/shared/src/core/fieldErrors.ts` is not touched.**

### Departure 1 — R6's expectation for the two choice fields

**Where:** §9's R6, and Appendix A.2's *The terms* lines (`billing`, `audience`), written in C3.

**What the plan said:** `{}` on `createPackageSchema` answers `required` on each of the five required
terms — the name, the validity, the billing, the price and the audience.

**What is built:** `required` on the name, the validity and the price; **`invalid_choice`** on the
billing and the audience, the code `toFieldErrors` already gives every enum in the repository when the
value is absent, so `billing` and `audience` now answer exactly as `period` and `audience` do on
`PUT /manage/spaces/:spaceId/prices`.

**Why:** Zod 4 emits `invalid_value` for an absent `z.enum`, not `invalid_type`, and `required` comes
only from `invalid_type` on an absent value (measured: `z.enum`, `z.literal` and
`z.union([z.enum])` all give `invalid_value`; `z.custom` gives `custom` → `invalid_format`). The only
fix lies in `packages/shared/src/core/fieldErrors.ts`, which §7 does not list for this item and §12.1
freezes. The owner's answer keeps this item inside its own file list, and both codes are field-error
codes of api-contract §3, so no new code is introduced and the contract's meaning is unchanged: a body
that leaves a choice out names that field either way.

**Not changed by it:** the API code, the schema, T3–T16, R1–R5, R7, U1–U5, the breaks B1–B13,
`packages.md`, or any file outside C3's own lines.

**Departure 1, extended to R8 at C4 — the same amendment, on the line the note did not enumerate.**
§9's R8 says `{ billing: null }` and `{ audience: null }` answer `invalid_format`. They answer
**`invalid_choice`**, for the same reason R6 does, and the owner's own words cover it: the note says
`toFieldErrors` "maps an enum's failure, **absent or not**, to `invalid_choice`". A `null` on an enum is
one more value it cannot take, so the same mapping applies. Observed before the change:

```
 FAIL  src/packages/requests.unit.test.ts > updatePackageSchema > never clears a required term on an edit
AssertionError: expected { billing: [ 'invalid_choice' ] } to deeply equal { billing: [ 'invalid_format' ] }
- Expected
+ Received
-     "invalid_format",
+     "invalid_choice",
 ❯ src/packages/requests.unit.test.ts:128:45
```

R8 as built: `invalid_format` on `name`, `validityDays`, `priceAgorot` and `isActive`;
`invalid_choice` on `billing` and `audience`. Every other line of R8 is the plan's, and the refusal is
still on the field either way — which is what R8's title asserts, "never clears a required term on an
edit", and the test still refuses all six. This was not a second decision: it is the amendment applied
consistently, and the contract line the owner wrote — "from their lists (`invalid_choice`)" — covers it.

Work resumes at C3 from exactly where it stopped.

### C3 — `76c35068 feat(packages): add the owner's packages` (40 chars)

**R1–R6, red first** (`npm run test:unit -w @masaha/shared -- src/packages/requests.unit.test.ts`).
The six tests ran and all failed against the schema that was not written yet:
```
 Test Files  1 failed (1)
      Tests  6 failed (6)
TypeError: Cannot read properties of undefined (reading 'safeParse')
 ❯ errorsOf src/packages/requests.unit.test.ts:16:38
```
After the schema: `Test Files  1 passed (1) / Tests  6 passed (6)` — with R6 first refusing `required`
on `billing` and `audience` (see the stop above), then passing on the owner's amendment.

**U1, red first** (`npm run test:unit -w @masaha/api -- src/modules/packages/packageTerms.unit.test.ts`).
The straightforward mapping — copying each optional field as it comes — is exactly the shape §9 names
as U1's break, so it is what was written first:
```
 Test Files  1 failed (1)
      Tests  1 failed (1)
-   "totalHours": null,
+   "shiftId": undefined,
+   "totalDays": undefined,
+   "totalHours": undefined,
 ❯ src/modules/packages/packageTerms.unit.test.ts:15:35
```
Then `?? null` on each of the five optional fields:
```
 Test Files  1 passed (1)
      Tests  1 passed (1)
```

**T3–T7, T9, T10 and T2's POST, red first** (`npm run test:api -w @masaha/api --
src/modules/packages/packages.api.test.ts`) with the POST route unmounted:
```
 ❯ |api| src/modules/packages/packages.api.test.ts (9 tests | 7 failed) 11879ms
   × creates an active package with its terms, placed after the last, and audits package.created
AssertionError: expected 404 to be 201 // Object.is equality
   × refuses a price of zero and a limit out of its range on their fields, writing nothing
AssertionError: expected 404 to be 422 // Object.is equality
   × refuses a name another package of the space holds, retired or not, on its field; another space may hold it
AssertionError: expected 404 to be 201 // Object.is equality
   × refuses a shift that is not the space's own with invalid_choice on shiftId, writing nothing
AssertionError: expected 404 to be 422 // Object.is equality
   × refuses reception's create with 403 before reading its body, and writes nothing
AssertionError: expected 404 to be 403 // Object.is equality
   × decides a write on the links under the space's lock: an owner unlinked meanwhile is refused 4318ms
Error: 1 request(s) never waited on a lock
   × refuses a write to a space deleted while it waited for its lock 4346ms
Error: 1 request(s) never waited on a lock
 Test Files  1 failed (1)
      Tests  7 failed | 2 passed (9)
```
The two races fail through `whileHeld`, exactly as a race must when the request never reaches the lock
it should wait on: with the POST route unmounted there is no lock to wait for, so `waitingOnLock()`
gives up after its reach (finding 77's subject, unchanged) rather than passing without interleaving.
T1 and T2 stayed green through it, T2 being ∅ (§9). Then the create code:
```
 Test Files  1 passed (1)
      Tests  9 passed (9)
```

**The code (C3):** the shared schema's bounds, `id`/`count`/`optional`, the `terms` object of D6 and
`createPackageSchema`; `packageTerms.ts` with `toPackageTerms` and `packageValues`; the repository's
`nextPlace`, `create` and the private `written`; the service's dependencies, `lockFor` and `packageOf`,
and `create`; the controller's `create`; the route's `requireCan('packages.manage')` before
`validate`; `app.ts`'s dependency; `foreignKeyViolation.ts`'s comment.

**The documents (C3):** the contract's *The terms*, the reception clause, *Order*'s second sentence,
*Audit*, and `POST`; `security.md`'s header and *Authorization*; `conventions.md` §6's bullet;
`spaces.md`'s *Who uses it*; finding 80 and its index line; `packages.md`'s C3 lines. Finding 80's
evidence re-verified: `packages_price_check … CHECK ("price_agorot" >= 0)` at
`20260929120200_front_desk/migration.sql:226-227`, against the prices' own
`CHECK ("amount_agorot" > 0)` in `20261012144622_space_price_above_zero`.

**After the commit:** `npm run lint` (`> eslint .`, no output), `npm run typecheck` (shared, api, web
clean), `npm run check:links` (`2132 links in 125 documents and 1201 source files all resolve.`),
`npm run format:check` (`All matched files use Prettier code style!`).

**Two lint corrections in my own new code**, both of my making and both fixed before the commit:
`AuditValues` imported and unused in `packages.service.ts`, and `expect.any(Number)` inside
`toEqual` (an `any`), which became `const zetaId = (dataOf(zeta) as { id: number }).id;` asserted on
its own and then compared by value — the same proof, typed.

### C3 notes for §12.2's checks 3 and 4

Neither was needed: **T5 answered 409** (`conflict`, `errors: { name: ['not_unique'] }`), not 500, so
`isUniqueViolation(error, 'packages_space_id_name_key')` matched the constraint as §4 writes it and no
`error.meta` was ever logged. **T6 answered 422** with `errors: { shiftId: ['invalid_choice'] }` for
both a foreign shift and an unknown one, not 500, so the foreign shift's violation is P2003 and no
`error.code` was ever logged. Neither fallback was taken.

### C4 — `cc54fe4c feat(packages): edit and retire a package` (41 characters)

§11's table prints 42 for this subject; the subject it gives is 41 characters, and the other three
match their stated counts exactly (44, 39, 40). The **subject text is the plan's, unchanged**, and 41 is
within §4's ≤ 50. Recorded because the table's number is off by one, not because anything differs.

**R7, R8, red first** (`npm run test:unit -w @masaha/shared -- src/packages/requests.unit.test.ts`):
```
 ❯ src/packages/requests.unit.test.ts (8 tests | 2 failed) 30ms
   × updatePackageSchema > takes any part of the terms and the active flag on an edit, and nothing
TypeError: Cannot read properties of undefined (reading 'parse')
   × updatePackageSchema > never clears a required term on an edit
TypeError: Cannot read properties of undefined (reading 'safeParse')
 Test Files  1 failed (1)
      Tests  2 failed | 6 passed (8)
```

**U2–U5, red first** (`npm run test:unit -w @masaha/api -- src/modules/packages/packageTerms.unit.test.ts`):
```
 ❯ |unit| src/modules/packages/packageTerms.unit.test.ts (5 tests | 4 failed) 12ms
   × packageChange > writes and records only the fields the edit sets to a new value
TypeError: packageChange is not a function
   × packageChange > clears a limit with null, recording what it held
TypeError: packageChange is not a function
   × packageChange > changes nothing for an edit of the same values, or of nothing
TypeError: packageChange is not a function
   × packageChange > records a retirement as the flag's change
TypeError: packageChange is not a function
 Test Files  1 failed (1)
      Tests  4 failed | 1 passed (5)
```
U1 stayed green throughout — it is C3's test, untouched by C4's code.

**T11–T15, T16 (T7's PATCH half) and T2's PATCH, red first** (`npm run test:api -w @masaha/api --
src/modules/packages/packages.api.test.ts`) with the PATCH route unmounted:
```
 FAIL … refuses reception's edit with 403 before reading its body, and changes nothing
AssertionError: expected 404 to be 403 // Object.is equality
 FAIL … edits what the patch sets, clears a limit with null, and audits package.edited with the fields that changed
AssertionError: expected 404 to be 200 // Object.is equality
 FAIL … retires a package with isActive false, keeps it in the list, and offers it again
AssertionError: expected 404 to be 200 // Object.is equality
 FAIL … writes nothing for a patch that changes nothing
AssertionError: expected 404 to be 200 // Object.is equality
 FAIL … refuses renaming to another package's name, and a shift that is not the space's own, on their fields
AssertionError: expected 404 to be 409 // Object.is equality
 Test Files  1 failed (1)
      Tests  5 failed | 10 passed (15)
```
T14 is **∅** and was green before its code (404, as the missing route answers), proven by break B11.

**One red of my own making, recorded.** The first C4 red run showed T2 failing with
`PrismaClientKnownRequestError: { code: 'P2002' }`: my first version of T2 seeded its package *inside*
the loop over the three callers, so the second caller collided with the first one's row on
`packages_space_id_name_key`. That was my test's defect, not the plan's — §9 says *"<a seeded package's
id>"*, singular, shared. The seed moved above the loop, the count became 1 with the seeded row
asserted unchanged, and the run was repeated. **The red above is the corrected run.**

**Then the code, green:** `Test Files  1 passed (1) / Tests  15 passed (15)` (API),
`Test Files  1 passed (1) / Tests  8 passed (8)` (shared R1–R8),
`Test Files  1 passed (1) / Tests  5 passed (5)` (api U1–U5).

**The code (C4):** `updatePackageSchema` and `UpdatePackageRequest`; `PackageChange` and
`packageChange`; the repository's `findIn` and `update`, both through `id_spaceId`; the service's
`update`; the controller's `update` with `parseId`; the route's `PATCH`.

**The documents (C4):** the contract's *Retired, never deleted*, *Audit*'s `package.edited`, and the
`PATCH` endpoint; `packages.md`'s C4 lines; `spaces.md`'s header sentence, its *What it does* line and
its date; `overview.md`'s Spaces sentence, its new Packages line and its date; `v1-mvp.md`'s *Built*
line, its packages row and its date. The four shared documents were re-read on the merged tree
(`origin/main` = `5e8c979d`) before being edited, and only the lines Appendix A names were touched.

## §12.4 — verification on the head `cc54fe4c`

Process check first, as §12.1 asks:
```
Get-CimInstance Win32_Process -Filter "Name = 'node.exe'" | Where-Object { $_.CommandLine -match 'vitest' }
→ no output (no vitest running; nothing under C:\Users\basel\masaha\)
```
Then one at a time:

| Command | Result |
|---|---|
| `npm run lint` | `> eslint .`, no output |
| `npm run typecheck` | shared, api, web clean |
| `npm run test:unit` | shared `Test Files  13 passed (13) / Tests  216 passed (216)` · api `45 passed (45) / 741 passed (741)` · web `78 passed (78) / 820 passed (820)` |
| `npm run test:api` | `Test Files  49 passed (49) / Tests  824 passed (824)` (573.81 s) |
| `npm run format:check` | `All matched files use Prettier code style!` |
| `npm run check:links` | `2136 links in 125 documents and 1201 source files all resolve.` |
| `npm run build -w @masaha/shared` | clean; `packages/shared/dist/packages/index.js` present |
| `git grep -n "#PRNUM"` | 17 lines, all in `docs/features/packages.md` (documents only) |
| `git diff --stat origin/main -- apps/web apps/api/prisma package.json package-lock.json` | **empty** |

**Not run, with why (§12.4's own words):** `test:component`, the web's `build`, `check:build` and
`check:classes` — no file in `apps/web` changes, and the prompt's list leaves them to CI, which runs
them on the pushed head.

## §12.5 — the thirteen breaks, each red then restored

Procedure as §12.5 states: the file was copied to `%TEMP%\packages-breaks\` as a backup, the one edit
made, the named test file run, the red output copied here, **the file restored from the backup (never
`git checkout`)**, the file run green again, then `git diff --stat`. B11 and B1 were run before the
helper script existed; both were restored the same way and both showed `Test Files 1 passed (1) /
Tests 15 passed (15)` with an empty `git diff --stat`, seen in the run, and B11's red output is in
`%TEMP%\packages-breaks\out\B11.txt`. After the last break, `git status --short` is **empty**.

| # | Test | File | The edit | Red | Restored |
|---|---|---|---|---|---|
| B1 | T1 | `packages.repository.ts` | `listFor`'s `where` without `spaceId` | `expected [ …(4) ] to deeply equal [ …(3) ]` — the other space's `Other` listed (`+ "name": "Other"`) | 15 passed |
| B2 | T1 | `packages.repository.ts` | `orderBy: [{ sortOrder: 'asc' }, { id: 'asc' }]` | `expected [ Array(3) ] to deeply equal [ …(3) ]` — `Beta` before `Alpha` | 15 passed |
| B3 | T2 | `app.ts` | the packages router mounted behind `loadSpaceLinks` on its own `api.use('/manage/spaces/:spaceId/packages', requireAuth(), …)` before the managed mount | `expected 200 to be 404` — the stranger's GET answered | 15 passed |
| B4 | T3 | `packages.repository.ts` | `nextPlace` returns `0` | `expected [ 'Alpha', 'Zeta' ] to deeply equal [ 'Zeta', 'Alpha' ]` | 15 passed |
| B5 | T4 | `packages.manage.routes.ts` | POST without `validate(createPackageSchema)` | `expected 500 to be 422` | 15 passed |
| B6 | T5 | `packages.repository.ts` | `written` without the P2002 branch | `expected 500 to be 409` — **T5 and T15 both** | 15 passed |
| B7 | T6 | `packages.repository.ts` | `written` without the P2003 branch | `expected 500 to be 422` — **T6 and T15 both** | 15 passed |
| B8 | T7 | `packages.manage.routes.ts` | POST without `mayManage` | `expected 422 to be 403` — the `{}` body answered | 15 passed |
| B9 | T9 | `packages.service.ts` | `can(actor, 'packages.manage', space)` | `expected 201 to be 403` | 15 passed |
| B10 | T10 | `packages.service.ts` | `lockFor` ignores `spaces.lock`'s answer | `expected 403 to be 404` | 15 passed |
| B11 | T14 | `packages.repository.ts` | `findIn` **and** `update` by `{ id }` alone | `expected 200 to be 404` | 15 passed |
| B12 | T16 | `packages.manage.routes.ts` | PATCH without `mayManage` | `expected 422 to be 403` | 15 passed |
| B13 | R3 | `requests.ts` (shared) | `priceAgorot` `.min(0)` | `expected null to deeply equal { priceAgorot: [ 'out_of_range' ] }` | 8 passed |

**Two notes on the breaks, both recorded because the plan's prediction and the run differ slightly.**

- **B11 needed both edits, as §12.5's row says** ("`findIn` *and* `update` by `{ id }` alone"). Breaking
  `findIn` alone gives `expected 500 to be 404`, not 200: `findIn` then finds the other space's row,
  and the still-scoped `update` raises a Prisma `P2025` that `written` does not map. With **both** by
  `{ id }`, the run gives `expected 200 to be 404` — §9's prediction exactly. The faithful break is the
  one recorded.
- **B6 and B7 each take two tests red, not one.** B6's P2002 drop reddens T5 *and* T15 (T15 checks the
  same mapping on an edit); B7's P2003 drop reddens T6 *and* T15. §12.5 names one test each, and that
  one is red in both — the extra red is the same refusal reaching the other endpoint.

**No break stayed green.**

## §12.6 — the real run (API on 3321, `masaha_b_dev`)

`npm run dev -w @masaha/api` in the background; `curl.exe -s http://localhost:3321/health` →
`{"status":"ok","db":"up","timestamp":"2026-10-18T07:52:27.454Z"}`.

**The data, built through the API as HARDEN's run builds it.** Every secret stayed in a variable: the
admin's credentials came from `apps/api/.env` and were never printed, the owner's temporary password
came from the `POST /admin/owners` answer and was never printed, and the new password was generated
into the run. `apps/api/.env` itself was never printed.

```
login(admin)                          -> 200
lookups (public)                      -> 200; area from the catalogue
POST /admin/spaces                    -> 201      spaceId=35 slug=packages-run-5534
POST /admin/owners                    -> 201
login(owner, temporary password)       -> 200
POST /me/password (owner's new token) -> 200
POST /auth/register (reception)       -> 201
POST /auth/register (stranger)        -> 201
INSERT space_managers (RECEPTION)      -> ok (docker exec psql, masaha_b_dev; the user taken from .env's URL, its password never printed)
PUT /manage/spaces/<id>/hours         -> 200      seven open days 480–1320, one shift صباحي 480–840, shiftId=3
```

**Each status §12.6 step 3 names** (`$base = /manage/spaces/35/packages`):

| Call | Status | Answer |
|---|---|---|
| owner `POST` with the shift | **201** | `packageId=6`, `shiftId=3`, `isActive=true` |
| owner `GET` | **200** | `[that one package]`, whole, no `meta` |
| reception `GET` | **200** | the **same body** — compared byte for byte, `$reception.Body -eq $owner.Body` → **True** |
| reception `POST` | **403** | `{"type":"forbidden","message":"Not permitted"}` |
| reception `PATCH` | **403** | `{"type":"forbidden","message":"Not permitted"}` |
| owner `PATCH { isActive: false }` | **200** | the package with `isActive: false` |
| owner `POST` the evening package | **201** | `packageId=7`, `isActive=true` |
| owner `POST` **the same name again** | **409** | `{"type":"conflict","message":"Package name taken","errors":{"name":["not_unique"]}}` — **S1 as approved** |
| owner `POST priceAgorot: 0` | **422** | `{"type":"validation","errors":{"priceAgorot":["out_of_range"]}}` |
| stranger `GET` | **404** | `{"type":"not_found"}` |
| admin `GET` | **404** | `{"type":"not_found"}` |
| no token `GET` | **401** | `{"type":"unauthorized"}` |

**D7 — nothing public reads the table.** `GET /api/v1/spaces/packages-run-5534` → **200**, and the
body saved to disk and searched with `Select-String -SimpleMatch` for the package's real name
(`باقة الصباح`, 21 bytes of UTF-8) found **nothing**. D7 holds.

The console printed the Arabic names as `????`, which is this shell's code page, not the data. Read
back from `masaha_b_dev` after the run:

```
id|name|bytes|validity|totalDays|daysPerWeek|hoursPerDay|totalHours|billing|price|audience|shift|active|sortOrder
6|باقة الصباح|21|30|10|3|5|40|PER_DAY|1000|STUDENT|3|f|0
7|باقة المساء|21|45|||||FIXED|5000|GENERAL||t|1
```

So: both names stored whole; the retired one kept its row (`f`) and the offered one is back (`t`);
`sortOrder` 0 then 1 — the second package placed after the last (D4). Rows 1–5 are the demo seed's
packages, all at `sortOrder` 0, exactly as §10's Review Focus predicts.

**Stopping the server.** `Get-NetTCPConnection -LocalPort 3321` gave its listening process, and the
process was stopped by that id: the API's `node.exe` (PID 6500), then the `tsx watch` parent
(PID 628, `…\tsx\dist\cli.mjs watch --conditions=@masaha/source --env-file-if-exists=.env src/server.ts`)
that a backgrounded dev task would otherwise leave behind. Afterwards:
```
Get-NetTCPConnection -LocalPort 3321   → nothing on 3321
curl.exe -s --max-time 3 …/health      → no answer on 3321
```

## §12.7 — the PR number, the push, the PR

`gh api "repos/{owner}/{repo}/issues?state=all&per_page=1&sort=created&direction=desc"` → **86**, so
`n = 87`, as §12.7 predicted. In Git Bash, exactly §12.7's commands:

```
n=87
base=5e8c979d7ece5193febedcae92db3e08510b2525
Rewrite 1202d322… (1/4) … Rewrite cc54fe4c… (4/4)
Ref 'refs/heads/feat/space-packages' was rewritten
--- git grep -n '#PRNUM' (expect nothing) ---
(none)
--- git grep -n '#87' ---
docs/features/packages.md:17
PR will be #87
```

`git status --short` empty after the rewrite, and `format:check` and `check:links` clean on the rewritten
tree. The rewritten shas:

| Commit | sha after the rewrite | subject | chars |
|---|---|---|---|
| C1 | `1202d322` | `docs(findings): record three review findings` | 44 |
| C2 | `bfcab517` | `feat(packages): list a space's packages` | 39 |
| C3 | `130487fc` | `feat(packages): add the owner's packages` | 40 |
| C4 | `9567da9a` | `feat(packages): edit and retire a package` | 41 |

**The push** — one honest note. The first `git push -u origin feat/space-packages` failed with
`error: RPC failed; HTTP 408 curl 22 … fatal: the remote end hung up unexpectedly`. Nothing had landed:
`git ls-remote --heads origin feat/space-packages` returned empty. The push was **retried unchanged** and
succeeded — `* [new branch] feat/space-packages -> feat/space-packages`. No setting was changed, no
`--force`, no rebase. Local and remote both `9567da9acf7e366a9486c8305ce70b10db1f8526`.

**`gh label list`** — `feat`, `area:api` and `area:docs` all already exist, each with a description and a
colour, so none was created.

**The PR** — one shell note: PowerShell 5.1 splits a native argument at an apostrophe, so
`--title "feat(packages): add the owner's packages"` was passed as a variable. The title is the plan's,
unchanged.

```
gh pr create --assignee @me --label feat --label area:api --label area:docs --title … --body-file …
→ https://github.com/Basel-Ghonaim/masaha/pull/87
```

**The number GitHub gave is 87, equal to `n`** — no fixup and no second push were needed.

## §12.8 — CI, CLEAN, conflicts

`gh pr checks 87 --watch` (the first watch's connection was closed by the network mid-poll; it was
re-run and the same run continued):

| Check | Result | Time |
|---|---|---|
| `lint` | pass | 1m8s |
| `format:check` | pass | 37s |
| `typecheck` | pass | 46s |
| `test:unit` | pass | 1m3s |
| `test:component` | pass | 3m32s |
| `check:classes` | pass | 24s |
| `check:links` | pass | 24s |
| `build` (with `check:build` inside it) | pass | 30s |
| `test:api` | pass | 3m49s |
| `CodeRabbit` | pass | review skipped, manual review required for this repository |

```
gh pr view 87 --json headRefOid,mergeStateStatus
headRefOid       : 9567da9acf7e366a9486c8305ce70b10db1f8526
mergeStateStatus : CLEAN
```

`headRefOid` is the pushed head, so the green is **on the pushed head**, and GitHub says **`CLEAN`**.
Nothing was merged, no rebase was made on a `CLEAN` PR, no Issue was created, and no comment was made on
any PR.

**Conflicts.** `gh pr list --state open` at §12.7's time and again at the end: **no other open PR**, so
there is nothing to run `git merge-tree` against — §12.8's check is vacuous, not skipped. `origin/main`
is still `5e8c979d`, the commit the branch was cut from: it has not moved under the work.

## Departures from the plan, all of them

1. **R6 and R8's two choice fields answer `invalid_choice`, not `required`** (departure 1 above and its
   C4 extension). Zod 4 reports an absent or null `z.enum` as `invalid_value`; the frozen
   `toFieldErrors` maps that to `invalid_choice`, as `period` and `audience` already answer on
   `PUT …/prices`. The executor stopped on it; **the owner approved the framework's answer** and the
   plan's approval note carries it. `fieldErrors.ts` untouched. The contract's terms lines read "from
   their lists (`invalid_choice`)".
2. **The first C1 commit message carried a UTF-8 BOM**, from PowerShell 5.1's
   `Set-Content -Encoding utf8`. Never pushed, so it was amended at once with a BOM-free file; every
   later message was written the same way. Nothing reached the branch's history but the fixed version.
3. **B11 needed both edits, as §12.5's row says.** Breaking `findIn` alone gives
   `expected 500 to be 404` (the still-scoped `update` raises P2025); with `update` by `{ id }` alone
   too, the run gives `expected 200 to be 404` — §9's prediction. The faithful break is the one recorded.
4. **B6 and B7 each redden two tests, not one** (T5 + T15, and T6 + T15). §12.5 names one each, and
   that one is red; the extra red is the same refusal reaching the other endpoint.
5. **T2's own first red was a defect in my test**: it seeded its package inside the loop over the three
   callers, so the second collided with the first on `packages_space_id_name_key` (a P2002 out of the
   test, not the plan). §9 says *"<a seeded package's id>"*, singular. The seed moved above the loop, the
   count became 1 with the seeded row asserted unchanged, and the red run was repeated. The corrected
   run is the one recorded.
6. **§11's table prints 42 characters for C4's subject**; the subject it gives is 41. The text is the
   plan's, unchanged, and within §4's ≤ 50.
7. **`prettier --write` was run over the new paths** — the tool that writes a file here omits its final
   newline, which `format:check` flagged. Content unchanged; one byte added per file.

Nothing else departed: no file outside §7's list was touched, no schema, migration, dependency or
`apps/web` change, no config, timeout, `.env`, script or lane altered, no test skipped, `.skip`ped or
deleted, no mock or stub standing in for the plan's code, and no break or lane called green without its
own output saying so.

## Where the work stands

**PR #87** · `https://github.com/Basel-Ghonaim/masaha/pull/87` · **CI green on the pushed head** ·
**`CLEAN`**. Four atomic commits, pushed, not merged (merging is the owner's). The head and the ids
above are current after the review fix round; see *§12.7* and *§12.8* for the first round's numbers and
*Review fixes* below for the second.

---

# Review fixes — the fix round on PR #87

Review read whole: `6_REVIEW_CLAUDE_CODE.md` (head reviewed `9567da9a`, base `5e8c979d`). The analyst ran
nothing; findings 1–3 were verified in the code. Preconditions first, before anything was touched:

```
git rev-parse HEAD   → 9567da9acf7e366a9486c8305ce70b10db1f8526   (= 9567da9a, as the prompt asks)
git status --short   → empty (clean, on feat/space-packages, tracking origin/feat/space-packages)
git rev-parse origin/main → 5e8c979d7ece5193febedcae92db3e08510b2525   (main had NOT moved)
```

## 1. The edit's lock and permission get their tests (review 1) → `7ddbebae` (now `8d84be6d`)

Two races in `packages.api.test.ts`, in C4, on `whileHeld` exactly as T9/T10 do:

- **T17** *decides an edit on the links under the space's lock: an owner unlinked meanwhile is refused* —
  the owner deactivates their own link while the PATCH waits; **403** `forbidden`, `priceAgorot` still
  5000, `auditEntries()` `[]`.
- **T18** *refuses an edit to a space deleted while it waited for its lock, and writes nothing* — the
  space is soft-deleted meanwhile; **404** `not_found`, `priceAgorot` still 5000, `auditEntries()` `[]`.

They are green before their breaks, which is the plan's **∅** pattern, so each break is its red:

| Break | Edit | Red |
|---|---|---|
| **R1a** | `update` without `lockFor` | **both** red: `Error: 1 request(s) never waited on a lock` — `whileHeld` gives up after its reach because with no lock taken the PATCH never blocks (finding 52's purpose). Restored from the backup, `Tests  17 passed (17)`. |
| **R1b** | `lockFor`'s `can` on `space` instead of the links read under the lock | the new test red: `AssertionError: expected 200 to be 403`; **T9 red with it** — `expected 201 to be 403` — since the break is on the shared `lockFor` the POST race also uses, exactly as B9 does. Restored, `Tests  17 passed (17)`. |

Both restores from `%TEMP%\packages-breaks\`, never `git checkout`. Neither break stayed green.

## 2. Every commit gets its body (review 2) → applied by `filter-branch`

Four subjects **unchanged** (44 / 39 / 40 / 41 characters), each with a one- or two-line *why*. Written
by `%TEMP%\packages-msg\msg.py` (outside the repository: it reads the message on stdin and prints the
subject, a blank line and that commit's body only when the first line is one of the four subjects and the
message has no body), applied with

```
git filter-branch -f --msg-filter 'python -I "$TEMP/packages-msg/msg.py"' 5e8c979d..HEAD
git for-each-ref --format='%(refname)' refs/original/ | xargs -r -n1 git update-ref -d
```

Checked with `git log --format='%h %s%n%b' 5e8c979d..HEAD`: **four** subjects (counted), each with its
body. Byte-checked on all four messages: first bytes `64`/`66` (`d`/`f`), so **no BOM**; no literal `\n`;
no `Co-Authored-By`, no "generated with", no tool named.

> A first check of mine said "BOM in all four". **That check was wrong**, not the commits: it read
> `git cat-file` through PowerShell, which re-encoded the captured lines. Re-checked by dumping each
> message to a file and reading its first bytes, no message starts with `EF BB BF`.

## 3. `docs/README.md` (review 3) → `32ad98f7`

The `spaces.md` line's em dash is back: `- [spaces.md](features/spaces.md) — a space's profile and
facts…`. It was the only hyphen in the features list; the packages line, added after it, always had `—`.
Folded into C2, as the review asked. **Departure 8 — this was an unplanned edit to a line the item does
not own, and the first round's report did not record it.** §7's file list gave C2 `docs/README.md` only
for *adding* the packages line; the em dash changed with the edit.

## 4. Nits

| Nit | Fix | Commit |
|---|---|---|
| The overview's Packages line sat **before** Spaces | moved below it, as A.8 says; verified in the tree: Spaces, then Packages | C4 |
| `packages.api.test.ts:495` asserted `alpha.id === beta.id - 1` | replaced with what the title needs: **Alpha is unchanged** — its stored `name` is `'Alpha'` and its `shiftId` is `null`, beside Beta's own two assertions | C4 |
| The contract's §4 full stop mid-list (line 64) | line 64 now ends `;`, so the list is `…;` throughout | C2 |
| `written`'s comment named only the unique violation | "A write, or the key that refused it, turned into its field. **Two keys can refuse one:** the name's own `packages_space_id_name_key` (P2002), and `(shift_id, space_id) → space_shifts(id, space_id)` (P2003) …" | C3 |

## 5. Finding 81 recorded → C4

`docs/architecture/findings/81-a-retired-package-that-keeps-its-shift-stops-the-owner-from-removing-that-shift.md`,
in finding 63's format, plus its index line under *Open* after 80: *a retired package that keeps its shift
stops the owner from removing that shift*. Evidence re-read before writing —
`hours/shifts.repository.ts`'s `remove` → `inUse` → 409, and `packages_shift_id_space_id_fkey`'s
`ON DELETE NO ACTION`. Resolves with the owner's packages screen, where the decision sits. One line added
to `docs/features/packages.md`'s *Behaviour and flows*, saying the same and naming the way out
(`PATCH { shiftId: null }`).

## 6. This report

- **Removed** the three sections left over from the R6 stop: *What is done, and where it stands* (which
  said C3 was uncommitted), *Not run, and why* (which said the breaks, the real run, the push and CI
  "were never reached") and *The environment*. The evidence for all of those is in §12.4–§12.8 above,
  which records them as done. **The sections that record the stop itself — the exact command, the exact
  error, why it could not be built, and departure 1 — are kept**, as they are the record of what was
  decided.
- **The pre-rewrite ids removed** from *The commits*: `edcb9dc4`, and with it the plain "edcb9dc4" reading
  as a live sha. *The commits* now gives the final ids and says, in the table's own note, that the ids
  quoted further down are the ones current when that step ran.
- **Departure 8 added** for review 3, above.

## Folding

Each change went in as `git commit --fixup=<sha> -- <paths>`, staged by path, then
`$env:GIT_SEQUENCE_EDITOR=':'; git rebase -i --autosquash 5e8c979d`.

**One conflict, resolved by hand and recorded.** The fixup for `packages.md`'s new behaviour line went in
on C3's fixup, but that line edits C4's *Edit* paragraph, which does not exist yet in C3:
`UU docs/features/packages.md`. Resolved by keeping **C3's version** of the file (`git checkout --ours`,
`git add`, `git rebase --continue`) — the *Edit* paragraph and the new line are C4's, so C3 must not carry
them — and then re-applying the line as a fresh fixup on C4, which folded cleanly. The final tree has the
line in C4 only, and `git log --stat` confirms it: C3 carries the repository comment and the findings
index, C4 carries `packages.md` and finding 81.

## What was run (the owner's rule: only what the changes touch)

```
Get-CimInstance … 'vitest'                    → none running
git rebase -x "npm run lint && npm run typecheck" 5e8c979d
                                             → Executing npm run lint && npm run typecheck  ×4, `> eslint .`, no error
npm run test:api -w @masaha/api -- src/modules/packages/packages.api.test.ts
                                             → Test Files  1 passed (1) / Tests  17 passed (17)
npm run format:check                          → All matched files use Prettier code style!
npm run check:links                           → 2140 links in 126 documents and 1201 source files all resolve.
git diff --stat origin/main -- apps/web apps/api/prisma package.json package-lock.json
                                             → empty
```

**One of my own errors, recorded.** The first `check:links` after finding 81 reported **7** broken links,
one mine and six pointing at `overview.md` headings the reordering had nothing to do with. The cause was
mine: I had reordered `overview.md` with .NET's `ReadAllLines`/`WriteAllLines`, which wrote the file with
Windows line endings, and the checker did not read those headings. Re-checked the file's bytes — 81 bare
LF and **0 CRLF pairs**, so the content was never wrong — then stashed everything and ran `check:links` on
the pristine head to be certain of the comparison: `2136 links … all resolve`. The six were an artifact of
the working copy, not of the commit. With the finding's own link corrected (`../api/…` →
`../../api/api-contract.md#5-endpoints`, as findings 78–80 use), the final run is clean at **2140 links in
126 documents**.

**Not run, and why (the owner's rule):** the full `npm run test:unit` and `npm run test:api` lanes. No
code outside `packages.api.test.ts` changed — the other changes are two document files, one comment, the
overview's line order and a T15 assertion — and CI runs every lane on the pushed head.
