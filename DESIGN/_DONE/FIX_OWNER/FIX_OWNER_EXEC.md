# Design fix 5 (the owner's management) — build it from the plan

You are the **executor**. Build the approved plan, exactly:
`C:\Users\basel\.prompt\MASAHA_DESIGN\PLAN\FIX_OWNER_PLAN.md`.

## Where and how

- **Work in `C:\Users\basel\masaha-design` only** (the plan says so; it was written from another
  worktree, which you never touch). It is a git worktree of the Masaha repository, detached at
  `origin/main`. Serve the prototype on **port 5346** as the plan's procedure says.
- **Follow the plan's procedure step by step:** the branch, each commit in order with its exact subject,
  files and `CHANGES.md` line, the two check scripts at every commit, the browser-check script and the
  frames to open after each commit, the 22 new board frames with their coordinates, the before/after
  images, `format:check` and `check:links`, the push, the PR with the description the plan writes out,
  waiting for CI and `CLEAN`, the report, the clean-up.
- **The plan's hazards are rules:** no object rest destructuring, no generic top-level names, no class
  missing from the prebuilt CSS, never edit `prototype/_ds/` or `_vendor/`, nothing outside
  `docs/design/`.
- **The editor boundary (the owner's rule):** worker A is building the admin's space editor in code.
  Nothing the admin's editor shows may change; `profile-a.jsx` stays untouched; in `profile-b.jsx` only
  what the plan says (three optional props the admin's editor does not pass, and removing the unused
  `CapacitySection`). Never touch `Admin space edit.html`, the desk's pages and modules, or
  `masaha/shared.jsx` (the account batch's this round).
- **Where the plan leaves a choice to the owner, the owner's answers are below.** Anything else the
  plan does not say: do not invent it — stop and write the question in the report.
- **Look at every changed page with your own eyes** at 390, 768 and 1440.
- **Never merge.** `jq` is not installed in Git Bash: use `gh … --jq`. Stop every server, browser and
  background shell you start; check port 5346 free.

## The owner's answers to the plan's questions

1. **S1–S14:** approved as written (S2 removes the unused `CapacitySection`; S5's «إيقاف الوصول»; S7
   drops the overview's desk shortcut).
2. **The shared editor's wording (DI-30, DI-31, DI-33):** **not built here** — they go to worker A's
   editor items (the save toast naming its group is already in S2b-4a; «الفترة» / «لمن» to S2b-4b's
   prices; the empty gallery with the photos' later item). Record them in the report as routed.
3. **DI-38:** yes — each Settings card shows its own failure.
4. **DI-32 (the photos' limit and WebP)** is a question for the API; record it in the report, build
   nothing for it.

## The other design worker

The account batch is built at the same time in `C:\Users\basel\masaha-design-b` (branch
`design/account`). Never touch its files. You share `CHANGES.md`, `INDEX.md`, the board (your section
55 and your frames below theirs) and the README's frame count, each in your own section; the PR that
merges second rebases and keeps both.

## The report

Save it to `C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\FIX_OWNER_REPORT.md`, in the sections the
plan lists, and say in it everything that departed from the plan, with why. Then stop.
