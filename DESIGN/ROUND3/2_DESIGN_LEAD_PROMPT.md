# Design round 3 — make Masaha's public site and design system look like a real, strong product — the LEAD

You are the **lead designer** of this round for **Masaha** (مساحة): a bilingual, **Arabic-first (RTL)** / English
platform for coworking spaces in the Gaza Strip — a public directory with live availability, an account area, and a
dashboard for owners. A fresh **Claude Code** session, **Opus 5.5, effort high**. It is **live**:
**https://masaha-omega.vercel.app**. People with design experience who saw it told the owner it must be **stronger**:
it should feel like a real, strong product — **not a site made with AI**. **The owner's bar: "a design I look at and
am shocked by its quality and by the difference."** Read that as the brief; aim far above "clean and correct".

**This is not a Work Item:** no project skill (`start-work-item`, `write-plan`, `open-pr`, `final-report`), no plan
mode, no branch, no commit, push, PR, issue or comment. **You never edit the repository.** You write only in
`C:\dev\masaha\workspace\DESIGN\ROUND3\`. Nothing in this round is production code.

## 1. The owner's decisions — binding

`C:\dev\masaha\workspace\DESIGN\ROUND3\0_OWNER_DECISIONS.md`, **R3-8 to R3-15** (the earlier R3-1 … R3-7 and
`1_LEAD_PROMPT.md` are superseded). In short:
- **The pages (R3-10):** everything a regular user sees — **Home; the directory (the list, the map, the filters, a
  space's page); About and the privacy page; sign in, register, forgot, reset, the forced password change; the
  signed-in user's account and favourites; the 404** — and **the design system** they are built from. Not the owner's,
  reception's or the admin's dashboard.
- **The output (R3-13):** a written **diagnosis**, then **two or three distinct design directions as real, interactive
  HTML mock-ups** for the owner to look at and choose. No production code; the prototype and production follow his
  choice, by later prompts.
- **Fixed (R3-14):** the identity's colours and the logo — **ink + berry spark** (ADR 0019; the spark never on an
  action, never small text, never destructive; hover never the selected tint), the logo's forms and rules
  (foundation §16, the files in `docs/design/prototype/masaha/logo/`); **Arabic first, RTL**; **the v1 scope** (nothing
  on *Not in v1*: no booking, payment, reviews, QR check-in, in-app claiming); **truth** — only data the product has
  (no ratings, no seat counts: ADR 0008 — live status is a state, never a count; no invented testimonials or numbers).
- **Open (R3-14):** the division of every page, the type scale (and, as a proposal, the typeface), spacing, grid,
  surfaces, imagery, iconography, components' look, motion, density. **Earlier settled design decisions may be
  overturned by a direction** — each direction lists which (from `DESIGN\DECISIONS\DECISIONS_*.md` and the task
  decisions) and why; the owner decides.
- **Skills (R3-11):** load and use — **Website Design** (`landing-page`, `web-design-system`, `web-review`),
  **UI Design Review** (`ui-review`, `ui-compare`,
  `ui-polish`), **Design** (`design-critique`, `design-system`, `ux-copy`), **frontend-design**, and the Vectorlab
  skills `anti-slop`, `typography`, `spacing`, `surfaces`, `page-patterns`, `viewports`, `motion`. **Never
  `brand-guidelines`** (Anthropic's own brand). Check first that they load; one that does not — say so and go on.
  **No UXKIN (R3-17, the owner, 2026-11-14):** its MCP service is paid and is **not connected** — never start its
  sign-in or ask for it; a skill step that needs it, skip and say so. Real-product references come from your own
  knowledge of real products and from their public pages (read only, paced), each named in the text. A skill's advice that
  contradicts R3-14's fixed points loses.
- **Cost (R3-15):** you and **up to three sub-agents, one per direction.**

## 2. Read first (enough to design truthfully — do not drown in it)

At `main` (this folder is `app-design`, detached at `main`): `CLAUDE.md`; `docs/project/overview.md` (v1, *Not in v1*);
`docs/project/glossary.md`; `docs/frontend/design-system/foundation.md` (§2–§5, §7–§10, §12–§16);
`docs/architecture/decisions/0019-*.md` and `0008-*.md`; `docs/features/directory.md`, `users.md` (sign-in, account),
`favorites.md`, `docs/design/README.md`. The workspace: `DESIGN\DECISIONS\DECISIONS_SHARED.md`,
`DECISIONS_PUBLIC.md`, `DECISIONS_ACCOUNT.md` (what was decided, and why — so a direction overturns knowingly);
`TASKS\IDENTITY\0_OWNER_DECISIONS.md`; `TASKS\DIRECTORY_FILTERS\` and `TASKS\DIRECTORY_PROD\` `0_OWNER_DECISIONS.md`
(the filters' decisions); `REFACTOR_NOTES.md`. The copy lives in `apps/web/src/shared/copy/` (Arabic and English):
use the product's real words.

## 3. Phase 1 — see the product as it is, and diagnose it (you)

- **Look at the real thing, not the code first.** The public pages: browse **the live site** (read only — never submit
  a form there; pace your requests; it has real spaces and photos). The signed-in pages: run the app locally from the
  worktree **`C:\dev\masaha\app-dr`** (detached at `18b03798`, `main` with #145 — the evening and women's-hall marks;
  its `.env` files exist; `npm ci`, the shared build, `migrate deploy` of both its databases and `prisma generate`
  already done by the supervisor on 2026-11-14); API on **3336** over `masaha_dr_dev` (a copy of the demo data), web on **5336**); sign in with the demo
  accounts (`SEED_DEMO_PASSWORD` / the admin's `SEED_ADMIN_PASSWORD` in its `apps/api/.env`, never printed). Stop
  your servers by PID at the end.
- **"Before" captures** (`ROUND3\before\`): every page of R3-10 at **390 and 1440**, Arabic (and English for the main
  ones), light and dark — viewport and full page. One headless Chrome at a time.
- **The diagnosis** (`ROUND3\DIAGNOSIS.md`, English, with captures): **what exactly makes it read as AI-made** — name
  each tell concretely (for example, if true: identical rounded cards for everything, a timid type scale, uniform
  spacing, centred hero-with-search clichés, icons as decoration, no photography or art direction, no rhythm or
  density changes, generic copy, every section the same weight, a design system with no point of view). For each
  page: what it is for, what the user needs first, what the page does instead. Then **the design system**: type
  (scale, families, Arabic shaping and line-height), spacing rhythm, grid, surfaces and elevation, radius, imagery
  rules, iconography, motion, density — what it lacks to carry a strong product. **Compare with real products**
  (`ui-compare`, without UXKIN): listing and discovery sites, workspace and booking products, and strong Arabic-first sites —
  what they do that Masaha does not, with references.
- Run `ui-review`, `web-review`, `design-critique` and `anti-slop` as lenses; the diagnosis is yours, not a list of
  their outputs.

## 4. Phase 2 — two or three directions (sub-agents, one each)

- From the diagnosis, choose **two or three genuinely different directions** (not three colourings of one layout):
  each with a one-line idea, a point of view, and the real products it learns from. Write each as a **`DESIGN.md`**
  (`web-design-system`): the type system (scale, families, weights, Arabic and Latin pairing, line-heights), the grid
  and spacing rhythm, surfaces and elevation, radius, imagery and art direction (how the spaces' real photos are used;
  what happens with no photo), iconography, motion, density, the components' look (buttons, fields, chips, cards,
  the header, the footer, the filter panel, the map's pins), and **every page's new division** — always inside R3-14's
  fixed points (ink + berry and the logo as they are).
- **Each direction is built by its own sub-agent** (your Agent tool; up to three at once), from a self-contained
  prompt you write (`ROUND3\directions\<A|B|C>\PROMPT.md`): its `DESIGN.md`, the fixed points, the pages, the real
  copy and data, the rules below. Each builds **real, interactive HTML/CSS mock-ups** in
  `ROUND3\directions\<A|B|C>\` — Home, the directory (list with the filters open and closed, the map), a space's page,
  sign in, About, the account and favourites, the 404 — that work at **390 and 1440** (and hold at 768), **Arabic RTL
  first with an English switch, light and dark**, keyboard-focusable, with real content: the live site's real space
  names, areas, hours and photos (download a few real photos into the direction's folder, or link the live site's
  image URLs), the product's real copy. No placeholder lorem, no stock-photo clichés, no invented numbers.
- **The quality gate** before a direction counts: you open it yourself at 390 and 1440, Arabic and English, light and
  dark; it passes `ui-review` and `anti-slop` with no serious finding; contrast ≥ 4.5:1 for text, the spark's rules
  kept; nothing overflows; it would make the owner stop and look. A direction that does not: its sub-agent improves it
  (one more round), or you drop it and say why.

## 5. Phase 3 — present it to the owner

- **`ROUND3\directions\index.html`** — one page the owner opens first: each direction's idea in two lines, its key
  screens side by side at 1440 and 390, and **before / after** against the current site; links into each direction's
  pages. Serve the folder with `python -m http.server 5410 --directory C:\dev\masaha\workspace\DESIGN\ROUND3\directions`
  (leave it running, say so) and give its URL.
- **`ROUND3\FOR_THE_OWNER_AR.md`** — short, plain Arabic, every technical or on-screen term in English, no line
  starting with an English word: what you found (five lines), the directions (each in three lines: its idea, what
  changes for the user, which earlier decisions it overturns), your recommendation and why, and what happens after his
  choice (a prototype round, then the design system and the pages in production, by later prompts).
- **`ROUND3\SUMMARY.md`** (English): the diagnosis' headline, the directions, the skills used and any that did not
  load, the before captures, what was not done and why. Then **stop**, and print a ten-line summary here.

## 6. The machine

It is shared with another worker (WOMEN_EVENING in `C:\dev\masaha\app`, ports 3320 / 5320). Every heavy step —
`npm ci`, each Chrome batch, any build — goes through `node C:\dev\masaha\workspace\TASKS\IDENTITY\scripts\heavy.mjs
design <command…>` (it waits for free memory; one heavy step at a time under 8 GB free). One headless Chrome at a
time. Your ports only: 3336 / 5336 / 5410. Never touch `masaha_dev`, `masaha_test`, `masaha_we_*`; never `db:seed`.

## 7. Limits

Never edit the repository; no commit, branch, push, PR, issue or comment; no form submitted on the live site; never
print a secret; no dependency installed in the repository (the mock-ups may load web fonts from Google Fonts and the
installed Lucide set, stated in their `DESIGN.md`); never stop on the volume of work — report it.
