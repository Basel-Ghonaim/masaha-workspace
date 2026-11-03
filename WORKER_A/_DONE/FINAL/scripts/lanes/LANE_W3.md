# Lane W3 — U7 then U8: the front desk, the subscription sheet, customers, the file, payments

Read `LANE_COMMON.md` and `LANE_W_COMMON.md` (same folder) first and follow them; this file adds your lane's facts.

- **Worktree** `C:\dev\masaha\app-lane-w3`, **branch** `lane/w3`, **base** `56e639c6` (U0 + the lanes joined: lane L (U3, all ten commits and finding 204)).
- **Scripts folder:** `C:\dev\masaha\workspace\WORKER_A\FINAL\scripts\lane-w3\`. **Finding numbers:** 212–213.
- **The plan's parts for you** (`2_PLAN.md` lines): §5.7 **1494–1608** (D7.1–D7.14) and §5.8 **1610–1672**
  (D8.1–D8.7); §8 U7, U8 **2119–2131**; §9.1 U7, U8 **2257–2280** (C7.1–C7.14, then C8.1–C8.7); §10.4 T200–T244
  (**2591–2631**); §12.1 U7, U8 **2804–2805**; §4.1's rows 13–17 and GX.1 (**311–356**); §7's rows for 160, 162, 163,
  164, 166, 171, 172 (**1947–2018**); DI10–DI13, DI19, DI23–DI25, DI32 (**1874–1943**); S6; EC10, EC16, EC24
  (2871–2929). Read `docs/features/{desk,visits,subscriptions,customers,payments,occupancy}.md` and the contract's
  *Front desk*, *Customers*, *Subscriptions*, *Occupancy* first. Lessons of the desk's earlier runs are in the code
  (`features/desk`): follow its keys (`useIntentKey`), its dialogs' focus rules, its 429 handling.
- **Your files:** §8 U7, U8 (2119–2131). Both units live in `features/desk`: U7's folders and copy sub-objects
  (`desk.ts`: `page`, `log`, `writtenOff`, `sheet`, `visit`, `checkOut`), U8's (`customers`, `file`, `actions`,
  `correct`), `features/occupancy` (EC24), `features/payments` (ledger, mine), `features/spaces/hooks/owners`
  (`useSpaceOwners`, 166), the pages `pages/dashboard/space/{desk/DeskPage,SubscriptionSheetSlot,
  customers/CustomersPage,customers/CustomerPage,payments/PaymentsPage}.tsx`, copy `{desk,occupancy,payments}.ts`.
- **Order:** U7's C7.1 first (its red test), then the rest of U7, then U8 — except where a commit waits.
- **What each commit needs from other lanes** (build those whose needs are in your base first):
  - C7.1, C7.6, C7.9, C7.14 — none. C7.2 — L's C3.5 (range) and the visits/check-ins reads on `main` (#131).
    C7.3 — A2's C2.10 (`GET …/written-off-visits`). C7.4 — A2's C2.7 (`customerId`). C7.5 — A2's C2.8 (and U0's
    `PUBLISHED_PRICE_CHANGED`, in your base). C7.7 — A2's C2.13 (`audience`). C7.8 — A2's C2.13 (`current.progress`).
    C7.10 — none. C7.11 — L's C3.4 (`Input size="lg"`). C7.12 — none (the check-out's answer). C7.13 — L's C3.5 if a
    list; the `DatePicker` is the layer's (`@shared/design-system/calendar`).
  - C8.1 — none (the file's and the list's reads on `main`). C8.2 — A2's C2.12 (`reminderTemplate`) and L's C3.10
    (`fillReminder`, `whatsappLink`). C8.3 — A2's C2.9 (`recordedBy`, `voided.by`). C8.4 — none (routes on `main`;
    the layer's `held` from L's C3.3 for the ended item). C8.5 — A2's C2.11 (`WEEK`/`MONTH`). C8.6 — L's C3.5,
    C3.6. C8.7 — A2's EC10 answer (`owners` on `GET /manage/spaces/:spaceId`; lane A2's reply says it — the lead
    passes it on).
- Reply DONE when all 21 commits are made and the lane-wide checks are green.
