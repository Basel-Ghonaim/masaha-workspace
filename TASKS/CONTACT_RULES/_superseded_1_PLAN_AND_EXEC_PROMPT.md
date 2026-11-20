# CONTACT_RULES — phones, links, a row's ghost control, two test hygiene findings — PLAN briefly, then BUILD

You are a **Claude Code worker** on **Masaha** (a bilingual Arabic RTL / English platform for coworking spaces in
Gaza; monorepo `apps/web`, `apps/api`, `packages/shared`), a fresh session, **Opus 5.5, effort high**. Production is
live: every merge to `main` deploys. The owner's decisions are binding and complete:
**`C:\dev\masaha\workspace\TASKS\CONTACT_RULES\0_OWNER_DECISIONS.md` (C1–C7) — read it first.** Plan briefly, save
the plan, then build at once (no stop): an open point you meet, take the safest answer the documents allow and record
it.

**Where:** a new worktree, so the PROTOTYPE_SPLIT worker in `C:\dev\masaha\app` is never disturbed:
`git -C C:\dev\masaha\app worktree add C:\dev\masaha\app-cr -b fix/contact-rules origin/main`, then work only in
`C:\dev\masaha\app-cr`. Copy the two `.env` files from `C:\dev\masaha\app` (`apps/api/.env`, `apps/web/.env`),
**pointing its databases at new ones of its own** — `masaha_cr_dev` (create it as a copy of `masaha_dev`:
`CREATE DATABASE masaha_cr_dev TEMPLATE masaha_dev` once no session uses `masaha_dev`) and `masaha_cr_test` (empty;
the API lane migrates it) in the Docker container `masaha-postgres-1` (port 5433; **start Docker Desktop and the
container first if they are down**). Ports **3337 / 5337** (API `PORT`, `CORS_ORIGIN`, the web's proxy). `npm ci`,
`npm run build -w @masaha/shared`, `prisma generate` — all through the grant script. No schema change in this item.

## Read

`CLAUDE.md`; `docs/development/workflow.md`, `testing.md` (§3 rule 8), `engineering-principles.md`;
`docs/features/spaces.md` (contacts), `customers.md` / `desk.md` (a customer's phone), `platform-settings.md`;
`docs/architecture/data-model.md` › Conventions (phones, contacts); `docs/api/api-contract.md` (contacts, phones,
`invalid_format`); `docs/frontend/design-system/foundation.md` (read only — C7) on hover and `hover-on-muted`; the
five findings 217, 218, 219, 225, 226 in full; `packages/shared/src/core/phone.ts`,
`packages/shared/src/spaces/contacts.ts` and their tests; the web's users of `normalisePhone`, `phoneSchema` and
`normaliseContact` (`useContactsSheet.ts`, `usePhoneOwner.ts`, `useEditDialog.ts`, `platformContact.ts`); the web's
existing `toWesternDigit…` helper (finding 217 names it) — one conversion, in `packages/shared`, used everywhere.

## Build — one commit per unit (subject ≤ 50, with a body; Conventional; no attribution)

1. **C1 + C2 — phones** (`packages/shared/src/core/phone.ts`): Arabic-Indic and Eastern digits become Western before
   the rule reads them; the accepted forms stay `+970` / `+972` / `00970` / `00972` / local (C2). Unit tests for each
   form, each digit set, mixed separators, and the refusals (another country code, too short, letters). API tests:
   a WhatsApp contact and a desk customer typed `٠٥٩٩١٢٣٤٥٦` are stored `+970599123456`. A component test: the
   contacts' Sheet takes Arabic digits and sends the E.164 form.
2. **C3 + C4 — links** (`packages/shared/src/spaces/contacts.ts`): the website and Facebook rules of C3; «وسيلة أخرى»
   keeps its rule (a number → phone, else a website). Unit tests for every accepted and refused shape listed in C3 —
   including `123`, `599123456`, `http://10.0.0.1`, `localhost`, `example` (no TLD), `facebook.com/watch?v=…`,
   `facebook.com/<page>/videos/…`, `/groups/…`, `/share/…`. A component test proving C4: a refused link is said on its
   row and **no request is sent**; an API test proving the server refuses it too (`invalid_format`). Existing
   contacts in the data that the new rules would refuse: **do not change data** — list how many in
   `masaha_cr_dev` (a read-only query) in the report.
3. **C5 — the row's ghost control** (design system: `Table.tsx` / `Button.tsx` or a row-scoped variant — the smallest
   change in the layer, semantic tokens only): the «⋯» of `StaffActionsMenu`, `CustomerMenu`, `SpaceActionsMenu`
   shows `hover-on-muted` over a hovered row and while its menu is open, both themes. A component test on the classes
   and `check:classes` green; a capture at 1440 light and dark (through the grant script) to
   `C:\Users\basel\Downloads\contact-rules-shots\`.
4. **C6 — tests:** 219 (the shared component setup removes toasts or waits out their timers at teardown — no
   production change) and 225 (the four files warm their lazy routes in `beforeAll`). Never weaken a test.
5. **Documents:** the capability documents, the contract and the data model where the rules are described; each
   finding marked resolved in its own file. **The findings index (`findings/README.md`) only after PROTOTYPE_SPLIT's
   PR has merged** (C7): until then, build everything else, then wait (check `gh pr list --state merged --search
   "head:chore/design-archive-out"` every few minutes, bounded), rebase on `main`, write the index lines.

Each new test: break the code it guards once, watch it fail, restore.

## Verify (complete, before the push)

Through the grant script (`node C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs cr <command…>`, which waits
for memory; a run killed for memory: retry once, then CI judges): `npm run lint`, `typecheck`, `format:check`,
`check:classes`, `check:links`, `check:conflicts`, `build` + `check:build` (production build), `test:unit`,
`test:component`, `test:api`.

## Finish

Push `fix/contact-rules`, open the PR with the `open-pr` skill (the decisions C1–C7, the data count of step 2, the
Evidence), wait until `gh pr checks <n>` is all green on the pushed head and `CLEAN`, write
`C:\dev\masaha\workspace\TASKS\CONTACT_RULES\4_REPORT.md` (PR, full head sha, commits, each finding's fix and test and
its seen failure, the decisions you took, anything left). Stop the servers you started by PID. **Never merge.**
Leave the worktree and its databases for the supervisor to remove after the merge.
