# R2-AD-UX — Round 2 review: the admin's dashboard · Experience and flow

- `HEAD`: `34a6c59aab049e8f2992b29b88c8a700b926ddba`
- `origin/main`: `34a6c59aab049e8f2992b29b88c8a700b926ddba`
- Match: yes — review ran on `origin/main` (`git fetch origin` first, worktree detached at `origin/main`).
- Server: prototype served on port **5415** (`python -m http.server 5415 --bind 127.0.0.1 --directory docs/design/prototype`, workdir `C:\Users\basel\masaha-design`); spot HTTP checks returned 200.

## Verdict

The admin can walk the whole daily chain, but filtering, paging, and the verified-report path force re-work: filter changes strand the admin on deep pages, empty lists offer no way out, and verified reports end in a read-only sheet with no next step.

## Five most important points

1. Changing any filter or search keeps the old page number, so the matching rows sit on page 1 while the admin stares at page 5.
2. A verified space's data report opens a sheet the admin can only close — no jump to the owner or the space.
3. The overview promises an admin/owner split of reports that the reports list cannot filter by.
4. The overview's stale tile counts verified spaces its own work-queue card excludes, so tile, card, and destination disagree.
5. Every filtered-empty list ends the flow with no one-tap clear-filters action.

## Issues

### R2-AD-UX-001 — Filtering does not return the admin to page 1

- **type:** defect · **level:** pattern · **impact:** high
- **where:** Spaces list frame (§43 "Spaces — desktop 1440"), `http://127.0.0.1:5415/Admin%20spaces.html` (+ `?stale=1`, `?status=verified|unverified|hidden|deleted`), seen in source at 1440 and 390 (Arabic, light; applies at 768 via `AdminList` cards branch and in English/dark as same state logic); screenshot `docs/design/screens/43-admin-spaces/01-spaces-desktop-1440.webp`
- **evidence:** `C:\Users\basel\Downloads\r2-shots\AD-UX\R2-AD-UX-001.png` (not captured — no browser tool in this environment; verified in `masaha/shared.jsx` `usePaged`)
- **what is wrong:** `usePaged` resets to page 1 only when the current page no longer exists (`page > last`). Typing a search or changing governorate/status/stale/role/action filters while on page 5 keeps page 5 whenever the result still spans 5 pages, so the best matches on page 1 stay hidden and the admin must page backwards manually.
- **proposal:** Reset to page 1 on every filter/search change in all five paged admin lists (spaces, owners, reports, users, audit): pass the filter values into `usePaged` (or key the pager by them) so any change sets page 1. Pattern change — applies to `Admin spaces.html`, `Admin owners.html`, `Admin reports.html`, `Admin users.html`, `Admin audit.html`.
- **why:** The admin looking for "the one row among hundreds" always starts reading at the top; keeping a stale deep page turns every filter into a two-step hunt.
- **cost:** S
- **rule:** REVIEW_LENS §3 B.3 (fewest steps, nothing asked twice) and prompt Q5.

### R2-AD-UX-002 — A verified space's report is a dead end

- **type:** defect · **level:** page · **impact:** high
- **where:** Data-reports frame (§45 "Verified · read-only"), `http://127.0.0.1:5415/Admin%20reports.html?open=r3`, 1440 and 390, Arabic light (same logic in English/dark); screenshot `docs/design/screens/45-admin-data-reports-all-spaces/05-verified-read-only-desktop-1440.webp`
- **evidence:** `C:\Users\basel\Downloads\r2-shots\AD-UX\R2-AD-UX-002.png` (not captured; verified in `Admin reports.html` `ro` branch)
- **what is wrong:** An owner-handled (verified-space) report opens a sheet that states "for reference only" and offers no onward step: no link to the space's editor (read-only view), no link to the owner row, no link to the user who reported. The unverified path has «تعديل الحقل» into the editor; the verified path has nothing, so an urgent wrong value (e.g. `r3` opening hours) forces the admin to close, re-search owners/users, and reconstruct context.
- **proposal:** In the verified sheet, add the same two forward links the editor's read-only alert already uses: «بلاغات \<space>»-style space link (`Admin space edit.html?id=<space>`) and an owner link (`Admin owners.html?q=<owner-email>`), using the design system's existing outline `Button asChild` links.
- **why:** Every daily-task step needs a next step; a reference-only view without one breaks the resolve-report leg of the chain.
- **cost:** S
- **rule:** REVIEW_LENS §3 B.3 (no dead ends; a way back/forward) and B.7; prompt Q1.

### R2-AD-UX-003 — Reports promise an admin/owner split the list cannot filter

- **type:** defect · **level:** page · **impact:** high
- **where:** Overview (§42) → reports (§45 "All reports"), `http://127.0.0.1:5415/Admin%20overview.html` then `http://127.0.0.1:5415/Admin%20reports.html?status=new`, 1440 and 390, Arabic light; screenshots `docs/design/screens/42-admin-overview/01-overview-desktop-1440.webp`, `docs/design/screens/45-admin-data-reports-all-spaces/01-all-reports-desktop-1440.webp`
- **evidence:** `C:\Users\basel\Downloads\r2-shots\AD-UX\R2-AD-UX-003.png` (not captured; verified in `Admin overview.html` tile 2 + `masaha/admin.jsx` nav badge vs `Admin reports.html` toolbar)
- **what is wrong:** The overview tile reads "N waiting for the admin · M waiting for owners" and the sidebar badges only admin-waiting reports, but the tile lands on `?status=new` (both handlers) and the reports toolbar has space + field filters only — no handled-by filter. The admin cannot isolate "my queue" without scanning the «يعالجه» column page by page.
- **proposal:** Add a handled-by `ToggleGroup` chip pair (الإدارة / المالك) beside the status chips on `Admin reports.html`, deep-linkable, so the overview tile can land on the admin-only slice.
- **why:** Counts that cannot be acted on force visual scanning across hundreds of rows; a queue tile must land on its queue.
- **cost:** S
- **rule:** REVIEW_LENS §3 B.3/B.4 (same job the same way; fewest steps); prompt Q1, Q5. Applies settled A7/A8 (which filter set a page carries) — reported as application gap, per lens §2b.

### R2-AD-UX-004 — Stale tile, work-queue card, and destination count different things

- **type:** defect · **level:** page · **impact:** medium
- **where:** Overview (§42 "Overview"), `http://127.0.0.1:5415/Admin%20overview.html` → `http://127.0.0.1:5415/Admin%20spaces.html?stale=1`, 1440 and 390, Arabic light; screenshot `docs/design/screens/42-admin-overview/01-overview-desktop-1440.webp`
- **evidence:** `C:\Users\basel\Downloads\r2-shots\AD-UX\R2-AD-UX-004.png` (not captured; verified in `Admin overview.html` `needs` vs `todo`)
- **what is wrong:** Tile 3 counts every non-deleted stale-or-missing space (`needs`, verified included); the «اكتمال البيانات» card lists only unverified ones (`todo`) with the note that verified spaces are their owners' to update; both «عرض الكل» and the tile land on `?stale=1`, which shows verified stale spaces too. Three numbers, three scopes, one link.
- **proposal:** Scope all three to the card's rule (unverified + hidden, the spaces the admin edits): count `todo` in the tile and pre-filter `?stale=1` from the overview entry to the same set, keeping the destination's own chip for the general case.
- **why:** A work queue whose count, list preview, and destination disagree makes the admin doubt which rows are actually theirs.
- **cost:** S
- **rule:** REVIEW_LENS §3 B.1 (one job per section), B.3; applies settled A8 (tile and card count stale and missing) — application gap.

### R2-AD-UX-005 — Filtered-empty lists offer no way out

- **type:** defect · **level:** pattern · **impact:** medium
- **where:** All admin lists (§43 spaces, §44 owners, §45 reports, §46 users, §48 audit), e.g. `http://127.0.0.1:5415/Admin%20spaces.html?q=<text>` with no match, 1440 and 390, Arabic light; screenshot `docs/design/screens/43-admin-spaces/01-spaces-desktop-1440.webp` (representative)
- **evidence:** `C:\Users\basel\Downloads\r2-shots\AD-UX\R2-AD-UX-005.png` (not captured; verified `empty=` props in all five pages)
- **what is wrong:** Every `EmptyState` for "no X match the filters" is title-only. The only recovery is reopening the `FilterSheet` and pressing «مسح الفلاتر». On a phone (bottom sheet, weak connection) that is two extra round-trips per dead search.
- **proposal:** Give each filtered-empty state a primary «مسح الفلاتر» action wired to the same `onClear` the sheet footer uses. Pattern change — `Admin spaces.html`, `Admin owners.html`, `Admin reports.html`, `Admin users.html`, `Admin audit.html`.
- **why:** Recovery belongs where the failure is announced; bouncing the admin back through the sheet punishes exploring filters.
- **cost:** S
- **rule:** REVIEW_LENS §3 B.6 (every failure says what to do); P5 sheet contract stays, only its entry point is duplicated.

### R2-AD-UX-006 — Spaces search covers names only, not owners

- **type:** improvement · **level:** page · **impact:** medium
- **where:** Spaces (§43), `http://127.0.0.1:5415/Admin%20spaces.html`, 1440 and 390, Arabic light; screenshot `docs/design/screens/43-admin-spaces/01-spaces-desktop-1440.webp`
- **evidence:** `C:\Users\basel\Downloads\r2-shots\AD-UX\R2-AD-UX-006.png` (not captured; verified `rows` filter matches `s.name` only)
- **what is wrong:** The daily unlink/link leg starts from a space, but the search matches the space name alone. "Which space does Ahmad own?" cannot be answered here; owners and users search name-or-email, spaces does notrau.
- **proposal:** Extend the spaces search to owner names/emails (match against `owners` via `personName`/email, same substring rule), keeping the placeholder honest; alternatively add the reports-style space/owner cross-filter. Prefer the extended search (smaller change).
- **why:** One search box that covers both ends of the link halves the hops for the most common lookup.
- **cost:** S
- **rule:** REVIEW_LENS §3 B.3/B.4; prompt Q5.

### R2-AD-UX-007 — Owners list cannot be narrowed by space

- **type:** improvement · **level:** page · **impact:** medium
- **where:** Owners (§44), `http://127.0.0.1:5415/Admin%20owners.html`, 1440 and 390, Arabic light; screenshot `docs/design/screens/44-admin-owners/01-owners-desktop-1440.webp`
- **evidence:** `C:\Users\basel\Downloads\r2-shots\AD-UX\R2-AD-UX-007.png` (not captured; verified toolbar has search + status only)
- **what is wrong:** Mirror of 006 from the person end: "who owns Golden Hub?" requires guessing the owner's name. Reports already filter by space via a searchable `Combobox` (A7); owners has only free-text search, so a space name typed there matches nobody.
- **proposal:** Add the same space `Combobox` filter to the owners `FilterSheet` (single space, clearable, counted in the badge), reusing the reports pattern verbatim.
- **why:** Space↔owner pivots happen from both ends daily; only one end currently pivots.
- **cost:** S
- **rule:** REVIEW_LENS §3 B.4 (same job the same way); prompt Q5.

### R2-AD-UX-008 — Governorate/area filter is a long unsearchable select

- **type:** improvement · **level:** page · **impact:** medium
- **where:** Spaces (§43), `http://127.0.0.1:5415/Admin%20spaces.html`, 1440 and 390 (worst on 390, bottom sheet), Arabic light; screenshot `docs/design/screens/43-admin-spaces/02-spaces-phone-390.webp`
- **evidence:** `C:\Users\basel\Downloads\r2-shots\AD-UX\R2-AD-UX-008.png` (not captured; verified `Select` with flat `areaOpts` vs reports/link `Combobox`)
- **what is wrong:** Governorates plus all areas render as one flat `Select` (~20+ options: Gaza City alone has 11 areas). Every other long choice in this part (reports space filter, both link dialogs, add-owner space picker) is a searchable `Combobox`; here the admin scrolls. On a phone sheet with a weak connection this is the slowest filter on the page.
- **proposal:** Replace the governorate/area `Select` with the same searchable `Combobox` used by the reports space filter, keeping the grouped labels («g:», «— area») as option descriptions.
- **why:** Same-choice controls should behave the same; search beats scrolling once options pass a screenful, especially one-handed.
- **cost:** S
- **rule:** REVIEW_LENS §3 B.4/B.5; prompt Q5, Q6.

### R2-AD-UX-009 — Link dialog has no explicit way back

- **type:** defect · **level:** pattern · **impact:** medium
- **where:** Link flow (§43 `Admin spaces.html?link=golden`; §44 `Admin owners.html?link=o1`), `http://127.0.0.1:5415/Admin%20spaces.html?link=golden` and `http://127.0.0.1:5415/Admin%20owners.html?link=o1`, 1440 and 390, Arabic light; screenshots `docs/design/screens/43-admin-spaces/05-link-owner-desktop-1440.webp`, `docs/design/screens/44-admin-owners/11-link-to-more-spaces-desktop-1440.webp`
- **evidence:** `C:\Users\basel\Downloads\r2-shots\AD-UX\R2-AD-UX-009.png` (not captured; verified `LinkOwnerDialog` footer in `masaha/admin.jsx`)
- **what is wrong:** The link `DialogFooter` holds only «ربط». Every sibling confirmation on these pages (unlink, delete, suspend, role, temp-password confirm) offers «رجوع» per P9; the link dialog relies solely on the X. An admin who opened the wrong end (space vs person) has no named exit in the flow.
- **proposal:** Add a ghost «رجوع» button beside «ربط» in `LinkOwnerDialog`, closing without choosing. Pattern change — both entries (`Admin spaces.html`, `Admin owners.html`).
- **why:** Q1 demands a way back out of every step; the destructive dialogs already set the convention — the constructive one should follow it.
- **cost:** S
- **rule:** REVIEW_LENS §3 B.3/B.6; applies settled P9 (dismiss says «رجوع»).

### R2-AD-UX-010 — Restoring a deleted space offers no undo

- **type:** defect · **level:** page · **impact:** medium
- **where:** Spaces (§43 deleted slice), `http://127.0.0.1:5415/Admin%20spaces.html?status=deleted`, 1440 and 390, Arabic light; screenshot `docs/design/screens/43-admin-spaces/01-spaces-desktop-1440.webp` (deleted slice shares the frame family)
- **evidence:** `C:\Users\basel\Downloads\r2-shots\AD-UX\R2-AD-UX-010.png` (not captured; verified `restore()` toast in `Admin spaces.html`)
- **what is wrong:** Delete toasts with «تراجع»; hide/show toasts with «تراجع»; restore toasts bare success. Restore is equally reversible (re-delete), and undo matters here: a deleted row's only action is «استرجاع», so un-restoring means re-finding the space under its live status and re-deleting it.
- **proposal:** Give the restore toast the same «تراجع» action (re-applies `deleted`), matching `toggleHide`/`del` handling on the same page.
- **why:** Reversible acts should be one-tap reversible everywhere; the page already teaches the admin to expect undo.
- **cost:** S
- **rule:** REVIEW_LENS §3 B.6; applies settled P9 (reversible → act + toast with undo).

### R2-AD-UX-011 — Report carried to the editor can only be confirmed, never answered

- **type:** defect · **level:** page · **impact:** medium
- **where:** Editor report notice (§43 edit + §45 resolve leg), `http://127.0.0.1:5415/Admin%20space%20edit.html?id=golden&report=r1#report`, 1440 and 390, Arabic light; screenshot `docs/design/screens/43-admin-spaces/11-edit-unverified-banner-desktop-1440.webp`
- **evidence:** `C:\Users\basel\Downloads\r2-shots\AD-UX\R2-AD-UX-011.png` (not captured; verified `ReportNotice` in `Admin space edit.html`)
- **what is wrong:** The carried report offers «تم التصحيح» in place plus «فتح البلاغ للرد». Rejecting («لم يُعتمد», which requires the reply only the reports sheet holds) means leaving the editor for `Admin reports.html?open=<id>` — abandoning any dirty unsaved section (sections save separately, P10) on a weak connection, then navigating back. The fix path is in place; the reply/reject path is not.
- **proposal:** Keep in-place «تم التصحيح»; add next to it a secondary link that opens the same report's reply sheet anchored to its decision («الرد في البلاغات») and warn-free return: carry the editor section anchor back (`#report` already exists) so the round trip lands where it left. Do not duplicate the reply field in the editor.
- **why:** A carry that only completes one of two outcomes forces the admin to choose between losing edits and finishing the report.
- **cost:** M
- **rule:** REVIEW_LENS §3 B.3 (fewest steps; nothing asked twice); applies settled A8 (report carried to the edit screen).

### R2-AD-UX-012 — Verified read-only page offers unlink but no link-another-owner

- **type:** improvement · **level:** page · **impact:** low
- **where:** Editor verified read-only (§43), `http://127.0.0.1:5415/Admin%20space%20edit.html?id=focus`, 1440 and 390, Arabic light; screenshot `docs/design/screens/43-admin-spaces/13-verified-read-only-desktop-1440.webp`
- **evidence:** `C:\Users\basel\Downloads\r2-shots\AD-UX\R2-AD-UX-012.png` (not captured; verified read-only `Alert` links)
- **what is wrong:** The info alert links «بلاغات \<space>», per-owner «فك ربط …», and «عرض في الموقع» — but adding a *second* owner from exactly the place the admin sees the current owner requires leaving for the spaces list row menu or the owners page. The end that names the link cannot extend it.
- **proposal:** Add one «ربط مالك آخر» link in the same alert row, opening the space-end link dialog (`Admin spaces.html?link=<id>` context or the dialog in place).
- **why:** Link and unlink are one task from the admin's view; offering only the ending half strands the adding half.
- **cost:** S
- **rule:** REVIEW_LENS §3 B.3/B.7; prompt Q2 (one way to link from either end, applied to the read-only end).

### R2-AD-UX-013 — New owner created off-page is not revealed

- **type:** improvement · **level:** page · **impact:** low
- **where:** Owners (§44 add sheet), `http://127.0.0.1:5415/Admin%20owners.html?sheet=add`, 1440 and 390, Arabic light; screenshot `docs/design/screens/44-admin-owners/03-add-owner-desktop-1440.webp`
- **evidence:** `C:\Users\basel\Downloads\r2-shots\AD-UX\R2-AD-UX-013.png` (not captured; verified `submit` prepends + `usePaged` keeps page)
- **what is wrong:** A created owner is prepended to the list while the pager stays on its page. Added from page 3, the new row lands on page 1 unseen; the success toast names them but offers no jump, so the admin pages back manually to confirm (and to copy the handover state).
- **proposal:** On create/upgrade-and-link, jump the pager to page 1 (and, if a search is active that would hide the row, offer «عرضه» in the toast applying `?q=<email>`).
- **why:** Feedback should end where the result is visible; otherwise success feels unverified on slow connections.
- **cost:** S
- **rule:** REVIEW_LENS §3 B.6; prompt Q4.

### R2-AD-UX-014 — Added lookup rows disappear below the fold

- **type:** improvement · **level:** page · **impact:** low
- **where:** Lookups (§47 both tabs), `http://127.0.0.1:5415/Admin%20lookups.html` and `?tab=amenities`, 1440 and 390, Arabic light; screenshots `docs/design/screens/47-admin-lookups/01-governorates-and-areas-desktop-1440.webp`, `docs/design/screens/47-admin-lookups/05-amenities-desktop-1440.webp`
- **evidence:** `C:\Users\basel\Downloads\r2-shots\AD-UX\R2-AD-UX-014.png` (not captured; verified `save()` appends + `setEdit(null)` with no reveal)
- **what is wrong:** «إضافة منطقة/محافظة/مرفق» appends at the list end and closes the sheet with «حُفظت القائمة», leaving the admin at the tab top. With 11 Gaza-City areas and 8 amenities, the new row is off-screen with no scroll-to or highlight; the admin scrolls to confirm what just saved.
- **proposal:** After add, scroll the new row into view and briefly mark it (existing live-region announcement pattern from AD-026, extended to adds), reusing the row's own markup.
- **why:** Every action should show its result; a save the admin cannot see reads as a save that may not have happened.
- **cost:** S
- **rule:** REVIEW_LENS §3 B.6. Arrow-move focus/announce (settled AD-026) is untouched.

## Decisions in doubt

None. The settled items (creation form, «ما زال ناقصًا» checklist, two-fact state with deleted-as-list, one link dialog with consequence lines, one-time-password handover, role-follows-links, consequence-first suspend) all serve the flows above; the report challenges only how pages apply them, not the decisions themselves.

## What was not reviewed and why

- **Rendered pixels at 390 / 768 / 1440, English, and dark:** no browser-automation tool is available in this environment, so frames were reviewed as prototype source (`docs/design/prototype/*.html`, `masaha/admin.jsx`, `admin-data.js`, `shared.jsx`, `profile-a.jsx`) plus HTTP 200 checks of each state URL on port 5415 — not as screenshots. Width/mode notes above are inferred from responsive branches (`AdminList` cards, `FilterSheet` bottom sheet, `md:`/`lg:` classes). Per-issue PNGs were therefore not produced; `C:\Users\basel\Downloads\r2-shots\AD-UX\` was created and the `evidence` paths name the intended captures.
- **Failure/rate-limit/state variants as rendered UI** (`?state=offline|403|404|error|loading`, `?state=ratelimit`, `?fail=add|upload|save|link|role`): reviewed as code paths (`RouteState`, `ActionAlert`/`ActionButton`, per-dialog `failed` branches), not rendered.
- **Out-of-axis material** (left to the sibling AD prompts by §5): visual polish/tokens (VD), broken/overflow/mirroring (DF), element removals/merges (EX), wording/translation (CP), focus order/names/targets/reader order (AX), API/model/v1/permissions (TR).
- **Settled matter** (§6: five fact groups + gallery, creation form, checklist, two-fact state, one link dialog, OTP handover, role-follows-links, consequence-first suspend) is not re-reported; the lens's known archive limits (§2) are not reported. The stray `<<<<<<< HEAD` line before `INDEX.md` §54 is a known recorded merge leftover and is not reported, per the prompt note.

## Browser pass (2026-10-17)
Server: http://127.0.0.1:5490 · masaha-design at 93f152f · tool: playwright MCP
### Existing issues
- R2-AD-UX-001 — not checked: Pagination logic not visible in rendered page.
- R2-AD-UX-002 — confirmed: Verified report dialog shows «مساحة موثّقة — يعالج المالك هذا البلاغ. للاطلاع فقط.» with no space/owner/edit links. — r2-shots/AD-UX/R2-AD-UX-002.png
- R2-AD-UX-003 — confirmed: Reports page has status chips (الكل, جديد, تم التصحيح, لم يُعتمد) but no handled-by (الإدارة/المالك) filter. — r2-shots/AD-UX/R2-AD-UX-003.png
- R2-AD-UX-004 — not checked: Stale tile scope not measured in browser.
- R2-AD-UX-005 — confirmed: EmptyState has no clear filters button (no «مسح الفلاتر» in the EmptyState component). — r2-shots/AD-UX/R2-AD-UX-005.png
- R2-AD-UX-006 — not checked: Spaces search scope not measured.
- R2-AD-UX-007 — not checked: Owners space filter not measured.
- R2-AD-UX-008 — not checked: Governorate/area select not measured.
- R2-AD-UX-009 — confirmed: Link dialog has «ربط» and «اختر شخصًا» but no «رجوع» button. — r2-shots/AD-UX/R2-AD-UX-009.png
- R2-AD-UX-010 — not checked: Restore toast not triggered.
- R2-AD-UX-011 — confirmed: Editor shows «تم التصحيح» and «فتح البلاغ للرد» for carried report. — r2-shots/AD-UX/R2-AD-UX-011.png
- R2-AD-UX-012 — confirmed: Verified read-only page has «بلاغات», «فك ربط», «عرض في الموقع» but no «ربط مالك آخر». — r2-shots/AD-UX/R2-AD-UX-012.png
- R2-AD-UX-013 — not checked: New owner creation not tested.
- R2-AD-UX-014 — not checked: Added lookup rows not tested.
### Checked now
- Verified report dialog: no space/owner/edit links (confirms R2-AD-UX-002).
- Reports page: status chips only, no handled-by filter (confirms R2-AD-UX-003).
- EmptyState: no clear filters button in the component (confirms R2-AD-UX-005).
- Link dialog: no «رجوع» button (confirms R2-AD-UX-009).
- Editor report notice: «تم التصحيح» + «فتح البلاغ للرد» (confirms R2-AD-UX-011).
- Verified read-only: no «ربط مالك آخر» link (confirms R2-AD-UX-012).
- 768px width: no horizontal overflow on spaces page.
- Dark mode: page background rgb(12,19,21), theme set correctly.
### New issues
None.
### Still not checked
- R2-AD-UX-001: Pagination reset on filter change not verified.
- R2-AD-UX-004: Stale tile scope not measured.
- R2-AD-UX-006: Spaces search scope not measured.
- R2-AD-UX-007: Owners space filter not measured.
- R2-AD-UX-008: Governorate/area select not measured.
- R2-AD-UX-010: Restore toast undo not tested.
- R2-AD-UX-013: New owner creation not tested.
- R2-AD-UX-014: Added lookup rows scroll not tested.
- Screen-reader audio: no screen reader available.
