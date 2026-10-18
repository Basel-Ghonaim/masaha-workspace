# M1 — reply to your plan

The plan is approved, all six stronger decisions included. Thank you for them: they are the kind this
section is for.

1. **The no-code exception:** `format:check` **and** the link check by hand (documentation §8). Yes.
2. **Workflow §3, *Commits*:** reworded to what is true — each commit a complete unit, lint and
   typecheck on each, the lanes once on the head (phase 4). Yes.
3. **The worker runs the early conflict check** and the report carries `git merge-tree --write-tree`
   of the pushed head against every other open PR's head. Yes; the analyst still reads it.
4. **B's licence names the error codes' catalogue entries**, declared in the plan. Yes.
5. **Two more triggers for a separate review:** a new dependency, and a change to CI or the build
   checks. Yes.
6. **Phase 4's lanes run one at a time;** servers started for the real run are stopped and their
   ports checked free. Yes.

**The main folder's `apps/web/.env`:** a note only, as you say; the owner will replace it. Nothing in
the documents.

**Two small points:**
- The plan reached us pasted in the conversation and `PLAN\` is still empty. As this item's step 2
  says, save it first to `C:\Users\basel\.prompt\MASAHA_WORKER_B\PLAN\M1_PLAN.md`, as approved here,
  then cut the branch and build.
- `write-plan` must say plainly that the plan is saved **before** any branch is cut or file edited,
  and that the turn ends there; `final-report` must include the merge-tree section (decision 3) and
  "anything that behaved unexpectedly, even unsolved".

Then carry on: four commits, `format:check` and the link check, `open-pr`, CI and `CLEAN`, the report
in `C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\M1_REPORT.md`. PR #50 is still open: touch none of
its files.
