# SK-1 — Work-item skills (procedures as Claude Code skills)

**Worker B** · folder `C:\Users\basel\masaha-b` · branch `chore/work-item-skills`

**Size cap:** use at most 4 subagents in total. Do not run any workflow.

## 1. How to work (mandatory)

1. Read `CLAUDE.md`, then `docs/development/workflow.md` (all of it: these skills package its procedures), then `docs/README.md`.
2. Then read:
   - `docs/backend/conventions.md` §4 (Errors: adding a domain error code);
   - `docs/api/api-contract.md` §6;
   - `docs/development/testing.md` and `docs/development/setup.md` (the lanes and their commands);
   - `.claude/settings.json`.
3. Work in **PLAN MODE**. Write nothing until the owner approves your plan.
4. Before you plan, check:
   - you are in `C:\Users\basel\masaha-b`;
   - the working tree is clean;
   - after `git fetch origin`, `HEAD` is detached at `origin/main`.

   If any check fails, stop and report. Do not fix it yourself.
5. Once the plan is approved, cut the branch with `git switch --no-track -c chore/work-item-skills origin/main`. The first push is `git push -u origin chore/work-item-skills`.

## 2. Context

Every Work Item prompt repeats the same procedures: the start-of-item checks, the PR rules, and the steps for a new error code. This item packages them as **project skills** in `.claude/skills/`. Claude Code loads a skill only when its description matches the task, so the prompts get shorter and no step is forgotten.

**The governing principle:** a skill is a **runbook, not a source of truth**. It holds ordered steps, and each step links to the section that owns its rule. It never restates a rule in its own words beyond one short line. If a skill and a document ever disagree, the document wins.

## 3. Decisions already made (do not reopen)

The owner approved these.

- **Q1. Location:** in the repository, under `.claude/skills/<name>/SKILL.md`, committed. Both worker folders get them through git.
- **Q2. Ownership:**
  - `workflow.md` stays the owner of every rule;
  - the skills only link to it and to the other owning documents;
  - three pointers are added: one sentence in `workflow.md`, one entry in the `docs/README.md` map, and the `CLAUDE.md` session checklist naming `start-work-item` and `open-pr`.
- **Q3. Invocation:** model-invoked, by a precise `description`. Prompts will also name the skill.
- **Q4. Timing:** now, in parallel with worker A's final F-5a round.
- **Exactly three skills,** with the content below. No others.

## 4. The three skills

Each `SKILL.md` has YAML frontmatter with `name` and `description`, then the steps.
- **The description** says WHEN to use the skill, in one or two sentences, precise enough that it triggers on the right task and not on others.
- **The steps** are numbered, each one line or two, with a relative link to the owning section (verify each anchor exists).
- **Each file stays under about 60 lines.**
- **The frontmatter format:** if you are unsure of the current Claude Code skill format, confirm it with one `claude-code-guide` subagent (it counts toward the cap). Do not guess fields.

### 4.1 `start-work-item`
**Use:** at the start of every Work Item conversation, before planning.
1. Identify the worker and its folder: worker A in the main folder, worker B in the `masaha-b` worktree (workflow §9).
2. `git fetch origin`; check the tree is clean and `HEAD` is at `origin/main` (detached for worker B). If not, stop and report.
3. Read `CLAUDE.md`, `workflow.md` and `docs/README.md`, then the single owning document for the area, found through the README map.
4. Plan in plan mode. The plan names:
   - the files to touch;
   - the files shared with the other worker, and the section each side owns (workflow §9);
   - the decisions needed from the owner;
   - the commit plan;
   - the lanes to run.
5. After approval, cut the branch: worker A `git switch -c <branch> origin/main`; worker B `git switch --no-track -c <branch> origin/main` (workflow §9).
6. Respect the size cap: at most 4 subagents and no workflows, unless the prompt says otherwise.

### 4.2 `open-pr`
**Use:** when a Work Item's implementation is finished, and again after each round of review fixes.
1. Self-review against the Definition of Done (workflow §5) and the scope (workflow §4).
2. **Truth check:**
   - every comment and every document sentence states what holds now, never what is planned (CLAUDE.md, "Claim only what is true");
   - every test's title is something the test actually asserts.
3. `git fetch` and rebase on `origin/main`. On conflict, keep both sides. The lockfile: take main's `package-lock.json`, run `npm install`, never edit it by hand (workflow §9).
4. Run every lane (setup.md), and record the counts and what was NOT run, for Evidence.
5. UI changes: screenshots in RTL and LTR, light and dark, phone and desktop (workflow §5). Save them outside the repository, in the folder the prompt names. Never commit them.
6. `gh pr create --assignee @me`, with one type label and the area labels, and the workflow §3 description template. No tool or AI attribution anywhere.
7. **After review fixes:**
   - update the PR description to the final state;
   - keep exactly ONE "Review fixes" comment, a table of each item id, its severity, and the commit that fixed it, or "not done" with the reason. Edit that comment in later rounds; never add a second.
8. Stop. Never merge; never create an Issue (workflow §6).

### 4.3 `add-error-code`
**Use:** when a change adds a new domain error code.
1. Follow the four steps of conventions §4, *Adding a domain error code*, in its order: the code in `packages/shared`, its text in both catalogues, its line in api-contract §6, a test that provokes it. Link there; don't copy the steps' details.
2. In the PR description, list each new code with its English and Arabic text, and mark the Arabic as **needing the owner's approval**.

## 5. The pointers

Each pointer is one sentence or one line. No restated rules.
- **`workflow.md`:** one sentence, where it reads naturally (propose the place in the plan): the repeating procedures are packaged as skills in `.claude/skills/`; they link to this document, and this document wins if they disagree.
- **`docs/README.md`:** one entry in the map for `.claude/skills/`, described as runbooks that own no facts.
- **`CLAUDE.md`:** the session checklist names `start-work-item` at step 1 and `open-pr` at step 4. Keep CLAUDE.md a pointer; add nothing else.

## 6. Contract

**Acceptance criteria**
- [ ] Three skills exist, each under `.claude/skills/<name>/SKILL.md`, each with valid frontmatter (`name`, `description`).
- [ ] Every step that carries a rule links to its owning section, and every link and anchor resolves.
- [ ] No skill restates a rule beyond one short line; nothing in them contradicts the documents.
- [ ] The three pointers exist, one line each.
- [ ] `.claude/settings.json` and `.claude/settings.local.json` are untouched.

**Out of scope**
- Any other skill (after-merge sync, review, screenshots).
- Any change to a rule in `workflow.md`, `conventions.md` or any other document beyond the three pointers.
- Any code change, dependency, hook or settings change.

## 7. Parallel work

**Worker A** is working in `C:\Users\basel\masaha` on PR #25 (`feat/auth-api`), its final round.

- **Worker A's files. Do not touch them:**
  - everything under `apps/api/` and `packages/shared/`;
  - `docs/backend/**`, `docs/api/**`, `docs/plans/**`, `docs/architecture/**`;
  - the copy catalogues.

  You only link to `conventions.md` §4 and `api-contract.md` §6; you never edit them.
- **Shared files.** Declare them in your plan, and edit each one minimally:
  - `docs/README.md`: your one map entry only (worker A changed one line there already);
  - `CLAUDE.md` and `docs/development/workflow.md`: yours alone in this round, but keep each change to one line.
- **Rebasing:** before you open the PR, fetch and rebase on the latest `origin/main`. If PR #25 merges first, rebase again and keep both sides on any conflict.
- **The lockfile:** no dependency is added, so `package-lock.json` must not change.
- **Databases:** none needed.

## 8. Commits

Atomic, in Conventional Commits format, staged by path (never `git add -A` or `git add .`), with `git status` before each commit. Propose the exact split in the plan. A likely split:
1. `chore(skills): add the start-work-item skill`, together with the three pointers, since this commit introduces the mechanism.
2. `chore(skills): add the open-pr skill`.
3. `chore(skills): add the add-error-code skill`.

## 9. Evidence

- This change is documentation and tooling only. Run `npm run lint` once to show nothing else moved, and state in Evidence that no test lane applies.
- **Check every link:** list in the PR each link and anchor you verified.
- **Discovery check:** state in the PR that the owner should confirm, in a fresh Claude Code session after merge, that the three skills are listed. You cannot prove this from inside your own session; don't claim it.

## 10. Pull request

- **Title:** the first commit's title.
- **Labels:** `chore`, `area:docs`.
- `gh pr create --assignee @me`.
- **Description:** the workflow §3 template. In the Summary, name Q1–Q4 and the runbook principle.
- **No tool or AI attribution** anywhere: commits, PR, files. No `Co-Authored-By` trailer, no "generated with" footer.
- **Do not merge. Do not create an Issue.**
- When the PR is open, stop and report briefly: the PR link, the commits, the links you checked, and anything you left out.

## 11. Stop rules

- **If a procedure has no owning section to link to** (a step whose rule exists nowhere in the documents), don't write the rule into the skill. Stop and list it in your plan or report, as a proposed document change for the owner to decide.
- **Anything unrelated you notice:** list it in your report; do not fix it.
- **Worker A's files:** if you think you need to touch one, stop and ask.
