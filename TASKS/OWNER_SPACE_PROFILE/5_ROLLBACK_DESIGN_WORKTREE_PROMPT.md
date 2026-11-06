# OWNER_SPACE_PROFILE — rollback design worktree

The first rollback was intentionally limited to `C:\dev\masaha\app`, but the remaining
OWNER_SPACE_PROFILE implementation work is in:

`C:\dev\masaha\app-design`

Revert **only the OWNER_SPACE_PROFILE work in that worktree**. Do not touch
`C:\dev\masaha\app`, which has already been restored and is clean.

## Required outcome

Restore `C:\dev\masaha\app-design` to the exact state it had immediately before the
OWNER_SPACE_PROFILE worker began:

- Remove every file created by that worker.
- Restore every file modified by that worker.
- Remove the worker's task commits if they contain only OWNER_SPACE_PROFILE work.
- Preserve unrelated changes, commits, branches and untracked files byte-for-byte.

## Safety rules

- Work only in `C:\dev\masaha\app-design`.
- Do not touch the main worktree at `C:\dev\masaha\app`.
- Do not use `git reset --hard`, `git clean`, recursive deletion, `git checkout .`,
  or `git restore .`.
- Do not remove or revert changes unless you can attribute them to OWNER_SPACE_PROFILE.
- Do not rewrite commits that predate the worker's task.
- Do not push, merge, open a PR, install dependencies, run builds, tests, formatting or code
  generation.
- Do not create a commit unless explicitly requested.

## Procedure

1. Record the current branch, `git status --short`, `git log --oneline --decorate -20`,
   and worktree path.
2. Establish the exact task-start baseline using the worker's task log, branch history and
   task handoff. The previous report says the branch is
   `feat/owner-space-profile-design`; verify that before acting.
3. Identify every commit, tracked file, untracked file and generated artifact created or changed
   by OWNER_SPACE_PROFILE in this worktree.
4. If task commits are isolated and unshared, remove their changes with a targeted,
   non-destructive method. If a commit mixes unrelated work, do not rewrite it; restore only
   the task-owned files and report the mixed commit.
5. Restore or delete only the identified task-owned paths. Never use a repository-wide restore.
6. Verify with `git status --short`, `git diff --stat`, targeted diffs and branch history that
   OWNER_SPACE_PROFILE changes are gone and unrelated work remains.
7. Leave the worktree clean only if it was clean before the task. Otherwise preserve its exact
   pre-task dirty state.

## Stop conditions

Stop and report without changing anything if:

- the pre-task baseline cannot be established;
- a file or commit cannot be attributed confidently;
- task changes are mixed with unrelated changes in a commit;
- the branch was pushed or shared;
- the rollback requires an owner decision.

Report the worktree, branch, baseline, removed task commits, restored/deleted files, preserved
unrelated changes, and verification evidence. Do not claim completion without that evidence.
