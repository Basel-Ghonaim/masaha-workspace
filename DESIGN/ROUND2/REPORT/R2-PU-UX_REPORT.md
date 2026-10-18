# R2-PU-UX — Round 2 review: the public site · Experience and flow

## 1. Revisions

- `git rev-parse HEAD`: `34a6c59aab049e8f2992b29b88c8a700b926ddba`
- `git rev-parse origin/main`: `34a6c59aab049e8f2992b29b88c8a700b926ddba`
- HEAD equals `origin/main`. Prototype served from `C:\Users\basel\masaha-design` on `http://127.0.0.1:5408` (all key states below returned 200). Read-only; nothing edited, committed, or moved in that directory.

## 2. Verdict

The find-a-space flow is short and recoverable, but near-me behaves as two controls, visitor actions assume success, and filter recovery costs too many steps.

## 3. Five most important points

1. «الأقرب إليّ» OFF wipes the location on Home but keeps it in the Directory — one control, two meanings (R2-PU-UX-001).
2. Saving a space and filing a report assume success: no failure or 429 path, and the report discards typed input (R2-PU-UX-002).
3. A filed report ends in a dead end: no way onward to «بلاغاتي», where the reply lands (R2-PU-UX-003).
4. Home search drops `lang`/`theme`: an English or dark-mode visitor lands on an Arabic light Directory (R2-PU-UX-005).
5. Removing one phone filter takes four taps and the count line hides non-place filters (R2-PU-UX-006).

## 4. Issues

Note on evidence: this runner has no browser or screenshot tool, so no new cropped PNGs were taken (see §6). `where.screenshot` cites the board's authoritative capture for the frame; `evidence` reuses that pre-existing capture path as the visual anchor. All findings were verified against the served markup and component logic (`Home.html`, `Directory.html`, `Space details.html`, `About.html`, `Error.html`, `masaha/shared.jsx`, `masaha/location.jsx`, `masaha/map.jsx`, `masaha/space-parts.jsx`, `masaha/i18n.js`).

### R2-PU-UX-001 — Near-me OFF means two different things on Home and the Directory

- **type:** defect · **level:** pattern · **impact:** high
- **where:** frame "Location allowed · «الأقرب إليك» — phone 390", `http://127.0.0.1:5408/Home.html?loc=granted`, 390, Arabic light; and frame "Location allowed · sorted «الأقرب إليّ» — phone 390", `http://127.0.0.1:5408/Directory.html?loc=granted`, 390, Arabic light. Screenshot: `docs/design/screens/02-home-states/04-location-allowed-phone-390.webp` and `docs/design/screens/03-directory-views-states/06-location-allowed-sorted-phone-390.webp`.
- **evidence:** pre-existing board captures above (no new crop taken).
- **what is wrong:** the same control with the same state line does opposite things. On Home, `NearMeButton` gets no `onToggle`, so pressing it while ON calls `near.clear()` — and the state line's «إيقاف الترتيب حسب المسافة» link also calls `clear` (`stop = onStop || clear`, no `onStop` passed). On the Directory, OFF only sets `sort` back to `updated`; the location is kept, distances stay visible, and «مسح موقعي» is a separate link. A visitor who learns "off keeps my distances" in the Directory loses their location (permission prompt + wait to re-grant) on Home, under a label that promises only to stop sorting.
- **proposal:** make Home behave like the Directory: OFF ends distance sorting but keeps the location (Home cards already render `km` when coords exist); show «مسح موقعي» as the only wipe, via the existing `stop !== clear` branch. Changes `Home.html` only in wiring (`onStop`, `onToggle`); no new components.
- **why it is better:** one control, one mental model across the two pages of a single flow; accidental taps stop costing a location re-grant.
- **cost:** S
- **rule:** applies `DECISIONS_PUBLIC.md` U2 ("turning it off says «إيقاف الترتيب حسب المسافة»") and `REVIEW_LENS.md` §3 B.3/B.4.

### R2-PU-UX-002 — Visitor saves and the report submit assume success

- **type:** defect · **level:** pattern · **impact:** medium
- **where:** frames "Directory · striking cards, signed in — phone 390", `http://127.0.0.1:5408/Directory.html?loc=none&auth=1`, 390, Arabic light; "Focus Hub · verified … — phone 390", `http://127.0.0.1:5408/Space%20details.html?id=focus&loc=none&auth=1`, 390, Arabic light; "Report · unverified space, read by the team — phone 390", `http://127.0.0.1:5408/Space%20details.html?id=golden&loc=none&auth=1&dialog=report`, 390, Arabic light. Screenshots: `docs/design/screens/01-flow/02-2-directory-list.webp`, `docs/design/screens/04-space-details-variants/02-focus-hub-verified-fresh-5-photos-location-allowed-phone-390.webp`, `docs/design/screens/04-space-details-variants/16-signed-in-report-wrong-info-phone-390.webp`.
- **evidence:** pre-existing board captures above (no new crop taken).
- **what is wrong:** three visitor actions have no failure or 429 path, against P8 ("every action … or it failed", "the 429 warning everywhere"). Card hearts (`useFavourites.toggle`) and the space-page heart (`toggleFav`) always toast success — only the post-sign-in return path handles `?fail=fav`. `ReportDialog.submit` always succeeds and clears `topic`/`msg` before any result, so on a weak connection a typed report is lost with a success toast. Nothing keeps the input, nothing offers a retry.
- **proposal:** apply the settled P8 treatment, no new components: hearts (Home cards, Directory cards, space-page heart — `Home.html`, `Directory.html` via `shared.jsx`, `Space details.html`) fail to an error toast with «إعادة المحاولة» that re-applies the toggle, honouring `?fail=` and `?state=ratelimit`; `ReportDialog` fails inline (`ActionAlert`, dialog stays open, input kept) with the 429 line where applicable.
- **why it is better:** on Gaza connections the failure path is the common path; the visitor keeps their work and has exactly one next step instead of a lie followed by confusion.
- **cost:** S
- **rule:** applies `DECISIONS_SHARED.md` P8; `REVIEW_LENS.md` §3 B.6.

### R2-PU-UX-003 — After filing a report there is no way onward to «بلاغاتي»

- **type:** improvement · **level:** component · **impact:** medium
- **where:** frame "Report · unverified space, read by the team — phone 390", `http://127.0.0.1:5408/Space%20details.html?id=golden&loc=none&auth=1&dialog=report`, 390, Arabic light (also verified variant `?id=focus`). Screenshot: `docs/design/screens/04-space-details-variants/16-signed-in-report-wrong-info-phone-390.webp`.
- **evidence:** pre-existing board capture above (no new crop taken).
- **what is wrong:** U10 promises the reply lands in «بلاغاتي» and the dialog says so, but the success toast (`toast.success(...)` in `ReportDialog.submit`) offers no action. After the dialog closes, reaching My reports means opening the avatar account menu — two or more steps the visitor was never shown. The loop the design opens ("you'll find the reply in My reports") has no bridge.
- **proposal:** give the report success toast an action «عرض بلاغاتي» linking `Reports.html` (design-system `toast` action, as the favourite-failure toast already does with «إعادة المحاولة»). Changes `Space details.html` only.
- **why it is better:** the visitor learns where replies live by going there once, instead of hunting the account menu later.
- **cost:** S
- **rule:** applies `DECISIONS_PUBLIC.md` U10; `REVIEW_LENS.md` §3 B.3/B.6.

### R2-PU-UX-004 — Space-page favourite toggle skips the P9 undo that card hearts have

- **type:** defect · **level:** component · **impact:** low
- **where:** frame "Focus Hub · verified … — phone 390", `http://127.0.0.1:5408/Space%20details.html?id=focus&loc=none&auth=1&fav=1`, 390, Arabic light. Screenshot: `docs/design/screens/14-account-signed-in-header/04-space-details-signed-in-saved-phone-390.webp`.
- **evidence:** pre-existing board capture above (no new crop taken).
- **what is wrong:** card hearts toast with «تراجع» (P9: reversible, affects no one else → act at once + undo). The space-page heart (`toggleFav`) toasts plain «أُضيفت إلى المفضلة» / «أُزيلت من المفضلة» with no undo and no space name. Same action, same user, two feedback contracts; an accidental un-save beside the h1 has no one-tap recovery.
- **proposal:** use the card hearts' toast-with-«تراجع» (and the saved line naming the space) for the space-page toggle. Changes `Space details.html` only.
- **why it is better:** consistent, cheapest recovery for a thumb slip next to the title.
- **cost:** S
- **rule:** applies `DECISIONS_SHARED.md` P9; `REVIEW_LENS.md` §3 B.4/B.6.

### R2-PU-UX-005 — Home search drops language and theme mid-flow

- **type:** defect · **level:** page · **impact:** medium
- **where:** frame "1 · Home", `http://127.0.0.1:5408/Home.html?loc=none&lang=en&theme=dark` submitted to `Directory.html?q=…`, 390, English dark (structural; verified in code, all widths). Screenshot: `docs/design/screens/01-flow/01-1-home.webp`.
- **evidence:** pre-existing board capture above (no new crop taken).
- **what is wrong:** `i18n.js` carries `lang`/`theme` only on anchor clicks; Home's search is a GET `form action="Directory.html"` with no hidden `lang`/`theme` fields. An English or dark-mode visitor who searches lands on an Arabic light Directory — the flow resets two modes at the exact moment of progress. Every other step in the flow (area cards, header, footer, back-link via `sessionStorage`, `switchLang`) preserves them.
- **proposal:** carry `lang`/`theme` through the Home search (hidden inputs or submit-time patch, reusing `carryParams`). Changes `Home.html` only.
- **why it is better:** the visitor's language and theme survive their first and most common action; English and dark-mode users stop being bounced back to defaults.
- **cost:** S
- **rule:** `REVIEW_LENS.md` §3 B.7/B.8.

### R2-PU-UX-006 — On the phone, removing one filter costs four taps and active filters are invisible

- **type:** improvement · **level:** component · **impact:** medium
- **where:** frame "Directory · place and price filters — desktop 1440" (behaviour identical below `lg`), `http://127.0.0.1:5408/Directory.html?loc=none&area=nasr,rimal&period=day&priceMax=20`, 390, Arabic light. Screenshot: `docs/design/screens/01-flow/02-2-directory-list.webp` (phone list frame).
- **evidence:** pre-existing board capture above (no new crop taken).
- **what is wrong:** below `lg` the only way to drop one of several active filters is: open «الفلاتر» → find the field → uncheck → «عرض N نتيجة». The toolbar shows only the count badge, and the result line names only place (`placeLine`) — price range, «متاحة الآن», «موثّقة», «أخرى» vanish from view, so the visitor must open the sheet just to recall what is filtering. The desktop sidebar does not have this problem; the phone flow does.
- **proposal:** add an active-filter chips row under the toolbar (one chip per active filter, one tap to remove; «مسح الكل» at its end), reusing `ToggleGroup` chips/`Badge` and the existing `clear`/`set` wiring. Phone-first; harmless above `lg`. Changes `Directory.html` only; leaves the P5 bar and sheet structure untouched.
- **why it is better:** the two most common filter adjustments (see what is on, drop one) become zero- and one-tap instead of a four-tap sheet round-trip.
- **cost:** M
- **rule:** `REVIEW_LENS.md` §3 B.3/B.5/B.6 (P5 structure unchanged).

### R2-PU-UX-007 — An invalid price range filters nothing but never says so; an inverted range needs retyping

- **type:** improvement · **level:** component · **impact:** low
- **where:** frame "Directory — list" with range error, `http://127.0.0.1:5408/Directory.html?loc=none&priceMin=50&priceMax=20`, 390, Arabic light. Screenshot: `docs/design/screens/01-flow/02-2-directory-list.webp`.
- **evidence:** pre-existing board capture above (no new crop taken).
- **what is wrong:** when the range is invalid (`priceRange.ok === false`), `inRange` returns true — results silently go unfiltered while the field error («أقل من الحد الأدنى») reads as if a filter applied. For the listed inverted-range state the fix is obvious to the visitor (swap the bounds) but requires retyping both fields on a phone keyboard.
- **proposal:** on the order-error case only, offer a one-tap «تبديل الحدّين» action on the max field that swaps min/max and re-applies. Changes `Directory.html` (`PriceField`) only.
- **why it is better:** the most common range mistake recovers in one tap instead of two error-prone retypes, and results match what the error implies.
- **cost:** S
- **rule:** `REVIEW_LENS.md` §3 B.6.

### R2-PU-UX-008 — From the bottom of long public pages there is no way to the Directory

- **type:** improvement · **level:** pattern · **impact:** low
- **where:** frames "4 · Space details", `http://127.0.0.1:5408/Space%20details.html?id=focus&loc=none`, 390, Arabic light; "About «عن مساحة» — phone 390", `http://127.0.0.1:5408/About.html`, 390, Arabic light. Screenshots: `docs/design/screens/01-flow/04-4-space-details.webp`, `docs/design/screens/10-about-error-pages/02-about-phone-390.webp`.
- **evidence:** pre-existing board captures above (no new crop taken).
- **what is wrong:** `SiteFooter` (shared by all five pages) links only «عن مساحة» and «تواصل معنا», and the header is not sticky. At the bottom of the space page (after report) or About (after owners), the only route back to browsing is scrolling to the top («العودة إلى المساحات» / header nav). The space page is exactly where "see more like this" intent peaks.
- **proposal:** add «تصفّح المساحات» (`Directory.html`) to `SiteFooter`. Changes `masaha/shared.jsx` `SiteFooter`, effective on `Home.html`, `Directory.html`, `Space details.html`, `About.html`, `Error.html`.
- **why it is better:** every long page ends with its natural next step; no scroll-back to navigate onward.
- **cost:** S
- **rule:** `REVIEW_LENS.md` §3 B.7.

## 5. Decisions in doubt

- **D1 — PU-020 / U8: the two highest-intent phone actions live at the bottom of the longest page.** «الاتجاهات» appears once, in the Location section header, and «الإبلاغ عن معلومة» once, after Contact — both a full scroll past prices, hours, amenities and about on the phone, while the fixed bottom bar repeats only WhatsApp and Call. A visitor standing outside a space (navigate now) or spotting a wrong hour at the top (report now) pays the longest scroll at the moment of highest intent. If the bar must stay two actions, consider whether «الاتجاهات» belongs in it, or a report entry belongs in the top status card. Owner's call; raised as doubt, not defect, per U8/PU-020 settled status.
- **D2 — U12 (2026-10-12): priceless cards keep the budget filter blind.** The price filter stays as a budget, but with no price on any card the visitor cannot verify a `priceMax` shortlist without opening every space. If the card must stay priceless, consider whether the count line or the sheet footer should state the active budget ("within يوم ≤ 20 ₪") so the invisible filter stays legible. Owner's call; raised as doubt, not defect.

## 6. What was not reviewed and why

- **Pixel-level visual verification and cropped captures:** this runner exposes no browser or screenshot tool (no chromium/chrome/edge/playwright binaries; `WebFetch`-style fetching returns markup, not renders), so widths (390/768/1440), English (`?lang=en`) and dark (`?theme=dark`) were verified structurally — responsive classes, `i18n.js` carrying, `theme` handling — against the served HTML, not by looking at renders. No `<ID>.png` files were written to `C:\Users\basel\Downloads\r2-shots\PU-UX\` (directory confirmed present and left empty) rather than fabricating evidence. Per-issue screenshots cite the board's authoritative captures in `docs/design/screens/`.
- **Out-of-axis matters** (left to the sibling PU prompts by §5/§7 of the brief): visual polish/tokens (VD), broken/overflow/mirroring (DF — including the space-page toaster offset over the phone bottom bar, treated as overlap), element removals/merges (EX), wording/translation (CP), focus order/names/targets/SR order (AX), API/data-model/v1 feasibility, pagination expectations and location privacy (TR).
- **Settled matters** (lens §2b, `DECISIONS_SHARED.md` P1/P4–P9, `DECISIONS_PUBLIC.md` U1–U12/H2–H5/PU-013/014/025 and the 2026-10-12, 2026-10-13 amendments): default Strip set, one place filter, pin shapes, phone sheet, hand-pinning mechanics, card photo treatment, page order, per-audience prices, report routing, About contact section, offline retry — verified as applied, not re-reported (the `<<<<<<< HEAD` line before `INDEX.md` §54 was seen but is recorded already and was not reported, as instructed).
- **Account pages** (`Favorites.html`, `Reports.html`, `Settings.html`, sign-in cards): out of scope except the guest → sign-in → return toast leg, which was traced (`?dialog=signin|signin-report`, `?toast=welcomefav`, `?fail=fav`) and found continuous.
- **Server port:** the review server (PID recorded at run time) is stopped at the end of the session and `5408` re-checked; see tool log.

## Browser pass (2026-10-17)
Server: http://127.0.0.1:5490 · masaha-design at 93f152f · tool: playwright MCP
### Existing issues
- R2-PU-UX-001 — not checked: Near-me control on Home vs Directory not compared in browser.
- R2-PU-UX-002 — not checked: Visitor saves assume success (code-level, not triggered).
- R2-PU-UX-003 — not checked: Report success toast not triggered.
- R2-PU-UX-004 — not checked: Space-page favourite toggle undo not tested.
- R2-PU-UX-005 — confirmed: Home search form has no hidden `lang`/`theme` inputs — English/dark visitors land on Arabic light Directory. — r2-shots/PU-UX/R2-PU-UX-005.png
- R2-PU-UX-006 — confirmed: No active-filter chips row on Directory at 390; only count badge shown. — r2-shots/PU-UX/R2-PU-UX-006.png
- R2-PU-UX-007 — confirmed: Inverted price range (50>20) shows error but no «تبديل الحدّين» swap action. — r2-shots/PU-UX/R2-PU-UX-007.png
- R2-PU-UX-008 — confirmed: SiteFooter has only 2 links («عن مساحة», «تواصل معنا»); no «تصفّح المساحات». — r2-shots/PU-UX/R2-PU-UX-008.png
### Checked now
- Home search form: no hidden lang/theme inputs (confirms R2-PU-UX-005).
- Directory at 390: no active-filter chips (confirms R2-PU-UX-006).
- Price range error: error shown, no swap action (confirms R2-PU-UX-007).
- SiteFooter: 2 links only, no Directory link (confirms R2-PU-UX-008).
- Home near-me: «الأقرب إليّ» button + «إيقاف الترتيب حسب المسافة» link present.
- Space page: heart button aria-label «حفظ في المفضلة».
- 768px width: no horizontal overflow on Home.
- Dark mode: page background rgb(12,19,21), theme set correctly.
### New issues
None.
### Still not checked
- R2-PU-UX-001: Near-me OFF behavior not compared (Home vs Directory).
- R2-PU-UX-002: Visitor saves assume success (not triggered).
- R2-PU-UX-003: Report success toast not triggered.
- R2-PU-UX-004: Space-page favourite toggle undo not tested.
- Screen-reader audio: no screen reader available.
