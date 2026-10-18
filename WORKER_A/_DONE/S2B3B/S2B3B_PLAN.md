# S2b-3b — Add a space, with its pin on the map · Plan

Worker A · main folder · branch `feat/admin-add-space` from `origin/main` (`bcb2e04`, verified clean and level with origin) · saved after approval to `C:\Users\basel\.prompt\MASAHA_WORKER_A\PLAN\S2B3B_PLAN.md`.

## 1. Summary

The admin adds a space from the spaces list: a page at `/dashboard/admin/spaces/new` with two sections, *Basics* and *Location*. *Location* includes a real map (React Leaflet over OpenStreetMap, loaded lazily) and a coordinates field. There is one submit, one `POST /admin/spaces`, and then a toast and the list. Building it needs:
- `shared/map`, a generic point picker;
- a new area field in `lookups`, read from the public catalogue;
- two small options in `shared/forms`.

The build gets two fixes:
- the data table moves to its own design-system entry (finding 45);
- `check:build` refuses Leaflet and TanStack Table in the site's first download.

## 2. Contract

**Scope**
- The page `spaces/new` under the admin branch, guarded `ADMIN`, lazy. It has a breadcrumb back to *Spaces*, then the *Basics* card (names and descriptions in both languages) and the *Location* card (area, both addresses, both landmarks, the pin with its coordinates field), then one "Add space" button.
- The "Add space" link on the spaces list.
- `features/spaces`:
  - the `create` call;
  - `useCreateSpace` (refreshes `['admin']`, then a toast "{name} added");
  - `useAddSpaceForm`;
  - the two section components (`BasicsFields`, `LocationFields`) and `AddSpaceForm`. `AddSpaceForm` takes the area field as a slot from the page.
- `features/lookups`: `AreaSelect`, one active area grouped under its governorate, from `GET /lookups` (`['public', 'lookups', 'catalogue']`).
- `shared/map`: the `PointPicker` and the coordinates helpers. Its stylesheet is `shared/design-system/leaflet.css`, imported by `shared/map` only.
- `shared/forms`: `prepare` and `failureLines` (§5, S8).
- The build:
  - the `@shared/design-system/data` entry;
  - the `leaflet` and `data-table` chunk groups;
  - `check:build`'s library and CSS checks;
  - the lint rules.
- Dependencies: `leaflet`, `react-leaflet@5` (made for React 19), `@types/leaflet` (dev).

**Acceptance criteria**
- [ ] A space is added by clicking the map, and another by pasting "31.52, 34.45". Each creation returns to the list with "{name} added".
- [ ] A point outside `GAZA_STRIP_BOUNDS` is refused on the field, and nothing is sent.
- [ ] Field errors are checked in the browser by the shared schema. The server's 422 lands on its fields. 409 is said plainly, and 429 counts down.
- [ ] With the tiles blocked, a line says so and the form still submits. The same happens when the map's code fails to load (S7).
- [ ] No pin until the admin places one. A click places it, and it can be dragged. The field moves it, and the map moves the field.
- [ ] The pin is drawn from the tokens. "© OpenStreetMap contributors" is always visible. The container is `dir="ltr"`, with the zoom at the start and the attribution at the end, in both languages.
- [ ] The manifest shows TanStack Table, Leaflet and Leaflet's CSS out of the first download. `check:build` fails when each is imported statically into the site (each break made once).
- [ ] Finding 45 is resolved. Finding 27 is studied, with its outcome written into it. Finding 46 is recorded.
- [ ] The required documents are updated (§7).

**Out of scope:**
- the edit route and screen, and the "Edit" item (S2b-4);
- the facts sections (hours, prices, amenities, contacts) and photos;
- directory markers;
- dark tiles (D10);
- a warning on leaving with unsaved changes;
- anything in `apps/api` or `packages/shared`.

## 3. Reading done

CLAUDE.md, workflow, the documentation map, and the findings index. Then:
- `features/spaces.md`, `space-links.md`, `lookups.md`;
- frontend architecture §1–§3, §6, §7;
- foundation §2–§3, §8–§12 (the Field, Input, Textarea, Select/Combobox and Button rows);
- `localisation.md`;
- testing §1–§3;
- the API contract: *Lookups (public)* and *Spaces (the admin)*;
- data-model › *Spaces*;
- findings 27, 33 and 45;
- `vite.config.ts`, `checkBuild.ts`, `dashboardOnly.ts`, `eslint.config.js`;
- the designs: 15 and 16 (add page), 01 and 02 (list), and the prototype's `profile-a.jsx`.

From the code:
- `useServerForm` and `schemaResolver`, `useRefusalView` and `useFormFailure`;
- `Field`, `GovernorateAreaSelect`, `SpacesPage`, `PageHeader` and `TopBar`, `routes.tsx`;
- the spaces repository, the toasts and `useRefreshAdmin`;
- `createSpaceSchema` and `gazaStrip.ts`;
- rolldown's code-splitting types.

## 4. The settled decisions, as built

- **D1:** `AddSpaceForm` is one `<form>`. It holds the *Basics* card and the *Location* card, then `FormFailure` and the "Add space" submit at the end, with one `POST`.
- **D2:**
  - On a 201, `useCreateSpace` awaits `refresh()` (the whole `['admin']` scope, as #50 does), then calls `toastDone(toasts.added, name)`. The name comes from `spaceNameOf`, marked with its language.
  - The form then calls `onCreated()`, and the page navigates to the list. This follows the `onSaved` pattern from lookups.
  - There is no edit route and no "Edit" item.
  - The list's "Add space" is a `Button asChild` around a `Link`.
- **D3:** `BasicsFields` and `LocationFields` render the parts of the form's view they are given, so S2b-4 can put each in its own card. No prop exists for the edit only.
- **D4:**
  - `lookups` exports `AreaSelect`. It is a `Select` with one `SelectGroup` per governorate, labelled with its name, holding that governorate's areas. Names are in the interface's language.
  - While loading, or after a failure, one disabled option says so, as the place field does.
  - Props: `value: number | null`, `onValueChange(id)` and `ref` (to the trigger, so that a refusal can focus it). It reads its id, label and descriptions from the Field.
  - The page passes it in `AddSpaceForm`'s `areaField` slot. A hidden area is never offered, and the server refuses it (`invalid_choice`, worded on the field).
- **D5:**
  - The shared `createSpaceSchema` checks the form in the browser.
  - A 422 lands on its fields, and the first such field takes the focus.
  - A 409 has its own line: "Another space with this name was added at the same moment. Add it again." It comes through `failureLines`, with the request's reference.
  - A 429 counts down and holds the submit (`FormFailure`).
- **D6:**
  - `shared/map` exports `PointPicker`, `parseCoordinates`, `formatCoordinates` and the `MapPoint` type.
  - `PointPicker` is a thin wrapper. Its Leaflet part is a `React.lazy` module, so Leaflet arrives only when the picker renders.
  - The directory's markers stay the directory's.
  - Architecture §6 gets its line.
- **D7:**
  - The map opens fitted to `bounds`, which the feature passes: `GAZA_STRIP_BOUNDS`.
  - With no value, there is no pin.
  - A click calls `onChange(point)`. The pin is a draggable `Marker`, and `dragend` calls `onChange`.
  - The coordinates field (`dir="ltr"`) holds the form's `location` value as text. A map change writes `formatCoordinates(point)` into it. A parseable text moves the pin, and the map pans to it if it is out of view.
  - A point outside the box is refused on submit by the schema's `out_of_range`, with the field's own line.
  - The pin is an `L.divIcon` with the class `map-pin`, styled in `leaflet.css` from the tokens. Leaflet's default icons are never used.
- **D8:**
  - The tile layer's `tileerror` (with no tile loaded yet) shows the line under the map: "The map didn't load. Enter the coordinates instead."
  - The coordinates field still sets the location, and the form still submits.
- **D9:**
  - `apps/web/src/shared/design-system/leaflet.css` `@import`s Leaflet's own stylesheet (S11). It then overrides, on semantic tokens:
    - the container's border, radius and background, and its focus outline (`ring`);
    - the zoom buttons and the attribution (`card`, `foreground`, `border`, `muted-foreground`, the type styles);
    - the `map-pin` itself.
  - Only `shared/map`'s lazy module imports it, so it is CSS of that lazy chunk.
  - The attribution's words come from the catalogue: «© مساهمو OpenStreetMap» / "© OpenStreetMap contributors". The name "OpenStreetMap" stays untranslated in both languages. They are linked to `https://www.openstreetmap.org/copyright` in both languages, in code (no markup in the catalogue). The control's `prefix` is `false`.
  - The container is `dir="ltr"`. The zoom control sits at the top start: `topleft` in English, `topright` in Arabic. The attribution sits at the bottom end, the other corner. The zoom buttons' titles come from the catalogue.
- **D10:** the standard tiles, `https://tile.openstreetmap.org/{z}/{x}/{y}.png`, in both themes.
- **D11:**
  - `apps/web/src/shared/design-system/data.ts` exports `DataTable`, `createDataTableColumnHelper` and their types.
  - `index.ts` drops those lines and nothing else.
  - Both importers move to `@shared/design-system/data`: the space-links admin list and the showcase's DataTable section.
  - The boundaries rule allows `data.ts` beside `index.ts`.
  - The manifest is read before and after; the first download's size is recorded in the PR.
- **D12:**
  - `scripts/libraryChunks.ts` names two groups, with `includeDependenciesRecursively: false` so that React is never pulled in:
    - `leaflet`: `node_modules/(leaflet|react-leaflet|@react-leaflet)/`;
    - `data-table`: `node_modules/@tanstack/(react-table|table-core)/`.
  - `vite.config.ts` adds both groups. `check:build` refuses a first-download chunk of either name.
  - Each break is made once, by a static import into the site, and seen failing.
- **D13 (finding 27): study, and expect to leave it open.**
  - What rolldown offers: a group's `test` sees only the module id. The one built-in tag, `$initial`, marks what the entry reaches. Neither can say "used only by the dashboard".
  - Why no group fixes it: a catch-all group for the rest would also take the site's lazy pages.
  - I read the manifest before and after. If the cycle is still there, the finding stays open and **its file is left untouched** (the owner's change 1: a finding gains only its status and a dated resolution). The study then goes in the PR description and the report: what rolldown offers, why no group fixes it, and the manifest before and after. If a clean rule does fold it, I fold it, prove it by the manifest, and resolve the finding.
- **D14:**
  - `leaflet@^1.9.4`, `react-leaflet@^5.0.0` (peer `react ^19`), and `@types/leaflet@^1.9.22` as a dev dependency;
  - `package-lock.json` is mine in this item.

## 5. Stronger decisions

Each item gives what, why, its cost, and a recommendation (rec).

- **S1. Leaflet is imported only by `shared/map`, by lint**, as Axios is held to `shared/api`.
  - Change: `leaflet`, `react-leaflet` and `@react-leaflet/*` join the restricted list. A block for `shared/map/**` keeps the list without them, with the list extracted to one constant so the two blocks never differ.
  - *Why:* the directory will reach the map through `shared/map` too, and D6's "generic picker" stays the one door.
  - *Cost:* about 15 lines in `eslint.config.js`, and a rule test.
  - *Rec:* yes.
- **S2. `check:build` also refuses Leaflet's CSS in the first download.**
  - Change: the check reads the `css` of the entry and of every chunk it imports, and fails if any contains `.leaflet-container`.
  - *Why:* the named chunk proves the JS only, and a static CSS import would slip by.
  - *Cost:* about 15 lines, and unit tests.
  - *Rec:* yes. It is inside D12's "and Leaflet".
- **S3. Each library group must exist in the manifest,** or the check fails, as it does today for the missing dashboard chunk.
  - *Why:* a group test that stops matching, after a path change or a renamed package, would otherwise make the check pass with nothing to hold.
  - *Cost:* a few lines.
  - *Rec:* yes.
- **S4. The coordinates field reads Arabic-Indic digits, the Arabic comma (،) and the Arabic decimal separator (٫)**, as well as "31.52, 34.45", "31.52,34.45" and "31.52 34.45".
  - *Why:* an Arabic keyboard types them.
  - *Cost:* a few lines in the pure parser.
  - *Rec:* yes.
- **S5. The map's view is held to the box**, with `maxBounds` set to the box plus a margin.
  - *Why:* the admin cannot pan to a place no pin may take.
  - *Cost:* one prop.
  - *Rec:* yes.
- **S6. The pin is named with its coordinates** (the marker's `title`: "Pin at 31.52050, 34.45350").
  - *Why:* a screen reader hears where it is, and the component test reads the same name.
  - *Cost:* one catalogue line.
  - *Rec:* yes.
- **S7. A map that cannot load its own code** (offline: the lazy chunk fails) shows D8's line too. `lazy(() => import(...).catch(() => failed view))` does it, with no error-boundary class.
  - *Why:* offline, the tiles are not the only thing missing.
  - *Cost:* about 3 lines.
  - *Rec:* yes.
- **S8. `shared/forms` gains two options. This changes a shared mechanism, so it is listed for approval.**
  - `prepare(values)`, which builds the schema's input from the form's values.
    - Why the resolver must apply it: `toFieldErrors` words each code from the input it is given. It must read the prepared input, or else a blank optional field would read as `too_short`, and an empty location as `invalid_format` rather than `required`.
    - In this form it does three things: blank optional texts become absent, the coordinates text becomes `{ lat, lng }` (left as text when it cannot be read, so it fails as `invalid_format`), and the area stays a number.
  - `failureLines`: the form's own words for a refusal on no field (`conflict` here).
  - *Why:* without them, no form can have an optional text field or a field typed otherwise than the contract. The edit screen and the owner's profile will need the same.
  - *Cost:* two options, with tests in their lanes, and architecture §3 › *Forms* updated.
  - *Rec:* yes.
- **S9. The area field reads the public catalogue,** under `['public', 'lookups', 'catalogue']` (§7's scope for public data).
  - *Why:* D4 says so, and the admin's lookups writes never refresh it. An area hidden less than 30 s earlier may still be offered; the server then refuses it on the field ("This area is no longer available. Choose another.").
  - *Cost:* none.
  - *Rec:* accept as is.
- **S10. Every optional field is marked "Optional"** in the Field's `labelEnd`. See design issue 2.
- **S11. `leaflet.css` `@import`s the package's stylesheet** rather than copying it.
  - *Why:* it stays in step with Leaflet's version. The overrides alone are ours.
  - *Cost:* none. Leaflet's two control images are emitted with the lazy CSS.
  - *Rec:* yes.

No rule of the documents is weakened. These rules gain a stated exception, documented where they live:
- "the design system's one public surface": now `index.ts`, `data.ts` and `leaflet.css` (foundation §3, architecture §1);
- "the one reference into the layer from outside": now also `shared/map` → `leaflet.css`.

## 6. Design issues

Proposals. Until approved, the design is kept.

1. **Frames 15 and 16, *Location*:** one "Landmark" field, but the contract has `landmarkAr` and `landmarkEn`. → Two fields side by side, like the addresses: Arabic at the start, English at the end.
2. **Frames 15 and 16:** only the landmark says "Optional". The Arabic name, both descriptions and the English address are optional too. → "Optional" in `labelEnd` on every optional field (S10).
3. **Frame 15:** the area's trigger is narrowed (`md:max-w-xs`), out of line with the two-column grid under it. → The area takes the start column of the same grid, so its edges line up with the Arabic address.
4. **Frames 15 and 16:** the governorate is shown as a helper under the area, and the list offers one governorate's areas. → The grouped list (D4) names the governorate as you choose. No helper.
5. **Frame 15:** the title is written twice: in the top bar and again as a large heading in the content. → The title once, in the top bar (`PageHeader`, as every dashboard page), with the breadcrumb "Spaces › Add space" above the form.
6. **Frames 15 and 16:** the map's hint, "Tap the map to move the pin…", assumes there is already a pin. → "Click the map to place the pin at the space's entrance, then drag it to adjust. Or paste its coordinates." Below it goes the coordinates field, labelled "Coordinates", with the helper "For example 31.52, 34.45".
7. **Frames 01 and 02:** "Add space" sits above the list at the end on a desktop, but between the filters and the list at the start on a phone. → **(Owner's choice: the fallback.)** A row above the list, at the end, at every width. The page composes the row, so `space-links` needs no new slot. *Why not the top bar:* on a phone it already holds the menu, the title, the theme toggle and the avatar.

The owner approved issues 1–6 and agreed with 8.
8. **Frames 15 and 16:** these belong to the edit screen and are left out under D1, so they are not mistakes:
   - the unverified banner;
   - the "last updated" line on each section;
   - Save and "Still correct";
   - the section navigation;
   - the five other sections.

## 7. Related findings

- **45: folded** (D11 and D12). The status changes to *Resolved*, with a resolution line and the manifest's figures before and after. Cost: commit 1.
- **27: studied** (D13). It is expected to stay open, with its file untouched; the study goes in the PR and the report. Cost: a reading of the manifest.
- **33: linked, not edited.** **46 (new):** "The deployment's content-security policy must let the map's tiles load." It covers `img-src https://tile.openstreetmap.org`, beside 33's Google rules.
- **47:** reserved for one case: if the manifest shows another wrapped library (react-day-picker, cmdk) in the first download, it is recorded and not fixed.
- No other open finding touches this item: 8, 35, 43 and 44 were checked.

## 8. Files

None in `apps/api` or `packages/shared` (no licence needed). **Shared with worker B:**
- `docs/features/spaces.md`: I edit only:
  - the header's "built" sentence;
  - *What it does* and *Who uses it*, the web lines only;
  - *Behaviour › On the web*;
  - *Web decisions* and *Web history*;
  - the code map's **Web** line.
- `docs/project/overview.md`: the spaces line only.
- `package-lock.json`: mine. B adds no dependency meanwhile.

**New**
- `apps/web/src/shared/map/`:
  - `index.ts`;
  - `components/PointPicker.tsx` (the wrapper, `lazy` and `Suspense` with a `Skeleton`);
  - `components/LeafletPointPicker.tsx` (the lazy module: `MapContainer`, `TileLayer`, `ZoomControl`, `AttributionControl`, `Marker`, the click handler, the tile state);
  - `components/MapFailed.tsx`;
  - `hooks/useTileStatus.ts`;
  - `services/coordinates.ts` with its unit test;
  - `types/MapPoint.ts`;
  - `PointPicker.component.test.tsx`.
- `apps/web/src/shared/design-system/data.ts` and `leaflet.css`.
- `apps/web/scripts/libraryChunks.ts`.
- `apps/web/src/shared/copy/{english,arabic}/map.ts`.
- `features/lookups`:
  - `components/area/AreaSelect.tsx` with its test;
  - `hooks/area/useAreaOptions.ts` with its test;
  - `hooks/area/useCatalogueQuery.ts`.
- `features/spaces`:
  - `hooks/add/useCreateSpace.ts`;
  - `hooks/add/useAddSpaceForm.ts` with its test;
  - `services/profileInput.ts` with its unit test;
  - `components/profile/BasicsFields.tsx`, `components/profile/LocationFields.tsx`;
  - `components/add/AddSpaceForm.tsx` with its test;
  - `types/AddSpaceSlots.ts`.
- `pages/dashboard/admin/AddSpacePage.tsx`.
- `docs/architecture/findings/46-…md`.

**Changed**
- `apps/web/package.json`, `package-lock.json`.
- `vite.config.ts`, `scripts/checkBuild.ts` with its unit test, `eslint.config.js` with a rule test beside `dashboardOnlyRule.unit.test.ts`.
- `shared/design-system/index.ts` (the DataTable lines out).
- `features/space-links/components/admin-list/*` (the import moves).
- `pages/showcase/sections/data/*` (the import moves).
- `shared/forms/hooks/useServerForm.ts`, `services/schemaResolver.ts`, `hooks/useRefusalView.ts`, `hooks/useFormFailure.ts`, and their tests.
- `features/lookups/{index.ts, repository/lookupsRepository.ts (+unit), hooks/queryKeys.ts}`.
- `features/spaces/{index.ts, repository/spacesRepository.ts (+unit)}`.
- The copy: `{english,arabic}/{spaces,lookups,dashboard,index}.ts`.
- `pages/dashboard/{routes.tsx, navigation.ts (the add page's path only: never a sidebar item; checked in the routes test), admin/SpacesPage.tsx (the row above the list)}`.
- Documents:
  - `spaces.md`, `lookups.md`;
  - architecture §1, §3 › *Forms*, §3 (check:build), §6, and the status header;
  - foundation §3;
  - `setup.md` (check:build);
  - `CLAUDE.md` (the check:build line);
  - finding 45, the new finding 46, and the index;
  - `overview.md`.

## 9. Tests: the lane, the test, and the break it catches

**Unit**

| Test | The break it catches |
|---|---|
| `coordinates.unit` reads "31.52, 34.45", "31.52,34.45", "31.52 34.45", "-1.5, 2" and Arabic «٣١٫٥٢، ٣٤٫٤٥». It refuses "", "31.52", "a, b", "91, 10", "1, 2, 3". `formatCoordinates` gives five decimals in Western digits. | a split on ", " only; no range check; `toFixed` dropped |
| `profileInput.unit`: a blank or space-only optional text is absent, and a required one is kept as written. Readable coordinates become `{lat, lng}`. Blank coordinates are absent. Unreadable ones stay text. | the blank mapping dropped, or applied to required fields; the coordinates not parsed |
| `schemaResolver.unit`: with `prepare`, the codes come from the prepared input, so an empty location is `required`, not `invalid_format`. | the resolver reads the raw values |
| `checkBuild.unit`: <br>• a first-download chunk named `leaflet` or `data-table` is reported, and a lazily imported one is not; <br>• a missing group is reported; <br>• the first-download CSS list holds the entry's CSS and every static import's CSS, and not a lazy chunk's. | the group not followed; the existence check dropped; the CSS taken from lazy chunks |
| `spacesRepository.unit` `create`: `POST /admin/spaces` with the body, the unwrapped `AdminSpace`, and a failure as an `AppError`. | the path or the body |
| `lookupsRepository.unit` `catalogue`: `GET /lookups`. | the admin's list read instead |
| The lint rule's test: <br>• a feature importing `leaflet` is refused, and `shared/map` may; <br>• a feature may import `@shared/design-system/data`; <br>• only `shared/map` may import `@shared/design-system/leaflet.css`. | the restriction or the allowance dropped |

**Component** (fake adapter; no `vi.mock`)

| Test | The break it catches |
|---|---|
| `PointPicker.component`: <br>• the map mounts after its lazy load and is named by `label`; <br>• the attribution "© OpenStreetMap contributors" links to the copyright page; <br>• the zoom buttons are named from the catalogue, at the top start in each language (`.leaflet-top.leaflet-left` in `en`, `-right` in `ar`); <br>• no pin while the value is null; <br>• a value gives a pin named with its coordinates, and a new value renames it. | the attribution control off; the default English titles; the controls not mirrored; a pin always drawn |
| `PointPicker.component`, the tiles: a tile's `error` event shows the failure line. This holds only if jsdom creates a tile; otherwise it is proven by hand and said so. | the `tileerror` handler dropped |
| `useServerForm.component`: `prepare`'s output is what `submit` receives, and `failureLines` words a refusal that lands on no field. | the option ignored |
| `AreaSelect.component` and `useAreaOptions.component`: <br>• one group per governorate, named after it, with its areas in the interface's language; <br>• a disabled option while loading and after a failure; <br>• choosing an area hands back its id; <br>• the data is read from `GET /lookups`; <br>• axe. | the admin's list (hidden rows) read instead; the groups lost |
| `useAddSpaceForm.component`: <br>• the body: blank optionals absent, the location parsed, the area as a number; <br>• coordinates outside the box or unreadable send nothing and get their field's own line; <br>• a 201: the POST, then the admin scope's GET, then `onCreated`, with the toast "{name} added"; <br>• a 422 (`location` out of range, `areaId` invalid choice, `nameEn` invalid format) lands on those fields, and the first takes the focus; <br>• a 409 shows the form's own line; <br>• a 429 blocks the submit. | `onCreated` before the refresh; the toast missing; the server's errors lost |
| `AddSpaceForm.component`: <br>• every label, and "Optional" on each optional field; <br>• the area slot renders inside its Field and is named by it; <br>• typing "31.52, 34.45" in Coordinates moves the pin (its name); <br>• the submit is enabled; <br>• axe. | the field not wired to the picker; the marks missing |

**By hand** (stated in the report): the click and the drag; the tiles blocked; the lazy chunk failing offline; the controls in RTL and LTR; light and dark; phone and desktop.

## 10. Review Focus (the inputs no planned test exercises)

- A real click or drag on the map: jsdom has no layout. It is proven by hand.
- Leaflet in jsdom at zero size with `bounds` fitting: if fitting throws, the test gives the picker a size through the platform. No mock.
- The tile failure, if jsdom creates no tile element.
- The lazy chunk's failure, which happens only in a real browser offline.
- A 409 slug race, which happens only through the fake transport; the API lane owns the race.
- An area hidden while the catalogue is cached (up to 30 s; S9).
- Leaflet's own keyboard panning and zoom.
- The `Add space` link's place in the top bar on a phone, and its wrap.
- The visual themes of `leaflet.css`, in dark especially.

## 11. Commits (lint and typecheck on each)

1. `fix(design-system): keep the data table off the site`
   - the `data.ts` entry and the moved imports;
   - the boundaries allowance;
   - the `data-table` group;
   - the `check:build` library check (S3) with its tests;
   - docs: finding 45 resolved, foundation §3, architecture §1 and §3, `setup.md`, `CLAUDE.md`.
2. `feat(map): add a point picker on OpenStreetMap`
   - the dependencies and the lock file;
   - `shared/map`, `leaflet.css` and the map copy;
   - the lint restriction (S1) and the CSS allowance;
   - the `leaflet` group and the CSS check (S2);
   - tests;
   - architecture §6, foundation §3, finding 46.
3. `feat(forms): let a form prepare its values` (`prepare`, `failureLines`; tests; architecture §3 › *Forms*).
4. `feat(lookups): add the area field` (`AreaSelect`, the catalogue query and repository, copy, tests, `lookups.md`).
5. `feat(spaces): add a space with its map pin`
   - the create call and the hooks;
   - the sections, the form and the page;
   - the route and the list's button;
   - copy and tests;
   - `spaces.md` and `overview.md`.

The PR title is commit 5's (42 characters).

## 12. Verification (phase 4)

- **Before any change:** `NODE_ENV=production npm run build` on `main`. I record the manifest's first download: its files, bytes, and whether TanStack Table, react-day-picker or cmdk is in it. I also record finding 27's cycle.
- **On the head, once each, one at a time:** `test:unit`, `test:component`, `test:api` (with Docker and `masaha-postgres-1` up). Then `NODE_ENV=production npm run build`, `check:build`, `lint`, `typecheck`, `check:classes`, `format:check`.
- **The breaks, each made once, seen failing, and reverted (not committed):**
  - a static `DataTable` import in a site page makes `check:build` fail;
  - a static import of `shared/map`'s Leaflet module in the site makes it fail;
  - a static `import '@shared/design-system/leaflet.css'` in `app/` makes it fail (S2);
  - a broken group test, with the chunk missing, makes it fail (S3);
  - each new test seen red first.
- **The manifest after:** the first download without the `data-table` and `leaflet` chunks and without Leaflet's CSS, with its bytes compared to before.
- **A real run** (API 3320, web 5320):
  - add a space by clicking the map, and another by pasting coordinates;
  - one refused outside the Strip;
  - tiles blocked (DevTools request blocking of `tile.openstreetmap.org`), and the form still sent;
  - the toast and the list.
  - The servers are stopped and the ports checked free.
- **Screenshots** to `C:\Users\basel\Downloads\s2b3b-shots`, in RTL and LTR, light and dark, phone and desktop:
  - the empty form;
  - the field errors;
  - the map with its pin;
  - the coordinates field;
  - the tiles failed;
  - the toast on the list.
- `git merge-tree --write-tree` against B's open PR at the report.
- **Not run:** E2E, which does not exist yet.

## 13. Decisions needed from the owner: answered (`S2B3B_PLAN_REPLY.md`)

The plan is approved with three changes:
1. Design issue 7 takes the fallback: a row above the list, at the end, at every width.
2. Finding 27's file is left untouched while it stays open; the study goes in the PR and the report.
3. `navigation.ts` gains the add page's path only, and it is not a sidebar item; the routes test checks this.

Also decided:
- Design issues 1–6 and 8, S1–S11 (S8 included), and the stated exceptions are approved. Each exception is written where its rule lives.
- "OpenStreetMap" stays untranslated, linked to its copyright page in both languages.
- The Arabic lines are approved; any further Arabic line is listed in the PR.

The original questions:

1. Design issues 1–7: approve or decline each. Issue 7 is where "Add space" goes.
2. Stronger decisions S1–S11.
3. S8: the two new `shared/forms` options. This is a change to a shared mechanism.
4. The Arabic copy. The main new lines, in the PR for approval:
   - «إضافة مساحة»;
   - «أُضيفت {name}»;
   - «اختياري»;
   - «الإحداثيات»;
   - «لم تُحمَّل الخريطة. أدخل الإحداثيات بدلًا منها.»;
   - «© مساهمو OpenStreetMap»;
   - «هذه النقطة خارج قطاع غزة»;
   - «أُضيفت مساحة بالاسم نفسه في اللحظة ذاتها. أضِفها مرة أخرى.»;
   - «الدبوس عند {point}».
5. D13: confirm "studied, left open" as the expected outcome for finding 27.
