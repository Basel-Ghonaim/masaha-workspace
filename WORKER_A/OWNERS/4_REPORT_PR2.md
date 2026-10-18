# OWNERS — PR 2 (`feat/admin-add-owner`) — the executor's report

> Written as the work goes, 2026-10-18. Executor: the second of three pull requests of the
> Work Item, building `2_PLAN.md` §12's four commits only. Nothing here re-decides the plan.

## 1. First checks (2026-10-18)

| Check | Result |
|---|---|
| `gh pr view 88 --json state` | `{"headRefName":"feat/admin-owners","mergeCommit":{"oid":"02b1067a136d3c86378b3da60937c5f51124dc5b"},"number":88,"state":"MERGED","title":"feat(space-links): add the admin's owners page"}` — the precondition, met. |
| Working folder | `C:\Users\basel\masaha` only. `git status --short --branch` → `## main...origin/main`, no changes. |
| `git fetch origin --prune`, `git pull --ff-only` | `Already up to date.` (`HEAD` = `origin/main` = `02b1067a`.) The first attempt, chained after the fetch in one command line, answered `fatal: Cannot fast-forward to multiple branches.`; run on its own it answers `Already up to date.` Recorded as an observation, not a change: no config was touched. |
| Base diff — `git diff --name-status e4e13e9e origin/main` | 29 files: worker B's PACKAGES (#87, `10d1e854`) only — `apps/api/**`, `packages/shared/src/packages/**`, `docs/**`. **No `apps/web` code file** is among them, so §7's code files are untouched. |
| `packages/shared` changed | Yes → `npm run build -w @masaha/shared` run before any web check: exit 0, output `@masaha/shared@0.0.0 build` / `> tsc -p tsconfig.build.json`. |
| Shared documents re-read on `origin/main` | `CLAUDE.md`; `docs/architecture/findings/README.md` (highest finding **81**, so **82** and **83** are free as the plan names them); `docs/api/api-contract.md` §5 › *Owners (the admin)*, *Users (the admin)*; `docs/features/**` as each commit needs them. |
| Open PRs | `gh pr list --state open` → `[]`. No other PR to conflict with at this moment; the early conflict check is repeated at the push. |

### The executor's own checks (plan §13 › first checks, 4)

1. **cmdk `^1.1.1` takes the controlled search.** `node_modules/cmdk/package.json` → `1.1.1`.
   `node_modules/cmdk/dist/index.d.ts` declares `shouldFilter?: boolean` on `Command`
   (two lines: *"Custom filter function for whether each command menu item should matches the given
   search query"*), and on `Command.Input`
   `/** Event handler called when the search value changes. */ onValueChange?: (search: string) => void;`
   with `value?: string`. Both props §9 gives the `Combobox` exist. ✔
2. **`userEvent.setup()` installs a clipboard stub in jsdom** — user-event is `14.6.7`. Checked in the
   component lane in commit 3's own test; if `navigator.clipboard` were still undefined in a hook
   test, it is defined in that test only, on `navigator`, as a platform seam.
3. **`ToggleGroup type="single"` hands `''`** when the chip already on is clicked; `useOwnersList`
   already reads `if (value === '') return;` (seen in `hooks/owners-list/useOwnersList.ts`). ✔
4. **`useServerForm` builds its resolver once** — `useServerForm.ts:84`
   `const [resolver] = useState(() => schemaResolver<Values, Request>(schema, prepare));`
   so the upgrade flag goes in `submit`, never in `prepare`. ✔

Branch cut: `git switch --no-track -c feat/admin-add-owner origin/main` → `Switched to a new branch 'feat/admin-add-owner'`.

## 2. Commits

_(written as each is made)_