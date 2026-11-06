# OWNER_SPACE_PROFILE — rollback execution prompt

You are reverting **only the work you performed for OWNER_SPACE_PROFILE**. Do not implement
anything else.

## Required outcome

Return the repository and your worktree to the exact state they had immediately before you began
the OWNER_SPACE_PROFILE task:

- Remove every file you created for this task.
- Restore every file you modified for this task to its pre-task contents.
- Remove every commit you created for this task from the task branch, if doing so is safe and the
  branch has not been shared.
- Leave all unrelated work exactly unchanged.

## Safety rules

- Work only in `C:\dev\masaha\app`.
- Do not touch `apps/`, `packages/`, `docs/`, or any other path unless it was changed by you for
  OWNER_SPACE_PROFILE.
- Never use `git reset --hard`, `git clean`, recursive deletion, `git checkout .`, or
  `git restore .`; those commands can destroy unrelated work.
- Do not revert the current uncommitted changes belonging to another task, especially existing
  changes under `docs/design/`.
- Do not amend or rewrite commits that predate your task.
- Do not push, open a PR, merge, or modify `main`.
- Do not run formatting, build, tests, migration, dependency installation or code-generation
  commands.

## Procedure

1. Record the current branch and `git status --short`.
2. Identify the exact task-start baseline from the task handoff, the branch history, and your own
   worker log. If the baseline or ownership of a change is uncertain, stop and report instead of
   guessing.
3. List every commit, file, and untracked file created or changed by you for OWNER_SPACE_PROFILE.
4. For committed changes, revert only those task commits with a targeted, non-destructive method.
   Do not reset past commits that contain unrelated work.
5. For uncommitted changes, restore only files you personally changed, and delete only files you
   personally created for this task after confirming their exact paths.
6. Verify with `git status --short`, `git diff --stat`, and targeted diffs that all task changes
   are gone and unrelated changes remain byte-for-byte untouched.
7. Do not create a commit unless the owner explicitly asks for one. Report the resulting branch,
   baseline comparison, removed commits, restored/deleted files, and proof that unrelated changes
   remain.

## Stop conditions

Stop immediately and report if:

- you cannot distinguish your changes from another worker's changes;
- the task branch contains commits mixed with unrelated work;
- the only available command would risk losing unrelated changes;
- the pre-task baseline cannot be established;
- the branch was pushed or shared and reverting it needs an owner decision.

The final response must be a concise rollback report. Do not claim completion unless the targeted
verification proves that only OWNER_SPACE_PROFILE work was removed.
