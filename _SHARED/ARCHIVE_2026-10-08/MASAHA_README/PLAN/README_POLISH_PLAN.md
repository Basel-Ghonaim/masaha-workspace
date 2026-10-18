# Plan — README polish: fix the run steps and the images

Saved, once approved, to `C:\Users\basel\.prompt\MASAHA_README\PLAN\README_POLISH_PLAN.md`.

## 1. Summary

PR #54's README stays as it is built: the same structure, the same sections in the same order, the same 20 image files. This item fixes two wrong facts, retakes 14 of the images, rebuilds the social preview and corrects the words. The facts are the run steps, which never start the API, and the test lanes. The retaken images are the map, the space page, the home row and the admin's spaces list. The words are the Arabic, the bilingual paragraph and the hero's alt text. Branch `docs/readme-polish`, one PR, two commits.

## 2. Contract

**Scope:** items 1–10 of the prompt, in `README.md` and `docs/assets/readme/` only, plus the social preview, which is kept outside the repository.

**Acceptance criteria**
- [ ] "Run it locally" starts both the API and the web. I follow it word for word from a fresh clone and reach a signed-in session as the seeded admin.
- [ ] The test lanes match `testing.md` §2: unit (with `packages/shared`), component, API integration and end-to-end smoke. The CI bullet names only the lanes CI actually runs.
- [ ] The map shows the Gaza Strip alone. It uses real OSM tiles, puts pins on real areas and shows "© OpenStreetMap contributors". Nothing outside the Strip carries a label.
- [ ] The space page shows five real-looking coworking photos. Each is under the Unsplash or Pexels licence, with no faces and no logos. Each one's URL and licence goes in the report. None is committed.
- [ ] Home, the hero, home-phone and the GIF show three cards under «متاحة الآن», each in a different area and with a different state.
- [ ] The admin's spaces list is varied. At least one space is verified with its owner's name. Others are hidden, stale and missing. Each SQL statement goes in the report.
- [ ] The social preview is 1280×640, in the brand's own colours, with nothing cut off.
- [ ] The Arabic slips are fixed, «الأقرب إليّ» is used throughout, the bilingual sentence describes only the interface, and every `<picture>` alt text is true of both of its images.
- [ ] I keep the identity rules, the rights line, the contacts, the honest gallery line, every image under 300 KB and about 20 image files.

**Out of scope:** `CLAUDE.md`, the design archive in the repository, any code, applying the repository metadata, and the six images that stay as they are (`app-signin`, `app-register`, `app-lookups`, `app-lookups-amenities`, `owner-light`, `desk-light`).

## 3. Reading done

- CLAUDE.md, workflow, the documentation map, and the findings index (titles).
- The prompt and the earlier prompt and report.
- `overview.md`, `glossary.md`, setup (*Commands*, *First run*, *Running a second folder*), testing §1–§2 and §5, and documentation §8.
- README.md, and the images: the map, home, the space page, the spaces list, the hero and the preview.
- With one Explore agent: the prototype's `BRIEF.md`, `data.js`, `details-data.js`, `space-parts.jsx`, `map.jsx` and `Home.html`; the spaces API (routes, `can.ts`, `staleness.ts`, schema columns); the admin list's columns and badges; and the brand tokens in `primitives.css` / `semantic.css`.

## 4. The settled decisions, as they will be built

**Item 1, Run it locally:**

```bash
git clone https://github.com/Basel-Ghonaim/masaha.git && cd masaha
npm ci                                   # every workspace, and the Prisma client
cp apps/api/.env.example apps/api/.env   # then set JWT_SECRET, SEED_ADMIN_EMAIL, SEED_ADMIN_PASSWORD
npm run db:up                            # PostgreSQL in Docker, on host port 5433
npm run db:migrate && npm run db:seed    # the schema; the lookups, the admin and the settings
npm run dev -w @masaha/api               # the API on http://localhost:3320; leave it running
```

Then, in a second terminal, `npm run dev` starts the web on `http://localhost:5320`, which forwards `/api` to the API. Open that address and sign in with the admin you seeded. The repository is public (checked with `gh repo view`), so the clone line is true.

**Item 2, the test lanes.** The README will say "Four test lanes — unit (the shared package's included), component, API integration and an end-to-end smoke". The CI bullet will read "lint, format, typecheck, the unit, component and API lanes, the class checks and the build". testing §5 says E2E runs locally before a release, not in CI.

**One data set across both sources.** These are the six existing fictional spaces plus one hidden space. Names, areas and prices stay as on `main`.

| Space | Area | Public (prototype copy) | Admin list (running app) |
|---|---|---|---|
| مساحة المنارة · Manara Space | الرمال | verified, available | verified, owner shown, fresh |
| ركن المكتب · Rukn Office | الشيخ رضوان | verified, available | verified, owner shown, fresh |
| درب الاستوديو · Darb Studio | النصيرات | verified, available, prices «قد يكون تغيّر» | verified, owner shown, prices **stale** |
| مكتب وصل · Wasl Desk | دير البلح | verified, full | verified, owner shown, fresh |
| سراج للعمل المشترك · Siraj Coworking | خان يونس | verified, closed now | verified, owner shown, fresh |
| مساحة ميدان · Maidan Space | شمال قطاع غزة | unverified, no live status | unverified, hours and amenities **stale** |
| مساحة سنبلة · Sunbula Space (new) | an active seeded area | not public (hidden) | **hidden**, unverified, amenities and contacts **missing** |

**Item 6, the admin's data.**
- **Through the API, as the admin:**
  - create Sunbula, save its profile, hours and prices, and hide it (`PUT …/hidden`);
  - register the five owners (`POST /api/v1/auth/register`, fictional Arabic names, `@example.com`).
  - Every fact edit happens before any owner link: once a space is verified, only its owner may edit it.
- **By one-off SQL, in `masaha_readme_dev` only, never committed:**
  - insert the five `space_managers` OWNER links;
  - set those five users to `users.role = 'OWNER'`;
  - backdate Darb's `prices_updated_at` by 45 days (past the 30-day price threshold);
  - backdate Maidan's `hours_updated_at` and `amenities_updated_at` by 75 days (past the 60-day threshold).
  - Each statement, word for word, goes in the report.
- I check the spaces the earlier session created first, and adjust only what the table needs.

**Item 3, the map.** In a scratchpad copy of the prototypes:
- Leaflet 1.9.4 from cdnjs, over `tile.openstreetmap.org`.
- `fitBounds` on the Strip.
- An **inverse mask**: a polygon of the whole frame with the Strip's outline cut out of it, filled opaque with the page's muted surface colour. Nothing beyond the Strip's edge stays visible, labels included.
- Pins on Rimal, Sheikh Radwan, Jabalia/North, Nuseirat, Deir al-Balah and Khan Younis.
- The attribution stays visible.

**Item 4, photos.**
- Five Unsplash or Pexels photos of empty coworking interiors: no faces, no logos, no readable signage.
- They are downloaded into their own scratchpad folder, and `PhotoTile` in the copy shows them as `<img>`.
- Each URL and licence goes in the report.

**Item 5, the home row.** In the copy's `data.js`:
- Manara, Rukn and Darb are verified and open, so `Home.html`'s filter (`verified && status === 'open'`) gives three cards.
- **"Different states"** is built as the card's own states, all true under «متاحة الآن»: Darb's prices carry «قد يكون تغيّر», and the three cards have different areas, prices and hours. A full or closed space in an "available now" row would be false.
- Retake `home-light`, `home-dark`, `home-phone`, both heroes and the GIF.
- Also retake `directory-light`, `directory-map` and `space-light`, so that verified states agree in every shot.

**Item 7, the social preview.** I rebuild it as a scratchpad HTML page and capture it at 1280×640.
- **Background:** neutral-950 `#0c1315` with a brand-950 `#001d1f` glow.
- **Accent bar:** brand-400 `#50b3b8`, the dark theme's primary.
- **Picture:** the new composite hero, scaled to sit fully inside the frame with margins.
- It goes to `C:\Users\basel\Downloads\readme-assets\social-preview.png` and replaces the old file.

**Items 8–10, words.**
- «الأصحاب والاستقبال» → «أصحاب المساحات والاستقبال».
- «يجيب مساحة» → «تجيب مساحة».
- Both «القريب منّي» become «الأقرب إليّ», and the visitors' sentence is rephrased so the term does not repeat.
- **Same kind of slip, found in the full read:**
  - «يضيفها الصاحب» → «يضيفها صاحب المساحة»;
  - «حسابات الأصحاب» → «حسابات أصحاب المساحات»;
  - «والموثّق» → «والمساحات الموثّقة».
- **Item 9:** "Every screen exists in Arabic and English, from one typed copy catalogue: no user-facing string lives in a component."
- **Item 10:** the hero's alt text becomes "Masaha's home page in Arabic on a desktop, beside the same page in English on a phone" (see 5.2).

**Capture.**
- Use Chrome's headless mode over CDP (memory: the Node script, no dependency).
- **Size (owner's reply):** desktop shots are **1280×800** and phone shots 390×844, matching the six kept images. They are WebP via Pillow, each ≤ 300 KB, with no metadata.
- **The map (owner's reply):**
  - the mask's fill is the page's own muted surface, so the Strip reads as the map, not as a cut-out;
  - neither the mask, a pin nor the popup covers "© OpenStreetMap contributors";
  - both are checked at full size before compression.
- **Servers:**
  - the API on 3322;
  - the web on 5322;
  - a static server for the copy on 5330.

## 5. Stronger decisions

1. **The map: a mask, not just zoom.**
   - **What:** add the opaque inverse mask on top of `fitBounds`.
   - **Why:** the Strip runs diagonally. Any rectangle that holds all six pins also holds Israeli and Egyptian land in its corners, so zoom and bounds alone cannot meet item 3.
   - **Cost:** one polygon of about 25 points in the copy; no change to the repository.
   - **Recommendation:** do it.
2. **The hero in one theme per image.**
   - **What:** `hero-light` shows a light desktop with a light phone, and `hero-dark` shows both dark. Today each composite mixes themes, and its alt text described one of them wrongly.
   - **Why:** each composite then matches GitHub's theme, and one alt text, naming only language and device, is true of both images. Light against dark is already shown by the Home pair and the GIF.
   - **Cost:** none.
   - **Recommendation:** do it.
3. **"Different states" under «متاحة الآن» means three available cards that differ.**
   - **What:** Darb's stale-price note, plus different areas and prices. I do not put full or closed cards in the row.
   - **Why:** the row's own filter and title make a full or closed card false.
   - **Cost:** none.
   - **Recommendation:** do it. **This is the one place I read the prompt differently. Please confirm.**
4. **Prove item 1 from a real fresh clone, not from this worktree.**
   - **What:** `git clone` the pushed branch into the scratchpad and type every command as written.
   - **The one departure:** before `db:migrate`, the copied `.env` files get this folder's settings from setup's *Running a second folder* (PORT 3322 and CORS 5322; WEB_PORT 5322 and the proxy on 3322) and a database of its own, `masaha_readme_fresh_dev`. `migrate dev` creates it.
   - **Why:** running the steps in this worktree would overwrite its configured `.env`. Its database is already migrated, so nothing fresh would be proven. The defaults (3320/5320 and `masaha_dev`) belong to worker A and are forbidden.
   - **Cost:** about 5 minutes of `npm ci`. I drop the fresh database afterwards and delete the clone.
   - **Recommendation:** do it.
5. **Add the clone line.**
   - **What:** the steps start with `git clone … && cd masaha`.
   - **Why:** "from a fresh clone" then starts at the start.
   - **Cost:** one line.
   - **Recommendation:** do it.
6. **Fix the CI bullet too (item 2's twin).**
   - **What:** the bullet names the lanes CI runs instead of "the test lanes".
   - **Why:** once E2E is named a lane, "the test lanes" in the CI bullet would claim CI runs E2E, and it does not.
   - **Cost:** a few words.
   - **Recommendation:** do it.
7. **Browse-by-area on Home.**
   - **What:** the copy's Home shows «النصر — 0 مساحات» today. I make it show only areas that hold spaces.
   - **Why:** an empty area card weakens the same image item 5 fixes.
   - **Cost:** one data edit in the copy.
   - **Recommendation:** do it.
8. **The hidden space as a seventh space, Sunbula.**
   - **What:** add Sunbula as a seventh space rather than hiding one of the six.
   - **Why:** a hidden space is never public, so the public shots keep their six, and the API can only make a "missing" group on a new space.
   - **Cost:** one more row in the admin's list.
   - **Recommendation:** do it.

None of these contradicts or weakens a rule of the documents.

## 6. Related findings

- **#37, links checked by hand:** I apply it (the link check by hand), but do not fold it, as the prompt says.
- No other open finding touches the README.
- A new finding, if any, is numbered from 60.

## 7. Files

- **Changed:** `README.md`; in `docs/assets/readme/`: `hero-light`, `hero-dark`, `home-light`, `home-dark`, `home-phone`, `directory-light`, `directory-map`, `space-light`, `app-spaces`, `app-spaces-menu`, `app-spaces-dialog`, `app-spaces-toast`, `app-spaces-phone` (`.webp`) and `masaha.gif`. That is 15 files.
- **Not in the repository:**
  - the prototypes' copy, the photos, the scripts and the fresh clone (scratchpad);
  - the preview (Downloads);
  - the SQL (report only);
  - the `.env` files, never printed.
- **No other layer's files and no shared files.** Workers A and B are untouched, and ports 3320, 3321, 5320 and 5321 are never used.

## 8. Lanes and tests

There is no code and no behaviour, so no lane and no test. These checks stand in for them:
- the fresh-clone run (item 1);
- a Pillow check of every image (size, blankness, ≤ 300 KB);
- a map check by eye against item 3;
- the link check;
- the rendered page.

## 9. Review Focus

These are things no check exercises:
- the Arabic's correctness as a reader would judge it;
- that the photos show no face or logo at full size;
- that the masked map still reads as a map;
- that the new data set agrees across all 14 retaken shots;
- that the Mermaid diagram draws for a signed-in viewer (the earlier report could not confirm it).

## 10. Commits

1. `docs(readme): retake the screenshots`: the 14 images in `docs/assets/readme/`.
2. `docs(readme): fix the run steps and the wording`: `README.md`.

The PR title is the prompt's, `docs(readme): fix the run steps and the images`, which covers both commits. Each commit is staged by path, with no attribution.

## 11. Verification (phase 4)

**Run:**
- `npm run format:check`.
- The link check by hand: every relative path in `README.md` exists.
- "Run it locally", word for word, in the fresh clone (5.4), up to signing in. Then stop it, drop `masaha_readme_fresh_dev` and delete the clone.
- **The identity search:** `university|Al-Quds|القدس المفتوحة|جامعة|graduation|تخرج|supervisor|مشرف|defence|مناقشة` over the diff and the alt texts, and an eye check of the preview.
- **After the push:** the branch's README on GitHub, light and dark, at 1440 and 390 width, including the Mermaid diagram.
- All servers stopped; ports 3322, 5322 and 5330 checked free.
- **Docker:** if `docker ps` fails (it fails now), start Docker Desktop, then `docker start masaha-postgres-1`.

**Not run:** lint, typecheck, build, check:build and the lanes. This is a no-code change (workflow §2, phase 4's exception); CI runs them.

## 12. Decisions from the owner (README_POLISH_PLAN_REPLY.md)

All approved:
1. **5.3:** three *available* cards that differ.
2. **5.4:** prove item 1 in a fresh clone, with this folder's ports and a throwaway `masaha_readme_fresh_dev`. Afterwards I drop the database and delete the clone. The report names the two settings that differed from the README's defaults (the ports and the database), and why.
3. **5.8:** Sunbula as a seventh, hidden space.
4. The new social preview replaces the old file.

The reply also adds two things, both folded into §4 *Capture*:
- shots at **1280×800**;
- the mask's muted-surface fill, with the attribution never covered.

Don't merge.
