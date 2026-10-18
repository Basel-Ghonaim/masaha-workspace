# Masaha — analyst handoff (2026-10-17, morning)

You are taking over as the owner's **analyst and control room** for Masaha. This file supersedes the
2026-10-14 handoff (archived in `C:\Users\basel\Downloads\masaha-handoffs\HANDOFF_2026-10-14.md` —
read its §4 *Decisions* and §7 *Hazards* too; they still hold). The older handoffs in that folder hold
the role and the method in full. Your auto-memory loads too; the repository and this file win.

**Nothing is open on GitHub. No worker is building.** The week's Claude limit has just reset.

## 1. Your role and how you speak

- Arabic with the owner; English in every prompt. Arabic replies: no line starts with an English word
  or a code token; decisions as items with options and a recommendation, never tables; short.
- You run in `C:\Users\basel\masaha` but never edit the repository. Read-only git and `gh`. With the
  owner's word you merge (`gh pr merge <n> --merge --match-head-commit <sha>`); **an approved merge
  also means: delete the branch (remote and local), move the worker's folder to the new `main`, and,
  after a schema change, migrate, regenerate the client and rebuild the shared `dist`** — in one go.
- Verify every report in the code before believing it: head, CI, `CLEAN`, each subject ≤ 50 (count),
  files, the claims that matter.
- **Cost (learned the hard way):** last week's limit ran out mostly in one analyst conversation that
  grew past 150 k tokens. **Keep conversations short; start a new one with this file when one grows
  long; read each file once; use subagents only when needed.** If Opus's weekly limit runs out, Claude
  Code's **Fable** model has its own weekly limit (`/model fable`).

## 2. State on 2026-10-17

**`main` = `93f152f`** (#84). Merged since the last handoff, while Claude was out (executed and
reviewed with Copilot/Codex from the standalone plans in `C:\Users\basel\Downloads\masaha-next\`):
- **#82** `feat(spaces): include owners in admin space reads` — finding 59's API part (B, OWNERSREAD).
- **#83** `feat(spaces): add managed space API` — step 5a: `requireSpaceAccess` on
  `/manage/spaces/:spaceId`, the owner's profile, facts, confirms and photos on the admin's services;
  reception reads; no link → 404 (B, MANAGE).
- **#84** `feat(space-links): show deleted space facts` — the admin's spaces list: a state as two facts,
  «محذوفة» with «استرجاع», A7's chip, A8's warning; findings 44 and 50 resolved (A, ADMINLIST).
**Verify these three merges in the code when you start** (they were not checked by Claude): read their
PRs, reports (`MASAHA_WORKER_A|B\REPORT\`), review reports and the diff against their plans
(`MASAHA_WORKER_A\PLAN\ADMINLIST_PLAN.md`, `MASAHA_WORKER_B\PLAN\OWNERSREAD_PLAN.md`,
`MANAGE_PLAN.md`). Report anything wrong as a finding or an Issue, with the owner.

**Open Issues:** #71 (the merge-apart rule's wording — next PR touching `workflow.md`), #72 (the editor
page's DI-27 comment — next design PR touching the editor's pages), **#81** (the owner's checklist of
round 2's review commands; tick it as reports land).

**Open findings:** 8, 14, 15, 17, 21, 22, 23, 27, 32, 33, 40, 46, 48, 52, 55, 59 (the web part: the
editor names the owner — «فك ربط {name}»), 63, 64, 65, 67.

**Known defect on `main`:** `docs/design/INDEX.md` has a stray `<<<<<<< HEAD` line before § 54 (from
#76's rebase). Fix it in the first design fix PR; propose a CI check for conflict markers in the next
item touching CI.

## 3. The folders (all clean, all at `93f152f`)

- **Worker A** `C:\Users\basel\masaha` (main folder, on `main`). Ports 3320/5320. Never `npm ci` there
  while VS Code is open (a locked ESLint native file leaves it half-installed): use `npm install`.
- **Worker B** `C:\Users\basel\masaha-b` (detached). Ports 3321/5321.
- **Design / planning** `C:\Users\basel\masaha-design` and `masaha-design-b` (detached). Round 2's
  reviews read from `masaha-design`. **A planner working while a worker builds plans from one of these,
  reading only `origin/main`'s commit objects** — never in the busy worker's folder.
- Migrations: none since #78; `masaha_dev` and `masaha_b_dev` are current. Docker may be stopped:
  start Docker Desktop, then `docker start masaha-postgres-1` (never `db:up`).

## 4. The way of working now (the owner's, on trial since 2026-10-13)

- **One Work Item, three conversations:** a planner writes a **standalone plan** for any capable agent
  (every decision with its reason, interfaces, strings in both languages, tests with their breaks,
  commits counted, the procedure with commands, "Stop and ask", an appendix mapping steps to Claude's
  skills); a fresh conversation executes it (Claude, Codex or Copilot); a third, **another tool**,
  reviews. Review fixes go back to the executor. Each step is checked with a verify prompt.
- **The kit:** `C:\Users\basel\Downloads\masaha-next\` — one folder per item with `1_PLAN_PROMPT`,
  `2_EXEC_PROMPT`, `3_REVIEW_PROMPT`, `4_VERIFY_PROMPT`, `5_FIXES_PROMPT`, `6_MERGE_AND_CLEAN`, and the
  Arabic `MAP_AR.md` the owner follows. New items copy that shape.
- **Lessons:** a plan's documents ride in the code's commits (workflow §3), not a docs-only commit;
  **Copilot in autopilot executed a "plan only" prompt** (it cut a branch, wrote code and ran tests on
  B's test database): planning prompts must forbid any branch, file or test run in their first line,
  and planners should be Claude or a tool not in full autopilot; an executor first checks that what it
  builds on is merged.
- **Small review fixes** may be a new commit on top, tested where they touch (the owner's exception).

## 5. Ready to run

- **A — GALLERY (S2b-4c, the editor's photos):** plan approved,
  `MASAHA_WORKER_A\PLAN\GALLERY_PLAN.md` (approval note at its top: progress as text, no Progress
  component, no dependency). Its prerequisites (#84, #82) are merged. **Next: execute** —
  `Downloads\masaha-next\A_GALLERY\2_EXEC_PROMPT.md` in a new conversation in `C:\Users\basel\masaha`.
- **B — next item to decide:** candidates — step 5b (the owner's packages: a new table's rules, the
  desk's picker answered whole); finding 52 (one race-test helper); the owner's settings (capacity and
  the stay limit, O2); DI-41 (a student visit's rate with no student price). Analyse with the owner,
  then a plan prompt in the kit's shape.
- **A after the gallery:** the web part of finding 59 (the editor names the owner; «فك ربط {name}»;
  A4's one dialog), the owners and users screens, then the public site on #73's API (the card's cover,
  U12; the privacy line «يُرسَل موقعك مقرَّبًا…»), later the design-system + shell item.

## 6. Design review, round 2

- In `C:\Users\basel\.prompt\MASAHA_DESIGN\ROUND2\` (`PROMPT\`, `REPORT\`, `SUMMARY\`, `RUN_SHEET.md`,
  the owner's map `MAP_AR.md`, the remaining commands `REMAINING_AR.md`, scripts `run-queue.ps1` and
  others). **25 of 40 reports done; no summary yet.** Missing (15): `R2-AU-DF`, `R2-DK-DF`, `R2-OW-CP`,
  `R2-OW-DF`, `R2-OW-EX`, `R2-OW-TR`, `R2-PU-AX`, `R2-PU-CP`, `R2-PU-DF`, `R2-PU-EX`, `R2-PU-TR`,
  `R2-SH-AX`, `R2-SH-CP`, `R2-SH-DF`, `R2-SH-VD` (Issue #81 ticks `R2-AU-DF` but its report is absent).
- Reviews read from `masaha-design` (now at `93f152f`; `docs/design/` unchanged since #80).
- **Check each report is real:** one agent without a browser wrote "not performed" — delete such a
  report and rerun. Free OpenCode models hit per-model limits and choke on long contexts; Sonnet via
  OpenRouter needs credit; Copilot or Codex can run a review prompt as written.
- **Then:** the six part summaries, then `R2-ALL-SUMMARY`; then the owner and you write
  `MASAHA_DESIGN\DECISIONS_ROUND2.md`; then fix batch(es) (Claude plans, OpenCode builds, another tool
  reviews), fixing the INDEX marker; then `docs/design/screens/` regenerated once and the owner reviews
  every screen.

## 7. Hazards (new)

- A planner tool in full autopilot may execute instead of plan — and run tests on another worker's
  database. Say "no branch, no file, no test run" first; prefer Claude for plans.
- An executor that hits its limit mid-item leaves a commit unpushed: resume with a short prompt that
  states where it stands (`Downloads\masaha-next\B_OWNERSREAD\2b_RESUME_PROMPT.md` is the model).
- The earlier hazards (conflict markers no check catches; `npm ci` with VS Code open; Copilot inside
  the repository runs the project's skills; restore breaks from a backup, never `git checkout`) hold.
