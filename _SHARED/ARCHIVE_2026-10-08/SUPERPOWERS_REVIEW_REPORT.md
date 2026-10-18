# Superpowers and Masaha's rules: who leads where

Analyst's report. Read-only. Superpowers v6.4.1. Written 2026-10-06. Nothing has been changed.

## 1. The verdict in five lines

1. Adopt the **discipline** skills: `test-driven-development` (with its `writing-good-tests.md`), `systematic-debugging` and `verification-before-completion`. Adopt `receiving-code-review` with adaptation. Use parts of `writing-plans` inside `start-work-item`'s plan mode.
2. Reject the **workflow** skills: `brainstorming`, `executing-plans`, `subagent-driven-development`, `dispatching-parallel-agents`, `requesting-code-review`, `using-git-worktrees` and `finishing-a-development-branch`. Each one replaces a gate the owner holds or breaks a cap.
3. Superpowers' rules rank as level 3 in CLAUDE.md's *Decision precedence*, below the prompt and the documents. Its own `using-superpowers` › *User Instructions* agrees, but only when the prompt names what is skipped.
4. The evidence: red-first alone would **not** have caught the two "test passes with broken code" findings (#40, #41). What would have caught them is `writing-good-tests.md`'s *Name the Break* and *Mutation Check*. These belong in `testing.md` as a project rule.
5. Move the plugin's enablement out of the tracked `.claude/settings.json` into each folder's `settings.local.json`. Today it dirties worker A's tree and fails `start-work-item` step 2.

## 2. Inventory and verdicts

The cost figures are word counts of each `SKILL.md`, plus its references where they get loaded. "Subagents" is what the skill dispatches by itself.

1. **using-superpowers** (492 words; loaded at every session start by `hooks/hooks.json`). Requires a skill call "if there is even a 1% chance". Before plan mode, it says to invoke `brainstorming`. *Project equivalent:* CLAUDE.md and `start-work-item`. **Adopt with adaptation:** it cannot be removed without disabling the plugin. Its *User Instructions* clause lets a prompt that names the skipped skills neutralise it.
2. **brainstorming** (2,613 words, plus the visual companion). Classifies a request as spike, bounded or architectural. Hard-gates implementation on approval. Writes and commits a spec under `docs/superpowers/specs/`. *Equivalent:* the analyst's analysis round, the prompt, plan-mode approval (workflow §2 "agree the contract before implementing"). **Reject.** It duplicates the owner's gate, and a committed spec outside the docs map breaks "one owner per fact" (CLAUDE.md, AI mission).
3. **writing-plans** (1,422 words). Bite-sized tasks with exact files, interfaces, complete code, failing-test steps and a commit per task. Includes a *Review Focus* section and a self-review. Saves to `docs/superpowers/plans/`. *Equivalent:* `start-work-item` step 4. **Adopt with adaptation** (§5.C).
4. **executing-plans** (3,267 words). Inline execution, a ledger under `.superpowers/sdd/`, one fresh reviewer subagent at the end. Also "Rulings, not stalls": decide conflicts and keep going. **Reject.** *Rulings, not stalls* contradicts workflow §8 ("An architectural choice → Stop and propose"; "Anything unclear → Record, never absorb"). The final reviewer is a self-review subagent, which HANDOFF §2 forbids.
5. **subagent-driven-development** (4,871 words plus 3 prompt templates). A fresh implementer and a reviewer for each task, up to 5 fix rounds, then a whole-branch review. Many subagents per item. **Reject.** It breaks the 4-subagent cap (HANDOFF §2) and has the same *rulings* conflict.
6. **dispatching-parallel-agents** (865 words). One agent per independent failure, run concurrently. **Reject as a workflow.** The prompt's cap governs subagents, and parallel implementers in one working tree collide (the skill says so itself: *When NOT to Use* › "Shared state").
7. **test-driven-development** (1,475 words, plus 1,310 in `writing-good-tests.md`). Red, then green, then refactor; "delete code written before the test". *Equivalent:* `testing.md` owns *where* a behaviour is proven and says it does not own "its style" (Authority line). Nothing owns *when* a test is written or how strong it must be. **Adopt with adaptation** (§4.2).
8. **systematic-debugging** (1,440 words). Four phases: root cause, then pattern, hypothesis, fix. After 3 failed fixes, "question the architecture" with the human. *Equivalent:* none. Workflow §8 has stop rules but no debugging method. **Adopt.** One adaptation: diagnostic logging comes out before commit.
9. **verification-before-completion** (580 words). "No completion claims without fresh verification evidence." *Equivalent:* CLAUDE.md "Claim only what is true", `open-pr` step 4, memory `ci-green-before-report`. **Adopt.** It is the same rule with a sharper procedure.
10. **requesting-code-review** (424 + 915 words). A reviewer subagent after each task and before merge. **Reject.** HANDOFF §2: "A worker's self-review with its own subagents is not the gate." The current prompts say "no self-review subagent".
11. **receiving-code-review** (913 words). Verify each item against the code, then push back with technical reasoning or fix. Clarify every unclear item before fixing any. *Equivalent:* memory `workers-may-challenge`, `fold-review-fixes`. **Adopt with adaptation:** ignore its *GitHub Thread Replies* section (the owner's rule is ONE "Review fixes" comment, HANDOFF §3). Fixes fold into their commits.
12. **using-git-worktrees** (1,069 words). Creates `.worktrees/`, commits a `.gitignore` change, runs `npm install` and a baseline test run. **Reject.** The folders are fixed (workflow §9).
13. **finishing-a-development-branch** (1,269 words). Offers to merge locally, open a PR, keep the branch, or discard it. **Reject.** Merging and deleting branches are the owner's (workflow §6). `open-pr` already opens the PR.
14. **writing-skills** (3,814 words plus references). TDD for skills, with subagent pressure tests. **Reject for workers.** It is optional for the analyst when editing `.claude/skills/`, but it is costly (*opinion*).
15. **diagnosing-superpowers** (1,065 words). Reads session transcripts and dispatches one analyst subagent per dimension in parallel. **Reject by default.** Only the owner should invoke it, with a cap stated.

This mostly confirms memory `superpowers-selective` (2026-10-06). It refines it in three places: `receiving-code-review` becomes adopted, the parts of `writing-plans` are named, and `writing-good-tests.md` is singled out as the most valuable file. No prompt in `MASAHA_WORKER_A|B` contains the word "superpowers" yet, so the line that memory records has not been written into any prompt.

## 3. Who leads at each stage

1. **Analysis and decisions.** *Leads:* the analyst's round and the owner (workflow §6). *When:* before every prompt. *Why:* `brainstorming`'s gate would ask the worker to re-approve what the owner already decided. It stays off.
2. **The Work Item prompt.** *Leads:* the analyst, with HANDOFF §2's list plus the standard block (§5.A).
3. **Planning.** *Leads:* `start-work-item` step 4, in plan mode. *Then:* `writing-plans`' file map, *Interfaces*, *No Placeholders* and *Review Focus*, inside that plan. *When:* substantial items only (workflow §1). *Why:* plan mode is the owner's approval point. `writing-plans` adds the test discipline the plans lacked.
4. **Implementation.** *Leads:* the documents (architecture §1/§3, conventions §2/§8, scope). *Then:* TDD sets the order of work inside a commit. *Why:* TDD has nothing to say about layers or scope.
5. **Testing.** In this order: `testing.md` decides **where** (the lane), TDD decides **when** (red first), and `writing-good-tests.md` decides **how strong** (name the break, mutate). *Why:* TDD's "every new function/method has a test" conflicts with "one behaviour, one lane" (testing §1). Duplicates appear in REVIEW35 #3, REVIEW41 #3/#8 and REVIEW43 #11.
6. **Debugging.** *Leads:* `systematic-debugging`. *When:* any failure, flake or unexpected behaviour. *Escalation:* at its "3+ fixes failed" point, workflow §8 applies: stop and propose.
7. **Self-checks and verification.** *Leads:* `verification-before-completion`, carried out through `open-pr` steps 1–4 and the CI-green rule. *Why:* identical intent. The skill adds "every claim needs a command run in this message".
8. **Review.** *Leads:* the independent review gate (HANDOFF §2). *Then:* `receiving-code-review`, adapted, for handling the fixes list.
9. **The PR and merging.** *Leads:* `open-pr`. The owner merges. `finishing-a-development-branch` stays off.
10. **Parallel work and folders.** *Leads:* workflow §9 only.
11. **Subagents.** *Leads:* the prompt's cap. None of the adopted skills dispatches a subagent: `writing-plans` › *Self-Review* says "not a subagent dispatch", and TDD, debugging, verification and receiving dispatch none.

## 4. Gaps, conflicts and precedence

### 4.1 What the project lacks and Superpowers provides

- **A rule on how strong a test must be.** Testing the evidence:
  - **PR #40, finding 1:** the test titled "…drops the token" checks only the mutation cache. If written red-first, it would fail before `reset()` and pass after it. **Red-first would not have caught it.** *Name the Break* would have: "what production change should make this fail? Keeping the AppError in state."
  - **PR #41, finding 1:** "If `writeAudit` ignored `tx`… the test would pass." Red-first would fail while the feature was missing, then pass. **It would not have caught this either.** The *Mutation Check* ("Missing state change or side effect") would have: mutate `tx` to `prisma` and the test stays green.
  - **The mutation check would also have caught** REVIEW38 #4 ("a gate that redirects every signed-in user would still pass") and REVIEW41 #5 (the off-by-one; the *Derive expectations independently* rule).
  - **Review Focus** would have caught the untested properties in REVIEW42 #3/#4 and REVIEW38 #7.
  - *Conclusion:* red-first is necessary but not enough. The rule that pays is **"each test names the break it catches; for security, transaction and ordering properties, make that break for real once and watch the test fail."**
- **A debugging method.** Findings 6 and 28 (flakes under load) and the stale-`dist` CI failure (memory `ci-green-before-report`) were handled case by case.
- **Claims tied to evidence.** Many findings are untrue claims: REVIEW35 #1 (documents say no test-only parameter exists), REVIEW41 #1 (the body says "proven"), REVIEW43 #6 (the body says "controls wrap"). The verification table's row "Requirements met → line-by-line checklist" addresses this.

### 4.2 What Superpowers lacks and the project needs

Superpowers has nothing on:
- architecture layers and boundaries;
- v1 scope and the *Not in v1* list;
- decisions gated by the owner (its executors decide alone);
- bilingual catalogues, RTL, and visual checks in four modes;
- documents with one owner per fact and triggered updates;
- the independence of the review gate;
- per-folder databases;
- token caps;
- the project's commit units.

### 4.3 What neither covers (*opinion*)

- **Async ordering and races in UI tests:** REVIEW43 #1, REVIEW38 #3/#5. `condition-based-waiting.md` fixes flakes, not ordering proofs.
- **How long a credential lives in client memory:** PR #40 #1, PR #42 #1, finding 34. This is a recurring class with no checklist.
- **Visual and RTL correctness:** manual only (testing §2) until E2E.

### 4.4 Conflicts, and the rule that settles each

The order is the prompt, then CLAUDE.md and the documents, then the project's skills, then the adopted Superpowers skills (CLAUDE.md › *Decision precedence*; workflow says the project's skills give way to the documents).

1. **`using-superpowers`' "1% → MUST invoke" and "brainstorm before plan mode" vs `start-work-item`.** The prompt wins. Its own *User Instructions* clause requires that the prompt says so explicitly.
2. **`brainstorming` and `writing-plans` write and commit specs and plans in `docs/superpowers/`** vs the docs map and scope. The project wins: plans stay in plan mode.
3. **TDD and `writing-plans` "commit" each red/green step** vs workflow §3 ("Every commit builds and passes… tests"; a unit's code and tests go in the same commit). The project wins: **a red test is never committed.**
4. **"Rulings, not stalls"** (`executing-plans`, `subagent-driven-development`) vs workflow §8. The project wins. Both skills are rejected.
5. **TDD "Write code before the test? Delete it"** vs review fixes on code that already exists. Adapted: for existing code, the proof is the revert check in `verification-before-completion` › *Key Patterns*. Revert the fix, the test must fail, then restore.
6. **TDD "every new function/method has a test"** vs testing §1. `testing.md` wins.
7. **TDD *When Stuck*: "Must mock everything → use dependency injection"** vs testing §3 rule 2 and memory `no-test-only-production-code`. The project wins: the seams are the platform's.
8. **TDD and verification "run the project's full suite"** vs HANDOFF §3 "Run checks one at a time". Compatible: run the lanes in sequence.
9. **`requesting-code-review` "Mandatory… before merge"** vs "no self-review subagent". The project wins.
10. **`receiving-code-review` replies in GitHub threads** vs ONE "Review fixes" comment. The project wins.
11. **`using-git-worktrees` and `finishing-a-development-branch`** vs workflow §6/§9. The project wins.
12. **`systematic-debugging` diagnostic logging** vs a clean commit. The logs come out before commit.
13. **The plugin's enablement** is an uncommitted edit to the tracked `.claude/settings.json` (`git diff`). It dirties worker A's tree, and `start-work-item` step 2 says "Check that the tree is clean… If a check fails, stop". So either A stops at every item, or it learns to ignore the check. §5.D settles it.

## 5. Recommendations (proposals only)

### 5.A A standard block for every worker prompt's "How to work"

> **Superpowers (selective).** This prompt, CLAUDE.md, the documents and the project's skills (`start-work-item`, `open-pr`, `add-error-code`) win over any Superpowers skill. This line is your human partner's explicit instruction to skip the skills marked "not used".
> - **Used:** `test-driven-development`, with `writing-good-tests.md` read. Write each test in its **owning lane** (testing.md) and see it fail first. Never commit a red test: a unit's test and code go in the same commit. For a fix to code that already exists, prove the test by reverting the fix. Name the break each test catches. For security, transaction and ordering properties, make that break once for real and watch the test fail. Seams stay the platform's (no test-only parameters).
> - **Used:** `systematic-debugging`, for any failure or flake. After three failed fixes, stop and report (workflow §8). Remove diagnostic logs before committing.
> - **Used:** `verification-before-completion`. Every claim in the PR description, the report or a commit body names the command or test that proves it, run on this head.
> - **Used, adapted:** `receiving-code-review`, for the fixes list. Verify each item and push back with reasons. Fold fixes into their commits, and write ONE "Review fixes" comment, with no thread replies.
> - **Used, in part:** `writing-plans`, inside plan mode: the file map, *Interfaces*, *No Placeholders*, and a *Review Focus* list (the inputs no planned test exercises), each with the test that pins it. Not used: its header, saving to `docs/superpowers/`, full code in the plan, per-step commits, and its execution handoff.
> - **Not used:** `brainstorming`, `executing-plans`, `subagent-driven-development`, `dispatching-parallel-agents`, `requesting-code-review`, `using-git-worktrees`, `finishing-a-development-branch`, `writing-skills`, `diagnosing-superpowers`.

### 5.B A block for review prompts

> **Superpowers is enabled in this folder; do not use it.** This prompt is your human partner's explicit instruction to skip every Superpowers skill and workflow. Invoke none: no `brainstorming`, no `requesting-code-review`, no `dispatching-parallel-agents`, no `subagent-driven-development`. Spawn no subagent beyond the ones this prompt names, and run no workflow. You may apply `writing-good-tests.md`'s *Mutation Check* as a reading lens on the tests, without invoking anything.

### 5.C Proposed edits to the project's documents

Each edit summarises and links, so each fact keeps one owner. Each one changes an authoritative document, so it needs the owner's approval (workflow §6).

1. **`docs/development/testing.md`.**
   - *Authority line:* "…It owns the placement of proof **and what makes a test a proof**, not its style."
   - *New §3 rules 5–7:*
     > 5. **Seen failing.** A new test is seen failing before the code that passes it, and in the same lane. A test for code that already exists is proven by reverting that code once. A red test is never committed ([workflow §3](workflow.md#commits)).
     > 6. **Name the break.** Every test can name the production change that would make it fail. An expectation is a hand-written literal, never computed by the code under test.
     > 7. **Make the break.** For a security, transaction or ordering property, the author makes that change once, sees the test fail, and restores it.
2. **`docs/development/workflow.md` §8**, a new row: *"A failure whose cause you have not found → Find the root cause before changing code; after three failed fixes, stop and escalate."*
3. **`docs/development/workflow.md` §5 (Done)**, one item: *"Every claim in the PR description names the test or command that proves it ([testing §3](testing.md#3-rules-that-bind-every-test))."*
4. **`.claude/skills/start-work-item/SKILL.md` step 4**, one bullet: *"each behaviour's lane, its test and the break it catches, and a Review Focus list ([testing §3](…))."*
5. **`.claude/skills/open-pr/SKILL.md` step 4:** *"…and which tests were seen failing first."*
6. **CLAUDE.md › *Decision precedence***, one line: *"A plugin's skills (such as Superpowers) are level 3; the prompt names which are used."*

### 5.D The configuration

There are three places the enablement can live:

1. **Each folder's untracked `.claude/settings.local.json`** (recommended).
   - `masaha-b` already does this.
   - It keeps the tree clean, it is personal and reversible, and it puts no third-party plugin on anyone else who clones the repository, such as an examiner.
   - The cost: every new folder needs it set by hand.
2. **Committed to `.claude/settings.json`.**
   - It is reproducible and visible in history.
   - But it is a new dependency of the working method, which workflow §6 says the owner approves. It would need its own PR and a line in `setup.md`. It also imposes the 1% rule on every session in every clone.
3. **The user-level `~/.claude/settings.json`.**
   - One place to set it.
   - But it loads Superpowers in every project the owner has, and in the analyst's and reviewers' sessions everywhere.

**Recommendation: option 1.** The owner should undo the uncommitted change to the tracked file and add the same key to `masaha/.claude/settings.local.json`. That file is gitignored (`.gitignore:29`) and already exists.

## 6. Open choices for the owner

1. **Where the red-first rule lives.**
   - Options: (a) in `testing.md` §3 (§5.C.1); (b) only in the prompts' block; (c) nowhere.
   - **Recommend (a).** A rule that only prompts carry is lost on the first prompt that forgets it, and one owner per fact puts it in the document.
2. **How strong the rule is.**
   - Options: (a) seen failing only; (b) plus *Name the Break*; (c) plus *Make the Break* for security, transaction and ordering properties.
   - **Recommend (c).** The evidence in §4.1 shows that (a) misses both named findings. (c) adds only a few runs per item.
3. **The plan format.**
   - Options: (a) `start-work-item` plus the named parts of `writing-plans`; (b) the full `writing-plans` format; (c) no change.
   - **Recommend (a).** (b) puts full code in the plan, which roughly doubles its tokens, and its header pulls in `subagent-driven-development`.
4. **`receiving-code-review`.**
   - Options: (a) adopt with the adaptations; (b) keep it "not used".
   - **Recommend (a).** It matches `workers-may-challenge`.
5. **Debugging as a project rule.**
   - Options: (a) the §8 row plus the skill; (b) the skill named in prompts only.
   - **Recommend (a).** It is one line, and it owns the stop.
6. **The configuration.**
   - Options: as in §5.D.
   - **Recommend option 1,** the local settings file.
7. **The pending per-commit check** (HANDOFF §3).
   - Red-first adds test runs on a machine that ran out of memory.
   - Options: (a) keep the full lanes for every commit; (b) lint and typecheck for every commit, with the full lanes on the head.
   - **Recommend deciding it now, with (b).** The red and green runs already test each unit as it is written (*opinion*).

### The cost (estimate, *opinion*)

- **Loading:** about 0.7k tokens for each session start, plus about 4k when TDD and `writing-good-tests.md` load, plus about 3k for debugging, verification and receiving when they trigger.
- **Red runs:** a single test file is cheap to run. An item with 5–15 new behaviours adds about 20–40k tokens and 15–40 minutes on the owner's machine.
- **Plan:** *Review Focus* and *Interfaces* add about 2–5k tokens. Rejecting full code in the plan avoids about 10–20k.
- **Net:** about +5–10% tokens for each Work Item compared with today's method. The return: about one should-fix test finding per reviewed PR was the class this targets (#40, #41, #38, #42). Each avoided fix round saves a fixes list, a worker round and a CI cycle.
- **What the rejected skills would have cost:** `subagent-driven-development` alone, at two subagents per task, would multiply an item's tokens several times. Today's reviews cost about 95k–296k each (REVIEW42, REVIEW38, REVIEW43).

## 7. What I could not verify, and the tokens

- **The H-1 plan itself** was not saved. Only the analyst's reply exists (`HOUSEKEEPING_PLAN_REPLY.md`, which keeps "item 3's three tests failing first"). The claim that Superpowers improved that plan rests on memory `superpowers-selective` alone.
- **I did not read** the session-start hook's script, so I cannot say whether it injects more than `using-superpowers`.
- **I did not check** whether `.superpowers/` is gitignored. Both skills that write there are rejected.
- **I had no data** on the workers' token use. The cost figures are estimates.
- **REVIEW35 and REVIEW38:** I read their findings and Verified OK lists, not every line.
- **Nothing was run.** No tests, no installs, no edits besides this file.

**Tokens:** about 180k for this conversation. No subagents and no workflows. This is under the 300k cap.
