# Design fix 3 — the public site, in the prototype

**The public design fixer** (one-off, named after its task; a second design worker beside the one in
`masaha-design`) · worktree `C:\Users\basel\masaha-design-public`, detached at `origin/main`
(`068efc6`) · branch `design/public`, cut with `git fetch --prune origin`, then
`git switch --no-track -c design/public origin/main`. **Nothing is installed here, on purpose:** no
`npm ci`, no database, no `.env`. Serve the prototype on **port 5347** with
`python -m http.server 5347 --bind 127.0.0.1` from `docs/design/prototype` (it keeps every `?…`
parameter, and needs no download).

**Model:** Opus 5.5, effort high. **Size cap:** at most 2 subagents, no workflow.
**Plan:** `C:\Users\basel\.prompt\MASAHA_DESIGN\PLAN\FIX_PUBLIC_PLAN.md` (`write-plan`; save, then stop).
**Report:** `C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\FIX_PUBLIC_REPORT.md` (`final-report`).
**Before/after images:** `C:\Users\basel\Downloads\design-fix-public\` (not committed).
Follow the skills: `start-work-item` (you are a task worker; your folder is the one above),
`write-plan`, `open-pr`, `final-report`.

## 1. The task in brief

Batch 3 of the design review — the public site (Home, the Directory, the space page, About, the
errors) — is decided. Apply its decisions to the prototype, as the owner amended them on 2026-10-12.
Another design worker builds batch 2b (the admin's pages) in parallel: see §6.

## 2. Read first

1. **The decisions:** `C:\Users\basel\.prompt\MASAHA_DESIGN\DECISIONS_PUBLIC.md` — its **Amended
   2026-10-12** note first (no amenity filter; a space's own amenities shown exactly as the common
   ones; the card keeps its four price cells beside the photo; no price of 0), then U1–U12 and the
   smaller items. Apply only what is marked **prototype**.
2. **Already settled:** `DECISIONS_SHARED.md` (P1 as amended, P5 and its Directory exception, P6–P9,
   SH-005, SH-007, SH-021) and `docs/design/CHANGES.md` (batches 1 and 2a: what is already built, the
   shared `FilterSheet` with its `wide` prop, the check scripts).
3. **The review behind them:** `C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\REVIEW_PUBLIC_REPORT.md`
   (PU-001 … PU-029, with frames and evidence).
4. **What the API holds** (the screens must not promise otherwise): `docs/features/spaces.md` and
   `lookups.md`; `docs/api/api-contract.md` › *Lookups (public)* and *Spaces (the admin)* (the facts a
   space has); `docs/architecture/data-model.md` › *Spaces* and the live-status rule (ADR 0008: a
   state, never a count); `docs/plans/v1-mvp.md` › the planned `GET /spaces` row (no `amenities`
   filter from now on). For the own amenities: `C:\Users\basel\.prompt\MASAHA_AMENITIES\PLAN\AMENITIES_PLAN.md`
   (being built: Arabic name required, English optional).
5. `docs/design/README.md` (its *check scripts* paragraph), `INDEX.md`; foundation §5, §7–§10, §12;
   `docs/project/glossary.md`; `docs/project/overview.md` (*Not in v1*).
6. The prototype's source: `Home.html`, `Directory.html`, `Space details.html`, `About.html`,
   `Error.html`, and `masaha/shared.jsx`, `space-parts.jsx`, `location.jsx`, `map.jsx`, `data.js`,
   `details-data.js`, `masaha.css`.

## 3. The settled decisions (review them in "Stronger decisions")

- **H1 — U1–U11 as the file says** (the place filter as one grouped multi-select of areas; one
  «الأقرب إليّ» control and one state line; one name per space; one freshness rule; the price filter;
  the map on a phone; placing a pin by hand; the space page's one order; prices per audience; who
  reads a report; About), and the smaller items under each heading.
- **H2 — U12, the cover photo on the card** (Home, the Directory, and every list of space cards): the
  space's first photo at a fixed ratio, lazy-loaded, a small thumbnail; a space with no photo shows its
  mark (the first letter of its name, as the dashboard's switcher, SH-006) in the same frame. **The
  card keeps all four price cells** beside the photo (the owner's answer). Design it for a weak
  connection: nothing jumps when the photo arrives.
- **H3 — no amenity filter:** the Directory's amenity group leaves its filters (the sidebar and the
  sheet), and nothing else on the public pages offers amenities as a filter.
- **H4 — own amenities show as the common ones:** on the space page (and anywhere amenities show), a
  space's «مرافق إضافية» sit in the same list, in the same style, after the common ones; no second
  section. An own amenity has no icon of its own: it takes one neutral mark that the list's layout
  already allows. Give the sample spaces a few own amenities, Arabic only for one of them, so the
  English interface shows how an Arabic-only name reads there.
- **H5 — no free price:** every price shown is above zero; a free event belongs in the space's
  announcements. If any frame shows «0 ₪» or «مجانًا», remove it.

## 4. Stay alert: new design issues

Report any new defect or better design — never silently fixed or ignored: in the plan's **"Design
issues"** (`write-plan`), or, once building, in the report's **"New design issues"**, each with the
frame, what is wrong, the better solution from the design system, and its level. Build none unless
the reply approves it.

## 4b. The owner's additions

A change **inside** a decision you apply — make it. A **new** change — say it goes to the analyst
first. List every addition in the report's **"Owner's additions"**.

## 5. Risks

- **Truth to the product:** live status is a state, never a count (ADR 0008); the device's location is
  never sent anywhere; nothing from *Not in v1* (booking, reviews, online payment).
- **Your checks' limit:** the two scripts and a load matrix see blanks and errors, not layout; #59's F2
  and #61's eleven fixes were found by eyes. Look at every changed page at 390, **768** and 1440, in
  both languages and themes.
- **The repository:** touch nothing outside `docs/design/`.

## 6. Boundaries with the other design worker (the parallel-work rule)

The design fixer in `masaha-design` builds **batch 2b** on branch `design/admin-rest`. Its files:
the eight admin pages, `Admin space edit.html`, `masaha/admin.jsx`, `admin-data.js`, `profile-b.jsx`.
**You edit none of them.** It does not touch `shared.jsx`, `data.js`, `details-data.js` or the public
pages, which are yours. Shared by both, each in its own section: `docs/design/CHANGES.md` (your
*Batch 3* section), `INDEX.md` (your rows), and the board `Flows - states.html` (your frames only).
Whichever PR merges second rebases and keeps both sides (the fast path). If you need one of its files,
stop and say so in the plan. Workers A and B and the amenities worker are outside `docs/design/`.

## 7. Phase 4 and the pull request

- **Checks:** the two scripts at every commit — `node docs/design/scripts/check-parse.mjs` and
  `check-classes.mjs` (Node's own modules; nothing to install). `format:check` and `check:links` need
  the repository's packages, which this worktree does not install: **CI runs them**; say so in the
  report and wait for CI green.
- **Real run:** every page you changed, at 390, 768 and 1440, Arabic and English, light and dark;
  before/after pairs in the images folder, named after the decision (`H2-home-390.png`). The server and
  any browser stopped and port 5347 checked free. Stop every background shell you start; `jq` is not
  installed — use `gh … --jq`.
- **The archive's documents:** a *Batch 3* section in `CHANGES.md`, one line per applied decision;
  `INDEX.md` for every URL or parameter you add or rename.
- **PR:** title `design: the public site` (≤ 50), labels `docs`, `area:docs`, assigned to the owner;
  commits grouped by decision (≤ 50 characters each — count them). The analyst reviews it. Don't merge.
