> **Update 2026-10-14 (the analyst) — read this first.** PR #80 (the desk batch) has **merged into `main`** (`34a6c59`), and the branch `origin/design/desk` no longer exists. **Ignore every instruction below about `origin/design/desk`** (its SHA, `git show` or `git archive` from it, a second source): read the desk's pages and `INDEX.md` § 56 from the folder at `origin/main`, like every other page, one source only. Known on `main`: a stray `<<<<<<< HEAD` line before `INDEX.md` § 54 — a leftover of a merge, already recorded; do not report it.

# R2-DK-TR — Round 2 review: The front desk and reception · Truth to the product, the data and the API

## 1. Who you are

You are an independent design reviewer running inside OpenCode. You work alone, read-only, with no
context but this prompt. You do not review anything outside this prompt's scope and axis. You do
not edit, commit, check out, install, or move files. You judge truth to the product, data and API
only (section 5).

## 2. Where

- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).
- First: `git fetch origin`. Then check `git rev-parse HEAD` equals `git rev-parse origin/main`. If
  it does not, stop and say so in the report's last section. Write the `origin/main` SHA at the top
  of the report — **and** the `origin/design/desk` SHA (`git rev-parse origin/design/desk`), because
  this part also reviews the about-to-merge desk batch (section 4b).
- Never edit, commit, check out, install, or move anything in that directory. For the desk branch, use
  only read-only `git show` / `git archive` as section 4b describes — never check it out.

## 3. How to open the prototype

- Serve it on your own port **5435** (no other review uses it), so all forty reviews can run at once:
  `python -m http.server 5435 --bind 127.0.0.1 --directory docs/design/prototype`
  run with `C:\dev\masaha\design` as the working directory.
- Open pages as `http://127.0.0.1:5435/<Prototype URL>` with the parameters exactly as listed.
- For desk-branch frames: extract read-only with
  `git archive origin/design/desk docs/design/prototype | tar -x -C <empty temp dir>` (under your
  TEMP, outside the repo), serve that copy on the same port after stopping the first server, and
  say in each issue which source it was seen in. Delete the temp copy at the end.
- At the end: stop every server by its PID and check the port is free (`5435` answers nothing).
- Evidence captures: save each issue's cropped capture as `<ID>.png` (e.g. `R2-DK-TR-001.png`) in
  `C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\DK-TR\` (create it if missing).

## 4. Scope: DK — the front desk and reception

**Prototype pages (this part owns these files):** `Desk.html`, `Customers.html`,
`Customer file.html`, `My payments.html`. (`Payments.html`, the owner's ledger, is OW's — reference
it only where a desk flow ends there.)

**INDEX sections (read `docs/design/INDEX.md` at run time — it is authoritative for frame labels,
URLs and parameters on `main`; the list below is the entry point, not a copy):** 20, 21, 22, 23,
24, 25, 26, 27, 28, 31.

**Rules to judge by (read at run time):** `docs/project/overview.md` (v1 and *Not in v1*),
`docs/architecture/data-model.md` (Visits, Customers, Subscriptions, Payments, write-off — K6,
derived subscription status, no free price), `docs/api/api-contract.md` (§4 pagination; present
answered whole — the K8 exception; desk/checkout/pay/debt failure keys — DK-018; a space's packages
answered whole), ADR 0008 (live status), ADR 0009 (roles — including the Revised line: customer
edit both roles; archive/restore owner-only) and ADR 0010 (the manual ledger: payments never edited
or deleted; void stays and counts nowhere).

**Roles:** reception (no finance, voids, staff or space settings — flag any shown) and owner
(write-off, void, archive/restore — flag any missing or any shown to reception).

**Widths and modes:** desktop **1440** and phone **390** in Arabic light are enough; add English or
dark only where the truth differs (it should not).

### 4b. The desk batch (PR #80, branch `origin/design/desk`) — also in scope

PR #80 (the desk batch) is about to merge, so this review covers its new state too: read the desk
branch's DK pages read-only and its `docs/design/INDEX.md` **section 56 · Batch 6** plus the
**Batch 6 parameters** (full list in the sibling DK scope). Judge the §56 truth where it supersedes
`main` — money-block arithmetic (rounding, cap, received/change/debt), oldest-first renewal
accounting, write-off vs payment, voided-in-handover exclusion, fixed-price one-tap semantics.
Touches outside DK pages are OW cross-references, not reviewed here.

## 5. Your axis: TR — truth to the product, the data and the API

Judge this part through this axis only, deeply:

1. The ledger (ADR 0010, K4): every payment for one visit or one subscription, recorded by hand;
   never edited or deleted; voided stays struck with who/why and counts nowhere — on the file, in
   Payments, in the handover figures, in toasts. Flag any edit, any deletion, any figure that
   counts a voided payment.
2. Write-off vs payment (K6): «لن يُحصَّل» removes the visit from uncollected and debt with a
   required reason, recorded and audited — never a payment, never a deletion. Flag any confusion.
3. Roles (ADR 0009): reception records visits, check-ins/outs and payments, edits customer data,
   renews — but never voids, writes off, archives/restores, or sees Finance/staff/settings; the
   owner does those. Flag any control shown to the wrong role or missing for the right one.
4. Money in view of others (O3's reason): the desk is often open in view of customers — flag
   figures the desk exposes that the model calls private (capacity is private; income totals belong
   in Finance).
5. *Not in v1* (overview.md): no online payment, no QR check-in, no booking, no reviews, no OTP, no
   receipts — flag anything that takes, promises, or implies them. Check-in warnings must be ones
   the model can serve (K5's count-based line, no weekdays).
6. Nothing else on screen the API, the data model or v1 cannot hold: every dialog field exists in
   the contract; the present read is whole only as the K8 exception allows; packages whole per the
   O-batch exception.

**Out of this prompt's axis (leave to the other DK prompts, do not report):** flow length (UX);
visual choices (VD); breakage (DF); removals (EX); wording quality except where words promise
something untrue — that boundary belongs to CP (CP); keyboard and resilience mechanics (AX).

## 6. What is settled — do not report again

- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then
  `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and
  `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_DESK.md` (K1–K8, DK-003–DK-023, with the API/docs
  routings: K8's whole read, K6's write-off, DK-018's keys, the contract §4 exceptions, ADR 0009's
  Revised line, the data-model write-off).
- What these settle is **not reported again**. Where the prototype contradicts the contract, the
  model, or an ADR, report the contradiction precisely (endpoint/field/rule).
- If you believe a settled decision makes the product worse, report it under **Decisions in doubt**
  with why — never as a defect.

## 7. The lens

Follow `REVIEW_LENS.md` §3 (especially A.11 and §2c: against the API contract), §4 (proposals from
the design system's own components and tokens; why it is better; cost S/M/L; pattern-level
proposals name every page they change) and the report shape in section 8 below. Known limits of the
archive (lens §2) are not reported.

## 8. The report

Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-DK-TR_REPORT.md`. English, concise.
In this order:

1. The commit SHAs from section 2 (main and `design/desk`).
2. A one-line verdict.
3. The five most important points, one line each.
4. The issues, most important first, one block each: **ID** (`R2-DK-TR-001`…), title,
   **type** (defect | improvement), **level** (design system | pattern | component | page),
   **impact** (high | medium | low, for the user), **where** (frame label from INDEX.md — on main
   or §56 on the desk branch — prototype URL with parameters on your local server, width and mode,
   screenshot path in `docs/design/screens/`), **evidence** (the capture's path), what is wrong /
   what could be better, **proposal**, **why** it is better, **cost** (S/M/L),
   **rule** (the document and section it applies or puts in doubt, if any).
5. Decisions in doubt (if any).
6. What was not reviewed and why.

## 9. Cap

At most 25 issues, the most important first. No praise. One issue per problem.
