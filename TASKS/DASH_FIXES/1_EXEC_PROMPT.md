# DASH_FIXES — four small findings, one PR (OpenCode)

You are a coding agent working in **`C:\dev\masaha\app`** (Masaha: a bilingual Arabic-RTL / English platform for
coworking spaces; monorepo `apps/web` React 19 + Vite, `apps/api` Express 5 + Prisma, `packages/shared`). The owner's
decisions: `C:\dev\masaha\workspace\TASKS\DASH_FIXES\0_OWNER_DECISIONS.md` (binding). **Do not stop to ask** unless a
hard limit below would be crossed; decide, and record each decision in your report.

## Read first

`CLAUDE.md` (the project's rules — they bind you too), `docs/development/workflow.md` (Git, commits, Definition of
Done), `docs/development/testing.md`, `docs/frontend/architecture.md`, `docs/frontend/design-system/foundation.md`
(§2–§5), `docs/architecture/findings/README.md` (how a finding is resolved), and the four findings in full:
`docs/architecture/findings/227-…`, `220-…`, `222-…`, `223-…`. Then `.claude/skills/open-pr/SKILL.md` — follow it to
open the PR.

## Start

`git status` clean, on `main`; `git pull --ff-only`; branch **`fix/dashboard-findings`**. Another agent (the design
round) works in other folders (`app-design`, `app-dr`) and edits no repository file: never touch them.

## The work — one commit per finding, in this order

1. **227** — an amenity's icon key the web does not know must fall back to none (as `iconOf` already does for retired
   amenities: `useAmenityChecklist.ts`, `useAmenitiesSection.ts`), never crash. Guard where the API's key enters
   (`AmenityIcon` / the amenity rows and checklist), keep `GlyphIcon`'s closed type. One shared helper rather than a
   third copy of `iconOf`. A component test: an active amenity with an unknown key renders, with no icon.
2. **220** — `useSpaceEditorActions` must read a space found deleted (a 404 on a later read) as `useSpaceEditor` and
   `useSpaceName` do: no action offered. A test that draws the actions, answers 404 to a later read, finds none.
3. **222** — a photo given the keyboard's focus in «إدارة الصور» shows a visible focus ring, light and dark (the tile's
   `overflow-hidden` clips the outside ring today: draw it inside, or move the clip). Semantic tokens only.
4. **223** — Finance › Occupancy must not scroll sideways at 390 px in either language; the Heatmap's visually hidden
   table stays readable by assistive technology. A test or check that would see the overflow return.

Each finding's file: mark it resolved as the findings README says (its status, the index line), naming this PR as
`#PRNUM` (replace it with the real number just before the push — check the next free number with `gh pr list
--state all --limit 1`; expected #146).

## Rules (hard limits)

- Touch only the files these four fixes need; stage by path, never `git add -A` / `git add .`. No refactoring beyond.
- No colours, fonts or CSS outside `apps/web/src/shared/design-system/`; semantic tokens only; no physical direction
  classes (`npm run check:classes` rules). Every user-facing string through the copy catalogue, both languages.
- **Never weaken a test.** No production code that only a test uses. No schema, no migration, no new dependency, no
  database write, no secret printed.
- Commits: Conventional Commits, **subject ≤ 50 characters, with a body** saying why. **No tool attribution** — no
  `Co-Authored-By`, no "generated with", anywhere. No `fixup!` left in the history.
- **Never merge, never push to `main`**, never force-push another branch.

## Tests — the owner's rule (D3)

- **Light (always):** the test files you touched or added, **each alone** (`npx vitest run <file>` in its workspace),
  plus `npm run check:classes`, `npm run check:links` and Prettier on the touched files.
- **Heavy (only if memory allows):** `npm run typecheck`, `npm run lint`, `npm run build`, a full lane, any headless
  Chrome batch — each **only** through the machine's grant script, from the repository root:
  `node C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs dash <command…>`. It waits for ≥ 4 GB free and one
  heavy run at a time. Before each heavy run, check free memory
  (`powershell -c "[math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory/1MB,1)"`); **if it does
  not grant within 10 minutes, skip that run** — CI judges it. A run killed for memory: retry once, then CI judges.
- Each new test: break the code it guards once, watch it fail, restore.
- Say exactly what ran and what was left to CI in the PR's Evidence and in the report.

## Seeing it (222, 223)

If memory allows (through the grant script): start the API (`npm run dev -w @masaha/api`, port 3320) and the web
(`npm run dev`, port 5320), sign in as the demo owner (`SEED_DEMO_PASSWORD` in `apps/api/.env`, never printed), and
capture with headless Chrome: 222 the focused photo (Tab to it) light and dark at 1440; 223 Occupancy at 390 in Arabic
and English (and the page's `scrollWidth` = 390). Shots to `C:\Users\basel\Downloads\dash-fixes-shots\` (never in the
repository). **Stop your servers by PID at the end** and check the ports are free. If memory never allows, say so —
the supervisor will look.

## Finish

Push the branch, open the PR (`open-pr`: title, description with each finding and its proof, Evidence with the D3
exception), wait until `gh pr checks <n>` is all green on the pushed head and GitHub says `CLEAN`. Then write
`C:\dev\masaha\workspace\TASKS\DASH_FIXES\4_REPORT.md`: the PR number and full head sha, the commits, each finding's
fix and test (and its seen failure), what ran locally and what CI judged, your decisions, anything left. **Stop.**
