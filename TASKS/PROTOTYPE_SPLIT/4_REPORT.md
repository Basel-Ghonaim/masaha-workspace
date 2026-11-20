# PROTOTYPE_SPLIT — the report

> Worker: Claude Code, main folder `C:\dev\masaha\app`. Plan: `2_PLAN.md`, approved with `3_APPROVAL.md`;
> images approved with `5_IMAGES_APPROVED.md`. Nothing merged.

## 1. The new repository

- **URL:** https://github.com/Basel-Ghonaim/masaha-prototype (public; description: the clickable prototype and
  design archive of Masaha). Local folder: `C:\dev\masaha\masaha-prototype` (`core.autocrlf=false`, remote
  `origin`).
- **Head:** `main` = `acf973a6465fc4f514353082158446e87436d77e` (93 commits). **Tag** `design-2026-09-29`
  (annotated, the original message) → `ba6a6c8e5088c2d0c4d6720212d594e1cd443add`, «docs(design): add the design
  archive». `git ls-remote` shows exactly `refs/heads/main` and the tag.
- **Commits:**
  - the archive's 89 commits, split from `docs/design/` and rewritten by R1b; the split tip is
    `b16cbf8d2d894f983e1ffb031c87cdd9d5ebb40f` («fix(design-system): identity review follow-ups», masaha's
    `3b5d9e89`);
  - `7628b81` chore: stand alone at the repository's root — `.gitattributes` (`* text=auto eol=lf`), `.editorconfig`
    (masaha's), `check-parse`'s Babel load (it read `globalThis.Babel`, which only worked under masaha's
    `"type": "module"`: 0/52 at the new root before, 52/52 after), both scripts' usage lines, the five links out of
    CHANGES.md and SCREENS.md → masaha URLs;
  - `0825201` feat: add page variants and their switcher — `prototype/masaha/variants.js`, `prototype/variants/index.js`
    (empty registry), the `.variant-switcher` rule in `masaha.css`, the two script tags in the 38 pages that load
    `i18n.js` and the 5 head templates, both checks extended to `variants/`;
  - `e95add8` docs: add the README and the workers' rules — README.md rewritten, CLAUDE.md;
  - `acf973a` docs: update the brief and add decisions — BRIEF.md, `decisions/README.md`.

## 2. The tree-hash proof

- `git subtree split --prefix=docs/design` in a fresh clone gave `7b4a3055`, whose tree is
  **`c9183a63ff75e6e3138a455ad68f89424828afe9` = `git rev-parse main:docs/design`** in masaha (`f073decb`):
  byte-identical, 89 commits, the oldest «docs(design): add the design archive», the tip's author and date equal
  `3b5d9e89`'s.
- **R1b** (the owner's choice), in the new repository only, with `git filter-branch --index-filter` swapping 58
  blobs. The 58 are the first `About.html` without the project line and the blank line before it, 52 versions
  of CHANGES.md with U11's «The university line goes» → «The project line goes», and the five About
  screenshots with that line painted over in the row's own background (Pillow, in a scratchpad venv). The
  rewritten tip, `b16cbf8`, differs from the plain split by exactly six files: `CHANGES.md` and the five
  `.webp`. `About.html` differs only in the 30 commits before U11 removed the line. Author, committer, dates and
  message are identical in all 89 commits. `refs/original` was deleted, the reflog expired and gc run: the
  old blobs are gone (`git cat-file -e` fails on the old About and image blobs).
- The supervisor approved the five images before publication: 01, 02, 34, 35, 36.

## 3. The scan

Over every commit (1,079 distinct blobs, 448 binaries), the commit messages and the people. Scripts and outputs:
`scan\scan_history.py`, `scan\out\` (masaha, before), `scan\out-rewritten\` (the rewritten history),
`scan\out-final\` (with my commits).
- **Secrets:** none, before or after.
- **E-mails and phones:** placeholders only. `0599 123 456` and the sample admin «باسل» are left, by the
  owner's answer.
- **Identity:** before, `About.html` (one version) and five screenshots named the university, and CHANGES.md U11
  referred to it. After R1b, no revision names it. What is left is the sample rule "a valid university ID", the
  `graduation-cap` icon, the verb خرج/تخرج («قبل أن تخرج»), and words inside the vendored libraries.
- **My own files:** CLAUDE.md states the identity rule without its words (an accepted departure).

## 4. The PR

- **#147**, `chore/design-archive-out`. Head **`a6afc3fbdb1e6b2e9dd2ea82a8aa8ceb2c0159e7`**. Labels: `chore`,
  `area:web`, `area:api`, `area:docs`, `area:ci`; assigned to the owner.
- **CI** on that head: 10 pass (build, check:classes, check:conflicts, check:links, format:check, lint, test:api,
  test:component, test:unit, typecheck), CodeRabbit skipping. **`CLEAN`, MERGEABLE.**
- **Commits:**
  - `de3fd1ed` docs(adr): record the design archive's own repo — ADR 0020 and the map's ADR list (2 files);
  - `b2a4aed9` docs: point the design links to masaha-prototype — 18 files: CLAUDE.md, `docs/README.md` (the
    design section), foundation §13 and §16, `features/auth.md`, `features/directory.md`, `plans/v1-mvp.md`
    (18 links), `plans/foundation.md` (3), findings 14, 19, 32, 73, 74, 96, 130, 215 (pinned to `b16cbf8`),
    `Logo/drawing.ts`, `resetEmail.ts`, `resetEmail.copy.ts` (comments);
  - `a6afc3fb` chore: remove the design archive — `docs/design/` (560 files) and its exclusions: `.prettierignore`,
    `eslint.config.js`, `.coderabbit.yaml`, `apps/api/scripts/checkLinks.ts` (`NOT_SCANNED`).
- 584 files in all (21 edited or added, 560 deleted, 3 configuration). The review threshold is passed, so a
  separate review conversation.

## 5. What ran

All locally on the head, each heavy one through `heavy.mjs split`, one at a time:
- lint: clean;
- typecheck: clean;
- format:check: see §7;
- check:links: 2,781 links in 263 documents and 2,688 source files;
- check:conflicts: none;
- check:classes: 1,990 files;
- `NODE_ENV=production` build, then check:build: clean;
- test:unit: 77 files, 924 tests, and 197 files, 1,401 tests;
- test:component: 348 files, 2,141 tests (second run);
- test:api: 126 files, 1,447 tests.

Also run:
- every repointed URL (14 distinct): 200;
- the four SCREENS.md anchors: present in GitHub's rendering;
- `git grep` for `docs/design` and `../design/`: only the records' kept link text and finding 37's and 74's
  prose remain, plus a branch name in a historical plan.

The new repository's checks: `52/52 blocks parsed`; `364 classes used, 5 dead uses, 0 new`.

**Not run:** lint and typecheck per commit, only on the head. Commit 2's code changes are comments, and commit 3's
are the ESLint config and one constant, which the head covers. **No test added or seen failing first**: no
behaviour changes. `check:links` passing with the archive gone is the proof for `NOT_SCANNED`.

## 6. The breaks made

- The new repository's checks were broken on purpose with a temporary variant, never committed. A dead class in it
  was caught by `check-classes` (`1 new`), and the variant parsed (`53/53`), so both scripts read `variants/`.
- `check-parse` at the new root before its fix: `0/52`, as the plan predicted.
- The served run (127.0.0.1:8765, PID 7976, stopped, port free), headless Chrome:
  - Sign in without `?v=` was the original, with the switcher showing «الأصل» while the temporary variant was
    registered;
  - `?v=check` drew the variant in Arabic light and in English dark, with the switcher;
  - an unknown `?v=` was the original;
  - Register, a page with no variant, had no switcher;
  - the variant inside a frame had no switcher.

  The temporary variant and frame page were removed, and `git status` is clean.

## 7. Problems met

- **The identity hits** (the plan's §6.3): solved by R1b and the owner's approval of the images.
- **`check-parse` at the new root:** solved in `7628b81`.
- **Line endings:** the machine's global `autocrlf=true` would have checked out CRLF. The clone set
  `autocrlf=false`, and `.gitattributes` was added. `git add --renormalize` showed no change. It also staged
  the four edited files, so I reset and staged by path.
- **The test:component run was killed for low memory by the session.** Its `heavy.mjs` wrapper died with it and left
  `heavy-slot-1` held, while `cr` (npm ci) and `super` waited on it. The grant log showed my GRANT with no END,
  and no vitest of mine lived, so I removed the slot and appended a hand-written END line
  (`2026-11-15 11:08:30 … released by hand`). Then I retried once, and the retry passed. Recorded in my memory notes.
- **format:check locally** warns on `.claude/launch.json`. It is untracked (Nov 14, not mine), excluded through
  `.git/info/exclude`, which Prettier does not read. Prettier over every tracked file (`git ls-files | xargs`,
  through `node node_modules/prettier/bin/prettier.cjs`, since `npx.cmd` hits cmd's 8 KB line limit) passes,
  and CI's format:check passed.
- **One commit message** (`chore: remove the design archive`) had a garbled sentence. Amended before the push.

## 8. Unexpected

- The archive's tip, on `main` today, showed the university in five screenshots, not only in history. The
  production repository still shows them in its history after this PR (the owner's decision: no rewrite, no
  finding).
- `git subtree split` prints a progress line per commit (1,081 lines), which flooded one tool output. Harmless.
- The phone-width headless shot crops the page sideways (headless Chrome's minimum window). The original page
  crops the same way, so it is not the mechanism. The 390 view was not seen in a real phone viewport.
- A `gh pr view` query once failed on a TLS handshake timeout; it worked on the retry.

## 9. Early conflict check

`gh pr list --state open`: #147 is the only open pull request, so there is nothing to check against.

## 10. Departures from the prompt and the plan

- **The plan was saved directly**, not through plan mode (the prompt's instruction wins over the `write-plan`
  skill). Stated in the plan.
- **A scratch file in Phase 1:** one list of the archive's links went to the session scratchpad (outside both
  repositories; no secret).
- **The proof is "identical except six files"**, not five: R1b also rewords CHANGES.md's U11. Said before
  publication.
- **CLAUDE.md's identity rule** is written without naming the university, the supervisor or the defence (accepted).
- **ADR 0020's URL** in the new repository's README and CLAUDE.md answers 404 until #147 merges (accepted).
- **The findings' links** pin to `b16cbf8` (the plan's §14, approved).
- **The new BRIEF** renames its old "Variants" (the dark and English versions) to "versions", so the word means
  only the new `?v=` variants. It also says «subscription» for «membership», following the glossary (SH-019).
- **The switcher's position and stacking** are one rule in `masaha.css`, since the vendored bundle has no
  `bottom-3`/`z-50`. Its look uses the bundle's classes.
- **Area labels** `area:web` and `area:api` were added, beside `area:docs` and `area:ci`: three comments and the link
  check live in the apps.

## 11. Left

- **Merge #147:** the owner's.
- **After the merge:**
  - ADR 0020's link in masaha-prototype's README and CLAUDE.md resolves;
  - the `app-design` worktree's copy of `docs/design` is obsolete, and its cleanup is the owner's;
  - finding 215 stays open, its fix now a commit in masaha-prototype.
- **The scratch files** (venv, redaction originals and outputs, screenshots, logs) are in the session scratchpad.
  `C:\dev\masaha\masaha-prototype` is the only new folder.
