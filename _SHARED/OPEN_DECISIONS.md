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
   owner's. *Settle in: the announcements item.*
3. **Every customer's phone number:** needed at the desk. → No export and no whole list for reception;
   search and pages only. *Settle in: step 8 (customers).*
4. **A shared desk device:** a payment may be recorded under another receptionist's session, spoiling
   «each staff member's collections». → A short idle sign-out for reception accounts and a visible
   «تبديل الموظف». *Settle in: the desk's screen item (worker A) — the owner's decision, 2026-10-20: it is a web
   behaviour; DESK PR 4 records payments without it.*
