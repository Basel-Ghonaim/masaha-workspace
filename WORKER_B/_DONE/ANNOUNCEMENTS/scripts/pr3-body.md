## Summary
Favourites, on the API: a signed-in user saves and removes a listed space (idempotent, at most 200, the ceiling held under the user's lock) and reads them whole as the directory's cards — newest saved first, or nearest first with `sort=distance` and the `Masaha-Near` header; a space that left the directory stays, `listed: false`, with its name.

**Carried from #120** (its review, `0_CARRIED_FROM_120.md`), the first two commits:
1. The data-reports router at the API's root is a **me** router (conventions › *Routers*' four kinds): `data-reports.me.routes.ts`, `createDataReportsMeRouter`; conventions §7 and §9, and the feature document, say me. No behaviour change — the data-reports API tests run green unchanged.
2. `data-reports.md` › *Decide* and the contract's `PATCH /admin/data-reports/:reportId`: an owner's decision while the admin's waits makes the admin's 403 while the owner is still linked, and `REPORT_ALREADY_DECIDED` once the space is unverified again.
3. The repository's-select sentence moved to the O12 bullet it belongs to.
4. The comment past the wrap in `apps/api/test/app.ts`: left, as the carried file allows — no commit of this PR touches that file.
5. Finding **150** recorded: the owner sees a report's exact time — **accepted as built** (the owner's decision, 2026-10-25).

## Scope / Acceptance criteria / Out of scope
**Scope**
1. `@masaha/shared/favorites` (L2: `FAVORITES_MAX = 200`); `@masaha/shared/directory` gains `FavoriteSpace` and `favoritesQuerySchema`.
2. `POST /me/favorites/:spaceId` and `DELETE /me/favorites/:spaceId` (👤, idempotent), in `favorites`.
3. `GET /me/favorites` (👤, whole; `sort=distance` with `Masaha-Near`), in `directory` (its new me router).
4. Error code `FAVORITES_LIMIT_REACHED` (409); api-contract §4 gains the exception.
5. `docs/features/favorites.md` (new).

**Acceptance criteria**
- [x] A signed-in user saves a listed space (204) and removes one (204); a repeat writes nothing; two at once make one; an unlisted or unknown space is not saved (404); the 201st is 409 `FAVORITES_LIMIT_REACHED`, the limit held under the user's lock.
- [x] `GET /me/favorites` answers every favourite, newest saved first: a listed space as the directory's card with its live status; one that left with `listed: false` and its name; another user's never.
- [x] With `sort=distance` and `Masaha-Near`, the listed ones nearest first with their distance, those that left last, `Cache-Control: no-store`; the header without `sort=distance` is `invalid_choice` on `near`.

**Out of scope:** the Favourites screen and the space page's heart (worker A's later items); every web change but the catalogue lines.

## Change type
feat — API code, the shared contract, tests and documents; no migration; the new code's catalogue lines in `apps/web`, worker B's licence.

## New error codes (the Arabic needs the owner's approval)
| Code | Answer | English | Arabic |
|---|---|---|---|
| `FAVORITES_LIMIT_REACHED` | 409 | Your favourites are full; remove a space first. | امتلأت مفضّلتك؛ أزل مساحة أولًا. |

## Evidence
- `lint`, `typecheck` (each commit and the head), `test:unit` (shared 259, api 876, web 967 passed), `test:api` (`Test Files 92 passed (92)`, `Tests 1209 passed (1209)`), `format:check`, `check:links` (2822 links resolve), `check:conflicts`, `build -w @masaha/shared`: all exit 0.
- Seen failing first: T1–T7 (`favorites.api.test.ts`, `6 failed | 1 passed`: `expected 404 to be 204`); U1 (`Cannot find module './favoritesOrder.ts'`); T8–T10 and T7's GET (`5 failed | 6 passed`: `expected 404 to be 200`).
- Deliberate breaks, each red then restored (sha256 same) and green: B1 the order mixing the unlisted by when saved; B2 the already-saved check removed (500); B3 the user's lock removed (T2 and T5: two saves at 199 both 204); B4 the listed check removed; B5 `>` for `≥`; B6 the delete without `userId`; B7 the unlisted dropped; B8 `no-store` not set; B9 the list's `userId` filter dropped.
- §12.2: 200 favourites by one `INSERT … SELECT` in ≈ 0.5 s; the near rule extracted — one refinement (`checkNear`) and one parser (`parseWithNear`) both routes use; the directory's existing near tests green unchanged.
- Real run on 3321 (`masaha_b_dev`, demo-reception): save 204, again 204; the list carries its card; `sort=distance` + `Masaha-Near` → `distanceMeters`, `no-store`; the header alone → 422 `invalid_choice` on `near`; unknown id 404; remove 204, gone; anonymous 401 on the three routes. Nothing left written.
- Not run locally: `test:component`, the web's `build`, `check:build`, `check:classes` — the web change is the two catalogue lines; CI runs them.
- Departures from the plan: `now` added to `favorites`' deps (a favourite dated by the one clock); `no-store` set before `requireAuth` on `GET /me/favorites`, so a refusal of a request carrying the point is not kept either (security › Location); T7's GET added with C2, when the route exists; C0's rename also says "me" in `data-reports.md`'s placement and code-map lines.

## Screenshots
None: API and documents only.

## Definition of Done checklist
- [x] Acceptance criteria met, scope kept.
- [x] Lint and typecheck clean; `packages/shared` builds.
- [x] Tests added in the owning lanes, each seen failing.
- [x] No hardcoded user-facing text (codes only; both catalogues).
- [x] Authorization on the server (`requireAuth`; the caller's own rows only).
- [x] Triggered documentation updated in this PR.
- [x] One home per fact; nothing claimed that is not built.
- [x] Every claim names its test or command.
- [x] Atomic history, pushed.
