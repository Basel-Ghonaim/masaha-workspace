# OWNERSREAD — a space's read names its owners (API; finding 59) — PLAN ONLY

**Worker B, the planning conversation** (the owner's trial: plan → execute → review, three
conversations; see §0). Worktree `C:\Users\basel\masaha-b`, detached at `origin/main` (`a82541b`).
**You write the plan only:** no branch, no edit, no commit. Databases `masaha_b_dev` / `masaha_b_test`;
API 3321 (only to look; stop what you start).
**Plan:** `C:\Users\basel\.prompt\MASAHA_WORKER_B\PLAN\OWNERSREAD_PLAN.md` — save it, then stop.
If you are Claude Code: use `start-work-item` (steps 1–4) and `write-plan`; otherwise follow §0.

## 0. The plan must stand alone

A fresh conversation executes it, **possibly Copilot or Codex** (Claude may be out of its limits);
a third conversation reviews. So: every decision taken with its one-line reason; the files and each
new function's interface; each test with its lane, title and the break that must make it fail
(`docs/development/testing.md` §3, rule 7 for a security or ordering property); the commits, subjects
counted (≤ 50); the executor's procedure with its commands (branch `feat/space-owners-read` cut with
`git switch --no-track -c feat/space-owners-read origin/main`; checks after each commit; the local
verification; real requests against 3321; push with `git push -u origin feat/space-owners-read`;
`gh pr create --assignee @me --label feat --label area:api --label area:docs` with the description
written out; `gh pr checks` and `CLEAN`; the report to
`C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\OWNERSREAD_REPORT.md`; the conflict check with
`git merge-tree --write-tree`); a **"Stop and ask"** list; an appendix mapping steps to Claude's skills,
"only a map". No step may depend on a Claude skill. Never merge; no tool attribution; stage by path.

## 1. The task

**Finding 59:** the admin's space editor cannot name a verified space's owner: `GET
/admin/spaces/:spaceId` does not say who owns it, so the read-only page says «يعدّلها مالكها» with no
name, and the design's «فك ربط {name}» (A4's one dialog, one item per owner) cannot be built. Add the
space's **active owners** (each `id` and `name`, oldest link first) to the admin's read of one space.

## 2. Read first

`CLAUDE.md`; `docs/development/workflow.md`; `docs/features/spaces.md` and `docs/features/space-links.md`
(whole: who owns a space, the links, the composed reads, the levels); `docs/backend/conventions.md` §7
(levels: `spaces` is L1 and **never imports `space-links`** (L2)), §9 *Composed reads*, §13 (the space's
share lock on the read); `docs/api/api-contract.md` › `GET /admin/spaces/:spaceId` and *Owners (the
admin)*; `docs/architecture/data-model.md` › *Spaces*; finding 59; `docs/development/testing.md` §1–§4.

## 3. Settled decisions (review them in "Stronger decisions")

- **D1 — the owners come from `space-links`, composed above `spaces`** (conventions §9): the read of one
  space for the admin is answered with its owners by a composition at the right level, never by
  `spaces` importing `space-links`. Choose where (a composed handler in `space-links`' admin router, or
  the composition root wiring a reader into the route) and say why.
- **D2 — the field:** `AdminSpace.owners: { id, name }[]`, active owner links only, oldest first; empty
  for an unverified space. Settle whether it is a new field of `AdminSpace` or its own read
  (`GET /admin/spaces/:spaceId/owners`): **the web imports `AdminSpace`** (the editor's fixtures), so a
  required new field breaks web tests — if you add it to `AdminSpace`, declare the narrow licence to
  update only the web's fixtures and types that break, and list those files.
- **D3 — consistency:** the owners read under the same share lock as the space's facts, so a link
  changing meanwhile cannot show a stale "verified" beside fresh owners (finding 43's lesson; #73's
  review leftover 3 on the public page).
- **D4 — no web screen here:** the editor's name in the Alert and «فك ربط {name}» are worker A's later.

## 4. Findings

59: the API part resolved (status stays *Open* until the web shows the name, or split it — say which).
New findings: **71–72**.

## 5. Boundaries

Worker A works in `apps/web` on the admin's spaces list (`features/space-links` › `admin-list`,
`features/spaces` › `menu`, `restore` flows) at the same time. If D2 makes you touch web files, they
must not be those: list yours, and stop if one overlaps. Shared documents take the fast path. One full
test run at a time on this machine: check the main folder runs no lane before `test:api`.
