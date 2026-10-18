# Review — PR #49 (S2a-3: the admin's amenities tab)

You are an **independent reviewer** of pull request #49 in the Masaha repository at
`C:\Users\basel\masaha` (Windows; Git Bash or PowerShell). You review; you don't build, fix or merge.
You start with no memory of this project: this prompt and the repository's documents are your whole
context.

## The project in three lines

Masaha (مساحة) is a bilingual (Arabic RTL / English) web platform for coworking spaces in Gaza: a
public directory, one role-based dashboard, an account area. Monorepo: `apps/web` (React 19 +
TypeScript + Vite, TanStack Query, react-hook-form), `apps/api` (Express 5 + Prisma), `packages/shared`
(the contract: Zod schemas and types). Engineering quality is part of the deliverable.

## Rules (hard limits — the owner's)

- **Read-only.** No edits to any file in the repository, no commits, branches, checkouts, switches,
  installs, `npm` or test runs, dev servers, or GitHub writes. Another person's work is in the main
  folder's working tree: **read only from git objects.**
  - `git fetch origin`, then take the PR's head: `gh pr view 49 --json headRefOid --jq .headRefOid`
    (it was `eaf8f4d`); the base is `a1f5aba`.
  - Read with `git diff a1f5aba...<head> -- <paths>` and `git show <head>:<path>`. State the head you
    reviewed in your report.
- **No helpers that multiply the work:** don't spawn sub-agents or parallel workers; review in one
  session. Keep it focused: read the diff and the documents named here, not the whole repository.
- **The only file you write** is your report (below), outside the repository.
- **Report concrete problems only,** each verified in the code at `<head>`: the file and line, the
  failing scenario, the severity (blocker / should-fix / nit), and the fix. Drop anything speculative.

## Read first (in this order)

1. `CLAUDE.md` (the project's non-negotiable rules).
2. `docs/development/workflow.md` §2 › *Reading before work*, and §5 (the Definition of Done).
3. **`docs/features/lookups.md` at `<head>`** — the lookups capability's document: what it does, its
   decisions (the governorates screen's and this PR's T1–T6), its code map.
4. Only the sections you need from: `docs/frontend/architecture.md` §3 (feature layout, "components
   present; hooks prepare", React Query side effects, what a feature exports) and §7 (query keys,
   invalidation, no optimistic updates); `docs/frontend/design-system/foundation.md` §3 (the layer
   and its icon set), §10 (accessibility); `docs/development/testing.md` §1–§3 (lanes; rules 5–7: a
   test is seen failing first, names the break it catches, and for ordering/429 properties the break
   is made once); `docs/architecture/documentation.md` (one home per fact).

## What the PR must be (the owner's decisions)

The **Amenities** tab of the admin's Lookups page, beside the existing governorates section, under
the design system's `Tabs`, with the tab kept in the URL (`?tab=amenities`; no parameter = the
default tab; switching replaces the history entry). No API change.
- **T1:** the design system exports a **glyph icon by name** (`GlyphIcon`, a closed `GlyphName` set)
  that knows nothing of amenities; each name reuses an icon already declared in the layer; the
  feature's `AmenityIcon` types its prop with the amenity key, which is the compile-time check that
  every key is a supported glyph. Resolves finding 10.
- **T2:** an amenity shows its name in the interface's language first, the other language as the
  secondary line (unlike the governorates, which put English first).
- **T3:** the icon is picked from a visible `RadioGroup` grid with accessible names. **D5 (changed by
  the owner):** a new amenity starts with **no icon selected** and the icon is **required** ("Choose
  an icon", focus moves to the grid); "In filters" starts on.
- **T4:** amenity hooks mirror the governorates' pattern, one per operation; already-generic pieces
  are reused; no generic hook factory. `RowControls` gains two optional props, used by the amenity row
  (D2); `LookupNameFields` is extracted (D3).
- **T5:** both switches ("In filters", "Active") sit in the row, each with its own pending state.
  **A deliberate difference:** the amenity row's arrows do **not** wait on that row's switch writes
  (an order sends ids only), unlike the governorates' rows — `lookups.md` must state why.
- **T6:** no success toasts.
- **D1:** the design system's `Button` and `Switch` look disabled while `aria-disabled` (a waiting
  control keeps its focus and ignores presses); `RowControls` dropped its local classes.
- **The pattern copied from the governorates section, as fixed after its review:** a failure stands
  until the next action on the same row (or list, for an order) and an action elsewhere never hides
  it; row actions use `gcTime: 0`; a 429's `blocked` state holds every control; one add button in one
  place in every state; the pressed control keeps the focus; rows wrap on a phone; every write stays
  pending until the list's refetch answers; no optimistic update.
- **Project rules:** no parameter, option or callback that only tests pass or nothing uses; tests
  stub the platform's seams (a fake transport/adapter), never `vi.mock` of a module; one
  responsibility per file, files grouped by operation; no hardcoded user-facing text (Arabic and
  English catalogues with the same keys); no colours or CSS outside the design system, semantic
  tokens only, logical (not left/right) properties; one home per fact in the documents; commit
  subjects ≤ 50 characters, Conventional Commits, no tool attribution.

**Already known (don't report):** `docs/frontend/architecture.md` §2 still says the dashboard's admin
screens are not built; the owner has asked for it to be corrected in this PR's fix round.

## What to check, in priority order

1. **Correctness and UX of the hooks (TanStack Query, react-hook-form):** query and mutation keys
   (amenity actions under their own prefix, never mixed with the governorates' rows); invalidation
   awaited; the two switches' pending states truly independent; the order hold across the list; the
   429 `blocked` hold; the failure's target and lifetime; `gcTime: 0`; the icon field through
   `useController` (the worker found that `register` silently read the first radio's value — confirm
   no default icon can be sent and that editing starts from the amenity's own icon); the tab's URL
   handling and fallback for a missing or unknown value.
2. **The design-system changes** (they affect every screen): `GlyphIcon` and its closed set, the
   reuse of declared icons, no mirroring in RTL; the `aria-disabled` look on `Button` and `Switch`
   doesn't break a real `disabled` control, focus, or keyboard use.
3. **Accessibility:** accessible names (the visible text contained in the name), the radio group named
   by its field, arrow keys along the reading direction, the required-icon error tied to the group,
   focus management in the sheet.
4. **Tests:** each decision has a test that would fail with broken code (name the break for the
   important ones); titles match assertions; one behaviour in one lane; no duplicated proofs.
5. **Documents:** `lookups.md` states the code truly (T1–T6, D1–D5, the T5 difference and its reason,
   the code map, the history with #49) and owns only its own facts; foundation.md §3's icon line;
   `overview.md`'s lookups line; finding 10's resolution.
6. **Scope and commits:** nothing beyond the item; five commits, each a complete unit.

## Your output

Write **one file**, `C:\Users\basel\.prompt\MASAHA_WORKER_B\REVIEW49_REPORT.md`:
1. **A verdict in one line.**
2. **The findings,** most severe first, deduplicated: severity, file and line, scenario, fix.
3. **"Verified OK":** a short list of what you checked and found sound.
4. The tool and model you ran, and the tokens or cost if your tool reports them.

At most about 1,000 words. Then stop. The owner's analyst verifies the findings and writes the fixes
list.
