# D-2 — Execute the feature-documents plan

**Worker C** · worktree `C:\Users\basel\masaha-c` (detached at `origin/main`, clean) · branch
`docs/feature-documents`, cut with `git fetch --prune origin` then
`git switch --no-track -c docs/feature-documents origin/main`.

**The plan is merged and is your contract:** `docs/plans/feature-documents.md` (PR #46). This item
executes it: the documentation strategy, the ADR, the capability documents under `docs/features/`,
every move out of the platform documents, the header clean-up and the verification pass, in **one
branch and one pull request**. Workers A and B are paused while it runs: no other worker edits the
documents.

**Size:** no token cap for this item (it is a large, project-wide change). **Subagents: at most 3 in
total, never a fourth.** No workflow. No self-review subagent: an independent review gate follows
the PR.

## 1. How to work

- **Start with the `start-work-item` skill. Then plan, in plan mode, before you write anything.**
- **Save your approved plan** as a file in `C:\Users\basel\.prompt\MASAHA_WORKER_C\PLAN_MODE\`
  (create the folder when you save it), for example `D2_PLAN.md`. That folder is outside the
  repository: nothing from it is committed, and no committed document cites its path.
- **Superpowers:** follow `docs/development/workflow.md` §10 (used: verification before completion,
  systematic debugging, receiving code review as adapted; not used: the rest). The project's skills,
  CLAUDE.md and this prompt win.
- **Read first:** CLAUDE.md; `docs/README.md`; `docs/development/workflow.md` (§3, §5, §7, §8, §10);
  **the plan, in full**; ADR style (short, decision-level, no file names).
- **Rules:** documents only, no code; stage by path; commit subjects ≤ 50 characters; no tool or AI
  attribution; no local paths in any committed document; rebase only on a real conflict.

## 2. What your plan (plan mode) must fix before execution

Your plan-mode plan turns the merged plan into the exact map you will walk. It names:

1. **The contracts** you build to: the strategy document's sections and the rules each states
   (decision 6 of the plan); the capability template (decision 4); the word limits (about 1,200 per
   capability document, about 1,500 for the strategy); "a section appears only when its code
   exists"; the classes; the ADR's scope.
2. **The constants** you never break: no fact in two homes, at any commit; no fact lost (every
   ledger row ends with exactly one home); a move and its link land in the same commit; nothing
   claimed that the code does not show; records (`plans/`, `findings.md`, the ADRs) are not rewritten,
   only their links repointed if a target moves; security rules stay whole in `backend/security.md`.
3. **The map:** the steps and commits of the plan's §6, in order, each with its ledger rows
   (by their ids), the decisions-index entries it writes, the contradictions it corrects, and its
   checks. Re-verify the ledger against `main` as it is now (PR #46 merged the plan only; nothing
   else has changed since) and say if any row moved.
4. **The open decisions:** any boundary case the merged plan does not settle, with options and a
   recommendation. **Stop and ask** before executing a step that depends on one.

## 3. The owner's answers to the plan's open questions (§10)

1. Routing that serves one capability (the password-change gate, `RequireSpaceRole`, the landing
   rule) **stays in frontend architecture §2**; capability documents link to it.
2. "The admin edits a space only while it is unverified" **moves to `backend/security.md` ›
   Authorization**; conventions keeps only the placement rule (`spaces` never imports `space-links`).
3. **The audit list stays in conventions §6** (the admin's allowlist reads it as one list).
4. **A platform rule keeps one short example;** full per-capability lists move to the capability
   documents.
5. **The overview's *Built* section: one line per capability,** each linking its document.
6. **The code governs.** What is built and not yet documented is documented as built: space delete
   and restore (PR #44) join the overview's v1 scope line and their capability document. (This is
   CLAUDE.md's rule — the code is the source of truth — not a new scope decision.)
7. **The contradicted claims:** each is corrected in the step that touches its section; a finding is
   recorded for each case where the code, not the document, may be what should change (at least the
   users service's `passwords` parameter that only its unit test passes).
8. **The map lists `docs/features/`** as the folder plus one line per document.

## 4. Checks

- **No `npm ci` and no local lanes:** the owner's connection is weak, and this item needs none.
  Prettier's ignore file excludes Markdown and ESLint lints only code, so `format:check` and `lint`
  can't see a document change; CI runs every lane on the pushed head. **Never run a check from the
  main folder** (`C:\Users\basel\masaha`): it would check `main`'s files, not this branch's. If a tool
  is truly needed, link the main folder's installed modules into this worktree instead of
  downloading them — `mklink /J C:\Users\basel\masaha-c\node_modules C:\Users\basel\masaha\node_modules`
  (same `main`, same lockfile; `node_modules` is git-ignored) — and say so in the report.
- **Per step:** the step's ledger rows each have one home; every link and anchor the step touched
  resolves; the touched documents' word counts against the plan's estimate.
- **The verification pass** (the plan's last step): all links and anchors across `docs/` resolve;
  no residual duplication (search for each moved fact's key phrases); every capability document
  within its limit; every header's declared class is true.
- `verification-before-completion`: every claim in the PR description names the check that proves
  it.

## 5. Pull request

- **Title:** `docs: add the feature documents` (or the main commit's subject).
- **Labels:** `docs`, `area:docs`. Assigned to the owner.
- **The description:** the steps done, per step the ledger rows closed and the decisions recorded;
  the word counts before and after for each platform document; the contradictions corrected and the
  findings recorded; anything that differed from the plan, and why.
- **Review:** the independent review gate for duplication, after you report.
- After CI is green on the pushed head, stop and report: the head, the commits, the counts, your
  tokens, the subagents used. Don't merge. Don't create an Issue.
