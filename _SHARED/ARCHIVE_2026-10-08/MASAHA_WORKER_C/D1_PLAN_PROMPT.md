# D-1 (plan) — The feature-documents plan

**Worker C** · worktree `C:\Users\basel\masaha-c` (detached at `origin/main`, clean) · branch
`docs/feature-documents-plan`, cut with `git fetch --prune origin` then
`git switch --no-track -c docs/feature-documents-plan origin/main`.

**This item writes a plan, not the change.** Its one deliverable is a formal execution plan,
`docs/plans/feature-documents.md`, in the shape of the project's other plans (`docs/plans/`). It
moves, rewrites or creates **no other document**; the only other edit is one line in
`docs/README.md`'s `plans/` list. A later item executes the plan, after the owner approves it.

**Size cap:** at most **3 subagents, read-only, for the inventories** (§4); no self-review subagent;
no workflow. Stay under **400,000 tokens** in total. The other two workers are paused while this
effort runs, so the documents won't change under you.

## 1. How to work

- **Start with the `start-work-item` skill.** Plan the plan in plan mode first (its outline, the
  inventories' method, the subagents' split), then write it.
- **Superpowers, selectively:** use `verification-before-completion` (every claim in the plan names
  its source: a file and section, a PR number, a commit) and `systematic-debugging` if anything
  fails. Do not use `brainstorming`, `writing-plans`' header or saved plan files,
  `executing-plans`, `subagent-driven-development`, `dispatching-parallel-agents` (beyond this
  prompt's cap), `requesting-code-review`, `using-git-worktrees` or
  `finishing-a-development-branch`. The project's skills, CLAUDE.md and this prompt win.
- **Read first:** CLAUDE.md; `docs/README.md`; `docs/development/workflow.md` (§3, §5, §7, §9);
  the plans in `docs/plans/` (their shape); ADR style (short, decision-level, no file names).
- **The source of the adopted rules** (to understand them, not to copy them):
  `D:\quick-tweets-app\docs\architecture\documentation-strategy.md` (§2–§6, §8, §10, §11.5–11.6) and
  one example, `D:\quick-tweets-app\docs\features\recovery.md`. Quick Tweets gives ideas, never text:
  the plan states the rules in Masaha's own words and for Masaha's shape.
- **Rules:** read-only everywhere except the plan file and that one README line; no code; commit
  subjects ≤ 50 characters; no tool or AI attribution; rebase only on a real conflict.

## 2. The effort the plan sequences (decided by the owner)

A documentation layer: **one document per capability** under `docs/features/`, and the removal of
every duplicated or misplaced fact, so that **no fact has two homes**. Its value: a worker changing a
capability reads one document first, then only the sections it links.

**The owner's decisions (fixed; the plan records them with their reasons):**
1. **The ownership boundary:** "Is this a shared mechanism, or a capability-specific application of
   one?" A mechanism stays in its platform document; an application belongs to its capability's
   document, which links to the mechanism and never restates it.
2. **The capabilities documented now:** `auth` (email sign-in, registration, Google, forgot and
   reset password, the recovery session's flow), `users` (the account, the forced password change,
   the account menu, sign-out), `space-links` (my spaces, the switcher, the admin's composed spaces
   list, the links loader), `lookups` (the admin's lookups screen, the public catalogue), `spaces`
   (the admin's create/list/edit/hide/delete/restore; no web section yet). **Not documented:**
   `sessions` (a platform mechanism: architecture §4, security.md), `platform-settings` and
   `space-settings` (mentioned where `spaces` uses them; their documents come with their screens),
   the page groups and the dashboard shell (composition: architecture §2).
3. **A document per capability, spanning the API module, `packages/shared` and the web feature,**
   named after the backend module (`lookups.md`, `space-links.md`). A web feature serving two
   audiences over one module gets a section in that module's document.
4. **The template:** header (status, class, authority, scope, last updated, owner); what it does;
   who uses it; responsibility boundary; how it composes the platform (links only); behaviour and
   flows; **decisions** (each with its reason, date and PR); code map (**folders and entry points
   only**, never a file list); open findings (links); history (PRs). **A section appears only when
   its code exists.** At most **about 1,200 words** per document.
5. **The stable-core rule for capabilities:** a capability's document is created in the PR in which
   the capability first has a stable core — its first merged, reviewed slice with settled decisions —
   and every later PR that changes its behaviour, decisions or code map updates it in the same PR,
   adding a section when a new layer arrives.
6. **The rules live in a new short document,** `docs/architecture/documentation.md` (the
   documentation strategy, about 1,500 words at most), which the map points to. Adopted from Quick
   Tweets, adapted: the boundary question; a **"single owner per kind of fact"** table (fact → owner →
   linked by); a **"what each category owns and must not contain"** table; document **classes**
   (Contract, Description, Record, Plan, Commitment) defined briefly — a declared class must be true;
   "a section appears only when its code exists"; describe rules and intent, not inventories (the code
   map is folders only); the ADR rule gains **"no ADR when a document naturally owns the decision"**
   (so capability decisions live in capability documents, never in ADRs); link integrity (a move
   updates every link in the same PR); one entry point (the map guides, never enumerates files).
   **Not adopted:** live status in an issue tracker, a version number per document, "constitutional
   documents", an agent-onboarding document.
7. **A short ADR** records the governance decision (a capability layer that owns capability-specific
   applications), decision-level, no file names.
8. **Security stays whole:** every rule whose reason is security stays in `backend/security.md`; a
   capability document owns its flow, experience and non-security decisions, and links security.md.
9. **Records are exempt from moves:** `plans/`, `findings.md` and the ADRs are records; capability
   documents link them; they are not rewritten (only their links repointed if a target moves).
10. **The long "Built:" status lines** in the headers of contract documents (for example
    `frontend/architecture.md`) are cut to the platform: what a capability built is its document's.
11. **Links are checked by hand** in this effort; a finding records the need for a link checker.
12. **Findings as one file each** (as Quick Tweets does) is deferred: a finding records it
    (`findings.md` is the largest document).
13. **Triggers:** workflow §7 gains the capability-document row (decision 5); the Definition of Done
    gains one documentation check (a single home, no duplication, links not copies, nothing claimed
    that isn't built); `start-work-item` reads the capability's document first; CLAUDE.md's list of
    authoritative documents gains the strategy and `docs/features/`.

## 3. What the plan must contain

`docs/plans/feature-documents.md`, a **Plan** (it sequences work and holds its rationale; it is not a
description of the system). Shape it like `docs/plans/foundation.md` where that fits.

1. **Context, goal, non-goals** (short).
2. **The decisions** above, each with its reason, in Masaha's words (the strategy document will own
   the lasting rules; the plan records why and in what order).
3. **The capability map:** per capability, its code entry points (folders) at the current `main`,
   and its PRs.
4. **The duplication ledger — the heart of the plan.** Every fact that today has more than one home,
   or is a capability-specific application living in a platform document. One row each: the fact (a
   short paraphrase, never a long quote), **where it lives now** (document › section), mechanism or
   application, **its owner after the change**, and **its fate** — keep, move (to which document and
   section), merge, or delete as a duplicate — plus the link left behind. Cover at least
   `frontend/architecture.md` (every section), `backend/security.md`, `backend/conventions.md`,
   `frontend/localisation.md`, `architecture/shared-package.md`, `architecture/system-overview.md`,
   `project/overview.md`, `api/api-contract.md` and `architecture/data-model.md` (both stay owners of
   their facts: check nothing else restates them), and the headers' status lines. **Nothing is lost:**
   every row ends with exactly one home.
5. **The decisions index:** per capability, the decisions to record in its document, each with its
   source (the PR description via `gh pr view <n> --json body`, the review reports and the prompts
   in `C:\Users\basel\.prompt\` and `C:\Users\basel\Downloads\`), and **its status at the current
   `main`: still true (cite the code), changed (cite what replaced it), or obsolete.** A decision not
   true today is never recorded as current.
6. **The execution steps:** the order and the commits of the execution item — governance first (the
   strategy document, the ADR, the triggers), then one step per capability (its document **and** the
   moves out of the platform documents, in the same commit, so no commit leaves a fact in two places
   or in none), then the header clean-up, then a final verification pass (links and residual
   duplication). Name the checks for each step.
7. **The review gate** for the execution item: its axes (duplication across all documents, every
   claim true against the code, nothing lost in a move, links resolve, the word limits, classes
   true) and its budget.
8. **Risks and mitigations.**
9. **Exit criteria:** what must be true for the effort to be done.
10. **Open questions for the owner,** each with options and a recommendation, where the inventories
    found a boundary case the decisions above don't settle.

## 4. The inventories (up to 3 read-only subagents)

A suggested split; your plan decides: (1) the frontend documents and the web code; (2) the backend
and shared documents and the API code; (3) the decisions harvest from the merged PRs (#27–#45), the
review reports and the prompts. Each returns its rows with sources; you merge, de-duplicate and check
them against the code yourself before they enter the plan.

## 5. Pull request

- **Title:** `docs(plans): plan the feature documents`.
- **Labels:** `docs`, `area:docs`. Assigned to the owner.
- **The description:** what the plan covers, the ledger's size (rows per document), the open
  questions, and that no other document changed.
- **Review:** the owner and the analyst review the plan; no code lanes are needed (documents only:
  run `format:check` and lint if `node_modules` is installed; otherwise say so — CI runs every lane).
- Report once CI is green: the head, the plan's size, the ledger's row counts, the open questions,
  your tokens. Don't merge. Don't create an Issue.
