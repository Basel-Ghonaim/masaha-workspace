# M1 — The work method, written into the repository · report

## 1. Pull request and head

- **PR #51**: https://github.com/Basel-Ghonaim/masaha/pull/51, titled `docs(workflow): define the work item phases`.
- **Labels:** `docs` and `area:docs`. Assigned to the owner. Not merged.
- **Branch:** `docs/work-method`, cut `--no-track` from `origin/main` (`5d692f3`).
- **Head:** `f8ff5c91c729b7677cef0ec62bfd5bed0eed9c23`.
- **CI:** every check passed on that head (`gh run view` gives the run's head SHA as `f8ff5c9`): build, check:classes, format:check, lint, typecheck, test:unit, test:component and test:api. GitHub shows `CLEAN` / `MERGEABLE`.

## 2. Commits

1. `717d974` docs(workflow): define the work item phases: §2 *Phases* (the seven phases), the §3 lifecycle line, and §3 *Commits* reworded (stronger decision 2).
2. `59dbe03` docs(workflow): split the two workers by layer:
   - §9 rewritten, with a new *Conflicts* subsection;
   - phase 6's merge-tree item;
   - documentation §5's API/Web rule;
   - v1-mvp's ordering note.
3. `dec584e` docs: give the standing rules a home: testing §3 rule 6 (honest titles), and engineering principles §1 (nothing no caller passes).
4. `f8ff5c9` chore(skills): add write-plan and final-report:
   - the two new skills;
   - `start-work-item` and `open-pr`;
   - workflow §10 (`writing-plans` now inside `write-plan`);
   - CLAUDE.md's checklist.

10 files, +137 −36. Every one is in the plan's file list, and none is a file of PR #50.

## 3. Run and not run

- `npm run format:check` on the head: passes. Prettier excludes Markdown, so it read none of the changed files.
- **The link check by hand** (documentation §8, stronger decision 1): every relative link in the 10 changed files, file and heading. Result: 225 links, 0 broken. I used a throwaway script in the session's scratchpad (not committed). It resolves each path and compares each anchor with the target's headings, slugged.
  - The check itself was checked: a probe file with a wrong anchor and a missing file reported both, then the probe was deleted.
- `git diff --stat origin/main`: the 10 planned files only. No path outside the repository in the diff (searched for `C:\`, `Users\`, `Downloads`, `.prompt`).
- Commit subjects are 43, 46, 36 and 46 characters. No attribution trailer.
- **Not run locally:** lint, typecheck, the lanes, `build` and `check:build`. There is no code; this is the phase-4 exception the item writes. CI ran all of them, and all passed.

## 4. Breaks made, tests seen failing first

None: no code and no tests. The only "break" was the link-check probe above.

## 5. Problems met

- **The plan was not saved first.** My first exit from plan mode was rejected. The plan then reached you pasted, with `PLAN\` still empty.
  - Solved: after your reply, the plan was saved to `PLAN\M1_PLAN.md` (with an approval line) before the branch was cut.
  - Fed back into the skill: `write-plan` now says plainly that the plan is saved before any branch or edit, and that the turn ends there.
- **A commit would have named a skill not yet added.** The §10 edit names `write-plan`, and the phase-6 item points to §9 *Conflicts*. In their planned commits, each would have pointed to something a later commit adds.
  - Solved: the §10 line moved into commit 4 and the merge-tree item into commit 2, so each commit is consistent on its own.

## 6. Anything that behaved unexpectedly

- **Plan mode shows the whole plan file, not a summary.** This harness has plan mode write to its own plan file, and leaving plan mode shows that whole file. So "leave with a short summary" amounts to a summary at the top of the full plan. The plan is then copied to the prompt's path. `write-plan` names no harness path, so it holds either way. Unsolved; a note only.
- **The link check relies on an approximate slug.** It uses a GitHub-like slug (lower case, punctuation dropped, spaces to dashes). All 225 links resolved under it. A heading with unusual characters could slug differently on GitHub. Finding 37 (a CI link checker) remains the real fix.
- **CodeRabbit** reports "Review skipped: manual review required for this OSS repository". It shows as a passing check.

## 7. Early conflict check

- **PR #50** (`feat/admin-spaces-list`, `cfd1a5a`): `git merge-tree --write-tree` against `f8ff5c9` exits 0, so it is **clean**. The two PRs share no file.

## 8. Departures from the prompt or the plan

- **CLAUDE.md:** `write-plan` is named in step 2, not step 1 as planned. Step 2 is where the reading happens, and the plan comes after it. Step 4 names `final-report` as planned, and nothing else changed.
- **Lifecycle line (§3):** it keeps "Self-review", as "Self-review and verify locally"; the plan's wording had dropped it. `open-pr` still self-reviews.
- **Phase 2's contents** also list "the decisions it needs from the owner (§6)". This comes from the old `start-work-item` list, which the plan moved into `write-plan`.
- **Phase 1** adds one sentence: "The prompt names those folders; no document or skill does." It applies documentation §8.
- **§9 *Conflicts*** has a third item, *Apart by design*. It covers the capability documents' API/Web parts, and each prompt giving its worker its own range of finding numbers. The second is today's practice, written down.
- **`open-pr`'s description** now also triggers "when it conflicts with main", for the fast path.
- **`final-report`** adds a step: after a round of review fixes, a section for that round.
- **PR title:** the first commit's subject (workflow §3: "same as the main commit").

No other departure. No finding recorded. The `apps/web/.env` note stays with the owner, as agreed.
