# Review — PR #64, its two added commits (no price of zero, in the code and the database)

You are an **independent reviewer** of the two commits added to PR #64 after its first review (which
found nothing, on `b7397dc`). Write your report to
`C:\Users\basel\.prompt\MASAHA_AMENITIES\REPORT\REVIEW64B_<YOU>_REPORT.md`, where `<YOU>` is your
tool's name in capitals (`OPENCODE`, `CODEX`, `COPILOT`, `CLAUDE`).

## Rules

- **Run from `C:\Users\basel\masaha`**, but **read only commit objects** (that folder's working tree
  is on another PR's branch). No edits, commits, checkouts, switches, installs, npm or test runs,
  database or Docker commands, no GitHub comments. `git fetch origin`, then pin to **the PR's current
  head** (`gh pr view 64 --json headRefOid`, expected `2e4aa4d`; written at the top of your report and
  checked again at the end). **Review only `b7397dc..<head>`**: `git diff b7397dc <head>`,
  `git show <head>:<file>`.
- **Report concrete problems only,** each verified in the code: file and line, the failing scenario,
  the severity (**blocker / should-fix / nit**) and the fix. No praise, no summary. If unsure, say
  "plausible" and why.
- **No tool attribution** in what you write.

## What the two commits must be (the owner's decisions, 2026-10-12)

**No free price:** every price of a space is above zero; a free event belongs in the announcements.
- **`ec2139d feat(spaces): refuse a price of zero`:** `amountAgorot` in
  `packages/shared/src/spaces/requests.ts` an integer from **1** to `PRICE_MAX_AGOROT`; 0 refused on
  `prices.<i>.amountAgorot` with `out_of_range` (the shared vocabulary's code for a number outside its
  bounds, as a negative price already gets); a shared unit test and an API prices test (nothing
  written on refusal); the contract's prices line (1 to 10,000,000); `spaces.md` › *API decisions*.
- **`2e4aa4d feat(db): refuse a zero price in the database`:** a hand-written migration
  (`20261012144622_space_price_above_zero`; Prisma does not model check constraints) dropping
  `space_prices_amount_check` and adding it back as `"amount_agorot" > 0`; **no other table changes**
  (the desk's packages, subscriptions and visits keep `>= 0` on purpose: their steps decide); an API
  test inserting 0 straight through Prisma, refused by the database; `data-model.md` › *Prices*.

## Look at these

1. **The migration:** correct SQL; the constraint's name matches the one the init migration created;
   its timestamp sorts after every earlier migration; it fails safely on a database holding a 0 price
   (none exists — say what would happen); nothing else altered.
2. **The rule:** both apps run the same shared rule; no other path writes a price around it (the
   prices service, the seed, any test fixture with 0).
3. **The tests:** each would fail if its code broke (the database test against the old `>= 0`, the
   shared and API tests against `min(0)`); expectations by hand.
4. **The documents:** the contract, `spaces.md` and `data-model.md` each state it once, truly.
5. **The commits:** count each subject (≤ 50); the PR description names both.

## Your output

One file (the path above): a one-line verdict; the findings, most severe first (severity, file:line,
scenario, fix); a short "Checked and fine" list; then stop.
