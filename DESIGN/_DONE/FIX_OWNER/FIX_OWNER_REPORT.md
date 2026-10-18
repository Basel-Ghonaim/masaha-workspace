# Design fix 5 (the owner's management) — execution report

Executor's report for `C:\Users\basel\.prompt\MASAHA_DESIGN\PROMPT\FIX_OWNER_EXEC.md`,
building `C:\Users\basel\.prompt\MASAHA_DESIGN\PLAN\FIX_OWNER_PLAN.md` in
`C:\Users\basel\masaha-design`, branch `design/owner`, prototype on port 5346.

## 1. PR and head

- **PR:** #76 — https://github.com/Basel-Ghonaim/masaha/pull/76
- **Title:** `design: the owner's management` (the plan's exact title; set via `gh pr edit`)
- **Head SHA:** `5a22676` (`5a2267633ca434b5ab32c26d58f15e1f0e95a478`)
- **Base:** `main`. CI: all 10 checks green; `mergeStateStatus`: **CLEAN**. Never merged.

Note on how the PR came to exist: after the 13 commits were pushed, PR #76 already
existed (created externally at 2026-10-13T11:41:44Z with the title
`docs(design): the owner's management (Batch 5)` and a non-plan body). The title
and body were corrected to exactly what the plan writes out (`PR_BODY.md`).
Two untracked files were found in the worktree that this run did not create and
did not touch: `pr-body.md` (a draft PR body) and `final-report-76.md` (another
report draft). Both left alone.

## 2. Commits (13, in order, exact subjects)

| SHA | Subject |
|---|---|
| `c60db41` | docs(design): the owner's bar on a phone |
| `33c2c21` | docs(design): counted words in Arabic |
| `ead8b0d` | docs(design): one editor; prices on their page |
| `1132f17` | docs(design): capacity and stay move to Settings |
| `db762dd` | docs(design): packages: the form the model holds |
| `d36930e` | docs(design): announcements follow the model |
| `4da9418` | docs(design): the closure extension stands alone |
| `9677833` | docs(design): staff: say what reaches people |
| `9bcc39f` | docs(design): reports: the reporter is a visitor |
| `e6420aa` | docs(design): finance: one month, lists that page |
| `a305713` | docs(design): the owner's overview is a work queue |
| `a12d1b1` | docs(design): the owner's audit log |
| `5a22676` | docs(design): the board's owner frames |

All subjects ≤ 50 chars, all `docs(design):`, staged by path only. One amend each
on commits 1 (hooks fix, §5-problems) and 6 (missing DS imports + README bullet).

## 3. What was run and its results

- `git fetch origin --prune` + `git status --short` (clean) + branch cut
  `git switch --no-track -c design/owner origin/main` at `e30a86c` (= `origin/main`
  at start; `main` later moved to `3c3dc47b` with zero `docs/design/` changes —
  build continued, no stop needed).
- Server: `python -m http.server 5346 --bind 127.0.0.1` in
  `docs/design/prototype` (PID 16804; stopped at the end).
- Pass script written verbatim to `tools/pass.mjs`. Validated before trusting:
  `Owner overview.html?state=404` → blank=false; `Nope.html` → blank=true.
- **Before images:** `urls-before.txt` (20 URLs) with `--shots` timed out at
  300 s with 83 files captured (partial — the tail admin URLs missing). The
  admin before-images were re-taken from a scratch `origin/main` worktree on
  port 5347 (`admin-before/`, then worktree removed, 5347 freed).
- **At every commit:** `check-parse.mjs` + `check-classes.mjs` (both pass every
  time; head: **50/50 blocks from 41 pages**, 333 classes, 5 dead uses all
  pre-existing, 0 new), `git diff --stat` (only the commit's files), commit,
  then the plan's URL table through `pass.mjs` **with `--shots`**, and the PNGs
  looked at at 390, 768 and 1440 (Arabic + dark variants in the matrix).
- **Commit 13 full matrix:** 21 frame URLs × 4 variants (ar, en, dark,
  en+dark) × 3 widths = **252 cells: 0 blank, 0 overflow, 0 console errors**.
  (`Flows - states.html` itself excluded: a static board page with no
  `#ds-root`, ~5000 px wide by design — the probe's blank/overflow flags do not
  apply; the page loads and renders.)
- **Head checks:** `npm run format:check` — pass. `npm run check:links` — pass
  (1940 links in 112 documents and 1011 source files). (As the plan says,
  `.prettierignore` excludes `docs/design/` and Markdown from `format:check`.)
- **No-money check:** `grep Money|₪|money` on `Owner overview.html` → empty.
- **Push:** `git push -u origin design/owner`. **PR:** title/body set to the
  plan's. **CI:** build, check:classes, check:links, format:check, lint,
  test:api, test:component, test:unit, typecheck all pass; CodeRabbit skipped.
- **After images:** `after/` holds 15 decision shots (DI-10, O1, O2, O3, O5,
  O6, O8, O9, O10, O11, O12, O13, OW-015, OW-017 ×2); per-commit shot dirs
  `pass-1…pass-13` hold the rest. Nothing committed.

## 4. Problems met and how they were solved

1. **Conditional-hook crash introduced by commit 1** (`?drawer=open`, Desk,
   Finance error rows): `const rail = useIsTablet() && !useIsDesktop()`
   short-circuits `useIsDesktop()` on phones, so the pass harness's
   width-cycling re-rendered with a different hook count. Fixed **inside this
   batch's file** by calling both hooks unconditionally
   (`tablet`/`desktop`/`rail`/`phone`); commit 1 amended. No visual change.
2. **`SHIFTS_NOW` temporal-dead-zone trap in the plan's §3.5 order:** the plan
   lists `publish('shifts', SHIFTS_NOW())` before the `SHIFTS_NOW` definition,
   which would throw at module eval. Defined `SHIFTS_NOW` first (same code,
   safe order).
3. **Missing DS imports:** the new announcement sheet uses `RadioGroup`,
   `RadioGroupItem`, `ToggleGroup`, `ToggleGroupItem`, which the page did not
   destructure (`ReferenceError`, whole page blank). Added them to the page's
   destructuring; commit 6 amended. (`DateField`/`TimeInput` are globals.)
4. **Stale headless Chrome holding port 9333:** after one hung run, an old
   `chrome.exe` kept the debugging port, so later passes drove the dead
   browser and reported phantom errors (`O.demo is not a function`,
   `O.announcements.map` on undefined, white screenshots). Solved by killing
   the listener before every pass and reading `pass.tsv` directly. Real bug
   count from those artifacts: zero.
5. **Flaky first-navigation blank:** the first URL of a fresh profile
   occasionally reports blank with no errors (cold Babel compile > 3.5 s).
   Always passes on re-run; treated as harness flake, recorded per commit.
6. **PowerShell vs plan's Git-Bash syntax:** `gh … --jq` quoting and `tail`
   don't work in PowerShell 5.1 — used `ConvertFrom-Json`/`Get-Content -Tail`
   instead. No `jq` installed, as stated.

## 5. Anything unexpected

- `origin/main` moved (`e30a86c` → `3c3dc47b`, PR #73 `feat/public-directory`)
  mid-build; it touches no `docs/design/` file, so the build continued per the
  plan's rule.
- `AdminShell` (`admin.jsx:27`) contains the **same** short-circuit hook
  pattern fixed in `OwnerShell`, and the harness's width-cycling logs React
  hook warnings on the admin pages. **Pre-existing on `origin/main`** (proven
  by screenshotting the admin editor from a scratch `main` worktree: identical
  warnings, identical pixels). Not fixed — `admin.jsx` is never-edited (AC19).
  The admin editor's before/after images are pixel-identical (golden, focus).
- `ExtendDialog`'s `onDone` (plan-verbatim) does not close the dialog; the
  success toast fires and the card behind updates. Built exactly as written;
  flagging in case the owner wants the dialog to close on success.
- `?tab=ended&edit=a4` opens with no console error, so README's known-limit
  bullet about it was deleted in commit 6 as the plan allows.
- Check-scripts chatter (`gone md:max-w-32 … drop it from KNOWN`) is advisory;
  dead-use count fell 8 → 5, new dead uses always 0.

## 6. Conflict check per open PR

| PR | Branch | Result |
|---|---|---|
| #77 | `feat/space-photos` | clean |
| #76 | `design/owner` (this) | — |
| #75 | `design/account` | **conflicts, fast path only**: `docs/design/CHANGES.md`, `docs/design/INDEX.md`, `docs/design/README.md`, `docs/design/prototype/Flows - states.html` — the four shared files, as the plan predicts |
| #74 | `feat/admin-space-editor` | clean |

Checked with `git merge-tree --write-tree --name-only HEAD FETCH_HEAD` per
head. Whichever of #75/#76 merges second rebases and keeps both sides
(CHANGES/INDEX/board/README).

## 7. Departures from the plan, each with why

1. OwnerShell hooks made unconditional (P1) — the plan's one-line addition
   exposed a real Rules-of-Hooks crash under width changes; same behaviour,
   stable hooks.
2. `SHIFTS_NOW` defined before its first call (P2) — the plan's order throws
   at eval; identical code, safe order.
3. Announcement sheet date/time pair written directly as
   `grid gap-3 md:grid-cols-2` (plan: try `grid-cols-2` first, stack if it
   overflows) — stacked from the start; no overflow at 390 in any variant.
4. RadioGroup/ToggleGroup imports added to `Announcements.html` (P3) — the
   plan's sheet needs them; missing import = blank page.
5. `Owner settings.html`'s «الباقات والأسعار» link also moved to
   `Packages.html#prices` — the plan's §3.3 rule ("every «الأسعار» link").
6. README frame counts written as 515/54/41 for this batch alone (plan's
   numbers); if batch 4 (#75) merges first, the rebase sums both.
7. After-images kept per-commit (`pass-1…pass-13`) plus a 15-file `after/`
   decision set, instead of one `after/` re-run — identical evidence, no
   extra runs. Before-images partial (P-before); admin before-images retaken
   from `main`.
8. `gh --jq` replaced by `ConvertFrom-Json` (P6); `tail` by `Get-Content -Tail`.
9. PR #76's pre-existing title/body corrected to the plan's via `gh pr edit`.
10. SCREENS row 12/18–24 and `Owner audit.html` line as written; audit page
    wrapped without `DeskProvider` (like the admin's page — the plan's only
    listed differences kept).

## 8. DI-30–DI-40 routing (per the owner's answers)

- **DI-30** (price-table «الفترة»/«لمن»), **DI-31** (group-naming save toast),
  **DI-33** (empty gallery `EmptyState`) — **not built**; routed to worker A's
  editor items.
- **DI-32** (photo limit/WebP) — question for the API; nothing built.
- **DI-34** (admin's phone bar) — recorded for the next admin item
  (hook-warning evidence in §5).
- **DI-35** (`Desk.html#unpaid` anchor), **DI-36** (`Payments.html?month=`)
  — recorded for batch 6 (desk); Finance's «عرض الكل» lands unfiltered.
- **DI-37** (one password-dialog component) — recorded for the web worker
  (`StaffPassDialog` is a deliberate copy; `admin.jsx` untouched).
- **DI-38** — **folded**: per-card `actionKey`s
  (`save-attendance`/`save-pricing`/`save-message`); verified one card fails
  alone.
- **DI-39** (¾-wide `Sheet` at 390) — recorded (design system); sheets kept
  single-column, no overflow.
- **DI-40** (foundation §13 screens) — recorded; audit page listed under
  *Also in the archive* with finding 14.
- **S1–S14** built as recommended (S2 deletion, S5 «إيقاف الوصول», S7 no desk
  shortcut, S8 «بلا حالة مباشرة», S9 whole hours, S12 «النظام», S13 copy,
  S14 comma `?demo=`).

## 9. Cleanup

Stopped: prototype server (PID 16804), every `chrome.exe` holding
`--remote-debugging-port=9333`, scratch `main` worktree removed.
`netstat -ano | grep 5346` and `| grep 9333` print nothing (only TIME_WAIT
leftovers). Background shells: none left running. **Never merged.**

## 10. Review fixes (FIX_OWNER_FIXES.md, after PR #75 merged)

- **Rebase:** `git fetch --prune origin`, `git rebase origin/main`
  (`1240736`). Conflicts only in the four shared files, all inside the
  allowed set: `CHANGES.md` + `INDEX.md` (first commit) and
  `INDEX.md`/`README.md`/`Flows - states.html` (board commit). Kept both
  sides — batch 4's §54 then batch 5's §55. README counts are true counted
  totals, not sums: **533 frames in 55 sections** (board iframes/section
  divs counted with a script), 41 pages. Batch 5 stays at top 150000; batch
  4 ends at 149904 — no overlap.
- **(a)** `ExtendDialog` calls `onClose()` in the success path (fixup folded
  into `the closure extension stands alone`): verified live via CDP —
  `?tab=ended&extend=a6`, click the destructive action, the dialog is gone
  and the a6 card shows the extended line. Failures keep it open (P8).
- **(b)** `AdminShell` hooks unconditional — own commit
  `fix(design): the admin shell's hooks run always` (47 chars):
  `Admin space edit.html?id=focus` cycled 390→768→1440 with zero hook
  warnings (it warned on every width switch before, pre-existing on `main`).
- **(c)** `check-classes.mjs` KNOWN dropped `hover:opacity-90`,
  `md:max-w-32`, `md:w-72` (fixup folded into the board commit): script
  output fully clean, 0 new dead uses.
- Autosquash rebase folded both fixups; final history is 14 commits
  (13 × `docs(design):` + 1 × `fix(design):`), every subject ≤ 50.
- Checks on the pushed head (`2fa9476`): check-parse 50/50, check-classes
  clean, format:check + check:links (2028 links) pass locally; all 10 CI
  checks green, PR **CLEAN**.
- Posted the "Review fixes" comment on #76 and updated the PR description's
  counts. Removed the leftover `final-report-76.md` from the worktree.
