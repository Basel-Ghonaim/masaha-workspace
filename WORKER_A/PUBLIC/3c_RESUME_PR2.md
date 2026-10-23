# PUBLIC PR 2 (`feat/directory-map`) — resume where the work stopped

You are worker A's executor, in a fresh conversation. **Any capable coding agent** may run this (Claude Code,
Codex, Copilot): no step depends on a Claude skill; do not run `start-work-item`. The previous executor stopped
at the end of the owner's working day on 2026-10-21 with a clean tree.

## Where it stands (2026-10-21, 18:00)

- Branch `feat/directory-map` in `C:\dev\masaha\app`, local only (nothing pushed), head `ecfb7556`, cut from
  `origin/main` `c3391d0e`. `git status --short` clean.
- Done: the eight carried commits (items 1–11 of `0_CARRIED_FROM_103.md`; item 12 is no change), the plan's
  commit 1 `feat(map): show many marks and pick a centre` (`4a9077a0`, with its `fixup!` `5fd9994b` to fold),
  and commit 2 `feat(directory): show the spaces on a map` (`ecfb7556`).
- Left: **the plan's PR 2 commit 3** `feat(directory): set my location on the map` (tests 59–60), then the
  fold of the `fixup!` (`GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash origin/main`), the head's checks, the
  real run, `#PRNUM`, push, the PR, CI green and `CLEAN`, the conflict check.
- `origin/main` has moved to `5a0cda1a` (#104, the seed only): **do not rebase for it.** `masaha_dev` now holds
  the directory's demo set (seeded by the supervisor); FULL and "closed today" held on 2026-10-21 only — on a
  later day a missing FULL is **not performed, by design**, with tests 50 and 55.

## Do

1. Read, in this order: `C:\dev\masaha\workspace\WORKER_A\PUBLIC\3_EXEC_PROMPT_PR2.md` (whole — it still binds:
   the stop rule, §3's runs, §6's reply), the report `4_REPORT_PR2.md` (whole — its departures stand), and in
   `2_PLAN.md` only: the approval note at the top, §9 *PR 2 · Commit 3*, §10's tests 59–60, §12's PR 2 row and
   §13 (the head's checks, the real run's PR 2 cases, push and the PR). Read the code files commit 3 names, each
   once.
2. `git status --short` clean and `git log --oneline -1` = `ecfb7556`; else **stop and report**.
3. Build commit 3 as the plan says (tests red first, then green; separate breaks only per §3.1), then continue
   from `3_EXEC_PROMPT_PR2.md` §1.5 onwards for what is left.
4. Append to `4_REPORT_PR2.md` as you go, under "Resumed (<the tool you are>, <date>)". Final reply in
   `3_EXEC_PROMPT_PR2.md` §6's shape.
