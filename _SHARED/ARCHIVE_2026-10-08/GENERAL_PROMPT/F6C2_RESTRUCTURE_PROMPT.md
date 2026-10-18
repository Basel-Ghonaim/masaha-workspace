# F-6c2 — rebase and restructure PR #39 (`feat/dashboard-shell`)

**Folder:** `C:\Users\basel\masaha-b` (worker B's worktree) · **branch:** `feat/dashboard-shell` · **PR #39**

## Hard limits (the owner's)

- **No subagents at all, and no workflows.**
- **Stay under 200,000 tokens for the whole session.** Read only what a step needs:
  - targeted `git diff` / `git show` / `grep`;
  - no full reads of the docs set;
  - pipe long test output through `tail` and read only the summary and any failure.
- **Run checks one at a time,** never in parallel (memory).
- **No production code exists only for a test:** no parameter, option or callback that only tests pass or that nothing uses.
- **Behaviour must not change.** This is a rebase plus a pure restructure.

## Step 1 — Rebase on `main`

PR #38 (F-5b3c1) is merged (`25eaf8c`), and its migration is already applied to `masaha_b_dev`.

1. `git fetch origin`, then `git rebase origin/main`.
2. **Expected conflicts.** Resolve them keeping both sides' intent:
   - **`features/users`** (`useAccount`, its test, `index.ts`): #38 extracted `useSignOutAction` out of `useAccount` and added `SignOutButton` and the forced-change form. Rebuild this PR's "Dashboard" item and the compact menu on that new shape. Tests move with the code they prove.
   - **`shared/routing/index.ts`:** #38 unexported `signInPath` and `changePasswordPath` (no outside consumer). Keep this PR's exports. Re-export one of #38's only if code outside `shared/routing` uses it, and say so in the PR.
   - **`architecture.md`, `RootLayout`, `router.tsx`:** keep both sides. #38's password-change gate and its `/change-password` route stay.
3. `npm exec -w @masaha/api -- prisma generate` (the schema changed).

## Step 2 — Run the tests (the baseline)

Run each lane once, one at a time:
- lint, typecheck, `check:classes`;
- `test:unit`, `test:component`, `test:api`;
- `build`, then `check:build`.

**Record the counts:** they are the "before" for step 3. Fix only what the rebase broke.

## Step 3 — Structure: one responsibility per file (the main task)

**The owner's rule, starting now:** every file has one responsibility, and the folders split the code logically.

- **One component per file, internal ones included,** named after the component.
  - A file such as `features/space-links/components/SpaceSwitcher.tsx` that defines `SpaceName`, `SpaceHead` and `SpaceSwitcher` becomes three files.
  - A component used only inside its feature or module stays internal: it is not exported from `index.ts`.
- **One hook per file.** Logic a component carries (deciding, mapping, formatting) moves into a hook or a `services/` function, so the component only renders (H6).
- **Folders by role** (architecture.md §1 and §3): `repository/`, `hooks/`, `components/`, `services/`, `types/` in a feature, and role folders in a module or page group (for example `pages/dashboard/shell/`). A pure helper never sits in `components/`.
- **Names say what a file holds.** A file named for one thing holds only that thing.

**Apply it to every file this PR adds or changes** under:
- `apps/web/src/features/`;
- `apps/web/src/pages/` (`site` and `dashboard`);
- `apps/web/src/shared/routing/`;
- `apps/web/src/shared/preferences/`.

For example:
- `SpaceSwitcher.tsx`;
- `pages/site/shell/toggles.tsx` and `pages/dashboard/shell/toggles.tsx`;
- `pages/dashboard/shell/SpaceLayout.tsx` and `DashboardNavigation.tsx`.

Find the others with a quick scan for files that declare more than one component, hook or helper.

**Not in scope:**
- **The design-system layer** (`shared/design-system/**`). Its layout is owned by foundation §3: compound components such as `Sidebar` and the `iconSet` registry are deliberate there.
- **The showcase** (`pages/showcase/**`), a development tool.
- **Any file this PR doesn't touch.** The owner plans a later project-wide refactor; record any you notice in your report, but don't change them.

**Write the rule down,** short, in `docs/frontend/architecture.md`:
- **§3:** extend H3 to "one component, one hook, one responsibility per file, internal ones included", with a one-line why: a file's name tells what it holds, and a reader never hunts inside a file;
- **§1:** one line pointing to it, for modules and page groups.

## Step 4 — Prove nothing changed

- Run every lane again, one at a time. **The test counts equal step 2's, and every test passes.**
- **`git diff -M`** between the rebased head and the new head shows moves, splits and import paths only: no logic change. Name any line that is not a move or an import.
- **Each module's and feature's `index.ts` exports are unchanged**, apart from the rebase's resolutions.

## Step 5 — History and report

- **Restructure commits:** the restructure is a new unit of work, so it goes in **new commits**, one per area, for example:
  - `refactor(space-links): one component per file`;
  - `refactor(dashboard): one responsibility per file`;
  - `refactor(site): split the shell toggles`.

  Each subject is 50 characters or fewer, and each commit passes lint, typecheck and the web lanes on its own. The rule's doc lines go in the first one.
- **Push** with `--force-with-lease`, to this branch only.
- **Update the PR description:**
  - the rebase's resolutions;
  - the restructure and the rule;
  - the before/after counts;
  - the `git diff -M` proof.
- **Report only once CI is green on the new head.** No tool or AI attribution anywhere. Don't merge. Don't create an Issue.
- **In your report:**
  - the tokens used;
  - the files you restructured;
  - any file outside this PR that breaks the rule (listed, not changed).
