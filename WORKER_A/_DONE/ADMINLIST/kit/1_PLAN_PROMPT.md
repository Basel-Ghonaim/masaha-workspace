# ADMINLIST — the admin's spaces list: a state as two facts, the deleted spaces and their restore (web) — PLAN ONLY

**Worker A, the planning conversation** (the owner's trial: plan → execute → review, three
conversations; see §0). Main folder `C:\Users\basel\masaha`, on `main` (`a82541b`), clean.
**You write the plan only:** no branch, no edit, no commit. Databases `masaha_dev` / `masaha_test`;
API 3320, web 5320 (only to look; stop what you start).
**Plan:** `C:\Users\basel\.prompt\MASAHA_WORKER_A\PLAN\ADMINLIST_PLAN.md` — save it, then stop.
If you are Claude Code: use `start-work-item` (steps 1–4) and `write-plan`; otherwise follow §0.

## 0. The plan must stand alone

A fresh conversation executes it, **possibly Copilot or Codex** (Claude may be out of its limits);
a third conversation reviews. So: every decision taken with its one-line reason; the files and, for each
new hook, component or service, its interface; every user-facing string in Arabic and English with its
catalogue key; each state named to the design system's components; each test with its lane, title and
the break that must make it fail (`docs/development/testing.md` §3); the commits, subjects counted
(≤ 50); the executor's procedure with its commands (branch `feat/admin-deleted-spaces` cut from the
latest `origin/main`; checks after each commit; the local verification; a real run with screenshots
to `C:\Users\basel\Downloads\adminlist-shots\`; push; `gh pr create --assignee @me --label feat --label
area:web --label area:docs` with the description written out; `gh pr checks` and `CLEAN`; the report
to `C:\Users\basel\.prompt\MASAHA_WORKER_A\REPORT\ADMINLIST_REPORT.md`; the conflict check with
`git merge-tree --write-tree`); a **"Stop and ask"** list; an appendix mapping steps to Claude's skills,
"only a map". No step may depend on a Claude skill. Never merge; no tool attribution; stage by path.

## 1. The task

The admin's spaces list on the dashboard (`features/space-links`, `AdminSpacesList`; the row menu is
`features/spaces`' `SpaceActionsMenu`) catches up with the design and with the API #67 already built:
- **A3 — a space's state is two facts:** each row shows its verification badge always (موثّقة /
  غير موثّقة) and, beside it, «مخفية» when hidden — no longer one badge, hidden first. The row's facts
  `isVerified`, `isHidden`, `deletedAt` are already in the API's rows.
- **«محذوفة» — the deleted spaces:** a fourth choice of the status filter, reading
  `GET /admin/spaces?status=deleted`; their rows muted, dated («حُذفت في …», Gaza's calendar, the list's
  date rule), naming their owners, with **«استرجاع»** (`POST /admin/spaces/:spaceId/restore`) as their
  only action (no Hide, no Delete, no Edit). After a restore: a toast naming the space, the list fetched
  again. This **resolves finding 44** (no screen restores a deleted space once its toast has gone) and
  the screen part of **finding 50** (an owner whose only spaces are deleted stays an owner: the way back
  is restore → unlink → delete; say so in the finding).
- **A7 — «بيانات قديمة فقط» becomes a `ToggleGroup` chip** by the result count (a switch is not a
  filter field); **A8 — «ناقصة» is `warning`** (the built list shows it `neutral`, #50).
- Remove the web's own status list that left `deleted` out (`space-links.md` › *Web decisions*: "The
  list keeps its own statuses…") — `?status=deleted` now opens the deleted list.

## 2. Read first

`CLAUDE.md`; `docs/development/workflow.md`; `docs/features/space-links.md` (whole: the admin's list on
the web, its address rules, its states, the deleted-spaces item's decisions) and `docs/features/spaces.md`
(the row actions, the Undo's restore, the 429 hold); `docs/api/api-contract.md` › `GET /admin/spaces`
(`status=deleted`, the row's facts) and `POST /admin/spaces/:spaceId/restore`; findings 44 and 50; the
design: `C:\Users\basel\.prompt\MASAHA_DESIGN\DECISIONS_ADMIN.md` › A3, A7, A8 and its *Amended* notes,
and the prototype's `docs/design/prototype/Admin spaces.html` (serve `docs/design/prototype` with
`python -m http.server`), `docs/design/INDEX.md` § 43; `docs/frontend/architecture.md` (§3, §7, *Where
state lives*); `docs/frontend/design-system/foundation.md` §5, §9, §10, §12; `docs/frontend/localisation.md`.

## 3. Settled decisions

- **D1 — web only.** Nothing in `apps/api` or `packages/shared`: the API (#67) answers everything. If
  the list needs a change there, stop and say so.
- **D2 — the restore's feedback follows P8 and #50's patterns:** pending on the row's button, then a
  toast «استُرجعت {name}» (write the English), the list fetched again; a failure in a toast naming the
  space; a 429 holds every row's actions, as the list does today.
- **D3 — a deleted row offers only «استرجاع»** (the space must be restored before anything else).
- **D4 — the phone's cards** show the same facts and the same single action.

## 4. Findings

44 resolved; 50's screen part resolved (status line and resolution). New findings: **69–70**.

## 5. Boundaries

Worker B works in `apps/api` (the owners on a space's read, finding 59) at the same time: you touch no
API file. Shared documents (`space-links.md` — the *Web* parts; `spaces.md` — *Web*; the findings
index; the overview's *Built* line) take the fast path. One full test run at a time on this machine.
