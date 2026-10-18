# M2 — The findings one file each, and the capability documents by layer

**Worker B** · worktree `C:\Users\basel\masaha-b` · branch `docs/findings-per-file`.
**Plan now; cut the branch only once PR #50 (worker A, the admin's spaces list) has merged** — the
owner will tell you. #50 adds findings 44 and 45 and edits three capability documents, so this item
starts from the `main` that holds them.

**Size cap:** at most 2 subagents, no self-review subagent, no workflow.
**Plan:** save it to `C:\Users\basel\.prompt\MASAHA_WORKER_B\PLAN\M2_PLAN.md` (`write-plan`).
**Report:** save it to `C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\M2_REPORT.md` (`final-report`).
Follow the skills from start to end: `start-work-item`, `write-plan`, `open-pr`, `final-report`.

## 1. The task in brief

M1 wrote the method; M2 applies it to the documents that exist. Three parts:
1. **Finding 38:** `docs/architecture/findings.md` (515 lines, 45 findings) becomes one file per
   finding in `docs/architecture/findings/`, with an index; **every inbound link repointed in the
   same PR**, as the finding's *Resolves when* requires. Finding 38 is resolved.
2. **The capability documents by layer:** in `auth`, `users`, `space-links`, `lookups` and `spaces`,
   *Decisions* and *History* each split into an API part and a Web part, the rule documentation §5
   now states ("not yet applied" is removed from it).
3. **One line of `open-pr`:** step 8 says to "repeat steps 4, 6 and 7", but step 6 opens the PR; a
   fixes round **pushes** (`--force-with-lease`) instead.

This is **moving, not rewriting**: no finding's words, number or status change (except 38's), and no
decision is reworded — each moves as it stands.

## 2. Read first

The order workflow §2 gives. For this item: documentation rules (all, §1's records rule and §8 above
all), workflow §2 (*Reading before work*), §4 and §9 *Conflicts*, the map, `findings.md` whole (its
header holds how a finding is written), the five capability documents, and finding 37.

## 3. The settled decisions (review them in "Stronger decisions")

- **D1 — the index** is `docs/architecture/findings/README.md`: the rules of a finding (from
  `findings.md`'s header), then the findings in three groups — **Open, Accepted, Resolved** — each
  line its number, its title as a link, and nothing more. The *Resolves when* line stays in the
  finding's own file only. The status is in both the file and the index's group: write that **both
  change in the same commit**. Workflow §2 (*Reading before work*) and §4 change to: read the open
  findings' titles in the index, and open the file of each that may touch the item.
- **D2 — file names** are each finding's current anchor, exactly: `findings.md#27-two-dashboard-…`
  becomes `findings/27-two-dashboard-….md`. No padding, no shortening: every old link maps to its new
  one mechanically. Each file keeps its heading `# 27. …` and its body unchanged.
- **D3 — the parts' headings are unique:** `### API decisions` and `### Web decisions` under
  *Decisions*; `### API history` and `### Web history` under *History*. A part appears only when its
  layer's code exists. The paragraphs "Owned by … and linked" stay after both parts.
- **D4 — a decision on both layers, or on `packages/shared`, goes to the API part** (the contract is
  the API worker's, workflow §9). A PR that touched both layers is listed in both histories, each line
  saying what that layer got. **List every decision you were unsure of in the plan**, with your
  choice; we settle them in the reply.
- **D5 — the four code comments** that cite `findings.md` (`apps/api/src/db/seed/lookups.ts`,
  `apps/api/test/drive-letter-hook.ts`, `apps/web/src/shared/errors/toAppError.ts`,
  `apps/web/test/driveLetterHook.ts`) are repointed, comments only; the two web ones are a licence in
  A's layer, declared in the plan. Because they are code files, phase 4 runs **lint and typecheck
  once** besides `format:check` and the link check.
- **D6 — finding 37 is not folded.** Instead, verify the links with a **local checker you write
  outside the repository** (never committed), stronger than M1's: every relative link in `docs/`,
  `.claude/`, `CLAUDE.md` and the code comments resolves to a file, and every `#anchor` to a heading
  of that file by GitHub's slug rules (lowercase; punctuation dropped except `-`; spaces to `-`; a
  repeated heading takes `-1`, `-2`). Test it first on a broken link and a broken anchor, and see it
  catch both. Leave `.design-sync/` and `docs/design/prototype/` out (an archive and a cache).
- **D7 — the review is the analyst's, with mechanical proof** (the owner's stated exception to the
  25-file rule, because this PR moves text and decides no behaviour). Your report carries three
  proofs, each as the command you ran and its output:
  1. the 45 files' bodies, in number order, equal `findings.md`'s body at `main` (bar the headings'
     level and the index), finding 38's status and resolution line excepted;
  2. the link checker's result over the whole set: zero broken, with the count checked;
  3. per capability document, the set of decision bullets and history lines before and after is the
     same (sorted, compared), so nothing was lost, added or reworded.

## 4. Findings

Finding 38 is resolved by this item: its status, a resolution line with the date and the PR, and its
place in the index's *Resolved* group. No other finding is folded. A new one, if any, numbers from 48.

## 5. Risks — read before you start

- **Broken links are the item's failure.** About 50 inbound links in 19 documents, the links
  *between* findings (45 points to 27, for example), the map, documentation §2 and §8, workflow §2,
  §4 and the line in §4 that says "recorded in findings", the capability documents' *Open findings*
  sections, and the records (ADRs, plans: documentation §1 allows repointing their links). **The move
  and every repointed link go in one commit**, so no commit leaves a link broken. Run the checker
  before every commit, not only at the end.
- **Anchors inside the capability documents change** when the parts are added: any link to
  `features/<cap>.md#decisions` still resolves, but check every link into those documents.
- **Records are not rewritten.** A finding's text, an ADR's, a plan's: only their links change.
- **Do not start implementing before #50 has merged.** The branch is cut from that `main`; if `main`
  moves again before you push (worker A's next item, or anything else), check with `git merge-tree`
  and take the fast path (workflow §9 *Conflicts*).
- **Worker A** plans its next item meanwhile (read-only) and may read the old paths; nothing to do
  about it but finish quickly. **Do not touch** `apps/web` beyond the two comments.
- **A decision that does not split cleanly** is the place a judgement can slip: list them (D4).

## 6. Out of scope

Any change to a finding's or a decision's words; a CI link checker (finding 37); `.design-sync/` and
the design archive; any code beyond the four comments; the folders of the prompts (they live outside
the repository and no document names them).

## 7. Pull request

- **Title:** `docs: one file per finding, documents by layer` (or the main commit's subject, ≤ 50).
- **Labels:** `docs`, `area:docs`. Assigned to the owner.
- **Commits:** three, as in your plan: the findings moved with every link; the capability documents
  by layer (with documentation §5's "not yet applied" removed); `open-pr`'s step 8.
- After CI is green and GitHub shows `CLEAN`: `final-report`, with the three proofs of D7 and the
  early conflict check. Don't merge.
