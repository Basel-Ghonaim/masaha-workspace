# IDENTITY — ink + berry and the logo in production — the LEAD executor (sub-agents, one PR)

You are the **lead executor and integrator** on **Masaha** (a bilingual Arabic RTL / English platform for coworking
spaces in Gaza), a fresh **Claude Code** session, **Opus 5.5, effort xhigh**, in **`C:\dev\masaha\app-design`**. You
build the approved plan **`C:\dev\masaha\workspace\TASKS\IDENTITY\2_PLAN_PROD.md`** — the shared layer yourself, the
rest by **sub-agents** you write prompts for and supervise — and you join it all into **one branch and one PR**. The
plan is **approved: do not re-plan, do not enter plan mode.** No stop until the report, except the two planned waits
below (#143's merge; the comparison servers' ports) and the stop rules of `docs/development/workflow.md` §8.

## 1. What is decided (binding)

- `C:\dev\masaha\workspace\TASKS\IDENTITY\0_OWNER_DECISIONS.md` — **the last section, «The production plan
  (2026-11-12)»**: OD1 **(b) a lead with sub-agents**, OD2 (a) one PR, OD3 (a) no logo in the owner / reception
  shell, OD4 (a) the raster icons rendered in headless Chrome and the `.ico` packed by a scratchpad script, OD5 (a)
  berry the prototype's default; **SD1–SD10 and D1–D5 as written.**
- **This prompt's departures from the plan** (say each in the report): (1) the shape of §3–§6 below; (2) you start
  **before #143 merges** — EC1's "stop if #143 is not in `main`" becomes the wait of §4; (3) the plan's finding is
  **220**, not 219 (#143's fix round records 219); (4) the report goes to
  **`C:\dev\masaha\workspace\TASKS\IDENTITY\4_REPORT_PROD.md`**; (5) the commits keep the plan's §15 units, but C1 and
  C6 come first (the shared layer); renumbering is fine; **every commit lints and typechecks on its own**; (6) **the
  owner's no-conflict rule** of §3: no file #143 changes is edited before #143 merges.
- Read first: `CLAUDE.md`; `docs/development/workflow.md` (§2–§10; §10 — sub-agents are capped by this prompt);
  `testing.md`; **the plan whole**. The method of earlier lead runs, these parts only:
  `C:\dev\masaha\workspace\WORKER_B\_DONE\BACKEND_FINAL\3_EXEC_PROMPT_LEAD.md` §3–§5 (lanes, joins, grants) and its
  `scripts\heavy.mjs`; `C:\dev\masaha\workspace\WORKER_A\_DONE\PAYMENTS_STEP10\4_REPORT_LEAD.md` (*Lane 0*, *The
  joins*, *Memory and the grants*).

## 2. The machine and its neighbours

- **This folder:** detached at `main` `f0709d28`, clean. Its `apps/api/.env` points at **`masaha_dev`** (the demo set
  the visual pass reads) and **`masaha_design_test`** (your `test:api`); its `apps/web/.env` sets `WEB_PORT=5323`,
  `API_PROXY_TARGET=http://localhost:3323` and `NODE_ENV=development` (build with `NODE_ENV=production`). Keep both
  files; never print them. **Never `db:seed` `masaha_dev`.** The admin account there signs in with this folder's
  `SEED_ADMIN_PASSWORD` (set today; it was Google-only); the demo owner and reception with `SEED_DEMO_PASSWORD`.
- **The supervisor's comparison servers** run **from this folder** on 3323 / 5323 (and 3326 / 5326 from
  `C:\dev\masaha\app-pr143`). **Never stop or kill them.** You need no server before the visual pass (§6).
- **`C:\dev\masaha\app-pr143`** is the supervisor's: its `node_modules` are **junctions into this folder's
  `node_modules`**. While it exists, **never run `npm ci` / `npm install`, `git clean`, or delete `node_modules` in
  this folder.** None is needed (`main` changes no dependency; #143 neither). If one ever is, ask the owner first.
- **#143's fixer** works in `C:\dev\masaha\app` (`feat/space-profile`, ports 3342 / 5342, `masaha_wi142_dev`): never
  touch that folder, its branch or its databases.
- **Memory:** the owner frees RAM and watches it; disk ~18 GB free. **Every heavy run goes through the grant
  script:** copy `BACKEND_FINAL\scripts\heavy.mjs` to `C:\dev\masaha\workspace\TASKS\IDENTITY\scripts\heavy.mjs` and
  adapt its paths (keep: ≥ 4 GB free before a run starts, at most two heavy runs at once, the lead first). Heavy =
  `lint`, `typecheck`, any test lane or test file run, a build, `npm ci`, a Chrome batch. **A lane killed for memory:
  retry once; killed again — record it, carry on, and CI on the pushed head judges** (said in the PR and the report).

## 3. Phase 1 — the shared layer (you, alone, now)

**The owner's rule — no conflict with #143 while it is open:** before #143 merges, **never edit a file #143
changes.** Before every commit of this phase, `git fetch origin` and read
`git diff --name-only origin/main...origin/feat/space-profile` (the fixer may push more): no file you stage may be in
it. Today that list holds two of the shared layer's files — **`docs/frontend/design-system/foundation.md`** and
**the layer's `apps/web/src/shared/design-system/index.ts`** — so every edit to them waits for §4, after the rebase.
#143's branch is never touched by you in any way.

1. `git fetch origin`; `git switch --no-track -c feat/ink-berry-identity origin/main`.
2. **C1, its code part** (the plan's §15.1): primitives (neutral in the ink's hue; `spark` in place of `brand`, SD7),
   the remap and the new roles (§5.2), the `skeleton` token, the utilities (§5.3, SD1, EC5), the token test
   **T1–T11** with its colour maths (EC3, EC4), **ADR 0019**, the map (`docs/README.md`). Seen failing first, as the
   matrix says. Its `foundation.md` part (Status, §4, §5, §15 row 1) is folded in after the merge (§4).
3. **C6, its first part:** the `display/Logo` component and its test **T16** (the test imports it by its folder,
   since the layer's index waits), EC6's component part. Record **EC7**'s first-download baseline before it. The rest
   of C6 — the index's export, `SidebarHeader({ mark, logo })` with T17 and every caller, the showcase's Logo section
   and SidebarSection, foundation §3 / §12 / §15 row 5 / §16 — comes after the merge (§4).
4. Each commit: `lint` + `typecheck` green on it; then `test:unit` and `NODE_ENV=production npm run build` green on
   the head. Keep a `backup/ink-berry-identity-1` before any rewrite.
5. **Write the three lane prompts now** (§5), saved as
   `C:\dev\masaha\workspace\TASKS\IDENTITY\lanes\LANE_A.md`, `LANE_B.md`, `LANE_C.md`.

## 4. Phase 2 — wait for #143's merge (only if Phase 1 ends first)

- No sub-agent starts before **#143 is merged into `main`** (its files are lanes A's and B's).
- Run a bounded wait **in the background**: every 3 minutes `gh pr view 143 --json state,mergeCommit`, at most
  8 hours, ending on `MERGED` (or `CLOSED`: tell the owner and wait for his word). Write it as a script file in your
  scratchpad (no heredoc). **The owner or the supervisor may also tell you in this conversation that #143 merged** —
  check it with `gh`, stop the wait, go on.
- On the merge: `git fetch origin`; `git rebase origin/main` (none of your commits touches a #143 file, so none is
  expected; if one appears, resolve it on your branch, keeping both sides); then **finish the shared layer on the
  merged `main`:** C1's `foundation.md` part (folded into C1) and the rest of C6 (§3 above), as `--fixup` +
  autosquash with a `backup/*` first; `lint` + `typecheck` on each commit, `test:unit`, the build. Then **EC1** on
  the real `main`: the next numbers (ADR 0019, finding **220**, PR — expected **#144**), the inventory command, and
  #143's final versions of `ContactsSheet`, `ContactsView`, `PhotosEdit`, `PhotosView` and any file its fix round
  added. Update the lane prompts with what EC1 finds.

## 5. Phase 3 — the lanes (sub-agents), then the joins

- **Three lanes, as the plan's OD1 (b) table:** **A** — components (C2, C3, C4); **B** — shells and fixes (C5, C7);
  **C** — outside the web's source (C8, C9, C10, C11 with finding **220**; added 2026-11-12: C11 records **two**
  findings, the next two free numbers — first #143's fix-round offer, "On the admin's 404 page the top bar still
  offers «إخفاء عن الزوار» and «حذف المساحة» for the space just found deleted" (`SpaceEditorActions` reads the space
  query, whose earlier data stays after the 404; `4_REPORT_C.md` › Fix round §6), then the README's Sea shots). **At most three sub-agents at once.**
- **Worktrees:** `git worktree add -b lane/<x> C:\dev\masaha\app-design-lane-<x> <the shared layer's head>`; copy
  `apps/api/.env` and `apps/web/.env` from this folder (never print them); `npm ci` **one worktree at a time, through
  `heavy.mjs`**. No lane runs a server, `test:api`, or touches a database.
- **Each lane's prompt is yours, self-contained:** its folder and branch; the files it owns and **what it may not
  touch** (the tokens, `foundation.md`, `setup.md`, `CLAUDE.md`, another lane's files); the plan's sections it builds
  (§7 rows, the rule "selected keeps its tint under the pointer", the spark's rules, D1/EC10 for A); its tests and
  the break that makes each fail **first**; its commands, each through `heavy.mjs` with its lane name, and only its
  own files' lint and test files plus `typecheck`; commits on `lane/<x>` with the plan's subjects (≤ 50, a body),
  staged by path, no push; **the document lines it needs written in its report, not in the documents** (you fold
  them into its commits after the join); the decide-and-record rule (a choice the plan does not settle: take the
  safest, record it); its final message = its report (you save it as `lanes\REPORT_<x>.md`).
- **Joins,** in the order A, B, C (or a safer one, recorded): rebase the lane branch onto
  `feat/ink-berry-identity` (no merge commits); after each, `lint`, `typecheck`, the lane's own tests; fold the lane's
  document lines (foundation §3 / §5 / §11 / §12, `setup.md`, `CLAUDE.md` for SD2) into its commits (`--fixup` +
  autosquash, a `backup/*` first). Remove each joined lane's worktree (`git worktree remove`) — **only the lanes'**,
  never `app-pr143`.

## 6. Phase 4 — the visual pass, the full verification, the PR

- **The visual pass** (plan §13, T23, EC8, EC9, EC11, EC13, EC14), by a **fourth sub-agent** once A–C have ended (or
  by you): API and web **from this folder on 3323 / 5323**. **Before starting them, check the ports:** if the
  supervisor's comparison servers still answer, tell the owner in this conversation and wait for his word. One Chrome
  at a time, each batch through `heavy.mjs`; screenshots to `C:\Users\basel\Downloads\identity-prod-shots\` (curated,
  never committed); it returns a findings list. Fix each defect in its commit (folded); re-run what it touches. Stop
  every server you started by its PID; check the ports free.
- **The rasters** (OD4 (a), plan §7.5): rendered in headless Chrome, the `.ico` packed by a scratchpad script; the
  120 × 120 PNG for Google to `C:\dev\masaha\workspace\TASKS\IDENTITY\google\masaha-logo-120.png` (not committed).
- **Complete verification on the head** (plan §13's order, each through `heavy.mjs`): `lint` and `typecheck` on
  **every** commit; `format:check`, `check:classes`, `check:links`, `check:conflicts`; `test:unit`, `test:component`,
  `test:api` in full; `NODE_ENV=production npm run build` + `check:build`; the prototype's `check-parse` and
  `check-classes`.
- **The PR** with the project's `open-pr` skill (plan §17): `#PRNUM` replaced with the real number just before the
  push (expected #144 — check), pushed with `-u`, `gh pr create` at once, assigned to the owner, the labels and
  description the plan names. Wait for CI green on the pushed head and GitHub `CLEAN` (a failure your PR did not
  cause: re-run once, then report). Then the `final-report` skill → `4_REPORT_PROD.md`: the head (full sha), the
  commits, the lanes (each lane's report summarised, its decisions), the joins, what ran and what did not, the breaks
  made, EC results, problems and their solutions, the file count, departures from the plan. **Then stop.**

## 7. Limits

No merge; no push to `main`; no force-push of another branch; no migration; no dependency; **never `db:seed`
`masaha_dev`**; stage by path, never `git add -A` / `git add .`; no tool attribution anywhere; no secret printed;
never weaken, skip or delete a test, a check or a lane to pass; no production code only a test uses; never stop on
file count — report it; public text never names hosting providers, free plans or session durations; nothing in
`C:\dev\masaha\app` or `C:\dev\masaha\app-pr143`.
