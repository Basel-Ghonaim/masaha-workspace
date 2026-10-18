# Review — PR #41, pinned to `af2c3d3` against `ce524bd`

**Verdict:** no blockers. The guard, audit writer, locks and errors are sound. Four should-fix items (what the tests prove, a project rule, a finding's Evidence) and five nits. The live head `35d68ab` differs only in the finding's number.

## Findings

**1. should-fix: the rollback test doesn't prove the audit entry shares the caller's transaction.**
- **Where:** `governorates.api.test.ts` L218–231 and L366–379.
- **Scenario:** the test makes the audit insert fail by deleting the actor. If `writeAudit` ignored `tx` and used the root `prisma`, the error would still roll back the change and the test would pass. The PR body says this is "proven". Areas and amenities have no rollback test. The code is correct (`writeAudit.ts:26` uses `tx`).
- **Fix:** add a service unit test that passes a sentinel `tx` through the fake `runInTransaction` and asserts that `audit` and the repository receive it. Or reword the claim.

**2. should-fix: the optional `repository` dependency is a parameter only tests pass or nothing uses.**
- **Where:** `governorates.service.ts:23,41`, `areas.service.ts:14,34`, the amenities service.
- **Scenario:** `app.ts` never passes it. For governorates and areas nothing passes it; for amenities only the unit test does. This follows the pattern that conventions §2 documents and the older services use.
- **Fix:** the owner decides which rule wins: remove the parameter or record the exception.

**3. should-fix: `amenities.service.unit.test.ts` repeats the API lane** (testing.md §1).
- **Where:** unit L63, L83, L96 and L107 repeat API L111, L164, L145 and L191. Only L93 ("no transaction opened") is new.
- **Scenario:** each behaviour is proven twice, and the unit titles say "answers 409", which a service doesn't do.
- **Fix:** drop the duplicates; combine what's left with the check from #1. If they go, the amenities parameter in #2 becomes unused.

**4. should-fix: the finding on repeatable English names leaves out amenities.**
- **Where:** `findings.md`, last section, Evidence.
- **Scenario:** `PATCH /admin/amenities/:id` accepts another amenity's `nameEn`, because only the `key` is unique (`amenities.repository.ts` L67).
- **Fix:** add "an amenity's English name, once edited".

**5. nit: the "placed last" test for amenities misses an off-by-one.**
- **Where:** `amenities.api.test.ts` L111–131.
- **Scenario:** with `internet` at 6, a new row at max instead of max + 1 ties, sorts second by id, and the test still passes.
- **Fix:** assert `sortOrder: 7`, as the governorates and areas tests do.

**6. nit: `amenityKey` drops some Latin letters.**
- **Where:** `amenityKey.ts:7–12`.
- **Scenario:** ß, æ, ø, œ, ł, đ, ı and þ are lost. "Straße" becomes `stra_e`, which can cause surprising collisions.
- **Fix:** map these letters before stripping, or document the limit.

**7. nit: `isUniqueViolation` matches the constraint name in `JSON.stringify(error.meta)`.**
- **Where:** `db/uniqueViolation.ts:11`.
- **Scenario:** a Prisma upgrade that changes `meta` would turn every duplicate into a 500.
- **Fix:** match the structured target fields.

**8. nit: duplicates across lanes.**
- **Where:** governorates API L285–298, L339–353, L407–423 and amenities API L177–187 repeat unit-tested codes; the `'abc'`/`'0'` 404s repeat `parseId`.
- **Fix:** let the API tests assert only the status and error type.

**9. nit: commit `1eae928` runs ahead of its code.**
- **Where:** commit `1eae928`.
- **Scenario:** its contract text names `area` and `amenity` before those exist. Its body says `signedIn` "moves", but the copies remain in `users.controller.ts:10` and `space-links.controller.ts:9`. Finding 25 and the PR body describe this correctly.
- **Fix:** reword the commit when it is next rewritten.

**10. nit: `validate()` runs before `parseId`.**
- **Where:** `lookups.admin.routes.ts:34,37,41`.
- **Scenario:** `PATCH /admin/areas/abc` with a bad body answers 422, not 404.
- **Fix:** only needed if the contract sets the precedence.

## Verified OK
- **Guard (L1):**
  - Mounted once at `app.ts:218`; the module router has no guard and is mounted nowhere else.
  - Every method passes through it.
  - `requireRole` answers 403 `forbidden` from the token's role; a pending password change is refused.
  - No `can()` call in the lookups services.
- **Audit writer:**
  - Create-only and the only writer.
  - `tx` is required, the writer knows no domain, and the composition root wires it.
  - Rows are locked `FOR NO KEY UPDATE` before they are read.
  - The actor comes from the token; the payloads hold only lookup fields.
  - Names plus the flag write two entries; no change writes none; reordering writes none.
- **Concurrency:**
  - Adding and ordering areas both lock the governorate.
  - Orders lock rows in id order.
  - Two PATCHes on one row are serialized.
  - The `max+1` race can only produce ties.
- **Errors:**
  - The three unique keys answer 409 `not_unique` on the right field, a retired amenity's key included.
  - An empty key is 422 on `nameEn`.
  - P2025 and P2003 can't be reached.
  - `parseId` refuses `0`, `01`, `+1`, `-1`, `" 1"`, `1e3`, `0x10` and ids above the int4 maximum.
  - Zod strips `key` and `governorateId`.
- **L3:** a bad id set is 409 with nothing changed; repeats are safe; 204. No delete; hiding a governorate leaves its areas alone.
- **Tests:** all 11 endpoints cover guest, USER, OWNER, a pending change and ADMIN.
- **Contract:** §5 and the §4 exception match the code.
- **Documents:** the status lines, the plan's "Built" line and finding 25's note are true.
- **Structure and commits:** one service, repository and controller per resource; R2, R3, R6 respected. Subjects of 43, 36 and 40 characters; Conventional; no attribution; each complete.

**Tokens used:** about 310,000 in total (subagent 1 about 110,000, subagent 2 about 120,000, this conversation about 80,000), under the 600,000 budget.
