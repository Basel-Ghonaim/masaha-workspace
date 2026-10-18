# Design fix 4 (the account) — build it from the plan

You are the **executor**. Build the approved plan, exactly:
`C:\Users\basel\.prompt\MASAHA_DESIGN\PLAN\FIX_ACCOUNT_PLAN.md`.

## Where and how

- **Work in `C:\Users\basel\masaha-design-b` only.** It is a git worktree of the Masaha repository,
  detached at `origin/main`. Nothing is installed there: `format:check` and `check:links` run in CI
  (the plan says so). Serve the prototype on **port 5347** as the plan's procedure says.
- **Follow the plan's §7 procedure step by step:** the branch, each commit in order with its exact
  subject, files and `CHANGES.md` line, the two check scripts at every commit, the frames to open after
  each commit and what to look for, the before/after images, the push, the PR with the description the
  plan writes out, waiting for CI and `CLEAN`, the report, the clean-up.
- **The plan's hazards (§9) are rules:** no object rest destructuring, no generic top-level names, no
  class missing from the prebuilt CSS, never edit `prototype/_ds/` or `_vendor/`, nothing outside
  `docs/design/`.
- **Where the plan leaves a choice to the owner, the owner's answers are below.** Anything else the
  plan does not say: do not invent it — stop and write the question in the report.
- **Look at every changed page with your own eyes** at 390, 768 and 1440 (the scripts see blanks and
  errors, not layout).
- **Never merge.** `jq` is not installed in Git Bash: use `gh … --jq`. Stop every server, browser and
  background shell you start; check port 5347 free.

## The owner's answers to the plan's questions

1. **Q1 — `Space details.html`:** yes, edit it for C4's two needs (AC-018's sign-in reason for a report;
   the favourite's failure on the way back), as the plan's "yes" path says.
2. **Q2 — `Directory.html:353`:** yes, reword its privacy promise («ويبقى على جهازك فقط») to agree with
   the new line, as the plan's "yes" path says.
3. **Q3 — AC-020's fourth password rule in the prototype's `auth.jsx`:** yes.
4. **S1–S10:** approved as written (DI-30, the countdown on the account pages only, is recorded).

## The other design worker

The owner's batch is built at the same time in `C:\Users\basel\masaha-design` (branch `design/owner`).
Never touch its files (the plan lists them). You share `CHANGES.md`, `INDEX.md`, the board and the
README's frame count, each in your own section; the PR that merges second rebases and keeps both.

## The report

Save it to `C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\FIX_ACCOUNT_REPORT.md`, in the sections the
plan's §7 lists, and say in it everything that departed from the plan, with why. Then stop.
