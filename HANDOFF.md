# Masaha — the main supervisor's handoff (2026-11-18)

You are taking over as the owner's **analyst and control room** for Masaha — the **main supervisor**. This file
supersedes the 2026-11-15 handoff (archived as `_SHARED\HANDOFFS\HANDOFF_2026-11-15_to_11-17.md`: CONTACT_RULES,
GOOGLE_VERIFY, the cleanup). **You may not be Claude:** the rules that lived in Claude's private
memory are in §8 — this file, the repository and `BOARD.md` are everything you have.
**Read this file whole, then `BOARD.md` (its top lines are the newest), then the active folders of §2, each from its
`0_OWNER_DECISIONS.md`.**

## 0. The supervisors

| Supervisor | Its one job | Its file |
|---|---|---|
| **You — the main supervisor** | analysis with the owner, plans, approvals, prompts, verification, reviews, merges, documents; **and, since 2026-11-15, the design work the owner hands you directly** (§2 A) | this file |
| «مشرف مراجعة التصميم #81» | design review round 2 — superseded; idle since 2026-10-20 | `DESIGN\ROUND2\HANDOFF_DESIGN_81.md` |

## 1. Your role and how you speak

- **Arabic** with the owner — **plain, colloquial-leaning Arabic, every technical or on-screen term in English**; never
  over-translate. UI tasks as short numbered click-by-click steps. **No line starts with an English word or a code
  token**; decisions as items with options and a recommendation, never tables; short first. **English** in every
  prompt and plan. Be direct and critical when the owner asks your opinion — he asks for it, and dislikes flattery.
- You run in `C:\dev\masaha\app` (the Claude desktop app's Code tab). **You never edit the production repository
  `masaha`** — read-only git and `gh` — **except a fix round the owner hands you by name** (he did for #147 on
  2026-11-15: folded fixups, full local checks, force-with-lease on that PR's own branch). You write in the workspace,
  and **in the design repository `masaha-prototype` when the owner asks you to design yourself** (§2 A).
  **Merge only with the owner's word**: `gh pr merge <n> --merge --match-head-commit <full sha>`; then delete the
  branch (remote, local), its `backup/*` and any `lane/*`; move the worktree that held it to `main` (never one a worker
  is using); `npm ci` only if `package-lock.json` moved; `npm run build -w @masaha/shared` if `packages/shared` moved;
  after a schema change `migrate deploy` + `generate`. Then watch `main`'s CI and the Vercel status on the merge
  commit. Update `BOARD.md` (and this file at a milestone).
- **Every merge to `main` deploys to production** (Vercel, `https://masaha-omega.vercel.app`). Say so before asking.
- **Verify every worker report in the code** before believing it (head, `gh pr checks`, `CLEAN`, subjects ≤ 50 with a
  body, no tool attribution, no `fixup!`, no `#PRNUM`, scope, the claims that matter) — **and look at the screens**.
- **The owner's bar:** production-ready, no errors; he reacts strongly to sloppy UI and to unexplained disabled
  controls. **Never revive a decision he cancelled** without asking.
- **The owner sets each day's work.** Delegated points ("as your recommendation") → the safest option, logged.
- **claude.ai is the owner's company account:** Artifacts fine while working; deliverables saved in the workspace.
  **This week (from 2026-11-14) the company limits outside work**: spend carefully.
- **While the owner is away** (he asked on 2026-11-15): watch the workers with bounded watchers, launch each finished
  worker's review, fix what he delegated, merge nothing. A worker that asks a question waits for him — you cannot type
  in its window.

## 2. State (2026-11-19, end of day)

**`main` = `9b4c4fc1`** (live; CI and Vercel green; no open PR). Merged since the last handoff: **#148**
GOOGLE_VERIFY, **#149** CONTACT_RULES and, on 2026-11-19, **#150 AXE_FIXES** (finding 224: the design system's
`ScrollRegion`, the photos' phone row and «ساعات الذروة» in it, the map's tooltip hidden from assistive technology;
a Claude Code worker; the supervisor's own axe pass; `TASKS\AXE_FIXES\`; its small notes C1–C2 are **carried to the
next PR's first commit**: `TASKS\AXE_FIXES\0_CARRIED_FROM_150.md`; a proposed next task there: the prices table's
`scrollable-region-focusable` → finding 229). Worktrees: **`app`** and **`app-design`**, both on `main`. Databases:
`masaha_dev`, `masaha_test`, `masaha_design_test` only.

### A. AUTH — the sign-in pages' design (`DESIGN\AUTH\`) — **Sign in FIXED as pictures (A13); the method changed**
- **The new method (the owner, 2026-11-19, A13): design as pictures first, never in code first.** Every coded
  round was rejected (the original, Slate, Slate 2, and round 4's Atlas / Threshold / Clearing by a Claude Code
  designer — "empty designs"). What worked: wireframes → one chosen → colour and identity, iterated by looking, on a
  private claude.ai Design canvas the supervisor draws himself, in short loops with the owner. **claude.ai is a shared
  company login: anything there is visible to colleagues — save locally and delete when done.**
- **Fixed — Sign in, design B:** an ink masthead (the logo, English + theme, «تسجيل الدخول» at 56 px and its line);
  under it two ways in on one 12-column grid — the form (Google at its real 40 px box, email, password, «نسيت كلمة
  المرور؟», the ink button) and «جديد على مساحة؟» (register's line, «إنشاء حساب», the owners' note); the phone: the
  masthead, then the form, then the new-account block. **Plain ink — no texture** (dots, berry dots, a berry rule,
  a floor plan, tatreez and a watermark mark were all tried and dropped). Files: `DESIGN\AUTH\round5-B\` (four
  standalone pages 1440 / 390 × light / dark, their PNGs, `canvas-source\`). Decisions: `0_OWNER_DECISIONS.md` A1–A13.
- **masaha-prototype:** `main` **pushed to `f140f8a`** on the owner's word (2026-11-19; the original pages and shared modules untouched): 5 commits (`b84fc7f` Coast and Dots retired, `96f7bc6`
  Slate 2, `d65ef9f` / `0b9b43c` / `f140f8a` round 4's three designs — all rejected, kept as variants). Nothing there is the chosen design.
- **Next (the owner sets it):** the other auth pages (register, forgot, reset, the forced change, the reset e-mail)
  in B's language, as pictures; then code once — a prototype variant or straight to the production Work Item.
  The owner also asked why design work with the supervisor has struggled (the answer given 2026-11-19: §9).

### B. GOOGLE_VERIFY — the consent screen's branding (`TASKS\GOOGLE_VERIFY\`) — **paused by the owner**
- «I have fixed the issues» → Proceed returns "home page … not registered to you" at once (2026-11-19), though Search
  Console verified the owner on 2026-11-16. Forum threads show the same for `vercel.app` homes, no answer from
  Google. **Paused (the owner):** Google sign-in already works for everyone; only the name and logo on the consent
  screen wait. Open for later: whether the Search Console owner is an Owner/Editor in the Cloud project's IAM (not
  checked); «I believe the issues found are incorrect»; a custom domain (C4).

### C. The owner's pending items
1. ~~The empty folder `C:\dev\masaha\app-cr`~~ — **removed** by the supervisor on the owner's word (2026-11-19; the
   restart had freed it; checked empty first).
2. ~~WSL / Docker memory~~ — **done**: `%UserProfile%\.wslconfig` `[wsl2]` **`memory=3GB`** (the owner's choice,
   2026-11-19, over the supervisor's 2 GB); in force after the next `wsl --shutdown` or restart.
3. Later: close Issue #81; the post-deployment measurements of findings 23, 65, 152; E2E at the end; the full project
   review on his word.
4. A custom domain — would cure the reset e-mail landing in spam and any Google doubt about `vercel.app` (to discuss).
5. **`masaha`'s old history**: left as it is (A) — decided; nothing to do.

### D. History (2026-11-16 → 17), for reference
CONTACT_RULES (`TASKS\CONTACT_RULES\`, done: Claude planned, Codex executed, a targeted review, an OpenCode fix round, a
supervisor doc fold, #149), GOOGLE_VERIFY (`TASKS\GOOGLE_VERIFY\`, done: Copilot CLI plan → APPROVED → #148), the
cleanup (databases `masaha_b_*`, `masaha_review_*`, `masaha_wi142_dev`, `masaha_dr_*`, `masaha_design_dev`,
`masaha_cr_*` dropped; `app-dr`, `app-cr` removed). Details in the archived handoff and `BOARD.md`.

## 3. The owner's standing rules

- **Nothing reaches CI untested** — complete local verification before a PR (Claude Code workers run it themselves;
  `test:api` may be left to CI only when a PR changes no API code and the owner allows it for that task).
- **Plans:** small, fully-decided tasks → the worker plans briefly and builds at once (WOMEN_EVENING ran so); big or
  open tasks → plan → the owner's approval → execution.
- **The no-stop rule** for long runs; hard limits: no merge, no push to `main`, no force-push of another branch, no
  unplanned migration, no data changed beyond named writes, never weaken a test, no secret printed, no tool
  attribution. Prisma refuses `migrate reset` from an AI agent: the worker asks the owner.
- **Fix rounds** fold into their commits (`backup/*` first, `--fixup` + autosquash). **Review findings:** serious →
  a fix round before the merge; small → **the next PR's first commit**, listed in a `0_CARRIED_FROM_<n>.md` and named
  in that PR's description (the owner chose this for #144).
- **Reviews:** a Claude review (headless, read-only, Opus xhigh) for big PRs and anything touching money, auth or the
  schema; for a big PR, **two reviewers by role** (as #144: R1 the colour system, R2 the rest and the PR as a whole).
- **The no-conflict rule (the owner, 2026-11-12):** a worker may start before an open PR merges, but edits none of that
  PR's files until it has merged; its sub-agents start only after the merge and its rebase.
- **Public text:** never name hosting providers, free plans or session durations.

## 4. The method that worked

- **Decisions first with the owner** (items, options, a recommendation, recorded in the task's `0_OWNER_DECISIONS.md`)
  → a self-contained prompt → the worker's plan → execution → your verification in the code and the screens → the
  owner's merge word.
- **Launching workers (the owner runs them in PowerShell):** `cd <folder>` then `claude --model claude-opus-5-5
  --effort <high|xhigh> --add-dir 'C:\dev\masaha\workspace' --strict-mcp-config --no-chrome --settings
  'C:\dev\masaha\workspace\_SHARED\worker-settings.json'`, then paste "Read <prompt> whole and do it." **A cut worker
  is resumed, not restarted:** `claude --resume <session-id>` with the same flags (the id is the newest
  `C:\Users\basel\.claude\projects\<C--dev-masaha-folder>\*.jsonl`) plus a pasted state message.
- **Big runs:** a lead + sub-agents (cap stated in the prompt), each lane in its own worktree when the disk allows, the
  lead joining by rebase (`TASKS\IDENTITY\3_EXEC_PROMPT_PROD.md` is the latest model). **The machine's one grant
  script:** `TASKS\IDENTITY\scripts\heavy.mjs <lane> <command…>` — every heavy command of every worker goes through it
  (≥ 4 GB free to start; one heavy run at a time under 8 GB free; the identity lead first). After a crash, a
  `heavy-slot-*` folder no process holds blocks everyone: remove it and log a `super CLEAR` line.
- **Watchers:** a bounded background script in your scratchpad (gh calls that fail are logged and retried, never
  fatal) wakes you when a PR is green, `CLEAN` and reported; tell the owner to keep the conversation open.
- **Claude review command** (from `app-design`; `git fetch origin pull/<n>/head` first): `claude -p "Read <prompt>
  whole and do it. Role: <R>. PR #<n>, branch <b>, head (<HEAD>) <sha>." --model claude-opus-5-5 --effort xhigh
  --add-dir 'C:\dev\masaha\workspace' --strict-mcp-config --no-chrome --settings
  'C:\dev\masaha\workspace\_SHARED\worker-settings.json' --allowedTools "Bash(git *)" "Bash(gh *)" Read Grep Glob
  Write Edit > <log> 2>&1` — run in the background, one per role.
- **Before / after comparison for the owner:** a detached worktree at the PR head on its own ports, against a copy of
  the demo data; each web needs its own API (`refuseCrossSite` checks the origin). Remove it junction-safely (§7).

## 5. Ledgers

- **Findings:** open 23, 65, 152 (measurements due); 215 (the prototype's Home, paused with AUTH); 221 (the README's
  Sea shots); 224 resolved by #150; 217, 218, 219, 225, 226, 228 by #149; 220, 222, 223, 227 by #146. The next free
  number is **229** (check the index) — proposed for the prices table's `scrollable-region-focusable`
  (`TASKS\AXE_FIXES\0_CARRIED_FROM_150.md`).
- **The owner's notes for the refactor:** `REFACTOR_NOTES.md`.
- **Decisions:** each task's `0_OWNER_DECISIONS.md`; `DESIGN\DECISIONS\` (round 2's settled design decisions — round 3
  may overturn them, each said); `_SHARED\OPEN_DECISIONS.md`; `WORKER_B\DEPLOY\0_OWNER_DECISIONS.md`.

## 6. The workspace and the machine

- `C:\dev\masaha\workspace\`: `TASKS\` (active: `GOOGLE_VERIFY`, the owner's step only), `DESIGN\` (active: `AUTH`), `WORKER_A\`,
  `WORKER_B\`, `_SHARED\`; `BOARD.md` (keep it true); `REFACTOR_NOTES.md`.
- **`C:\dev\masaha\masaha-prototype`** — the design repository (public `Basel-Ghonaim/masaha-prototype`); its server
  on 5410 from `app\.claude\launch.json` › `proto` (the launch file also holds `api-app` / `web-app` on 3320 / 5320,
  `api-before` / `web-before` on 3323 / 5323 from `app-design`; it is git-excluded but Prettier checks it — run
  `npx prettier --write .claude/launch.json` after editing it, or a worker's `format:check` fails). Captures: `D:\MASAHA\DT\AUTH\` (the owner's naming
  `<n>-<page>-<width>-<theme>.png`).
  Backup: private repo `Basel-Ghonaim/masaha-workspace`, nightly 23:00.
- **Worktrees now:** `app` (on `main`), `app-design` (detached at `main`; launch folder for headless reviews; its
  `.env` on `masaha_dev` + `masaha_design_test`; Prisma client regenerated 2026-11-16). Removed 2026-11-16/17: `app-dr`,
  `app-cr` (junction-safe; an empty `app-cr` folder may remain, §2 C1). Removed on 2026-11-14: `app-b` (its branch
  `design/palette-lab` kept), `app-review`, 17 leftover lane folders; their uncommitted work in
  `C:\dev\masaha\_worktree-backups\2026-11-14\`.
- **Databases** (Docker container `masaha-postgres-1`, port 5433): `masaha_dev` holds the demo set (**never
  `db:seed`**; the demo accounts sign in with `SEED_DEMO_PASSWORD`; **the admin account there now also has a local
  password, `app`'s `SEED_ADMIN_PASSWORD`** — it was Google-only, and Google sign-in fails on non-registered local
  ports); `masaha_design_test`, `masaha_test` — nothing else (every old one dropped 2026-11-16/17). Sign-in rate-limit rows may be cleared in a local database, never in code.
- **Memory:** 15.3 GB; usually 3–7 GB free. The Claude desktop app alone is ~1.8 GB (11 Electron processes — normal;
  a very long conversation makes its renderer heavy, so hand over to a fresh session at a milestone), Docker / WSL
  ~1.9 GB, Chrome ~1.8 GB.

## 7. Hazards and lessons

- **After a reboot or an outage:** Docker Desktop is down — start it, then `docker start masaha-postgres-1`; worker
  sessions are gone — resume them (§4); clear any stale grant slot; re-arm your watchers.
- **Claude Code's low-memory guard reaps background commands** (watchers, test runs) — workers record it and retry
  once; never let a worker restart a reaped run blindly in a loop.
- **Junctions in `node_modules`:** npm workspaces link `node_modules/@scope/<pkg>` to the project's own `apps/*` and
  `packages/*`. To delete `node_modules` or a worktree: `rmdir` each link first, then `cmd /c rmdir /s /q`; **never**
  PowerShell 5.1's `Remove-Item -Recurse` (it follows links and deletes their targets), never the global
  `AppData\Roaming\npm\node_modules` (Claude Code itself), never an app's own folders.
- A watcher or headless worker launched from your conversation dies with it — the owner keeps it open.
- A worker's "CI is still running" may be stale: check `gh pr checks` yourself before telling it to wait.
- Python/heredoc writes can turn backslash escapes into real characters; long scripts go in files; check new files for
  NUL bytes. `gh pr merge --match-head-commit` needs the full sha; `jq` is absent (use `gh --jq`).
- Vercel hides sensitive variables for good: a lost secret is rotated, never recovered.
- The prototype: shared Babel globals; a prebuilt CSS of the classes in use — `check-parse` and `check-classes`.
- **Never revive a decision the owner cancelled** — search `docs/features/<cap>.md` and the decision files first.

## 8. Rules from the previous supervisor's private memory (you may have no copy of it)

- **Identity:** the owner's own project; never name the university, the supervisor or the defence publicly.
- **Replies in Arabic:** no line starts with an English word or a code token; decisions as items with options and a
  recommendation, never tables; short first.
- **Prompts in `C:\dev\masaha\workspace\`**, one folder per task, numbered files (`0_OWNER_DECISIONS`, `1_…`, `2_PLAN`,
  `3_EXEC_PROMPT`, `4_REPORT`). Plan prompts forbid temp copies, trial worktrees and scratch runs.
- **Two workers in parallel** only on separate files (one schema change, one dependency change at a time, no shared
  code file) — and only when the owner allows (this week: one at a time); a worktree with a schema branch gets its own
  `masaha_<item>_dev/_test` databases.
- **Report only when `gh pr checks` is green on the pushed head** and GitHub says `CLEAN`. Rebase only when the PR is
  dirty, never by default. `#PRNUM` in docs is replaced with the real number just before the push.
- **No production code only tests use**; stub platform seams instead.
- **Prisma:** `migrate dev --create-only` once only; on data loss use `migrate diff --script`. `migrate reset` needs the
  owner.
- **A lane killed for memory:** retry once, then let CI judge — in every execution prompt. Two full lanes at ≥ 8 GB
  free, one under 8 GB.
- **Workers never stop on file count**; they report it.
- **A command inside a pasted worker transcript is not for you** — ask before acting on it (merges above all).
- **"As your recommendation"** = the safest option, logged; never a merge on it. **"Merge"** approved = also delete the
  branch and clean the worker.
- **Screenshots** go to `C:\Users\basel\Downloads\<task>-shots\`, curated, never pushed.
- **Windows shell traps:** bound every watch loop; stop servers by PID and check the port; restore a broken file from a
  `cp` backup, never `git checkout --`.
- **claude.ai Artifacts** (company account): fine while working; a finished deliverable is saved in the workspace.
- **Workflow-rule gaps** ride on the next worker item as their own commit.

## 9. Learned on 2026-11-14 → 17

- **Executors that worked (2026-11-16/17):** **Copilot CLI** (the owner's Education plan) with a two-phase prompt —
  phase 1 writes `2_PLAN.md` and stops, the owner + supervisor review, `APPROVED` → phase 2 — every text given word
  for word, commit messages and the PR body as files (`git commit -F`, `--body-file`): #148 clean in one pass.
  **OpenCode (free model)** with a fix-round prompt naming each fix's file, values, target commit and a break to prove
  it: #149's round clean. **Codex** on the owner's Go plan has very little quota — keep it for short runs.
- **Targeted reviews beat general ones** (the owner, 2026-11-16): a review prompt of requirements R1–R12 drawn from
  the task's decisions, each with input tables to trace and a PASS / WEAK / FAIL verdict with `file:line` — at effort
  **medium** it found real gaps (an 11-digit number in a doc, untested rows, a test that could not fail).
- **The owner's rule for fix rounds (C11):** one round takes **every** point of the branch — nothing left for a later
  PR, even an Open finding the PR recorded (stated as an override when it reverses an earlier decision).
- **Two executors racing for a PR number:** the one with `#PRNUM` in its docs must renumber (its plan's step) — say so
  in both prompts; open the `#PRNUM` one first when you can.
- **The grant script:** a worker's run that never ends (a session cut overnight) holds `heavy-slot-1` and the next
  run waits up to 90 min — check `heavy-grants.log` for a GRANT with no END, and clear the stale slot (log a `super
  CLEAR`). Light checks (`format:check`, `check:links`, `check:conflicts`, the shared build) need no grant; under 4 GB
  free the script makes them wait for nothing.
- **A long API lane failing with 500s and connection drops** was Postgres under memory pressure, not the branch: run
  the failing files alone on the branch and on `main` before believing a regression.
- **PowerShell 5.1's `Tee-Object` writes UTF-16 logs** — read them with a converter, not `grep`.
- **Python heredocs:** a `\a` / `\0` in a non-raw string becomes a BEL / NUL byte (it broke this file once) — write
  paths with `chr(92)` or a raw string, and check for control characters after any scripted write.

- **Free executors skip heavy checks and go red:** OpenCode's PR went red three times in CI (an import, lint
  boundaries, Prettier) because its prompt let it skip lint and typecheck "if memory allows". For OpenCode / Codex:
  **lint, typecheck and format are mandatory after every commit**, the full verification before the push, and a
  context limit (handoff at 75 %). The Claude-plans / Codex-executes trial (CONTACT_RULES) is judged by its PR.
- **Watchers:** treat `gh` network errors ("api.github.com", "timeout") and "no checks reported" as retry, never as
  red; fire on a report only when it is complete (not on the file's first appearance); never edit a running bash
  watcher script — write a new one.
- **Production's rate limits:** checking a fake reset token repeatedly hit the live site's limit; capture states
  locally with the API's answer set in the browser (`Fetch.fulfillRequest`), never by a database write.
- **The browser pane hidden:** screenshots time out; read the page with `javascript_tool` measurements, or render
  with headless Chrome (`--screenshot`) through the grant script.
- **A worktree's files may be CRLF while git stores LF** (`eol=lf`): normalise before exact-string edits.
- **A hidden browser pane draws no frames** (2026-11-19): `requestAnimationFrame` and `ResizeObserver` never fire
  there, so anything measured by them (`ScrollRegion`'s tab stop) reads as broken. Show the pane
  (`mcp__ccd_view__show_pane` › `preview`) before an axe or layout check, and confirm a frame fires first.
- **Design (2026-11-19, the owner's verdict after six rejected coded designs):** design is settled as **pictures,
  by the supervisor himself, with the owner, in short loops** — never a worker's coded round judged afterwards. Start
  from real references the owner points at, then grayscale layouts, then colour; one change per loop, shown at once.
  Separate the **product rules** (Arabic RTL, v1 scope, no fake data, accessibility) from the **taste constraints**
  piled up across rounds (no photo, no product glimpse, the berry only as a mark, an ink panel, the Strip's rules):
  the second kind narrowed every design to "a form and a decorative slab" and is reopened with the owner, never
  enforced silently. The design system follows the approved picture, not the other way round.
- **The prototype server dies with the app's idle:** `proto` (5410) was stopped by the app while the owner was away;
  restart it with `preview_start` before giving him links. The in-app pane is ~900 px wide — the auth panel needs
  1280+: send the owner links for his own Chrome, full screen.
- **Design with the owner:** he decides by looking; offer options with a recommendation and a reason, keep each round
  small, and let him check in the browser himself when he says so.
