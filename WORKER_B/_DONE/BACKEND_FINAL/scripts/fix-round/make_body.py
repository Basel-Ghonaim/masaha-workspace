import pathlib, sys
d = pathlib.Path(r"C:\dev\masaha\workspace\WORKER_B\BACKEND_FINAL\scripts\fix-round")
t = (d / "pr-body-before.md").read_text(encoding="utf-8")
old = "Recorded: **158** —"
if t.count(old) != 1: sys.exit("findings line")
t = t.replace(old, "Recorded: **193** — an auto-closed visit left to a customer is both in that customer's debt and in the uncollected count (the review's R2-F1, for the owner's decision); **158** —")
section = """## Review fixes (2026-10-29)

The three reviews (R1 the foundation and the items left, R2 finance, R3 the overviews and the documents): no blocker; every finding fixed, each folded into the commit that made its lines (subjects unchanged, no fix commit).

- **R2-F1 (should-fix) — finance's `owed` and `uncollected` overlap.** The contract (*Finance*), `finance.md` and the `DebtsMeta` comment now say what the code does: the uncollected count is the desk's list, which keeps an auto-closed visit left to a customer, so its rest is also in that customer's debt, and the two figures are never added. Pinned by a test in `debts.api.test.ts` (in `owed`, in `uncollected` and on the desk's list); red by a break that dropped visits with a customer from `uncollectedOf` (`uncollected` 0 ≠ 1), green after. `overview.md` says the overview's consequence (`uncollectedVisits` and `customersOwing` both count such a visit). **Finding 193** recorded for the owner: whether finance's `uncollected` should leave out a visit with a customer (it cannot change the shared count, which AC-O2 keeps equal to the desk's list). → `feat(finance): read who owes and who paid`; `finance.md` → `…occupancy` (its last writer); the overview's lines → `feat(overview): read the owner's overview`.
- **R2-F2** — `finance.md`: income reads 46 windows, not 45. → `feat(finance): read a space's occupancy`.
- **R2-F3** — `todayWindow`, used by a test only, removed; its unit case asserts `dayWindow` of today's date. → `feat(finance): read a space's income`.
- **R3-F1 (should-fix)** — `announcements.md`: `runningTypes` is one query of the running ones, each type kept once by Prisma's `distinct` in memory, not a SQL `DISTINCT` (the code unchanged). → `feat(api): count what the owner's overview shows`.
- **R3-F2** — conventions §9 *Composed reads*: the owner's overview *reads* `closures.summary`. → `feat(overview): read the owner's overview`.
- **R3-F3** — `occupancy.glance`'s `at` is required; its test passes its clock. → `feat(api): count what the owner's overview shows`.
- **R1-F1** — `visits.service.ts`: `terms`'s doc comment back on `terms`. → `feat(visits): list a space's visits by day`.
- **R1-F2** — `payments.md` *Who uses it*: the desk's web sentences back under the front desk bullet (→ `feat(payments): total a space's balances`, carried through the two finance commits that rewrote the Finance bullet); "will count" → "counts" (→ `feat(overview): read the owner's overview`, which built the count).
- **R1-F3** — `apps/api/.env.example`: the seed's WhatsApp is a Palestinian or Israeli number, read by the phone rule in any typed form and stored in its one E.164 form. → `fix(seed): store the contact in its one form`.

On the new head: `lint`, `typecheck`, `test:unit`, `test:api`, `format:check`, `check:links`, `check:conflicts` all pass.

"""
old = "## Left out"
if t.count(old) != 1: sys.exit("left out")
t = t.replace(old, section + old)
(d / "pr-body.md").write_text(t, encoding="utf-8", newline="\n")
