# M2 plan — the findings one file each, and the capability documents by layer

Worker B · worktree `C:\Users\basel\masaha-b` · branch `docs/findings-per-file`, cut with
`git switch --no-track -c docs/findings-per-file origin/main`, at `origin/main` d4d5b57, PR #50's
merge. It was planned against PR #50's head (cfd1a5a). The plan was re-read against the merge and
amended by the owner's reply (§12).

## 1. Summary

M2 applies the method M1 wrote to the documents that exist. It makes three changes:
1. `docs/architecture/findings.md` (45 findings once #50 merges) becomes 45 files in
   `docs/architecture/findings/`, with an index, `README.md`. Every inbound link is repointed in the
   same commit, and finding 38 is resolved.
2. In the five capability documents, *Decisions* and *History* each split into an API part and a
   Web part. Documentation §5 drops "Not yet applied".
3. `open-pr` step 8: a fixes round pushes with `--force-with-lease`. It does not open the PR again.

All of it is moved, not rewritten. Apart from 38, no finding changes its words, number or status, and
no decision is reworded.

## 2. Contract

**Scope**
- 45 finding files, each named `<its current anchor>.md` (D2), with heading `# N. <title>` and the
  body unchanged. Finding 38 gets `Resolved` and a resolution line.
- `findings/README.md`: the rules of a finding, then the groups Open, Accepted and Resolved.
- `findings.md` is deleted.
- Every inbound link and citation is repointed: the docs, the records (ADR 0017 and the plans, links
  only), the capability documents' *Open findings*, the links between findings, and the four code
  comments.
- The text that describes the findings as one file now describes the folder:
  - workflow §2 *Reading before work* item 1, and §4 (the "recorded in findings" link and the
    *Related findings* bullet);
  - the map's line;
  - documentation §1 and §2 (link and name), and §8 (link only).
- `auth`, `users`, `space-links`, `lookups` and `spaces`:
  - `### API decisions` / `### Web decisions` under *Decisions*;
  - `### API history` / `### Web history` under *History*;
  - the "Owned by … and linked" paragraphs after both parts;
  - *Last Updated* set to the commit's date.
- Documentation §5: "Not yet applied: …" is removed.
- `.claude/skills/open-pr/SKILL.md` step 8.

**Acceptance criteria**
- [ ] Proof 1: the 45 files, in number order, equal `findings.md`'s body at `main` once their links
  are compared by the target they resolve to. The only exception is finding 38's status line and its
  new resolution line.
- [ ] Proof 2: the link checker reports zero broken links and zero broken anchors over the whole set,
  with the count it checked. It is run before each commit. The index lists every file once, under
  the group its status names.
- [ ] Proof 3: in each capability document, the sorted decision bullets and history lines are the
  same before and after, apart from the additions listed in §5 below. Everything else in the
  document is unchanged apart from the four new headings and the date.
- [ ] No `findings.md` is cited anywhere in scope (`git grep` returns nothing).
- [ ] `format:check`, `lint` and `typecheck` are clean. CI is green and GitHub shows `CLEAN`.

**Out of scope:** any change to the words of a finding or a decision; a CI link checker (finding 37);
`.design-sync/` and `docs/design/`; any code beyond the four comments; the prompt folders.

## 3. Reading done

- CLAUDE.md, workflow (whole: §2 *Phases* and *Reading before work*, §3, §4, §9 *Conflicts*, §10).
- The map, and documentation rules (whole; §1's records rule, §5 and §8).
- `findings.md`, whole, and #50's two new findings (44 and 45). Finding 37 is in it.
- The five capability documents, as they will stand after #50 (read from #50's head), and #50's
  documentation diff.
- The `start-work-item`, `write-plan` and `open-pr` skills.
- Every citation of `findings.md` (54 in 23 files, plus #50's) and of `<cap>.md#decisions`.
- The layers each listed PR touched, per capability, from the merge commits (used for D4).

## 4. Settled decisions, as they will be built

- **D1 — the index.** `findings/README.md` keeps findings.md's header (status, owner, authority)
  and its rule line ("Each entry: number, title, status, date, evidence, and what would resolve it.
  Numbers are never reused."). It adds the rules a separate file now needs:
  - a finding is a file named after its heading's anchor, headed `# N. <title>`;
  - the index lists it under its status's group;
  - a status change edits both the file and the index **in the same commit**;
  - *Resolves when* lives in the file only.

  The groups are **Open**, **Accepted** and **Resolved**, in ascending number. Each line is only the
  number and the title as one link: `- [27. Two dashboard chunks import each other](27-two-dashboard-chunks-import-each-other.md)`.
  Workflow §2 item 1 and §4 then read: "the open findings' titles in the
  [index](../architecture/findings/README.md), and the file of each that may touch the item". The
  map's line says the same.
- **D2 — file names.** Each file is named exactly after the finding's current anchor, under GitHub's
  slug rules, for example `26-npm-run-format----check-rewrites-files.md`. Links map mechanically:
  - `…/findings.md#N-slug` becomes `…/findings/N-slug.md`;
  - `#N-slug` between findings becomes `N-slug.md`;
  - a bare `findings.md` becomes `findings/README.md`.

  Every link inside a finding gains one `../`, since the file sits one folder deeper (`../plans/` →
  `../../plans/`, `data-model.md` → `../data-model.md`, `../../apps/` → `../../../apps/`).
- **D3 — headings.** The parts are `### API decisions`, `### Web decisions`, `### API history` and
  `### Web history`. A part appears only when its layer's code exists, and all five capabilities
  have both layers. The bullets keep their relative order inside each part.
- **D4 — placement.** A decision goes to the layer whose code it rules. One that rules both layers,
  or rules `packages/shared`, goes to the API part. A history line goes to the layer in which that
  PR changed this capability: the module or the shared folder count as API, the feature folder as
  Web. A PR that changed both is listed in both parts. The allocation is in the appendix, and every
  doubtful case is listed in §5.
- **D5 — the four comments**, rewrapped only where the long path needs it:
  - `apps/api/src/db/seed/lookups.ts` and `apps/api/test/drive-letter-hook.ts` (B's layer);
  - **licence in A's layer:** `apps/web/src/shared/errors/toAppError.ts` and
    `apps/web/test/driveLetterHook.ts`, comments only.

  Each cites `docs/architecture/findings/<file>.md` in full. The repository has no `max-len` rule,
  so one long path line is allowed. Phase 4 runs `lint` and `typecheck` once.
- **D6 — the link checker.** It is a Node script in the session scratchpad and is never committed.
  - **Scope:** every `*.md` in the repository (root `README.md` and `CLAUDE.md`, `docs/`,
    `.claude/`), minus `node_modules`, `dist`, `.design-sync/` and `docs/design/prototype/`.
  - **Code citations:** it also checks every `docs/….md` path cited in a comment under `apps/` and
    `packages/`, not only the four.
  - **What it checks:** each inline or reference link, outside fenced code and skipping
    `http(s):`/`mailto:`, resolves to a file or a folder. Each `#anchor` into a `.md` file matches a
    heading of that file under GitHub's slug rules:
    - inline markup is dropped to its text;
    - the text is lowercased;
    - characters other than letters, digits, `-`, `_` and spaces are dropped;
    - spaces become `-`;
    - a repeated heading takes `-1`, `-2`.
  - **Tested first:** on fixtures with one broken link and one broken anchor, it must report both.
    Then it runs once on `main`, and any broken link it finds there is reported as already existing.
  - **When it runs:** before each commit, and at the end.
- **D7 — the three proofs.** Each goes in the report as the command run and its output. The scripts
  are scratchpad Node scripts.
  1. Split `findings.md` at `main` by `## N.`, and read the 45 files. In both, rewrite every link to
     the repository path and anchor it resolves to, mapping `findings.md#N-slug` to the file per D2.
     Normalise the heading level, then compare the findings one by one. The only expected
     difference is finding 38's two lines, which the proof prints.
  2. The checker's output: links and anchors checked, zero broken. The index check: every file is
     listed exactly once, under its status's group.
  3. For each capability document: the decision bullets and history lines at `main`, then after
     the change. They are sorted and diffed, and the only differences are the listed additions.
     Each bullet's part is checked against the appendix. The document is diffed with those lines
     removed, so only the headings and the date differ.

## 5. Stronger decisions

1. **Compare links by target in proof 1** (prompt D7.1 says "bar the headings' level and the index").
   - *What:* every relative link in a finding must change, because the file moves one folder deeper.
     A byte-equal comparison is therefore impossible. Comparing by resolved target proves that each
     link still points where it did.
   - *Cost:* none.
   - *Recommendation:* adopt. This is a stated departure from the wording of D7.1.
2. **Write the D3/D4 rule into documentation §5.** Without it, the next worker has to rediscover where
   a both-layer decision or PR goes.
   - *What:* add one sentence: the parts are headed *API decisions*, *Web decisions*, *API history*
     and *Web history*. A decision that rules both layers or `packages/shared` goes to the API part
     ([workflow §9](../development/workflow.md#9-parallel-work)). A PR that changed both layers is
     listed in both histories.
   - *Cost:* one sentence in an authoritative document, which the owner approves.
   - *Recommendation:* adopt.
3. **Widen the checker** to the root README and every `docs/` path cited in code. It is stronger than
   the prompt's minimum and costs nothing. Adopt.
4. **The index check in proof 2** (status in the file equals the index group). D1 puts the status in
   two places, so this is the drift to catch. Adopt; it costs a few lines of script.
5. **Leave the links into `#decisions`** from `api-contract.md`, `security.md` and `data-model.md`,
   and from `spaces.md` into `space-links.md`, as they are. They still resolve. Pointing them at
   `#api-decisions` would be an edit beyond the move. Recommendation: leave them, and record nothing.
6. **The resolution line's PR number** *(changed by the reply)*. Do not predict the number. Push,
   run `gh pr create`, fold the real number into commit 1 (`**Resolution (<date>, #N):**`), and push
   again with `--force-with-lease`, all before waiting for CI.

**History lines added (the only additions to proof 3).** The owner added a fourth:
`space-links`, API history, "#48 — the missing fact groups on the admin list's rows." D4 adds:
- `users`, API history: **#35** changed `packages/shared/src/users` (`passwordRules`, the policy's
  checklist rules) as well as the account menu. The new line is
  "#35 — the password policy's rules for a checklist."
- `space-links`, Web history: **#44** changed `features/space-links` (`choiceOf`: an English-only name
  marked `lang="en"`) as well as the API. The new line is
  "#44 — an English-only name marked as English in the Arabic interface."
- `space-links`: **#36** changed both layers, and its line ("the caller's spaces") names what each
  got, so it appears verbatim in both parts.

**Doubtful placements (D4), with my choice:**
- `space-links` "The list's states are lowercase, like its filter" → **API**: these are the contract's
  values.
- `users` "`users` owns `User`; the session's user extends it" → **API**: shared, and both layers.
- `lookups` "The amenity icon keys live in `packages/shared`, and the design system does not import
  them" → **API**: shared.
- `lookups` "Duplicate English names are allowed" (#45, no code) → **API**: a data rule (finding 30).
- `lookups` "A new amenity starts with no icon chosen, and its icon is required" → **Web**: it is the
  form's.
- `auth` "The check names the account, masked" → **API**: the answer's shape.
- `space-links` "An English-only name shows marked `lang="en"`" (#44) → **Web**.
- `lookups` history **#49** → **Web only**. Its `packages/shared` change was a comment.
- `auth` and `users` history **#25** and **#34** → **API only**. Their web changes were in
  `shared/` and the error copy, not the capability's feature folder.
- `auth` history **#31** → **API**. Its code is in `users`, but the line is auth's.

**Rules the item would bend, stated:**
- Documentation §1 lets a record change only a link whose *target* moves. Here the *source* moves,
  so every link inside a finding changes its prefix. It still points to the same place, which proof
  1 shows.
- Records keep their link text: `[findings.md](…)` in `plans/feature-documents.md` keeps the words
  "findings.md". Only the target changes.

## 6. Related findings

- **38: folded,** per the prompt.
- **37: not folded** (D6). The local checker gives this PR its proof; CI stays unchanged.
- No other open finding (8, 14–17, 20–25, 27, 32, 33, 35, 39, 40, and 42–45) touches the item. A
  new finding would number from 48. I expect none.
- **An observation, not a finding.** `space-links`' History omits **#48**, which added the missing
  groups to the admin list's rows (`adminSpaces.mapper.ts`, `responses.ts`). Adding a line would be
  new content, so I leave it to the owner (decision 4 in §12).

## 7. Files

- **New:** `docs/architecture/findings/README.md` and 45 `docs/architecture/findings/N-slug.md`.
- **Deleted:** `docs/architecture/findings.md`.
- **Links repointed:**
  - `docs/README.md`, `docs/development/workflow.md`, `docs/architecture/documentation.md`;
  - `docs/architecture/data-model.md`, `docs/architecture/decisions/0017-recovery-session.md`;
  - `docs/api/api-contract.md`, `docs/backend/conventions.md`, `docs/backend/security.md`;
  - `docs/frontend/architecture.md` and `docs/frontend/design-system/foundation.md`, which are A's
    layer's documents (links only);
  - `docs/plans/foundation.md`, `docs/plans/v1-mvp.md`, `docs/plans/feature-documents.md` and
    `docs/plans/historical/design-system-layer.md`;
  - the five `docs/features/*.md`;
  - the four code comments (D5).
- **Restructured:** the five `docs/features/*.md`.
- **Also changed:** `docs/architecture/documentation.md` §5 and `.claude/skills/open-pr/SKILL.md`.
- **Shared with worker A:**
  - In the web part of `lookups`, `space-links` and `spaces`, A's next item may append. This item
    adds only the headings and moves bullets.
  - The two web comments (licence above).
  - `docs/frontend/*` (links only).

  `git merge-tree --write-tree` is checked against every open PR before the push and at the report.
- About 70 files. The prompt allows this (D7 exception): the PR moves text and decides no behaviour.

## 8. Lanes and tests

No behaviour changes, so no lane owns a test, and none is added. The breaks are the checker's (D6):
a broken link and a broken anchor in fixtures, both seen reported before the real run. Proof 1 is
also tested first: a one-word edit to one finding file must make it fail.

## 9. Review Focus (inputs no check exercises)

- Headings whose slugs need care:
  - backticks (26);
  - a colon (1);
  - `--` (26);
  - apostrophes, straight or curly (`owner’s`).

  Verify that the checker's slugs match GitHub's on the rendered branch for 2–3 of them.
- The index group of finding 15, which is `Open` while one of its items is accepted; it stays in Open.
- Link text that still says "findings.md" in the records (plans), by design.
- The comments' wrapped lines in the four code files.
- Links into `features/<cap>.md#decisions` that land on the parent heading, not on a part.

## 10. Commits

1. `docs: give each finding its own file`. It holds:
   - the 45 files and the index, with finding 38 resolved;
   - `findings.md` deleted;
   - every inbound link repointed (docs, records, capability documents, the four comments);
   - the workflow §2 and §4, map and documentation §1, §2 and §8 wording.

   The checker runs before it.
2. `docs(features): split decisions and history by layer`. It holds the five documents and
   documentation §5 (with "Not yet applied" removed, and, if approved, the sentence of §5 item 2).
3. `chore(skills): push review fixes in open-pr`. Step 8 becomes: fold the fixes, repeat step 4,
   push with `git push --force-with-lease`, then step 7, and update the PR description.

PR: `docs: one file per finding, documents by layer`. Labels `docs` and `area:docs`. Assigned to the
owner.

## 11. Verification (phase 4)

- **Runs:**
  - the checker (tested first) before each commit and on the head;
  - proofs 1–3 on the head;
  - `npm run format:check`;
  - `npm run lint` and `npm run typecheck` once (D5);
  - `git grep -n "findings\.md"` over the repository, minus `.design-sync`, `docs/design` and
    `dist`, which must return nothing.
- **Does not run:**
  - the test lanes, `build` and `check:build`: no behaviour changes, only four comments do, and CI
    runs them on the pushed head;
  - a browser: there is no UI.

## 12. Decisions from the owner (settled by M2_PLAN_REPLY.md)

1. The doubtful D4 placements and the three history additions in §5: **approved as listed.**
2. Stronger decisions 1–5: **approved.** Decision 2 adds the sentence to documentation §5.
3. Stronger decision 6: **changed**, as now written in §5.
4. `space-links`' missing #48: **add it in the API history**, as "#48 — the missing fact groups on
   the admin list's rows." It is the fourth addition in proof 3.
5. The branch is cut from `origin/main` at d4d5b57, once #50 has merged. #50's final documents were
   re-read: the appendix below is updated, and proof 1 runs against that commit.

**Re-read after #50 merged** (`cfd1a5a` → `d4d5b57`):
- finding 45 was corrected: a *Corrected* date, new evidence and a new *Resolves when*. It no longer
  links to finding 27;
- `space-links` gained two #50 Web decisions: the page shown stays busy, and the search field keeps
  what was typed;
- `spaces` gained one #50 Web decision: a 429's wait is one time, kept in the cache;
- the prose changes in `lookups`, `space-links` and `spaces` leave their *Decisions* and *History*
  as they were;
- no History line changed.

## Appendix — the allocation (D4), from `main` at d4d5b57

- **auth.**
  - API decisions: Google race (#31); the recovery a server session; a link checked in a browser
    with no recovery opens one; the check names the account, masked; the Gmail sender.
  - Web decisions: the remaining ten, from "the recovery pages read their step" to "mutations that
    carry a credential".
  - API history: #25, #31, #34, #38. Web history: #35, #40, #42, #45.
- **users.**
  - API decisions: `users` owns `User`.
  - Web decisions: the other seven.
  - API history: #25, #31, #34, #35 (new line). Web history: #35, #38, #39, #42, #45.
- **space-links.**
  - API decisions:
    - the caller's spaces open to any signed-in user;
    - hidden listed, deleted not;
    - names in both languages;
    - composed from three modules;
    - a link to a deleted space;
    - the admin's list composed here;
    - states lowercase;
    - the links loader without its refusal.
  - Web decisions:
    - `['me', 'spaces']`;
    - dashboard-only;
    - the switcher;
    - `lang="en"`;
    - #50's nine.
  - API history: #25, #34, #36, #44, #48 (new line, the owner's). Web history: #36, #39, #44 (new
    line), #50.
- **lookups.**
  - API decisions:
    - icon keys in shared;
    - the guard on `/admin`;
    - not paginated;
    - an order is the whole list;
    - hiding is `isActive`;
    - no new codes;
    - duplicate English names;
    - the key from the English name;
    - a new row last;
    - internet and power not filters;
    - the public catalogue.
  - Web decisions: the other sixteen, #43, #49 and #50 (sections, keys, no optimistic update and the
    rest).
  - API history: #16, #27, #34, #36, #41, #44, #45. Web history: #43, #49, #50.
- **spaces.**
  - API decisions: every #44 and #48 bullet, the last ("one save path", #48) included.
  - Web decisions: #50's nine.
  - API history: #36, #44, #48. Web history: #50.
