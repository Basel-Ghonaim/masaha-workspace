# Review of #147 (PROTOTYPE_SPLIT) — Claude Code, Opus 5.5
Head: a6afc3fbdb1e6b2e9dd2ea82a8aa8ceb2c0159e7 · commits 3 · files 583 · checks: green (10 pass, CodeRabbit skipping) · head moved: no
Verdict: mergeable after a fix round (F1 and F2 are one line each in two documents, folded into `b2a4aed9`; F3 and F4 can ride along)

## Findings (verified defects only, most severe first)

### F1 — should-fix · Finding 74's resolution still cites `docs/design/CHANGES.md`
- **Where:** `docs/architecture/findings/74-the-designs-gallery-copy-states-limits-the-contract-no-longer-has.md:11`.
- **Seen in the code:** «**Resolution (#132):** … its chooser and refusals the same; `docs/design/CHANGES.md` has the row.» The PR leaves this line as it was. At `a6afc3f`, `docs/design/` has 0 files.
- **Scenario:** a reader checking how 74 was resolved is sent to a path that exists nowhere in this repository. Nothing tells them the row (D6.14, `CHANGES.md:234` at the split) now lives in masaha-prototype. This is the same kind of citation the PR did link in 19:5, 96:5 and 215:6–7, by the plan's own rule for records («a path in backticks is turned into the same text linked to its URL»). The plan's §4.2 listed only 74:5, so the gap came from the inventory. The PR's first acceptance box («No relative link or path citation into `docs/design` remains outside the records' kept link text (`git grep`)») is ticked but false for this line. It also does not mention the two prose mentions the PR keeps on purpose (37:9, 74:7). `check:links` does not read backticked paths in Markdown, so CI cannot catch this.
- **Fix:** link the text, pinned like the other findings: [`docs/design/CHANGES.md`](https://github.com/Basel-Ghonaim/masaha-prototype/blob/b16cbf8d2d894f983e1ffb031c87cdd9d5ebb40f/CHANGES.md). Reword the acceptance line so it names what stays as prose (37:9, 74:7).
- **Belongs:** commit `b2a4aed9` (fixup + autosquash), and the PR description.

### F2 — should-fix · The map says the prototypes have page variants; none exists
- **Where:** `docs/README.md:80`.
- **Seen in the code:** «a screenshot of every frame, the clickable prototypes and their page variants». On masaha-prototype `main` (`acf973a`), `prototype/variants/index.js` is `window.MASAHA_VARIANTS = {};`. The split item set up the mechanism only (P6).
- **Scenario:** a worker reading the map before building a screen looks for variants that do not exist. The line describes something unbuilt as built (documentation §1; CLAUDE.md «Claim only what is true»).
- **Fix:** «the clickable prototypes, where a page gains variants (`?v=`)», or «…and the page-variant mechanism».
- **Belongs:** `b2a4aed9`.

### F3 — nit · `resetEmail.copy.ts`'s comment line grows further past the width, while `resetEmail.ts`'s was rewrapped
- **Where:** `apps/api/src/modules/auth/email/resetEmail.copy.ts:4`.
- **Seen in the code:** the line is now about 156 characters (about 141 on `main`; `printWidth` is 100). In the same commit, `resetEmail.ts:4–9` was rewrapped to 100.
- **Scenario:** cosmetic only, and Prettier does not wrap comments. The two sibling comments the commit touched are now wrapped differently.
- **Fix:** rewrap lines 3–5 to 100 columns. Comment only.
- **Belongs:** `b2a4aed9`.

### F4 — nit · The owner of link integrity does not state the prototype-by-URL rule
- **Where:** `docs/architecture/documentation.md:93` and `:96` (the PR does not touch them); `docs/architecture/decisions/0020-design-archive-own-repository.md:14`.
- **Seen in the code:** §8 says «Links are relative» and «A document never cites a path outside the repository». ADR 0020 decides «This repository links the prototype by URL. A document that cites a file of it links that file in the other repository». `foundation.md:562` now cites `` `prototype/masaha/logo/` … in masaha-prototype ``, a path outside the repository, linked by URL. documentation §2 says an ADR is linked by the document that applies it, but §8 neither applies nor links ADR 0020.
- **Scenario:** someone reading §8 literally flags the PR's own links. The exception lives only in the plan's reasoning («§8 forbids paths, not URLs»).
- **Fix:** one bullet in §8: «The design lives in masaha-prototype; a document cites its files by URL ([ADR 0020](decisions/0020-design-archive-own-repository.md)), unchecked by `check:links`.»
- **Belongs:** `b2a4aed9`, or the next documentation PR (the owner's choice).

## Every pointer of the plan's §4.2 — done / missed / wrong

**Configuration and code**
- `.prettierignore:8–9`: **done**. The blank line, the comment and the entry are gone; the file now ends at `coverage/`.
- `eslint.config.js:248–249`: **done**. The comment and the `globalIgnores` call are gone; the `.design-sync/` ignore is kept.
- `checkLinks.ts:175`: **done**. `NOT_SCANNED = ['.design-sync/']`. It is still read only by `main()`'s Markdown filter; `SOURCE_ROOTS` and `NOT_SOURCES` are unchanged.
- `.coderabbit.yaml:9–11`: **done**. The comment and `path_filters` are gone; `inheritance` and `high_level_summary` are kept.
- `Logo/drawing.ts:2`, `resetEmail.ts:4–5`, `resetEmail.copy.ts:4`: **done**. Comment lines only; the diff touches no code token. F3 covers the wrapping.
- `reminderText.ts:5` and the `*.prototype` test uses: **left**, correctly.
- On `origin/main`, nothing outside the archive excludes `docs/design` other than these four (`git grep` outside `docs/design`). `.gitattributes`, `package.json`, `.github/` and `.design-sync/` have no entry for it.

**Bootstrap, map and platform documents** (active, so on `main`)
- `CLAUDE.md:71`: **done**. The repository's URL, «read-only from here», and a link to ADR 0020.
- `docs/README.md:79–80`: **done**. A new section with the URL, the SCREENS.md URL, the foundation §13 anchor and «read it when your task builds a screen». F2 covers its wording.
- The ADR list, `docs/README.md:62`: **done**.
- foundation §13 (`:474`): **done**. foundation §16 (`:562`): **done**, linking `tree/main/prototype/masaha/logo`.
- `features/auth.md:42`: **done**. Row 7 on prototype `main` is «Forgot / reset password (+ the reset email)».
- `features/directory.md:144`: **done**. R9 is at `CHANGES.md:269` as of the split.
- `plans/v1-mvp.md`: **done**, all 18 links (1 plain, 17 with anchors). The word diff shows only the URL swaps.
- `plans/foundation.md:217, 311, 348`: **done**. Both plans say *Status: Active* and are not under `plans/historical/`, so `main` is right by P7.
- Prose «the prototype's …» in directory, audit, finance, payments and visits; `historical/design-system-layer.md:246` (a branch name); foundation `:3, 527, 530`: **left**, correctly.

**Records** (pinned to `b16cbf8`)
- Findings 14 (both links), 19, 32, 73, 74:5, 96, 130, 215 (both): **done**. 10 links, all pinned. The backticked paths in 19, 96 and 215 became link text, per the plan.
- Findings 37:9 and 74:7 (prose about what was, at the time), 110, 165, the findings README, ADR 0019: **left**, correctly.
- **Missed:** finding 74:11 (F1). It is not in the plan's inventory.
- **Wrong:** none. One note, not a defect: the pin shows the archive as at the split, and for findings 14 and 74 that is already after their #132 resolution. For example, the gallery line at the split reads «حتى 4 ميجابايت» (`profile-a.jsx:592`). So `b2a4aed9`'s body («keeping the evidence as it was») is true only of the state at the split, not of each finding's date. The old relative links showed the same post-fix state, and the pin follows approval 5 exactly.

**From inside the archive out** (in the new repository, not this PR): `CHANGES.md:25, 30, 355` and `SCREENS.md:60` are masaha URLs on prototype `main`. I read them from the local clone, whose `main` equals the remote's `acf973a`.

## The URLs checked
- I ran `curl -sI` on each URL without following redirects. Every one answered **200**:
  - the repository's root;
  - pinned to `b16cbf8`: `CHANGES.md`, `SCREENS.md`, `prototype/Admin%20space%20edit.html`, `prototype/BRIEF.md`, `prototype/Home.html`, `prototype/Owner%20settings.html`, `prototype/Reset%20email.html`, `prototype/masaha/profile-b.jsx`, `prototype/masaha/shared.jsx`;
  - on `blob/main`: `CHANGES.md`, `README.md`, `SCREENS.md`;
  - `tree/main/prototype/masaha/logo`.

  That makes 14 distinct URLs, as the PR says. I also checked the files the comments name: `blob/main/prototype/masaha/logo/masaha-logo-berry.svg`, `masaha-mark-berry.svg` and `prototype/Reset%20email.html`, all 200.
- **Anchors:** the headings of SCREENS.md on prototype `main` are `## Public site (9)` (:5), `## My account (3)` (:19), `## Owner and reception dashboard (13)` (:27) and `## Admin (8)` (:45). By GitHub's slug rule they give `#public-site-9`, `#my-account-3`, `#owner-and-reception-dashboard-13` and `#admin-8`, the four the PR uses.
- **Remote:** `git ls-remote` shows `refs/heads/main` at `acf973a` and the tag `design-2026-09-29`, which resolves to `ba6a6c8`. `b16cbf8` is an ancestor of `main`, so the pins stay reachable.
- **P7:** every record link is pinned, and every active-document link is on `main`. Nothing is the other way round.

## Documents and the ADR
- **ADR 0020:** it follows workflow §7's format (Context · Decision · Alternatives · Consequences) and 0019's header. It is 25 lines, decision-level, with no file names and no implementation details. It covers plan §6.6 and P1/P4 point by point. It is true at the head: «Nothing of them stays here» holds, with 0 files under `docs/design/`. Its line in the map is correct. F4 covers how it relates to documentation §8.
- **CLAUDE.md:** a single line, still a pointer.
- **docs/README.md:** see F2. The section keeps the map's shape: what the repository holds, where, and when to read it.
- **The identity rule:** I searched the PR's added lines, its 3 commit messages, its title and its description for these words, in English and Arabic: university, graduat-, thesis, defence/defense, supervisor, college, academic, capstone, degree, course, student, Quds, branch, جامع, تخر, مشرف, مناقش, كلي, القدس, فرع. The only hits are unchanged context lines («student prices»). Two phrases refer to the rule: «the project's identity rule» in the description and «for the project's public identity» in `a6afc3fb`'s body. Neither says for whom, where or as what the project was made.

## Scope and commits
- **Commits:** `de3fd1ed` (47 characters), `b2a4aed9` (48) and `a6afc3fb` (32). Each has a body giving the why. None has a trailer or a tool attribution, and the tree has no `#PRNUM`.
- **Files:** `de3fd1e` changes 2 (the ADR and the map); `b2a4aed` changes 18, exactly the plan's documents and comments; `a6afc3f` deletes 560 files and edits the 4 configuration files. The 583 files match plan §8's list exactly, with no extra file and no 4th commit (no finding, by approval 3).
  - The plan's estimate («25 edited, 1 added») and `4_REPORT.md`'s «584» are miscounts: the real count is 22 edited and 1 added. The PR description states no total, so it is unaffected.
- **Base:** `f073decb`, which is still the remote `main` (`ls-remote`). GitHub shows the PR CLEAN and OPEN.
- I cannot see from commit objects whether files were staged by path. The contents match the plan.

## Not checked, and why
- **Lint, typecheck, the tests, the build and `check:*`:** not run, by the read-only rule. CI on the head is green.
- **The new repository's own checks** (`52/52`, `364 classes`), the variant mechanism's served run, the history scan and the redacted images: they are not this PR, the supervisor approved them (`3_APPROVAL.md`, `5_IMAGES_APPROVED.md`), and I did not repeat them.
- **The anchors as GitHub renders them:** I worked them out from the heading text with GitHub's slug rule (the one `checkLinks.ts` uses). I did not fetch the rendered HTML, since only `curl -sI` is allowed.
- **Leftover untracked files under `docs/design/` on someone's disk** (for example the `app-design` worktree once it moves to the merged `main`): `check:links` walks the disk, and ESLint and Prettier no longer ignore that folder, so they would read such files. Git objects cannot show this. The cleanup of `app-design` is the owner's (plan §12).
- **Why CodeRabbit skipped:** not looked into. It is not a required check.
