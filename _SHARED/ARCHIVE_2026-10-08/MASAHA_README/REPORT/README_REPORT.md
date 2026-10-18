# Report — README as Masaha's public face

## 1. The pull request and its head

- **PR:** [#54 — `docs: rebuild the README as the project's face`](https://github.com/Basel-Ghonaim/masaha/pull/54)
- **Branch:** `docs/readme` → `main`
- **Head:** `b93c9e8819a133c807ca2b088bf2920fbd86f06b` (`b93c9e8`) — equal to the CI run's head SHA
- **CI:** all checks pass (`lint`, `format:check`, `typecheck`, `test:unit`, `test:component`,
  `test:api`, `check:classes`, `build` + `check:build`); `mergeStateStatus` = **CLEAN**
- **Labels:** `docs`, `area:docs` · **Assignee:** the owner
- **Files:** 22 (20 images + `README.md` + `CLAUDE.md`), no code

## 2. The commits

| SHA | Message |
|---|---|
| `bcdb655` | `docs(readme): add the product screenshots` — the 20 files in `docs/assets/readme/` |
| `b93c9e8` | `docs: rebuild the README as the project's face` — `README.md` and `CLAUDE.md` |

Two commits, staged by path, with no tool attribution.

## 3. What was run, and what was not

This is a documents-and-images change, so phase 4's exception applies (workflow §2): a change with no
code runs `format:check` and the link check by hand, and nothing else.

**Run**

- `npm run format:check` — "All matched files use Prettier code style!" (Prettier excludes Markdown, so
  this covers the repository's other files; `README.md` and `CLAUDE.md` are outside it).
- **The link check by hand** — 32 relative links and image paths in `README.md`, 0 missing.
- **The image validation** (Pillow, scratchpad only) — every file's dimensions and a stddev check for
  blankness; 18 WebP + 1 GIF + the two composites. All non-blank; every WebP ≤ 300 KB (largest
  `directory-map.webp` at 65.4 KB); the GIF ≤ 3 MB (122.5 KB).
- **The GIF** — 3 frames after GitHub-safe optimization (the three held states), 1000×625, brightness
  and frame differences checked (AR-light → EN-light diff 7.5; EN-light → dark diff 227.5).
- **A real run for the shots** — API on **3322**, web on **5322**, a static server on **5330** for the
  scratchpad copy of the prototype. Screens captured from both sources; all servers then stopped;
  ports **3322, 5322, 5330 free** (and 3320, 3321, 5320, 5321 never used, checked free).
- **The rendered page on GitHub** — the branch's `README.md` loaded in a headless browser at
  desktop (1440) and phone (390) widths, light and dark: **24 `<img>` elements, 23 distinct, 0 broken,
  0 missing alt text**, 5 RTL blocks, the `<picture>` element picking `hero-light` in light mode and
  `hero-dark` in dark mode, and the `<details>` gallery rendered.

**Not run (stated, with why)**

- `lint`, `typecheck`, `build`, `check:build` and the test lanes — no code changed (phase 4's
  exception). CI ran all of them on the same head and they pass.

## 4. The breaks made, and tests seen failing first

None. This Work Item changes no code and no behaviour, so there is no lane to own a break, and no test
was added or seen failing. The Visual and content assertions that stand in for a test are §3's image
validation and rendered-page check.

## 5. The problems met, and how they were solved

- **The hero pairing.** The prompt asks for a composite hero: desktop in Arabic and light **beside a
  phone in English and dark**. The first captures had only an Arabic phone, so two extra phone
  captures were taken (English light and English dark) purely for the composite; they are not
  committed files (the composite is `hero-light.webp` / `hero-dark.webp`).
- **The map.** The prototype's map illustration was replaced, in the scratchpad copy only, with
  Leaflet 1.9.4 from a CDN over real OpenStreetMap tiles, pins placed on real areas, interaction off,
  and `© OpenStreetMap contributors` left visible. A pin-overlap check confirmed no two pins collide
  and all sit inside the map bounds.
- **A `setState` loop** in the copied `map.jsx` (positioning pins re-rendered on each pass) was fixed
  with a JSON-key dedupe before `setState`.
- **The directory's governorate filter** defaulted to one governorate and hid the others; it was
  changed to an "all governorates" sentinel so the shot shows all six fictional spaces.
- **Radix menus** do not open on a programmatic `.click()`; the driver dispatches real
  `Input.dispatchMouseEvent` mouse events. The header account menu also matches
  `button[aria-haspopup=menu]`, so the row trigger is matched by `button[aria-label^="إجراءات"]` to
  avoid the wrong menu.
- **Sign-in** is in-memory with a refresh cookie, so the driver signs in through the real form (after
  `Network.clearBrowserCookies`), not by seeding a token.
- **A silent-stdout bug:** calling `process.exit` during WebSocket teardown dropped the script's
  output (a libuv assertion). The driver now closes the socket and sleeps before exiting.

## 6. Anything that behaved unexpectedly, even unsolved

- **The Mermaid diagram.** GitHub renders Mermaid client-side. In our headless, anonymous probe the
  fence appeared as a hidden plaintext block (`pre.render-plaintext-hidden`, height 0) with no SVG
  found in the main frame or in the one iframe, across repeated loads; the probe could not confirm the
  rendered diagram. The fence is the idiomatic, prompt-required form, so it was left as is. **Worth a
  one-second visual check on the branch** to confirm the diagram draws for a signed-in viewer; if it
  does not, the fallback is to commit a small rendered SVG instead.
- **The GIF collapsed from 28 captured frames to 3.** Pillow's optimizer merges identical consecutive
  frames and sums their durations, so the 28 captures became the three held states (AR light 1120 ms,
  EN light 1400 ms, dark 1400 ms). This is the intended result of "switching the language flips the
  direction, then the theme", and it kept the GIF tiny (122.5 KB).
- **`app-register.webp` was promoted into the committed set** (see §8) to substantiate "sign-in and
  register" from the running build.

## 7. The early conflict check

`gh pr list --state open` returns **only PR #54** (this one). There is no other open pull request, so
there is nothing to `git merge-tree` against and no conflict. `origin/main` is still `1333e66`; the
branch was pushed `--no-track` from it and needs no rebase.

## 8. Each departure from the prompt, with its reason

- **20 image files, not 19.** The prompt lists "sign-in and register" among the running-build shots
  and allows "about 20" files including the GIF. `app-register.webp` was added (20 total) to make the
  "sign-in and register" claim literal; the two weakest candidates (`app-signin-phone`, a dark map
  still) were left out. `directory-map.webp` is used twice in the page but is one file.
- **The hero composites** use two phone captures (English light and dark) that are not committed; only
  `hero-light.webp` and `hero-dark.webp` are files.
- **Nothing else.** No finding was folded or opened (the map/`README` defects fixed here were the
  items themselves, not recorded divergences). The design archive in the repository was not touched;
  the OSM map lives only in the scratchpad copy. No Issue was created.

## Prepared repository metadata (not applied)

The owner applies these; nothing here is committed.

- **Description (one line):**
  `Masaha — a bilingual platform for coworking spaces in the Gaza Strip: a public directory with live availability, and one dashboard for owners, reception and the admin.`
- **Topics (~8):** `coworking` · `gaza` · `palestine` · `react` · `typescript` · `express` ·
  `prisma` · `monorepo` · `bilingual` · `rtl`
- **Social preview (1280×640):** `C:\Users\basel\Downloads\readme-assets\social-preview.png`
  (not committed, non-blank: per-channel stddev ≈ 38–41)

## The images, each with its source

**From the design prototype copy** (scratchpad copy of `docs/design/prototype/`, real OpenStreetMap
tiles; the archive in the repository is untouched):

| File | Screen |
|---|---|
| `hero-light.webp` | Composite: Home (desktop, Arabic, light) beside Home (phone, English, dark) |
| `hero-dark.webp` | Composite: Home (desktop, Arabic, dark) beside Home (phone, English, light) |
| `home-light.webp` / `home-dark.webp` | Home (light / dark) |
| `home-phone.webp` | Home, phone |
| `directory-light.webp` | Directory, list |
| `directory-map.webp` | Directory, map (Leaflet + OSM) |
| `space-light.webp` | Space details |
| `owner-light.webp` | Owner overview |
| `desk-light.webp` | Front desk |
| `masaha.gif` | Home: Arabic light → English light → dark |

**From the running build** (this worktree's app; API 3322, web 5322):

| File | Screen |
|---|---|
| `app-signin.webp` / `app-register.webp` | `/login` and `/register` |
| `app-spaces.webp` | `/dashboard/admin/spaces` |
| `app-spaces-menu.webp` | The row actions menu |
| `app-spaces-dialog.webp` | The delete confirmation dialog |
| `app-spaces-toast.webp` | The "hidden" toast |
| `app-spaces-phone.webp` | The admin's spaces list, phone |
| `app-lookups.webp` / `app-lookups-amenities.webp` | `/dashboard/admin/lookups`, both tabs |

The one honest line under the gallery, in the page: *"Screens from Masaha's product design and its
running build."*
