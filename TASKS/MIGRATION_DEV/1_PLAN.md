# MIGRATION_DEV — move every Masaha folder under `C:\dev\masaha\`, with no broken link

**Status:** approved by the owner in principle (2026-10-18): one root for all projects, `C:\dev\`, and Masaha
under `C:\dev\masaha\`. **Executed only by the "organisation and migration supervisor", at a quiet point the
owner names, phase by phase, each phase verified before the next.** Written by the analyst from a read-only
inventory of 2026-10-18; every step that depends on the machine's state at that moment is a **check first**.


> **Amended by the owner, 2026-10-18 (binding):** (1) **the whole migration fits in one sitting of one to two
> hours** — the owner does not stop work for days; the old copies are deleted **at the end of the same sitting**,
> after §10's proof, with the owner's word. (2) **`node_modules` is deleted, not moved**, in all four worktrees
> before Phase 1, and reinstalled afterwards with `npm ci` **only in `app` and `app-b`** (the design worktrees
> only serve the prototype with Python and need none). (3) **Only two Claude Code memories matter**: worker A's
> (main worktree, key `c--Users-basel-masaha`) and worker B's (`C--Users-basel-masaha-b`); the others are left.

## 0. Why, and the target

Today Masaha lives in two places: four git worktrees in `C:\Users\basel\` and the working files on
`D:\masahaWorkspace`. `D:` is **not a separate disk** — a 19 GB partition (15 GB free) of the same 238 GB NVMe
as `C:` (35 GB free): it protects nothing and fills up. The user profile is crowded and partly synced by
OneDrive; the desktop path holds Arabic (`OneDrive\سطح المكتب`), which breaks tools.

| Today | Target |
|---|---|
| `C:\Users\basel\masaha` (main worktree; worker A) | `C:\dev\masaha\app` |
| `C:\Users\basel\masaha-b` (worker B) | `C:\dev\masaha\app-b` |
| `C:\Users\basel\masaha-design` (design reviews) | `C:\dev\masaha\design` |
| `C:\Users\basel\masaha-design-b` | `C:\dev\masaha\design-b` |
| `D:\masahaWorkspace` (working files, a private git repo) | `C:\dev\masaha\workspace` |

Other projects of the owner later go to `C:\dev\<project>\` — **not moved in this item**; the supervisor only
lists candidates (and what `D:\MASAHA\` — `DOCS`, `DS`, `PROTOTYPE`, `VD` — is) for the owner to decide.

## 1. What binds a path today (the inventory, 2026-10-18)

1. **Git worktrees.** `C:\Users\basel\masaha\.git\worktrees\<name>\gitdir` holds the absolute path of each
   linked worktree (`masaha-b`, `masaha-design`, `masaha-design-b`); each linked worktree's `.git` file holds
   the absolute path back to the main `.git`. A plain folder move breaks both directions.
2. **npm workspace junctions.** `node_modules\@masaha\{api,shared,web}` are **junctions with absolute
   targets** (`C:\Users\basel\masaha\apps\api`, …) in every worktree that has `node_modules` (the design
   worktrees have one too). A moved folder keeps junctions pointing at the old place: dead or, worse, at
   another worktree.
3. **Ignored local files that must travel:** `apps/api/.env`, `apps/web/.env` in each app worktree (they hold
   the database names and ports: A → `masaha_dev`/`masaha_test`, 3320/5320; B → `masaha_b_dev`/`masaha_b_test`,
   3321/5321), `apps/api/.storage/` (local photos), the generated Prisma client if ignored.
4. **Docker:** `docker-compose.yml` sets `name: masaha`, so the project and the container `masaha-postgres-1`
   keep their names wherever the folder is; the data is in a Docker volume, not the folder. The container's
   `working_dir` label still says `C:\Users\basel\masaha` — harmless (we never run `db:up`; we run
   `docker start masaha-postgres-1`).
5. **The workspace's active files:** 80 files, 474 references to `C:\Users\basel\masaha*` or
   `D:\masahaWorkspace` (task prompts and plans, ROUND2's prompts, scripts and run sheets, `HANDOFF*.md`,
   `BOARD.md`, `_SHARED\snapshot.ps1`, `_SHARED\MAP_AR.md`). Records (`_DONE\`, `REPORT\`, `LOGS\`, archives,
   `MIGRATION\`) keep their old paths **on purpose** — they record what was true.
6. **The nightly backup:** the Windows task `masaha-workspace-snapshot` runs
   `D:\masahaWorkspace\_SHARED\snapshot.ps1`, which `Set-Location`s to `D:\masahaWorkspace`.
7. **Claude Code:** project memory lives in `C:\Users\basel\.claude\projects\<key>\memory\`, the key being the
   folder's path (`c--Users-basel-masaha`, `C--Users-basel-masaha-b`, `C--Users-basel-masaha-design`,
   `C--Users-basel-masaha-design-b`, `D--masahaWorkspace`). A new folder means a new, **empty** key unless
   copied. `C:\Users\basel\.claude\settings.json` holds permission rules naming `C:\Users\basel\masaha`.
   Workers are launched with `--add-dir D:\masahaWorkspace`.
8. **Not bound (checked):** the repository itself (`git grep` finds no absolute path), the Playwright MCP
   configs of Kilo, OpenCode, Copilot CLI and VS Code (their `--output-dir` is `C:\Users\basel\Downloads`).

## 2. Hard rules for the executor

- **Quiet point only:** no worker session open (Claude Code, OpenCode, Kilo, Copilot), no `vitest`, no dev
  server, no Docker command running, **VS Code closed** (it locks `node_modules`). The owner confirms in writing.
- **Every worktree clean** (`git status --short` empty) — or the owner says how to keep its changes. Unpushed
  commits are fine (they move with the folder); record each branch and head first.
- **One phase at a time; verify; record in `4_REPORT.md`; only then the next.** A failed check → stop, report,
  do not improvise. Every move is a rename on `C:` (fast, reversible); the cross-volume workspace move is a
  **copy + hash check, never a move**; the old folder is deleted at the end of the sitting, after §10.
- **Never** `git worktree prune`, `git clean`, `npm ci`, `db:up`, `db:reset`, a delete of `.git`, a delete of
  any old folder before §10.

## 3. Phase 0 — snapshot and record (no change)

1. Run `D:\masahaWorkspace\_SHARED\snapshot.ps1` (the workspace is on GitHub as of now). Disable the task:
   `schtasks /Change /TN masaha-workspace-snapshot /DISABLE`.
2. Record into `4_REPORT.md`: `git -C C:\Users\basel\masaha worktree list --porcelain`; for each worktree its
   branch, head, `git status --short`, `git stash list`; `gh pr list --state open`.
3. Backup outside every folder being moved, to `C:\dev-migration-backup\2026-10-<dd>\`: each worktree's
   `apps\api\.env`, `apps\web\.env` (copy, never print), a listing of `apps\api\.storage\` with sizes, and a
   zip of the two memories that matter: `C:\Users\basel\.claude\projects\c--Users-basel-masaha` and
   `C--Users-basel-masaha-b`.
4. **Delete `node_modules` in all four worktrees** (VS Code closed, no node process): `cmd /c rmdir /s /q
   <wt>\node_modules` — it holds absolute junctions that a move would carry broken, and it makes the moves
   lighter. Check each is gone. (Nothing in it is unique: the lockfile rebuilds it.)

## 4. Phase 1 — the linked worktrees (main still in place)

```powershell
New-Item -ItemType Directory C:\dev\masaha
git -C C:\Users\basel\masaha worktree move C:\Users\basel\masaha-b         C:\dev\masaha\app-b
git -C C:\Users\basel\masaha worktree move C:\Users\basel\masaha-design    C:\dev\masaha\design
git -C C:\Users\basel\masaha worktree move C:\Users\basel\masaha-design-b  C:\dev\masaha\design-b
git -C C:\Users\basel\masaha worktree list
```
**Check:** the list shows the three new paths with the same heads; in each, `git status --short` as recorded.
If `worktree move` refuses (a lock, an open file), stop: find the process, do not force.

## 5. Phase 2 — the main worktree

```powershell
Move-Item C:\Users\basel\masaha C:\dev\masaha\app
git -C C:\dev\masaha\app worktree repair C:\dev\masaha\app-b C:\dev\masaha\design C:\dev\masaha\design-b
git -C C:\dev\masaha\app worktree list
```
**Check:** four entries, new paths, same heads; `git -C <each> status` works (not "not a git repository");
`.git\worktrees\*\gitdir` all name `C:/dev/masaha/...`; each linked `.git` file names `C:/dev/masaha/app/.git/...`.
`.env` files and `apps\api\.storage\` present (compare with the backup listing).

## 6. Phase 3 — the junctions

In `app` and `app-b` only: `npm ci` (VS Code closed — it is safe then; it installs exactly the lockfile), then
`Get-ChildItem node_modules\@masaha -Force | Select Name,LinkType,Target`: every target must be **inside the
same worktree's new path**. The design worktrees get no `node_modules`. Then in `app`
and `app-b`: `npm run build -w @masaha/shared` and `npx prisma generate` (from `apps/api`) if the client is ignored.

## 7. Phase 4 — prove the apps still work

In `app` and in `app-b` (one at a time): `npm run lint`, `npm run typecheck`, `npm run test:unit`; one focused
API test file (`npm run test:api -w @masaha/api -- src/modules/packages/packages.api.test.ts`) after
`docker start masaha-postgres-1`; `npm run dev -w @masaha/api` → `GET /health` `"db":"up"` on its port, then
stop it by PID and check the port is free. In `design`: serve the prototype once
(`python -m http.server 54xx --directory docs/design/prototype`), open a page, stop it.
**Any red → stop** (a red here is the migration's, never "flaky").

## 8. Phase 5 — the workspace (cross-volume: copy, verify, then switch)

1. `robocopy D:\masahaWorkspace C:\dev\masaha\workspace /E /COPY:DAT /DCOPY:DAT /R:1 /W:1 /XJ` (includes `.git`).
2. Verify: same file count and SHA-256 of every file (a Python script that walks both trees); `git -C
   C:\dev\masaha\workspace status` clean and `git log -1` equal to D's.
3. Rename the old one: `Rename-Item D:\masahaWorkspace masahaWorkspace.OLD-<date>` (never written again;
   deleted at the end of the sitting, §10).
4. **Rewrite the active files' paths** (§1.5) with one script, in this order (longest first):
   `C:\Users\basel\masaha-design-b` → `C:\dev\masaha\design-b`; `C:\Users\basel\masaha-design` →
   `C:\dev\masaha\design`; `C:\Users\basel\masaha-b` → `C:\dev\masaha\app-b`; `C:\Users\basel\masaha` →
   `C:\dev\masaha\app`; `D:\masahaWorkspace` → `C:\dev\masaha\workspace` — both `\` and `/` spellings; skip
   `.git`, `_DONE`, `REPORT`, `LOGS`, `shots`, `_SHARED\ARCHIVE_*`, `_SHARED\HANDOFFS`, `_SHARED\MIGRATION`,
   `_superseded`, `_aborted`. **First a dry run** listing every file and count; the supervisor reads it;
   then apply (UTF-8, keep a BOM only where one was, LF/CRLF as found); then a scan must find **zero** old paths
   in the active set. Commit in the workspace repo: «paths moved to C:\dev\masaha (migration)», push.
5. The backup task: edit `snapshot.ps1`'s `Set-Location`; recreate the task with the new path
   (`schtasks /Create /TN masaha-workspace-snapshot /TR "powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\dev\masaha\workspace\_SHARED\snapshot.ps1" /SC DAILY /ST 23:00 /F`); run it once by hand; check the log.

## 9. Phase 6 — Claude Code, VS Code and the habits

1. **Memories (two only):** copy `c--Users-basel-masaha\memory\` → the key of `C:\dev\masaha\app`, and
   `C--Users-basel-masaha-b\memory\` → the key of `C:\dev\masaha\app-b` (**check the exact key** Claude
   Code creates: open it once in the new folder, `/memory`, and see the folder it names; copy there). Then
   update the memory files that name old paths (`prompt-folders`, `workspace-backup`, `two-workers`,
   `worktree-databases`, `task-workers`, `pr-screenshots`, others found by a scan) — wording only.
2. `C:\Users\basel\.claude\settings.json`: the permission rules naming `C:\Users\basel\masaha` get the new path
   (a copy first; only path strings change).
3. Launch lines change: `claude --add-dir C:\dev\masaha\workspace` from `C:\dev\masaha\app` (or `app-b`); Kilo
   and OpenCode open in `C:\dev\masaha\design`; VS Code opens the new folders (old recent entries removed).
4. `CLAUDE.md` and the repository need no change (no absolute path). `docs/development/setup.md` names no
   absolute folder either — **check**; if it does, record it for the next item (no repository edit here).

## 10. Phase 7 — the final proof, then the clean-up

1. A scan of `C:\Users\basel` (top level), `D:\` and every active file finds no live use of an old path.
2. The owner opens each new folder in VS Code and the workers' launch lines work; one design review and one
   focused test run from the new paths.
3. **At the end of the same sitting**, once 1–2 pass and with the owner's word: delete
   `D:\masahaWorkspace.OLD-<date>` (the workspace is also on GitHub) and the empty old folders in
   `C:\Users\basel\`. The backup folder of §3.3 is deleted with them, or kept if the owner prefers.

## 11. Rollback (any phase)

Phases 1–2 are renames: reverse them (`git worktree move` back, `Move-Item` back) and `git worktree repair`.
Phase 3: `npm ci` again. Phase 5: the old workspace is intact until §10 — rename it back, restore
the task. Memories and settings: the zip of §3.3. Nothing is deleted before §10.

## 12. Report

`D:\masahaWorkspace\TASKS\MIGRATION_DEV\4_REPORT.md` (after §8, `C:\dev\masaha\workspace\TASKS\MIGRATION_DEV\4_REPORT.md`),
written as you go: each phase, each command, each check's output line, each stop.
