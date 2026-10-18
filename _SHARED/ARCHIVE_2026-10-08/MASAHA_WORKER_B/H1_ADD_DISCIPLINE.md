One more unit for PR #45, in this same session: the owner adopted part of Superpowers, and its
lasting rules belong in the project's own documents. They touch the files this PR already edits, so
they go here as **a sixth commit** (a new unit, not a fixup), before the PR's review.

**Plan it briefly in plan mode first** (the files, the exact wording, the commit), then build it.

## Source
Read `C:\Users\basel\.prompt\SUPERPOWERS_REVIEW_REPORT.md` §4.1 (the evidence), §4.4 and **§5.C**
(the proposed wording). The owner approved §5.C's six edits and the report's choices 1–5 (a red-first
rule in testing.md, at strength (c); plans keep `start-work-item` with the named parts of
`writing-plans`; `receiving-code-review` adapted; debugging as a workflow §8 row). Superpowers' own
`test-driven-development/writing-good-tests.md` (under
`C:\Users\basel\.claude\plugins\cache\claude-plugins-official\superpowers\6.4.1\skills\`) is the
background for rules 6 and 7; the project states them in its own words.

## The edits (one owner per fact; summarise and link; keep each short)
1. `docs/development/testing.md`: the Authority line ("…the placement of proof **and what makes a
   test a proof**, not its style"), and §3 rules 5–7 — **seen failing** (a new test fails before the
   code that passes it; code that already exists is proven by reverting it once; a red test is never
   committed), **name the break** (every test can name the production change that would make it
   fail; expectations are hand-written, never computed by the code under test), **make the break**
   (for a security, transaction or ordering property, the author makes that change once, sees the
   test fail, and restores it). Fit them with the rule 3 you have just rewritten.
2. `docs/development/workflow.md` §8: a row — a failure whose cause you have not found → find the
   root cause before changing code; after three failed fixes, stop and escalate.
3. `docs/development/workflow.md` §5 (Done): one item — every claim in the PR description names the
   test or command that proves it.
4. `.claude/skills/start-work-item/SKILL.md` step 4: the plan names each behaviour's lane, its test
   and the break it catches, plus a *Review Focus* list (inputs no planned test exercises).
5. `.claude/skills/open-pr/SKILL.md` step 4: the evidence says which tests were seen failing first.
6. `CLAUDE.md` › *Decision precedence*: one line — a plugin's skills (such as Superpowers) rank below
   the documents and the project's skills; each prompt names which are used.

## Rules
- No other change. No code. Headers' *Last Updated* where the documents carry one.
- Commit subject ≤ 50 characters, for example `docs: adopt the test and debugging rules`.
- Checks: this commit is documents only; lint and typecheck on the head are enough locally; CI runs
  every lane.
- Update the PR: the title (for example `chore: resolve five findings, adopt test rules`) and the
  description (the sixth commit, and that it comes from the owner's Superpowers decision).
- Push (a plain push: a new commit, no rewrite), report once CI is green. Don't merge. No subagents.
