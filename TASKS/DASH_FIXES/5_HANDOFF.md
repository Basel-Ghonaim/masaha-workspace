# DASH_FIXES — hand over to a fresh OpenCode session (context at 80%)

## A. Paste to the current OpenCode session

```
Supervisor's message (relayed by the owner). Your context is at 80%: hand over now to a fresh session.
1. Reach a safe point: never stop inside a rebase, a merge or with a run going — finish or abort the step you are in (a rebase in progress: finish it if it is clean, else `git rebase --abort`). Stop any server you started, by PID.
2. Do not push anything new.
3. Write C:\dev\masaha\workspace\TASKS\DASH_FIXES\4_HANDOFF_STATE.md (English, short): the branch and its local head (full sha), whether it differs from the PR's pushed head, `git status`, the backup/* branches you made; for each of 227, 220, 222, 223 and the lint message (3_LINT_RED_MESSAGE.md) — done / partly / not started, with the files; what you ran locally and its result; anything you decided; the exact next step.
4. Stop.
```

## B. Then start a new OpenCode session in `C:\dev\masaha\app` and paste

```
You continue an item another session started. Read whole, in order: C:\dev\masaha\workspace\TASKS\DASH_FIXES\0_OWNER_DECISIONS.md, 1_EXEC_PROMPT.md (your task and every rule), 2_CI_RED_MESSAGE.md and 3_LINT_RED_MESSAGE.md (the two red CI rounds and the supervisor's direction), then 4_HANDOFF_STATE.md (where the last session stopped). Check the state yourself (git status, git log origin/main..HEAD, gh pr checks 146) before acting. Then finish: 3_LINT_RED_MESSAGE.md's fixes folded into their commit, `npm run lint` and `npm run typecheck` required before the push (through the grant script), the touched test files alone, push with --force-with-lease, CI green and CLEAN, write 4_REPORT.md, stop. Never merge.
```
