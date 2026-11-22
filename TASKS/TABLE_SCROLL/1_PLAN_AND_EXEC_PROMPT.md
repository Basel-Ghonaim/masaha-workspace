# TABLE_SCROLL — finding 229: a table that scrolls sideways is reached by the keyboard

You are a **Claude Code worker** on **Masaha**, a bilingual Arabic RTL / English platform for coworking spaces in
Gaza. This is a fresh session, **Opus 5.5, effort medium**, started in **`C:\dev\masaha\app`**:
- `main` is at `9b4c4fc1`, clean, and **live in production**: every merge to `main` deploys;
- no other worker is running;
- the owner is busy elsewhere, so **work through to the end without stopping**.

The decisions are binding: **`C:\dev\masaha\workspace\TASKS\TABLE_SCROLL\0_OWNER_DECISIONS.md` (T1–T5) and
`0_CARRIED_FROM_150.md`. Read both first, whole.**

Follow the project's own skills: `start-work-item`, `write-plan`, `open-pr`, `final-report`, with one exception from
T4: the plan is short and **you do not stop after it**. The plan goes to
**`C:\dev\masaha\workspace\TASKS\TABLE_SCROLL\2_PLAN.md`**, the report to **`4_REPORT.md`** beside it.

## Hard limits

- **Scope:** touch only what finding 229 and C1–C2 need. Stage by path, never `git add -A` or `git add .`. No drive-by
  refactoring: anything else you notice goes into the report.
- **Web and docs only:**
  - no API code, no schema, no migration, **no new dependency**;
  - no database write: never `db:seed`, never a reset;
  - no secret printed. `SEED_DEMO_PASSWORD` is read from `apps/api/.env`, never shown.
- **The design system's rules:**
  - no colours, fonts or CSS outside `apps/web/src/shared/design-system/`, and semantic tokens only;
  - logical classes only (`check:classes`);
  - every user-facing string through the copy catalogue, in both languages.
- **Tests:** never weaken one. No production code that only a test uses: stub a platform seam such as
  `ResizeObserver` in the test instead. For each new or changed test, break the code it guards once, see the test
  fail, then restore.
- **Commits:**
  - Conventional, **subject ≤ 50 characters, with a body** that says why;
  - no tool attribution anywhere, and no `fixup!` left;
  - `#PRNUM` in documents, replaced with the real number just before the push. Expect **#152**, and check it with
    `gh pr list --state all --limit 1` and `gh issue list --state all --limit 1`, since Issues share the numbers.
- **Git:** never push to `main`, never merge, and never force-push a branch that is not yours.
- **Heavy commands** (lint, typecheck, build, a test lane, headless Chrome) run only through the machine's grant
  script, from the repository root: `node C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs table
  <command…>`. It waits for ≥ 4 GB free and runs one heavy command at a time: let it wait.
  - **A run killed for memory: retry once, then CI judges.** Say so in the report.
  - Run two lanes at once only with ≥ 8 GB free.
  - Never stop on file count; report it.

## 1. Read, then write a short plan (do not stop)

**Read:**
- `CLAUDE.md`, `docs/development/workflow.md`, `docs/development/testing.md`, `docs/architecture/documentation.md`;
- `docs/frontend/design-system/foundation.md`: §3 (categories), §10 (the accessibility baseline: its line on regions
  that scroll sideways), §11 (one focus style) and §12 (the inventory);
- the findings README: the next free number should be **229** (check the index), and the shape of a finding;
- finding **224** and its resolution (#150), the same problem fixed for two strips.

**The code:**
- `apps/web/src/shared/design-system/components/data/Table/Table.tsx`: the `table-container` div scrolls
  (`overflow-x-auto`) and nothing in it takes the focus.
- `apps/web/src/shared/design-system/components/display/ScrollRegion/` (#150): a named `group`, a tab stop only while
  it overflows, measured by `ResizeObserver`.
- The three kinds of caller:
  - `features/spaces/components/prices/PricesView.tsx`: named by its `caption`;
  - `features/directory/components/page/HoursSection.tsx`: the public space page's hours;
  - `shared/design-system/components/data/DataTable/DataTable.tsx`: `<Table aria-label={label}>`.
- Their component tests, and `apps/web/src/test/componentSetup.ts` (jsdom has no layout).

**Plan (T2 leaves these to you):**
- how the `Table`'s container becomes reachable while it overflows: reuse `ScrollRegion`, or share its measuring;
- how the container gets its name, such as the table's caption or label, so it never goes unnamed and nothing is
  said twice;
- every caller's change, and the tests that prove it: no tab stop while the table fits, a tab stop once it overflows,
  the right name, axe clean;
- the documents: finding 229 recorded and Resolved in this PR as the README says; §10 and §12 where `Table`'s
  behaviour is described; any capability document whose described behaviour changes;
- the commits:
  1. **C1–C2** (`0_CARRIED_FROM_150.md`);
  2. the `Table` with its tests and the finding.

Save the plan as `2_PLAN.md`: every file and its change, each test with the break that proves it, the commits and
the verification. Add a short **Decisions taken** section. **Then go on.**

## 2. Build, verify, open the PR, report

1. **Branch:** after `git fetch`, with the status clean, run `git switch --no-track -c fix/table-scroll-229
   origin/main`. Build the plan's commits.
2. **Complete local verification on the head,** each check through the grant script where it is heavy:
   - `npm run format:check`, `lint`, `typecheck`, `check:classes`, `check:links`, `check:conflicts`;
   - `test:unit`, `test:component`;
   - a production build (`NODE_ENV=production`, since `apps/web/.env` sets development), then `check:build`.

   **`test:api` is left to CI,** since no API code changes (T5). Say so in the PR's Evidence.
3. **axe in headless Chrome:**
   - Start the API (`npm run dev -w @masaha/api`, port 3320) and the web (`npm run dev`, port 5320), on `masaha_dev`.
   - Drive headless Chrome over CDP with Node's own WebSocket. Model it on
     `C:\dev\masaha\workspace\TASKS\AXE_FIXES\scripts\`; your script goes in this task's `scripts\`. Set the phone
     widths with `Emulation.setDeviceMetricsOverride`: headless Chrome will not lay out a window under 500 px.
   - Inject `node_modules/axe-core/axe.min.js` and run axe on:
     - a public space page with prices and hours, as a guest, at 320 and 390;
     - one dashboard page with a `DataTable`, as the demo owner, at 390. A local sign-in rate-limit row may be cleared
       in `masaha_dev`, never in code.
   - Check Arabic and English, light and dark. Expect **no `scrollable-region-focusable`** and no new violation, and
     list every rule reported per screen.
   - Tab to one overflowing table and capture its focus ring at 390, light and dark: the ring whole, not clipped.
   - Shots go to `C:\Users\basel\Downloads\table-scroll-shots\`, curated, never in the repository.
   - **Stop your servers by PID,** and check that 3320 and 5320 are free.
4. **Push and open the PR** with the `open-pr` skill:
   - replace `#PRNUM` just before the push;
   - the description names C1–C2 as carried from #150;
   - the Evidence holds each check, the axe table, the shots' folder, and `test:api` left to CI.

   Wait until `gh pr checks <n>` is all green on the pushed head and GitHub says `CLEAN`.
5. **Report** with the `final-report` skill to `4_REPORT.md`:
   - the PR number and the full head sha;
   - the commits;
   - each change with its test, and the break you saw fail;
   - the axe results per screen;
   - what ran locally and what CI judged;
   - every decision you took, and anything left or recorded.

   **Then stop. Never merge.**
