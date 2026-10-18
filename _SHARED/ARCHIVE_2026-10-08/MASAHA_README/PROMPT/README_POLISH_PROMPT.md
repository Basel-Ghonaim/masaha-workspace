# README polish — fix the merged README and its images

**The readme worker** (a one-off worker, named after its task; neither A nor B) · worktree
`C:\Users\basel\masaha-readme`, detached at `origin/main` (`793189a`) and clean · branch
`docs/readme-polish`, cut with `git fetch --prune origin`, then
`git switch --no-track -c docs/readme-polish origin/main`. Its own `node_modules`; databases
`masaha_readme_dev` / `masaha_readme_test` (migrated and seeded, plus the spaces an earlier session
created); API on **3322**, web on **5322** (both `.env` files are set; never print or commit them).
**Docker Desktop stops sometimes on this machine:** if `docker ps` fails, start Docker Desktop, then
`docker start masaha-postgres-1`.

**Size cap:** at most 2 subagents, no self-review subagent, no workflow.
**Plan:** `C:\Users\basel\.prompt\MASAHA_README\PLAN\README_POLISH_PLAN.md` (`write-plan`).
**Report:** `C:\Users\basel\.prompt\MASAHA_README\REPORT\README_POLISH_REPORT.md` (`final-report`).
Follow the skills: `start-work-item` (you are a third worker; your folder is the one above),
`write-plan`, `open-pr`, `final-report`.

## 1. The task in brief

PR #54 rebuilt the root `README.md` as the project's public face, with 20 images in
`docs/assets/readme/`. It is merged, and its structure is right, but an independent review found two
factual errors and several images that weaken it. Fix all of it in **one new PR**. The aim has not
changed: a visitor — an employer, an investor, a developer — should be struck by its quality. The
earlier worker is gone; its scratchpad (the prototypes' copy, its scripts) is gone with it, so you
rebuild what you need.

## 2. Read first

`README.md` and its images as they are on `main`; the earlier prompt and report —
`C:\Users\basel\.prompt\MASAHA_README\PROMPT\README_PROMPT.md` (its decisions all still hold) and
`…\REPORT\README_REPORT.md` (each image's source); CLAUDE.md (its "Claim only what is true" rule
and the README's exception); `docs/project/overview.md`; `docs/project/glossary.md`;
`docs/development/setup.md` (*Commands*); `docs/development/testing.md` §2; `docs/design/README.md`
and `docs/design/prototype/` (`BRIEF.md` first).

## 3. What to fix — the review's list (settled; review it in "Stronger decisions")

**Facts (must fix):**
1. **"Run it locally" does not run.** `npm run dev` starts the web only; without
   `npm run dev -w @masaha/api` (a second terminal) nobody can sign in. Make the steps work as
   written from a fresh clone, and **prove it**: follow them yourself in this worktree, word for word.
2. **The test lanes are wrong.** The README says "unit, component, API integration and the shared
   package"; `testing.md` §2 has **unit** (which covers `packages/shared`), **component**, **API
   integration** and **end-to-end smoke**. Say what the document says.

**Images (must fix):**
3. **The map** (`directory-map.webp`) shows half its frame outside the Strip, with Israeli towns
   labelled in Hebrew. Recapture it **framed on the Gaza Strip alone** (zoom and bounds so nothing
   beyond the Strip's edge carries a label), real OpenStreetMap tiles, the pins on real areas inside
   the Strip, "© OpenStreetMap contributors" visible.
4. **The space page** (`space-light.webp`) shows grey boxes "صورة 1 … صورة 5". Give it **real-looking
   photos of coworking interiors under a free licence** (Unsplash or Pexels licence; no identifiable
   faces, no visible logo or real business name), placed in the prototypes' copy. Record each photo's
   source URL and licence in the report. Never commit the source photos; only the screenshot.
5. **Home and the hero** (`home-*.webp`, `hero-*.webp`, `home-phone.webp`, the GIF) show one card
   under "Available now", leaving two thirds of the row empty. Show **three** spaces there, with
   different areas and states, so the row is full.
6. **The admin's spaces list** (`app-spaces*.webp`): all six rows are unverified, ownerless and fresh.
   Make them **varied**: at least one verified with its owner's name, one hidden, one with stale
   groups, one with missing groups. Data is made through the API where it can be; what the API
   cannot make yet (an owner link, an old date) by **one-off SQL in `masaha_readme_dev` only**, never
   committed — list each statement in the report.
7. **The social preview** (`C:\Users\basel\Downloads\readme-assets\social-preview.png`, 1280×640, not
   committed): its accent bar is blue-violet, not the brand; the phone is cut at the edge. Remake it
   in the brand's own colours (read them from the design system's tokens), nothing cut off.

**Words (must fix):**
8. **Arabic:** «الأصحاب والاستقبال» → «أصحاب المساحات والاستقبال»; «يجيب مساحة» → «تجيب مساحة»;
   one term for near me throughout — the design's «الأقرب إليّ» (the README now mixes it with
   «القريب منّي»). Read every Arabic block again for the same kind of slip.
9. **The bilingual section's first sentence** mixes the README with the interface ("the
   customer-facing screens with an Arabic paragraph under each English one here"). Say only what the
   interface does.
10. **The hero's alt text** says the phone is "in English and dark theme"; in the light image it is
    light. Each `<picture>`'s alt text must be true of both of its images, or name what they share.

**Keep:** the structure, the order of the sections, the identity rules (no university, supervisor,
defence or "graduation project" anywhere — text, image, alt text, metadata), the rights line, the
contacts, the honest line under the gallery, every image under 300 KB, at most about 20 image files.

## 4. Findings and boundaries

- No finding is folded. Number any new one from 60.
- **Your files only:** `README.md`, `docs/assets/readme/`. `CLAUDE.md` needs no change. Workers A and
  B work in their own folders; start no server on 3320, 3321, 5320 or 5321.
- **Repository metadata** (description, topics, the preview) stays prepared, not applied: the owner
  applies it.

## 5. Risks

- **Truth:** the README's exception covers build status only. A count of seats, anything on
  *Not in v1*, or anything the design does not hold is false. A command in "Run it locally" that you
  have not run is a claim you cannot make.
- **Identity:** search your whole diff, the alt texts and the preview for the university before the
  push.
- **Photos:** a licence that requires attribution, or a recognisable person or business, rules a
  photo out.
- **The map:** a frame that still shows a Hebrew or any outside label fails item 3.
- **Consistency:** the same fictional spaces, names and prices in every image, whichever source.

## 6. Phase 4 and the pull request

- **Locally:** `format:check`, the link check by hand (documentation §8), and "Run it locally" run
  word for word. Stop every server afterwards; ports 3322 and 5322 free.
- **The rendered page:** after the push, look at the README on the branch in GitHub, light and dark,
  desktop and phone width.
- **PR:** title `docs(readme): fix the run steps and the images` (≤ 50), labels `docs`, `area:docs`,
  assigned to the owner; 2 commits (the images; the README's text). The analyst reviews it before
  the owner merges. Don't merge.
- **Report** (`final-report`): each item 1–10 with what changed; every image with its source (the
  running app, or the prototypes' copy), the photos' URLs and licences, the SQL statements; the
  rendered-page check.
