## Summary

This PR implements five goals:

1. **Stray conflict marker**: Removes a leftover `<<<<<<< HEAD` line from `docs/design/INDEX.md:868`.

2. **New `check:conflicts` CI check**: Adds `npm run check:conflicts` that fails when any git-tracked file contains a merge-conflict marker (`<<<<<<< `, `>>>>>>> `, `||||||| `, or `=======` between `<<<<<<< ` and `>>>>>>> `). It skips binary files, prints each hit as `<file>:<line> <marker>`, and a one-line total. Modeled on the existing `check:links` script.

3. **CI wiring**: The new check is added to the root `package.json`, `apps/api/package.json`, the GitHub Actions matrix in `.github/workflows/ci.yml`, `docs/development/setup.md` (commands table and CI sentence), and `CLAUDE.md` (commands list).

4. **Workflow §9 reword**: The "merge apart" rule now reads: "a merge into `main` that deletes or renames no file **the PR refers to**, and changes none of the PR's files, calls for no rebase and no new CI run". This closes #71.

5. **Carried from #111 (documents only)**: Four document fixes from #111's review:
   - `docs/features/lookups.md` line 5: Scope now includes "Home and Directory" (was "the site's Directory" only).
   - `docs/frontend/architecture.md` §2: The sub-bullet "Offline and the general error (`RetryState`, PU-024)" gains `(2026-10-24, #111)`.
   - New finding 137: `docs/architecture/findings/137-homes-area-counts-fall-short-past-a-thousand-spaces.md`
   - New finding 138: `docs/architecture/findings/138-a-failed-refresh-keeps-a-status-that-still-reads-live.md`
   - `docs/architecture/findings/README.md`: Both findings added under `## Open` after 136.

All `npm run check:links` passes with the new files.

## Changes

### Commit 1: `fix(docs): drop a stray conflict marker` (a4a4fcd2)
- `docs/design/INDEX.md`: Removed the stray `<<<<<<< HEAD` line at line 868.

### Commit 2: `chore(ci): fail on merge-conflict markers` (a1f595ce)
- New: `apps/api/scripts/checkConflicts.ts` — the check script
- New: `apps/api/scripts/checkConflicts.unit.test.ts` — unit tests (8 cases)
- `apps/api/package.json`: Added `check:conflicts` script
- `package.json`: Added root `check:conflicts` script
- `.github/workflows/ci.yml`: Added `check:conflicts` to matrix
- `docs/development/setup.md`: Added command row and updated CI sentence
- `CLAUDE.md`: Added command to list

### Commit 3: `docs(workflow): say what a merge apart guards` (6648f370)
- `docs/development/workflow.md`: Reworded the "merge apart" sentence in §9 to specify "no file the PR refers to". Closes #71.

### Commit 4: `docs: record #111's review` (5b7a7ca0)
- `docs/features/lookups.md`: Updated Scope line
- `docs/frontend/architecture.md`: Added date/PR to sub-bullet
- New: `docs/architecture/findings/137-homes-area-counts-fall-short-past-a-thousand-spaces.md`
- New: `docs/architecture/findings/138-a-failed-refresh-keeps-a-status-that-still-reads-live.md`
- `docs/architecture/findings/README.md`: Added both findings under Open

## Evidence

- `npm run test:unit -w @masaha/api` → 65 test files, 872 tests passed
- `npm run check:conflicts` → "No conflict markers found." (exit 0)
- `npm run check:links` → "2678 links in 181 documents and 1789 source files all resolve." (exit 0)
- `npm run format:check` → "All matched files use Prettier code style!" (exit 0)
- `npm run lint` → exit 0
- `npm run typecheck` → exit 0

### Unit test red→green
- **Red** (module missing): `Error: Cannot find module './checkConflicts.ts'`
- **Green** (after script created): 8 tests passed

### Break test (manual conflict injection)
- Added `<<<<<<< HEAD` to `docs/design/INDEX.md:868` (uncommitted):
  ```
  docs/design/INDEX.md:868  <<<<<<<
  
  1 conflict marker(s) found in 1 file(s).
  exit 1
  ```
- After `git restore docs/design/INDEX.md`:
  ```
  No conflict markers found.
  exit 0
  ```

Closes #71