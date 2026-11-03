"""Commit 4's words: `payments.mine` in both catalogues."""
from pathlib import Path

COPY = Path("C:/dev/masaha/app/apps/web/src/shared/copy")

EN = """  /** Reception's own payments of today, for the end-of-shift handover (K4). */
  mine: {
    intro: ({ date }: { date: string }) =>
      `The payments you recorded today, for the end-of-shift handover · ${date}`,
    figures: 'Handover figures',
    cash: 'Cash to hand over',
    transfer: 'Transfer',
    transferHelper: 'Received in the space’s account',
    total: 'Total',
    note: 'A mistake in a payment? The space’s owner voids it, and it shows here struck through.',
    label: 'My payments today',
    columns: { time: 'Time', name: 'Name', item: 'For', method: 'Method', amount: 'Amount' },
    empty: 'You haven’t recorded any payments today',
    loadFailed: 'We couldn’t load your payments',
  },
"""
AR = """  mine: {
    intro: ({ date }: { date: string }) =>
      `الدفعات التي سجّلتها أنت اليوم، لتسليمها في نهاية الوردية · ${date}`,
    figures: 'أرقام التسليم',
    cash: 'نقدًا للتسليم',
    transfer: 'تحويل',
    transferHelper: 'وصلت إلى حساب المساحة',
    total: 'المجموع',
    note: 'خطأ في دفعة؟ يلغيها صاحب المساحة، وتظهر هنا مشطوبة.',
    label: 'دفعاتي اليوم',
    columns: { time: 'الوقت', name: 'الاسم', item: 'عن', method: 'الطريقة', amount: 'المبلغ' },
    empty: 'لم تسجّل أي دفعة اليوم',
    loadFailed: 'تعذّر تحميل دفعاتك',
  },
"""

for name, block, end in (
    ("english/payments.ts", EN, "} as const;\n"),
    ("arabic/payments.ts", AR, "} satisfies Catalogue['payments'];\n"),
):
    path = COPY / name
    text = path.read_text(encoding="utf-8")
    tail = "  },\n" + end
    assert text.endswith(tail), name
    text = text[: -len(end)] + block + end
    path.write_bytes(text.encode("utf-8"))
text = (COPY / "english/payments.ts").read_text(encoding="utf-8")
text = text.replace(
    "/** The space's payments: the owner's ledger (screen 17). */",
    "/** The space's payments (screen 17): the owner's ledger, and reception's «دفعاتي اليوم». */",
)
(COPY / "english/payments.ts").write_bytes(text.encode("utf-8"))
print("copy c4 ok")
