# Review — PR #48 (S2b-2: the spaces' facts API)

**Head reviewed:** `c4e993d` (`c4e993d0491ed33d1701f40de82a614f3131e050`), base `a1f5aba`. Read-only, from commit objects.

**Verdict: approve after fixes.** Nothing blocks: authorization, transactions, the shifts' write order and the migration are sound. Five should-fix items (two test gaps, two in the docs, one commit subject) and four nits.

## Findings (most severe first)

**1. Should-fix: the refused-caller matrix cannot catch a leak on the prices and amenities PUTs.**
- **Where:** `apps/api/src/modules/spaces/space/space.api.test.ts:92-105`. The bodies are `{ prices: [] }` and `{ amenityIds: [] }`.
- **Scenario:** `spaceDated(1)` (`:27-40`) dates every group, and the space has no prices or amenities. Both bodies are therefore no-op saves (D3), so even the ADMIN writes nothing. If a guest, USER or OWNER got through, no date would move and no audit entry would be written, and the "changing nothing" check (`:166-177`) would still pass.
- **Fix:** send bodies that really write: one plain price, and one active amenity's id (or set `amenitiesUpdatedAt: null`). Also assert that the rows stay empty.

**2. Should-fix: three of the four "missing" branches of the stale filter are untested.**
- **Where:** `listing/listing.repository.ts:54-60`, tested only by `adminSpaces.api.test.ts:219-236` ("No Hours").
- **Scenario:** delete the `pricesUpdatedAt: null`, `amenitiesUpdatedAt: null` or `contactsUpdatedAt: null` branch, and every test still passes. The PR's listed break removed all four at once.
- **Fix:** add one space each with prices, amenities or contacts missing, using `it.each` over the groups.

**3. Should-fix: a network "handle" check lets a host or `profile.php` through, which defeats F6 and the Facebook-id rule.**
- **Where:** `packages/shared/src/spaces/contacts.ts:21` (`HANDLE` allows dots), tried first at `:85-86`.
- **Scenario:**
  - FACEBOOK `profile.php` is stored as `https://www.facebook.com/profile.php` with no `id`.
  - INSTAGRAM `instagram.com` is stored as `https://www.instagram.com/instagram.com`.
  - Yet `instagram.com/` (with a slash) is refused.
- **Fix:** refuse a handle that is one of the network's hosts (with or without `www.`) or `profile.php`, and add unit cases.

**4. Should-fix: `spaces.md` says every group saves through one path, but the profile's edit does not.**
- **Where:** `docs/features/spaces.md`, decision "Every group changes through one save path…" (with *Behaviour › Save a group*).
- **Scenario:** `PATCH` on the profile still runs its own copy of the sequence in `profile/profile.service.ts:51-78` (lock, `can()`, change, date, audit). Only the profile's confirm uses `createGroupEdit`. The document claims a single path that the code does not have.
- **Fix (the owner's choice):** either move `profile.update` onto `editGroup` (the step returns `null` for no change and checks the area inside), or narrow the decision to the four fact groups and the confirms.

**5. Should-fix: `spaces.md` restates facts that other documents own (documentation.md §1, §3).**
- **Where:** the F6, Facebook-id and D6 decisions repeat the contact storage forms, which data-model › Conventions › Contacts already owns (lines 18-19, in more detail). D8 repeats the caps, which the contract's request bodies own.
- **Fix:** keep each decision's headline and its *Why*, and link to the owner for the details.

**6. Should-fix: one commit subject is over the 50-character limit** (`workflow.md:54`).
- `4f36359 feat(spaces): confirm fact groups, missing until set` is 52 characters.
- **Fix:** reword it at the next fold, for example `feat(spaces): confirm groups, missing until set` (47).

**7. Nit: the retired-amenity test does not check that the retired link was kept.**
- **Where:** `amenities.api.test.ts:122-131`.
- **Scenario:** if `replace` dropped the retired link, the final state is still `[internet]`.
- **Fix:** after the first save, assert that the stored ids are `[internet, retired]`.

**8. Nit: the contract says the audit records the group "as AdminSpace shows it", which is not true for unsaved hours.**
- **Where:** `docs/api/api-contract.md:279`.
- **Scenario:** with no rows, `AdminSpace.hours` is `null`, but the audit `before` is `{days: [], shifts}`.
- **Fix:** drop that phrase, or state that `days: []` is recorded.

**9. Nit: `+970 (0)59 912 3456` is refused.**
- **Where:** `packages/shared/src/core/phone.ts:20-21`. The number becomes `+9700599…`, and a national part starting with `0` is refused.
- **Fix:** if the owner wants this common form accepted, drop one `0` after the country code.

**10. Nit (record a finding; the pattern predates this PR): `can()` decides from links read before the lock.**
- **Where:** `facts/groupEdit.ts:71-73`, and likewise the profile service.
- **Scenario:** an owner link committed between the links loader and the lock lets one admin save land on a now-verified space. Separately, `space.service.ts:90-94` reads the space and its facts outside a transaction, so a concurrent hours save can show the old week with the new shifts.
- **Fix:** record both. Re-reading the links under the lock would close the first if it is ever worth it.

## Verified OK

**Authorization:**
- The 4 PUTs and 5 confirms are only in `createSpacesAdminRouter`, under `/admin` behind `requireAuth` and `requireRole('ADMIN')`, with the links loader first. An owner cannot reach them.
- `can()` runs after the lock and before the step, so a verified space gets 403 with nothing written.
- The profile confirm uses `space.profile.update`.

**Transactions:**
- Every write and its audit entry use `tx`. The thresholds are read before the transaction, and there is no `Promise.all` inside one.
- The lock is taken before every read that decides: the no-op compare, `idsOf`, the active-amenity check and the shift diff.
- Shifts:
  - The write order (remove, rename aside, update, create) is safe under name swaps.
  - The passing name `\u0001<id>` cannot collide, because `textSchema` refuses control characters.
  - P2003 alone maps to 409, and the transaction takes the week back.
  - Another space's shift id gets 422.
- The lock test truly proves the lock: without it, the save answers 500.

**Migration and seed:**
- The migration only makes the four dates nullable and clears each one where the space has no rows (shifts count for hours).
- The demo seed dates and fills all four groups.

**Validation:**
- The +972→+970 rewrite for 59/56, with only separators stripped.
- Hosts are checked, and `evil`/userinfo hosts are refused.
- A1's duplicates are detected on normalised values, on the right field.
- The caps and the int32 ids are enforced. I found no input that reaches a 500.

**Freshness:**
- `staleGroups` ignores the nulls, and `missingGroups` is correct.
- `lastUpdate` always has a value, because the profile is always dated.
- The filter matches the row.

**Tests, contract and docs:**
- The caller matrix covers all 9 endpoints for all five refused callers.
- The listed breaks match real assertions.
- The contract matches the code.
- data-model (F3, missing groups), conventions §2 and §10, the overview, v1-mvp, lookups.md and the README are accurate.

**Findings:**
- 31, 36 and 41 are truly resolved.
- 42 is a real, separate flake: it failed at 761 ms, inside finding 28's 3 s wait, in a hook test with no lazy page.

**Commits:** seven, Conventional, each a complete unit, with no tool attribution.

## Tokens

About 355k in all: subagent 1 ≈ 117k, subagent 2 ≈ 140k, this conversation ≈ 100k.
