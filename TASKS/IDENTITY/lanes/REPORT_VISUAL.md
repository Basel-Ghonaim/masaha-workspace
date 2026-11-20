# IDENTITY visual pass (T23): report

(Saved by the lead from the sub-agent's final message, 2026-11-12. The agent's scripts, results and raw shots are in
`lanes\scratch-v\`; the curated shots in `C:\Users\basel\Downloads\identity-prod-shots\`.)

I changed no file in any repository (`git status` in `C:\dev\masaha\app-design` is clean). I wrote no data: every API request went through CDP `Fetch`, every non-GET except sign-in and refresh would have been refused, and none was attempted (blocked list empty in every run). I did not run db:seed and printed no secret. I did not touch the lead's servers.

## Findings, most severe first

**F1. `primary-hover` paints warm instead of ink, so EC3 fails (the item's).**
- **Where:** every primary button hovered, at 1440, light and dark, in both languages: the sign-in submit, the desk's «تسجيل زيارة / Check in a visit», and the filled range ends of the calendar.
- **Expected:** light `#3c4147`, dark `#c7cbd0`.
- **Painted (screenshot pixel):** light `#463e40` (Δ +10/−3/−7), dark `#cfc9ca` (Δ +8/−2/−6).
- **Cause, measured in the page:**
  - Chrome treats the ink neutrals' hue as powerless when it converts hex to OKLCH. `oklch(from #1a1f25 l c h)` computes to `oklch(0.2369 0.0137 none)` and paints `#241c1e`.
  - So `color-mix(in oklch, var(--neutral-900), var(--neutral-50) 18%)` computes to `oklch(0.371743 0.0124857 none)`: the chroma is kept, the hue becomes 0, and the result is a reddish grey.
  - The same mix `in oklab` computes to exactly the token test's `#3c4147` / `#c7cbd0`. Proposal: mix in oklab (the lead decides).
- **Same mechanism on older classes, now on the ink ramp:**
  - Button `secondary` hover (`in_oklch`, already on main) computes to `#e8dcdf`.
  - `--overlay-scrim` (`in oklch`, already on main) paints `#8a8788` over white, where ink at 50 % would be `#86898b`. In dark it paints `#181417` over `#1a1f25`, where ink at 70 % would be `#11161b`.
- **Shots:** `25-hover-primary-light.png`, `25-hover-primary-dark.png`.

**F2. A lifted photo shows no edge at all (PhotosEdit). The item's C4 intent is not met; the mechanism is older.**
- **Where:** owner profile → «Manage photos», 1440, light and dark.
- **Lifted by the keyboard (Space):** the class `outline-spark` is present, but the computed outline is the ink ring (`solid 2px #1a1f25 offset 2px` light, `#f7fbff` dark), because `focus-visible:outline-ring` wins.
- **Lifted by a mouse drag:** the outline is `solid 2px #b55bb3` (dark `#d27ed0`) at offset 0.
- **Clipping, in both modes:** the outline is clipped completely by the tile's frame. The frame is a parent div with `overflow:hidden`, 1 px larger than the tile (frame 257×146, tile 255×144). Pixels 3 px outside the tile are the card's own ground (`#ffffff` / `#1a1f25`).
- **Older consequence:** a photo tile that simply has keyboard focus has its ring clipped too, so its focus is invisible.
- **Shots:** `29-photo-lifted-keyboard-light-en-1440.png`, `30-photo-lifted-mouse-light-en-1440.png`.
- **For contrast, the contacts work:** a contact lifted by the keyboard (Space on its handle, then Escape) shows the spark edge on the row and the ink ring on the handle, and Escape cancels the drag and leaves the sheet open. Shot: `28-contact-lifted-keyboard-light-en-1440.png`.

**F3. Site phone menu (SiteMenu), dark: the current page's entry looks the same as a hovered entry (the item's).**
- **Where:** 390, en, dark.
- **Values:** the current entry is `aria-[current=page]:bg-secondary`, which is `#2c3137`. Hovering another entry paints `#2c3137`. Under the pointer, the current entry keeps `#2c3137`.
- **Light is fine:** current `#ecf4fc`, hover `#dde5ed`.
- **Cause:** in dark, `hover` is n-800, which is also `secondary`.
- **Shot:** `42-hover-phone-menu-current-dark.png`.

**F4. LiveStatusControl, neutral tone, dark: no hover is seen (the item's).**
- **Where:** desk top bar, 1440, en. The state was made by response rewriting in the browser: a hand-set CLOSED.
- **Values:** rest is `bg-secondary` `#2c3137`; hovered is `#2c3137`.
- **The other tones change on hover:** neutral light goes `#ecf4fc` → `#dde5ed`; success goes `#ecfcef` → `#dde5ed` (dark `#001f0a` → `#2c3137`); warning goes `#fff5ea` → `#dde5ed` (dark `#261400` → `#2c3137`).
- **Observation:** on hover, the tone's tinted fill gives way to the neutral hover fill.
- **Shot:** `37-hover-live-status-neutral-dark.png`.

**F5. Finance › Occupancy (heatmap) scrolls sideways at 390 (older).**
- **Values:** `scrollWidth` is 426 in English and 395 in Arabic, against a `clientWidth` of 390. It holds in every 390 variant; 768 and 1440 are clean.
- **Cause, confirmed:**
  - The Heatmap's `<table class="sr-only">` is `position:absolute`, and a table ignores `width:1px`: its box is 390 / 359 px wide.
  - Its containing block lies outside the `overflow-x-auto` CardContent, so it escapes that scroller.
  - With the table set to `display:none`, the page is 390 wide again.
- **Shot:** `22-finance-heatmap-overflow-light-ar-390.png`.

**F6. axe violations (older).**
- **Map:** `aria-tooltip-name` (serious, 1 node, the Leaflet tooltip `role=tooltip`), at light-ar-390 and dark-en-1440.
- **`scrollable-region-focusable` at light-ar-390:** on the profile's photo thumbnail row (`.pb-1`) and on the heatmap's CardContent.
- **Colour contrast:** no colour-contrast violation on any screen.

**Not findings, recorded so they are not re-raised:**
- **Spark-button hits are chips by design.** The "no button with the spark" rule fires only on ToggleGroup chips that are on (`button[data-slot=toggle-group-item][role=radio]`, spark border on all four sides): List/Map, the desk's «غير محصّل», the check-in dialog's «صباحي», /me language and theme, and the admin reports filters. This is §5's "a chip that is on has its spark edge". If the lead agrees, the rule's wording could exempt chips.
- **Line tabs:** the desk's Now/Log line tabs hover by text colour only, by design.
- **Account menu:** an item highlighted by the keyboard and one under the pointer both use `hover` (`#dde5ed` / `#2c3137`).
- **Inputs:** an input draws its focus ring on its box (`[data-slot=input-group]`: `solid 2px` in the ring colour, border in the ring colour). That is why my probe reported "outline none" on the input itself.

## Clean on every load checked
- **No Sea:** 0 hits across every element and every `::before`/`::after`, on colour, background, the four borders, outline, fill, stroke, shadow, text-decoration, caret and gradients; 0 in data-SVG `src`; 0 in the text of any stylesheet, including leaflet.css.
- **Spark text:** 0 elements with spark-coloured text.
- **Painted contrast:** 0 failures (between 5 and 205 texts checked per variant; the self-test caught a 1.23:1 pair). Text over photos («+2», «View all photos (7)») measured 6.23 and 15.79 at the 10th percentile; that ground is the placeholder, because the photo files return 404.
- **Overflow:** none except F5.
- **Status colours:** the tokens are exact (light `#be222a #137d41 #b27406 #1f6cb0`, dark `#fc6e68 #63b77c #d6912b #64a6e9`); every sampled element equals its token: `bg/border/text` for destructive, success and info, and the `-subtle` and `-foreground` pairs (warning only as `-subtle`).
- **Console:** no app error or exception on any screen; the only noise is environmental.
- **Focus ring after three Tabs:** visible, `solid 2px`, in the ring colour (`#1a1f25` light, `#f7fbff` dark), offset 2, in every context: the page (header logo link and nav); a card (a directory card link, its favourite button, the next card); the sidebar («Front desk»); a Sheet (the phone menu, both drawers, the contacts sheet on the input box, the date picker inside the filters sheet); a dialog (the check-in dialog's chip, the void dialog's «إلغاء الدفعة»). The one exception is the photo tiles (F2).
- **Hover vs selected (1440, en; verdicts from screenshot pixels):** the neutral hover reads `#dde5ed` light / `#2c3137` dark on the desk row, a sidebar item beside the current one (owner and admin), the outline buttons, the menu item, the chip off, the space card, the contact tile and the admin spaces row; the ink wash over muted reads `#d7dee6` / `#3d4147` on the subscription choice, the pill tabs (finance and hours), FilterTag's remove, today in the calendar and the sort header; selected stays `#ffe3fd` / `#471f46` under the pointer and differs from the hover on the sidebar's current item, a chip that is on, and a range day; the sidebar's spark bar is 3 px of `#b55bb3` / `#d27ed0` at the inline start (LTR x 12–14, RTL x 1425–1427); a chip that is on has its spark edge; the checked segment and the active pill tab are the card fill and are kept. No production table sorts, so the sort header was measured on the showcase DataTable.

## Executor checks
- **EC3:** dark `accent` painted `#471f46`, exact; light `#ffe3fd`. `hover-on-muted` over muted: light `#d7dee6` against `#d7dfe6`, dark `#3d4147` against `#3c4147`, both within 1/255 ✓. `primary-hover` ✗: light `#463e40` (want `#3c4147`), dark `#cfc9ca` (want `#c7cbd0`) — F1.
- **EC6:** `h-10` 109.53 × 40 ✓; `h-9` 98.58 × 36 ✓; the mark `size-9` 36 × 36 ✓; `transform: none` on every logo and every ancestor ✓; the header link names «مساحة» / "Masaha" ✓; the admin's header reads «مساحة · إدارة المنصة» / "Masaha · Platform admin" once, both logos `aria-hidden` ✓; in the phone menu's drawer the logo sits at the inline start, gap 0, in both directions (Arabic right edge 374 = 390 − 16; English left edge 16) ✓; the component's mark at 64 px against `masaha-mark-berry.svg` at 64 px on white: 0 of 4096 pixels differ by more than 8/255 ✓.
- **EC8:** `/favicon.svg` 200 `image/svg+xml`; `/favicon.ico` 200 `image/x-icon`; `/apple-touch-icon.png` 200 `image/png` ✓; the links: ico (`sizes="16x16 32x32 48x48"`), svg, apple-touch, two `theme-color` metas; on load Chrome requested `/favicon.svg` (type Other), so the tab takes the SVG; under emulated `prefers-color-scheme` light paints `#1a1f25` + `#b55bb3`, dark `#f7fbff` + `#d27ed0` ✓.
- **EC9:** `apple-touch-icon.png` 180 × 180, opaque white, full bleed (margins 22/12/22/11); `favicon.ico` three 32-bit PNG entries 16, 32, 48, the 16 a white rounded tile with transparent corners, reading as the ة with its two dots; the Google 120 white, margins 24/18/24/18, 0 ink pixels outside a round crop ✓ (`ec9-rasters.png`).
- **EC11:** axe light-ar-390 and dark-en-1440 on every screen (drawers, signed-in phone menu, void at 390, date picker at 390: light only; guest phone menu light-ar-390 and dark-en-390; loading: none); violations only those in F6. An early colour-contrast hit on the space page was the script's own (it hid text while colours transitioned back); clean after the fix.
- **EC13:** the prototype (berry its default, 1440) equals production on the primary at rest `#1a1f25` / `#f7fbff`; the primary hover `#463e40` / `#d0c9ca` (the same hue loss); the sidebar's current `#ffe3fd` / `#471f46` and its bar `#b55bb3` / `#d27ed0` (an inset shadow there, a `::before` here); a chip on `#ffe3fd` / `#471f46` with a `#b55bb3` / `#d27ed0` border; the hovers `#dde5ed` / `#2c3137`. Pages: Desk, Directory, Owner overview, Admin spaces.
- **EC14:** at 360, guest and signed in, ar/en, light/dark: `scrollWidth` 360, no overlap ✓ (ar: menu 304–344, logo 186–296, language 16–121 / 68–173 signed in, avatar 16–60; en: menu 16–56, logo 64–174, language 252–344 / 200–292, avatar 300–344).

## Coverage
- **Full matrix** (390, 768, 1440 × ar/en × light/dark): Home, the directory (`?period=MONTH&open=1&verified=1`), the map (a mark selected), a space's page (the gallery made seven photos, contacts, today's hours), sign in, register, forgot, the 404, the desk (the owner's rail at 768), the owner's overview, the owner's profile («+2»), Finance income and heatmap, /me, favourites, the admin's overview (rail at 768), spaces, a space's editor.
- **Subsets:** the check-in dialog 5 variants; payments 3; the void dialog 4 at 1440 + light-ar-390, dark-ar-390, dark-en-768; the date picker on a range 1440 dark en and ar (+ inside the filters sheet); the contacts sheet 4; the owner's and admin's drawers 4 each at 390; the phone menu guest 8 (390 and 360), signed in 4; loading (directory request held) 4; admin reports with a FilterTag 2. Hover tests 1440, en, light and dark.
- **Not covered:** 390 was a narrow desktop window (fine pointer), so the `pointer-coarse` sizes were not exercised; the photos return 404 in this folder's API storage, so photo grounds are placeholders; no production table sorts (the showcase's measured); the desk's three present people, «+N» and the live-status tones were made by rewriting responses (`Fetch`), not by data; the script's computed "painted" composite was unreliable on rows and pills, so every hover verdict uses screenshot pixels.

## Environment notes (not the item's)
- The demo photo files return 404: `/api/v1/files/spaces/*/card.webp`.
- Google's sign-in button returns 403 and its stylesheet fails CORS (`accounts.google.com/gsi`): `localhost:5323` is not an allowed origin.

## Processes and grants
- Chrome, each stopped by its PID, 0 `cdp-profile` processes left after each: 29512, 31616, 11744, 22428, 23196, 20964, 28676, 21648, 22040, 4228.
- `http.server`: PID 30932 on port 58713, stopped by its PID; the port free afterwards.
- Grants: 10 in `heavy-grants.log` (11:55–12:42 UTC), all immediate, no WAIT.
- Sessions: `/auth/refresh` called 0 times (client-side navigation after one sign-in per run; preferences switched by the storage event).

## Screenshots
37 curated, in `C:\Users\basel\Downloads\identity-prod-shots\`: 01-home-light-ar-390, 01-home-dark-en-1440,
02-directory-dark-en-1440, 03-map-selected-dark-en-1440, 04-space-page-light-ar-390, 05-sign-in-light-ar-390,
08-404-dark-en-1440, 09-phone-menu-light-ar-390, 09-phone-menu-light-en-390, 10-header-360-guest-ar,
11-loading-light-ar-390, 12-desk-dark-en-1440, 13-owner-rail-light-ar-768, 14-check-in-dialog-light-ar-390,
17-date-picker-range-light-ar-390, 18-void-payment-dialog-light-ar-390, 19-owner-profile-photos-plus-n-light-en-768,
21-finance-charts-dark-en-1440, 22-finance-heatmap-overflow-light-ar-390, 25-hover-primary-light,
25-hover-primary-dark, 26-hover-calendar-today-dark, 28-contact-lifted-keyboard-light-en-1440,
29-photo-lifted-keyboard-light-en-1440, 30-photo-lifted-mouse-light-en-1440, 32-owner-drawer-light-ar-390,
34-hover-sidebar-dark, 37-hover-live-status-neutral-dark, 42-hover-phone-menu-current-dark,
43-header-360-signed-in-en-dark, 45-admin-rail-dark-en-768, 47-admin-space-editor-light-ar-390,
48-ec6-mark-64-component-vs-file, 49-admin-drawer-dark-en-390, 52-prototype-desk-dark-en-1440, ec8-favicon-svg-dark,
ec9-rasters.

---

## Re-check of the lead's fixes at `5e8a3b7b` (the same agent, one Chrome batch, PID 14700, stopped by PID)

All four pass (screenshot pixels, 1440 en, 390 for F3, light and dark):
- **F1:** the primary hovered `#3c4147` / `#c7cbd0`, exact (the desk's «Check in a visit», a calendar range end;
  computed `oklab(0.371743 -0.0037 -0.0119)` / `oklab(0.840961 -0.0029 -0.0073)`). The secondary variant hovered
  (the live-status neutral tone): light `#ecf4fc` → `#d9e1e9`, dark `#2c3137` → `#3a3f45` (before: `#e8dcdf`,
  `#443c3e`) — no warm cast. The dialog scrim over white `#85888a` (ink 50 % `#86898b`, −1 a channel), over
  `#1a1f25` `#11161b` (ink 70 %, exact); before `#8a8788`, `#181417`.
- **F2:** a lifted photo, by a mouse drag or by the keyboard (still `:focus-visible`): `solid 2px #b55bb3` / `#d27ed0`,
  offset −2 px, inside the picture, the ink ring not shown; the pixel outside the tile is the card's ground. A photo
  only focused: unchanged, its ring clipped (finding 222).
- **F3:** the phone menu's current entry `#ffe3fd` / `#471f46` at rest and under the pointer; another entry `#ffffff`
  → `#dde5ed`, `#1a1f25` → `#2c3137`.
- **F4:** the neutral tone light `#ecf4fc` → `#d9e1e9`, dark `#2c3137` → `#3a3f45`.
- **axe:** the phone menu (light-ar-390) and the desk (dark-en-1440): none. Both loads also clean on no Sea, no spark
  text, contrast, overflow, the focus ring, the logo (109.53 × 40, named «مساحة»).
- Shots added to `C:\Users\basel\Downloads\identity-prod-shots\` (`F1-…`, `F2-…`, `F3-…`, `F4-…`); script
  `scratch-v\run-recheck.mjs`, results `results-recheck.json`. No watcher left.
