Resume WI-C2 (the owner restarted you, interactively, on 2026-11-25).

What happened: your headless run ended on 2026-11-24 around 18:00 local (exit 4) while you were waiting on your own
background runs; the machine then restarted (21:11). Your last messages said a batch of deliberate test breaks was
applied for a run, to be restored from its backup when the script ended — that script was killed.

State now (checked by the supervisor):
- `C:\dev\masaha\app-design` on `feat/sign-in-in-place`, **nothing committed**; 68 tracked files changed
  (+1,341 / -428) and 22 untracked. A copy is in `C:\dev\masaha\_worktree-backups\2026-11-25-c2\`
  (`c2-tracked.patch`, `c2-untracked.txt`). Do not delete it.
- The stale `heavy-slot-1` (your lint GRANT of 15:59 UTC, no END) was cleared and logged as `super CLEAR`.
- Docker and `masaha-postgres-1` are up. `main` is now `c3968a74` (#156, ADR 0022, docs only, merged after you
  branched — no file of yours). Your PR number is **#157** unless taken first: check both lists before the push.

Do, in order:
1. **First, find and undo any deliberate break still applied.** Compare the working tree with your break batch's
   backup and your plan's break list; restore from your own backup, never with `git checkout --` (it would wipe the
   uncommitted work). Say in the report what you found.
2. Then continue the approved plan to the end without stopping: commits, local verification, the Chrome pass, the
   PR, green CI and `CLEAN`, then `4_REPORT.md`. Never merge.
3. **Run heavy commands in the foreground** (through `heavy.mjs c2`), one at a time, and wait for each; do not end
   your turn while a run is pending.
