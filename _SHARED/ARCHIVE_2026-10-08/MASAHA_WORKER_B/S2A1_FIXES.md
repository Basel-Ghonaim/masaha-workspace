# PR #41 — review fixes (one list)

The review gate ran on `af2c3d3` (no blockers); the analyst verified the items in the code. Fold each
fix into the commit it corrects (fixup + autosquash, `--force-with-lease`); no "fix" commits. Then
post ONE "Review fixes" comment on the PR and update its description. No subagents.

**Keep this round tight:** only these items, the smallest change that closes each. No new tests
beyond the one named in item 4, no refactor beyond the item. If an item turns out bigger than
described, stop and report.

## The owner's decision (item 2 of the review)

**No repository parameter in the lookups services.** The owner's rule — no parameter only tests pass
or nothing uses — applies to the API too. The services' logic already lives in pure, unit-tested
helpers (`lookupChange`, `exactOrder`, `amenityKey`), and the services themselves are proven by the
API lane on the real database, which is the API's platform seam.

1. **Remove the optional `repository` dependency** from the governorates, areas and amenities
   services: each creates its repository itself. `runInTransaction` and `audit` stay injected by the
   composition root (they have a production caller).
2. **Remove the amenities service's unit test** that only served that parameter: its four cases
   repeat the API lane (unit L63, L83, L96, L107 ↔ API L111, L164, L145, L191). For its one new case
   ("no transaction opened" for an unchanged PATCH), check whether an API test already proves that an
   unchanged PATCH writes nothing (no audit entry, row unchanged); if not, add that one assertion to
   an existing API test.
3. **Record a finding:** `docs/backend/conventions.md` §2 (dependency injection with defaults, "tests
   pass plain-object fakes") and R8, and `docs/development/testing.md` §3 rule 3 ("inject the
   repository"), contradict the owner's rule that no parameter exists only for tests. Evidence: the
   older services still follow §2; the lookups services no longer do. Resolves when a docs item
   aligns those sections with the rule (the older services follow in the planned refactor). Number it
   after main's last finding (30 is yours; this one is 31). Put it in the amenities commit with the
   other finding.

## Other fixes

4. **The rollback claim (review item 1):** the API rollback test proves the change and its entry roll
   back together, not that the writer uses the caller's transaction. Reword the PR description (and
   any commit message or comment that says "proven"): the change and its entry roll back together;
   the writer's use of the caller's transaction is enforced by its required `tx` parameter. No new
   test.
5. **Finding 30 (review item 4):** add to its Evidence that an amenity's English name can also repeat
   once edited, since only the key is unique.
6. **The "placed last" amenities test (review item 5):** assert `sortOrder: 7`, as the governorates
   and areas tests do.
7. **`amenityKey` (review item 6):** one comment line stating the limit (letters such as ß, ø, æ are
   dropped, not transliterated). No code change.
8. **Commit `206c729` (governorates) message (review item 9):** don't describe areas or amenities
   before they exist, and say `signedIn` is added to `shared/auth` (the two old copies remain, per
   finding 25), not that it "moves".

**Left as they are (the owner's call):** review items 7 (`isUniqueViolation` matching the error
text, as `users` does), 8 (error codes asserted in the API tests: they are the endpoint's contract)
and 10 (422 before 404: the contract sets no precedence).

## Checks — don't re-run what already passed

- Per rewritten commit: lint and typecheck only.
- On the head, once: `test:unit` and `test:api` (the lanes these changes touch). **Skip**
  `check:classes`, `test:component`, `build` and `check:build` locally: no web file changes, and CI
  runs every lane on the pushed head.
- Report once CI is green: the head, what changed per item, the counts of the two lanes you ran.
  Don't merge.
