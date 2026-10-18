Work Item P-2 — Parallel-work rules in the workflow · branch `docs/parallel-work`

## How to work (mandatory)

1. Read CLAUDE.md, then docs/development/workflow.md, then docs/README.md. Follow the project's workflow exactly.
2. You are **worker B**. You work in the worktree `C:\Users\basel\masaha-b`, detached at the latest `origin/main`. Never work in the main folder `C:\Users\basel\masaha`.
   - Before planning, check:
     - `git rev-parse --show-toplevel` is that folder;
     - the tree is clean;
     - HEAD is detached at the latest `origin/main` after `git fetch`.

     If not, stop and report.
3. Start in PLAN MODE and present a SHORT plan: the section's text, the files, the commit, and how you verify. No edit, no branch and no commit before the owner approves.
4. After approval: `git fetch origin`, then `git switch --no-track -c docs/parallel-work origin/main`. The first push is `git push -u origin docs/parallel-work`.
5. Finish at "Ready for review": self-review, push, open the PR. Never merge.

## Context

Since A-1, the owner runs **two Claude Code workers at the same time**. The rules that keep them from colliding have been repeated in every prompt, but they live nowhere in the project:
- `docs/plans/foundation.md` §2 holds the parallel rules of one past period (the design-system plan beside F-1 to F-3, in a worktree called `masaha-api`).
- `docs/development/workflow.md` owns how work is executed, and says nothing about parallel work.

P-2 records the **stable** rules in `workflow.md`. Documentation only.

## The rules to record (stable rules, not the current assignment)

- **Two workers:**
  - **worker A** works in the main folder and carries the critical path;
  - **worker B** works in one long-lived worktree, `masaha-b`, and carries items that neither block nor wait for worker A;
  - one Work Item is one fresh conversation, as today.
- **Worker B's branches:** between items its worktree is detached at `origin/main`. Each item cuts its own branch with `git switch --no-track -c <branch> origin/main`: `--no-track`, so a plain push can never target `main`.
- **Files:**
  - every prompt names the other worker's files;
  - a file both items need is declared in the plan first, edited minimally, and each side keeps to its own section;
  - new dependencies on both sides at once are avoided, because `package-lock.json` would conflict.
- **Databases:** the API test lane empties every table between files. So two workers never share a test database:
  - worker B uses its own `masaha_b_dev` / `masaha_b_test` in the shared container;
  - a branch that changes the schema always uses its own databases.
- **Merging:**
  - one PR is merged at a time;
  - before opening a PR, fetch and rebase on the latest `main`;
  - whoever merges second rebases, and resolves a conflict by keeping both sides.
- **After each merge, in the main folder:**
  - `git pull`;
  - after a schema change, regenerate the Prisma client and apply the new migrations to `masaha_dev`.

  The dev database once fell seven migrations behind because nobody applied them after merging from worktrees.
- **Who works on what at a given moment is NOT recorded** in any document: it changes too often, and would go stale.

## Placement

- **Propose in the plan:** a new section, or a subsection of §3 *Git lifecycle*. Keep the section short: rules, not narrative.
- **Why in `workflow.md`, not a document of its own:** CLAUDE.md makes every session read `workflow.md`, so rules placed there are always read, while a separate document is read only if a session follows its link. A document of its own is justified only if the content grows past rules into procedures (step-by-step commands). Those would then belong in `setup.md`, or in a dedicated document. If you see a reason for that now, propose it in the plan.
- **`foundation.md` §2 is worker A's file:** F-5a is editing `foundation.md` right now. Don't touch it. In the plan, say whether §2 now reads as history of one period (fine as it is) or contradicts the new section. If it contradicts, record a finding; don't edit it.
- If `docs/README.md`'s line for `workflow.md` should mention parallel work, say so in the plan. `README.md` is not worker A's file today.

## Parallel work (read before planning)

**Worker A** runs at the same time in the MAIN folder, on **F-5a** (`feat/auth-api`). Never touch that folder.

**F-5a's documents:**
- `docs/plans/foundation.md`, `docs/plans/v1-mvp.md` (*Planned API surface*);
- `docs/backend/conventions.md`, `docs/backend/security.md`, `docs/api/api-contract.md`;
- `docs/architecture/data-model.md`, `docs/architecture/findings.md`;
- `docs/development/setup.md`.

**P-2's files:** `docs/development/workflow.md`, and `docs/README.md` only if approved.

**Shared:** `docs/architecture/findings.md`, only if a finding is needed. Add it at the end, and keep both sides on rebase.

**Before opening the PR:** fetch and rebase on the latest `main`.

## Out of scope

Any other document, all code, and any change to an existing rule in `workflow.md` beyond adding the section.

## Verification and PR

- Every relative link and anchor resolves.
- `npx prettier --check .` and `npm run lint` pass.

The PR follows workflow §3:
- labels `docs` + `area:docs`, assigned to me (`--assignee @me`);
- the description template, with `@coderabbitai ignore` in the body;
- no AI attribution.

Don't merge.
