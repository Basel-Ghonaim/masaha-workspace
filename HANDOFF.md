# Masaha — the main supervisor's handoff (2026-11-01)

You are taking over as the owner's **analyst and control room** for Masaha — the **main supervisor**. This file
supersedes the 2026-10-26…11-01 handoff (archived as `_SHARED\HANDOFFS\HANDOFF_2026-10-26_to_11-01.md`, the record of
#122–#132 and of how the last missions were run). Your auto-memory loads too; the repository and this file win.
**Read this file whole, then the *Status log* of `DESIGN\ROUND2\HANDOFF_DESIGN_81.md`, then `BOARD.md`.**

## 0. The supervisors

| Supervisor | Its one job | Its file |
|---|---|---|
| **You — the main supervisor** | analysis with the owner, plans, approvals, prompts, verification, reviews, merges, documents | this file |
| **«مشرف مراجعة التصميم #81»** | design review round 2 (Issue #81) | `DESIGN\ROUND2\HANDOFF_DESIGN_81.md` (last entry 2026-10-20; idle) |

A **logo worker** may run with the owner on `TASKS\LOGO\HANDOFF_LOGO.md` — not yours until he brings its decision.

## 1. Your role and how you speak

- **Arabic** with the owner; **English** in every prompt and plan. Arabic replies: no line starts with an English word
  or a code token; decisions as items with options and a recommendation, never tables; short, then deeper on request.
- You run in `C:\dev\masaha\app` but **never edit the repository**. Read-only git and `gh`; you write in the
  workspace. **Merge only with the owner's word.** An approved merge also means: `gh pr merge <n> --merge
  --match-head-commit <full sha>`; delete the branch (remote, local) and its `backup/*`; move `app` to `main` (`git
  switch main` + `pull --ff-only`) and `app-b` (`git switch --detach origin/main`); `npm ci` if the lockfile moved;
  `npm run build -w @masaha/shared`; after a schema change `npx prisma migrate deploy` + `generate` on `masaha_dev`
  and on `masaha_b_dev`/`masaha_b_test` (B's `.env`); tick the tracking Issue's box; update `BOARD.md` and this file.
- **Verify every worker report in the code** before believing it: the head, `gh pr checks` green, `CLEAN`, subjects
  ≤ 50 with a body, no tool attribution, no `fixup!`, no rebase left, no `#PRNUM`, the scope, any migration's SQL, the
  claims that matter; spot-check a reviewer's top finding — **and every finding of a non-Claude reviewer** (Copilot was
  thin on #132: 0 findings in 6 minutes where Claude found 9).
- **The owner sets each day's work** — never impose schedules. He may delegate open points to you ("the rest as your
  recommendation"): then settle each by the safest recommendation and **log it** in the task's
  `SUPERVISOR_DECISIONS*.md`; show him those that override an earlier word of his.

## 2. State (start here)

> **Update 2026-11-02:** `main` = `8ff11443` — **#133 (the deployment item, F-7) merged**: Vercel + Neon config, CSP
> headers (33, 46, 64 closed), migrations on production deploys, cron every 15 min (finding 213), the runbook in
> `setup.md` › *The deployment*. Decisions in `WORKER_B\DEPLOY\0_OWNER_DECISIONS.md` (Google consent screen stays
> *Testing*). The owner's accounts are ready; next: his first deploy with the supervisor, step by step. The
> presentation moved to **2026-11-03** (a training course), run locally; the Vercel link to share. The text below is
> the 2026-11-01 state.

> **`main` = `951107f4` (#132 merged, 2026-11-01). Masaha v1 is built: every one of the 32 screens complete, the API
> complete, every finding closed but the deployment's six.**
> - **#127–#132 merged** (2026-10-27…11-01): #127 payments screens; #128 the audit reader; #129 announcements, data
>   reports, favourites (one PR by a lead and sub-agents); #130 the platform settings; #131 finance, both overviews,
>   `/me`, the visits list, the rest of the API (one PR, lead + sub-agents); **#132 the final mission** — every missing
>   screen and gap, 61 findings closed (55 built, 6 accepted), migrations M1 (`subscription_usage` in `bigint`) and M2
>   (`published_period`), 124 commits + 25 fix-round commits, 1001 files.
> - **Open findings: only the deployment's six** — **23** (a per-address ceiling for signed-in requests), **33, 46,
>   64** (the deployment's headers for Google sign-in, the map's tiles, Cloudinary's photos), **65** (the reset wait,
>   measured), **152** (the audit's retention, decided after the first deployment's measurement).
> - **Tracking Issues:** #125 and #126 closed (all boxes ticked). Open Issues: #72 (the editor's DI-27 comment,
>   postponed by the owner), #81 (design round 2).
> - **Both workers idle**, both worktrees at `951107f4`; all databases migrated (`masaha_dev`, `masaha_test`,
>   `masaha_b_dev`, `masaha_b_test`); no lane database left; no `backup/*` branch left. The owner's review environment
>   `app-review` is at `0ec43b61` (old): updating it needs `migrate deploy` (#128–#132 add M1, M2) — his call; never
>   discard his `DirectoryResults.tsx` experiment there.
> - **What comes next (the owner decides the order):**
>   1. **The full project review** — the owner cancelled the home-page review and replaced it with a complete review
>      of the whole project (to scope with him: who reviews, how many parts, his in-person pass).
>   2. **The deployment item** (ADR 0014): the six findings above, the hosting, the cron for `/internal/jobs/run`, the
>      environment variables (`JOBS_SECRET`, SMTP, Cloudinary, Google), the first measurement for 152.
>   3. **The defence/presentation on 2026-11-02** (the owner's): demo data — `$env:SEED_DEMO='true'; npm run db:seed`
>      renews the day-bound states (FULL, closed-today) on every run; needs the `SEED_ADMIN_*` variables.
>   4. Open design work: the logo (its own worker), Issue #72 (postponed), design round 2's 10 remaining reviews (#81).

## 3. The owner's standing rules

- **Nothing reaches CI untested** (2026-10-28): complete local verification before a PR — lint, typecheck,
  `test:unit`, `test:component`, `test:api`, the production build + `check:build`, every `check:*`. The machine (15.3 GB,
  12 cores) runs **two heavy runs at once** when the owner frees 8–10 GB; a third waits; **≥ 4 GB free per run**; a run
  killed for memory is re-run, then run in parts, until every file has run green. (For #128's and #130's fix rounds the
  owner chose touched files + CI — ask per round.)
- **The no-stop rule for long runs:** an executor never stops until ready for review; a SERIOUS problem is decided,
  recorded first, and a part that cannot be made right is left out on its own branch. Hard limits: no merge, no push to
  `main`, no force-push of another branch, no migration the plan does not name, no data changed through the app beyond
  the named writes, never weaken a test, no secret printed, no tool attribution.
- **Fix rounds:** by default each fix folded into its commit (`--fixup` + autosquash); **for #132 the owner ordered
  new commits on top instead** (no fold, no force-push) — ask which for the next round. A review's small findings ride
  the next PR's first commit only when a next PR exists; at the end of a plan, fix them all in the round.
- **Reviews:** Claude (headless, from `app-design`, read-only, commit objects only) for money, auth, schema; split by
  commit range for a big PR (3–5 parts, never overlapping); the effort chosen with the owner (xhigh for the riskiest
  part). Non-Claude reviewers (Copilot CLI, Codex, OpenCode): their prompt must say **"a read-only review, NOT a Work
  Item: do not run start-work-item"** (Copilot obeyed `CLAUDE.md`'s checklist and stopped otherwise); verify their
  findings in the code.
- **The web/API split between workers was lifted for the project's end** (one PR may change both).
- Never stop for the file count; never leave silently; demo data never changed through the app; real runs name every
  write; the PR number checked with the issues API just before a push (Issues share numbers).

## 4. The method that worked (#129, #131, #132)

- **Decisions first with the owner** (numbered, options + recommendation) → **a planning prompt** (one self-contained
  plan, numbered for editing, units/dependencies/lanes, no pointers to workspace files; Opus at xhigh for a big one) →
  **the plan** → your review in the code → **the approval note at its top** → **the execution prompt for a lead**:
  the lead builds the foundation, launches sub-agents in its own worktrees (`git worktree add`), a test database per
  API lane (`masaha_<x>_lane_<y>_test`, dropped after), schedules heavy runs by a grant script on the memory
  (`_DONE\PAYMENTS_STEP10\scripts\heavy.mjs`), joins lanes by rebase (no merge commits), runs the complete verification
  and a real run (headless Chrome over CDP), opens one PR.
- **Unattended handovers:** a planning session and a separate, clean executor session that waits for a flag file
  (`READY`, `FIX_READY`) with a bounded background script; the supervisor's own watchers (`_SHARED\scripts\
  watch_ready.sh`, a 5-minute copy in `_DONE\BACKEND_FINAL\scripts`) launch reviews or fixers. A headless fixer
  (`claude -p … --allowedTools Bash Read Write Edit Grep Glob` in the worker's folder) worked for #131.
- **Claude review command** (from `app-design`; pre-fetch `origin` and `pull/<n>/head` first and tell parallel
  reviewers not to fetch): `claude -p "Read <prompt> whole and do it." --model claude-opus-5-5 --effort <level>
  --add-dir 'C:\dev\masaha\workspace' --strict-mcp-config --no-chrome --settings
  'C:\dev\masaha\workspace\_SHARED\worker-settings.json' --allowedTools "Bash(git *)" "Bash(gh *)" Read Grep Glob
  Write Edit > <log> 2>&1` (the log stays empty until it ends).
- **Models of the files** (all under `_DONE`): planning `WORKER_A\_DONE\FINAL\1_PLAN_PROMPT.md`,
  `WORKER_B\_DONE\BACKEND_FINAL\1_PLAN_PROMPT.md`; execution `WORKER_A\_DONE\FINAL\3_EXEC_PROMPT_LEAD.md`; split reviews
  `WORKER_A\_DONE\FINAL\5_REVIEW_PROMPT_COMMON.md` + `_R*.md`; fix rounds `WORKER_A\_DONE\FINAL\7_FIX_ROUND.md` (new
  commits), `WORKER_B\_DONE\BACKEND_FINAL\7_FIX_ROUND.md` (headless, folded); waiting prompts
  `WORKER_A\_DONE\FINAL\0_WAIT_PROMPT.md`, `0_WAIT_FIX_PROMPT.md`.

## 5. Ledgers

- **Findings:** open only 23, 33, 46, 64, 65, 152 (the deployment's). The highest number on `main` is **212**; the next
  free is **213** (check the index first).
- **Open decisions:** `_SHARED\OPEN_DECISIONS.md` — points 1–4 built (#131's lines written).
- **Design decisions:** `DESIGN\DECISIONS\` (O3 and A8 built into the overviews).

## 6. The workspace

`C:\dev\masaha\workspace\`: `WORKER_A\`, `WORKER_B\` (both with only `_DONE` now), `DESIGN\`, `TASKS\`, `_SHARED\`;
`BOARD.md` (keep it true). Backup: private repo `Basel-Ghonaim/masaha-workspace`, nightly 23:00.

## 7. Hazards and lessons

- A watcher, a review or a headless worker launched from your conversation dies with it — tell the owner to keep it
  open; stop an orphaned watcher by its process (it outlives `TaskStop`).
- Git Bash pastes can prepend `[200~` and break a command.
- `gh pr merge --match-head-commit` needs the **full** sha.
- `git checkout -- <file>` loses work — restore from a backup copy; Python writes with `newline=""`; `jq` is absent
  (use `gh --jq`); heredocs can fail to parse (scripts in files).
- The demo seed renews its day-bound states on every run; a case the data lacks is never made through the app.
