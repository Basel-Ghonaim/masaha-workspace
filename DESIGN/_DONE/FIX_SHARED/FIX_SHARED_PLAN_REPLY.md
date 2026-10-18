# Design fix 1 — reply to your plan

A careful plan: the bundle's dead classes, the parse and class checks, the before-shots from the
clean tree, the reclassification under P9 — all right. **Approved**, with **six amendments to the
shared decisions** (the owner settled them after the five other reviews, while you planned — read the
two *Amended* notes at the head of `DECISIONS_SHARED.md`) and the answers below. **Save the plan
first** (as amended) to `C:\Users\basel\.prompt\MASAHA_DESIGN\PLAN\FIX_SHARED_PLAN.md` — `PLAN\` is
still empty — then cut the branch and build.

## 1. Six amendments
- **P1 narrowed.** The phone's fixed bottom bar holds **only the desk's «تسجيل زيارة»**. **The owner's
  overview has no bottom bar** (the desk is in the navigation). A **list's "add"** (Customers, Staff,
  Announcements, Admin spaces, owners, users…) sits in **a row above the list, at its end, at every
  width** — so **`AdminShell` does not gain a `bottomAction`**, and the per-page `md:hidden` copies
  become that one row. Secondary page actions (CSV export) go in the top bar's «⋯». The title in the
  top bar and the sub-pages as you planned.
- **P8's exception.** An action whose result **shows in the row it changed** (a switch, a reorder)
  raises **no success toast**; only its failure is announced — leave those call sites out of
  `useAction`'s toast (keep the pending state). **But not at the front desk:** check-in and check-out
  keep their success toast, and every money action one with its amount.
- **P5's Directory exception.** The Directory **keeps its filter sidebar from `lg` and the sheet below
  `lg`**, and takes the rest of P5 (labelled fields, the count badge, the footer, the count by the
  toolbar). Its bespoke sheet still merges into the shared `FilterSheet`; only its breakpoint stays.
- **P9 — archiving a customer is two cases:** a settled customer is archived at once with «تراجع» (no
  dialog); a customer who owes gets an `AlertDialog` naming the debt, with no undo.
- **P9 — "sign out of all devices" is dropped from v1** (batch 4): don't build its dialog; leave the
  Settings button as it is — batch 4 removes it.
- **The other batches' page changes are not this item** (§4): only batch 1's patterns and issues,
  with these amendments.

## 2. Your decisions (§13)
1. **The bar's title stays `text-heading-3`;** record the §7 tension in the report's rules in doubt.
   Approved.
2. **The §9 wording note** (cards *or* column priority): approved; the analyst passes it to worker A.
3. **`?status=open` → `?publicstate=open`:** approved, with `INDEX.md` and the board.
4. **`?override=<minutes>` parses as `full:<n>`,** and README's *Known limits* drops that line:
   approved.
5. **SH-020 at the root** (one scoped `color: inherit` rule): approved.
6. **DI-2** (the two dead classes in the shells), **DI-4** (one discard label), **DI-5**
   (`Error.html`'s toaster), **DI-6** (the templates on the vendored Babel), **DI-7** (`Money`'s
   nowrap): all folded. **DI-3** goes to the public batch (recorded in `DECISIONS_PUBLIC.md`).

## 3. Corrections
- **Commit type:** `design` is not one of workflow §3's types. Use **`docs(design): …`**, each subject
  ≤ 50 characters — count them; the plan's first is 63.
- **The link check exists now:** run **`npm run check:links`** on your head instead of the check by
  hand (it covers `docs/design/README.md`, `CHANGES.md` and `INDEX.md`; not the prototype's HTML).
- **A new port:** serve the prototype on **5346**, not 5343. Check it is free before you start and at
  the end.

## 4. Noted for later, not this item
- Committing your Babel-parse and class-check scripts under `scripts/` for the next design fixes: a
  separate small Work Item; the analyst will propose it.
- The other five batches' decisions (`DECISIONS_ADMIN`, `_PUBLIC`, `_ACCOUNT`, `_OWNER`, `_DESK`) are
  **the next items**, one or two batches per item — not this one.

The review: the PR is about 49 files, so the owner decides at your report whether it gets a separate
review conversation or the analyst's. Don't merge.
