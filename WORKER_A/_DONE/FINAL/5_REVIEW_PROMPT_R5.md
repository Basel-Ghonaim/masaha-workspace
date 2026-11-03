# Review of #132 — R5: the front desk, the customers and the payments

Read this file, then `C:\dev\masaha\workspace\WORKER_A\FINAL\5_REVIEW_PROMPT_COMMON.md` whole, and do it. Your report:
`C:\dev\masaha\workspace\WORKER_A\FINAL\6_REVIEW_R5.md`. New findings, if any: **236–239**.

**Your commits (21):**
- U7 (the desk and the subscription sheet): `f78c1f46 62b90d57 2daa4143 15feecfd ca8bce43 2e572b17 5ed2e8b2 4a591222
  e7d0cd63 001c2501 902dd226 f9be0553`
- U8 (customers, the customer's file, payments): `eaf2f978 3827ee48 84375a56 f631ea57 71bcb39f 5d082659 c0e37ea3
  c60865c0 d41b079f`

**Read in the plan:** §5.7 (U7), §5.8 (U8) and their DIs (desk DI-14 and DI-48 superseded — OD10); §9.1's commits;
§10.4's tests for them; §11's desk and customers cases. The prototypes: `Desk.html`, `Customers.html`,
`Customer file.html`, and the subscription sheet's and payments' pages screens 13–17 name.

**Look hardest at (money and keys):**
- **The price sent (171 (a)):** the sheet sends the published price it showed; a 409 when it changed — worded, the
  sheet re-reading the price and **never charging silently or retrying under a new key**; the amount recorded the
  server's.
- **The written-off visits (164):** listed with reason, who and when; the undo — the owner only, its key, its refusal
  worded, the lists refreshed; the write-off's reason focused first (172).
- **A customer's visit (160):** checked in as their visit (`customerId`), the debt landing on that customer.
- **Renew or subscribe from the desk; correct a subscription from its card (163):** the owner's corrections only where
  the routes allow, each with its reason; money fields in agorot; keys one per intent.
- **The WhatsApp reminder:** the number in E.164, the template's text, no other personal data in the link.
- **Who recorded and voided (162)** on the statement; **the ledger's staff filter naming the space's other owners
  (166)**; the customers' filter by week and month (G14.1, M2's column).
- **The desk's day log beside who is here; a full space counted and the rates shown; the phone's desk ordered; a
  refused payment said to have recorded nothing; a usage subscriber's due at check-out.**
- Roles: reception vs the owner on every action; the server's refusal worded when the UI hides nothing.
- **Every screen of your range complete, no gap** — both languages, dark, 390 / 768 / 1440, empty / loading / error.
