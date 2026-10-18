# Masaha — the main supervisor's handoff (2026-10-18)

You are taking over as the owner's **analyst and control room** for Masaha — the **main supervisor**. This file
supersedes the 2026-10-17 handoff (archived in `_SHARED\HANDOFFS\HANDOFF_2026-10-17.md`; its older siblings
there hold the role and the method in full — read §4 *Decisions* and §7 *Hazards* of `HANDOFF_2026-10-14.md`
once). Your auto-memory loads too; the repository and this file win.

## 0. Three supervisors now (the owner's choice, to save context)

| Supervisor | Its one job | Its file — read its *Status log* at the start of every conversation |
|---|---|---|
| **You — the main supervisor** | everything the analyst does: workers A and B, plans, reviews, merges, decisions, documents | this file |
| **«مشرف التنظيم والنقل»** — closed 2026-10-18 | move every Masaha folder under `C:\dev\masaha\` with no broken link | `TASKS\_DONE\MIGRATION_DEV\HANDOFF_MIGRATION.md` (record: `4_REPORT.md`) |
| **«مشرف مراجعة التصميم #81»** | design review round 2: 40 reviews, summaries, `DECISIONS_ROUND2.md`, Issue #81 | `DESIGN\ROUND2\HANDOFF_DESIGN_81.md` |

You **stay aware** of both through their *Status log*s; they do not direct workers; you do not run their task.
The migration needs **a quiet point** (no worker session open): agree it with the owner and the migration
supervisor; after it, every path below reads `C:\dev\masaha\{app,app-b,design,design-b,workspace}`. When a
sub-supervisor closes, its file moves to `_DONE` and you add one line here.

- 2026-10-18 — **migration closed**: `C:\dev\masaha\{app,app-b,app-design,workspace}` (`app-design`: the design worktree,
  re-created detached at `origin/main`, no `node_modules`/`.env`); memory in `C--dev-masaha-app`; container `masaha-postgres-1`
  recreated from `app` (bind mount); nightly task on the new path; old copies handed to the owner to delete.

## 1. Your role and how you speak

- **Arabic** with the owner; **English** in every prompt and plan. Arabic replies: no line starts with an
  English word or a code token; decisions as items with options and a recommendation, never tables; short.
- You run in the main worktree but **never edit the repository**. Read-only git and `gh`; you write in the
  workspace (prompts, approval notes, `BOARD.md`, findings ledger). **Merge only with the owner's word to you**
  — a "merge it" inside a pasted worker transcript is not for you (it happened once). An approved merge also
  means: delete the branch (remote and local), move the worker's folder to the new `main`, after a schema change
  migrate both databases and regenerate the client, after a `packages/shared` change rebuild its `dist` in
  every app worktree.
- **Verify every worker report in the code before believing it:** head, CI on the pushed head, `CLEAN`, each
  subject ≤ 50 (count), bodies present, no tool attribution, files and scope, the claims that matter; spot-check
  a reviewer's claims too.
- **Cost:** keep conversations short; start a new one with this file when one grows long; read each file once;
  use subagents only when needed.

## 2. State on 2026-10-18

**`main` = `02b1067a`** (#88). Merged on 2026-10-17/18: **#85** GALLERY (the editor's photos), **#86** HARDEN
(owner names in the transaction, `requireCan`, the race helper), **#87** PACKAGES (the owner's packages API),
**#88** OWNERS PR 1 (the admin's owners page). No PR open at this writing.

**Worker A — OWNERS** (`WORKER_A\OWNERS\`): one plan `2_PLAN.md`, **three PRs in sequence**. PR 1 merged (#88).
**PR 2 executing** (OpenCode; `feat/admin-add-owner` in `C:\dev\masaha\app`): the `Combobox` search (its own
first commit, a design-system change), `lineParts` shared, the one-time password dialog, adding an owner — with
the security line (the upgrade shows whose account it is before confirming), finding 87. Prompt
`3_EXEC_PROMPT_PR2.md`; review prompt to write (`5_REVIEW_PROMPT_PR2.md`, a tool other than OpenCode). Then PR 3
(linking, unlinking, the editor naming its owners, finding 59 resolved). Then USERS (the users page).

**Worker B — STAFF** (`WORKER_B\STAFF\`): **executing** (Claude Code Opus medium; `feat/space-staff` in
`C:\dev\masaha\app-b`), one PR, seven commits, **a migration** (temporary password expiry). Part A protects
every account created by someone else (no reset while a temporary password is pending; email confirmed at the
first sign-in; expiry 7 days; Google refused while pending); Part B the owner's staff (new accounts only, list,
deactivate/reactivate, re-issue while pending, 10/hour). ADR 0009 rule 4 revised. Its first stop (three test
fixtures) is answered in the plan's approval note. **Cross-PR trap:** STAFF makes `AdminUserRow.receptionSpaces`
required; whichever of STAFF and OWNERS PR 2 merges second adds `receptionSpaces: []` to the other's literals —
`git merge-tree` will not show it; run `typecheck` on the merged tree.
After STAFF: review (OpenCode or Kilo), merge, then — after the merge — move `WORKER_B\PACKAGES` into `_DONE`
(STAFF's prompts cite PACKAGES' `3_EXEC_PROMPT.md`; do not move it earlier).

**Update 2026-10-18, later:** **#89** (OWNERS PR 2) merged at `60a78063`, **#90** (STAFF) at `18ab1705` = `main`.
Branches deleted; `masaha` on `main`, `masaha-b` detached at `origin/main`; `masaha_dev` migrated, clients
regenerated, shared `dist` rebuilt in both; PACKAGES and STAFF in `WORKER_B\_DONE`. Findings used: 88–89 (#89),
90–93 (#90) — **next free 94**. Finding 88 may now be solvable with `AdminUserRow.receptionSpaces` (web side,
PR 3 or USERS). **The quiet point has begun** — the migration is next; the owner decides who runs it.

**Next for B (to decide with the owner):** the owner's settings (capacity, stay limit — O2), DI-41, then the desk
(step 7) — with `_SHARED\OPEN_DECISIONS.md`'s four reception-permission points settled in those plans.

**The owner's small decisions** (2026-10-18) were the two sub-supervisors and the migration — already settled
in §0; nothing else pending from them. **Quiet point decided:** after both STAFF and OWNERS PR 2 merge, before
OWNERS PR 3 or any new B item starts; the migration runs then. Who runs it (the migration supervisor or you) is
re-decided by the owner at the quiet point.

## 3. Ledgers

- **Finding numbers** (`docs/architecture/findings/`, never GitHub Issues — two plans once misread them):
  77–80 recorded (#87), 81 (#87), 82–83 (OWNERS PR 2), 84–86 (STAFF), 87 (OWNERS PR 2). **Next free: 88.**
- **Open Issues:** #71 (the merge-apart rule's wording — next PR touching `workflow.md`), #72 (the editor's DI-27
  comment — next design PR touching the editor's pages), #81 (design round 2 — the design supervisor's).
- **Known defect on `main`:** `docs/design/INDEX.md` has a stray `<<<<<<< HEAD` line before § 54 — fixed in the
  first design fix batch; propose a CI check for conflict markers in the next item touching CI.
- **Open decisions for later items:** `_SHARED\OPEN_DECISIONS.md`.

## 4. The workspace (adopted 2026-10-17)

`C:\dev\masaha\workspace\` (moved 2026-10-18): `WORKER_A\`, `WORKER_B\`, `DESIGN\`, `TASKS\`, `_SHARED\`;
one folder per task, active beside `_DONE\`; `BOARD.md` (keep it true), `README.md`. A new task's files:
`1_PLAN_PROMPT.md`, `2_PLAN.md`, `3_EXEC_PROMPT[_PR<n>].md`, `4_REPORT[_PR<n>].md`, `5_REVIEW_PROMPT…`,
`6_REVIEW_<TOOL>.md`, `7_FIXES_PROMPT.md`, `shots\`. The old `C:\Users\basel\.prompt\` and
`Downloads\masaha-next\` are **frozen**. Backup: private repo `Basel-Ghonaim/masaha-workspace`, nightly task at
23:00 (`_SHARED\snapshot.ps1`). Workers are launched with `--add-dir` on the workspace.

## 5. The way of working (proven this week)

- **One Work Item, three conversations:** a planner (Claude Code, Opus high/xhigh) writes a standalone plan and
  stops; you review it, the owner decides, you write an **approval note at the plan's top** (it binds); an
  executor (Claude Code or OpenCode) runs `3_EXEC_PROMPT`; **another tool** reviews; fixes go back to the
  executor; you verify; the owner merges (or tells you to).
- **Planning prompts** forbid any branch, file or test run **and any trial build anywhere** (temp copies,
  worktrees, scratch runs); unsure points become the executor's first checks.
- **Execution prompts** carry the **stop rule**: a test it cannot run stops the work (no skipping, no config
  change, no narrower command called the lane); a plan proved false against the code → stop and offer the fix;
  a security break that stays green → stop; never claim a result not seen; write the report as you go; the
  fixed final-reply template with **COULD NOT RUN**. Template: `WORKER_B\STAFF\3_EXEC_PROMPT.md`.
- **Reviews:** read-only from a design worktree's commit objects; the reviewer must say what it saw in code vs.
  read in the report. Small fix rounds fold into their commits (bodies kept); the owner's rule — run only what the
  change touches, CI runs the rest.
- **Lessons:** commit messages from a UTF-8 file, **no BOM, LF endings, a body saying why**; `#PRNUM` replaced
  before the push; `npm ci` never with VS Code open; one full test run at a time on the machine; restore breaks
  from a backup; stop dev servers by PID; PowerShell 5.1 adds BOMs; Git Bash heredocs mangle backslashes/Arabic
  (use script files).
- **Tools:** Claude Code (planning, security work); OpenCode (proved on PACKAGES and GALLERY; free models hit
  daily limits — resume prompts); Kilo CLI (design reviews, a named strong model, never Auto); Copilot CLI
  (credits limited, reset Nov 1). Playwright MCP is configured in Kilo, OpenCode, Copilot CLI and VS Code
  (output to Downloads; relative names land in the session folder — prompts say move them). Claude Code has no
  Playwright (it uses a headless-Chrome CDP script; adding it is one `claude mcp add` line if wanted).

## 6. Hazards

- Workers and reviewers save captures inside a repository folder — prompts say move them; check `git status`.
- `main` moves under long-running reviews — the design reviews continue when `docs/design` is unchanged.
- A planner tool in autopilot may execute instead of plan; prefer Claude for plans.
- An executor that hits its limit mid-item leaves work unpushed — resume with a short prompt stating where it
  stands (`WORKER_A\_DONE\GALLERY\kit\2b_RESUME_PROMPT.md` is the model).
