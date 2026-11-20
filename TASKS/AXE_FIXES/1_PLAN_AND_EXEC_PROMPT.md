# AXE_FIXES — finding 224 (axe: the map's tooltip and two scrolling strips) — PLAN, STOP, then EXECUTE

You are a **Claude Code worker** on **Masaha** (a bilingual Arabic RTL / English platform for coworking spaces in
Gaza), a fresh session, **Opus 5.5, effort high**, started in **`C:\dev\masaha\app`** (on `main` `05822b5e`, clean,
**live in production**: every merge to `main` deploys). No other worker is running. The owner's decisions are binding:
**`C:\dev\masaha\workspace\TASKS\AXE_FIXES\0_OWNER_DECISIONS.md` (X1–X7) — read it first, whole.**

Follow the project's own skills: `start-work-item`, `write-plan`, `open-pr`, `final-report`. This prompt names their
files: the plan is **`C:\dev\masaha\workspace\TASKS\AXE_FIXES\2_PLAN.md`**, the report **`4_REPORT.md`** beside it.

## Hard limits (the whole item)

- **Phase 1 is read-only:** no branch, no file written outside the task folder. It ends with the saved plan and a
  **STOP**; the owner approves it in this conversation.
- Touch only the files finding 224 needs; stage by path, never `git add -A` / `git add .`; no drive-by refactoring
  (anything else you notice: record it in the report, do not do it).
- Web only: no API code, no schema, no migration, **no new dependency**, no database write (never `db:seed`, never a
  reset), no secret printed (`SEED_DEMO_PASSWORD` is read from `apps/api/.env`, never shown).
- The design system's rules: no colours, fonts or CSS outside `apps/web/src/shared/design-system/`; semantic tokens
  only; logical classes only (`check:classes`); every user-facing string through the copy catalogue, both languages.
- **Never weaken a test**; no production code that only a test uses (stub a platform seam such as `ResizeObserver`
  in the test instead). Each new or changed test: break the code it guards once, see it fail, restore.
- Commits: Conventional, **subject ≤ 50 characters, with a body** saying why; no tool attribution anywhere; no
  `fixup!` left. `#PRNUM` in documents, replaced with the real number just before the push (expected **#150** — check
  `gh pr list --state all --limit 1`; Issues share the numbers).
- Never push to `main`, never merge, never force-push a branch that is not yours.
- Heavy commands (lint, typecheck, build, a test lane, headless Chrome) only through the machine's grant script, from
  the repository root: `node C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs axe <command…>` (it waits for
  ≥ 4 GB free and one heavy run at a time — let it wait). **A run killed for memory: retry once, then CI judges** —
  say so in the report. Two lanes at once only with ≥ 8 GB free. Never stop on file count; report it.

## Phase 1 — read and plan (read-only)

**Read:** `CLAUDE.md`; `docs/development/workflow.md`; `docs/development/testing.md`;
`docs/architecture/documentation.md`; `docs/frontend/architecture.md` (§6, the map — note its line on the map as
`role="application"`); `docs/frontend/design-system/foundation.md` §3 (categories, the showcase), §10 (accessibility
baseline), §11 (the component contract, *one focus style*), §12 (the inventory); the findings README and
**finding 224** in full; the capability documents of the three places: `docs/features/spaces.md` («الصور», the read
view's phone row of 96×72 thumbnails), `docs/features/finance.md` (*Occupancy*: «ساعات الذروة» "scrolling sideways
below 768 px"), `docs/features/directory.md` (*The map on the web*: "its name shows beside it").

**The code (verify each, find what the supervisor missed):**
- `apps/web/src/features/spaces/components/photos/PhotosView.tsx:44` — below 768 px the others' `ul`
  (`aria-label={gallery.view.others}`, `overflow-x-auto`) holds only images: nothing in it takes the focus.
- `apps/web/src/features/finance/components/OccupancyTab.tsx:54–68` — the card is `role="region"` named by its
  heading; `CardContent` scrolls (`overflow-x-auto`) around the Heatmap (`min-w-xl md:min-w-0`) or its empty state.
- `apps/web/src/shared/map/components/LeafletMarkerMap.tsx:195–227` — each mark is a named button; its `Tooltip`
  (`map-tooltip`, re-created per state by its `key`, permanent while selected) holds the name in an `aria-hidden`
  span. Leaflet 1.9.4 sets `role="tooltip"` on the tooltip's container and points the mark's `aria-describedby` at it
  (`node_modules/leaflet/dist/leaflet-src.js`, about lines 10732 and 11001).
- Tests: `PhotosSection.component.test.tsx` (the phone's row, about line 80: it finds the list by its name),
  `OccupancyTab.component.test.tsx` (finds the region 'Peak hours'), `shared/map/components/MarkerMap.component.test.tsx`
  and `features/directory/components/map/DirectoryMap.component.test.tsx` (Leaflet renders in jsdom);
  `apps/web/src/test/componentSetup.ts` (jsdom has no layout; `ResizeObserver` is a do-nothing stand-in).

**The work to plan (X2, X3 — the owner's; the details are the supervisor's, challenge them in *Proposed alternatives*):**
1. **A new design-system component** in `components/display/<Name>/` (the supervisor's name: `ScrollRegion`), its own
   `index.ts`, exported from the layer's root: a `div` that scrolls along the inline axis; **`role="group"`**, named
   by a required `aria-label` or `aria-labelledby` (typed so one of them is required); **`tabIndex={0}` only while its
   content overflows**, measured (scroll width over client width) and measured again when it or its content resizes;
   the layer's one focus style (§11); props extending the `div`'s; no built-in words. Its showcase section
   (`pages/showcase/sections/display/`) and registry entry; its row in §12's `display` table and its name in §3's
   category table (add only it — other gaps you see there are recorded, not fixed); one line in §10 saying that a
   region scrolling sideways is reached by the keyboard, through this component. Its component test: the named
   group; no tab stop while its content fits; a tab stop once it overflows (sizes and `ResizeObserver` stubbed in the
   test); axe clean.
2. **The photos' phone row** in the component: it takes the name `gallery.view.others`; the list inside it keeps its
   list role without a name of its own (the name is not said twice). The test finds the group by its name and the
   list within it. The 768 px grid is unchanged.
3. **«ساعات الذروة»:** `CardContent` no longer scrolls; the Heatmap alone sits in the component, named by the card's
   heading (`aria-labelledby`); the empty state stays outside it (nothing to scroll). The card stays the region.
4. **The map's tooltip:** its element is `aria-hidden="true"` whenever Leaflet draws it, passing or permanent (both of
   the `key`'s instances), and the mark carries no `aria-describedby` to it; the mark's own name is unchanged. A test
   with a selected mark: the tooltip's element hidden, the mark not described by it, axe clean.
5. **Documents:** finding 224 Resolved as the findings README says (its status line, a resolution naming `#PRNUM`, the
   index moved to *Resolved*); each capability document whose described behaviour changes, in the home
   `documentation.md` gives it (summarise and link, one home per fact, dated history lines as those documents keep
   them).
6. **The commits** (the supervisor's suggestion; code, tests and documents of a unit together): the component; the
   two scrolling places; the map's tooltip with the finding's resolution.
7. **The proof, beyond the tests (X4):** your headless-Chrome pass of Phase 2 §3 — say how you will drive it, sign in,
   reach each place, and run axe.

**Save the plan** as `2_PLAN.md` (English): every file and its change, each test and the break that proves it, the
commits, the verification, the Chrome pass, risks, and a **Proposed alternatives** section (or "None"). **Then STOP**
and say in the chat that the plan is ready.

## Phase 2 — execute (only after the owner approves the plan)

1. **Branch:** `git switch --no-track -c fix/axe-224 origin/main` after `git fetch` (status clean). Build the plan's
   commits.
2. **Complete local verification on the head (X6)**, each through the grant script where heavy: `npm run format:check`,
   `lint`, `typecheck`, `check:classes`, `check:links`, `check:conflicts`, `test:unit`, `test:component`, then a
   production build (`NODE_ENV=production`: `apps/web/.env` sets development) and `check:build`. **`test:api` is left
   to CI** (no API code; the owner's allowance) — say so in the PR's Evidence.
3. **Seen in Chrome, and axe (X4):** start the API (`npm run dev -w @masaha/api`, 3320) and the web (`npm run dev`,
   5320) on `masaha_dev` (the demo set); drive headless Chrome over CDP with Node's own WebSocket (model:
   `C:\dev\masaha\workspace\TASKS\CONTACT_RULES\scripts\shots.mjs`; your script in the task folder's `scripts\`), the
   demo owner signed in (a local sign-in rate-limit row may be cleared in `masaha_dev`, never in code). Inject
   `node_modules/axe-core/axe.min.js` and run axe on: the space profile's «الصور» with a photo row that overflows (at
   390 px; if no demo space has enough photos to overflow there, narrow to 320 and say which space and how many — add
   no photo), Finance › Occupancy with the heatmap drawn, and the directory's map with a mark selected — at 390 and
   1440, light and dark, Arabic and English. **No `aria-tooltip-name` and no `scrollable-region-focusable` anywhere**,
   and no new violation; list every rule reported per screen. Tab to each scrolling region and capture its focus ring
   (390, light and dark) — the ring whole, not clipped. Shots to `C:\Users\basel\Downloads\axe-fixes-shots\`, curated,
   never in the repository. **Stop your servers by PID** and check 3320 / 5320 are free.
4. **Push and the PR** with the `open-pr` skill (`#PRNUM` replaced just before the push; the Evidence: each check, the
   axe table, the shots' folder, `test:api` left to CI). Wait until `gh pr checks <n>` is all green on the pushed
   head and GitHub says `CLEAN`.
5. **Report** with the `final-report` skill to `4_REPORT.md`: the PR number and full head sha, the commits, each fix
   and its test (and the break you saw fail), the axe results per screen, what ran locally and what CI judged, every
   decision you took, anything left or recorded. **Stop. Never merge.**
