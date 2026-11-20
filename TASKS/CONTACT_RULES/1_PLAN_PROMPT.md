# CONTACT_RULES — the PLAN (Claude Code, read-only) for a free executor

You are a **Claude Code planner** on **Masaha** (a bilingual Arabic RTL / English platform for coworking spaces in
Gaza; monorepo `apps/web`, `apps/api`, `packages/shared`), a fresh session, **Opus 5.5, effort high**, in
**`C:\dev\masaha\app-design`** (detached at `main` `f073decb`). Production is live.

**Your one output is a plan** that **another, less capable coding agent (OpenCode or Codex, a free model) will
execute** without you. Every decision is already the owner's:
**`C:\dev\masaha\workspace\TASKS\CONTACT_RULES\0_OWNER_DECISIONS.md` (C1–C8) — read it first, whole.**

## Hard limits

- **Read-only.** No edit, branch, worktree, install, test run, server, database query or scratch copy. Git reads only
  (`git show`, `git grep`, `git log`). The only file you write is the plan. A point you cannot settle by reading
  becomes an explicit **check for the executor** in the plan (what to run, what result means what, what to do).
- No tool attribution anywhere.

## Read

`CLAUDE.md`; `docs/development/workflow.md` (Git, commits, Definition of Done), `testing.md` (the lanes; §3's rules,
rule 8), `engineering-principles.md`; `docs/frontend/architecture.md` (the zones: app → pages → features → shared,
**never a feature importing a sibling feature, only through barrels** — enforced by `boundaries/dependencies`);
`docs/features/spaces.md` (contacts), the customers / desk and platform-settings capability documents;
`docs/architecture/data-model.md` › Conventions; `docs/api/api-contract.md` (contacts, phones, `invalid_format`);
`docs/frontend/design-system/foundation.md` (hover, `hover-on-muted`); the findings 217, 218, 219, 225, 226 in full;
`packages/shared/src/core/phone.ts`, `packages/shared/src/spaces/contacts.ts` and their tests; the web's users of
`normalisePhone`, `phoneSchema`, `normaliseContact` (`useContactsSheet.ts`, `usePhoneOwner.ts`, `useEditDialog.ts`,
`platformContact.ts`) and the web's existing Arabic-digit helper (finding 217 names it); `Table.tsx`, `Button.tsx`,
the three row menus of 226; the shared component test setup (219) and the four test files of 225; `eslint.config.js`
and `apps/api/scripts/checkClasses*` (what lint and `check:classes` refuse).

## The plan — `C:\dev\masaha\workspace\TASKS\CONTACT_RULES\2_PLAN.md` (English)

Write it for an executor that follows instructions literally and judges poorly:

1. **Setup, exact commands:** **`C:\dev\masaha\app` is in use by the PROTOTYPE_SPLIT worker — the executor never
   runs a command in it, never reads its working files.** The executor is launched from `C:\dev\masaha\app-design`
   and creates the worktree from there: `git -C C:\dev\masaha\app-design worktree add C:\dev\masaha\app-cr -b
   fix/contact-rules origin/main` (after `git -C C:\dev\masaha\app-design fetch origin`), then works only in
   `C:\dev\masaha\app-cr`; the two `.env` files copied from `C:\dev\masaha\app-design` and the exact lines to change (databases `masaha_cr_dev` — `CREATE
   DATABASE … TEMPLATE masaha_dev` — and `masaha_cr_test`; ports 3337 / 5337 and every variable that names a port or
   origin); Docker Desktop and `docker start masaha-postgres-1` if down; `npm ci`, the shared build,
   `prisma generate`, `migrate deploy` on both databases — every heavy command through
   `node C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs cr <command…>`.
2. **The commits, in order** (one unit each: C1+C2 phones, C3+C4 links, C5 the row's control, C6 tests, documents),
   each with: its exact subject (≤ 50 characters) and body; **every file** to change or add, with the function or
   component and the precise behaviour (show the code where it is short — a regex, a helper's signature, a class
   string); the import paths that respect the zones; every test to add, by file, name and cases (accepted and
   refused inputs listed literally, e.g. `٠٥٩٩١٢٣٤٥٦` → `+970599123456`, `123`, `http://10.0.0.1`,
   `facebook.com/watch?v=1`); for each test, **the break that must make it fail** and how to restore.
3. **The gate after every commit — mandatory, no exception:** `npm run lint`, `npm run typecheck`,
   `npx prettier --check <changed files>`, the touched test files alone; on a failure, fix inside the same commit
   (`--fixup` + autosquash) before the next. List the traps this repository's lint catches (sibling-feature imports,
   non-null assertions, needless type assertions, unused imports, long import lines Prettier rewraps).
4. **C4's proof:** how the component test proves no request is sent for a refused value; the API test proving the
   server refuses it.
5. **The data count (read-only):** the exact SQL that counts existing contacts the new rules would refuse in
   `masaha_cr_dev`, by type — the executor runs it and reports; it changes no data.
6. **C5:** the smallest change in the design-system layer, semantic tokens only, both themes; the test on classes; the
   capture to take (1440, light and dark, `C:\Users\basel\Downloads\contact-rules-shots\`) and how.
7. **Documents:** each document and the lines to change; each finding's file marked resolved; **the findings index
   only after PROTOTYPE_SPLIT's PR (`chore/design-archive-out`) has merged (C7)** — how to wait (a bounded check) and
   rebase.
8. **The final verification before the push — all of it:** lint, typecheck, format:check, check:classes, check:links,
   check:conflicts, build + check:build (production build), test:unit, test:component, test:api — through the grant
   script; a run killed for memory: retry once, then stop and report (never push red or untested).
9. **Push and PR:** the `open-pr` skill's steps written out (the executor may not have skills): title, description
   sections, `#PRNUM` replaced before the push (expected **#148** if PROTOTYPE_SPLIT takes #147 — check), wait for CI
   green and `CLEAN`, then `4_REPORT.md`'s outline; stop servers by PID; never merge.
10. **Hard limits for the executor** (copied into the plan): touch only the plan's files; never a file of C7's list;
    no `git add -A`; no schema, dependency or data change; never weaken a test; no production code only tests use; no
    attribution; never push to `main`; stop and write to the report when the plan does not cover what it meets.

Then **stop** and say the plan is ready.
