# SPACE_PROFILE — EXECUTE the approved production plan (fresh session)

You are a **Claude Code executor** on **Masaha**, in **`C:\dev\masaha\app`**, in a fresh conversation. Another session
wrote the plan; the owner approved it on 2026-11-10. You **build it, verify it, open the PRs, and stop when CI is
green** — you do not re-plan and you never merge. **Model Opus 5.5, effort high.**

## 0. Read first, in this order

1. `CLAUDE.md` (in your context), `docs/development/workflow.md`, `docs/development/testing.md`,
   `docs/development/engineering-principles.md`.
2. **The plan, whole: `C:\dev\masaha\workspace\TASKS\SPACE_PROFILE\2_PLAN_PROD.md`** — your specification, starting
   with the **APPROVED** note at its top (every OD as (a); DI-1…DI-8 and SD1–SD7 approved; PA-1/PA-2 not taken; the
   §7 migration approved as shown). Its sections: binding decisions (§4), how each is built (§4.1–4.2), checks (§5),
   dependency (§6), migration (§7), PRs and files (§8), SD (§9), findings (§10), DI (§11), the test matrix (§12),
   review focus (§13), commits (§14), EC (§15), verification (§16), limits (§17), risks (§18).
3. **The owner's decisions:** `C:\dev\masaha\workspace\TASKS\SPACE_PROFILE\0_OWNER_DECISIONS.md` (M1–M4 override
   earlier lines; X1–X3; A3 deferred — build nothing for women / evening).

Do **not** run `start-work-item` or `write-plan` (the plan exists and is approved). Run **`open-pr`** and
**`final-report`** at their moments.

## 1. Two phases

**Phase 1 — PR-A then PR-B, then stop.** Both start from the latest `origin/main` (`7fb73c3c` or later; if `main`
moved, read what changed and say so in the report), each on its own branch:
- **PR-A** `feat/contact-types` (expected **#140**): commits A1–A2 (§14), the one migration (§7, EC5).
- **PR-B** `feat/sortable-list` (expected **#141**): commit B1, the dnd-kit dependency (EC2).
Build A, verify it fully, open its PR; then `git switch` to a fresh branch from `origin/main` for B, build, verify,
open its PR. Wait for CI on both (bounded). When **both** are green and `CLEAN`, write the report (§4) and **stop**.
The reviews and the merges are the owner's.

**Phase 2 — PR-C, only after the owner says both merged.** On his word ("continue"), `git switch main`,
`git pull --ff-only`, `npm ci` (the lock moved with B), `npm run build -w @masaha/shared`, `npm run db:migrate`
if needed, then `feat/space-profile` from `origin/main` (expected **#142**): commits C1–C5. Verify, PR, CI, report,
stop.

## 2. Build — no stop inside a phase

- Follow §14's commits (Conventional, atomic, subject ≤ 50 characters, a body). Stage **by path**; never
  `git add -A` / `git add .`; no tool attribution anywhere; no `fixup!` left.
- **Tests — the owner's bar:** they must work and point the right way, never bent to pass; no gap. Build every `T…`
  of §12; every new test seen failing first (before its code, or by breaking that code once — say which). Never
  weaken, skip or loosen a test to get green; never add production code only a test uses (inject seams the way the
  codebase does).
- Run every `EC…` of §15 at its moment and record its outcome. **Docker must be up** (`npm run db:up`) for EC1, EC5
  and `test:api`. EC1 and EC5 read `masaha_dev` read-only apart from applying §7's migration; **never `db:seed`
  `masaha_dev`** (it holds the presentation's data). `migrate dev --create-only` **once**; `migrate reset` needs the
  owner.
- If the plan proves wrong in the code: choose the safest reading that keeps the owner's decisions, write it down
  (the report's "Deviations"), and continue. **Stop and ask only** for a migration other than §7, a dependency other
  than §6, a change to an owner's decision, or anything touching the palette lab's or the women + evening task's
  areas. **Never stop on file count** — report it.

## 3. Verify, open each PR, wait for CI

- **Complete local verification before each push** (§16): `lint`, `typecheck`, `format:check`, `check:classes`,
  `check:links`, `check:conflicts`, `NODE_ENV=production npm run build` then `check:build`, and `test:unit`,
  `test:component`, `test:api` **in full**. Two full lanes at once with 8–10 GB free; a third waits; run heavy
  commands one at a time and never leave an orphan process. **A lane killed for memory: retry once; if killed
  again, CI judges** — say so in the PR and the report. Lint and typecheck on each commit, one command at a time,
  returning to the branch after each (never leave it detached).
- The real runs of §16 (PR-A: requests with an OTHER contact and the public page; PR-B: the showcase; PR-C: both
  pages, every Sheet, mouse/keyboard/touch drag, «نسخ الرابط», «استخدم موقعي الحالي»). Screenshots to
  `C:\Users\basel\Downloads\wi<n>-shots\`, curated, never pushed. If the Chrome extension is unavailable, use
  headless Chrome over CDP against the local dev server. Stop servers by PID; check the ports free.
- The **`open-pr`** skill for each PR: check the next number just before the push (no `#PRNUM` left); assigned to
  the owner; labels by area (`feat`, `area:api`, `area:web`, `area:docs`, `area:design-system`, as each touches);
  the description in the workflow's sections, its Evidence naming every command run and what was not run, a
  "Deviations" section, and **"What changes on merge"** from §17 (PR-A: one migration runs online).
- Watch CI with a **bounded** loop (≤ 60 minutes; `gh pr checks`, `gh pr view --json mergeStateStatus`; `gh --jq`,
  never `jq`). A failure the PR caused: fix it, fold it into its commit (`git branch backup/<branch>-<n>` first,
  `--fixup` + `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash origin/main`), `git push --force-with-lease`. A
  failure it did not cause: retry the job once, then report it.

## 4. Report, then stop

When every check is green on the pushed head(s) and GitHub says `CLEAN`, the **`final-report`** skill:
- Phase 1 → `C:\dev\masaha\workspace\TASKS\SPACE_PROFILE\4_REPORT_AB.md` (both PRs);
- Phase 2 → `C:\dev\masaha\workspace\TASKS\SPACE_PROFILE\4_REPORT_C.md`.
Each names **every PR number and its full head sha**, the commits, the file count, every command's result, the EC
outcomes (EC1's count, EC2's versions and chunk size, EC5's before/after counts), the deviations, the findings
recorded, and anything noticed outside scope. **Then stop. Never merge; never delete a branch.**
