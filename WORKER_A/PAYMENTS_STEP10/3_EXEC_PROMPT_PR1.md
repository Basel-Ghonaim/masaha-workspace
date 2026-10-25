# PAYMENTS_STEP10 — execute PR 1 only (`feat/payments`, screen 17)

You are worker A's **executor**, in a fresh conversation. You did not plan this item and you will not review it.
**The plan is approved; do not re-decide anything in it.** **PR 1** is the plan's PR 1, commits 1–4: the days' words
shared; **the owner's void of a payment** (from the payments page and, S10, from a subscription's statement); **the
owner's payments ledger** (screen 17, its filters, opening on today); and **reception's «دفعاتي اليوم»**. Web only
(`apps/web`, `docs`); the API is built (#114).

## 0. The rule for this run — no stop until ready for review

**The owner's autonomy rule applies to the whole run** (`C:\dev\masaha\workspace\_SHARED\AUTONOMY_2026-10-25.md` —
read it first; the plan's §13 *Decide and record* applies it to this item). You do not stop and you do not ask until
the work is **ready for review**: the PR open, CI green on its pushed head, `CLEAN`, the report written, the final
reply sent. Every "stop and ask" becomes **decide, record under *Decisions taken without the owner*, continue**. A
command or lane you cannot run → find the root cause (up to three tries; Docker Desktop not running: `Start-Process
"C:\Program Files\Docker\Docker\Docker Desktop.exe"`, then wait for `docker info`), else COULD NOT RUN with the exact
error, continue, CI judges. A real-run case the data cannot hold → not performed, with why and the test that proves
it. **The hard limits hold:** never merge, push to `main`, force-push another branch, create an Issue or delete a
remote branch; never change data through the app, API or database to pass a case beyond the plan's named writes,
never reseed; never touch worker B's worktree (`C:\dev\masaha\app-b`), databases (`masaha_b_*`) or port 3321; never
skip or weaken a test, config, timeout or lane; never print a secret, a password or a demo phone number; no tool
attribution. **Never stop for the file count** (the plan says ≈ 83) — report it.

## 1. What to read — and only this

The owner's instruction overrides the bootstrap's session checklist for this task, stated here: **do not run the
`start-work-item` skill** and do not read `docs/development/workflow.md` whole. `CLAUDE.md` is already in your
context. Read only:

1. `C:\dev\masaha\workspace\WORKER_A\PAYMENTS_STEP10\2_PLAN.md` — **these parts only:** the owner's approval note at
   its top (binding, it wins where the plan differs) and the header; §1; §2 *Scope*, *Acceptance criteria* and *Out of
   scope* for **PR 1**; §3; §4; §5 as it touches PR 1 (S1, S7, S8, S10 above all); §6's lines for PR 1 (and finding
   165, recorded in PR 1 by the approval note); §7 *PR 1 — payments* (the design issues, approved); §8 *PR 1*'s
   files; §9's opening and *PR 1 · Commits 1–4* (the interfaces and the words); §10 *PR 1* (the tests and their
   breaks); §11's PR 1 focus; §12's PR 1 rows; §13 (every part for PR 1: first checks, per commit, on the head, the
   real run's **PR 1** writes, push and the PR, *Decide and record*).
2. In the repository: the code and documents a step touches, when that step needs them — search first (`git grep`),
   then read the section, not the whole file. The `open-pr` skill may help at the end.

Read each file once. A document a step proves to need: read the part it needs and say so in the report.

## 2. Then begin

1. **Preconditions:** #124 merged (`origin/main` = `39ef0504` or later). The owner moved `C:\dev\masaha\app` to
   `main` (clean, pulled) and cleaned #124's branches. Check `git status --short` empty and `git log -1` at
   `origin/main`; `npm run build -w @masaha/shared`; in `apps/api` `npx prisma migrate status` → up to date (else
   `migrate deploy` + `generate` on `masaha_dev`, and say so).
2. **§13's first checks for PR 1**, each with its fallback; the base diff from `e6737da5` to `origin/main` (#124: what
   the plan read as merged, at `5682764b`).
3. **Worker B runs beside you:** FINANCE_AUDIT PR 1 (`feat/audit-log`: `apps/api`, `packages/shared`, documents; no
   `apps/web`). Shared documents only (`api-contract.md`, `v1-mvp.md`, `overview.md`, `docs/README.md`, the findings
   index — B records 151 and 152, you 165): each side keeps its own lines; whichever merges second rebases. Its API
   lanes may overlap yours: before each full lane, record the free memory and whether a `vitest` of
   `C:\dev\masaha\app-b\` runs; never stop its processes; a lane killed for memory is re-run once when quieter, then
   CI judges.
4. **Build PR 1 as §13 says:** the branch `feat/payments` from the latest `origin/main` (`--no-track`); commits 1–4;
   per commit `lint`, `typecheck` and the touched test files, each test red before its code; on the head once
   `test:unit -w @masaha/web`, the scoped `test:component` (the folders the PR touches, named in the report), the
   production build (`$env:NODE_ENV='production'`), `check:build`, `check:classes`, `format:check`, `check:links`,
   `check:conflicts`; every break of §10 *PR 1*, its red output recorded, restored **from a backup copy** (never `git
   checkout -- <file>`); finding 87's family as the plan says (a local miss of only those, each passing alone → CI
   judges).
5. **The real run** (§13's PR 1 cases and its **named writes**: the two ₪1 payments and their voids, with their demo
   accounts and ids), real screenshots by local headless Chrome over CDP (the model:
   `C:\dev\masaha\workspace\WORKER_A\_DONE\DESK_SCREENS\scripts\run3.mjs` on `cdp3.mjs`; Enter with `text: '\r'`; the
   script **never keeps an `/auth/` request's body**), as the owner and as reception, Arabic light and English dark at
   390, 768 and 1440, to this folder's `shots\pr1\` — never inside the repository.
6. **`#PRNUM`, push, the PR:** replaced per commit tree by a self-checking script (the model:
   `C:\dev\masaha\workspace\WORKER_A\_DONE\DESK_SCREENS\scripts\prnum4.sh`, its branch adapted), the next number
   checked just before the push with `gh api "repos/Basel-Ghonaim/masaha/issues?state=all&per_page=1" --jq
   '.[0].number'` plus one — **Issues share the numbers** (#125 and #126 are the two tracking Issues, so the next PR
   is #127 or later; `gh pr list` alone would miss them); **after `gh pr create`, compare the number it
   answered with the commits'** — if worker B opened first, redo `#PRNUM` on your own branch and push with
   `--force-with-lease=feat/payments:<the sha you pushed>`. The PR: title `feat(payments): list the space's payments`,
   `--assignee @me --label feat --label area:web --label area:docs`; CI green and `CLEAN`; the conflict check against
   any open PR. A red CI lane → find why, fix, fold, push again.
7. Write nothing outside the repository except this folder's `4_REPORT_PR1.md`, `shots\` and `scripts\`.

## 3. Discipline

Write `4_REPORT_PR1.md` **as you go** (after the first checks, each commit — sha, subject with its length, the red
line, the green line —, each break, each decision taken, the real run, the push, CI). Keep long outputs in
`scripts\` and read exit codes. Stage by path (never `-A` or `.`); each commit message written to a UTF-8 file
**without a BOM, LF line endings**, with a body saying why, `git commit -F <file>`; subjects ≤ 50, your count
decides; **no tool attribution**; **no `fixup!`, `style:` or `wip` commit left** — a fix folds into its commit
(`--fixup` + `GIT_SEQUENCE_EDITOR=:` autosquash); **no rebase left in progress**; `git status --short` clean at the
end; both servers stopped by process id, ports 3320 and 5320 free; name every local `backup/*` branch you leave.
Never claim a result you did not see: copy the line, read the exit code.

## 4. Your final reply — this shape

```
Status: READY FOR REVIEW | INCOMPLETE (only if nothing at all could continue)
PR: #<n> <url> · head <sha> · CI <green/red> · <CLEAN/not CLEAN> · files <count>
Commits: <sha> <subject> (<chars>) — one line each
Findings: 165 (recorded) — <its file>; any other, numbered
Ran and passed: <each command, with the result line you saw>
Ran and failed: <each, what failed, what you did>   (or "none")
Not run locally (CI judges): <each lane, and CI's result on the head>
COULD NOT RUN: <each, the exact command, the exact error, why>   (or "none")
Breaks: <each: red seen / NOT red (why, and the break made instead)>
First checks: <each of §13's checks for PR 1>
Real run: <each case and its screenshot, or NOT PERFORMED with why and its test>
Network log: <the void's request: its key or none, its body; the ledger's queries>
Data left in masaha_dev: <each write, with ids>
Open PRs and merge order: <worker B's PR, shared files, which merges first>
Departures from the plan: <each, with its reason>   (or "none")
Decisions taken without the owner: <each: met, options, chose, why, undo>   (or "none")
Leftovers: <backup/* branches left; "no rebase in progress" checked>
Report: C:\dev\masaha\workspace\WORKER_A\PAYMENTS_STEP10\4_REPORT_PR1.md
```
