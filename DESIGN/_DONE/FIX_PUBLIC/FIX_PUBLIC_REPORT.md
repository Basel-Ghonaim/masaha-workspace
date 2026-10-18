# Design fix 3 — the public site: report

The public design fixer · worktree `masaha-design-public` · branch `design/public` · 2026-10-12.

## 1. The pull request

**#65 — `design: the public site`** · head **`51685d0`** · CI green on that head (format:check,
check:links, check:classes, lint, typecheck, build, test:unit, test:component, test:api) ·
GitHub `CLEAN` · labels `docs`, `area:docs` · assigned to the owner · not merged.

## 2. The card first (the owner's change)

Before/after at each width, in `C:\Users\basel\Downloads\design-fix-public\`:

| Width | Before | After |
|---|---|---|
| 390 | `H2-directory-390-before.png`, `H2-home-390-before.png` | `H2-directory-390-after.png`, `H2-home-390-after.png` (signed in: the heart), `H2-directory-390-dark-after.png` |
| 768 | `H2-directory-768-before.png`, `H2-home-768-before.png` | `H2-directory-768-after.png`, `H2-home-768-after.png`, `H2-directory-failed-768.png` (no photo: the mark) |
| 1440 | `H2-directory-1440-before.png`, `H2-home-1440-before.png`, `H2-directory-1440-dark-en-before.png` | `H2-directory-1440-after.png`, `H2-home-1440-after.png`, `H2-directory-1440-dark-en-after.png`, `H2-directory-loading-1440.png` (photos loading), `H2-favorites-1440.png` |

What it is now: the photo leads, edge to edge, in a frame reserved before it arrives (2:1 on a phone,
16:9 from 768 — design issue 2, weighed again with the prices gone: a 16:9 frame on a 390 card was
22 px taller for no gain); under it the display name (`heading-3`), the area, one row with the state
badge (or «لا تتوفر حالة مباشرة») and «موثّقة», one row with today's hours and the distance. No
price, no «آخر تحديث» (freshness moved to the page's groups). A space with no photo shows its mark
(the first letter of its display name, in the switcher's primary square). The archive has no real
photos, so the frame holds a drawn room tinted from the layer's tokens with `color-mix` (one tone
per space: primary, info, success, warning) — **a stand-in, not artwork to build**; `CHANGES.md`
says so. My first stand-in, on the raw `-subtle` tokens, was washed out in light theme and did not
lead the card; the tinted one does in both themes.

## 3. The commits

| # | Commit | Decision(s) |
|---|---|---|
| 1 | `2722067 docs(design): one name for each space` | U3 |
| 2 | `b0429b6 docs(design): place is one filter, no amenities` | U1, H3 |
| 3 | `2a153fe docs(design): a price filter and the sort's name` | U5, S1 |
| 4 | `c0dc6d5 docs(design): one near-me control and state line` | U2 |
| 5 | `2d9d5e5 docs(design): the map by shape, on a phone too` | U6, design issue 1, PU-026, PU-013 |
| 6 | `3cc7f3c docs(design): place a pin from the keyboard` | U7, S2, S6 |
| 7 | `14ca308 docs(design): a striking space card` | U12/H2, PU-014, PU-025, design issues 2 and 4, S5 |
| 8 | `1830c93 docs(design): the space page in one order` | U8, PU-020/021/022/023/027, DI-3 |
| 9 | `023dcca docs(design): one freshness rule` | U4 |
| 10 | `0e44b64 docs(design): prices per audience` | U9, H5 |
| 11 | `bd92e4b docs(design): own amenities in the one list` | H4 |
| 12 | `631b10e docs(design): the report names its reader` | U10 |
| 13 | `324a493 docs(design): About and the error pages` | U11, PU-024, S3, S4 |
| 14 | `51685d0 docs(design): batch 3 on the board` | the board's section, INDEX §53, README's count |

Every subject ≤ 50 characters (longest 48). 19 files, all under `docs/design/`.

## 4. What was run, and what was not

- **At every commit:** `check-parse.mjs` — 49/49 blocks parsed; `check-classes.mjs` — 0 new dead
  classes (8 known).
- **The real run** (headless Chrome over CDP, `python -m http.server` on 5347; `origin/main`'s
  prototype on 5348 for the "before" images):
  - a 96-frame matrix — Home, the Directory's list and map, the space page, About, Error,
    Favourites, «بلاغاتي» × 390 (touch) / 768 (touch) / 1440 × Arabic / English × light / dark —
    with **no runtime error**; I looked at a selection of each page, every width and both themes;
  - each decision's own states: the place combobox open (desktop and in the phone's sheet), the
    price range applied and its error, near-me in four states and «إيقاف الترتيب»/«مسح موقعي»,
    Home's «اختر منطقتك» moving the focus, the map's sheet and ring, picking with arrow keys,
    «ثبّت الموقع هنا», «تغيير الموقع» → «رجوع», `?photos=loading|failed`, both report readers,
    `Error.html?type=offline&fail=retry`;
  - **regression looks** on the shared parts' other users: Customers' filter sheet at 390, the
    admin's spaces list, the admin's read-only Focus Hub, the editor's pin map (`Admin space
    add.html`, still tap-to-place, no crosshair), the owner's space profile, the desk's offline state;
  - 30 before/after pairs named by decision (`U1-…`, `U6-map-390-…`, `H4-…`), 48 images in all.
- **Not run locally:** `format:check` and `check:links` — this worktree installs no packages, by
  the prompt; **CI ran both, green**. No test lanes or build locally: no application code changed.
- Servers stopped, ports 5347 and 5348 checked free; my headless Chromes exited with each run.

## 5. Breaks made, tests seen failing first

No test lane covers `docs/design/`. What the checks caught on the way: `check-classes` failed on
`pin-` (a class built by concatenation) — fixed by naming the four mark classes whole;
`check-parse` failed on a duplicate `groupDays` (see §6).

## 6. Problems met, and how each was solved

- **The `\u` escapes.** The tools turned `\u0600-\u06FF` and `'\u00a0'` into literal characters
  (my memory warned of it): the first edit wrote the literal range, and a script's match failed on
  the escape. Solved by building every backslash with `chr(92)` in scratchpad scripts.
- **The cards showed only marks** at first: `photos` lived in `details-data.js`, which the lists do
  not load. Moved into `data.js`, as the plan said.
- **A name clash:** my freshness helper `groupDays` collided with the hours' own `groupDays`, which
  blanked the space page; renamed `factAge`.
- **The ₪ in the price fields** sat on the wrong side in Arabic as an end icon; a start icon gives
  «50 ₪» and «₪50» in both directions.
- **A note starting with «** flipped its guillemets in RTL; it now starts with an Arabic word.

## 7. Anything that behaved unexpectedly

- **The static server sometimes dropped the design-system bundle** (`window.MasahaDesignSystem`
  undefined, a blank page, no page error). It is the server, not the pages: a reload always loaded
  it. The screenshot script reloads up to three times; one frame of 96 needed it.
- **A full-page capture moves the map's pin:** the map's height follows the viewport (`100svh`), and
  stretching the viewport to the page's height after the pin was centred moves it down. At a real
  phone's height the pin sits in the upper third, as `U6-map-390-after.png` shows.
- **Two headless Chromes not mine** were running (port 9100, a `cdp-…` profile) — probably the other
  design worker's; I left them.
- **Already inconsistent in the samples, not changed:** the admin's sample says Number One has no
  photos while the public sample gives it two, and its price age differs between the two (41 days
  vs 5). I took the admin's ages for the four new groups (profile, hours, amenities, contacts) so
  both sides agree there, and left the prices' and the photos' as they were.

## 8. Readers of the moved or retyped data (the reply's correction)

Searched across the whole prototype before each change:
- **`nameAr`** (moved to `data.js`; ZM Hub's removed): `Admin space edit.html` (`base.nameAr || ''`,
  its read-only row), `profile-a.jsx` (`space.nameAr || ''`), `Admin space add.html` (its own form
  state), and my pages. None broke: the admin's editor shows ZM Hub's Arabic name empty, which the
  model allows.
- **`photos`** (moved to `data.js`): `Admin space edit.html` (the photos count), `space-parts.jsx`.
  Same object, still read.
- **`lastReview`, `statusUpdated`, `hoursUpdated`** (replaced by `fresh`): read only by
  `Space details.html` and `space-parts.jsx`.
- **`jawwal` / `ooredoo`** (retyped `phone`): `profile-b.jsx`'s `OLD_TYPE` map (the other worker's;
  untouched, still harmless) and `Admin space edit.html`'s read-only contacts, which read `phone` and
  show its carrier («جوال»). None broke; none of the other worker's files was edited.
- Also kept for its readers: `studentMonth` (the admin's read-only prices) and `M.amenities` /
  `allAmenities` (the editor).
- **A new top-level name, `spaceName`** (`shared.jsx`, U3), and the other globals this PR adds
  (`otherName`, `SpaceName`, `without`, `CoverArt`, `SpaceCover`, `HeartButton`, `useFavourites`,
  `WifiOffIcon`, `PinMark`, `pinState`). Every page's scripts share one global scope: on `main`,
  `Admin owners.html` declares its own `spaceName`, which on that page replaces the shared one
  (harmless there — it renders no card, and the page runs without error on this branch). #66
  removes that declaration, so the merged tree is clean; no file of #66 declares any of the other
  names (searched).

## 9. The early conflict check

- **#64 `feat/space-own-amenities`** (the amenities worker): `git merge-tree` **clean**.
- **`design/admin-rest`** (the other design worker): not pushed at the first report. **Now #66,
  checked at the review round: only `CHANGES.md` conflicts** (both sections appended at the end; the
  fast path keeps both). Shared with
  it: `CHANGES.md` (my *Batch 3* section is appended after 2a), `INDEX.md` (my parameter table under
  the fix-phase one, and section 53 at the end), the board (my section at `top:142400px`, after the
  last frame), and **`README.md`'s frame count** (now 493 in 53 sections): whichever merges second
  keeps both sides and adds its frames to that count, and moves its board section if both took the
  same height.

## 10. Departures from the prompt and the plan

- **Design issue 1 went with the map commit**, not the near-me commit: «مركّز على موقعي» needs the
  map's re-centring, which U6 builds.
- **The smaller Directory items** (PU-013's view switch, PU-025's columns) rode on the map and card
  commits, which touch the same lines; the plan's commit list did not name them.
- **A 14th commit** for the board's section and INDEX §53, and **`README.md`'s frame count**, which
  the new frames made untrue (`README.md` is inside `docs/design/`).
- **The public area list now mirrors the admin's seeded catalogue** (19 areas in four
  governorates) instead of inventing four areas, as the plan had it: the same facts on both sides,
  and a real grouping for the combobox. Its effect on the other worker's pages: the admin spaces
  list's area filter offers the same catalogue it already seeds.
- **The heart on the cards is for a signed-in visitor only**, as the reply's card brief says; the
  plan had also offered the sign-in dialog to a signed-out one.
- **Design issue 5** was not built: the combobox does not clip in the phone's sheet.
- **Golden Hub's notice reads «آخر تحديث للمعلومات قبل شهرين»**, not the decision's example «قبل 4
  أشهر»: the age comes from the admin's sample date for Golden's profile (70 days), so both sides of
  the space agree; the decision's wording is kept, its number is the sample's.
- **U4's sections without a date:** «عن المساحة» and «الموقع» carry no «آخر تحديث». The description
  and the address are the profile group, whose age the unverified notice gives; a verified space's
  page shows no profile age. Only the four groups a visitor acts on (prices, hours, amenities,
  contacts) say theirs.

## 11. New design issues (not built)

1. **The light-theme map illustration is very pale** beside the new cards (land and blocks on
   `muted` / `accent`); the pins carry it, but the map reads washed out at 1440. Better: the same
   `color-mix` tints as the cover stand-in. Page · low. (The real map is OpenStreetMap's, so this is
   the archive only.)
2. **The space page's gallery still uses the old «صورة n» grey tiles** while the cards show drawn
   covers, so a card and its page look unrelated. Better: the same stand-in in the gallery's tiles.
   Page · low.
3. **The phone's map view stacks five rows above the map** (the view switch, search, «الفلاتر», the
   count with «الأقرب إليّ», the state line, the legend), leaving ~470 px of map at 390. Better: the
   count and «الأقرب إليّ» in the row with «الفلاتر» on a phone. Page · medium.

## 12. Owner's additions

None during the build (the reply's card change and answers are folded into the plan and §2).

## Review fixes (round 1)

From `PROMPT\FIX_PUBLIC_FIXES.md` (the analyst's review of `51685d0`).

### 1. The pull request
#65 · head **`1f3fb91`** · CI green on that head (all ten checks) · `CLEAN` · one "Review fixes"
comment on the PR · the description updated.

### 2. The commits
Every fix folded into the commit of its decision with `--fixup` and one autosquash; the final tree
is byte-identical to the pre-squash head (`92fd52d`). Now 15 commits: the 14 before, rewritten, and
**`1f3fb91 docs(design): no object rest in shared parts`** (DI-27, its own: it belongs to none of
the batch's decisions).

| Fix | Folded into |
|---|---|
| R1 — «اختر منطقتك» on a desktop list goes to the sidebar's «المنطقة»; the sheet only below 1024 or on the map | `5b3c708` one near-me control |
| R2 — Home's «تغيير الموقع» goes to the Directory's picking | `5b3c708` one near-me control |
| R2 — «رجوع» after arriving to pick restores the tab's saved location | `80e37cf` place a pin |
| R3 — the space page's map label by `spaceName` | `87ecf84` the map by shape (the commit that last wrote the line; folding into U3's would have conflicted) |
| `M.minPrice` removed; the two group ids by `React.useId` | `9697ac7` a price filter |
| the spaces' `updated` texts removed | `c16cc79` one freshness rule |
| the unused `Tabs` imports removed | `87ecf84` the map by shape |
| `account.jsx`'s `HeartIcon` removed | `010c2c6` a striking space card |
| the map's light drawing; the legend inside the map; one row for search and «الفلاتر» on the map | `87ecf84` the map by shape |
| the gallery's tiles as the card's stand-in | `590f329` the space page in one order |
| each decision's `CHANGES.md` line amended (U2, U6, PU-023) | their commits |

### 3. What was run, and what was not
- Both scripts **at every one of the 15 commits**: 49/49 parsed, 0 new dead classes.
- The browser: the map at 390 and 1440 in both themes and English; the gallery at 1440 and 390
  dark; R1 at 1024 (the sidebar's field takes the page, no sheet) and at 1440 then a switch to the
  map (no stray sheet) and at 390 (the sheet opens); R2's whole round trip at 390 (a saved manual pin
  on Home → «تغيير الموقع» → the Directory picking → «رجوع» → the pin kept, «مرتبة حسب المسافة من
  الموقع الذي حدّدته»); a 34-frame sweep (the public pages and the shared parts' dashboard users,
  `Admin owners.html` among them) with no runtime error.
- DI-27 probed with a script that mounts an `ActionButton` on a page and reads its button.
- **Not run locally:** `format:check`, `check:links` — CI ran them, green.

### 4. Breaks made, seen failing first
DI-27 was reproduced before the fix: on `Admin space edit.html?id=white` and `Owner space
profile.html`, the mounted `ActionButton`'s DOM had `actionkey` and `success`, with React's
"does not recognize the prop" and "unknown event handler `onAction`" warnings; `_excluded` was
`["value","onChange","end"]` (the editor's `ClockInput`). After it: only `data-slot` and `class`, no
warning, the action ran — on both pages and on `Admin settings.html`, which loads no editor module.

### 5. Problems met
- **The autosquash conflicted five times**, where a fixup's context held a later commit's lines (the
  `SpaceMap` signature, the Directory's map props, Home's top lines) and on `CHANGES.md`. Each was
  resolved to the state the commit should have had; a small script resolved the `CHANGES.md` ones
  (HEAD's lines, the fixup's version of the edited line, and a commit's own new lines). Once it
  dropped the edited U2 line; caught by a check for its new sentence, restored from the pre-squash
  head. The final tree equals the pre-squash one, which settles that nothing was lost.
- The probe hung twice: Chrome's path lost its backslashes in a heredoc, and the socket opened before
  its listener; both fixed in the script.

### 6. Unexpected
- R2 hid a second gap: arriving at the Directory with `?pick=1` started picking with no "before"
  location, so «رجوع» would have cleared the saved pin — against U7. Fixed with R2 (the tab's saved
  location is the one before).
- A full-page capture still stretches the map with the viewport (as in round 0); not a defect of the
  page.

### 7. The early conflict check (at `1f3fb91`)
- **#66 `design/admin-rest`:** conflicts in **`CHANGES.md` only**. Whichever of #65 and #66 finishes
  its fixes first merges first; the second rebases keeping both sections.
- **#64** `feat/space-own-amenities`, **#67** `feat/admin-deleted-spaces`, **#68**
  `refactor/web-storage-titles`: clean.

### 8. Departures
- R3 went into the map commit, not U3's, as above.
- DI-27 is a commit of its own.
- The phone's map rows: the legend moved **inside** the map at every width (the decision allowed
  "inside the map … or above it"); the search and «الفلاتر» share a row on the map at every width
  (there is no sort there).
