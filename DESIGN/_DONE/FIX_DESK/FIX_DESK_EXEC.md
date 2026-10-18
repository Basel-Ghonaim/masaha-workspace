# Design fix 6 (the front desk) — build it from the plan

You are the **executor**. Build the approved plan, exactly:
`C:\Users\basel\.prompt\MASAHA_DESIGN\PLAN\FIX_DESK_PLAN.md`.

## Where and how

- **Work in `C:\Users\basel\masaha-design-b` only.** It is a git worktree of the Masaha repository,
  detached. **Batch 5 (#76) has merged** (`main` = `bfe1749`): the plan's first step checks that and
  the two batch-5 lines it changes; cut `design/desk` from the latest `origin/main` as the plan says.
  Serve the prototype on **port 5347** as the plan's procedure says.
- **Follow the plan's procedure step by step:** the branch, each commit in order with its exact
  subject, files and `CHANGES.md` line, the check scripts at every commit, the frames to open after
  each commit, the board's section 56 with its frames and coordinates, the before/after images,
  `format:check` and `check:links` (or CI, as the plan says), the push, the PR with the description the
  plan writes out, waiting for CI and `CLEAN`, the report, the clean-up.
- **A tested reference exists.** The planner built every code change in a scratch copy and checked it
  in the browser. Its diff against the pages before the batch is
  `C:\Users\basel\.prompt\MASAHA_DESIGN\PLAN\desk-scratch-reference.diff` (11 files; the board's
  frames are not in it). **The plan wins:** use the diff to check your work or to resolve a doubt, never
  to add anything the plan does not say. If the two disagree, follow the plan and note it in the report.
- **The plan's hazards are rules:** no object rest destructuring; no generic top-level names; each new
  top-level name once per page; hooks before any early return; no `size` or `variant` value the design
  system does not have (`"default"` is not one); no class missing from the prebuilt CSS; never edit
  `prototype/_ds/` or `_vendor/`; nothing outside `docs/design/`.
- **Boundaries:** worker A builds the admin's editor in code: never touch `Admin space edit.html`,
  `profile-a.jsx`, `profile-b.jsx`, `admin.jsx` or the admin's pages; nor `shared.jsx`, `auth.jsx`,
  `account.jsx` or the account pages. Batch 5's files only where the plan says (one line each in
  `Owner overview.html` and Finance's link).
- **Look at every changed page with your own eyes** at 390, 768 and 1440, Arabic and English, light
  and dark.
- **Never merge.** `jq` is not installed in Git Bash: use `gh … --jq`. If `git rebase --continue` or a
  commit would open an editor, use `git -c core.editor=true …`. Stop every server, browser and
  background shell you start; check port 5347 free.

## The owner's answers to the plan's §10

1. **S1–S17:** approved as recommended.
2. **DI-41–DI-47:** recorded as routed, nothing built for them (DI-41 and DI-47 to the docs with step
   7; DI-42 to the API and web; DI-43 to worker A's design-system item; DI-44–DI-46 to a later
   prototype item). List them in the report and the PR description.
3. **Where:** `C:\Users\basel\masaha-design-b`, as above.

Anything else the plan does not say: do not invent it — stop and write the question in the report.

## The report

Save it to `C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\FIX_DESK_REPORT.md`, in the sections the plan
lists, and say in it everything that departed from the plan, with why. Then stop.
