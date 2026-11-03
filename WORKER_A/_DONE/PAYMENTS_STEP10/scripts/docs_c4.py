"""Commit 4's document lines: payments.md («دفعاتي اليوم»), architecture §2, overview, finding 162's evidence."""
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
    (
        "the payments list and the uncollected visits; on the web, the owner's «الدفعات».",
        "the payments list and the uncollected visits; on the web, the owner's «الدفعات» and reception's «دفعاتي اليوم».",
    ),
    (
        "the web feature `features/payments`, dashboard-only: the owner's ledger.",
        "the web feature `features/payments`, dashboard-only: the owner's ledger and reception's «دفعاتي اليوم».",
    ),
    (
        f"On the dashboard, the owner reads «الدفعات» (`/dashboard/spaces/:spaceId/payments`, {DATE}, #PRNUM).",
        f"On the dashboard, the owner reads «الدفعات» (`/dashboard/spaces/:spaceId/payments`) and reception «دفعاتي اليوم» (`…/my-payments`, {DATE}, #PRNUM).",
    ),
    (
        "\n## Decisions\n",
        "\n**«دفعاتي اليوم» on the web** (reception's, `pages/dashboard/space/payments/MyPaymentsPage.tsx`). It reads `GET …/payments` with no range and no `recordedById` — the server answers reception's own payments of today — voided ones included, the page in the address (`?page=`). What it is for and today's date first; then the handover's figures, every one the answer's `meta.totals`: «نقدًا للتسليم» first, «تحويل» with «وصلت إلى حساب المساحة» under it, «المجموع» with how many — one card of three rows below 768 px, three stat cards from it; then «خطأ في دفعة؟ يلغيها صاحب المساحة، وتظهر هنا مشطوبة.»; then the payments — from 768 px a table of the time, the name, what it paid, the method (cash `neutral`, a transfer `info`) and the amount, a card each below it. A voided payment is struck through, with «ملغاة» and «ألغاها {name}: {reason}», and counts in no figure. Its states: loading, a failure with its reference and a retry, a failed refresh over the rows, «لم تسجّل أي دفعة اليوم».\n\n## Decisions\n",
    ),
    (
        f"- **Every figure is the server's** (DI-11): agorot end to end; the totals are `meta.totals`, never a sum of a page. {DATE}, #PRNUM.\n",
        f"- **Every figure is the server's** (DI-11): agorot end to end; the ledger's totals and «دفعاتي اليوم»'s handover are `meta.totals`, never a sum of a page; the cash to hand over comes first. {DATE}, #PRNUM.\n"
        f"- **«دفعاتي اليوم» keeps the transfer's helper on a phone** (DI-10): «وصلت إلى حساب المساحة» under the transfer in the one card, as under its stat card. {DATE}, #PRNUM.\n"
        f"- **Reception's list sends no range and no `recordedById`** (S5): the server answers reception's own of today and refuses either (403). {DATE}, #PRNUM.\n",
    ),
    (
        "entry `index.ts` (`PaymentsLedger`, `LedgerRowAction`, `LedgerPerson`, `LedgerPayment`), read by `pages/dashboard/space/payments/PaymentsPage.tsx`,",
        "entry `index.ts` (`PaymentsLedger`, `LedgerRowAction`, `LedgerPerson`, `LedgerPayment`, `MyPaymentsToday`), read by `pages/dashboard/space/payments/` — `PaymentsPage.tsx`,",
    ),
    (
        "in the rows and [staff](space-links.md)'s `useStaffPeople` in the staff filter: the repository in `repository/`; the keys, the ledger's filters in the address and its view (`ledger/`),",
        "in the rows and [staff](space-links.md)'s `useStaffPeople` in the staff filter, and `MyPaymentsPage.tsx`: the repository in `repository/`; the keys, the ledger's filters in the address and its view (`ledger/`), «دفعاتي اليوم»'s (`mine/`),",
    ),
    (
        "the ledger, its filters and its totals (`ledger/`) and a payment's amount in `components/`.",
        "the ledger, its filters and its totals (`ledger/`), «دفعاتي اليوم» and its handover figures (`mine/`) and a payment's amount in `components/`.",
    ),
    (
        "the voided payments shown on demand, and [desk](desk.md)'s void in each row.\n",
        "the voided payments shown on demand, and [desk](desk.md)'s void in each row; «دفعاتي اليوم», reception's own payments of today and the handover's figures.\n",
    ),
])

edit(DOCS / "frontend/architecture.md", [
    (
        f"and [staff](../features/space-links.md)'s reception accounts in its staff filter ({DATE}, #PRNUM), each space page",
        f"and [staff](../features/space-links.md)'s reception accounts in its staff filter, and «دفعاتي اليوم», reception's own payments of today with the handover's figures ({DATE}, #PRNUM), each space page",
    ),
])

edit(DOCS / "project/overview.md", [
    (
        "on the dashboard, the owner's ledger with its filters and totals, and the void from it and from a subscription's statement.",
        "on the dashboard, the owner's ledger with its filters and totals, and the void from it and from a subscription's statement, and reception's «دفعاتي اليوم».",
    ),
])

edit(DOCS / "architecture/findings/162-no-route-names-a-spaces-staff-to-reception.md", [
    (
        "the file's statement (#122) shows neither, for either role.\n",
        "the file's statement (#122) shows neither, for either role. #PRNUM: «دفعاتي اليوم» names who voided reception's own payment (`PaymentRow.voided.by`); the statement still names neither.\n",
    ),
])
print("docs c4 ok")
