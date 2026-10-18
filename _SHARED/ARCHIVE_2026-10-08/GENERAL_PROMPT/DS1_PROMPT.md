Work Item DS-1 — Design-system categories and showcase navigation · branch `refactor/design-system-categories`

## How to work (mandatory)

1. Read CLAUDE.md, then docs/development/workflow.md, then docs/README.md, then docs/frontend/design-system/foundation.md (especially §3, §11 and §12) and `.design-sync/NOTES.md`. Follow the project's workflow exactly: task classes, Git lifecycle, scope control, Definition of Done, decision authority, stop rules.
2. You run in a git worktree the owner has already created: `C:\Users\basel\masaha-ds`, on the branch `refactor/design-system-categories`, cut from `origin/main`, with `npm ci` already run. Before planning, verify and report:
   - `git rev-parse --show-toplevel` is that folder, and `git branch --show-current` is that branch;
   - the tree is clean;
   - after `git fetch`, the branch contains the latest `origin/main`.

   If any check fails, stop and tell the owner. Do NOT create another worktree or branch, and never work in the main folder `C:\Users\basel\masaha`.
3. Start in PLAN MODE. No edit and no commit before the owner approves a written plan. The plan lists:
   - the final category names, the classification rule, and the full mapping (every component → one category);
   - the showcase's routes, navigation and registry;
   - every file to create, move or change;
   - the commits (atomic units per workflow §3);
   - how you verify;
   - any question or divergence you found.

   Wait for approval.
4. After approval, work ONLY in that worktree. No database is needed. Run every check from an uppercase `C:\` path (finding 9). The branch has no upstream yet: the first push is `git push -u origin refactor/design-system-categories`.
5. Implement only the approved plan. Anything outside it: stop and ask. Unrelated problems are recorded as findings, not fixed.
6. Finish at "Ready for review": self-review against the Definition of Done, push, open the PR. Never merge.

## Context

- **The design-system layer** (`apps/web/src/shared/design-system/`) holds 37 component folders in one flat, alphabetical list. Nothing says what role a component plays.
- **The development-only showcase** (`/__showcase`) renders every section on ONE long page, in the order the components were built (the design-system Work Items), not by role. There is no navigation and no link to a single component. The heavy sections (DataTable, Calendar) re-render with every change of theme, language or width.
- **The Claude Design sync:** `.design-sync/NOTES.md` says every component lands in the group `general` "because the layer has no category folders".

## Approved direction (the owner's decisions)

### 1. Components are grouped into category folders inside the layer

The owner approved the idea; the names are provisional. Starting point:

| Category | Role | Components |
|---|---|---|
| `controls` | triggers an action | Button · ToggleGroup · LanguageToggle · ThemeToggle |
| `fields` | enters a value | Field · Input · Textarea · Select · Combobox · Checkbox · RadioGroup · Switch · DatePicker · Calendar |
| `display` | shows content | Avatar · Badge · Card · StatCard · Separator |
| `data` | shows tabular data | Table · DataTable |
| `feedback` | tells the system's state | Alert · Toast · Skeleton · Spinner · EmptyState |
| `overlays` | floats above the page | Dialog · AlertDialog · Sheet · Popover · Tooltip · DropdownMenu |
| `navigation` | moves between places | Breadcrumb · Tabs · Pagination · Sidebar |

`DirectionProvider` is not a visual component. The analyst suggests moving it next to `lib/`; the plan decides.

**Your planning task here:**
- Write the classification rule: a category is the component's primary role for the user, and each component has exactly one.
- Check every component against it. Propose the final names, and say whether categories are missing (for example layout, providers) or redundant.
- Also take into account the components the plans and findings say are coming, such as the removable filter tag (finding 8).
- Present the final table for approval.

### 2. The showcase has three views, with one shared navigation

1. **A page per component**, with its own URL, for checking one component in isolation.
2. **A page with all components**, in today's order, so the current one-page view stays available.
3. **A page per category**: all of `controls`, all of `display`, and so on.

**Also approved:**
- A sidebar grouped by category, shared by the three views.
- The toolbar (theme, language, width) stays global, and its state stays in the URL across views.
- One registry (category, name, section, sample key) drives the navigation, the routes and the three views. No component is listed twice.
- The `sections/` folder mirrors the layer's categories.

The plan decides the URL scheme, the registry's shape, and whether the showcase uses the layer's own Sidebar for its navigation.

## Invariants (this is a pure refactor)

- **The public surface does not change.** `@shared/design-system` exports exactly the same names before and after: prove it with a diff of the export list. No consumer outside the layer changes.
- **No component changes visually or in behaviour.** Every existing test passes, changed only by its path.
- **The showcase stays development-only:**
  - its routes stay under `/__showcase`;
  - `check:build` passes;
  - fixture strings are reused, not rewritten.
- **The layer's rules still hold:** the ESLint boundaries, the import restrictions, `check:classes` and the closure (the layer imports nothing outside itself).
- **History is kept:** use `git mv` for the moves.

## Also updated

- `docs/frontend/design-system/foundation.md`:
  - §3: the category structure and the classification rule, and the showcase's three views;
  - §11: the step for adapting a copied shadcn component becomes "move it into its category folder";
  - §12: grouped by category, if that reads better (the plan decides).
- `apps/web/components.json`: check whether the shadcn CLI's aliases need a change.
- `.design-sync/`:
  - the `Toaster` source path in `config.json`;
  - the note on groups in `NOTES.md`.

  Running a sync is out of scope.

This is not an ADR: the change is inside one layer and easy to reverse. If the plan finds a reason it should be one, say so.

## Parallel work (read before planning)

Another conversation runs at the same time: **A-3, recording the cross-cutting decisions** (documentation only).
- It works in the MAIN folder `C:\Users\basel\masaha`, on the branch `docs/cross-cutting`. Never edit, switch branches or run anything in that folder; work only in your worktree.
- **A-3's files:** the ADRs, `docs/backend/**`, `docs/api/**`, `docs/frontend/architecture.md`, `docs/plans/**`, `docs/README.md`. DS-1 never touches them.
- **DS-1's files:** `apps/web/src/shared/design-system/**`, `apps/web/src/pages/showcase/**`, `apps/web/components.json`, `.design-sync/**`, `docs/frontend/design-system/foundation.md`. A-3 is told the same list.
- **Shared risk:** if DS-1 truly needs a file from A-3's list (for example a line in `docs/README.md`), the plan says so first. Keep any such edit minimal.
- **Before opening the PR:** fetch and rebase on the latest `main`. Merge order doesn't matter: whoever merges second rebases, and resolves any conflict by keeping both sides.
- No dependency changes: `package-lock.json` stays untouched.

## Out of scope

- New components, and any change to a component's look, API or behaviour.
- Running a Claude Design sync.
- New dependencies.
- Any file on A-3's list.

## Verification

- `npm run lint`, `typecheck`, `check:classes`, `test:unit`, `test:component`, `build` and `check:build` pass.
- The diff of the public export list is empty.
- **In a browser:** each of the three views, in light and dark, Arabic and English, at 360 and 1280. Deep links to a component and to a category open directly.
- **Screenshots** go to `C:\Users\basel\Downloads\ds1-shots` as a curated set:
  - the three views in light-ar-360 and dark-en-1280;
  - the sidebar open on phone.

  Never commit images.

## PR

Per workflow §3:
- labels `refactor` + `area:design-system` + `area:web`, assigned to me (`--assignee @me`);
- the description template, with the Screenshots section listing the files in `ds1-shots`;
- no AI attribution anywhere.

Don't merge.
