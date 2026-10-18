# MANAGE (step 5a) — the owner's API for their space: profile, facts, confirms, photos (API) — PLAN ONLY

**Worker B, a planning conversation** (the owner's trial: plan → execute → review). **You write the
plan only:** no branch, no edit, no commit, no server.
**Plan:** `C:\Users\basel\.prompt\MASAHA_WORKER_B\PLAN\MANAGE_PLAN.md` — save it, then stop.
If you are Claude Code: use `write-plan` for its discipline; otherwise follow §0.

**Where you read — important.** Worker B is **executing another plan right now** (OWNERSREAD, branch
`feat/space-owners-read`) in `C:\Users\basel\masaha-b`: **do not work in that folder.** Work in
`C:\Users\basel\masaha-design-b` (a clean worktree at `origin/main`; never check out anything there):
run `git fetch origin`, then read the code **only from `origin/main`'s commit objects** —
`git show origin/main:<path>`, `git ls-tree -r --name-only origin/main <dir>`,
`git grep <pattern> origin/main -- <paths>`. Read OWNERSREAD's plan
(`C:\Users\basel\.prompt\MASAHA_WORKER_B\PLAN\OWNERSREAD_PLAN.md`): it changes the admin's read of one
space and the composition root, which this item builds on. **Do not run the start-state check that
requires the main folder:** this conversation only plans.

## 0. The plan must stand alone

A fresh conversation executes it — **possibly Copilot or Codex** — **after OWNERSREAD has merged**,
from the latest `origin/main`; a third conversation reviews (independent: it touches authorization).
So: every decision taken with its one-line reason; the files and each new function's or router's
interface; each test with its lane, title and the break that must make it fail
(`docs/development/testing.md` §3; **rule 7 for every authorization property: make the break once**);
the commits, subjects counted (≤ 50); the executor's procedure with its commands (check OWNERSREAD is
in `origin/main`; `git switch --no-track -c feat/owner-space-api origin/main` in
`C:\Users\basel\masaha-b`; checks after each commit; `test:unit`, `test:api`, `lint`, `typecheck`,
`format:check`, `check:links` — `test:component` only if a type the web imports changes; real requests
against 3321 as an owner, as reception, as a stranger and as the admin; `git push -u origin
feat/owner-space-api`; `gh pr create --assignee @me --label feat --label area:api --label area:docs`
with the description written out; `gh pr checks` and `CLEAN`; the report to
`C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\MANAGE_REPORT.md`; the conflict check with
`git merge-tree --write-tree`); a **"Stop and ask"** list; an appendix mapping steps to Claude's skills,
"only a map". No step may depend on a Claude skill. Never merge; no tool attribution; stage by path.

## 1. The task (step 5a of `docs/plans/v1-mvp.md`)

The owner keeps their space's public facts true through `/manage/spaces/:spaceId/...`, on the **same
services** the admin's routes use (the profile's edit, each fact group's save and confirm, the
photos), with `can()` deciding who may act (the owner of a verified space; reception reads):
- the space middleware (`requireSpaceAccess`, conventions §8) mounted **once** on
  `/manage/spaces/:spaceId`, before every module's `manage` router;
- `GET` the space (profile and facts) for the owner **and reception**; `PATCH` the profile, `PUT` each
  fact group (`hours` with the shifts, `prices`, `amenities`, `contacts`), `POST …/:group/confirm`, for
  the owner;
- the photos: `GET|POST /manage/spaces/:spaceId/photos`, `DELETE …/:photoId`, `PUT …/order`, the
  owner's, on the photos service of #77.
**Not here:** packages (step 5b, its own item); capacity and the stay limit (the space's settings,
O2 — a later item); any web screen.

## 2. Read first (from `origin/main`)

`CLAUDE.md`; `docs/development/workflow.md`; `docs/features/spaces.md` and `space-links.md` (whole);
`docs/backend/conventions.md` §2, §7, §8 (*Space access*, the links loader, `requireSpaceAccess`),
§9, §13; `docs/backend/security.md` (*Authorization*, the `can()` table, rate limits);
ADR 0002 and **ADR 0009** (the space-scoped roles; who may do what); `docs/api/api-contract.md` §1–§6,
*Spaces (the admin)* (the shapes to mirror), *Managed spaces*; `docs/plans/v1-mvp.md` › step 5 and the
planned `/manage` rows; `docs/architecture/data-model.md` › *Spaces*; the design for the owner's
editor (what the API must serve): `C:\Users\basel\.prompt\MASAHA_DESIGN\DECISIONS_OWNER.md` › O1, O6,
O7; `docs/development/testing.md` §1–§4.

## 3. Settled decisions (the owner, 2026-10-15)

- **D1 — step 5a only:** the routes above; packages are 5b.
- **D2 — the space middleware refuses a caller with no link to the space as security.md says;** if
  security.md is silent, **404** (no hint that the space exists). Verify which, and cite it.
- **D3 — reception reads, the owner writes:** reception gets the `GET` of the space (the desk needs the
  hours and the prices); every write is the owner's, decided by `can()`. A stranger and a user with no
  link are refused; the admin keeps the `/admin` routes (decide, with a reason, whether `/manage` also
  admits the admin or not, following ADR 0009).
- **D4 — the owner's photos are in this item,** on the same service, limits, lock and `can()` as the
  admin's.
- **D5 — capacity and the stay limit are out** (the space's settings, a later item).
- **D6 — the audit:** the same action names as the admin's changes; the actor tells them apart.
- **D7 — one implementation:** no copy of a service or a rule; the routers differ, the services do not.
  A deleted space answers 404 on `/manage` as on `/admin`; a hidden space stays editable by its owner.

## 4. Findings

Read the open findings' titles; open those that touch authorization, rate limits or the space's
routes (17, 21, 23, 52, 59). New findings: **75–76**.

## 5. Boundaries

Worker A builds the editor's gallery in `apps/web` (after ADMINLIST and OWNERSREAD merge): you touch
nothing in `apps/web` unless a type the web imports changes — then declare the files. If a shared type
must change, say so. Shared documents (`spaces.md` — *API* parts; the contract; the findings index;
the overview's *Built* line) take the fast path. One full test run at a time on this machine.
