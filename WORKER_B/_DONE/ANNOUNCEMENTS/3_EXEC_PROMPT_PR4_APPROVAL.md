# ANNOUNCEMENTS PR 4 — the supervisor's approval of phase 1 (2026-10-26)

**Phase 1 approved. Go on to phase 2 now** (`3_EXEC_PROMPT_PR4.md` §3–§8), to the end: the PR open, CI green on
its head, `CLEAN`, the report and the final reply. This file wins where the prompt differs.

## 1. The SQL — approved as written

`apps/api/prisma/migrations/20261026114022_closure_extension_key/migration.sql`, read whole by the supervisor:
the key added nullable, existing rows given `gen_random_uuid()`, `SET NOT NULL`, the unique index
`closure_extensions_request_id_key`; the function and the trigger word for word as D12; no PR number. The schema's
two added lines (`idempotencyKey … @unique @map("request_id") @db.Uuid`) approved. `migrate diff --script` instead
of `--create-only` (refused as non-interactive): accepted, as the prompt allowed. Apply it now with `npx prisma
migrate dev` on `masaha_b_dev` (no second migration may appear: if Prisma proposes one, stop and read why), then
the test database as the lanes do.

Accepted as departures (say them in the PR's description): `daysFrom` moved from `subscriptionStatus.ts` to
`packages/shared/src/core/gazaTime.ts`, exported, imported back (C2); `lockClosure` = `repository.lockIn` plus the
`CLOSURE` check, no second lock.

## 2. `main` moved — bring the branch up first

The owner merged **#122** (worker A's customers file, `apps/web` and `docs`): `origin/main` = `3855e37f`. Your
branch sits at `1a89da5d` with no commit and two uncommitted paths (`schema.prisma`, the new migration folder),
neither touched by #122. Before the first commit: `git fetch origin`, then `git merge --ff-only origin/main`
(it keeps the working tree's changes; **never** `git checkout`, `stash` or `reset`). `git log -1` must show
`3855e37f`. #122 changed `docs/features/subscriptions.md` and `docs/architecture/findings/README.md` (its
findings 162–163, 123 resolved): re-read them on this tree before editing; keep their lines.

## 3. No stop until ready for review — the owner's word for this run

The owner is away. **You do not stop and you do not ask** until the work is ready for review: the PR open, CI
green on its pushed head, `CLEAN`, the report written. **The autonomy rule applies to all of phase 2:** read
`C:\dev\masaha\workspace\_SHARED\AUTONOMY_2026-10-25.md` and follow it. Every "stop and ask" or "stop and report"
in `3_EXEC_PROMPT_PR4.md` and the plan becomes **decide, record, continue**:
- a decision the plan or prompt leaves open, a plan false against the code, a break that stays green, a carried
  item larger than its file, 12.2's checks 1–2 failing → choose the option that best keeps the plan's intent, the
  documents' rules and v1 scope, the smaller and safer change first; record it as you go under *Decisions taken
  without the owner* (what you met, the options, the choice and why, how to undo it);
- a command or lane you cannot run → find the root cause (up to three tries; Docker Desktop not running: start it
  with `Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"` and wait for `docker info`), else
  record it under COULD NOT RUN with the exact error, continue every step it does not block, and let CI judge on
  the pushed head;
- a real-run case the demo data cannot hold → record it as not run, with why, and continue (never change data
  through the app to pass it, never reseed).
The rule's hard limits still hold: never merge, push to `main`, force-push another branch, create an Issue,
delete a remote branch, touch worker A's folder, worktree (`C:\dev\masaha\app`), database (`masaha_dev`) or ports
(3320, 5320), skip or weaken a test, print a secret or add tool attribution.

## 4. Worker A runs beside you

Worker A starts DESK_SCREENS PR 4 in `C:\dev\masaha\app` now (`apps/web`, `docs`; no API or `packages/shared`
code). Its web lanes and yours may overlap: before each full lane check free memory and record it; the memory rule
as the prompt says (never stop A's processes).
**The PR number:** you will likely open first, as **#123** — check `gh pr list --state all --limit 1` just before
the push. **After `gh pr create`, compare the number it answered with the one written into the commits.** If they
differ (A opened first), re-run the `#PRNUM` replacement with the right number on your own branch and push it with
`git push --force-with-lease=feat/closure-extension:<the sha you pushed>`; record it. This is the only force-push
allowed, and only on your own branch.

## 5. The end

Ready for review = the final reply in the prompt's §8 shape, with `Decisions taken without the owner` filled,
`files <n>` given (no size stop, the owner's rule), and the report complete. Then end.
