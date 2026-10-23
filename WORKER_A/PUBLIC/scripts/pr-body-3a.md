## Summary

PUBLIC, PR 3a: the site's Space details page at `/spaces/:slug`. These are the plan's PR 3 commits 1–4. Before them come eight commits carried from #105's review. The photos and the live status's refresh are PR 3b. The owner accepted about 100 files for this PR (2026-10-22).

**Carried from #105** (`0_CARRIED_FROM_105.md`, items 1–14; each code fix was seen failing before its fix):
1. The pick ends with the map. Leaving the map while picking restores the location from before. This holds under React's development double run too. — `2a0ffa2a`
2. The chosen space is reached first. The map's overlay (the card, the legend, «مركّز على موقعي») comes before the pins in the tab order. Below 768 px, one polite line says «{name}: التفاصيل في أسفل الصفحة» / "{name}: details at the bottom of the page" (**words proposed by the executor, for this review to check**). — `378a1079`
3. The pick's centre never leaves unrounded. No box is sent while picking, and every box is rounded outward to two decimals. — `25e90a91`
4. The map has its own near-me line: «موقعك ظاهر على الخريطة. تُرتَّب القائمة حسب المسافة منه.», with no privacy sentence and no stop button. — `4bc2f3c9`
5. The pins' first load is shown: «جارٍ تحميل المساحات…», and the section is marked busy. — `33c49922`
6. The picking card goes under the map below 1024 px. — `2a0ffa2a`
7. Escape closes the chosen space's card from 768 px, and the focus goes back to its pin. — `2a0ffa2a`
8. Tests that the sheet's «إغلاق» and Escape return the focus to the pin. — `2a0ffa2a`
9. The ceiling's number comes from `MAP_PINS_CEILING`, formatted for the language. — `4faaca45`
10. `map.pin`'s catalogue comment is corrected. — `4faaca45`
11. The non-modal Sheet is described in the layer's comment and in foundation's Sheet row. — `27341a91`
12. The overview's build line names the site's map. — `27341a91`
13. Architecture §6 says why the map is `role="application"` and what that costs. — `27341a91`
14. Findings 134, 135 and 136 are recorded. — `664ba099`

**The plan's commits:**
- `refactor(spaces): share the carrier and date rules`: `carrierOf` and `updatedAgo` move to `shared/lib` (S3).
- `feat(platform-settings): read the public contact`: `VITE_CONTACT_EMAIL` and `VITE_CONTACT_WHATSAPP`, each kept only when valid; `PlatformContact` (S11, decision 5); finding 40's evidence line.
- `feat(map): show one place on a map`: `PlaceMap`, whose pin is a picture and never a button (PU-026).
- `feat(directory): show a space's public page`: the page itself, in U8's order:
  - prices per audience and by shift (U9);
  - hours Saturday first, with today and «عرض كل الأيام»;
  - amenities, about, location with «الاتجاهات», and contacts with their carriers;
  - each fact group's date and «قد يكون تغيّر» (U4);
  - an unverified space's notice, with the platform's contact in a dialog;
  - an aside from 1024 px, a breadcrumb from 768 px, and a back link and the WhatsApp/Call bar below it;
  - «لم نجد هذه المساحة» for a missing space;
  - finding 131: no closure's notice until step 10.

## Scope / Acceptance criteria / Out of scope

**Scope:**
- `shared/lib`: `carrierOf`, `updatedAgo`.
- `shared/map`: `PlaceMap`; and the overlay order (carried).
- `features/platform-settings` (new).
- `features/directory`: the page's repository call, query and view; `hooks/page/`, `components/page/`, the page's services; and the carried map fixes.
- `pages/site`: the `/spaces/:slug` route and `SpacePage`.
- Copy: `directory.page`, `platformSettings`, `site.links.space`.
- `apps/web/.env.example` and `vite-env.d.ts`.
- Docs: `directory.md`, `architecture.md`, `setup.md`, `overview.md`, `spaces.md`, `foundation.md` (the Sheet row), and findings 40, 131 and 134–136.

**Acceptance criteria (PR 3's, without PR 3b's parts):**
- [x] `/spaces/:slug` shows the space's page, titled by its name, in U8's order at every width. A hidden, deleted or unknown space shows «لم نجد هذه المساحة» with «تصفّح المساحات».
- [ ] The live status is read every 60 s while the page is visible. **PR 3b.**
- [x] Prices per audience. Hidden prices are explained with their date. Each fact group shows its date, and «قد يكون تغيّر» when stale. Hours with today and the shifts once. The amenities as one list. Contacts with their values and a phone's carrier. The static map's pin is `role="img"`. The breadcrumb from 768 px, «العودة إلى المساحات» below it. The WhatsApp/Call bar below 768 px. (The gallery is PR 3b; until then the page says «لا توجد صور بعد» only when a space has no photo.)
- [x] An unverified space's notice offers the platform's contact: the configured email alone until a WhatsApp number is configured, and neither when neither is set.
- [x] The same checks as before; CI below.

**Out of scope:** the photos' gallery and viewer, and the live status's 60 s refresh (PR 3b). Home, About and the error states (PR 4). No API, `packages/shared`, schema, migration, seed or dependency change.

## Change type

Feature (web), with documentation and one comment in the design-system layer (the Sheet). Labels: `feat`, `area:web`, `area:docs`, `area:design-system`.

## Evidence

Run locally on the head (each line is the command's own output):
- `npm run lint`, `npm run typecheck`: exit 0 on every commit.
- `npm run test:unit -w @masaha/web`: `Test Files  115 passed (115)` / `Tests  917 passed (917)`.
- `npm run test:component -w @masaha/web -- src/shared/map src/features/directory src/features/platform-settings src/features/spaces src/pages/site src/shared/design-system src/shared/routing`: `Test Files  90 passed (90)` / `Tests  668 passed (668)`.
- Production build exit 0. `npm run check:build`: "No dashboard code in the site's first download." / "No data-table or leaflet, nor Leaflet's stylesheet, in the site's first download."
- `npm run check:classes`: `No physical direction or arbitrary-value classes in 1212 files.`
- `npm run format:check`: `All matched files use Prettier code style!`
- `npm run check:links`: `2587 links in 209 documents and 1720 source files all resolve.`
- The site's first download is **999,477 bytes in 7 chunks** (PR 2: 992,328; the difference is the new catalogue lines). No leaflet, data-table or dashboard chunk in it.
- **Seen failing first:**
  - the carried fixes, and the services' and repository's tests (65–69);
  - separate breaks for the `wa.me` digits, the box's rounding, the picking guard, the busy section and the pin's focus hand-back;
  - tests 70–75 and 79, each proven by its planned break: 404 shown as a failure; the hidden line without its date; the bar always; prices after hours; the aside at every width; `none` never shown; the last search dropped;
  - test 64 (`role="button"`).
- **Real run** on `masaha_dev`, in local headless Chrome over CDP, Arabic light and English dark:
  - a verified space at 390, 768 and 1440: the order, the aside, the breadcrumb, the back link and the bar;
  - «عرض كل الأيام»;
  - an unverified space with hidden prices, and its dialog with the email alone, then both channels, then none;
  - a stale group's badge;
  - an unknown slug;
  - the carried items in the browser: the pins' loading line; the pick ending with the map (including the dev StrictMode run); the map's near-me line; the tab order; the picking card under the map at 768 px; Escape on the card;
  - the width break: with the main column's `lg:col-span-8` removed, the column collapsed to one grid column; restored.
- **Not run locally (CI judges):** the full `test:component` lane, `test:unit` of `apps/api` and `packages/shared`, and `test:api` (no API change).

## Screenshots

Taken in the real run; attached by the owner:
- `3a-verified-*` (6)
- `3a-hours-*`
- `3a-unverified-*`
- `3a-dialog-{email,both,none}-*`
- `3a-stale-*`
- `3a-unknown-*`
- `3a-carried-*`
- `break-main-column.png` and `break-main-column-restored.png`

## Definition of Done checklist

- [x] Acceptance criteria met for 3a, scope kept (the 3b items are named above).
- [x] Lint and typecheck clean; build passes.
- [x] Tests added in the owning lane and passing.
- [x] No hardcoded user-facing text; both catalogues (ar, en) updated.
- [x] UI checked in RTL and LTR, light and dark, phone and desktop.
- [x] Authorization enforced on the server for any protected action (public reads only).
- [x] Triggered documentation updated in this PR; no deferred document's trigger met.
- [x] Each fact has one home; nothing claimed that is not built.
- [x] Every claim above names the test or command that proves it.
- [x] Atomic history, pushed, PR description complete.
