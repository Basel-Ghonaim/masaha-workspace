# HARDEN — execute the approved plan (the execution conversation)

You are the **executor** of one Work Item in the Masaha repository, in a fresh conversation. You have
not seen the planning conversation and do not need it.

1. Work in `C:\Users\basel\masaha-b` — never in `C:\Users\basel\masaha` (worker A is building GALLERY
   there) and never in a design worktree. Read `CLAUDE.md` at the repository's root.
2. Read the plan **whole**: `C:\Users\basel\.prompt\MASAHA_WORKER_B\PLAN\HARDEN_PLAN.md`, including the
   owner's approval at its top (S1–S6 approved). **Do not re-decide anything in it.** No plan mode: the
   plan is approved; go straight to §12.1.
3. Follow its procedure step by step: §12.1 (the folder, `origin/main`, the branch
   `fix/space-api-hardening`, `docker start masaha-postgres-1`, never `db:up`), **§12.2's first checks
   before any code**, the six commits in order (each red first, each break recorded), §12.4's checks,
   §12.5's breaks (backup copy, never `git checkout`), §12.6's real run on 3321, §12.7's PR number,
   push and PR, §12.8's CI, `CLEAN`, conflict check and the report at
   `C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\HARDEN_REPORT.md` (UTF-8, written in parts).
4. **§14 "Stop and ask" binds.** A break that stays green, a first check that fails three root-cause
   attempts, a code conflict with GALLERY: stop and say so — never improvise around it.
5. **One full test run at a time on this machine:** before every full lane, §12.1's process check; if
   worker A's folder (`C:\Users\basel\masaha\`) runs one, wait. Focused runs of one or two files are fine.
6. Never merge, create an Issue, add tool attribution, print a secret (never print `apps/api/.env`), or
   use `git add -A` / `.`. A fix before the push folds into its commit (§12.3).
7. The project's skills (`open-pr`, `final-report`) may be used as the appendix maps them; the plan wins
   where they differ.

When the PR is green and `CLEAN` and the report is saved, say so in a short summary and stop.
