Work Item F-6a — Preferences: language and theme · branch `feat/preferences`

## How to work (mandatory)

1. Read CLAUDE.md, then docs/development/workflow.md (including §9 Parallel work), then docs/README.md. Follow the project's workflow exactly.
2. You are **worker B**. You work in the worktree `C:\Users\basel\masaha-b`. Never work in the main folder `C:\Users\basel\masaha`.
   - Before planning, check:
     - `git rev-parse --show-toplevel` is that folder;
     - the tree is clean;
     - HEAD is DETACHED at the latest `origin/main` after `git fetch`.

     If HEAD is still on an old branch, stop and tell the owner; the owner cleans it.
3. Start in PLAN MODE. No edit, no branch, no install and no commit before the owner approves a written plan. The plan holds:
   - the state-library comparison (below), with your recommendation;
   - the store's API and behaviour;
   - every file to create or change;
   - the commits;
   - how you verify;
   - every question.

   Wait for approval.
4. After approval: `git fetch origin`, then `git switch --no-track -c feat/preferences origin/main`. The first push is `git push -u origin feat/preferences`.
5. Finish at "Ready for review": self-review, push, open the PR. Never merge.

## Read first

- **docs/frontend/localisation.md:** the language resolution, the pre-paint script, the storage keys `masaha.language` and `masaha.theme` as **plain strings**, the language source that the preferences store replaces, and the agreement test with the pre-paint script.
- **docs/frontend/architecture.md:** §1 (`app/` owns the providers) and §4 (`shared/preferences`).
- **docs/architecture/decisions/0004-frontend-data-and-state.md:** Zustand for `session` and `preferences`.
- **docs/frontend/design-system/foundation.md:** §6 themes, each a complete token set, with a parity test.
- **The code:** `apps/web/index.html` (the pre-paint script), `apps/web/src/app/`, `apps/web/src/shared/localisation/`, `apps/web/src/app/prePaint.unit.test.ts`.
- **The design:** `docs/design/SCREENS.md` row 9 (the account settings theme options); the top-bar toggles in the shells.

## The owner's decisions (binding)

1. **Theme has THREE choices:** light, dark, and "as the device" (system).
   - "As the device" = **no stored key**: the key is removed, and the app follows `prefers-color-scheme`, **live**, while it is the choice. This keeps the pre-paint script's behaviour, since it already follows the device when no key is stored.
   - The store exposes **the choice** (light | dark | system) and **the resolved theme** actually shown (light | dark).
   - **Two UI forms** will use it. Both are built in F-6, not here, so the API must serve them:
     - a select in the account settings with all three choices;
     - a toggle in the top bar that switches between light and dark: pressing it sets the explicit opposite of the resolved theme. "As the device" is chosen from the settings.
2. **Cross-tab sync:** a change in one tab updates every open tab, through the browser's `storage` event.
3. **State library: compare first, the owner decides.** ADR 0004 chose Zustand. Before building, compare **Zustand** with **React Context** (with `useSyncExternalStore` where it fits) for Masaha's client state, and recommend one.
   - **The decision applies to BOTH stores:** `preferences` now, and `session` in F-5b. Never two mechanisms.
   - The criteria:
     - use from OUTSIDE React. F-5b's Axios interceptor must read and refresh the session token outside any component, and the localisation mechanism already has a non-component accessor (`currentCopy()`);
     - re-render behaviour;
     - provider nesting (Zustand needs no provider);
     - testability;
     - dependency cost and bundle size;
     - consistency with ADR 0004.
   - **If the owner chooses Context:** add a `Revised:` line to ADR 0004 in this PR.
   - **If Zustand:** it is the one new dependency (approved by ADR 0004).
4. **Extensible by registries, not by a framework.**
   - Languages and themes are DERIVED from their owners, never written by hand in the store:
     - the languages and their types from the copy catalogues' registry (`CATALOGUES`) and `directionOf`;
     - the theme names from the design system. If the layer exports no theme list today, propose the smallest export, checked against the token files by the existing parity test.
   - Adding a language or a theme later must not touch the preferences code.
   - **No generic "preferences engine",** no runtime-loaded catalogues, and no plugin system: that is generalising before a second instance (engineering-principles §1).
   - What can't be derived stays manual and test-guarded: the pre-paint script, which runs before the bundle, and the database language enum. Say so in the plan.
5. **One providers file.** Move the provider composition out of `App.tsx` into one component in `app/` (for example `app/providers.tsx` › `AppProviders`). Today it holds `DirectionProvider` around the router. F-5b will add TanStack Query's provider there, and later ones follow. `App.tsx` stays minimal.
6. **`docs/plans/foundation.md` is worker A's file: don't touch it.** Say in the PR that F-6a took the preferences part of F-6's contract; F-6's own plan updates its entry.

## Scope

- **`shared/preferences`:**
  - the store (with the chosen library): language, theme choice, resolved theme;
  - setters for language and theme;
  - persistence to `masaha.language` and `masaha.theme` as plain strings, exactly as localisation.md and the pre-paint script expect. A library's own persist format (one JSON object under one key) is NOT acceptable: the pre-paint script couldn't read it, and the page would paint the wrong theme first;
  - on every change, it writes `lang`, `dir` and `data-theme` on `<html>`;
  - the live device listener while the choice is "system";
  - cross-tab sync;
  - a public `index.ts`.
- **Localisation:** the preferences store replaces `documentLanguage` as the language source at bootstrap (localisation.md › The language source). Remove `documentLanguage` if nothing else uses it.
- **The pre-paint agreement test** now also holds the storage keys and the values the app writes equal to the script's (localisation.md says so).
- **`app/`:** the providers file (decision 5); `bootstrap.ts` wires the store.
- **Docs, in the same PR:**
  - localisation.md › Mechanism: the language source, and the keys the app writes;
  - architecture.md §4 only: `shared/preferences` is built (say what), plus the providers file in §1 if you mention it;
  - ADR 0004, only if Context is chosen.

## Out of scope

- The theme and language UI (the settings select, the top-bar toggles): F-6.
- The account's language after sign-in ("the account's language wins"): it needs the session, so F-5b or F-6.
- Any `/me` endpoint.
- `foundation.md`, all of `apps/api`, and `packages/shared`.

## Parallel work (read before planning)

**Worker A** runs at the same time in the MAIN folder, on F-5a's review fixes (`feat/auth-api`). Never touch that folder.

**Its files:**
- `apps/api/**` and `packages/shared/**`;
- `docs/backend/**`, `docs/api/**`, `docs/architecture/**` (ADR 0003, data-model, findings);
- `docs/plans/**`;
- `docs/development/testing.md` (possibly);
- ONE line in `docs/frontend/architecture.md` (the guards are F-5b's, in §2).

**F-6a's files:**
- `apps/web/src/shared/preferences/**`, `apps/web/src/app/**`, `apps/web/src/shared/localisation/**`;
- the design-system export, if one is needed;
- `docs/frontend/localisation.md`, `docs/frontend/architecture.md` (§1 and §4 only);
- ADR 0004 (only if Context is chosen);
- `apps/web/package.json` (only if Zustand is chosen).

**Shared files:**
- `docs/frontend/architecture.md`: keep to your sections.
- `package-lock.json`: F-5a also changed it. If you add a dependency, whoever merges second takes `main`'s lockfile and runs `npm install`, never editing it by hand (workflow §9).

**Before opening the PR:** fetch and rebase on the latest `main`. Whoever merges second rebases and keeps both sides.

## Verification and PR

- **Unit tests:**
  - the store's logic: the three choices, the resolved theme, the toggle's behaviour, the key removed for "system";
  - the persistence format (plain strings at the exact keys);
  - the live device change;
  - cross-tab sync, through a simulated `storage` event;
  - the derivation from the registries.
- **Component tests:** changing the language re-renders the copy and flips `dir`; changing the theme sets `data-theme`.
- **The pre-paint agreement test** holds the keys and values.
- `lint`, `typecheck`, `check:classes`, `test:unit`, `test:component`, `build` and `check:build` pass. No UI is added, so no screenshots.

The PR follows workflow §3:
- labels `feat` + `area:web`, assigned to me (`--assignee @me`);
- the description template, including the library comparison and the owner's choice;
- no AI attribution.

Don't merge.
