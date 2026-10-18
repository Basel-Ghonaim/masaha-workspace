# M3 — Three small document fixes

**Worker B** · worktree `C:\Users\basel\masaha-b`, detached at `origin/main` and clean · branch
`docs/small-fixes`, cut with `git fetch --prune origin`, then
`git switch --no-track -c docs/small-fixes origin/main`.

**Size cap:** no subagents, no workflow. A documentation item: no code, no tests.
**Plan:** `C:\Users\basel\.prompt\MASAHA_WORKER_B\PLAN\M3_PLAN.md`.
**Report:** `C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\M3_REPORT.md`.

**The steps** (the skills `start-work-item`, `write-plan`, `open-pr` and `final-report` hold them;
if your tool does not load skills, follow these): plan, then save the plan to the path above and
**stop** until the reply; after the reply, cut the branch, make the commits, run §5's checks, push,
open the PR, wait for CI and GitHub's `CLEAN`, then save the report to the path above and summarise
it. **No tool attribution anywhere** — no `Co-Authored-By`, no "generated with" line in a commit, the
PR or a document. Never merge.

## 1. The task in brief

Three fixes, all in documents:
1. **Issue #53** — the repository stops naming the university and the defence: Masaha is the
   owner's own project.
2. **Finding 60** — running `npm run db:up` from a second folder recreates the shared database
   container bound to that folder.
3. **A plan's "Design issues" section** becomes a standing part of every plan that builds a screen.

## 2. Read only these

Nothing else is needed; don't read the capability documents, the API, the web or the tests.
- `CLAUDE.md` (its *Project mission*), and workflow §2 *Phases* (phase 2) and §7 (an ADR revised in
  place with a *Revised* line);
- documentation rules §1 (records) and §8 (links);
- issue #53 (`gh issue view 53`);
- the files you edit (§3), and `docker-compose.yml` for finding 60;
- `docs/architecture/findings/README.md` (how a finding is written and indexed) and one existing
  finding as a model.

## 3. The settled decisions (review them in "Stronger decisions")

**Issue #53**
- `CLAUDE.md`, *Project mission*: "It is a graduation project (Al-Quds Open University, Gaza) built by
  one developer in four months, where engineering quality is part of the deliverable." becomes
  **"It is built by one developer, where engineering quality is part of the product."** Nothing else
  in `CLAUDE.md` changes.
- `docs/plans/v1-mvp.md`, *Timeline*: 16 January 2027 stays, as **v1's target date** (no report or
  defence in the sentence); phase 8 becomes **"Report and presentation"**, its work unchanged (the
  final report, the presentation, the rehearsal), without the defence.
- `docs/architecture/decisions/0014-deployment.md`, *Context*: "The graduation defence runs on the
  local environment" becomes **"The demonstration runs on the local environment"**, revised **in
  place**, with a dated `> **Revised:** 2026-10-10 — …` line (workflow §7). Its decision does not
  change. (Issue #53's "not by rewriting it" was wrong: the workflow allows the in-place revision.)
- The PR closes the issue (`Closes #53`). The README is already done; the `graduation-cap` icon and
  the showcase's sample text are not mentions.

**Finding 60**
- Record **finding 60**, *Open*: the compose file binds its init script by a path relative to the
  folder (`./docker/postgres/…`), so `npm run db:up` from any other folder sees a changed
  configuration and **recreates `masaha-postgres-1` bound to that folder**. The data survives (the
  named volume), but the container then depends on that folder, and fails to start once the folder is
  gone. **Resolves when:** the container no longer depends on the folder that started it.
- **And now, in `docs/development/setup.md` › *Running a second folder*:** one line — in a second
  folder, never run `npm run db:up`; run `docker start masaha-postgres-1`.
- Add 60 to the index's *Open* group.

**Design issues**
- `docs/development/workflow.md` §2, phase 2's plan contents gain one bullet: **for an item that builds
  or changes a screen, the design issues it finds** (a mistake in the design, with a better solution
  from the design system's components and tokens), built only once the reply approves them.
- `.claude/skills/write-plan/SKILL.md` gains that section in its list, linking the bullet.

## 4. Boundaries

- Worker A works in the main folder on the web (`feat/admin-add-space`); a design reviewer reads
  there too. **Touch nothing in `apps/`, `packages/`, `docs/features/`, `docs/frontend/` or
  `docs/design/`.**
- New findings, if any, number from 61.
- Run `git merge-tree --write-tree` against A's open PR, if there is one, at the report.

## 5. Checks — only these

This item has no code (workflow §2, phase 4's exception): run **`npm run format:check`** and **the
link check by hand** over the files you changed (every link and anchor you added or touched
resolves). **Don't run** the test lanes, the build, lint or typecheck: CI runs them.

## 6. The pull request

- **Title:** `docs: remove the university, record finding 60` (≤ 50), or your commit subject.
- **Labels:** `docs`, `area:docs`. Assigned to the owner.
- **Commits:** two or three, each one unit (#53; finding 60 with `setup.md`; the design issues).
- The analyst reviews it; don't merge.
