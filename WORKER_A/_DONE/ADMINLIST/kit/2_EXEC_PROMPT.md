# ADMINLIST — execute the approved plan (the execution conversation)

You are the **executor** of one Work Item in the Masaha repository, in a fresh conversation. You have
not seen the planning conversation and do not need it.

1. Work in `C:\Users\basel\masaha`. Read `CLAUDE.md` at the repository's root.
2. Read the plan **whole**: `C:\Users\basel\.prompt\MASAHA_WORKER_A\PLAN\ADMINLIST_PLAN.md`. It is approved as written (with any answers the owner added at
   its top). **Do not re-decide anything in it.**
3. Follow its procedure step by step: the branch `feat/admin-deleted-spaces` from the latest `origin/main`, the
   order of work, the checks after each commit, the local verification (test:unit, test:component; not test:api (no API change)),
   the real run on 5320 (web) with the API on 3320, the push, the PR with the description the plan writes out, CI and
   `CLEAN`, the conflict check, and the report at `C:\Users\basel\.prompt\MASAHA_WORKER_A\REPORT\ADMINLIST_REPORT.md`.
4. Whenever the plan's *Stop and ask* applies, stop and ask; never improvise around it.
5. Never merge, create an Issue, add tool attribution, print a secret, or use `git add -A` / `.`.
   **One full test run at a time on this machine:** before a full lane, check that the other worker's
   folder runs none.
6. If you are Claude Code, the plan's appendix maps its steps to the project's skills; otherwise ignore it.

When the PR is green and `CLEAN` and the report is saved, say so in a short summary and stop.
