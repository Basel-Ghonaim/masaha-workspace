# M4 — report: check the documents' links in CI

## 1. Pull request

**#58** https://github.com/Basel-Ghonaim/masaha/pull/58 · branch `chore/check-links` · head `d148212668012e250a4204955c7d7706c9962fae` · CI green on that head (9 of 9 checks, including the new `check:links`) · GitHub `CLEAN`. Not merged.

## 2. Commits

1. `ea68d1f` chore: add the documents' link check — `apps/api/scripts/checkLinks.ts` and its unit test, the `check:links` scripts (API and root), `apps/api/vitest.config.ts` and `tsconfig.json` (the new folder), and `eslint.config.js` (one glob, see §8).
2. `d148212` chore(ci): run the link check, say so in the docs — `ci.yml`, documentation §8, workflow §2 phase 4, `setup.md`, `CLAUDE.md`, finding 37 and the index.

PR title `chore(ci): check the documents' links` (37 characters). Labels `chore`, `area:ci`, `area:docs`; assigned to the owner.

## 3. What was run, and what was not

| Check | Result |
|---|---|
| `npm run test:unit -w @masaha/api` | 34 files, 644 tests pass (22 of them the new file) |
| `npm run check:links` | 1,817 links in 102 documents and 937 source files, all resolve |
| `npm run lint` | clean (after the config fix in §6) |
| `npm run typecheck` | clean (after the import fix in §6) |
| `npm run format:check` | clean |
| CI on the head | all 9 checks pass |

Not run: the component lane, `test:api`, `build`, `check:build`, `check:classes`, locally — nothing they cover changes (no web code, no database). CI ran them all on the pushed head.

Before the build, on `main` as it was: a throwaway script in the scratchpad (the prompt's D2/D3 rules) found 102 files, 1,606 links, 0 broken, and 209 `docs/….md` citations in comments, 0 missing. The real check agrees: 1,606 + 209 = 1,815, then 1,817 after the two lines this PR adds to documents.

## 4. Breaks and tests seen failing first

- **Seen failing first:** the test file was written before the module; the first run failed to import `./checkLinks`. 22 cases: a good file, folder, image, own-file and cross-file heading; a missing file, a missing image, a link climbing out of the repository, a missing heading (own and other file); repeated headings `-1`/`-2` and the one past them; fenced code and inline code ignored; the real line below a fenced block; a heading inside a fence is no anchor; HTML `src`, `href` and each `srcset` candidate; external links and `mailto:` not checked; a wrong-case path fails; an anchor with capitals; an Arabic heading; a missing document cited in a source comment, and a bad anchor in one; and 7 slug cases.
- **The break on the real repository, once:** in `docs/development/workflow.md` line 48, `setup.md#running-a-second-folder` became `…folders`. `check:links` failed with `docs/development/workflow.md:48  setup.md#running-a-second-folders  (no such heading)` and `1 broken link(s) of 1815 checked`, exit 1. Restored with `git checkout`; the check passes again.
- **A bug the first green run exposed:** the source-comment case failed on first run — a citation is a path from the repository's root, and I had resolved it from the citing file's folder. Fixed (the check now takes the resolved target); the test is the one that caught it.

## 5. Problems met, and how each was solved

- A heredoc with quotes and backticks failed to parse twice (the checker's source, the PR body). Both were written with the Write tool instead (the memory note on long scripts in files).
- My first attempt at the break matched nothing: the link I tried lives in `workflow.md`, not `setup.md`. Checked the diff stat showed no change, and retried on a real link.
- The first `gh pr create` did not run because the command before it had failed; the branch was pushed in the next call.

## 6. Anything that behaved unexpectedly

- **Lint failed on the new test**, not on the checker: `eslint.config.js` had a block `files: ['apps/api/**/*.test.ts']` that sets `boundaries/dependencies`, but the plugin is declared only for `apps/api/src/**` and `apps/api/test/**`. A test in `apps/api/scripts` matched the block without the plugin ("could not find plugin boundaries"). I narrowed the glob to `apps/api/src/**/*.test.ts` and `apps/api/test/**/*.test.ts`, the two folders the block above declares. Lint passes. This is a third configuration line the plan did not list (see §8).
- **Typecheck:** the API is `NodeNext`, so the test's import needed `./checkLinks.ts`; the web's habit of an extensionless import fails there.
- Prettier reformatted `ci.yml`'s matrix from one wrapped line into a list, one task per line (11 lines instead of 1). Harmless, and the same content.
- A new `docs/….md` in a code comment is now checked by path, so the checker's own two files are excluded from the citation scan (their fixtures cite missing paths on purpose).

## 7. The early conflict check

Open pull requests: **#57** (`feat/admin-add-space`, worker A).

`git merge-tree --write-tree` of this head against `origin/feat/admin-add-space`: **conflicts** in two files, both trivial and both the same row:
- `docs/development/setup.md`: both sides edit the `check:build` row of *Commands* (mine adds the `check:links` row above it; #57 changes the `check:build` row's text).
- `CLAUDE.md`: both sides edit the `check:build` line of *Commands*.

`eslint.config.js` and `docs/architecture/findings/README.md` auto-merge. Neither file is conflicting against `main`: this PR is `CLEAN` as it stands. Whichever PR merges second resolves two one-line conflicts in its rebase; nothing is resolved now (rebase only when dirty).

## 8. Departures from the prompt

- **`eslint.config.js` changed** (one glob, §6): the prompt and plan named only the vitest include and the tsconfig include. It is required for lint to pass once a test lives in `apps/api/scripts`, and it keeps the boundary rule for the folders it was written for. Stated here and in the PR description.
- The prompt's D3 says "each `docs/….md` path cited in a code comment"; the check scans the whole source file for such a path (not only comments), excluding the checker's own two files. A path in a string would be checked too. None exists today; a comment-only parser would add a per-language grammar for no case found.
- Nothing else: D1, D2, D4, D5 and every "stronger decision" are built as the plan says (case-exact paths, the matrix entry, `docs/design/` kept in, `›` citations noted and left).
