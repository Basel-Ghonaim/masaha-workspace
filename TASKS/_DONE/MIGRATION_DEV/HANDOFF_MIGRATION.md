# Handoff — the organisation and migration supervisor («مشرف التنظيم والنقل»)

**Temporary.** It lives until the migration is closed (§10 of the plan), then it moves to `_DONE` with the task.
You are **one of three supervisors**. The main supervisor (the project's analyst, its own conversation, reading
`D:\masahaWorkspace\HANDOFF.md`) reads this file's *Status log* to know where you are. The design-review
supervisor (#81) is the third. You do not direct workers' Work Items, and they do not touch your task.

## 1. Your one task

Move every Masaha folder under `C:\dev\masaha\` **with no broken link**, by the plan
`D:\masahaWorkspace\TASKS\MIGRATION_DEV\1_PLAN.md` — read it whole first. You may execute the commands yourself
(read-write on these folders) or give them to the owner; either way **one phase at a time, each verified, each
recorded** in `4_REPORT.md`. A mistake here is hard to undo: when anything differs from the plan, **stop and
ask the owner** — never improvise.

## 2. How you work with the owner

- Reply in **Arabic**, short; no line starts with an English word or a code token; decisions as items with
  options and a recommendation, never tables. Commands and paths in code blocks, in English.
- The owner decides. You propose. "Approved" for one phase is not approval for the next.
- **The quiet point is the owner's call.** Before Phase 1, ask the owner — and check with your own commands —
  that no worker runs: worker A (OWNERS, branch `feat/admin-add-owner` in `C:\Users\basel\masaha`), worker B
  (STAFF, `feat/space-staff` in `C:\Users\basel\masaha-b`), design reviews (Kilo in `masaha-design`). Their PRs
  may be open on GitHub — that is fine; their **sessions** must be closed and their trees clean or recorded.
- Tell the main supervisor nothing directly; write your *Status log* — the owner relays.

## 3. Facts you can rely on (verified 2026-10-18)

- One NVMe disk (238 GB): `C:` 218 GB (35 free), `D:` a 19 GB partition (15 free). `C:\dev\` does not exist yet.
- `git worktree list` (main `C:\Users\basel\masaha`): `masaha-b`, `masaha-design`, `masaha-design-b` linked.
- Junctions `node_modules\@masaha\{api,shared,web}` are absolute: `node_modules` is **deleted before the
  moves** and reinstalled with `npm ci` in `app` and `app-b` only (the owner's amendment at the plan's top).
- `docker-compose.yml` has `name: masaha`; the container is `masaha-postgres-1`; data in a volume. Never
  `npm run db:up` or `db:reset`; start with `docker start masaha-postgres-1`.
- The repository has no absolute path; the Playwright MCP configs point to `C:\Users\basel\Downloads` only.
- The workspace is the private repo `Basel-Ghonaim/masaha-workspace`; nightly task
  `masaha-workspace-snapshot` at 23:00 runs `_SHARED\snapshot.ps1`.
- Memories that matter (two): `C:\Users\basel\.claude\projects\c--Users-basel-masaha\memory\` (worker A)
  and `C--Users-basel-masaha-b\memory\` (worker B). The others are left as they are.

## 3b. The one absolute rule

**You never delete an old copy** (the old workspace, the old folders, the backup) — not even with the owner's word in the chat. You hand him the paths and the commands; **he deletes them by hand.**

## 4. Lessons the project paid for (keep them)

- Never `npm ci` while VS Code is open — a locked native file leaves `node_modules` half-installed. During
  the migration VS Code is closed, so `npm ci` is right.
- Heredoc edits in Git Bash can mangle backslashes and Arabic: write scripts to files and run them with
  `python -I <file>`; write files as UTF-8, keep LF/CRLF as found; PowerShell 5.1's `Set-Content -Encoding utf8`
  adds a BOM — use `[IO.File]::WriteAllText(p, s, (New-Object Text.UTF8Encoding $false))`.
- Restore from a backup copy, never `git checkout` (it wipes uncommitted work).
- A backgrounded dev server leaves `tsx watch` on its port: stop by PID, then check the port.
- Never claim a check you did not see pass: copy its output line into the report.

## 5. Done means

All seven phases verified; the owner opened the new folders and ran one worker; the workspace repo pushed with
the path commit; the nightly task runs from the new path; memories copied and readable; the old copies listed
for the owner, **who deletes them himself**. **The whole task is one sitting of one to two hours.** Then: `HANDOFF.md` (the main one) gets one line, this file
and the task move to `_DONE`, and your conversation ends.

## Status log (append one dated line per step; newest last)

- 2026-10-18 — created by the analyst; plan approved in principle; waiting for the owner's quiet point.
- 2026-10-18 — owner fixed the quiet point: after STAFF and OWNERS PR 2 both merge, before any new item. Who
  runs the migration (this supervisor or the main one) is re-decided then.
- 2026-10-18 17:15 — owner declared the quiet point (#89, #90 merged; main = 18ab1705; no open PR). Checked: heads,
  clean trees, no stash, `feat/admin-add-owner` / `feat/space-staff` gone — all true (§2's branch names are stale).
  Not quiet yet: VS Code open with 3 Claude Code sessions (one resumes a `c--Users-basel-masaha` chat), Codex and
  Copilot in it; `opencode serve` running with 2 Playwright MCPs. `4_REPORT.md` absent — Phase 0 not done. Waiting.
- 2026-10-18 17:20 — owner closed VS Code (checked: no Code/codex/copilot/IDE claude left). Still running:
  `opencode serve --service` (PID 3656, since 09:42) + its Playwright MCPs. Owner confirmed: memories from the main
  worktree and `masaha-b` only. Found: `c--Users-basel-masaha\memory` has 35 files; `C--Users-basel-masaha-b` has
  **no `memory\` folder** (transcripts only) — nothing to copy for B. `masaha-b` has no `apps\api\.storage`.
- 2026-10-18 17:25 — owner amends: `masaha-design` and `masaha-design-b` are temporary — **not moved**. `masaha-b`:
  delete if nothing is lost, move if something is. Checked: both design heads are on `origin/main`, ignored files
  only `apps/api/src/generated/` → nothing lost; they are removed **by the owner** (`git worktree remove`), never by
  me. `masaha-b`: head on `origin/main`, clean; unique only `.claude/settings.local.json` + two `.env` (backup in
  Phase 0); 10 active workspace files name `masaha-b`. Recommended: move it (cheap, keeps worker B ready). Waiting.
- 2026-10-18 17:40 — owner: `masaha-b` is moved; opencode stopped. **Phase 0 done** (see `4_REPORT.md`): snapshot
  `ae869df` pushed, task disabled; backup `C:\dev-migration-backup\2026-10-18\` hash-verified (35 memory files);
  `node_modules` gone in `masaha` and `masaha-b`, 2032 tracked files intact. Waiting for the owner on Phase 1.
- 2026-10-18 17:50 — owner removed both design worktrees (checked). **Phase 1 done**: `masaha-b` →
  `C:\dev\masaha\app-b`, head `18ab1705`, clean, 2032 files, `.env` = backup. Waiting for the owner on Phase 2.
- 2026-10-18 18:00 — **Phase 2 done**: main → `C:\dev\masaha\app` (4622 files, same bytes), `worktree repair` linked
  `app-b` both ways; both clean at `18ab1705`; `.env`/settings/storage = backup; fsck clean; memory 35 untouched.
  No `masaha*` folder left in `C:\Users\basel`. Waiting for the owner on Phase 3.
- 2026-10-18 18:10 — **Phase 3 done**: `npm ci` exit 0 in `app` then `app-b`; the three `@masaha` junctions in
  each point inside their own worktree, 0 outside; shared built, Prisma generated; both clean. Waiting on Phase 4.
- 2026-10-18 18:20 — Phase 4: `app` lint/typecheck/unit green (1788 tests). **STOP**: `masaha-postgres-1` won't
  start — its bind mount names the old path `C:\Users\basel\masaha\docker\postgres\...` (plan §1.4 missed it);
  Docker re-created 3 empty folders there. Volume `masaha_masaha-pgdata` intact. Asked the owner.
- 2026-10-18 17:55 — owner: back up the volume, recreate via compose. Volume tar hash-verified (3018 files);
  container recreated from `C:\dev\masaha\app`, same data ("Skipping initialization", clean shutdown 14:08:35 UTC),
  4 DBs present. **Phase 4 done**: `app` and `app-b` lint/typecheck/unit/API test green, `/health` db up on
  3320 and 3321, ports freed. Waiting for the owner on Phase 5.
- 2026-10-18 18:05 — Phase 5 started (owner's word): snapshot `c9ad45c`; robocopy to `C:\dev\masaha\workspace`
  2485 files, SHA-256 IDENTICAL, git log equal, fsck clean. Dry run: 73 files / 439 replacements (`5_DRYRUN.md`).
  From now this log lives only in the new copy. Waiting for the owner on the dry run.
- 2026-10-18 18:05 — owner approved the four recommendations. **Phase 5 done**: old copy renamed
  `D:\masahaWorkspace.OLD-2026-10-18` (not deleted); 71 files / 434 paths rewritten, 0 residual, 2 lines fixed by
  hand; `ec6bffc` pushed; nightly task recreated on the new path, run once (Last Result 0). Waiting on Phase 6.
- 2026-10-18 18:10 — **Phase 6 done**: memory copied (not moved) to `C--dev-masaha-app\memory` (35 = source =
  backup), wording updated there only (5 files, 0 residual); `settings.json` 3 rules → `/c/dev/masaha/app`;
  setup.md clean. Waiting on Phase 7.
- 2026-10-18 18:10 — **Phase 7 done**: memory key confirmed by the owner's session (`C--dev-masaha-app`); final scan
  clean (tasks, Docker, git, env, tool configs, workspace, repo); old copies listed for the owner (3 items).
  Migration complete. Waiting for the owner's deletes and his word to close the task.
- 2026-10-18 18:20 — **closed** on the owner's word: one line in `HANDOFF.md` (§0), its row and `BOARD.md` point
  here; this folder moved to `TASKS\_DONE\MIGRATION_DEV`. The owner deletes the three old copies himself (4_REPORT §7.3).
