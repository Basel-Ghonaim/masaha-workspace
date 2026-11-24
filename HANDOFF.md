# Masaha — the main supervisor's handoff (2026-11-24)

You are taking over as the owner's **analyst and control room** for Masaha — the **main supervisor**. This file
supersedes the 2026-11-18 handoff (archived as `_SHARED\HANDOFFS\HANDOFF_2026-11-18_to_11-24.md`: AUTH rounds 4–5,
the free round, the model trial, Stitch, #152, #153). **You may not be Claude:** the rules that lived in Claude's private
memory are in §8 — this file, the repository and `BOARD.md` are everything you have.
**Read this file whole, then `BOARD.md` (its top lines are the newest), then `DESIGN\AUTH\0_OWNER_DECISIONS.md`
(A1–A17).**

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

## 2. State (2026-11-24)

**`main` = `17a51adc`** (#153 merged 2026-11-24; main's CI and Vercel **success**, the live home and `/api/v1/spaces` 200). No open PR. Merged since the last handoff:
- **#152** TABLE_SCROLL (finding 229: every `Table` scrolls in a `ScrollRegion`; #150's C1–C2);
- **#153** TABLE_NAME (a table that fits says its name once: `ScrollRegion`'s `quietWhileFits`; `TableCaption`
  removed; #152's notes).

Nothing is carried to the next PR. Worktrees: `app` (on `main`) and `app-design`. Databases: `masaha_dev`,
`masaha_test`, `masaha_design_test`. Docker and `masaha-postgres-1` may still be running (a worker started them).

**The owner's word for the next session (2026-11-24):** no more small production tasks for now. He will discuss the
next task with the new supervisor.

### A. The design work — where it stands (`DESIGN\AUTH\0_OWNER_DECISIONS.md` A1–A17)

- **Sign in, design B** (A13: ink masthead, two ways in) is still the fixed picture (`DESIGN\AUTH\round5-B\`).
- **Why the rounds were weak (the supervisor's finding, 2026-11-20).** The briefs, not the designers, narrowed every
  round: long ban lists, "choose the safest option", the old design system read before drawing. Round 4's Threshold
  and round 5's B converged on one composition.
- **The owner's rule since then (A14):** a design brief gives **principles, never prohibitions**, and a design worker
  launches from a clean folder (no CLAUDE.md, no memory).
- **The free round (A14–A15):**
  - Claude Code built three directions in `C:\dev\masaha\free-round\`, copied to `DESIGN\AUTH\free-round\`.
  - **Notebook:** rejected ("not professional").
  - **Lights:** the page liked, the map rejected.
  - **Berry:** its berry-to-plum colour liked, its layout, elements and light theme rejected.
- **Design 4, the fusion (A16–A17):** Codex took Lights' structure and Berry's colour, without a map. Its step 1 was
  not convincing, and the fusion stopped there.
- **The model trial (A17):** Codex, OpenCode and Copilot each ran the free round's brief in
  `C:\dev\masaha\design-trials\<tool>\`. Only Copilot finished; OpenCode and Codex were cut by a shutdown. The owner
  judged the trial a waste of time.
- **Google Stitch:**
  - The owner's own web attempt was weak, so he switched to a staged method: the logo and the design system, then
    the base layout, then the page.
  - It is reached through the **Stitch MCP**: `@_davideast/stitch-mcp`, key in `.claude.json` under this project
    (memory `stitch-mcp`).
  - The owner **never signs his Google account into a browser**, and Claude in Chrome is unavailable (his extension
    is on a free Claude account).
  - **Step 1 is done:** project "Masaha sign-in" (`projects/6952382136728417437`), a style sheet of the current
    system in `design-trials\stitch\step1\`. The colours and type are right. The logo became an empty box (the MCP
    takes no images), and it invented a seat count.
- **The owner's next design method (2026-11-22, not started; he paused it for production tasks):**
  - **The worker:** a new Claude Code worker in a new folder inside `C:\dev\masaha\` (name not set; the supervisor
    proposed `studio`). It has **read access to `app` and `masaha-prototype`** but is not bound by their rules or
    documents; writes are blocked by settings, not words. It has its own Stitch MCP, writes Stitch prompts and reads
    the designs, and edits only when the owner asks.
  - **The way of working:** it works step by step in conversation with the owner, never one big brief. The first
    message (written by the supervisor) holds the product's details, a first reading list and the full way of
    working, with **no trace of the earlier rounds**.
  - **Still open for the owner:** whether the identity (logo, ink + berry) is fixed for it, whether it sees the
    earlier designs, and the folder's name.
  - **The settling order the owner accepted:**
    1. the folder and access;
    2. Stitch, tested;
    3. the product's details;
    4. the reading list;
    5. the way of working;
    6. the first message, reviewed by him;
    7. the launch.

### B. GOOGLE_VERIFY — paused by the owner (unchanged since 2026-11-19)

The consent screen's name and logo wait. Google sign-in works for everyone.

### C. The owner's pending items

1. Later:
   - close Issue #81;
   - measure findings 23, 65 and 152 after deployment;
   - E2E at the end;
   - the full project review, on his word.
2. A custom domain (to discuss).
3. **Issue #151** «Design restructure: the design system and the pages a visitor sees» tracks the design work (five
   steps, ticked on merge).
4. **Data notes from the free round** (production's directory data, not code):
   - «جاردن سبييس» and «إليفييت هاب» spellings;
   - Golden Hub filed under North Gaza though it sits in Gaza City.

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
  Sea shots); 229 resolved by #152; 224 by #150; 217, 218, 219, 225, 226, 228 by #149; 220, 222, 223, 227 by #146. The
  next free number is **230** (check the index). Nothing is carried to the next PR.
- **The owner's notes for the refactor:** `REFACTOR_NOTES.md`.
- **Decisions:** each task's `0_OWNER_DECISIONS.md`; `DESIGN\DECISIONS\` (round 2's settled design decisions — round 3
  may overturn them, each said); `_SHARED\OPEN_DECISIONS.md`; `WORKER_B\DEPLOY\0_OWNER_DECISIONS.md`.

## 6. The workspace and the machine

- `C:\dev\masaha\workspace\`: `TASKS\` (active: `GOOGLE_VERIFY`, the owner's step only), `DESIGN\` (active: `AUTH`), `WORKER_A\`,
  `WORKER_B\`, `_SHARED\`; `BOARD.md` (keep it true); `REFACTOR_NOTES.md`.
- **Design folders outside the workspace:**
  - `C:\dev\masaha\free-round\`: the free round's `PROMPT.md`, `PROMPT_4.md` (Codex's fusion), `materials\`, and
    `work\` (Lights, Berry, Notebook, Codex's `fusion\`, the CDP capture tool `work\tools\capture.mjs`).
  - `C:\dev\masaha\design-trials\{codex,opencode,copilot,stitch}\`: the model trial and Stitch's step 1.
  - Neither is a repository. The free round's `work\` is copied into `DESIGN\AUTH\free-round\`.
- **`C:\dev\masaha\masaha-prototype`** — the design repository (public `Basel-Ghonaim/masaha-prototype`); its server
  on 5410 from `app\.claude\launch.json` › `proto` (the launch file also holds `api-app` / `web-app` on 3320 / 5320,
  `api-before` / `web-before` on 3323 / 5323 from `app-design`; it is git-excluded but Prettier checks it — run
  `npx prettier --write .claude/launch.json` after editing it, or a worker's `format:check` fails). Captures: `D:\MASAHA\DT\AUTH\` (the owner's naming
  `<n>-<page>-<width>-<theme>.png`).
  Backup: private repo `Basel-Ghonaim/masaha-workspace`, the task `masaha-workspace-snapshot` at **08:00 and 17:30**
  (catches up at the next boot, runs on battery, retries 3×; a failed push is logged as FAILED). It had silently
  failed from 2026-11-09 to 11-20 (a 1.5 GB commit of browser profiles); repaired 2026-11-20.
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

## 9. Learned on 2026-11-14 → 24

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

- **Design briefs (2026-11-20, A14):** principles, never prohibitions. Past rejections are not passed on as bans.
  Launch a design worker from a folder with no CLAUDE.md: the app's and the prototype's load their fixed points and
  "Never" lists automatically. Never tell a design worker to "choose the safest option".
- **The supervisor is the most constrained designer:** it carries every past round. A fresh worker runs a free round.
- **Headless Chrome cannot lay out a page under 500 px.** `--window-size=390,…` renders 500 px and crops it, so RTL
  pages lose their start. Capture phones over CDP with `Emulation.setDeviceMetricsOverride`
  (`free-round\work\tools\capture.mjs`).
- **Capture scripts must keep their browser profiles out of the workspace,** or under a name the `.gitignore` drops
  (`cdp-profile*`, `chrome-profile*`).
- **Claude Code's memory guard stops a worker's background servers** when free memory runs low. The worker then
  stops, by its rule. Archiving idle sessions and closing Chrome tabs freed about 1 GB (2026-11-22). Put a "restart
  once, else skip the Chrome pass and say so" line in every prompt.
- **The owner's GitHub activity:** he asked for small real production tasks so the day shows activity (#152, #153).
  Never make empty commits for it. Private-repo commits count only if his profile shows private contributions.
- **Stitch:** the MCP takes no images, so a logo has to be placed by hand. Stitch invents data (a seat count): say "no
  numbers, no fake data" in each prompt.
