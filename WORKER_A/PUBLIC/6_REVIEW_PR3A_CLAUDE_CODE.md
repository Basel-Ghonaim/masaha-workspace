# Review — PUBLIC PR 3a (#107, `feat/space-page`)

**Head:** `a85151b94c5b496b7f6cd6e0110a74b7524ea310`. CI on it: every lane `pass` (build, check:classes, check:links, format:check, lint, test:api, test:component, test:unit, typecheck; CodeRabbit rate limited). `CLEAN`. I checked the head again at the end, and it had not moved. 12 commits, 100 files, `apps/web` and `docs` only. No tool attribution in any commit. Every subject is 50 characters or fewer.

**Verdict:** mergeable. No blocker. Five small should-fixes and some nits. All of them fit PUBLIC PR 3b's first commit (`0_CARRIED_FROM_107.md`). Nothing needs a fix round on this PR.

How I worked: everything below marked "seen" I read in the code at the head (`git show` / `git diff origin/main...head`). From the executor's report and screenshots I used only two things: the red/green lines of the breaks, which I did not re-run, and screenshot `3a-verified-ar-light-390.png`, which I looked at for finding 1.

## The five most important

1. **should-fix — the phone's contact bar covers the end of the site's footer.**
   - Where: `components/page/SpaceDetails.tsx:56-60` (padding `pb-24 md:pb-0` on the page's own grid) and `ContactBar.tsx:13` (`fixed inset-x-0 bottom-0`). The site's `SiteFooter` comes after `<main>` (`pages/site/shell/SiteFooter.tsx:10`).
   - Why it happens: the padding is inside `main`. It pushes the footer down, but it does not leave room under the footer. At the end of the scroll, the fixed bar sits over the footer's last ~72 px.
   - Seen in the code, and also in `3a-verified-ar-light-390.png`: the footer's line shows cut off behind «واتساب | اتصال».
   - Who it hurts: a phone visitor never sees the footer's last line or its links («تواصل معنا»).
   - Fix: pad the page's real foot while the bar shows, for example a spacer after the footer or padding on the site layout. The other way is to leave room after the footer instead of inside the details. Add a width test, or a real-run shot at the bottom of the page.
   - Where the fix goes: next PR.

2. **should-fix — the "static" place map still catches one-finger swipes on a phone.**
   - Where: `shared/map/components/LeafletPlaceMap.tsx:672-681`. It sets `keyboard={false}` and `scrollWheelZoom={false}`, but leaves Leaflet's defaults `dragging: true` and `touchZoom: true`.
   - Why it happens: with touch dragging on, Leaflet gives the container `touch-action: none`.
   - Who it hurts: on a 390 px phone, a finger that lands on the 288 px map (`h-72`) pans the map instead of scrolling the page. On a long page, that is a scroll trap.
   - What the documents say: the plan says "a static map" (§1). `architecture.md` §6 says "so the page scrolls past it", which is true only for the mouse wheel.
   - Seen in the code. Leaflet's touch behaviour comes from its defaults; I did not test it on a device.
   - Fix: `dragging={false}` (and `touchZoom={false}`, keeping the zoom buttons), or Leaflet's `tap`/`dragging` only from `md`. Make §6's sentence say what the code does.
   - Where the fix goes: next PR.

3. **should-fix — `frontend/architecture.md` §2 contradicts itself about the space page.**
   - The paragraph now says the site has "a space's page at `/spaces/:slug` … (2026-10-22, #107)". It still ends with "…`account/` and the space details page are not built yet."
   - This breaks the rule "claim only what is true".
   - Also, the file's `Last Updated` stays at 2026-10-21 although it was edited on 2026-10-22.
   - Fix: drop "and the space details page" from that last sentence, and bump the date.
   - Where the fix goes: next PR.

4. **should-fix — `directory.md`'s Authority line is out of date.**
   - The header still says "On the web, the directory's list, its filters and near me are built." The map (#105) and the space page (#107) are missing from it, though its own Behaviour sections describe both.
   - In the same file, the map paragraph has a stray double comma: "the number taken from the ceiling,,".
   - Fix: name the map and the space's page in the Authority line, and remove the comma.
   - Where the fix goes: next PR.

5. **should-fix — test 75 does not prove the page's wiring of the dialog's `none` line, nor the "contact shown" case.**
   - Where: `SpaceDetails.component.test.tsx` › "the owner's dialog shows the page's contact, or its `none` line". The test passes the `none` line itself as `ownerContact` (`<p>لا توجد وسيلة تواصل متاحة الآن.</p>`). Test 63 checks `PlatformContact`'s `none` with a stub `<p>`.
   - The gap: no test checks that `SpacePage` passes `none={words.dialog.none}` (`SpacePage.tsx:78-81`).
   - The failing scenario: drop `none` there. With no contact configured, the dialog would show only its title and «إغلاق». Every test would stay green. The planned break ("`none` never shown") was made one level below that wiring.
   - Fix: in `routes.component.test.tsx` (test 79's setup, an unverified space, `vi.stubEnv('VITE_CONTACT_EMAIL', '')`), open the dialog and expect the none line. Then stub an email and expect the `mailto:` link.
   - Where the fix goes: next PR.

## The rest

6. **nit — the phone's live line's words.**
   - The executor proposed «{name}: التفاصيل في أسفل الصفحة» / "{name}: details at the bottom of the page".
   - My judgement: acceptable as they are. The sheet is a portal at the end of `body`. It sits after the footer in reading order and at the foot of the screen to the eye, so "at the bottom of the page" is true both ways.
   - Two small points:
     - The name is a plain string with no language mark. An English-only name in Arabic is read with Arabic voice rules.
     - The line lives inside the section that turns `aria-busy="true"` during a viewport re-ask. Some screen readers hold live updates inside a busy region until it ends.
   - Optional: «التفاصيل في آخر الصفحة», and the live line moved outside the busy section (`DirectoryMap.tsx:247`).
   - Where the fix goes: a finding to record, or the next PR, as the owner prefers.

7. **nit — Escape on the map section closes the card even when the focus is not on its mark.**
   - Where: `DirectoryMap.tsx:239-244`. The comment says "the focus is on its mark already", but that is true only while the focus is on the chosen mark. Escape pressed on another pin, or on «مركّز على موقعي», closes the card and leaves the focus where it was.
   - Harmless, and it matches carried item 7. Make the comment say what the code does.
   - Where the fix goes: next PR.

8. **nit — the loading and failed states of the space page have no `h1`.**
   - Where: `SpaceDetails.tsx:42-51`. The skeleton is `aria-hidden`, and the failure is only the `FailureAlert`.
   - After navigation the focus goes to `#main`, and a screen-reader user hears no heading.
   - The 404 state has its `h1` (`EmptyState titleAs="h1"`), as it should.
   - Fix: a visually hidden `h1` with `site.links.space` while loading or failed.
   - Where the fix goes: next PR.

9. **nit — finding 131's evidence is ambiguous for this PR.** It says "meanwhile the live status says «مغلق الآن» while a closure holds". The #107 page draws no live status (that is 3b). The sentence is true of the card and the pin, but reads as true of the page. Fix: "the cards' and pins' live status (and the page's, from PUBLIC PR 3b)". Next PR.

10. **plausible — prices that all name a shift outside `hours.shifts` render an empty section.**
    - Where: `priceGroups.ts:66-70`. With no saved shift named, only `shiftId === null` prices are kept, while the page's `state` is `'shown'` (`useSpacePage.ts`, `prices.length > 0`).
    - Result: the heading, then nothing — no «لم تُضف أسعار بعد».
    - Why only plausible: it is reachable only if the API can answer a price whose shift is not in `hours.shifts`. I did not prove that the API can.
    - Record it if the API allows it.
    - Where the fix goes: a finding to record.

## The executor's departures, judged

- **The overlay stacked with `isolate` + `z-sticky`:** fine. `.leaflet-container` is already `isolation: isolate` (`leaflet.css:13-14`), so Leaflet's panes and controls (z up to 1000) stay inside their own stacking context. The overlay at `--z-sticky` (100) in the frame's isolated context therefore stands above the map and never reaches the page's sticky bar. `z-sticky` is the layer's one named utility for use outside the layer (`tokens/tailwind.css:151-155`). No new CSS outside the layer.
- **«1,000» in Arabic:** fine. `ar-u-nu-latn` grouping follows localisation › Formatting (Western digits).
- **`.env.example`'s `masahagaza@gmail.com`:** fine. The owner's approval note asks for exactly that, and it wins over §9's "empty".
- **`PlaceMapProps` and the shared fixture `src/test/publicSpace.ts`:** fine. One type file more, and one fixture used by three test files.
- **Price labels carrying their language (`LocalText`):** fine and better. A label in the other language is marked (`PricesSection.tsx` `dt lang/dir`).
- **No `spacePath`, `publicSpacePath` kept:** fine. There is one link builder, and `SITE_PATHS.space` is only the route pattern.
- **The way back keeps the Directory's address on every change:** fine. It is in memory only (`directoryReturn.ts`), and a hand-edited `?…` only goes back to `/spaces`, where the filters sanitise it.
- **Tests 70–75 and 79 written after their code:**
  - Each planned break targets a guard the test really reads:
    - 70: `notFound` from the 404 status.
    - 71: the hidden prices' meta line.
    - 72: `bar` null without a phone or WhatsApp.
    - 73: the section order at both widths.
    - 74: the `aside` only when `wide`.
    - 79: the breadcrumb's and the back link's `href` with the search.
  - These would turn red as reported. I read the breaks; I did not run them.
  - 75 is weaker than its title (finding 5).

## Checked and fine (seen in the code)

- **Carried item 1:**
  - The pick ends on the map's unmount (`useDirectoryMap.ts:380-390`). It is judged in a microtask, so StrictMode's synchronous unmount and remount keep the pick.
  - `cancelPick` is stable and does nothing when not picking (`nearMeStore.ts:55-58`).
  - Tested both ways: the list shows the pin's line and `Masaha-Near`; the map reopens without a crosshair.
- **Carried items 6–8:**
  - `pickUnder` below 1024 px.
  - Escape in the card: `preventDefault`, the section skips it, and the focus goes back to the pin.
  - The sheet's «إغلاق» and Escape return the focus, with tests.
- **Carried item 2:** the overlay precedes the panes in the DOM (`LeafletMarkerMap.tsx:599-601`). Its order is tested in `MarkerMap` and `DirectoryMap`. The live line is `role="status"`, always rendered, and filled only on a phone.
- **Carried item 3:**
  - No `onViewChange` while picking (`useDirectoryMap.ts:410`).
  - `boundsText` rounds outward to hundredths: floor for south and west, ceil for north and east, with the float noise trimmed.
  - Both are unit- and component-tested.
- **Carried item 4:** on the map, `useLocationStatus` gives the owner's words with `privacy: null`, `stop: null`, and «مسح موقعي» / «تغيير الموقع» kept. The list's line is unchanged.
- **Carried item 5:** `busy` comes from `whole.isPending` (false on error, so there is no endless spinner). «جارٍ تحميل المساحات…» shows while the first answer is pending.
- **Carried items 9–14:** the ceiling's count comes from `MAP_PINS_CEILING`; the `map.pin` comment; Sheet's non-modal clause in `Sheet.tsx` and in foundation's row; the overview's map line; `role="application"`'s cost in §6; findings 134–136 written and indexed.
- **What the page claims:**
  - Hidden prices (`prices === null`, the shared type's "an unverified space's stale prices") say why, with «آخر تحديث للأسعار …».
  - Prices and hours never saved say so.
  - The unverified line is dated by `updatedAt.profile`.
  - Stale groups carry «قد يكون تغيّر».
  - The stale prices also get the warning Alert.
  - A 404 shows «لم نجد هذه المساحة» as an `EmptyState` `h1` with «تصفّح المساحات», distinct from the failure (reference and retry) and from offline.
  - Nothing outside `PublicSpace` is drawn: no announcement, no closure, no live status, no gallery yet.
- **Links:**
  - `wa.me/` gets the digits only.
  - `tel:` and `mailto:` use the stored value.
  - Instagram, Facebook, TikTok and the website use their stored `https://` address. The shared contact rule guarantees `https` (`packages/shared/src/spaces/contacts.ts`).
  - A phone's carrier is in its label («اتصال — جوال»).
  - «الاتجاهات» goes to `google.com/maps/search/?api=1&query={lat},{lng}`, in a new tab, `rel="noopener"`.
  - The slug is `encodeURIComponent`ed, and the API answers `not_found` for anything unlisted, so a hand-edited slug can only give 404.
- **The platform's contact:**
  - Read from `VITE_CONTACT_EMAIL` / `VITE_CONTACT_WHATSAPP` on each call.
  - The email is kept only if `emailSchema` takes it. WhatsApp is kept only if `normalisePhone` gives a number. An empty or invalid value is left out.
  - WhatsApp comes first and opens in a new tab.
  - No secret enters the bundle: the email is meant to be public.
- **Layout:**
  - One `h1` in the ready state.
  - The sections are `section[aria-labelledby]` under `h2`s, in U8's order.
  - The `aside` is named «الحالة والتواصل» only when `wide`.
  - Below 1024 px the status card comes before the prices, and «التواصل» is the last section.
  - The bar shows only when `phone` and a WhatsApp or phone contact exists.
  - The breadcrumb shows from 768 px with the last search, and «العودة إلى المساحات» below it.
  - The place's pin has `role="img"`, `aria-label`, `interactive={false}` and no tabindex.
  - Names and texts in the other language carry `lang`/`dir`.
  - Only logical classes; the values are `dir="ltr"`.
- **Weight:**
  - `PlaceMap` is lazy, like the other maps. The route is lazy.
  - CI's `check:build` passed. The report's 999,477 bytes I only read.
  - `carrierOf` and `updatedAgo` moved byte-for-byte (rename, 0 lines changed), and the four `spaces` importers only changed their import path.
- **Copy:** every new string is in both catalogues, with the plan's words. `platformSettings` was added to both indexes.
- **Documents:**
  - `directory.md`'s page paragraph, decisions, code map, findings and history; `spaces.md`'s carrier line; foundation's Sheet row; `setup.md`'s bullet; finding 40's evidence; findings 131 and 134–136 and the index; `overview.md`.
  - `#107` replaced everywhere.
  - Apart from findings 3, 4 and 9, they are true to the code.
