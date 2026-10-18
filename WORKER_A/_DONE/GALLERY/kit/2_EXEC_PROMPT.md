# GALLERY — execute the approved plan (the execution conversation)

You are the **executor** of one Work Item in the Masaha repository, in a fresh conversation. You have
not seen the planning conversation and do not need it.

1. Work in `C:\Users\basel\masaha` — never in a design worktree. Read `CLAUDE.md` at the repository's root.
2. **First check:** ADMINLIST (`feat/admin-deleted-spaces`) and OWNERSREAD (`feat/space-owners-read`) are both merged into `origin/main` (`git fetch origin; git log --oneline origin/main -8`). If not, stop and say so.
3. Read the plan **whole**: `C:\Users\basel\.prompt\MASAHA_WORKER_A\PLAN\GALLERY_PLAN.md`, including the owner's approval note at its top. **Do not
   re-decide anything in it.**
4. Follow its procedure step by step: the branch `feat/space-gallery` from the latest `origin/main`, the order of
   work, the checks after each commit, the local verification (test:unit, test:component; not test:api (no API change)), the
   real run on 5320 (web) with the API on 3320 and STORAGE_MODE=local, the push, the PR with the description the plan writes out, CI and `CLEAN`,
   the conflict check, and the report at `C:\Users\basel\.prompt\MASAHA_WORKER_A\REPORT\GALLERY_REPORT.md`.
5. Whenever the plan's *Stop and ask* applies, stop and ask; never improvise around it.
6. Never merge, create an Issue, add tool attribution, print a secret, or use `git add -A` / `.`.
   **One full test run at a time on this machine:** before a full lane, check that the other worker's
   folder runs none.
7. If you are Claude Code, the plan's appendix maps its steps to the project's skills; otherwise ignore it.
8. **The owner's approval of 2026-10-17 at the plan's top binds** (seven amendments, among them
   **commit 0 = §14, #84's review corrections, first in the history**). Work commit by commit — 0, 1, 2, 3 —
   and finish each commit's checks before the next. Write the report in parts: first the file with the
   head, the commits and the checks, then append the rest in short steps.

When the PR is green and `CLEAN` and the report is saved, say so in a short summary and stop.
