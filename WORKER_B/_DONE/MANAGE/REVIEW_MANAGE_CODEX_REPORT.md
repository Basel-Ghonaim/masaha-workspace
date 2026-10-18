PR #83 — head `d5726ddfa3057e8c368dd58d995e82dde526dd59`

Request changes.

## Findings

1. [should-fix] `apps/api/src/modules/spaces/manage.api.test.ts:45-65` — The integration suite does not exercise the required permission matrix across protected route kinds. It checks reception denial only for profile PATCH and photo reorder; hours, prices, amenities, contacts, every confirmation route, photo upload and photo delete are not tested, and owner success is asserted only for profile PATCH. A regression that routes any omitted write around its service's owner-only `can()` check would pass this suite. Add owner-success and reception-forbidden assertions for each fact write, confirmation, and photo mutation, plus owner success for photo list/upload/delete/reorder, with stranger, unrelated-owner and unlinked-admin refusal coverage as required by the plan. These were specified properties and deliberate-break checks, so CI being green does not establish them.

2. [should-fix] `apps/api/src/shared/auth/spaceAccess.api.test.ts:37-38` — The test says it verifies `linksUnder(tx)` preservation, but only asserts the second loader call's space id. If the middleware's `linksUnder` implementation drops the supplied transaction and calls `loader(id)` instead of `loader(id, tx)`, this test still passes. Capture the transaction passed to `linksUnder` and assert the loader received that exact object; then the planned lock-aware-path break is observable.

## Checked and fine

- PR head remained `d5726ddfa3057e8c368dd58d995e82dde526dd59` at the end of review.
- `requireSpaceAccess` is mounted once at `/manage/spaces/:spaceId` after auth and before the manage routers; the `/manage/spaces` list mount remains before it.
- No-link and soft-deleted access resolve to 404 through `linksAt`; hidden live spaces are not filtered by that loader.
- Managed handlers reuse the existing controllers/services; fact writes, confirmations and photo mutations reach services that decide via `can()` under the space lock. Photo upload places the limiter before `receiveFile` and calls the shared photos service.
- `/admin` retains its prior guard and non-refusing links loader. Scope has no `apps/web` or `packages/shared` changes.
- The single commit subject `feat(spaces): add managed space API` is 36 characters, within the 50-character limit.

Trial: the plan was explicit about the omitted endpoint matrix and transaction assertion, so it left the executor no material authorization or locking behavior to guess; the tests simply do not prove all of it.
