# Review — PR #43 (S2a-2: the admin's lookups screen, governorates and areas)

You are the **independent reviewer** of PR #43. Run from `C:\Users\basel\masaha` (the main folder).
You don't build, fix or merge.

## Budget (hard limits — the owner's)

- **At most 2 subagents. Never a third,** not even an empty one. No workflows.
- **The whole review stays under 600,000 tokens**, this conversation and both subagents together. Aim
  for about 200,000 per subagent.
- **Read the diff, not the repository.** Use `git diff 315aa52...2a98662 -- <paths>` and
  `git show 2a98662:<file>`, only for files the PR changes, plus the few named below.
- **Read the documents only in the sections named.**
- **Reports:** at most 700 words per subagent, and at most 900 for yours.

## Rules

- **Read-only.** No edits, commits, checkouts, switches, installs, npm or test runs, dev servers,
  database commands, or GitHub comments. Run `git fetch origin` first if `2a98662` is missing.
- **Pin everything to commit `2a98662`**, compared with its base `315aa52`. (PR #42 may merge first
  and this branch may then be rebased for a docs conflict in `architecture.md`; ignore that.) Prefix
  `git show` with `MSYS_NO_PATHCONV=1` if a path is mangled.
- **Report concrete problems only:** the file and line, the failing scenario, the severity
  (blocker / should-fix / nit) and the fix. **Verify each in the code before reporting it;** drop
  anything speculative.

## What the PR must be (the owner's decisions)

The admin's **Lookups** page at `/dashboard/admin/lookups`: governorates and their areas, added,
renamed, hidden, restored and ordered, over the API built in PR #41 (`GET /admin/governorates`;
`POST`/`PATCH` governorates and areas; `PUT …/order` with `{ ids }`, 204; hide and restore are
`isActive` in the `PATCH`; a duplicate Arabic name is 409 `not_unique` on `nameAr`; a stale order is
409). It is the **first real admin screen: its patterns will be copied by every admin screen after
it**, so judge them as patterns, not only as this page.

- **K1:** query keys start `['admin', 'lookups', …]` (added to architecture.md §7).
- **K2 + approved A1:** after a write, the governorates list is invalidated, and the mutation stays
  pending until the refetch answers.
- **K3:** no optimistic update; a row's switch and arrows are disabled while that row's request is
  pending (tracked per row via `useMutationState` and mutation keys); every arrow of a list is
  disabled while that list's order is pending; the edge rows' outward arrows are disabled.
- **K4:** a row action's failure shows inside its governorate's card (`useRefusalView` /
  `FormFailure`); the next action clears it; a 409 on an order refetches and says the order changed.
  No toasts.
- **K5:** real Arabic plurals: `shared/copy/plural.ts`, all six categories via `Intl.PluralRules`,
  with its test — the project's first counted line, to be reused everywhere.
- **K6 + approved A4:** no tabs yet; the page composes one self-contained `GovernoratesSection`
  (its own query, states, failures and add action), so the amenities tab can be added later without
  reshaping; the section owns its loading, error and empty states.
- **K7:** the English name is the primary line, the Arabic the secondary, in both languages.
  **Approved A3:** accessible names use the name in the interface's language.
- **K8:** the "Active" switch only when editing. **Approved A2(a):** a hidden card or row is dimmed
  by its text (`muted-foreground`) plus the "Hidden" badge, not by a surface tint.
- **The sheet:** opens at `side="end"`; focus on the first field; validation on submit, first invalid
  field focused; `not_unique` lands on `nameAr`; on success it closes and focus returns to its
  trigger.
- **Project rules:** no parameter, option or callback that only tests pass or nothing uses; tests
  stub the platform's seams (`fakeTransport`/`fakeAdapter`), never `vi.mock` of a module; pages pass
  no navigating callbacks; one responsibility per file, files grouped by operation; components only
  render, hooks prepare; no hardcoded user-facing text (both catalogues, same keys); no colours or
  CSS outside the design system; honest test titles; commit subjects ≤ 50 characters.

## The split

### Subagent 1 — the hooks, TanStack Query, security and bugs

**Its files:** the PR's changes under `apps/web/src/features/lookups/` in `repository/`, `hooks/`,
`services/`, `types/`; `apps/web/src/pages/dashboard/routes.tsx` and its test.

**It reads only:** `docs/frontend/architecture.md` §3 (*React Query in a feature*, *Where state
lives*, *Components present; hooks prepare*) and §7 (query keys, invalidation, retries, defaults,
optimistic updates).

**It checks:**
- **TanStack Query usage:** keys and their scope; invalidation awaited as A1 says, with no stale
  window; `useMutationState` filters truly per row and per list (two rows, two cards, a governorate
  and its own areas); no mutation retried; `gcTime` and cleanup; no state that outlives the page
  wrongly; no request fired twice under StrictMode; refetch on window focus does not reset a pending
  UI.
- **Bugs and races:** a toggle during an order and the reverse; two quick clicks on one arrow; an
  order computed from a stale list; the 409 path refetches and clears correctly; the "next action
  clears the failure" rule cannot hide a newer failure; a sheet submitted twice; the sheet closing
  before the refetch; an area added to a governorate that was just hidden; edge rows' arrows; an
  empty governorate; `moved()` at both ends.
- **Security:** the route keeps its visible `RequireRole roles={['ADMIN']}` guard; nothing assumes
  the UI is the authorization; no admin data reaches a non-admin path; `check:build`'s first-download
  rule still holds (the route file holds only paths, guards and lazy imports); no user text injected
  as HTML.
- **UX from the hooks' side:** every failure maps to a line (network, timeout, 429 countdown, 422,
  409, 5xx); the busy and disabled states are what the user would expect.

### Subagent 2 — the components, UX, accessibility, plurals, tests and documents

**Its files:** the PR's changes under `features/lookups/components/`, `features/lookups/index.ts`,
`pages/dashboard/admin/`, `shared/copy/` (the `lookups` sections, `plural.ts` and its test, the
`index.ts` lines), every test file in the PR, `docs/` (architecture.md, localisation.md,
findings.md), the commits, and the PR body (`gh pr view 43 --json body`, read-only).

**It reads only:** `docs/frontend/localisation.md` (plurals, formatting);
`docs/frontend/design-system/foundation.md` §10 (accessibility) and the rows of the components used;
`docs/development/testing.md` §1–§3 and *A feature, layer by layer*.

**It checks:**
- **The plural mechanism:** correct for all six Arabic categories and for English; the samples
  tested; reusable as a pattern for every later counted line; not exported where it shouldn't be.
- **Accessibility:** accessible names (A3) and their language; the switch's and arrows' states
  announced; focus management in the sheet (open, error, close, return); disabled vs `aria-disabled`
  choices; the hidden state conveyed beyond colour; axe coverage.
- **RTL, phone and dark:** logical properties only; the arrows don't mirror; rows wrap on a phone as
  in frame 02; no physical classes; tokens only.
- **Components only render:** no logic, no `AppError`, no mutation in a component.
- **Tests:** one behaviour in one lane; each decision K1–K8 (and A1–A4) has a test that would fail
  with broken code; titles match assertions; no duplicated proofs; finding 28's lazy-page timeouts
  not hidden by weaker assertions.
- **Documents:** architecture.md §2, §3, §7 and the status line, localisation.md and finding 28's
  widening state the code truly; nothing claims more than is built.
- **The commits:** atomic, Conventional, ≤ 50 characters, each a complete unit.

## Your output

Write **one file**, `C:\Users\basel\.prompt\MASAHA_WORKER_B\REVIEW43_REPORT.md`:
1. **A verdict in one line.**
2. **The findings,** most severe first, deduplicated. Each gives the severity, the file and line, the
   scenario and the fix.
3. **"Verified OK":** a short list, grouped by the two subagents' areas.

State the total tokens used. Then stop. The owner's analyst verifies the findings and writes the
fixes list.
