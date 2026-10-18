# S2b-3b — Add a space, with its pin on the map

**Worker A** · main folder `C:\Users\basel\masaha`, on `main` at `bcb2e04`, clean · branch
`feat/admin-add-space`, cut with `git switch main`, `git pull --ff-only`, then
`git switch -c feat/admin-add-space`. Databases `masaha_dev` / `masaha_test`; API on 3320, web on 5320.

**Size cap:** at most 4 subagents, no self-review subagent, no workflow.
**Plan:** `C:\Users\basel\.prompt\MASAHA_WORKER_A\PLAN\S2B3B_PLAN.md` (`write-plan`).
**Report:** `C:\Users\basel\.prompt\MASAHA_WORKER_A\REPORT\S2B3B_REPORT.md` (`final-report`).
Follow the skills from start to end: `start-work-item`, `write-plan`, `open-pr`, `final-report`.

## 1. The task in brief

The second half of screen 26: the admin adds a space from the spaces list — its basics, its
location and its pin on a real map. The API is built (`POST /admin/spaces`, PR #44); this item is the
web, `shared/map` (Leaflet, which the architecture names and nobody has built yet), and two build
fixes the new map makes urgent: the data table's library out of the site's first download
(finding 45), and a build check that keeps it — and Leaflet — out.

## 2. Read first

In the order workflow §2 gives — **`docs/features/spaces.md` first** (its web part: #50's
decisions, the toasts, the `['admin']` scope), then `space-links.md` (the list the button sits
over) and `lookups.md` (the catalogue the area comes from). Then: `docs/frontend/architecture.md`
§1–§3 (the zones, no sibling imports, the dashboard-only rule, forms, *Where state lives*), §6 (the
map), §7; `docs/frontend/design-system/foundation.md` §2–§3, §10 and the rows of Field, Input,
Textarea, Select or Combobox, Button; `docs/frontend/localisation.md`; `docs/development/testing.md`
§1–§3; `docs/api/api-contract.md` §5 › *Spaces (the admin)* (the profile, `POST /admin/spaces`, its
errors) and *Lookups (public)*; `docs/architecture/data-model.md` › *Spaces* (the location, the
Strip's box); findings 27, 33 and 45 in full; `apps/web/vite.config.ts` and
`apps/web/scripts/checkBuild.ts`.

**The designs:**
- the add page: [desktop](docs/design/screens/43-admin-spaces/15-add-space-desktop-1440.webp),
  [phone](docs/design/screens/43-admin-spaces/16-add-space-phone-390.webp) — the
  *Basics* and *Location* sections only (the rest is the edit screen, S2b-4);
- the list with its "Add space" button: [desktop](docs/design/screens/43-admin-spaces/01-spaces-desktop-1440.webp),
  [phone](docs/design/screens/43-admin-spaces/02-spaces-phone-390.webp);
- the sections' layout in the edit screen (reference only): [desktop](docs/design/screens/43-admin-spaces/11-edit-unverified-banner-desktop-1440.webp),
  [phone](docs/design/screens/43-admin-spaces/12-edit-unverified-banner-phone-390.webp);
- the prototype: `docs/design/prototype/Admin space edit.html?new=1`. Its map is an illustration;
  ours is OpenStreetMap.

**The designs are a guide, not a contract.** They hold mistakes: elements out of alignment or out of
their grid, spacing that differs between twin elements, a control drawn in the wrong shape or state,
text cut off, a layout that breaks at one width or in one direction. Don't copy a mistake. List each
one you find in the plan under **"Design issues"**: the frame, what is wrong, and the better solution
you propose, built from the design system's own components and tokens. Build the proposal only once
the reply approves it; until then, keep to the design.

## 3. The settled decisions (review them in "Stronger decisions")

**The page**
- **D1 — one form, one submit.** The *Basics* section (names, descriptions) and the *Location*
  section (area, addresses, landmark, pin), and one "Add space" at the end; one `POST`. The design's
  per-section Save belongs to the edit screen: a space does not exist before it is created.
- **D2 — after the creation, back to the list** with a toast naming the space ("{name} added"), as
  #50's toasts do. **No edit route and no "Edit" item yet** (#50's L7: no entry point leads
  nowhere); they arrive with S2b-4. The list's **"Add space" button** arrives now.
- **D3 — the two sections are this capability's,** built so S2b-4 can reuse them for the edit; but
  **add nothing only the edit would use** (no option nothing passes yet).
- **D4 — the area is one active area,** chosen from the public catalogue (`GET /lookups`), grouped
  under its governorate: a **new component in `lookups`**, not an option on #50's filter field (a
  filter and a choice are different jobs; the creation refuses a hidden area).
- **D5 — errors:** 422 field errors on their fields (the shared profile schema validates first in
  the browser); 409 (two creations raced for the slug) said plainly; 429 as the other screens do.

**The map (`shared/map`)**
- **D6 — a generic point picker in `shared/map`,** React Leaflet over OpenStreetMap's standard tiles,
  **loaded lazily**; the directory's markers stay the directory's. Write the one line in
  architecture §6.
- **D7 — no pin until the admin places it:** the map opens on the Gaza Strip; a click places the pin,
  the pin can be dragged, and a **coordinates field** ("31.52, 34.45", pasted from Google Maps) moves
  it, and it the field — the keyboard's way, and the way when tiles fail. A point outside the Strip's
  box (`GAZA_STRIP_BOUNDS`, `@masaha/shared/spaces`) is refused on the field. The pin is drawn from
  the design system's tokens, never Leaflet's default image.
- **D8 — tiles that fail** leave a line under the map ("The map didn't load; enter the
  coordinates"), and the form still submits.
- **D9 — `leaflet.css` lives in the design-system folder,** with its overrides on semantic tokens,
  but is **imported by `shared/map` only**, so it loads with the map, never in the site's first
  download. "© OpenStreetMap contributors" always visible. The map's container is `dir="ltr"` in
  both languages; its controls sit where the language expects them.
- **D10 — standard tiles in both themes,** for now (revisited with the directory, step 3).

**The build**
- **D11 — finding 45:** a **separate entry for the design system's heavy data components**
  (`DataTable` first), imported only where needed, so TanStack Table leaves the site's first
  download. **Not** a `sideEffects` declaration (a file it misses is dropped silently in production
  only). Prove it with the manifest; resolve finding 45.
- **D12 — `check:build` also refuses Leaflet and TanStack Table** in the site's first download, as
  finding 45's *Resolves when* allows. Make each break once (import each statically into the site)
  and see the check fail.
- **D13 — finding 27:** study it in the plan; fold it only if a clean fix exists, proven by the
  manifest; otherwise leave it open and say why.
- **D14 — the dependencies:** `leaflet`, `react-leaflet` (a version made for React 19) and
  `@types/leaflet`, nothing else; `package-lock.json` is yours in this item.

## 4. Findings

- **Folded:** 45 (D11–D12). **Studied:** 27 (D13).
- **Record:** finding **46** — the deployment's content-security policy must allow OpenStreetMap's
  tiles (`img-src`), beside finding 33's Google rules; it links 33, it does not edit it (a record).
- Your new findings number **46–47**.

## 5. Risks — read before you start

- **Testing a map without `vi.mock`.** jsdom has no layout, so Leaflet cannot place a click. Put the
  logic in pure helpers (parse "lat, lng", check the Strip's box, field ↔ point) in the unit lane;
  a component test proves the map mounts, the attribution shows, and the coordinates field moves the
  pin; the click itself is proven by hand in the browser and said so in the report. No module is
  replaced with a mock.
- **Weight.** Leaflet and its CSS must arrive only with the add page. Read the manifest before and
  after; D12's check holds it.
- **D11 touches the design system's entry:** every existing import of `DataTable` moves to the new
  entry; nothing else in the barrel changes.
- **RTL.** Leaflet assumes LTR: container `dir="ltr"`, attribution and zoom controls checked in Arabic
  and English.
- **Leaflet's default marker icons** break with bundlers: don't use them (D7).
- **The other worker:** worker B builds the API in `masaha-b` meanwhile (owner linking). It touches
  `apps/api`, `packages/shared` and the API's documents; **you touch none of them**, and B adds no
  dependency while yours is open. Run `git merge-tree --write-tree` against B's open PR at your report.
- **Your web `.env`** sets `NODE_ENV=development`: build with `NODE_ENV=production` before
  `check:build`.
- **Docker Desktop stops sometimes:** start it, then `docker start masaha-postgres-1`; never
  `npm run db:up` from another folder.

## 6. Phase 4, screenshots and the pull request

- **Locally, once each on the head, one at a time:** `test:unit`, `test:component`, `test:api`; then
  `NODE_ENV=production npm run build` and `check:build`; lint, typecheck, `check:classes`,
  `format:check`.
- **A real run in the browser:** add a space by clicking the map; another by pasting coordinates;
  one refused outside the Strip; the tiles blocked (offline) and the form still sent; the toast and
  the list.
- **Screenshots** to `C:\Users\basel\Downloads\s2b3b-shots` (RTL and LTR, light and dark, phone and
  desktop): the empty form, field errors, the map with its pin, the coordinates field, tiles failed,
  the toast on the list.
- **PR:** title `feat(spaces): add a space with its map pin` (≤ 50), labels `feat`, `area:web`,
  `area:design-system`, `area:ci`, `area:docs`, assigned to the owner. **An independent review
  follows** (a new dependency and a change to the build checks). Don't merge.
- **The documents in this PR:** `spaces.md`'s *Web decisions* and *Web history* (D1–D9, with
  reasons, dates, the PR) and its code map; `lookups.md` (the area field); architecture §6 (D6) and
  §3 if the new entry needs a line; `foundation.md` if the layer's entries are listed there;
  findings 45 (resolved), 27 (resolved or why not), 46 (new); `overview.md`'s spaces line.
