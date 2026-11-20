# IDENTITY — lane B: the shells and the fixes (C5, C7)

You are **lane B**, a sub-agent of the IDENTITY item's lead, on **Masaha** (a bilingual Arabic RTL / English web
platform for coworking spaces in Gaza; React 19 + TypeScript + Vite, Tailwind 4, a design-system layer in
`apps/web/src/shared/design-system/`). The lead built the shared layer (tokens, roles, the `Logo` component,
`SidebarHeader`'s new API); you build two commits on top of it, in your own worktree, and **return your report as
your final message**. You run in the background: you cannot ask the lead a question and wait. **Decide and
record:** a choice the plan does not settle — take the safest option, build it, record it (what, why, undo).

## 1. Where you work

- **Folder:** `C:\dev\masaha\app-design-lane-b` (a git worktree). **Branch:** `lane/b`, cut by the lead at the shared
  layer's head `22ddac1c`. Every command starts with `cd /c/dev/masaha/app-design-lane-b && …` (Bash) and every file
  tool takes an absolute path inside this folder. Never touch any other folder: not `C:\dev\masaha\app-design` (the
  lead's), `app-design-lane-a` / `-c`, `C:\dev\masaha\app` or `C:\dev\masaha\app-pr143`.
- The worktree is installed (`npm ci`, `packages/shared` built) and has its `.env` files. Never print them. **Never**
  run `npm ci` / `npm install`, `git clean`, or delete `node_modules`.
- **No server, no `test:api`, no database, no Chrome, no build.** No push, no merge, no branch but `lane/b`.
- Write long edits as a Python script in `C:\dev\masaha\workspace\TASKS\IDENTITY\lanes\scratch-b\` (heredocs with
  quotes fail to parse; tools turn `\u` escapes into literal characters). Open files with `newline=''`.

## 2. Read first

1. `CLAUDE.md` (in your folder), `docs/development/workflow.md` §3 (*Commits*) and §8, `docs/development/testing.md`
   §3 (rules 5–8: seen failing, name the break, make the break, a lazy route's first load in a `beforeAll`).
2. **The plan:** `C:\dev\masaha\workspace\TASKS\IDENTITY\2_PLAN_PROD.md` — §1, §2, §4 (the logo's places and sizes),
   §5.2 (`skeleton`, `scrim`), §6 SD4, SD5, SD9, SD10, **§7.1's rows for Skeleton and PhotosView**, **§7.2 (the
   shells)**, §10 T18, T19, T21, §12 EC6 and EC14 (what the lead's visual pass will measure), §15 commits 5 and 7.
3. `docs/frontend/design-system/foundation.md` §12 (Skeleton's row) and §16 *The logo* (the lead's) — read, never edit.
4. The shared layer as built (read, never edit): `components/display/Logo/` (`Logo`, `LogoProps`: `form` `'full'` |
   `'mark'`, `label` — named with it, decorative without), `components/navigation/Sidebar/Sidebar.tsx`
   (`SidebarHeader({ mark, logo })`: the rail shows `mark`, desktop and the phone drawer show `logo`), the tokens.

## 3. Your commits (on `lane/b`, in this order)

Subjects exactly as below (≤ 50 characters), each with a body that says **why**:

1. **`fix(web): raise the skeleton and photo count`** — `components/feedback/Skeleton/Skeleton.tsx`: `bg-muted` →
   `bg-(--skeleton)` (the component token, 1.11 → ≈ 1.27 on a card); #143's
   `features/spaces/components/photos/PhotosView.tsx`: the «+N» count's `bg-foreground/60 … text-background` →
   `bg-scrim … text-scrim-foreground` (3.64 → ≥ 4.5 over any photo; the token test proves the pair). *Body:* those
   numbers.
2. **`feat(web): show the logo in every shell`** — §7.2:
   - `pages/site/shell/SiteHeader.tsx`: the home `Link` holds `<Logo label={copy.site.wordmark} className="h-10" />`
     in place of the text, the link taking the layer's one focus style (SD10: `rounded-sm focus-visible:outline-2
     focus-visible:outline-offset-2 focus-visible:outline-ring`) in place of the browser's default.
   - `pages/site/shell/SiteMenu.tsx`: the drawer's `<p>` wordmark → `<Logo label={copy.site.wordmark}
     className="h-10 self-start" />` (`self-start`: a stretched column would centre it). Keep the dialog's own name.
   - `pages/site/shell/FocusLayout.tsx`: as SiteHeader (sign in, register, forgot, reset, the forced change).
   - `pages/dashboard/shell/AdminLayout.tsx` (today, after the lead's C6, a `tile` constant passed as both `mark` and
     `logo`; it goes): `SidebarHeader mark={<Logo form="mark" className="size-9" />}
     logo={<Logo className="h-9" />}`, both decorative (no `label`); its children: `<span className="sr-only">
     {copy.site.wordmark}</span>` and the caption («إدارة المنصة», `copy.dashboard.platformAdmin`, as today), so the
     header is read «مساحة، إدارة المنصة» once. The «م» tile goes.
   - `SpaceLayout` / `SpaceHead` (the owner's and reception's shell): **unchanged** (OD3 (a)).
   - Comments that say "the wordmark" in these files: keep them true (the logo is the wordmark drawn).
   - `copy.site.wordmark` stays the logo's name; no catalogue line changes; `PageHeader`'s and `DocumentTitle`'s
     fallback text stay text.

**Rules:** logical classes only; no arbitrary value outside the layer (`h-10`, `h-9`, `size-9` are scale classes);
no colour, font or CSS outside the layer; no new user-facing string; touch only these files and their tests; no
drive-by changes — anything else wrong you notice: record it in your report, do not fix it.

## 4. Tests — each seen failing first, each break made

| Test | File · lane | Proves | Seen failing |
|---|---|---|---|
| T18 | `pages/site/shell/SiteLayout.component.test.tsx`, `pages/site/auth/changePasswordPage.component.test.tsx` · component | the header's home link is named «Masaha» / «مساحة» by the logo's image (`getByRole('link', { name })` containing `getByRole('img', { name })`); the phone menu holds the logo; the focus shell's header too | before C7's change |
| T19 | `pages/dashboard/routes.component.test.tsx` · component | the admin's sidebar header: the logo drawn and hidden from assistive technology, the name «مساحة» for assistive technology once, the caption; no «م» tile | before C7's change |
| T21 | the existing tests of the files you touch (Skeleton, PhotosView's section tests, the shells) · component | still green, axe clean | n/a (existing) |

- C5 has no new component test: the token test (the lead's) proves the values; the class change is proven by the
  lead's visual pass. If Skeleton has a test that names `bg-muted`, update it to the new class (and say so).
- **Breaks**, each from a backup copy, restored by copy, the red line copied into the report: T18 — the text wordmark
  back in SiteHeader; the logo without its `label`. T19 — the «م» tile back; the name read twice (the logo given a
  `label` beside the sr-only name).
- Expectations by hand; each title says what it proves; a lazy route's first load is paid in a `beforeAll` as the
  files already do (testing §3 rule 8). The routes test is long: run only it and the site shell's tests, by file.
- Known slow-machine misses (findings 55 / 87's family): a routes test that misses its 3 s wait in a busy run but
  passes alone — re-run that file alone, record both lines, carry on.

## 5. Documents — in your report, not in the files

You do **not** edit `foundation.md` or any document. Write, per commit, the exact text to add or replace, with its
section and the line it replaces (quote it):
- C5: foundation §12's Skeleton row (its fill is the `skeleton` token, ≥ 1.2:1 on card and background).
- C7: foundation §16's *Where it shows* (the site's header, the phone menu and the focus shell 40 px; the admin's
  sidebar 36 px, the mark 36 px on its rail; not the owner's and reception's shell, OD3 (a)).

## 6. Commands — every heavy one through the grant script

The grant: `node C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs lane-b <command…>` (it waits for a slot
and ≥ 4 GB free; it may wait minutes — let it; never bypass it). Heavy = lint, typecheck, any test run.
- Typecheck: `node …/heavy.mjs lane-b npm run typecheck`
- Lint, **your files only:** `node …/heavy.mjs lane-b npx eslint <your files…>`
- Tests, **your files only:** `node …/heavy.mjs lane-b npx vitest run --project component <files…> --root apps/web`
- Light, no grant: `npm run check:classes`; `npx prettier --check <your files>` (and `--write` on them only).
- **A run killed for memory** (exit 137, a signal, "JavaScript heap out of memory"): retry once; killed again — record
  it and carry on; the lead's full run and CI judge.
- **Every commit lints and typechecks on its own.** Prettier-clean files only.

## 7. Committing

- `git status` before each commit; stage **by path** (never `git add -A` / `git add .`); no tool attribution, no
  `Co-Authored-By`, no "generated with" anywhere.
- A fix to an earlier commit folds into it (`git commit --fixup <sha>`, then
  `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash 22ddac1c`), after `git branch backup/lane-b-<n>` first.
- At the end: `git log --oneline 22ddac1c..lane/b` shows exactly your two commits, the tree clean.

## 8. Limits

No merge; no push; no migration; no dependency; no database; never `db:seed`; never weaken, skip or delete a test,
a check or a lane to pass; no production code only a test uses; never stop on file count — report it; public text
never names hosting providers, free plans or session durations; nothing outside your folder but your scratch folder.

## 9. Your report = your final message

The harness refuses a sub-agent's report file: return it as text; the lead saves it as `lanes\REPORT_B.md`.
- `lane/b`'s head (full sha) and each commit: sha, subject (length), files.
- Per test: the red line (copied) before its code, the green line after; per break: the red line and "restored".
- The commands run and their results, any wait or kill, any slow-machine miss.
- **The document lines** of §5, ready to paste.
- Every decision you took without the lead (what, why, undo), and anything that behaved unexpectedly.
