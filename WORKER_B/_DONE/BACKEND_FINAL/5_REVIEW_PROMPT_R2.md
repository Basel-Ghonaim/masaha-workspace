# Review of #131 — R2: the finance

Read this file, then `C:\dev\masaha\workspace\WORKER_B\BACKEND_FINAL\5_REVIEW_PROMPT_COMMON.md` whole, and do it.
Your report: `6_REVIEW_R2_CLAUDE_CODE.md`. **Head: `c41a5397`.** New findings, if any: **193–195**.

**Your range:** `6d563549..53c6a7e3` — 3 commits: `feat(finance): read a space's income`, `feat(finance): read who owes and
who paid`, `feat(finance): read a space's occupancy`. They read the `payments` totals of R1's range (read those at the
head as needed).

**Read in the plan:** §2.1 and §2.2 (the finance's binding decisions: income = cash collected without voids; Gaza
months and fixed windows, no free range; the server aggregates; CSV built by the web, no export route; finance the
owner's alone; occupancy from closed stays, auto check-outs included; …); §3.1; §4.1 (the re-verified corrections);
§5.1–§5.3 (routes, shapes, windows, aggregates, occupancy, service); §5.6 S2, S3; §9.3; §9.7; §9.8; §10's finance cases.

**Look hardest at (money):**
- **Income:** cash collected in the window, voided payments out, by Gaza month and the fixed windows only; the
  comparison with the month before; subscriptions vs visits split exactly; nothing double-counted (a renewal's payment
  allocated over old debts — counted once, in the window it was collected).
- **Debts and payers:** the debtors include **archived customers** (Q2, as the plan corrected); each balance by
  `payments`' one rule; the totals equal the pages' sums; paging bounded (the web builds the CSV from pages — DI7).
- **Occupancy:** from closed stays, auto check-outs included; the peak hour and the averages in Gaza time; whole
  minutes.
- **One snapshot (S3):** the income and the debts read from one consistent snapshot where the plan says; no read on
  another pool connection inside a transaction.
- **Authorization:** the owner only (`finance.read`); reception 403 before anything is read; a stranger and the admin
  `not_found`.
- **Cost:** the queries on a busy space's year (the plan's §5.3 bounds); indexes used or a finding.
- Tests and breaks (§9.3) — would each fail?; documents (contract *Finance*, data model, conventions R7, security,
  `finance.md` new) true to the code.
