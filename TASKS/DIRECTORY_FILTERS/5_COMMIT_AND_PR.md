# DIRECTORY_FILTERS — commit, push, open the PR (the owner approved, 2026-11-07)

Same session, same branch (`refactor/directory-filters` in `C:\dev\masaha\app`). The owner approved the work as it
stands in the working tree. Now: one commit, push, open the PR, wait for CI. **The owner merges — never you.**
This replaces §6 of `3_EXEC_PROMPT_FINAL.md`.

## 1. Commit

1. `git branch --show-current` must say `refactor/directory-filters`; `git status -s` must list only files under
   `docs/design/` (8 modified). Anything else: stop and say so.
2. `git branch backup/directory-filters-4` and copy the 8 modified files to
   `C:\dev\masaha\workspace\TASKS\DIRECTORY_FILTERS\backup-4\`.
3. `git reset --soft main`, then `git restore --staged .` — the 5 old commits are folded away, nothing is staged, the
   working tree is untouched. `git status -s` again: the same files under `docs/design/` only.
4. **One commit** — the whole round is one unit (the directory's filters redesigned in the prototype, with the
   records that describe it, which the workflow puts in the same commit). Stage by explicit path, never
   `git add -A` / `git add .`:
   ```
   git add docs/design/prototype/Directory.html "docs/design/prototype/Flows - states.html" docs/design/prototype/masaha/data.js docs/design/prototype/masaha/masaha.css docs/design/prototype/masaha/shared.jsx docs/design/prototype/masaha/space-parts.jsx docs/design/INDEX.md docs/design/CHANGES.md
   ```
   Subject (≤ 50 characters): `feat(design): rework the directory's filters`. Body (wrap at 72): what changed —
   the price (a subscription choice with a range, the order by price in the sort), «الدوام» (open now by the hours on
   Gaza's clock for every space, open in the evening by the schedule or a declared evening shift, Friday), «أخرى»
   (verified, students), an unverified space's state by its hours, hours optional, the sheet's Arabic plurals, the
   1024–1279 column — and why (the owner's refactor round 1, decisions of 2026-11-05 to 2026-11-07). **No tool
   attribution, no `Co-Authored-By`.**
5. `git log --oneline main..HEAD` must show exactly one line; `git status -s` must be clean (an untracked
   `.claude/launch.json` is excluded locally and must not appear; if it does, do not add it).

## 2. Checks before the push (all from the repository root)

- `node docs/design/scripts/check-parse.mjs`
- `node docs/design/scripts/check-classes.mjs`
- `npm run check:links` — CI checks every Markdown link and anchor; `INDEX.md` and `CHANGES.md` changed.
- `npm run check:conflicts`
All four must pass. No test lane, build, lint or typecheck is needed: no file under `apps/` or `packages/` changed
(say so in the PR's Evidence). If `npm run` fails for a missing dependency, stop and print the error — do not run
`npm ci`.

## 3. Push and open the PR

1. The next number: `gh api "repos/{owner}/{repo}/issues?state=all&per_page=1&sort=created&direction=desc" --jq
   '.[0].number'` — expect 136, so this PR is **#137**. If any changed file cites a placeholder PR number, put the
   real one in before pushing (amend the one commit). Do not add a PR number where none is cited.
2. `git push -u origin refactor/directory-filters`.
3. `gh pr create --base main --head refactor/directory-filters --assignee @me --label feat --label area:docs
   --title "feat(design): rework the directory's filters" --body-file <a file you write in the workspace task folder,
   6_PR_BODY.md>`. The body, in English, with these sections:
   - **Summary** — refactor round 1 of the live site: the directory's filters redesigned in the prototype only; the
     web and the API follow in a later PR.
   - **Scope / Acceptance criteria / Out of scope** — in scope: the 8 files under `docs/design/`; acceptance: the
     decisions below as built; out of scope: `apps/`, `packages/`, the docs outside `docs/design/` (D4, U1, U5 and ADR
     0008's revision are owed by the production step), spaces for women (approved as a direction, own ticket), the
     owner-declared evening shift (future feature, simulated in sample data only).
   - **The decisions built** — the price (segmented «الكل · ساعة · يوم · أسبوع · شهر», «الكل» default; a range once a
     subscription is chosen, validated; cards show the price; the price order in the sort, shown only once a
     subscription is chosen); «الدوام» («مفتوحة الآن» by the hours on Gaza's clock and closures, verified and
     unverified alike, a space without hours never passes; «مفتوحة مساءً» = closes at 20:00 or later on one of its open
     days or declares an evening shift; «مفتوحة يوم الجمعة»); «أخرى» (verified, students); «ممتلئ» a badge, not a
     filter; an unverified space's card says open/closed by its hours (neutral badge); hours optional (ZM Hub has
     none; its card and page say so); the sheet's Arabic plurals; the filter column 4/12 between 1024 and 1279.
   - **Change type** — design prototype (docs).
   - **Evidence** — the four commands of §2 with their output lines; the pages looked at in a browser at 390, 768,
     1024 and 1440, Arabic and English, light and dark; **not run:** test lanes, build, lint, typecheck (no
     application code changed).
   - **Screenshots** — "Kept locally in `Downloads\directory-filters-shots\` (not pushed)", and ready prototype URLs
     for the owner (serve `docs/design/prototype` on 5325).
   - **Definition of Done checklist** — the workflow's items that apply, ticked honestly; the rest marked N/A with why.
   No `Closes #` (no Issue). No tool attribution anywhere.

## 4. Wait for CI, then report

- Watch with a **bounded** loop (≤ 30 minutes, every 2 minutes): `gh pr checks <n>` and `gh pr view <n> --json
  mergeStateStatus --jq .mergeStateStatus`. Do not use `jq` directly; use `gh --jq`.
- If a check fails: read its log (`gh run view <id> --log-failed`), fix only what this PR caused, fold the fix into
  the one commit (`git branch backup/directory-filters-5` first, `git commit --amend` or `--fixup` + autosquash),
  `git push --force-with-lease`, and watch again. A failure not caused by this PR: stop and report it.
- When every check is green on the pushed head and the state is `CLEAN`: write
  `C:\dev\masaha\workspace\TASKS\DIRECTORY_FILTERS\4_REPORT.md` — the PR number and URL, the head sha (full), the
  commit, `git diff --stat main`, the checks' output, CI's result, and anything noticed outside scope (recorded, not
  fixed). Then stop. **Do not merge. Do not delete any branch.**
