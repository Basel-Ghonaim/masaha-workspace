# OWNER_SPACE_PROFILE — prototype execution prompt

You are the implementation worker for Masaha's **design prototype only**. Read this prompt
completely before changing anything.

## 0. Start and repository state

- Repository: `C:\dev\masaha\app`.
- Read `CLAUDE.md`, `docs/design/README.md`, and the approved plan
  `C:\dev\masaha\workspace\TASKS\OWNER_SPACE_PROFILE\2_PLAN.md`.
- Start only after verifying the worktree is clean and based on the latest `origin/main`.
  Fetch first, then create `feat/owner-space-profile` from `origin/main`. Do not reuse the
  currently dirty branch.
- This is a prototype-only implementation. The existing uncommitted design-prototype changes
  belong to another task and must not be overwritten; coordinate or stop if they conflict.

## 1. Scope and hard limits

This task is **prototype work, not production application work**:

- Edit only `docs/design/`.
- The primary target is `docs/design/prototype/Owner space profile.html` and only the prototype
  data/shared files needed to make that screen work.
- You may update `docs/design/INDEX.md`, `docs/design/CHANGES.md`, and
  `docs/design/prototype/Flows - states.html` when required by prototype documentation rules.
- Never edit `apps/`, `packages/`, production React/TypeScript, API code, Prisma/schema files,
  production copy catalogues, or any file outside `docs/design/`.
- Do not add a production route, endpoint, schema, dependency or application implementation.

Implement the approved prototype experience only:

- View-first Owner profile with six cards:
  Basics & Location, Photos, Hours, Prices, Amenities, Contact.
- Independent section Sheets with Save and Cancel inside each Sheet.
- Prototype loading, error, success, dirty-close and responsive states.
- Freshness summary, stale ages, `Still correct`, section navigation and `View public page`.
- Grouped-hours editing, prices table, contact/amenity states and photo drag-and-drop-only reorder
  as prototype interactions.

Do not add booking, payment, reviews, QR check-in, Admin-specific behavior, new production
contracts, or unrelated prototype screens.

Do not use `git add -A` or `git add .`. Do not amend commits. Do not add tool attribution or a
`Co-Authored-By` trailer. Do not push or open a PR unless separately instructed.

## 2. Prototype rules

- Read and follow `docs/design/README.md`.
- Use only classes already defined by the prototype's prebuilt design-system bundle or existing
  prototype classes; run the class check after changes.
- Keep every visible and assistive string bilingual using the prototype's existing translation
  pattern, Arabic first where that is the established convention.
- Respect the prototype's single global scope per page; do not introduce duplicate top-level names.
- Do not use object rest syntax if prohibited by the prototype rules.
- Use semantic design-system components/tokens and existing interaction patterns. No raw colors or
  arbitrary CSS values outside the prototype's established rules.
- Validate the screen at 390, 768 and 1440 widths, RTL/LTR and light/dark.
- Keep each commit complete and working, with a Conventional Commit subject of 50 characters or
  fewer. Run the prototype checks for each commit.

## 3. Decisions that are already approved

- This is a visual/interaction prototype; production API authorization and server contracts are
  not implemented here.
- Photos are excluded from freshness confirmation.
- Prices are represented as the canonical table while preserving the prototype's supported
  dimensions and unavailable values.
- The archived prototype is the implementation target for this task only after applying the
  approved View-first redesign; production code and API documents are reference material.
- Drag-and-drop remains the only photo movement interaction. Do not add before/after/cover buttons.
  Use an accessible prototype interaction. If the prototype framework cannot express the
  required keyboard/assistive behavior without a new dependency or production work, stop and
  report the blocker.
- Put `View public page` in the desktop page header and in the compact narrow-screen header/menu.

## 4. Tests and verification

Cover the prototype states and interactions for:

- View default, section order, index, summary and public-page action.
- Sheet open/save/cancel/dirty-close/error/success states.
- Hours grouping, Friday, custom per-day mode and validation states.
- Prices table dimensions, unavailable values and responsive presentation.
- Photo complete reorder interaction, failure state and accessible drag behavior.
- Amenities and contact view/edit states.
- RTL/LTR, light/dark and the 390/768/1440 responsive matrix.

Before each commit, run from the repository root:

`node docs/design/scripts/check-parse.mjs`

`node docs/design/scripts/check-classes.mjs`

Serve the prototype over HTTP and manually inspect the required matrix. Record screenshots/evidence
and any skipped checks in the handoff. Do not run production test lanes, builds, API tests,
database commands or `npm ci`; they are outside this prototype-only task.

## 5. Stop rules

Stop and report before editing if:

- the worktree cannot be cleanly based on `origin/main`;
- an unrelated uncommitted prototype change conflicts with the target files;
- the prototype rules cannot support an accessible drag-only interaction without production work;
- a new dependency or any edit outside `docs/design/` appears necessary;
- a required behavior cannot be represented by the prototype's existing patterns.

At completion, report the branch, commits, files changed, prototype checks/results, browser
evidence, skipped checks and remaining findings. Leave the branch local and ready for review.
