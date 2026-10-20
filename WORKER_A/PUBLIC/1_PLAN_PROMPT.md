# PUBLIC — the public site on the web: Home, Directory, Space details, About (build map step 3, screens 1–4) — PLAN ONLY

**No branch, no checkout, no file edit in the repository, no commit, no install, no test run, no
server, no database command.** You write one file — the plan — then stop.
**No trial build anywhere either:** no temporary copy of the repository, no `git worktree add`, no
`git stash`, no scratch or temp folder holding code, no `node` / `tsx` / `tsc` / `vitest` / `psql` /
`npm` run — not in the repository, not in a scratchpad, not in a temp directory. The only commands are
`git fetch`, `git show`, `git log`, `git ls-tree`, `git grep`, `git diff` between commits, read-only `gh`,
and reading files. Where you are unsure that something works, write it in the plan as **a check the
executor makes first, with what to do if it fails** — never try it yourself. Read only the files the plan
needs, each once.

**The task's folder:** `C:\dev\masaha\workspace\WORKER_A\PUBLIC\`. This prompt is `1_PLAN_PROMPT.md`; **save
the plan as `2_PLAN.md` here**; reports `4_REPORT_PR<n>.md`. If you are Claude Code: use `write-plan` for its
discipline (save the file; no plan-mode step is needed).

**Where you read.** `C:\dev\masaha\app-design` (the read-only worktree reviews and planners use) — commit
objects only: `git fetch origin`, then `git show origin/main:<path>`, `git ls-tree`, `git grep origin/main`.
Never check anything out, switch or reset it (design reviews may read there too). Worker A executes
OWNER_SETUP PR 3 in `C:\dev\masaha\app` and worker B DESK PR 4 in `C:\dev\masaha\app-b` — never work there.

## 0. The base and what runs beside it

Plan from today's `origin/main`. **Worker A's OWNER_SETUP PR 3** (`feat/owner-staff-settings`, the staff and
settings pages: `apps/web`, `docs`) is executing; **the executor of this plan starts only after it has
merged**, and its first step is `git diff --name-status <the plan's base> origin/main` — a code file the plan
names changed in a way the plan does not cover → stop and ask. Shared files OWNER_SETUP PR 3 also edits
(`shared/copy/*/index.ts`, `docs/frontend/architecture.md`, `overview.md`, `docs/README.md`, the findings
index): name each as a likely text conflict. Worker B's DESK PR 4 and step 8 (API) run in parallel: no code
file is shared; `docs/project/overview.md`, `v1-mvp.md` and the findings index are. **Finding numbers:** this
item's start at **130** — write `130`, `131`, … in the plan.

## 1. The plan must stand alone

Fresh conversations execute each PR (Claude Code or another capable coding agent — no step may depend on a
Claude skill; an appendix maps steps to skills, "only a map"), and another conversation reviews each (one
reviewer, no subagents). Every decision with its one-line reason; the files; each component, hook, query and
type with its interface; the words in both catalogues (Arabic plurals through the catalogue's plural forms;
every line in both languages; the Arabic for the owner's approval); each test with its lane, title and the
break that must make it fail (`docs/development/testing.md` §3 — **every break run and its red output
recorded**); **each accessibility rule, each state (loading, empty, failure, offline), each width and each
privacy rule gets a deliberate break**; the commits, subjects counted (≤ 50); fixes before the push folded
(`--fixup` + autosquash, `GIT_SEQUENCE_EDITOR=:`); every new decision and history line ends with its date and
`#PRNUM`; the procedure with its commands (branches from the latest `origin/main` in `C:\dev\masaha\app`,
`--no-track`; `docker start masaha-postgres-1`, never `db:up`, never `npm ci`; the API on 3320 and the web
on 5320 with worker A's `masaha_dev`; **memory: one full test run at a time on this machine, none while a
`vitest` of `C:\dev\masaha\app-b\` runs, the free memory recorded before each full lane; the known exceptions
— finding 87's routes test and a component lane killed for memory — as `OWNER_SETUP\3_EXEC_PROMPT_PR3.md` §2
words them, CI's `test:component` the judge**; per commit `lint` + `typecheck`; on the head once
`test:unit`, `test:component`, the production build (`$env:NODE_ENV='production'`), `check:build` (the
public site's first download must stay free of dashboard code and of Leaflet), `check:classes`,
`format:check`, `check:links`; a real run with **real screenshots** (the `playwright` MCP tools if present,
else local headless Chrome over CDP), Arabic light and English dark at 390, 768 and 1440, screenshots to this
folder's `shots\pr<n>\`; push; `gh pr create --assignee @me --label feat --label area:web --label area:docs`;
`gh pr checks` and `CLEAN`; the conflict check); a **"Stop and ask"** list; the executor's stop rule (**a
test it cannot run stops the work** — the same wording as `OWNER_SETUP\3_EXEC_PROMPT_PR3.md` §2, its break
clause and its two exceptions included); **a demo account or demo data that does not hold what a real-run
case needs → stop and report, never change data through the app to get past it**; the executor's scripts in
this folder's `scripts\`, never committed; **carried items:** a `0_CARRIED_FROM_<n>.md` from the previous
PR's review, if any, is that PR's first commit. Never merge; no tool attribution; stage by path.

## 2. The owner's decisions (2026-10-20)

**The goal (build map step 3, the web):** anyone finds a space, in the list or on the map, near them or by
filter, sees its page and how to reach Masaha. The API is built (#73, the live status #94, the cover); the
four public pages are placeholders today (`apps/web/src/pages/site/public/*`).

1. **Worker A builds it** after OWNER_SETUP — no third worker (the machine's memory).
2. **Four PRs in sequence**, each cut from `main` once the one before it has merged:
   - **PR 1 — the Directory's list** (≈ 60 files): the space card (the cover or the space's mark, U12; no
     prices; the live status), the search (both names and the area, U3), the place filter (U1), the price
     filter (U5), «متاحة الآن فقط» and «المساحات الموثّقة فقط», the sort, the pages (P6), «الأقرب إليّ» with
     its one state line (U2) and the location's privacy line, the filter sidebar from `lg` and the sheet below
     (the P5 exception).
   - **PR 2 — the map** (≈ 40 files): the pins by state, a shape as well as a colour (U6), the legend, the
     selected card as a bottom `Sheet` on a phone, placing a pin by hand (U7); Leaflet lazily loaded
     (frontend architecture §6).
   - **PR 3 — the Space details page** (≈ 55 files): one order at every width (U8), prices per audience
     (U9's page part), the hours and the shifts once, the amenities as one list (own ones included, one
     neutral mark), the gallery or its caption, the location (its pin `role="img"`), the contacts (value
     shown, carrier from the prefix), the freshness per fact group (U4), the closure Alert, the live status,
     the breadcrumb from `md`, the phone bottom bar (WhatsApp and Call) at `md`.
   - **PR 4 — Home, About and the error pages** (≈ 35 files): Home (near me, «تصفّح حسب المنطقة»), About
     (U11: no university line; «تواصل معنا» and «لأصحاب المساحات» sections and anchors), offline and error
     pages (PU-024).
   If the reading shows a better cut, propose it in *Proposed alternatives* — do not apply it.
3. **The live status's delivery (step 3 "settles" it):** the space page reads `GET /spaces/:slug/occupancy`
   again **every 60 seconds while the page is visible** and on returning to it; the Directory and Home
   refresh their lists' statuses **on returning to the page only** — no polling of lists. Record it where
   the frontend architecture or the capability's document owns it.
4. **No report button and no favourite heart** until step 10 builds their API — not shown at all (no dead
   control); the space page's layout leaves their place without a gap.
5. **The platform's contact:** its WhatsApp and email come from **one web configuration** (say which: a
   `VITE_` variable read in one module, or one constants file — recommend one), never from the copy
   catalogue; each contact shows only when it is set. Until the owner supplies the values, **the email only**
   (the configured one), WhatsApp hidden. The plan names the exact place the owner fills.
6. **Design round 2:** build from the **settled** decisions now; round 2's decisions come later as small
   items. But read the four finished public reviews — `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\
   R2-PU-AX_REPORT.md`, `R2-PU-CP_REPORT.md`, `R2-PU-UX_REPORT.md`, `R2-PU-VD_REPORT.md` — and **do not copy a
   defect they prove** into the web (e.g. the skip link to a `#main` no public page defines; a fixed results
   label); list each such point in the plan with the report and issue it comes from. Anything in them that
   would change a settled decision → a *Proposed alternative*, never applied.
7. **The decisions file's amendments win:** `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_PUBLIC.md`
   carries its original lines and the owner's later amendments; where they differ, **the amendment wins** —
   the card shows **no prices** (U9's card part and U12's open point are superseded), the sort has **no
   «الأقل سعرًا»**, **amenities are no filter**. Propose (in the plan's documents step of PR 1) the line that
   corrects the file — the supervisor edits it, not the executor.
8. **The privacy line under «الأقرب إليّ»** is the prototype's corrected one (`shared.jsx`'s `PRIVACY_LINE`:
   «يُرسَل موقعك مقرَّبًا لترتيب المساحات حسب المسافة فقط، ولا يُحفظ.» and its English), not the old «يبقى
   موقعك على جهازك فقط».

## 3. Read first

`CLAUDE.md`; `docs/development/workflow.md`; `testing.md`; `docs/frontend/architecture.md` (§3 features, §6
the map, §7 the cache); `design-system/foundation.md` (§9 widths, §10 actions, §12 components, §13 screens
1–4 and near me, §15 touch); `localisation.md`; `documentation.md` §5; `docs/features/directory.md`,
`spaces.md` (its public reads), `lookups.md`, `occupancy.md`; `docs/api/api-contract.md` (§1–4, the public
endpoints: `GET /lookups`, `GET /spaces`, the pins, `GET /spaces/:slug`, `GET /spaces/:slug/occupancy`); ADR
0002, 0008; `docs/plans/v1-mvp.md` step 3; `docs/design/SCREENS.md` (the public site); the prototype's
public pages and `masaha/shared.jsx`, `location.jsx` and the directory's and space page's modules
(`docs/design/prototype/…`); `DECISIONS_PUBLIC.md`, `DECISIONS_SHARED.md`; the four round-2 reports above;
the findings index; the code of `pages/site` (the shell, `routes.tsx`, `navigation.ts`, the placeholders),
`shared/map`, `shared/routing`, `shared/copy`, `features/lookups` (the public catalogue), `features/spaces`
(what the public page can reuse — the price and hours views — and what it must not), `packages/shared`'s
`directory`, `spaces` and `lookups` responses; `apps/web/scripts/` (`check:build`'s rules); OWNER_SETUP's
`2_PLAN.md` as the model of a web plan.

## 4. Decisions the plan must state (with a recommendation each)

- The features: a new `directory` web feature (and whether the space page is its own or `spaces`' public
  part), what each owns, and what stays in `pages/site`.
- The URL state of the Directory (filters, sort, page, view, near me) — shareable and restorable — and how
  the device's rounded location is kept (never stored server-side; in the browser only as the storage layer
  allows).
- The caching and keys of each public read (§7), the live status's refetch (decision 3), and the first
  download's budget (`check:build`).
- Each width's layout against foundation §9, each state, and accessibility (names, landmarks, the skip link,
  focus on page change, the map's keyboard use).
- Any document this decision set proves wrong — as a proposal, never applied silently.

## 5. The plan's shape

As `C:\dev\masaha\workspace\WORKER_A\OWNER_SETUP\2_PLAN.md`: summary; the contract per PR (scope, acceptance
criteria, out of scope); the reading done and what it changed; the decisions as built; stronger decisions
(S…) and **Proposed alternatives**; related findings (folded or not, why); design issues found in the
reading (each with its fix, built only once the owner approves); the files; the interfaces and the words; the
tests with their breaks; the commits; the procedure and the stop rules; the decisions needed from the owner.
Stop after saving it.
