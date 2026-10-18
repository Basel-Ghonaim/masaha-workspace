# Review — PR #76 (design batch 5: the owner's management — prototype conformance)

You are an **independent reviewer** of PR #76 in the Masaha repository (Basel-Ghonaim/masaha), a
change to the living prototype in `docs/design/` only. Judge it **against its plan and against the
documents**, by reading the code and by looking at the frames.
Write your report to `C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\REVIEW76_<YOU>_REPORT.md`, where
`<YOU>` is your tool's name in capitals (`OPENCODE`, `COPILOT`). If two reviewers run, they work
apart; do not read the other's report.

## Rules

- **Work in `C:\Users\basel\masaha-design`**, the fixer's folder, now at the PR's head (`5a22676`).
  Its tree holds one untracked file, `final-report-76.md`, the fixer's leftover: ignore it, do not
  delete it. **Read only:** no edits, commits, checkouts, switches, installs, npm or test runs, no
  GitHub comments. First `git fetch origin` and check that `gh pr view 76 --json headRefOid` is still
  `5a226726…` and that the folder's `HEAD` matches it; write the head at the top of your report and
  check it again at the end. Base: `git merge-base origin/main HEAD`.
- **To look at frames:** serve the prototype read-only from that folder,
  `python -m http.server 5346 --directory docs/design/prototype` (port 5346; `npx serve`'s clean URLs
  drop query strings), and open the frames in a browser at the widths named. Save any evidence
  capture as `<ID>.png` in `C:\Users\basel\Downloads\review76-shots\`. **Stop the server by its PID at
  the end and check port 5346 is free.**
- **Report concrete problems only,** each verified: the file and line or the frame and its URL, what
  is wrong, the severity (**blocker / should-fix / nit**) and the fix. No praise, no summary. If
  unsure, say "plausible" and why.
- **No tool attribution** in what you write.

## What the PR must be

- **The plan, your checklist:** `C:\Users\basel\.prompt\MASAHA_DESIGN\PLAN\FIX_OWNER_PLAN.md`. Its
  **§8 *The reviewer's checklist*** (AC1–AC19 and the hazards row) is the core of this review: walk
  every row at **390, 768 and 1440, Arabic and English, light and dark**, unless the row names a
  width. Then §9 (the hazards) and §5 (the only files it may touch).
- **How it was built:** `PROMPT\FIX_OWNER_EXEC.md` (the execution brief) and the fixer's report
  `REPORT\FIX_OWNER_REPORT.md` — read its departures and judge each: the conditional-hook crash fixed
  in `OwnerShell` (and the same pattern left in `AdminShell` on `main`: confirm it is real and record
  it as a finding for later, not a fix here), the `SHIFTS_NOW` ordering trap, the missing design-system
  imports, `ExtendDialog` staying open after success (built verbatim, flagged), DI-30/31/33 routed to
  worker A, DI-32 to the API.
- **The owner's decisions:** `C:\Users\basel\.prompt\MASAHA_DESIGN\DECISIONS_OWNER.md` (O1–O13, the
  smaller OW items, and its notes at the top: **DI-10** — the account avatar leaves the phone's top bar
  and heads the drawer; **a package's price is above zero**; **O3 amended — no money on the
  overview**, not in a tile, a helper, a caption or a toast; **the editor boundary** — nothing the
  admin's editor shows changes), `DECISIONS_SHARED.md` (P1–P10, settled, with their amendments: no
  bottom bar on the owner's overview; report only how a page applies them).
- **The documents it must stay true to** (the lens, `MASAHA_DESIGN\REVIEW_LENS.md` §2–§3): nothing on
  screen the API or the data model cannot hold (`docs/api/api-contract.md`,
  `docs/architecture/data-model.md`: no reporter's name to the owner, no title or author on an
  announcement, one amount and one billing per package, prices and packages above zero); live status
  a state, never a public count (ADR 0008; «27 / 40» is the owner's private figure only); the glossary
  (`docs/project/glossary.md`); the design system's components and tokens
  (`docs/frontend/design-system/foundation.md`); RTL/LTR; Arabic plurals (O5).

## Look at these, in this order

1. **The editor boundary (AC4):** `profile-a.jsx` untouched; `profile-b.jsx` changed only by the plan's
   three default-preserving props and one deletion; `Admin space edit.html?id=golden`, `?id=focus` and
   `?id=new` identical to `main` (compare against `main`'s files served the same way, or the fixer's
   before images in `C:\Users\basel\Downloads\design-fix-owner\`). Worker A is building that editor
   in code from `main`'s prototype: any change here is a blocker.
2. **§8's rows, every one,** at the widths and modes it names: a frame that blanks, errors, scrolls
   sideways or cuts at the edge is a blocker.
3. **No money on the overview,** and DI-10's top bar on a phone (`Owner overview.html` and `Desk.html`
   at 390, the drawer open).
4. **Truth to the API and the data model** (above), and every price and package amount above zero.
5. **The hazards (§9):** no object rest; no generic top-level names; `O` never redeclared; every class
   in `_ds_bundle.css` or a token-only rule in `masaha.css` (classes in conditions checked by eye);
   `_ds/` and `_vendor/` untouched; hooks before any early return (the crash the fixer found — any
   other page with the same pattern in this PR?).
6. **The archive:** `CHANGES.md`, `INDEX.md` (§55, 22 rows), the board (its owner section, 22 frames)
   and README's counts agree with each other and with the frames.
7. **Boundaries and commits:** `git diff --stat $(git merge-base origin/main HEAD)..HEAD` lists only
   §5's files, nothing of batch 4's (`design/account`, PR #75) beyond the shared archive files; 13
   commits, each subject ≤ 50 characters (count them yourself).

PR #75 (batch 4) is open beside it and conflicts with it only in the four shared archive files
(`CHANGES.md`, `INDEX.md`, the board, the README's count) — by design, resolved at merge; do not
report that conflict.

## Your output

One file (the path above): a one-line verdict; the findings, most severe first (severity, where,
what, fix); a short "Checked and fine" list; then stop.
