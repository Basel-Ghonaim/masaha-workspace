# README — Masaha's public face on GitHub

**The readme worker** (a one-off worker, named after its task; neither A nor B) · worktree
`C:\Users\basel\masaha-readme`, detached at `origin/main` (`1333e66`) and clean · branch
`docs/readme`, cut like worker B's: `git fetch --prune origin`, then
`git switch --no-track -c docs/readme origin/main`. Its own `node_modules`; databases
`masaha_readme_dev` / `masaha_readme_test` (migrated and seeded: lookups, the admin, the settings);
API on **3322**, web on **5322** (both `.env` files are set; never print or commit them).

**Size cap:** at most 2 subagents, no self-review subagent, no workflow.
**Plan:** `C:\Users\basel\.prompt\MASAHA_README\PLAN\README_PLAN.md` (`write-plan`).
**Report:** `C:\Users\basel\.prompt\MASAHA_README\REPORT\README_REPORT.md` (`final-report`).
Follow the skills: `start-work-item` (you are a third worker: your folder is the one above),
`write-plan`, `open-pr`, `final-report`.

## 1. The task in brief

Today's `README.md` is three lines. Rebuild it as **the project's official face on GitHub**: a
visitor — an employer, an investor, a developer — should understand in seconds what Masaha is and
why it matters, see it, and be struck by its quality. It is a **product page, not a build log**: it
presents Masaha as designed (v1), and changes only when the architecture or the product's direction
does.

## 2. Read first

CLAUDE.md; `docs/project/overview.md` (the v1 scope and *Not in v1* — never present anything on that
list); `docs/project/glossary.md`; `docs/design/README.md`, `docs/design/SCREENS.md` and the
prototypes in `docs/design/prototype/` (`BRIEF.md` first); `docs/frontend/design-system/foundation.md`
§1–§2 and §13; `docs/architecture/system-overview.md`; ADRs 0001, 0008, 0011, 0012; `docs/development/setup.md`
(*Commands*); `docs/development/workflow.md` §2 *Phases*. The `docs/features/` documents only for the
facts you cite.

## 3. The settled decisions (review them in "Stronger decisions")

**Ownership and identity**
- **Masaha is Basel Ghoneim's own project:** the idea, the plan and the code are all Basel Ghoneim's. **Never mention a
  university, a supervisor, a defence or "graduation project"** — anywhere in the README, its images
  or the repository metadata you prepare.
- **Rights:** "© 2026 Basel Ghoneim. All rights reserved." No licence file.
- **Contact:** `baselghonaim@gmail.com` and LinkedIn
  `https://www.linkedin.com/in/basel-ghonaim`, with the GitHub profile.

**Language**
- **English throughout**, with **Arabic beneath the explanatory parts only** — the introduction, the
  problem and the idea, and each audience's short description: an Arabic rendering of the paragraph
  above it in `<div dir="rtl" lang="ar">`, so GitHub lays it out right to left. The technical parts
  (stack, architecture, quality, running it, structure, documents) are English only.

**What the README is — and an exception to state**
- It describes **the product as designed**: the v1 scope, the three audiences, the design. It names
  no build status, no "built / planned" labels, no roadmap dates. **Write the exception into
  `CLAUDE.md`'s rule "Claim only what is true"**, in one sentence: the root `README.md` presents
  Masaha as designed (its v1 scope) rather than its build state, and never states that a feature is
  built. It is still bound by everything else: nothing on *Not in v1*, nothing the design does not
  hold.
- **True to the decisions:** live status is a state (available, full, closed), **never a count of
  seats** (ADR 0008 — today's README says "live available seats": wrong); the dashboard serves owners,
  **their reception staff** and the admin; "near me" never sends the device's location to Masaha.

**The sections, in this order** (your plan may refine the wording, not drop a part):
1. **Header:** the name «Masaha · مساحة», one true value line, a few honest badges (CI status, live
   from GitHub; Node 24; TypeScript), the rights line.
2. **Introduction** + Arabic.
3. **Hero image** (§4).
4. **The problem and the idea** + Arabic: why Gaza's students and freelancers depend on coworking
   spaces (power, internet), why the information is scattered and stale, what Masaha gives instead.
5. **What it offers**, by audience — visitors (directory, map, near me, filters, live status, space
   page), owners and reception (front desk, visits, subscriptions, payments, announcements), the
   admin (spaces, owners, lookups, reports) — each with a short Arabic description.
6. **Screens** (§4).
7. **Bilingual, both directions, accessible:** the same screen in Arabic and English side by side
   and/or the GIF; the copy catalogue, logical directions only, contrast, keyboard, axe in tests.
8. **Tech stack:** web, API, shared, tooling, each a short list; link ADR 0001.
9. **Architecture at a glance:** a small **Mermaid** diagram (one web app for the site and the
   dashboard, the levelled modular monolith, PostgreSQL, the shared package), linking
   `system-overview.md`.
10. **Engineering quality:** short, true, linked: server-side authorization tested per role, the ADRs,
    the four test lanes and "seen failing first", the CI checks, the one-layer design system with
    semantic tokens, the build check that keeps dashboard code out of the site's first download.
11. **Run it locally:** prerequisites and about five commands, linking `setup.md`.
12. **Repository structure:** a five-line tree.
13. **Documentation:** the map, the ADRs, the capability documents, the build plan.
14. **Author and contact.**
15. **Rights.**

## 4. The images — the heart of it

- **Two sources, one look:**
  - **screens that run today** (sign-in and register, the dashboard shell, the admin's lookups with
    the amenities, the admin's spaces list with its filters, menu, dialog and toast) — captured from
    **this worktree's running app** (API 3322, web 5322);
  - **screens not yet running** (home, directory, the map, the space page, the owner's dashboard,
    the front desk) — captured from **the design prototypes** (`docs/design/prototype/`, real HTML on
    the real design system), served from **a copy in your scratchpad, never committed** (the archive
    is a frozen record).
  - **One honest line under the gallery,** static and always true: "Screens from Masaha's product
    design and its running build."
- **The map must look real:** in the scratchpad copy of the prototypes, replace the map illustration
  with **real OpenStreetMap tiles of the Gaza Strip** (Leaflet from a CDN, in the copy only), the
  pins on real areas, and **"© OpenStreetMap contributors" visible** in the shot.
- **One data set for both sources:** fictional but realistic spaces (names that sound like Gaza's,
  never a real business's name; areas from the seeded lookups; plausible prices in ILS, hours,
  amenities). Create them in `masaha_readme_dev` **through the API** (as the admin), and use the same
  names in the prototypes' copy. No real person's data; e-mails on `example.com`.
- **Curated, not random:** fixed sizes (desktop 1440×900, phone 390×844), no browser chrome, the same
  zoom; pairs that each tell one thing (Arabic beside English, light beside dark, phone beside
  desktop); a caption under each.
- **Professional touches:**
  - a **composite hero** (desktop in Arabic and light beside a phone in English and dark);
  - **theme-aware images** with `<picture>` (the dark shot for GitHub's dark mode);
  - **one short GIF** (≤ 3 MB): switching the language flips the direction, then the theme;
  - galleries beyond the essentials in `<details>`, so the page opens short.
- **Files:** `docs/assets/readme/`, WebP (≤ 300 KB each), alt text on every image. **At most about 20
  image files** in all, the GIF included — choose; the PR must stay under 25 files.
- **Repository metadata** (prepared, **not applied**): a one-line description, about eight topics, and
  a social-preview image (1280×640) saved to `C:\Users\basel\Downloads\readme-assets\` (not
  committed). The owner applies them.

## 5. Findings and boundaries

- No finding is folded. Number any new one from 60.
- **Issue #53** (the university in `CLAUDE.md`, the plan and ADR 0014) is separate: in `CLAUDE.md`
  touch only the one sentence of §3, nothing of its mission paragraph.
- **Your files only:** `README.md`, `docs/assets/readme/`, `CLAUDE.md`'s one sentence. Workers A and B
  work in their own folders; touch nothing of theirs, start no server on 3320/3321/5320/5321.

## 6. Risks — read before you start

- **Truth.** The exception covers build status only. A feature on *Not in v1* (online payment, QR
  check-in, in-app claiming, booking, reviews), a seat count, or anything the design does not hold
  would be false. Check every claim against `overview.md` and the design.
- **Identity.** One mention of the university anywhere — text, image, alt text, metadata — fails the
  item. Search your own diff for it before the push.
- **Images.** Real map tiles need their attribution; no real business names; no secrets, tokens or
  real e-mails in a shot; the design archive is never edited in the repository.
- **Links.** Every relative link and image path resolves on GitHub (check them on the pushed branch's
  rendered page, both themes).
- **Weight.** Keep the README's images light: the page must open fast on a weak connection.

## 7. Phase 4 and the pull request

- **Locally:** `format:check` and the link check by hand (documentation §8) — no code changes. The
  real run here is the app you start for the shots; stop every server afterwards and check ports
  3322 and 5322 free.
- **The rendered page:** after the push, look at the README on the branch in GitHub, light and dark,
  desktop and phone width; fix what renders badly before you report.
- **PR:** title `docs: rebuild the README as the project's face` (≤ 50), labels `docs`, `area:docs`,
  assigned to the owner; 2–3 commits (the images; the README with `CLAUDE.md`'s sentence).
- **Report** (`final-report`): add the prepared metadata (description, topics, the preview's path)
  and a list of every image with its source (running app or prototype copy). The analyst reviews it.
  Don't merge.
