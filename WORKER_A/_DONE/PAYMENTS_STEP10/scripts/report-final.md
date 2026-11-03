## Push, the PR, CI

- Just before the push: `origin/main` `76661f7c` (unmoved); open PRs none; `gh api "repos/Basel-Ghonaim/masaha/issues?state=all&per_page=1" --jq '.[0].number'` → 128, so **129**.
- `scripts\prnum-lead.sh 129` (a temporary branch rewritten by `git filter-branch --tree-filter` over `origin/main..`,
  checked — no `#PRNUM` in any commit's tree, only number lines changed, the same files, commits and subjects — then
  the branch moved onto it; no `reset --hard`): "PRNUM OK #129 fcf46637 (was 921b1a2e)"; `git diff
  backup/step10-pre-prnum HEAD`: 16 files, 94 lines, every one a `#PRNUM` → `#129`; the description's `#PRNUM` none.
- `git push -u origin feat/step10-screens` (a new branch); `gh pr create --assignee @me --label feat --label area:web
  --label area:docs --label area:design-system --title "feat(web): announcements, data reports, favourites"` (50) →
  **https://github.com/Basel-Ghonaim/masaha/pull/129** — the number the commits carry; no second push.
- **CI on `fcf46637bf84ab2de598abf0f8080bb42f8964f2`:** build pass (39 s), check:classes pass, check:conflicts pass,
  check:links pass, format:check pass, lint pass (1m53s), test:api pass (6m6s), test:component pass (4m53s), test:unit
  pass (1m18s), typecheck pass (52 s); CodeRabbit skipping. `mergeStateStatus` **CLEAN**; 248 files.
- No `Co-Authored-By`, "generated with" or tool name in any commit message; no `fixup!` left.

## The commits (final)

`4ebc2785 perf(design-system): serve the calendar on its own` (50) · `18db0601 fix(design-system): start a range on
each click` (47) · `a23896a7 test(web): pre-bundle the calendar for jsdom` (44) · `ddaa3db2 feat(announcements): list a
space's announcements` (49) · `74000c57 feat(announcements): post and edit an announcement` (50) · `2279134a
feat(announcements): end, start or delete one` (45) · `2fa45cf8 feat(announcements): extend after a closure` (43) ·
`7d892c86 feat(design-system): add a removable filter tag` (47) · `44e8ee1f feat(data-reports): decide a space's
reports` (44) · `dc427a54 feat(data-reports): list every space's reports` (46) · `fda9559c feat(data-reports): show a
user's own reports` (45) · `c9739dcd feat(data-reports): report wrong information` (44) · `97ec50fe
feat(design-system): add the heart icon` (39) · `1285d9ab feat(favorites): save a space from its card` (43) ·
`0b75e262 feat(favorites): list a user's favourite spaces` (47) · `fcf46637 feat(announcements): show a space's
announcements` (49).

## Memory and the grants

- Every heavy run went through `scripts\heavy.mjs` (`scripts\heavy-grants.log`, UTC): two slots at most, ≥ 4 GB free
  at each grant. Waits: lane C's typecheck once ("both slots taken", 10:42). **No kill** in any lane or in the lead's
  runs. Free memory before the lead's full lanes: 5,734,580 KB (first component pass), 5,997,116 KB (second), 4,972,360
  KB (the pass with the preload that skipped a file's tests — a hook timeout, not a kill).

## Decisions taken without the owner

None **SERIOUS** (§6's list: no money, role, private data, plan decision or redesign touched).

- **LEAD-D1** — no seam commit; each lane added its own entries (alphabetical, apart). *Undo:* none needed.
- **LEAD-D2** — PR 4a waits on PR 3's commit 2: lane C built the heart first, then rebased onto lane B's commit 2.
- **LEAD-D3** — finding 169's break made through the main barrel from a site page (Home); a first break from the site's
  lazy shell stayed green, since a lazy page is outside the first download `check:build` guards.
- **LEAD-D4** — the lanes' worktrees made by the lead (`git worktree add`), not by the Agent tool.
- **LEAD-D5** — the heavy runs' grant by a script (two slots, ≥ 4 GB, logged), since a background sub-agent cannot wait
  on a question. *Undo:* grant by message.
- **LEAD-D6** — the lanes' reports returned as text (the harness refuses a sub-agent's report file) and saved by the lead.
- **LEAD-D7** — the routes test's 403 miss checked on `main` and Lane 0 (red on both under load) → later found to be
  the calendar's cold import (LEAD-D11).
- **LEAD-D8** — the public pieces: `ClosureAlert` (presentational, the sheet's preview) and `ClosureNotice({ items })`
  (the page's), a local `PublicAnnouncement` type (the feature may not import the directory's). *Undo:* rename back.
- **LEAD-D9** — the closure's notice keeps the layer's polite `role="status"` for a warning. *Undo:* `role="alert"`.
- **LEAD-D10** — finding 180 recorded (check 5.k: the space page's and «بلاغاتي»'s chunks reach `data-table` /
  `calendar` through the features' one entry). *Undo:* drop the finding.
- **LEAD-D11** — react-day-picker pre-bundled for the component lane (`deps.optimizer.client`), its own Lane 0 commit;
  a test preload, a lazy load of the page's pieces and the locales by subpath tried and dropped. *Undo:* drop the
  commit.
- **LEAD-D12** — the real run's defect (a guest's favourite saved on the return but shown unpressed): the scope's
  in-flight reads cancelled before the invalidation, with a test, folded into `feat(favorites): save a space from its
  card`. *Undo:* revert the three lines.
- **The lanes' decisions** (each in its report): lane A LA-D1–D15 (LA-D1: #128's count worded «يشمل التمديد {n}
  اشتراكات.» with its line); lane B LB-D1–D17; lane C LC-D1–D21. None SERIOUS.
- **Observation, not a decision:** while the favourites' ids are on their way, a heart is drawn unpressed (S13's
  design); a press then saves again (204, idempotent).

## Leftovers

- **Branches (local):** `feat/step10-screens` (the PR's); backups `backup/step10-pre-join-a`, `-pre-join-b`,
  `-pre-join-c`, `backup/step10-lane-b-pre-join`, `backup/step10-lane-c-pre-join`, `backup/step10-pre-fold-180`,
  `-pre-fold-preload`, `-pre-unpreload`, `-pre-reorder`, `-pre-fold-heart`, `-pre-prnum` (all mine; kept for the
  owner; delete after the merge). The lane branches `lane/a`, `lane/b`, `lane/c` deleted once the PR was open.
- **Worktrees:** `app-lane-a`, `app-lane-b`, `app-lane-c` removed (`git worktree remove`; their leftover
  `node_modules\@masaha` junctions deleted, the folders gone). `app-b`, `app-design`, `app-review` untouched.
- `git status --short` clean in `C:\dev\masaha\app`; ports 3320 and 5320 free; `masaha-postgres-1` left running (it was
  running at the start).
- Outside the repository: this report, `scripts\` (the lanes' folders, the run's scripts and logs, the backups) and
  `shots\lead\`.

## Not run locally, or not as planned

- The final-report skill's format: the prompt's §9 reply and this report are the ones the owner asked for.
- Nothing else: every lane of §5 ran on the head, and CI ran them all again.
