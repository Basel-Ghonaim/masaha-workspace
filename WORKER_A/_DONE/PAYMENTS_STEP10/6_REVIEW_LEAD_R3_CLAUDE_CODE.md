# Review of #129 — R3: the user's side (my reports, the report dialog, favourites) and the space page — Claude Code
Head: fcf46637 · range dc427a54..fcf46637 (6 commits) · checks: green (build, check:classes, check:conflicts, check:links, format:check, lint, test:api, test:component, test:unit, typecheck pass; CodeRabbit skipping) · head moved during the review: no (`headRefOid` fcf46637 at the start and the end, `CLEAN`)
Verdict for my range: mergeable after a fix round (F1 needs the owner's word on DI-58 first)

Read pinned to commit objects only (`git show <sha>`, `git show fcf46637:<path>`); no checkout, no run of any test or build. Every file of my range was read at its commit; where a later commit in my range changed a file, it was read at fcf46637 too. No file outside my range changed one of mine after it.

## Findings (verified defects only, most severe first)

### R3-F1 — should-fix · «تراجع» after «إزالة» of a space that left can never work
- Where: `apps/web/src/features/favorites/components/RemoveFavorite.tsx:17` (the removal through `useFavoriteToggle`, `saved: true`), its undo at `apps/web/src/features/favorites/hooks/favoriteWrite.ts:60` (`again(!save, 'quiet')` → `POST /me/favorites/:id`); the test `RemoveFavorite.component.test.tsx:35`; the documents `docs/features/favorites.md:35`, `docs/features/directory.md:134` — at fcf46637.
- Seen in the code: «إزالة» is offered only on the rows `listed: false` (`useFavoritesView`, `FavoritesView` → `unlistedAction`). Its toast's «تراجع» sends `POST /me/favorites/:spaceId`. The contract at `origin/main` (*Favourites*, `POST /me/favorites/:spaceId`) answers **`not_found` (404) for a space that is not publicly listed — unknown, hidden, deleted, or in an area not listed**, which is exactly what `listed: false` means (`FavoriteSpace`'s comment: "hidden, deleted, or in an area not listed"). So the undo always fails. `toastFavoriteFailed` then says «لم تعد هذه المساحة في الدليل.», and the favourite is gone for good. Test 81's undo case passes only because its fake server answers the `POST` with 204, an answer the API never gives for that space.
- Scenario: a user opens «المفضّلة», presses «إزالة» on a space that left, sees «أُزيلت من المفضّلة · تراجع» and presses «تراجع» → an error toast «لم تعد هذه المساحة في الدليل.» The space is not restored, and it can no longer be saved again from anywhere. The UI offered an undo it cannot honour, and `favorites.md` says «تراجع», "which saves it again", which is false.
- Fix: one of these, for the owner to choose, since DI-58 (approved) says «إزالة» (with «تراجع») and the plan did not know about the API's 404:
  - **(a)** No «تراجع» on «إزالة» of a space that left. The toast says it was removed, and that it cannot be saved again while it is out of the directory. Optionally the removal asks first (as a destructive action with no undo). Test 81's undo case becomes "no undo offered". The two document lines are corrected.
  - **(b)** Keep the undo and record a new finding (187) for the API: allow the re-save of a favourite the user just removed. This is an API change, out of this PR's scope; until then the undo stays broken, so (a) is still needed now.
- Belongs: a fix round on #129 (folded into `0b75e262 feat(favorites): list a user's favourite spaces`) after the owner's word on DI-58.

### R3-F2 — should-fix · A guest's held favourite (and report) has no end: it waits for any later sign-in in the tab, whoever's
- Where: `apps/web/src/features/favorites/hooks/intent/favoriteIntent.ts:9,13` (a module variable, cleared only by `takeFavorite` or `dropFavorite`), `features/favorites/hooks/resume/useResumeFavorite.ts` (mounted by `pages/site/shell/SiteLayout.tsx` on every site page, it takes and saves the held favourite on any transition to a session); `apps/web/src/features/data-reports/hooks/intent/reportIntent.ts:7` with `hooks/report/useReportAction.ts:27` (`resumed = signedIn && held === slug`) — at fcf46637.
- Seen in the code: the only things that clear a held intent are a session being established (the favourite is then saved; the report's dialog opens on that space's page) and the prompt's own close (`useSignInPrompt`'s `onClose` → `cancel`). Pressing the prompt's «تسجيل الدخول» / «إنشاء حساب» link navigates away. The page unmounts, Radix's `Dialog` does not call `onOpenChange(false)` on unmount, and nothing else clears the intent. Neither the sign-in page being left without a session, nor a later navigation, nor any time limit does. A grep of the head finds no other caller of `dropFavorite`, `dropReport`, `takeFavorite` or `takeReport`. Not reproduced in a browser (no runs allowed); the path is read in the code.
- Scenario: on a shared device (a coworking space's or a café's computer), guest A presses the heart on «نور هب», then «تسجيل الدخول», then leaves the sign-in page through the wordmark without signing in. Later, in the same tab with no reload, B signs in from the header. `ResumeFavorite` saves «نور هب» into **B's** favourites with «حُفظت نور هب في المفضّلة»: a write B never asked for. The report's variant: the held slug stays until someone signed in opens that space's page, and the report dialog then opens by itself. It is never sent by itself, so the harm there is small. This is also the "later visit" the role file names: the intent survives any length of browsing in the tab.
- Fix: bound the held intent to the round trip it serves. Keep a timestamp with it and drop it once stale (for example 15 minutes), and/or drop it when the site shell sees a guest land on a page that is neither the sign-in/register pages nor the page that held it. Add one test each: a held favourite is not saved by a sign-in after the guest left the auth pages, or after the bound. S14 stays as approved: memory only, never the address.
- Belongs: a fix round on #129 (folded into `c9739dcd feat(data-reports): report wrong information` for the report and `1285d9ab feat(favorites): save a space from its card` for the favourite).

### R3-F3 — nit · The heart changes its name and is `aria-pressed` too
- Where: `apps/web/src/features/favorites/hooks/toggle/useFavoriteToggle.ts:41` (`label: pressed ? words.remove(...) : words.save(...)`) with `components/FavoriteButton.tsx:30` (`aria-pressed`) — at fcf46637.
- Seen in the code: a toggle button whose accessible name flips between «حفظ {name} في المفضّلة» and «إزالة {name} من المفضّلة» while `aria-pressed` also flips. A screen reader then reads "Remove Noor Hub from favourites, toggle button, pressed", which is two opposite cues at once. WAI-ARIA APG's button pattern asks that a toggle's label not change with its state. The plan's §9 (commit 4) specified both, so this follows the plan.
- Scenario: a screen-reader user presses "Save Noor Hub to favourites, toggle button, not pressed" and hears "Remove Noor Hub from favourites, pressed". It is unclear whether "pressed" means saved or removed.
- Fix: keep `aria-pressed` with one fixed name («حفظ {name} في المفضّلة»), or keep the changing name and drop `aria-pressed`. Either way, update test 77 and `favorites.md`'s heart paragraph.
- Belongs: a fix round on #129 (folded into `1285d9ab`), or the owner keeps the plan's wording. If so, record it.

### R3-F4 — nit · `overview.md` omits the report from a space's page
- Where: `docs/project/overview.md:31` at fcf46637.
- Seen in the code: the *Data reports* line ends "on the site, a signed-in user's «بلاغاتي» with the replies". The report button and dialog on a space's page, built in `c9739dcd`, are not named, while `data-reports.md` (scope, *Who uses it*, *Behaviour*) names them.
- Scenario: a reader of the overview's *Built* list concludes that reporting wrong information is API-only.
- Fix: "…on the site, the report of wrong information from a space's page and a signed-in user's «بلاغاتي» with the replies."
- Belongs: a fix round on #129 (folded into `c9739dcd`).

## The plan's tests and breaks for my range (one line each: present / missing / weaker; would it fail?)

The breaks' red output is **only in the reports** (`scripts\lane-c\REPORT.md`, the lead's *Commit 6*). I ran none. For each test I judged from its code whether the named break would turn it red.

- 59 `dataReportsRepository.unit.test.ts`: present (201 → `repeated: false`, 200 → `true`, no key). `repeated` always false fails it.
- 60 `useMyReports`: present (listed link; a gone space as text with C7's line; reply by `repliedBy`). A gone space linked fails it.
- 61 `useMyReports`: present (chip replaces the address, `REPLACE`, page 1; the two empties; loading, failure). The page kept fails it.
- 62 `MyReportsList`: present (161 characters folded, `aria-expanded`/`aria-controls`, the short one has none, `dir="auto"`, axe). The toggle always drawn fails it.
- 63 `AccountLayout`: present (nav «My account», `aria-current`, a guest to `/login?next=`). Would fail.
- 64 the users' menus: present (`AccountMenu`, `AccountMenuSection` order with favourites and reports; `CompactAccountMenu` dashboard and sign-out only). Would fail.
- 65 `reportIntent.unit.test.ts`: present (taken once; another slug not). Would fail.
- 66 `useReportAction`: present (guest holds and asks with `report`; back signed in it opens; closed it does not reopen; another slug and a dropped hold do not open). Would fail. It does not cover F2 (an abandoned sign-in).
- 67 `useReportDialog`: present («أخرى» needs details; the body; 429 countdown with values kept; no answer keeps input and nothing is re-sent in 10 s). Would fail.
- 68 the same file: present (the toast by verification with «عرض بلاغاتي»; a 200 says repeated; `['me','reports']` invalidated). Would fail.
- 69 `ReportAction`: present (dialog named, U10 line, the combobox focused first, `role="alert"`, the focus back on the button, axe). Would fail.
- 70 `SignInPrompt`: present (title and line by reason; both links carry `next` with the query). Would fail.
- 71 `Icon.component.test.tsx`: present (`HeartIcon` drawn, `fill-current` kept, never mirrored). Would fail.
- 72 `favoritesRepository` / `favoriteIntent` units: present (paths, no body, no `Idempotency-Key`; held and taken once; dropped). Would fail.
- 73 `useFavoriteToggle`: present (pressed before the answer, held until the read, `invalidateQueries(['me'])`; «Undo» sends the inverse once). Would fail.
- 74 the same file: present (network failure flips back, «Try again», nothing re-sent in 10 s; `FAVORITES_LIMIT_REACHED` with «Manage favourites»; 404 worded). Would fail.
- 75 the same file: present (a guest holds, `signIn('favorite', …)`, nothing sent). Would fail.
- 76 `useResumeFavorite`: present, under `StrictMode` (saved once; once again after a remount with the session; failure with retry; nothing without a hold). Would fail.
- 77 `FavoriteButton`: present (`aria-pressed`, name, `fill-current text-primary`, axe). Would fail; see F3 on what it pins.
- 78 `useFavoriteIds`: present (one `GET /me/favorites` with a session, the ids of listed and gone; none for a guest). Would fail.
- 79 `SpaceCard`: present (one link, the button not inside it, axe). Would fail.
- 80 `useFavoritesView`: present (newest first, gone ones apart; near me with `sort=distance` and the header; clearing drops the near answer — one key left; empty; failure with retry). Would fail.
- 81 `FavoritesView` / `RemoveFavorite`: present (focus to the next row, else the first heart, else the count; axe at 390 and 1440). **Weaker:** its «Undo» case proves a `POST` the API answers 404 for that space (F1), so it pins a behaviour that cannot happen.
- 82 `runningClosure.unit.test.ts`: present (starts now; ends at now passed over; upcoming and other types passed over; the first of several). `<=` on the end fails it.
- 83 `SpaceAnnouncements` / `ClosureNotice`: present (closure not repeated; the others by start, with an upcoming closure among them; Arabic fallback marked `lang`/`dir`; nothing with none). Would fail.
- 84 `SpacePage.component.test.tsx`: present (U8 at 390 and 1440: notice before the `h1`, section after the status card at 390 and after the name, before the prices, report after the prices; the heart in the name's row). Would fail. The 1440 case cannot check "after the status" (the aside), and says so.
- 84b / LEAD-D12's test ("shows the heart pressed once a guest's held favourite is saved on their return"): present. Its red is in `scripts\fix-heart-red.txt` ("Unable to find role="button" and name `/^Remove .Noor Hub. from favourites$/`", 4496 ms), read there. The test is real but depends on timing: it is red only while the hearts' first `GET` is still in flight when the save lands, which the fake transport's ordering produced in the lead's run. I could not re-run it.
- 85 catalogue parity: existing test. The new sections (`favorites`, `dataReports.mine/report`, `site.account/signInPrompt`, `users.account.links`) are typed `satisfies Catalogue[…]` and covered by it.

## Decisions taken without the owner in my range, judged

- **LC-D1** `HeartIcon` in the showcase's icon list: sound.
- **LC-D2** no document in commit 3: sound (foundation has no icon list).
- **LC-D3 / LEAD-D6** reports returned as text: acceptable, process only.
- **LC-D4** «بلاغاتي» reuses `useSpaceReportsFilters`: sound. It is the same address rule (S8), and DI-55 holds.
- **LC-D5** copy reused by key (`sheet.replySpace/replyTeam`, `pagination`, `site.browseSpaces`, `status.retry`): acceptable. Also reused without being listed: `occupancy.present.refreshFailed` («تعذّر التحديث؛ تظهر آخر قائمة.») for «بلاغاتي»'s failed refresh; the words fit.
- **LC-D6** no `SITE_PATHS.account`: sound (S6 said it is not a route yet; nothing uses it).
- **LC-D7** `signIn(reason, cancel)`, closing the prompt drops the intent: sound as far as it goes; it is the only drop, which is F2.
- **LC-D8** the held report a zustand store; "once" means until the dialog closes, where the plan had `takeReport` on mounting: acceptable for the round trip, but it widens F2 (the report reopens on any later signed-in visit to that space).
- **LC-D9** `SpacePageView.space: { id, slug, name, verified }`: sound.
- **LC-D10** `useReportDialog`'s tests render `ReportDialog`: acceptable.
- **LC-D11** `invalid_choice` → «اختر نوع المعلومة»: sound.
- **LC-D12** favourite writes in `writeFavorite`, outside the component: sound («تراجع» works after the heart left the page).
- **LC-D13** `RemoveFavorite` held with `aria-disabled`: sound (keeps the focus for DI-52).
- **LC-D14** DI-52's order (next «إزالة», else the **first** card's heart, else the count): acceptable. DI-52 says "the next card's heart"; the rows come after the cards, so "first" is the reasonable reading.
- **LC-D15** clearing near me drops the favourites' near answers: sound (the point is not kept past its clearing).
- **LC-16** the site routes test's QueryClient: sound.
- **LC-17** `beforeAll` preload in `SpacePage.component.test.tsx`: acceptable (a test-time measure; LEAD-D11, R1's range, addresses the root).
- **LC-18** architecture's "`account/` not built" corrected to "the account's settings (screen 9)": sound.
- **LC-19** `DirectoryList` unchanged: sound (`DirectoryResults` draws the cards).
- **LC-20** a press while the session restores is ignored: acceptable, though silent. A press in that brief window does nothing, with no sign.
- **LC-21** the account's links before the dashboard in the menu: acceptable.
- **LEAD-D8** `ClosureAlert` (presentational) beside `ClosureNotice({ items })`, with a local `PublicAnnouncement = Pick<Announcement, …>`: sound. It keeps the no-cross-feature rule, and the directory's type is structurally the same.
- **LEAD-D9** the layer's polite `role="status"` for the warning: acceptable. The notice is present at load, not an interruption, and DI-59 asks only for `Alert variant="warning"`.
- **LEAD-D10** finding 180 recorded rather than fixed: sound. The plan made it a conditional finding (§6's last row), and `check:build` guards the first download, which this PR made smaller. The stated cause fits the code I saw: `data-reports`' `index.ts` exports `SpaceReportsList`/`AdminReportsList` beside `ReportAction`/`MyReportsList`, and `announcements`' exports `AnnouncementsList` (the sheet's date fields) beside the public pieces. App modules are not side-effect-free to the bundler, so a page importing the entry carries the others' chunks. The byte sizes are **only in the report** (I ran no build).
- **LEAD-D12** cancel the in-flight `['me']` reads, then invalidate: sound. TanStack Query v5's `Query.fetch` joins an in-flight fetch when the query has no data yet (`cancelRefetch` cancels only when data exists), which is the lead's stated cause. `cancelQueries` (with `revert`) sets the state back to idle synchronously, so the following `invalidateQueries` starts a new read. No code awaits a `fetchQuery`/`ensureQueryData` under `['me']` (grep of the head), so the cancel rejects nothing that waits on it.

## Outside my range (one line each, for the other reviewers)

None found.

## Checked and fine

- **The guest's round trip (S14/S15):** the favourite is held as `{ spaceId, name }`, taken once by the shell's `ResumeFavorite` (StrictMode-safe: `takeFavorite` clears as it reads), saved and said «حُفظت {name} في المفضّلة». The report is held by slug; the dialog opens only on that space's page, and closing it or the prompt lets it go. It is never sent by itself. Nothing is in the address. Finding 168 is true: a reload or an e-mailed recovery link loses memory, and Google sign-in is the GIS button (`renderButton`), so the page stays alive.
- **The toggle:** optimistic and held until the `['me']` read after the write (S13); a double press is handled by the `latest` ref, so an earlier write's late settle leaves the later press's state alone; a failure rolls back. `FAVORITES_LIMIT_REACHED` gets «إدارة المفضّلة» → `/me/favorites`; a 404 is worded and invalidates `['me']`. The undo is sent once with no key, and nothing is re-sent by the transport. `Button size="icon"` is `size-(--control-height)` (44 × 44 on touch; the real run measured it, only in the report). The name is isolated in the label and the toasts.
- **One source for the saved state:** `useFavoriteIds` (`['me','favorites',{}]`, `enabled` only with a session) is read by `DirectoryResults`, `HomeSpaces` and `SpaceDetails`. «المفضّلة» reads the same key, or `{ near }`. The point goes in `Masaha-Near` only, never in params (repository unit), and lives only in memory: there is no query persister in the app.
- **«المفضّلة»:** the listed spaces as the directory's cards with their heart pressed; the gone ones as muted cards with C7's line; count `aria-live`, `tabIndex={-1}`; skeletons, failure, empty with «تصفّح المساحات»; the grid `md:grid-cols-2 xl:grid-cols-3`. `useUnlistedFocus` hands the focus on only when it fell to `body`.
- **The report dialog:** the field `Select` (combobox focused first by `onOpenAutoFocus`), details required only for `OTHER` (`createReportSchema` via `useServerForm`), a blank message left out, nothing closes it while it is sent, the failure an alert with the input kept, offline worded as a safe retry, 429 counted down with the submit blocked. Toasts: success for 201 by verification, info for 200, each with «عرض بلاغاتي». `['me','reports']` invalidated, not awaited. `DialogClose asChild` keeps `type="button"` (the layer's `Button` sets no type).
- **«بلاغاتي»:** `/me/reports` only (the user's own, server-side); 20 a page; chips in the address with page 1 on a change; the day only (`reportDay`, Gaza); the message folded by length (>160 code points, `Array.from`); the reply labelled by `repliedBy`; a gone space as text.
- **The account area:** `AccountLayout` nav `aria-labelledby` «حسابي» (`sr-only lg:not-sr-only`), `aria-current="page"`, `Button size="sm"` (44 on coarse pointers). Each page is wrapped in `RequireAuth` (a guest goes to `/login?next=` with the query). The site's menus pass `ACCOUNT_LINKS` (favourites, reports); `CompactAccountMenu` passes none. A staff account sees the same two links, as S5 allows every signed-in role.
- **Commit 6:** `runningClosure` compares instants (`Date.parse` against `now.getTime()`), so Gaza and UTC give the same result; `start <= now < end` (or no end). The notice slot sits above the grid (`empty:hidden lg:col-span-12`, so no gap without a closure). The section comes after the status card below 1024 px and after the head and unverified notice from it, before the prices. The running closure is left out of the section; the others are sorted by start, then id. Finding 131 is moved to *Resolved* in the index with its resolution line; 168 and 180 are in *Open*.
- **The joins (lane C onto lane B):** at fcf46637 `dataReports` copy has `admin`, `mine`, `report` once each in both languages. `queryKeys` has `spaceAll`, `space`, `adminAll`, `admin`, `mineAll`, `mine`; `index.ts` five exports. The repository has six methods in the interface and the factory, and `src/test/dataReport.ts` has `spaceReport`, `adminReport`, `myReport`, `reportsPage`. In `data-reports.md`, each *Behaviour* paragraph appears once and the three *Web history* lines are distinct. Nothing is lost or duplicated.
- **Documents:** `data-reports.md`, `users.md`, `favorites.md` (except F1's line), `directory.md` (except F1's line), `announcements.md`, `architecture.md` §2 (AccountLayout built; *Built so far*) and §7 (the favourites' `['me']` sentence), `foundation.md` §13 screen 11 «ردّ فريقنا», findings 131 (*Resolved*), 168 (both actions in its evidence), 180, and the index. Each is true to the code and dated `#129`, with no `#PRNUM` left in my range's files.

## Not checked, and why

- No test, build, `check:build` or manifest run (the rules forbid them): the breaks' red output, finding 180's byte sizes and the 44 × 44 touch targets are taken from the reports and logs, as marked.
- No browser: F2's scenario is read in the code, not reproduced; the guest flow through register and Google was not exercised.
- The «تراجع»-after-«إزالة» 404 (F1) is from the contract at `origin/main` and the code path. I did not call the API.
- The map view's chosen-space card: its heart (the plan names the Directory's and Home's cards only) was not looked at.
