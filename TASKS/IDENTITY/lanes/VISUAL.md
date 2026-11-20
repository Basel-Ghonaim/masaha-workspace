# IDENTITY — the visual pass (T23; EC3, EC6, EC8, EC9, EC11, EC13, EC14)

You are the **visual pass**, a sub-agent of the IDENTITY item's lead, on **Masaha** (a bilingual Arabic RTL / English
web platform for coworking spaces in Gaza). The item replaced the visual identity *Sea* (a petrol teal) with **ink +
berry** (ADR 0019) and added the logo, the browser's icons and a reset e-mail in ink. The code is joined and green;
you look at it **in a real browser** and return **a findings list**. You **change no file in the repository**: the
lead fixes what you find. You run in the background and cannot ask the lead a question: **decide and record**.

## 1. Where, and what is running

- **The app:** the lead's folder `C:\dev\masaha\app-design`, branch `feat/ink-berry-identity` at `5862e2a4`. The lead
  started its servers: the API on `http://localhost:3323` and the web on **`http://localhost:5323`** (browse
  `localhost`, never `[::1]`: the API's CORS origin is `localhost`, and from `[::1]` the session refresh is refused).
  Never start, stop or restart them; never touch any other folder's servers.
- **The data:** `masaha_dev`, the demo set, read only. **Never `db:seed`.** Never submit a form that writes (no
  check-in, no payment, no void, no save, no upload, no delete): open a dialog or a sheet, look, close it. A state
  the data lacks (a loading state, «+N» with six photos or more) is made with CDP's `Fetch.enable` +
  `Fetch.fulfillRequest` / holding a request, never by writing data.
- **The demo set in `masaha_dev`** (the lead checked it): the directory lists 37 spaces (the 24 of the demo set
  among them, e.g. `noor-hub`, `tuffah-place`); there is **no `masaha-demo`** here — the demo owner and the demo
  reception both hold **`pal-hub`, space 26** («بال هاب»), so the owner's and reception's screens are space 26's.
- **Sign-in:** `/login?next=<page>`, waiting for the page (routing elsewhere right after submitting races the
  landing redirect). Accounts: `demo-owner@example.com`, `demo-reception@example.com` (password
  `SEED_DEMO_PASSWORD`), and the admin (`SEED_ADMIN_EMAIL` / `SEED_ADMIN_PASSWORD`) — read them inside your script
  from `C:\dev\masaha\app-design\apps\api\.env`; **never print them** or write them to a file. `/auth/refresh` allows
  30 refreshes per 15 minutes per user, and every reload refreshes: keep to ~25 reloads per 15 minutes per account,
  and sign in again in each run (the profile's session does not survive between runs).
- **Your scratch folder:** `C:\dev\masaha\workspace\TASKS\IDENTITY\lanes\scratch-v\` (scripts, the Chrome profile,
  raw shots, JSON results). **Screenshots for the owner:** about 30, curated, to
  `C:\Users\basel\Downloads\identity-prod-shots\` (never in the repository).

## 2. Chrome — one at a time, through the grant

- Drive `C:\Program Files\Google\Chrome\Application\chrome.exe --headless=new --remote-debugging-port=<random free
  port> --user-data-dir=<scratch-v>\cdp-profile-<run>` over CDP with Node 24's built-in `WebSocket` (no dependency).
- **Every Chrome batch through the grant:** `node C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs visual
  node <your script>` (it waits for a slot and ≥ 4 GB free; let it). One Chrome at a time. At each batch's end stop
  the Chrome it started **by its PID** (only `cdp-profile` ones you started) and check none is left.
- Gotchas the project met: navigate to `about:blank` between loads (a hash-only change never re-renders); the theme
  and language come from localStorage `masaha.theme` / `masaha.language` set before a reload (a sign-in switches to
  the account's language); RTL pages: capture the viewport only, sized tall enough (`captureBeyondViewport` shifts an
  RTL page sideways); Radix menus open on Enter on a focused trigger, not `.click()`; `Emulation.setEmulatedMedia`
  changes `matchMedia` but its `change` event fires only in the foreground tab (`Page.bringToFront` first); a query's
  30 s `staleTime` can keep an intercepted request from being made (wait 31 s or use an uncached key); a route's
  error element swallows render errors silently (`Debugger.setPauseOnExceptions` shows them).

## 3. The screens (plan §13)

Read `C:\dev\masaha\workspace\TASKS\IDENTITY\2_PLAN_PROD.md` §13 (your brief) and §5.2 (the values), §7.2 (the logo's
places and sizes), §12 (the ECs below).

- **Screens:** Home; the directory (cards, the subscription choice and filters set); its map with a mark selected; a
  space's page (gallery, contacts, today's hours); sign in, register, forgot; `/me` and the favourites; the phone menu
  open; the desk (owner) with the check-in dialog open; Payments with «إلغاء الدفعة» open; the owner's overview; the
  owner's space profile (a Sheet open, the photos with «+N», a contact lifted by the keyboard — Space on its handle,
  then Escape); Finance (charts, heatmap); a date picker open (a range); the admin's overview, spaces and a space's
  editor; a loading state; the 404; the owner's rail and the admin's rail (768) and drawer (390).
- **At** 390, 768 and 1440 — Arabic and English, light and dark (prioritise: every screen at light-ar-390 and
  dark-en-1440; the rest of the matrix as the reload budget allows — say what you covered); the site's header also
  at **360** in both languages (EC14: menu, logo, language, avatar fit with no overflow).

## 4. On each load

- Console errors (and uncaught exceptions).
- **No Sea:** a computed-colour scan of every element (`color`, `background-color`, the four border colours,
  `outline-color`, `fill`, `stroke`, `box-shadow`, `text-decoration-color`) for Sea's 22 values: `#eafbfc #d5f4f5
  #b3e6e8 #85d0d4 #50b3b8 #15959b #02787d #096165 #05494c #023235 #001d1f #f4fcfe #eaf5f7 #dbe6e9 #c7d1d4 #9da7a9
  #747e80 #5c6567 #464f51 #2a3234 #182022 #0c1315` (compare in sRGB, exact). Any hit is a finding.
- **The spark's rules:** no element whose text `color` is the spark (light `#b55bb3`, dark `#d27ed0`) with text in it;
  no button (`button`, `[role=button]`, `a[data-slot=button]`) whose background or border is the spark.
- **Painted contrast:** every visible text node against its painted ground (the nearest opaque background, the
  translucent layers composited): < 4.5:1 for body text, < 3:1 for large text — a finding.
- **The focus ring** after three Tabs: on the page, a card, the sidebar, a Sheet and a dialog — visible, `ring`
  coloured, 2 px outline.
- Overflow: `documentElement.scrollWidth > clientWidth`.
- **The logo** where it shows: its element is the `Logo` SVG (`data-slot="logo"`), its size (EC6: `h-10` 110 × 40 ±
  1, `h-9` 99 × 36, the mark `size-9` 36 × 36), `transform: none` on it and every ancestor up to the header, its
  accessible name (the header's link «مساحة» / "Masaha"; the admin's header read once); in the phone menu's drawer it
  sits at the inline start in both directions.
- The status colours sampled where they show (light `#be222a #137d41 #b27406 #1f6cb0`, dark `#fc6e68 #63b77c #d6912b
  #64a6e9`): unchanged.
- **axe** (EC11): inject `C:\dev\masaha\app-design\node_modules\axe-core\axe.min.js` (read it and evaluate it in the
  page; no dependency), run it light and dark on each screen once; report every violation, colour contrast included.

## 5. Hover vs selected, with a real pointer (1440, light and dark)

With `Input.dispatchMouseEvent` (`mouseMoved` onto the element), read the computed `background-color` before and
while hovered, and of the selected one beside it: a desk row; a sidebar item beside the current one; an outline
button; a menu item (a menu opened by Enter); a chip beside a chip that is on; the subscription choice; the desktop
tabs; a sort header; FilterTag's remove; today in the calendar; a contact tile; a space card. Expected: the hover is
`hover` (light `#dde5ed`, dark `#2c3137`) or, on a muted ground, the wash over it (light `#d7dfe6` over `#ecf4fc`,
dark `#3c4147` over `#2c3137`); the selected is `accent` (light `#ffe3fd`, dark `#471f46`) and **keeps it under the
pointer**; the two differ; the sidebar's current item has its 3 px spark bar at the inline start; a chip that is on
has its spark edge. Any other result is a finding.

### Also look at (the lanes flagged these; each is a finding if it shows)
- `features/occupancy/components/LiveStatusControl.tsx`: its neutral tone is an outline Button on `bg-secondary`; in
  dark its hover may equal its rest fill (no hover seen). Hover it in dark and light, each tone.
- The site's phone menu (`SiteMenu`): the current page's entry (`aria-[current=page]:bg-secondary` on a ghost
  Button) under the pointer — does it keep its look?
- The owner's profile photos (PhotosEdit): a photo lifted **by the keyboard** — is its edge the spark or the ink
  focus ring? Is the outline clipped by the tile's frame? And lifted by a mouse drag.
- EC8 in a real tab: which icon Chrome shows in the tab (the SVG over the `.ico`): read `document.querySelectorAll
  ('link[rel~=icon]')` and, if you can, the favicon request Chrome makes on load (`Network.requestWillBeSent`).

## 6. The executor checks

- **EC3:** from a screenshot pixel (not computed style), Chrome's painted dark `accent` (`#471f46`), `primary-hover`
  (a primary button hovered: light `#3c4147`, dark `#c7cbd0`) and `hover-on-muted` over muted (above): within 1/255 a
  channel of the token test's values.
- **EC6:** the sizes above; the component's mark at 64 px against `docs/design/prototype/masaha/logo/
  masaha-mark-berry.svg` drawn at 64 px: ≤ 1 % of pixels differing by more than 8/255 in any channel (render both in
  one page on white; count).
- **EC8:** `GET /favicon.svg`, `/favicon.ico`, `/apple-touch-icon.png` on `http://localhost:5323` answer 200 with
  `image/svg+xml`, `image/x-icon` (or `image/vnd.microsoft.icon`), `image/png`; open `/favicon.svg` in a page under
  `Emulation.setEmulatedMedia` `prefers-color-scheme` light then dark and sample its ink and dots (`#1a1f25` /
  `#b55bb3`, then `#f7fbff` / `#d27ed0`).
- **EC9:** open the committed `apps/web/public/apple-touch-icon.png` (180 × 180, full bleed), `favicon.ico`'s 16 px,
  and `C:\dev\masaha\workspace\TASKS\IDENTITY\google\masaha-logo-120.png` (clear space all round, a round crop never
  cutting the dots); say what you saw.
- **EC13:** serve `C:\dev\masaha\app-design\docs\design\prototype` with `python -m http.server <a free port>` (stop
  it by its PID at the end; check the port free). The same screens at 1440, light and dark: the primary button, the
  sidebar's current item, a chip on, a hover — computed colours equal to production's. (The prototype's default is
  berry once lane C's commit is in; `?identity=sea` is the old look.)
- **EC14:** the 360 header (above).

## 7. Limits

No file in `C:\dev\masaha\app-design` or any repository changes; no server of the lead's stopped or started (only
your prototype's `http.server`); no data written; never `db:seed`; no secret printed; nothing in `C:\dev\masaha\app`
or `C:\dev\masaha\app-pr143`; public text never names hosting providers, free plans or session durations.

## 8. Your report = your final message

Return it as text (the lead saves it as `lanes\REPORT_VISUAL.md`):
- **Findings**, most severe first, each: the screen, width, language, theme; the element (a selector or its text);
  expected vs actual (values); the screenshot's path; whether it is the item's (a change of this PR) or older.
- Each EC with its numbers (EC3, EC6, EC8, EC9, EC11 per screen, EC13, EC14).
- The coverage: which screens at which widths, languages and themes were loaded; what was not, and why.
- The Chrome and `http.server` processes stopped by PID; the grants (any wait).
- The screenshots written (their names).
