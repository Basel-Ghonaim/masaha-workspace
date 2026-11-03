# BACKEND_FINAL — the rest of the API in one unified plan: finance, the overviews, and every API item left — PLAN ONLY

You are worker B's **planner**, in `C:\dev\masaha\app-b`, in a fresh conversation. You write **one plan** and stop.
You build nothing. Do not run the `start-work-item` skill (the owner's instruction for this task); `CLAUDE.md` is in
your context.

## 0. What the owner wants (2026-10-29) — read this twice

- **One plan that finishes the API of Masaha v1.** It holds, merged into one document, **everything**: (1) the space's
  **finance** (build map step 11's last part — today planned as PR 3 of `FINANCE_AUDIT`), (2) **the owner's and the
  admin's overviews** (build map step 12, never planned), (3) **every API item still left** (§4 below).
- **The plan stands alone, literally.** It must not send its reader to another plan, prompt or report for anything it
  needs: **copy into it, in full, every decision, rule, route, shape, query, test and break it relies on** — the
  finance part included (re-verified, §2). Pointers to the **repository's own documents** (the contract, conventions,
  data model, ADRs, findings) are allowed as the source of truth for what is built; never to workspace files.
- **It is ours to edit.** Number everything (sections, decisions `D…`, stronger decisions `S…`, tests `T…`/`U…`,
  breaks `B…`, design issues `DI…`), so the owner and the supervisor can change one item by its number. Each decision:
  its one-line reason and its undo. Put the owner's decisions in one binding section, verbatim.
- **It is executed by a lead with sub-agents, in one PR** (as worker A's step-10 run, #129): the execution rules
  (lanes, joins, test runs, stops) are **being settled by the owner and the supervisor in parallel** and will come in
  the execution prompt. Your plan provides what they need: **the units of work, their dependencies, the files each
  touches, which units can run in parallel and which must come first, and the shared files** (§5, *Lanes*).
- **Plan only:** no branch, no edit to the repository, no build, no test run, no server, no database command, no
  trial copy or worktree. Read with `git show origin/main:<path>`, `git grep`, `git log`, `gh`. A point you cannot
  prove by reading becomes an **executor check** in the plan (what to check, what to do if it fails).

## 1. The base

`git fetch origin`; `git switch --detach origin/main` in `C:\dev\masaha\app-b` (clean). `main` = **`e3b2f97b`** or
later: **#128** (the audit reader; finding 151; account events of a space's reception carry the space) and **#130**
(the platform settings: three admin cards, the public contact, `AuditEntry.entityId` may be `null`, the staleness
thresholds in the typed catalogue) are merged. **#129** (worker A: announcements, data reports, favourites screens —
`apps/web`, `docs`) is open in its fix round and may merge while you plan: it touches no API file; shared documents only
(`overview.md`, `architecture.md`, the findings index, `docs/README.md`). Finding numbers: **yours start at 154**
(A's run uses 174–189).

## 2. Part one — the finance (re-verified, merged in full)

The approved finance plan is part of `C:\dev\masaha\workspace\WORKER_B\FINANCE_AUDIT\2_PLAN.md` — **read it as your
source only; your plan must not point to it.** Read: the owner's approval note at its top; §2's PR 3 scope and
acceptance criteria; §4's owner's decisions (the 12 of 2026-10-26 — income = cash collected without voids; Gaza
months and fixed windows, no free range; the server aggregates; CSV built by the web, no export route; finance the
owner's alone; occupancy from closed stays, auto check-outs included; and the rest), **D8–D12**, D13, D14, D15's PR 3
part; §5 **S2, S3** and the rules; §6; §7's PR 3 rows; §9 *PR 3*; §10; §11 *PR 3*; §12's PR 3 checks; §13 (Q1–Q12,
approved as recommended); Appendix A *PR 3*. Also `C:\dev\masaha\workspace\WORKER_B\FINANCE_AUDIT\1_PLAN_PROMPT.md` §2
(the owner's decisions as he gave them).
**Then re-verify every finance claim against `origin/main` as built** — it was written before #128 and #130 merged:
the `payments` repository and service as they stand (the ledger's aggregates D10 plans to add — do any exist now?),
`customers.contactsOf`, `occupancy`'s closed stays, `core/gazaTime.ts` (does `monthOf`/`addMonths` exist?), the audit
writer (`entityId: number | null` now), `can()`'s `finance.read`, the lint level map (`finance` L5). **Copy the
finance part into your plan in full, corrected where `main` changed it, each correction marked `(re-verified
2026-10-29: …)`.**

## 3. Part two — the overviews (build map step 12) — the owner's decisions, binding

**The owner's decisions (2026-10-29), verbatim intent — put them in your plan's binding section:**
- **OV1 — the owner's overview (screen 12) is a work queue with no amount anywhere** (the owner's O3, amended
  2026-10-12: income and the debts' total are sensitive and the overview is often open at the desk, in view of
  customers and staff; they live in Finance only). Its order: **«يحتاج انتباهك»** first — the space's groups missing
  or stale, new data reports, the uncollected visits (a count), a started closure without its extension, capacity not
  set; then **«الحاضرون الآن»** — present now, capacity and the live status; then **the subscriptions ending this
  week** and **the announcements running**. Each item a count and a link to where it is acted on; confirm only beside
  what it confirms.
- **OV2 — debts on the owner's overview:** «عملاء عليهم ديون» as a **count of customers** only, linking to Finance ›
  debts; no amount.
- **OV3 — the overview is the owner's only.** Reception has none (it lands on the desk, as today).
- **OV4 — the admin's overview (screen 25) is a work queue** (the owner's A8): the tiles — spaces verified,
  unverified, **unverified with no owner**, open data reports, new users; **«اكتمال البيانات»** — the first five
  spaces with a group missing or stale that the admin can act on, with «عرض الكل»; missing is a warning, stale counts
  too (the tile and the card count stale **and** missing).
- **OV5 — "new users" = the last 30 days on Gaza's calendar.**
- **OV6 — "stale" uses the staleness thresholds the admin saves in the platform settings (#130)**, on both screens;
  never a constant in code.
- **OV7 — one aggregate endpoint per screen** (conventions §9, *overview*: the users' connection is weak), every
  figure from its owning module (no logic in `overview`; it never imports `finance` — the figures both show come from
  `payments`; fetched in parallel); no polling — the web refreshes on return to the page.
- **OV8 — the foundation's screen 12 line** (`docs/frontend/design-system/foundation.md` §13: "income today and this
  month, total debt") is corrected to OV1 by this plan, as O3 ordered.
**Read for this part:** the conventions' `overview` section and §8 R7 (read models), §9 *Composed reads*; the
contract's routes every figure comes from (spaces' groups and confirmations, staleness, data reports, desk's
uncollected, occupancy's present, `closures.summary`'s `closuresAwaitingExtension`, subscriptions ending, announcements
running, customers with debt, users, owners' links); `docs/design/SCREENS.md` (12, 25) and the prototypes
`docs/design/prototype/Owner overview.html`, `Admin overview.html` (at `origin/main`); the workspace's design decisions
`C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_OWNER.md` (O3 and its 2026-10-12 amendment) and
`DECISIONS_ADMIN.md` (A8) — **copy what you use into the plan**. Design each endpoint: route, guard (`requireCan`),
the answer's shape (shared types in `packages/shared`), each figure's owning module and the set-based API it calls
(add one where none exists — say so), the queries and their cost on a busy space, the lock and snapshot rules (D14's
style), the tests, the breaks. **Proposed alternatives** where you see a better way — argued, not applied.

## 4. Part three — every API item left (find them; propose in or out)

Sweep `origin/main` and list each with a recommendation **in this plan / out (and why)** for the owner:
- **Carried from #130's review** (`C:\dev\masaha\workspace\WORKER_B\FINANCE_AUDIT\6_REVIEW_PR2_CLAUDE_CODE.md`,
  findings F1–F4 — copy each in full): F1 a contact stored in another form (`+972…`, mixed-case email) answered as
  stored and rewritten by the next save — a test pair and one sentence in the contract; F2 finding 153's wording and its
  foreign-number case; F3 `platform-settings.md`'s "in the browser too"; F4 "changes no value". **These are in** (the
  owner's rule: small review fixes ride the next PR's first commit).
- **Open findings on the API side:** read the findings index at `origin/main` and every open finding whose fix is in
  `apps/api`, `packages/shared` or the seed — at least **153** (the seed accepts any contact form), **187** (re-saving a
  favourite just removed, for an undo — recorded by #129's fix round; may not be on `main` yet), **152** (the audit's
  retention — the owner's decision; propose options), **170**, **171** (171 is the owner's to confirm). Each: what,
  where, the fix, size, in/out.
- **`docs/plans/v1-mvp.md`'s *Planned API surface***: any route listed and not built (outside finance and the
  overviews) — in/out.
- **`docs/README.md`'s *Deferred documents***: any trigger this plan meets — the document owed, written by the plan's
  PR.
- **`C:\dev\masaha\workspace\_SHARED\OPEN_DECISIONS.md`**: any point the finance or the overviews settle or build
  (point 3 is finance's) — what the report must write there.

## 5. The plan's shape (number everything)

1. **Header:** base sha, what it read, what it could not prove (→ executor checks), the size (files, commits), the
   finding numbers it uses.
2. **The owner's decisions, binding:** the finance's 12 (2026-10-26), Q1–Q12 as approved, and OV1–OV8 — verbatim.
3. **Scope, acceptance criteria, out of scope** — per part, each criterion testable.
4. **The reading done** — what `main` shows that the finance plan did not know (re-verified lines).
5. **Decisions as built** (`D…`): routes and answers (one table per part), shared shapes, queries, services, windows,
   aggregates, locks and snapshots, bounds and cost — the finance's re-verified and the overviews' new; **stronger
   decisions** (`S…`) and **Proposed alternatives**.
6. **Related findings** — folded or recorded, with numbers.
7. **The files** — per unit, each file A/M with its purpose.
8. **The units of work and the lanes:** every commit (subject ≤ 50, its contents, its tests), grouped into **units**;
   for each unit its dependencies; **which units can run in parallel, which must come first** (e.g. the `payments`
   aggregates both parts read; the shared types); **the shared files** (the contract, conventions, data model,
   `app.ts`, the shared index, the audit lists, `v1-mvp.md`, `overview.md`) and how each lane adds to them without
   colliding; a recommended number of lanes and their order — a proposal; the execution prompt decides.
9. **Tests** — each with its lane (`*.unit.test.ts`, `*.api.test.ts`), title, and **the break that must make it fail**;
   *Not tested, and said*; *Review Focus* (inputs no test exercises).
10. **The real run** — on 3321, `masaha_b_dev`: each case, each role, **every write named** and put back where it can
    be; what the demo data lacks (→ not performed, with why, never changed through the app).
11. **Documents** — every repository document each unit changes (contract, conventions, data model, ADRs if any,
    security, feature documents — `finance.md` and `overview.md` capability documents new —, `v1-mvp.md` *Built*,
    `overview.md` *Built*, `docs/README.md`, foundation §13's screen 12 line, the findings and the index), one home per
    fact, `#PRNUM` where the number goes.
12. **The decisions needed from the owner** — each with options and a recommendation, numbered.
13. **Executor checks** — each with what to do if it fails.

## 6. Write it, then stop

Write the plan to `C:\dev\masaha\workspace\WORKER_B\BACKEND_FINAL\2_PLAN.md` (write nothing else outside the
repository except notes in `C:\dev\masaha\workspace\WORKER_B\BACKEND_FINAL\scripts\`). English. Then **stop** and
reply:

```
Plan: C:\dev\masaha\workspace\WORKER_B\BACKEND_FINAL\2_PLAN.md
Base: <sha>
Parts: finance (<n> routes, re-verified: <n> corrections) · overviews (<n> routes) · left items (<n> in, <n> out)
Units: <n> · commits <n> · lanes proposed <n> · files ≈ <n>
Owner decisions needed: <n> (one line each)
Executor checks: <n>
Proposed alternatives: <n>
```
