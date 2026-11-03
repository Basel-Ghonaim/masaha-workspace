"""Commit 3's document lines: payments.md (the ledger on the web), space-links.md, architecture §2, overview, findings 165 and 166."""
from pathlib import Path

DOCS = Path("C:/dev/masaha/app/docs")
DATE = "2026-10-27"


def edit(path, pairs):
    text = path.read_text(encoding="utf-8")
    for old, new in pairs:
        assert text.count(old) == 1, (path.name, old[:70], text.count(old))
        text = text.replace(old, new)
    path.write_bytes(text.encode("utf-8"))


edit(DOCS / "features/payments.md", [
    ("**Last Updated:** 2026-10-24", f"**Last Updated:** {DATE}"),
    (
        "the payments list and the uncollected visits; no web screen yet.",
        "the payments list and the uncollected visits; on the web, the owner's «الدفعات».",
    ),
    (
        "> **Scope:** the API module `payments` (L4); `@masaha/shared/payments`. No web feature yet.",
        "> **Scope:** the API module `payments` (L4); `@masaha/shared/payments`; the web feature `features/payments`, dashboard-only: the owner's ledger.",
    ),
    (
        "- **The space's owner**, whose ledger reads every payment, and **reception**, whose «دفعاتي اليوم» reads its own of today, through its own route. No web screen yet.",
        f"- **The space's owner**, whose ledger reads every payment, and **reception**, whose «دفعاتي اليوم» reads its own of today, through its own route. On the dashboard, the owner reads «الدفعات» (`/dashboard/spaces/:spaceId/payments`, {DATE}, #PRNUM).",
    ),
    (
        "\n## Decisions\n",
        "\n**The ledger on the web** (`features/payments`, composed by `pages/dashboard/space/payments/`). «الدفعات», the owner's, lists `GET …/payments` 20 a page, the latest received first: from 768 px a table of five columns — the day (`اليوم`, `أمس`, else the date) with the time under it on Gaza's clock; the customer, a link to their file, or the visitor's name (else «زائر»), with the item under it («زيارة» or the subscription's name); the amount with its method under it; who recorded it; the row's action — and below it a card each. Its filters, every one in the address with the page (`?from=&to=&staff=&method=&kind=&voided=1&page=`), each read by the contract's rule so a value the server would refuse falls back: the period (a range of Gaza dates on a calendar, both ends or neither, at most 92 days — a longer one is not applied and says «أطول فترة 92 يومًا؛ اختر فترة أقصر.»; «اليوم» by default), the staff member (the owner signed in, «{name} (أنت)», then the space's reception accounts, a deactivated one «{name} · موقوف»), the method and the kind; inline from 768 px, in a bottom sheet below it whose button counts what applies, the period included; «إظهار الملغاة» on every width, hidden by default; «مسح الفلاتر» while any applies, which takes off every one. The totals line starts with its period («اليوم», «21 أكتوبر 2026», «1–21 أكتوبر 2026») and says the answer's `meta.totals` — the total received, by cash, by transfer, how many — and the voided ones apart; no figure is a sum of the rows. A voided payment, when shown, is struck through, with «ملغاة» and «ألغاها {name}: {reason}». Its states: loading, a failure with its reference and a retry, a failed refresh over the rows shown, «لا توجد دفعات اليوم», and a filter that matches nothing, with «مسح الفلاتر». Each row of a payment not voided ends with [desk](desk.md)'s void, the page's; when the row whose action has the focus leaves, the next row's action takes it, else the totals line.\n\n## Decisions\n",
    ),
    (
        "\n## Code map\n",
        "\n### Web decisions\n\n"
        f"- **The list is `payments`', the void `desk`'s** (S1): the ledger calls `GET …/payments`; the void is the desk module's route, so the page sets [desk](desk.md)'s «⋯» in the ledger's row slot. *Why:* each capability's web feature calls its own module's routes (architecture §3). {DATE}, #PRNUM.\n"
        f"- **Every filter and the page in the address** (S8, DI-5): a value the server would refuse falls back; half a range, an inverted one or one past 92 days is dropped whole; a change replaces the address and returns to page 1; no default is written. {DATE}, #PRNUM.\n"
        f"- **No CSV export here** (DI-1): it would export a page's rows, not the ledger, and the income's export is Finance's (step 11). {DATE}, #PRNUM.\n"
        f"- **The period is said, and counted** (DI-2): the totals line starts with it, and the phone's filters button counts a range when one is set. {DATE}, #PRNUM.\n"
        f"- **«مسح الفلاتر» on every width, clearing every filter** (DI-3): the range and «إظهار الملغاة» included; the no-match state offers it too. {DATE}, #PRNUM.\n"
        f"- **The staff filter names real people** (DI-4): the owner signed in and the space's reception accounts from [staff](space-links.md) (`useStaffPeople`, the staff list's one cache), a deactivated one marked; a space's other owners cannot be named ([finding 166](../architecture/findings/166-the-ledgers-staff-filter-cannot-name-a-spaces-other-owners.md)). {DATE}, #PRNUM.\n"
        f"- **A voided payment is never told by a strike alone** (DI-6): «ملغاة» and «ألغاها {{name}}: {{reason}}» beside it; hidden by default; never counted as received. {DATE}, #PRNUM.\n"
        f"- **A customer's name links to their file** (DI-13), the page's link; a visit with no customer shows the visitor's name as text, «زائر» with none. {DATE}, #PRNUM.\n"
        f"- **Every figure is the server's** (DI-11): agorot end to end; the totals are `meta.totals`, never a sum of a page. {DATE}, #PRNUM.\n"
        "\n## Code map\n",
    ),
    (
        "the responses (`VisitPayment`, `UncollectedVisit`, `PaymentRow`, `PaymentItem`, `PaymentTotals`, `PaymentsMeta`).\n",
        "the responses (`VisitPayment`, `UncollectedVisit`, `PaymentRow`, `PaymentItem`, `PaymentTotals`, `PaymentsMeta`).\n"
        "- **Web:** `apps/web/src/features/payments/`, entry `index.ts` (`PaymentsLedger`, `LedgerRowAction`, `LedgerPerson`, `LedgerPayment`), read by `pages/dashboard/space/payments/PaymentsPage.tsx`, which sets [desk](desk.md)'s `VoidPaymentAction` in the rows and [staff](space-links.md)'s `useStaffPeople` in the staff filter: the repository in `repository/`; the keys, the ledger's filters in the address and its view (`ledger/`), and the focus kept when a row leaves (`useFocusAfterLeave`) in `hooks/`; the address's query (`ledgerQueryOf`), the period's words (`periodText`) and a row's (`paymentRowView`) in `services/`; the ledger, its filters and its totals (`ledger/`) and a payment's amount in `components/`. Words: the catalogue's `payments` section; the methods are `desk`'s.\n",
    ),
    (
        "- #114 — the owner's void of a payment,",
        "- #114 — the owner's void of a payment,",
    ),
])

text = (DOCS / "features/payments.md").read_text(encoding="utf-8")
assert text.endswith("\n")
text += f"\n### Web history\n\n- #PRNUM — «الدفعات», the owner's ledger: its filters in the address, the totals of the whole filter, the voided payments shown on demand, and [desk](desk.md)'s void in each row.\n"
(DOCS / "features/payments.md").write_bytes(text.encode("utf-8"))

edit(DOCS / "features/space-links.md", [
    (
        "- **A space's owner,** on the dashboard's «الموظفون» (`/dashboard/spaces/:spaceId/staff`), through `features/staff`: their reception accounts.",
        f"- **A space's owner,** on the dashboard's «الموظفون» (`/dashboard/spaces/:spaceId/staff`), through `features/staff`: their reception accounts. The ledger's staff filter reads the reception accounts' names on the web (`useStaffPeople`, the same list's one cache; [payments](payments.md), {DATE}, #PRNUM).",
    ),
])

edit(DOCS / "frontend/architecture.md", [
    (
        "its path in `navigation.ts` but not in the sidebar (2026-10-25, #122), each space page",
        f"its path in `navigation.ts` but not in the sidebar (2026-10-25, #122), «الدفعات», the owner's ledger of [payments](../features/payments.md) with [desk](../features/desk.md)'s void in each row and [staff](../features/space-links.md)'s reception accounts in its staff filter ({DATE}, #PRNUM), each space page",
    ),
])

edit(DOCS / "project/overview.md", [
    (
        "and reception's own of today; the uncollected visits.",
        "and reception's own of today; the uncollected visits; on the dashboard, the owner's ledger with its filters and totals, and the void from it and from a subscription's statement.",
    ),
])

FINDINGS = DOCS / "architecture/findings"
(FINDINGS / "165-the-dashboards-navigation-is-not-grouped-by-task.md").write_bytes(
    (
        "# 165. The dashboard's navigation is not grouped by task\n\n"
        f"**Status:** Open · **Date:** {DATE}\n\n"
        "**Evidence:** the settled prototypes group the space's sidebar by task (P3: the day's work — the desk, the customers, the payments —, the space's offer, its page, its team and settings), and the admin's likewise. The shell's `DashboardNavigation` draws one flat `SidebarGroup` from `SPACE_NAV` and `ADMIN_NAV`, which hold no group; the owner's eleven pages read as one list. PAYMENTS_STEP10 (#PRNUM) fills four of those pages and leaves the list flat (its A4, not taken): grouping it touches every dashboard page's shell and its slow routes test (finding 87).\n\n"
        "**Resolves when:** `SPACE_NAV` and `ADMIN_NAV` carry each item's group and the sidebar draws the groups with their labels (hidden on the rail), in an item of its own; or the owner keeps the flat list.\n"
    ).encode("utf-8")
)
(FINDINGS / "166-the-ledgers-staff-filter-cannot-name-a-spaces-other-owners.md").write_bytes(
    (
        "# 166. The ledger's staff filter cannot name a space's other owners\n\n"
        f"**Status:** Open · **Date:** {DATE}\n\n"
        "**Evidence:** «الدفعات»'s staff filter (#PRNUM) offers the owner signed in and the space's reception accounts (`GET …/staff`, reception links only). A space may have more than one owner (ADR 0009), and no route names a space's owners to an owner, so a payment another owner recorded can be read in the rows («سجّلها» names them) but not chosen in the filter.\n\n"
        "**Resolves when:** a managed route names a space's owners to its owners (or the staff list includes them, marked), and the filter offers them; or the owner accepts the rows' names as enough.\n"
    ).encode("utf-8")
)
edit(FINDINGS / "README.md", [
    (
        "- [164. A written-off visit is listed nowhere](164-a-written-off-visit-is-listed-nowhere.md)\n",
        "- [164. A written-off visit is listed nowhere](164-a-written-off-visit-is-listed-nowhere.md)\n"
        "- [165. The dashboard's navigation is not grouped by task](165-the-dashboards-navigation-is-not-grouped-by-task.md)\n"
        "- [166. The ledger's staff filter cannot name a space's other owners](166-the-ledgers-staff-filter-cannot-name-a-spaces-other-owners.md)\n",
    ),
])
print("docs c3 ok")
