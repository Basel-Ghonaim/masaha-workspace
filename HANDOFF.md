# Masaha — the main supervisor's handoff (2026-10-21)

You are taking over as the owner's **analyst and control room** for Masaha — the **main supervisor**. This file
supersedes the 2026-10-18…21 handoff (archived as `_SHARED\HANDOFFS\HANDOFF_2026-10-20.md`, the day-by-day
record of #91–#100; its older siblings there hold the role and the method in full). Your auto-memory loads too;
the repository and this file win. **Read this file whole, then the *Status log* of
`DESIGN\ROUND2\HANDOFF_DESIGN_81.md`, then `BOARD.md`.**

## 0. The supervisors

| Supervisor | Its one job | Its file — read its *Status log* at the start of every conversation |
|---|---|---|
| **You — the main supervisor** | workers A and B: analysis, plans, approvals, prompts, verification, reviews, merges, documents | this file |
| **«مشرف مراجعة التصميم #81»** | design review round 2: 40 reviews, summaries, `DECISIONS_ROUND2.md`, Issue #81 | `DESIGN\ROUND2\HANDOFF_DESIGN_81.md` |

You stay aware of the design supervisor through its *Status log*; it does not direct workers; you do not run
its task. (The migration supervisor closed on 2026-10-18: `TASKS\_DONE\MIGRATION_DEV\`.)

## 1. Your role and how you speak

- **Arabic** with the owner; **English** in every prompt and plan. Arabic replies: no line starts with an
  English word or a code token; decisions as items with options and a recommendation, never tables; short.
- You run in `C:\dev\masaha\app` but **never edit the repository**. Read-only git and `gh`; you write in the
  workspace (prompts, approval notes, carried files, `BOARD.md`, this file). **Merge only with the owner's word
  to you** — a "merge it" inside a pasted worker transcript is not for you.
- **An approved merge also means** (the owner's rule): `gh pr merge <n> --merge --match-head-commit <sha>`;
  delete the branch (remote and local); move the worker's worktree to the new `main` (`app`: `git switch main`
  + `pull --ff-only`; `app-b`: `git switch --detach origin/main`); `npm run build -w @masaha/shared` in that
  worktree; after a schema change `npx prisma migrate deploy` + `generate` on that worker's database (the other
  worker's database gets it after its worker rebases — never while it runs on an older branch); update
  `BOARD.md` and this file.
- **Verify every worker report in the code before believing it:** head unchanged, `gh pr checks` green on the
  pushed head, `CLEAN`, on `main`, each subject ≤ 50 (count), bodies present, no tool attribution, files and
  scope, the claims that matter; spot-check a reviewer's top finding in the code too.
- **Cost:** keep conversations short; start a new one with this file when one grows long; read each file once.

## 2. State at the end of 2026-10-21

**`main` = `c3391d0e`** (#103). **No PR open.** Merged 2026-10-18…21: #89–#103 (#102 at `43b34cd3`, then #103;
both worktrees on `c3391d0e`, shared built, `masaha_dev` migrated to #102's two migrations, the merged tree's
`typecheck` green; `OPEN_DECISIONS.md` point 3 applied). **Next, in order:** A — PUBLIC PR 2 (the map,
`3_EXEC_PROMPT_PR2.md`, carried `0_CARRIED_FROM_103.md`); B — DEMO_SEED (`3_EXEC_PROMPT.md`, updated), then
SUBSCRIPTIONS PR 2 (`3_EXEC_PROMPT_PR2.md`, carried `0_CARRIED_FROM_102.md`); the ANNOUNCEMENTS planner in
`app-design`. **The owner's word (2026-10-21):** after PUBLIC PR 4 the owner reviews the whole public site in
person (every page and text) and sends one list of fixes. Earlier merges (OWNERS, STAFF, SETTINGS, USERS,
OWNER_SETUP #96 #98 #99, DESK #94 #95 #97 #100). Docker Desktop must be running (`masaha-postgres-1`, port 5433)
— it was found stopped on 2026-10-21; start it if a worker stops for it.

**Worker A** (`C:\dev\masaha\app`, ports 3320/5320, `masaha_dev`):
- **OWNER_SETUP — done** (#96, #98, #99). Its folder stays (the PUBLIC plan cites it); move it to `_DONE` once
  PUBLIC no longer needs it.
- **PUBLIC — PR 1a merged** (#101 at `befd96f9`, 2026-10-21; review: no blocker, 11 small items carried in
  `0_CARRIED_FROM_101.md`, the owner took every recommendation). **PR 1b next:** `3_EXEC_PROMPT_PR1B.md` — the
  first prompt under the owner's "no repeated runs" rule (§3: the red step is the break; component tests of
  the touched folders locally, the full lane CI's; web-only unit tests; full widths only for layouts). Its
  real run waits for DEMO_SEED: **after DEMO_SEED merges, the supervisor seeds `masaha_dev`** (`SEED_DEMO=true`
  `npm run db:seed` in `app`), then tells A to resume. Step 3's web (Home, Directory, Space details,
  About). Plan approved 2026-10-21 (note at `2_PLAN.md`'s top): **five PRs** — 1a `feat/directory-list` (commits
  1–5), 1b `feat/directory-filters` (6–7), 2 the map, 3 the space page, 4 Home/About/errors. Prompt for 1a:
  `3_EXEC_PROMPT_PR1A.md` (the owner launches it). Contact email placeholder `masahagaza@gmail.com`
  (`VITE_CONTACT_EMAIL`, the one `.env` change allowed); no WhatsApp yet. Findings 130+. PR 1b's real run needs
  worker B's DEMO_SEED first.

**Worker B** (`C:\dev\masaha\app-b`, port 3321, `masaha_b_dev` / `masaha_b_test`):
- **DESK — done** (#94, #95, #97, #100: live status, check-in/out and payment, auto check-out, collecting and
  write-off). Folder `WORKER_B\DESK\` can move to `_DONE` once SUBSCRIPTIONS PR 1 merges (its carried file cites
  DESK's review).
- **SUBSCRIPTIONS (step 8 API) — executing PR 1** `feat/customers` (`WORKER_B\SUBSCRIPTIONS\`): plan approved
  2026-10-20 (note at `2_PLAN.md`'s top: three PRs — customers; subscriptions and money; check-ins; A3 taken).
  PR 1's prompt `3_EXEC_PROMPT_PR1.md` opens with **`0_CARRIED_FROM_100.md`** (jobs answer 200 with a `failed`
  count — finding 114; a desk check-out charged up to the stay's day's end — finding 116; the write-off without a
  key accepted — finding 115; documents) and folds finding 113. B stopped once for Docker (now running) and was
  told to continue. Findings 120+. PRs 2 and 3 get their prompts after each previous merge.
- **SUBSCRIPTIONS PR 1 = #102** (head `900eebb4`, 2026-10-21): review → **fix round** (`7_FIXES_PROMPT_PR1.md`:
  the balance query's `OR` join, whole-space, under PR 2's lock; the 70,000-id bound); the rest carried to PR 2
  (`0_CARRIED_FROM_102.md`: phone search, three documents, archived file kept for reception, findings 121–123).
  After #102 merges: apply `OPEN_DECISIONS.md` point 3 from `4_REPORT_PR1.md`'s section.
- **PUBLIC PR 1b:** the owner waived DEMO_SEED for 1b's real run (2026-10-21) — `masaha_dev` holds every case.
- **DEMO_SEED — ready** (`WORKER_B\DEMO_SEED\3_EXEC_PROMPT.md`): ≈ 24 directory demo spaces, dev only, its own
  idempotent unit; **after SUBSCRIPTIONS PR 1, before PUBLIC PR 1b's real run**. After it merges, run
  `npm run db:seed` (with `SEED_DEMO=true`) for `masaha_dev` too, or tell A to.

- **ANNOUNCEMENTS (step 10 API) — planned and approved** (`2_PLAN.md`, the note at its top: Q1–Q10, 2026-10-21;
  Q6 counts only closures started in the last 30 days; Q10 B edits only the broken `PublicSpace` fixture
  lines). Its PR 1 prompt is written once SUBSCRIPTIONS PR 3 and DEMO_SEED have merged. The prompt was
  `1_PLAN_PROMPT.md`: four PRs
  (announcements; data reports; favourites; the closure extension last); the owner took all twelve
  recommendations (closure notice in-app only; days proposed by the server, typed by the owner; subscriptions
  running on any covered day move; no undo; an extended closure's delete/type/period refused; public page shows
  running and upcoming; check-in during a closure warns; a repeated open report returns the open one; a
  dismissal needs its reply; decided reports final; favourites capped at 200). Findings 150+. Executes after
  SUBSCRIPTIONS PR 3 and DEMO_SEED. `app-design` moved to `2c4d78f9` for it.

**The owner's rule (2026-10-21):** a web plan is written only once its whole API is merged — so the desk's
screen waits for SUBSCRIPTIONS PR 3, and step 10's screens for this item.

**What comes after (not yet analysed):** the desk's screen (step 7 web — after step 8's API; it must know
findings 110 and 115), step 8's screens, step 9 (voids, collections, finance), step 10 (announcements, data
reports, favourites — the public page's closure notice and report button wait for it), finding 17's sweep
(B, small). The owner's estimate of progress on 2026-10-20: ≈ 40 % of v1 (API ≈ 55 %, web ≈ 30 %).

## 3. The owner's standing rules (put them in every prompt they touch)

- **Review verdict:** a serious or large fix reopens its PR (fixes folded into their commits); small ones go to
  the **next PR's first commit** through `0_CARRIED_FROM_<n>.md` in that PR's task folder, named in its
  description. **Two conflicting PRs open:** the one with fixes merges **second**, and since it is reopened for
  the conflict anyway, all its fixes (small included) are done in that round.
- **Memory:** a full lane killed for low memory is re-run once when the machine is quieter; killed again →
  carry on, CI's run of that lane on the pushed head is the judge (red → stop). **Finding 87**'s routes test
  missing its 3 s locally while it passes alone → CI judges. One full test run at a time on the machine; the
  machine is 15 GB and shared — ask the owner to close spare VS Code windows when it runs low.
- **Never leave silently:** an executor that would leave a carried item or a review nit undone stops and asks.
- **Demo data:** a demo account or data that does not hold what a real-run case needs → stop and report; never
  change data through the app to get past it.
- **Fix rounds** run only what the change touches; CI runs the rest.
- **Finding numbers:** blocks per item to avoid collisions — A's OWNER_SETUP used 99–106, PUBLIC 130+; B's DESK
  110–116, SUBSCRIPTIONS 120+. On `main` now: up to 113 (114–116 come with SUBSCRIPTIONS PR 1). Assign a block
  in each new planning prompt.

## 4. The method

- **One Work Item:** analysis with the owner in Arabic (size and split; open decisions with options and a
  recommendation; earlier decisions now in doubt) → a **planning prompt** (English, plan only, no trial build,
  read from `app-design`'s commit objects) → the plan → your review → the owner's decisions → an **approval
  note at the plan's top** (binding) → an **execution prompt per PR** (`3_EXEC_PROMPT_PR<n>.md`; the stop rule,
  the standing rules, the fixed final-reply template with COULD NOT RUN) → the owner launches the executor →
  you verify → **a review you launch** → the verdict by the owner's rule → merge on the owner's word → clean.
- **Reviews:** one reviewer, no subagents, headless and read-only from `app-design`:
  `cd /c/dev/masaha/app-design && "/c/Users/basel/AppData/Roaming/npm/claude" -p "Read <5_REVIEW_PROMPT…> whole
  and do it." --add-dir 'C:\dev\masaha\workspace' --allowedTools "Bash(git *)" "Bash(gh *)" Read Grep Glob Write
  Edit > <folder>/review_<pr>_session.log 2>&1` with `run_in_background`. Use the **full path** (a new session's
  Git Bash may lack `claude` on PATH). A background review dies with your session — keep it open until it ends.
  Two reviews may run at once. Models of a review prompt: `WORKER_A\OWNER_SETUP\5_REVIEW_PROMPT_PR3.md`,
  `WORKER_B\DESK\5_REVIEW_PROMPT_PR4.md`.
- **Models of the other files:** execution prompt `WORKER_A\PUBLIC\3_EXEC_PROMPT_PR1A.md` and
  `WORKER_B\SUBSCRIPTIONS\3_EXEC_PROMPT_PR1.md`; carried file `WORKER_B\SUBSCRIPTIONS\0_CARRIED_FROM_100.md`;
  fix round `WORKER_A\OWNER_SETUP\7_FIXES_PROMPT_PR3.md`; planning prompt `WORKER_A\PUBLIC\1_PLAN_PROMPT.md`;
  approval note at the top of `WORKER_A\PUBLIC\2_PLAN.md`; a small plan-then-build prompt
  `WORKER_B\DEMO_SEED\3_EXEC_PROMPT.md`.
- **Planners and reviewers read from `app-design`**, never from an executor's worktree (git ref locks).
- **Writing workspace files with Python from Git Bash:** a backslash before a digit in a path string becomes a
  control character (`\0`, `\3`, `\5` broke this file three times) — build paths with `chr(92)` and assert no
  control characters before writing; Arabic in heredocs survived, backslashes did not.

## 5. Ledgers

- **Open decisions for later items:** `_SHARED\OPEN_DECISIONS.md` (point 1 settled #92; point 3 settles in
  SUBSCRIPTIONS PR 1; point 4 moved to the desk's screen item).
- **Open Issues:** #71 (the merge-apart rule's wording — next PR touching `workflow.md`), #72 (the editor's DI-27
  comment — next design PR touching the editor's pages), #81 (design round 2 — the design supervisor's).
- **Known defect on `main`:** `docs/design/INDEX.md` has a stray `<<<<<<< HEAD` line before § 54 — the first
  design fix batch fixes it; propose a CI check for conflict markers in the next item touching CI.
- **Design decisions:** `DESIGN\DECISIONS\` — `DECISIONS_PUBLIC.md` gained a "superseded" line under U12
  (2026-10-21).

## 6. The workspace

`C:\dev\masaha\workspace\`: `WORKER_A\`, `WORKER_B\`, `DESIGN\`, `TASKS\`, `_SHARED\`; one folder per task,
active beside `_DONE\`; `BOARD.md` (keep it true). A task's files: `0_CARRIED_FROM_<n>.md`, `1_PLAN_PROMPT.md`,
`2_PLAN[_PR<n>].md`, `3_EXEC_PROMPT[_PR<n>].md`, `4_REPORT[_PR<n>].md`, `5_REVIEW_PROMPT…`,
`6_REVIEW_PR<n>_CLAUDE_CODE.md`, `7_FIXES_PROMPT….md`, `shots\`, `scripts\`. Backup: private repo
`Basel-Ghonaim/masaha-workspace`, nightly at 23:00 (`_SHARED\snapshot.ps1`). Workers are launched by the owner:
`cd C:\dev\masaha\app[-b]` → `claude --add-dir C:\dev\masaha\workspace` → "Read <prompt> whole and execute it."
(Opus, high effort, for money, security or large refactors).

## 7. Hazards

- Workers and reviewers may save captures inside a repository folder — prompts say move them; check `git status`.
- `main` moves under long-running reviews; a reviewer checks its head has not moved at the end.
- An executor that hits its limit mid-item leaves work unpushed — resume with a short prompt stating where it
  stands (`WORKER_B\DESK\3c_RESUME_PR2.md` is the model).
- Merging two PRs that touch the same documents: the second rebases (text conflicts only so far); run
  `typecheck` on the merged tree when both touch shared types.
