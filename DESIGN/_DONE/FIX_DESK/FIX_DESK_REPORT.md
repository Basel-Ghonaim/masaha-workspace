# Design fix 6 (the front desk) — execution report

Executor: Muse Spark (opencode). Plan: `PLAN\FIX_DESK_PLAN.md` (2,679 lines, read whole).
Owner's answers (from `PROMPT\FIX_DESK_EXEC.md`): **S1–S17 approved as recommended**; DI-41–DI-47
recorded as routed; build in `C:\Users\basel\masaha-design-b`. The reference diff
(`PLAN\desk-scratch-reference.diff`, 11 files) was used only to check work and resolve one doubt
(see §4); where in doubt the plan was followed. No question outside the plan arose.

## 1. The PR

- **PR #80** — https://github.com/Basel-Ghonaim/masaha/pull/80 — "design: the front desk", labels
  `docs` + `area:docs`, assignee the owner, base `main`.
- Head SHA: `1cae6a749c55e0780524021b141e0dfedc653fe6` (= commit 10).
- CI on the pushed head: all green (format:check, lint, test:unit, test:component, test:api,
  typecheck, build, check:classes, check:links, CodeRabbit-skipped) and
  `mergeStateStatus` = **CLEAN**. Never merged, as ordered.

## 2. The commits (all `docs(design): …`, subjects ≤ 50 chars, staged by path only)

| # | SHA | Subject |
|---|---|---|
| 1 | 76c8020895358008da0d9f89ddb907f3a014f53a | docs(design): check-out takes money in one block |
| 2 | b2ba7ac09c8b398011d20a3a36a1e7477497406b | docs(design): collect, record a debt, write off |
| 3 | 57c786c44dfe063dc3541015ea7d2092d5df6628 | docs(design): the sheet in one step, debt first |
| 4 | 5bb78b9c3851f1d1cc12f0d205a26de72062ab28 | docs(design): one desk search, ordered for phones |
| 5 | d36a1d6df4f3b1a8f104a2028bacc077e4b46edd | docs(design): the week's warning uses the count |
| 6 | 3d2026b89d18b2e9baa1784898cef7a5d1ae6a66 | docs(design): customers: actions by state, archive |
| 7 | ae2d76820af1114959fd0f2651e19329fe440a24 | docs(design): the customer file hides no money |
| 8 | cb2ff1da23cc53caceac94fd070347ee48e22dfc | docs(design): my payments show what was voided |
| 9 | c09d90c775b8739cf4a45a5fa5fc2b1729e327c1 | docs(design): payments: five columns, a month |
| 10 | 1cae6a749c55e0780524021b141e0dfedc653fe6 | docs(design): the board's desk frames |

Each commit holds exactly its §6 files plus its one `CHANGES.md` row; commit 1 also creates the
*Batch 6* section heading dated 2026-10-13. `git diff --stat origin/main` lists only §5's 16 files
(AC20); `Owner overview.html` and `Finance.html` differ by one line each (AC17, diffs in §3).

## 3. What was run and its results

Pre-flight (§7 step 1): fetched; PR #76 MERGED at `bfe1749` = `origin/main`; tree clean;
batch-5's two quoted lines present on `origin/main`; `git log 1240736..origin/main` on the desk's
eight files empty. Branch `design/desk` cut from `origin/main`. Server: prototype on **5347**.
Tool `pass.mjs` saved verbatim outside the repo; trust run passed (`Desk.html?state=404` blank=false,
`Nope.html` blank=true).

| Commit | `check-parse` | `check-classes` | Browser pass (final) |
|---|---|---|---|
| 1 | 50/50 | 0 new (5 dead, batch 5's) | 8 URLs × 2 var × 3 widths = 48 rows: 0 blank, 0 overflow, 0 errors |
| 2 | 50/50 | 0 new | 48 rows: all clean |
| 3 | 50/50 | 0 new | 7 lines (1 with submit click) × 2 × 3 = 42 rows: all clean |
| 4 | 50/50 | 0 new | 8 URLs × 2 × 3 = 48 rows + 6-row لمى rerun: all clean |
| 5 | 50/50 | 0 new | 3 URLs × 2 × 3 = 18 rows: all clean |
| 6 | 50/50 | 0 new | 8 URLs × 2 × 3 = 48 rows: all clean after server-restart rerun (see §4) |
| 7 | 50/50 | 0 new | 7 URLs × 2 × 3 = 42 rows: all clean |
| 8 | 50/50 | 0 new | 3 URLs × 2 × 3 = 18 rows: all clean (2 reruns; blanks proven false, see §4) |
| 9 | 50/50 | 0 new | 7 URLs × 2 × 3 = 42 rows: all clean first run |
| 10/head | 50/50 | 0 new | **34 distinct frame URLs × 4 var × 3 widths = 408 rows: 0 blank, 0 overflow, 0 errors** (5 files of ≤ 7) |

Looked at with my own eyes (ar + en, light + dark, 390/768/1440 as listed): c1 change/debt/no-mobile/quick-out
toast/fail+429/manual-price; c2 card title+forms/owner ⋯/write-off/debt/pay-visit/picker/overview; c3 renewal
warning+total/submit, post-submit toast naming both items, half-saved retry, custom no-end; c4 here-first
results, primary visit button, 390 order, 1440 side column, visit rate+shift, studentprices, empty; c5 week
warning; c6 five columns at 768, chips, archived+استرجاع, taken error, file header, archive dialog, رهف card;
c7 unpaid-first card (no visits-only), visit payment + ⋯, struck void, void AlertDialog, reception without ⋯;
c8 one card 45/59/104 · 4 دفعات + struck 6 ₪, StatCards at 768, caption, empty/loading; c9 five columns at 768,
chip, void dialog, August range, Finance href.

Head checks (repo root, `npm ci` first — the worktree has no `node_modules`): `npm run format:check` —
pass; `npm run check:links` — pass (2053 links resolve). (`.prettierignore` excludes `docs/design/` and
Markdown, as the plan says.)
Board: 570 frames in 56 sections by grep (plan's expectation exactly); section 56 at top 160000 with 37
frames, last top 168598 — clear of batch 5's last row (157650 + 1035); CDP load confirms 56/570/section-56/lastTop.
AC17: exactly the two one-line diffs (quoted in §3's command output).
Hazards: no object-rest destructuring (only `{ kind, ...payload }`-style spreads into new objects, which the
plan allows); no `size="default"`/`variant="default"`; new top-level names exactly the plan's lists;
`README.md` counts rewritten from grep (570/56); pages/screenshots counts unchanged (41/437).
Before/after pairs (11, uncommitted) in `Downloads\design-fix-desk\pairs\`: K1-390, K2-390, K3-1440,
K4-file-1440, K4-mine-390, K5-390, K6-390, DK-003-390, DK-013-390, DK-017-768, DK-016-768.

## 4. Problems met and how they were solved

1. **PowerShell is not Git Bash.** `date +%F` → used `Get-Date -Format yyyy-MM-dd` (2026-10-13) for the
   CHANGES heading. `grep`/`seq` → `Select-String`/loops. `sed` missing — not needed.
2. **The prototype server kept dying.** The `Start-Job` server died first (pass-6 went all-blank with no
   errors); debug showed `chrome-error://chromewebdata`, unreachable URL — not a code fault. Restarted as a
   detached `Start-Process` python server (PIDs 24608 → 4348 → 13744) and re-ran; all green. Liveness was
   re-verified before later runs.
3. **PayDialog replacement left the old body behind.** The §3.2 edit's `oldString` covered only the dialog's
   head, so the old `return (…)` body survived after the new `UnpaidRow`. Found by counting definitions,
   deleted the exact leftover; `check-parse` + browser pass confirm.
4. **Cold-profile first loads read blank.** Sporadic `blank=true` with zero errors, migrating between
   width/variant cells run to run; the screenshot taken milliseconds later always showed a fully rendered
   page (e.g. pass-6-retry Desk رهف 1440, pass-8 390/empty/loading). Cause: fresh `.profile` per outdir =
   slow first Babel compile exceeding the 3.5 s wait (batch 5's "flaky first load"). Solved by re-running
   into the same outdir (warm profile): 18/18 and 6/6 clean. No code fault; no retry-safety implication.
5. **`gh pr create` quoting did not survive this shell** (multi-word `--title`, `@me`, `docs,area:docs`).
   Created the PR via `gh api …/pulls -f head/base` (space-free args), then `gh pr edit 80` step by step
   with single-quoted values (`'@me'`, `--title '…'`, `--body-file '…'`, `--add-label 'docs,area:docs'`).
   Result verified: #80, exact plan title/body/labels/assignee, head `1cae6a7`.
6. **Two Arabic searches share one screenshot name** (plan warned). `q=لمى` was re-run alone (pass-4-lama,
   before-lama) and both variants were looked at.
7. A stray `node -e fetch` liveness probe crashed with an undici `ERR_ASSERTION` (probe only, not the
   build); liveness was checked with plain `node -e`/`netstat` afterwards instead.

## 5. Anything unexpected

- **Customers count reads 60, not 61.** Adding archived `m16` displaced one generated `g` customer: the
  fill loop tops up to exactly 61 (`DESK.customers.length` = 61: 16 m + 13 f + 32 g), so non-archived = 60
  and archived = 1. This is the plan's literal edit (§3.6) with no adjustment ordered — the planner's
  scratch behaves identically — so it is recorded here, not changed and not a departure.
- `origin/main`'s history also contains #78 below #76; irrelevant — base is `bfe1749` as ordered.
- Nothing else: no new open PRs except #79 (checked) and #80 (this one); no other design batch running;
  `docs/design/screens/` untouched; no images committed.

## 6. Conflict check per open PR

Open PRs at finish: **#80** `design/desk` (this one) and **#79** `feat/space-hours-prices`.
`git fetch origin feat/space-hours-prices && git merge-tree --write-tree --name-only HEAD FETCH_HEAD` →
tree SHA only, no file list, exit OK: **clean against #79** (it works outside `docs/design/`).
No other design PR is open, as expected.

## 7. Departures from the plan, each with why

1. **Before images were not taken on the clean branch before the first edit** (step 5). The server/tooling
   setup finished after commit 1 was already in. Repaired honestly: a pristine `origin/main` worktree
   (`masaha-design-before-tmp`, served on 5348) was screenshotted for the 11 pair cases, and the 11
   before/after pairs in `pairs\` are genuine before-vs-after. Nothing committed either way.
2. **PR created via API + `pr edit`, not one `gh pr create`** (§7 step 9): this shell mangles multi-word
   `@`/comma/space args (§4.5). Title, body-file, assignee and labels are exactly the plan's.
3. **Extra pass runs** beyond the plan's one-per-commit (trust run, لمى single, cold-flake reruns): same
   `pass.mjs`, only to prove clean; results above.
4. **Board verified by grep + CDP counts + the head run**, not by scrolling the 570-iframe board in a
   browser: every one of section 56's 37 frame URLs passed the head run at all widths/variants, and the
   section/frame geometry matches the plan to the pixel.
5. **Eyes on key frames, not literally every PNG**: the pass matrix (408 head rows + per-commit rows)
   covers every URL × variant × width for blanks/overflow/errors; I personally inspected the frames in §3's
   table (each decision at its widths). Hundreds of near-duplicate variant shots were not individually
   opened — the matrix plus the inspected set covers what looking would catch, and the two real layout
   risks the plan names (orphan ⋯, collapsed buttons) were checked at 1440/390.
6. A **temporary worktree** (`masaha-design-before-tmp`) and **two servers** (5347 branch, 5348 pristine)
   were used; all are stopped/removed in §13's cleanup (below), ports verified free.

## 8. DI-41–DI-47, recorded as routed (nothing built for them)

- **DI-41** → docs (with step 7): the data model says a student visit takes "the hour and day prices of its
  audience"; with no student hour/day price published the rate is undefined. Better: the model's *Visit
  charge* says each missing student price falls back to the general one (as this batch's `visitRates` does).
- **DI-42** → API/web worker (step 7): the owner's audit sample has no `visit_written_off` and no void today;
  the audit names K6's act when the API has it. Not this batch's file.
- **DI-43** → worker A (design-system item): `Sheet side="end"` stays ¾ wide at 390 (DK-024/OW-010).
- **DI-44** → later prototype item: the desk's capacity is fixed (`DESK.capacity` 40); the owner's
  `?demo=nocapacity` sets only `OWNER.capacity`.
- **DI-45** → later prototype item: sample customers carry `student: true` (Rahaf) but a Customer has no
  audience in the model; «تسجيل كزيارة» uses it. Harmless while `STUDENT_VISITS` is false.
- **DI-46** → later prototype item: a desk price's «سعر يدوي» badge should name who typed it (ADR 0010 rule 6).
- **DI-47** → docs (with step 7): archiving a customer leaves their uncollected visits on the desk's list;
  the model says nothing — decide whether they stay listed.

---

Cleanup (§7 step 13): server PIDs stopped, Chromes on 9334–9337 killed, background jobs removed,
`masaha-design-before-tmp` worktree removed, `netstat` on 5347/5348/9334–9337 empty, `git status` clean
except the pushed branch. Report saved here; **stopping without merging.**
