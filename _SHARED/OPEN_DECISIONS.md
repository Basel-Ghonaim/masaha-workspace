# Open decisions — settled in principle, built later

Each line: what, the owner's leaning (2026-10-18), and the item that must settle it in its plan.

## Reception's permissions (for the desk steps 7–9)

1. **A price typed by hand at the desk** (a custom subscription's price, a visit's charge) — **settled
   (#92, 2026-10-19):** the space setting «السماح للاستقبال بالأسعار اليدوية» is stored
   (`receptionMayTypePrices`, **off by default**, every existing space included); the owner always may; **every
   hand-typed price, the owner's included, carries a required reason**, recorded with who typed it (data model
   › *Front desk and money*, ADR 0009 revised). *Enforced in: step 7 (visits) and step 8 (subscriptions).*
   **Carried to step 7 (Q4, the owner's answer) — built (#95, #97, 2026-10-20):** reception closes the visit
   unpriced (#95); the owner prices it (`PUT …/visits/:visitId/charge`, #97); «يحتاج انتباهك» counts
   `GET …/unpriced-visits` and `GET …/uncollected-visits` (#97) — never closed free.
2. **A closure announcement** turns the space «مغلق الآن» in public. → Reception keeps it (a power cut in
   Gaza needs a decision on the spot), **the owner is notified**; extending subscriptions stays the
   owner's. *Settle in: the announcements item.* **Settled (#112, 2026-10-24):** reception posts a closure;
   the owner learns of it in the app only — the managed list's extension state per closure and the summary's
   `closuresAwaitingExtension`, which the overview (step 12) will read through `subscriptions`'
   `closures.summary`; no email.
3. **Every customer's phone number:** needed at the desk. → No export and no whole list for reception;
   search and pages only. **Settled (#102, 2026-10-21):** a paged, searched list (at most 50 a page) for the
   owner and reception; no export and no whole list for anyone in step 8; an export is the owner's, later, in
   finance. Reception also reads an archived customer's file by id (its debts are collected at the desk —
   the owner's word, 2026-10-21, carried to SUBSCRIPTIONS PR 2).
4. **A shared desk device:** a payment may be recorded under another receptionist's session, spoiling
   «each staff member's collections». → A short idle sign-out for reception accounts and a visible
   «تبديل الموظف». *Settle in: the desk's screen item (worker A) — the owner's decision, 2026-10-20: it is a web
   behaviour; DESK PR 4 records payments without it.* **Revised by the owner, 2026-10-24:** a sign-out in the
   browser alone protects nothing; reception's session ends after **15 minutes idle on the server** (an API
   change, worker B) and the web shows «تبديل الموظف» — both specified in `WORKER_A\DESK_SCREENS\2_PLAN.md`.
   **Built as (#118, 2026-10-25):** the server ends a session of an account whose only active links are
   reception links after 15 minutes with no request other than the desk's polled state; the access token names
   its session (`sid`); every other request renews it (at most one write a minute); an idle session's requests
   answer 401 `SESSION_IDLE` and its refresh deletes it and answers the same, ending only that device's session.
   «تبديل الموظف» is on the desk (#116); the sign-in page's idle line comes with DESK_SCREENS PR 3.
