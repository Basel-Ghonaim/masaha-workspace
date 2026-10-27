# Masaha — the main supervisor's handoff (2026-10-26, evening)

You are taking over as the owner's **analyst and control room** for Masaha — the **main supervisor**. This file
supersedes the 2026-10-25 handoff (archived as `_SHARED\HANDOFFS\HANDOFF_2026-10-25.md`, the record of #118–#121).
This file covers #122–#124 and the two plans in flight.
Your auto-memory loads too; the repository and this file win. **Read this file whole, then the *Status log* of
`DESIGN\ROUND2\HANDOFF_DESIGN_81.md`, then `BOARD.md`.**

## 0. The supervisors

| Supervisor | Its one job | Its file — read its *Status log* at the start of every conversation |
|---|---|---|
| **You — the main supervisor** | workers A and B: analysis, plans, approvals, prompts, verification, reviews, merges, documents | this file |
| **«مشرف مراجعة التصميم #81»** | design review round 2: 40 reviews, summaries, `DECISIONS_ROUND2.md`, Issue #81 | `DESIGN\ROUND2\HANDOFF_DESIGN_81.md` (last entry 2026-10-20; idle) |

A **logo worker** may run in `C:\dev\masaha\app` (read-only) with the owner, on its own handoff
`TASKS\LOGO\HANDOFF_LOGO.md`. It is **not yours**: the owner brings its `LOGO_DECISION.md` to you when the logo
is ready, and you turn it into a Work Item then.

## 1. Your role and how you speak

- **Arabic** with the owner; **English** in every prompt and plan. Arabic replies: no line starts with an
  English word or a code token; decisions as items with options and a recommendation, never tables; short.
- You run in `C:\dev\masaha\app` but **never edit the repository**. Read-only git and `gh`; you write in the
  workspace (prompts, approval notes, carried files, scripts, `BOARD.md`, this file). **Merge only with the
  owner's word** (he often merges himself and gives you the result). The safety classifier may refuse you a
  force-push: the owner approved one on 2026-10-24 for a fixup squash (`--force-with-lease=<branch>:<sha>`);
  otherwise give him the commands.
- **An approved merge also means:** `gh pr merge <n> --merge --match-head-commit <sha>`; delete the branch
  (remote and local) and its `backup/*` branches; move the worker's worktree to the new `main` (`app`: `git
  switch main` + `pull --ff-only`; `app-b`: `git switch --detach origin/main`); `npm run build -w
  @masaha/shared`; after a schema change `npx prisma migrate deploy` + `generate` on that worker's database
  (another worker's database only when that worker is idle — or put it in that worker's next prompt); update
  `BOARD.md` and this file. Give the owner the commands when he merges himself.
- **Verify every worker report in the code before believing it:** head, `gh pr checks` green, `CLEAN`, each
  subject ≤ 50 with a body, no tool attribution, no `fixup!`/`style:`/`wip` commit, **no rebase left in
  progress**, no `#PRNUM` left, scope (files), migration SQL read, the claims that matter; spot-check a
  reviewer's top finding before acting on it.
- **Cost:** keep conversations short; read each file once; start a new conversation from this file when one
  grows long.

## 2. State (start here)

> **Now — 2026-10-27 (this block wins over the 2026-10-26 state below, kept as its record):**
> - **`main` = `39ef0504`** — **#124 merged** after its fix round (F1–F6 folded, verified by the supervisor in the
>   code; no second review). **The DESK_SCREENS plan is complete.** Finding 171 stays Open: **ask the owner to
>   confirm** the provisional choice (prices re-read on opening, the toast states the server's amount). Remote
>   branches: `main` and the old `feat/admin-owners` only.
> - **Finished task folders moved to `_DONE`:** `WORKER_A\_DONE\{DESK_SCREENS,OWNER_SETUP,OWNERS}`,
>   `WORKER_B\_DONE\{ANNOUNCEMENTS,DEMO_SEED,DESK,DESK_API,PAYMENTS,SUBSCRIPTIONS}` (paths in this file and the active
>   plans rewritten). Active: `WORKER_A\PAYMENTS_STEP10`, `WORKER_A\PUBLIC`, `WORKER_B\FINANCE_AUDIT`.
> - **Both plans approved** (the owner accepted every recommendation; the approval notes at the top of each
>   `2_PLAN.md`): **FINANCE_AUDIT** (worker B, 3 PRs: audit → platform settings → finance; finding 152 recorded in PR
>   1) and **PAYMENTS_STEP10** (worker A, 5 PRs: payments → announcements → data reports → 4a report → 4b favourites;
>   finding 165 recorded in PR 1). **Both executions run under the autonomy rule, no stop until ready for review.**
> - **PR 1's execution prompts are written; the owner launches the two workers in parallel:**
>   `WORKER_B\FINANCE_AUDIT\3_EXEC_PROMPT_PR1.md` (in `app-b`) and `WORKER_A\PAYMENTS_STEP10\3_EXEC_PROMPT_PR1.md`
>   (in `app`). When each replies: verify (§1's list), show the owner its decisions, then the review — **Claude** for
>   B's PRs and for A's PRs 1–2, a free model for A's 3, 4a, 4b — on this conversation's model and effort.
> - **Tracking Issues, the owner's request:** **#125** (FINANCE_AUDIT) and **#126** (PAYMENTS_STEP10) — a paragraph
>   on the plan, then one checkbox per PR with a short paragraph. **Tick a PR's box when it merges** (fetch the body
>   to a file, edit it with a script, `gh issue edit <n> --body-file`, read it back). **Issues take numbers too:** the
>   next PR is #127 or later — the prompts check with the issues API, not `gh pr list`.

**`main` = `e6737da5`** (#123 merged). Merged 2026-10-26: **#122** (DESK_SCREENS PR 3, the customers list and file,
edit / archive / restore, the statement and the end, the idle line; light Claude review: F1–F4 → carried into PR 4),
**#123** (ANNOUNCEMENTS PR 4, the closure extension; migration `closure_extension_key` with its trigger; Claude review:
mergeable — finding 151 and three nits → `WORKER_B\FINANCE_AUDIT\0_CARRIED_FROM_123.md`). **The ANNOUNCEMENTS plan
(step 10's API) is complete.** Open: **#124**. Remote branches: `main`, `feat/subscription-sheet` (#124), the old
`feat/admin-owners` (ask before deleting).

**Right now all three are working — the owner launched them:**

1. **Worker A — #124's fix round** (`C:\dev\masaha\app`, ports 3320/5320, `masaha_dev`). #124 = DESK_SCREENS PR 4,
   the subscription sheet (head `bc8fe86a` before the round, 70 files, CI green, CLEAN). Its Claude review
   (`WORKER_A\_DONE\DESK_SCREENS\6_REVIEW_PR4_CLAUDE_CODE.md`): mergeable after a fix round — F1 (a lost subscribe answer
   told as "not saved", inviting a second subscription — **money**, confirmed), F2 (the sheet's focus after a «⋯»
   item), F3 (a published-price renewal preselects the first price — **money**, confirmed), F4 (test 72 cannot
   fail), F5–F6 nits. **The owner: all six fixed now, none carried.** Its prompt `WORKER_A\_DONE\DESK_SCREENS\
   7_FIX_ROUND_PR4.md`: rebase on #123 first (merged now), each fix folded into its commit, **only the touched test
   files locally — no full lane; CI judges**, no real run, the autonomy rule, no stop until ready for review.
   **When it replies:** verify (§1's list: the new head, CI green, CLEAN, no `fixup!`, no rebase left, subjects, the
   folds), read its decisions, and judge F1–F6 in the code; a second review only if the owner asks. Then merge on
   the owner's word and clean (`backup/subscription-sheet-pre-prnum` among the branches). **The DESK_SCREENS plan
   ends with #124.** Finding 171 stays Open: the sheet re-reads prices on opening and the toast states the server's
   amount — the supervisor's provisional choice under the autonomy rule; **the owner has not confirmed it yet** —
   ask him.
   - The run's slip: two extra renewals (subscriptions 5 and 6) left in `masaha_dev` — the owner may end them or
     reseed; never by the supervisor without his word.
2. **Worker B — planning FINANCE_AUDIT** (step 11's API: the audit reader, platform settings, finance; three PRs in
   that order). The owner's 12 decisions are in `WORKER_B\FINANCE_AUDIT\1_PLAN_PROMPT.md` (binding: income = cash
   collected without voids; Gaza months and fixed windows, no free range; the server aggregates; CSV built by the web,
   no export route; finance the owner's alone; occupancy from closed stays, auto check-outs included; the owner's audit
   shows the admin as Masaha; the admin's per AD-028; kept for ever; the contact details into the typed catalogue,
   finding 40; finding 151 option A). PR 1 opens with `0_CARRIED_FROM_123.md` (finding 151: the extension moves a
   covered subscription's not-yet-started renewal chain; a retried key kept to its space; two document fixes). The
   planner started before #123 merged and read `origin/feat/closure-extension` as merged — **the same tree as `main`
   now** (`git diff ff8743c8 e6737da5` is empty); fix its header's base in the approval note. B's findings: **151**
   (the carried file's), the item's own from **152**. **When `2_PLAN.md` arrives:** check its key claims in the code,
   show the owner its decisions (items with options and a recommendation), write the approval note at its top, then
   PR 1's execution prompt (two-phase if PR 1 has a migration; the autonomy rule if the owner says so for the run).
3. **The design worktree (`C:\dev\masaha\app-design`, read-only) — planning worker A's next item, PAYMENTS_STEP10**
   (steps 9–10's screens: PR 1 payments — the owner's list and the void, «دفعاتي اليوم»; PR 2 announcements with the
   extension; PR 3 data reports, owner and admin; PR 4 the user's side — favourites, my reports, the report dialog,
   the space page's announcements, the favourite action). The owner's 6 decisions in `WORKER_A\PAYMENTS_STEP10\
   1_PLAN_PROMPT.md`: one item, four PRs in that order; PR 4 last, before or after the public fix PR; finding 8's
   filter tag in the first PR that uses it; **Claude reviews PRs 1–2, a free model PRs 3–4**; **every execution
   under the autonomy rule, no stop until ready for review**. PR 1 starts after #124 merges. A's findings from **165**.
   **When `2_PLAN.md` arrives:** as for B's.

**Still open, not running:**
- **The public site's fix PR** (worker A): `WORKER_A\PUBLIC\0_CARRIED_FROM_111.md` + the owner's in-person review
  (still open) + his page-change jump find. Never block other work on it; it runs before or after PAYMENTS_STEP10's
  PR 4 (the owner's decision 3).
- **Issue #72** (the editor's DI-27 comment in `docs/design/prototype/Admin space edit.html`): a one-file design task,
  **postponed by the owner** (2026-10-26). Memory: the prototype's shared globals (`_excluded`) may still break
  `ActionButton` after the editor's modules — check in a browser before dropping the workaround.
- **The owner's test environment** (`app-review`, `TASKS\HOME_REVIEW_ENV\`): moved by the owner to `3855e37f` (#122)
  — his `DirectoryResults.tsx` experiment kept, never discard it; updating it to `e6737da5` needs `migrate deploy`
  (#123's migration). Ports 3324/5324; accounts in `app-review\REVIEW_ACCOUNTS.md` (never print them).
- **Step 12** (the overviews) follows step 11; the owner's rule that the overview shows no amounts (DECISIONS_OWNER's
  top note) stands.

**Progress:** steps 1–10's APIs built; step 11's API planning; the desk's screens (steps 7–8) built but #124;
steps 9–10's screens planning; the public site built (its fix PR pending the owner's review).

## 3. The owner's standing rules (put them in every prompt they touch)

- **Review verdict:** a serious or large fix reopens its PR (fixes folded into their commits); small ones go to
  the **next PR's first commit** through `0_CARRIED_FROM_<n>.md` in that PR's folder, named in its description.
  A merged PR's review with a **critical** finding → a fix branch at once (as #110).
- **Reviews — who:** the owner chooses. **Free models (Codex, OpenCode)** for web PRs: self-contained,
  read-only prompts with a mandatory checklist (models: `WORKER_A\_DONE\DESK_SCREENS\5_REVIEW_PROMPT_PR1A.md`,
  `…PR1B.md`) — **verify their findings in the code before acting**: OpenCode over-states (it listed "no change
  needed" points as findings and misread TanStack's defaults); Codex was precise. **Claude reviews** for the
  backend, money, auth and schema (headless, below).
- **Memory:** a full lane killed for low memory is re-run once when quieter; killed again → CI judges. **A
  command timeout is not a memory kill:** `test:api` takes ≈ 10 minutes — prompts say "no command timeout".
- **Finding 87's family** (slow first lazy imports, 3 s): `routes` › "lists the owner's eleven pages" and
  "lists reception's four pages", the two site tests opening `/spaces`, `App` › "renders the main landmark",
  `router` › "shows the root's general error…" — locally missed and alone-passing → CI judges.
- **Never leave silently:** an executor that would leave a carried item or a review nit undone stops and asks.
- **Demo data:** a case the data lacks → stop and report; never change data through the app to pass it; a
  reseed only on the owner's word. Real runs name every write.
- **Fix rounds** run **only the touched test files** (plus lint and typecheck), each fix folded into its original
  commit; **a full lane locally is forbidden** in a fix round — CI judges (the owner, 2026-10-26). A fix round fixes
  every finding of the review unless the owner carries some.
- **The autonomy rule** (`_SHARED\AUTONOMY_2026-10-25.md`): when the owner says so for a run — and by default for
  every PAYMENTS_STEP10 execution — the executor never stops until ready for review (PR open, CI green, CLEAN,
  report); decisions are recorded under *Decisions taken without the owner*, which you show him. "Ready for review"
  includes opening the PR and CI; stopping before the PR was not adopted.
- **The PR number:** with two workers pushing, each prompt says: check the next number just before the push, and
  after `gh pr create` compare it; if it differs, redo `#PRNUM` on its own branch and `--force-with-lease` it.
- **Simple tasks go to non-Claude-Code models** (chores, seed, documents, environment setup): self-contained
  prompts, PowerShell, exit codes read; the supervisor reviews their plans and writes corrections at the plan's
  top (the model: `TASKS\CONFLICT_GUARD_BASEL\2_PLAN.md`, `TASKS\DEMO_DAILY_BASEL\2_PLAN.md`).
- **Exceptions the owner granted:** #115's 52-character subject (one-off); #116's 90 files in one PR.
- **No stop for size (2026-10-26):** an executor never stops to ask about the file count; it carries on and
  writes the count (and, past the plan's estimate, why it grew) in its report and reply; the supervisor tells the
  owner. Every execution prompt says so.

## 4. The method

- **One Work Item:** analysis with the owner in Arabic → a **planning prompt** (English, plan only, no trial
  build, read from `app-design`'s commit objects; the planner may challenge decisions in *Proposed
  alternatives*) → the plan → your review (check its key claims in the code) → the owner's decisions → an
  **approval note at the plan's top** (binding) → an **execution prompt per PR** (closed reading list, skip
  `start-work-item`, the stop rule, the standing rules, the final-reply template with COULD NOT RUN) → the owner
  launches → you verify → a review → the verdict → merge on the owner's word → clean.
- **Two-phase executors** for auth/schema items: a short plan, stop, your approval note, then the build (the
  model: `WORKER_B\_DONE\DESK_API\3_EXEC_PROMPT.md` and its `2_PLAN.md`'s note).
- **Claude reviews**, headless and read-only from `app-design`:
  `cd /c/dev/masaha/app-design && "/c/Users/basel/AppData/Roaming/npm/claude" -p "Read <5_REVIEW_PROMPT…> whole
  and do it." --add-dir 'C:\dev\masaha\workspace' --strict-mcp-config --no-chrome --settings
  'C:\dev\masaha\workspace\_SHARED\worker-settings.json' --allowedTools "Bash(git *)" "Bash(gh *)" Read Grep
  Glob Write Edit > <folder>/review_<pr>_session.log 2>&1` with `run_in_background` (the log stays empty until it
  ends; ≈ 20–40 minutes; it dies with your session). **The owner's choice (2026-10-26): reviews run on the
  supervisor conversation's own model and effort** — read them with `get_session self` and pass `--model <id>
  --effort <level>` (today `claude-opus-5-5`, `medium`). Models: `WORKER_B\_DONE\ANNOUNCEMENTS\5_REVIEW_PROMPT_PR4.md`,
  `WORKER_A\_DONE\DESK_SCREENS\5_REVIEW_PROMPT_PR4.md`; a light review on chosen axes: `…\5_REVIEW_PROMPT_PR3.md`.
  Launch a review only once every check on the head is green (`gh pr checks <n> --watch` in the background).
- **Watching workers while the owner is away:** `_SHARED\scripts\watch_ready.sh <deadline epoch>
  <name>=<branch>=<report>…` in the background (every 10 minutes; ready = PR open, checks all passed, CLEAN, the
  report naming the PR and unchanged for one interval; the owner's limit was 2 hours); on READY, verify and launch
  the review.
- **Models of the other files:** execution prompts `WORKER_A\_DONE\DESK_SCREENS\3_EXEC_PROMPT_PR2.md`,
  `WORKER_B\_DONE\PAYMENTS\3_EXEC_PROMPT.md`; carried files `WORKER_B\_DONE\ANNOUNCEMENTS\0_CARRIED_FROM_118.md`,
  `WORKER_A\_DONE\DESK_SCREENS\0_CARRIED_FROM_117.md`; planning prompts `WORKER_A\_DONE\DESK_SCREENS\1_PLAN_PROMPT.md`,
  `WORKER_B\_DONE\PAYMENTS\1_PLAN_PROMPT.md`; approval notes at the top of `WORKER_A\_DONE\DESK_SCREENS\2_PLAN.md` and
  `WORKER_B\_DONE\PAYMENTS\2_PLAN.md`.
- **Workers are launched by the owner:** `cd C:\dev\masaha\app[-b]` → `claude --add-dir
  C:\dev\masaha\workspace --strict-mcp-config --no-chrome --settings
  C:\dev\masaha\workspace\_SHARED\worker-settings.json` → "Read <prompt> whole and execute it." (Opus; high
  effort for money/security unless the owner picks medium with a two-phase prompt).

## 5. Ledgers

- **Open decisions:** `_SHARED\OPEN_DECISIONS.md` — point 2 built (#123, its *Built as* line written), point 4
  built (#118).
- **Open Issues:** #72 (postponed by the owner), #81 (design round 2). #71 closed by #113.
- **Findings:** on `main` 150 (accepted), 160–164, 170, 171 (Open; the owner to confirm the provisional choice).
  151 is FINANCE_AUDIT PR 1's (resolved there); B's own next free **152**; A's next free **165**.
- **The owner's in-person review of the public site:** open; its fixes go to the public fix PR.
- **Design decisions:** `DESIGN\DECISIONS\` — the logo (foundation §15 row 5) is the one open visual decision,
  handled by the logo worker.

## 6. The workspace

`C:\dev\masaha\workspace\`: `WORKER_A\`, `WORKER_B\`, `DESIGN\`, `TASKS\`, `_SHARED\`; one folder per task;
`BOARD.md` (keep it true). A task's files: `0_CARRIED_FROM_<n>.md`, `1_PLAN_PROMPT.md`, `2_PLAN.md`,
`3_EXEC_PROMPT[_PR<n>].md`, `4_REPORT[_PR<n>].md`, `5_REVIEW_PROMPT…`, `6_REVIEW_…`, `shots\`, `scripts\`.
Backup: private repo `Basel-Ghonaim/masaha-workspace`, nightly 23:00.

## 7. Hazards and lessons (put them in prompts)

- **Leftovers an executor may leave:** a `fixup!` commit (#113), a rebase in progress (#113's worktree), backup
  branches — prompts forbid the first two and ask the names of the third; check `git status` for a rebase.
- **No PR number in a migration's SQL** (the `#PRNUM` rewrite changes an applied checksum; #114) — now a rule in
  `data-model.md`. Executors run `migrate dev --create-only` once; non-interactive → `migrate diff --script`.
- **Plans predate merges:** each execution prompt names the merged changes the plan did not know (as PR 1b's
  did for #114's wider uncollected list) and tells the executor to adapt to the contract or stop.
- **Two workers on the same documents:** text conflicts only so far (desk.md, the findings index); whichever
  merges second rebases, keeping both sides.
- **`app-design`'s working tree is old:** workers there must read `origin/main`, not the files (the conflict
  guard's planner read the old tree).
- **Writing workspace files from Python:** a backslash before a digit or letter becomes a control character
  (`\2` corrupted the board on 2026-10-24) — use the editor tools, or `chr(92)`, and assert no control characters.
- **CDP real runs:** Enter with `text: '\r'`; the network log proves one key across an offline retry.
- **`git checkout -- <file>` loses uncommitted work** (worker A, PR 3, 2026-10-25: it reset `desk.md`; re-applied
  by its script) — prompts say: restore from a backup copy, never checkout.
- **Size bounds:** web PRs grow past the plan's estimate when a shared control (the «⋯» menu) reaches several
  screens; the owner granted 65 (#119) and 81 (PR 3). Since 2026-10-26 no prompt stops on size (§3).
- **A transaction's reads go through its `tx`** (conventions §8): #121's save read the listing on other pool
  connections while holding the user's lock (pool of 10, no `max`) — reviewers look for it.
- **The demo seed renews its day-bound states on every run (#115)**, so FULL and closed-today hold today after
  `$env:SEED_DEMO='true'; npm run db:seed` (it needs the `SEED_ADMIN_*` variables).
