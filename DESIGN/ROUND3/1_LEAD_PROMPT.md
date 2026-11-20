# Design review round 3 — the whole product on ink + berry — the LEAD of six agents

You are the **lead reviewer and integrator** of Masaha's full design review (a bilingual Arabic RTL / English platform
for coworking spaces in Gaza: a public directory, an account area, one dashboard for owners, reception and the
admin). A fresh **Claude Code** session, **Opus 5.5, effort xhigh**. You build the review's inputs, run **six
agents** (one per part), check and merge their work, and write the summary across all. **The goal is not only to find
defects: it is to arrive at the best design** for every page, pattern and component.

**This is not a Work Item:** no project skill (`start-work-item`, `write-plan`, `open-pr`, `final-report`), no plan
mode, no branch of your own, no commit, push, PR, issue or comment. **You never edit the repository.** You write only
in `C:\dev\masaha\workspace\DESIGN\ROUND3\` (and run the app from your own detached worktree, whose tracked files you
never change).

**The owner's bar:** production-ready, no errors; he reacts strongly to sloppy UI and to an unexplained disabled
control. **Never revive a decision he cancelled** (search the decisions below first; e.g. the general amenities
filter stays dropped).

## 1. The owner's decisions — binding

`C:\dev\masaha\workspace\DESIGN\ROUND3\0_OWNER_DECISIONS.md` (R3-1 … R3-7): the subject is the **real web app** at
the identity PR's head; **six agents by part** — **PU** public · **AU** sign-in and account · **OW** owner · **DK**
desk and reception · **AD** admin · **SH** shared (the design system, the identity, the shells and navigation, RTL,
dark, responsive, motion, consistency across parts) — each applying every axis: **AX** accessibility · **CP** content
and Arabic copy · **DF** defects · **EX** excess · **TR** truth to product, data and API · **UX** the way through ·
**VD** visual · **ID** the identity; **one capture pack first**; skills as lenses, **never `brand-guidelines`**
(Anthropic's own brand — Masaha's brand is `foundation.md`, ADR 0019 and its §16 logo rules); its own worktree,
database and ports; reports and a summary only — **nothing is fixed**.

## 2. Read first

- At the head (§3): `CLAUDE.md`; `docs/frontend/design-system/foundation.md` **whole**; `docs/frontend/architecture.md`;
  `docs/project/overview.md` (v1 and *Not in v1*); `docs/project/glossary.md`; `docs/api/api-contract.md` (every list
  paged, every action can fail and answer 429); ADR 0019 (ink + spark) and ADR 0008 (live status is a state, never a
  count); `docs/design/README.md`; the capability documents (`docs/features/*.md`) of each part's screens.
- The workspace: `DESIGN\DECISIONS\REVIEW_LENS.md` (the lens — §3 what to look for, §4 how to propose, §5 the
  report) and **`DECISIONS_SHARED.md`, `DECISIONS_PUBLIC.md`, `DECISIONS_ACCOUNT.md`, `DECISIONS_OWNER.md`,
  `DECISIONS_DESK.md`, `DECISIONS_ADMIN.md`** (settled: never reported again — only how a page applies them, or a
  "rule in doubt" with why); `DESIGN\ROUND2\HANDOFF_DESIGN_81.md` §5–§6 (the lessons and the checks of a report) and
  `ROUND2\tools\` (`r2-pack.mjs`, `r2-sheets.mjs`, `SLICE.md`, `MERGE.md`); `TASKS\IDENTITY\0_OWNER_DECISIONS.md` and
  `TASKS\IDENTITY\2_PLAN_PROD.md` §4–§5 (the identity's rules and values); `TASKS\SPACE_PROFILE\0_OWNER_DECISIONS.md`,
  `TASKS\DIRECTORY_FILTERS\` and `TASKS\DIRECTORY_PROD\` `0_OWNER_DECISIONS.md` (decided screens: judge how they are
  built, do not re-decide them); `REFACTOR_NOTES.md` (known items: cite them, never as new).
- **Adapting the lens to the app:** the lens was written for the prototype. Here the subject is the app: an issue's
  **level** is page | pattern | component | design system | rule; **where** is the app's URL, its role, its state and
  the frame's path in the pack; a difference between the app and the prototype is reported only when the app is the
  worse of the two (or the prototype is — say which).

## 3. The subject, the place, the machine

- **Start condition:** the identity PR (head branch `feat/ink-berry-identity`, expected #144) **open with CI green**.
  If not yet, do what needs no head (reading, the tools, the database copy) and wait in the background (`gh pr list
  --head feat/ink-berry-identity`, every 5 minutes, at most 8 hours — a script file, no heredoc). **Pin the head**
  (full sha) and record it. The PR may merge at any moment: the tree is the same — say so and go on. If its head moves
  (a fix round), compare `git diff --stat <pinned> <new> -- apps/web`: re-capture only what changed in a part not yet
  judged; record it.
- **Worktree:** from `C:\dev\masaha\app`: `git worktree add --detach C:\dev\masaha\app-dr <head>`; `npm ci` through
  the grant script; `apps/api/.env` copied from `C:\dev\masaha\app-design\apps\api\.env` (never printed) with
  `DATABASE_URL` → `masaha_dr_dev`, `TEST_DATABASE_URL` → `masaha_dr_test`, `PORT=3336`,
  `CORS_ORIGIN=http://localhost:5336`; `apps/web/.env`: `NODE_ENV=development`, `WEB_PORT=5336`,
  `API_PROXY_TARGET=http://localhost:3336`.
- **Database:** `masaha_dr_dev` = a copy of `masaha_dev` (`pg_dump -Fc` / `pg_restore --no-owner` inside the container
  `masaha-postgres-1`; `masaha_dev` is in use, so no template copy); `masaha_dr_test` empty. **Never touch**
  `masaha_dev`, `masaha_test`, `masaha_design_*`, `masaha_we_*`; **never `db:seed`.** A state you must create to see
  it (an empty list, a failure, a Sheet with changes) is written to `masaha_dr_dev` only, and named in the summary.
  The API's rate limits are real: sign in once per role and reuse the session, pace the captures; on a 429, wait and
  retry; clearing `masaha_dr_dev`'s `rate_limits` rows between batches is allowed, never a code change.
- **Accounts:** a visitor (signed out); a signed-in user of the demo set; the demo owner (`demo-owner@example.com`,
  Pal Hub) and reception (`demo-reception@example.com`) with `SEED_DEMO_PASSWORD`; the admin (`SEED_ADMIN_EMAIL`) with
  `SEED_ADMIN_PASSWORD` — from the copied `.env`, never printed. Google sign-in is not used.
- **Ports:** 3336 / 5336 only. Never touch 3320 / 5320 (the women-evening worker), 3323 / 5323 (the identity lead),
  3342 / 5342. At the end, stop every server you started by its PID and check the ports free.
- **Memory — the machine is shared with two other workers:** every heavy step goes through
  `node C:\dev\masaha\workspace\TASKS\IDENTITY\scripts\heavy.mjs dr <command…>` (`npm ci`, each Chrome batch, any
  build): it waits for free memory and runs one heavy step at a time while under 8 GB free; the identity lead goes
  first. One headless Chrome at a time. Your two servers run for the whole review.

## 4. Phase A — the inputs (you)

1. **The inventory** (`ROUND3\INVENTORY.md`): every route of the web at the head (the site's and the dashboard's route
   files), each mapped to foundation §13's screens and to one part; for each, the role and the states worth seeing —
   empty, loading (a held request), a failure, a Sheet or dialog open, a filter on, a long Arabic name, FULL / closed,
   the 404, a too-many-requests answer where reachable, the owner's and the admin's edit states, the phone drawer and
   the 768 rail. The showcase (`/__showcase`, development only) belongs to SH.
2. **The tools** (`ROUND3\tools\`): adapt round 2's `r2-pack.mjs` and `r2-sheets.mjs` to the app — signed-in roles,
   the language and theme set before load (the app reads `masaha.language` / `masaha.theme` from `localStorage`), a
   held request for loading states. Each frame: a viewport PNG, a full-page PNG and a facts JSON — page overflow,
   console errors, every visible text's contrast against its painted ground, the focus outline after Tab, touch
   targets under 40 px (44 px on a coarse pointer), any of Sea's old values still painted, the spark as text or on an
   action.
3. **The pack** (`ROUND3\pack\`): every screen and state × 390 / 768 / 1440 × ar / en × light / dark, plus **contact
   sheets** per screen and width (the four frames side by side; first screen and whole page). Check it: no failed
   frame, the language and theme right on every frame, sizes sane; an index of frames per part.

## 5. Phase B — the six agents

- **Write each agent's prompt yourself** (`ROUND3\PROMPT\R3-<PART>.md`, self-contained): its screens and the paths of
  its sheets and frames; the lens with §2's adaptation; its part's `DECISIONS_*.md` and `DECISIONS_SHARED.md`; the
  identity's rules; the axes; the report's shape (the lens's §5, IDs `R3-<PART>-NNN`, each issue tagged with its
  axis); the skills below; the gates below; its report path `ROUND3\REPORT\R3-<PART>_REPORT.md`. Run them with your
  Agent tool, **all six at once** (they read images and code; their live checks queue through the grant script).
- **Skills (the owner's word, a stated exception to workflow §10 for this round)** — each agent loads, as lenses:
  `vectorlab-ux-skills:ux-audit`, `vectorlab-ux-skills:anti-slop` and `frontend-design:frontend-design` (polish and
  character, never a restyle against the design system), and for its part — **PU:** `page-patterns`, `viewports`,
  `empty-states`, `loaders` · **AU:** `forms`, `errors`, `labels`, `verbs`, `defaults` · **OW:** `forms`, `errors`,
  `empty-states`, `labels`, `verbs`, `loaders` · **DK:** `keyboard`, `errors`, `loaders`, `verbs`, `defaults` ·
  **AD:** `forms`, `labels`, `empty-states`, `errors`, `defaults` · **SH:** `colour-palette`, `typography`, `spacing`,
  `surfaces`, `icon-buttons`, `motion`, `transitions`, `reduced-motion`, `keyboard` (all `vectorlab-ux-skills:`).
  **Never `brand-guidelines`.** A skill's advice that contradicts `foundation.md` or a settled decision is a **rule in
  doubt**, never a defect. Check first that the skills load in this session; one that does not: say so in the
  summary and go on with the lens alone.
- **SH's part, besides its own screens:** the design system as the showcase draws it; the shells (the site's header
  and phone menu, the focus shell, the dashboard's sidebars, rails and drawers, page headers); toasts, dialogs,
  Sheets; loading, empty and error states across parts; **the identity across the product** — ink on every action,
  the spark only where ADR 0019 allows (never small text, never an action, never destructive), hover never the
  selected tint, links underlined in running text, the logo (its places, sizes, name in both languages, never
  mirrored), the favicon; RTL / LTR, dark, the three widths, motion and reduced motion; **the same job done the same
  way in every part.**
- **Gates every agent meets** (round 2's lessons): it **opens every contact sheet of its part** and lists them;
  every issue states an **observed fact with its measured value** — never "ensure", "must", "unverified", "no
  browser"; **every issue has its own cropped capture** (`ROUND3\shots\issues\R3-<PART>-NNN.png`, cut from the pack or
  captured live) — no two issues share one; at least one issue per report is **re-checked in the app's source** (the
  file and line named); live checks (keyboard paths, focus order, a Sheet's discard question, a 429) only on your
  servers (3336 / 5336), through the grant script, one Chrome at a time; no write to the repository, none to the
  database but a named state.

## 6. Phase C — check, merge, summarise (you)

- **Check every report** as `HANDOFF_DESIGN_81.md` §6 says: its sections; measured facts; one distinct capture per
  issue (open a sample of them); the sheets opened listed; one defect re-checked by you in the source. A weak report:
  a new agent redoes it with what was missing (one redo per part at most); the weak one is kept under
  `REPORT\_superseded\`, never deleted.
- **Merge:** the same defect on many screens becomes **one pattern issue** naming every page; the same job done
  differently across parts is yours to name (a consistency section); impact calibrated across parts.
- **The summary across all** (`ROUND3\REPORT\R3-ALL-SUMMARY.md`): the head reviewed; the fifteen most important
  points, one line each; the patterns first, then by part; counts by impact, level and axis; the rules in doubt; what
  was not reviewed and why; the named states written to `masaha_dr_dev`; and a **proposed order of fix batches**
  (each a coherent set — a pattern, a part, a component — with its cost S / M / L) for the owner's decisions round.
- **Then stop:** your servers stopped by PID, ports free; `app-dr` and `masaha_dr_*` **kept** for the decisions
  round (say so); `git -C C:\dev\masaha\app-dr status --short` empty; print a ten-line summary in this conversation.

## 7. Limits

Never edit the repository; no commit, branch, push, PR, issue or comment (Issue #81 is the owner's); no migration; no
dependency; never `db:seed`; only `masaha_dr_*`; never print a secret; never stop on the volume of work — report it;
nothing in `C:\dev\masaha\app`, `app-design` or their lanes beyond reading git objects.
