# OWNER_SPACE_PROFILE — plan-only prompt

You are a planning worker for Masaha. This is **Phase 1 only** for a redesign of the
space profile used by the space owner. Do not implement anything in this phase.

## 0. Hard limits

- Write exactly one file: `C:\dev\masaha\workspace\TASKS\OWNER_SPACE_PROFILE\2_PLAN.md`.
- Do not create a branch, switch branches, edit repository files, commit, push, open a PR,
  install dependencies, run tests, run a build, start a server, or change a database.
- Do not create a temporary copy, scratch worktree, stash, or trial implementation.
- Read-only commands are limited to repository inspection (`git fetch`, `git show`, `git log`,
  `git diff`, `git ls-tree`, `git grep`) and reading the files listed below.
- Do not print, copy, or write secrets.
- Stop immediately after saving `2_PLAN.md` and report its path.

## 1. Task context

The current owner space profile opens as a large edit-oriented page. The owner approved a
more professional shared structure:

- The page opens in **View** mode.
- Every section is a card showing the information as a visitor sees it.
- Every card has its own **Edit** action.
- Editing opens one section-specific **Sheet**; on mobile it takes the full screen.
- The page remains visible behind the Sheet.
- Each section saves independently.
- `Save` and `Cancel` stay in the Sheet, not on the page.
- If the user tries to close a Sheet with unsaved changes, show the existing confirmation pattern.
- On success, close the Sheet and use the existing success feedback pattern.
- On failure, keep the Sheet open, preserve entered values, and use the existing error pattern.
- On desktop, show a sticky section index; on mobile, use a compact section menu.
- A single status line summarizes how many sections need confirmation.
- A stale section card shows its last-update age and a `Still correct` action that confirms it
  without opening the editor.
- The section order is:
  1. Basics & Location
  2. Photos
  3. Hours
  4. Prices
  5. Amenities
  6. Contact
- The page includes a `View public page` action.

## 2. Settled section content

### Basics & Location

View shows the space name, short description, area and address, verification status, and a
small map. The Sheet edits the name, description, area, address, and location with a larger map.

### Photos

View shows a gallery with a clear primary image. The editor supports adding and deleting images
and reordering them by **drag-and-drop only**, never by up/down buttons. Reordering uses
auto-save. Use the existing photo upload/delete/reorder contracts and feedback patterns.

### Hours

View shows a compact summary such as `Saturday–Thursday 08:00–18:00 · Friday closed`.
The common case must be simple: the same opening and closing time for a group of days, with Friday
closed by default when applicable. The editor must remain flexible:

- the owner can add Friday easily;
- the owner can select arbitrary day groups (for example Saturday–Wednesday and Thursday–Friday);
- each group can have its own opening and closing time;
- the owner can switch to custom hours for individual days;
- each day has one continuous opening interval only;
- no break intervals or exceptional closures belong here; exceptional closures use Announcements.

Do not recreate the previous crowded, repeated time-input layout.

### Prices

View and edit use one clear table rather than repeated form rows. Rows are the periods
`hour`, `day`, `week`, and `month`; columns represent the supported categories such as
`everyone` and `students`. Empty or unavailable prices must remain representable according to
the existing contract.

### Amenities

View shows only amenities that are actually enabled, with their existing icons and labels.
The Sheet provides a clear selection list, reusing the existing catalogue and selection pattern.

### Contact

View shows only enabled contact methods, each with a clear icon and label. The Sheet can add,
edit, and remove contact methods and shows the existing link/number preview pattern before save.

## 3. Scope boundary

- This Phase 1 plan must focus on the **Owner** experience.
- The same structural pattern is intended to be reusable by Admin later, but Admin-specific
  contents, permissions, and behavior are explicitly deferred and must not be designed or built
  in this Work Item unless the plan identifies an unavoidable shared contract.
- Reuse existing loading, error, success, confirmation, authorization, localization, design-system,
  Sheet, form, map, photo, and drag-and-drop patterns. Do not redesign those patterns.
- Do not change product scope or add booking, payment, reviews, QR check-in, or other Not-in-v1 work.

## 4. Read first, in this order

Read only what is needed, in this order:

1. `CLAUDE.md`
2. `docs/development/workflow.md`
3. `docs/README.md`
4. The capability documents for spaces, photos, prices/packages, hours/settings, amenities, and
   contact, following the documentation map's `Read it when` rules.
5. The relevant sections of `docs/frontend/architecture.md`,
   `docs/frontend/design-system/foundation.md`, and `docs/frontend/localisation.md`.
6. `docs/api/api-contract.md` for the existing managed space, photo, price, and contact routes.
7. The existing Owner space-profile implementation and its tests.
8. The closest existing Sheet-based section editors, the existing photo reorder flow, the map
   editor, and the existing status/confirmation/error/success patterns.
9. Relevant prototype screens and design decisions only where they clarify the current behavior.
10. Open findings that touch the space editor or any named section.

Start from the latest `origin/main` objects without checking anything out. If a capability
document or route does not exist, record that fact and identify the authoritative existing code
instead of inventing a contract.

## 5. Required `2_PLAN.md` contents

The plan must be standalone and detailed enough for a fresh worker and a reviewer. Include:

1. The base commit and the branch/worker intended for the later implementation phase.
2. The exact Owner routes, components, hooks, services, shared types, API endpoints, and catalogue
   keys that will be reused or changed.
3. The proposed component and state structure for View mode, cards, the section index, status
   summary, stale confirmation, and each Edit Sheet.
4. The exact behavior of the Hours grouping editor, including arbitrary day groups, custom per-day
   hours, Friday, one interval per day, validation bounds, and the compact View summary.
5. The exact table model and validation behavior for Prices.
6. The photo drag-and-drop, auto-save, upload, delete, failure, and ordering behavior.
7. Authorization boundaries: owner-only actions, server enforcement, and any existing role-dependent
   behavior that must remain unchanged.
8. Localization requirements and all new user-facing copy keys in Arabic and English.
9. Responsive behavior at 390, 768, and 1440, in RTL/LTR and light/dark themes.
10. Accessibility behavior: keyboard focus, Sheet focus management, drag-and-drop alternative if
    an existing accessible pattern is required, labels, errors, and announcements.
11. Tests for every new behavior, with the test lane, title, and the deliberate break each test
    catches. Include browser screenshots and real-request verification where required by the
    repository workflow.
12. Commits with Conventional Commit subjects of at most 50 characters, each complete and working.
13. Local verification commands, the order, prerequisites, and what must be recorded.
14. A `Strong(er) decisions` section for any safer or more precise interpretation of the settled
    decisions, with reason, cost, and recommendation; do not apply alternatives.
15. A `Decisions needed` section. If none are needed, write `none`; do not silently decide an
    architectural or scope change.
16. A `Proposed alternatives` section for improvements that are outside the approved direction.
17. A clear `Out of scope` section, explicitly including Admin-specific behavior and the deferred
    Admin decision.

## 6. Stop rule

Write `2_PLAN.md`, do not implement or verify code, and stop. Return only:

`PLAN READY: C:\dev\masaha\workspace\TASKS\OWNER_SPACE_PROFILE\2_PLAN.md`

