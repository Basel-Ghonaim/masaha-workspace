# FINDING_232 — Phase 2 report

## Pull request and head

- PR: [#160](https://github.com/Basel-Ghonaim/masaha/pull/160)
- Head SHA: `f548475de76e34376649c89c9b6a87008b0a73c3`
- GitHub CI: all required checks passed on this head; CodeRabbit was skipped.
- GitHub merge state: `CLEAN`.

## Commits

- `f548475de76e34376649c9b6a87008b0a73c3` — `refactor(shared): remove unused password rules`

## Verification

**Run locally and passed:**

- `npm run build -w @masaha/shared`
- `npm run format:check`
- `npm run lint`
- `npm run typecheck`
- `npm run check:links` — all 2,830 links resolved.
- `npm run check:conflicts`
- `npm run test:unit` — shared: 29 files / 383 tests; API: 77 files / 924 tests; web: 199 files / 1,477 tests (305 files / 2,784 tests total).
- `npm run build` — passed.
- `$env:NODE_ENV="production"; npm run build; npm run check:build; Remove-Item Env:NODE_ENV` — passed; no showcase code in 78 build files.
- `git diff --check`

**CI passed:** `build`, `check:classes`, `check:conflicts`, `check:links`, `format:check`, `lint`, `test:api`, `test:component`, `test:unit`, and `typecheck`. CodeRabbit was skipped.

`test:api` and `test:component` were not run locally because this change does not alter API or component behavior; CI ran both successfully. No E2E/browser run was done because no screen or user-visible behavior changed.

## Breaks and tests seen failing

Temporarily omitted `bytes` from `passwordRules()` and ran the focused ordered-key unit test. It failed as expected: received `['minLength', 'letter', 'digit']` instead of all four keys. Restored `bytes`; the complete unit lane passed.

## Problems and resolutions

An initial build and `check:build` without an explicit production `NODE_ENV` included the development showcase and reported 1,178 strings. The owner identified that `apps/web/.env` sets `NODE_ENV=development`; this was a false alarm, not a change regression. Rebuilt with `NODE_ENV=production` and reran `check:build`; it passed, checking 1,174 strings across 78 build files. No unrelated files were changed.

The full build emitted non-failing chunk-size warnings.

## Unexpected outcomes

The environment-dependent showcase false alarm described above. No unresolved issues.

## Early conflict check

`gh pr list --state open` listed only this PR (#160); there were no other open PR heads to compare. No conflicts to report.

## Departures from the prompt

None. The extra `npm run check:build` added in the approved plan initially failed in development mode, then passed in production mode as confirmed above. The branch was pushed only to `chore/finding-232`; it was not merged. Returned to `main`, which is clean and up to date with `origin/main`.
