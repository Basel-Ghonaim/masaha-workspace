# M1 — The new way of working, written into the repository

**Worker B** · worktree `C:\Users\basel\masaha-b` · branch `docs/work-method`, cut with
`git fetch --prune origin` then `git switch --no-track -c docs/work-method origin/main`. The worktree
is detached at `origin/main` (`5d692f3`) and clean.

**Size cap:** at most 2 subagents, no self-review subagent, no workflow. A documentation item: no code.

## 1. The task in brief

The owner has changed how Work Items are run. The analysis and the decisions now happen with the
owner before a prompt is written; prompts become short; the standing rules move into the repository's
skills; the two workers split **by layer**; conflicts get a fast path. This item writes that method
into the documents and the skills, so every later prompt can simply point to it. **It is the first
item run this way**, before the skills that describe it exist: follow §5 below by hand.

A second item (M2, after worker A's PR #50 merges) will apply the new layout to the existing documents
(finding 38, the findings one file each; the capability documents' per-layer sections). **Not this
item**: here only the rules.

## 2. Read first

In the order `docs/development/workflow.md` §2 › *Reading before work* gives: CLAUDE.md, the whole
workflow (§2, §3, §5, §8, §9, §10 above all), the map, `docs/architecture/documentation.md` (§1, §5,
§6), `docs/development/testing.md` §3, `docs/plans/v1-mvp.md` (*Sequence inside the build* and its
*Ordering notes*), and the three skills in `.claude/skills/`. The open findings' titles; finding 38 in
full (only to word M2's rule, not to do it).

## 3. The decisions the owner settled

These are settled, **but review them**: if one can be stronger within this item's scope, put it in
your plan's **"Stronger decisions"** section (what, why, its cost, your recommendation). Do the same
for any rule already in the documents that this method contradicts or makes weaker.

**The phases of a Work Item** (workflow §2 owns them; the skills follow):
1. **Before the prompt** (the owner, with an analyst): the task is explained, its open decisions
   settled, the related findings to fold chosen. The prompt carries the task in brief, what to read,
   the settled decisions, the folded findings, the boundaries with the other worker, and where to
   save the plan and the report.
2. **Plan:** in plan mode, a complete, decided plan. It contains a **"Stronger decisions"** section:
   any decision of the prompt **or of the documents, an ADR's included**, within the item's scope,
   that the worker can make stronger, with its reason, cost and recommendation. It also lists the
   folded findings, the files (the other layer's included), each test with the break it catches, a
   *Review Focus* list, the commits and the verification. **Saving it:** plan mode cannot write files,
   so the worker leaves plan mode with a short summary; the owner's approval of that exit means
   "save the plan", not "build it". The worker then writes the plan to the file the prompt names and
   **stops** until the reply comes.
3. **Implement** the approved plan; every new test seen failing first (testing §3).
4. **Verify locally, before any push:** every lane, once, on the head; `build` and `check:build`; a
   real run (the browser for the web, real requests for the API). **Exception, written as such:** a
   change with no code (documents, skills only) runs `format:check` alone. Anything not run is said,
   with why.
5. **Pull request:** push, open it, wait for CI to pass and GitHub to show `CLEAN`.
6. **Report:** saved to the file the prompt names, summarised in the conversation: the head, the
   commits, what was run and not run, the breaks made, the problems met and how they were solved,
   **anything that behaved unexpectedly** (even unsolved), and any departure from the prompt with
   its reason.
7. **Review:** the owner and the analyst read the report and the branch. A separate review
   conversation opens when the PR touches more than about 25 files, or authorization or security,
   or a transaction, or the schema; otherwise the analyst reviews it. Fixes stay in the worker's
   conversation, as today (workflow §3, *Commits*).

**Two new skills** (runbooks, like the three today: they link to the section that owns each rule and
own no fact):
- **`write-plan`** — how to write and save the plan of phase 2: its sections in order, the "Stronger
  decisions" section, the save-then-stop step, the path taken from the prompt.
- **`final-report`** — how to write and save the report of phase 6: its sections in order.
- `start-work-item` calls `write-plan`; `open-pr` gains phase 4's local verification before the push
  and calls `final-report` once CI passes. **No path outside the repository is written in a skill or
  a document** (documentation rules §8): the prompt names the folders.

**The standing rules leave the prompts.** Every rule today's prompts repeat must have one home in the
documents, which the skills link. Map each to its home in your plan, and give a home to any that has
none (in its owning document, minimally): honest test titles; no parameter, option or callback only
tests pass or nothing uses; tests stub the platform's seams, never `vi.mock` of a module; one
responsibility per file, files grouped by operation; no hardcoded text, both catalogues; no colours
or CSS outside the design system; lint and typecheck on each commit; commit subjects ≤ 50
characters; report only once CI is green on the pushed head; review fixes folded into their commits
with ONE "Review fixes" comment; rebase only on a real conflict; no tool attribution; never merge,
never create an Issue.

**The two workers, by layer** (workflow §9, rewritten):
- **Worker A builds the web; worker B builds the API** (and the schema, the migrations, the seed).
- **A narrow licence in the other layer,** declared in the plan and approved: for A, for example, a
  field in a shared schema or a small fix in the API the screen needs; for B, what breaks in the web
  when a shared type changes. **A never writes a migration; B never builds a page.**
- **`packages/shared` and the API contract are the API worker's** (they are the contract between the
  two); a change the web needs there is declared in A's plan.
- **Two items in flight never work in the same layer.** The build map may change shape to keep it so
  (`v1-mvp.md`: the API may run one step ahead of the screens — a line in its *Ordering notes*).
- **Dependencies:** either worker may add one, declared in its plan; never both at once. A conflict
  in `package-lock.json` is never merged by hand: after the rebase, `npm install` regenerates it.

**Conflicts:**
- **Early:** at each report the analyst checks the open branches against each other
  (`git merge-tree`); a conflict found then decides the merge order, and the second branch rebases
  in its last push, not after it.
- **The fast path,** in `open-pr`: a conflict only in documents is a rebase that keeps both sides,
  `format:check` alone, one push, no lanes (CI runs them); a target of ten minutes. A conflict in
  code adds lint and typecheck.
- **The capability documents' rule** (documentation rules §5, the rule only, applied in M2):
  *Decisions* and *History* each split into an **API** and a **Web** part, so the two workers append
  in different places.

**`CLAUDE.md`:** its session checklist names the two new skills. Nothing else there changes.

## 4. Findings

None folded. Finding 38 stays open: M2 resolves it. If your plan sees another open finding this
item should close, propose it.

## 5. How this item runs

1. `start-work-item`, plan mode. Write the plan with the sections of §3, phase 2.
2. Leave plan mode with a short summary; once approved, save the plan to
   `C:\Users\basel\.prompt\MASAHA_WORKER_B\PLAN\M1_PLAN.md` and **stop** for the reply.
3. After the reply: implement in 3–4 commits (each a complete unit, subjects ≤ 50 characters).
4. Locally: `npm run format:check` only (this item has no code — the exception it writes).
5. `open-pr`: push, `gh pr create --assignee @me`, labels `docs` and `area:docs`; wait for CI and
   `CLEAN`.
6. Save the report to `C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\M1_REPORT.md` with the sections
   of §3, phase 6, and summarise it here. Don't merge.

## 6. Boundaries

- **Worker A** has PR #50 open (the admin's spaces list): it edits `docs/architecture/findings.md`,
  `docs/features/{lookups,space-links,spaces}.md`, `docs/frontend/architecture.md` and
  `docs/project/overview.md`. **Touch none of them.** Your files: `docs/development/workflow.md`,
  `docs/architecture/documentation.md`, `docs/plans/v1-mvp.md`, `CLAUDE.md`, `.claude/skills/`, and
  any other document a standing rule needs as its home (declare it in the plan; if it is one of A's,
  stop and ask).
- Findings, if any: number from 48.
