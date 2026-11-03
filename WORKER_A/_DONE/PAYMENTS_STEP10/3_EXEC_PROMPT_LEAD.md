# PAYMENTS_STEP10 — the rest of the plan in one run: worker A as the lead of sub-agents, one PR

You are **worker A's lead executor** in `C:\dev\masaha\app` (ports 3320 / 5320, `masaha_dev` / `masaha_test`). You
build **everything left of the approved plan** — its PR 2 (announcements), PR 3 (data reports), PR 4a (report wrong
information) and PR 4b (favourites), plus **findings 169 and 173** — by running **sub-agents in parallel**, each on
its own lane, then you join their work into **one branch and one PR**, with the plan's atomic commits and the same
quality as if each PR had run alone. **The owner (2026-10-28) is away and has left the machine to you.** Do not run
the `start-work-item` skill. This file binds where it differs from the plan.

## 0. The rule for this run — you never stop until the whole task is done

- **No stop, no question, for any reason**, until the PR is open, CI is green on its head, it is `CLEAN`, the report
  is written and the final reply is sent. This is the owner's rule for this run and it is stricter than the
  autonomy rule (`C:\dev\masaha\workspace\_SHARED\AUTONOMY_2026-10-25.md`, read it whole): **even a serious problem
  does not stop you** — you decide, act, record and continue (§6).
- **Every decision you take on your own** (and every decision a sub-agent takes) is recorded under *Decisions taken
  without the owner* in the report: met, options, chose, why, undo. A decision you mark **SERIOUS** (§6) is listed
  first, at the top of the report and of the final reply.
- **The hard limits hold, always:** never merge; never push to `main`; never force-push a branch other than your own
  PR branch; never create an Issue; never change data through the app, the API or the database beyond the real run's
  named writes (§7), never reseed; never skip, weaken or delete a test, a check, a lane or a config to make it pass;
  never print a secret or keep an `/auth/` body; no tool attribution anywhere; never `git checkout -- <file>`,
  `stash` or `reset --hard` (restore from a backup copy); no `git add -A` / `git add .`; **never stop for the file
  count** (give it in the reply; it will be large — about 210 files — and that is expected).
- **A refused command** (the permission classifier blocks something, e.g. a force-push): do not stop — carry on with
  everything that does not need it, write the exact command in the report and in the final reply.

## 1. Read first (closed list; search before reading more)

1. This file, whole. Then `AUTONOMY_2026-10-25.md` (above), whole.
2. `C:\dev\masaha\workspace\WORKER_A\PAYMENTS_STEP10\2_PLAN.md`: **the owner's approval note at its top (binding)**;
   §2 *Scope*, *Acceptance criteria* and *Out of scope* (PRs 2, 3, 4a, 4b); §4; §5 (the S-decisions these PRs use;
   *Proposed alternatives* — A1 taken: 4a then 4b); §6; §7 *PR 2*, *PR 3*, *PR 4*; §8 *PR 2*, *PR 3*, *PR 4* and
   *Shared with the other items*; §9 *PR 2 · Commit 1* to *PR 4 · Commit 6*; §10 *PR 2*, *PR 3*, *PR 4* and *Review
   Focus*; §11; §12; §13 (first checks, per commit, on the head, **the real run**, push and the PR, *Decide and
   record*).
3. PR 1 as built and reviewed (so you reuse it and repeat none of its slips): `4_REPORT_PR1.md` (its decisions
   D1–D12, the fix round's R1–R3, its scripts) and `6_REVIEW_PR1_CLAUDE_CODE.md` (F1: react-day-picker 10's range
   ends on its first click without `resetOnSelect`; F2: a date test that cannot fail on UTC/Gaza machines — the web
   unit lane now runs in `America/New_York`).
4. On `origin/main`: `docs/architecture/findings/169-the-calendar-rides-in-the-sites-first-download.md`,
   `173-the-layers-range-calendar-ends-a-range-on-its-first-click.md`, `45-…` (the precedent: the table's own layer
   entry), `docs/frontend/design-system/foundation.md` §3, `apps/web/vite.config.ts`, `scripts/libraryChunks.ts`, the
   `check:build` script.

## 2. What changed since the plan was written (adapt to it; record each adaptation)

- **`main` = `76661f7c`.** Merged since the plan: **#127** (PR 1: `features/payments`, the void in `features/desk`,
  `shared/lib/time`, the web unit lane's `TZ`, `resetOnSelect` in the ledger's `RangeField`, findings 165, 166, 169,
  172, 173) and **#128** (worker B, FINANCE_AUDIT PR 1, API only: the audit reader; **the closure extension now also
  moves each covered subscription's renewals not started** — the preview's `subscriptions` count includes them, the
  `201` answer carries `renewalIds`; a key of another space's closure is `409 conflict`). **PR 2 commit 4 (the
  extension dialog)** reads that preview: read the contract at `origin/main` (*Announcements (managed)*), word the
  count as the server answers it, and adapt any test or copy the plan wrote before #128.
- **Worker B is idle** for this run (the owner's word): no one else pushes; PR numbers move only by you.
- **Finding numbers:** worker A's next free is **174** (167 and 168 are reserved by the plan for PR 3 and PR 4a).
- **No carried file** comes from #127's review (all its findings were fixed in its round). Finding 172 (the
  write-off's first focus) is **not** in scope.

## 3. Your role and the lanes

You are the **lead and the integrator**: you build the shared foundation yourself, launch and supervise the
sub-agents, grant their heavy checks (§5), join their work, run the complete verification and the real run, and
open the PR. **You decide how many sub-agents to run** (recommended: three — one per lane below; never more than
three at once). Launch them with the **Agent** tool (background, each on its own worktree and branch); continue a
sub-agent with **SendMessage**. A sub-agent's prompt is **yours to write**: self-contained, naming its folder, its
branch, the plan's sections and commits it builds, the files it owns, the files it must not touch, the test and
break list (§10) it must run, the decide-and-record rule, the hard limits of §0, and the reply it returns (its
commits, red/green lines, breaks, decisions).

### Lane 0 — the foundation, by you, first, on the PR branch (before any sub-agent starts)

1. **Branch:** `git fetch origin`; `git switch -c feat/step10-screens origin/main` in `C:\dev\masaha\app`.
2. **Finding 169 — the calendar on its own entry** (the owner scheduled it before PR 4; it is in scope because PR 2's
   announcement sheet draws `DatePicker` + `Calendar mode="single"`, and PR 4 measures the site's first download):
   the layer's `Calendar` and `DatePicker` served by an entry of their own, as `@shared/design-system/data` serves
   the table (finding 45, foundation §3); react-day-picker a library chunk in `scripts/libraryChunks.ts` that
   `check:build` refuses in the site's first download; every importer (the ledger's `LedgerFilters`, the showcase)
   moved to the entry; the first download measured base vs head (PR 1's `scripts\firstDownload.mjs`) and back near
   its size before #127 (1,055,704 bytes then); finding 169 → *Resolved* with its line, the index updated;
   foundation §3 says the new entry. Tests: `check:build` red with the calendar imported through the main barrel
   from a site page (a break), green after.
3. **Finding 173 — the layer's range calendar starts a range on each click:** the layer's range `Calendar` defaults
   to `resetOnSelect` (a caller may still pass it), its `DateRange` comment true; a component test of a first click
   (the picker keeps `from`, `to` empty) red before, green after; the ledger keeps working (its F1 test green);
   finding 173 → *Resolved*, the index.
4. **The shared seams**, so lanes never edit the same lines: read §8's lists and *Shared with the other items*; add,
   once, what several lanes would otherwise each add — at least the new pages' entries in
   `pages/dashboard/routes.tsx` / `navigation.ts` and `pages/site/routes.tsx` / `navigation.ts` pointing at
   placeholders the lanes replace, and the copy namespaces' files and their `index.ts` lines (`announcements`,
   `dataReports`, `favorites`) with empty objects typed against the catalogue, if the catalogue's types allow it.
   Decide what the seam holds and record it; anything you leave to the lanes is joined at the end (§4).
5. Lane 0's commits, each atomic, red first, Conventional, ≤ 50 characters with a body (e.g.
   `perf(design-system): serve the calendar on its own`, `fix(design-system): start a range on each click`, a
   `chore(web)`/`refactor` seam commit only if it is a real unit). Run their checks (§5's own-files rule, then lint
   and typecheck) **before** launching the lanes, so every lane branches from a green foundation.

### The lanes (branch each from Lane 0's head)

- **Lane A — announcements:** PR 2's commits 1–4 (§9 *PR 2*), the dashboard's screen 18, with the extension dialog
  on #128's contract (§2).
- **Lane B — data reports:** PR 3's commits 1–3 (§9 *PR 3*): `FilterTag` (finding 8), the owner's screen 23, the
  admin's screen 28 (finding 167).
- **Lane C — the user's side:** PR 4's commits 1–5 (§9 *PR 4*): my reports and the report dialog (4a, finding 168),
  the heart icon, the favourite action and the favourites page (4b).
- **PR 4's commit 6** (`feat(announcements): show a space's announcements`, finding 131) needs Lane A's commit 2
  (`components/public/*`) and Lane C's `SpacePage` / `SpaceDetails` edits: **build it last, on the joined branch**
  (yourself, or a sub-agent continued there), with its tests and breaks.

Each lane works in **its own worktree** (`C:\dev\masaha\app-lane-a|b|c` made by you with `git worktree add`, or the
Agent tool's worktree isolation — your choice, recorded): copy `apps/web/.env` and `apps/api/.env` into it (never
print them), run `npm ci` there **one worktree at a time**, and `npm run build -w @masaha/shared` before the first
test. A lane touches **only its own files** plus the shared files §8 gives it; a shared file it must change beyond
the seam → it adds its own lines only (never reorders or rewrites another lane's), and says so in its reply.

## 4. Joining the lanes

- When a lane has passed its heavy checks (§5), bring its commits onto `feat/step10-screens` **in the plan's
  order** — Lane A, then Lane B, then Lane C, then commit 6 — by rebasing the lane's branch onto the PR branch's head
  (no merge commits in the PR; atomic commits kept). After each lane: `npm run typecheck`, `npm run lint`, and the
  lane's routes test; a text conflict in a shared file → keep both sides' lines in the plan's order, record it; a
  semantic conflict → decide under §6, record.
- Commit subjects as §12 gives them (recount, ≤ 50), each with a body; a fix found while joining is **folded into
  the commit that made the code** (`--fixup` + `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash`), no fix commit,
  no `fixup!` left, every subject checked after each autosquash. Backups: a `backup/step10-<what>` branch before each
  rebase or fold; name them all in the report.
- Remove the lanes' worktrees once their commits are on the PR branch (`git worktree remove`); keep their branches
  until the PR is open, then delete the local lane branches; name what you removed.

## 5. Tests — the owner's rules (complete testing before CI; memory managed by you)

- **During the work, every sub-agent tests its own work only:** each new test seen **red before its code** (record
  the line), green after; each break of §10 for its commits run **from a backup copy and restored by copy** (record
  the red line); **only the test files its change touches** (`npx vitest run` through `npm run test:unit -w
  @masaha/web -- <files>` / `test:component -w @masaha/web -- <files>`) — never tests of files it did not touch.
- **Heavy checks are granted by you:** a sub-agent asks you before any heavy command — `npm run lint`, `npm run
  typecheck`, the full web lanes on its branch (`npm run test:unit -w @masaha/web`, `npm run test:component -w
  @masaha/web`), a production build. **At most two heavy runs at once on the machine.** Before granting one, read the
  free memory (`(Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory`): grant it when **≥ 4 GB** is free;
  else make it wait and check again every 2 minutes (bounded loops only). A third waits for one of the two to end.
  **Every lane passes, before you join it:** its touched tests, lint, typecheck, and the two full web lanes on its
  branch — all green.
- **A heavy run killed for low memory:** wait until memory is free again and re-run it once; killed again → run that
  lane in parts (by directory, e.g. `test:component -w @masaha/web -- src/features src/pages`, then `src/shared
  src/app`), until every file has run green once. Record each kill. Never leave a lane unrun.
- **The final, complete verification — by you, on `feat/step10-screens` after commit 6, before the PR is opened:**
  `npm run build -w @masaha/shared`; `npm run lint`; `npm run typecheck`; `npm run test:unit` (every workspace);
  `npm run test:component`; `npm run test:api` (`docker start masaha-postgres-1`; it takes about 10 minutes — **no
  command timeout**, run it in the background and wait for it); `NODE_ENV=production npm run build` then `npm run
  check:build`; `npm run check:classes`; `npm run check:links`; `npm run check:conflicts`; `npm run format:check`;
  the site's first download measured against `origin/main`'s (§3 Lane 0). Then **the real run** (§7). Finding 87's
  family (slow first lazy imports: `routes` › the owner's and reception's page lists, the site tests opening
  `/spaces`, `App` › "renders the main landmark", `router` › the root's general error) missed in a full run and
  passing alone is known: re-run it alone, record it, go on.
- **Only when all of this is green do you push and open the PR.** A failure → §6.

## 6. A problem — never a stop

- **Simple** (a test, a type, a lint rule, a document line, a lane's slip, a conflict resolved by keeping both
  sides): fix it, fold it into its commit, re-run what it touched **and the whole lane it failed in**, go on.
- **SERIOUS** — wrong money shown or sent, a role offered what it must not, private data shown to whom it must not,
  a change to a plan decision, a conflict between lanes that needs a redesign, a failure across several lanes: you
  **still do not stop**. Find its cause and where it lives; choose the safest course that keeps the plan's decisions
  and the hard limits — fix it inside the plan if you can; if a lane's part cannot be made right and green, **leave
  that part (its commits) out of the PR** on its own branch, keep the rest whole and green, and name it. Record it as
  **SERIOUS** (met, cause, where, options, chose, why, undo), at the top of the report and the reply. Never weaken a
  test to pass.
- A case the demo data lacks → never change data through the app to make it: record it as not performed, with why.

## 7. The real run (on the joined branch, after the full verification is green)

As §13 *The real run* of the plan for **PRs 2, 3, 4a, 4b** (PR 1's is done): the API on 3320 and the web on 5320 on
`masaha_dev`; local headless Chrome over CDP on the model of PR 1's `scripts\run1.mjs` / `cdp1.mjs` (Enter with
`text: '\r'`; no `/auth/` body kept); each role, Arabic light and English dark, 390 / 768 / 1440 where the layout
changes; the network log (method, URL, status, `Idempotency-Key`; the offline retry proving one key). **The writes,
each named, only those of §13** (the approval note allows them; **the extension applied with 1 day** on
`masaha-demo`'s covered seed subscriptions — it now also moves their renewals not started, #128: record the preview's
count and the subscriptions moved). The width breaks and touch targets as §13 lists them. Screenshots in
`C:\dev\masaha\workspace\WORKER_A\PAYMENTS_STEP10\shots\lead\`. Stop every server by process id; ports 3320 and 5320
free after; `git status --short` clean. Name every write and every row left in `masaha_dev` in the report.

## 8. Push, the PR, CI

- **The PR number:** `gh api "repos/Basel-Ghonaim/masaha/issues?state=all&per_page=1" --jq '.[0].number'` just
  before the push → the next number; replace `#PRNUM` in every commit's tree **before the first push** (PR 1's
  `scripts\prnum1.sh` model; no PR number in any SQL — there is none here); `git grep '#PRNUM'` on the head → nothing.
  After `gh pr create`, compare the number; if it differs, redo the rewrite and `git push
  --force-with-lease=feat/step10-screens:<sha>` (your branch only; if refused: §0).
- `git push -u origin feat/step10-screens`; `gh pr create --assignee @me --label feat --label area:web --label
  area:docs`, the title ≤ 50 (e.g. `feat(web): announcements, data reports, favourites` — recount). The description:
  a short summary; **one section per former PR** (2, 3, 4a, 4b) with its acceptance criteria from §2 and how each is
  met; Lane 0 (findings 169, 173 resolved); *Closes* findings 8, 131, 169, 173 (and 167, 168 recorded); the lanes
  and how they were joined; the verification run locally (each command and its result); the real run; the decisions
  taken without the owner (SERIOUS first); anything left out (§6) and where it is.
- `gh pr checks <n> --watch` (bounded; no command timeout) → all green, then `gh pr view <n> --json
  mergeStateStatus` → `CLEAN`. A red lane → read why, fix, fold, re-run that lane locally in full, push (lease on your
  own head), watch again.

## 9. The report and the final reply

- The report: `C:\dev\masaha\workspace\WORKER_A\PAYMENTS_STEP10\4_REPORT_LEAD.md`, **written as you go** (a section
  per lane and per stage): Lane 0; each lane (its sub-agent, its commits, red/green lines, breaks, heavy checks and
  when they were granted, its decisions); the joins (conflicts and how kept); memory (each grant, each wait, each
  kill); the full verification (each command, its result line); the first download (base vs head); the real run
  (cases, network log, writes, data left); push, PR, CI; *Decisions taken without the owner* (SERIOUS first);
  leftovers (branches, worktrees, backups — named).
- Write only that report and files under `C:\dev\masaha\workspace\WORKER_A\PAYMENTS_STEP10\scripts\` and `shots\`
  outside the repository. Scripts in files (heredocs can fail to parse); Python writing a file uses
  `newline=""`; never `cd` into `node_modules`; `jq` is absent — use `gh --jq`; stop a backgrounded dev server by its
  process ids (tsx watch, server, pino) and check the port.

```
Status: READY FOR REVIEW | INCOMPLETE (only if nothing at all could continue)
SERIOUS decisions: <each, one line>   (or "none")
PR: #<n> · head <sha> · CI <green/red> · <CLEAN/not CLEAN> · files <n>
Lanes: <n sub-agents> · Lane 0 <commits> · A <commits> · B <commits> · C <commits> · commit 6 <sha>
Left out of the PR: <part, branch, why>   (or "nothing")
Commits: <sha> <subject> (<chars>) — all, in order
Verification (local, on <sha>): <each command with its result line>
First download: base <bytes> → head <bytes>
Real run: <cases> · writes <each> · data left <rows>
Memory: <grants, waits, kills>
CI on the head: <each lane>
Findings: <resolved / recorded / new (174+)>
Decisions taken without the owner: <count>, in the report
Refused commands: <command>   (or "none")
Leftovers: <branches, worktrees, backups>
Report: C:\dev\masaha\workspace\WORKER_A\PAYMENTS_STEP10\4_REPORT_LEAD.md
```
