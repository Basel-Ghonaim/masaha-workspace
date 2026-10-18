# DELETED — the deleted spaces in the admin's list, one table of error statuses, and the parallel-work rule (API) — Report

Worker B · worktree `C:\Users\basel\masaha-b` · branch `feat/admin-deleted-spaces`, cut from `origin/main` at `068efc6`.

## 1. The pull request and its head

**#67** — `feat(space-links): list the deleted spaces` — https://github.com/Basel-Ghonaim/masaha/pull/67
Head **`c309164`** (`c309164c5ae700a1a52605a7de9825331e3f7d96`). CI passed on that head (lint, format:check, typecheck, test:unit, test:component, test:api, check:classes, check:links, build). GitHub shows **`CLEAN`**. Labels `feat`, `area:api`, `area:web`, `area:docs`; assigned to the owner. Not merged.

## 2. The commits

1. `9b7523a` `docs(workflow): run items in parallel by files` — workflow §9 rewritten by files (four conditions, in §9 only); §2's two mentions, `v1-mvp` › *Ordering notes* and `write-plan` 1.7 link it.
2. `3fa7035` `refactor(errors): keep each error status in shared` — `ERROR_STATUSES` and `errorTypeOfStatus` in `@masaha/shared/core` (+ unit test); the API's `AppError` keeps only its messages, the error handler and the web's `toAppError` use the lookup; contract §3 line; finding 24 resolved, moved in the index.
3. `97b48c3` `feat(space-links): give a row its state as facts` — `SPACE_STATES` → `SPACE_STATUSES`; `AdminSpaceRow.state` → `isVerified`, `isHidden`; API mapper and tests; the web reads the facts (badge "hidden first" in `rowView`, the menu's `isHidden`); fixtures; contract row; `space-links.md`.
4. `c309164` `feat(space-links): list the deleted spaces` — `deleted` in `SPACE_STATUSES`; `deletedAt` on the row; `spaces`' listing filter `deleted`; `listingQueryOf`; the API tests; the web's own `LIST_STATUSES`; contract (`GET`, `DELETE`); `space-links.md` (the deleted list, the owners' narrowing, `deletedAt`, the web's statuses); `spaces.md`; overview's *Built*.

## 3. What was run, and what was not

Locally, once each on the head, one at a time, after rebuilding the shared `dist`:
- `test:unit` — shared 10 files / 171 tests, web 36 / 663, API 65 / 726: all pass.
- `test:api` — 40 files / 673 tests: all pass.
- `test:component` — 123 files / 786 tests: 785 pass, 1 fails (see §6): "lists the owner's eleven pages", a test this item does not touch, which fails the same way on `main`.
- `NODE_ENV=production npm run build` and `check:build` — pass.
- `lint`, `typecheck`, `check:classes` (690 files), `format:check`, `check:links` (1,924 links) — pass. Commit 1 alone: `format:check`, `check:links`.
- **CI** on `c309164`: every job passes, `test:component` included.

**Real requests** against the API on 3321 (`masaha_b_dev`):
- "Demo Space" (id 1, verified, owner أحمد الشوا, area 2): `PUT …/hidden` 204, `DELETE` 204.
- `GET /admin/spaces?status=deleted&q=Demo&areaId=2` → 200, that space alone: `isVerified: true`, `isHidden: true`, `deletedAt: "2026-10-12T14:47:13.486Z"`, owners `["أحمد الشوا"]`, `meta.totalRecords: 1`.
- `status=deleted` with another area → `[]`.
- No status (3 rows), `verified` (1), `unverified` (2), `hidden` (0): the space listed in none.
- `POST …/restore` 204 → under `hidden` again, `isVerified: true`, `deletedAt: null`; not under `status=deleted`.
- Then `PUT …/hidden` `false` (204), leaving the data as it was.

**Browser** (headless Chrome over CDP, web on 5321, signed in as the seed admin): `/dashboard/admin/spaces?status=deleted` keeps the address, asks the API for `GET /admin/spaces?page=1` (no status), shows every live space, the status field reads «كل الحالات», and its options are «كل الحالات», «موثّقة», «غير موثّقة», «مخفية». Servers stopped by PID; ports 3321 and 5321 checked free.

**Not run:** E2E (end of project); screenshots and the RTL/LTR, theme and width review (nothing visible changes).

## 4. The breaks made, and the tests seen failing first

**Seen failing first:**
- `packages/shared/src/core/errors.unit.test.ts`: 13 tests, before `errorTypeOfStatus` existed.
- `adminSpaces.mapper.unit.test.ts`: facts (3 tests), then `deletedAt` (2).
- `listingQuery.unit.test.ts`: the two `deleted` tests.
- `rowView.unit.test.ts`: the badge from facts (5).
- `SpaceActionsMenu.component.test.tsx`: Show for a hidden space (2), with `isHidden` fixtures before the menu read it.
- `filtersOf.unit.test.ts` `status=deleted`, and `useAdminSpacesList` "offers the three states it shows as filters": both failed once `SPACE_STATUSES` held `deleted` and before the web kept its own list.
- `adminSpaces.api.test.ts`: the deleted list, its filters and its pages (3), plus the full row (`deletedAt`), with the listing's `deletedAt` filter reverted to `null`.

**Breaks made once, then restored:**
- The listing's `deletedAt` filter removed, so deleted spaces leak into every status: "orders by English name, and leaves a soft-deleted space out" and the four "leaves every soft-deleted space out for …" failed (`verified` included).
- `toAppError`'s shared lookup removed: "types a status of the contract by its status" and "infers the type from the status when the envelope's type is unknown" failed.

## 5. The problems met, and how each was solved

- **Docker Desktop was not running** (no database for the API lane). I started it and ran `docker start masaha-postgres-1`, never `db:up` from this folder (finding 48).
- **The Chrome extension showed an error page** for `localhost:5321`. I used the headless-Chrome CDP fallback (a script in the scratchpad, no dependency).
- **`deletedAt` made the routes test's `PALM` fixture need a fourth line** (`deletedAt: null`), inside the granted *admin's spaces page* fixtures (§8).
- **Component runs failed under load** (§6). Other folders were running their own lanes at the same time, and the failures followed the machine's load, not this branch. I waited for quiet before the final runs and compared against `main`.
- **A finding I recorded duplicated another.** I recorded the owner-pages timeout as finding 57 in a fifth commit. The early conflict check then showed #68 (worker A) had already recorded it as **finding 55**, with the same test and the same error, `main` included. One home per fact: I dropped my unmerged commit (`git reset --hard c309164`, then `push --force-with-lease`), cited finding 55 in the PR, and CI passed again on `c309164`. Numbers 57–58 stay unused.

## 6. Anything that behaved unexpectedly

- **`test:component` on this machine:**
  - While two other folders (`masaha` and `masaha-webbase-base`) ran their lanes at the same time (CPU 94–100%), my full runs failed 4, then 12 tests of untouched pages (`/login`, the lookups icons, the switcher, the drawer): all 3–5 s timeouts.
  - With the machine quiet, two full runs on the head failed 2, then 1: "lists the owner's eleven pages" each time, plus finding 47's drawer test once.
  - A full run of **`main` at `068efc6`** failed the same owner-pages test with the same error (`Unable to find role="navigation" and name "Space dashboard"`, body still empty), plus the drawer test and "keeps every menu waiting out a 429…".
  - The routes file passes alone (33/33), and CI's component lane passes. This is **finding 55** (#68): a file's first wait for a lazy shell outlasts 3 s on a busy machine.
- **The interrupted session:** the conversation ended mid-run once. The work was all committed, and nothing was lost; the run was repeated.
- **#68 edits `SpaceActionsMenu.component.test.tsx`**, a file this item also edits (two fixture lines: `state` → `isHidden`). Neither prompt listed it for the other side, so it is an overlap under the new rule's condition (3) that the prompts did not foresee. Git merges it cleanly (§7): #68 changes the file's toast helper, this item its two fixtures.

## 7. The early conflict check (`git merge-tree --write-tree`, head `c309164`)

- **#64** (`feat/space-own-amenities`, the amenities worker): **conflict in `docs/features/spaces.md`** only. Both append to *API history* and set *Last Updated*. Documents only, so the fast path: whichever merges second rebases keeping both lines, runs `format:check`, and pushes once. `routes.component.test.tsx`, the contract, v1-mvp and the overview merge cleanly.
- **#65** (`design/public`): clean.
- **#66** (`design/admin-rest`, the design fixer): clean.
- **#68** (`refactor/web-storage-titles`, worker A): clean. `routes.component.test.tsx` and `SpaceActionsMenu.component.test.tsx` merge automatically.

## 8. Departures from the prompt

- **The granted routes-test edit is four lines, not three:** `PALM`'s `state` became `isVerified`, `isHidden` and `deletedAt`, and `FOCUS`/`WHITE`'s `state` became `isHidden`. All are in *the admin's spaces page* fixtures, as granted. The extra line is the owner's decision 5 (`deletedAt`), which is required on every row.
- **`FOCUS`/`WHITE` keep only `isHidden: false`** (their old `state: 'verified'` is now unverified through `PALM`'s facts). The test checks the menus' 429 wait, not the badge, and adding `isVerified: true` would have pushed each line past the width and spread the edit over more lines of the granted file.
- **No new finding:** the timeout is #68's finding 55 (§5). Findings 44 and 50 are untouched.
- **Commit 2's type is `refactor(errors)`**, as the plan said: no behaviour changes.
