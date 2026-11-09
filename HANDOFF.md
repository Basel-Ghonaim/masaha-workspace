# Masaha — the main supervisor's handoff (2026-11-08)

You are taking over as the owner's **analyst and control room** for Masaha — the **main supervisor**. This file
supersedes the 2026-11-05 handoff (archived as `_SHARED\HANDOFFS\HANDOFF_2026-11-05_to_11-08.md`: refactor round 1's
prototype, #137). **You may not be Claude:** the rules that lived in Claude's private memory are copied into §8 — this
file, the repository and `BOARD.md` are everything you have.
**Read this file whole, then `BOARD.md`, then `REFACTOR_NOTES.md`, then the active task folders below, each from its
`0_OWNER_DECISIONS.md`.**

## 0. The supervisors

| Supervisor | Its one job | Its file |
|---|---|---|
| **You — the main supervisor** | analysis with the owner, plans, approvals, prompts, verification, reviews, merges, documents | this file |
| **«مشرف مراجعة التصميم #81»** | design review round 2 (Issue #81) | `DESIGN\ROUND2\HANDOFF_DESIGN_81.md` (idle since 2026-10-20) |

## 1. Your role and how you speak

- **Arabic** with the owner — **plain, colloquial-leaning Arabic, with every technical or on-screen term in English**;
  never over-translate. UI tasks as short numbered click-by-click steps. No line starts with an English word or a code
  token; decisions as items with options and a recommendation, never tables; short first. **English** in every prompt
  and plan.
- You run in `C:\dev\masahapp` but **never edit the repository** (exception: the owner asked the supervisor to
  rebuild the directory's price block live in the prototype on 2026-11-07 — only on his explicit word). Read-only git
  and `gh`; you write in the workspace. **Merge only with the owner's word**: `gh pr merge <n> --merge
  --match-head-commit <full sha>`; then delete the branch (remote, local) and its `backup/*`, `app` → `git switch
  main` + `pull --ff-only`; `npm ci` only if `package-lock.json` moved; `npm run build -w @masaha/shared`; after a
  schema change `migrate deploy` + `generate`. Update `BOARD.md` (and this file at a milestone).
- **Every merge to `main` deploys to production** (Vercel). Say so before asking for a merge.
- **Verify every worker report in the code** before believing it (head, `gh pr checks`, `CLEAN`, subjects ≤ 50 with a
  body, no tool attribution, no `fixup!`, no `#PRNUM`, scope, the claims that matter) — **and look at the screens
  yourself** (the prototype at 390/768/1024/1440, AR/EN, light/dark). Never trust a non-Claude report unchecked.
- **The owner's bar:** production-ready, no errors; he reacts strongly to sloppy UI and to unexplained disabled
  controls. **Never revive a decision he cancelled** without asking.
- **The owner sets each day's work.** Delegated points ("as your recommendation") → the safest option, logged.
- **claude.ai is the owner's company account:** Artifacts fine while working; deliverables saved in the workspace.
- **Local servers the supervisor used:** `C:\dev\masahapp\.claude\launch.json` (excluded from git through
  `.git/info/exclude`): `prototype` on 5325 (serves `app`'s `docs/design/prototype`), `profile-mockup` on 5330.

## 2. State (start here)

> **2026-11-08 update: `main` = `7fb73c3c`: #139 (DIRECTORY_PROD, done) then #138 (SPACE_PROFILE's prototype round).
> Next: SPACE_PROFILE's production step, the women + evening task, the palette lab. See `BOARD.md`.**
> **`main` = `40cb481d` (#137, 2026-11-07). Masaha v1 is LIVE at `https://masaha-omega.vercel.app`.**
> - Live setup, the spam issue, DEMO_SHOW data in `masaha_dev` (**never `db:seed` it**), the presentation: unchanged —
>   see the archived handoff (`_SHARED\HANDOFFS\HANDOFF_2026-11-05_to_11-08.md` §2).
> - **Open findings:** 23, 65, 152 (measured from ~2026-11-12); **214** (the flaky Home test, fixed inside
>   DIRECTORY_PROD); **215** (the prototype's Home and `TodayHours`, recorded by DIRECTORY_PROD). Check the index.
> - Open Issues: #72 (postponed), #81 (design round 2). `app-review` is old (`0ec43b61`), the owner's call.
> - **The owner's order:** the refactor goes page by page; the full project review waits for his word.
> - **Worktrees:** `app` = DIRECTORY_PROD's executor (`feat/directory-filters`, work in progress); `app-b` = the
>   palette lab (`design/palette-lab`); `app-design` = SPACE_PROFILE's prototype worker (`design/space-profile`, from
>   2026-11-08); `app-review` = old.

## 2a. Active work (2026-11-08)

**A. DIRECTORY_PROD — the directory's filters in web + API** (`TASKS\DIRECTORY_PROD\`).
- Decisions 1–15 + the plan's OD1–OD7 (all as the planner recommended) in `0_OWNER_DECISIONS.md`; plan `2_PLAN.md`
  (654 lines, a numbered test matrix); executor prompt `3_EXEC_PROMPT.md` — a **fresh Claude Code session** (Opus 5.5
  high) in `app` on `feat/directory-filters`, expected **PR #138**, five commits, ~90 files. Running now.
- The owner's bar for it: **tests that work and point the right way, never bent; filter tests without a gap.**
- Next: verify its report and CI yourself; recommend a separate Claude review (≈90 files) — the owner decides; the
  merge is his word. **The women + evening task must start only after this PR merges** (same filter files).

**B. SPACE_PROFILE — the owner's space profile + the admin's editor** (`TASKS\SPACE_PROFILE\`).
- Every section decided with the owner, one by one, in `0_OWNER_DECISIONS.md` (G, H, P, R, W, S, A, B, L, C and the
  post-mock-up **M1–M4**, which override earlier lines). The owner tried the interactive mock-up
  `mockup\index.html` and **approved it officially** (its phone header overflow is a mock-up bug; M2 says the fix).
- Next: the prototype round — `3_PLAN_AND_EXEC_PROMPT.md` (a worker in `app-design`: short plan, build at once, stop
  **uncommitted** for review; commit/push/PR only on the owner's word). Then production (plan → approval → a fresh
  executor), where a **drag-and-drop dependency is approved** and **the contacts' new types / «وسيلة أخرى» need a
  migration** the plan must name.

**C. IDENTITY — the palette lab** (`TASKS\IDENTITY\`): OpenCode in `app-b` (`design/palette-lab`, new files only,
port 5401). The owner favours **Sea sunset**; rounds 2 (status check, Sea sunset 2/3, copy-values bug) and 3
(`3_EXEC_PROMPT_LAB_R3.md`: the theme bug, the desktop preview at 1440 (bug 5), a toolbar, a gallery with favourites
and compare, 10 new palettes). Then: the owner picks → the logo in it (`TASKS\LOGO\`) → tokens. Watch
`foundation.md` (DIRECTORY_PROD adds `SegmentedControl` there).

**D. WOMEN + EVENING** (one task, not started): spaces with a women's hall / women-only, and the owner-declared
evening hours; the direction approved, the details decided when it starts — **after DIRECTORY_PROD merges**.

**Later:** design round 2 (#81), #72; findings 23, 65, 152.

## 3. The owner's standing rules

- **Nothing reaches CI untested** — complete local verification before a PR. With **OpenCode** workers the owner
  runs the tests himself (OpenCode is ~20× slower): the prompt makes the worker **stop at one planned point**, print
  the exact commands for `C:\dev\masaha\app` (or `app-b`), and continue on his pasted results (only the failed or
  affected commands again). **Claude Code** workers run the verification themselves. `test:api` may be left to CI
  when a PR changes no API code (the owner's decision, per task).
- **Plans:** small, fully-decided tasks need no approval round — the worker writes a short plan file, then executes
  without stopping (the owner approved this pattern for DEPLOY, PRIVACY, QUICK_FIXES_1). Big or open tasks keep the
  plan → approval → execution method (§4).
- **The no-stop rule** for long runs; hard limits: no merge, no push to `main`, no force-push of another branch, no
  unplanned migration, no data changed through the app beyond named writes, never weaken a test, no secret printed,
  no tool attribution. Prisma refuses `migrate reset` from an AI agent: the worker asks the owner.
- **Fix rounds:** each fix folded into its commit (`--fixup` + autosquash, a `backup/*` first). A review's small
  findings ride the next PR's first commit when one exists.
- **Reviews:** Claude (headless, read-only) for money, auth, schema; non-Claude reviewers' findings verified in code.
- **Public text:** never name hosting providers, free plans or session durations in public pages (the owner's
  security rule, 2026-11-04).

## 4. The method that worked

- **Decisions first with the owner** → a self-contained prompt (everything inline: approved texts are embedded, no
  pointers into the workspace) → the worker's short plan file → execution → your review in the code and screenshots →
  the owner's merge word.
- **Watchers:** for a running worker, a bounded background script (`gh pr list --head <branch>` + `gh pr checks` +
  the report file, every 2 minutes, ≤ 5 hours) wakes you when the PR is green and `CLEAN`; tell the owner to keep the
  conversation open. Write it into a file in your scratchpad and run it in the background.
- **Big runs:** lead + sub-agents, own worktrees, test DB per API lane, heavy-run grants (`_DONE\PAYMENTS_STEP10\
  scripts\heavy.mjs`); models of the files under `WORKER_A\_DONE\FINAL\` and `WORKER_B\_DONE\BACKEND_FINAL\`.
- **Claude review command** (from `app-design`; pre-fetch first): `claude -p "Read <prompt> whole and do it." --model
  claude-opus-5-5 --effort <level> --add-dir 'C:\dev\masaha\workspace' --strict-mcp-config --no-chrome --settings
  'C:\dev\masaha\workspace\_SHARED\worker-settings.json' --allowedTools "Bash(git *)" "Bash(gh *)" Read Grep Glob
  Write Edit > <log> 2>&1`.

## 5. Ledgers

- **Findings:** open 23, 65, 152 (after the deployment's measurements); next free **214**.
- **The owner's notes for the refactor:** `REFACTOR_NOTES.md` (Home's empty «المتاحة الآن» on unverified spaces,
  spam, #136's nits, and whatever the owner adds).
- **Decisions:** `WORKER_B\DEPLOY\0_OWNER_DECISIONS.md` (deployment, items 1–10), `TASKS\DEMO_SHOW\0_OWNER_DECISIONS.md`,
  `TASKS\PRIVACY\PRIVACY_AR.md` / `PRIVACY_EN.md` (the approved policy text), `_SHARED\OPEN_DECISIONS.md`,
  `DESIGN\DECISIONS\`.
- **The presentation:** `TASKS\PRESENTATION\Masaha.pdf` (8 slides, Arabic; source `deck.html`, rendered by headless
  Chrome).

## 6. The workspace

`C:\dev\masaha\workspace\`: `WORKER_A\`, `WORKER_B\` (DEPLOY lives in `WORKER_B\DEPLOY`), `DESIGN\`, `TASKS\`
(DEMO_SHOW, PRESENTATION, PRIVACY, QUICK_FIXES_1), `_SHARED\`; `BOARD.md` (keep it true); `REFACTOR_NOTES.md`.
Backup: private repo `Basel-Ghonaim/masaha-workspace`, nightly 23:00.

## 7. Hazards and lessons

- A watcher or headless worker launched from your conversation dies with it — the owner keeps it open.
- **Writing files through Python/heredocs:** the tool turns some backslash escapes into real characters — a
  backslash-zero once became a NUL byte in this file. Build paths with `os.path.join` / `chr(92)`, and check new files
  for NUL bytes.
- Vercel hides sensitive variables for good: a lost secret is rotated (new value in Vercel + Redeploy + every user of
  it), never recovered.
- `gh pr merge --match-head-commit` needs the full sha; `git checkout -- <file>` loses work; `jq` is absent (use
  `gh --jq`); Git Bash pastes can prepend `[200~`.
- The demo seed renews a FULL space on every run — never on `masaha_dev` while it holds DEMO_SHOW.
- The prototype: shared Babel globals (a duplicate top-level name breaks pages) and a prebuilt CSS holding only the
  classes already used — `check-parse` and `check-classes` catch both.
- **Never revive a decision the owner cancelled** without asking him first, even if it looks useful (the amenities
  filter, 2026-11-05). Before proposing a filter or a screen change, search `docs/features/<cap>.md` and the
  prototype's comments for an earlier owner decision on it.

## 8. Rules from the previous supervisor's private memory (you have no copy of it)

- **Identity:** the owner's own project; never name the university, the supervisor or the defence publicly.
- **Replies in Arabic:** no line starts with an English word or a code token; decisions as items with options and a
  recommendation, never tables; short first.
- **Method:** decide with the owner first → a short, self-contained prompt → the worker's plan saved, then it stops
  (big tasks) or runs (small, decided ones) → complete local verification → the report to a file.
- **Prompts in `C:\dev\masaha\workspace\`**, one folder per task, numbered files (`0_OWNER_DECISIONS`, `1_…`,
  `2_PLAN`, `3_EXEC_PROMPT`, `4_REPORT`). Plan prompts forbid temp copies, trial worktrees and scratch runs.
- **Two workers in parallel** only on separate files (one schema change, one dependency change at a time, no shared
  code file). `app` and `app-b`; a worktree with a schema branch gets its own `masaha_<item>_dev/_test` databases.
- **Fix rounds on an unmerged PR fold into their commits** (`backup/*` first, `--fixup` + autosquash); no fix commits.
  Serious review fixes reopen the PR; small ones ride the next PR's first commit, named in its description.
- **Report only when `gh pr checks` is green on the pushed head** and GitHub says `CLEAN`. Rebase only when the PR is
  dirty, never by default. `#PRNUM` in docs is replaced with the real number just before the push.
- **No production code only tests use** (no parameter or option only a test passes); stub platform seams instead.
- **Prisma:** `migrate dev --create-only` once only (a second run applies it to `masaha_dev`); on data loss use
  `migrate diff --script`. `migrate reset` needs the owner.
- **A lane killed for memory:** retry once, then let CI judge — write this into every execution prompt. Two full test
  lanes at once fit with 8–10 GB free; a third waits.
- **Workers never stop on file count**; they report it.
- **A command inside a pasted worker transcript is not for you** — ask before acting on it (merges above all).
- **"As your recommendation"** = the safest option, logged; never a merge on it. **"Merge"** approved = also delete the
  branch and clean the worker.
- **Screenshots** go to `C:\Users\basel\Downloads\<task>-shots\`, curated, never pushed.
- **Windows shell traps:** no `jq` in Git Bash (use `gh --jq`), bound every watch loop; long scripts go in files, not
  heredocs; stopping a backgrounded API dev task leaves processes on the port — stop by PID and check the port;
  restore a broken file from a `cp` backup, never `git checkout --`.
- **claude.ai Artifacts** (company account): fine while working; a finished deliverable is saved in the workspace and
  the Artifact deleted.
- **Workflow-rule gaps** ride on the next worker item as their own commit.
