# DIRECTORY_PROD — the directory's filters in production — PLAN (then execute on approval)

You are a **Claude Code worker** on **Masaha**, in **`C:\dev\masaha\app`**. This task builds, in the **web and the
API**, the directory's filters that the design prototype already shows (#137), plus a few fixes. You **plan first**;
the owner approves; then you execute in this same session. **Model Opus 5.5, effort xhigh — be complete.**

## 0. How this task runs

1. Run the project's **`start-work-item`** skill (it reads `CLAUDE.md` and `docs/development/workflow.md`, checks
   the folder and git state, and plans in plan mode). Then plan with the **`write-plan`** skill: the plan is saved
   to **`C:\dev\masaha\workspace\TASKS\DIRECTORY_PROD\2_PLAN.md`** and **your turn ends** — no branch, no edit
   before the owner approves.
2. On approval, cut **`feat/directory-filters`** from the latest `origin/main` (`40cb481d` or later), execute the
   plan without stopping, verify everything locally, and follow the **`open-pr`** skill (push, PR, CI green and
   `CLEAN`), then the **`final-report`** skill (report to `C:\dev\masaha\workspace\TASKS\DIRECTORY_PROD\4_REPORT.md`).
   **Done = ready for review. Never merge.**
3. **Parallel work exists:** other workers will soon work on the owner's space profile, the visual identity, and
   spaces for women + an evening feature, each on its own branch. Touch only this task's files; if you see an
   overlap, record it in the plan.

## 1. The owner's decisions — binding (copy them into the plan's binding section, word for word)

Read **`C:\dev\masaha\workspace\TASKS\DIRECTORY_PROD\0_OWNER_DECISIONS.md`** whole (items 1–15 and "Not in this
PR"). The source of the design is the prototype at `origin/main`: `docs/design/prototype/Directory.html`,
`docs/design/prototype/masaha/shared.jsx` (`LiveStatus`, `TodayHours`, `resultsLabel`, the open-now rule),
`docs/design/prototype/masaha/space-parts.jsx` (a space without hours), `docs/design/prototype/masaha/data.js`,
`docs/design/prototype/masaha/masaha.css` (`.dir-filters`), and the «Refactor 1» section of `docs/design/CHANGES.md`.
The prototype is a **specification, not code to copy** (`docs/design/README.md` › Rules for implementing).

## 2. Read before planning

`CLAUDE.md`; `docs/development/workflow.md`, `engineering-principles.md`, `testing.md`; `docs/features/directory.md`,
`spaces.md`, `occupancy.md`, `lookups.md`, `space-links.md`; `docs/architecture/decisions/0008-live-status-not-counts.md`;
`docs/architecture/data-model.md` (hours, closures, derived values); `docs/api/api-contract.md` (the directory, §4
pagination); `docs/backend/conventions.md`; `docs/frontend/architecture.md`; `docs/frontend/design-system/foundation.md`;
the findings index (the next free number — 214 is expected for item 1; check). Then the code: `packages/shared/src/
directory/`, the API's directory and spaces modules (the filters, the orders, the hidden-price rule, `liveStatusFor`,
`availableAmong`), `apps/web/src/features/directory/` (filters, `requestOf`, `filtersOf`, the cards, Home's spaces),
`ListPagination`, the admin's spaces list, and every test that covers them.

## 3. Tests — the owner's bar

**The tests must work and point the right way — never bent to pass; the filters' tests must be very strong, with no
gap.** The plan holds a **test matrix** (`T…` numbered), each test naming the behaviour it proves and the lane
(`testing.md`). At least:

- **Each filter alone and in combination**, through the API (`test:api`) on real queries: area · period (alone now
  filters) · priceMin/priceMax (inclusive bounds, either alone, both, min > max refused, a bound without the period
  refused, zero/negative/non-integer refused) · openNow · evening · friday · students · verified · q — and every
  filter applied **before** the page is cut (full pages, a correct total).
- **Hidden prices**: an unverified space with stale prices never passes a price filter, never gets a price on its card,
  and never enters a price order.
- **The price order**: both directions, ties ended by the id, stable across pages (page 1 + page 2 = the whole order,
  no repeat, no gap), refused without the period.
- **openNow on Gaza's clock**, with a **fixed clock** (inject time; never the real one): the opening minute passes,
  the closing minute does not; a day closed (`fri` null); a space without hours; a closure in force (and one ended or
  not yet begun); verified FULL still passes; an unverified space passes; the **day boundary in Gaza vs UTC**
  (e.g. 23:30 UTC is the next day in Gaza) and a **DST change** (Gaza observes DST); and the data model's rule on a
  closing time before the opening time (an executor check: if the model allows overnight ranges, test them; if it
  forbids them, say where).
- **evening**: 20:00 exactly passes, 19:59 does not; one evening day among others passes; no hours never.
- **The card's by-hours state** for unverified spaces (open / closed / closure / no hours) and the live status
  unchanged for verified ones.
- **18 a page**: the web asks 18; page boundaries and the total with filters.
- **Shared schemas** (`test:unit`): every query rule above, accepted and refused, with the exact error codes.
- **The web** (`test:component`): the panel's order and groups; `SegmentedControl`'s keyboard (arrows in RTL and LTR,
  Home/End, roving tab stop) and accessibility (axe-clean); the range's validation (Arabic-Indic digits, «إلى» under
  «من», nothing sent while invalid); the sort's price items absent under «الكل» and present after; clearing the
  subscription while sorting by price; «مسح» clears the subscription and the range but not the order; the active
  count; the URL round trip (reload and Back keep the state; an old `availableNow`/`available` link opens unfiltered);
  the card's price and by-hours badge; «ساعات العمل غير متوفرة» on the card and the space page; the sheet's plurals.
- **Finding 214**: explain the root cause and fix the wait in the test; prove it by running the component lane in
  full (not the file alone) — say how many full runs.
- No production code exists only for a test (no parameter or option only a test passes); time and other platform
  seams are injected the way the codebase already does.

## 4. What the plan contains

Number everything. The binding decisions (verbatim); for each item 1–15: the files, the API change (query, card
shape, error codes), the web change, the documents, and its tests (`T…`); the new `SegmentedControl` (props, states,
the design-system rules: semantic tokens only, `check:classes`); the commits (Conventional, atomic, 3–8; the first is
items 1–2); executor checks (`EC…`) for what reading cannot prove; risks; **"Proposed alternatives"** — where you
think a decision is wrong or weaker than another way, say so with your reasoning (you may challenge the owner's
decisions; you never deviate silently); open points for the owner (`OD…`, each with options and your
recommendation).

## 5. Limits (planning and execution)

- No migration is expected; if one seems needed, it is an `OD…` — never create one unasked.
- **Never `db:seed` `masaha_dev`** (it holds the presentation's data). `test:api` uses the test database.
- Complete local verification before the PR: `lint`, `typecheck`, `format:check`, `check:classes`, `check:links`,
  `check:conflicts`, `build` + `check:build` (with `NODE_ENV=production`), and `test:unit`, `test:component`,
  `test:api` in full. Two full lanes may run at once with 8–10 GB free; a third waits. **A lane killed for memory:
  retry once; if it is killed again, CI judges** — say so in the report.
- Stage by path; never `git add -A` / `git add .`; no tool attribution anywhere; no `#PRNUM` left (the PR is
  expected to be **#138** — check the next number just before the push). No push to `main`, no merge, no force-push
  of another branch, no secret printed. Review fixes later fold into their commits (`backup/*` first).
- The prototype change of item 14 (18 a page) goes in this PR with the web's (`docs/design/` is allowed for it).
