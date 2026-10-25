# OWNER_SETUP — PR 1 report (`feat/owner-space-profile`, the owner's space profile)

Executor: Claude Code (Opus 5.5), 2026-10-20. Written as the work goes.

## 1. First checks (plan §13, PR 1)

1. `git status` clean on `main`; `git fetch origin`; `git pull --ff-only` → `main` at `7d48c9c3`.
2. USERS merged: `gh pr list --state merged --head feat/admin-users` → `93 7d48c9c3…` (and an old `62` row: see 4).
   `gh pr view 93 --json state` → `MERGED`.
3. Base diff `git diff --name-status 4daedc94 origin/main` → 144 lines. `4daedc94` sat on `a8c39bda`, so the
   diff also carries #92's and #94's merges (eff0a3d1, eabdb919), which the plan already read or which touch
   none of PR 1's code. PR 1's code files (`features/spaces`, `features/lookups`, `pages/dashboard/routes.tsx`,
   its test, `navigation.ts`, `SpaceEditPage`, `AddSpacePage`, the `spaces`/`lookups`/`dashboard` copy):
   `git diff --stat 4daedc94 origin/main -- <those>` → only `shared/copy/*/errors.ts` (+1 line each, not
   PR 1's) and `navigation.ts` (one comment reworded). USERS' fix round (the one-time dialog's `returnFocus`,
   the users page holding the dialogs, the users list's core) touches `features/users`, `space-links` and
   `admin/UsersPage` — PR 3's files, not PR 1's. **No difference the plan does not cover; no stop.**
   USERS' `4_REPORT_PR1.md` read (its fix round FR1, its departures): nothing reaches PR 1's files.
   `packages/shared` changed (#94: `core/gazaTime`, `directory`, `occupancy`): `npm run build -w @masaha/shared`
   before the web checks. `packages`, `space-settings`, `space-links` staff types: unchanged since `eff0a3d1`
   (`git diff --name-status eff0a3d1 origin/main -- packages/shared/src/{packages,space-settings,space-links}` →
   empty). `occupancy/requests.ts` changed (#94's override) — PR 3's concern, to re-read there.
4. Open PRs: only **#62** (`feat/admin-users` head `18e0edcf`, last updated 2026-10-12: an old PR on the name
   #93 reused). Its files: `apps/api`, `packages/shared`, docs, `shared/copy/*/errors.ts` — **no code file of
   this plan**. DESK is not open (no head to note).
5. - `toFieldErrors` (`packages/shared/src/core/fieldErrors.ts:39`): a wrong type gives `required` only when the
     value is `undefined`, so a count sent as `''` gives **`invalid_format`**. PR 2's concern (packages): the
     limit's `fieldLines` must word `invalid_format` with `limitEmpty` too, as the fallback says.
   - `useServerForm` passes `failureTitle` to `useFormFailure` in its body (`useServerForm.ts:106-107`), every
     render. PR 3's concern; holds.
   - `TemporaryPasswordDialog` keeps `kind` (required) and now takes an optional `returnFocus` (USERS' fix
     round); `RefusalText` is in `shared/forms` (`components/RefusalText.tsx`). As USERS left them.
6. `Sheet side="end"`: `w-3/4 max-w-sm` at every width — **not** full width below 768 px. PR 2's (the package
   sheet): build with it as it is and record the finding there (`<n+1>` per the approval note).
7. `#hours` from another page: PR 1 links to `#hours` nowhere (its prices row goes to Packages & prices);
   PR 2's concern.
8. The next free finding: **98** (`docs/architecture/findings` ends at 97) → `<n>` = 98; **the supervisor then reserved 98 for worker B’s DESK PR 2: this PR’s findings start at 99** (see commit 4).
9. Branch: `git switch --no-track -c feat/owner-space-profile origin/main`; `npm run build -w @masaha/shared` → exit 0.

## 2. Commits

### Commit 1 — `1845c50f` `refactor(spaces): share the shekel helpers` (42)
- Moved: `priceText` (+ test, `git mv`), `agorotOf`/`shekelsOf` → `shared/lib/money/shekels.ts`, their cases →
  `shekels.unit.test.ts` (unchanged); `shared/lib/index.ts`; importers `pricesForm.ts`, `useReadOnlyPrices.ts`
  (`git grep` found no other). Architecture's status line names `shared/lib`'s money helpers.
- Test 1 (moved, refactor): `npx vitest run --project unit src/shared/lib` → `Tests  5 passed (5)`.
- Break: the plan's `Math.round` → `Math.floor` **stayed green** (`Tests  5 passed (5)`): every moved case's
  `shekels * 100` is exact in floating point (12.5, 0.05 → 5.000000000000001, 12.75 …), so floor and round agree
  and, the tests moving unchanged, the break cannot change the outcome. **Departure:** the break that can —
  `decimals <= 2` → `decimals <= 3` → `Tests  1 failed | 4 passed (5)`,
  `AssertionError: expected 100 to be '1,000'`; restored.
- `npx vitest run --project unit src/shared/lib src/features/spaces/services` → `Test Files  11 passed (11)` /
  `Tests  57 passed (57)`. `npm run lint` → exit 0; `npm run typecheck` (`tsc -b`) → exit 0.

### Commit 2 — `refactor(spaces): give the editor its place` (43) — in progress
- Built as §9: `types/EditorPlace.ts` (`EditorPlace`, `AdminPlace`, `OwnerPlace`), `spaceEditorRepository.ts` (the
  editor's calls by place; `SpacesRepository` keeps create, hidden, delete, restore), `editor/editorScope.ts`
  (`EDITOR_SCOPES`), `editor/meanwhileLines.ts`, `services/mayEdit.ts`; every editor hook and section takes `place`;
  `SpaceEditor({ spaceId, place, areaField, amenitiesField, publicLink })`; `SpaceEditPage` passes the admin's place.
- **Departures (shape, within the plan's lines):** `meanwhileLines(place, copy, of = 'section' | 'photos')` — the
  admin's gallery has its own "verified meanwhile" line («…edits its photos now»), so the helper takes which;
  `AmenitiesSection`'s `listLink: string | null` arrives here (§7 lists it under commit 5) because `SpaceEditor`
  must type the owner's place from this commit; the read-only view is the admin's place only (its names are the
  admin's), and an owner `mayEdit` refuses — unreachable, since an owner's link is what verifies a space — shows
  the 403 (`ForbiddenState`); the checklist follows `readOnly` (`!mayEdit`), not `isVerified`, so the owner's
  verified space shows it (the plan's acceptance: "the missing checklist").
- Tests 2, 3, 4 (new; their code written in the same step, so each red is its break):
  - Test 2 break (the owner's base `/admin/spaces`) → `Failed Tests 13`, `AssertionError: expected [ 'get /admin/spaces/7', …(10) ] to deeply equal [ 'get /manage/spaces/7', …(10) ]`; restored.
  - Test 3 breaks: the owner's `spaceKey` `['admin', …]` → `Failed Tests 1`, `AssertionError: expected [ 'admin', 'spaces', 'space', 7 ] to deeply equal [ 'space', 7, 'spaces', 'space' ]`; the owner's `answered` `['admin']` → `Failed Tests 1`, `AssertionError: expected [ 'admin' ] to deeply equal [ 'me' ]`; restored.
  - Test 4 break (`mayEdit` → `!isVerified`) → `Failed Tests 1`, `AssertionError: expected false to be true`; restored.
- Test 5 (existing hook tests, `'admin'` passed, titles unchanged): `npx vitest run --project unit src/features/spaces`
  → `Test Files  13 passed (13)` / `Tests  86 passed (86)`; `npx vitest run --project component src/features/spaces
  src/pages/dashboard` → `Tests  1 failed | 263 passed (264)`: the one failure is routes › «lists the owner’s eleven
  pages» (a cold-load wait under the parallel run, finding 87, as USERS saw; no file of it changed) — the file alone
  → `Test Files  1 passed (1)` / `Tests  39 passed (39)`.
- Lint (after removing an unused `vi` import the move left) → exit 0; `tsc -b` → exit 0.
- **Committed `e1297b84`** `refactor(spaces): give the editor its place` (43), 56 files.

### Commit 3 — `2e74a8d3` `fix(spaces): start the prices table at 1024 px` (46)
- `PricesSection`: every `md:` (24) → `lg:`. `spaces.md` *Behaviour* (from 1024 px) and a *Web decisions* line;
  finding 67 → Resolved, moved in the index.
- **Departure (docs):** the plan's *Why* cites foundation §9 "more than five columns → cards below `lg`"; §9 no
  longer says so (USERS' A7 moved that wording off the layer), so the line says what §9 does say — full tables are
  the desktop's, from 1024 px — and finding 67's cut select. No "owner's page" claim: PR 1 builds no owner's
  prices table (the owner's prices page is PR 2).
- No planned test (classes only). `npm run lint` → exit 0; `npm run typecheck` → exit 0; `npm run check:classes` →
  `No physical direction or arbitrary-value classes in 943 files.`; prices hook and editor tests →
  `Test Files  2 passed (2)` / `Tests  42 passed (42)`.

### Commit 4 — `f734a297` `feat(lookups): offer the public lists to owners` (47)
- `types/LookupsSource.ts`; `useAreaOptions`/`AreaSelect` and `useAmenityChecklist`/`AmenityChecklist` take `source`;
  `useAmenitiesQuery` and `useCatalogueQuery` take `enabled` (each list read only for its source); the checklist's
  `retiredKept` line; `AddSpacePage`, `SpaceEditPage` pass `source="admin"`; copy `areaSelect.unavailable`,
  `amenityChecklist.retiredKept` (both catalogues); `lookups.md` (*Who uses it*, *Behaviour*, *Web decisions*,
  *Open findings*, *Web history*); finding 99 (Open) and its index line.
- Tests 6 and 7 (added to the existing hook tests; the existing tests pass `'admin'`, titles unchanged). Run with the
  code → green; `npx vitest run --project component src/features/lookups src/features/spaces` →
  `Test Files  44 passed (44)` / `Tests  343 passed (343)`.
  - Test 6 break (`useGovernoratesQuery` enabled for `public`) → `Failed Tests 1`, `AssertionError: expected [ 'get /lookups', …(1) ] to deeply equal [ 'get /lookups' ]`; restored.
  - Test 7 breaks: `useAmenitiesQuery` read for `public` → `Failed Tests 1`, `AssertionError: expected [ 'get /admin/amenities', …(1) ] to deeply equal [ 'get /lookups' ]`; the retired ids dropped from the value on toggle → `Failed Tests 1`, `AssertionError: expected last "vi.fn()" call to have been called with [ [ 2, 3, 1 ] ]`; restored.
- **Departure:** `useCatalogueQuery` gains `enabled` too, so the admin's checklist reads no catalogue it does not show.
- `npm run lint` → exit 0; `npm run typecheck` → exit 0 (a first run failed only on commit 5's files already written, set aside and run again); `npm run check:links` → `2335 links in 181 documents and 1375 source files all resolve.`
- **Renumbered (the supervisor's note):** 98 is reserved for worker B's DESK PR 2, so this PR's finding is **99**
  (`99-the-owners-checklist-cannot-name-a-retired-amenity.md`, its index line, `lookups.md`, the commit body).
  Commit 4 was still `HEAD`: amended (`e7edc82e` → `f734a297`), the commit-5 work stashed meanwhile; `npm run
  check:links` → `2335 links in 181 documents and 1376 source files all resolve.`

### Commit 5 — `c1b9bb08` `feat(spaces): add the owner’s space profile` (43)
- Built: `usePricesLink`, `OwnerHead`, `PricesLinkCard`; `useSpaceEditor` gives `head` (owner), `notice` (admin,
  else `null`), the owner's badges (only «مخفية عن الزوار» while hidden), `privacy` (admin only), `pricesLink`;
  `meanwhileLines('owner')` the approval note's lines (403 «لم يعد هذا متاحًا لك في هذه المساحة؛ لم يُحفظ شيء.»,
  404 «لم تعد هذه المساحة متاحة لك.»), the gallery's upload tiles too (`PhotoUploadTile` takes `meanwhile`);
  `spacePagePath`; `space/ProfilePage.tsx`; `routes.tsx` `SPACE_PAGES` (lazy); copy `spaces.editor.owner` ×2;
  docs `spaces.md`, `architecture.md`, `overview.md`, `docs/README.md`.
- **Departures (shape):** `head` carries `{ intro, viewPublic }` and `pricesLink.action` only its label — the hrefs
  (the public page by slug, the Packages path) are the page's props, so `SpaceEditor` composes them; the public
  link uses `rel="noreferrer"` as the shell's `PublicPageLink` and the verified notice do (the plan says
  "noopener, as the shell's" — the shell's is noreferrer, which implies it). Test 12 lives in
  `SpaceEditor.component.test.tsx`, not a new `AmenitiesSection` test: its break (the owner given the link) is the
  editor's, which an `AmenitiesSection` test could not see. Test 9's "only while hidden" is two tests (shown /
  hidden), each one render.
- Tests (new code, each written with its code; red shown by its break):
  - 8 (`useSpaceEditor`): 3 new tests → `Tests  14 passed (14)`. Breaks: the admin's notice for the owner →
    `Tests  1 failed | 13 passed (14)`; `pricesLink` for the admin → `Tests  12 failed | 2 passed (14)`.
  - 9 + 12 (`SpaceEditor`): 4 new tests → `Tests  31 passed (31)`. Breaks: `PricesSection` for the owner →
    `Tests  1 failed | 30 passed (31)`; the verified badge pushed for the owner → `Tests  2 failed | 29 passed (31)`;
    `listLink` for the owner → `Tests  1 failed | 30 passed (31)`.
  - 10 (`useSaveGroup`, new file) → `Tests  1 passed (1)`; break `refetchType: 'none'` for the owner → `Tests  1
    failed (1)`, `AssertionError: expected [ { …(19) } ] to have a length of 2 but got 1`.
  - 11 (`useSectionFrame`, new file; title per the approval note) → `Tests  2 passed (2)`; break `meanwhileLines`
    ignores the place → `Tests  1 failed | 1 passed (2)`.
  - 14 (`routes`, the profile and reception's 403 only) → `Tests  2 passed | 39 skipped (41)`; breaks `profile`
    with `BOTH` → `Tests  1 failed | 1 passed | 39 skipped (41)`; the profile left out of `SPACE_PAGES` → the same.
- Checks: `npm run lint` → 1 error (`no-unnecessary-type-assertion`, my test's `as AdminSpace`), fixed, the file
  linted alone → exit 0; `npm run typecheck` → exit 0; `npm run check:links` → `2337 links in 181 documents and
  1378 source files all resolve.`; component `src/features/spaces src/features/lookups` → `Test Files  46 passed
  (46)` / `Tests  353 passed (353)`; unit `src/features/spaces src/shared/lib` → `Test Files  15 passed (15)` /
  `Tests  91 passed (91)`; routes alone → `Tests  41 passed (41)`. 22 files.

## 3. On the head (`c1b9bb08`) — STOPPED at the component lane

- Before the lanes: `Get-CimInstance … app-b … vitest` → 2 processes; waited until 0, then ran.
- `npm run test:unit` → every workspace green: `Test Files  17 passed (17)` / `Tests  227 passed (227)`;
  `Test Files  48 passed (48)` / `Tests  757 passed (757)`; `Test Files  84 passed (84)` / `Tests  858 passed (858)`.
- `npm run test:component` → **`Test Files  1 failed | 172 passed (173)` / `Tests  1 failed | 1155 passed (1156)`**,
  `Duration  495.16s`:
  `FAIL |component| src/pages/dashboard/routes.component.test.tsx > the dashboard's navigation > lists the owner’s
  eleven pages, the overview marked as the page shown` — `TestingLibraryElementError: Unable to find
  role="navigation" and name "Space dashboard"`. The space shell's cold load did not arrive within the test's wait:
  **finding 87's timeout**, which §13 names as a stop ("The routes test times out (finding 87)… never raise a limit").
- **Recorded time (finding 87):** the same file alone, once, as a diagnostic (not the lane):
  `✓ … lists the owner’s eleven pages, the overview marked as the page shown 2492ms`, `Tests  41 passed (41)`,
  `Duration  25.73s`. In the parallel run during commit 2 the same test failed the same way, and passed alone.
- Context, not an excuse: the machine was heavily loaded during the lane (other agents' processes: Codex, Copilot,
  several Playwright MCP servers; the lane took 495 s). This PR does not change the owners' shell or what it
  cold-loads; `routes.tsx` now resolves a space page through `SPACE_PAGES` first and the placeholder otherwise —
  the overview still loads `PlaceholderPage` lazily, as before.
- The JSON reporter's file was not written (the `--outputFile` path through the workspace script); the time above is
  from the verbose reporter of the single-file run.

**Not run yet (stopped before them):** the build with `NODE_ENV=production`, `check:build`, `check:classes`,
`format:check`, `check:links` on the head; the real run (`docker start masaha-postgres-1` done, `masaha_dev`
migrations up to date — "Database schema is up to date!" — the demo space 7 with its owner and receptionist
present; the CDP scripts are written: `scratchpad/run/run1.mjs`–`run3.mjs`; no server started); `#PRNUM`, the push,
the PR, CI, `CLEAN`, the conflict check.

**Where the work stands:** five commits on `feat/owner-space-profile`, local, not pushed; `git status` clean.

**The owner decides (offered, not chosen):**
- **A (recommended):** run the component lane again on a quieter machine (no other agents' test or browser processes)
  and, if it passes, go on; finding 87 stays open with today's numbers (2492 ms alone, a miss under a 495 s lane).
- **B:** fix finding 87 first (a separate item: the owners shell's cold load of the whole `space-links` index), then
  resume this PR.
- **C:** accept the routes test's timeout for this PR as a known finding-87 miss, and go on to the build, the real run
  and the PR.

## 4. The owner chose A — the component lane once more on the head (`c1b9bb08`)
- 12:39: `Get-CimInstance … app-b … vitest` → 0; free memory **3,964 MB of 15,680 MB**.
- `npm run test:component` (verbose reporter) → **`Test Files  1 failed | 172 passed (173)` / `Tests  1 failed | 1155
  passed (1156)`**, `Duration  431.00s`:
  `× lists the owner’s eleven pages, the overview marked as the page shown 3085ms` —
  `TestingLibraryElementError: Unable to find role="navigation" and name "Space dashboard"`. The same test, the
  same miss as the first lane (2492 ms when the file runs alone). Every other test passed.
- 12:47: free memory after the lane **5,410 MB of 15,680 MB**.
- **STOPPED again, as the owner's instruction says:** no limit raised, no narrower run, nothing after the lane run
  (no build, `check:build`, `check:classes`, `format:check`, `check:links` on the head; no real run; no push, no PR).
  Five commits local on `feat/owner-space-profile`, `git status` clean.
- **For the owner:** the miss now repeats in two full lanes (495 s, 431 s) while the file alone passes. Whether this
  PR makes it likelier is not known: it does not change the space shell or its cold load, but it adds a lazily
  loaded space page and two routes tests (whose `beforeAll` imports `ProfilePage` only for their own describe). A run
  of the same lane on `origin/main` (`7d48c9c3`) would tell whether the miss predates the PR: not done, as it is a
  decision (B in §3: finding 87 fixed first, or C: accepted for this PR).

## 5. The owner chose C (CI as the judge)
- Recorded as a **local timeout of finding 87 under load**: lane 1 495.16 s and lane 2 431.00 s, each `1 failed | 1155
  passed (1156)` on «lists the owner’s eleven pages» (3085 ms in lane 2); the file alone passes it in 2492 ms; free
  memory 3,964 MB before lane 2, 5,410 MB after (of 15,680 MB). The PR's Evidence says so. CI's `test:component` on
  the pushed head must be green; if that test fails on CI: stop (no limit raised, no CI re-run).
- On the head (`c1b9bb08`): `NODE_ENV=production npm run build` → `✓ built in 2.02s` (Vite's usual chunk-size
  warning); `npm run check:build` → `No showcase code in 38 build files (1033 strings checked).` / `No dashboard code
  in the site's first download.` / `No data-table or leaflet, nor Leaflet's stylesheet, in the site's first
  download.`; `npm run check:classes` → `No physical direction or arbitrary-value classes in 950 files.`;
  `npm run format:check` → `All matched files use Prettier code style!`; `npm run check:links` → `2337 links in 181
  documents and 1378 source files all resolve.` Not run: `test:api` (no API or shared change; CI runs it).

## 6. The real run (head `c1b9bb08`)
- **Browser:** local headless Chrome over CDP (Node's own WebSocket; no `playwright` MCP tools in this session).
  Scripts: `scratchpad/run/run1.mjs`, `run1b`, `run2` (widths), `run3` (reception, admin), `run4` (checklist),
  `run5` (admin prices). Shots: `C:\dev\masaha\workspace\WORKER_A\OWNER_SETUP\shots\pr1\` (48 PNG, 4 network logs).
- **Setup:** `docker start masaha-postgres-1`; `masaha_dev` "Database schema is up to date!"; API `npm run dev -w
  @masaha/api` (`/health` → `{"status":"ok","db":"up"}`), web `npm run dev` (5320 → 200).
- **A setup problem met, and how it was solved (no code, no `.env` change):** both demo accounts refused
  `SEED_DEMO_PASSWORD` (`401 INVALID_CREDENTIALS`; the admin signed in): the accounts no longer held the `.env`'s
  demo password. Through the app's own routes, the admin issued each a temporary password
  (`POST /admin/users/14|15/temporary-password` → 200, handover 204), and each account changed it to the
  `.env`'s demo password (`POST /me/password` → 200); signing in with it → 200. No password printed. **Data changed
  in `masaha_dev`** by this and the run: the demo accounts' passwords (now the `.env`'s again; two
  `user.temporaryPasswordIssued`/`HandedOver` audit entries each); demo space 7's hours (a shift «مسائية»
  16:00–20:00), amenities (+«طاقة شمسية», own «ركن قهوة»), contacts (+0599111222), «المساحة» confirmed, its name
  changed and put back, its gallery 2 → 5 photos (two runs' uploads, one removal); space 14 a contact (+0599333444);
  space 16 linked to the demo owner and the link ended again (two audit entries).

| Case | Seen | Shots |
|---|---|---|
| The page, its head line | h1 «ملف المساحة»; «كل قسم يُحفظ وحده، ويظهر للزوار فور حفظه.» and «عرض الصفحة العامة» (`href="/spaces/masaha-demo"`, `target="_blank"`, `rel="noreferrer"`); no notice, no privacy line, no verified badge | `ar-light-{1440,768,390}-profile-head`, `en-dark-{1440,768,390}-profile-head` |
| The checklist | demo space 7 has nothing missing (none shown, as designed); on space 16 (the demo owner linked by the admin for the case): «ما زال ناقصًا» — «المساحة تمّت», four «لم تُضف بعد» — / "Still missing…" | `ar-light-1440-checklist`, `en-dark-390-checklist` |
| Each section saved, dated | toasts «حُفظ قسم «المساحة»», «…«ساعات العمل»» (a new shift), «…«المرافق»» (an amenity ticked, one of its own), «…«التواصل»» (a contact); no section failure | `ar-light-1440-hours-saved`, `-amenities-saved`, `-contact-saved` |
| A group confirmed | toast ««المساحة»: المعلومات ما زالت صحيحة»; its date «آخر تحديث اليوم» | — |
| The switcher follows the name | the sidebar's name «مساحة تجريبية» → «مساحة تجريبية الجديدة» after the save, then back | `ar-light-1440-switcher-follows-name` |
| Photos | 4 → 6 uploaded (tiles while travelling); «الصورة 6 الآن في الموضع 5 من 6»; «الصورة 2 هي الغلاف الآن»; the removal's dialog «حذف الصورة 6؟ / تختفي من صفحة المساحة فورًا ولا يمكن استرجاعها. / رجوع / حذف» → toast «حُذفت الصورة 6», 5 left | `ar-light-1440-photos-uploading`, `-photos-uploaded`, `-photos-cover`, `-photo-remove-dialog`; `{ar-light,en-dark}-{1440,768,390}-photos` |
| The leave guard | an unsaved name, then the sidebar's «الإعلانات»: «مغادرة الصفحة مع تغييرات غير محفوظة؟ / ستضيع التغييرات غير المحفوظة في المساحة. / البقاء / المغادرة»; «البقاء» kept the page | `ar-light-1440-leave-guard` |
| The prices row → Packages & prices | «الأسعار / تُعدَّل وتُؤكَّد في الباقات والأسعار · / آخر تحديث قبل 377 يومًا / قديمة / الباقات والأسعار»; the link `/dashboard/spaces/7/packages` → its placeholder titled «الباقات والأسعار» (the page is PR 2's) | `{ar-light,en-dark}-{1440,768,390}-prices-row`, `ar-light-1440-packages-placeholder` |
| No way to the amenities list; public lookups | «المرافق» has no link; the area «الرمال» from the catalogue | `{ar-light,en-dark}-{1440,768,390}-amenities` |
| Reception refused | `/dashboard/spaces/7/profile` → «لا تملك صلاحية الوصول إلى هذه الصفحة / هذه الصفحة غير متاحة لحسابك.» in the shell; no «ملف المساحة» in its sidebar | `ar-light-{1440,768,390}-reception-403` |
| Network log | every owner run: **0** `/admin/` requests (run 1: 28 requests; run 1b; both widths runs 15 each; run 4); writes only on `/manage/spaces/7…` | `ar-light-1440-network-log.txt`, `-network-log-b.txt`, `ar-light-network-log.txt`, `en-dark-network-log.txt` |
| No horizontal scroll | `scrollWidth > innerWidth` false at 1440, 768, 390, both languages | — |
| The admin's editor (regression) | unverified space 14: its notice and «Link an owner»; «Amenities» with "Manage the amenities list" → `/dashboard/admin/lookups?tab=amenities`; a contact saved → "Contacts saved", `PUT /admin/spaces/14/contacts` | `en-dark-1440-admin-contact-saved` |
| The admin's prices table from 1024 | two draft rows (never saved): the header row `grid` at 1440 and 1024, `none` at 768, each price a card | `en-dark-1440-admin-prices-table`, `en-dark-1024-admin-prices-table`, `en-dark-768-admin-prices-cards` |

- Page errors: 0 in every run. Not performed, as the plan names (component tests prove them): the owner's link ending
  mid-session (tests 10, 11), a retired amenity's line (test 7; the demo space has none retired).
- Servers stopped by PID (tsx watch, the API, pino-pretty, vite; the CDP Chrome profiles); `Get-NetTCPConnection
  -LocalPort 3320,5320 -State Listen` → none.

## 7. `#PRNUM`, the push, the PR
- `git grep -n "#PRNUM" HEAD` → 12 lines; the next number → 96 (DESK's #95 open; #62 no longer open).
  `git filter-branch … 's/#PRNUM/#96/g'` over `origin/main..HEAD`; `refs/original` removed; `git grep "#PRNUM" HEAD`
  → 0; `git diff origin/main --stat` → `98 files changed, 1642 insertions(+), 615 deletions(-)`, before and after.
- Commits now: `1845c50f` refactor(spaces): share the shekel helpers (42) · `e3d2d944` refactor(spaces): give the
  editor its place (43) · `4072e26c` fix(spaces): start the prices table at 1024 px (46) · `1a56a31b` feat(lookups):
  offer the public lists to owners (47) · `677d7822` feat(spaces): add the owner's space profile (43).
- Pushed `feat/owner-space-profile`; **PR #96** https://github.com/Basel-Ghonaim/masaha/pull/96 (assignee me; `feat`,
  `area:web`, `area:docs`; title = commit 5's subject). The Evidence records finding 87's local timeout as the owner said.
- Note: 98 files, above the plan's ≈ 70 — the threaded place touched each hook's test, as S1's cost said.
- **Conflict check** with DESK #95 (`origin/feat/desk-visits` at `b225d1fa`): `git merge-tree --write-tree
  origin/feat/owner-space-profile origin/feat/desk-visits` → `CONFLICT (content): Merge conflict in
  docs/architecture/findings/README.md`; `docs/README.md` and `docs/project/overview.md` auto-merge. Files shared:
  those three documents only, no code file. The conflict: both add their finding's line after 97 under *Open* (DESK's
  98, this PR's 99) — the fast path (workflow §9): keep both lines, in number order, for whichever merges second.
- First CI on `677d7822`: every check passed (lint, format:check, typecheck, test:unit, check:classes, check:links,
  test:api, **test:component**, build, CodeRabbit; run 39407660364 `success`). Meanwhile DESK #95 merged
  (`f77d2012`) and GitHub showed `DIRTY`: the findings index's conflict foreseen above.
- **Rebased on `origin/main` (`f77d2012`)** (workflow §9: dirty): the one conflict, in commit 4, resolved by keeping
  both lines (98 DESK's, then 99). No code file of this PR changed on `main` (`comm` of both change lists → the three
  documents only). `packages/shared` changed on `main`: `npm run build -w @masaha/shared`; the local Prisma client was
  older than #95's migration (API typecheck `TS2353 … 'chargeReason'` in DESK's test), so `npx prisma generate` in
  `apps/api` (what its `postinstall` runs; no repository file changed). Then `npm run typecheck` → no error;
  `npm run check:links` → `2411 links in 185 documents and 1410 source files all resolve.`; `npm run format:check` →
  `All matched files use Prettier code style!`. Commits now: `2274db9b`, `06b2705b`, `15a33bad`, `2200ea92`,
  `9fae4e00` (subjects unchanged). Pushed with `--force-with-lease`.
- **CI on `9fae4e00`:** lint, format:check, typecheck, test:unit, **test:component**, check:classes, check:links,
  build, test:api, CodeRabbit — all `pass` (run 39408550023 `success`); `gh pr view 96 --json mergeStateStatus` →
  **`CLEAN`**. The PR description's Evidence updated with the rebase and CI. `git status --short` → empty.

## 8. Final report (`final-report`)
1. **PR #96** https://github.com/Basel-Ghonaim/masaha/pull/96 · head **`9fae4e00`** · CI green on that head (run
   39408550023) · **`CLEAN`**. Not merged.
2. **Commits:** `2274db9b` refactor(spaces): share the shekel helpers (42) · `06b2705b` refactor(spaces): give the
   editor its place (43) · `15a33bad` fix(spaces): start the prices table at 1024 px (46) · `2200ea92` feat(lookups):
   offer the public lists to owners (47) · `9fae4e00` feat(spaces): add the owner's space profile (43).
3. **Run:** per commit lint + typecheck (§2); on the head `test:unit` (227 / 757 / 858 passed), `test:component`
   twice locally `1 failed | 1155 passed` (finding 87's local timeout, §3–§5), build, `check:build`, `check:classes`
   (950 files), `format:check`, `check:links` (2337; after the rebase 2411); CI all green, `test:component`
   included. **Not run:** `test:api` locally (no API change; CI passed it); E2E (end of project).
4. **Breaks / red first:** tests 1–12 and 14 each seen red through their breaks (§2); test 1's planned break
   replaced by one that can fail.
5. **Problems and how solved:** the shell's `d.type` misuse in my CDP scripts (rewritten); the demo accounts no
   longer held `.env`'s demo password (restored through the app's own admin and forced-change routes, §6); typecheck
   run while commit-5 files existed (set aside, re-run); the finding renumbered 98 → 99 at the supervisor's word
   (commit 4 amended); DESK's merge made the PR dirty (rebased, fast path); the stale Prisma client after #95's
   migration (`prisma generate`).
6. **Unexpected, unsolved:** the routes test «lists the owner’s eleven pages» missed its cold-load wait in both
   local full lanes (495 s, 431 s) while passing alone (2492 ms) and on CI — finding 87's margin, not fixed here.
   `docs/design/INDEX.md` still holds a `<<<<<<<` marker on `main` (as USERS noted; not this PR's).
   The gallery's «رُفعت N من M» line was not read by my script after the uploads (the tiles, toasts and order lines
   were); not investigated further.
7. **Early conflict check:** `gh pr list --state open` → only #96 itself; no other open PR. (Before DESK merged:
   one docs conflict with #95, resolved by the rebase.)
8. **Departures:** gathered at §1–§7: the finding number (99); test 1's break; commit 3's *Why* wording; the
   shapes in commits 2 and 5 (the `meanwhileLines` third argument, `listLink` nullable from commit 2, the owner's
   403 for a space they may not edit, the checklist by `mayEdit`, hrefs composed in `SpaceEditor`, `rel="noreferrer"`);
   test 12's file and test 9 as two tests; `useCatalogueQuery`'s `enabled`; the PR at 98 files (plan ≈ 70); the
   demo passwords reset through the app; the stale Prisma client regenerated.
