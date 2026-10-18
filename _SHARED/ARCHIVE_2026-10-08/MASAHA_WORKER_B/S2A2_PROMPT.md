# S2a-2 — The admin's lookups screen: governorates and areas

**Worker B** · worktree `C:\Users\basel\masaha-b` · branch `feat/admin-lookups-screen`, cut with
`git fetch --prune origin` then `git switch --no-track -c feat/admin-lookups-screen origin/main`.
**Start only once PR #41 (the lookups API) is merged;** the owner will tell you. If the worktree is
still on `feat/admin-lookups-api`, switch to detached `origin/main` first (leave the local branch:
deleting it is the owner's).

**Size cap:** at most 4 subagents in total, and **no self-review subagent** (an independent review
follows the PR). Do not run any workflow. Read the documents and sections named here; don't sweep the
repository.

## 1. How to work

- **Start with the `start-work-item` skill.** Plan in plan mode before writing code.
- **The owning documents, by section:**
  - `docs/frontend/architecture.md`: §1 (zones), §2 (the dashboard group, its layout tree, guards
    on each route, lazy loading), §3 (feature layout, operation folders, "components present; hooks
    prepare", React Query side effects, where state lives, what a feature exports, Forms), §7 (query
    keys, invalidation, retries, query defaults, no optimistic updates except favourites);
  - `docs/development/testing.md` §1–§3 and *A feature, layer by layer*;
  - `docs/frontend/localisation.md` (catalogues, **plurals**);
  - `docs/frontend/design-system/foundation.md` › the components you use (Card, Sheet, Switch,
    Badge, Button, EmptyState, Skeleton) and §10 (accessibility);
  - `docs/api/api-contract.md` §5 › *Lookups (the admin)* (built by PR #41), and §3;
  - `docs/plans/v1-mvp.md` step 2.
- **The designs:** SCREENS.md row 30; `docs/design/screens/47-admin-lookups/` frames 01–04
  (governorates and areas, desktop and phone; the edit sheet with a hidden area); frame
  `50-dashboard-variants-arabic-dark/14-admin-lookups-dark.webp`. Frames 05–06 (amenities) are the
  next item's.
- **When finished, follow the `open-pr` skill.**
- **The owner's rules:**
  - honest test titles;
  - **no parameter, option or callback that only tests pass or that nothing uses**; tests stub the
    platform's seams (`fakeTransport` / `fakeAdapter`, `vi.stubGlobal`), never `vi.mock` of a module;
  - **pages pass no navigating callbacks**; guards own navigation;
  - **one responsibility per file**, files grouped **by operation** inside `hooks/` and
    `components/` (architecture.md §3);
  - no hardcoded user-facing text, both catalogues; no colours or CSS outside the design system;
  - **checks:** lint and typecheck on each commit; the full lanes (`check:classes`, unit,
    component, api, build + `check:build`) once on the head, one at a time; don't re-run a lane that
    already passed on unchanged code;
  - commit subjects of 50 characters or fewer; report only once CI is green on the pushed head;
  - review fixes fold into their commits, with ONE "Review fixes" comment;
  - **rebase only on a real conflict:** if GitHub shows the PR `CLEAN`, don't rebase on `main`;
  - no tool or AI attribution anywhere.

## 2. What this item delivers

The admin's **Lookups** page at `/dashboard/admin/lookups` (today a placeholder): the governorates
and their areas, which the admin adds, renames, hides, restores and orders. It is the first real
dashboard screen and the first admin management screen; its patterns (a side sheet for add and
edit, actions from a row, pending states) will be reused by every admin screen after it.

**The API is built** (PR #41): `GET /admin/governorates` (each governorate with its areas, hidden
ones included, in order); `POST /admin/governorates`, `PATCH /admin/governorates/:id`;
`POST /admin/areas`, `PATCH /admin/areas/:id`; `PUT /admin/governorates/order` and
`PUT /admin/governorates/:id/areas/order` with `{ ids }` (204). Hiding and restoring are `isActive`
in the `PATCH`. A duplicate Arabic name is 409 with `errors.nameAr = ["not_unique"]`; a stale order
is 409. The types and schemas come from `@masaha/shared/lookups`.

**What the page shows** (from the designs):
- the page's title in the dashboard's top bar (`PageHeader`), and the hint line: hidden items don't
  appear in filters and forms, the spaces linked to them stay as they are, and the order here is the
  order shown;
- one card per governorate: its names, its count of areas, its active switch, its up and down
  arrows, and "Edit"; inside it, its areas as rows with the same controls and a "Hidden" badge when
  hidden; "Add area" at the card's foot. A hidden governorate's card is dimmed;
- "Add governorate" at the page's foot;
- a side sheet to add or edit: the Arabic name, the English name and, when editing only, the
  "Active" switch with its hint; "Save";
- loading, error (with "Try again") and empty states.

## 3. The proposed decisions

These came out of the analysis and the owner agrees with them, **but they are proposals, not
orders.** You know the code best: if you find a stronger option for any of them, put it in your plan
under a dedicated section, **"Proposed alternatives"**, with its trade-off and your recommendation.
The owner and the analyst weigh it; build an alternative only once it is approved.

- **K1 — a query-key scope for the admin:** `['admin', 'lookups', …]`, added to architecture.md §7
  beside `space`, `me` and `public`. The admin's lists include hidden rows and are never the public's.
- **K2 — after a write, invalidate the governorates list** so it is fetched again: the server stays
  the one source of truth, and the list is a few dozen rows. No cache surgery from responses.
- **K3 — no optimistic updates, and no racing orders:** a row's switch and arrows are disabled while
  its request is pending, and every arrow of the same list is disabled until an order request
  answers. The first and last rows' outward arrows are disabled.
- **K4 — a row action's failure shows inside its governorate's card,** above its rows, with the
  shared failure view (`useRefusalView` / `FormFailure`). A 409 on an order refetches the list and
  says the order changed and to try again. No toasts in this item.
- **K5 — the count of areas uses real Arabic plurals:** this is the project's first counted line, so
  it brings the plural mechanism localisation.md describes (`Intl.PluralRules`, all six Arabic
  categories) and its test ("11 منطقة", never "11 مناطق"). Build it as that document says, in
  `shared/copy`.
- **K6 — no tabs yet, but ready for them:** the design has two tabs (governorates and areas;
  amenities), and amenities come in the next item. This item shows the governorates list directly,
  with **no tab UI and no unused abstraction**, but its structure must let the next item add the
  amenities tab without reshaping it: the page composes one self-contained section (the governorates
  list with its own query, failure and add action), so a second section can sit beside it under
  tabs. Describe in your plan how the next item would add the tab.
- **K7 — names: English first.** Most names are used in English, so each governorate and area shows
  its **English name as the primary line** and its Arabic name as the secondary, smaller one, in both
  interface languages.
- **K8 — the "Active" switch appears only when editing:** a new governorate or area is always
  active (the create request has no `isActive`).

**Fixed by the documents** (flag any you find no longer holds):
- the route keeps its visible `RequireRole roles={['ADMIN']}` guard and loads its page lazily; the
  server is the authority;
- `features/lookups` is one capability, usable later by any page group (architecture.md §3); the
  public read (`GET /lookups`) is not built yet and is out of scope;
- the feature exports UI first: the page composes what the feature offers; nothing internal leaves
  `index.ts`;
- TanStack Query's `retry` is off; the transport retries only `GET`s;
- an error loading the list is the page's own state (an `EmptyState` with "Try again"), not a route
  error.

## 4. Your plan decides

- the feature's files: the repository (one per capability), the hooks per operation (the list, add,
  edit, hide and restore, order), the components, the pure helpers in `services/` (for example the
  new order after an arrow);
- the sheet's form hooks on `useServerForm` (create and update schemas from `@masaha/shared/lookups`)
  and where a 409 `not_unique` lands (on its field);
- the layout on a phone (frames 02 and 04) and in dark mode;
- the copy: every new line, both languages; **list the Arabic lines for the owner's approval**;
- the tests, per testing.md, one behaviour in one lane:
  - the repository's calls in the unit lane;
  - the pure helpers and the plural mechanism in the unit lane;
  - the hooks with `renderHook` through the fake adapter: the list, each write and its
    invalidation, the pending and disabled states, each failure's view, the 409 on an order;
  - the components on rendering: the cards, the hidden badge and dimming, the disabled arrows, the
    sheet's fields, focus and errors, the states; axe;
  - the route: the page shows for the admin (the existing dashboard routes test);
- the documents: architecture.md (§7 the admin scope, §3 the feature's exports, the status line),
  localisation.md (the plurals built), and anything else your changes make untrue;
- the commits (3–5, each a complete unit).

## 5. Out of scope

- The amenities tab, the amenity icons and finding 10 (the next item, S2a-3).
- Any API change; `GET /lookups`; `overview.md` › *Built* (S2a-3 writes it).
- Toasts; the dashboard's own 404 and error states.
- New dependencies. If you think one is needed, stop and ask.

If the plan finds the documents or the API missing something this item needs, stop and report:
record it, don't absorb it.

## 6. Parallel work

Another worker may be working in the main folder at the same time.
- **Declare in your plan every file outside your own feature and page** that you will edit (for
  example the copy catalogues' `index.ts`, architecture.md, localisation.md, `findings.md`), and edit
  each minimally, in your own section.
- Number any new finding after the last one on `main` when you start; if a conflict appears later,
  the PR is rebased then, keeping both sides.
- Your databases are `masaha_b_dev` and `masaha_b_test`; your API runs on 3321. For the browser
  check, point Vite's proxy at 3321 with a scratch config that is never committed (finding 29).

## 7. Pull request

- **Title:** `feat(lookups): add the admin's governorates screen` (or the main commit's subject).
- **Labels:** `feat`, `area:web`, `area:docs`. Assigned to the owner.
- **The description:** scope, acceptance criteria and out of scope; the decisions K1–K8 and any
  alternative approved; evidence per lane; what was not run.
- **Screenshots** of every state (RTL and LTR, light and dark, phone and desktop: the list, a hidden
  governorate and area, the sheet adding and editing, a field error, a row failure, loading, error,
  empty) go to `C:\Users\basel\Downloads\s2a2-shots`, never committed.
- **Review:** an independent review, after you report.
- After CI is green on the pushed head, stop and report: the head, the commits, the counts per lane,
  your tokens. Don't merge. Don't create an Issue.
