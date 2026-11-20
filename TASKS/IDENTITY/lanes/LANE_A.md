# IDENTITY — lane A: the components (C2, C3, C4)

You are **lane A**, a sub-agent of the IDENTITY item's lead, on **Masaha** (a bilingual Arabic RTL / English web
platform for coworking spaces in Gaza; React 19 + TypeScript + Vite, Tailwind 4, a design-system layer in
`apps/web/src/shared/design-system/`). The lead built the shared layer (tokens, roles, the logo); you build three
commits on top of it, in your own worktree, and **return your report as your final message**. You run in the
background: you cannot ask the lead a question and wait. **Decide and record:** a choice the plan does not settle —
take the safest option, build it, and record it in the report (what, why, how to undo).

## 1. Where you work

- **Folder:** `C:\dev\masaha\app-design-lane-a` (a git worktree). **Branch:** `lane/a`, cut by the lead at the shared
  layer's head `22ddac1c`. Every command starts with `cd /c/dev/masaha/app-design-lane-a && …` (Bash) and every file
  tool takes an absolute path inside this folder. Never touch any other folder: not `C:\dev\masaha\app-design` (the
  lead's), `app-design-lane-b` / `-c` (the other lanes'), `C:\dev\masaha\app` or `C:\dev\masaha\app-pr143`.
- The worktree is installed (`npm ci`, `packages/shared` built) and has its `.env` files. Never print them. **Never**
  run `npm ci` / `npm install`, `git clean`, or delete `node_modules`.
- **No server, no `test:api`, no database, no Chrome, no build.** No push, no merge, no rebase of anything but your
  own commits, no branch other than `lane/a`.
- Write long edits as a Python script in your own scratch folder `C:\dev\masaha\workspace\TASKS\IDENTITY\lanes\scratch-a\`
  (heredocs with quotes and backslashes fail to parse; tools turn `\u` escapes into literal characters). Open files
  with `newline=''` so CRLF / LF are kept as they are.

## 2. Read first

1. `CLAUDE.md` (in your folder), then `docs/development/workflow.md` §3 (*Commits*) and §8, and
   `docs/development/testing.md` §3 (rules 5–7: seen failing, name the break, make the break).
2. **The plan:** `C:\dev\masaha\workspace\TASKS\IDENTITY\2_PLAN_PROD.md` — §1, §2, §4 (*The spark's rules*, *How each
   is built*), §5.2–§5.3 (the roles you use), §6 SD2 and SD6, **§7.1 (every row marked C2, C3 or C4)**, §7.3 (the
   showcase's Nav, Sortable and Field sections), §9 D1 and D5, §10 T12, T20, T21, §11, §12 EC10, §15 commits 2–4.
3. `docs/frontend/design-system/foundation.md` §3 (*Enforcement*), §5, §11, §12 — what the documents say today; you do
   **not** edit them (§6 below).
4. The shared layer as built (read, never edit): `apps/web/src/shared/design-system/tokens/semantic.css` and
   `tailwind.css`.

## 3. What the shared layer gives you (built by the lead; never edit it)

- **Roles and utilities:** `bg-primary-hover` (the ink's hover, `primary-foreground` stays its text); `bg-hover` /
  `text-hover-foreground` (hover: a neutral fill, never the spark); `bg-hover-on-muted` (an ink wash for a control on
  a `muted` or `secondary` ground; its text stays the control's `foreground`); `bg-accent` / `text-accent-foreground`
  and `bg-sidebar-accent` / `text-sidebar-accent-foreground` now mean **selected** (the spark's tint);
  `bg-scrim` / `text-scrim-foreground` (text over a photo — lane B's).
- **The spark** has exactly four utilities: `bg-spark`, `border-spark`, `outline-spark`, `fill-spark`. There is no
  `text-spark` and must never be (no `--color-spark`). Variants work on them (`data-on:border-spark`,
  `after:bg-spark`, `data-[active=true]:before:bg-spark`).
- `primary` / `ring` are the ink (dark in light, near-white in dark).
- `SidebarHeader({ mark, logo })` (the lead's) — leave `SidebarHeader` as it is; your Sidebar edits are the items'.

## 4. Your commits (on `lane/a`, in this order)

Subjects exactly as below (≤ 50 characters, Conventional Commits), each with a body that says **why**:

1. **`feat(design-system): tell hover from selected`** — the plan's C2 rows of §7.1 (the layer's components, the
   features' card hovers, #143's ContactsSheet handle and ContactsView tile, the showcase's `ShowcaseNav` and
   `SortableSection` handle), and **SD2:** `check:classes` refuses the selected tint as a hover (T12). *Body:* the
   tint meant both; the wash for muted grounds; the rule for future copies.
2. **`feat(web): underline links in running text`** — the C3 rows: the link Button (`text-primary underline
   underline-offset-4`, no `hover:underline`), RegisterPage, AboutPage's `#contact` link, SiteFooter, MissingChecklist,
   the showcase's `FieldSection` link; T20. *Body:* ink links read as text unless underlined.
3. **`feat(design-system): mark what matters in spark`** — the C4 rows: Tabs' `line` indicator (`after:bg-spark`), the
   map's selected mark in `leaflet.css` (`outline: 3px solid var(--spark)`), the lifted item (ContactsSheet
   `border-spark`, PhotosEdit `outline-spark`, SortableSection `border-spark`). ToggleGroup's `data-on:border-spark`
   is a C2 row: it belongs to commit 1. *Body:* where the spark shows and why only there.

**The rules while editing** (the plan's, binding):
- Hover = `hover` (or `hover-on-muted` on a muted / secondary ground); selected = `accent` / `sidebar-accent`.
- **Selected keeps its tint under the pointer:** a hover class applies only when the item is not selected
  (`not-data-on:`, `not-data-active:`, `not-data-[active=true]:`, or the caller's own condition). Never rely on the
  order Tailwind emits variants in.
- The sidebar's current item keeps its tint and gains a 3 px spark bar at the inline start, as a logical
  pseudo-element (`relative overflow-hidden` + `data-[active=true]:before:absolute data-[active=true]:before:inset-y-0
  data-[active=true]:before:start-0 data-[active=true]:before:w-0.75 data-[active=true]:before:bg-spark`), clipped by
  the item's radius. Its badge is unchanged.
- **The spark** is a fill, an edge, an outline or a mark only: never text, never on an action (no Button variant
  names it), never destructive.
- Logical classes only (`start`/`end`, `ms`/`me`, …); no arbitrary value outside the layer; no colour, font or CSS
  outside the layer; no new user-facing string (every word through the copy catalogue — none is expected).
- Touch only the files the rows name, plus what EC10 finds (below) and the tests. **No drive-by changes.** Something
  else wrong that you notice: record it in your report, do not fix it.
- **D1 / EC10:** search `apps/web/src/features` and `apps/web/src/pages` for a ghost or outline Button, or any
  `hover:` class, drawn inside a `bg-muted` / `bg-secondary` container; each takes `hover-on-muted` as D1 says (the
  plan names DataTable's sort headers, the calendar's today, FilterTag's remove, #143's contact tiles). List every
  one you found and what you did, in the report.
- **The inventory:** after commit 1, `npm run check:classes` must pass on the whole `src` — the new rule finds any
  `hover:bg-accent` (or the other forms) the plan's table missed; each takes the same rule and is named in your
  report.
  **EC1 (the lead, on `main` `f58c12a8`, #143 merged):** the plan's inventory command finds no file beyond §7.1's
  tables; #143's ContactsSheet, ContactsView and PhotosEdit read as the plan's rows say; its fix round added no
  colour class. The lead's C6 changed only `SidebarHeader` in `Sidebar.tsx`: your edits there are the items'.

## 5. Tests — each seen failing first, each break made

| Test | File · lane | Proves | Seen failing |
|---|---|---|---|
| T12 | `apps/web/scripts/checkClasses.unit.test.ts` · unit | the rule refuses `bg-accent`, `text-accent-foreground`, `bg-sidebar-accent`, `text-sidebar-accent-foreground` under `hover:`, `focus:`, `focus-visible:`, `aria-expanded:`, `data-open:`, `has-data-open:`, `data-[selected=true]:`, `data-highlighted:`, alone or compounded (e.g. `md:hover:`, `dark:focus:`, `not-data-active:hover:`); and allows `bg-accent`, `data-on:bg-accent`, `data-[active=true]:bg-sidebar-accent` | before the rule |
| T20 | `components/actions/Button/Button.component.test.tsx` · component | the link variant is underlined at rest (`underline`, no `hover:underline`); no variant's class names the spark | before the Button change |
| T21 | the existing tests of every component and feature file you touch · component / unit | still green, axe clean (jsdom has no colour contrast) — ContactsView's `<li>`/`<a>` restructure keeps its focus ring on the anchor and its name | n/a (existing) |

- The rule's place: `apps/web/scripts/checkClasses.ts`, a third finder beside the physical and arbitrary ones,
  applied to every file under `apps/web/src` (the layer included), reported like the others, with its own message
  line ("… the selected tint as a hover …"). Export the finder for the unit test as the others are. The comment
  example `bg-(--brand-600)` names a primitive that no longer exists: write `bg-(--spark-500)`.
- **Breaks** (testing §3 rule 7), each from a backup copy, restored by copy, the red line copied into the report:
  T12 — the rule removed, then narrowed to `hover:` only (a `focus:bg-accent` must still fail); T20 —
  `hover:underline` back; `border-spark` added to the outline variant.
- Expectations are written by hand, never computed by the code under test; each title says what it proves.

## 6. Documents — in your report, not in the files

You do **not** edit `foundation.md`, `docs/development/setup.md` or `CLAUDE.md` (the lead folds your lines into your
commits after the join). Write, per commit, the exact text to add or replace, with its section and the line it
replaces (quote it):
- C2: foundation §3 *Enforcement* — a point (e): the selected tint is never a hover (`check:classes`); §5 *usage
  rules* — hover vs selected (hue + a second mark; selected keeps its tint under the pointer; a control on a muted
  ground takes the wash); §11 — "A hover never fades a fill" rewritten (secondary and destructive mix toward the
  foreground, the ink's hover is `primary-hover`, outline / ghost / items hover with `hover`, never `accent`); §12
  rows: Table, DataTable (sort header), Select / Combobox (highlighted item), ToggleGroup (hover; on: the tint, a spark
  edge, the check), SegmentedControl (the wash on hover), Sidebar (hover; current: tint + spark bar), Calendar (filled
  days' hover); `setup.md`'s commands row for `check:classes` and `CLAUDE.md`'s commands line (its third rule).
- C3: §5 *usage rules* — links in running text are underlined; §12's Button row (the link variant).
- C4: §12 rows — Tabs (`line`: a spark indicator) and Sortable (its callers draw the lifted item with a spark edge);
  §3's paragraph on the map's stylesheet (`leaflet.css`): the selected mark is ringed in the `spark`, no longer on
  `primary`.

## 7. Commands — every heavy one through the grant script

The grant: `node C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs lane-a <command…>` (it waits for a slot
and ≥ 4 GB free; it may wait minutes — let it; never bypass it). Heavy = lint, typecheck, any test run.
- Typecheck: `node …/heavy.mjs lane-a npm run typecheck`
- Lint, **your files only:** `node …/heavy.mjs lane-a npx eslint <your files…>`
- Tests, **your files only:** `node …/heavy.mjs lane-a npx vitest run --project component <files…> --root apps/web`
  (and `--project unit` for the unit files).
- Light, no grant: `npm run check:classes`; `npx prettier --check <your files>` (and `--write` on them only).
- **A run killed for memory** (exit 137, a signal, "JavaScript heap out of memory"): retry it once; killed again —
  record it and carry on; the lead's full run and CI judge.
- **Every commit lints and typechecks on its own** (run both before each commit). Prettier-clean files only.

## 8. Committing

- `git status` before each commit; stage **by path** (never `git add -A` / `git add .`); no tool attribution, no
  `Co-Authored-By`, no "generated with" anywhere.
- A fix to an earlier commit of yours folds into it (`git commit --fixup <sha>` then
  `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash 22ddac1c`), after `git branch backup/lane-a-<n>` first.
- At the end: `git log --oneline 22ddac1c..lane/a` shows exactly your three commits, the tree clean.

## 9. Limits

No merge; no push; no migration; no dependency; no database; never `db:seed`; never weaken, skip or delete a test,
a check or a lane to pass; no production code only a test uses; never stop on file count — report it; public text
never names hosting providers, free plans or session durations; nothing outside your folder but your scratch folder.

## 10. Your report = your final message

The harness refuses a sub-agent's report file: return it as text; the lead saves it as `lanes\REPORT_A.md`.
- `lane/a`'s head (full sha) and each commit: sha, subject (length), files.
- Per test: the red line (copied) before its code, the green line after; per break: the red line and "restored".
- EC10's list; the inventory's extra files (anything `check:classes` found beyond the plan's table).
- The commands run and their results (typecheck, lint, the test files), any wait or kill.
- **The document lines** of §6, ready to paste.
- Every decision you took without the lead (what, why, undo), and anything that behaved unexpectedly.
