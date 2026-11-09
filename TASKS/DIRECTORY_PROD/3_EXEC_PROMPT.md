# DIRECTORY_PROD — EXECUTE the approved plan (fresh session)

You are a **Claude Code executor** on **Masaha**, in **`C:\dev\masaha\app`**, in a fresh conversation. Another session
wrote the plan; the owner approved it. You **build it, verify it, open the PR, and stop when CI is green** — you do not
re-plan and you never merge. **Model Opus 5.5, effort high.**

## 0. Read first, in this order

1. `CLAUDE.md` (in your context) and `docs/development/workflow.md`, `docs/development/testing.md`,
   `docs/development/engineering-principles.md`.
2. **The plan, whole: `C:\dev\masaha\workspace\TASKS\DIRECTORY_PROD\2_PLAN.md`** — it is your specification: the
   binding decisions (§4), each item as built (§4.2), the stronger decisions (§5), findings (§6), `SegmentedControl`
   (§7), files (§8), design issues (§9), the test matrix (§10), review focus (§11), executor checks (§12), risks (§13),
   the five commits (§14), verification (§15).
3. **The owner's decisions:** `C:\dev\masaha\workspace\TASKS\DIRECTORY_PROD\0_OWNER_DECISIONS.md` — items 1–15 and
   the section «The plan's open decisions»: **OD1 (a), OD2 (a), OD3 (a), OD4 (a), OD5 (a), OD6 (a), OD7 (b)** — every
   one as the plan recommends. Where the plan says "if OD… (a)/(b)", take the approved branch and drop the other.

Do **not** run the `start-work-item` or `write-plan` skills (the plan exists and is approved). Do run **`open-pr`**
and **`final-report`** at their moments (§3).

## 1. Start

- `git status` must be clean and the branch `main`. `git fetch origin` and `git switch -c feat/directory-filters
  origin/main` (`40cb481d` or later; if `main` moved, read what changed and say so in the report).
- **Never `db:seed` `masaha_dev`** (it holds the presentation's data). `test:api` uses the test database.
- No migration is planned; if one becomes necessary, **stop and ask** (an owner's decision).

## 2. Build — no stop until the PR is ready

- Follow the plan's §14 commits (Conventional, atomic, subject ≤ 50 characters, a body; the first commit is finding
  214 and #136's two nits). Stage **by path**; never `git add -A` / `git add .`; no tool attribution anywhere.
- **Tests — the owner's bar:** they must work and point the right way, never bent to pass; the filters' tests have no
  gap. Build every `T…` of §10; a test written before its code should fail first where that is possible. Never weaken,
  skip or loosen a test to get green; never add production code only a test uses (inject time and other seams the way
  the codebase does). Finding 214: the fix waits for content only the Directory has and expects exactly one search
  box — prove it with **three full `test:component` runs**, not the file alone.
- Run every executor check of §12 and act as each says; record each outcome for the report.
- If something in the plan proves wrong in the code: choose the safest reading that keeps the owner's decisions, write
  it down (the report's "Deviations"), and continue. **Stop and ask only** for a migration, a new dependency, a change
  to an owner's decision, or anything that would touch the parallel tasks' areas (§8's overlap list).

## 3. Verify, open the PR, wait for CI

- **Complete local verification before any push** (§15): `lint`, `typecheck`, `format:check`, `check:classes`,
  `check:links`, `check:conflicts`, `build` then `check:build` (build with `NODE_ENV=production`), and **`test:unit`,
  `test:component`, `test:api` in full**. Two full lanes may run at once with 8–10 GB free; a third waits. **A lane
  killed for memory: retry once; if killed again, CI judges** — say so in the PR and the report.
- Screenshots of the directory (the panel, the price, «الدوام», the cards' price and by-hours badge, a space without
  hours, the sheet on a phone): RTL and LTR, light and dark, phone and desktop, to
  `C:\Users\basel\Downloads\directory-prod-shots\` — never pushed. If the Chrome extension is unavailable, use headless
  Chrome over CDP against the local dev server.
- Then the **`open-pr`** skill: the PR number is expected to be **#138** (check the next number just before the push;
  no `#PRNUM` left), assigned to the owner, labels `feat` + `area:web` + `area:api` + `area:docs` (+
  `area:design-system` for `SegmentedControl`), the description in the workflow's sections, its Evidence naming every
  command run and what was not run, and a "Deviations" section.
- Watch CI with a **bounded** loop (≤ 60 minutes; `gh pr checks`, `gh pr view --json mergeStateStatus`; `gh --jq`,
  never `jq`). A failure this PR caused: fix it, fold it into its commit (`git branch backup/directory-filters-<n>`
  first, `--fixup` + `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash origin/main`), `git push --force-with-lease`.
  A failure it did not cause: retry the job once, then report it.
- When every check is green on the pushed head and GitHub says `CLEAN`: the **`final-report`** skill, written to
  `C:\dev\masaha\workspace\TASKS\DIRECTORY_PROD\4_REPORT.md` — the PR, the full head sha, the commits, the file count,
  every command's result, the executor checks' outcomes, the deviations, the findings recorded, and anything noticed
  outside scope. **Then stop. Never merge; never delete a branch.**
