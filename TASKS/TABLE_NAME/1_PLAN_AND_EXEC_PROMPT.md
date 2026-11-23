# TABLE_NAME — a table that fits says its name once

You are a **Claude Code worker** on **Masaha**, a bilingual Arabic RTL / English platform for coworking spaces in Gaza.
This is a fresh session, **Opus 5.5, effort medium**, started in **`C:\dev\masaha\app`**. `main` is at `ff9094f2`, clean
and **live in production**: every merge deploys. No other worker is running. The owner is busy, so **work through to
the end without stopping**.

The decisions are binding: **`C:\dev\masaha\workspace\TASKS\TABLE_NAME\0_OWNER_DECISIONS.md` (N1–N5) and
`0_CARRIED_FROM_152.md`. Read both first.**

Follow the project's skills `start-work-item`, `write-plan`, `open-pr` and `final-report`, with one exception (N4): the
plan is short and **you do not stop after it**. Plan: `TASKS\TABLE_NAME\2_PLAN.md`. Report: `4_REPORT.md` beside it.

## Hard limits

- Touch only what N2 and N3 need. Stage by path, never `git add -A` or `git add .`. No drive-by refactoring.
- Web and docs only: no API code, schema, migration, new dependency or database write. No secret printed.
- The design system's rules hold: semantic tokens, logical classes, every user-facing string through the catalogue.
- Never weaken a test. No production code only a test uses. Break the code each new or changed test guards once, see
  the test fail, restore.
- Commits: Conventional, **subject ≤ 50 characters, with a body** saying why; no tool attribution; no `fixup!` left.
  `#PRNUM` in documents, replaced just before the push (expect **#153**; Issues share the numbers, so check both lists).
- Never push to `main`, never merge, never force-push a branch that is not yours.
- Heavy commands (lint, typecheck, build, a test lane, headless Chrome) run through the grant script from the repository
  root: `node C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs tablename <command…>`. It waits for ≥ 4 GB free.
  **A run killed for memory: retry once, then CI judges,** and say so in the report.
- If Claude Code's memory guard stops your background servers, restart them once when ≥ 4 GB is free. If that fails,
  skip the Chrome pass, say so in the report and the PR's Evidence, and carry on to the PR.

## 1. Read, then write a short plan

- `CLAUDE.md`, `docs/development/workflow.md`, `docs/development/testing.md`, `docs/architecture/documentation.md`.
- `docs/frontend/design-system/foundation.md` §10 and §12 (what they say of `Table` and `ScrollRegion`).
- Finding **229** and its resolution.
- `apps/web/src/shared/design-system/components/data/Table/` and `components/display/ScrollRegion/`, with their tests,
  and the showcase's `ScrollRegionSection.tsx`.

## 2. The work

1. **N2:** give `ScrollRegion` a way for `Table` to ask for a container that, while its content fits, has no role, no
   name and no tab stop; while it overflows it is the named group and tab stop it is today. Keep the type's rule of
   exactly one name. The default stays as it is, so the photos, Occupancy and the showcase do not change.
2. **N3:** remove `TableCaption` and its two exports. Confirm with a search that nothing uses it.
3. **Tests:** a table that fits exposes no `group` and one named `table`; once it overflows (sizes and `ResizeObserver`
   stubbed) the named group and tab stop appear; a default `ScrollRegion` that fits is still a named group.
4. **Documents:** update what §10, §12 or finding 229 now say wrongly. Keep one home per fact.
5. **Commits:** one for N2 with its tests and documents, one for N3.

## 3. Verify, open the PR, report

1. **Branch:** after `git fetch`, with a clean status: `git switch --no-track -c fix/table-name-once origin/main`.
2. **Local verification on the head:** `npm run format:check`, `lint`, `typecheck`, `check:classes`, `check:links`,
   `check:conflicts`, `test:unit`, `test:component`, a production build (`NODE_ENV=production`, since `apps/web/.env`
   sets development), then `check:build`. **`test:api` is left to CI** (N5).
3. **Chrome:** adapt a copy of `TASKS\TABLE_SCROLL\scripts\axe.mjs` in this task's `scripts\`. With the API (3320) and web
   (5320) on `masaha_dev`, run axe on the public page's hours at 390 and the owner's profile prices at 320 and 390, in
   Arabic and English, light and dark. Expect no violation. Record, for the prices at 390 (fits) and 320 (overflows),
   whether the container is a `group`. Stop your servers by PID and check both ports are free. Shots go to
   `C:\Users\basel\Downloads\table-name-shots\`, curated, never in the repository.
4. **Push and open the PR** with `open-pr`. The description names C1–C2 as carried from #152. Wait until
   `gh pr checks <n>` is all green on the pushed head and GitHub says `CLEAN`.
5. **Report** with `final-report` to `4_REPORT.md`: PR number and full head sha, the commits, each change with its test
   and the break you saw fail, the axe results, what ran locally and what CI judged, your decisions, anything left.

**Then stop. Never merge.**
