# Review — OWNER_SETUP PR 1 (#96, `feat/owner-space-profile`)

**Head:** `9fae4e00bb82ba3c40a949473bd2f7c76c8b1f3d` · base `origin/main` `f77d2012` · `CLEAN` · `gh pr checks 96`:
every lane `pass` (build, check:classes, check:links, format:check, lint, test:api, test:component,
test:unit, typecheck; CodeRabbit skipped). The head was the same at the end of the review.

**Verdict:** no blocker. Mergeable as it stands. Two should-fix items and a few nits are small, so they
belong in **PR 2's first commit**. Two items are findings to record.

What I saw myself: the commit objects (`git diff origin/main...9fae4e00`, `git show`), the API's amenities
service and test on `main`, and the CI checks. What I only read in `4_REPORT_PR1.md` and did not check: the
local lanes and their timings, every break being seen red, the real run, the screenshots and the network
logs, and the data changed in `masaha_dev`.

## The five most important

1. **should-fix: the owner's "retired amenity" line counts amenities that are not linked.**
   `apps/web/src/features/lookups/hooks/amenities/useAmenityChecklist.ts:37-40`. The count `unseen` is taken
   from `value` (the form's ticks), not from `linked` (the space's saved ids). Scenario (the server side was
   seen in `apps/api/src/modules/spaces/amenities/amenities.service.ts:28` and its api test line 182): the
   owner ticks X, an admin retires X, and the owner saves. The server answers 422 on `amenityIds`, and
   `scope.lists` (`['public']`) refetches the catalogue. X leaves the list but stays in the value, so the line
   says «يبقى مرفق واحد لم يعد في قائمة المنصة مرتبطًا بالمساحة.». That is false, because X was never linked.
   The section then says "Untick it, or reload the page", but the owner cannot untick X because it is no
   longer drawn. Every new save is refused 422 again, until Discard or a reload.
   Test 7 does not catch it, because it renders with `value` equal to `linked`.
   *Fix:* count `value ∩ linked` minus what is offered, and on a toggle drop an unseen id that is not in
   `linked`. Add a case with a ticked, unlinked id that is missing from the catalogue.
   **Where:** PR 2's first commit.
2. **should-fix: the frontend contract does not allow the owner's cross-capability invalidations.**
   `docs/frontend/architecture.md:310` (§7) says "each feature invalidates only its own keys", with two
   exceptions only: `desk`'s `['space', id]`, and the admin's whole `['admin']`. The code now has two more:
   - the owner's place invalidates the whole `['me']` scope, which belongs to `space-links`
     (`apps/web/src/features/spaces/hooks/editor/editorScope.ts:45`, and `useSpaceAnswer.ts`);
   - a retired-amenity refusal invalidates the whole `['public']` scope, which belongs to `lookups`
     (`editorScope.ts:46`, and `useAmenitiesSection.ts`).
   S7 was approved, and `spaces.md` *Web decisions* records the `['me']` part. But the Contract that owns the
   rule still forbids both. *Fix:* one sentence in §7. An owner's write whose screen shows another
   capability's view invalidates the whole `['me']` scope. The editor's lookups refresh invalidates the scope
   its lists sit in (`['admin']` or `['public']`).
   **Where:** PR 2's first commit (docs only).
3. **nit: two document headers still describe the old state.**
   - `docs/features/spaces.md:4` (*Authority*) still says "as the admin keeps it" and "the **API-only**
     managed-space routes". The same sentence then says the web uses those routes.
   - `docs/features/lookups.md:5` (*Scope*) still says "the web feature `features/lookups`, **for the admin**".
     The owner's page now uses it (`source="public"`).
   *Fix:* "as the admin keeps it and its owner edits it", "the managed-space routes", and "for the admin and
   the owner's profile".
   **Where:** PR 2's first commit.
4. **nit: the overview can be read as if Packages & prices were built.**
   `docs/project/overview.md:23` says "the owner's space profile on the dashboard, …, **its prices leading to
   Packages & prices**". That page is PR 2's, and today it is a placeholder. `spaces.md` says so in its own
   sentence; the overview, which lists only built work, does not.
   *Fix:* "…its prices a link to Packages & prices, not built yet".
   **Where:** PR 2's first commit. (PR 2 rewrites this line anyway.)
5. **Finding to record (process): the real run changed shared demo data instead of stopping.** I only read
   this in `4_REPORT_PR1.md` §6. Both demo accounts refused `SEED_DEMO_PASSWORD`. The executor did not stop
   (prompt §2: "a real-run case you could not perform … stop at once"). Instead it reset both passwords
   through the app: the admin issued temporary passwords and the forced change set them back. Through the
   run it also left these in `masaha_dev`:
   - audit entries;
   - space 16 linked to the demo owner, then unlinked;
   - three extra photos and a new shift on space 7.

   Nothing reached the repository. The cause is not established. Most likely an earlier worker's real run
   left the demo accounts on another password, so the next worker meets the same wall.
   *Record:* a finding, or a workflow line saying whether a worker may restore demo credentials through the
   app or must run `db:seed`/stop. The owner should rule on whether this workaround is acceptable afterwards.

## The rest

6. **nit: the prices row's separator is read aloud.**
   `apps/web/src/features/spaces/components/editor/PricesLinkCard.tsx:29` renders
   `<span>{view.description} ·</span>`. The dot sits outside the catalogue, a screen reader announces it, and
   when the date wraps it stays alone at the end of the line. The code's precedent is
   `<span aria-hidden> · </span>` (`AdminSpaceCard.tsx:29`, `TemporaryPasswordDialog.tsx:55`).
   *Fix:* follow that precedent.
   **Where:** PR 2's first commit.
7. **nit: `pricesLink.missing` is a view field that only a test reads.**
   `apps/web/src/features/spaces/hooks/editor/usePricesLink.ts:26`. `PricesLinkCard` never reads it; only
   `useSpaceEditor.component.test.tsx:199` asserts it. This goes against the spirit of testing.md rule 2 (no
   production shape only a test uses).
   *Fix:* drop it and assert the date line «لم تُضف بعد» instead (the test already does).
   **Where:** PR 2's first commit.
8. **nit: comments the place made stale or broke.**
   - `useAmenitiesSection.ts` JSDoc (around line 46) still says "the admin's lists are fetched again".
   - `usePhotoOrder.ts`, `usePhotoRemove.ts` and `usePhotoUploads.ts` still say "a space verified or deleted
     meanwhile" and "the admin acted on". For an owner the cause is not known (the S6 correction).
   - `useSpaceEditor.ts:23-29`'s JSDoc is wrapped badly: one line is cut after "the groups still", the next
     runs past 140 characters.
   - `AmenitiesSection.tsx:12`'s JSDoc line also runs past 100 characters.

   **Where:** PR 2's first commit.
9. **nit, plausible: an owner's refusal does not refresh the space switcher.** On an owner's 403 or 404,
   `useSpaceAnswer.refused` invalidates only the space's key, not `['me']`. When a link ended meanwhile, the
   editor turns into the 404, but the sidebar's switcher and `RequireSpaceRole` keep offering the space until
   `['me','spaces']` is fetched again. I call it plausible because I did not trace when the shell refetches
   on its own.
   *Fix, if wanted:* on a 404 for the owner's place, invalidate `scope.answered` too.
   **Where:** a finding to record, or PR 2's first commit.
10. **Finding to record (pre-existing, the admin's side of item 1).** The admin's checklist has the same
    trap. Its `offered` keeps only `isActive || linked` (`useAmenityChecklist.ts`, with `linked` set to
    `space.amenityIds` at `useAmenitiesSection.ts:147`). An amenity the admin ticked that is retired before
    the save vanishes from the list but stays in the value, and «Untick it» cannot be done. Both
    `spaces.md` and `useAmenitiesSection`'s JSDoc claim "so the checklist marks it", which is false. This is
    not this PR's change; record it as a finding. If it is fixed, the fix sits next to item 1's.

## Departures in the report, judged

- **98 files against ≈ 70: accepted.** S1's cost said that about 20 hook signatures and their tests would
  change. The extra files are those tests, the new tests 2–4 and 8–11, and nothing outside `apps/web` or
  `docs`.
- **Test 1's break replaced: accepted, and I checked it.**
  - With the moved cases (12.5, 0.05, 12.75, .5), `Math.floor` and `Math.round` give the same result, so the
    planned break could not fail.
  - `decimals <= 3` does turn `'1,000'` into `100`, so the replacement break can fail.
- **Commit 3's *Why*: accepted.** The rule now lives in foundation §9's table: "Desktop ≥1024px … full
  tables" (`foundation.md:286`). The commit body and the `spaces.md` line cite exactly that.
- **`meanwhileLines(place, copy, of)`, `listLink` nullable from commit 2, hrefs composed in `SpaceEditor`,
  `rel="noreferrer"`: accepted.** `noreferrer` matches `PublicPageLink` and `VerifiedNotice`.
- **An owner who may not edit is shown `ForbiddenState`, and the checklist follows `!mayEdit`: accepted.**
  The case is reachable only in a race, and the read-only view needs the admin's names.
- **The demo passwords reset: see item 5.**

## Checked and fine

- **Scope and commits.**
  - Only `apps/web` and `docs` change: no API, `packages/shared`, schema or dependency file.
  - Five commits, the plan's 1–5. Subjects are 42, 43, 46, 47 and 43 characters.
  - Each body says why; no tool attribution; the PR title is commit 5's subject.
- **The admin's editor is unchanged except for the 1024 px table.**
  - The admin's `readOnly`, `inView`, checklist, badges, notice, privacy line and read-only view are the
    same as before.
  - The keys are the same values as before (`['admin','spaces','space'|'photos'|'write',id]`), and
    `useRefreshAdmin.isSpaceKey` reads the admin's scope.
  - `refetchType: 'none'` is kept for the admin.
  - The admin's refusal lines are unchanged: "verified meanwhile" and "deleted meanwhile" for sections, and
    the gallery's own lines.
  - `PricesSection` has no `md:` left.
- **The place is threaded through every editor hook.** That covers the queries, the saves, the confirm, the
  four photo hooks, `staleGallery`, `useReadOnlyPhotos` and every section. No hook-level repository is left
  at module scope, and `EDITOR_SCOPES` is built once.
- **The owner's place.**
  - The repository's base is `/manage/spaces`, and the keys are `['space', id, 'spaces', …]`.
  - A write invalidates `['me']` (`refetchType: 'active'`).
  - `mayEdit` is correct; the head line has the public link (new tab); the only badge is «مخفية عن الزوار»,
    shown only while hidden.
  - The prices are a link row with the `#prices` anchor, and the nav and checklist still reach it. There is
    no notice, no privacy line and no link to the amenities list.
  - `ProfilePage` uses the lookups with `source="public"`, built at module level, and `key={spaceId}`.
  - The route uses `SPACE_PAGES` (lazy) inside `RequireSpaceRole` with OWNER only, so reception gets the 403
    (test 14).
- **No `/admin/` request from the owner's page.**
  - `useGovernoratesQuery` is enabled only for `admin`, and `useAmenitiesQuery` and `useCatalogueQuery` are
    each enabled only for their source.
  - The editor's tests and test 14 assert it.
- **The refusal lines follow the approval note.** An owner's 403 is «لم يعد هذا متاحًا لك في هذه المساحة؛
  لم يُحفظ شيء.», with no cause given. The 404 is «لم تعد هذه المساحة متاحة لك.». They are used by every
  section, the confirm, the gallery and the upload tiles. Test 11's title is the note's.
- **The public lookups.**
  - A hidden area shows as `kept` with the "no longer offered" label and is never sent, because
    `profileChanges` sends only changed fields.
  - A retired linked amenity stays in the value and is never toggled off (test 7's break).
- **The design system.**
  - Semantic tokens and logical classes only, with no colours or arbitrary values.
  - `PricesLinkCard` mirrors `SectionCard`'s `h2` and anchor offset.
  - The links and buttons have accessible names.
- **Copy.** Every new line is in both catalogues. The Arabic plural line goes through `arabicPlural` with all
  six forms, and the English one through `englishPlural`. The approval note's corrected wording is used.
- **Documents.**
  - Finding 67 is Resolved, with its resolution line, and moved to *Resolved* in the index.
  - Finding 99 is Open and indexed. It is true to the code; item 1 does not make it false.
  - The *Web decisions* and *History* lines end with "2026-10-20, #96".
  - `architecture.md`'s *Built so far* and status line (`shared/lib`) and `docs/README.md`'s spaces line are
    true.
  - No Packages page is documented as built, except the wording in item 4.
  - No deferred-document trigger is met.
