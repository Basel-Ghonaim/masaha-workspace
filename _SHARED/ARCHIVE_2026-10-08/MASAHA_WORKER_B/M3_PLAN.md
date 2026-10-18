# M3 — Three small document fixes (plan)

## 1. Summary

Documents only. Three units:
1. **#53** — the repository stops naming the university and the defence (`CLAUDE.md`, `docs/plans/v1-mvp.md`, ADR 0014).
2. **Finding 48** — `npm run db:up` from a second folder recreates the shared container bound to that folder; recorded, indexed, and one line added to `setup.md`.
3. **Design issues** — a standing bullet in workflow §2 phase 2 and a matching section in the `write-plan` skill.

## 2. Contract

**Scope:** the edits below, on branch `docs/small-fixes` from `origin/main` (`bcb2e04`).

**Acceptance criteria**
- [ ] No in-scope document names the university, a supervisor, a defence or a graduation project (grep over `CLAUDE.md`, `docs/` minus `docs/design/`, `.claude/`).
- [ ] v1-mvp keeps 16 January 2027 as v1's target date; phase 8 is "Report and presentation", work unchanged.
- [ ] ADR 0014 carries a dated `Revised` line; its decision is unchanged.
- [ ] Finding 48 exists (Open), is in the index's Open group, and `setup.md` says what to run in a second folder.
- [ ] Workflow phase 2 and the `write-plan` skill both list the design issues.
- [ ] `npm run format:check` passes; every link/anchor I added or touched resolves.

**Out of scope:** `README.md` (done), the `graduation-cap` icon key (finding 10 mentions it), showcase text, `docs/design/`, `.design-sync`, anything in `apps/`, `packages/`, `docs/features/`, `docs/frontend/`. No fix of the compose file itself (finding records, doesn't schedule).

## 3. Reading done

`CLAUDE.md` (mission), `workflow.md` §2 phases and §7, documentation rules §8, issue #53, `docker-compose.yml`, findings README, finding 29 (model), `setup.md` › Running a second folder, ADR 0014, `v1-mvp.md` timeline, `write-plan/SKILL.md`.
(Documentation rules §1 was not re-read: the prompt's §7 route — ADR revised in place — is what the workflow states, line 166.)

## 4. Settled decisions, as built

**Commit 1 — `docs: remove the university and the defence`** (`Closes #53` in the PR)
- `CLAUDE.md` line 8: "It is a graduation project (Al-Quds Open University, Gaza) built by one developer in four months, where engineering quality is part of the deliverable." → "It is built by one developer, where engineering quality is part of the product." Nothing else.
- `docs/plans/v1-mvp.md`: Timeline sentence → "The project started on 27 September 2026 and v1's target date is **16 January 2027**, its only fixed date." Phase 8 row → "8. Report and presentation | Final report, presentation, rehearsal; by 16 January 2027 | To come". `Last Updated` → 2026-10-10.
- ADR 0014 *Context*: "The graduation defence runs on the local environment" → "The demonstration runs on the local environment"; a second line under the existing header: `> **Revised:** 2026-10-10 — the context no longer names the defence; the decision is unchanged`.

**Commit 2 — `docs: record finding 48, the shared container's folder`**
- New `docs/architecture/findings/48-db-up-from-another-folder-recreates-the-shared-container.md`, in finding 29's shape: `# 48. …`, **Status:** Open · **Date:** 2026-10-10, **Evidence** (relative bind `./docker/postgres/create-test-database.sql` in `docker-compose.yml`; compose project name `masaha` is shared, so a second folder's `db:up` sees a changed config and recreates `masaha-postgres-1` bound to that folder; the named volume `masaha-pgdata` keeps the data; the container fails to start once the folder is gone), **Resolves when:** the container no longer depends on the folder that started it.
- Index: add `48` at the end of the *Open* group.
- `setup.md` › *Running a second folder*: one line — in a second folder never run `npm run db:up`; run `docker start masaha-postgres-1` (linking finding 48 for the why). `Last Updated` → 2026-10-10.

**Commit 3 — `docs: make a plan's design issues a standing section`**
- `workflow.md` §2 phase 2: new bullet after "the files": "for an item that builds or changes a screen, the design issues it finds — a mistake in the design, with a better solution from the design system's components and tokens — built only once the reply approves them;". `Last Updated` → 2026-10-10.
- `write-plan/SKILL.md`: new list item after "the files", renumbering 8→12 to 9→13, linking `workflow.md#phases`.

## 5. Stronger decisions

1. **Finding number: 48, not 60 (owner's reply).** 60 came from a range that no longer exists; workflow §9 *Conflicts* gives worker B 48 onward (A holds 46–47). Built as 48.
2. **ADR revised in place (the prompt corrects issue #53).** Agreed — workflow §7 allows it; no stronger alternative.
3. **"The demonstration" in ADR 0014** still reads as an event for an audience, but it is the owner's wording and accurate enough; no alternative is worth the churn.
4. **Finding 48 is a record of a hazard, not a fix.** A real fix (an absolute bind path, or baking the init SQL in) changes `docker-compose.yml`, outside this item. Proposed, not built.
5. Otherwise none: no document rule is contradicted or weakened.

## 6. Related findings

- 29 (second folders): related, not folded — it is Resolved and about ports; finding 48 is a new, separate hazard. Linked from finding 48's evidence for context.
- 10 mentions `graduation-cap`: not a mention of the university; untouched.
- No finding folded.

## 7. Files

Edit: `CLAUDE.md`, `docs/plans/v1-mvp.md`, `docs/architecture/decisions/0014-deployment.md`, `docs/architecture/findings/README.md`, `docs/development/setup.md`, `docs/development/workflow.md`, `.claude/skills/write-plan/SKILL.md`. Add: finding 48. Nothing in A's area. Shared with A: `findings/README.md` index (A adds 46 and resolves 45 in the same file) — I own only the line for 48 at the end of *Open*; the risk is a trivial merge conflict, checked with `git merge-tree --write-tree` at the report if A's PR is open (none is open now).

## 8–9. Tests and Review Focus

No behaviour, no code, no tests. Review Focus: the exact new wording of the three replaced sentences; whether "Report and presentation" should keep "final report" (kept, per prompt).

## 10. Commits

The three above, Conventional Commits, no tool attribution, staged by explicit path. PR title `docs: remove the university, record finding 48`; labels `docs`, `area:docs`; assignee the owner; body carries the contract and `Closes #53`.

## 11. Verification

Run: `npm run format:check`; link check by hand (each added/touched link and anchor: finding 48 ↔ index ↔ setup.md, skill → `workflow.md#phases`, finding 48 → finding 29 and ADR 0014); a grep for the university/defence terms over the in-scope files. Not run: test lanes, build, lint, typecheck — no code (workflow §2 phase 4 exception); CI runs them. Then push, PR, wait for CI and `CLEAN`, report to `M3_REPORT.md`. Never merge.

## 12. Decisions needed from the owner

- None open: the reply settled the number (48).
