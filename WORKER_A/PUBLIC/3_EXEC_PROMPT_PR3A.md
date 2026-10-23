# PUBLIC — execute PR 3a only (`feat/space-page`, the Space details page)

You are the **executor**, in a fresh conversation. You did not plan this item and you will not review it.
**The plan is approved; do not re-decide anything in it.**

**The owner's split (2026-10-22):** the plan's PR 3 (six commits, ≈ 75 files) becomes two PRs, both yours:
**PR 3a — this one:** the carried items of #105, then the plan's PR 3 **commits 1–4** (the shared carrier and
date rules; the public contact; one place on a map; the space's public page); tests **61–75 and 79**. **PR 3b —
later, another prompt:** commits 5–6 (the photos; the live status's refresh), tests 76–78. Nothing of commits
5–6 here: the page leaves the gallery's place empty and its status panel shows what the page's own read gives,
as the plan's commit 4 describes.

## 0. What to read — and only this (the owner's instruction, 2026-10-22)

The owner's instruction overrides the bootstrap's session checklist for this task, stated here: **do not run
the `start-work-item` skill** and do not read `docs/development/workflow.md` whole. `CLAUDE.md` is already in
your context. Read only:

1. `C:\dev\masaha\workspace\WORKER_A\PUBLIC\2_PLAN.md` — **these parts only:** the owner's approval note at its
   top (lines 1–40, binding, it wins where the plan differs); §1; §2 *Scope*, *Acceptance criteria* and *Out of
   scope* as they touch PR 3; §4; §5's decisions that name PR 3 or the space page; §6; §7 *PR 3* and *Shared
   with the other open items*; §8 *PR 3* (design issues); §9 *PR 3 · Commits 1–4*; §10 *PR 3* tests 61–75 and
   79; §11's PR 3 points; §12's PR 3 lines; §13 (first checks, per commit, on the head, the real run's PR 3
   cases, push and the PR, the stop rule, *Stop and ask*); §14's answers.
2. `0_CARRIED_FROM_105.md` whole, and in `6_REVIEW_PR2_CLAUDE_CODE.md` **only the findings it cites**.
3. `4_REPORT_PR2.md` — only its departures (search `Departures`) and its §6 table: `MapLayers` and `mapBox`
   are now shared, which `PlaceMap` uses.
4. In the repository: the code and documents a step touches, when that step needs them — search first
   (`git grep`), then read the section, not the whole file. The `open-pr` skill may help at the end; no other
   skill is needed.

Read each file once. If a step proves to need a document not named here, read the part it needs and say so in
the report.

## 1. Then begin

1. **Precondition:** PR 2 (#105, `feat/directory-map`) is merged — `gh pr view 105 --json state` → `MERGED`
   (at `a3828e09`, 2026-10-22); if not, stop.
2. Work in `C:\dev\masaha\app` only — never in `C:\dev\masaha\app-b` (worker B) or `C:\dev\masaha\app-design`.
   `app` is on `main` at `a3828e09`, clean, shared built.
3. **Carried from #105 — this PR's first commit(s), before the plan's PR 3 commit 1:** every item of
   `0_CARRIED_FROM_105.md` (1–14; the owner's decisions of 2026-10-22, the map line's words included). Each code
   fix red first, then green. The PR's description names them under "Carried from #105". If an item proves
   larger than the file says, **stop and ask**.
4. **Then the plan's PR 3 commits 1–4**, following §13 for them: the first checks against the merged
   `origin/main` (a code file this PR names changed in a way the plan does not cover → stop and ask); the branch
   `feat/space-page` from the latest `origin/main` (`--no-track`); per commit `lint` and `typecheck`; the head's
   checks; the real run; `#PRNUM`; push; the PR, titled **`feat(directory): show a space's public page`**,
   `--label feat --label area:web --label area:docs --label area:design-system` (carried item 11 touches the
   layer's Sheet); CI green and `CLEAN`; the conflict check against any open PR (worker B's SUBSCRIPTIONS PR 2,
   #106, may be open: shared documents only). Stop at the plan's *Stop and ask*.
5. **Size:** ≈ 60 files with the carried items is expected and accepted by the owner; **stop and ask only past
   75 files**.
6. **Finding numbers:** 131 is the plan's (this PR writes it, commit 4); 134–136 are the carried file's; a new
   one takes **137** and on, said in the report.
7. `docker start masaha-postgres-1` (never `db:up`; never `npm ci`; if Docker Desktop is not running, stop and
   ask the owner to start it); in `apps/api` `npx prisma migrate status` → up to date (pending → stop and ask);
   API on 3320, web on 5320, worker A's `masaha_dev`.
8. **The demo data:** run §13's data inventory first (read-only `GET`s, a script in `scripts\`). `masaha_dev`
   holds the directory's demo set (seeded 2026-10-21; its FULL and "closed today" held that day only) and some
   older test spaces. A case the data does not hold → **not performed, by design** only where §13 allows it,
   with the test that proves it; any other → stop and report. **Never add or change data through the app, the
   API, the database or the seed.** `apps/web/.env`: `VITE_CONTACT_EMAIL` and `VITE_CONTACT_WHATSAPP` as §13
   says for the run, then back to what it was; `.env` is never committed.
9. **The real run** with real screenshots (local headless Chrome over CDP, as `scripts\cdp2.mjs` and
   `run2b.mjs` do; **send Enter with its text** — `text: '\r'` — or a native button never activates): §13's
   PR 3 cases **without the photos' viewer and the status's refresh** (PR 3b's): a verified space (the order at
   each width, the status, today, the prices per audience and by shift, the hours with today and «عرض كل
   الأيام», the amenities, the map's pin, «الاتجاهات», the contacts and the carrier, the breadcrumb from 768, the
   back link and the bar at 390); an unverified space with hidden prices (the notice, its dialog with the email
   alone, then both channels, then none); a stale group's badge; an unknown slug; and the carried items a
   browser shows (the pick ending with the map; the overlay before the pins in the tab order; the map's own
   near-me line; the pins' loading line; the picking card under the map at 768; Escape on the card). Widths as
   §3.4 below. Screenshots to `C:\dev\masaha\workspace\WORKER_A\PUBLIC\shots\pr3a\`.
10. Write nothing outside the repository except this folder's `4_REPORT_PR3A.md`, `shots\` and `scripts\`.

## 2. A test you cannot run stops the work

A test **failing** because its code is not written yet is the plan's red step — normal. A test, lane or
command you **cannot run** is not: it errors before any test runs (the database unreachable, Docker down, a
port taken, a module or `dist` missing, a migration pending, `No test files found`, a Vitest or TypeScript
startup error, the whole run timing out, a crash with no result); a break you could not make or run; a
real-run case you could not perform (other than those §1.8 allows). **Then stop at once** — never skip,
`.skip` or delete a test, never change a config, a timeout, `.env` (beyond §1.8), a script or a lane, never
mock what the plan does not, never run a narrower command and call it the lane, never call it "flaky" and move
on. Write the command, its exact error and where you were into the report, and reply with §6's shape,
`Status: STOPPED`.

**The owner's standing exceptions:**
- `routes.component.test.tsx` › "lists the owner's eleven pages" (finding 87) may miss its 3 s locally when the
  machine is loaded. If **only that test** fails and it passes alone, record both runs (times, free memory) and
  go on; **CI's `test:component` is the judge** — if it fails there, stop.
- A run **killed for low memory** is re-run **once** when the machine is quieter (no `vitest` of
  `C:\dev\masaha\app-b\` running, the free memory recorded); killed again → record it, carry on, and CI's run
  of that lane on the pushed head is the judge — red there → stop.

**A plan that proves false against the code:** stop too, say exactly what and why, and offer the fix — do
not choose it yourself. **A break that stays green:** stop — unless it is plainly your own test's defect, or
the plan's break cannot change the outcome; then make the break that can, see it red, and state it as a
departure. **A design issue, a carried item or a review point you would leave undone: stop and ask** — never
silently.

**Never claim a result you did not see:** a command passed only if you saw its own output say so; copy that
line (read it by its exit code). A break counts only when you saw it red.

## 3. What runs where (the owner's rule: no run that only repeats another)

1. **A test seen red before its code is its own break.** Record that red line once. Make a **separate** break
   only where the plan's break targets a guard the red step did not prove — the page's order and its aside by
   width, a link's form (`wa.me` digits), the pin as a picture and not a button, a carried privacy rule (the
   pick's centre rounded, nothing sent while picking) — and record its red output.
2. **Locally, on the head:** `npm run test:unit -w @masaha/web` · `npm run test:component -w @masaha/web --
   src/shared/map src/features/directory src/features/platform-settings src/features/spaces src/pages/site
   src/shared/design-system` (the folders this PR touches; add any other whose files it changes, and say so) ·
   `$env:NODE_ENV='production'; npm run build; Remove-Item Env:NODE_ENV` · `npm run check:build` · `npm run
   check:classes` · `npm run format:check` · `npm run check:links`. Before each test run: no `vitest` of
   `C:\dev\masaha\app-b\` running, the free memory recorded.
3. **Not run locally — CI's run on the pushed head is the judge:** the full `test:component` lane, `test:unit`
   of `apps/api` and `packages/shared`, and `test:api` (no API change). Report them under "Not run locally (CI
   judges)", not under COULD NOT RUN. A red CI lane → fix it, fold the fix, push again.
4. **The real run's widths:** the layouts that change with width — the page's order, the aside from 1024, the
   bar below 768, the breadcrumb from 768 — in Arabic light and English dark at 390, 768 and 1440; every other
   case once in Arabic light at 390 and once in English dark at 1440. The width break (§13: the main column's
   `lg:col-span-8` removed once) with its screenshot.
5. **A fix after a lane passed** re-runs only the test files it touches, plus `typecheck` and `lint`; say so.

## 4. Limits and not losing work

- Write `4_REPORT_PR3A.md` **as you go**: after the first checks, after each commit (sha, subject with its
  length, the red line before the code, the green line after), after each break, after the real run, after
  the push. If you stop for any reason, the report already says where the work stands.
- Keep a long command's output in a file under `scripts\` and read its exit code and the lines you need, not
  the whole output.
- Keep the scripts you write for the real run in this folder's `scripts\`, never committed.

## 5. Discipline

Stage by path (never `-A` or `.`); each commit message written to a UTF-8 file **without a BOM, LF line
endings**, with a body saying why, and `git commit -F <file>`; subjects counted ≤ 50; **no tool
attribution**; a fix before the push folds into its commit (`--fixup` + `GIT_SEQUENCE_EDITOR=:`
autosquash); `#PRNUM` replaced in each commit's tree just before the push (§13), never in the working tree
alone; never print a secret or a password; never merge, create an Issue, or comment on another PR. `git status
--short` clean at the end; stop both servers by process id; ports 3320 and 5320 free.

## 6. Your final reply — this shape, finished or stopped

```
Status: DONE | STOPPED
PR: #<n> <url> · head <sha> · CI <green/red/pending> · <CLEAN/not CLEAN> · files <count>   (or "no PR")
Commits: <sha> <subject> (<chars>) — one line each, the carried ones first
Carried from #105: <each item 1–14: done in <sha>, red then green / recorded as finding <n>>
Ran and passed: <each command, with the result line you saw>
Ran and failed: <each, what failed, what you did>   (or "none")
Not run locally (CI judges): <each lane, and CI's result on the head once seen>
COULD NOT RUN: <each test, lane, break or real-run case not run, the exact command, the exact error,
               why>   (or "none" — only if every planned run happened)
Breaks: <each: red seen (in the red step or as its own break) / NOT red (why)>
Real run: <each case and its screenshot, or NOT PERFORMED (by design) with the test that proves it>
Data left in masaha_dev: <what the run changed>   (expected: nothing)
Departures from the plan: <each, with its reason>   (or "none")
Stopped at (if STOPPED): <the step, and what the owner must decide or fix>
Report: C:\dev\masaha\workspace\WORKER_A\PUBLIC\4_REPORT_PR3A.md
```
