# PUBLIC — PR 3a report (`feat/space-page`, the Space details page, commits 1–4 + carried from #105)

Executor: Claude Code (Opus 5.5), 2026-10-22. Written as the work goes.

## 1. First checks (before any edit)

- `gh pr view 105` → `MERGED a3828e09025f017c16fa76e881592a63c3672bff`. `main` = `origin/main` = `a3828e09`,
  `git status --short` empty.
- Base diff `git diff --name-status 644908a8 origin/main`: `apps/api/.env.example`, `apps/api/src/db/seed/demo.ts`,
  `demoDirectory.api.test.ts` (A), `demoDirectory.ts` (A), `run.ts`, `docs/development/setup.md` — the seed item
  merged before #105; no web code file this plan names. `packages/shared` unchanged.
- Open PRs: none (`gh pr list --state open` → `[]`).
- Check 5a: `useMediaQuery` exported from the layer (`index.ts:210`). Check 5i: `normalisePhone(input: string):
  string | null` (`core/phone.ts:21`) and `emailSchema` (`core/fields.ts:24`), both from `@masaha/shared/core`.
- `packages/shared/src/directory/responses.ts` `PublicSpace` as §9 uses it; it carries **no live status** — so in
  3a the page's status panel shows today's hours and the distance (the page's own read); the status itself is
  3b's `useLiveStatusQuery`.
- Findings: the index's highest 133 (131 reserved); carried 134–136; a new one would take 137.
- Docker: `masaha-postgres-1` already up (healthy). `npx prisma migrate status` → `23 migrations found` / `Database
  schema is up to date!`.
- **Data inventory** (`scripts\inventory3a.mjs` → `inventory3a.out.txt`, plain GETs): 59 listed spaces, 59 pins.
  The cases: a verified space with shift prices, student prices, phone + WhatsApp + Instagram, 7 amenities, a
  description, 3 photos → **`noor-hub`** (also `deir-al-balah-campus`, `masaha-demo`); an unverified space with
  hidden prices → **`tuffah-place`** (`golden-hub` too); a stale group's badge → **`sabra-lab`** (hours, prices);
  hours never saved → `daraj-corner`; prices never saved → `palm-corner-pr1`; unknown slug → 404. Every 3a case is
  held. API (3320) stopped by id (26016, 18392, 7192); port free.

## 2. Branch

`git switch --no-track -c feat/space-page origin/main` → at `a3828e09`.

## 3. Commits — carried from #105 first

Per commit: `npm run lint` exit 0, `npm run typecheck` exit 0 (outputs `scripts\lint3a.txt`, `tc3a.txt`).

### Carried 1 — `2a0ffa2a` `fix(directory): end the pick with the map` (41) — items 1, 6, 7, 8
- Item 1: `useDirectoryMap` ends the pick when the map's view unmounts (`cancelPick` in a cleanup, judged in a
  microtask so StrictMode's development double run of effects does not end a pick the map just opened for).
- Item 6: `DirectoryMapView.pickUnder` (below 1024 px) places the picking card under the map; the test's width 1000.
- Item 7: Escape on the map (the section) closes the card from 768 px; Escape inside the card closes it and hands
  the focus back to the pin (`SelectedCard`'s own handler, `preventDefault` so the section does not act twice).
- Item 8: a test of the sheet's «إغلاق» and Escape returning the focus to the pin.
- **Red first** (`vitest run --project component src/features/directory/components/map`): `Tests  3 failed | 8
  passed (11)` — item 7 `expect(element).not.toBeInTheDocument()`; item 6 `expected <div …> to be null`; item 1
  `Unable to find an element with the text: مرتبة حسب المسافة من الموقع الذي حدّدته على الخريطة.`. Item 8's test
  was green on the existing code → **own break**: `controls.focusSelected()` removed from `close` → `Tests  1
  failed | 10 skipped (11)` (`expect(element).toHaveFocus()`), restored from a copy.
- **Green:** `Test Files  1 passed (1)` / `Tests  11 passed (11)`.
- Docs: `directory.md` (the card under the map below 1024 px; leaving the map ends the pick; Escape).

### Carried 2 — `378a1079` `fix(directory): reach the chosen space first` (44) — item 2
- `LeafletMarkerMap`: the overlay is drawn **before** the map's panes, `absolute inset-0 z-sticky` inside the
  frame, which becomes `relative isolate` — so it stands above Leaflet's isolated panes without reaching the
  page's sticky bar. **Departure (small):** the overlay's layer is named with the one z-utility open outside the
  layer (`z-sticky`), contained by `isolate`; the alternative was a new `leaflet.css` rule (a layer change beyond
  the plan's allowance). For the reviewer to judge.
- Below 768 px a polite `role="status"` line (visually hidden) in `DirectoryMap`: **proposed words**
  `directory.map.detailsBelow` «{name}: التفاصيل في أسفل الصفحة» / "{name}: details at the bottom of the page"
  (the name not isolated, as the pin's). The focus stays on the pin.
- **Red first** (`--project component src/features/directory/components/map src/shared/map`): `Tests  3 failed |
  21 passed (24)` — `MarkerMap` order `AssertionError: expected +0 to be truthy`; `DirectoryMap` card order the
  same; the phone line `Unable to find an element with the text: مساحة 1: التفاصيل في أسفل الصفحة`.
- **Green:** `--project component src/features/directory src/shared/map` → `Test Files  12 passed (12)` / `Tests
  75 passed (75)`. Docs: `directory.md` (the order and the line).

### Carried 3 — `25e90a91` `fix(directory): keep the pick's centre rounded` (46) — item 3
- `useDirectoryMap`: no `onViewChange` while picking; `boundsText` rounds outward to hundredths (south/west down,
  north/east up, the float's noise trimmed first so `31.55` stays `31.55`).
- **Red first:** unit `boundsText` → `Received: "31.412345,34.345678,31.551234,34.500001"` (`Tests  1 failed | 1
  passed (2)`); component `useDirectoryMap` → `AssertionError: expected [Function] to be null` (`Tests  1 failed
  | 3 passed (4)`).
- **Own privacy breaks** (§3.1): north left unrounded → `Received: "31.41,34.34,31.551234,34.51"` (`Tests  1
  failed | 1 passed (2)`); the picking guard removed → `expected [Function] to be null` (`Tests  1 failed | 3
  passed (4)`). Both restored from copies.
- **Green:** `Tests  2 passed (2)` (unit), `Tests  4 passed (4)` (component). Docs: `directory.md`.

### Carried 4 — `4bc2f3c9` `fix(directory): say what the map does with me` (45) — item 4
- `useLocationStatus` takes `view: 'list' | 'map'`; on the map, a location in use → `directory.near.onMap`
  «موقعك ظاهر على الخريطة. تُرتَّب القائمة حسب المسافة منه.» / "Your location is shown on the map. The list is
  sorted by distance from it." (the owner's words), no privacy sentence, no stop; «تغيير الموقع» and «مسح موقعي»
  kept. While not sorting, no line (as the list).
- **Red first:** `Unable to find an element with the text: موقعك ظاهر على الخريطة. …` (`Tests  1 failed | 11
  skipped (12)`). **Green:** `--project component src/features/directory` → `Test Files  10 passed (10)` / `Tests
  64 passed (64)`. Docs: `directory.md` (the map's line; the privacy line now true on both views).

### Carried 5 — `33c49922` `fix(directory): show the pins loading` (37) — item 5
- `busy: whole.isPending || whole.isFetching || within.isFetching`; `loading` «جارٍ تحميل المساحات…» / "Loading
  spaces…" as a `MapNotice` over the map's foot while `whole.isPending`.
- **Red first** (a held answer): `Unable to find an element with the text: جارٍ تحميل المساحات…` (`Tests  1 failed
  | 12 skipped (13)`). **Own break** (the busy guard back to `answer !== undefined && …`):
  `expect(element).toHaveAttribute("aria-busy", "true")` (`Tests  1 failed | 12 skipped (13)`), restored.
  **Green:** `Tests  65 passed (65)` (directory component).

### Carried 6 — `4faaca45` `fix(directory): word the pins' ceiling` (38) — items 9, 10
- `directory.map.truncated({ count })`, `count` = `MAP_PINS_CEILING` through `Intl.NumberFormat` (`en` /
  `ar-u-nu-latn`): «تظهر أول 1,000 مساحة؛ …» (was «1000»: Arabic now groups as English does — Western digits,
  localisation › Formatting). `map.pin`'s comment: "not isolated (an attribute, never drawn)".
- **Red first:** `Expected: "تظهر أول 1,000 مساحة؛ …"` / `Received: "تظهر أول 1000 مساحة؛ …"` (`Tests  1 failed | 3
  passed (4)`). **Green:** directory component `Tests  65 passed (65)`; `--project unit src/shared/copy` `Tests
  33 passed (33)`.

### Carried 7 — `871bc5bd` `docs: say the sheet and the map as they are` (43) — items 11, 12, 13
- `Sheet.tsx`'s comment and foundation's Sheet row: non-modal on request (`modal={false}`: no scrim, no trap).
  `overview.md`: the site's map in the Directory's build line. `architecture.md` §6: why `role="application"`
  and its cost (browse mode off inside the map). `check:links` → `2573 links in 208 documents and 1674 source
  files all resolve.`

### Carried 8 — `7016998d` `docs(findings): record #105's review findings` (45) — item 14
- 134 (each render rebuilds every marker), 135 (dark: marks vs legend), 136 (the 15 s wait counts the prompt);
  each a file and an index line.

### Plan commit 1 — `739a9bb2` `refactor(spaces): share the carrier and date rules` (50)
- `git mv` of `carrierOf` (+ `Carrier`) → `shared/lib/phone/`, `updatedAgo` → `shared/lib/time/`, with their unit
  tests; `shared/lib/index.ts` exports them; the four `spaces` importers read `@shared/lib`. Docs:
  `architecture.md`'s status line; **also `spaces.md`'s code map** (it listed the moved helpers under `spaces`'
  `services/` — a small departure, to keep it true).
- Moved tests green before and after: `--project unit src/shared/lib src/features/spaces` → `Test Files  18
  passed (18)` / `Tests  93 passed (93)`; `--project component src/features/spaces` → `Test Files  23 passed (23)`
  / `Tests  228 passed (228)`.

### Plan commit 2 — `a60fa2ee` `feat(platform-settings): read the public contact` (48)
- `types/PlatformChannel.ts`, `services/platformContact.ts` (`contactOf`, `platformContact`),
  `components/PlatformContact.tsx`, `index.ts`; copy `platformSettings` (both); `vite-env.d.ts`; `.env.example`
  with `VITE_CONTACT_EMAIL=masahagaza@gmail.com` and `VITE_CONTACT_WHATSAPP=` (the owner's approval note wins over
  §9's "empty"). Docs: `setup.md` › The web, `architecture.md` §3 (S11, #PRNUM), finding 40's evidence line.
- **Red first (= the breaks of 62, 63):** unit `Cannot find module './platformContact'`; component `Failed to
  resolve import "./PlatformContact"`. On the way: the link's name read `بريدteam@example.com` (no space between
  the word and the value) — a space added. **Green:** unit (with `src/shared/copy`) `Test Files  3 passed (3)` /
  `Tests  36 passed (36)`; component `Tests  2 passed (2)`. `check:links` → `2574 links … all resolve.`

### Plan commit 3 — `106985f0` `feat(map): show one place on a map` (34)
- `PlaceMap` (lazy) + `LeafletPlaceMap` + `types/PlaceMapProps.ts` (the plan's file list omits the props type; one
  file more): zoom 16, the `.map-pin`, `role="img"` + `aria-label`, `interactive={false}`, `keyboard={false}`;
  the map takes no keyboard panning and no wheel zoom (the page scrolls past it). Docs: `architecture.md` §6.
- **Red first:** `Failed to resolve import "./PlaceMap"`; then, my own defect, `Unable to find role="img" and name
  "Noor Hub on the map"` — the naming effect ran before `MapContainer` rendered its children; moved into a child
  (`PlacePin`). **Green:** `Tests  1 passed (1)` (axe-clean). **Break 64** (`role="button"`) → `Unable to find
  role="img" and name "Noor Hub on the map"` (`Tests  1 failed`), restored.

### Plan commit 4 — `feat(directory): show a space's public page` (43) — in progress
- **Red first** for the services (65–69): `Test Files  6 failed | 9 passed (15)` — each `Cannot find module`.
  On the way, my own expectations corrected: English prices are `₪6`/`₪250` (whole, no decimals), the Rimal–Khan
  Younis pair is 23.2 km (not 23.3), and Arabic says two days ago «أول أمس». Repository `space`: `TypeError:
  repository.space is not a function` (`Tests  1 failed | 3 passed (4)`), then green.
- **Own break 68** (§3.1, the `wa.me` form): `https://wa.me/${value}` → `-   "href": "https://wa.me/970599111001"` /
  `+   "href": "https://wa.me/+970599111001"`, restored.
- **A slip, stated:** the hook `useSpacePage`, the components and `SpacePage` were written before tests 70–75 and
  79. Each of those tests was therefore proven by **its planned break**, seen red, restored
  (`scripts\breaks3a.py`, which restores from a copy in a `finally`):
  - 70 (404 shown as a failure): `AssertionError: expected 'failed' to be 'notFound'` (`Tests  1 failed | 3
    skipped (4)`);
  - 71 (the hidden line without its date): `expected { title: 'الأسعار', …(8) } to match object { state:
    'hidden', …(3) }`;
  - 72 (the bar always): `expected { label: 'التواصل السريع', …(2) } to be null`;
  - 73 (prices after hours), at 390 and 1440: `expected [ 'ساعات العمل', 'الأسعار', …(4) ] to deeply equal [
    'الأسعار', 'ساعات العمل', …(4) ]` (`Tests  2 failed | 3 skipped (5)`);
  - 74 (the aside drawn at every width, §3.1's width break): `expected document not to contain element, found
    <aside` (`Tests  1 failed | 4 skipped (5)`);
  - 75 (`none` never shown — the dialog without the page's contact): `Unable to find an element with the text:
    لا توجد وسيلة تواصل متاحة الآن.`;
  - 79 (the last search dropped), at 1440 and 390: `expect(element).toHaveAttribute("href",
    "/spaces?q=Hub&verified=1")` (`Tests  2 failed | 5 skipped (7)`).
- On the way, my test's defect: test 79 read the Directory's `h1` before the lazy route swapped; it now waits for
  the space's own heading.

### Plan commit 4 — `d9415649` `feat(directory): show a space's public page` (43) — committed
- Checks before the commit: `lint` exit 0; `typecheck` exit 0; `check:links` → `2587 links in 209 documents and 1720
  source files all resolve.`; `check:classes` → `No physical direction or arbitrary-value classes in 1212 files.`;
  `--project unit src/features/directory src/shared/copy` → `Test Files  18 passed (18)` / `Tests  70 passed (70)`;
  `--project component src/features/directory src/pages/site src/shared/map src/features/platform-settings` →
  `Test Files  23 passed (23)` / `Tests  135 passed (135)`.
- Docs: `directory.md` (what it does, who uses it, how it composes, «A space's page on the web», seven web
  decisions, code map, open findings 131 and 134–136, web history incl. the carried items), `architecture.md` §2,
  `overview.md`, `spaces.md` (the carrier line), finding 131 + index. `docs/README.md` needed no change (its
  directory line already names the public page). No deferred-document trigger met.
- **Departures (small):** `PriceGroupView`'s cell label carries its language (`LocalText`) so a label in the other
  language is marked; `SITE_PATHS.space` with `publicSpacePath` as the one link builder (§9), no `spacePath` (§2
  named one) and `DirectoryPage` unchanged; `useDirectoryReturn` reads an address kept on **every change** of the
  directory's address (page links and the view switch included), not only on writes; the fixture
  `src/test/publicSpace.ts` (shared by three test files); the hook test adds a fourth case (the distance).

## 4. STOPPED (2026-10-22) — the branch is past 75 files

`git diff --name-only origin/main | wc -l` → **100** (`100 files changed, 3031 insertions(+), 51 deletions(-)`), no
stray file (only `.ts`/`.tsx`/`.md` and `apps/web/.env.example`). Per commit: carried 6, 10, 5, 7, 8, 5, 4, 4
(= 49 with overlaps); plan 1: 11, 2: 15, 3: 6, 4: **53**. The prompt (§1.5): "stop and ask only past 75 files".

**Not done yet:** the head's checks (§3.2), the real run, `#PRNUM`, push, PR. Branch `feat/space-page`, head
`d9415649`, 12 commits on `a3828e09`, not pushed; `git status` clean; no server running (3320, 5320 free since the
inventory); `masaha_dev`: GETs only.

**Options for the owner:** (a) accept ≈ 100 files for PR 3a and let me continue (head checks, real run, push);
(b) split: push the eight carried commits + plan commits 1–3 as one PR (≈ 47 files) and commit 4 as the next
(≈ 53); (c) another cut the owner names.

## 5. Resumed (2026-10-22) — the owner accepts ≈ 100 files as one PR

The owner's word: keep PR 3a whole; continue from the head's checks. The phone line's words stand for the review.

### On the head (`d9415649`), once each
- No `app-b` vitest/tsc/dev process (count 0); free memory 5,166,456 KB before unit, 5,195,480 KB before component.
- `npm run test:unit -w @masaha/web` → exit 0, `Test Files  115 passed (115)` / `Tests  917 passed (917)`
  (`scripts\lane3a-unit.txt`).
- `npm run test:component -w @masaha/web -- src/shared/map src/features/directory src/features/platform-settings
  src/features/spaces src/pages/site src/shared/design-system src/shared/routing` (the prompt's folders, plus
  `src/shared/routing`, whose `publicSpacePath` comment changed) → exit 0, `Test Files  90 passed (90)` / `Tests
  668 passed (668)` (`lane3a-component.txt`). `shared/lib` and `shared/copy` hold unit tests only (in the unit lane).
- Production build exit 0; `check:build` exit 0 — `No dashboard code in the site's first download.` / `No
  data-table or leaflet, nor Leaflet's stylesheet, in the site's first download.`; `format:check` → `All matched
  files use Prettier code style!`; `check:classes` → `No physical direction or arbitrary-value classes in 1212
  files.`; `check:links` → `2587 links in 209 documents and 1720 source files all resolve.`
- First download (`firstDownload-3a-head.txt`): **999,477 bytes, 7 chunks** (PR 2's head: 992,328; +7,149, the new
  catalogue lines); no leaflet, data-table or dashboard.

## 6. The real run (2026-10-22)

API 3320, Vite 5320, worker A's `masaha_dev`; local headless Chrome over CDP (`scripts\cdp3a.mjs`, `run3a.mjs`;
Enter sent with its text). `apps/web/.env`: `VITE_CONTACT_EMAIL=hello@example.com` appended for the run, then
`VITE_CONTACT_WHATSAPP=0599 000 099` for the both-channels case, then both removed — the file's md5 checked equal to
before (`.env: OK`). No copy of `.env` kept (it holds secrets). Outputs `scripts\run3a-*.txt`; shots `shots\pr3a\`.

| Case | Result | Shots |
|---|---|---|
| Verified `noor-hub`, ar light and en dark at 390, 768, 1440 (reached from `/spaces?q=Noor`) | title «نور هب · مساحة» / "Noor Hub · Masaha"; one `h1`; sections «الأسعار · ساعات العمل · المرافق · عن المساحة · الموقع» + «التواصل» below 1024; «الحالة» card first below 1024, aside «الحالة والتواصل» at 1440; prices tabs «اليوم كاملًا · صباحي · مسائي», general then «للطلاب»; today «السبت – الخميس · اليوم · 08:00–22:00» (`aria-current`); the shifts line; amenities with icons; the pin `role=img` «موقع نور هب على الخريطة», no tabindex; «الاتجاهات» → `google.com/maps/search/?api=1&query=31.5228,34.4489`, new tab; contacts «واتساب → wa.me/970599111001», «اتصال — جوال → tel:+970599111002», Instagram; breadcrumb from 768 «الرئيسية › المساحات › نور هب», «المساحات» → `/spaces?q=Noor`; at 390 «العودة إلى المساحات» → `/spaces?q=Noor` and the bar «واتساب \| اتصال» | `3a-verified-*` (6) |
| «عرض كل الأيام» (`hours-hub`, 6 grouped rows) | grouped «الاثنين، الثلاثاء» → each day (7 rows), `aria-expanded` true, «عرض مختصر» | `3a-hours-*`, `3a-hours-all-*` |
| Unverified `tuffah-place`, hidden prices | notice «جمع فريقنا … · آخر تحديث للمعلومات أمس» with «هل تدير هذه المساحة؟ تواصل معنا»; prices «لا نعرض الأسعار …» with «آخر تحديث للأسعار قبل 61 يومًا» and «قد يكون تغيّر»; bar «واتساب» only | `3a-unverified-*` |
| Its dialog: email alone → both → none | email: «بريد hello@example.com» (`mailto:`, same tab); both: «واتساب +970599000099» primary (`wa.me/970599000099`, new tab) then the email; none: «لا توجد وسيلة تواصل متاحة الآن.», no link | `3a-dialog-{email,both,none}-*` |
| A stale group's badge (`sabra-lab`) | «قد يكون تغيّر» on prices and hours; «تأكّد من السعر مع المساحة قبل الذهاب.» | `3a-stale-*` |
| Unknown slug `/spaces/no-such-space` | «لم نجد هذه المساحة» / «ربما أُزيلت …», «تصفّح المساحات» → `/spaces`; title «صفحة المساحة · مساحة» | `3a-unknown-*` |
| Carried 5 — the pins' first load (pins request held 8 s via CDP `Fetch`) | «جارٍ تحميل المساحات…» over the map's foot, section `aria-busy="true"`; gone once the pins arrive | `3a-carried-loading-*` |
| Carried 1 — the pick ends with the map (denied → set on the map → placed → «تغيير الموقع» → «قائمة» → «خريطة») | the crosshair **stays** after the StrictMode mount (dev); on the list the pin's line and the distance order (`sort=distance [Masaha-Near 31.41,34.395]`); the map reopens with **no crosshair** | `3a-carried-pickends-*` |
| Carried 4 — the map's own near-me line | «موقعك ظاهر على الخريطة. تُرتَّب القائمة حسب المسافة منه.» with «تغيير الموقع \| مسح موقعي», no privacy sentence, no stop | `3a-carried-mapline-*` |
| Carried 2 — the overlay before the pins | Tab from the view switch at 1440: «Filters → Nearest to me → Close → View details → Map of spaces → (the pins)»; at 390 the live line «مساحة تجريبية: التفاصيل في أسفل الصفحة» | `3a-carried-chosen-*` |
| Carried 6 — the picking card under the map at 768 | not in the overlay, after the map | `3a-carried-pickunder-ar-light-768` |
| Carried 7 — Escape on the card (1440) | Escape on the pin and inside the card: the card gone, the focus on the pin | `3a-carried-escape-en-dark-1440` |
| **Width break** — the main column's `lg:col-span-8` removed once (HMR) | the column collapses to one grid column (72 of 1216 px), the sections crushed beside the aside; restored → 800 of 1216 | `break-main-column.png`, `break-main-column-restored.png` |

- Page errors: none in every case. My `carried` probe's DOM-order flag read the wrong «عرض التفاصيل» at 1440
  (`detailsBeforePins:false`); the Tab sequence above is the evidence. **Departure:** the width break gives one
  grid column, not "full width" as §13 expected — the same proof that the span holds the layout.
- Not performed, by design: the photos' viewer and the live status's refresh (PR 3b).
- Servers stopped by id (19316, 1168, 4944, 16484); ports 3320 and 5320 free; no headless Chrome left;
  `git status` clean. `masaha_dev`: GETs only.

## 7. #PRNUM, push, PR, CI

- `git grep "#PRNUM" HEAD` listed 15 lines in 6 documents; the next number was 107 (latest 106, worker B's open
  #106, checked again just before the push). `git filter-branch` replaced it in each commit's tree; `git grep -n
  "#PRNUM" HEAD` empty (exit 1); the stat unchanged, `100 files changed, 3031 insertions(+), 51 deletions(-)`. The
  rewrite renewed the shas from `27341a91` on: carried 7 `27341a91`, carried 8 `664ba099`, plan 1 `64930130`, plan 2
  `1afdf235`, plan 3 `1b0b4fe0`, plan 4 `a85151b9` (carried 1–6 unchanged).
- `git push -u origin feat/space-page`; **PR #107** https://github.com/Basel-Ghonaim/masaha/pull/107, title
  `feat(directory): show a space's public page`, labels `feat`, `area:web`, `area:docs`, `area:design-system`;
  description `scripts\pr-body-3a.md`, with "Carried from #105" and the phone line's words for the review.
- **CI on `a85151b9`:** check:links, lint, format:check, typecheck, test:unit, test:component, check:classes,
  build, test:api — all `pass`; CodeRabbit `pass` (rate limited). `mergeStateStatus` → **`CLEAN`**.
- **Conflict check:** #106 (`feat/subscriptions`, head `d0acc06b`) shares only `docs/architecture/findings/README.md`
  and `docs/project/overview.md`; `git merge-tree --write-tree origin/feat/space-page origin/feat/subscriptions` →
  exit 0, tree `48df6b99` — no conflict.
- `git status --short` clean; ports 3320, 5320 free. Not merged.
