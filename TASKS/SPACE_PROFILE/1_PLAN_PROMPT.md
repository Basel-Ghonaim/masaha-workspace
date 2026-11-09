# SPACE_PROFILE — the space profile in production — PLAN (execution later, by a fresh session)

You are a **Claude Code planner** on **Masaha**, in **`C:\dev\masaha\app`** (on `main`, clean). This task builds, in
the **web, the API and `packages/shared`**, the owner's space profile and the admin's space editor as the design
prototype now shows them (**#138**, merged 2026-11-08 at `7fb73c3c`). You **plan only**: the plan is saved, your turn
ends, the owner approves, and **a fresh Claude Code session executes it** (you do not execute). **Model Opus 5.5,
effort xhigh — be complete.**

## 0. How this task runs

1. Run the project's **`start-work-item`** skill (it reads `CLAUDE.md` and `docs/development/workflow.md`, checks the
   folder and git state, and plans in plan mode). Plan with the **`write-plan`** skill: the plan is saved to
   **`C:\dev\masaha\workspace\TASKS\SPACE_PROFILE\2_PLAN_PROD.md`** (not `2_PLAN.md`, which is the prototype round's)
   and **your turn ends** — no branch, no edit, no migration file, no install.
2. **No trial builds:** no temporary copies, no trial worktrees, no scratch runs, no `npm install` of a candidate
   library. What reading cannot settle becomes an executor check (`EC…`).
3. **Parallel work:** the palette lab runs in `C:\dev\masaha\app-b` (new prototype files only; it may later change the
   design system's tokens). A later task, **spaces for women + the owner-declared evening feature**, will touch the
   space's schema, the directory and the profile. Touch nothing of theirs; record any overlap.

## 1. The owner's decisions — binding (copy them into the plan's binding section, word for word)

Read **`C:\dev\masaha\workspace\TASKS\SPACE_PROFILE\0_OWNER_DECISIONS.md`** whole: G1–G5 and the settled order, H1–H4,
P1–P7, R1, R2, **R5–R9** (R3/R4 were replaced), W1–W5, S1–S5, A1–A2, B1–B2, L1–L2, C1–C2, **M1–M4 (they override
earlier lines)**, and **«Before production» X1–X3 and A3 (deferred: build nothing for women / evening, reserve
nothing)**. Two approvals already given: **a drag-and-drop dependency** (name it and say why: touch, keyboard, screen
readers, RTL, size, maintenance), and **the contacts' new types and «وسيلة أخرى» need a migration** (name it: the
enum change, the name column, existing rows untouched — the SQL is shown in the plan for the owner).

**The design source** is the prototype at `origin/main`: `docs/design/prototype/Owner space profile.html`,
`Admin space edit.html`, `Packages.html`, `Owner settings.html`, `masaha/profile-a.jsx`, `profile-b.jsx`,
`profile-c.jsx`, `masaha/owner-data.js`, `masaha/masaha.css` (`.pf-*`), the «Refactor 2 — the space profile» section of
`docs/design/CHANGES.md`, and `docs/design/INDEX.md` §58. The prototype is a **specification, not code to copy**
(`docs/design/README.md` › Rules for implementing). Where the prototype simulates (touch drag, geolocation, the
clipboard, the pin's drag), production does it for real — say how.

## 2. Read before planning

`CLAUDE.md`; `docs/development/workflow.md`, `engineering-principles.md`, `testing.md`; `docs/features/spaces.md`,
`media.md` (or wherever photos live), `amenities.md`, `lookups.md`, `space-links.md`, `packages.md` (or the packages'
capability), `occupancy.md`, `announcements.md` (closures); `docs/architecture/data-model.md`;
`docs/api/api-contract.md` (the profile's groups, photos, prices, hours, shifts, amenities, contacts); 
`docs/backend/conventions.md`; `docs/frontend/architecture.md`; `docs/frontend/design-system/foundation.md` (§3, §12,
§13 for these screens); the ADRs that touch spaces, media and contacts; the findings index (next free number:
**216**; check). Then the code: the web's owner profile page (`/dashboard/spaces/:spaceId/profile`), the admin's
space editor, «الباقات والأسعار», their hooks, repositories and tests; the API's spaces modules (profile groups, the
staleness dates, photos and their order, prices, hours, shifts, amenities, contacts); `packages/shared` schemas
(`CONTACT_TYPES`, the profile requests); the Prisma schema and migrations for these tables.

## 3. Executor checks the decisions already name — plan each as an `EC…` or settle it by reading

- **S5 / B2 / L2:** hours and shifts share one API group, «عن المساحة» and «الموقع» share another. Can each be saved
  from its own Sheet without touching (or clearing) the other half? Its date and staleness: one per group or per
  section — decide by the API's model and say what the view shows.
- **R3/R6 the custom price description:** does any real row use it (a read of `masaha_dev`, GET or a read-only
  query)? Production drops it from the editor; labelled rows are kept and shown.
- **W5 overnight:** the hours model forbids closing after midnight (confirm where).
- **P4 / C2 order:** how photos' and contacts' order is stored and saved (one request per drop, or the whole order).
- **M4:** every place that reads `CONTACT_TYPES` (the public page's contacts, the admin's, seeds, tests) and how
  «وسيلة أخرى» shows its own name there.
- **R1:** «الباقات والأسعار» shows prices read-only; every link that edits prices lands on the profile's «الأسعار».

## 4. Tests — the owner's bar

**The tests must work and point the right way — never bent to pass; no gap.** A numbered **test matrix** (`T…`), each
test naming the behaviour it proves, the break it catches, and its lane (`testing.md`): the shared schemas (every
rule accepted and refused, exact codes — the new contact types and «وسيلة أخرى»'s name included); the API on real
queries (each group's save alone, partial saves not clearing the other half, staleness and «ما زالت صحيحة», photos'
order and the cover, a shift used by a price or package refused on removal, the migration's existing rows); the web
(view first, each Sheet's save/«رجوع»/«تجاهل التغييرات؟», the completeness bar with **X2**, the side index, the
keyboard drag announced, the delete confirmation «حذف»/«رجوع», the admin's badges with **X3**, Packages read-only, both
languages, axe-clean). Time and platform seams injected as the codebase does; **no production code only a test
uses.** Every new test seen failing first.

## 5. What the plan contains

Number everything. The binding decisions (verbatim); for each section: the files, the API change (routes, shapes,
error codes), the schema change, the web change, the documents (`docs/features/spaces.md` and the other capability
docs, `api-contract.md`, `data-model.md`, `foundation.md`, an ADR only if a decision is architectural), and its tests;
the dependency (name, version, why, bundle cost, `check:build`); the migration (its SQL in full); **the PR split** —
one PR or several (by layer or by section), with your recommendation as an `OD`; the commits (Conventional, atomic);
`EC…`; risks; **"Proposed alternatives"** (you may challenge a decision; never deviate silently); open points for
the owner (`OD…`, each with options and your recommendation).

## 6. Limits (for the plan, and written into it for the executor)

- No migration beyond the one named and approved in the plan; **never `db:seed` `masaha_dev`**; `migrate dev
  --create-only` **once** (a second run applies it); `migrate reset` needs the owner.
- Complete local verification before any PR: `lint`, `typecheck`, `format:check`, `check:classes`, `check:links`,
  `check:conflicts`, `build` + `check:build` (with `NODE_ENV=production`), and `test:unit`, `test:component`,
  `test:api` in full. Two full lanes at once with 8–10 GB free; a third waits. **A lane killed for memory: retry once;
  if killed again, CI judges** — said in the PR and the report.
- Stage by path; never `git add -A` / `git add .`; no tool attribution; no `#PRNUM` left (the next PR is expected to be
  **#140** — checked just before the push). No push to `main`, no merge, no force-push of another branch, no secret
  printed. Workers never stop on file count; they report it. Review fixes fold into their commits (`backup/*` first).
- **Every merge to `main` deploys to production** — the plan says what a visitor or an owner sees change on the day
  of each PR's merge.
