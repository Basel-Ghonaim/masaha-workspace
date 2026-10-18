# F-10 — The amenity icons (finding 10, first part)

**Worker B** · folder `C:\Users\basel\masaha-b` · branch `feat/amenity-icons`

**Size cap:** use at most 4 subagents in total. Do not run any workflow.

## 1. How to work (mandatory)

1. Read `CLAUDE.md`, then `docs/development/workflow.md` (especially §9, Parallel work), then `docs/README.md`.
2. Then read:
   - `docs/frontend/design-system/foundation.md` §3 (architecture and enforcement) and §8 (direction and icon mirroring);
   - `docs/architecture/findings.md`, finding 10;
   - `docs/architecture/data-model.md`, the Amenity entity;
   - `apps/web/src/shared/design-system/icons/` (`Icon.tsx`, `iconSet.tsx`, `index.ts`, the component test);
   - `apps/web/src/pages/showcase/sections/icons/IconsSection.tsx`;
   - `apps/api/src/db/seed/lookups.ts`;
   - `packages/shared/src/index.ts`.
3. Work in **PLAN MODE**. Write nothing until the owner approves your plan.
4. Before you plan, check:
   - you are in `C:\Users\basel\masaha-b`;
   - the working tree is clean;
   - after `git fetch origin`, `HEAD` is detached at `origin/main`.

   If any check fails, stop and report. Do not fix it yourself.
5. Once the plan is approved, cut the branch with `git switch --no-track -c feat/amenity-icons origin/main`. The first push is `git push -u origin feat/amenity-icons`.

## 2. Context

The seed gives each of the eight amenities an icon key: `wifi`, `zap`, `sun`, `plug-zap`, `coffee`, `users`, `presentation` and `graduation-cap`. These are Lucide glyph names. Lucide may be imported only inside the design-system layer, and the layer's icon set has only two of these icons today (`SunIcon`, `UsersIcon`). So the web has nothing to show for the other six keys, and the admin's amenity form (build step 2) has no set to offer.

This item builds the first part of the fix: the missing icons, and one official list of the keys. It does **not** build the map from key to icon.

## 3. Decisions already made (do not reopen)

The owner approved these. Follow them as written.

- **Q1. Where the list of keys lives:** in `packages/shared`.
  - Why: the list is a contract between the client and the server. In step 2, the admin sends a key and the server validates it against this list.
  - The design-system layer does not import it: the layer imports nothing outside itself.
- **Q2. Where the key-to-icon map lives:** not in this item. It belongs to `features/lookups` and is built in step 2, together with its first consumer.
  - Why: no code is built without a consumer, and this item must not create a feature before the frontend feature shape is decided.
  - The layer never knows the amenity concept: it exports plain icons only.
- **Q3. Names and mirroring:**
  - each icon is named for its glyph, like the existing ones (`WifiIcon`, `ZapIcon`, `PlugZapIcon`, `CoffeeIcon`, `PresentationIcon`, `GraduationCapIcon`);
  - none of them mirrors in RTL: they are not directional.
- **Q4. Tests:** do **not** add a test script or a test setup to `packages/shared`. Worker A is adding one there now (F-5a fix S8), so `packages/shared/package.json` is worker A's file. The list is an `as const` tuple, and the typecheck on the seed guards it. The existing icon component test and the showcase cover the icons.
- **Q5. Finding 10's status:** it stays **Open**. Add a dated progress line saying the icons and the key list are built, and that the map and the admin's form remain for step 2.

## 4. Contract

**Scope**
- **The icons.** The six missing Lucide icons are declared in `iconSet.tsx` through the `Icon` wrapper, with no mirroring, and exported from the icons barrel and the layer's public entry, where the existing icons are.
- **The showcase.** The icons section shows the six new icons with the non-mirrored icons.
- **The key list.** `packages/shared` exports the eight keys as an `as const` tuple, with its type (for example `AMENITY_ICON_KEYS` and `AmenityIconKey`, in a new file such as `amenities.ts`). Propose the final names in the plan.
  - No Zod schema yet. The endpoint that validates the key adds it in step 2.
- **The seed.** `lookups.ts` types each amenity's `icon` with that type, so a key outside the list fails `typecheck`. Its finding-10 comment is updated to match.
- **The documents:**
  - `data-model.md`: the Amenity line points to the shared list as the owner of the valid keys. One sentence; link, don't copy.
  - `findings.md`: finding 10's progress line (Q5).

**Acceptance criteria**
- [ ] The eight seeded keys each have a layer icon: six new, two existing.
- [ ] None of the new icons mirrors in RTL.
- [ ] `lucide-react` is still imported only inside the design-system layer, and lint proves it.
- [ ] A seed amenity with an icon key outside the list fails `typecheck`. Prove this once locally, then revert it; do not commit the probe.
- [ ] The showcase shows the new icons in RTL and LTR, light and dark.
- [ ] Finding 10 stays Open, with its progress line.

**Out of scope**
- The key-to-icon map, and any `features/` folder.
- Any endpoint, any Zod schema for the key, and the admin's amenity form.
- Any change to `schema.prisma` or any migration.
- A test script or a test configuration in `packages/shared`.
- Any new dependency.
- Any other icon, and any refactor of the icon wrapper.

## 5. Parallel work

**Worker A** is working in `C:\Users\basel\masaha` on PR #25 (`feat/auth-api`, the F-5a review fixes).

- **Worker A's files. Do not touch them:**
  - `apps/api/src/modules/**`;
  - `apps/api/src/shared/**`;
  - `apps/api/src/config/**` and `apps/api/src/app.ts`;
  - `apps/api/src/db/` except `seed/lookups.ts`;
  - `packages/shared/package.json` and `packages/shared/src/` files other than your new one and `index.ts`;
  - `docs/backend/**`, `docs/api/**`, ADRs;
  - the copy catalogues.
- **Shared files.** Declare them in your plan, and edit each one minimally, in your own section only:
  - `packages/shared/src/index.ts`: your single export line;
  - `docs/architecture/findings.md`: finding 10's section only (worker A edits findings 16–19 and adds new ones);
  - `docs/architecture/data-model.md`: the Amenity line only.
- **Rebasing:** before you open the PR, fetch and rebase on the latest `origin/main`. If PR #25 merges first, rebase again and resolve any conflict by keeping both sides.
- **The lockfile:** you add no dependency, so `package-lock.json` must not change. If a rebase ever conflicts on it, take main's version, run `npm install`, and never edit it by hand.
- **Databases:** only `masaha_b_dev` and `masaha_b_test`, through this folder's `apps/api/.env`. Never touch worker A's databases.

## 6. Commits

Atomic, in Conventional Commits format, staged by path (never `git add -A` or `git add .`), with `git status` before each commit. Expected:
1. `feat(design-system): add the amenity icons`: the icons, the barrel exports and the showcase.
2. `feat(lookups): add the amenity icon keys`: the shared list, the seed typing, `data-model.md` and finding 10's progress line.

Each commit builds and passes lint, typecheck and the tests on its own.

## 7. Evidence

- **Run:** `lint`, `typecheck`, `check:classes`, `build`, then `check:build`, `test:unit`, `test:component`, and `test:api` against `masaha_b_test`, because the seed was touched.
- **In the PR,** state what you ran and what you did not run.
- **Screenshots** of the showcase's icons section: RTL and LTR, light and dark, phone and desktop. Save them to `C:\Users\basel\Downloads\f10-shots`. Never commit them.

## 8. Pull request

- **Title:** the main commit's title.
- **Labels:** `feat`, `area:design-system`, `area:web`, `area:api`, `area:docs`.
- `gh pr create --assignee @me`.
- **Description:** the workflow §3 template: Summary; Scope / Acceptance criteria / Out of scope; Change type; Evidence; Screenshots (list the files in `f10-shots`, don't upload them); the Definition of Done checklist. Name decisions Q1–Q5 in the Summary.
- **No tool or AI attribution** anywhere: commits, PR, documents. No `Co-Authored-By` trailer, no "generated with" footer.
- **Do not merge. Do not create an Issue.**
- When the PR is open, stop and report briefly: the PR link, the commits, the lanes run, and anything you left out.

## 9. Stop rules

- **An architectural question beyond Q1–Q5** (for example, if the layer's public entry or the lint rules need a change): stop and propose; do not decide.
- **Anything unrelated you notice:** record it as a finding, or list it in your report. Do not fix it.
- **Worker A's files:** if you think you need to touch one, stop and ask.
