# Verify a step of OWNERSREAD (for any assistant — Copilot, Codex, Claude)

You check, **read-only**, what a worker or a reviewer just claimed, before the owner acts on it.
Run from `C:\Users\basel\masaha-b`. Never edit, commit, merge, comment or run tests. **Do not use any project skill.**
Answer the owner **in Arabic**, short, ending with one line: «جاهز للخطوة التالية» or «غير جاهز: …».

**Which step** (the owner says one of these):

- **After the plan:** read `C:\Users\basel\.prompt\MASAHA_WORKER_B\PLAN\OWNERSREAD_PLAN.md`. Does it stand alone (every decision with its reason, files and
  interfaces, strings in both languages, tests with their breaks, commits with subjects ≤ 50 — count
  them, a procedure with commands, a "Stop and ask" list)? List its open questions for the owner, each
  with a recommendation. Does it stay in the prompt's scope (apps/api, packages/shared and docs; web files only if the plan declared them)?
- **After the execution (the PR):** `gh pr list --head feat/space-owners-read --json number,headRefOid,mergeStateStatus`;
  `gh pr checks <n>` (every check passed, on this head); `mergeStateStatus` is `CLEAN`; the commits'
  subjects counted (≤ 50); `git diff --name-only origin/main...origin/feat/space-owners-read` stays in scope;
  the report `C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\OWNERSREAD_REPORT.md` exists and its claims match the PR (head, commits, what was run).
- **After the review:** read the review report in `C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\`. Is it a real review (concrete
  findings with file and line, or a reasoned "nothing found"), not an empty one? For each finding:
  real or not, small or not; recommend **a fix round** (anything about money, data, security or a
  blocker) or **merge and record** (nits).
- **After a fix round:** the new head, CI passed on it, `CLEAN`, the fix present in the code
  (`git show origin/feat/space-owners-read:<file>`), and a "Review fixes" comment on the PR.
