# S2a-3 — The admin's lookups screen: the amenities tab

**Worker B** · worktree `C:\Users\basel\masaha-b` · branch `feat/admin-amenities-screen`, cut with
`git fetch --prune origin` then `git switch --no-track -c feat/admin-amenities-screen origin/main`.
The worktree is detached at `origin/main` (`a1f5aba`, after the feature-documents PR #47) and clean.

**Size cap:** at most 4 subagents in total, and **no self-review subagent** (an independent review
follows the PR). Do not run any workflow. Read what the task needs; don't sweep the repository.

## 1. How to work

- **Start with the `start-work-item` skill.** Plan in plan mode before writing code.
- **Read in the order `docs/development/workflow.md` §2 › *Reading before work* gives:** the
  essentials and the open findings' titles; then **`docs/features/lookups.md` first** (what the
  capability does, its decisions — the governorates screen's among them — and its code map) and only
  the sections it links; then the documents whose *read it when* line matches. For this item that
  includes the sections below.
- **Related findings** (workflow §4): your plan lists the open findings that touch this item, each
  folded in or not, why and its cost; the owner decides. Finding 10 is already in scope.
- **Superpowers: follow workflow §10.** Testing follows `testing.md` §3 rules 5–7: each test seen
  failing first, naming the break it catches; for the 429 and ordering properties, make that break
  once and watch the test fail.
- **The sections this item needs, by document:**
  - `docs/frontend/architecture.md`: §1, §2 (the dashboard group), §3 (feature layout, operation
    folders, "components present; hooks prepare", React Query side effects, *Where state lives*, what
    a feature exports, Forms), §7 (the `admin` key scope, invalidation, no optimistic updates);
  - `docs/frontend/design-system/foundation.md` §3 (the layer's architecture and its icon set), §10
    (accessibility), and the rows of the components you use (Tabs, Switch, Badge, RadioGroup or
    ToggleGroup, Sheet);
  - `docs/frontend/localisation.md`; `docs/development/testing.md` §1–§3 and *A feature, layer by
    layer*;
  - `docs/api/api-contract.md` §5 › *Lookups (the admin)* (amenities); `docs/architecture/data-model.md`
    › *Lookups* (Amenity: key, icon, filter flag);
  - findings 10 (the amenity icons) and 30 (an amenity's English name may repeat).
- **The designs:** SCREENS.md row 30; `docs/design/screens/47-admin-lookups/` frames 05–06
  (amenities, desktop and phone) and 01 (the tabs); `50-dashboard-variants-arabic-dark/14`.
- **The pattern to follow:** PR #43's governorates section, **as fixed after its review** (a failure
  stays until the user acts again on that row; `gcTime: 0` on row actions; the 429 `blocked` state
  honoured; one add button in one place; the pressed control keeps the focus; rows wrap on a phone).
  Copy the fixed pattern, never the pre-review one.
- **When finished, follow the `open-pr` skill.**
- **The owner's rules:**
  - honest test titles;
  - **no parameter, option or callback that only tests pass or that nothing uses**; tests stub the
    platform's seams (`fakeTransport` / `fakeAdapter`), never `vi.mock` of a module;
  - **one responsibility per file**, files grouped **by operation**;
  - no hardcoded user-facing text, both catalogues; no colours or CSS outside the design system;
  - **checks:** lint and typecheck on each commit; the full lanes once on the head, one at a time;
    skip `test:api` locally (no API change; CI runs it); don't re-run a lane that already passed on
    unchanged code;
  - commit subjects of 50 characters or fewer; report only once CI is green on the pushed head;
  - review fixes fold into their commits, with ONE "Review fixes" comment;
  - **rebase only on a real conflict:** if GitHub shows the PR `CLEAN`, don't rebase on `main`;
  - no tool or AI attribution anywhere.

## 2. What this item delivers

The **Amenities** tab of the admin's Lookups page, which completes the screen (S2a-1 built the API,
S2a-2 the governorates and areas). It closes finding 10, adds the tab to `docs/features/lookups.md`,
and updates the lookups line of `overview.md` › *Built* (today: "the amenities … on the API").

**The API is built:** `GET /admin/amenities` (in order, retired ones included), `POST` and
`PATCH /admin/amenities/:id` (names, `icon` from `AMENITY_ICON_KEYS`, `isFilterable`, and `isActive`
on edit), `PUT /admin/amenities/order` with `{ ids }` (204). The key is derived from `nameEn` on the
server when an amenity is added and never changes; a taken key is 409 with
`errors.nameEn = ["not_unique"]`.

**What the tab shows** (frames 05–06): the hint line; one ordered list; each amenity with its icon,
its names, a "Not in filters" badge when not filterable, an "In filters" switch, an "Active" switch,
up and down arrows, and "Edit"; "Add amenity". A side sheet adds and edits: the Arabic and English
names, the icon, "In filters", and "Active" when editing only.

**The page:** the two sections under the design system's `Tabs` — "Governorates and areas" (the
default) and "Amenities" — with the tab kept in the URL (`?tab=amenities`), as PR #43 planned.

## 3. The proposed decisions

These came out of the analysis and the owner approved them, **but they are proposals, not orders.**
You know the code best: if you find a stronger option for any of them, put it in your plan under a
dedicated section, **"Proposed alternatives"**, with its trade-off and your recommendation. The owner
and the analyst weigh it; build an alternative only once it is approved.

- **T1 — the icon's map lives in the design system, by glyph name:** the layer exports one icon
  component by its glyph's name (for example `<GlyphIcon name="wifi" />`), with a closed type of the
  names it supports; it still knows nothing of amenities. `features/lookups` checks at compile time
  that every `AMENITY_ICON_KEYS` entry is one of those names (`satisfies`), and renders the amenity's
  icon through it. So the directory (build step 3) can draw the same icons without importing a
  sibling feature. A small, tested change to the layer, with its line in foundation.md §3. This is
  what finding 10's "map from key to icon" becomes; resolve finding 10.
- **T2 — an amenity shows its name in the interface's language first,** the other language as the
  secondary line. (The governorates' "English first" rule was made for place names; amenities are
  common words.)
- **T3 — the icon is picked from a visible grid** of the eight icons (`RadioGroup` or `ToggleGroup`,
  your plan chooses), each with an accessible name, one selected.
- **T4 — amenity hooks mirror the governorates' pattern,** one per operation (the list, add, edit,
  visibility, filter flag, order); the components and helpers that are already generic
  (`RowControls`, `LookupSheet`, `LookupNameFields`, `moved`, …) are reused as they are. **No generic
  hook factory** across lookups: two examples are too few to generalise.
- **T5 — both switches sit in the row,** as designed, each with its own pending state, both following
  the section's failure pattern.
- **T6 — no success toasts,** as in the first tab, so the page stays consistent. (Whether admin
  screens use success toasts at all is a separate, later decision for every screen.)

**Fixed by the documents or by PR #43** (flag any you find no longer holds):
- the query keys under `['admin', 'lookups', …]`; after a write the list is invalidated and the
  mutation stays pending until the refetch answers; no optimistic update;
- the section owns its loading, error and empty states; the page composes the sections;
- accessible names carry the name in the interface's language;
- finding 30 stays open: the web does not try to prevent a repeated English name (only the server
  could, without a race);
- the key is never typed or shown as an editable field.

## 4. Your plan decides

- the files per operation, the tab's URL handling (a missing or unknown `tab` falls back to the
  first), and the page's composition;
- **whether the governorates section needed any change to sit under a tab** — PR #43 claimed it was
  ready. If it did, say exactly what and why: the owner wants to learn from it for later admin
  screens;
- the copy, both languages; **list the Arabic lines for the owner's approval**;
- the tests, per testing.md, one behaviour in one lane:
  - the design system's glyph icon (each supported name renders; the compile-time check covers the
    amenity keys);
  - the repository's amenity calls in the unit lane;
  - the hooks: the list, each write and its invalidation, the two switches' independent pending
    states, the order, each failure's view, 409 `not_unique` on `nameEn`;
  - the components: the icon and names (T2), the badge, the switches, the arrows, the sheet's fields
    and icon grid (keyboard and accessible names), focus, the states, axe;
  - the page: the tab from the URL, switching tabs, the default;
- the documents, **one owner per fact** (`docs/architecture/documentation.md`):
  **`docs/features/lookups.md` in this PR** — its web section gains the amenities tab, its decisions
  gain T1–T6 (each with its reason, date, PR), its code map and history follow; foundation.md §3
  (T1, a platform rule: the glyph icon); `overview.md` › *Built*'s lookups line if it changes;
  finding 10 resolved. Never restate in a platform document what `lookups.md` now owns;
- the commits (3–5, each a complete unit).

## 5. Out of scope

- Any API change. The public `GET /lookups` (built by the admin spaces API item).
- New icons beyond the eight; a generic lookups hook factory; success toasts.
- New dependencies. If you think one is needed, stop and ask.

If the plan finds the documents or the API missing something this item needs, stop and report:
record it, don't absorb it.

## 6. Parallel work

Another worker may be working in the main folder at the same time.
- **Declare in your plan every file outside `features/lookups` and the lookups page** that you will
  edit (for example the design system's icons and `index.ts`, the copy catalogues, foundation.md,
  `overview.md`, `findings.md`), and edit each minimally, in your own section.
- **Findings numbering:** main ends at 41; the other worker numbers from 42, so **number yours from
  46**. If a conflict appears later, the PR is rebased then, keeping both sides.
- The other worker builds the spaces' facts API: it edits `docs/features/spaces.md`, the API contract,
  the data model, a migration and `findings.md`, and may touch `overview.md`'s spaces line. Keep to
  your lines.
- Your databases are `masaha_b_dev` and `masaha_b_test`; your API runs on 3321. For the browser
  check, run this worktree's own web on its own port: set `WEB_PORT=5321` and
  `API_PROXY_TARGET=http://localhost:3321` in `apps/web/.env` (never committed; setup.md › *Running a
  second folder*). No scratch Vite config any more. Stop every server you started afterwards and
  check the ports are free.
- **Also fold in one pattern fix from PR #43's review:** `RowControls` styles its own
  `aria-disabled:opacity-50`; give the design system's `Button` an `aria-disabled` appearance instead
  (the same as `disabled`), so every admin screen gets it, and drop the local class.

## 7. Pull request

- **Title:** `feat(lookups): add the admin's amenities tab` (or the main commit's subject).
- **Labels:** `feat`, `area:web`, `area:design-system`, `area:docs`. Assigned to the owner.
- **The description:** scope, acceptance criteria and out of scope; T1–T6 and any alternative
  approved; evidence per lane; what was not run.
- **Screenshots** of every state (RTL and LTR, light and dark, phone and desktop: the tab, a retired
  and a not-filterable amenity, the sheet adding and editing with the icon grid, a field error, a row
  failure, loading, error, empty) go to `C:\Users\basel\Downloads\s2a3-shots`, never committed.
- **Review:** an independent review, after you report.
- After CI is green on the pushed head, stop and report: the head, the commits, the counts per lane,
  your tokens. Don't merge. Don't create an Issue.
