# M4 — Check the documents' links in CI (plan)

Worker B · branch `chore/check-links` (not cut yet) · HEAD detached at `origin/main` `49cd088`, clean · #57 (worker A) is the only open PR.

## 1. Summary

A new check, `npm run check:links`, reads every Markdown file and every `docs/….md` citation in code comments, and fails when a relative link, an image path or an `#anchor` does not resolve. It runs in CI (one more entry in the `check` matrix). The documents that say "by hand" say `npm run check:links`, and finding 37 is resolved. No dependency, no change to `package-lock.json`.

## 2. Contract

**Scope**
- `apps/api/scripts/checkLinks.ts` and `checkLinks.unit.test.ts`; the API's unit lane and typecheck learn the new folder; root and API `check:links` scripts.
- `ci.yml`: `check:links` in the `check` matrix.
- Documents: documentation §8, workflow §2 phase 4, `setup.md` (*Commands*, *CI*), `CLAUDE.md` (*Commands*), finding 37 and the findings index.

**Acceptance criteria**
- [ ] `npm run check:links` passes on `main` as it is (measured below: 102 files, 1,606 links, 0 broken) and fails, naming `file:line`, on a broken file, folder, image or anchor.
- [ ] The unit test was seen failing first and covers the seven cases of the prompt §4, plus the ones added in §5.
- [ ] The break was made once on the real repository, seen failing, restored.
- [ ] CI runs it as its own check on the pushed head.
- [ ] Finding 37 is Resolved (status, dated resolution, index); the three documents and `CLAUDE.md` no longer say "by hand".
- [ ] `test:unit -w @masaha/api`, `check:links`, lint, typecheck, `format:check` pass.

**Out of scope:** external links; headings written as HTML (`<h2>`, `<a name>`) or Setext (`===`); reference-style link definitions (none exist); a convention for citing a heading in a code comment (finding below); the component lane, `test:api`, the build.

## 3. Reading done

Finding 37, `.github/workflows/ci.yml`, root and API `package.json`, `apps/api/vitest.config.ts` and `tsconfig*.json`, `apps/web/scripts/checkClasses.ts` and its test (the model: pure `find…` functions, a `main()` guarded by `import.meta.main`, Node runs the `.ts` directly), documentation §8, `setup.md` (*Commands*, *CI*), workflow §2 phase 4 and §9 (dependencies), `eslint.config.js` (no rule is specific to `scripts/`).

**Measured before planning** (a throwaway script in the scratchpad, the prompt's D2/D3 rules): 102 Markdown files, 1,606 relative links and anchors, **0 broken**; 209 `docs/….md` citations in code comments under `apps/` and `packages/`, **0 missing**, 6 with an `#anchor`. So the check lands green, and no document needs a fix.

## 4. The settled decisions, as built

- **D1.** `apps/api/scripts/checkLinks.ts`, run by `node scripts/checkLinks.ts` (as `checkClasses` does); API script `check:links`, root `"check:links": "npm run check:links -w @masaha/api"`. Two small config lines come with it, because the folder is new: `apps/api/vitest.config.ts` unit `include` gains `scripts/**/*.unit.test.ts`, and `apps/api/tsconfig.json` `include` gains `scripts` (so typecheck and lint's project service see it). `tsconfig.build.json` already includes only `src`, so the build never contains it. No dependency; `package-lock.json` untouched.
- **D2.** The anchor rule, ours: drop inline markup (code spans, links and images keep their text, emphasis, HTML tags), lowercase, remove everything that is not a letter, number, mark, `_`, `-` or a space (Unicode, so Arabic headings survive), each space to `-` (so `a › b` is `a--b`, as on GitHub), a repeated heading takes `-1`, `-2`. Headings inside fenced code do not count.
- **D3.** Every `*.md` except under `node_modules`, `dist`, `.git`, `.design-sync/` and `docs/design/prototype/`. In each: a Markdown link or image `(…)` and an HTML `src`, `srcset` (each candidate) or `href`; not `http(s):`, `mailto:`, or a bare `#anchor` that is checked against its own file. Fenced code and inline code are masked, with offsets preserved, so a reported line is the real one. Plus, in every non-Markdown file under `apps/` and `packages/` (outside `node_modules`, `dist`, `src/generated`): each `docs/….md` path, and its `#anchor` when it has one.
- **D4.** `check:links` is added to the matrix. It runs after `npm ci` like the others (about 40 s it does not need; chosen for uniformity, see §5.4).
- **D5.** Documentation §8's third bullet: "`npm run check:links` checks every relative link and anchor of the Markdown files, and every document path cited in a code comment, in CI." Workflow §2 phase 4's exception: "runs `format:check` and `check:links`, and nothing else". `setup.md`: a row in *Commands*, and `check:links` in the *CI* list. `CLAUDE.md` *Commands*: one entry. Finding 37: **Status:** Resolved, a **Resolution** paragraph dated 2026-10-10 (M4: no dependency was needed), moved from *Open* to *Resolved* in the index, in the same commit.
- **D6.** A light independent review follows.

## 5. Stronger decisions

1. **The checker's shape: a pure core.** `checkLinks({ markdown, sources, entries })` takes the files' text and the set of every file and folder path of the repository, and returns the problems; only `main()` walks the disk. The unit test passes literal objects: no temporary directory, no disk, deterministic. *Cost:* the walk is the one part the test does not run; the real-repository break covers it. **Recommended.**
2. **Case-exact paths.** The owner works on Windows, where `Docs/README.md` resolves; on GitHub (Linux) it does not. Checking a link against the *set of real entries*, not `existsSync`, makes the check catch it for free. *Cost:* none beyond one test case. **Recommended.**
3. **Where it lives (D1).** `apps/api/scripts` is not the API's concern, but it is worker B's layer; `apps/web/scripts` has the lane already wired but is A's layer and A has #57 open there. Root `scripts/` would need a new lane. *Cost of D1:* the two config lines above. **Keep D1.**
4. **CI shape (D4).** The check needs only Node, so a job without `npm ci` would answer in about 15 s instead of about 55 s. *Cost:* a second job shape in `ci.yml`, a deviation from "every check is a matrix entry". **Keep the matrix entry**; faster is not worth the second shape for one 55 s check.
5. **A heading cited in a comment is not checked.** Comments write `docs/backend/conventions.md › space-settings`, which no anchor rule can resolve; only the 6 `#` forms are. Changing the convention is a decision for the owner, and out of scope. Recorded here, not as a finding (it is a limit of the check, written in documentation §8).
6. **`docs/design/` stays in** (prompt D3 lists only its `prototype/` as excluded). Measured: 5 Markdown files there, all green. No change.
7. **Rules of the documents the item touches:** documentation §8 and workflow §2 phase 4 are rewritten by D5 (the point of the item), `CLAUDE.md` "update only when a stable, project-wide fact changes": a new command is one. No rule weakened.

## 6. Related findings

- **37**: resolved here.
- **9** (drive-letter case, Resolved): not related, but the case-exact decision in §5.2 shares its cause (Windows paths); noted only.
- None folded otherwise; nothing found to record yet.

## 7. Files

Added: `apps/api/scripts/checkLinks.ts`, `apps/api/scripts/checkLinks.unit.test.ts`.
Edited: `apps/api/package.json` (one script), `apps/api/vitest.config.ts` (one include), `apps/api/tsconfig.json` (one include), `package.json` (one script), `.github/workflows/ci.yml` (one matrix entry), `docs/architecture/documentation.md`, `docs/development/workflow.md`, `docs/development/setup.md`, `CLAUDE.md`, finding 37, the findings index.
**Shared with worker A (#57):** none of these files is in #57's area (web and `docs/features`); the one risk is `docs/architecture/findings/README.md` if #57 records or resolves a finding. At the report: `git merge-tree --write-tree` against #57's head. `package-lock.json` is not touched.

## 8. Tests (lane: API unit, `*.unit.test.ts`; testing §1)

The break each test names is the production change that would make it fail.

| Case | Break it catches |
|---|---|
| a good link, an image, a folder link, a link to a file with `#anchor`, an own-file `#anchor` all pass | the checker reports a good link (a false failure blocks every PR) |
| a missing file | file existence is not checked |
| a missing anchor | anchors are not checked |
| a repeated heading: `#section` and `#section-1` both resolve, `#section-2` does not | the `-1`/`-2` rule is dropped |
| a heading with inline code, a link and `›`: the slug matches GitHub's | inline markup is kept in the slug |
| an Arabic heading resolves | non-ASCII letters are stripped |
| a link inside a fenced block and inside inline code is ignored | code is scanned |
| an HTML `src` and a `srcset` with two candidates, one missing | HTML is not scanned, or only the first candidate is |
| a link with the wrong case (`Docs/a.md`) fails | existence is tested with a case-insensitive disk |
| an external link and a `mailto:` are not checked | external links are followed or reported |
| a code comment citing a missing `docs/x.md` fails; one citing an existing file passes; one with a bad `#anchor` fails | comment citations are not scanned |
| the reported line is the link's own line, after a fenced block above it | masking shifts line numbers |

Seen failing first (the module is written after the test file); then the real-repository break: one anchor in `docs/development/setup.md` changed, `check:links` fails naming it, restored.

## 9. Review Focus (inputs no planned test exercises)

- The walk itself (`readdirSync` recursive, the exclusions, Windows `\` to `/`).
- A link with a space or `%20`, a title (`[a](b.md "t")`), `<…>` form, and an anchor with an uppercase letter (compared lowercase).
- A reference-style link (`[x][y]`) or an autolink: not supported, none in the repository.
- A Setext or HTML heading: not an anchor target, none in the repository.
- CRLF files: line numbers counted on `\n`, text is not trimmed of `\r`.

## 10. Commits

1. `chore: add the documents' link check` — script, test, the two API config lines, the two `package.json` scripts.
2. `chore(ci): run the link check, say so in the docs` — `ci.yml`, documentation §8, workflow phase 4, `setup.md`, `CLAUDE.md`, finding 37 and the index.

Subjects ≤ 50 characters (counted). PR title `chore(ci): check the documents' links` (37). Labels `chore`, `area:ci`, `area:docs`; assigned to the owner. No tool attribution. Never merge.

## 11. Verification

Run, once, on the head: `npm run test:unit -w @masaha/api`, `npm run check:links`, `npm run lint`, `npm run typecheck`, `npm run format:check`; and the one break on the real repository. Not run: `test:component`, `test:api`, `build`, `check:build`, `check:classes` — nothing they cover changes (no web code, no database, no schema). CI runs everything on the pushed head; wait for green and `CLEAN`, then the report to `M4_REPORT.md` with the merge-tree check against #57.

## 12. Decisions needed from the owner

None open. §5.5 (a convention for citing a heading in a comment) is for later, only if wanted.
