# Report: README polish (fix the run steps and the images)

## 1. The pull request and its head

- **PR:** [#55, `docs(readme): fix the run steps and the images`](https://github.com/Basel-Ghonaim/masaha/pull/55)
- **Branch:** `docs/readme-polish` → `main`, cut `--no-track` from `origin/main` (`793189a`)
- **Head:** `ba15621ab668d434840319bae055e9e8ff3dbb72` (`ba15621`), the same as the PR's `headRefOid`
- **CI:** every check passes on that head:
  - `lint`, `format:check`, `typecheck`;
  - `test:unit`, `test:component`, `test:api`;
  - `check:classes`, `build` (with `check:build`);
  - CodeRabbit: skipped, since this repository has no automatic reviews.
- **GitHub state:** `mergeStateStatus` = **CLEAN**.
- **Labels and assignee:** labels `docs` and `area:docs`; assigned to the owner. Not merged.
- **Files:** 15 in all: `README.md` and 14 images in `docs/assets/readme/`. No code.

## 2. The commits

| SHA | Message | Files |
|---|---|---|
| `0a60a1f` | `docs(readme): retake the screenshots` | the 14 images |
| `ba15621` | `docs(readme): fix the run steps and the wording` | `README.md` |

Both were staged by path and carry no tool attribution. The PR title is the prompt's and covers both
commits.

## 3. What was run, and what was not

**Run**

- **`npm run format:check`:** "All matched files use Prettier code style!" Prettier excludes Markdown.
- **The link check by hand:** 32 relative links and image paths in `README.md`, none missing.
- **"Run it locally", word for word, in a fresh clone** (`git clone https://github.com/Basel-Ghonaim/masaha.git`, `main` at `793189a`):
  - Every command ran as the README writes it:
    - `npm ci` added 681 packages in 46 s;
    - `cp apps/api/.env.example apps/api/.env`, then `JWT_SECRET`, `SEED_ADMIN_EMAIL` and `SEED_ADMIN_PASSWORD` were set;
    - `npm run db:up` started PostgreSQL and waited until it was healthy;
    - `npm run db:migrate && npm run db:seed` printed "Seeded the lookups, the admin account and the settings.";
    - `npm run dev -w @masaha/api` made `/health` answer `{"status":"ok","db":"up"}`;
    - `npm run dev` in a second process started Vite.
  - Signing in through the web form as the seeded admin landed on **`/dashboard/admin`** («نظرة عامة»).
  - The branch changes no code, so the clone of `main` runs exactly the code the branch carries.
  - **The two settings that differed from the README's defaults, and why** (the owner's reply asked for this):
    1. **Ports:** the API ran on `3322` (`PORT`, with `CORS_ORIGIN` on `5322`), and the web on `5322` (`WEB_PORT`, `API_PROXY_TARGET`). The defaults, 3320 and 5320, belong to worker A, and the prompt forbids them. These are the setting setup's *Running a second folder* describes.
    2. **The database:** a throwaway `masaha_readme_fresh_dev` instead of `masaha_dev`. `masaha_dev` is worker A's, and a fresh database is what proves a fresh clone. `prisma migrate dev` created it.
  - **Afterwards:**
    - the database was dropped;
    - the clone was deleted;
    - the generated credentials file was deleted.
- **The images** (Pillow, in the scratchpad):
  - 20 files;
  - all desktop shots 1280×800, the phone shots 390×844, and the heroes 1400×803;
  - the largest is `masaha.gif` at 179 KB (3 frames, 1000×625); the largest WebP is `space-light.webp` at 90 KB;
  - none is blank (standard deviation 18–69);
  - none carries EXIF, XMP or an ICC profile.
- **The map**, checked by eye at full size before compressing:
  - nothing beyond the Strip's edge is visible or labelled;
  - "© OpenStreetMap contributors" sits bottom-left, clear of the mask, the pins and the popup;
  - the popup is bottom-right in RTL.
- **The identity search:** `universit|Al-Quds|القدس|جامعة|graduat|supervisor|مشرف|defen[cs]e|مناقشة` over the whole `README.md` and the diff found nothing. I also checked the social preview by eye.
- **The rendered page on GitHub:** the branch's README, in headless Chrome, at 1440 and 390 width, light and dark.
  - In every mode:
    - 23 content images, none broken, none without alt text;
    - the `<picture>` picks `hero-light.webp` in light and `hero-dark.webp` in dark;
    - 5 RTL blocks;
    - no horizontal scroll.
  - **The Mermaid diagram draws** (seen in a dark desktop screenshot). This answers the open question of PR #54's report.
- **Servers:**
  - stopped: the API (3322), the web (5322) and the static server for the prototype copy (5330);
  - ports 3320, 3321, 3322, 5320, 5321, 5322 and 5330 checked free;
  - 3320, 3321, 5320 and 5321 were never used.

**Not run (stated, with why)**

- **`lint`, `typecheck`, `build`, `check:build` and the test lanes:** this change has no code (workflow §2, phase 4's exception). CI ran them all on the head, and they pass.

## 4. The breaks made, and tests seen failing first

None. This item changes no code and no behaviour, so no lane owns a break and no test was added.
Instead of a test there are:
- the fresh-clone run;
- the image checks;
- the map check;
- the rendered-page check (§3).

## 5. The problems met, and how each was solved

- **Unsplash refuses plain requests:**
  - both the search API and the search page return 401 or a bot page to `curl`;
  - so I opened the search page in headless Chrome, with the "free licence" filter;
  - each chosen photo's page shows "Free to use under the Unsplash License".
- **Photos rejected:**
  - five candidates had people, a business name painted on the wall, room signs or wall lettering;
  - one I first chose (`Qe22xl-yoWg`) carries small logo stickers and a poster on its glass partition, so I replaced it with `oUpLJxufIiM`.
- **The map's frame.** The Strip runs diagonally, so any rectangle that holds all six pins also holds land beyond it:
  - Stronger decision 5.1, approved: an opaque inverse mask over everything outside the Strip.
  - **The outline:**
    - the land border comes from OpenStreetMap's own boundary, relation 1473938, fetched once from Nominatim;
    - it is closed by a line a few kilometres offshore;
    - the outline's sea side stays inside Gaza's waters.
  - **The mask's fill** is the design system's `--muted`, which is the map container's own surface, with a `--border` edge.
- **Pins overlapping in Gaza City.** Manara, Rukn and Maidan are a few kilometres apart:
  - each of those pills got an anchor (to the west, above, to the east), so its dot still sits on the point;
  - the prototype's precompiled CSS has no `flex-row-reverse` class, so the west-anchored pill uses an inline `flex-direction` to keep its dot on the point.
- **Siraj's stored pin is on the border.** `masaha_readme_dev` holds 31.3382, 34.3663 for Siraj, which is about the eastern boundary of Khan Younis governorate:
  - in the prototype copy the pin sits on Khan Younis city (31.3445, 34.3045);
  - the database was left as it is, because Siraj is now verified and the admin may no longer edit it, and its coordinates appear in no image.
- **A fresh clone in the scratchpad fails on Windows:**
  - the scratchpad's path is long enough that the prototype's font files pass 260 characters ("Filename too long"), and the checkout fails;
  - so I cloned into `C:\Users\basel\masaha-fresh` instead, and deleted it afterwards.
- **The clone could not be deleted at first:**
  - processes from my first API start in this worktree (an `npm`/`tsx watch` tree from 10:21) were still alive;
  - I identified them by creation time and parent, and killed the tree;
  - the delete then succeeded.
- **The home row's data:**
  - in the prototype copy, Manara, Rukn and Darb are verified and open, so `Home.html`'s own filter (`verified && status === 'open'`) gives three cards;
  - Darb carries «قد يكون تغيّر» (its prices are stale, as in the admin's list);
  - the browse-by-area cards now list the areas that hold spaces, «في كل المحافظات», so the old «النصر — 0 مساحات» card is gone (Stronger decision 5.7).

## 6. Anything that behaved unexpectedly, even unsolved

- **`npm run db:up` from another folder recreates the shared PostgreSQL container.**
  - **What happened:**
    - Docker Compose prints "Container masaha-postgres-1 Recreated";
    - the cause is that the bind mount of `docker/postgres/create-test-database.sql` resolves to that folder's absolute path, so the configuration differs;
    - the data survived, because it lives in the named volume `masaha_masaha-pgdata`, and all seven databases were checked after it;
    - but the container briefly restarted, and its bind mount then pointed at the throwaway clone.
  - **What I did:**
    - before deleting the clone, I re-pointed the container with `docker compose -f C:\Users\basel\masaha\docker-compose.yml up -d --wait` (the main folder's file; no file there was changed);
    - this restarted the container a second time;
    - the mount now points at `C:\Users\basel\masaha\docker\postgres\create-test-database.sql`.
  - **Why it matters:**
    - any worktree that runs `db:up` does the same;
    - if that worktree is later deleted, the container's bind source disappears;
    - this is a candidate finding, from 60, if the owner wants it recorded. I did not record it: it is outside this item's files.
- **One GitHub probe saw the GIF unloaded.** In the 1440 / dark pass the GIF read as not loaded. Two repeat runs at the same mode loaded it, and the raw URL serves 200, `image/gif`, 183,788 bytes. I treat it as a loading-time glitch of the probe.
- **A contact address went to a third-party service.** My first Nominatim request carried the account's email address in its User-Agent, as a contact. That was not needed, and I did not repeat it.

## 7. The early conflict check

`gh pr list --state open` returns **only PR #55** (this one). There is no other open pull request to
run `git merge-tree` against, so there is no conflict. `origin/main` is still `793189a`, so no rebase is needed.

## 8. Each departure from the prompt, with its reason

- **The fresh clone was not in this worktree.** The prompt said "follow them yourself in this worktree, word for word". As approved (5.4), the proof ran in a fresh clone with this folder's ports and a throwaway database. It ran in `C:\Users\basel\masaha-fresh`, not the scratchpad, because of Windows' path limit (§5).
- **Two alt texts changed beyond item 10.** The map's alt now reads "the Gaza Strip on OpenStreetMap tiles, with a pin on each space". The space page's alt now reads "its photos, live status and contacts", because prices and amenities are below the shot's fold. Both are needed for each alt to be true of its image.
- **The repository tree's `.github/` line** now says "three test lanes" instead of "the test lanes". It is the same truth problem as the CI bullet (5.6), now that E2E is named a lane.
- **Arabic slips fixed beyond item 8's list:**
  - «يضيفها الصاحب» → «يضيفها صاحب المساحة»;
  - «حسابات الأصحاب» → «حسابات أصحاب المساحات»;
  - «والموثّق والمتاح الآن» → «والمساحات الموثّقة والمتاحة الآن».
  - The visitors' sentence was rephrased so «الأقرب إليّ» does not repeat.
- **"Run it locally" no longer offers "the API on its own"** in the line that links `setup.md`. The steps above it now start the API.
- **Nothing else.** No finding was folded or opened, no Issue was created, and the design archive in the repository is untouched.

## The data set

**Through the API, as the admin (API on 3322):**
- created `مساحة سنبلة · Sunbula Space` (id 7, تل الهوا);
- saved its hours and prices and hid it (`PUT /admin/spaces/7/hidden`), leaving its amenities and contacts missing;
- registered five owners with `POST /api/v1/auth/register`: هبة سالم, محمد عوض, رنا خليل, يوسف حمدان and سارة النجار, each `@example.com` with a random password;
- for the toast shot, hid Maidan and then showed it again (`PUT /admin/spaces/5/hidden`, `{ "isHidden": false }`).

**By one-off SQL, in `masaha_readme_dev` only, never committed:**

```sql
INSERT INTO space_managers (space_id, user_id, role, created_at, updated_at)
SELECT s.id, u.id, 'OWNER', now(), now()
FROM (VALUES ('manara-space', 'heba.salem@example.com'),
             ('rukn-office', 'mohammed.awad@example.com'),
             ('darb-studio', 'rana.khalil@example.com'),
             ('wasl-desk', 'yousef.hamdan@example.com'),
             ('siraj-coworking', 'sara.najjar@example.com')) AS l(slug, email)
JOIN spaces s ON s.slug = l.slug
JOIN users u ON u.email = l.email;

UPDATE users SET role = 'OWNER'
WHERE email IN ('heba.salem@example.com', 'mohammed.awad@example.com', 'rana.khalil@example.com',
                'yousef.hamdan@example.com', 'sara.najjar@example.com');

UPDATE spaces SET prices_updated_at = now() - interval '45 days' WHERE slug = 'darb-studio';

UPDATE spaces SET hours_updated_at = now() - interval '75 days',
                  amenities_updated_at = now() - interval '75 days'
WHERE slug = 'maidan-space';
```

The other statements, also in the `masaha-postgres-1` container and not part of the data set:
- `DROP DATABASE masaha_readme_fresh_dev WITH (FORCE);` after the fresh-clone proof.

**The admin's list as captured:**

| Space | Status | Owner | Data |
|---|---|---|---|
| Darb | verified | رنا خليل | stale: prices |
| Maidan | unverified | — | stale: hours and amenities |
| Manara | verified | هبة سالم | fresh |
| Rukn | verified | محمد عوض | fresh |
| Siraj | verified | سارة النجار | fresh |
| Sunbula | hidden | — | missing: amenities and contacts |
| Wasl | verified | يوسف حمدان | fresh |

## Items 1–10: what changed

1. **Run it locally:**
   - it now starts with `git clone … && cd masaha`;
   - `npm run dev -w @masaha/api` ("leave it running") is added;
   - a second block starts the web, followed by "Open `http://localhost:5320` and sign in with the admin you seeded";
   - proven word for word (§3).
2. **The test lanes:**
   - "unit (the shared package's included), component, API integration and an end-to-end smoke";
   - CI: "the unit, component and API lanes";
   - the tree's `.github/` line: "three test lanes".
3. **The map:** retaken as in §5, «6 مساحات في كل المحافظات», with Manara's popup.
4. **The space page:** Manara with five photos in the gallery (sources below).
5. **Home, the heroes, home-phone and the GIF:**
   - three available cards: Manara (الرمال، غزة), Rukn (الشيخ رضوان، غزة) and Darb (النصيرات، الوسطى, with «قد يكون تغيّر»);
   - `hero-light` is a light desktop plus a light English phone; `hero-dark` is the dark pair;
   - the GIF goes Arabic light → English light → English dark.
6. **The admin's spaces list:** varied as in the table above. Its menu, dialog, toast and phone shots were retaken on the same data.
7. **The social preview:** remade at 1280×640 (below).
8. **Arabic:**
   - «أصحاب المساحات والاستقبال», «تجيب مساحة», and «الأقرب إليّ» twice (no «القريب منّي» left);
   - plus the slips in §8.
9. **The bilingual section** now begins "Every screen exists in Arabic and English, from one typed copy catalogue: no user-facing string lives in a component."
10. **The hero's alt text** is now "Masaha's home page in Arabic on a desktop, beside the same page in English on a phone", which is true of both images.

## The images, each with its source

**From the prototypes' copy.** This is a scratchpad copy of `docs/design/prototype/`, with the README's data set, real photos and Leaflet 1.9.4 from cdnjs over `tile.openstreetmap.org`. The archive in the repository is untouched.

| File | Screen |
|---|---|
| `hero-light.webp` | Composite: Home (desktop, Arabic, light) beside Home (phone, English, light) |
| `hero-dark.webp` | Composite: Home (desktop, Arabic, dark) beside Home (phone, English, dark) |
| `home-light.webp` / `home-dark.webp` | Home, desktop, Arabic |
| `home-phone.webp` | Home, phone, Arabic |
| `directory-light.webp` | Directory, list |
| `directory-map.webp` | Directory, map, framed on the Strip |
| `space-light.webp` | Space details, Manara, with photos |
| `masaha.gif` | Home: Arabic light → English light → English dark |

**From the running build** (this worktree; API 3322, web 5322):

| File | Screen |
|---|---|
| `app-spaces.webp` | `/dashboard/admin/spaces`, the varied list |
| `app-spaces-menu.webp` | The row actions on Darb |
| `app-spaces-dialog.webp` | Delete Darb: the confirmation |
| `app-spaces-toast.webp` | «أُخفيت مساحة ميدان من الموقع» |
| `app-spaces-phone.webp` | The list on a phone |

**Kept unchanged:** `app-signin`, `app-register`, `app-lookups`, `app-lookups-amenities`,
`owner-light` and `desk-light`.

## The photos (space page), with sources and licences

All five are under the **Unsplash License**: free to use, no attribution required. Each page reads
"Free to use under the Unsplash License". None shows a face, a logo or a business name. The source
files stay in the scratchpad and are not committed.

| Tile | Photo page |
|---|---|
| 1 | https://unsplash.com/photos/modern-dining-area-with-long-tables-and-chairs-BrlIqTYR190 |
| 2 | https://unsplash.com/photos/modern-office-with-desks-and-chairs-oUpLJxufIiM |
| 3 | https://unsplash.com/photos/black-metal-table-and-chairs-kTlUazWP5b0 |
| 4 | https://unsplash.com/photos/a-room-with-a-lot-of-chairs-and-windows-4xyezFffAAg |
| 5 | https://unsplash.com/photos/square-white-wooden-tables-and-chairs-CW88ysx7Amk |

Licence: https://unsplash.com/license

## The social preview (prepared, not applied)

- **File:** `C:\Users\basel\Downloads\readme-assets\social-preview.png`, 1280×640, 205 KB. It replaces the old file.
- **Colours:** the brand's Sea tokens from `primitives.css`.
  - Background: neutral-950 `#0c1315`, with a glow of brand-900 `#023235` and brand-950 `#001d1f`.
  - Accent bar: brand-400 `#50b3b8`, the dark theme's primary.
  - Chips: brand-300 `#85d0d4`.
- **Content:**
  - "Masaha مساحة", the value line and three chips;
  - the dark desktop Home and the English dark phone;
  - every part fits inside the frame (measured: text 72–542 px; desktop 600–1200 × 118–493; phone 1052–1222 × 236–604).
- **The description and topics** prepared in PR #54's report still hold.
