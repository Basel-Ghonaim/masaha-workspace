# S2b-4b — execute the approved plan (the execution conversation)

You are the **executor** of one Work Item in the Masaha repository, in a fresh conversation. You have
not seen the planning conversation, and you do not need it.

1. Work in `C:\Users\basel\masaha` (the main folder). Read `CLAUDE.md` at its root.
2. Read the plan **whole**: `C:\Users\basel\.prompt\MASAHA_WORKER_A\PLAN\S2B4B_PLAN.md`. It is approved
   as written (the owner, 2026-10-13: the four design answers, design issues E–H and the stronger
   decisions S1–S4 included). **Do not re-decide anything in it.**
3. Follow its §14 *The executor's procedure* step by step: the branch, the order of work, the checks
   after each commit, the local verification, the real run and the screenshots, the push, the PR with
   its description (§15), CI and `CLEAN`, the conflict check, and the report at
   `C:\Users\basel\.prompt\MASAHA_WORKER_A\REPORT\S2B4B_REPORT.md`.
4. Whenever §16 *Stop and ask* applies, stop and ask; never improvise around it.
5. **Never** merge, create an Issue, add tool attribution to a commit or the PR, print a secret, or use
   `git add -A` / `git add .`. **One full test run at a time on this machine:** before
   `test:component`, check that no other folder (`masaha-b`) is running a test lane.
6. If you are Claude Code, the plan's appendix maps its steps to the project's skills; otherwise
   ignore it — the steps are complete without it.

When the PR is green and `CLEAN` and the report is saved, say so in a short summary and stop.
