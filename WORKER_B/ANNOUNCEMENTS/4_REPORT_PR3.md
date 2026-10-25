# ANNOUNCEMENTS PR 3 — `feat/favorites` — the executor's report

Written as the work goes. Scripts and outputs: `C:\dev\masaha\workspace\WORKER_B\ANNOUNCEMENTS\scripts\` (`pr3-*`).

The owner's autonomy rule (`_SHARED\AUTONOMY_2026-10-25.md`, ≈ 1 hour, PR 2's session) is **not** taken as in
force here: this prompt's "stop and ask" applies.

## Preconditions and §12.1

- `C:\dev\masaha\app-b` detached at `origin/main` = `541f3e63` (Merge #119; #120 merged as `082c205a`), clean. ✔
- `git diff --name-status befd96f9 origin/main` (617 entries) read against PR 3's code files: `app.ts`,
  `directory/directory.service.ts`, `packages/shared/src/core/errors.ts`, `directory/responses.ts`, the two web
  `errors.ts` changed only by the merged items the prompt names (PR 1's announcements on the page and
  `directory.service`, PR 2's data-reports routers in `app.ts`, the error codes of #112/#114/#118/#120);
  `favorites/` (api, shared) absent; `directory/{controller,routes,index,listQuery}.ts` unchanged. ✔
- Re-read on `541f3e63`: `model Favorite` (`@@id([userId, spaceId])`, `createdAt`, cascade) ✔; `can.ts`
  `'favorites.manage': 'self'` ✔; `users.lockAccount(id, tx): Promise<Account | null>` ✔;
  `spaces.namesWithDeleted(ids, tx?)` ✔; `publicListing.upTo(filter, ceiling)` / `page(filter, order, page)` with
  `onlyIds` filtering and `verifiedIds` marking ✔; `app.ts` mounts `/me` (`createUsersMeRouter`, only
  `POST /password`) and `createDataReportsSiteRouter` at the root ✔.
- Open PRs: **none** (`gh pr list --state open` → `[]`).
- `0_CARRIED_FROM_120.md` present → C0 (items 1–5).
- Branch `feat/favorites` from `origin/main` (`--no-track`). `docker start masaha-postgres-1` ✔. `apps/api/.env`
  names `masaha_b_dev`, `masaha_b_test`, `PORT=3321` (by pattern) ✔.
- `npm run build -w @masaha/shared` exit 0. `prisma migrate status` (masaha_b_dev): "28 migrations found …
  Database schema is up to date!"; `masaha_b_test`'s and `masaha_b_dev`'s last migration
  `20261025112542_data_report_rules` ✔.

## §12.2 first checks (PR 3)

- 2. The near rule: `directory/listQuery.ts`' `validateListQuery` reads `Masaha-Near` into `near`, sets `no-store`
  first, and parses it **bound to `directoryQuerySchema`**; the point's format (`nearPoint`) and the sort/near
  refinements are private to `packages/shared/src/directory/requests.ts`. → extracted (see C2).

## C0 — carried from #120

- Item 1 (rename, no behaviour change): `data-reports.site.routes.ts` → `data-reports.me.routes.ts`,
  `createDataReportsSiteRouter` → `createDataReportsMeRouter` (`index.ts`, `app.ts`); conventions §7's row "me (at
  the API's root: a report, and the reporter's own)", §9's `data-reports` line "`me`, at the API's root"; also
  `data-reports.md`'s *Placement* bullet "Its site router" → "Its me router" (the same name, one more place).
  `vitest run --project api src/modules/data-reports` (the files unchanged): `Test Files 4 passed (4)`,
  `Tests 19 passed (19)`.
- Item 2: `data-reports.md` › *Decide* and the contract's `PATCH /admin/data-reports/:reportId` errors, as the
  review's fix says.
- Item 3: "The repository's select leaves the reporter out…" moved to the O12 bullet.
- Item 4: **left, as the carried file allows** — no commit of this PR touches `apps/api/test/app.ts`.
- Item 5: finding **150** (`150-the-owner-sees-a-reports-exact-time.md`, status Accepted, its resolution the
  owner's 2026-10-25 decision) and its index line under *Accepted*.
- After both: `npm run lint` exit 0; `npm run typecheck` exit 0; `npm run check:links` exit 0 ("2798 links in 188
  documents and 1958 source files all resolve."); Prettier on the three code files ✔.

| sha | subject (chars) |
|---|---|
| `546c0ea8` | `refactor(data-reports): name its router me` (42) — item 1 |
| `42e8d055` | `docs(data-reports): state the decision race` (43) — items 2, 3, 5 (the suggested subject was 53: shortened) |

## C1 — `477ce1c7` `feat(favorites): save and remove a favourite` (44)

- T1–T7 (`favorites/favorites.api.test.ts`) red before the code: `Tests 6 failed | 1 passed (7)` (`expected 404 to
  be 204`, `expected 404 to be 409`, `expected 404 to be 401`; the races `never waited on a lock`); T3 passed on
  404 alone (proven by B4). Green after the code: `Test Files 1 passed (1)`, `Tests 7 passed (7)`.
- §12.2 check 1: T4's 200 spaces (one `createMany`) and 200 favourites (one `INSERT … SELECT`): the test ran in
  ≈ 0.5 s (`502ms` in the red run), under Vitest's 5 s ✔.
- §12.2 check 2 (the level rule): `npm run lint` exit 0 with `favorites` importing `users`, `spaces`, `lookups` ✔.
- `FAVORITES_LIMIT_REACHED` added in the conventions §4 order: `core/errors.ts`; both catalogues (English «Your
  favourites are full; remove a space first.», Arabic «امتلأت مفضّلتك؛ أزل مساحة أولًا.»); api-contract §6; T4/T5.
- T7 covers POST and DELETE here; `GET /me/favorites`' anonymous 401 is added in C2, when the route exists.
- First lint: 1 error in my test (`no-unnecessary-type-assertion`, `ids[0] as number`), fixed (`ids[0] ??
  'missing'`) before the commit; `npm run lint` exit 0 again; the file re-run green (7 passed).
- `npm run typecheck` exit 0; `check:links` exit 0 ("2809 links in 189 documents and 1969 source files all
  resolve."); Prettier on the code files ✔.
- (C0, later) `data-reports.md`'s *Code map* still said "its site, manage and admin routers": fixed to "me" in a
  `--fixup` of C0's first commit, folded by autosquash before the push (C0's first commit is now `613610cd`, the
  second `f0e62aba`, C1 `87edf72f`).

## C2 — `d576461b` `feat(directory): answer a user's favourites` (43)

- U1 (`directory/favoritesOrder.unit.test.ts`) red: `Error: Cannot find module './favoritesOrder.ts'`
  (`Test Files 1 failed`, `no tests`); green `Tests 1 passed (1)`.
- T8–T10 (`directory/favorites.api.test.ts`) and T7's GET red: `Tests 5 failed | 6 passed (11)` (`expected 404 to
  be 200`, `expected 404 to be 401`). Green after the code: `vitest run --project api src/modules/directory
  src/modules/favorites` → `Test Files 7 passed (7)`, `Tests 69 passed (69)` (the directory's existing list, near,
  page, pins and live-status files unchanged and green: the extraction keeps `GET /spaces`' rule).
- `@masaha/shared` directory unit file: `Tests 32 passed (32)` (the sort/near refinement moved into `checkNear`).
- §12.2 check 2 (the near rule): **extracted**, as the check says, since it was bound to `directoryQuerySchema`:
  shared `checkNear` (one refinement both `directoryQuerySchema` and the new `favoritesQuerySchema` use, the point's
  format `nearPoint` shared); API `listQuery.ts` `parseWithNear(schema, req, res)` (the header read as `near`,
  `no-store` first), called by `validateListQuery` and `validateFavoritesQuery`.
- `npm run lint` exit 0 (the level rule: `directory` → `favorites` (L2) ✔); `npm run typecheck` exit 0;
  `check:links` exit 0 ("2822 links in 189 documents and 1970 source files all resolve."); Prettier ✔.
- After the autosquash the four commits' trees are those checked (the fixup changed one document line); the plan's
  `rebase -x "lint && typecheck"` was not re-run for that reason — said here.

## §12.5 — the breaks (`scripts\brk.py pr3-breaks.json`, output `pr3-breaks.out`)

Each: backed up into `scripts\breaks\`, one edit, the named test (`-t`) red, restored from the backup (sha256 same),
green again. After all nine `git status --short` empty.

| B | The edit | Red seen |
|---|---|---|
| B1 | `favoritesOrder`: by distance answers the saved order (the unlisted mixed by `savedAt`) | U1 `expected [ 5, 3, 9, 1, 7 ] to deeply equal [ 7, 3, 1, 5, 9 ]` |
| B2 | the "already saved" check removed | T1 `expected 500 to be 204` (the key) |
| B3 | `lockAccount` removed | T2 `expected [ 500, 204 ] to deeply equal [ 204, 204 ]`; T5 `expected [ 204, 204 ] to deeply equal [ 204, 409 ]` |
| B4 | the listed check removed | T3 `expected 204 to be 404` |
| B5 | `>` for `≥` | T4 `expected 204 to be 409` |
| B6 | the delete without `userId` | T6 `expected [] to deeply equal [ { userId: 2, spaceId: 1, …(1) } ]` |
| B7 | the unlisted ones dropped (`name` undefined) | T8 `expected [ { listed: true, …(2) }, …(1) ] to deeply equal [ { listed: false, …(2) }, …(3) ]` |
| B8 | `no-store` not set (`keepPrivateIfNear`) | T9 `expected undefined to be 'no-store'` |
| B9 | the `userId` filter dropped in `favorites.of` | T10 `expected [ 2, 1, 1 ] to deeply equal [ 1 ]` |

The red steps' own reds (C1, C2) stand for T7's anonymous 401 (no separate break planned).

## §12.4 — the head (`d576461b`), each once

Free memory before the full lanes: 4 060 540 KB (after worker A's `vitest` and `tsc` under `C:\dev\masaha\app\`
ended — waited, never stopped), 5 891 144 KB before `test:api`.

- `npm run format:check` exit 0 — "All matched files use Prettier code style!"
- `npm run check:links` exit 0 — "2822 links in 189 documents and 1970 source files all resolve."
- `npm run check:conflicts` exit 0 — "No conflict markers found."
- `npm run build -w @masaha/shared` exit 0.
- `npm run lint` exit 0; `npm run typecheck` exit 0.
- `npm run test:unit` exit 0 — `Tests 259 passed (259)` (shared), `Tests 876 passed (876)` (api), `Tests 967
  passed (967)` (web).
- `git grep -n "#PRNUM"`: documents only (api-contract 3, conventions 2, security 2, directory 1, favorites 6,
  v1-mvp 3). `git diff --stat origin/main -- apps/web`: the two `errors.ts`, one line each.
  `git diff --stat origin/main -- package.json package-lock.json`: empty. Files changed: 35.
- **Not run locally (CI judges):** `test:component`, the web's `build`, `check:build`, `check:classes` — the web
  change is the two catalogue lines.
- `npm run test:api` exit 0 — `Test Files 92 passed (92)`, `Tests 1209 passed (1209)` (671.64 s).

## §12.6 — the real run (API on 3321, `masaha_b_dev`, `scripts\realrun3.mjs`, output `realrun3.out`)

`/health` → `{"status":"ok","db":"up",…}`. `demo-reception` (user 3, a global USER) signed in; the data read first:
0 favourites before; the first listed space of `GET /spaces?limit=1` (space 2, `noor-hub`), its point from its page,
rounded to 3 decimals. The script ran in one go (well inside reception's 15-minute idle window).

| Case | Answer |
|---|---|
| `POST /me/favorites/2` | 204 |
| the same again | 204 |
| `GET /me/favorites` → its card (`listed: true`, its slug, `liveStatus`, no distance) | 200 |
| `?sort=distance` + `Masaha-Near` → `distanceMeters` (0), `Cache-Control: no-store` | 200 |
| `Masaha-Near` without `sort` → `invalid_choice` on `near` | 422 |
| `POST /me/favorites/999999` | 404 |
| `DELETE /me/favorites/2` | 204; the list no longer carries it (200) |
| anonymous `GET`, `POST`, `DELETE` | 401 each |

`ALL PASS`, exit 0. **Data changed:** none left — the one favourite it saved it removed
(`SELECT count(*) FROM favorites` on `masaha_b_dev` → 0). The server stopped by its process ids (`tsx watch`
31788, the server 29336, `pino-pretty` 27052); `Get-NetTCPConnection -LocalPort 3321` prints nothing;
`server.log` deleted.

## §12.7 — `#PRNUM`, push, PR

- Just before the push: `gh pr list --state all --limit 1` → 120; open PRs none. `scripts\prnum-pr3.sh 121` (PR 2's,
  adapted to `feat/favorites`, its checks kept): "PRNUM OK #121 91d9b27f (was d576461b)"; backup branch
  `backup/favorites-pre-prnum` at `d576461b`. Then `check:links` exit 0 (2822 links resolve), `format:check` exit 0.
- Pushed `feat/favorites`; **PR #121** https://github.com/Basel-Ghonaim/masaha/pull/121, `--assignee @me`, labels
  `feat`, `area:api`, `area:docs`, `area:web` (all existed). GitHub's number = 121 ✔.

| sha | subject (chars) |
|---|---|
| `613610cd` | `refactor(data-reports): name its router me` (42) |
| `f0e62aba` | `docs(data-reports): state the decision race` (43) |
| `1d42978a` | `feat(favorites): save and remove a favourite` (44) |
| `91d9b27f` | `feat(directory): answer a user's favourites` (43) |

## Departures from the plan

- `now` added to `favorites`' deps (D15 names `{ runInTransaction, users, publicListing, lookups }`): a favourite's
  `savedAt` is dated by the one clock (conventions §11), as PR 2 did for reports.
- `GET /me/favorites`: `keepNearPrivate` (the header's `no-store`) runs **before** `requireAuth()`, then the
  near/sort rule (D15's order), so an anonymous request carrying the point is refused 401 with `no-store` too — what
  security › Location and D9 require ("every answer to a request carrying it", "a refusal … included"). T9 asserts it.
- T7 ("anonymous is 401 on the three routes") holds POST and DELETE in C1; its GET is added in C2, with the route.
- §12.2 check 2: the near rule extracted (shared `checkNear`; API `parseWithNear`), as the check allows; said in C2.
- C0 item 1 also renames "site" in `data-reports.md`'s placement and code-map lines (the same name; the code-map line
  first missed, then folded in by `--fixup` before the push).
- C0's second subject shortened (53 → 43).
- After the autosquash, `rebase -x "lint && typecheck"` was not re-run: the fixup changed one document line; the
  head's lint and typecheck ran green.
- A U1 red step taken by moving the just-written `favoritesOrder.ts` aside (it was written together with its test),
  then back.

## Decisions taken without the owner

None (the autonomy rule not in force; nothing met a "stop and ask").

## §12.8 — CI, CLEAN, conflicts

- `gh pr checks 121 --watch` → every check `pass` on head `91d9b27f` (= `git rev-parse HEAD`): `build` 50s,
  `check:classes`, `check:conflicts`, `check:links`, `format:check`, `lint`, `test:api` 6m21s, `test:component`
  12m59s, `test:unit`, `typecheck`, CodeRabbit. `gh pr view 121` → `mergeStateStatus: CLEAN`, 35 files.
- Not run locally (CI judges): `test:component` pass, the web's `build` (with `check:build`) pass, `check:classes`
  pass.
- Conflicts: no other open PR (`gh pr list --state open` → only #121); worker A's DESK_SCREENS PR 3 not open —
  nothing to `merge-tree`. Whichever merges second rebases, keeping both sides' lines in the shared documents.

## Leftovers

- `git status`: clean, "nothing to commit"; no rebase in progress.
- Local branch left: `backup/favorites-pre-prnum` (at `d576461b`, before the `#PRNUM` rewrite).
- Port 3321 free; no server running. Scripts kept in `scripts\` (`pr3-*`, `pr3msg\`, `prnum-pr3.sh`,
  `realrun3.mjs`, `breaks\`), never committed.
