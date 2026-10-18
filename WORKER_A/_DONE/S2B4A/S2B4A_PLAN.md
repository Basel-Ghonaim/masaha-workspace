# S2b-4a — The admin's space editor, first half (web) — Plan

**Worker A** · main folder · branch `feat/admin-space-editor` from `origin/main` (`e30a86c`) · PR
`feat(spaces): the admin's space editor` · labels `feat`, `area:web`, `area:docs` · `Closes #70`.

## 1. Summary

The admin opens a space on the dashboard and edits it, section by section, from the living design
(#61, #66). This item builds the editor's frame (a page per space, titled by the space's own name,
with its section navigation), three of its sections — «المساحة» (the profile), «المرافق» (the platform's
amenities and the space's own) and «التواصل» (the contacts) — each saved, dated and confirmed alone,
the «ما زال ناقصًا» checklist, the warning on leaving with unsaved changes, the read-only page of a
verified space, and the two ways in from the spaces list. After a creation the add page now lands on
the new space's editor (supersedes #57's D2). It fixes Issue #70 and builds the record-name title of
`frontend/architecture.md` §2 for its first page. The hours with the shifts, and the prices, are S2b-4b.

## 2. The contract

**Scope**
- Route `/dashboard/admin/spaces/:spaceId` (ADMIN), titled «تعديل مساحة» while it loads, then the
  space's name (its language marked) in the top bar and the tab, through one record-title context.
- Frame: breadcrumb back to the list; the state badges (verification always, «مخفية» when hidden);
  the unverified warning Alert; the sections; the privacy note at the end.
- Section navigation: a sticky side list from `lg`; below it a sticky row of chips under the top bar,
  scrolling sideways; the section in view marked (`aria-current="location"`) at every width.
- «المساحة»: `BasicsFields` and `LocationFields` (#57) as two blocks under a `Separator`
  (`#basics`, `#location` kept), one date, one footer, one confirm; saved with `PATCH`.
- «المرافق»: the platform's amenities to tick (a field `lookups` hands in), «إدارة قائمة المرافق»
  under it (a link the page hands in), then «مرافق إضافية» (add up to 20, remove, Arabic required,
  English optional); one save (`PUT …/amenities`), one date, one confirm.
- «التواصل»: rows of the seven types; each value's helper shows its stored form as typed (from
  `normaliseContact`, `@masaha/shared/spaces`) or an example; «هاتف» shows its carrier beside it;
  refused on its field when it cannot be stored or repeats; up to 20; `PUT …/contacts`.
- Every group: «لم تُضف بعد» and Save only while missing; otherwise its date, «قديمة» when stale, and
  «المعلومات ما زالت صحيحة» (`POST …/{group}/confirm`) while clean; Save always enabled;
  «تغييرات غير محفوظة» and «تجاهل التغييرات» while dirty; its own failure (422 on fields, 403, 404,
  409, 429 counting down) leaving the other sections as they are.
- «ما زال ناقصًا»: heads a space with any missing group, the five groups each «تمّت» (`success`) or
  «لم تُضف بعد» (`warning`), a built section's line linking it; gone once nothing is missing.
- Leaving with a dirty section (a link, Back, the sidebar) asks first in an `AlertDialog` naming the
  sections; closing or reloading the tab asks through the browser (`beforeunload`).
- Verified space: read-only text rows under the same section names, its `info` Alert (see Q1) with
  «عرض في الموقع»; no section list below `lg`.
- After a creation: the new space's editor (the toast stays).
- Entry points: «تعديل» first in each row's menu, and the space's name a link, in the spaces list.
- Issue #70: `PageHeader` never renders an empty heading.

**Acceptance criteria**
- [ ] Opening a space shows «تعديل مساحة» until it loads, then its name in the top bar and the tab;
      an English-only name in Arabic is marked `lang="en" dir="ltr"` in the top bar.
- [ ] Each of the three sections saves alone; a failure in one changes no other; the date, the
      «قديمة» badge, the missing state and the checklist follow the server's answer.
- [ ] A cleared optional profile field is sent as `null`; only the changed profile fields are sent.
- [ ] A contact that cannot be stored, or repeats, is refused on its own field before any request.
- [ ] A dirty section blocks a navigation to another path with a dialog naming it; a hash change
      within the page is never blocked; Save or Discard clears it.
- [ ] A verified space opens read-only; a 403 on a save (verified meanwhile) turns the page read-only.
- [ ] Creating a space lands on its editor; «تعديل» and the name in the list lead to it.
- [ ] `PageHeader` renders no empty `h1` (#70).
- [ ] RTL/LTR, light/dark, 390/768/1440 checked; both catalogues; every lane and check green.

**Out of scope**
- The hours, the shifts and the prices (S2b-4b): their sections are absent, not "coming soon"; the
  checklist still lists them, without a link.
- Photos and the open-report notice (D3); «بلاغات <المساحة>» (data reports not built).
- Unlinking an owner (the owners item, A4's one dialog) — see Q1.
- The owner's Space profile (step 5), which will reuse the sections (D5/O1).
- No change in `apps/api` or `packages/shared`.

## 3. The reading done

CLAUDE.md; `workflow.md`; `docs/README.md`; the findings index's open titles (opened 27, 44, 46, 55);
`features/spaces.md` (all); `features/lookups.md`; `features/space-links.md` (its list's slots);
`api-contract.md` §1–4 and *Spaces (the admin)*, *Owners*, *Users*; `frontend/architecture.md` (all);
`foundation.md` §5, §9, §10, §12; `localisation.md`; `testing.md`; `design/CHANGES.md` › 2a and 2b;
`DECISIONS_ADMIN.md` (A1, A2, contacts, AD-012 and the amendments); the prototype
(`Admin space edit.html`, `profile-a.jsx`, `profile-b.jsx`, `admin.jsx`'s `SpaceStatus`/`PrivacyNote`);
frames 01–04, 06 (`01_EDIT_UNVERIFIED_3LG` viewed; the rest read through the prototype's source,
which draws them); Issue #70. Code: `features/spaces` (all), `features/lookups` (index, keys,
queries, `AreaSelect`), `features/space-links` (`AdminSpacesList`, `SpaceSwitcher`'s `spaceLink`),
`pages/dashboard` (routes, navigation, the three admin pages, the shell), `shared/forms`,
`shared/routing/title`, `app/RootLayout.tsx`, `@masaha/shared/spaces` (requests, responses,
contacts), `core/phone.ts`, `scripts/checkClasses.ts`.

## 4. The settled decisions, as built

- **D1 — two items.** Sections «المساحة», «المرافق», «التواصل» only; nav lists those three; the
  checklist lists five, hours and prices as text without a link.
- **D2 — leaving warns.** `useLeaveGuard` in the editor: React Router's `useBlocker` (the app's router
  is `createBrowserRouter`), blocking only when some section is dirty **and the path changes** (a
  chip's `#hours` hash never asks); a `beforeunload` listener while dirty. The dialog names the dirty
  sections («تغييرات غير محفوظة في: المساحة، التواصل»), «البقاء» (focused) and «المغادرة»
  (`destructive`). Sections report dirty to the editor's state (cleared on unmount).
- **D3 — no photos, no report notice.** Absent; nothing promised.
- **D4 — the title is the space's name.** `shared/routing`: a `RecordTitleProvider` in `RootLayout`,
  `useRecordTitle(title)` which a page sets and clears (effect cleanup), and `usePageTitle()`
  preferring it to the route's. `usePageTitle` returns `{ text, lang?, dir? }` so `PageHeader` marks
  the name's language; `DocumentTitle` reads `text`. The page gets the name from `spaces`'
  exported `useSpaceName(spaceId)`. **#70 in its own commit:** `PageHeader` falls back to the
  wordmark, as `DocumentTitle` does, so the heading and the tab agree and there is one `h1`.
- **D5 — the sections are the capability's, made for the owner.** `SpaceEditor` (exported) takes
  slots the page sets: `areaField` (lookups' `AreaSelect`), `amenitiesField` (lookups' new
  `AmenityChecklist`), `areaName` (lookups' new `AreaName`, read-only), `manageAmenities` (a link
  node, the admin's only), `publicLink` (`publicSpacePath(slug)`). Nothing inside is the admin's.
- **D6 — the add page's landing.** `AddSpaceForm`'s `onCreated(spaceId)`; `useCreateSpace` also seeds
  the space's query with the answer, so the editor opens at once, under the checklist. `spaces.md`:
  #57's D2 superseded, dated, with its reason.

## 5. Stronger decisions and proposed alternatives

1. **The profile's save sends only the changed fields** (the parsed profile compared with the
   space's, a pure `profileChanges`), cleared optionals as `null`. *Why:* the whole profile resent
   would carry an unchanged area hidden since, which `PATCH` refuses (`invalid_choice`), so the
   section could not be saved at all; it also never overwrites a field another admin changed. *Cost:*
   one service and its test. **Recommend.**
2. **Save on a clean, non-missing section sends nothing** and says, in the section, «لم يتغيّر شيء.
   لتجديد تاريخه: «المعلومات ما زالت صحيحة»» (design issue 2). *Why:* the server writes nothing and
   keeps the date (D3), so «حُفظ» would be untrue. Save stays enabled (foundation §10). **Recommend.**
3. **A save's answer is the space's state:** set in its query, the admin scope only marked stale
   (`refetchType: 'none'`), no waiting — unlike #50's actions, which wait for the list they change.
   *Why:* the editor shows the answer itself; the list refetches when shown. A clean section follows
   new server data; a dirty one keeps its edits. **Recommend.**
4. **A 403 on a save or confirm** refetches the space, so the page turns read-only with its notice,
   and the section's failure says «صارت المساحة موثّقة: يعدّلها مالكها الآن». A 404 says it was
   deleted. **Recommend.**
5. **The amenities field reads the admin's amenities list** (`['admin','lookups','amenities']`):
   active ones to tick, plus any retired one the space still has, ticked, with «غير نشط» (design
   issue 3). *Why:* the catalogue has no names for a retired one, which would stay linked unseen.
   *Cost:* the owner's page (step 5) will hand a catalogue-based field; the slot already allows it.
   **Recommend.**
6. **The carrier is a web display rule** in `features/spaces/services/carrierOf.ts` (+97059 جوال,
   +97056 أوريدو), read from the stored form. *Why:* the API never computes it; the stored form stays
   the shared rule's. If the directory's page needs it, it moves to `shared/lib` then. **Recommend.**
7. **The chips stick under a one-line top bar:** `PageHeader`'s `h1` truncates, so the bar is always
   56 px and the row sticks at `top-14` (no measured offset, no arbitrary value). The full name stays
   in the breadcrumb and the tab. *Cost:* every dashboard title truncates instead of wrapping (none
   wraps today). **Recommend.**
8. **The leave guard lives in `spaces`** until a second form needs it (the owner's settings), then moves
   to `shared/forms`. **Recommend.**
9. **The section in view** by `IntersectionObserver` (a platform seam the component tests stub), a chosen
   chip marked at once. **Recommend.**

No rule of the documents is weakened. One rule is applied for the first time: architecture §2's
record-name title ("built with the first such page") — its *built* status is updated.

## 6. Related findings

- **27** (two dashboard chunks import each other) — not folded: the editor adds no load-time import
  across the chunks. Cost of folding: a build change outside the item.
- **44** (no screen restores a deleted space) — not folded: G3's «محذوفة» filter is another item.
- **46** (the deployment's headers must let the map's tiles load) — not folded: the editor's map is the
  add page's; the deployment's.
- **55 / 28** (lazy-shell waits under load) — not folded; I run the component lane alone (prompt §5).
- **New, 59:** the verified space's editor cannot name its owner — `AdminSpace` carries no owners
  (only if Q1 is answered (b)).
- **New, 60:** the area field shows no area for a space whose area has been hidden since: it reads the
  public catalogue. The profile still saves (stronger decision 1).

## 7. Files

**`shared/routing`, `app`, the shell** (D4, #70)
- `shared/routing/title/`: new `PageTitle.ts`, `RecordTitleProvider.tsx`, `useRecordTitle.ts`; changed
  `usePageTitle.ts`, `DocumentTitle.tsx`; tests `recordTitle.component.test.tsx` (new),
  `DocumentTitle.component.test.tsx` (updated); `shared/routing/index.ts`.
- `app/RootLayout.tsx`; `pages/dashboard/shell/PageHeader.tsx` (+ new `PageHeader.component.test.tsx`).

**`pages/dashboard`**
- `navigation.ts` (`adminSpacePath(id)`), `routes.tsx` (the route and its title).
- `admin/SpaceEditPage.tsx` (new): `PageHeader`, breadcrumb, `useRecordTitle(useSpaceName(id))`,
  `SpaceEditor` with its slots; a `:spaceId` that is no positive integer → `NotFoundState`.
- `admin/AddSpacePage.tsx` (landing), `admin/SpacesPage.tsx` (`editLink`, `spaceLink`).

**`features/spaces`** (one folder per operation)
- `repository/spacesRepository.ts` (+ `get`, `updateProfile`, `updateAmenities`, `updateContacts`,
  `confirm`) and its unit test.
- `hooks/queryKeys.ts` (+ `space(id)`: `['admin','spaces','space',id]`).
- `hooks/editor/`: `useSpaceQuery`, `useSpaceEditor` (states, badges, checklist, nav, read-only),
  `useSectionFrame` (date, stale, missing, dirty, confirm, discard), `useSectionInView`,
  `useLeaveGuard`, `useSpaceName` (exported).
- `hooks/profile/` `useProfileSection`, `useUpdateProfile`; `hooks/amenities/` `useAmenitiesSection`,
  `useUpdateAmenities`; `hooks/contacts/` `useContactsSection`, `useUpdateContacts`;
  `hooks/confirm/useConfirmGroup`.
- `components/editor/`: `SpaceEditor` (exported), `EditorState`, `SectionNav`, `MissingChecklist`,
  `SectionCard`, `SpaceStatusBadges`, `VerifiedNotice`, `LeaveDialog`, `PrivacyNote`.
- `components/profile/` `ProfileSection`, `ReadOnlyProfile`; `components/amenities/`
  `AmenitiesSection`, `OwnAmenityRow`, `ReadOnlyAmenities`; `components/contacts/`
  `ContactsSection`, `ContactRow`, `ReadOnlyContacts`.
- `components/menu/SpaceActionsMenu.tsx` + `hooks/menu/useSpaceActionsMenu.ts` («تعديل», `editLink`).
- `components/add/AddSpaceForm.tsx`, `hooks/add/useAddSpaceForm.ts`, `hooks/add/useCreateSpace.ts`.
- `services/`: `profileValues` (space → form), `profileEditInput` (blank → `null`), `profileChanges`,
  `carrierOf`, `updatedAgo` (relative date, Gaza's day, `Intl.RelativeTimeFormat`, Western digits).
- `types/`: `AmenitiesField`, `AreaNameField`, `SectionFrameView`, `SpaceEditorView`, etc.
- `index.ts` (`SpaceEditor`, `useSpaceName`, the slot types).

**`features/lookups`**: `components/amenities/AmenityChecklist.tsx`, `hooks/amenities/useAmenityChecklist.ts`;
`components/area/AreaName.tsx`, `hooks/area/useAreaName.ts` (the admin's governorates, hidden
included); `index.ts`; tests.

**`features/space-links`**: `AdminSpacesList.tsx`, `AdminSpaceCard.tsx`, `SpaceNameText.tsx` (the name a
`Link` by the page's `spaceLink`); `AdminSpacesList.component.test.tsx` (updated).

**Copy** (en and ar): `spaces.ts` (editor, sections, checklist, guard, toasts, contacts' types and
examples, carriers), `dashboard.ts` (the route's title, the breadcrumb), `lookups.ts` (checklist).

**Documents:** `features/spaces.md` (*Web* part: what it does, flows, *Web decisions* incl. D6
superseding D2, code map, *Web history*), `features/lookups.md` (the two new fields),
`features/space-links.md` (the name link slot), `frontend/architecture.md` §2 (the editor page built;
the record title built), `project/overview.md` (*Built*, spaces line), findings 59–60 + index.

**Other layer:** none (see Q1 for the one API field it would need). **Shared with open items:** no open
PR now; worker B's item touches `apps/api`, `packages/shared`, the contract — none of these files.
Shared documents (`spaces.md`, overview *Built*, findings index) by the fast path.

~65 files → a separate review conversation (workflow phase 7).

## 8. Design issues (built only once approved)

1. **The save toast names no section** («حُفظ القسم»): with three sections it says nothing of which.
   → «حُفظت «التواصل»» / "Contacts saved"; the confirm toast likewise.
2. **Save on an unchanged section** toasts «حُفظ» though nothing is written and the date stays (D3).
   → no request; a line in the section points to «المعلومات ما زالت صحيحة» (stronger decision 2).
3. **A retired amenity the space still has is invisible** in the design's checklist, yet stays linked.
   → shown ticked with a `neutral` «غير نشط» badge; once unticked and saved it is gone.
4. **The chips' row measures the top bar** in the prototype (`style.top`), which the layer forbids
   outside it. → the bar is one line (the title truncates) and the row sticks at `top-14`.
5. **The checklist's hours and prices lines link nowhere** in this item. → plain text, same badge.

## 9. Tests (each seen failing first; the break each catches)

**Unit**
- `spacesRepository`: each new call's method, path, body; the confirm's path per group. *Break:* a
  wrong path or verb.
- `profileChanges`: only changed fields; the pin by `lat`/`lng`; nothing for an unchanged profile.
  *Break:* sending the whole profile.
- `profileEditInput`: blank optional → `null`, required kept as typed. *Break:* omitting a cleared field.
- `profileValues`: `null` → `''`, pin → coordinates' text.
- `carrierOf`: 059 → Jawwal, 056 → Ooredoo, +972 and landlines → none.
- `updatedAgo`: today, yesterday, 2, 11 days, on Gaza's day across midnight UTC.

**Component**
- `recordTitle`: route title while unset; the record's once set, in top bar and tab; cleared on unmount.
- `PageHeader`: never an empty `h1` (#70); the record name's `lang`/`dir`.
- `useProfileSection`: sends changed fields with `null`s; a 422 lands on its field and focuses it;
  a 403 refetches the space; a clean save sends nothing.
- `useAmenitiesSection`: own amenities add/remove, the 20 limit with its reason; a blank Arabic name
  refused on its row; a repeat `not_unique` on the later row; one body with both lists.
- `useContactsSection`: the helper's stored form as typed; an unstorable value refused on its row with
  no request; a repeat once stored refused; «هاتف»'s carrier.
- `useConfirmGroup`: the group's date renewed from the answer; hidden while missing or dirty.
- `useLeaveGuard`: blocks another path while dirty, lets a hash change through, adds and removes
  `beforeunload`. *Break:* blocking every navigation.
- `SpaceEditor`: loading, failure with retry, 404; the checklist shown with a missing group and gone
  once saved; read-only for a verified space (no inputs, no Save); nav marks the section in view
  (stubbed observer); a failure in one section leaves another's edits.
- `SectionCard`: missing → Save only, «لم تُضف بعد»; stale badge; dirty badge and Discard.
- `AmenityChecklist`: active ones and a linked retired one, marked; read-only names.
- `SpaceActionsMenu`: «تعديل» leads to the page's link, never waits during a 429.
- `AdminSpacesList`: the name is a link to `spaceLink(row)`.
- `AddSpaceForm`/`useAddSpaceForm`: `onCreated` with the new id; the space's query seeded.
- `pageTitles.unit.test.ts` covers the new route without change.

## 10. Review Focus (no planned test exercises)

- A real browser's hash navigation through React Router (popstate) and `ScrollRestoration` with the
  sticky bar: anchors landing under the bar (`scroll-mt-*`).
- `beforeunload`'s browser prompt (jsdom only proves the listener).
- Retired-amenity `invalid_choice` on `amenityIds.<i>` (an amenity retired while the page was open):
  shown as the section's failure, not on a box.
- The area hidden since (finding 60) in a real run.
- Long Arabic and English names truncating in the top bar at 390.

## 11. Commits

1. `fix(web): no empty heading on an untitled page` — #70.
2. `feat(web): a page titled by its record's name` — the context, `usePageTitle`'s view, the truncating
   top bar, architecture §2.
3. `feat(lookups): amenities checklist and area name` — the two slots, `lookups.md`.
4. `feat(spaces): the admin's space editor` — route, page, frame, nav, checklist, «المساحة», read-only,
   leave guard, `spaces.md`, overview, findings.
5. `feat(spaces): a space's amenities and contacts` — the two sections.
6. `feat(spaces): open the editor from list and add` — menu, name link, D6, `space-links.md`.

## 12. Verification (phase 4)

- One at a time on the head, after checking worker B runs no lane: `test:unit`, `test:component`;
  `NODE_ENV=production npm run build`, `check:build`; `lint`, `typecheck`, `check:classes`,
  `format:check`, `check:links`. **Not run:** `test:api` (no API change).
- Real run (API 3320, web 5320): create a space → its editor under the checklist; save and confirm
  each section; add own amenities; a contact refused on its field; leave with a dirty section (link,
  Back, reload); a verified space read-only. Screenshots 390/768/1440, RTL/LTR, light/dark in
  `Downloads\s2b4a-shots\`. Servers stopped by PID, ports checked free.

## 13. Decisions needed from the owner

> **Answered 2026-10-13** (`S2B4A_PLAN_REPLY.md`): **approved.** Q1 → **(b)**: the Alert reads
> «يعدّلها مالكها», finding 59 recorded; nothing in `apps/api` or `packages/shared`. Q2 → design issues
> 1–5 approved. Q3 → stronger decisions 1–9 approved. Q4 → the new Arabic lines listed in the PR
> description. **Corrections:** commits 3 and 6 are renamed `feat(lookups): amenities checklist and
> area name` (48) and `feat(spaces): open the editor from list and add` (47); every subject counted
> (≤ 50) before its commit. Finding 60 recorded as planned, and the report says what the admin sees in
> a real run.

- **Q1 — the verified page's owner.** `AdminSpace` has no owners, and no endpoint gives a space's
  owners by id; the web has no unlink anywhere yet.
  (a) Worker B adds `owners: { id, name }[]` to `AdminSpace` (as `AdminSpaceRow`'s; contract + shared
  type + test, no schema), merged before this PR; the Alert then reads «يعدّلها {name}».
  (b) This item's Alert reads «يعدّلها مالكها» without a name; finding 59 records it.
  **Either way, «فك ربط {name}» arrives with the owners item (A4's one dialog)**, since an entry point
  must lead somewhere. **Recommend (a)** if B can fit it now; else (b).
- **Q2** — approve design issues 1–5.
- **Q3** — approve stronger decisions 1–9.
- **Q4** — the new Arabic lines are the design's words; the few new ones (stronger decisions 2 and 4,
  the leave dialog) are listed in the PR for the owner's approval.
