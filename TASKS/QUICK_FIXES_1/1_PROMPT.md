# QUICK_FIXES_1 — two small web fixes (one PR)

You are a worker in `C:\dev\masaha\app` (web 5320, API 3320). Fix the two defects below in **one small PR**. This is
a Work Item: follow `CLAUDE.md`, but do **not** run any skill (`start-work-item`, `write-plan`…) and never stop to ask,
except at the one planned stop (§4). **Never merge** — a merge deploys to the live site.

## 0. Rules

- Write a short plan first to `C:\dev\masaha\workspace\TASKS\QUICK_FIXES_1\2_PLAN.md` (the files you will change, the
  tests you will add), then go straight on.
- **Web only** (`apps/web/` and the documents the change makes stale). No `apps/api/`, no `packages/shared/`, no
  migration, no dependency.
- **Do not run tests, lint, typecheck or builds yourself** — the owner runs them (§4).
- `masaha_dev` holds the owner's presentation demo: never reset, seed or write it; never delete `apps/api/.storage`.
- No `git add -A` / `.`; Conventional Commits (subject ≤ 50, a body), atomic; no tool attribution; never print a
  secret.

## 1. Branch

```
git fetch origin
git status --short          # clean
git switch main
git pull --ff-only
git switch -c fix/quick-fixes-1
```

## 2. The fixes

1. **The pagination bar shows with a single page.** On the directory's list with few results the bar reads
   «السابق 1 التالي» / "Previous 1 Next" although there is only one page. It must not show when there is one page
   or none; it shows from two pages up, exactly as today. Find where the paged lists build their bar (the directory
   list, and every dashboard list that uses the design system's `Pagination` — `git grep -n "Pagination"` in
   `apps/web/src`; prefer **one** shared place, e.g. the component or helper that all of them use, over a patch in each
   list) and hide it when the total pages ≤ 1. Keep the page's results and the "dim while a page loads" behaviour as
   they are. Tests (component lane): one page → no bar; two pages → the bar, as today — for the shared place, plus
   one list as a witness.
2. **A stray full stop on the privacy page.** On `/privacy`, section «تواصل معنا» / "Contact us", the sentence's
   closing «.» is left on its own after the email's card/button
   (`apps/web/src/pages/site/public/privacy/PrivacyPage.tsx`, `PrivacyContact`). Remove the lone dot (keep the
   approved sentence's words; the sentence ends at the email). Its test asserts no lone «.» / "." after the email.

## 3. Commits

1. `fix(web): hide the pagination on a single page`
2. `fix(web): drop the privacy contact's stray dot`

## 4. The tests — the one planned stop

When both commits are made, **stop and reply with exactly this block**, then wait:

```
TESTS FOR THE OWNER — in C:\dev\masaha\app (PowerShell), on head <sha>:
npm run format:check
npm run lint
npm run typecheck
npm run check:classes
npm run test:unit
npm run test:component
$env:NODE_ENV='production'; npm run build; Remove-Item Env:NODE_ENV
npm run check:build
Paste back the last lines of each (pass/fail, counts), and any failure in full.
```

All green → §5. A failure → fix it, fold it into its commit (`git commit --fixup <sha>`, then
`GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash origin/main`, a `backup/quick-fixes-1` branch first), and hand the
owner only the commands that failed or that the fix could affect, in the same format.

## 5. Push, PR, reply

- `gh api "repos/Basel-Ghonaim/masaha/issues?state=all&per_page=1" --jq '.[0].number'` + 1 = this PR's number (if a
  document names it).
- `git push -u origin fix/quick-fixes-1`; `gh pr create --assignee @me --label fix --label area:web --title "fix: hide
  single-page pagination and a stray dot"` (≤ 50 characters — recount); the description: the two fixes, the shared
  place chosen and why, the tests, the owner's results, `test:api` left to CI (no API change).
- `gh pr checks <n> --watch` → green; `CLEAN`. Then write `C:\dev\masaha\workspace\TASKS\QUICK_FIXES_1\4_REPORT.md` and
  reply:

```
Status: READY FOR REVIEW | INCOMPLETE (what, why)
PR: #<n> · head <sha> · CI <green/red> · <CLEAN/not CLEAN> · files <n>
Pagination: hidden at ≤ 1 page in <the shared place>; lists covered: <list>
Privacy dot: removed
Owner's results: <each command: pass/fail>
Decisions: <each, one line>   (or "none")
```
