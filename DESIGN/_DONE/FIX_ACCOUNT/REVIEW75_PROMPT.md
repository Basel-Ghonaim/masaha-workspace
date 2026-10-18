# Review — PR #75 (design batch 4: the account and signing in — prototype conformance)

You are an **independent reviewer** of PR #75 in the Masaha repository (Basel-Ghonaim/masaha), a
change to the living prototype in `docs/design/` only. Judge it **against its plan and against the
documents**, by reading the code and by looking at the frames.
Write your report to `C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\REVIEW75_<YOU>_REPORT.md`, where
`<YOU>` is your tool's name in capitals (`OPENCODE`, `COPILOT`). If two reviewers run, they work
apart; do not read the other's report.

## Rules

- **Work in `C:\Users\basel\masaha-design-b`**, the fixer's folder, now at the PR's head
  (`f100a28`, tree clean). **Read only:** no edits, commits, checkouts, switches, installs, npm or
  test runs, no GitHub comments. First `git fetch origin` and check that `gh pr view 75 --json
  headRefOid` is still `f100a287…` and that the folder's `HEAD` matches it; write the head at the top
  of your report and check it again at the end. Base: `git merge-base origin/main HEAD`.
- **To look at frames:** serve the prototype read-only from that folder,
  `python -m http.server 5347 --directory docs/design/prototype` (port 5347; `npx serve`'s clean URLs
  drop query strings), and open the frames in a browser at the widths named. Save any evidence
  capture as `<ID>.png` in `C:\Users\basel\Downloads\review75-shots\`. **Stop the server by its PID at
  the end and check port 5347 is free.**
- **Report concrete problems only,** each verified: the file and line or the frame and its URL, what
  is wrong, the severity (**blocker / should-fix / nit**) and the fix. No praise, no summary. If
  unsure, say "plausible" and why.
- **No tool attribution** in what you write.

## What the PR must be

- **The plan, your checklist:** `C:\Users\basel\.prompt\MASAHA_DESIGN\PLAN\FIX_ACCOUNT_PLAN.md`.
  Its **§8 *The reviewer's checklist*** is the core of this review: walk every row (decision, files,
  frames, what to verify by eye) at **390, 768 and 1440, Arabic and English, light and dark**, unless
  the row names a width. Then its *Acceptance criteria* (the reviewer ticks each), §5 (the files never
  touched) and §9 (the hazards: Babel's shared globals, hooks order, the prebuilt CSS, truth to the
  API).
- **How it was built:** `PROMPT\FIX_ACCOUNT_EXEC.md` (the execution brief) and the fixer's report
  `REPORT\FIX_ACCOUNT_REPORT.md` — read its departures and judge each.
- **The owner's decisions:** `C:\Users\basel\.prompt\MASAHA_DESIGN\DECISIONS_ACCOUNT.md` (C1–C8, the
  smaller AC items, its *Amended 2026-10-13* note: C5's forced-change line), `DECISIONS_SHARED.md`
  (P1–P10, settled; report only how a page applies them), and from `DECISIONS_PUBLIC.md` the
  *Changed 2026-10-13* note: the location privacy line now reads «يُرسَل موقعك مقرَّبًا لترتيب
  المساحات حسب المسافة فقط، ولا يُحفظ.» in `shared.jsx` **and** `Directory.html`'s own promise.
- **The documents it must stay true to** (the lens, `MASAHA_DESIGN\REVIEW_LENS.md` §2–§3): nothing on
  screen the API cannot do (`docs/api/api-contract.md`: no sign-out of all devices, no email change,
  no password form for a Google-only account, favourites answered whole, reports paged); the location
  is sent rounded, only to sort, never stored (`docs/backend/security.md` › *Location*,
  `docs/project/overview.md` › *Near me*); the glossary's terms (`docs/project/glossary.md`); the
  design system's components and tokens (`docs/frontend/design-system/foundation.md`); RTL/LTR
  (addresses, emails and numbers LTR inside Arabic).

## Look at these, in this order

1. **§8's rows, every one,** at the widths and modes it names: a frame that blanks, errors, scrolls
   sideways or cuts at the edge is a blocker.
2. **Truth to the API and the privacy line:** no control the API cannot serve; the new location line
   in every place §7 names, and `grep -rn "على جهازك فقط\|stays on your device"
   docs/design/prototype` prints nothing.
3. **The hazards (§9):** each new top-level name defined once per page (grep the list in §9); no
   object rest; hooks before any early return; every class either in `_ds_bundle.css` or a
   token-only rule in `masaha.css` (classes chosen in a condition checked by eye); `_ds/` and
   `_vendor/` untouched.
4. **The archive:** `CHANGES.md`, `INDEX.md`, the board (section 54) and README's frame count agree
   with each other and with the frames; no overlap with batch 3's frames.
5. **Boundaries:** no file of §5's *Never touched* (the owner's batch files above all); ten commits,
   each subject ≤ 50 characters (count them yourself).
6. **The fixer's departures:** the 19 before-files "of unknown provenance" kept in the shared images
   folder (are they in the repository? should they be?), the accidental kill of every Chrome (any
   trace in the tree?), en/dark only spot-checked (check them yourself).

## Your output

One file (the path above): a one-line verdict; the findings, most severe first (severity, where,
what, fix); a short "Checked and fine" list; then stop.
