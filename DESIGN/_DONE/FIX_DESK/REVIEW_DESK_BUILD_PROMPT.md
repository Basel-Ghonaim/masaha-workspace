# Review — the desk batch's PR (design batch 6: the front desk — prototype conformance)

You are an **independent reviewer** of the pull request built from branch `design/desk` in the
Masaha repository (Basel-Ghonaim/masaha), a change to the living prototype in `docs/design/` only.
Judge it **against its plan and against the documents**, by reading the code and by looking at the
frames. Write your report to `C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\REVIEW_DESK_<YOU>_REPORT.md`,
where `<YOU>` is your tool's name in capitals (`COPILOT`, `OPENCODE`). If two reviewers run, they work
apart; do not read the other's report.

## Rules

- **Find the PR first:** `gh pr list --head design/desk --state open --json number,headRefOid`. If
  there is none, stop and say so. Write its number and head at the top of your report, and check at
  the end that the head has not moved.
- **Work in `C:\Users\basel\masaha-design-b`**, the executor's folder, once it stands at the PR's head
  with a clean tree (`git status`, `git rev-parse HEAD`). If it does not, stop and say so. **Read
  only:** no edits, commits, checkouts, switches, installs, npm or test runs, no GitHub comments.
  `git fetch origin` first. Base: `git merge-base origin/main HEAD`.
- **To look at frames:** serve the prototype read-only from that folder,
  `python -m http.server 5348 --bind 127.0.0.1 --directory docs/design/prototype` (port **5348**, so
  the executor's 5347 stays free), and open the frames at the widths named. Save any evidence capture
  as `<ID>.png` in `C:\Users\basel\Downloads\review-desk-shots\`. **Stop the server by its PID at the
  end and check port 5348 is free.**
- **Report concrete problems only,** each verified: the file and line or the frame and its URL, what
  is wrong, the severity (**blocker / should-fix / nit**) and the fix. No praise, no summary. If
  unsure, say "plausible" and why. **No tool attribution** in what you write.

## What the PR must be

- **The plan, your checklist:** `C:\Users\basel\.prompt\MASAHA_DESIGN\PLAN\FIX_DESK_PLAN.md`. Its
  **§8 *The reviewer's checklist*** is the core of this review: walk every row at **390, 768 and 1440,
  Arabic and English, light and dark**, unless the row names a width. Then its *Acceptance criteria*
  (§1), §5 (the files and the boundaries), §6 (the ten commits) and §9 (the hazards).
- **The owner's answers:** `PROMPT\FIX_DESK_EXEC.md` (S1–S17 approved; DI-41–DI-47 recorded, not
  built). **How it was built:** the executor's report `REPORT\FIX_DESK_REPORT.md` — judge each
  departure. A tested reference of the code exists (`PLAN\desk-scratch-reference.diff`); the plan wins
  over it.
- **The owner's decisions:** `C:\Users\basel\.prompt\MASAHA_DESIGN\DECISIONS_DESK.md` (K1–K8 and the
  DK items), `DECISIONS_SHARED.md` with its amendments (**P1:** «تسجيل زيارة» is the phone's one
  bottom-bar action; **P8:** the desk keeps its success toasts, every money action naming its amount;
  **P9:** a settled customer archived at once with «تراجع», an owing one through an `AlertDialog`
  naming the debt), `DECISIONS_OWNER.md` (the shell and DI-10 the desk inherits).
- **The documents it must stay true to** (the lens, `MASAHA_DESIGN\REVIEW_LENS.md` §2–§3): the data
  model's desk entities and the ledger (ADR 0010: append-only, a payment voided with who and why,
  never deleted; credit only on usage), ADR 0009 (who may do what at the desk), ADR 0008 (live status
  a state, never a public count), `docs/project/overview.md` (*Not in v1*: no online payment, no QR,
  no booking), the glossary, the design system's components and tokens, RTL/LTR, Arabic plurals.

## Look at these, in this order

1. **No hidden money (K4) and the ledger's rules:** every amount the desk takes or leaves owing is
   shown and named; a void shows who and why, struck through, out of the totals; nothing deletes a
   payment; the write-off (K6) is the owner's only, with a required reason, never a payment.
2. **The money block (K2, K3):** «المستحق», «المستلم الآن» filled with what is due, «الطريقة», the live
   line (debt with the phone required, or the change), the submit naming the amount, «لم يدفع شيئًا»;
   a renewal with a debt paid oldest first; S4, S5, S14 as approved.
3. **§8's rows, every one,** at the widths and modes it names: a frame that blanks, errors, scrolls
   sideways or cuts at the edge is a blocker.
4. **The search (K1, S7, S12)** and the phone order (DK-003); the bottom bar (P1).
5. **The hazards (§9):** no object rest; no generic top-level names; each new top-level name once per
   page; hooks before any early return (no `useIsTablet() && …` pattern); no `"default"` size or
   variant; every class in `_ds_bundle.css` or a token-only rule in `masaha.css` (classes in
   conditions checked by eye); `_ds/` and `_vendor/` untouched.
6. **Batch 5's two lines only** (`Owner overview.html`'s `Desk.html#unpaid`; Finance's `?month=`):
   nothing else of the owner's, admin's, account's or the editor's files.
7. **The archive:** `CHANGES.md` (batch 6), `INDEX.md` (section 56), the board (section 56, its frames
   after batch 5's without overlap, the 768 frames, the twelve relabelled frames of S8), README's
   counts and `SCREENS.md` (S17) agree with each other and with the frames.
8. **The commits:** ten; count each subject's characters yourself (≤ 50, no exception).

## Your output

One file (the path above): a one-line verdict; the findings, most severe first (severity, where,
what, fix); a short "Checked and fine" list; then stop.
