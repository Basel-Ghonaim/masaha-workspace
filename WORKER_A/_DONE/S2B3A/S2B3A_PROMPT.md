# S2b-3a — The admin's spaces screen: the list and its actions

**Worker A** · main folder `C:\Users\basel\masaha` · branch `feat/admin-spaces-list`, cut with
`git switch main`, `git pull --ff-only`, then `git switch -c feat/admin-spaces-list`. The folder is on
`main` at `5d692f3` (after PR #49, the amenities tab) and clean; `masaha_dev` is up to date and the
shared package's `dist` was rebuilt after #48.

**Size cap:** at most 4 subagents in total, and **no self-review subagent** (an independent review
follows the PR). Do not run any workflow. Read what the task needs; don't sweep the repository.

## 1. How to work

- **Start with the `start-work-item` skill.** Plan in plan mode before writing code.
- **Read in the order `docs/development/workflow.md` §2 › *Reading before work* gives:** the
  essentials and the open findings' titles; then **the capability documents first:
  `docs/features/space-links.md`** (the admin's spaces list is its composed read) **and
  `docs/features/spaces.md`** (hide, show, delete, restore), and only the sections they link; then the
  documents whose *read it when* line matches. For this item that includes the sections below.
- **Related findings** (workflow §4): your plan lists the open findings that touch this item, each
  folded in or not, why and its cost; the owner decides. Candidates the analyst sees: **27** (two
  dashboard chunks import each other — new dashboard pages change the chunks: check the manifest, say
  whether it still holds), **35** (no document title — a new page; not expected to be folded).
- **Superpowers: follow workflow §10.** Testing follows `testing.md` §3 rules 5–7: each test seen
  failing first, naming the break it catches. **Make the break once** for: the filters read from and
  written to the address (drop one, see the test fail); the undo calling restore for the space that
  was deleted (restore another id); the 429 hold.
- **The sections this item needs, by document:**
  - `docs/frontend/architecture.md`: §1 (the dependency rule: **no sibling imports**), §2 (the
    dashboard group), §3 (feature layout, operation folders, "components present; hooks prepare",
    **where a place mixes capabilities, the page composes**, what a feature exports, the
    dashboard-only rule), §7 (the `admin` key scope, invalidation, no optimistic updates);
  - `docs/frontend/design-system/foundation.md` §10 (accessibility) and the rows of the components
    you use (DataTable, Pagination, DropdownMenu, AlertDialog, Select or Combobox, Switch, Badge,
    Sheet, Toast, EmptyState, Skeleton);
  - `docs/frontend/localisation.md` (dates, an English-only name in the Arabic interface);
    `docs/development/testing.md` §1–§3 and *A feature, layer by layer*;
  - `docs/api/api-contract.md` §4 (pagination) and §5 › *Spaces (the admin)*: `GET /admin/spaces`
    and its `AdminSpaceRow`, `PUT …/hidden`, `DELETE`, `POST …/restore`.
- **The designs:** SCREENS.md row 26; `docs/design/screens/43-admin-spaces/` frames 01–04 (the list,
  desktop and phone, and "stale only") and 09–10 (the delete); `50-dashboard-variants-arabic-dark/13`
  and `51-dashboard-variants-english-ltr-light/05`. The prototype `docs/design/prototype/Admin
  spaces.html` shows the row menu, the toasts and the undo. Frames 05–08 (owner linking) and 11–16
  (edit, add) are **not** this item.
- **The patterns to follow:** PR #49's amenities, **as fixed after its review** — a failure names
  what failed and is never hidden by a later failure elsewhere; `gcTime: 0` on row actions; the 429
  `blocked` state held while any 429 counts down; the pressed control keeps the focus; rows wrap on
  a phone; the tab kept in the address (`?tab=`) as the model for keeping state there.
- **When finished, follow the `open-pr` skill.**
- **The owner's rules:**
  - honest test titles;
  - **no parameter, option or callback that only tests pass or that nothing uses**; tests stub the
    platform's seams (`fakeTransport` / `fakeAdapter`), never `vi.mock` of a module;
  - **one responsibility per file**, files grouped **by operation**;
  - no hardcoded user-facing text, both catalogues; no colours or CSS outside the design system;
  - **checks:** lint and typecheck on each commit; the full lanes once on the head, one at a time;
    skip `test:api` locally (no API change; CI runs it); `build` + `check:build` once on the head
    (new dashboard pages: the site's first download must not reach them; set `NODE_ENV=production`
    for the build, the web's `.env` sets development); don't re-run a lane that already passed on
    unchanged code;
  - commit subjects of 50 characters or fewer; report only once CI is green on the pushed head;
  - review fixes fold into their commits, with ONE "Review fixes" comment;
  - **rebase only on a real conflict:** if GitHub shows the PR `CLEAN`, don't rebase on `main`;
  - no tool or AI attribution anywhere.

## 2. What this item delivers

The admin's **Spaces** page (`/dashboard/admin/spaces`, today a placeholder): the first half of
screen 26. The owner split the screen in two: **this item is the list and its row actions**; the next
(S2b-3b) adds "Add a space" with the map pin and Leaflet; the edit screen is S2b-4.

**The API is built** (PRs #44, #48): `GET /admin/spaces` with `q`, `status`
(`verified` | `unverified` | `hidden`), `governorateId`, `areaId`, `stale`, `page`, `limit`, answering
`AdminSpaceRow[]` with `meta` (from the `space-links` module); `PUT /admin/spaces/:spaceId/hidden`
(`{ isHidden }`, 204), `DELETE /admin/spaces/:spaceId` (204) and `POST …/restore` (204) (from
`spaces`). A soft-deleted space is never listed.

**What the page shows** (frames 01–04, 09–10):
- desktop: a table — the space's name, its area, its state badge, its owners, its freshness, its last
  update, and a row menu; the count of spaces under it;
- phone: one card per space with the same facts, and the filters behind a "Filters" button;
- the filters: search by name, one "Governorate / area" field, the state, and a "Stale only" switch;
- the row menu: **Hide / Show** and **Delete** (with its confirmation dialog). Its loading, failure
  (with "Try again") and empty states, the empty state also for "no space matches these filters".

## 3. The proposed decisions

The owner approved these after the analysis, **but they are proposals, not orders.** You know the
code best: if you find a stronger option for any of them, put it in your plan under a dedicated
section, **"Proposed alternatives"**, with its trade-off and your recommendation. The owner and the
analyst weigh it; build an alternative only once it is approved.

- **L1 — the page composes two capabilities.** The list's read (its query, its filters' request, its
  rows, its states) is `space-links`' — its web feature already exists, dashboard-only; the row
  actions (hide, show, delete, the undo's restore) are a new web feature, **`features/spaces`**
  (already listed as dashboard-only in `apps/web/scripts/dashboardOnly.ts`). No feature imports the
  other: the page composes them (architecture §3), for example the list taking the row's menu as its
  child or slot. The governorate and area options come from `lookups`, also composed by the page.
  Your plan decides the exact seam; state it, since S2b-4 and the owner's screens will reuse it.
- **L2 — success toasts, as designed** (a first for the admin's screens; the lookups screen keeps
  none): "hidden" / "shown again", and "deleted" with an **Undo** action that calls `restore` for that
  space. The undo is the only way the interface restores a space; **record a finding** (number 44)
  that no screen restores a deleted space once the toast has gone.
- **L3 — the filters and the page live in the address** (`?q=&status=&area=&stale=true&page=2`, your
  plan names them): a reload or the back button keeps them; a missing or invalid value falls back to
  its default; a change of filter returns to page 1.
- **L4 — one "Governorate / area" field,** as designed: a governorate, then its areas under it;
  choosing a governorate sends `governorateId`, an area `areaId`. Whether it lists hidden
  governorates and areas (the admin's lists) or the active ones only (the public catalogue) — your
  plan recommends; a hidden area's spaces still exist.
- **L5 — a failed action names its space.** The analyst proposes an error toast that names the space,
  with the request's reference; a 429 holds every row's menu while it counts down, as in #49. Your
  plan may propose another place (the dialog, the row), with its reason.
- **L6 — freshness shows stale and missing groups,** both: the design predates "missing" (#48). Your
  plan proposes how (for example "Stale: prices, contacts" and "Missing: hours"), in the badge's
  existing variants.
- **L7 — no entry points that lead nowhere:** the "Add space" button and the menu's "Edit" arrive with
  S2b-3b, which builds their routes. The owner-linking items (step 4) are not shown.

**Fixed by the documents or by earlier PRs** (flag any you find no longer holds):
- query keys under the `admin` scope; after a write the list is invalidated and the mutation stays
  pending until the refetch answers; no optimistic update;
- `space-links` and `spaces` are dashboard-only on the web; the site's first download never reaches
  them (`check:build`);
- an English-only name shows marked `lang="en"` in the Arabic interface (space-links' decision);
- the rows' order, states and filters are the contract's; the web computes none of them.

**Decided for S2b-3b, not this item** (don't build them, don't preempt them): "Add a space" is a
creation form with the basics and the location only, its two sections built for reuse by the edit
screen; after a creation the admin goes to the edit route (a placeholder until S2b-4); the pin also
takes typed or pasted coordinates; OpenStreetMap's standard tiles in both themes; `leaflet.css`
inside the design-system layer.

## 4. Your plan decides

- the files per operation in each feature, the page's composition (L1), the address's parameter names
  (L3), the page size (`limit`) and the pagination's place;
- the copy, both languages; **list the Arabic lines for the owner's approval**;
- the tests, per testing.md, one behaviour in one lane:
  - the repositories' calls in the unit lane (the list's query string from each filter; hide, delete,
    restore);
  - the hooks: the filters from and to the address, the page, each action and its invalidation, the
    toasts and the undo, each failure's view, the 429 hold;
  - the components: the table and the cards, the badges, the menu (keyboard, accessible names that
    carry the space's name), the delete dialog and its focus, the filters (the phone's sheet
    included), the states, axe;
  - the page: the composition, the default address, an invalid parameter;
- the documents, **one owner per fact** (`docs/architecture/documentation.md`):
  **`docs/features/space-links.md`** gains the web section of the admin's list, and
  **`docs/features/spaces.md`** its first web section (its header says "No web feature yet"): their
  decisions (L1–L7, each with its reason, date and PR), code maps and history;
  `docs/frontend/architecture.md` §2's "Built so far" line (the spaces page); `overview.md` › *Built*'s
  spaces line; the new finding 44. Never restate in a platform document what a capability document
  now owns;
- the commits (3–6, each a complete unit).

## 5. Out of scope

- "Add a space", the map, Leaflet, the edit screen and its route (S2b-3b, S2b-4).
- Linking and unlinking owners, and their menu items (build step 4).
- A view of deleted spaces; any API change; new dependencies. If you think one is needed, stop and
  ask.

If the plan finds the documents or the API missing something this item needs, stop and report:
record it, don't absorb it.

## 6. Parallel work

Worker B works in the worktree `masaha-b` at the same time; its next item is not yet chosen, and it
will be one that avoids your files.
- **Declare in your plan every file outside `features/space-links`, `features/spaces` and the spaces
  page** that you will edit (for example `pages/dashboard/routes.tsx`, the copy catalogues' index,
  `features/lookups`' exports, the design system, `overview.md`, `architecture.md`, `findings.md`),
  and edit each minimally, in your own section.
- **No new dependency:** `package-lock.json` must not change in this item.
- **Findings numbering:** `main` ends at 43. **Number yours from 44**; worker B numbers from 48. If a
  conflict appears later, the PR is rebased then, keeping both sides.
- Your databases are `masaha_dev` and `masaha_test`; your API runs on 3320 and your web on 5320. Stop
  every server you started afterwards and check the ports are free.

## 7. Pull request

- **Title:** `feat(spaces): add the admin's spaces list` (or the main commit's subject).
- **Labels:** `feat`, `area:web`, `area:docs`. Assigned to the owner.
- **The description:** scope, acceptance criteria and out of scope; L1–L7 and any alternative
  approved; evidence per lane; what was not run.
- **Screenshots** of every state (RTL and LTR, light and dark, phone and desktop: the list with a
  verified, an unverified, a hidden, a stale and a missing-groups space; "stale only"; filters applied
  and the phone's filter sheet; the row menu; the delete dialog; the toasts with Undo; a failure;
  loading, error, empty and no-match) go to `C:\Users\basel\Downloads\s2b3a-shots`, never committed.
  The demo seed (`SEED_DEMO=true`) adds one space only: create the others in `masaha_dev` through
  the API itself (`POST /admin/spaces`, the facts' `PUT`s, `PUT …/hidden`), never through a script
  committed to the repository.
- **Review:** an independent review, after you report.
- After CI is green on the pushed head, stop and report: the head, the commits, the counts per lane,
  your tokens. Don't merge. Don't create an Issue.
