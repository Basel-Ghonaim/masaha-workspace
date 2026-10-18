# Design review 6 — the front desk

**The design-review-desk worker** (a one-off reviewer, named after its task). **Read-only:** you
write nothing in the repository, run no git command that changes anything, and touch no worker's
folder.

**Size cap:** at most 1 subagent, no workflow; the whole review under 500,000 tokens. Two other
reviews and a building worker run beside you, so keep the load light.
**Report:** `C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\REVIEW_DESK_REPORT.md`.
**Evidence images:** `C:\Users\basel\Downloads\design-review-desk\` (create it).

## 1. The task in brief

The last of six design reviews. The shared layer, the admin's dashboard and the public site are
reviewed and **decided**. This review takes **the front desk and what hangs from it**: the screens
that reception and the owner use all day, at speed, with customers waiting, often on a phone. Look at
what each page is for, its sections and components, its flows and states, and the better design for
each. Speed and error-proofing come first: the fewest taps for a check-in, a check-out with payment,
and a subscription; no money mistake that cannot be seen and voided.

## 2. Read first

1. **The lens:** `C:\Users\basel\.prompt\MASAHA_DESIGN\REVIEW_LENS.md`. It sets your method and the
   report's shape; follow it exactly.
2. **What is settled:** `C:\Users\basel\.prompt\MASAHA_DESIGN\DECISIONS_SHARED.md` (read its amended
   head: P1's bottom bar is for the desk's «تسجيل زيارة»), `DECISIONS_ADMIN.md` and
   `DECISIONS_PUBLIC.md`. Don't report any of it again (lens §2b).
3. The design's guides:
   - `docs/design/README.md`;
   - `docs/design/SCREENS.md`, rows 13–17;
   - `docs/design/INDEX.md`;
   - `docs/design/prototype/BRIEF.md`.
4. The product's documents:
   - `docs/frontend/design-system/foundation.md` §5, §7–§10, §12, §13 (*Owner and reception
     dashboard* › the front desk);
   - `docs/project/overview.md` (the dashboard's v1 scope, *Not in v1*: no online payment, no QR
     check-in); `docs/project/glossary.md`;
   - ADRs 0008 (live status), 0009 (what reception may do), 0010 (the manual, append-only ledger)
     and 0015 (idempotency: a payment is never recorded twice);
   - `docs/architecture/data-model.md` › *Entities* › *Operations*, and *Derived values* › *Front desk
     and money* and *Subscription scenarios* (the visit's price, auto check-out);
   - `docs/plans/v1-mvp.md`, steps 7–8 and *Planned API surface* › the desk's and payments' rows.
5. The prototype's source: `masaha/desk-core.jsx`, `desk-sheet.jsx`, `desk-data.js`, and
   `Desk.html` (its `?dialog=` states), `Customers.html`, `Customer file.html`, `Payments.html`,
   `My payments.html`.

## 3. Your scope

The screens and their frames:
- **13 Front desk:** check in, check out with payment, the override, the uncollected;
- **14 Customers**;
- **15 Customer details:** subscriptions, statement, payments;
- **16 New or renew a subscription:** the sheet;
- **17 Payments:** the owner's, all with void; reception's «دفعاتي اليوم».

Board sections **20–28**, **31–32**, and the desk's variants of **41** and **50–52**. Show where the
owner's view and reception's differ, and whether each difference is right.

**Issue IDs:** `DK-001`, `DK-002`, …

## 4. How to look

- **Serve a copy, never the repository's folder.** Extract the archive from `origin/main` to a short
  path and serve it on **port 5345**:
  `git archive origin/main docs/design | tar -x -C C:\Users\basel\design-review-desk` (create the
  folder), then serve `C:\Users\basel\design-review-desk\docs\design\prototype` on 5345.
- Look at every page in Arabic and English, light and dark, at 390, 768 and 1440, and with the
  keyboard. Take evidence with headless Chrome (a script in your scratchpad, never committed).
- Count the taps of each common task on a phone, and say it in the report.
- Read the source of each page, so a proposal names what really changes.
- At the end: stop the server, delete `C:\Users\basel\design-review-desk`, and check port 5345 is
  free.

## 5. Risks

- **Writing anything** in the repository or in `masaha` or `masaha-b`: other workers are building
  there.
- **Reporting settled decisions** again, or the archive's known limits.
- **A proposal outside the design system:** a colour, size or font outside its tokens.
- **A proposal against a product rule:**
  - an occupancy count made public;
  - a payment edited or deleted rather than voided;
  - online payment or QR check-in;
  - reception given the owner's rights.
- **A design the API cannot serve** (lens §2c).
- **Many small items, no big picture:** lead with the *Patterns* (the desk's speed and its money
  safety), then the front desk's structure.

## 6. When you finish

Save the report. Summarise it here in ten lines at most: the five most important points, the counts
by level and impact, and the tap counts before and after your proposals. Change nothing else.
