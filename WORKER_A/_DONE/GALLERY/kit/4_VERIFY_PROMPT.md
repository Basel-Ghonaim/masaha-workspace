# Verify a step of GALLERY (for any assistant — Copilot, Codex, Claude)

You check, **read-only**, what a worker or a reviewer just claimed, before the owner acts on it.
Run from `C:\Users\basel\masaha`. Never edit, commit, merge, comment or run tests. **Do not use any project skill.**
Answer the owner **in Arabic**, short, ending with one line: «جاهز للخطوة التالية» or «غير جاهز: …».

**Which step** (the owner says one of these):
- **After the execution (the PR):** `gh pr list --head feat/space-gallery --json number,headRefOid,mergeStateStatus`;
  `gh pr checks <n>` (every check passed, on this head); `CLEAN`; the commits' subjects counted (≤ 50);
  `git diff --name-only origin/main...origin/feat/space-gallery` stays in scope (apps/web and docs only; nothing in apps/api or packages/shared); the report
  `C:\Users\basel\.prompt\MASAHA_WORKER_A\REPORT\GALLERY_REPORT.md` exists and its claims match the PR (head, commits, what was run).
- **After the review:** read the review report in `C:\Users\basel\.prompt\MASAHA_WORKER_A\REPORT\`. Is it a real review (concrete
  findings with file and line, or a reasoned "nothing found"), not an empty one? For each finding: real
  or not, small or not; recommend **a fix round** (anything about money, data, security, authorization
  or a blocker) or **merge and record** (nits).
- **After a fix round:** the new head, CI passed on it, `CLEAN`, the fix present in the code
  (`git show origin/feat/space-gallery:<file>`), and a "Review fixes" comment on the PR.
