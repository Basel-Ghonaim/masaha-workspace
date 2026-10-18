# M2 report — the findings one file each, and the capability documents by layer

## 1. Pull request and head

- **PR #52:** https://github.com/Basel-Ghonaim/masaha/pull/52, "docs: one file per finding, documents by layer".
  - Labels `docs` and `area:docs`; assigned to the owner.
  - **Head:** `3d6e4c695c39937fc0bba2836339f8af9ba21a0a`.
- **Branch:** `docs/findings-per-file`, cut with `--no-track` from `origin/main` at `d4d5b57` (#50's merge). `main` has not moved since.
- **CI:** run 37776554780 on `3d6e4c6` succeeded: lint, typecheck, format:check, check:classes, build, test:unit, test:component and test:api.
- **Merge state:** GitHub shows `CLEAN`.

## 2. Commits

1. `f155e77 docs: give each finding its own file`
   - the 45 files and the index; finding 38 resolved (#52);
   - `findings.md` removed;
   - 53 inbound links in 19 documents repointed, and the four code comments;
   - the wording of workflow §2 and §4, the map, and documentation §1, §2 and §8.
2. `b566352 docs(features): split decisions and history by layer`: the five capability documents, and documentation §5.
3. `3d6e4c6 chore(skills): push review fixes in open-pr`: step 8.

In all, 71 files change (+664, −590).

## 3. What was run, and what was not

The three proofs were re-run on the final head. Each script lives in the session's scratchpad and is never committed.

**Proof 1.** The 45 files against `findings.md` at `main`, each link compared by the target it resolves to.

`node proof1.mjs . origin/main`

```
base origin/main: 45 findings · files: 45 · equal: 44 · links compared by target: 74
38-the-findings-are-one-file.md differs:
  - **Status:** Open · **Date:** 2026-10-06
  + **Status:** Resolved · **Date:** 2026-10-06
  + **Resolution (2026-10-08, #52):** each finding is a file of its own in this folder, named after its heading's anchor, and the [index](<docs/architecture/findings/README.md>) lists them by status. Every inbound link, from the documents, the records and the code's comments, was repointed in the same PR.
```

**Proof 2.** The link checker over the whole set, then the index check.

`node check-links.mjs .`

```
Markdown files: 101 · links checked: 1571 · anchors checked: 600 · code files: 975 · docs paths cited in code: 231 · broken: 0
```

`node check-index.mjs .`

```
finding files: 45 · index: Open 22, Accepted 3, Resolved 20 · problems: 0
```

- **Baseline, before the move:** on `main` (`d4d5b57`), 1,522 links and 647 anchors in 56 Markdown files, plus 231 citations, with 0 broken.
- **Before each commit:** the checker ran each time, with 0 broken.
- **Why anchors fell from 647 to 600:** each anchor into `findings.md` became a link to a file, so 47 fewer anchors are checked.

**Proof 3.** Per capability document, against commit 1, so the split commit is measured alone.

`python proof3.py f155e77`

```
auth Decisions: before 15, after 15 (API decisions 5, Web decisions 10); missing 0; added 0 (expected 0) OK
auth History: before 8, after 8 (API history 4, Web history 4); missing 0; added 0 (expected 0) OK
auth rest of the document (bar the part headings and the date): unchanged
users Decisions: before 8, after 8 (API decisions 1, Web decisions 7); missing 0; added 0 (expected 0) OK
users History: before 8, after 9 (API history 4, Web history 5); missing 0; added 1 (expected 1) OK
users rest of the document (bar the part headings and the date): unchanged
space-links Decisions: before 21, after 21 (API decisions 8, Web decisions 13); missing 0; added 0 (expected 0) OK
space-links History: before 6, after 9 (API history 5, Web history 4); missing 0; added 3 (expected 3) OK
space-links rest of the document (bar the part headings and the date): unchanged
lookups Decisions: before 27, after 27 (API decisions 11, Web decisions 16); missing 0; added 0 (expected 0) OK
lookups History: before 10, after 10 (API history 7, Web history 3); missing 0; added 0 (expected 0) OK
lookups rest of the document (bar the part headings and the date): unchanged
spaces Decisions: before 37, after 37 (API decisions 28, Web decisions 9); missing 0; added 0 (expected 0) OK
spaces History: before 4, after 4 (API history 3, Web history 1); missing 0; added 0 (expected 0) OK
spaces rest of the document (bar the part headings and the date): unchanged
ALL OK
```

The expected additions:
- `users` API history: "#35 — the password policy's rules for a checklist.";
- `space-links` API history: "#48 — the missing fact groups on the admin list's rows." (the owner's);
- `space-links` Web history: "#44 — an English-only name marked as English in the Arabic interface.";
- `space-links`: "#36 — the caller's spaces." in both parts.

**Also run:**
- `npm run format:check`: clean, before each commit.
- `npm run lint` and `npm run typecheck`: once, before commit 1, which holds the four code comments. Both passed.
- `git grep -n "findings\.md"`, excluding `.design-sync`, `docs/design` and `dist`, finds two lines only. Both are in `docs/plans/feature-documents.md` (lines 40 and 46), whose link text keeps the words "findings.md" while its targets now point at `findings/README.md`. This is by design: a record keeps its text.

**Not run locally:** the test lanes, `build` and `check:build`. Nothing changes behaviour (four comments only), and CI ran them all on the head.

## 4. Breaks made, seen failing first

- **Link checker,** on fixtures. Three planted breaks were all reported: a missing file (`c.md`), a missing anchor (`b.md#no-such-heading`) and a missing cited path in code (`docs/missing.md`). On the same fixtures it resolved a repeated heading (`#notes-1`) and ignored a link inside fenced code.
- **Proof 1:** "today" was changed to "now" in finding 27. The proof reported 43 equal, and printed the line.
- **Index check:** finding 38's file was set back to `Open` while the index still listed it as Resolved. It reported "status Open, listed under Resolved".
- **Proof 3:** "last" was changed to "first" in one `lookups` decision. It reported FAIL, with the missing line and the added one.

Each break was restored afterwards, and the restore was checked.

## 5. Problems met, and how each was solved

- **The plan's example name for finding 26 was wrong.** The plan wrote it as `26-npm-run-format----check-…` (four dashes). The first fixture run reported that anchor as missing, because GitHub turns each space into its own `-`. ``format -- --check`` therefore gives six dashes: the file is `26-npm-run-format------check-rewrites-files.md`. The checker was right and the example was wrong. No document links finding 26, so nothing else was affected.
- **The PR number in finding 38's resolution** followed the reply's method:
  - commit 1 was first pushed with `#N`;
  - `gh pr create` returned #52;
  - the number was folded into commit 1 (fixup and autosquash), then pushed with `--force-with-lease` before waiting for CI.

  CI ran on the folded head `3d6e4c6`.
- **The index first had a double blank line** under its header. I fixed it by hand before commit 1, and Prettier is clean.

## 6. Unexpected behaviour

- **A stale comment, not fixed.** The comment in `apps/api/src/db/seed/lookups.ts` still says "the web will map each key to the design system's icon of that glyph in build step 2". That is stale: finding 10 was resolved in S2a-3 (#49), and the web draws each icon by its glyph's name. M2 only repointed the comment's link, since its words are out of scope. Proposal: fix the wording in the next item that touches the seed, or record it as finding 48 if you prefer.
- **A CI run for the replaced head.** The pre-fold head `2073523` also got a CI run (37776488169), which is superseded. The run on `3d6e4c6` is the one that counts.

## 7. Early conflict check

`gh pr list --state open` lists only #52, so there is no other head to run `git merge-tree` against. `main` is still `d4d5b57`, the branch's base.

## 8. Departures from the prompt

1. **Proof 1 compares links by resolved target**, not byte for byte apart from the heading. Every link inside a finding gained one `../` for the deeper folder. Approved as Stronger decision 1.
2. **Wider checker:** it covers the root README and every `docs/` path cited in code, not only the four comments. Approved (decision 3).
3. **Index check** in proof 2. Approved (decision 4).
4. **Documentation §5** gained the D3/D4 sentence, as well as losing "Not yet applied". Approved (decision 2).
5. **Four history lines added**, all approved: three from D4, and #48 from the owner.
6. **Two `findings.md` text hits remain** in a record's link text, as §3 explains. The plan's acceptance criterion said the grep "returns nothing"; the plan's own records rule keeps those two.

## Review fixes (round 1)

**1. The PR and its head.**
- **Head:** `227ff17cc4dc264eadd8a970cccc9f367e8e22c4`, pushed once with `--force-with-lease`.
- **CI:** run 37778608525 on `227ff17` succeeded: lint, typecheck, format:check, check:classes, build, test:unit, test:component and test:api.
- **Merge state:** GitHub shows `CLEAN`.
- **Comment:** the fixes are reported in one "Review fixes" comment on #52.

**2. The commits:**
1. `9e4024d docs: give each finding its own file`;
2. `8618a87 docs(features): split decisions by layer`;
3. `227ff17 chore(skills): push review fixes in open-pr`.

The two fixes:
1. **Commit 2's subject** was 52 characters and is now `docs(features): split decisions by layer` (40). It was reworded in an autosquash rebase.
2. **The seed's comment** (`apps/api/src/db/seed/lookups.ts`) is folded into commit 1 as a fixup.
   - It now reads: "Icon keys come from the shared list: each is a glyph's name that the web's design system draws (`GlyphIcon`), and the web's typecheck refuses a key it cannot draw (docs/architecture/findings/10-….md)."
   - "Will" and "build step 2" are gone, and the finding 10 citation stays, since its resolution records this.

**3. What was run.**
- `git diff --stat 3d6e4c6 227ff17`: only `apps/api/src/db/seed/lookups.ts` changes, by 2 lines.
- Link checker: 1,571 links and 600 anchors in 101 Markdown files, plus 231 citations, with 0 broken.
- Proof 1: 44 of 45 equal; finding 38 differs only by its status and resolution.
- `format:check`, `lint` and `typecheck`: clean.
- Not run locally: the test lanes, `build` and `check:build`, since only a comment changed; CI ran them all.

**4. Breaks made:** none new. The checks were already proven on breaks in the first round.

**5. Problems met:** none.

**6. Unexpected behaviour:** none. The stale comment in §6 above is fixed by this round.

**7. Early conflict check:** #52 is the only open PR, and `main` is still `d4d5b57`.

**8. Departures from the prompt:** none in this round.
