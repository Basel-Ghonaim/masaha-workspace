# FINAL — close every screen and every open finding of Masaha v1 in one unified plan — PLAN ONLY

You are **worker A's planner** for the project's last build mission, in a fresh conversation, in
**`C:\dev\masaha\app`** (read-only for you). You write **one plan** and stop. You build nothing. Another session of
worker A, **in the same folder**, is waiting to execute it with sub-agents — **so never change this folder's working
tree, branch or `HEAD`** (no switch, no checkout, no fetch into a branch other than `origin/*`). Do not run the `start-work-item` skill (the
owner's instruction for this task); `CLAUDE.md` is in your context. **Model Opus 5.5, effort xhigh — take the time to
be complete.**

## 0. What the owner wants (2026-10-29) — read this twice

- **After this mission, every one of the 32 screens is complete, with no gap, and every open finding is closed** —
  built, or accepted by the owner. The API of v1 is complete on `main` (#131); this mission builds every screen still
  missing, closes every gap on the screens already built, and closes every open finding — on the web **and the API
  alike**: **one PR may change `apps/web`, `apps/api`, `packages/shared` and `docs` together** (the web/API split
  between workers is lifted for this mission).
- **The plan stands alone, literally:** it never sends its reader to another plan, prompt or report — **copy into it,
  in full, every decision, rule, route, shape, design detail, word (Arabic and English), test and break the executor
  needs.** Pointers to the repository's own documents (contract, conventions, data model, foundation, ADRs, findings,
  the prototypes under `docs/design/`) are allowed as the source of truth for what exists; never to workspace files.
- **It is ours to edit:** number everything (§, `D…` decisions, `S…` stronger decisions, `DI…` design issues, `T…`/`U…`
  tests, `B…` breaks, `EC…` executor checks, `OD…` decisions for the owner). Each decision: its one-line reason and its
  undo. The owner's decisions in one binding section, verbatim.
- **It is executed by a lead with sub-agents, in one PR** (as #129 and #131): your plan gives the units of work,
  their dependencies, the files each touches, which can run in parallel and which must come first, the shared files
  and how lanes add to them without colliding, and a proposed number of lanes (the execution prompt decides).
- **Plan only:** no branch, no edit, no build, no test run, no server, no database command, no trial copy or worktree.
  Read with `git show origin/main:<path>`, `git grep`, `git log`, `gh`. A point you cannot prove by reading becomes an
  **executor check** (what to check, what to do if it fails).
- **Open points:** anything the owner has not decided becomes an `OD…` with options and **your recommendation**. The
  supervisor settles them on the owner's behalf; make each self-contained and decidable.

## 1. The base

`git fetch origin` in `C:\dev\masaha\app`, then read **only from `origin/main`'s commit objects** (do not switch or
touch the working tree: worker A's executor session shares the folder). `origin/main` = **`ce671b37`** or
later (#131 merged: finance, the two overviews, `GET`/`PATCH /me`, `GET …/visits`, finding 167's filter, the `payments`
totals). Finding numbers for this plan: **from 200**.

## 2. The owner's decisions — binding (copy them verbatim into the plan)

Read **`C:\dev\masaha\workspace\WORKER_A\FINAL\0_OWNER_DECISIONS.md`** whole and copy it into the plan's binding
section, word for word: the mission; the framework **F1–F4** (F1: every open finding is in except the deployment's —
**23, 33, 46, 64, 65, 152** — which go to the deployment item; F2 web + API in one PR; F3 migrations allowed when the
plan names each, the SQL read at review, no PR number in SQL; F4 one PR, reviews by lane); the findings **built** (14,
21, 32, 83, 89, 92, 99, 160, 162, 163, 164, 165, 166, 168, 171 (a), 91 (a), and 158) and **accepted** (84, 187, 193 —
each moved to *Accepted* with the owner's line); **every other open finding built as its own *Resolves when* says**,
and where a finding offers "or the owner accepts", your recommendation as an `OD…`.

## 3. Part one — the screens

For **each of the 32 screens** of `docs/design/SCREENS.md` (at `origin/main`): its state on `main` (built / partial /
missing), checked against **its prototype** (`docs/design/prototype/*.html` named in SCREENS.md) and **foundation §13**
(and §12's components), the design decisions in `C:\dev\masaha\workspace\DESIGN\DECISIONS\` (`DECISIONS_OWNER.md`,
`DECISIONS_ADMIN.md`, `DECISIONS_SHARED.md`, `REVIEW_LENS.md` — **copy what you use**), and the routes the API answers.
List **every gap** on a built screen (a missing state, action, filter, figure, empty/error/loading state, width
layout, both languages, dark) — and plan it closed. The screens missing or partial today include at least: **9** (the
name and language through `GET`/`PATCH /me`), **12** (the owner's overview: a work queue, **no amount anywhere** — O3,
OV1–OV8 as #131 built them), **19** (finance: income, debts with the CSV built in the browser from the pages, payers,
occupancy — the owner's alone), **the owner's audit** (O13, `Owner audit.html`, finding 14, with its place in the
owner's navigation), **25** (the admin's overview, A8; finding 158), **31** (the admin's audit log), **32** (the
platform settings, three cards, AD-029), and the built screens' gaps the API now closes (finding 161's visits of a day,
finding 167's filter on screen 28). For each screen: routes it reads and writes, the page and its features (the web
architecture's layers — `docs/frontend/architecture.md`), states, words (both languages, through the copy catalogue,
Arabic plurals), widths (390 / 768 / 1440), accessibility, the tests and breaks, the real-run cases.
**Design gaps** (a screen detail no prototype or decision settles) → `DI…` with a recommendation.

## 4. Part two — every open finding

Read the findings index at `origin/main` (`docs/architecture/findings/README.md`, *Open*) and **every open finding's
file**. For each (except F1's deployment six): what, where, the fix (web, API, shared, schema, test, document,
tooling), its size, its tests and breaks, and **its unit**. The owner-chosen ones as §2 says; the rest as their
*Resolves when*; "or the owner accepts" → an `OD…` with your recommendation. **A migration** only where a fix needs
one (F3): its SQL in full in the plan, its checksum-safe procedure (`migrate dev --create-only` once, or `migrate diff
--script` when non-interactive; no PR number in SQL). Also: `0_CARRIED_FROM_111.md`'s small public-site fixes
(`C:\dev\masaha\workspace\WORKER_A\PUBLIC\0_CARRIED_FROM_111.md` — **copy each item in full**); the open findings that
#129 and #131 recorded (180, 184, 158 and others); `docs/README.md`'s *Deferred documents* (any trigger met — the
document owed by this PR); `docs/plans/v1-mvp.md` (every step *Built* at the end) and `docs/project/overview.md`.

## 5. The plan's shape (number everything)

1. **Header:** base sha, what it read, what it could not prove (→ executor checks), the size (files, commits), the
   finding numbers used.
2. **The owner's decisions, binding** (§2 above, verbatim).
3. **Scope, acceptance criteria, out of scope** — per part; **one criterion per screen: "complete, no gap"**, broken
   into testable lines; one per finding: "closed (built / accepted)".
4. **The reading done** — each screen's state and gaps (a table: screen · state · gaps · unit); each finding's state.
5. **Decisions as built** (`D…`), per unit: routes used or added, shapes, the web's features and pages, states, words
   (both languages, verbatim), layouts; **stronger decisions** (`S…`); **Proposed alternatives**.
6. **Design issues** (`DI…`) with a recommendation each.
7. **Related findings** — each closed or accepted, with its *Resolution* line to write.
8. **The files** — per unit, each file A/M with its purpose; migrations named.
9. **Units, commits and lanes:** every commit (subject ≤ 50, Conventional, its contents, its tests); units; dependencies;
   **what must come first** (shared foundations: navigation groups (165), shared components the layer gains, shared
   types, migrations); **what can run in parallel**; **the shared files** (routes, navigation, the copy indexes, the
   layer's index, `app.ts`, the contract, conventions, `overview.md`, `v1-mvp.md`, the findings index) and how each lane
   adds without colliding; a proposed lane count and order.
10. **Tests** — each with its lane (`*.unit.test.ts`, `*.component.test.tsx`, `*.api.test.ts`), title, and **the break
    that must make it fail**; *Not tested, and said*; *Review Focus*.
11. **The real run** — the web on 5320 and the API on 3320 (`masaha_dev`), headless Chrome over CDP: each screen, each
    role (owner, reception, admin, user, guest), Arabic light and English dark at 390 / 768 / 1440 where layouts change;
    the network log; **every write named** and put back where it can be; what the demo data lacks (never changed through
    the app).
12. **Documents** — every repository document each unit changes, one home per fact, `#PRNUM` where the number goes;
    **at the end every build-map step *Built*, every screen built, the findings index with no open finding but F1's
    six**.
13. **Decisions needed from the owner** (`OD…`) — options and a recommendation each.
14. **Executor checks** (`EC…`) — what to do if each fails.

## 6. Write it, then stop

Write the plan to **`C:\dev\masaha\workspace\WORKER_A\FINAL\2_PLAN.md`** — write it **in full first to
`2_PLAN.draft.md`, then rename it to `2_PLAN.md` as your last step** (a watcher waits for `2_PLAN.md`; it must never see
a half-written file). Notes only in `C:\dev\masaha\workspace\WORKER_A\FINAL\scripts\`. English. Then **stop** and reply:

```
Plan: C:\dev\masaha\workspace\WORKER_A\FINAL\2_PLAN.md
Base: <sha>
Screens: <n complete already> · <n partial> · <n missing> — gaps <n>
Findings: <n built> · <n accepted> · <n to the deployment> · migrations <n>
Units: <n> · commits <n> · lanes proposed <n> · files ≈ <n>
Owner decisions needed (OD): <n> (one line each)
Design issues (DI): <n> · Executor checks (EC): <n> · Proposed alternatives: <n>
```
