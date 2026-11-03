"""Commit 2's document lines: desk.md (the void on the web) and payments.md (*Who uses it*)."""
from pathlib import Path

DOCS = Path("C:/dev/masaha/app/docs/features")
DATE = "2026-10-27"


def edit(path, pairs):
    text = path.read_text(encoding="utf-8")
    for old, new in pairs:
        assert text.count(old) == 1, (path.name, old[:60], text.count(old))
        text = text.replace(old, new)
    path.write_bytes(text.encode("utf-8"))


edit(DOCS / "desk.md", [
    ("**Last Updated:** 2026-10-26", f"**Last Updated:** {DATE}"),
    (
        "and «الزبائن», the customers list, and a customer's file.\n",
        "«الزبائن», the customers list, and a customer's file; and the owner's void of a payment, in «الدفعات»'s rows and a subscription's statement.\n",
    ),
    (
        "- Voids a payment, as the owner, with a reason; a second void answers it as it is.\n",
        "- Voids a payment, as the owner, with a reason; a second void answers it as it is. On the web, the owner voids one from «الدفعات» ([payments](payments.md)) and from a subscription's statement.\n",
    ),
    (
        "- **«بدون سعر»** lists the visits closed with no charge",
        "- **A payment's void on the web** (the owner's): a payment's «⋯», named «إجراءات الدفعة: {المبلغ} · {الاسم}» (DI-9), holds «إلغاء الدفعة…», destructive; its `AlertDialog` (DI-7) names the amount, who, the day and the method, says «تبقى ظاهرة مشطوبة مع السبب واسمك، ولا تُحسب في الدخل ولا في التسليم. لا يمكن التراجع.» and asks the reason, required, focused first. It is sent once with no key (`POST …/payments/:paymentId/void`): no answer says «لم يصل الرد. أعد المحاولة — إلغاؤها مرة ثانية لا يغيّر شيئًا.»; `VISIT_WRITTEN_OFF` says «لا تُلغى دفعة زيارة شُطب مبلغها.» (DI-12), a 404 that the payment no longer exists, and a 403 that it is no longer open here. Done, the space is read again and the toast names the amount and who. Closed, the focus returns to the «⋯»; once the «⋯» leaves under the focus, the page places it (DI-8): in a statement, on its payments' heading. The payments page sets it in each row of the ledger; a statement's payment not voided offers it to the owner (S10).\n- **«بدون سعر»** lists the visits closed with no charge",
    ),
    (
        "## Code map\n",
        f"- **The void is the desk's on the web, set by the payments page in its rows** (S1): the void is the desk module's route, so `VoidPaymentAction` is `desk`'s, exported, and `payments`' ledger takes it through its row slot. *Why:* each capability's web feature calls its own module's routes (architecture §3). {DATE}, #PRNUM.\n"
        f"- **The void in a statement too** (S10): a statement's payment not voided offers the owner the same «⋯» (DK-016). *Why:* a payment recorded on the wrong subscription is found in its file first. {DATE}, #PRNUM.\n"
        f"- **A written-off visit's payment is not voided** (DI-12): the refusal says so; the write-off's undo lives only in its toast ([finding 164](../architecture/findings/164-a-written-off-visit-is-listed-nowhere.md)). {DATE}, #PRNUM.\n"
        "\n## Code map\n",
    ),
    (
        "`DeskAbilities`, `SheetEntry`, `SheetChoices`, `OpenSheet`), read by `pages/dashboard/space/desk/` and `space/customers/`,",
        "`DeskAbilities`, `SheetEntry`, `SheetChoices`, `OpenSheet`, `VoidPaymentAction`, `VoidTarget`), read by `pages/dashboard/space/desk/`, `space/customers/` and `space/payments/`,",
    ),
    (
        "a subscription's statement and its end, and the subscription sheet, its form and its two writes (`sheet/`: `useSubscriptionSheet`, `useSheetForm`, `useCreateCustomer`, `useSubscribe`) in `hooks/`;",
        "a subscription's statement and its end, the subscription sheet, its form and its two writes (`sheet/`: `useSubscriptionSheet`, `useSheetForm`, `useCreateCustomer`, `useSubscribe`), and a payment's void (`void/`: `useVoidPayment`, `useVoidDialog`) in `hooks/`;",
    ),
    (
        "and the sheet (`sheet/`: `SubscriptionSheet`, `PackageOptions`, `CustomTerms`, `PriorDebts`) in `components/`.",
        "the sheet (`sheet/`: `SubscriptionSheet`, `PackageOptions`, `CustomTerms`, `PriorDebts`), and a payment's «⋯» and its dialog (`void/`: `VoidPaymentAction`, `VoidDialog`) in `components/`.",
    ),
    (
        "Carried from #122: the focus back on «⋯» after the edit and the archive's question; an unchanged phone typed locally not sent.\n",
        "Carried from #122: the focus back on «⋯» after the edit and the archive's question; an unchanged phone typed locally not sent.\n- #PRNUM — the owner's void of a payment: its «⋯» and dialog, in «الدفعات»'s rows and a subscription's statement.\n",
    ),
])

edit(DOCS / "payments.md", [
    (
        "- **The front desk** ([desk](desk.md)), for the space's owner and reception, at a visit's check-out, and for the owner's void of a payment;",
        "- **The front desk** ([desk](desk.md)), for the space's owner and reception, at a visit's check-out, and for the owner's void of a payment — on the web, from «الدفعات» and from a statement ([desk](desk.md), " + DATE + ", #PRNUM);",
    ),
])
print("docs c2 ok")
