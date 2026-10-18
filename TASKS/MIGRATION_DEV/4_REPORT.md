# MIGRATION_DEV — report

Written as the work goes, by the organisation and migration supervisor. Every check line is copied from output seen.

## Owner's amendments in this sitting (2026-10-18)

- `masaha-design` and `masaha-design-b` are temporary: **not moved**. Checked: both heads on `origin/main`; ignored
  files only `apps/api/src/generated/` — nothing is lost. The **owner** removes them (`git worktree remove`) before
  Phase 1; the supervisor never deletes.
- `masaha-b` **is moved** (owner's word, 17:30).
- Memories: only the main worktree's and `masaha-b`'s. Found: `c--Users-basel-masaha\memory\` has 35 files;
  `C--Users-basel-masaha-b\` has **no `memory\` folder** (transcripts only). Both keys are backed up whole anyway.
- Consequence for later phases: `node_modules` deleted in `masaha` and `masaha-b` only; Phase 1 moves `masaha-b`
  only; the design checks of Phases 4 and 7 are dropped.

## Quiet point (checked 17:20–17:25)

- VS Code closed by the owner; `opencode serve` stopped by the owner. Check: no `Code`, `node`, `opencode`,
  `codex`, `copilot`, `python`, `docker` CLI process left. Only Claude desktop sessions in `C:\Users\basel`
  (this one and two idle side chats).
- Ports 3320/3321/5320/5321 and 54xx: nothing listening.

## Phase 0 — snapshot and record (2026-10-18)

### 0.1 Snapshot and task

```
== before: 87070f5 snapshot 2026-10-18
exit=0
== after:  ae869df snapshot 2026-10-18
== status count: 0
== remote main: ae869dfea0b33e916975e29c00a4f54e674742c1	refs/heads/main
2026-10-18 17:25 committed and pushed ae869df
SUCCESS: The parameters of scheduled task "masaha-workspace-snapshot" have been changed.
Status:        Disabled
```

### 0.2 Records

```
worktree C:/Users/basel/masaha
HEAD 18ab1705149773bd05f2f7349ef341e33d175ca3
branch refs/heads/main

worktree C:/Users/basel/masaha-b
HEAD 18ab1705149773bd05f2f7349ef341e33d175ca3
detached

worktree C:/Users/basel/masaha-design
HEAD 02b1067a136d3c86378b3da60937c5f51124dc5b
detached

worktree C:/Users/basel/masaha-design-b
HEAD 93f152fe70f0b17e3e26a76fd7fa7fd7546ba75f
detached

C:\Users\basel\masaha | branch=main | status=0 | stash=0
C:\Users\basel\masaha-b | branch= | status=0 | stash=0
C:\Users\basel\masaha-design | branch= | status=0 | stash=0
C:\Users\basel\masaha-design-b | branch= | status=0 | stash=0
open PRs (Basel-Ghonaim/masaha): prcount=0
```

Also present (recorded only, nothing to do): local branch `pr88` in the main repo; remote branch
`feat/admin-owners` at `e4e13e9`. `origin/main` = `18ab1705` (= #90's merge commit).

### 0.3 Backup — `C:\dev-migration-backup\2026-10-18\`

Made by a Python script (copies only; every file SHA-256 checked against its source; each zip re-read and every
member hash-checked). `MANIFEST.json` in the folder lists every file with its hash.

```
verified file copies: 46
verified zip: c--Users-basel-masaha.zip members=334 MB=187.4
verified zip: C--Users-basel-masaha-b.zip members=85 MB=32.6
memory files copied plain: 35
OK
```

Independent check (PowerShell `Get-FileHash`):

```
memory src=35 dst=35 diff=0
C--Users-basel-masaha-b.zip entries=85 memoryEntries=0
c--Users-basel-masaha.zip entries=334 memoryEntries=35
```

Contents: `worktrees\masaha\` (`apps\api\.env`, `apps\web\.env`, `.claude\settings.local.json`, `apps\api\.storage\`
4 files + `storage_listing.json`); `worktrees\masaha-b\` (`apps\api\.env`, `apps\web\.env`,
`.claude\settings.local.json`; no `.storage`); `claude\settings.json`; `claude\memory-plain\c--Users-basel-masaha\`
(35 files); the two key zips.

### 0.4 `node_modules` deleted — `masaha-b` then `masaha` (17:40)

Script `phase0_nm.ps1`: lists every reparse point under `node_modules` (stops if any but the three `@masaha`
junctions), unlinks each junction with `rmdir` (link only) and counts the target's files before/after, checks
`git ls-files --deleted`, then `rmdir /s /q node_modules`. Nested `apps\*\node_modules` hold no link; left as
the plan says (root only).

```
== C:\Users\basel\masaha-b
reparse points under node_modules: 3
unlinked ...\node_modules\@masaha\api ; target C:\Users\basel\masaha-b\apps\api files 589 -> 589
unlinked ...\node_modules\@masaha\shared ; target C:\Users\basel\masaha-b\packages\shared files 123 -> 123
unlinked ...\node_modules\@masaha\web ; target C:\Users\basel\masaha-b\apps\web files 1398 -> 1398
after unlink: git status lines=0 deleted tracked=0
node_modules exists: False
final: tracked=2032->2032 git status lines=0 deleted tracked=0
OK
== C:\Users\basel\masaha
reparse points under node_modules: 3
unlinked ...\node_modules\@masaha\api ; target C:\Users\basel\masaha\apps\api files 603 -> 603
unlinked ...\node_modules\@masaha\shared ; target C:\Users\basel\masaha\packages\shared files 123 -> 123
unlinked ...\node_modules\@masaha\web ; target C:\Users\basel\masaha\apps\web files 1456 -> 1456
after unlink: git status lines=0 deleted tracked=0
node_modules exists: False
final: tracked=2032->2032 git status lines=0 deleted tracked=0
OK
```

`.env` (both app worktrees) and `masaha\apps\api\.storage` still present. Design worktrees untouched; their
junctions point inside themselves (`C:\Users\basel\masaha-design*\...`), so the owner's `git worktree remove`
cannot reach another worktree.

**Phase 0 done.** Phase 1 waits for the owner's word.

## Phase 1 — the linked worktree (2026-10-18, 17:50)

Before: owner removed `masaha-design` and `masaha-design-b` by hand. Checked: both folders gone; `.git\worktrees\`
holds only `masaha-b`; `worktree list` shows two entries; main and `masaha-b` clean at `18ab1705`; no
Code/node/opencode process; `C:\dev` absent.

```
New-Item -ItemType Directory C:\dev\masaha          -> C:\dev\masaha
git -C C:\Users\basel\masaha worktree move C:\Users\basel\masaha-b C:\dev\masaha\app-b   -> exit=0
```

Checks:

```
C:/Users/basel/masaha 18ab1705 [main]
C:/dev/masaha/app-b   18ab1705 (detached HEAD)
== old path exists: False
== b: head=18ab1705149773bd05f2f7349ef341e33d175ca3 status=0 deleted=0 tracked=2032
== b .git file: gitdir: C:/Users/basel/masaha/.git/worktrees/masaha-b
== main gitdir for b: C:/dev/masaha/app-b/.git
apps\api\.env exists=True sameAsBackup=True
apps\web\.env exists=True sameAsBackup=True
.claude\settings.local.json exists=True sameAsBackup=True
== main: head=18ab1705149773bd05f2f7349ef341e33d175ca3 status=0 deleted=0
== memory untouched: 35
```

(One check command ended with exit 255: `Select-Object -First 3` cut git's output pipe; re-run untruncated from
`C:\dev\masaha\app-b`: same two entries, `exit=0`.) The metadata folder keeps its name `worktrees\masaha-b` —
normal for `git worktree move`.

**Phase 1 done.** Phase 2 waits for the owner's word.

## Phase 2 — the main worktree (2026-10-18, 18:00)

Pre-check: no Code/node/opencode/python/git process; main clean at `18ab1705`, no stash, 2032 tracked; no
`index.lock`; no reparse point in the tree (outside `.git`); target absent; this session's cwd `C:\Users\basel`.

```
before: files=4622 bytes=155111809
Move-Item -LiteralPath C:\Users\basel\masaha -Destination C:\dev\masaha\app   -> moved
after:  files=4622 bytes=155111809
old path exists: False
git -C C:\dev\masaha\app worktree repair C:\dev\masaha\app-b
repair: .git file broken: C:/dev/masaha/app-b      (git's note on what it fixed)
exit=0
```

Checks:

```
== worktree list (from app)
C:/dev/masaha/app   18ab1705 [main]
C:/dev/masaha/app-b 18ab1705 (detached HEAD)
== worktree list (from app-b)   — same two lines, exit=0
== b .git file: gitdir: C:/dev/masaha/app/.git/worktrees/masaha-b
masaha-b: C:/dev/masaha/app-b/.git
== C:\dev\masaha\app head=18ab1705… branch=main status=0 deleted=0 tracked=2032
== C:\dev\masaha\app-b head=18ab1705… branch= status=0 deleted=0 tracked=2032
.env ×2, settings.local.json — app and app-b: same=True (6 of 6, against the backup)
storage files ok=4 of 4
origin = https://github.com/Basel-Ghonaim/masaha.git ; origin/main=18ab1705…
git fsck --no-dangling: exit=0
memory untouched: 35
C:\Users\basel masaha* folders left: none
```

**Phase 2 done.** Phase 3 (`npm ci` in `app` and `app-b`) waits for the owner's word.

## Phase 3 — the junctions (2026-10-18, 18:10)

Pre-check: node v24.19.0, npm 11.17.0; no Code/node/tsx process; `package-lock.json` identical in `app` and
`app-b`; `apps/api` has `postinstall: prisma generate`; `apps/api/src/generated/` is ignored (`.gitignore:10`).
Check script `phase3_links.ps1`: lists `node_modules\@masaha`, then every reparse point under the root and the
nested `node_modules` folders, and counts any whose target is outside the worktree.

### `C:\dev\masaha\app`

```
npm ci -> exit=0  seconds=38 ; added 696 packages, and audited 700 packages in 38s
  api [Junction] -> C:\dev\masaha\app\apps\api
  shared [Junction] -> C:\dev\masaha\app\packages\shared
  web [Junction] -> C:\dev\masaha\app\apps\web
reparse points: 3 ; pointing outside C:\dev\masaha\app: 0
git status lines: 0 ; deleted tracked: 0
npm run build -w @masaha/shared -> build exit=0
npx prisma generate (apps/api) -> ✔ Generated Prisma Client (7.10.0) to .\src\generated\prisma ; prisma exit=0
git status lines: 0
```

### `C:\dev\masaha\app-b`

```
npm ci -> exit=0  seconds=41 ; added 696 packages, and audited 700 packages in 40s
  api [Junction] -> C:\dev\masaha\app-b\apps\api
  shared [Junction] -> C:\dev\masaha\app-b\packages\shared
  web [Junction] -> C:\dev\masaha\app-b\apps\web
reparse points: 3 ; pointing outside C:\dev\masaha\app-b: 0
git status lines: 0 ; deleted tracked: 0
npm run build -w @masaha/shared -> build exit=0
npx prisma generate (apps/api) -> ✔ Generated Prisma Client (7.10.0) to .\src\generated\prisma ; prisma exit=0
```

After both: `app` and `app-b` status=0 at `18ab1705`; no node/tsx process left; memory 35 untouched.
Recorded only (not the migration's): `npm ci` reports "10 vulnerabilities (7 high, 3 critical)" from the
lockfile as it is on `main`; Prisma offers 8.0.0-rc — nothing changed.

**Phase 3 done.** Phase 4 (lint, typecheck, unit, one API test, `/health`) waits for the owner's word.

## Phase 4 — prove the apps still work (2026-10-18) — **STOPPED**

Pre-check: `app` api `.env` PORT=3320, db `masaha_dev`/`masaha_test`; `app-b` PORT=3321, db
`masaha_b_dev`/`masaha_b_test`; nothing listening on 3320/3321/5320/5321.

### `C:\dev\masaha\app` — static checks (green)

```
== lint exit=0 seconds=71
== typecheck exit=0 seconds=23
== test:unit exit=0 seconds=37
   Tests  216 passed (216)
   Test Files  45 passed (45) ; Tests  743 passed (743)
   Test Files  80 passed (80) ; Tests  829 passed (829)
```

### Stop: the database container does not start

```
docker ps -a: masaha-postgres-1 Exited (127) 35 minutes ago
docker start masaha-postgres-1 -> start exit=1
Error response from daemon: ... error mounting "/run/desktop/mnt/host/c/Users/basel/masaha/docker/postgres/create-test-database.sql"
to rootfs at "/docker-entrypoint-initdb.d/create-test-database.sql": ... not a directory
```

Cause: the container carries a **bind mount with the old absolute path** —
`C:\Users\basel\masaha\docker\postgres\create-test-database.sql -> /docker-entrypoint-initdb.d/...` (from
`./docker/postgres/...` in `docker-compose.yml`, resolved when the container was created). The plan's §1.4 ("the
`working_dir` label … harmless") missed it. The data volume `masaha_masaha-pgdata` is untouched (a named volume,
not the folder). Docker Desktop also **re-created empty folders at the old path** at 17:42:47 —
`C:\Users\basel\masaha\docker\postgres\create-test-database.sql\` (three empty directories) — to add to the
owner's §10 list; not touched. Last clean shutdown of Postgres: 2026-10-18 14:08:35 UTC ("database system is shut
down"). Timing note: the Phase 2 move happened ≈17:42 (the "18:00" above is approximate).

Waiting for the owner's decision; `app-b` not started.

### Owner's decision (17:50 local): back up the volume, recreate the container from `app` with compose

Volume backup — `C:\dev-migration-backup\2026-10-18\docker\masaha_masaha-pgdata.tar` (local image
`postgres:18-alpine`, `--network none`, volume mounted `:ro`; the container was stopped, last shutdown clean):

```
files in volume: 3018 ; files in tar: 3018
sha256 of all source files : ec77af2e66fb894c3510d9f8ec3339538b9818250aa6d38fd9140126f8091a2f
sha256 of all files re-extracted from the tar : ec77af2e66fb894c3510d9f8ec3339538b9818250aa6d38fd9140126f8091a2f
tar MB=184.8 sha256=6170CDBAE1787AFD7C2F50A8E507F91F23A24C283D15A57217555ED2FD56887D
```

Recreate (from `C:\dev\masaha\app`; `docker compose config` first: bind source
`C:\dev\masaha\app\docker\postgres\create-test-database.sql`, volume `masaha_masaha-pgdata`):

```
docker compose up -d --wait postgres
 Container masaha-postgres-1 Recreate / Recreated / Started / Healthy ; exit=0
masaha-postgres-1 Up 3 seconds (healthy) 0.0.0.0:5433->5432/tcp
bind | /run/desktop/mnt/host/c/dev/masaha/app/docker/postgres/create-test-database.sql -> /docker-entrypoint-initdb.d/...
volume | masaha_masaha-pgdata -> /var/lib/postgresql
working_dir label: C:\dev\masaha\app
PostgreSQL Database directory appears to contain a database; Skipping initialization
database system was shut down at 2026-10-18 14:08:35 UTC
database system is ready to accept connections
```

The four databases (repo has 18 migrations):

```
masaha_dev    tables=33 applied=18 live rows=309 size=11 MB
masaha_test   tables=32 applied=12 live rows=0   size=13 MB   (behind before the move; the API lane's
              global-setup runs `prisma migrate deploy` on it — after the test: applied=18)
masaha_b_dev  tables=33 applied=18 live rows=149 size=11 MB
masaha_b_test tables=33 applied=18 live rows=29  size=13 MB
masaha_dev   : refresh_tokens=212, rate_limits=43, audit_logs=26, users=9, space_managers=8, space_settings=4
masaha_b_dev : rate_limits=46, audit_logs=34, refresh_tokens=17, users=14, space_managers=10, spaces=7
```

### `C:\dev\masaha\app` — API and health (green)

```
npm run test:api -w @masaha/api -- src/modules/packages/packages.api.test.ts -> exit=0 ; Test Files 1 passed (1) ; Tests 17 passed (17)
GET /health on 3320: {"status":"ok","db":"up","timestamp":"2026-10-18T14:50:53.034Z"}
listener PID 19808 stopped (taskkill /T) ; port 3320 free: True ; stray node/tsx: 0
```

### `C:\dev\masaha\app-b` (green)

```
== lint exit=0 seconds=76
== typecheck exit=0 seconds=23
== test:unit exit=0 seconds=38 ; Tests 216 passed (216) ; Test Files 45 passed (45), Tests 743 passed (743) ; Test Files 80 passed (80), Tests 829 passed (829)
test:api packages.api.test.ts -> exit=0 ; Test Files 1 passed (1) ; Tests 17 passed (17)
GET /health on 3321: {"status":"ok","db":"up","timestamp":"2026-10-18T14:53:54.094Z"}
listener PID 28320 stopped ; port 3321 free: True ; stray node/tsx: 0
```

After: no node/tsx process; `app` and `app-b` status=0; memory 35 untouched. Design check dropped (owner's
amendment). For the owner's §10 list: the three empty folders Docker created under `C:\Users\basel\masaha\`.
For the next item (not here): `docs/development/setup.md` could warn that moving the folder needs the container
recreated (bind mount).

**Phase 4 done.** Phase 5 (the workspace) waits for the owner's word.

## Phase 5 — the workspace (2026-10-18, from 17:55)

From here the report is written **only** in `C:\dev\masaha\workspace\TASKS\MIGRATION_DEV\` (the old copy stays as
it was at `c9ad45c`).

Pre-check: `D:\masahaWorkspace` 2479 files, 243.8 MB, no reparse point; pending only this task's two files →
`snapshot.ps1` by hand: `exit=0`, `c9ad45c snapshot 2026-10-18`, status=0, remote main = `c9ad45cd…`; task still
`Disabled`.

### 5.1 Copy

```
robocopy D:\masahaWorkspace C:\dev\masaha\workspace /E /COPY:DAT /DCOPY:DAT /R:1 /W:1 /XJ /NP  -> exit=1 (files copied, no failure)
    Dirs :       338       338         0         0         0         0
   Files :      2485      2485         0         0         0         0
   Bytes :  243.83 m  243.83 m         0         0         0         0
```

### 5.2 Verify (Python, every file's size and SHA-256; directory sets)

```
files: src=2485 dst=2485
dirs:  src=338 dst=338
only in src: 0 ; only in dst: 0 ; hash/size differ: 0
total bytes: src=255676394 dst=255676394
IDENTICAL
new: log=c9ad45c snapshot 2026-10-18 status=0 ; old: log=c9ad45c ; fsck exit=0
remote: git@github.com:Basel-Ghonaim/masaha-workspace.git
```

### 5.4 Dry run of the path rewrite (nothing written) — full listing in `5_DRYRUN.md`

```
DRY RUN: files changed=73 replacements=439 design-b=1 design=101 app-b=7 app=14 workspace=316
skipped records hits: DESIGN=212, TASKS=71, WORKER_A=44, WORKER_B=112, _SHARED\ARCHIVE_2026-10-08=75, _SHARED\HANDOFFS=19, _SHARED\MIGRATION=2166
other spellings: (none)
undecodable with masaha: 10 (9 Chrome cache files under shots\_aborted, 1 non-UTF-8 file under WORKER_B\_DONE — all skipped areas)
encodings / line endings of changed files: utf-8/CRLF=1, utf-8/LF=72
```

Supervisor's reading, for the owner's decision:
- Added to the skip list: `TASKS\MIGRATION_DEV` (its plan and report are the record of old → new).
- Two lines become self-contradictory and need a wording fix after the apply: `HANDOFF.md` L87 ("… (soon
  `C:\dev\masaha\workspace\`)") and `DESIGN\ROUND2\HANDOFF_DESIGN_81.md` L6–8 (the "after the move, … →" sentence).
- Two finished reports would be rewritten: `WORKER_A\OWNERS\4_REPORT_PR1.md`, `4_REPORT_PR2.md` — records.
- 102 design paths would point to `C:\dev\masaha\design(-b)`, which does not exist now (removed by the owner).

Waiting for the owner. Step 5.3 (rename the old copy) not done.

### Owner's decision on the dry run: "موافق على توصياتك" (all four recommendations)

`TASKS\MIGRATION_DEV` stays skipped; the two contradictory lines are fixed by hand; `WORKER_A\OWNERS\4_REPORT_PR1.md`
and `4_REPORT_PR2.md` are skipped as records; design paths are rewritten to `C:\dev\masaha\design(-b)`.

### 5.3 Rename the old copy (no delete)

```
old last: c9ad45c snapshot 2026-10-18 status=0
Rename-Item -LiteralPath D:\masahaWorkspace -NewName masahaWorkspace.OLD-2026-10-18 -> renamed
D:\ now: MASAHA, masahaWorkspace.OLD-2026-10-18 ; old copy files: 2485
```

### 5.4 Apply

```
second dry run: files changed=71 replacements=434 design-b=1 design=101 app-b=7 app=12 workspace=313   (= 439 − 5, the two reports)
APPLIED: files changed=71 replacements=434 ... residual: 0
independent re-run of the dry run after apply: files changed=0 replacements=0
git diff --numstat: every rewritten file adds = dels (line-level only); unequal: only this task's 4_REPORT.md and
HANDOFF_MIGRATION.md (appends); CRLF file DESIGN/ROUND2/REMAINING_AR.md 33/33 (line endings kept); no BOM file touched
second-opinion scan (Select-String 'Users[\/]+basel[\/]+masaha' | 'masahaWorkspace', 85 active files): 1 hit —
  README.md:1 "# masahaWorkspace" (the repository's title, not a path; left)
```

Hand fixes (wording only): `HANDOFF.md` L87 "(soon `C:\dev\masaha\workspace\`)" → "(moved 2026-10-18)";
`DESIGN\ROUND2\HANDOFF_DESIGN_81.md` L6–8 → "moved these folders on 2026-10-18 (every path below reads
`C:\dev\masaha\…`; the design worktree was removed — re-create it at `C:\dev\masaha\design` from `origin/main` when a
review needs it)".

```
git commit -F commit_msg.txt -> commit exit=0 ; git push -> push exit=0
local: ec6bffc paths moved to C:\dev\masaha (migration) ; remote: ec6bffc57a36b949d13ebd04c0085bb73c3a03ee ; status=0
files in commit: 74
```

(A first `git commit -F -` failed — PowerShell passed the message as a pathspec; nothing committed or pushed; redone
with a message file.)

### 5.5 The nightly task

Old definition saved: `C:\dev-migration-backup\2026-10-18\task-masaha-workspace-snapshot.xml` (was: `-File
D:\masahaWorkspace\_SHARED\snapshot.ps1`, 23:00, InteractiveToken, Disabled). `snapshot.ps1`'s `Set-Location`
now reads `C:\dev\masaha\workspace` (rewritten in 5.4).

```
schtasks /Create /TN masaha-workspace-snapshot /TR "powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\dev\masaha\workspace\_SHARED\snapshot.ps1" /SC DAILY /ST 23:00 /F
  -> SUCCESS ... create exit=0
new: args=-NoProfile -ExecutionPolicy Bypass -File C:\dev\masaha\workspace\_SHARED\snapshot.ps1 start=2026-10-18T23:00:00 daily=1 logon=InteractiveToken
schtasks /Run -> run exit=0 ; task: Status: Ready | Last Result: 0
new log tail: 2026-10-18 18:01 nothing to commit
old copy untouched: c9ad45c ; its log tail: 2026-10-18 17:55 committed and pushed c9ad45c
```

**Phase 5 done.** Phase 6 (memories, settings, launch lines) waits for the owner's word.

## Phase 6 — Claude Code, VS Code and the habits (2026-10-18, 18:10)

### 6.1 Memory (worker A only; worker B's key has no `memory\`)

New key: `C:\dev\masaha\app` → `C--dev-masaha-app` (Claude Code replaces `:` and `\` with `-`; same rule gives this
session's `C--Users-basel`; NTFS is case-insensitive, so the VS Code spelling `c--dev-masaha-app` is the same
folder). **Copied, not moved** — the old key stays as it is. To be confirmed by the owner in Phase 7 (`/memory`).

```
Copy-Item c--Users-basel-masaha\memory\* -> C--dev-masaha-app\memory\
src=35 new=35 backup=35
new vs src diff=0 ; new vs backup diff=0
```

Wording updated in the **new copy only** (same rewrite script; dry run read first):

```
DRY RUN: files changed=5 replacements=10 app-b=1 app=1 workspace=8 ; other: C:\Users\basel\masaha-readme ×1 (task-workers.md, a past worktree — left)
APPLIED: files changed=5 replacements=10 ... residual: 0
hand fix prompt-folders.md: "Workers writing to D: need" -> "Workers writing to the workspace need" (1 occurrence)
count still 35 ; old key's files hash-equal to the backup: True
```

Files: `MEMORY.md` (2 index lines), `pr-screenshots.md`, `prompt-folders.md`, `two-workers.md`, `workspace-backup.md`.

### 6.2 `C:\Users\basel\.claude\settings.json`

Fresh copy first: `C:\dev-migration-backup\2026-10-18\claude\settings.before-phase6.json` (same as Phase 0's).
No BOM, LF. Three rules, each found exactly once, path string only:

```
L24: "Bash(git -C /c/dev/masaha/app log --oneline -1)",
L25: "Bash(git -C /c/dev/masaha/app branch --show-current)",
L26: "Read(//c/dev/masaha/app/apps/api/**)",
json valid after write ; diff lines vs copy: 6 (3 out, 3 in)
```

Left: L20–21 name an old session's scratchpad (`c--Users-basel-masaha-api`), not a Masaha folder. The two
`.claude\settings.local.json` (in `app`, `app-b`) name no absolute path. `C:\Users\basel\.claude.json` has 15
old-path mentions — Claude Code's own per-folder state; not edited (a new folder gets its own entry when opened).

### 6.3 Launch lines (for the owner)

```
cd C:\dev\masaha\app   ; claude --add-dir C:\dev\masaha\workspace     (worker A)
cd C:\dev\masaha\app-b ; claude --add-dir C:\dev\masaha\workspace     (worker B)
```

Design reviews (Kilo/OpenCode): the design worktree was removed — re-create at `C:\dev\masaha\design` from
`origin/main` when needed. VS Code: open the new folders; remove the old recent entries (owner).

### 6.4 Repository

`docs/development/setup.md`: no absolute folder (scan for `X:\`, `Users\basel`, `/c/`: 0 hits). Recorded for the
next item (no repository edit here): moving the folder needs the Postgres container recreated (bind mount, Phase 4).

**Phase 6 done.** Phase 7 (final proof, then the list of old copies for the owner) waits for the owner's word.
