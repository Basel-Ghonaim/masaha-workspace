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
the path commit; the nightly task runs from the new path; memories copied and readable; the old copies deleted
at the end of the same sitting, with the owner's word. **The whole task is one sitting of one to two hours.** Then: `HANDOFF.md` (the main one) gets one line, this file
and the task move to `_DONE`, and your conversation ends.

## Status log (append one dated line per step; newest last)

- 2026-10-18 — created by the analyst; plan approved in principle; waiting for the owner's quiet point.
