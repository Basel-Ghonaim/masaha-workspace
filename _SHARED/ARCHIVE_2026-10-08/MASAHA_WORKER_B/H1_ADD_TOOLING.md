An addition to the sixth commit of PR #45 (`docs: adopt the test and debugging rules`), which you are
building now. The owner and the analyst wrote the section below; **include it as written** (fix only
links or anchors that don't resolve, and say so). Same commit, no new one.

## 1. `docs/development/workflow.md` — a new §10 at the end

```markdown
## 10. AI tooling

The owner works with AI assistants in Claude Code. Their plugins are tools, not dependencies of the
project: nothing in the repository needs them, and the rules they help apply are owned by the
documents ([testing §3](testing.md#3-rules-that-bind-every-test), [§5](#5-definition-of-done-and-accepted),
[§8](#8-stop-rules)).

- **Superpowers** is optional and local: it is enabled per folder in the untracked
  `.claude/settings.local.json`, never in the tracked `.claude/settings.json`.
- **Precedence:** the task's prompt, then these documents, then the project's skills
  ([`.claude/skills/`](../../.claude/skills/)), then a plugin's skills. A session with no prompt
  follows this section too.
- **Used:**
  - `test-driven-development`, with its `writing-good-tests.md`: how testing §3's rules 5–7 are met
    (seen failing, name the break, make the break), each test in its owning lane. A red test is never
    committed.
  - `systematic-debugging`: for any failure or flake, the root cause first (§8). Diagnostic logs are
    removed before a commit.
  - `verification-before-completion`: every claim names the test or command that proves it (§5).
  - `receiving-code-review`, adapted: each item of a fixes list is verified against the code, and
    pushed back with reasons when it is wrong. Fixes fold into their commits, with ONE "Review fixes"
    comment and no thread replies.
  - `writing-plans`, in part, inside `start-work-item`'s plan mode: the file map, the interfaces
    between tasks, no placeholders, and a *Review Focus* list. Not its header, its saved plan files,
    full code in the plan, a commit per step, or its execution handoff.
- **Not used:**
  - `brainstorming`: the analysis round and the Work Item's prompt settle the decisions (§6).
  - `executing-plans` and `subagent-driven-development`: they decide conflicts and carry on, against
    §8, and exceed the prompts' subagent caps.
  - `dispatching-parallel-agents`: each prompt caps its subagents.
  - `requesting-code-review`: the review is an independent gate, never the author's own subagent.
  - `using-git-worktrees`: the folders are fixed (§9).
  - `finishing-a-development-branch`: merging and deleting branches are the owner's (§6);
    `open-pr` opens the pull request.
  - `writing-skills` and `diagnosing-superpowers`: only the owner invokes them.
- **Review sessions** use no plugin skill. They may read `writing-good-tests.md`'s mutation check as
  a lens on the tests.
```

## 2. `CLAUDE.md` › *Decision precedence*

Replace the line your plan adds with:

```markdown
A plugin's skills (such as Superpowers) rank below the documents and the project's skills; which are
used, and when, is in [workflow §10](docs/development/workflow.md#10-ai-tooling).
```

## 3. `docs/README.md` (the map)

The `workflow.md` entry gains "and the AI tooling", for example: "how work is executed, including two
workers in parallel and the AI tooling."

## Then
- Update `workflow.md`'s status line if it lists its sections, and the PR description's sixth row
  (it now also adds workflow §10).
- Checks as planned (lint and typecheck on the head; documents only). A plain push. Report once CI is
  green. Don't merge. No subagents.
